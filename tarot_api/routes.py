import random
import hashlib
from datetime import date
from flask import Blueprint, jsonify, request
from sqlalchemy import func

from .app import db
from .models import Card

api_bp = Blueprint("api", __name__)

# GET /cards?arcana=&suit=&q=&limit=&offset=
@api_bp.get("/cards")
def list_cards():
    q = Card.query

    arcana = request.args.get("arcana")
    if arcana:
        q = q.filter(Card.arcana.ilike(arcana))

    suit = request.args.get("suit")
    if suit:
        q = q.filter(Card.suit.ilike(suit))

    name_q = request.args.get("q")
    if name_q:
        q = q.filter(Card.name.ilike(f"%{name_q}%"))

    # pagination
    try:
        limit = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return jsonify(error="limit/offset must be integers"), 400

    if limit < 1 or offset < 0:
        return jsonify(error="limit must be >=1 and offset >=0"), 400

    items = q.order_by(Card.id).offset(offset).limit(limit).all()
    total = q.with_entities(func.count()).scalar()

    return jsonify({
        "cards": [c.to_dict() for c in items],
        "total": total,
        "limit": limit,
        "offset": offset
    })


# GET /cards/<int:id>
@api_bp.get("/cards/<int:card_id>")
def get_card(card_id: int):
    card = Card.query.get(card_id)
    if not card:
        return jsonify(error="Card not found"), 404
    return jsonify(card.to_dict())


# POST /draw?count=1 — random unique cards
@api_bp.post("/draw")
def draw_cards():
    try:
        count = int(request.args.get("count", 1))
    except ValueError:
        return jsonify(error="count must be an integer"), 400

    if count < 1:
        return jsonify(error="count must be >= 1"), 400

    all_ids = [cid for (cid,) in db.session.query(Card.id).all()]
    if count > len(all_ids):
        return jsonify(error="count exceeds number of available cards"), 400

    picks = random.sample(all_ids, k=count)
    by_id = {c.id: c for c in Card.query.filter(Card.id.in_(picks)).all()}
    ordered = [by_id[i].to_dict() for i in picks]
    return jsonify({"cards": ordered, "count": count})


@api_bp.route("/yesno", methods=["GET"])
def yes_no_maybe():
    all_ids = [cid for (cid,) in db.session.query(Card.id).all()]
    if not all_ids:
        return jsonify(error="no cards available"), 400

    pick = random.choice(all_ids)
    card = Card.query.get(pick)

    # pull yes/no/maybe from your model, with a safe fallback
    yn = getattr(card, "yesNoMaybe", None) or getattr(card, "yes_no_maybe", None)
    answer = (str(yn).lower() if yn is not None else ["yes", "no", "maybe"][card.id % 3])

    return jsonify({
        "answer": answer,
        "card": card.to_dict(),
        "count": 1
    })

# GET /daily?date=YYYY-MM-DD — deterministic card by date
@api_bp.get("/daily")
def daily_card():
    ds = request.args.get("date")
    seed = request.args.get("seed")  # optional personalization seed

    if ds:
      try:
          y, m, d = map(int, ds.split("-"))
          target = date(y, m, d)
      except Exception:
          return jsonify(error="date must be YYYY-MM-DD"), 400
    else:
      target = date.today()

    # make a deterministic integer from (seed + date)
    seed_input = f"{seed or ''}-{target.isoformat()}"
    seed_val = int(hashlib.sha256(seed_input.encode()).hexdigest()[:8], 16)

    ids = [cid for (cid,) in db.session.query(Card.id).order_by(Card.id).all()]
    if not ids:
        return jsonify(error="no cards available"), 400

    rng = random.Random(seed_val)
    pick = rng.choice(ids)
    card = Card.query.get(pick)

    return jsonify({"date": target.isoformat(), "card": card.to_dict()})
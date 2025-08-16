# tarot_api/seed.py
import json
import os
from .app import create_app
from .models import Card, db

HERE = os.path.dirname(__file__)
CARDS_JSON = os.path.join(HERE, "cards.json")


def load_cards():
    """Load tarot cards from cards.json into a list of dicts for bulk insert."""
    with open(CARDS_JSON, "r", encoding="utf-8") as f:
        raw = json.load(f)

    cards = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        if not item.get("id") or not item.get("arcana"):
            continue
        try:
            item_id = int(item["id"])
        except (ValueError, TypeError):
            continue

        cards.append({
            "id": item_id,
            "name": item.get("name"),
            "arcana": item.get("arcana"),
            "suit": item.get("suit"),
            "upright_meaning": item.get("upright_meaning"),
            "reversed_meaning": item.get("reversed_meaning"),
            "yes_no": item.get("yes_no"),
            "image_url": item.get("image_url"),
        })
    return cards


def run_seed(drop=None):
    """
    Seed the database with tarot cards.

    Behaviour:
      - If SEED_DROP=true (or drop=True), drop & recreate tables, then insert all.
      - Otherwise, create tables if missing and insert only missing rows (idempotent).
    """
    if drop is None:
        drop = os.getenv("SEED_DROP", "false").lower() == "true"

    app = create_app()
    with app.app_context():
        if drop:
            db.drop_all()
        db.create_all()

        cards = load_cards()

        if drop:
            # Full reset
            db.session.query(Card).delete(synchronize_session=False)
            db.session.bulk_insert_mappings(Card, cards)
            db.session.commit()
            total = db.session.query(Card).count()
            print(f"✅ Seeded ALL {total} cards (after drop).")
            return

        # Idempotent insert: add only missing IDs
        existing_ids = {cid for (cid,) in db.session.query(Card.id).all()}
        new_rows = [row for row in cards if row["id"] not in existing_ids]

        if new_rows:
            db.session.bulk_insert_mappings(Card, new_rows)
            db.session.commit()

        total = db.session.query(Card).count()
        print(f"Seed complete. Added {len(new_rows)} new cards. Total now {total}.")


if __name__ == "__main__":
    run_seed()

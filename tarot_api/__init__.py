import json, os
from .app import create_app
from .models import Card, db

HERE = os.path.dirname(__file__)
CARDS_JSON = os.path.join(HERE, "cards.json")

def load_cards():
    with open(CARDS_JSON, "r", encoding="utf-8") as f:
        raw = json.load(f)
    rows = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        if not item.get("id") or not item.get("arcana"):
            continue
        try:
            item_id = int(item["id"])
        except Exception:
            continue
        rows.append({
            "id": item_id,
            "name": item.get("name"),
            "arcana": item.get("arcana"),
            "suit": item.get("suit"),
            "upright_meaning": item.get("upright_meaning"),
            "reversed_meaning": item.get("reversed_meaning"),
            "yes_no": item.get("yes_no"),
            "image_url": item.get("image_url"),
        })
    return rows

def run_seed(drop=True):
    app = create_app()
    with app.app_context():
        if drop:
            db.drop_all()
        db.create_all()
        db.session.query(Card).delete()

        cards = load_cards()
        db.session.bulk_insert_mappings(Card, cards)
        db.session.commit()
        print(f"✅ Seeded {len(cards)} cards.")

if __name__ == "__main__":
    run_seed()

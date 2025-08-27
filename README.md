# 🔮 Tarot API

A standalone Flask API serving tarot card data from a Postgres database.  
Supports filtering, single card lookup, random draws, a daily deterministic card, and yes/no/maybe answers.  

Built for integration with **Lunara**, but usable standalone.  

---

## 📂 Project Structure

```plaintext
tarot_api/
  __init__.py       # seed helper (alternate entrypoint)
  app.py            # Flask app setup, CORS, DB config
  models.py         # SQLAlchemy Card model
  routes.py         # API routes (/cards, /draw, /daily, /yesno)
  seed.py           # Seeder script (loads cards.json)
  cards.json        # Full tarot deck (Major + Minor Arcana)
  requirements.txt  # Python dependencies
  .env.example      # Example environment configuration (copy to .env)
```
## ⚙️ Setup

1. **Clone & enter project**
```bash
   git clone <your-repo-url> tarot-api
   cd tarot-api
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. **Environment variables**
Copy .env.example → .env and set:
```js
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/tarot_db
CORS_ORIGIN=http://localhost:5173   # Comma-separated if multiple origins
```

⚠️ Postgres is required. No SQLite fallback.

5. **Create database**
```bash
createdb tarot_db
```

6. **Seed the database**
Fresh reset:
```bash
SEED_DROP=true python -m tarot_api.seed
```

Idempotent insert (only missing cards):
```bash
python -m tarot_api.seed
```

7. **Run the server**
```bash
python -m tarot_api.app
```

Available at:

http://localhost:5001

## Endpoints
**GET /cards**

List cards with optional filters:

- arcana → "Major Arcana" | "Minor Arcana"

- suit → "Cups" | "Swords" | "Pentacles" | "Wands"

- q → search by name (partial match)

- limit, offset → pagination

**GET /cards/<id>**

- Fetch a single card by ID.

**POST /draw?count=1**

- Draw random unique cards.
- Query param:

    - count (integer, default=1)

**GET /daily?date=YYYY-MM-DD&seed=foo**

- Deterministic "Card of the Day."

- date → optional (defaults to today)

- seed → optional personalization string

**GET /yesno**

- Returns a yes/no/maybe answer with a random card.

## 🧪 Example curl commands
 1. **Get first 3 cards**
```bash
 curl -s "http://localhost:5001/cards?limit=3" | jq
```
 2. **Get The Fool (id=1)**
 ```bash
curl -s "http://localhost:5001/cards/1" | jq
```
 3. **Draw 3 random cards**
 ```bash
curl -s -X POST "http://localhost:5001/draw?count=3" | jq
```
 4. **Card of the day (today)**
 ```bash
curl -s "http://localhost:5001/daily" | jq
```bash
 5. **Yes/No/Maybe answer**
 ```bash
curl -s "http://localhost:5001/yesno" | jq
```
##  ⚠️ Error Handling

- 404 → not found (invalid card ID)

- 400 → invalid query params (bad limit/offset, count, or date format)

## 🌐 CORS

- Origins allowed via CORS_ORIGIN env var (comma-separated).
Default:

    - http://localhost:5173

## 🗄️ Database Notes

- Requires Postgres.

- Seeder loads cards.json (78 tarot cards + back).

- Supports full reset or incremental seeding.
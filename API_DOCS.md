# 🔮 Tarot API — Public Documentation

A minimal JSON API for tarot cards. Supports listing/filtering cards, fetching a single card, drawing random unique cards, a deterministic “card of the day,” and a yes/no/maybe endpoint.

- **Base URL (prod):** `https://tarot-api-lnhc.onrender.com`
- **Content type:** `application/json`
- **Auth:** None (public)
- **CORS:** Allowed origins are controlled via `CORS_ORIGIN` env var (comma-separated). Default includes `http://localhost:5173`.

> Replace `<BASE_URL>` in examples with your actual Render domain.

---

## 📦 Card object

```json
{
  "id": 1,
  "name": "The Fool",
  "arcana": "Major Arcana",
  "suit": null,
  "upright_meaning": "New beginnings, optimism, trust in life",
  "reversed_meaning": "Recklessness, taken advantage of, inconsideration",
  "yes_no": "Yes",
  "image_url": "/static/images/major_arcana/fool.jpg"
}
```

1. **GET /cards**

- List cards with optional filters and pagination.

- Query params

- arcana — "Major Arcana" | "Minor Arcana" (case-insensitive)

- suit — "Cups" | "Swords" | "Pentacles" | "Wands" (case-insensitive)

- q — substring match on name

- limit — integer ≥ 1 (default 100)

- offset — integer ≥ 0 (default 0)

- Response (200)
```json
{
  "cards": [ /* array of Card */ ],
  "total": 78,
  "limit": 10,
  "offset": 0
}
```

## Examples

### First 3 cards
```bash
curl -s "<BASE_URL>/cards?limit=3" | jq
```

### Only Major Arcana
```bash
curl -s "<BASE_URL>/cards?arcana=Major%20Arcana&limit=5" | jq
```

### Minor / Cups containing "Queen"
```bash
curl -s "<BASE_URL>/cards?arcana=Minor%20Arcana&suit=Cups&q=Queen" | jq
```

## Errors

- 400 — invalid limit/offset types or values.

2) **GET /cards/{id}**

Fetch a single card by numeric id.

## Examples
```bash
curl -s "<BASE_URL>/cards/1" | jq
```

## Errors

404 — card not found.

3) **POST /draw?count=1**

- Draw random unique cards.

- Query params

- count — integer ≥ 1 (default 1)

- Response (200)

{
  "cards": [ /* array of Card, length=count */ ],
  "count": 3
}


## Examples

### One random card
```bash
curl -s -X POST "<BASE_URL>/draw" | jq
```

### Three random cards
```bash
curl -s -X POST "<BASE_URL>/draw?count=3" | jq
```

## Errors

- 400 — invalid count type/value, or count exceeds deck size.

4) **GET /daily?date=YYYY-MM-DD&seed=optional**

- Deterministic “Card of the Day.”

- If date omitted → uses server’s current date.

- Optional seed lets a client personalize the result (e.g., a username).

- Response (200)
```json
{
  "date": "2025-08-27",
  "card": { /* Card */ }
}
```

## Examples

### Today’s card
```bash
curl -s "<BASE_URL>/daily" | jq
```

### Specific date
```bash
curl -s "<BASE_URL>/daily?date=2025-08-27" | jq
```

### Personalized (stable per seed+date)
```bash
curl -s "<BASE_URL>/daily?seed=ara&date=2025-08-27" | jq
```

## Errors

- 400 — bad date format (must be YYYY-MM-DD).

- 400 — no cards available (empty DB).

5) **GET /yesno**

- Return a yes/no/maybe answer plus a random card.

- Response (200)
```json
{
  "answer": "yes",
  "card": { /* Card */ },
  "count": 1
}
```

## Example
```bash
curl -s "<BASE_URL>/yesno" | jq
```

## Errors

- 400 — no cards available (empty DB).

## HTTP Status Codes

- 200 — success

- 400 — invalid parameters / bad request

- 404 — not found (e.g., card id)

- 500 — unexpected server error

## Rate Limits

- No strict rate limiting is enforced by this API. If hosted on Render free tiers, cold starts and provider-level limits may apply.

## Versioning

- Current: v1 (unversioned paths). If a breaking change is needed later, new routes will use /v2/....

## Changelog

- 2025-08-27 — Public docs created; endpoints: /cards, /cards/{id}, /draw, /daily, /yesno.
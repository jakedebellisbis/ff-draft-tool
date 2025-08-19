# Fantasy Draft Tool — React + FastAPI Starter

Multi-league, snake-draft fantasy football tool with keepers and availability probabilities.

## Features
- **Multi-league** (10-team by default; configurable)
- **Keepers** per league (by overall or Round/Pick) — players excluded from suggestions
- **ADP per league** and **availability** at *your next* and *next-next* pick
- Simple, clean React frontend; FastAPI backend (SQLite DB)

---

## Getting Started

### 1) Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
uvicorn app.main:app --reload
```
In another terminal, seed example data once:
```bash
python -c "from app.seed import run; run()"
```

### 2) Frontend
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

---

## Key API Routes

- `POST /admin/initdb` — create tables
- `GET /leagues` — list leagues
- `GET /leagues/{id}` — league details
- `GET /players?league_id=1` — players joined with per-league ADP and keeper flag
- `GET /keepers?league_id=1` — list keepers
- `POST /keepers` — add/update keeper (body: league_id, player_id, [round, pick_in_round] or overall_pick)
- `POST /availability` — compute P(available) at next and next+1 pick for top N players

---

## Data Model (SQLite)
- **players**: id, name, team, pos, bye, age, proj_points, boom_pct, bust_pct, depth_chart, injury_status
- **leagues**: id, name, teams, rounds, draft_slot, adp_sd
- **adp**: (league_id, player_id) -> adp, source
- **keepers**: unique (league_id, player_id) with overall_pick or round/pick_in_round

---

## Where to Add Your Data
- Upsert leagues: `POST /leagues`
- Insert players (you can extend the API; for now seed file shows how)
- Insert ADP per league (extend with CSV import; example in seed)

---

## Next Up (easy improvements)
- CSV upload endpoints for Players, ADP, Depth Charts
- Draft tracker (mark picks by any team; persist a draft session)
- “Best Pick Now” score blending value + availability + positional scarcity
- Auth + multi-user (JWT) if you want to share
- Postgres + Alembic for prod deployments

Enjoy! 🏈

---

## Templates & Imports — Quick Start

This project ships with CSV templates under **`templates/`** so you can load real data fast.

### Where the templates live
```
ff-draft-tool/
  templates/
    players_template.csv
    adp_template.csv
    espn_analyst_ranks_template.csv
```
Open these in Excel/Google Sheets, replace rows with your data, save as CSV, and POST them to the API as shown below.

### 1) Players
**Purpose:** Create/refresh your master player table (names, teams, pos, projections, boom/bust, depth chart).
**CSV header:**  
`name,team,pos,bye,age,proj_points,boom_pct,bust_pct,depth_chart,injury_status`

**Upload:**
```bash
curl -X POST http://localhost:8000/import/players   -F "file=@templates/players_template.csv"
```

### 2) ADP by Source (Sleeper / ESPN / Yahoo)
**Purpose:** Load platform ADP per league. Do one file **per league per source**.
**CSV header:**  
`name,adp` (overall pick; can be fractional)

**Upload (examples):**
```bash
# Sleeper ADP for league 1
curl -X POST http://localhost:8000/import/adp   -F league_id=1   -F source=Sleeper   -F "file=@templates/adp_template.csv"

# ESPN ADP for league 1
curl -X POST http://localhost:8000/import/adp   -F league_id=1   -F source=ESPN   -F "file=@/path/to/espn_adp.csv"

# Yahoo ADP for league 1
curl -X POST http://localhost:8000/import/adp   -F league_id=1   -F source=Yahoo   -F "file=@/path/to/yahoo_adp.csv"
```

> Tip: You can import multiple sources for the **same** league; the API stores them with the `source` tag.

### 3) ESPN Host / Analyst Ranks
**Purpose:** Store ESPN host ranks (e.g., Berry, Karabell, Yates) for deltas vs. consensus.
**CSV header:**  
`name,analyst,overall_rank,pos_rank`

**Upload:**
```bash
curl -X POST http://localhost:8000/import/espn/analyst_ranks   -F league_id=1   -F "file=@templates/espn_analyst_ranks_template.csv"
```

### Common gotchas
- **Name matching:** `name` must match across all CSVs (Players/ADP/Analysts). Normalize before upload.
- **Multiple leagues:** Repeat ADP uploads per league (change `league_id`).
- **Keepers:** Use `POST /keepers` with either `overall_pick` or (`round`, `pick_in_round`). The UI greys out those picks and excludes the players automatically.

### Next steps
- Add a frontend toggle for ADP source (Sleeper/ESPN/Yahoo/Consensus).
- Add CSV upload forms in the UI so you don’t need curl.
- Create a `/consensus` endpoint to blend sources and apply analyst bumps.

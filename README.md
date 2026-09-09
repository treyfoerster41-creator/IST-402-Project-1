# Expedia Lite — CSV city search

Expedia Lite is a local classroom travel application. Part 1 implements city search over the instructor-supplied hotel and trip CSV files. It uses Vue for the frontend and FastAPI for the Python backend.

## Part 1 scope

- Enter a city and search matching offered stays.
- The Vue frontend requests search results from FastAPI.
- The Python backend reads `hotels.csv` and `trips.csv`, connects them through `hotel_id`, and returns joined stay records.
- Results appear in a plain, labeled table; an empty city and a city with no matches have distinct clear messages.

Booking, history, cancellation, deletion, and SQLite CRUD are intentionally deferred to Part 2.

## Run locally

Use two terminals from the repository root.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

```bash
npm install --prefix frontend
npm run dev --prefix frontend
```

Open [http://localhost:5173](http://localhost:5173). The Vite dev server forwards `/api` requests to FastAPI on port 8000.

## Verify

```bash
.venv/bin/python -m unittest discover -s backend/tests -v
npm run build --prefix frontend
```

Expected examples: `Boston` returns 4 stays (`T001`, `T002`, `T009`, `T010`); `Miami` returns no matching stays.

## Project map

| Path | Purpose |
| --- | --- |
| `frontend/` | Vue/Vite interface and browser-side search state |
| `backend/` | FastAPI routes and CSV-reading/join logic |
| `backend/data/` | supplied CSV records for Parts 1 and 2 |
| `backend/tests/` | backend search behavior checks |
| `docs/` | design note, supplied data guide, and relationship diagram |
| `prompts/` | concise record of material project instructions |
| `handoffs/` | current project state and next task |
| `evidence/` | review and verification evidence |

## Data and attribution

The supplied Expedia Lite classroom pack contains fictional hotel, traveler, trip, and booking records. It is used locally only. Expedia is referenced as an observable travel-search pattern, not as a data source; this project has no connection to Expedia or live booking inventory.

AI assistance: OpenAI Codex assisted with project setup, implementation, and verification. The student reviewed accepted work in VS Code and remains responsible for the submission.

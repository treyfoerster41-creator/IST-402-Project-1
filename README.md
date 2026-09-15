# Expedia Lite - SQLite booking and history

Expedia Lite is a local classroom travel prototype. It uses fictional instructor-supplied hotel, trip, traveler, and booking records. Part 2 adds simulated booking and history CRUD to the Part 1 city search.

## What it does

- Search offered hotel stays by city.
- Select a stay and create a simulated booking for a demo traveler.
- Load saved booking history for a selected demo traveler.
- Cancel a booking while retaining its history record.
- Delete a test booking.
- Persist all application changes in local SQLite across browser refreshes and backend restarts.

There are no live Expedia records, payments, accounts, credentials, or real bookings.

## Run locally

Use two terminals from the repository root.

    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install -r backend/requirements.txt
    uvicorn backend.app.main:app --reload --port 8000

    npm install --prefix frontend
    npm run dev --prefix frontend

Open http://localhost:5173. The Vite server forwards API requests to FastAPI on port 8000.

## SQLite and supplied data

On the first backend start, FastAPI creates backend/data/expedia_lite.db, creates SQLite tables, imports all four supplied CSVs once, and writes a seed marker. Later starts use the existing SQLite data only, so new bookings, cancellations, and deletions persist without duplicated or restored starter rows.

The database file is intentionally ignored by Git because it is local runtime state. To return to fresh supplied sample data during local development, stop the backend, delete only backend/data/expedia_lite.db, and start the backend again.

## Verify

    .venv/bin/python -m unittest discover -s backend/tests -v
    npm run build --prefix frontend

The backend suite checks city search, seeded and empty history, create, cancel, delete, and one-time seed behavior. In the browser, exercise a created booking through history, cancel it, delete a test booking, refresh, and restart the backend to verify persistence.

## Project map

| Path | Purpose |
| --- | --- |
| frontend | Vue/Vite search, booking, and history interface |
| backend/app/database.py | SQLite schema, one-time CSV seed, and data operations |
| backend/app/main.py | FastAPI search, booking, history, cancel, and delete routes |
| backend/data | supplied source CSV files and ignored local SQLite runtime file |
| backend/tests | backend behavior and persistence checks |
| docs | design note and supplied data guide |
| prompts | concise record of material project instructions |
| handoffs | current state and next task |
| evidence | review and verification evidence |

## Data and attribution

The supplied Expedia Lite classroom pack contains fictional hotel, traveler, trip, and booking records. Expedia is a reference pattern only; this project has no connection to Expedia or live booking inventory.

AI assistance: OpenAI Codex (GPT-5) assisted with implementation, documentation, and verification. The student reviews accepted work in VS Code and remains responsible for the submission.

# Expedia Lite - hotel discovery and classroom travel prototype

Expedia Lite is a local classroom travel prototype. Assignment 2 Part 1 adds live hotel-place discovery near a U.S. ZIP code. The October 1 in-class activity adds separate local storage for selected API hotels and fictional nightly values. The earlier city search and simulated booking/history section remains based only on fictional instructor-supplied records. Live Geoapify places are not bookable offers and are never inserted into the fictional booking tables.

## What it does

- Resolve an exact five-digit U.S. ZIP through FastAPI and Geoapify, then request up to 50 `accommodation.hotel` places inside a 5 km circle around the returned point.
- Show returned places in a synchronized Vue list and Leaflet map; selecting either highlights the same place. Distinguish invalid input, unresolved ZIP, no results, and service failure.
- Search the local saved-hotel database first. If it has hotels for the ZIP, show that saved subset and its simulated dated rates/room counts; otherwise fall back to the live Part 1 search. Save or remove API places through the frontend.
- Search offered hotel stays by city.
- Select a stay and create a simulated booking for a demo traveler.
- Load saved booking history for a selected demo traveler.
- Cancel a booking while retaining its history record.
- Delete a test booking.
- Persist all application changes in local SQLite across browser refreshes and backend restarts.
- Look up a U.S. ZIP location through FastAPI and real Geoapify data, with an input and labeled results table.

There are no live Expedia records, payments, traveler accounts, or real bookings. The backend uses one private Geoapify credential for location and hotel-place queries. Leaflet uses public OpenStreetMap tiles with no browser-visible key.

## Run locally

Use two terminals from the repository root.

    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install -r backend/requirements.txt
    uvicorn backend.app.main:app --reload --port 8000

    npm ci --prefix frontend
    npm run dev --prefix frontend

Open http://localhost:5173 (or http://127.0.0.1:5173 in Firefox). The Vite server forwards API requests to FastAPI on port 8000.

## Configure the public API activity

The existing root `.env` sits beside `README.md`, `frontend/`, and `backend/`.
If it is missing, copy the key-free `.env.example` to `.env`, then privately set
`GEOAPIFY_API_KEY` there. Preserve an existing key. Never paste it into Vue, a
`VITE_` variable, screenshots, reports, prompts, or Git. Dotfiles may be hidden
in Finder; use Command+Shift+Period to show them.

The backend loads this exact file using a path derived from `backend/app/config.py`,
not the shell's working directory. An existing process environment value takes
precedence. Restart the backend after any `.env` edit; Vite alone is not enough.
The approved `python-dotenv==1.2.3` and existing HTTPX are declared in requirements.

- Health: http://127.0.0.1:8000/api/health reports `status` and whether the key is configured, never its value.
- Original direct demo: http://127.0.0.1:8000/api/demo/zip-location resolves ZIP 16802.
- Entered ZIP: http://127.0.0.1:8000/api/zip-location?zip_code=02108 demonstrates leading-zero handling.
- In Vue, use the ZIP panel's fixed demonstration button or enter five digits and select **Look up ZIP**.

Configuration presence is not proof of a valid key. A successful live request
returns a matching U.S. ZIP, optional locality, country, latitude, and longitude.
Invalid input, unresolved ZIP, missing key, timeout, and provider errors get useful
feedback. ZIP lookups neither change the booking database nor retrieve hotels.
The earlier ZIP-only activity intentionally excluded a map, live hotel retrieval, and a shortlist; its panel remains available below Assignment 2's new discovery section.
See [ZIP design/research](docs/zip-lookup-design.md) and [activity evidence](evidence/zip-lookup/verification.md).

## Assignment 2, Part 1 - live hotel discovery

At the top of the page, enter a five-digit ZIP (try `16802` or leading-zero `02108`) and select **Find nearby hotels**. Vue first requests `GET /api/hotels/saved?zip_code=...` through the Vite proxy. When that local request succeeds with no matching hotels, Vue calls the existing `GET /api/hotels/nearby?zip_code=...` endpoint. A failed local request shows an error and does not silently fall back. For the live search, FastAPI first verifies an exact U.S. postcode match, then uses the returned latitude/longitude as the center of a Geoapify Places `accommodation.hotel` search filtered to a 5 km circle. The backend returns only place ID, optional name/address, and valid coordinates. A feature without a provider ID or valid point is omitted. A malformed provider response is an error, not an empty successful search.

The result limit is 50, so a dense-area list may stop at that cap and is **not exhaustive**. Select a place in the list or click/keyboard-activate its numbered map marker; the corresponding place is highlighted in both. A missing name or address is labeled, not invented. No prices, ratings, availability, room offers, or booking confirmations are inferred from this API. The old fictional booking interface remains separate below the ZIP-only demonstration.

OpenStreetMap map tiles load only for the interactive viewport, with visible on-map attribution. They require an internet connection but no tile credential. The backend Geoapify key never enters `frontend/` or browser API calls. The October 1 activity's saved-hotel subset is not a completed Assignment 2 Part 2 shortlist workflow.

See the [research and design decisions](docs/assignment-2-part-1-research.md), [early mockup](docs/assignment-2-part-1-mockup.svg), and [Part 1 verification](evidence/assignment-2-part-1-verification.md).

## October 1 in-class activity - local hotel storage

On API results, **Add to Local** saves the provider place ID, optional name/address, coordinates, and the searched ZIP/center in `backend/data/expedia_lite.db`. It creates five fictional nightly rows for October 10-14, 2026. Each starts at `nightly_rate_cents = 10000` ($100.00) and `rooms_available = 20`. Repeated saves leave existing nights and manual edits unchanged. A saved place has Add disabled and **Remove from Local** available; removal also deletes its ZIP associations and nightly rows, while leaving unrelated hotels alone.

Repeat the ZIP search to see **Saved locally** and current database values. This list is only the saved subset. A ZIP without saved matches shows **API results** after the live search. Live API places have no verified price or availability; the displayed local figures are simulated classroom data, not bookable offers. The original fictional booking section remains separate.

To inspect or edit the database with DB Browser for SQLite, open this exact file: `backend/data/expedia_lite.db`. In **Browse Data**, select `demo_hotel_nights`, change a saved hotel's `nightly_rate_cents` and `rooms_available` for one `stay_date`, then click **Write Changes**. Search the same ZIP again and compare that same hotel/date in the frontend. Do not delete or recreate the database to reset this activity. The [activity evidence and manual checklist](evidence/local-hotel-activity.md) records what has been checked and what still needs a student browser/DB Browser demonstration.

## SQLite and supplied data

On the first backend start, FastAPI creates backend/data/expedia_lite.db, creates SQLite tables, imports all four supplied CSVs once, and writes a seed marker. Later starts use the existing SQLite data only, so new bookings, cancellations, and deletions persist without duplicated or restored starter rows.

The database file is intentionally ignored by Git because it is local runtime state. Preserve it during this activity: deleting it would erase saved hotels, manual nightly edits, and prior booking changes.

## Verify

    .venv/bin/python -m unittest discover -s backend/tests -v
    npm run build --prefix frontend

The backend suite checks city search, seeded and empty history, create, cancel, delete, one-time seed behavior, ZIP validation, hotel Places response/error handling, and saved-hotel schema/idempotence/cascade behavior. Provider tests use synthetic fixtures and mocks rather than spending API quota. For live checks, search 16802, select a list item then a map marker, try 02108, invalid `1680`, and unresolved `00000`; live result counts may change. For local-storage checks, use Add, refresh/re-search, inspect the Network panel and SQLite rows, edit and **Write Changes** in DB Browser, then re-search. The existing booking flow can still be checked with temporary demo bookings only. Never restore or remove existing local records just to test.

## Project map

| Path | Purpose |
| --- | --- |
| frontend | Vue/Vite search, booking, and history interface |
| frontend/src/components/HotelDiscovery.vue | ZIP input, local-first/live states, Add/Remove, dated values, result list, and shared selection |
| frontend/src/components/HotelMap.vue | Leaflet map, returned-place markers, ZIP point, search circle, and tile attribution |
| backend/app/hotel_discovery.py | Geoapify Places query and allowlisted hotel response |
| backend/app/saved_hotels.py | Saved hotel validation, ZIP association, dated rows, local reads and delete |
| backend/app/database.py | SQLite schema, one-time CSV seed, and data operations |
| backend/app/main.py | FastAPI live hotel, ZIP, search, booking, history, cancel, and delete routes |
| backend/app/config.py | Explicit project-root .env loading and safe configuration status |
| backend/app/geoapify.py | Backend-only ZIP validation, provider request, and sanitized location response |
| frontend/src/components/ZipLookup.vue | ZIP entry, fixed demonstration, loading/errors, health status, and results table |
| backend/data | supplied source CSV files and ignored local SQLite runtime file |
| backend/tests | backend behavior and persistence checks |
| docs | design note and supplied data guide |
| prompts | concise record of material project instructions |
| handoffs | current state and next task |
| evidence | review and verification evidence |

## Data and attribution

The supplied Expedia Lite classroom pack contains fictional hotel, traveler, trip, and booking records. Expedia is a reference pattern only; this project has no connection to Expedia or live booking inventory.

ZIP location data is provided by [Geoapify](https://www.geoapify.com/), with
[OpenStreetMap contributors](https://www.openstreetmap.org/copyright) and
[other credited data sources](https://www.geoapify.com/credits/). Provider data is
separate from the fictional hotel records.

AI assistance: OpenAI Codex (GPT-5) assisted with implementation, documentation, and verification. The student reviews accepted work in VS Code and remains responsible for the submission.

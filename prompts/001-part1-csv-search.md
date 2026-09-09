# 001 — Part 1 CSV search scope

## Course requirements applied

- Use Vue in `frontend/`, Python/FastAPI in `backend/`, and supplied CSV data.
- Search by city and return hotel stays joined from `hotels.csv` and `trips.csv` through `hotel_id`.
- Show a plain table with labels for matches and a clear no-results state.
- Record manual review and browser checks, commit the reviewed work, and upload a single Markdown `report.md`.

## Project decisions

- Application name: Expedia Lite.
- Part 1 contains search only; booking/history/SQLite CRUD are reserved for Part 2.
- The backend reads CSVs with `utf-8-sig` and compares city names case-insensitively.


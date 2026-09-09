# Project instructions — Expedia Lite

## Part 1 goal

Build only the CSV city-search scope: a Vue frontend calls a FastAPI backend, which reads `hotels.csv` and `trips.csv`, joins them by `hotel_id`, and returns matching offered stays. Use the supplied fictional classroom records only.

## Architecture

- `frontend/` owns the city input, Search button, loading/no-result/input-error messages, and plain results table.
- `backend/` owns CSV reading, the `hotel_id` join, case-insensitive city matching, nights/price calculation, and API responses.
- The frontend must request `/api/stays`; it must not read CSV files directly.
- Part 1 does not implement booking, history, cancellation, deletion, SQLite storage, login, payments, or live inventory.

## CSV rules

- Read supplied CSV files with `utf-8-sig` encoding.
- Preserve existing identifiers and treat them as text.
- Keep all supplied CSVs in `backend/data/` for Part 2 seeding.
- Keep `hotels.csv` and `trips.csv` source-controlled. Do not edit their records.

## Verification and Git

- Before committing, manually review changed files in VS Code and run the backend tests and frontend production build.
- In a browser, check `Boston` (four results) and `Miami` (no results). Record expected and observed behavior in `evidence/evidence-log.md`.
- Keep README, `docs/design.md`, prompts, and `handoffs/current.md` consistent with what actually works.
- Part 1 ends with a reviewed Git commit pushed to GitHub. Part 2 work will use a feature branch and preserve this checkpoint.


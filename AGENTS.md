# Project instructions - Expedia Lite

## Part 2 goal

Build a local classroom travel prototype with city search, simulated booking, and booking history. Use supplied fictional records only. Do not add live inventory, authentication, payments, or real traveler data.

## Architecture

- frontend owns Vue rendering, selection and form state, loading states, and API error messages.
- backend owns FastAPI routes, SQLite initialization, one-time CSV seeding, validation, booking IDs, and all application reads and writes.
- The frontend requests API routes only; it never accesses CSV files or SQLite directly.
- After the first seed, all application reads and writes use SQLite. CSV files remain source records only.

## Required Part 2 behavior

- Search stays by city through the frontend.
- Create a simulated booking from a selected offered stay and demo traveler.
- Read that booking in the selected traveler's history.
- Cancel a booking by updating its status while keeping it in history.
- Delete a test booking through the frontend.
- Keep create, update, and delete results after browser refresh and server restart without re-importing starter records.

## Data rules

- Read supplied CSVs with utf-8-sig only during first-time seed.
- Preserve supplied identifiers and create new unique B### booking IDs.
- Keep CSV source files in backend/data unchanged and source-controlled.
- Keep the local SQLite database ignored; it is created at backend/data/expedia_lite.db.

## Verification and Git

- Before committing, manually review changed files in VS Code and run backend tests plus the frontend production build.
- Exercise search, create, read, cancel, delete, empty history, browser refresh, and server restart in the browser. Record expected and observed behavior in evidence/evidence-log.md.
- Keep README, design, prompts, handoff, evidence, and report consistent with what actually works.
- Develop Part 2 work on feature/booking-history, then merge reviewed work into main, verify the combined application, and push it. Preserve the Part 1 checkpoint.

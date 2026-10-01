# Project instructions - Expedia Lite

## Part 2 goal

Build a local classroom travel prototype with city search, simulated booking, and booking history. Use supplied fictional records only. Do not add live inventory, authentication, payments, or real traveler data.

## Architecture

- frontend owns Vue rendering, selection and form state, loading states, and API error messages.
- backend owns FastAPI routes, SQLite initialization, one-time CSV seeding, validation, booking IDs, and all application reads and writes.
- The frontend requests API routes only; it never accesses CSV files or SQLite directly.
- After the first seed, all booking/search data reads and writes use SQLite. CSV files remain source records only. The separate public ZIP activity reads geographic locations through Geoapify, not SQLite.

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

## Public API activity (September 2026)

- Complete the fixed ZIP 16802 milestone and entered five-digit ZIP lookup/table in this same app, on codex/geoapify-zip-activity.
- Keep the backend key in the ignored project-root .env. Do not print it, log provider request URLs, return raw upstream errors, or add VITE_ credentials.
- Preserve leading zeros, require an exact U.S. postcode match and finite coordinates, use a finite HTTP timeout, and distinguish unresolved ZIP from provider failure.
- Keep the Vue panel separate from booking state. No live hotels, map, or shortlist in this graded activity.
- Use mocked provider tests for failures. Record real browser/backend 16802 checks separately; mocks do not prove live success.
- Preserve existing local database records and deletions. Never reseed just to make test evidence look cleaner.
- Preserve the completed Assignment 1 report at docs/assignment-1-report-archive.md. `report.md` is for the current assignment submission; Assignment 2 Part 1 requires its own report and an accessible demo-video link. The earlier ZIP activity's screenshot/video and key-status instructions applied to that activity only.
- Do not claim student VS Code review, class demonstration, Canvas upload, commit, or push until each actually occurs.

## Assignment 2, Part 1 - live hotel discovery

- Continue in the same Vue/FastAPI/SQLite project. Live hotel discovery is separate from fictional booking data; it does not create bookings or imply room availability.
- MVC split: Vue owns ZIP input, loading/error/empty/results states, selected hotel ID, list/map rendering, and accessible controls. FastAPI owns exact ZIP validation, Geoapify geocoding and Places requests, response shaping, and sanitized failures. SQLite remains the model for the existing fictional bookings; Part 1 does not store live places.
- Resolve the requested five-digit U.S. postcode exactly (preserving leading zeros), then center a `accommodation.hotel` Places search on that returned point with a 5 km circle. Do not fall back to the user's current position or a broader ZIP boundary.
- Present only fields supplied by Geoapify. Use honest missing-field labels. Do not add invented price, rating, availability, or booking controls to live places. Disclose the result cap; do not call the list exhaustive.
- Keep `GEOAPIFY_API_KEY` in the ignored root `.env` and backend only. Leaflet uses public OpenStreetMap tiles with visible attribution and no client credential or tile prefetch.
- Dependency loop: CHECK the existing environment; before adding any new dependency, explain the exact installation and receive the student's approval; then TAKE ACTION and VERIFY the installed package/build. Leaflet 1.9.4 was approved on 2026-09-28.
- Verification loop: run mocked backend tests and the frontend build, then manually exercise live 16802 and a leading-zero ZIP, list-to-map and map-to-list selection, invalid and unresolved input, and any available failure/empty simulations. Record expected versus observed results and dates. Do not claim student review, class demo, video link, commit, or push until confirmed.
- Preserve the local SQLite database and prior assignment evidence. Part 2 will add a separate persistent shortlist; do not claim it exists in Part 1.

## October 1 in-class activity - local hotel storage

- Continue on `assignment2_part2_in_class` for this activity. The existing Part 1 Geoapify endpoint and list/map behavior remain intact. The saved-hotel subset is not a claim that the full Assignment 2 Part 2 shortlist is finished.
- `saved_hotels` stores provider ID and available place fields, `saved_hotel_zips` stores the searched ZIP/center association, and `demo_hotel_nights` stores five fictional October 10-14, 2026 rows. Preserve the original Assignment 1 tables and local data. Keep the SQLite file ignored and do not reseed it to make screenshots look cleaner.
- Vue searches local storage first. Only a successful empty local lookup falls back to the existing Part 1 hotel endpoint. A local error is a failure. Add is disabled for a saved provider ID; Remove is offered only for saved IDs. Repeated saves do not overwrite manually edited nightly rows.
- The student must manually inspect schema and rows in DB Browser for SQLite, inspect the browser Network panel, and personally use **Write Changes** for one night before re-searching. Agent-run API/SQL checks and automated tests are separate evidence and must not be described as student manual observations.
- Before committing, obtain student VS Code review and browser acceptance, run backend tests and frontend build, and update the activity evidence/handoff with actual results. Keep `report.md` as the first-person Assignment 2 Part 1 report unless the student explicitly asks to repurpose it.

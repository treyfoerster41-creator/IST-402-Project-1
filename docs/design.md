# Expedia Lite Part 2 design

## Responsibilities

| Layer | Responsibility |
| --- | --- |
| Vue interface | Collects city and demo-traveler selections, renders search results, lets the user select a stay, and displays booking/history outcomes and safe errors. |
| FastAPI logic | Validates requests, provides search and history data, creates unique booking IDs, updates cancellation status, and deletes a selected test booking. |
| SQLite persistence | Holds hotels, trips, users, bookings, and a one-time seed marker. It is the source for all booking/search reads and writes after seeding. |
| CSV source data | Supplies initial fictional hotels, trips, users, and bookings only. Files are read with utf-8-sig during the first SQLite seed and are not changed by the application. |

## Connected flows

Search: Vue city input -> GET API stays -> FastAPI SQLite hotel/trip join -> labeled results or no-results message -> selected stay and demo traveler -> POST API bookings -> FastAPI creates B### booking -> SQLite saves a confirmed booking -> Vue history.

History: Vue traveler selection -> GET API bookings -> FastAPI SQLite booking join -> labeled history or empty-history message. Cancel sends PATCH to update the row to cancelled; delete sends DELETE to remove the selected test booking.

## Decisions and states

- City matching ignores capitalization and surrounding whitespace. A blank city receives input guidance; a valid city with no matching stay receives a no-results message.
- The user chooses from supplied demo travelers. This is not login or authentication.
- The backend assigns new B### IDs. The frontend does not invent booking IDs, totals, or status.
- Cancel updates status to cancelled and keeps a history row. Delete removes the chosen test booking row. These are intentionally distinct actions.
- A one-time csv_seed_v1 marker prevents startup from restoring deleted starter records, overwriting cancellations, or duplicating rows.
- SQLite persists across browser refreshes and server restarts. Preserve the ignored local database during Assignment 2; removing it would erase the student's saved hotels and manual night edits.

## Part 1 continuity

Part 1 city search remains available, and its implementation checkpoint is dc413fd. Part 2 replaces Part 1 CSV-at-request-time reads with SQLite-backed application queries after the one-time seed.

## Public API activity extension

The separate [ZIP lookup design](zip-lookup-design.md) documents the September
activity, early panel sketch, sources, API boundary, and error states. Geographic
lookup uses Geoapify through FastAPI without modifying the SQLite booking flow.

## Assignment 2 continuity and local hotel advisor

The [Part 1 research](assignment-2-part-1-research.md) and [early list/map mockup](assignment-2-part-1-mockup.svg) guide the exact-ZIP Geoapify search, capped Places list, and synchronized Leaflet map. Vue owns input/selection/states; FastAPI owns validation and external calls. The October 1 additive SQLite tables store saved provider hotels, searched ZIP context, and five simulated dated nightly rows. Local-first lookup returns that saved subset or falls back to the live API only after a successful empty local result. It does not change the fictional Assignment 1 bookings.

The revised Part 2 [research](assignment-2-part-2-research.md) and [early chatbot mockup](assignment-2-part-2-mockup.svg) add a separate question area after the map. Its sequence is: Vue question -> FastAPI sends local schema/rules and question to Gemini -> Gemini proposes SQL -> FastAPI validates a single bounded read-only SELECT over saved hotel/ZIP/night tables -> SQLite returns checked rows -> FastAPI computes whole-stay coverage, total cents, and minimum rooms -> FastAPI sends original question and checked evidence to Gemini -> Vue shows a grounded answer, checked table, accepted SQL, and retrieved rows. Gemini never receives database credentials or connects to SQLite; it receives only the limited rows included in the second prompt.

The SQL policy uses a read-only SQLite connection, query-only pragma, table/function authorizer, output cap, progress limit, and source-row value check. Invalid SQL is rejected without fallback to unchecked execution. For a dated stay, checkout is excluded; missing/zero-room nights are not described as available. Vue distinguishes pending, answered, no-match, insufficient-data, and failed requests. Gemini and Geoapify keys remain in the ignored backend `.env`. The advisor is a classroom decision aid over saved simulated data, not a live hotel booking flow.

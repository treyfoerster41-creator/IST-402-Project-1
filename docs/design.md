# Expedia Lite Part 2 design

## Responsibilities

| Layer | Responsibility |
| --- | --- |
| Vue interface | Collects city and demo-traveler selections, renders search results, lets the user select a stay, and displays booking/history outcomes and safe errors. |
| FastAPI logic | Validates requests, provides search and history data, creates unique booking IDs, updates cancellation status, and deletes a selected test booking. |
| SQLite persistence | Holds hotels, trips, users, bookings, and a one-time seed marker. It is the source for all application reads and writes after seeding. |
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
- SQLite persists across browser refreshes and server restarts. The ignored local database can be removed manually only to restart with fresh supplied data.

## Part 1 continuity

Part 1 city search remains available, and its implementation checkpoint is dc413fd. Part 2 replaces Part 1 CSV-at-request-time reads with SQLite-backed application queries after the one-time seed.

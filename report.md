# Expedia Lite - Part 2

## Repository and checkpoints

Repository: [treyfoerster41-creator/IST-402-Project-1](https://github.com/treyfoerster41-creator/IST-402-Project-1)

Preserved Part 1 implementation checkpoint: [dc413fd](https://github.com/treyfoerster41-creator/IST-402-Project-1/commit/dc413fdca0d0ba11ea1fbfe8405c57541004a7e6)

Part 2 was developed on feature/booking-history. The final main checkpoint will be recorded after student review, merge, combined-app check, and push.

## Implementation

Expedia Lite now provides connected search, simulated booking, and booking-history flows. The Vue frontend searches fictional offered stays by city, lets the user select a stay and demo traveler, creates a simulated booking, and displays saved history. History includes cancellation that retains a row and deletion of a test booking.

The FastAPI backend owns validation, booking creation, unique B### ID generation, cancellation, deletion, and API responses. The SQLite module creates the schema and seeds hotels, trips, users, and bookings from supplied CSV files only once. A seed marker prevents future starts from duplicating records, restoring a deleted booking, or overwriting a cancellation. All application reads and writes after the first seed use SQLite.

Runtime state is stored in the local Git-ignored backend/data/expedia_lite.db file. Changes persist through browser refresh and backend restart. The application uses fictional classroom records only; it does not collect payment data, connect to live Expedia inventory, or implement accounts.

## Verification

Automated checks passed:

- Seven FastAPI backend tests cover city search, seeded and empty history, create, cancel, delete, and no-reseed persistence.
- The Vue production build completed successfully.

Browser checks against the local Vue and FastAPI servers:

| Action | Expected result | Observed result |
| --- | --- | --- |
| Search Boston | Four offered stays including T001, T002, T009, and T010 | Four labeled offers appeared. |
| Create booking | Selected T001 and U006 produce unique confirmed booking | B007 was created and appeared in U006 history. |
| Cancel booking | Status changes while row remains in history | B007 changed to cancelled and remained visible. |
| Refresh and restart | Saved cancellation remains without duplicate starter rows | B007 remained cancelled after browser refresh and FastAPI restart. |
| Delete test booking | Selected test booking is removed | B007 was deleted through the frontend. |
| Restart after delete | Deleted record is not restored by seeding | U006 displayed clear empty-history message after a new FastAPI start. |

The student manually scanned the changed Part 2 files in VS Code and accepted the work before the feature commit and merge. The complete dated record, decisions, browser checks, and AI role disclosure are in [the evidence log](evidence/evidence-log.md).

## Project context

- [Setup and run instructions](README.md)
- [Project-specific instructions](AGENTS.md)
- [Part 2 design note](docs/design.md)
- [Part 1 prompt record](prompts/001-part1-csv-search.md)
- [Part 2 prompt record](prompts/002-part2-sqlite-crud.md)
- [Current handoff](handoffs/current.md)
- [Supplied data guide](docs/sample-data-guide.md)

The handoff records the fresh-session continuation used before Part 2 implementation. After the final main checkpoint is recorded, this report is the single file to upload to Part 2 Canvas.

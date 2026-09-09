# Expedia Lite - Part 1

## Repository and commit

Repository: [treyfoerster41-creator/IST-402-Project-1](https://github.com/treyfoerster41-creator/IST-402-Project-1)

Part 1 implementation checkpoint: [`dc413fd`](https://github.com/treyfoerster41-creator/IST-402-Project-1/commit/dc413fdca0d0ba11ea1fbfe8405c57541004a7e6)

## Implementation

Expedia Lite implements the required Part 1 city-search flow. The Vue frontend in [`frontend/`](frontend/) provides a city input, Search button, clear input/no-result messages, and a plain labeled table. It requests `GET /api/stays?city=...` from the FastAPI backend.

The Python/FastAPI backend in [`backend/`](backend/) reads the supplied `hotels.csv` and `trips.csv` files with UTF-8 BOM handling, joins each trip to its hotel through `hotel_id`, compares city names case-insensitively, and calculates nights and estimated stay price. Part 1 reads CSV data only. Booking, history, SQLite persistence, cancellation, and deletion are reserved for Part 2.

## Verification

The student manually scanned the Part 1 changes in VS Code and accepted the checkpoint commit.

Automated checks passed:

- Three backend tests verify Boston's expected IDs, Miami's empty result, and blank-city feedback.
- The Vue production build completed successfully.

Browser checks were performed against the local Vue and FastAPI servers:

| Action | Expected result | Observed result |
| --- | --- | --- |
| Search `Boston` | Four joined stays: `T001`, `T002`, `T009`, `T010` | Four labeled rows appeared with the expected trip IDs, hotels, dates, nights, and stay prices. |
| Search `Miami` | No matching rows and clear feedback | The table cleared and displayed "No offered stays match 'Miami.' Try another city." |

The complete dated verification record, including the required SQLite capability check and the dependency correction, is in [the evidence log](evidence/evidence-log.md).

## Project context and next steps

- [Setup and run instructions](README.md)
- [Project-specific agent instructions](AGENTS.md)
- [Part 1 design note](docs/design.md)
- [Selected Part 1 prompt record](prompts/001-part1-csv-search.md)
- [Current handoff](handoffs/current.md)
- [Supplied sample-data guide](docs/sample-data-guide.md)

The Part 1 limitation is intentional: the application has no booking CRUD or SQLite application storage yet. The next task is Part 2: seed SQLite once from the supplied CSVs, then implement booking create/read/cancel/delete actions through the Vue frontend and FastAPI backend without reloading or duplicating the starter records.

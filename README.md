# Stayfinder — local hotel booking prototype

Stayfinder is a deliberately small, local hotel-booking prototype inspired by the observable hotel-search flow on [Expedia Hotels](https://www.expedia.com/Hotels). It uses only synthetic hotels, travelers, prices, and booking records. It does not contact Expedia, process payment, or create real reservations.

## Assignment status

Part 1 is preserved on `main`. The working Part 2 implementation is complete and browser-verified on `feature/booking-history`, pending final student review, commit, merge, and GitHub push. See [the current handoff](handoffs/current.md) for the authoritative status.

## Intended user flows

1. **Make a booking:** enter a destination and dates, view matching synthetic hotel cards, select a hotel, provide a traveler name and email, and receive a simulated confirmation.
2. **Review booking history:** open the history view, see an empty-state explanation before any booking exists, and inspect bookings created through the first flow.

Bookings are created through the backend API and written to a local JSON file. They remain visible after a browser refresh and after a normal server restart; resetting `server/data/bookings.json` to `[]` clears the prototype history.

## Technology choices

| Concern | Choice | Why |
| --- | --- | --- |
| Frontend | React with Vite | A compact component-based interface with fast local development. |
| Backend | Node.js with Express | A small, explicit HTTP API that keeps booking rules off the client. |
| Communication | JSON over REST-style HTTP | Easy to inspect in the browser network panel and explain at the assignment’s level. |
| Storage | Server-owned JSON file | Makes persistence visible and avoids database setup for a small synthetic prototype. |
| Testing / verification | Node tests, production build, and browser walkthrough | Matches the assignment’s expectation of manual review and browser verification. |

## Run locally

Prerequisite: Node.js 22 or later.

```bash
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). The Vite client runs on port 5173 and proxies `/api` requests to the Express server on port 3001.

Useful checks:

```bash
npm run test
npm run build
```

`npm run test` runs three booking-validation tests and two API/persistence tests. The API tests reset the synthetic booking store to an empty array after they finish.

## API behavior

| Route | Result |
| --- | --- |
| `GET /api/properties?destination=Asheville` | Returns the three synthetic Asheville stays. Other destinations return an empty list. |
| `POST /api/bookings` | Server validates details, calculates nights and total, creates a confirmation code, and persists a booking. Invalid requests return a safe error and field details. |
| `GET /api/bookings` | Returns saved bookings newest first for the history view. |

## Repository map

| Path | Purpose | Current state |
| --- | --- | --- |
| `design/` | decomposition, flow diagrams, reference observations, and design decisions | updated for implementation |
| `client/` | React/Vite frontend | complete on the feature branch |
| `server/` | Express API, validation, and local booking storage | complete on the feature branch |
| `server/data/bookings.json` | server-owned persisted booking records | empty initial state; changes at runtime |
| `server/test/` | validation and API/persistence checks | complete |
| `handoffs/` | truthful continuation notes | current |
| `prompts/` | ordered, concise record of material project instructions | current |
| `evidence/` | evidence log for instructions, decisions, reviews, and verification | current |
| `AGENTS.md` | repository-specific working instructions | current |

## Design and evidence

- [Application design and flow diagrams](design/application-design.md)
- [Expedia reference observations and interface sketch](design/reference-observations.md)
- [Current handoff](handoffs/current.md)
- [Evidence log](evidence/evidence-log.md)
- [Part 1 project brief record](prompts/001-assignment-brief.md)
- [Implementation record](prompts/002-implementation.md)

## Attribution and disclosure

The observable reference is [Expedia Hotels](https://www.expedia.com/Hotels), accessed September 8, 2026. Expedia is used only as a product-behavior reference. This project will use original interface code and synthetic records, and it will not reuse Expedia’s branding, imagery, screenshots, or listing data.

AI assistance: OpenAI Codex was used to help organize the Part 1 documentation, research publicly observable interface patterns, and will be disclosed in the evidence log with the work actually accepted and checked by the student. The student remains responsible for review, testing, commits, and the final submission.

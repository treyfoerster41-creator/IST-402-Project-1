# Stayfinder — local hotel booking prototype

Stayfinder is a deliberately small, local hotel-booking prototype inspired by the observable hotel-search flow on [Expedia Hotels](https://www.expedia.com/Hotels). It uses only synthetic hotels, travelers, prices, and booking records. It does not contact Expedia, process payment, or create real reservations.

## Assignment status

This repository is at the **Part 1 planning checkpoint**. The design, intended structure, and implementation handoff are complete; the React client and Express server are planned but not yet implemented. See [the current handoff](handoffs/current.md) for the authoritative status.

## Intended user flows

1. **Make a booking:** enter a destination and dates, view matching synthetic hotel cards, select a hotel, provide a traveler name and email, and receive a simulated confirmation.
2. **Review booking history:** open the history view, see an empty-state explanation before any booking exists, and inspect bookings created through the first flow.

Bookings will be created through the backend API and written to a local JSON file. They will remain visible after a browser refresh and after a normal server restart; deleting the local data file resets the prototype.

## Intended technology choices

| Concern | Choice | Why |
| --- | --- | --- |
| Frontend | React with Vite | A compact component-based interface with fast local development. |
| Backend | Node.js with Express | A small, explicit HTTP API that keeps booking rules off the client. |
| Communication | JSON over REST-style HTTP | Easy to inspect in the browser network panel and explain at the assignment’s level. |
| Storage | Server-owned JSON file | Makes persistence visible and avoids database setup for a small synthetic prototype. |
| Testing / verification | Browser walkthrough plus API/manual checks | Matches the assignment’s expectation of manual review and browser verification. |

Implementation dependencies have not been installed yet. Setup and run commands will be added and tested during Part 2.

## Repository map

| Path | Purpose | Current state |
| --- | --- | --- |
| `design/` | decomposition, flow diagrams, reference observations, and design decisions | complete for Part 1 |
| `client/` | planned React/Vite frontend | placeholder; no application code yet |
| `server/` | planned Express API and local booking storage | placeholder; no application code yet |
| `server/data/` | planned server-owned JSON booking records | placeholder; intentionally empty |
| `handoffs/` | truthful continuation notes | current |
| `prompts/` | ordered, concise record of material project instructions | current |
| `evidence/` | evidence log for instructions, decisions, reviews, and verification | started |
| `AGENTS.md` | repository-specific working instructions | current |

## Design and evidence

- [Application design and flow diagrams](design/application-design.md)
- [Expedia reference observations and interface sketch](design/reference-observations.md)
- [Current handoff](handoffs/current.md)
- [Evidence log](evidence/evidence-log.md)
- [Part 1 project brief record](prompts/001-assignment-brief.md)

## Attribution and disclosure

The observable reference is [Expedia Hotels](https://www.expedia.com/Hotels), accessed September 8, 2026. Expedia is used only as a product-behavior reference. This project will use original interface code and synthetic records, and it will not reuse Expedia’s branding, imagery, screenshots, or listing data.

AI assistance: OpenAI Codex was used to help organize the Part 1 documentation, research publicly observable interface patterns, and will be disclosed in the evidence log with the work actually accepted and checked by the student. The student remains responsible for review, testing, commits, and the final submission.


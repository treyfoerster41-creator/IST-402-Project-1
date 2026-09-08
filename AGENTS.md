# Project instructions for Stayfinder

## Goal and scope

Build a small local hotel-booking prototype, not a real travel product. Preserve exactly two connected flows: a simulated hotel booking and booking-history review. Use synthetic data only.

## Architecture boundaries

- The React client owns rendering, local form state, navigation, loading states, and displaying API errors.
- The Express server owns the synthetic-property catalog, booking validation, total calculation, booking-id/confirmation creation, and reading/writing booking records.
- The client must not write the JSON data file directly or invent a confirmation number or total.
- The server must be involved in both booking creation and booking-history retrieval.

## Required behavior

- A successful interface booking must appear in history after browser refresh.
- Keep the explicit empty-history state and at least one meaningful validation failure.
- Validate required traveler details and sensible dates on the server, then return a user-safe error message.
- Do not add real payments, authentication, external booking APIs, user accounts, or scraped/live Expedia data.
- Keep server data in a clearly documented local JSON file. State what persists over browser refresh and server restart.

## Work and verification

- Before changing files, read `handoffs/current.md` and the applicable design documents.
- Make focused changes and keep documentation synchronized with behavior.
- Review changed files before committing. Exercise the flows in a browser before calling a feature verified.
- Record material prompts, decisions, browser checks, limitations, and AI tool/model roles in `evidence/evidence-log.md`.
- Never commit credentials, real traveler data, or generated dependency folders.

## Git plan

- Preserve the Part 1 planning checkpoint on `main`.
- Do substantial implementation on `feature/booking-history`.
- Merge reviewed and tested work to `main`, then verify the combined application.


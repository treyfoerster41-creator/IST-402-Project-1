# 002 — Implementation and verification record

## Objective

Implement the approved small hotel-booking prototype on `feature/booking-history` while preserving the Part 1 checkpoint on `main`.

## Accepted implementation decisions

- Use three source-controlled synthetic Asheville properties; do not call or scrape Expedia.
- Use React/Vite for interface state and rendering, and Express for catalog retrieval, validation, calculations, confirmation creation, and persistence.
- Persist bookings only through `server/data/bookings.json`; begin with an empty array.
- Keep confirmation, history, empty, and field-level validation states visible in the browser.

## Verification record

- `npm run test`: five checks passed (validation plus API/persistence).
- `npm run build`: production client build passed.
- Browser walkthrough: searched Asheville, selected Blue Ridge Lodge, created a synthetic booking, opened history after a browser refresh, submitted empty traveler fields to receive server errors, and confirmed the empty-history state after resetting the test record.

## Limitation

The local sandbox blocks binding an HTTP test port, so the API tests were run outside the sandbox’s port restriction. The completed app itself was also browser-tested outside that restriction on localhost.

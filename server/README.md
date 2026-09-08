# Backend

This folder contains the Node/Express server for Stayfinder.

Responsibilities: synthetic property data, API routes, booking validation, nights/total calculation, confirmation-code generation, and JSON-file persistence. `data/bookings.json` is the local, server-owned booking store and begins as an empty array.

The server serves its API on port 3001 by default. Run both client and server from the repository root with `npm run dev`, or run this server alone with `npm run start --workspace=server`.

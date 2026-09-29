# Current handoff - Assignment 2, Part 1

Updated 2026-09-29. Branch: `codex/assignment2-part1-hotel-discovery`. The implementation snapshot is committed locally as `571fa23`; the branch is **not pushed**. Assignment 1 Part 2 remains preserved on `main`; the earlier ZIP activity changes were included because Assignment 2 builds on them. The local SQLite database and its existing bookings/deletions were not reset. An unrelated untracked Assignment 1 compressed video was excluded from the commit.

## What exists

- The prior Vue/FastAPI/SQLite fictional city-search and booking CRUD flow remains below the earlier fixed/entered ZIP-only demonstration.
- A new top-of-page live hotel-discovery section accepts five ASCII ZIP digits, including leading zeros. Vue calls only local FastAPI, displays loading/results/invalid/unresolved/empty/failure messages, shows provider names/addresses/coordinates honestly, and shares one selected place ID between list buttons and Leaflet markers.
- `backend/app/hotel_discovery.py` calls the exact-ZIP geocoding controller first, then Geoapify Places for `accommodation.hotel` with a 5 km circle around the returned ZIP point and a 50-result cap. It returns allowlisted provider IDs, optional names/addresses, and valid geometry. No live place is a bookable offer or SQLite booking.
- Leaflet 1.9.4 was installed after student approval and uses public OpenStreetMap tiles with visible attribution. The Geoapify key remains in the ignored root `.env` and backend only.
- Dated research, pre-implementation mockup, prompt record, README, evidence, and Assignment 2 `report.md` draft exist. The former Assignment 1 report and ZIP handoff were archived under `docs/` and `handoffs/`.

## What was checked

- All 38 backend tests passed; the Vue production build passed, and `npm ls` confirmed Leaflet 1.9.4.
- September 28 direct backend live 16802 request returned HTTP 200, exact State College center, and 21 hotel places. Browser 16802 showed loading, list, map tiles, markers, 5 km circle, and attribution. List-to-map and marker-to-list selection worked. Browser 02108 retained its leading zero and reached the displayed 50-place cap. Invalid 1680 and unresolved 00000 showed distinct feedback.
- The earlier fixed ZIP table and fictional Boston city search still worked. Mocked tests cover empty Places data, rate-limit, timeout, malformed responses, optional fields, duplicate IDs, and no hotel call after unresolved ZIP.
- A first map attempt failed because circle bounds were read before the map had a starting view. Setting the view first fixed it, and the browser map was rechecked.
- The root `.env` is ignored. No key was printed, put into Vue, or included in evidence.

## Incomplete and next task

1. The student selected a shorter replacement recording on September 29 and asked that it be used without agent review. Per the student's description, it shows unresolved ZIPs 11111 and 00000, Boston ZIP 02108 with a selected hotel/map zoom, and State College ZIP 16802 with a selected hotel/map interaction. Its supplied TemporaryItems path has expired, so it could not be copied into Finder/project evidence. Have the student reattach or save it to a durable location, confirm no key/private data is visible, and add an instructor-accessible link to `report.md`. Separate live 16802 and 02108 checks remain documented in the verification record.
2. Student acceptance review is not yet confirmed. The implementation was manually inspected in VS Code and passed its tests/build before local commit `571fa23`; do not claim student acceptance. After the student supplies a durable, instructor-accessible video link and accepts the work, push the branch and update `report.md` with the final artifact links.
3. `report.md` is a draft and **not ready for Canvas upload** while the branch is unpushed and the instructor-accessible video link is pending. Canvas upload and class demonstration are also unconfirmed.
4. Part 2 persistent shortlist is not implemented and must not be claimed. Keep the existing local SQLite database intact when resuming.

The project servers were running locally on `127.0.0.1:8000` and `127.0.0.1:5173` during verification; check whether they are still running before attempting to start another pair. Use README instructions if needed. See [verification](../evidence/assignment-2-part-1-verification.md) for exact observations.

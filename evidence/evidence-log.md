# Evidence log

| Date | Instruction / decision | Action | Expected result | Observed result / status |
| --- | --- | --- | --- | --- |
| 2026-09-09 | Part 1 checkpoint | Built Vue and FastAPI city search from supplied CSVs and recorded the exact implementation commit. | Preserve an inspectable Part 1 starting point. | Passed: Part 1 implementation checkpoint is dc413fd. |
| 2026-09-15 | Resume from handoff | Read handoffs/current.md, the Part 1 design, data guide, and current source before starting Part 2. | Continue from the repository as it actually stood. | Passed: only Part 1 CSV search was implemented, so Part 2 began from that state. |
| 2026-09-15 | Feature branch | Found an incompatible legacy React/Express branch with the required name, preserved it as archive/legacy-booking-history, then reset feature/booking-history to current Part 1 main. | Use the required branch without losing the earlier prototype. | Passed: Part 2 is based on correct Vue/FastAPI Part 1 work. |
| 2026-09-15 | SQLite CRUD | Added one-time CSV seed marker, SQLite tables for all four CSV record types, and FastAPI routes for search, users, booking create/read/cancel/delete. | After initial seed, all application reads and writes use SQLite without duplicate or restored starter records. | Implemented. New IDs use B###; runtime database is ignored by Git. |
| 2026-09-15 | Automated verification | Ran backend unit tests and Vue production build. | Backend behavior/persistence checks and Vue production build succeed. | Passed: 7 backend tests and the Vue production build completed successfully. |
| 2026-09-15 | Browser CRUD and persistence | Searched Boston, selected T001, booked it for U006, loaded history, cancelled B007, refreshed, restarted FastAPI, deleted B007, and restarted FastAPI again. | Search returns 4 Boston stays; create/read/cancel/delete use frontend; changes survive refresh/restart; deleted record stays absent. | Passed: B007 was confirmed, appeared for U006, changed to cancelled and persisted, then was deleted. After final restart, U006 showed empty history. |
| 2026-09-15 | Manual review and final integration | Student manually reviewed the changed Part 2 files in VS Code and accepted the work. Part 2 was committed as 2b1809a and merged into main as deebfc58. | Commit reviewed work, merge to main, then check combined app. | Passed: combined main ran all 7 backend tests, Vue production build, and browser Boston search. Final main is pushed to GitHub. |
| 2026-09-24 | Part 2 demonstration recording | Captured one full-display walkthrough with Boston search, create/read/cancel B008 for U001, create/delete disposable B009, refresh, restart both services, and reload U001 history. | Demonstrate frontend CRUD and persistence through refresh and service restart in one video under 3 minutes. | Passed: B008 remained cancelled in SQLite-backed history and B009 stayed deleted. Full-display WebM verified at 2:45 and 36 MB. No API key or `.env` content was shown. |

## Public API activity - September 23, 2026

The [activity instructions](../prompts/003-public-api-activity.md) led to backend
configuration/health integration, a Geoapify controller, fixed/entered-ZIP routes,
and a separate Vue input/results table. The SQLite booking flow remains available.

[Detailed checks and screenshots](zip-lookup/verification.md) record real
backend/frontend 16802 requests, entered 02108, Firefox compatibility, mocked
failures, 28 passing tests, a passing build, safe key handling and the SQLite
connection-cleanup correction. Work is uncommitted on codex/geoapify-zip-activity;
student review, class demonstration and Canvas upload are not claimed complete.

## Tool disclosure

OpenAI Codex (GPT-5) assisted with implementation, documentation, automated checks, and local browser verification. The student performs the required VS Code review before accepting changes and remains responsible for Git and Canvas submission.

## Assignment 2, Part 1 - September 28, 2026

The [selected assignment instruction](../prompts/004-assignment2-part1-hotel-discovery.md) led to the [research and early mockup](../docs/assignment-2-part-1-research.md), the exact-ZIP/circle-filter backend route, and synchronized Vue list/Leaflet map. [Expected versus observed checks](assignment-2-part-1-verification.md) include the dated live 16802 and 02108 lookups, keyboard-relevant controls, safe failures, and prior-flow regression checks.

Dependency loop: inspected `frontend/package.json`, lockfile, and `node_modules` and found no Leaflet. Explained `leaflet@1.9.4` installation; the student explicitly approved it. An initial sandboxed npm request could not resolve registry.npmjs.org, so the authorized install was retried with network permission. `npm ls` confirmed the package, and the Vue build passed.

Failed/revised approach: the first browser check found a populated hotel list but a blank Leaflet map. Browser console evidence identified `getBounds()` before map initialization. Set the map view before fitting the circle; after reload, tiles, 21 markers, center/circle, attribution, and bidirectional selection worked. No provider key was included in frontend configuration.

Tool/model disclosure for this work: OpenAI Codex (GPT-5) assisted with research, design sketch, implementation, mocked tests, and local browser checks. Web research used Geoapify, Leaflet, OSM tile-policy, and Expedia-owned Egencia documentation linked from the research note. The student confirms manually reviewing changed files in VS Code and checking the running app in the browser after implementation changes. Implementation commit `571fa23` was created after the local tests/build passed.

## Assignment 2, Part 1 - demo recording, September 29, 2026

The student recorded a shorter replacement MOV and asked that it be used without agent review. Per the student's description, it shows errors for ZIPs 11111 and 00000, Boston ZIP 02108 with a selected hotel and map zoom, and State College ZIP 16802 with a selected hotel and map interaction. The student supplied a Penn State Kaltura media-page link, now included in `report.md`, and confirmed that the video loads in a private window. Before submitting, the student should make sure the recording contains no API key, `.env` content, or private browser information.

## Assignment 2, Part 1 - implementation checkpoint, September 29, 2026

The student confirms manually reviewing the changed files in VS Code and checking the app in the browser after implementation changes. The complete backend suite passed (38 tests), the Vue production build passed, `git diff --check` passed, and `.env` plus the SQLite database were confirmed ignored. Implementation commit `571fa23` and report-link commit `c53abc0` are pushed on `codex/assignment2-part1-hotel-discovery`. The unrelated Assignment 1 compressed video was not staged. The student confirmed Kaltura access in a private window; Canvas upload remains the student's step.

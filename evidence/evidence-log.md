# Evidence log

| Date | Instruction / decision | Action | Expected result | Observed result / status |
| --- | --- | --- | --- | --- |
| 2026-09-09 | Part 1 checkpoint | Built Vue and FastAPI city search from supplied CSVs and recorded the exact implementation commit. | Preserve an inspectable Part 1 starting point. | Passed: Part 1 implementation checkpoint is dc413fd. |
| 2026-09-15 | Resume from handoff | Read handoffs/current.md, the Part 1 design, data guide, and current source before starting Part 2. | Continue from the repository as it actually stood. | Passed: only Part 1 CSV search was implemented, so Part 2 began from that state. |
| 2026-09-15 | Feature branch | Found an incompatible legacy React/Express branch with the required name, preserved it as archive/legacy-booking-history, then reset feature/booking-history to current Part 1 main. | Use the required branch without losing the earlier prototype. | Passed: Part 2 is based on correct Vue/FastAPI Part 1 work. |
| 2026-09-15 | SQLite CRUD | Added one-time CSV seed marker, SQLite tables for all four CSV record types, and FastAPI routes for search, users, booking create/read/cancel/delete. | After initial seed, all application reads and writes use SQLite without duplicate or restored starter records. | Implemented. New IDs use B###; runtime database is ignored by Git. |
| 2026-09-15 | Automated verification | Ran backend unit tests and Vue production build. | Backend behavior/persistence checks and Vue production build succeed. | Passed: 7 backend tests and the Vue production build completed successfully. |
| 2026-09-15 | Browser CRUD and persistence | Searched Boston, selected T001, booked it for U006, loaded history, cancelled B007, refreshed, restarted FastAPI, deleted B007, and restarted FastAPI again. | Search returns 4 Boston stays; create/read/cancel/delete use frontend; changes survive refresh/restart; deleted record stays absent. | Passed: B007 was confirmed, appeared for U006, changed to cancelled and persisted, then was deleted. After final restart, U006 showed empty history. |
| 2026-09-15 | Manual review and final integration | Student manually reviewed the changed Part 2 files in VS Code and accepted the work. | Commit reviewed work, merge to main, then check combined app. | Review accepted; feature commit, merge, final main check, and push are next. |

## Tool disclosure

OpenAI Codex (GPT-5) assisted with implementation, documentation, automated checks, and local browser verification. The student performs the required VS Code review before accepting changes and remains responsible for Git and Canvas submission.

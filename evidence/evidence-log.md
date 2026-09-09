# Evidence log

| Date | Instruction / decision | Action | Expected result | Observed result / status |
| --- | --- | --- | --- | --- |
| 2026-09-09 | SQLite capability check from supplied data guide | Used `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3`; imported `sqlite3`, created a local verification database, saved `sqlite-ok`, closed/reopened it, and read it back. | SQLite is available without installation and retains a saved row after reopening. | Passed: Python 3.14.7, SQLite 3.50.4, readback was `sqlite-ok`. |
| 2026-09-09 | Part 1 CSV search requirement | Rebuilt the project as Vue + FastAPI, keeping the supplied CSV records under `backend/data/`. | Frontend uses FastAPI; backend joins hotels and trips by `hotel_id`. | Implemented and browser-verified; student review and checkpoint commit remain. |
| 2026-09-09 | Dependency check | Ran FastAPI import and backend tests after installing the declared packages. | Backend tests should import and run. | Passed after two scoped corrections: `httpx` was added for `TestClient`, and `backend/` became an explicit package. All 3 backend tests passed; Vue production build passed. |
| 2026-09-09 | Required browser checks | Searched `Boston` and `Miami` through the Vue interface. | Boston returns `T001`, `T002`, `T009`, `T010` in a labeled table; Miami shows a clear no-results message. | Passed: Boston displayed 4 stays with the expected trip IDs, hotel joins, nights, and prices. Miami displayed "No offered stays match 'Miami.' Try another city." |
| 2026-09-09 | Manual review and Part 1 checkpoint | Student reviewed the report and Part 1 work in VS Code, reported the non-ASCII highlighting concern, and accepted the changes after it was corrected to ASCII punctuation. | Commit only reviewed work, preserve the prior incorrect app in a backup, and identify the exact checkpoint. | Passed locally: Part 1 implementation checkpoint is `dc413fd`; the prior app is preserved on `archive/react-express-prototype`. |

## Tool disclosure

OpenAI Codex (GPT-5) assisted with setup, code generation, documentation, and checks. The student reviews accepted changes in VS Code and remains responsible for Git and Canvas submission.

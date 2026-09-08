# Evidence log

This log connects material instructions to accepted work, checks, decisions, and limitations. Entries will be updated as the repository changes.

| Date | Instruction / prompt | Change or decision | Review / verification | Limitation / next action |
| --- | --- | --- | --- | --- |
| 2026-09-08 | `prompts/001-assignment-brief.md` | Chose a constrained synthetic hotel prototype with booking and history flows. | Student approved scope and stack in the project conversation. | No application code yet. |
| 2026-09-08 | Public Expedia Hotels reference | Recorded destination/dates/travelers search pattern and result-card cues in `design/reference-observations.md`. | Public page inspected without login or purchase. | This is behavioral inspiration, not copied UI/assets/data. |
| 2026-09-08 | Part 1 repository requirements | Added README, AGENTS instructions, design, prompt record, evidence log, and handoff. | Documentation cross-checked against the stated Part 1 requirements. | Awaiting student review, initial commit, and remote push. |
| 2026-09-08 | Student-provided GitHub URL | Created local Part 1 checkpoint `7496620` and inspected the remote before any push. | Remote `main` was found to contain an unrelated calculator application; no remote history was changed. | Student must choose a separate empty repository or explicitly authorize replacing the existing remote main. |
| 2026-09-08 | Student-provided IST-402 repository URL | Inspected the intended repository before connecting it. | Its `main` contained only GitHub's one-line initial README; it is safe to integrate with the assignment checkpoint. | Push the checkpoint, then begin implementation on the planned feature branch. |
| 2026-09-08 | Part 1 Git checkpoint requirement | Pushed the documentation checkpoint to `main` at `79749f7`, preserving the remote's initial commit without a force-push. | Local `main` was confirmed to track `origin/main` after the push. | Create the planned implementation branch before substantive application code. |
| 2026-09-08 | Part 2 booking/history requirement | Implemented React/Vite client, Express API, synthetic property catalog, server validation, confirmation creation, and JSON persistence on `feature/booking-history`. | Architecture boundary checked in code: only `server/src/booking-store.js` writes the JSON file and only `server/src/server.js` creates totals/confirmation codes. Student reviewed the named feature files in VS Code; accepted work was committed as `302ab1a` and merged to `main` as `b98bf81`. |
| 2026-09-08 | Required behavior and failure/empty state | Added five automated checks: three validation tests and two API/persistence tests. | `npm run test` passed all 5 checks; `npm run build` completed a production Vite build. | Local sandbox blocks binding a test port; the API test was run outside that restriction and passed. |
| 2026-09-08 | Browser verification requirement | Exercised local search, selection, confirmation, history, validation failure, and empty-history flows. | Browser showed three Asheville results; a synthetic Blue Ridge Lodge confirmation; history after refresh; required-field server errors; and empty history after reset. After merge, a synthetic Taylor Morgan booking was confirmed on `main`, retrieved from history, and retrieved again after a full browser refresh. The JSON store was reset to `[]` afterward. |
| 2026-09-08 | Feature branch / final main requirement | Pushed the reviewed feature branch and merged it with `--no-ff` into `main`. | Combined `main` at `b98bf81` passed all five tests and the production Vite build before push; browser walkthrough also ran from merged `main`. | A short screencast and Canvas submission remain. |

## AI/tool disclosure

| Tool / model | Role | Human responsibility |
| --- | --- | --- |
| OpenAI Codex (GPT-5) | Helped research public reference patterns and draft repository documentation. | Student reviews every accepted change, runs the application, verifies browser behavior, and owns submissions/commits. |

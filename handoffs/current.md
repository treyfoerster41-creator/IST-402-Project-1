# Current handoff - Assignment 2 Part 2

Updated October 6, 2026. The working branch is `main`. Assignment 2 Part 2 was developed on `codex/assignment2-part2-rag` and fast-forwarded into `main`. Its implementation checkpoint is `c40bc73898b2d80b25b791375ff1ea080c46513e`. Both the feature branch and `main` were pushed to GitHub. The student reviewed the files in VS Code, recorded the browser and terminal demos, accepted the results, and authorized the commit, merge, and push. Canvas upload and a class demonstration have not been claimed.

## What exists

- The earlier fictional booking CRUD, Geoapify ZIP search and hotel list/map, and local-first saved-hotel Add/Remove behavior remain. The ignored local SQLite database holds one saved Scholar Hotel State College for ZIP 16802, with five October 10-14, 2026 simulated nights. The student's manual October 10 edit is 12500 cents and 7 rooms. Do not reset or reseed the database for evidence.
- The new Vue hotel advisor asks about saved hotels. FastAPI sends the question and limited schema to Gemini 3.5 Flash-Lite, validates one bounded read-only SELECT, retrieves checked SQLite rows, then sends the question and those rows to Gemini for a grounded answer. The page shows the answer, stay coverage, SQL, and retrieved rows. No live booking claim is made.
- Root `report.md` is the first-person Part 2 submission, with the assessed implementation commit and three MediaSpace demo links. The earlier Part 1 report is archived in `docs/assignment-2-part-1-report-archive.md`. Research, an early mockup, selected prompt, synthetic JSON sample, tests, and expected-versus-observed evidence are linked from the report.
- `.env` and `backend/data/expedia_lite.db` are ignored and not tracked. The unrelated `evidence/Assignment 1 Part 2 Demo Vid - compressed.mp4` is untracked and was excluded from the Part 2 commit.

## What was checked

- The live ZIP 16802 question returned two Scholar rows ($125/7 rooms on October 10 and $100/20 on October 11), a checked $225 two-night total, minimum 7 rooms, and a matching second-model answer. ZIP 00000 returned no match. The student recorded both browser flows and a focused SQL safety test ending in `OK`.
- Codex inspected the three clips and did not see an API key or `.env` contents. The student supplied three MediaSpace links; Codex opened each while logged out and found a playable video without a sign-in prompt. Copies of the clips are in `evidence/assignment-2-part-2-*.mov`.
- After the fast-forward into `main`, all 51 backend tests and the Vue production build passed. A merged-app browser check showed ZIP 16802 still returns the saved Scholar hotel, its map marker, and the October 10 $125/7 edit. Fixture and mocked-provider checks remain labeled separately in `evidence/assignment-2-part-2-verification.md`.

## Next concrete task

Upload **only `report.md`** to the Assignment 2 Part 2 Canvas item. The three MediaSpace links inside it provide the recorded demonstration. `main` and `origin/main` agreed after the push, and Codex opened the GitHub report while logged out. The student should make sure the instructor can open the MediaSpace clips and complete any separate in-class demonstration if required. Preserve the ignored database and credentials.

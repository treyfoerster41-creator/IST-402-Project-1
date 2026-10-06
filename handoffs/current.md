# Current handoff - Assignment 2 Part 2

Updated October 6, 2026. Working branch: `codex/assignment2-part2-rag`, based on pushed October 1 local-storage commit `11c918b`. This new Part 2 work is **not yet committed or pushed**. The student has authorized Gemini integration and privately added a key to the ignored root `.env`. Do not inspect, print, commit, or submit that file. The ignored local SQLite file and its backup hold actual saved hotels and earlier booking changes; never reset/reseed to make a test pass.

## What exists

- Existing Vue/FastAPI/SQLite fictional city search and booking CRUD, Geoapify ZIP and hotel list/map, and local-first saved-hotel Add/Remove remain. The current ignored DB has one Scholar Hotel State College saved for ZIP 16802 with five October 10-14, 2026 nights; October 10 was manually edited by the student to 12500 cents/7 rooms. This state is not a live price/availability claim.
- Part 2 research and an early SVG mockup were saved before code changes. The earlier first-person Assignment 2 Part 1 report was copied to `docs/assignment-2-part-1-report-archive.md`; root `report.md` is now a **draft Part 2 report** with a pending final-commit item.
- `backend/app/hotel_advisor.py` makes a Gemini SQL-proposal call, validates and executes a single bounded SELECT against an allowlist in read-only SQLite, checks source rows, computes full-stay nights/total/minimum rooms, and makes a second Gemini answer call. `POST /api/hotels/ask` serves it. `frontend/src/components/HotelAdvisor.vue` provides question, states, answer, checked-stay table, and expandable SQL/row evidence. Gemini key and model are backend configuration only.
- A fixed synthetic JSON sample and temporary-DB tests cover the two-call flow, no match, missing night, disallowed SQL, and mocked quota. Existing screenshots that the student moved into `evidence/Local-Hotel-Evidence Pics/` were preserved and their Markdown links updated. An unrelated untracked compressed Assignment 1 video remains untouched.

## What was checked

- A live backend-only Gemini 3.5 Flash-Lite call returned successfully after one network-restricted attempt failed. The full live question for ZIP 16802, October 10-12 returned a focused SQL SELECT, two local Scholar rows (12500/7 and 10000/20), checked $225 total/minimum 7 rooms, and matching second-model answer. Live ZIP 00000 returned zero rows and `no_match`.
- Codex's local in-app browser check showed the successful answer, 2/2-night table, SQL and rows; the no-match state; and the preserved 16802 saved-hotel list/map with edited night. These were agent checks separate from the student's later recordings.
- The final backend suite passed 51 tests without resource warnings, the Vue production build passed, and `git diff --check` passed. The first full backend run had two failures because an old health test expected no Gemini field; that test was updated and the suite rerun. A new test connection-cleanup warning was also corrected. No new dependency was installed.
- The student confirmed an October 6 VS Code review and made separate browser clips of the $225/7-room success with SQL and two rows, and a ZIP 00000 no-match result with SQL. A third clip showed the focused SQL-safety test ending in `OK`. Codex inspected the clips and saw no `.env` contents or API key, then copied them to stable files in `evidence/assignment-2-part-2-*.mov` without deleting the originals. The student supplied three MediaSpace links; Codex opened all three while logged out and found the expected titles and playable videos without a sign-in prompt. Earlier student DB Browser, Firefox Network, refresh, Add/Remove, and local error screenshots remain documented in `evidence/local-hotel-activity.md`.

## Next concrete tasks

1. Review the final diff and inspect `git status`; keep `.env`, SQLite, and unrelated video out of staging. If code changes after this handoff, rerun the backend tests, frontend build, and `git diff --check`.
2. Ask the student whether the recorded success and no-match browser results match their expectations; correct any issue they identify. The clips themselves show the student exercising both flows.
3. After student acceptance, commit reviewed work on this feature branch, merge into `main` only if the student directs that step, verify combined app, push, and insert the exact assessed pushed commit in the report. The student submits `report.md` to Canvas. Do not claim those steps early.

See [Part 2 verification](../evidence/assignment-2-part-2-verification.md), [research](../docs/assignment-2-part-2-research.md), [mockup](../docs/assignment-2-part-2-mockup.svg), and [prompt record](../prompts/006-assignment2-part2-rag.md).

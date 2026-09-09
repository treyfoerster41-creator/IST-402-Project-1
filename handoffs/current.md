# Current handoff

**Last updated:** September 9, 2026  
**Checkpoint:** Part 1 implementation complete and verified locally; awaiting student VS Code review, checkpoint commit, and GitHub push.

## What exists

- Instructor-supplied fictional CSV files are copied to `backend/data/`; the supplied data guide and relationship diagram are in `docs/`.
- FastAPI route and CSV join logic are in `backend/app/`, with three backend behavior tests in `backend/tests/`.
- Vue city-search interface and labeled results table are in `frontend/`.
- README, project instructions, design note, prompt record, evidence log, and `report.md` describe the corrected assignment scope.
- SQLite capability was checked with the selected Python interpreter and passed; `backend/data/sqlite-capability-check.db` is ignored.

## What has been checked

- Python 3.14.7 can import `sqlite3` version 3.50.4.
- A local SQLite file retained `sqlite-ok` after a close and reopen.
- The supplied data guide states that Boston must return `T001`, `T002`, `T009`, and `T010`; Miami must return no rows.
- FastAPI backend tests passed all three checks; Vue production build passed.
- Browser verification passed: Boston showed four labeled joined records; Miami showed the no-results message.

## What remains

- The student must manually scan the changed project files in VS Code and accept them.
- Add any desired repository-stored browser screenshots to the report/evidence before Canvas upload.
- Commit the correct Part 1 checkpoint and force-push the approved rebuilt `main` while retaining the archive branch.

## Next concrete task

After the student review, commit the Part 1 scope, force-push the rebuilt `main`, and replace the pending commit text in `report.md` with the exact GitHub commit link before upload.

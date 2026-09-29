# ZIP activity handoff archived at Assignment 2 transition

Last updated: September 24, 2026

Branch: codex/geoapify-zip-activity (new changes are uncommitted and not pushed).

State: Assignment 1 Part 2 remains completed on main (c5ea540). The new graded
public API ZIP activity is implemented and verified locally. Its student review,
class demonstration, Canvas upload and any commit/push are not yet confirmed.

## What exists

- Vue provides city search, selectable offered stays, a simulated booking form, traveler-selectable booking history, cancellation, deletion, and empty states.
- FastAPI routes use SQLite for search and all booking CRUD after a one-time seed from the four supplied CSV files.
- backend/app/database.py creates schema and a csv_seed_v1 marker. The marker prevents restart from duplicating or restoring supplied booking rows.
- Backend tests cover search, seeded and empty history, create, cancellation, deletion, and persistence after reinitialization.
- The local database is backend/data/expedia_lite.db and is intentionally ignored by Git.
- New config.py loads the ignored root .env explicitly; geoapify.py resolves exact
  five-digit U.S. ZIP codes; main.py exposes safe health and fixed/entered routes.
  ZipLookup.vue supplies both buttons, input, results table and safe errors.
- The student's existing key is configured. Never display it or .env contents.
  .env.example is key-free. ZIP lookup does not modify the booking database.
- The old SQLite deletion connection leak was fixed using database_session.

## What has been checked

- The current 28 backend tests passed: 7 existing SQLite checks and 21 new mocked
  ZIP/configuration/route checks. The suite passes without the connection warning.
- The Vue production build passed.
- Browser checks passed: Boston returned four stays; selected T001 was booked as B007 for U006; B007 appeared in history; cancellation retained it; refresh and FastAPI restart retained the cancelled record; deletion removed it; a later restart left U006 history empty.
- The Part 1 checkpoint remains dc413fd. The reviewed Part 2 feature commit is 2b1809a and the merge commit on main is deebfc58.
- The incompatible earlier feature branch was preserved at archive/legacy-booking-history; feature/booking-history was rebased to correct Part 1 main before Part 2 work.
- September 23 live Geoapify checks: direct backend 16802, fixed Vue button and
  entered 16802 returned State College; entered 02108 returned Boston and kept
  its leading zero. Firefox at http://localhost:5173 also completed the live
  fixed 16802 lookup. Chrome Network showed sanitized local API data only.
- Invalid ZIP and mocked provider/unresolved feedback passed. Temporary mocks
  were stopped and normal backend behavior restored. Loading is implemented and
  code-reviewed; its separate delayed UI capture was interrupted.
- Existing browser Boston search, stay selection, empty U001 history and saved
  U002 history worked. Latest read-only DB check found B003-B006; the student's
  earlier B001/B002 deletions were preserved. Tests use a temporary database.
- Recorded the Assignment 1 Part 2 walkthrough at
  evidence/assignment-1-part-2-demo-fullscreen.webm. The single full-display
  Sep 24 take created/cancelled B008 for U001, created/deleted B009, refreshed
  Firefox, restarted FastAPI and Vite, then confirmed B008 remained cancelled.
  Firefox verified the WebM duration as 2:45; it contains no credentials.
- See evidence/zip-lookup/verification.md for exact checks and screenshot links.

## What remains

1. Student must show the public API activity to TA/instructor and upload its
   screenshot with configuration status. Do not claim either action complete.
2. Review/accept new files in VS Code before requesting a commit/push. Preserve
   the prior .gitignore and dependency setup edits as part of this activity.
3. Full Assignment 2 overview is still unavailable. Do not add live hotels, map
   or shortlist without further direction. report.md remains Assignment 1's report.

## Next concrete task

Upload evidence/zip-lookup/submit-zip-16802.png to the graded public API activity,
stating "Backend health: ok. Geoapify key is configured." Its provided deadline
is September 24, 2026 at 4:00 PM ET. This activity does not request report.md.

FastAPI and Vue were stopped after the recording. To inspect the app again,
follow the README run instructions and open http://localhost:5173 in Firefox.
Stop only these project servers if requested; preserve unrelated processes.

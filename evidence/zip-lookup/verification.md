# Public API activity - verification and submission

Checked September 23, 2026 on `codex/geoapify-zip-activity`. Work is local,
uncommitted and not pushed. This is the in-class ZIP activity, not full Assignment 2.

## Grading checklist

| Criterion | Expected | Observed |
| --- | --- | --- |
| API key/project structure (1) | Backend-only key in the existing Vue/FastAPI app. | Reused student-supplied key authenticated real Geoapify requests. Separate config, controller, routes and Vue component exist. Key creation itself was performed earlier by the student. |
| .env integration (1) | Explicit root-file loading; no key exposure. | Helper derives root .env path from its own file. Tests cover that path, override=False, absent/empty/whitespace key. .env is ignored and untracked. |
| Health check (1) | Configuration status only. | Browser returned status ok and Geoapify key is configured. [Screenshot](health.png). |
| Direct backend ZIP test (1) | Real 16802 request via /api/demo/zip-location in browser. | Returned 16802, us, State College, latitude 40.803167822, longitude -77.861384958. [Direct response](backend-16802.png). |
| Frontend fixed button (1) | Vue -> FastAPI -> Geoapify. | Look up ZIP 16802 returned the same live fields in Chrome and Firefox. [Result](fixed-16802.png). |
| Entered ZIP input (2) | Use entered text, preserving leading zeros. | Entered 02108 returned Boston, US, 42.357581412, -71.065946589, not the fixed result. [Entered ZIP](entered-02108.png). |
| Returned data table (3) | Labeled fields for the entered ZIP. | Entered 16802 and selected Look up ZIP; table showed matching ZIP, locality, country and coordinates. [Submission screenshot](submit-zip-16802.png). |

These are completed technical checks, not a guarantee of an awarded grade.
Showing the app to the TA/instructor and uploading evidence remain student actions.

## Additional checks and limitations

- Firefox at http://localhost:5173 loaded the app/configured health and completed
  the real fixed 16802 lookup after restarting the normal backend. Chrome also
  verified entered 16802 and 02108; the app is not Chrome-only.
- Chrome Network showed GET `http://127.0.0.1:5173/api/zip-location?zip_code=16802`,
  HTTP 200, and only five sanitized location fields, no key/provider request URL.
  [Network evidence](network-response.png).
- Entering abc cleared old results and showed five-digit guidance.
  [Invalid input](invalid-input.png).
- A temporary process-only mocked connection error produced a useful provider
  error and no stale table. Mock empty results for 99999 produced a distinct
  unresolved-ZIP message. These are mock tests, not live 99999 evidence.
  [Failure](mocked-provider-failure.png), [unresolved](mocked-unresolved.png).
- All mock servers were stopped; normal behavior was restored and subsequently
  verified by Firefox's live success. No production mock toggle was added.
- Loading text, disabled controls and frontend timeout are implemented and
  code-reviewed. The separate delayed-loading UI capture was interrupted and
  is not claimed verified.
- Existing browser Boston search returned T001, T002, T009 and T010. T001
  selection populated the booking form; U001 showed its existing empty history
  and U002 loaded B003. Mutation/persistence regression tests use an isolated
  temporary database. No original local booking was removed or restored by
  these checks. After the student's own Firefox interaction, a read-only check
  found B003-B006 with existing statuses; prior B001/B002 deletions remain intact.

## Automated checks and revised approach

```text
.venv/bin/python -W error::ResourceWarning -m unittest discover -s backend/tests -v
npm run build --prefix frontend
git diff --check
```

All 28 tests passed (7 existing SQLite tests and 21 new mocked ZIP/config/route
tests); Vue production build and whitespace checks passed. ZIP tests cover
parameters, invalid input/no request, leading zeros, missing key, wrong
country/postcode, empty results, malformed responses, invalid/nonfinite
coordinates, timeouts, redirects and provider errors without live API quota.

The combined run exposed an existing SQLite connection ResourceWarning in
delete_booking. Its final `with connection()` was changed to the existing
database_session helper, which closes the connection. The final suite passed
without that warning. CSV records and booking semantics were not changed.

A value-comparison scan found no configured key in Git candidate files or the
frontend build. The submission screenshot was visually checked: no key, .env
contents, private account information or real traveler records are visible.

## Submit this activity

1. Show the app/current progress to the TA/instructor if not already done.
2. Upload [submit-zip-16802.png](submit-zip-16802.png) to the graded public API
   activity in Canvas. One screenshot satisfies the stated upload format.
3. Include: "Backend health: ok. Geoapify key is configured. ZIP 16802 returned
   State College, US, with latitude and longitude through Vue and FastAPI."

Due September 24, 2026 at 4:00 PM ET, per the supplied instructions. Never upload
.env or the key. This activity does not request report.md; that file remains the
completed Assignment 1 Part 2 report.

## Trace and disclosure

[Selected instructions](../../prompts/003-public-api-activity.md) ->
[design/research](../../docs/zip-lookup-design.md) ->
frontend/src/components/ZipLookup.vue -> backend/app/main.py ->
backend/app/geoapify.py -> Geoapify. backend/app/config.py provides private
configuration; only sanitized data returns to Vue.

OpenAI Codex assisted with implementation, research, tests, documentation and
browser checks. A separate Codex agent wrote/reviewed mocked tests and audited
errors/configuration. Student VS Code acceptance and commit/push remain pending.
Hotel retrieval, map and shortlist remain intentionally outside this activity.

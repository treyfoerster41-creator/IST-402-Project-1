# Assignment 2 Part 2 verification - October 6, 2026

This record separates student browser/terminal recordings, Codex-run checks, model calls, and synthetic fixtures. No API key or `.env` contents are included. All currency and room counts below are simulated local course data, not live offers.

## Student manual review and recordings

On October 6, the student confirmed reviewing the Part 2 files in VS Code. The student then made three short screen recordings. Codex inspected the clips afterward; the observations below describe what is visible in the recordings, not additional tests run by the student.

| Student action | Expected | Observed in recording |
| --- | --- | --- |
| Ask about a saved hotel in ZIP `16802` from October 10 to checkout October 12, then expand the evidence panel. | A grounded two-night answer with accepted SQL and the two source rows. | The browser showed Scholar Hotel State College, $225.00 total, minimum 7 rooms, a bounded SELECT, and October 10 and 11 rows of $125.00/7 rooms and $100.00/20 rooms. |
| Ask which saved hotels are in ZIP `00000` and expand the evidence panel. | A clear no-match result, not a fabricated hotel or provider-error message. | The browser showed the `00000` question, “No matching saved records were found,” a no-match answer, and a read-only SELECT filtered to `00000`. |
| Run the focused SQL safety test in VS Code's terminal. | The guard test passes without changing or reading unrelated tables. | The terminal showed `test_model_sql_cannot_change_or_read_other_tables ... ok`, followed by `Ran 1 test` and `OK`. This is one isolated automated test visibly run by the student, not proof of a malicious live-model response. |

Codex did not see a key or `.env` contents in the reviewed clips. Copies are saved as [successful answer](assignment-2-part-2-success.mov), [no-match case](assignment-2-part-2-no-match.mov), and [SQL safety test](assignment-2-part-2-sql-safety.mov); the original macOS temporary recordings were left untouched. The student supplied MediaSpace links for [success](https://psu.mediaspace.kaltura.com/media/t/1_mm1w7j33), [SQL safety](https://psu.mediaspace.kaltura.com/media/t/1_nsgnwgsr), and [no match](https://psu.mediaspace.kaltura.com/media/t/1_3m0srbwj). Codex opened each page in a logged-out in-app browser and confirmed that the expected title and playable video appeared without a sign-in prompt. This is an access check, not a claim that the student tested a private window.

## Live Gemini and local SQLite workflow (Codex-run)

The project-root `.env` contained a Gemini key, confirmed only as configured; its value was not printed. A small backend-only call to the configured `gemini-3.5-flash-lite` model returned `Ready.` The first network attempt in the restricted sandbox could not reach Gemini; a permitted backend-only run outside that network restriction succeeded. This was a connectivity correction, not evidence that a provider failure means no saved hotels.

| Input/action | Expected | Observed |
| --- | --- | --- |
| Ask: `For ZIP 16802, which saved hotel has rooms from 2026-10-10 to 2026-10-12, and what is the total simulated cost?` | First model request proposes a focused SELECT; backend validates it and retrieves only saved ZIP 16802 nights for Oct 10 and 11; second model request receives the question and those rows; answer uses the checked two-night sum and minimum rooms. | Live first Gemini response proposed the query below. Read-only SQLite returned Scholar Hotel State College's two rows: Oct 10 = 12500 cents / 7 rooms, Oct 11 = 10000 cents / 20 rooms. Backend check produced 2/2 nights, 22500 cents ($225.00), minimum 7 rooms. Live second Gemini response named Scholar, $225.00 and 7 rooms. |
| Ask: `Which saved hotels are in ZIP 00000?` | Valid query, no local records, clear no-match rather than a model/provider failure. | Live Gemini proposed a SELECT filtered to ZIP `00000`; local row count was 0; endpoint status was `no_match` with “No saved local hotel records matched this question.” |
| In the local browser at `http://127.0.0.1:5173`, submit the first question and expand evidence. | Answer, checked stay table, accepted SQL, and two retrieved rows visible. | Codex's browser inspection showed Scholar, $225.00, 7 rooms, 2/2 nights, accepted SQL, and two dated rows. The separate no-match question showed its own message. This is agent browser verification, not a claim that the student has reviewed this new Part 2 change. |
| Re-run ZIP 16802 discovery in the same browser. | The existing local-first lookup and map remain intact. | `Saved locally` displayed one Scholar hotel with five rows, including the Oct 10 $125.00/7 edit, and a numbered Leaflet marker. No hotel was added or removed in this check. |

The live proposed SQL was:

```sql
SELECT h.hotel_id, h.name, h.address, z.zip_code, n.stay_date, n.nightly_rate_cents, n.rooms_available
FROM saved_hotels AS h
JOIN saved_hotel_zips AS z ON z.hotel_id = h.hotel_id
JOIN demo_hotel_nights AS n ON n.hotel_id = h.hotel_id
WHERE z.zip_code = '16802' AND n.stay_date >= '2026-10-10' AND n.stay_date < '2026-10-12'
LIMIT 40
```

The backend sent the original question, that accepted SQL, the two retrieved local rows, and the checked 22500-cent/7-room summary to Gemini in the second request. The browser displayed the resulting answer with SQL and row evidence. The saved hotel provider ID is intentionally omitted from this prose but is present in the local API response; it is not a private credential.

## Isolated synthetic and automated checks

The [fixed JSON sample](../backend/tests/fixtures/assignment2_part2_saved_hotel.json) is synthetic, not a live Geoapify response. To repeat it without touching the student's database: run `.venv/bin/python -m unittest backend.tests.test_hotel_advisor -v` from the repository root. The tests create a temporary SQLite database, seed the fictional Assignment 1 sample, save `Fixture Hotel`, modify Oct 10 to 12500 cents/7 rooms, and mock the two Gemini replies. Expected 2-night total is 22500 cents with a minimum of 7 rooms. A second synthetic saved hotel yields a $200 two-night total for a comparison test. Other tests remove a required night or set its room count to zero and verify `insufficient_data`, check a no-match case, reject unsafe/mismatched SQL, and simulate a Gemini quota response. The quota simulation is labeled a mock; it did not consume actual service quota.

The SQL guard was tested against DELETE, an unrelated SQLite schema read, multiple statements, and a SELECT that invented a rate. Each was rejected. A byte-for-byte comparison of the temporary database before and after these rejected proposals matched. No test modifies the student's ignored `backend/data/expedia_lite.db`.

After the code changes, the full backend suite passed **51 tests** with no resource warnings, the Vue production build passed, and `git diff --check` passed. The 51 tests and Vue build passed again after the feature branch was fast-forwarded into `main`. In the merged app, Codex's browser check showed the saved Scholar hotel for ZIP 16802, its map marker, and the October 10 $125.00/7-room edit. Earlier October 1 student screenshots, DB Browser observations, refresh, and Network-panel checks remain in [local hotel activity](local-hotel-activity.md).

## Git and remaining submission step

The student accepted the browser results and authorized committing, merging, and pushing. The implementation commit is `c40bc73898b2d80b25b791375ff1ea080c46513e`; `main` was fast-forwarded to it before the combined checks above. The final documentation update and push are still pending as this line is written. Canvas upload and TA/instructor demonstration remain student actions.

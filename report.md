# Expedia Lite - Assignment 2, Part 2 report

## Repository and setup

For Part 2, I kept working in my Vue, FastAPI, and SQLite travel app: [treyfoerster41-creator/IST-402-Project-1](https://github.com/treyfoerster41-creator/IST-402-Project-1). I built this part on `codex/assignment2-part2-rag` and merged it into `main`. My assessed implementation checkpoint is [c40bc73898b2d80b25b791375ff1ea080c46513e](https://github.com/treyfoerster41-creator/IST-402-Project-1/commit/c40bc73898b2d80b25b791375ff1ea080c46513e). I kept my [Part 1 report](https://github.com/treyfoerster41-creator/IST-402-Project-1/blob/main/docs/assignment-2-part-1-report-archive.md) in the repo instead of losing it when I updated this report.

To run the app, I create a Python virtual environment, install `backend/requirements.txt`, and start `uvicorn backend.app.main:app --port 8000`. In a second terminal I run `npm ci --prefix frontend` and `npm run dev --prefix frontend`, then open `http://127.0.0.1:5173` (Firefox also works). I keep `GEOAPIFY_API_KEY` and `GEMINI_API_KEY` in the ignored project-root `.env`, using `.env.example` as a key-free template. Neither key belongs in the frontend, report, recording, or Git. [README.md](https://github.com/treyfoerster41-creator/IST-402-Project-1/blob/main/README.md) has the full instructions. The backend health route reports only whether each key is configured.

## Research and early design

I started with my [Part 1 research](https://github.com/treyfoerster41-creator/IST-402-Project-1/blob/main/docs/assignment-2-part-1-research.md) and [map mockup](https://github.com/treyfoerster41-creator/IST-402-Project-1/blob/main/docs/assignment-2-part-1-mockup.svg). For this part, I looked at how Expedia lets people ask hotel questions, then checked the Gemini and SQLite documentation for the pieces I needed. I wanted the chatbot near the hotel results, but I did not want its answer to look like a real room offer. That is why the page says it uses saved, simulated data and lets me open the SQL, source rows, and checked stay total. My [research note](https://github.com/treyfoerster41-creator/IST-402-Project-1/blob/main/docs/assignment-2-part-2-research.md) has the sources and the choices I made.

I made this [early mockup](https://github.com/treyfoerster41-creator/IST-402-Project-1/blob/main/docs/assignment-2-part-2-mockup.svg) before building the chatbot. It shows the question box below the list and map, plus the loading, answer, no-match, and error states. As I built it, I added a section I can expand to see the SQL and rows, along with a table that checks the full stay. That makes it easier to tell whether the answer actually matches the saved data.

## What I built

The local hotel storage I finished on October 1 is still there. I can add or remove a Geoapify hotel, keep the ZIP I searched, and see five simulated nightly rows for October 10-14, 2026. A ZIP search checks saved hotels first and only calls the live API if there are no saved results. The chatbot uses those saved hotels; it is not searching every hotel near the ZIP. I also kept the earlier ZIP lookup, list and map, and fictional Assignment 1 booking data separate.

I can type a hotel question in Vue and see a loading state, an answer, or a clear no-match, insufficient-data, or error message. The question goes to `POST /api/hotels/ask`. FastAPI gives Gemini 3.5 Flash-Lite only the relevant local table structure and query rules, and Gemini suggests SQL. The backend checks that SQL before running it: one limited, read-only SELECT over saved hotels, their ZIPs, and the simulated nights. It rejects writes or unrelated reads and checks the returned values against the stored rows. Then it sends my question, the accepted SQL, the rows, and the checked stay summary to Gemini for an answer. Gemini never opens the database itself. I can see the answer and expand the SQL and rows in the page.

For a dated stay, checkout is excluded from billed nights. The backend itself checks that every night is present, sums cents, and finds the lowest room count. A missing night or zero rooms does not become an available stay. Rates and room counts are fictional classroom values; the chatbot makes no real booking or live-availability claim.

## Verification: expected and observed

I kept a [dated verification record](https://github.com/treyfoerster41-creator/IST-402-Project-1/blob/main/evidence/assignment-2-part-2-verification.md) so my browser recordings are not confused with Codex's checks or automated tests. The [fixed JSON sample](https://github.com/treyfoerster41-creator/IST-402-Project-1/blob/main/backend/tests/fixtures/assignment2_part2_saved_hotel.json) is made-up test data. I can rerun those tests with `.venv/bin/python -m unittest backend.tests.test_hotel_advisor -v`. They use a temporary database and mocked Gemini replies, so they do not reset my saved hotel.

| Input/action | Expected | Observed on October 6, 2026 |
| --- | --- | --- |
| Ask about saved ZIP `16802`, check-in `2026-10-10`, checkout `2026-10-12` | Gemini proposes a focused SELECT; the backend retrieves Oct 10 and 11; the second Gemini call uses those rows to answer. | I saw Scholar Hotel State College in the browser with a $225.00 two-night total and at least 7 rooms. I opened the SQL and saw two rows: October 10 was $125.00/7 rooms and October 11 was $100.00/20 rooms. Codex also checked both live model calls and the backend's 22500-cent total. |
| Ask about saved ZIP `00000` | No local match, not a provider error or invented hotel. | My browser recording shows the no-match message and a SELECT filtered to `00000`. Codex's live model check returned zero local rows. |
| Submit DELETE, an unrelated table read, multiple statements, or a fabricated rate as proposed SQL | Reject them before they can alter or misstate data. | Isolated synthetic tests rejected each proposal; temporary database bytes and row count stayed unchanged. This is a mocked/fixture safety test, not a malicious live-model response. |
| Simulate a missing required night or Gemini quota response | Missing data is insufficient; quota is a service failure, not “no hotels.” | Temporary-database and mocked-provider tests produced those separate outcomes. They are not live provider failures. |
| Search ZIP `16802` in the existing discovery UI | Saved local hotel and edited night remain after the chatbot addition. | Codex's browser check showed Scholar as the one saved hotel, its map marker, and the Oct 10 $125.00/7-room edit. Earlier student DB Browser, refresh, Add/Remove, and Network-panel checks are linked in [the local-storage activity record](https://github.com/treyfoerster41-creator/IST-402-Project-1/blob/main/evidence/local-hotel-activity.md). |

The live first-model query was:

```sql
SELECT h.hotel_id, h.name, h.address, z.zip_code, n.stay_date, n.nightly_rate_cents, n.rooms_available
FROM saved_hotels AS h
JOIN saved_hotel_zips AS z ON z.hotel_id = h.hotel_id
JOIN demo_hotel_nights AS n ON n.hotel_id = h.hotel_id
WHERE z.zip_code = '16802' AND n.stay_date >= '2026-10-10' AND n.stay_date < '2026-10-12'
LIMIT 40
```

The second Gemini request got my original question, the checked SQL, both rows, and the backend's 22500-cent total and minimum of 7 rooms. The answer matched the math: $125 + $100 = $225. Geoapify's live results can change, but this check used my one saved local hotel, not a fixed count of live places.

After merging into `main`, the automated checks passed again: **51 backend tests** and the Vue production build. `git diff --check` also passed. I checked the combined app in the browser: ZIP `16802` still returned my one saved Scholar hotel, its map marker, and the October 10 $125.00/7-room edit. The advisor tests use a synthetic temporary database, not my saved local hotel file. The fixed sample also contains a second synthetic hotel for a two-hotel comparison without changing my saved Scholar record.

I reviewed the new files in VS Code on October 6 and they looked good to me. I then tried the successful question in the browser and recorded the $225 answer, SQL, and two rows. I also recorded the ZIP `00000` question so the no-match behavior is visible. Finally, I ran the focused SQL safety test in VS Code's terminal; it finished with `Ran 1 test` and `OK`. Codex checked the clips for legibility and did not see an API key or `.env` contents. These are my manual browser and terminal actions; the 51-test suite and frontend build are separate automated checks.

My Part 2 demo is in three short clips: [the successful question, SQL, rows, and answer](https://psu.mediaspace.kaltura.com/media/t/1_mm1w7j33), [the read-only SQL safety test](https://psu.mediaspace.kaltura.com/media/t/1_nsgnwgsr), and [the ZIP `00000` no-match question and SQL](https://psu.mediaspace.kaltura.com/media/t/1_3m0srbwj). Codex opened all three MediaSpace pages while logged out and found playable videos without a sign-in prompt.

## AI assistance and evidence

I used OpenAI Codex (GPT-5) to help with research, design, coding, and checks. Gemini 3.5 Flash-Lite is the model the app calls at runtime. My selected [prompt record](https://github.com/treyfoerster41-creator/IST-402-Project-1/blob/main/prompts/006-assignment2-part2-rag.md) and [evidence log](https://github.com/treyfoerster41-creator/IST-402-Project-1/blob/main/evidence/evidence-log.md) show the main instructions, changes, checks, and a revised approach. Codex's first live model check was blocked by its restricted network; a later permitted backend-only request worked. I did not count a fluent answer alone as proof—the saved rows and checked stay math are shown with it.

This is the `report.md` I will upload for Assignment 2 Part 2 after the final Git push.

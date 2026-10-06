# Expedia Lite - Assignment 2, Part 1 report

## Repository and setup

I continued my local Vue, FastAPI, and SQLite travel app for this assignment. The repository is [treyfoerster41-creator/IST-402-Project-1](https://github.com/treyfoerster41-creator/IST-402-Project-1), and the hotel-discovery work is on branch `codex/assignment2-part1-hotel-discovery`. The implementation checkpoint is commit `571fa23`.

To run the app, I create and activate a Python virtual environment, install `backend/requirements.txt`, and start FastAPI with `uvicorn backend.app.main:app --port 8000`. In another terminal, I run `npm ci --prefix frontend` and `npm run dev --prefix frontend`, then open `http://localhost:5173`. For live results, I put `GEOAPIFY_API_KEY=...` in the ignored project-root `.env` file and restart FastAPI. I use `.env.example` as the key-free template. I never put the Geoapify key in frontend code or submit the `.env` file. The map uses OpenStreetMap tiles with attribution and no client key. Full setup instructions are in [README.md](../README.md).

## Research and design

I researched hotel list-and-map patterns using an Expedia-owned Egencia hotel guide, along with the Geoapify, Leaflet, and OpenStreetMap documentation. I used the list/map pattern to help travelers compare location, but did not copy commercial rates, ratings, or booking controls because Geoapify does not provide verified room inventory. My [research note](assignment-2-part-1-research.md) links these sources and explains the decisions.

Before implementation, I made an [early mockup](assignment-2-part-1-mockup.svg) of the ZIP form, results list, map, selection, and status messages. I kept the list and map side by side on wider screens and stacked them on smaller screens. The sketch includes loading, invalid, unresolved, empty, and failure states. I also added numbered keyboard-usable map markers, a 5 km circle, and a selected-place summary.

## How the application works

I kept the responsibilities separate. Vue handles the ZIP input, loading and error messages, results list, map, and selected hotel ID. FastAPI validates the ZIP, calls Geoapify, shapes the response, and returns safe errors. The frontend talks to API routes; it does not read CSV files or SQLite directly.

When I search, FastAPI first checks that the requested five-digit ZIP resolves to that exact U.S. postcode. It preserves leading zeros, so `02108` stays a ZIP string rather than becoming a number. Only after that match does the backend ask Geoapify for `accommodation.hotel` places within a 5 km circle centered on the returned coordinates. It does not use my device location or search the entire ZIP boundary.

The `GET /api/hotels/nearby?zip_code=16802` response includes the ZIP center, search radius, result limit, and up to 50 places with a provider ID, optional name/address, and valid coordinates. I label missing names or addresses instead of inventing them, and I omit places without usable IDs or coordinates. The interface distinguishes loading, results, invalid input, an unresolved ZIP, no returned places, and a failed request. The 50-place limit is not exhaustive. These live places are not bookable hotel offers and are not added to my fictional SQLite booking records. The persistent shortlist is for Part 2.

## My manual verification

I reviewed the changed project files in VS Code and manually exercised the running app in the browser after each implementation change, rechecking the affected behavior before moving on. I recorded a final walkthrough on September 29. I entered `11111` and `00000`; the app displayed an error for each instead of hotel results. I then searched `02108`, saw Boston-area places, selected a hotel, and zoomed and moved around the map. Finally, I searched `16802` and repeated the hotel-selection and map check in State College. The [recording is on Penn State Kaltura](https://psu.mediaspace.kaltura.com/media/t/1_hm69rmma).

In my live check on September 28, a direct request for `16802` returned HTTP 200 with State College as the matching ZIP center and 21 hotel places. In the browser, I saw the loading state followed by 21 list items and 21 map markers. I selected a place from the list and another from the map; both selections highlighted the same place in the other view. The map showed the ZIP center, 5 km circle, tiles, and OpenStreetMap attribution.

I also tried invalid `1680` and unresolved `00000`. The app cleared old results and showed the appropriate message instead of searching another place. For `02108`, it preserved the leading zero and centered results on Boston. The response reached the 50-place limit, and the interface said the list might not be exhaustive. A place without a name was labeled "Name not provided." My earlier ZIP lookup table and fictional Boston city search still worked. The [dated verification record](../evidence/assignment-2-part-1-verification.md) has the exact coordinates and expected-versus-observed results.

My browser checks were supplemented by automated checks: all **38 backend tests** passed, and the Vue production build passed. The tests use synthetic data and mocked provider responses for empty results, rate limits, timeouts, malformed data, duplicate IDs, missing fields, and no-fallback behavior. Mocks do not prove live API results. I did not record a browser demonstration of an empty-results or provider-failure simulation. Results are limited to 50 and depend on Geoapify coverage and tile-network availability.

My first map check showed a populated hotel list but a blank map because the circle bounds were fitted before the map had an initial view. Codex helped me initialize the map at the returned ZIP point before fitting the circle. I retested after that fix, and the tiles, markers, circle, and attribution appeared. The [evidence log](../evidence/evidence-log.md) records the correction.

## AI assistance and submission

I used OpenAI Codex (GPT-5) to help with research, the mockup, implementation, automated tests, and documentation. I approved installing `leaflet@1.9.4` after checking the existing environment. The [selected prompt excerpt](../prompts/004-assignment2-part1-hotel-discovery.md) links the assignment instruction to the design and implementation, and the [evidence log](../evidence/evidence-log.md) records the dependency retry and map correction.

I opened the Kaltura link in a private window and confirmed that the video loads without signing in. Before I upload this report to Canvas, I will make sure the recording does not show an API key, `.env` contents, or private browser information. The report includes the demo link; I will upload `report.md` for Part 1.

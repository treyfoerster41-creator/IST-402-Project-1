# Expedia Lite - Assignment 2, Part 1 report

## Project access and setup

Repository: [treyfoerster41-creator/IST-402-Project-1](https://github.com/treyfoerster41-creator/IST-402-Project-1). Assessed Part 1 implementation commit: `571fa23` on branch `codex/assignment2-part1-hotel-discovery`. The screen-recorded demonstration is linked below. Before submitting, confirm that the Kaltura page is viewable to the instructor.

The project continues the existing Vue, FastAPI, and SQLite travel app. From the repository root, create and activate a Python virtual environment, install `backend/requirements.txt`, and run `uvicorn backend.app.main:app --port 8000`. In another terminal, run `npm ci --prefix frontend` and `npm run dev --prefix frontend`, then open `http://localhost:5173`. For live results, put a Geoapify key in the ignored project-root `.env` as `GEOAPIFY_API_KEY=...`, then restart FastAPI. Use `.env.example` as a key-free template. Never upload `.env` or put its contents in frontend configuration. The map uses public OpenStreetMap tiles with visible attribution and no client key. Full instructions are in [README.md](README.md).

## Research and early mockup

The [dated research note](docs/assignment-2-part-1-research.md) links Geoapify Geocoding and Places documentation, Leaflet, OpenStreetMap's tile policy, and an Expedia-owned hotel-list/map reference. The reference's spatial comparison pattern was useful; its commercial rates and booking controls were inappropriate for Geoapify place data. Geoapify supplies hotel places and coordinates but not confirmed room availability, prices, or ratings. Leaflet needs a separate tile source and does not retrieve hotels.

The [early mockup](docs/assignment-2-part-1-mockup.svg), prepared before implementation on September 28, places a five-digit ZIP form and status area above a side-by-side hotel list and map. It sketches one highlighted place in both views and notes invalid, unresolved, empty, loading, and failure states. The implementation kept that design and added numbered, keyboard-usable map markers, a visible 5 km circle, a selected-place summary, responsive stacking, and an explicit 50-result cap. The earlier ZIP-only demonstration and fictional booking section remain below the new discovery screen instead of being removed.

## Part 1 implementation and MVC responsibilities

Vue owns ZIP text entry, state messages, list/map rendering, and one selected provider place ID. A list-button selection highlights its Leaflet marker; a marker click highlights and scrolls the corresponding list item. FastAPI owns exact five-digit U.S. postcode validation, backend-only Geoapify requests, data validation, and safe errors. The existing ZIP geocoding controller first requires the returned postcode to match the requested ZIP and country to be U.S.; only then does the new hotel controller call Geoapify Places for `accommodation.hotel` within a `circle:lon,lat,5000` centered on that returned point. Neither browser geolocation nor the whole ZIP boundary is used.

`GET /api/hotels/nearby?zip_code=16802` returns the validated ZIP center, 5 km radius, result limit, and up to 50 usable provider places. Each exposed hotel has a provider place ID, optional name/address, and valid coordinates. A missing name/address is labeled "not provided" in Vue. Unusable geometry/IDs are omitted; a wholly unusable nonempty provider response is an error, not an empty search. The UI distinguishes loading, results, invalid input, unresolved ZIP, zero returned hotels, and failed service requests. A 50-place page may not include every hotel in a dense area; coverage changes over time. No live place is offered as a bookable room or inserted into the fictional SQLite booking flow. Persistent shortlist actions are **Part 2 only**.

## Screen-recorded demonstration

The student supplied a shorter replacement recording for this submission. Per the student's description, it shows unresolved ZIPs `11111` and `00000`, a Boston search for `02108` with a selected hotel and map zoom, and a State College search for `16802` with a selected hotel and map interaction. Before submitting, confirm that the recording contains no API key, `.env` content, or private browser information. **Demo video link:** [Assignment 2 Part 1 video on Penn State Kaltura](https://psu.mediaspace.kaltura.com/media/t/1_hm69rmma). The separate dated live checks below document observed 16802 and 02108 responses.

## Verification and limitations

The [detailed expected-versus-observed record](evidence/assignment-2-part-1-verification.md) dates live checks to September 28, 2026. A direct backend 16802 request returned HTTP 200, State College as the exact ZIP center, and 21 hotel places on that date. In the browser, the same search showed a loading state followed by 21 list items and 21 map markers; selection worked in both directions, with visible tiles, radius, and attribution. `02108` retained its leading zero and returned a Boston-centered result at the 50-place cap. `1680` showed an invalid-input message; `00000` showed an unresolved-ZIP message instead of hotel results. The earlier fixed ZIP table and fictional Boston city search still worked.

All **38 backend tests** passed, including synthetic/mocked Places empty, rate-limit, timeout, malformed response, duplicate-ID, missing-field, and no-fallback cases; the Vue production build passed. Mocks do not prove live success, so the real observations are recorded separately. An empty or failed Places response was not captured in the browser; the backend handling was tested with mocks and the frontend state logic was reviewed. Results are limited to 50 and depend on Geoapify coverage and tile-network availability.

The first browser pass found a blank map despite a populated list: Leaflet circle bounds were calculated before a map view existed. Initializing the map at the returned ZIP point before fitting the circle fixed it; the browser then showed tiles, markers, circle, and attribution. This failed/revised approach is recorded in the [evidence log](evidence/evidence-log.md).

## AI disclosure and prompt trail

OpenAI Codex (GPT-5) assisted with research, the SVG sketch, backend/frontend implementation, mocked tests, browser verification, and this report. The student supplied the assignment and approved installation of `leaflet@1.9.4` after the existing environment was checked. The [selected prompt excerpt](prompts/004-assignment2-part1-hotel-discovery.md) links the main instruction to the research, code, and verification decisions; the [evidence log](evidence/evidence-log.md) records the dependency retry and map-initialization correction. Commit `571fa23` is the implementation checkpoint; the report and demo link are included on branch `codex/assignment2-part1-hotel-discovery`. The student must verify Kaltura access and upload `report.md` to Canvas.

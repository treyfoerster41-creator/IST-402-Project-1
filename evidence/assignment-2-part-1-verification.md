# Assignment 2, Part 1 - verification record

Observed on 2026-09-28 in the local Vue app (`127.0.0.1:5173`) and FastAPI (`127.0.0.1:8000`). Live hotel counts are dated observations, not fixtures or promises. No key or `.env` content appears here.

| Input or action | Expected | Observed |
| --- | --- | --- |
| Direct backend `GET /api/hotels/nearby?zip_code=16802` | Exact U.S. ZIP center; Geoapify hotel places within a 5 km circle; capped response | HTTP 200. Center was ZIP 16802, State College, 40.803167822, -77.861384958. 21 places returned with provider IDs and coordinates; first was Scholar Hotel State College. |
| Search `16802` in Vue | Loading then populated list and map using the same returned places | Loading message and disabled form appeared. Then 21 list items and 21 numbered markers appeared. Map tiles, 5 km circle, ZIP-center dot, and OpenStreetMap attribution were visible. |
| Select Scholar Hotel State College in list | Matching marker becomes selected | The list control changed to selected; exactly one marker and one list item carried selected styling. Summary named Scholar Hotel State College. |
| Select marker 3 | Matching list item becomes selected | Nittany Lion Inn became the selected list item and summary; prior Scholar selection cleared. |
| Enter `1680` | Client rejects invalid ZIP without stale results | The app showed the exact-five-digit instruction; old list/map results cleared. |
| Enter `00000` | Unresolved requested ZIP, not a different-location hotel search | The app showed "No matching U.S. location was found for this ZIP code"; no hotel results appeared. |
| Enter `02108` | Preserve leading zero and return places around the resolved point | The app displayed ZIP 02108, Boston center 42.357581412, -71.065946589. The response reached the 50-place cap; the UI explicitly said results are not exhaustive. One unnamed provider record displayed "Name not provided." |
| Earlier fixed ZIP button | Existing ZIP-only demonstration still works | ZIP 16802 returned its location in the labeled table. |
| Earlier fictional Boston city search | Existing local-record flow remains available | Four offered stays appeared. No live place was inserted into booking history. |

## Synthetic and automated checks

- `backend/tests/test_hotel_discovery.py` uses only synthetic keys, locations, and mocked Geoapify responses. It checks 5 km circle parameters, cap, exact-ZIP prerequisite, leading zeros, empty success, optional fields, duplicate IDs, unusable features, rate limit, timeout, malformed response, and safe route errors. These mocks do **not** prove live provider success; the dated live checks above do.
- Full backend suite: **38 tests passed** on 2026-09-28. Frontend `npm run build --prefix frontend` passed after approved Leaflet installation. `npm ls leaflet --prefix frontend --depth=0` confirmed `leaflet@1.9.4`.
- `.env` is ignored by `.gitignore`; the health/configuration check reported only "key is configured." This proves presence, not validity. Successful live requests separately demonstrate that the configured key worked on the observation date.
- The first browser run exposed a real failure: Leaflet's 5 km `getBounds()` ran before the map had a starting view, leaving a gray map while the list loaded. Adding `setView(center, 12)` before circle fitting fixed it. A reload then showed tiles, markers, circle, and attribution; list-to-map and map-to-list selections were retested.

## Limits and remaining submission steps

- Places coverage and fields vary. The app requests at most 50 features and does not paginate; dense ZIPs can have additional places. A returned feature without a usable point geometry or provider ID is omitted; if all returned features are unusable, this is a service-data error, not a successful empty result.
- Empty Places responses, provider failure, timeout, and rate limit are covered by mocked backend tests. Invalid and unresolved cases were also checked in the live browser; a browser demonstration of a simulated empty/failure response was not recorded.
- The student confirms manually reviewing changed files in VS Code and rechecking the app in the browser after implementation changes. The student also confirmed that the Kaltura video loads in a private window. The demo link is in `report.md`, and the Assignment 2 Part 1 branch has been pushed. Canvas upload remains the student's step.

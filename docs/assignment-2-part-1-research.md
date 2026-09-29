# Assignment 2, Part 1 - research and early design

Prepared before implementation on 2026-09-28. The [early mockup](assignment-2-part-1-mockup.svg) shows the intended ZIP search, list/map pairing, selection, and status area. It is a design sketch, not a screenshot of working code.

## Sources and decisions

| Source | Useful pattern or constraint | Weakness or omission for this project | Decision |
| --- | --- | --- | --- |
| [Expedia-owned Egencia hotel guide](https://media.expedia.com/media/content/expcorp/graphics/docs/traveler_guide_to_hotels_on_egencia.pdf) | A hotel-results list can be paired with a map for spatial comparison. | Its rates, star ratings, and booking controls assume commercial inventory unavailable from Geoapify. The guide is dated. | Pair a compact list with a map, but show only returned place names, addresses, and coordinates. Do not copy booking claims. |
| [Geoapify forward geocoding](https://apidocs.geoapify.com/docs/geocoding/forward-geocoding/) | Structured postcode search, U.S. filtering, and returned coordinates. | A provider suggestion can differ from the requested ZIP. | Reuse the existing exact U.S. postcode validation before any hotel request. |
| [Geoapify Places API](https://apidocs.geoapify.com/docs/places/) | `accommodation.hotel` category and a `circle:lon,lat,5000` filter; response is a GeoJSON FeatureCollection with place identifiers and optional name/address fields. | A limited result page is not exhaustive inventory, and optional fields can be absent. | Request a capped result set from the returned ZIP point, disclose the cap, omit features without valid coordinates or a place ID, and label missing names/addresses honestly. |
| [Leaflet reference](https://leafletjs.com/reference.html) | Markers support click and keyboard focus; map view can fit returned points. | Leaflet does not supply the hotel data or tile imagery. | Keep a single selected place ID in Vue and synchronize list buttons and markers. Load map tiles separately with visible attribution. |
| [OpenStreetMap tile policy](https://operations.osmfoundation.org/policies/tiles/) | Normal interactive tile requests are permitted with visible attribution and correct HTTPS tile URL. | No bulk download, prefetching, or production availability guarantee. | Use only interactive browser tile loading for this local classroom app; no tile credential or prefetch. |

## Intended states and responsibility split

- Initial: ZIP field and an explanation; no results or map markers yet.
- Loading: disable repeat submission and clear stale results.
- Results: show the resolved center and returned hotels within a 5 km circle. One selected place ID highlights the matching list row and marker in both directions.
- Invalid input: five ASCII digits are required; leading zeros are preserved.
- Unresolved ZIP: no request for hotels and an explicit unmatched-ZIP message.
- Empty Places response: a successful search with no returned hotels, distinct from a failed request.
- Provider failure or quota response: an error, never described as an empty search.

Vue owns form state, selected ID, and presentation. FastAPI owns validation, the geocoding and Places requests, response shaping, and safe errors. The existing booking/SQLite section remains separate from live hotel discovery. Part 2's persistent shortlist is intentionally not in this Part 1 mockup or implementation.

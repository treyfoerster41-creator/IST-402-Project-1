# ZIP lookup activity - design and research

Scope: complete and extend the public API demonstration in the existing travel
app. This is not the full Assignment 2 implementation. No hotel discovery, map,
shortlist, payments, or real traveler records are added.

## Research and early panel sketch (2026-09-23)

Before implementation, inspected [Geoapify's forward-geocoding documentation](https://apidocs.geoapify.com/docs/geocoding/forward-geocoding/)
and [its location-search demo](https://www.geoapify.com/geocoding-api/#demo).
The demo pairs a text field with an explicit Geocode action. We use that pattern
with a ZIP-only field and submit button, rather than requesting on every keystroke.
The provider supports structured postcode search, a U.S. country filter, JSON
results, and latitude/longitude fields; optional locality data may be missing.

Early panel sketch:

```text
ZIP LOOKUP DEMONSTRATION             Backend key configuration status
U.S. ZIP code [16802] [Look up ZIP]   [Look up ZIP 16802]
Hint: five digits; keep leading zeros.
Loading / useful error / lookup completed for requested ZIP
| ZIP | Locality | Country | Latitude | Longitude |
| returned data, only after a successful request  |
Powered by Geoapify + data-source attribution
```

The final panel keeps the original fixed button to make that milestone repeatable.
The input uses text, not number, so leading zeros survive. Editing it clears an
old result; both actions and the input are disabled during lookup. A caption
identifies the returned ZIP. Missing locality is shown honestly as not provided.

## Responsibility and request trace

1. `frontend/src/components/ZipLookup.vue` owns input, loading, errors, and table.
   It sends only ZIP data to our local API through Vite's existing proxy.
2. `backend/app/main.py` has a fixed `GET /api/demo/zip-location` route for 16802
   and an entered-value `GET /api/zip-location?zip_code=16802` route. Thin routes
   translate controller failures into safe HTTP errors.
3. `backend/app/geoapify.py` validates five ASCII digits and requests the fixed
   Geoapify geocoding endpoint with `postcode`, `type=postcode`,
   `filter=countrycode:us`, and `format=json`. It uses a finite HTTP timeout.
4. `backend/app/config.py` uses its own file path to load the root `.env` with
   python-dotenv. Process environment takes precedence; restart after edits.
5. The controller accepts only a matching U.S. postcode with valid finite
   coordinates, then returns an allowlisted location object. No provider URL,
   key, query object, or raw exception is returned to Vue.

The health endpoint retains `status` and adds `geoapify` configuration text only.
Configured does not prove the key is valid; only the live lookup proves success.
Invalid ZIP, missing configuration, unresolved ZIP, provider failure, and timeout
are distinct outcomes. Automated provider tests use mocks, not real quota.

Location lookups do not read or write SQLite. Existing fictional city search,
booking, cancellation, deletion, and one-time CSV seeding remain unchanged.

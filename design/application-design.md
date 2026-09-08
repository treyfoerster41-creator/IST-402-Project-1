# Stayfinder application design

## Product boundary

Stayfinder is a local learning prototype for one traveler booking one room at one of a few synthetic hotels. A traveler searches a fixed destination, picks an available result, supplies contact details, and receives a simulated confirmation. The traveler can then review saved bookings.

Out of scope: payment, cancellation, authentication, multiple rooms, live availability, real travel inventory, external APIs, and emails.

## Four-layer decomposition

| Layer | Responsibility in this prototype | Evidence in the interface |
| --- | --- | --- |
| Interface | Search form, result cards, booking form, confirmation view, history view, empty/error/loading messages | Inputs, buttons, price cards, confirmation number, and saved-booking cards |
| Logic | Match a supported destination, require valid dates and traveler details, compute nights and total, create IDs, reject malformed booking requests | Validation message, computed total, and confirmation outcome |
| Data | Synthetic hotel catalog; selected hotel, destination, date range, traveler, price, booking ID, status, and timestamp | Hotel names, ratings, nightly prices, trip dates, guest name, and confirmation number |
| Persistence | Server reads/writes bookings to `server/data/bookings.json`; seed hotel catalog remains source-controlled | Booking stays available after refresh and normal server restart |

### Data model

```text
Property
  id, name, city, rating, reviewCount, nightlyRate, refundable, amenities, imageAlt

Booking
  id, confirmationCode, propertyId, propertyName, city,
  checkIn, checkOut, travelerName, travelerEmail,
  nights, nightlyRate, total, status, createdAt
```

All records are synthetic. `Booking` snapshots the display-critical property values so history remains understandable even if the seed catalog changes later.

## Frontend/backend contract

| HTTP request | Server responsibility | Client use |
| --- | --- | --- |
| `GET /api/properties?destination=...` | returns the three synthetic properties only for `Asheville`; otherwise returns an empty list | render results or no-results feedback |
| `POST /api/bookings` | validates payload, finds property, calculates nights/total, creates confirmation, persists booking; returns `201` or `400` with safe field errors | show field/general error or confirmation screen |
| `GET /api/bookings` | reads persisted booking records, newest first | render history or empty-history state |

The client never writes the data file or generates a confirmation/total. Those values always come from the server response.

## Flow 1 — make a simulated booking

```mermaid
flowchart TD
    A[Search view: destination and dates] --> B{Client fields present?}
    B -- No --> C[Client shows required-field guidance]
    B -- Yes --> D[Client requests matching properties]
    D --> E{Results returned?}
    E -- No --> F[No-results state with change-search action]
    E -- Yes --> G[Results view: choose a property]
    G --> H[Booking view: traveler name and email]
    H --> I[POST booking request to server]
    I --> J{Server validation passes?}
    J -- No --> K[Show server validation error; preserve form]
    J -- Yes --> L[Server calculates total, saves JSON record]
    L --> M[Confirmation view: code and booking summary]
```

| Step | Interface | Logic | Data | Persistence |
| --- | --- | --- | --- | --- |
| Search | collects destination and dates | basic required-field check | query values | none |
| Results | renders selectable cards/no-results state | destination matching | property catalog | none |
| Booking | collects traveler info and summarizes selection | validates traveler/date/property; totals nights × rate | selected property and payload | none until valid submit |
| Confirmation | displays returned booking | creates ID and confirmation code | completed booking | append to JSON file |

### Flow 1 failure cases

- Missing destination, dates, traveler name, or email: form remains open and explains the missing/invalid value.
- Checkout on or before check-in: server rejects it; no booking is stored.
- Unknown property or unsupported destination: server rejects/returns no results; no booking is stored.

## Flow 2 — review booking history

```mermaid
flowchart TD
    A[Traveler opens Booking history] --> B[Client requests GET /api/bookings]
    B --> C{Stored records?}
    C -- No --> D[Empty-history view with Book a stay action]
    C -- Yes --> E[History cards: confirmation, hotel, dates, total, status]
    E --> F[Traveler inspects a booking record]
```

| Step | Interface | Logic | Data | Persistence |
| --- | --- | --- | --- | --- |
| Open history | navigation and loading state | asks server for newest-first records | booking collection | reads JSON file |
| Empty result | clear next action | recognizes zero records | empty list | no change |
| Saved results | cards and booking details | ordering/formatting | booking snapshots | records survive refresh/restart |

## Storage lifetime

The server owns `server/data/bookings.json`. Browser refresh does not clear it because history is fetched from the server. A normal server restart also preserves records because the server reloads the same JSON file. Resetting that file to an empty JSON array clears the prototype. This behavior was browser-verified in the implementation branch.

## Technology decision rationale

React/Vite keeps the visible flow organized into small reusable components without imposing a large framework. Express keeps the API and business rules explicit and inspectable. JSON over HTTP makes the client/server boundary visible in browser developer tools. A JSON file is sufficient for a single-user synthetic classroom prototype and makes persistence concrete; it is not appropriate for concurrent or production use.

## Implementation and verification status

1. React/Vite client and Express server have been created.
2. The server returns a source-controlled synthetic Asheville catalog.
3. Booking validation, total calculation, confirmation creation, and JSON persistence are implemented on the server.
4. The client has results, selection, booking, confirmation, history, empty, and error states.
5. Five automated checks pass: three validation tests plus two API/persistence tests. The production client build passes.
6. Browser verification demonstrated a successful booking, persisted history after refresh, empty history, and server-returned required-field errors.
7. The reviewed feature branch was merged to `main` and pushed at merge commit `b98bf81`. The next submission step is a brief screencast of the verified flows.

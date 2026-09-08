# Expedia reference observations and interface sketch

## Reference

- Product observed: [Expedia Hotels](https://www.expedia.com/Hotels)
- Accessed: September 8, 2026
- Method: public page inspection; no login, reservation, payment, or personal information used.

## Observed interaction patterns

The public Expedia hotel page presents a stay-search form with three high-level decisions: **where to go**, **dates**, and **travelers/rooms**, followed by a search action. Its hotel content emphasizes result cards carrying property identity, rating/review evidence, price, and stay-policy information. The public page also describes filters, sort controls, and fully refundable stays.

These observations inform Stayfinder’s structure, but not its visual identity or copy. Stayfinder intentionally reduces the scope to one supported city, a few synthetic properties, no filters/sorting controls, one room, and a simulated confirmation.

## Interface sketch for the planned prototype

```text
┌────────────────────────────────────────────────────────────────┐
│ Stayfinder                                      My bookings     │
├────────────────────────────────────────────────────────────────┤
│ Find a stay                                                    │
│ [ Destination             ] [ Check-in ] [ Check-out ] [Search]│
├────────────────────────────────────────────────────────────────┤
│ Stays in Asheville                                              │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ [image placeholder]  Blue Ridge Lodge     ★ 4.6 (312)       │ │
│ │                      Free cancellation   $145 / night       │ │
│ │                                        [Select stay]        │ │
│ └────────────────────────────────────────────────────────────┘ │
│ (two additional synthetic result cards)                         │
└────────────────────────────────────────────────────────────────┘

Selection → traveler form → confirmation code
My bookings → empty state OR saved booking cards
```

## Design decisions where the reference is silent

| Decision | Stayfinder rule | Reason |
| --- | --- | --- |
| Inventory | Three source-controlled synthetic Asheville hotels | Keeps the feature demonstrable without external data or credentials. |
| Availability | Every seed property is bookable for valid future dates | Avoids misleading real-time availability behavior. |
| Total | nights × fixed nightly rate; taxes/fees excluded and labeled | Keeps the calculation easy to verify. |
| Booking identity | Server returns a generated confirmation code | Demonstrates backend responsibility without a real reservation system. |
| History | Records appear newest first and are readable after refresh | Directly fulfills the connected-history requirement. |
| Reset | Deleting the local JSON booking file clears history | Makes persistence lifetime explicit. |

## Attribution

Expedia’s public page is referenced solely for observable travel-search patterns. No Expedia screenshots, assets, listing details, trademarks, or private data will be included in the product interface. Any original application screenshots captured for Part 2 will be labeled as Stayfinder local-prototype evidence.


# Selected instruction - October 1 local hotel storage activity

Source: user-provided graded activity and instructor demonstration text on October 1, 2026. This is a concise, redacted record of the material requirements, not a claim that the student has completed the manual checkpoints.

1. Preserve the completed Assignment 2 Part 1 ZIP resolution, Geoapify hotel search, and synchronized Vue list/map, plus the Assignment 1 SQLite tables and records.
2. Add `saved_hotels` with exact provider ID, optional name/address, and coordinates. Add a ZIP/location association. Add `demo_hotel_nights` with a hotel/date key, hotel foreign key, and nonnegative integer defaults of 10000 cents and 20 rooms.
3. Save an API place using **Add to Local** and create only five October 10-14, 2026 nights. Repeated saves must not duplicate or overwrite existing nights. **Remove from Local** must cascade related rows but preserve unrelated records.
4. Search local storage first. Show stored hotels and dated simulated values with **Saved locally**. Only a successful empty local result may fall back to the existing Part 1 endpoint and show **API results**; a failed local request is an error.
5. The student manually inspects the database and browser Network panel, edits a saved hotel's cents/rooms in DB Browser, clicks **Write Changes**, reruns the ZIP search, and records expected versus observed behavior. Automated checks must be labeled separately.
6. Stop after the dated database edit and frontend reread. No chatbot, RAG, or model integration is required. Keep keys and `.env` content out of Git and evidence.

Implementation: [saved-hotel backend](../backend/app/saved_hotels.py), [Vue hotel discovery](../frontend/src/components/HotelDiscovery.vue). Verification status: [activity evidence](../evidence/local-hotel-activity.md).

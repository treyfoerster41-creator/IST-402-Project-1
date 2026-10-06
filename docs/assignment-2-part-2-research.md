# Assignment 2, Part 2: research and early design

Prepared October 6, 2026, before the chatbot implementation. The [early mockup](assignment-2-part-2-mockup.svg) is a design sketch, not a screenshot of working software. This builds on the [Part 1 research](assignment-2-part-1-research.md) and the October 1 local-storage activity.

## Sources and decisions

| Source | Useful pattern or rule | Weakness or limit | Decision for Expedia Lite |
| --- | --- | --- | --- |
| [Expedia Trip Matching](https://www.expedia.com/tripmatching) and [Expedia AI terms](https://www.expedia.com/legal/ai-terms) | Travelers can refine hotel ideas through questions; Expedia warns that AI answers can be mistaken. | Its commercial booking suggestions and inventory are outside our classroom data. | Use a compact question panel beside the saved-hotel workflow, label results as based on saved local data, and show the records behind each answer. Do not add booking claims to the chat. |
| [Gemini API reference](https://ai.google.dev/api), [model catalog](https://ai.google.dev/gemini-api/docs/models), and [pricing](https://ai.google.dev/gemini-api/docs/pricing) | Backend REST `generateContent` accepts a private `x-goog-api-key`; `gemini-3.5-flash-lite` is listed with a free text tier. | Availability and free quotas can change by project; model prose and SQL can be wrong. | Use one configurable Gemini model for two backend requests. Check live access and never trust a proposed query or answer without local validation. |
| [SQLite authorizer](https://www.sqlite.org/c3ref/set_authorizer.html) and [Python sqlite3](https://docs.python.org/3/library/sqlite3.html) | A connection can deny disallowed SQL while compiling it. | A prompt telling the model to write safe SQL is not an enforcement boundary. | Open the database read-only, enable `query_only`, allow only `SELECT` and reads of the three local hotel tables, cap rows and execution, and test attempted writes and unrelated-table reads. |

## Interaction and states

The traveler asks about **saved local hotels**, such as a ZIP and dates. The panel presents one question at a time with an example prompt, a loading message, a grounded answer, and a disclosure that rates and room counts are simulated. An expandable evidence area shows the proposed SQL and returned rows for instructor verification. If no row matches, the answer states that no saved local match was found. Provider errors and rejected queries receive separate messages. The interface does not imply that every nearby API hotel is in local storage.

For a stay from October 10 to October 12, the nights are October 10 and 11; checkout is excluded. A hotel with a missing night or no rooms on either night cannot be described as available for that stay. The backend will validate query access and bound results. The second model prompt will be limited to the retrieved rows and original question. We will compare a live answer with the rows in the verification record.

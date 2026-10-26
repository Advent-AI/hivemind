# D184: inspect the returned Idea analysis

Alex asked what the clipped Idea paragraph is and whether the complete reasoning trace can be shown. It is `reading.summary` from the second Idea call. Census: one card renderer truncates that summary to five lines; zero Idea detail views expose `reading.parts[].why`, search records, context choices or dropped choices. The current cached response has three parts and ten selected theses. The API already returns these records, so no model/backend change is needed.

Expose a View analysis button on a completed Idea card. A shared-style sliding drawer shows the full returned summary, each part and its explanation, direct/driver/context choices, searches and candidate names, dropped choices, and expandable structured response data. These are the returned explanations and service trace; the configured model does not return private internal reasoning. Do not invent intermediate reasoning or a reason for an unselected candidate.

| State / event | Result |
|---|---|
| Pending or failed request | No analysis action for an unfinished response |
| Completed response | Action opens the response attached to that card; no new request |
| No recorded coverage / no chosen theses | Show the actual empty-response state and available explanation |
| New submit, Library navigation, page close | Close the old drawer; stale results cannot reopen it |
| Close, Escape, scrim | Shared slide animation; focus returns to opener |
| Missing candidate bundle | Show its stored ID as unavailable, never invent a title |
| Several instances | Instance-owned events and no duplicated element IDs |

| Value | Writer | Reader |
|---|---|---|
| Summary, part definitions, explanations and selected fit | Existing Idea response | Full text in drawer, summary preview on card |
| Candidate IDs / search queries / dropped reasons | Existing service trace | Collapsible trace and response details |
| Immutable thesis titles | Loaded canonical library | Resolve names only; no new selection, score or link |
| Active response | Page controller | Open/close drawer lifecycle |

New paths retain existing escaping and shared drawer motion. Native button makes the action accessible without changing canvas drag. Use real stored Idea fixtures for complete-text/part/search/null checks and one truncation mutant. Verify the cached current response in-browser, including close/reopen and new submission. No paid call, prompt change or database write is required. D130 owns components, D138 links and D182 presentation; D184 adds this read-only inspection.

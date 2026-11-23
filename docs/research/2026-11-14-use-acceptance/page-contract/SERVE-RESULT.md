# The product's API serving a new-system store to the page (D572), 2026-11-16, $0

Store: a copy of the closing replay's store (the extension draw judged through the accepted loop to 2027-04-02, D567; source path in
the scratch run's `source-closing.txt`), 7 questions. The API (`scripts/hivemind_api.py --lexical --config ''`, no model or
embedding call) on a free local port; stopped afterwards. Saved output: `serve-check.txt`.

- `/days`: 2026-09-22 to 2027-04-02.
- `/library` at 2026-09-28, 2027-01-30, 2027-01-31 and 2027-04-02 equals `bundle.library` read directly from the store (4 of 4).
- v3, v4 and v7 are open on 2027-01-30 and closed on 2027-01-31, their due day; v6 (due 2028-03-24) is open on 2027-04-02;
  `/thesis-bundles` carries v7 as an event and v5 as a figure with `n/a`. Cross-origin headers present.
- **The page reading the API:** a page built with the fortnight's 12 questions embedded, pointed at the API by `data-api`, rendered
  in headless Chrome, replaced them with the API's 7: the four events titled "Current outcome" with neutral chips (Yes, Still open),
  the theme range "Current range" with a neutral range chip, the two company figures "AI score" with "−2 Strongly bearish" (negative).
- Observed on the way (existing behaviour, not a defect of this slice): when the live library replaces the embedded one, the page
  keeps its date if the new history contains it, else moves it to the nearest end; a page shell embedding production's ledger (last
  day 2026-08-28) therefore opened the new library at 2026-09-22, where 2 questions exist. A failed live read is silent (the embedded
  snapshot stays), so a check must embed a different dataset to show the live read happened, as this one did.

**Not covered:** the Idea planner on a new-system ledger (open); a person's view of the page; a long-running service.

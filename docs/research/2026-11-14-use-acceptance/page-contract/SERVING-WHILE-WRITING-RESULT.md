# Serving while a stored replay writes (D573), 2026-11-16, $0

`serving_while_writing.py` → `serving-while-writing.txt`: the extension draw judged through the accepted loop into a new scratch store
to 2027-04-02, answered from its archive; the API (no model or embedding call) and a fresh page read the store at seven pauses.

**Held:** inside 2026-09-25, before its judging round, `/library` equals what the API served right after 2026-09-24 completed (no
partial day leaks into the completed-day view); right after 2026-09-25 completed it is as of 2026-09-25; on 2027-01-31 before its
closing it equals the 2027-01-30 view; after 2027-01-31 completed its three due questions are closed on that day.

**Two findings (the checks written before the run failed on them; neither is a defect of this slice's code):**
1. **The first day.** Before any day has completed, `/library` answers with the day in progress (as of 2026-09-22, two questions with
   that day's judgements) while `/days` gives no first or last day: `service.default_as_of` falls back to the latest judgement's day
   when no day is completed. On a store being written, the first day's partial state is served as a view.
2. **The page's date when the live library arrives.** A fresh page during 2026-09-25 showed 2 questions (the library as of
   2026-09-22) instead of the 5 of the last completed day: the page keeps the embedded snapshot's date when the live library replaces
   it, clamped to the new history (`library.setDataset`, verified as designed by `verify-library.mjs`, "library day clamps before
   replacement"). The page shell here embedded production's ledger (last day 2026-08-28), so the date went to the new library's
   first day. In any deployment whose shell is built on one day and opened on a later one, a fresh page opens on the shell's day, not
   on the latest completed day; production's served ledger is sealed, so this never showed. `docs/poc/thesis-ui.md` says "The supplied
   snapshot defines the displayed date" and "Automatic API loading keeps the current snapshot when unavailable" (the silent keep on a
   failed read is as specified).

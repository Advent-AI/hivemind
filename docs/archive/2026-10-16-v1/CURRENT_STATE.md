# Current state

As of 2026-10-16. The design lives in `docs/system-design.html` (New tab); decisions D1–D20 in `docs/DECISIONS.md`.
The work is an architecture POC before the PRD: design page and DECISIONS only, no code.

## Status

- Sealed copy of v1: `docs/archive/2026-10-16-v1/` (checksums in `SHA256SUMS`).
- PRDs (D20): one per module in `docs/prd/` (index `README.md`), viewable from each module on the design page.
  After editing a .md, run `python3 docs/prd/build_bundle.py`; `--check` finds a stale bundle.
- Frozen v1 (D19): everything up to classification — the research universe, the Input classification contract,
  Config, dispatch and the human review pool. A change needs a new decision and a re-run of the simulation or the
  boundary reasoning.
- Boundary (D10): the system consumes a stream of classified items: dispatch (the single entry, D17) → code processing
  or model extraction → research store. Upstream supply and classification are outside, discussed later. Testing is a
  test feeder streaming a test database through the same path. Not the old system's pull-by-date batch design.
- Two modes (D14): stream mode, driven by arriving information and never by the calendar (D12, D13), designed now;
  pull mode (an agent checks ladders and evidence at a due date or on cron), designed later.
- One switch (D18): the universe states what is researched and which tags each object tracks; the supply scope is
  objects × tracked tags; every item that arrives is processed. Config holds only the extraction policy.
- Research store: processing records and facts attached to objects; no copy of materials (D7). Not designed yet.

## Open defects

- `simulate_classification.py` resolves a ticker on the UTC date of `published_at`; the page says the New York
  publication day (D9). It has no cases for the macro rules (D15) or for crypto, commodity and theme objects (D11).
  The script is not changed at the POC stage.

## Next task

To be chosen by Alex. Candidates: what a fact in the research store looks like; the theme library's concrete themes.
Deferred by Alex: text extraction policy; upstream supply; pull mode; the review pool's mechanism.

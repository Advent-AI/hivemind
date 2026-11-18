# Council mp: the full run (D448: "the full run only by a separate decision after the slice is read")

**What the slice showed** (`clean-arch/e2e-comparison-2026-11-13/SLICE-RESULT.md`, every answer read): the wiring works live; both draws
completed in 8 minutes; 60 ledger lines all attributed, summing exactly to the ledger ($0.1593); Step 1's ledger equals its archive; no
stop, refusal or retry. Two theses, two sound ladders, two judgements on the evidence shown; production one view. Nothing in it argues
against the full run; it did not exercise passes 2–3, many theses, the judge over many days, or any reading.

**Proposal (the run D447 decided; its purpose and decision rules are WIRING-DESIGN.md §E, unchanged):**
- `poc/data/clean-e2e-full-2026-11-13/` (new), a new ledger with ceiling **$14.84** ($15.00 − the slice ledger's final spent $0.1593 −
  its reserved ≈ $0; the slice's launchers have ended and its ledger holds no launcher).
- Six launchers at once after a machine and network check, each detached with its log and pid file: `run_fresh.py clean` for `c1`,
  `c2`, `c3` (`--until-day 2026-07-14 --passes 3`) and `run_fresh.py prod` for `p1`, `p2`, `p3` (`--until-day 2026-07-14`), all on that
  ledger. The sends fall on 2026-11-13.
- Projection (estimate from the slice's per-item rates and the stored runs): about $10.4 of ledger; Step 1 about 2 h 20 min a clean draw
  (sequential within a draw, the three in parallel); the whole run about 2.5 h.
- Stops: D449's rules; any stop is read before anything else is sent; a redo only by a recorded council decision with `--redo-reason`.
  No edit to code or prompt files while it runs.
- After it, in order: the per-component spend and time (`spend_by_component.py`); every trace read by Claude (the opened theses and their
  articles, the ladder answers of the three passes, every judgement with its evidence shown, production's views and judgements); then a
  reading plan for §E's lines (the census by MATCHING-v2; Stage A's reading procedure on every answer of the three passes; Stage B with
  D429's every-judgement reading by both families), reviewed by the council before any reader runs. Lines whose reading cannot be completed
  are reported not measured.
- Spend under D439 would reach about $17.7 of $40.

**My own doubts, for you to test:** (1) six launchers at once: production's 16 extraction workers × 3 beside three sequential Step 1
draws; the earlier measurements ran three at a time; (2) the reading load is large (Stage B historically 13–18 reader-hours for 210–360
judgements); the run is worth sending only if the readings will be done, else the lines are not measured; (3) whether the clean draws'
judge cap per draw (local cap = the ledger's ceiling) and Stage B's own redo inside `run_stage_b` behave as intended over 14 days (the
slice judged one day).

Agree to launch exactly this, or say what to change.

End with: "Council position: <launch the full run | change ... first>".

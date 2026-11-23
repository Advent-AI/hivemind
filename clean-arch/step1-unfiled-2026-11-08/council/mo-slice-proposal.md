# Council mo, the slice (D448: "the slice only after the code review, by its own decision")

**Proposal.** One fresh day through the wired path, live, as a wiring check (WIRING-DESIGN.md §G): not a draw, not evidence of quality.

- **Folder and ledger:** `poc/data/clean-e2e-slice-2026-11-13/` (new); `budget_replay.py --init-ledger <folder>/ledger.json --ceiling 1.50`.
- **Runs, at the same time, each detached with its log and pid file, after a machine and network check** (load, free disk, the provider
  hosts answering an unauthenticated HTTPS request):
  - `run_fresh.py clean --root <folder> --label s1 --ledger <ledger> --until-day 2026-07-01 --passes 1` (Step 1 c8 on the 13 items of
    2026-07-01 from an empty library → Steps 2–3 → cases → the ladder step, one pass → the frozen judge);
  - `run_fresh.py prod --root <folder> --label sp1 --ledger <ledger> --until-day 2026-07-01` (v118 on the same day).
- **Expected spend** (estimate from the stored runs' tokens at `model.PRICES`, the ledger's conservative charges): about $0.15–0.20 of
  ledger (Step 1 ≈ $0.12, Step 2 ≈ $0.02, ladder ≈ $0.005, judge ≈ $0.01, production ≈ $0.01). Spend under D439 so far $7.11 of $40.
- **Stops:** the ledger's $1.50 ceiling and every D449 rule. Any stop is read before anything else is sent; no relaunch without a
  recorded council decision; a redo only with `--redo-reason` after reading the component's output.
- **What it decides:** whether every component runs live through the wiring (real sends, real usage settled on one ledger), the time per
  component, the ledger's charge per component against the recorded cost, and any failure the $0 proofs could not show (provider errors,
  usage shapes, timeouts). It does not decide quality and is not compared with any draw.
- **What I read after it, myself:** every Step 1 answer beside its article (13), Step 2's decisions and refusals, the cases, every ladder
  answer and its check, every judge request and judgement with the evidence shown, production's day (items, evidence, views, judgements);
  the ledger against the archives' token counts; each component's log. Then a written reading and a separate council decision on the full
  run (ledger $15.00 minus the slice's final spent and anything still reserved).

Do you agree to launch exactly this? If you would change any part (ceiling, scope, checks, the reading), say what and why.

End with: "Council position: <launch the slice as proposed | change ... first>".

# Findings outside the comparison's scope (recorded, not acted on; to Alex with the verdict)

- 2026-11-17: the answer-choice step's code default is still luna (`clean-arch/step4-2026-11-10/stage_a/stage_a.py` `SETTING`), although D648
  chose astra. The comparison runs astra as a named, hashed variant; the default is not edited by this plan.
- 2026-11-17 (stage 0, exposure census): under D667's rule no article of 2026-08-31..09-20 is unread. Every past week of the corpus has been
  touched, mostly by corpus storage and code-only corpus censuses, but the week of 08-31 by real old-system development runs as well. An
  "unread weeks" comparison (D665) is not possible on the current corpus without either a new reading of "read" or fresh articles after
  2026-10-27.
- 2026-11-17: `stage_a_astra.py`'s first test stopped its run (`limit.stopped` true on the resend case); not yet diagnosed. Code work paused
  with the census result.
- 2026-11-17: a folder `downloaded_files/` with an empty `dashboard.lock` appears in the repository root (18:34, 18:35); not created by this work, not touched.

- 2026-11-18 00:40 — **Step 2 line 3 (a hard check) is predetermined under design v6's key.**
  - The frozen dossier renderer `group_text` drops a later report's tier, stated day, period and speaker. v6 counted those as details,
    and on c1, 78 of 79 eligible groups differ in them.
  - The product's judge reads each member's own full record, with a same-claim note (PRD §6), not `group_text`.
  - Taken to the council (round 8) before any output; the decision is recorded in D675.

- 2026-11-18, new-1 Step 1, one item:
  - **What failed:** the c8 model left out the required `figures` on evidence items 2 to 4, twice. This was the run's first format
    failure that its retry did not recover. Before this, 9 of 9 retries had recovered.
  - **Cost of the rule:** under D449, one failed article out of 1884 forces a Step 1 redo from empty, costing about $21 and about 20 h.
    The $65 guard was sized at 1.6 times one pass with no redo, so a redo puts the draw at its guard.
  - **Scope:** out of scope for this run. A finding about the redo unit (an item-level redo) and about how the guard is sized.
- 2026-11-19: new-1's only failure repeated exactly on the redo: same item, same missing `figures`, twice each time. It was
  deterministic in that draw's context, not a transport failure. D449's full-step redo cannot recover such a failure.
  - An item-level re-send, about a cent, would have shown this first.
  - Proposal, for Alex: before any D449 redo, re-send the failed item's stored request. Redo only if that send passes.

# Stage 2 of D392: arms, decision rule and labels, frozen before any send (2026-11-09)

**Arms.** Three draws each, launched the same day, on v108's 243 items (`stage2-manifest.json`, in v108's dispatch order):
- **Clean:**
  1. `run_clean_draw.sh <draw>` checks that the PRD request is c8 (`test_runner.py`) and that the frozen files are unchanged. It then
     runs Step 1 with no candidate prompt or schema (`clean-arch/step1/run_live.py`).
     - The 22 seeds are the initial theses (`stage2-initial.json`).
     - DeepSeek Flash, high effort, 64k cap (`stage2-settings.json`, byte-identical to the c8 dev run's).
     - Limits are scaled to 243 items at rates at or above the published ones (`stage2-limits.json`).
  2. Steps 2–3 run with `clean-arch/step2/run_forward.py`.
  3. The launcher lists the clean-opened theses that match the scorer's q23 rule.
  4. If there is a candidate, a reader who did not write this code checks that it asks q23's question ("Will NVIDIA sign a guarantee
     of OpenAI's Ohio data-center lease by 2027-06-30?"). Only a confirmed candidate is passed as `--q23`. It gets a yes/no ladder from
     its opening article onward.
  5. `adapter.py live` replays the draw into a seeded view store and judges it daily with the frozen judging-v7 on gpt-6-luna. Judging
     is capped at $3 per draw: every concurrent call reserves its worst case (request characters as input tokens plus the output cap)
     before it is sent. The adapter refuses a library whose record copies or references differ from the trace.
- **Control:** poc-v108 re-sent through `control_v108.py live`, only after `control_v108.py prove` passed.
- **Scoring:** both arms are scored with the frozen `score_judgement.py`, window end 2026-07-14.

**Decision rule.** The thresholds are from `calibrate.py` (`calibration.json`), exploratory, on six stored v108 draws. Between identical
configurations, total differences were 0 or 2 with all questions, and 1 or 3 without q09, q12 and q23. A collapse fired in 1 of 20
splits.
- **Better:** the clean total minus the control total over three draws is at least 3 with all questions and at least 4 without q09, q12
  and q23; q10 and q12 both agree in at least 2 of 3 clean draws; and no collapse. A collapse is a question the control agrees in at
  least 2 of 3 that falls to 0 of 3 in the clean arm.
- **Worse:** the difference with all questions is −3 or less, or a collapse.
- **Inconclusive:** anything else, including ties.

Stage 1 showed q12 cannot be delivered under the current cash-flow ruling, so "better" is expected to be out of reach. Alex chose to
run regardless ("照样跑正式对比").

**The rule is applied by `stage2_decide.py`**, written and frozen before any result. It reads the frozen scorer's outcomes; a dry run on
the two stored sets of v108 draws (r9 against the r10 control, the same configuration) reads INCONCLUSIVE (+0, +1, no collapse).

**Reported for every run:**
- every question and draw for both arms, and the judge's reasons for every disagreement;
- the adapter's counts and losses (records dropped without a verified passage, quotes over 400 characters, links to clean-opened
  theses dropped);
- cost from tokens.

**Labels:**
- conditional on the supplied questions;
- says nothing about whether the clean system opens them;
- the articles tuned c8;
- the threshold is exploratory.

**Addendum, 2026-11-09, written before any clean result: a draw that production itself stops.**

Control draw 2 stopped on 2026-07-07: "judgement refused twice: v17: v8 is not a dependency of v17". This is the frozen judge's own check,
and it stops a production run, which leaves the day resumable.
- Production recovers by resuming the day, which re-samples the refused judgement (`docs/research/2026-10-27-nvda-3m/plan.md`,
  mechanism A). The control harness has no resume, so the draw is replaced by a fresh draw in a new folder (`stage2-control-d4`).
- The same rule holds for the clean arm: if `adapter.py live` stops on a refused judgement, that draw's judging is redone from its start
  in a new folder, with fresh samples.
- Every stopped draw is kept and reported beside the replacement, with its stop. The verdict uses the three completed draws of each arm.

**Addendum, 2026-11-09, written before any clean result: a clean Step 1 stopped by the network.**

Clean draw 3's Step 1 stopped after 40 completed articles: "TransportError: IncompleteRead" at `gnews:a8fab49de53d125314a6688a`.
- It is continued as an established segment (round log §30): `stage2-clean-d3-segment-2` holds the remaining 203 items in manifest
  order, starting from the theses after article 40, with the same pinned c8 request, settings and limits (`continuation.json`).
- Steps 2–3 read both segments as one draw ('first+segment', `run_forward.step1_records`). The adapter reads the same joined trace and
  numbers articles by the first manifest; a test checks that a split trace reads exactly like the unbroken one.
- The stopped call is re-sent, as the failure left no answer. The draw is reported as continued.
- `continue.sh` was launched before the adapter read segments, so `stamp_after.sh` writes the stamp (both segments and the library)
  and the q23 candidates as soon as Steps 2–3 end.
- **Every stopped draw or segment is reported with its stop and its cost beside the result**, because a verdict on completed draws
  could hide a difference in how often each arm stops.
- Clean draw 1 stopped the same way after 50 articles (`IncompleteRead`). It is continued by `continue_clean_draw.py`, which generalises
  the d3 handling: any number of segments; only a network cut is continued; each new segment's limits are the draw's limits less what
  earlier segments reserved and called.
- d1 and d3 segment 2 were created with a fresh copy of the limits before that fix. Those two draws are bounded by at most $46.16 and
  $44.95 of reservations (disclosed).
- The clean transport makes one attempt per call by design (`clean-arch/step1/live.py`), so a cut reply stops the run where
  production's transport would retry. This is noted for the report as an infrastructure difference, not a judgement difference.
- Clean draw 3's first judging stopped on 2026-07-05 after 62 judgements, on the same refusal as control draw 2 ("v17: v8 is not a
  dependency of v17"). Per the rule above, it is redone from its start in `stage2-clean-d3/judged-2`; the stopped attempt is kept.
- Census of this class in today's finished archives: every run has 3–10 judge answers refused by the frozen check, nearly all on v17
  naming v8 and/or v2 as dependencies. A run stops when both attempts of one judgement are refused. It is the frozen judge's, shared by
  both arms.

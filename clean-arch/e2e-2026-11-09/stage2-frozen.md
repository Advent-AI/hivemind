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

# The same-provider model comparison (D629): result, 2026-11-16

**Run:** six interleaved arm-draws of 26 sends, gpt-6-luna against gpt-6.1-sol on the same request bytes except `model`
(`poc/data/clean-model-probe-2026-11-16/`). The first sol topic was sent alone and accepted, and every arm-draw finished with no
charge above its reserve. Spend: luna $0.074, sol $0.646, $0.72 in all.

**Reading:** 162 blind items read by both families. All six controls behaved as fixed, so the reading is valid.

**The verdict under the rule fixed before: inconclusive.** Sol meets the improvement and new-harm conditions, and fails only the
refusal bound.

| | luna | sol |
|---|---:|---:|
| Failed sends (agreed hard-line faults plus code refusals), of 78 | **13** | **5** |
| The same, unresolved points counted against | 29 | 20 |
| Topics failed in 2 or more sol draws but in no luna draw | | none |
| Model refusals | 15 | **24** (the bound is luna + 2) |

**Per topic** (each send as an agreed-clean ladder, a faulted ladder, or a refusal):
- **Clean ladders:** luna 41, sol 50.
- **Refusals both families call justified:** 8 in each arm.
- **Refusals both families call unjustified (N):** luna 1, sol 4.
- **Sol's extra refusals fall mostly where luna's ladders failed:**
  - fortnight c1/clean-13 (CPO shipments): luna faulted in 3 of 3; sol refused in 3, 2 of them agreed unjustified ("not one fiscal or
    calendar year", the same refusal the Codex reference writer made);
  - fortnight c1/clean-3: luna faulted in 3 of 3; sol refused in 3, disputed.
- **The one topic where sol mostly refuses while luna writes 2 or more clean ladders:** week c1/clean-3 (memory contract prices over
  2027).
- **One topic gained:** week c1/clean-10, where luna's refusals are disputed and sol writes 3 clean ladders.

**What it means:**
- A stronger model on the same provider and request halves the step's agreed hard-line failures (13 to 5 of 78), with 9 more clean
  answers.
- Its cost is a different failure: more refusals, a few of them unjustified, concentrated on two or three topics.
- At about 5 failures in 78 sends (about 6% a send), gate 1's zero-fault lines on 131 sends stay out of reach (about 8 expected
  faults).
- Measured per-send rates of agreed hard-line faults on these 26 topics:
  - luna about 17%;
  - sol about 6%;
  - the Claude reference writer 0 of 26 in one draw (4 of 26 when unresolved points count against).

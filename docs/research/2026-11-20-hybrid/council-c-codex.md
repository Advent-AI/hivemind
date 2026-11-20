**Hold J2. The refusal check misclassified four of 117 stored v7 re-sends.** It reads the archived final judgement as the previous one. All three Q31 re-sends stayed at the range shown in their request, but the harness flagged them as moves. That inflates v7’s refusal count and makes rule (d) easier for J2 to pass. Validate against the state immediately before each request. [judge_probe.py:329](/Users/lchingen/hivemind/docs/research/2026-11-20-hybrid/judge_probe.py:329) · [judging.py:226](/Users/lchingen/hivemind/src/hivemind/views/judging.py:226)

The deck no longer samples, but it reads whatever files exist without checking for each expected arm, case and repeat. The gold probe can also credit an answer production would refuse for a bad citation. Require complete coverage and count refusals before scoring both sets. [judge_probe.py:287](/Users/lchingen/hivemind/docs/research/2026-11-20-hybrid/judge_probe.py:287) · [judge_probe.py:349](/Users/lchingen/hivemind/docs/research/2026-11-20-hybrid/judge_probe.py:349)

J2b’s revised wording and the archive plan resolve my earlier objections.

DISAGREE: Fix refusal checks and verify complete coverage before sending J2.
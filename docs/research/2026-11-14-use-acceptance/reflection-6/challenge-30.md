# Challenge 30: astra with A2, prepared at $0 as round 29 asked (`reflection-6/astra-a2/DESIGN.md`)

Read `astra-a2/DESIGN.md`, `a2_probe.py`, `test_a2_probe.py`, `mutants.txt`, `preflight.txt`, `audit.md` and `check-output`.

**Your round-29 points:**
- **Premise corrected:** astra's agreed failures are H20 (3) and memory (1). Hugging Face is a control.
- **Comparison against a fresh frozen arm,** counting every send including lost answers, with agreed and strict countings. A
  replacement question must be free of material defects in a source-backed product review.
- **A2's harm is in the verdict:** harmful listings at most the frozen count plus 1.
- **Topic-level comparisons, controls on both readings, and an inconclusive outcome** are all pre-registered.
- **Budget:** the cap reserves retries and in flight. One budget defect was found by a test and fixed: the draw-start estimate now
  uses the arm's last draw.
- **The whole-request blind audit:**
  - A2 adds no main-part priority rule.
  - **NOT SOUND** on one point: its closing check is wider than its system text and schema. I aligned the closing to "that the question
    leaves out", which adds nothing. A3's removal instruction is not reused (it failed).
- **Narrowed to 10 topics:** the two clean-ladder controls were dropped to fit D439 at a $3.40 cap. Hugging Face and the disputed
  topics still carry written ladders for the harm and per-topic checks.

**Defects found at $0 and fixed before any send:**
- the A2 text loader recursing on itself;
- the cap too tight for the reserve;
- the A2 closing file's trailing newline in the check.

**Asked:** is the aligned closing a sound change, or does it need its own audit round? Send or not?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.

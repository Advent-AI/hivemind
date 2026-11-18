# Astra with A2: design (council rounds 29 and 30; D639 when sent)

**What it tests.** On astra, does arm A2's request reduce the step's gate-line failures against a fresh frozen-request arm, without A2's
known harm?
- **A2:** D436's second-side sentences, and "the topic's wording" read as its description and outcome.
- **Not tested:** any rule for choosing the main part. The blind audit (`audit.md`) finds A2 adds none.
- **One alignment after the audit:** A2's closing check said "every other part … listed", wider than its own system text and schema
  ("that the question leaves out"). The closing is aligned to them; nothing is added. A3's removal instruction was not used: it
  failed (D584, D585).

**Topics** (exposed, outside the 44; a diagnostic, not a production claim):
- astra's agreed failures: H20 and memory;
- the disputed main-part topics: Reflection, equity commitments, Blackwell into China, CPO;
- Hugging Face, which astra writes;
- three declines both families justify: the two-year capex topics and robotics funding.

**Arms and spend.** Frozen and A2, interleaved, 2 draws, 40 sends.
- **Requests:** the frozen ones are the stored ones, and A2's differ only by the recorded edits (`check-passed.json`).
- **Cap:** $3.40, one attempt in flight ($1.14 reserve). A draw starts only if its arm's last draw and the reserve fit.
- **D439:** about $36.43 used, so at most about $39.83.

**Two blind readings, both families each:**
1. **The gate form with A2's H field** (`unlisted-parts/run_readers.py`, first kind), with six known controls. A missed control
   voids it.
2. **The source-backed product review** (`review-brief.md`), with the due-day probe's four known controls. A missed control voids it.

**Verdict, fixed before.** It is counted twice: with unresolved points held, and with them failed (one reviewer suffices for a
material flag). When the two countings differ, the verdict is inconclusive.
- **Moves (a diagnostic),** when all of these hold:
  - failed sends (agreed hard-line faults plus lost answers) are at least 2 fewer in A2 than in the frozen arm;
  - no topic is worse;
  - the three justified declines stay declined in both draws;
  - harmful listings (already decided, or a settlement route) are at most the frozen count plus 1;
  - every A2 question written where the frozen arm declined is free of material defects;
  - no topic has more material defects in A2.
- **Closes:** A2 fails as many sends as the frozen arm or more, flips or loses a justified decline, exceeds the harm bound, or a
  replacement question is flagged.
- **Otherwise:** inconclusive.

**Proofs:**
- tests 12 of 12;
- nine mutants, each caught (`mutants.txt`);
- the preflight: 200 stored attempts on the 10 topics, the current checks agreeing with every stored verdict (`preflight.txt`);
- the check passes.

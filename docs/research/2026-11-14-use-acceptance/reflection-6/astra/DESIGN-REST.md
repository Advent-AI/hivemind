# The complementary Astra screen (council round 15; D633 when sent)

**What it is.** The same launcher, checks, controls, reading and verdict as the first screen (`DESIGN.md`), run on the 14 topics that
the first screen's seeded draw left out (`astra_rest.py`).
- **Topics:**
  - fortnight c1/clean-1, -3, -4, -5, -6, -7, -10, -12 and -13;
  - week-10-06 c1/clean-1, -6, -7, -9 and -10.
- **How the complement is fixed:** it is computed from the first draw's own seed and size (20261123, 12) and checked against the
  topics the first run actually sent.
- **The defect the tests found:** the first draft read the size from the launcher after overriding it, which silently drew 14. It was
  caught by the test, and is now mutant R3.
- **Disclosed:** on these 14, D629 had sol at 3 agreed failures (week c1/clean-7 L once; fortnight c1/clean-13 refusals twice) and
  luna at 12. These are the topics where the earlier ladder faults were.
- **This is an exposed development set** chosen after the first result. A positive result makes astra a stronger candidate lead. It
  does not establish a general fault rate or pass gate 1.

**Arms.** Fresh sol and astra, interleaved, three draws each, 42 sends an arm. Only `"model"` differs (`check-output-rest.txt`).

**Spend.**
- **Caps:** sol $1.20 (2 in flight) and astra $5.00 (1 in flight), $6.20 in all. About $7.45 remains of D439's $40.
- **Worst-case reserve:** $0.22 a sol attempt, $1.09 an astra attempt.
- **First request:** sent alone. The rest is refused if its price × 42 plus one attempt in flight passes $5.00.
- **Estimate:** about $1.8, from the first screen's measured averages (astra $0.037 a send, sol $0.006).

**Verdict.** Unchanged from `DESIGN.md`, on 42 sends an arm:
- closes this candidate at 3 or more astra failures;
- inconclusive if sol has fewer than 2;
- promising at astra 1 or fewer and below sol, with strict below strict, no more unjustified refusals and no new harm;
- closes if astra has at least sol's failures;
- otherwise inconclusive.

Both halves are reported side by side, never pooled into a new verdict.

**Proofs at $0:**
- `test_astra_rest.py`: 4 of 4. `test_astra_probe.py`: still 16 of 16, run in its own process.
- `mutants-rest.txt`: three mutants caught, each traceback read.
- `preflight-rest.txt`: 95 stored attempts; the current checks agree with every stored verdict. The 11 refusals there are the model's
  known contract errors, each repaired on its resend in D629.

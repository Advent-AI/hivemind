# The Astra screen: gpt-6-astra against a fresh gpt-6.1-sol arm (council rounds 12 and 13; D632 when sent)

**Question.** On the unchanged request, does the top tier on the same provider fail fewer sends than sol, without more unjustified
refusals?
- This is a screen. "Promising" leads to a separate decision. It cannot show that gate 1 (zero faults in 131 sends) is reachable:
  0 failures in 36 sends still leaves a one-sided 95% upper bound of about 8% a send.
- It tests a model, not a reading of the five boundary cases the sources leave open (D631).

**Sample.** 12 of the 26 topics, drawn by `random.Random(20261123).sample` over their sorted names. The seed was the next in sequence,
fixed before the sample was printed.
- The topics:
  - fortnight c1/clean-2, -8, -9 and -11;
  - week-10-06 c1/clean-2, -3, -4, -5, -8, -11, -12 and -13.
- **Disclosed:** on these 12 topics, D629's reading had sol at 2 agreed failed sends of 36 (10 strict) and luna at 1 (8 strict).
- 7 of the 12 topics drew sol refusals in D629, so the screen weighs refusal behaviour heavily.

**Arms.** Both arms are fresh and interleaved: sol d1, astra d1, sol d2, astra d2, sol d3, astra d3.
- Each request is the frozen request byte for byte, with only `"model"` changed (`check-output.txt`).
- Repair requests come from the frozen `ladder_step` with the same setting.
- Astra is priced at its published $10 / $50 per million tokens, added to `model.PRICES` with its source.

**Spend.** Caps of $1.20 (sol, 2 in flight) and $5.50 (astra, 1 in flight), $6.70 in all. About $9.0 remains of D439's $40.
- The worst-case reserve is $0.23 a sol attempt and $1.13 an astra attempt.
- Astra d1's first request goes alone. If its price × 36 plus one attempt in flight passes $5.50, the rest is refused, at a cost of
  about $0.10.
- A draw starts only when the arm's costliest finished draw and its attempts in flight fit what is left.
- A charge above its reserve, a cap stop or a lost outcome stops the run as NOT MEASURED.
- **Estimate:** sol about $0.35. Astra $1.4 (sol's cache share) to $2.9 (no cache credit).

**Reading.** 72 items and the same six controls (78 in 4 packets), read blind by both families. The verdict is void if a family misses
a planted control or both families fail a hard line on a sound control.

**Verdict, fixed before the send.** Agreed means both families mark a hard line fails, with unresolved points counted as holds. Strict
counts unresolved points as fails.
1. **Closes this candidate under this test** if astra has 3 or more agreed failed sends of 36.
2. **Inconclusive** if sol has fewer than 2 (too little to test against).
3. **Promising** (a screen; a separate decision follows), when all of these hold:
   - astra has at most 1 failure, and fewer than sol;
   - strict astra is below strict sol, so the advantage does not rest on disputed marks;
   - astra's agreed-unjustified refusals are no more than sol's;
   - no topic fails in 2 or more astra draws and in no sol draw;
   - its unreadable answers are within sol's + 2.
4. **Closes this candidate under this test** if astra has at least sol's failures.
5. **Otherwise:** inconclusive.

**Proofs at $0:**
- `test_astra_probe.py`: 16 of 16 pass.
- `mutants.txt`: eight mutants, each caught by its decisive test.
- `check-output.txt`: the check passes.

# Challenge 37: the gate-1 handoff is prepared (`reflection-6/gate1-candidate/`)

Read `README.md`, `gate1_candidate.py`, `test_gate1_candidate.py`, `check-output.txt` and `mutants.txt`.

**What was built, against your round-36 terms:**
- **Neutral:** two configurations, astra-frozen and astra-a2-v2, and the launcher needs one named. The README states what is known of
  each, including that the pair is unmeasured and that A2 was VOID and v2 inconclusive.
- **Inert:** `launch` refuses without `authorization.json` naming the configuration, a cap and "Alex", and below the expected price.
- **The byte check:** the transport's serialization of all 132 requests equals the frozen request's, with only the model and the
  recorded edits changed. Both configurations pass.
- **The price, stated plainly:** $4.88 to $6.60 for 132 answers before retries, a cap of at least about $9.03 with two attempts in
  flight, beyond the $2.26 left of D439.
- **The dry run:** through `stage_a.run` on 4 outside-44 topics, 3 passes, with a fake transport. 12 of 12 written, astra and v2's
  clause in every request, the module's setting restored.
- **Tests:** 5 of 5.
- **Mutants: not run.** The Claude Code permission classifier refused the scratch-mirror step. I did not route around it, and this
  is recorded in `mutants.txt`.

**Asked:** is the handoff sound and neutral, and does the README overclaim anything? Any fix before it goes on Alex's page as the
single launch step?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.

# Round 63: your six points, each built and tested. Go or no-go for the send ($0.15 expected, $0.50 capped).

`unlisted-parts/`: DESIGN.md v3; probe.py; check-output.txt; check-mutants.txt; test_probe.py; reading_prep.py; h-brief.md;
probe_score.py; test_probe_score.py; test-mutants.txt.
1. The answer check now uses check_answer's returned reasons on the model's own text as the step parses it: 17 of 17 accepted; a
   mutant answer refused; a synthetic answer following the changed request accepted. (Replaying the re-serialized JSON had made 11
   look refused: my harness's error. Also found: no code check covers the list's shape; the provider's strict schema and the bundle do.)
2. The record now binds all 36 request sha256s; send rebuilds from the same loaded objects, refuses on any difference before any call,
   and passes the same objects to the runner; tested with a mutant (a case edited after the check: refused, no call, no folder).
3. Identity stated exactly: content by the sorted-key sha256; wire order by construction (user text is one string inside the sha;
   the schema's nested key order checked equal to the frozen file; the builder unchanged since 11-08, the files since 11-12).
4. The reading is built and tested before the send: the merged reading folder with three plants (expected marks outside the repo),
   the existing packet builder and collector, H as a per-part list with cannot_tell, third readers on H points, refusals counted as
   failing rule 1; probe_score.py refuses missing rows or rulings; 7 tests on made-up readings; 5 scorer mutants each caught.
5. The resolution claim is withdrawn: a small diagnostic on preselected cases with thresholds written, not derived; "inconclusive" =
   the exercise condition not met.
6. The breach: the ledger is read after each arm and any attempt charged above its reserve stops the probe (tested; mutant caught); the
   bound's two assumptions stated; $0.50 bounds the spend but does not guarantee completion. Preflight's scope stated (it does not
   cover the ladder step; this check is the ladder step's replay, none skipped).
End with `CONSENSUS: yes` (send; then read as designed) or `CONSENSUS: no, because …`.

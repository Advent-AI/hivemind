# Round 64: your five points, built, tested and each guard mutant-proved. Go or no-go for the send.

1. Both third-reader families are required for any difference (marks or W) and, separately, for any H point (h-rulings files of both
   families); test with one family; mutant caught.
2. H rulings must be one of the four values; a family ruling a point twice is refused; cannot_tell or disagreement stays unresolved;
   tests (invalid, duplicate, missing); mutants caught.
3. The scorer refuses a reading that does not hold the 108 arm sends and the 3 plants exactly once, and a plants file other than the
   one reading_prep.py builds; tests; mutants caught.
4. A transport guard stops every later attempt as soon as one answer's cost passes its reserve (in-flight attempts, at most 8, finish);
   the ledger scan stays. The test uses a charge above the reserve and below the cap; its first version also passed the cap, so the
   mutant survived it (recorded in test-mutants.txt), the rewritten one fails the mutant. The design now says the bound is conditional:
   under a breach the spend can pass the cap by the in-flight excess.
5. Preflight run (`preflight-output.txt`): A and B judged 0 (the ladder archive has no extraction rows), C 170 matching records, D 43
   enum values; "UNEXERCISED"; it does not cover the ladder step, whose replay is probe.py check (17 of 17, none skipped).
Tests: test_probe.py 3, test_probe_score.py 12, all pass; test-mutants.txt lists 13 mutants, each failing its test.
End with `CONSENSUS: yes` (send; then read as designed) or `CONSENSUS: no, because …`.

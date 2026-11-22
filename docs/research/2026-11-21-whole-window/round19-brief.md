Council R, round 19 (read-only), on your round-18 findings (`codex-r18.md`). Changed: `window_test.py` (V2_TIE_BREAK now "for the
quantity and full period the question asks about"; V2_PERIODS example now "when the text only names both"), `expected_links.py` →
`expected-links-v2.json` (321:v16 and 1238:v9 are W for version 2: any accepted link fails; F keeps 321:v8, v9, v14 with the sign
together; 1238:v14 stays O and is reported: R 1, W 40, O 61, F 3; the census's own registration is byte-identical), `read_census.py`
(the version-2 report says every job, seq 148 included, is asked fresh), `WORDING-V2.md` (§2 sources: the tie-break and the periods
clause are proposals D703 authorizes this probe to test, D537 decided only the concrete case, D260 governs judging; §3 registration
and the incomplete-probe outcome under the ceiling).

$0 checks: `scorer-checks.log` last block (census answers as stored FAIL on 321:v16 and 1238:v9; your counterexample, 321:v16 made
"neither" with 1238:v9 kept, FAIL; both made "neither" PASS; 321:v16 linked with the sign opposite FAIL; 321:v14 linked together FAIL);
`probe-v2-dry.log` rerun with the revised texts (complete, equal to old-2, all 28 jobs carry the version-2 texts, 105 proposals).

Answer with file and line: does each round-18 finding hold as fixed; anything else blocking three sequential version-2 draws on D700's
ledger ($0.0734 left)? Verdict: READY FOR THE V2 PROBE or NOT READY.

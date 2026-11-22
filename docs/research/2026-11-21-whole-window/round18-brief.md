Council R, round 18 (read-only): the sharpened link question before its cents probe. Alex chose this path (D703, last entries of
`docs/DECISIONS-log.md`: "先试新问法", with the promise of no blanket ban on a whole reading its part). Read `WORDING-V2.md` (audit,
the three changes, sources, growth, what the probe decides), `window_test.py` (section "version 2": `wording_v2`, `with_wording_v2`,
`probe_pass`, `probe_v2_dry`, `probe_v2`), `expected_links.py` → `expected-links-v2.json` (the census's classes plus F: v17 reading an
FY2027 revenue amount with the sign together, 4 pairs), `read_census.py` (`--v2`, the F verdict), and the current texts in
`src/hivemind/views/links.py` lines 22-47.

$0 checks: `probe-v2-dry.log` (fake "reads" answers: complete, equal to old-2, all 28 jobs carry the version-2 texts, 105 proposals);
`probe-v2-mutant.log` (texts not patched: the first link job stops before the inner transport, 0 calls); `scorer-checks.log` (census
draws refused under --v2 for their wording; the census answers scored on the v2 registration fail F in 3 of 3, the positive control).

Answer with file and line:
1. Prompt audit: is each change traced to a standard line or decision, general across industries (examples name no covered company,
   none from the test articles), and does any change contradict another sentence of the request or the SIGN examples?
2. Will the tie-break ("the one whose answer the supplied text anchors less ... is judged with the other's conclusion in view") keep
   v9 reads v14 given what each side was shown at seq 148, and does it ban a whole reading its part (it must not)?
3. Does the periods clause remove v17 reads v16 and v35 reads v9 without removing a link the material supports (v35 reads v14 was
   called defensible in round 17; the clause keeps a cross-period link only when the text states how)?
4. The registration v2 and the gate: sound? Anything else blocking three draws on D700's ledger ($0.0734 left)?
5. Verdict: READY FOR THE V2 PROBE or NOT READY.

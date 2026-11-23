Council R, round 16 (read-only), on your round-15 findings (`codex-r15.md`). Changed: `window_test.py` (`census_pass` takes a
transport kind written to `draw.json`; `JULY_HASHES` and `pinned`; a link job at seq 148 not pinned stops before the inner transport;
`reuse_refusals`), `read_census.py` (refuses a draw whose transport is not paid), `expected_links.py` (206:v2 and the credit-support
against gross-margin pairs, 746:v1, 746:v2 and by the same reasoning 1102:v1, 1102:v2, moved to O: R 1, W 38, O 66), `DESIGN.md` §3.
$0 checks: `reuse-refusals.log` (a loader missing a pinned row refused; an unpinned seq-148 READS job stopped with nothing sent to the
inner transport at seq 148); `census-reuse-dry.log` rerun (both July answers reused, counted, transport dry); `scorer-checks.log`
rerun (the dry draw refused as not paid; no draws, no draw.json and a missing answer refused; fake answers 114 wrong, gate FAIL;
control PASS; the known positive with the opposite sign or reversed FAIL).

Answer with file and line: does each round-15 finding hold as fixed, and is anything else blocking three sequential paid census draws
under Alex's $0.10 (D700)? Verdict: READY FOR THE CENSUS SEND or NOT READY.

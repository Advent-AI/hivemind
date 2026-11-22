Council R, round 14 (read-only), on your round-13 findings for the census (`codex-r13.md`). Read the changed files:
`docs/research/2026-11-21-whole-window/DESIGN.md` (§1 scope, §3 rewritten), `window_test.py` (harness-only marker and store lock in
`replay_window`; `complete`; `census` with the approved-ceiling check and launcher registration), `expected_links.py` →
`expected-links.md` / `.json` (the registered reading of all 105 pairs, written before any census answer), `read_census.py` (the
scoring), `census-dry.log` (rerun after the changes: equal to old-2, 105 proposed, 0 written, complete).

$0 checks run since round 13 (outputs in this conversation's record, summarised in DESIGN.md §3):
- `complete` on the dry record: control True; a dropped READS answer, a dropped SIGN answer, a failed job: each False with its reason.
- `census` refuses an approved ceiling of NaN, 0 and 0.2 before touching a ledger; it refuses a ledger whose ceiling is not the
  approved one.
- `read_census.py` on the dry pass (every pair answered "the THESIS reads the CANDIDATE", sign together) plus the three July draws:
  58 wrong links (57 W pairs and v14 reads v16 against the registered v16 reads v14), 7 required right, 3 missed (July v8 reads v14),
  6 fragile, gate FAIL.
- Price: 28 jobs in the dry pass (all SIGN jobs included), ledger settlement at three times the reported input: at most about $0.022 a
  draw, $0.066 for three; largest reservation $0.0084; the draws run one after another.

Answer with file and line:
1. Does each round-13 blocking finding hold as fixed (a gate with a known positive and registered wrong links; the July samples
   reused; a complete draw proved; launcher registration and a finite approved ceiling; harness-only marker and lock; preflight)?
2. The registered reading: is any R or W class wrong under the READS criterion as written and D537? (O pairs are not scored.) Is it a
   problem that the registration encodes "a part reads its whole" when the criterion's second clause can be read the other way?
3. Anything else that blocks a census send of three draws under a $0.10 ceiling Alex names.
4. Verdict: READY FOR THE CENSUS SEND (once Alex names the ceiling) or NOT READY.

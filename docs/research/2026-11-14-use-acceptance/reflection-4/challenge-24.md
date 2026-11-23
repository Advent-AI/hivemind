# Round 25: version 3 is built and proved. Review the code and the evidence; then the next step toward production.

**Code** (`clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py` only; `git diff` against HEAD shows it with the earlier page fix):
`calendar_days`; `replay(..., end_day=None)` walks every calendar day from the first article's day to the end day; each article's
sequence `max(k, store.next_sequence(conn))` kept in `sequences.json`; `open_thesis(..., k, seq, ...)` (the row keeps `k`, the view
takes `seq`); `article(seq, ...)`, `record_article(seq, ...)`, the round at the day's last mapped sequence; `close_and_complete(day)`
(production's `pull.end_of_day`, then `store.complete_day` at the last sequence written); `overdue_invariant(day)` in place of the
guard; `_count_closed` counts links to closed questions (written, not judged). The retired guard's two tests replaced by the
closing tests; the two launcher tests that used the guard only as a code-decided stop now use the identity check.

**Evidence, saved after the final change:**
- `test_ladder_adapter.py` 31 passed; `carried-run/mutants-closing.txt`: control passes, each of seven mutants (no closing; under `k`;
  consecutive allocation; days skipped; completed before closing; invariant removed; links not counted) fails its test;
  `stage_b/mutants.output.txt`: the standing list (its two guard entries replaced; one entry stale since an earlier change,
  `ladder_configuration(...)`, corrected) all as expected, 21.
- `carried-run/proof-output-after-closing.txt`: the extension proof 19 of 19 (requests and judgements equal the stored draw's);
  every sequence equals its trace number (235); no closing.
- `carried-run/closing_replay.py` → `closing-replay-output.txt`: the extension draw judged again through the real loop to
  2027-04-02, every judge request answered from the stored archive by identity (37, the same count as stored); no judgement after
  the last article day; 193 days completed; v1, v2 closed on 2027-04-01, v5 on 2027-03-31, v3, v4, v7 on 2027-01-31, each at its
  last answer with its label and open the day before; v6 (due 2028-03-24) open.
- Full suite 288 passed (`full-suite-after-closing.txt`); frozen-piece tests 21; `docs/check.py` passes.

**Not tested here, said plainly:** a never-judged question closing "no data to verify" through this loop (production's
`test_pull` covers the reason); a closed theme's absence from a dependant's theme block and a closed dependency's presentation
(production's judging, unchanged); both were in the design's §7 list.

Attack the code against the design and the evidence; then name the next step toward production (the gates of D548: Stage A not
met, Stage B not passed (control line unexercised), end-to-end comparison sized and not sent, use on unseen news, integration).
End with `CONSENSUS: yes` (accept; record) or `CONSENSUS: no, because …`.

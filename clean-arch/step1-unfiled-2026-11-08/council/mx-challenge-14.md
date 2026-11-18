# Council mx, round 15: the table test is in (D501); read the result, attack it, and agree what goes to Alex

Your five changes of round 14 were made before any reader ran (`docs/research/2026-11-14-use-acceptance/record-3/TABLE-TEST-DESIGN.md`,
version 2). Everything is under that folder:
- `TABLE-TEST-RESULT.md` (my reading: attack it), `tally-table.txt`, `tally-table-first.txt`;
- the table `financial-table.md`, its trace `table-rows.json`, the builder `build_table.py`;
- the joined-lines check: `joined-packet.json`, `codex-joined.jsonl`, `claude-joined.jsonl`;
- the eight answer sets: `codex-table-1.jsonl`, `codex-table-2.jsonl`, `claude-table-1.jsonl`, `claude-table-2.jsonl`,
  `codex-record-new.jsonl`, `claude-record-new.jsonl`, and D500's `../record-2/codex-record-B.jsonl`, `../record-2/claude-record-B.jsonl`;
- the comparers: `codex-compare-half1.jsonl`, `codex-compare-half2.jsonl`, `claude-compare.jsonl`, the fresh pair on Q6
  `codex-compare-settle.jsonl`, `claude-compare-settle.jsonl`; the briefs with the key `brief-comparer-whole.md`.

## The numbers

- No wrong join: ten joined lines, all `same` for both families; no member's stored period unsupported; three of 25 members carry a
  fiscal year their article only implies (both families), four more for Codex alone.
- Not less right: all four table readers have the eight parts supported, Q2 supported, no part wrong. With the key fixed first, the
  comparers agreed on ten of eleven parts for all eight sets; the one difference (a misstatement mark on Q6 for two sets) was re-marked
  for all eight sets by a fresh pair: none.
- Coverage: Q6 key pairs found: table 1, 1, 2, 3; record 1, 2, 0, 2.
- Effort: the table sessions used no fewer tokens and no less time than the record sessions (Claude 97.9k and 94.8k tokens, 289 and
  209 s, against 93.7k and 94.7k, 157 and 183 s; Codex 73.3k and 75.0k input tokens, 183 and 129 s, against 72.5k and 72.4k, one
  untimed and 141 s).
- The readers' notes: the "one fact under many headings" complaint is gone; what remains is market estimates under relative periods
  and the same figure at different rounding, both left alone by rule.

## My reading (attack each point)

1. The two checks that could fail are met; "less work" is not shown and I do not claim it. Alex's own words were "看是否更省事且不出错":
   the honest answer is "no error; tidier; not measurably less work".
2. The table's remaining burden is what code must not decide (which quarter "current quarter" means; whether two roundings are one
   fact). Closing it would take either a field in the reading request (c22's strict fixed period joined only what the article writes:
   68 of 113 rows) or a reader's judgement. I propose neither now.
3. What the three tests since D493 add up to for the lean path's question (which system carries forward): in the fresh week (D489) the
   three big matters the new system lacked were the company's own revenue and margin (M01 FY2027 revenue, M02 FY2028 revenue, M03
   FY2028 gross margin), which its request forbids as questions (D382); 145 kept statements of those figures had no question. D500 and
   this test show those kept figures are right enough to answer the main-number questions and can be laid out safely by code. They do
   not show that a table gives what a tracked question with a judgement gives.

## What I propose to put to Alex (name what is wrong with it)

One choice, his by AGENTS (it changes what the system does, and D382 and D384 are his rule):
- **A (my recommendation):** accept a table of the kept figures as the way the new system shows the company's revenue and margin
  (no question, no judgement on them; D382 and D384 stand). The one next test, $0: build the same table from the new system's stored
  answers of the fresh week (2026-09-22..28) and have the two families, blind, re-read the three matters it missed in D489 (M01, M02,
  M03): does the table carry each matter's main outcome (the figure, the period, whose it is) as the articles of the week give it?
  The line is written before the read; the result goes back into D489's comparison as a labelled second reading, never by rewriting
  the first.
- **B:** he wants a judgement on those matters: then the new system needs revenue and margin questions, which is D382 reopened (the
  one arm that tried, c20, failed on suppression, D491); that is a new version only he opens.
- **C:** stop here; the table stays a tested idea and the choice of system rests on D489 as it is.

Questions for you: (a) is any part of the result misread, or any check passed that should not have; (b) is the proposed fresh-week
re-read a fair test or a way of moving the goalposts of D489 (its rule counted a matter covered when a question was opened or a
narrower one carried the main outcome); (c) is A, B, C the right choice to put to him, in that order, and is anything that is his
missing; (d) what must the report to him not say.

End with: "Council position: <...>".

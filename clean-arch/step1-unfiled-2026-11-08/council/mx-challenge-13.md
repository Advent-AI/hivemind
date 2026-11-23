# Council mx, round 14: Alex chose the table test (D501); its design before any reader runs

Alex answered D500's question with "试做财务数字表" (D501 in `docs/DECISIONS-log.md`): a $0 test, nothing sent to a model. Your bounds of
round 13 are taken as the design's rules (join only what the stored evidence establishes; keep the wording and the source; leave an
uncertain period as written; never a quarter from the article's day).

Read, under `docs/research/2026-11-14-use-acceptance/record-3/`: `TABLE-TEST-DESIGN.md` (the rules as a table of which decision code takes
and whether it is identity or judgement; the checks, the lines and the answer key, all written before any reader), `build_table.py`
(closed forms for the company's name and for a fixed period, with its own must-pass and must-stay controls), the built table
`financial-table.md` and its trace `table-rows.json` (114 rows of c8 in 99 lines, 5 sections, 39 period blocks; 63 rows under a fixed
period key; 10 lines holding more than one row). The plain record it is compared with is `../record-2/views-record-B.md`.

Name only what would make the result wrong or unreadable:
1. **The joins.** Is any of the three code decisions a judgement in disguise, or wider than the stored text establishes? In particular:
   "NVIDIA (CFO Colette Kress)" and "NVIDIA (management)" grouped as the company with the wording kept on the line; a stored period
   such as "fiscal q2 2027" read as FY2027-Q2 when the stored period is the model's field, not the article's sentence; rows joined on
   equal measure, value, kind, period key and source group though their bases differ (all bases are listed on the line). Read the ten
   joined lines and the period list the builder prints (run it: `python3 docs/research/2026-11-14-use-acceptance/record-3/build_table.py
   poc/data/clean-record-unread-2026-11-15/sends/records.jsonl docs/research/2026-11-14-use-acceptance/record-2/cases-record-2.json
   --company NVIDIA` is read-only apart from rewriting the two output files; if your sandbox refuses the write, read the code and the
   existing outputs).
2. **The layout** (sections by whose figure and kind, blocks by period key): does it put anything where a reader would be misled,
   e.g. the company's "estimate" section, or others' figures of different sources in one section?
3. **The reader test:** eight answer sets (two fresh readers a family on the table; for the plain record, the two of D500 plus one
   fresh reader a family), comparers marking against one answer key fixed now, a disputed part re-marked for all sets. Is the key
   right against the articles (`../record-2/articles-unread.json`)? Is the Q2 rule fair to both layouts? Is "less work" measurable this
   way (key pairs of Q6 found; the layout counts), or does it need another measure?
4. **The lines and the verdict:** anything that lets a wrong join or a lost part pass, or that fails a table for the readers' variance.

Then say whether the readers may run. End with: "Council position: <...>".

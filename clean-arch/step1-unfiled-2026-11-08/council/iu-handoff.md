# Council iu: an independent read of a measurement's result (read-only)

You are an independent investigator, new to this work. Read-only: do not edit files, run model calls or start runs. Running the
existing scripts and tests, and small Python snippets that only read files, is fine. Form your own view from the primary
material; you are not given the author's conclusions and should not look for them (do not open `iu-claude.md` in this folder,
nor `clean-arch/step4-2026-11-10/stage_a/result/RESULT.md` or `own-read-before-rulings.md`: they hold the author's reading and
come to you in a second round).

## The work

A new pipeline step, the "ladder step", turns a thesis (a question the system opened from a news article) into one judged
question with an answer ladder and a due day, or declines. One model call, code checks, one resend
(`clean-arch/step4-2026-11-10/ladder/ladder_step.py`; the request is `ladder/candidate-system.txt`, `candidate-closing.txt`,
`candidate-schema.json`; the design is `clean-arch/step4-2026-11-10/DESIGN.md`, §5 for the step and §8 from "Stage A" for the
measurement, with the six lines under "Lines (Alex's, D400)" and the accounting under it).

Stage A measured the step alone: 44 stored theses, three sends each, read by two reader families with the form
`ladder/stage-a-reader-brief.md`, a third reader ruling where they differ (`ladder/stage-a-third-reader-brief.md`). The lines
are the owner's (decisions D400 and D401 in `docs/DECISIONS-log.md`): a line missed stops the work and goes to him.

## The material

- `poc/data/clean-ladder-stage-a-2026-11-10/run/`: the run as sent (`send-<n>/outcomes.jsonl`, one row a send, with every
  request's answer and reasons; `spend.jsonl`).
- `poc/data/clean-ladder-stage-a-2026-11-10/run-rechecked-2/`: the stored answers replayed through one corrected check
  (`clean-arch/step4-2026-11-10/stage_a/recheck_stored_run.py`); the folder the result is read on. `readers/packet-*.json` are
  the items as the readers saw them (thesis, article, ladder as the judge is shown it); `readers-answers/reader-codex-*.jsonl`
  is reader 1 and `reader-claude-*.jsonl` reader 2; `third-reader/` holds the ruling packets and `rulings-*.jsonl`;
  `key-item-to-send.json` maps an item number to its case and pass (items 48, 75, 98 and 113 are retired and were read again
  as 129 to 132).
- `clean-arch/step4-2026-11-10/stage_a/`: `accounting.py` (the lines), `collect_readings.py`, `result_tables.py`,
  `code_counts.py`, their tests; `cases.json` (the 44 theses with their articles); `result/report.txt`, `result/tables.txt`
  and `result/code-counts.txt` (generated: the lines, the shares, each thesis's three sends, what code counts across sends).
- `AGENTS.md` (the working rules; §1 on diagnosis, §7 on measuring and iterating).

## Your questions

1. **Is the measurement sound?** Recompute the six lines from the rows and the rulings yourself, or check the code that does.
   Name any error in the join, the accounting, the replay, or the handling of the retired items, and anything in the way the
   readers or the third reader were set up that makes a line's verdict unreliable. The third reader is of reader 1's family:
   say what that does to each line, using `tables.txt` (line 5 under each reading).
2. **Read the failures against the articles.** Take at least 25 failed marks, spread over the marks and the kinds of answer,
   and include every mark behind lines 3 and 4 that both readers failed. For each: is it the model's error, the reader's or the
   form's error, or a fault of the thesis the step was given? Quote the words that decide it.
3. **Decompose the misses by mechanism**, with counts on the stored data: which few causes explain most of what is wrong, and
   for each, where the decision is made (the request's sentence, the schema's field, a code check, the thesis upstream).
   Separate what both reader families agree on from what only the stricter reading finds.
4. **The next step.** The rules say a failed step is fixed and re-run at that step, one class at a time, by a structural change
   at the owner of the rule rather than by sentences, and that a choice that changes what the system does is the owner's. What
   one next step would you recommend, what would falsify it, and which decisions must go to the owner?

Out of scope: the judge that reads these ladders later (Stage B), the steps before this one, production's own pipeline.

## Deliver

Findings by severity with the file, the case and pass, or the exact words that show each; then your decomposition table; then
your one recommendation with its falsifier. No praise, no summary of what you read.

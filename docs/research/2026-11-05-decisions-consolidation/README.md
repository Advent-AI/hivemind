# Consolidating the decisions and working rules (2026-11-05, D367)

Alex asked for the decisions and principles to be cleaned up: too long, out of hand and conflicting; structured and matched to the product
and the PRDs; reviewed several times with Codex; then the README and AGENTS.md deeply cleaned. This folder holds the work behind the
result: [`docs/DECISIONS.md`](../../DECISIONS.md) (what is in force), [`docs/DECISIONS-log.md`](../../DECISIONS-log.md) (every record,
unchanged) and [`docs/DECISIONS-frontend.md`](../../DECISIONS-frontend.md).

## Method

1. **First reading.** Four Claude readers, one range each (D1–D63, D64–D198, D199–D265, D266–D366), classified every decision against
   [`brief.md`](brief.md): its module, whether it is in force, superseded, retired or a record, the standing rule in its own words,
   the decisions that amended it, whether it rests on Alex's words, its home and the conflicts with other decisions or documents.
   Records: `claude-1.jsonl` … `claude-4.jsonl`.
2. **Second reading.** Codex (read-only) checked each classification against the log in eleven ranges (`verify-*.jsonl`; a first attempt
   at a whole range at once stopped after a dozen decisions, so the ranges were cut to about 50 KB of log each).
3. **Merge.** [`merge.py`](merge.py) checks every number appears once; [`apply_findings.py`](apply_findings.py) applies the second
   reader's status, authority and amendment corrections and attaches its other checks; [`make_index.py`](make_index.py) builds the index
   and the lists the register was written from. Result: `final.jsonl` (365 decisions: 266 in force, 110 of them frontend).
4. **Writing.** The register's sections were written by hand from the in-force lists and the checks; the conflicts were sorted into those
   a later decision or a reading of the decisions together settles, and those only Alex can settle (the register's "Open for Alex").
5. **Rounds of review.** Read-only Codex reviews by angle: A, the register against the log; B, AGENTS.md new against old; C, the PRDs and
   the design page against the decisions in force; D, the README, the state page and the pipeline guide against the code and the runs.
   Serious findings per round: round 1, 30; round 2, 9 (and 13 classes in the PRDs, corrected by two agents with separate files, then
   re-rendered with [`regen_blocks.py`](regen_blocks.py)); round 3, 7; round 4, 7; round 5, 3 (the register 0); the PRD round 2, 7, of
   which 5 corrected, 1 kept with its reason and PRD 10 left for Alex; round 6, 6; round 7, 5 (the register and the guides 0; the
   log's 143 broken links fixed by keeping the log beside the register as `docs/DECISIONS-log.md`, unedited). What remains is PRD 10's
   two lines, left for Alex. From round 5 on, the register states that each decision's record
   governs conditions where an entry is shorter, so the rounds stopped counting omitted conditions. Each finding was checked against its
   source before a change; the reviews are `review-r*-*.md`.

## What changed besides the register

- AGENTS.md: every rule kept at its decision with Alex's words; incident narratives left to the log; the extraction ruler joined §7.1
  with the standard's version corrected (version 5, the signed version 3 with D248's and D250's boundaries) and the frozen gold named
  golden-v5; "own the loop" bounded by "a full run, a registered test or a paid send beyond a few cents starts on his word"; one
  recommendation and one test for the next step of work, options and a recommendation for a product choice; §11 says how a decision is
  recorded.
- README, `docs/CURRENT_STATE.md`, `docs/poc/pipeline-plan.md`: rewritten to the current pipeline (the coverage-start reading, the one
  decider, the daily judging round); the state page's chronicle replaced by what runs, the open defects and the next task.
- PRDs 00, 01, 03, 05, 06, 07 and the page data corrected where they contradicted decisions in force (daily judging, evidence in view,
  the writer retiring nothing, Jev with the collision judge, judgement as a forecast, one-home filing, the day-start request, themes one
  to all, the Config settings); decided-but-unbuilt rules marked as such.
- Found in the process and recorded: the default Jev path chooses no dependencies although D51 has matching choose them (open item 2);
  D366's "since D256" means D351; the service contract's broken anchor; two untraced defects added to the state page.

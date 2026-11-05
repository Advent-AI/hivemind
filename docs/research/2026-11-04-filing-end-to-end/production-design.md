# The coverage-start reading in the product: design before code (D363, D364)

2026-11-05. Alex: "好开始做到production 上，完整的更新所有系统设计等"; "好，按这三步做，你不要再搬石头砸自己脚了，你要收敛上生产". What is built is what was validated
(`baseline-design.md` rounds 13-25): the third version of the reading (`baseline_read.TASK_V3`), the check with the row repair (`hivemind.baseline.check_figures`,
round 24), the document rule (round 18), records as the judging tests wrote them (round 16), and a figure several questions read stored once and linked to each
(D364). Nothing else is added.

## What the step does

At coverage start, after the seed questions are written and before the first day's items, the run reads the covered company's latest earnings report once per
open question and report item, keeps the figures the check accepts, and writes them as evidence linked to the questions that read them. The first day's judging
round judges those questions together with the day's other changes. The daily path is unchanged (§5.3 restatements stay excluded).

## Where and how

- **Entry:** `scripts/replay.py`, right after `--seed` writes the seeds, when the configuration has a `baseline` setting: `baseline.run(conn, items_db, archive, cfg,
  company, ticker, coverage_start, transport)`. Coverage start is the run's `--from` day. A configuration without `baseline` behaves exactly as today.
- **Configuration:** `poc/config/poc-v116.json` = `poc-v108` plus `"baseline": {model gpt-6-luna, prompt_version "baseline-v3", temperature 0, reasoning medium,
  max_output_tokens 16000}` (the judging step's setting, as validated). `config.load` reads it as an optional setting; `baseline.SUPPORTED_VERSIONS = ('baseline-v3',)`
  refuses any other (as D359 for extraction and judging). `poc-v108` stays the default until Alex's word.
- **Prompt file:** `src/hivemind/prompts/baseline-v3.json` = {"system": SYSTEM, "task": TASK_V3}, byte-equal to the validated texts; the schema stays in code
  (`baseline.SCHEMA`, the validated one). A test pins the file's sha256 (as `test_frozen_extraction_prompt.py`).
- **Documents (code owns identity):** items of category T1 whose object identifiers carry the company's ticker, published before coverage start; the latest such
  day; of that day the filed ones (channel EDGAR) when any, else all. Text: the item's `text_page` (the page text with its tables; the cleaned text drops tables),
  read from the run's items database (`--testdb`). The step refuses before any call when that database has no `text_page` column or a chosen item's page text is
  empty (a configured step whose input is missing refuses the run, AGENTS §3); `scripts/replay.py`'s default window database has no such column, the NVDA database
  the acceptance runs use (`poc/data/items-nvda-2026-07-01-10-27.sqlite`, `run_arm.sh`'s default) has it, byte-equal to the page database the validation read.
  No such item: the step records "no report" and writes nothing.
- **Questions:** every open question at coverage start that `extraction.shown_views` shows for an item of the company on the report's day, each with its lines from
  `placement.question_lines` (as validated).
- **Request:** per question and item, `model.call(archive, cfg, cfg.baseline, system, user, SCHEMA, 'extraction', 'baseline')` with the validated user message
  ("[Question]" lines, "[Report] id …, published … by …: title", the page text, the task). Same bytes as the validated requests (checked at $0, below).
- **Check:** `check_figures` on each answer; a refused figure is dropped with its reason (D209) into the step's record; nothing refused is kept anywhere else.
- **Records:** one evidence record per distinct (item, quote) that any question kept (D364): `quote` the stored quote (the report's row span when repaired),
  `one_line` the model's one-line followed by `(unit: …)` when the value has no scale of its own (as the validated judging requests), `speaker` and `original_who`
  the item's publisher, `original_day` the item's day, `tier` 'fact', `event_time` '', `created_seq` the step's sequence number, `created_from_input` the item; one
  source row (the item, category T1, its day, the step's sequence number); a link at the step's sequence number to every question whose reading kept it. When two questions keep the same quote with different one-lines, the record
  keeps the first question's (questions in id order).
- **Sequence number:** the step takes the ledger's next sequence number (1 on a new ledger: seeds are at 0), so the service and the dated bundles, which map
  sequence numbers above 0 to the day of their processing row (`service.seq_day_map`, `bundle._visible`), show the records from the coverage-start day; the first
  item of the first day then takes the next number.
- **Record of the step:** one `processing_steps` row: input `baseline:<ticker>:<report day>`, that sequence number, step `baseline`, result `ok`, publication day
  the coverage start day, reason JSON {changed: the questions linked, report: the items, kept, refused (question, item, quote, reason), empty (question, item)}.
- **Judging:** `round.changed_views_of_day` also reads `baseline` rows of the day, so the first day's round judges those questions with the day's other changes
  (themes first, D191). No judging at coverage start itself.
- **Seeded questions visible:** seeds are written at sequence 0 (D253), which `service.seq_day_map` does not map, so the service and the bundles show no seeded
  question at all (a gap since seeding, not of this step, which links its records to those questions). The map gives sequence 0 the ledger's first processing day
  (the coverage-start day): seeded questions, and the records linked to them, are visible from coverage start. One line in `service.seq_day_map`, with its test.
- **Coverage-start day finished first:** a ledger whose `baseline` row's day is not yet a completed day refuses a run that starts after that day (before any call):
  the first day's round, which judges the linked questions, must run.
- **Once, and only at coverage start:** a ledger that has a `baseline` row for the company skips the step (a resumed run). A ledger without one that has already
  processed anything (a processing row above sequence 0, or a completed day) refuses the step before any call: the reading belongs to coverage start, and a
  record written into a progressed ledger would carry a day the replay has passed.
- **Atomic:** all model calls first (archived, so a rerun after a crash reuses them), then every record, link and the step row in one commit.

## Table 1: state × event

| State | Event | Transition, what is written, which day |
|---|---|---|
| seeds written, no baseline row, nothing processed | run starts, config has `baseline` | reads, checks, writes records + links + the step at the next sequence number (1), day = coverage start, in one commit |
| no baseline row, items or days already processed | run starts or resumes, config has `baseline` | refused before any call ("coverage start has passed in this ledger") |
| items database without `text_page`, or a chosen item's page text empty | run starts, config has `baseline` | refused before any call |
| seeds written, no baseline row | config has no `baseline` | nothing; behaviour as today |
| no T1 item before coverage start | run starts | step row with reason "no report"; no records |
| baseline row present, its day completed | run resumes or restarts | skipped; nothing written |
| baseline row present, its day not completed | run starts from that day | skipped; the day runs and its round judges the linked questions |
| baseline row present, its day not completed | run starts after that day | refused before any call (the first round would be lost) |
| calls half done | crash or transport failure after the transport's retries | nothing written (one commit at the end); the run stops before the first day; a rerun reuses the archived answers |
| an answer | reply not JSON / missing fields | the run stops with the error (no silent empty answer: a failed read is not an empty read, round 15) |
| a figure | check refuses it | dropped, reason in the step row |
| a figure kept by several questions | write | one record, one link per question (D364) |
| first day | `judge_day` | judges the questions in the baseline row's `changed` with the day's other changes |
| later days | any | the step never runs again; its records are evidence in force like any other (shown while arrivals or cited, D198) |
| a later run on another coverage start (new ledger) | run starts | reads that ledger's latest report before its own coverage start |

## Table 2: value × reader

| Value written | Readers (searched) | What they do with it |
|---|---|---|
| `evidence` row (quote, one-line, speaker, original_who, original_day, tier, created_seq = the step's sequence number, created_from_input = report item) | `judging._lines_english` via `evidence_in_view`; `jev_matching.thesis_text` (a question's first two pieces in force); the UI evidence lists; `store.last_check` | judged as a fact of the company dated the report day; becomes the first pieces Jev shows for that question (a production effect the end-to-end run measures); shown with its source |
| `evidence_sources` row (report item, T1, report day) | `store.evidence`, measure scripts | the source line "from <item> <day>" |
| `evidence_links` rows (the step's sequence number) | `evidence_in_force`, `evidence_in_view` (arrival seq), `views_linked_to`, `bundle` (`_visible(linked_seq)`) | in force from the start; an arrival for each question's first five judgements; shown in the dated bundle from the coverage-start day |
| `processing_steps` row `baseline` (the next sequence number, 1; day = coverage start) | `round.changed_views_of_day` (extended), `store.next_sequence` (the first item takes 2), `service.seq_day_map` (maps the number to the coverage-start day, so the records are visible from it), `replay.run`'s back-dating check (max day of rows above 0 = coverage start, not after the start day), `refuse_unfinished_parallel` (extracted rows only), `parallel_day`'s "day started" check (steps extracted/written/handed_over only), `dispatch.route` (per item id; never sees this id) | first-day judging; the records' day in the service and bundles; no other reader acts on it |

## Table 3: new path × old checks

| Old check | Does the new path meet it |
|---|---|
| The extraction's quote check (quote in the item's text, at least 8 characters) | yes, against the page text (the cleaned text has no tables); the row repair stores the exact source span, so a stored quote is always verbatim (as D236) |
| `judging.check_answer` (cites only shown ids) | yes: the records are ordinary evidence ids shown in the block (validated by the synthetic checks, rounds 13 and 16) |
| `parallel_day` day-started guard | not triggered (step name `baseline`) |
| `replay.run` back-dating guard | not triggered: the step's row is dated the coverage-start day, the run's first day |
| Seeds' numbering and ids | untouched; evidence ids continue the ledger's own numbering |
| D359 (the code builds only frozen versions) | the baseline builds only `baseline-v3`, refusing any other |
| Tests never call a paid service | the step's tests use a fake transport; `conftest.py` refuses credentials |

## Table 4: prior decisions

D363 (the mandate: once at coverage start from the latest report; restatements stay excluded on the daily path) · D364 (one record linked to each question that read
it; the daily path's one-home pruning, D207, D265, D360, does not apply to these records) · D209 (a dropped figure is dropped with its reason) · D274, D359 (frozen
extraction and judging untouched; this prompt is opened by D364) · D354 (judging-v7 unchanged) · D198 (evidence in view) · D191 (themes first in a round) ·
PRD 10 §6 (the acceptance run, the 14-day three draws, starts only on Alex's word, against a control re-run the same day).

## Known gaps, written down and not built (validated as they are)

- The capex line is missed in about 1 read of 6 per send (`census-all-reads.txt`); a miss leaves the question as it is today.
- Records are written with tier 'fact'; a labelled guidance figure the reading keeps (2 of 46 in May, the August outlook) is a party statement by the T1 rule.
- The reading runs once at coverage start; a later quarter's report reaches the questions only through the daily path.

## $0 verification before any paid run

1. The production step builds, for the 22 seeds on the May report under `poc-v116`, exactly the 44 requests of the validated third-version reading: the bytes the
   transport sends (`json.dumps` of the request as built, key order kept), compared with the validated builder's (`baseline_all.build(3)`); a request with its schema
   keys reordered is the negative control (equal archive key, different bytes, so the comparison must catch it).
2. With a transport serving the stored third-version answers (each of the three sends in turn), the records and links it writes equal the harness's kept figures
   (same quotes after repair, one-lines with the unit rule, the same questions linked), and the step row lists the same refusals.
3. The first day's `judge_day` picks up the linked questions (a ledger with the step and no other change judges exactly them).
4. The service (`service.view`) and the bundles (`bundle.library`, `bundle.thesis_bundles`) show the seeded questions and the records, with their sources and arrival
   days, from the coverage-start day and not before it.
5. Through the entry point (`scripts/replay.py` with `--seed` and `poc-v116`, a fake transport): a new ledger runs the step once; a resumed ledger skips it; a ledger
   whose coverage-start day did not finish resumes that day or refuses a later start; a progressed ledger without the step and an items database without page text
   are refused before any call.
6. The touched suites, the frozen-ruler and frozen-prompt tests, then the full suite.

## Review record

- Codex round 1 (`review-prod-codex-r1.md`): four serious findings, each checked against the code and accepted: records at sequence 0 invisible to the service and the
  dated bundles (`service.seq_day_map` maps only numbers above 0) → the step takes its own sequence number; `text_page` absent from `replay.py`'s default database →
  refuse before any call, name the database the acceptance runs use; a progressed ledger newly given the step → refused; equal archive keys do not prove equal bytes
  (the key sorts JSON keys) → compare the transport's bytes, with a reordered-schema negative control.
- Codex round 2 (`review-prod-codex-r2.md`): round 1's findings 2-4 confirmed; two serious and one minor, accepted: seeded questions (sequence 0) are invisible to the
  service and bundles (a gap since seeding) → the service maps sequence 0 to the ledger's first day; an interrupted coverage-start day could be skipped → a later start
  is refused until that day completes; two cells still said sequence 0 → corrected.

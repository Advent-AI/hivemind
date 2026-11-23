# Task C: the measuring method, audited

You are an independent reviewer of the repository `/Users/lchingen/hivemind` (branch `clean-arch`; sibling folder
`../tn-hivemind` holds the older system's lessons). **Read-only**: do not edit files, run model calls, start runs, or read
credentials or settings files. You are given no preferred conclusion and must not look for one: the folders
`docs/research/2026-11-14-use-acceptance/reflection-2/`, `reflection-3/` and `reflection-4/` hold earlier councils'
arguments. Do not open `reflection-4/` at all. Form your view from the design documents and the primary records first; if
you read `reflection-2/` or `reflection-3/`, read them last, as past attempts to be assessed, not as the answer.

The owner, Alex, wrote on 2026-11-15 (his words): "我觉得你的council 需要认真的end to end read 我现在的system design, 以及过去所有的尝试，
到底你要达到的目标是什么？是不是量测方法问题，我们已经stuck 很久了需要重新审视突破". In English: the council must seriously read, end to end,
the present system design and every past attempt; what is the goal we are actually trying to reach; is it a problem of the
measuring method; we have been stuck for a long time and must re-examine and break through.

Background you can verify: the project builds "Hivemind", a research system that reads news about a company, keeps a
library of questions (theses), files evidence under them and judges each question's answer. There are two systems: the one
called production (`poc/config/poc-v118.json`, code under `src/hivemind/`, design in `docs/system-design.html` with data in
`docs/system-design/new-*.js` and one PRD per module in `docs/prd/`), and a rebuild in `clean-arch/` (`clean-arch/PRD.md`).
`AGENTS.md` holds the working rules and names the frozen measuring standard ("the ruler", §7.1). `docs/DECISIONS.md` is the
index of every decision (one row each, about 560); `docs/DECISIONS-log.md` holds the full records (large: search it, do not
read it whole unless your task says so). `docs/CURRENT_STATE.md` is the status page.

Rules for your report: every claim cites the file (and decision number or line) you read it in; say what you read first-hand
and what you infer; quote the documents where the wording decides; no finding about modules upstream of reading the news
(the research universe, classification, dispatch, configuration) unless it bears on the three questions; write for a reader
who did not follow the project; plain words; at most about 1,500 words plus tables. Your final message is the report.

## Your reading

The instruments in use, each with its definition, its code and its results:
- the frozen ruler (`AGENTS.md` §7.1): the extraction standard and `docs/research/2026-10-29-ledger-standard/golden-v5/`; the
  questions gold (must_open / may_open) and the seeds `poc/seeds/nvda-2026-07-01-v2.json`; the judgement ruler
  `docs/research/2026-11-01-e2e-loop/judgement-gold/` (`ruler-v1.md`, `reader-brief.md`, `gold-v1.json`, `score_judgement.py`,
  `corrections-v1.json`); how questions a system opens by itself are matched to it (`clean-arch/unseeded-2026-11-10/MATCHING-v2.md`);
- Alex's six lines for the step that writes a question's answer choices (D400; `clean-arch/step4-2026-11-10/DESIGN.md`), the
  reading form and its accounting (`clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md`,
  `clean-arch/step4-2026-11-10/stage_a/accounting.py`, `collect_readings.py`), and the four readings taken with it
  (`docs/research/2026-11-14-use-acceptance/second-week/FIRST-GATE-MAP.md`, `RESULT.md`);
- the use-oriented acceptance (`docs/research/2026-11-14-use-acceptance/ACCEPTANCE-DESIGN.md`, `TRIAL-DESIGN.md`,
  `TRIAL-RESULT.md`, `LEAN-LOG.md`) and the gates as listed in `NEW-SYSTEM-FRAME.md`;
- the end-to-end comparisons (`clean-arch/e2e-comparison-2026-11-13/`, `clean-arch/unseeded-2026-11-10/`,
  `docs/research/2026-11-04-filing-end-to-end/`), and `docs/prd/10-filing-phase.md` §6.
Search `docs/DECISIONS.md` for: ruler, gold, reader, split, null, control, variance, draw, line, pass.

## Answer

1. **One row per instrument:** what it measures and at which point of the pipeline; its unit and how many units a
   measurement has; who or what does the judging; what it costs in time and money per use; how many times it has been used
   and how often anything passed.
2. **Is each instrument's own error known?** For each: has the reference itself, or a second draw of the same system, been
   put through it (a null or a control)? How far do two readers, or two draws, differ with nothing changed? Could a system
   that serves the product's purpose fail it, and could one that does not serve it pass? Give the evidence from the record.
3. **Validity:** which instruments measure the thing the product is for, and which measure agreement with one reference's
   particular choices (for example a question's exact shape) or a step's internal form?
4. **Conditions:** under what conditions was each measurement taken (which days of news, starting from what library, with
   or without preset questions, how many draws), and do those conditions match how the design says the product runs?
5. **The record's own warnings:** places where the working rules or earlier decisions already said how a measuring stick
   must be checked before use, and whether that was done for each instrument.
6. **Verdict with evidence both ways:** is the project stuck because the product does not work, because the measuring
   cannot tell, or both? Which specific findings about the product do you consider established regardless of the
   measuring problems?
7. **What a sound measurement would be:** one that sits where the product is judged, accumulates from run to run, has a
   known error rate, and can be read by Alex himself in under an hour. Describe it concretely from what already exists in
   storage; say what it would cost and what it could not show.
8. **Your own answer to Alex's three questions,** each in two or three sentences, with what would change your mind.

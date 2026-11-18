# Task B: every past attempt, read end to end

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

Read `docs/DECISIONS.md` whole (the index rows from D229 to the end are the spine: read every row). Open
`docs/DECISIONS-log.md` for any decision whose row is not enough. Read `../tn-hivemind/docs/LESSONS.md`,
`docs/CURRENT_STATE.md`, and the round logs: `docs/research/2026-11-01-e2e-loop/` (its log and design files),
`docs/research/2026-11-04-filing-end-to-end/log.md`, `clean-arch/takeover-2026-11-07/LOG.md` (if present),
`clean-arch/step1-unfiled-2026-11-08/LOG.md`, `clean-arch/step2-validation-2026-11-07/LOG.md`, the result files under
`clean-arch/step4-2026-11-10/` and `clean-arch/e2e-comparison-2026-11-13/`, and
`docs/research/2026-11-14-use-acceptance/LEAN-LOG.md`.

## Produce

1. **A timeline table of every measured attempt to improve the product since 2026-10-29** (the first signed standard), one
   row each: date; decision numbers; what was changed (a prompt sentence, a schema field, a model or effort, a new step, the
   architecture, a rule in code, the measuring method); what it was measured on (which standard or reading, which articles,
   starting from what library, how many repeats); the result in its own numbers; adopted, rejected or left open. Be complete
   rather than brief here; group rows by week.
2. **Classes of attempt:** group the rows; for each class give how many times it was tried, how many were adopted, and the
   reason the record gives for the failures.
3. **What actually moved the result where the product is judged** (the final judgement of a question, or a reader's use),
   as opposed to a step's own count? List each such result with its size and how sure the record is.
4. **Circles:** conclusions, proposals or questions to Alex that were reached more than once, with their dates and decision
   numbers; and decisions or requirements of Alex's that later work did not follow.
5. **What stayed constant through all attempts** and could be the real constraint: the measuring standard and its test
   window, the starting state of each test, the readers, the model, the architecture, the working process itself.
6. **What was never tried.**
7. **Your own answer to Alex's three questions,** each in two or three sentences, with what would change your mind.

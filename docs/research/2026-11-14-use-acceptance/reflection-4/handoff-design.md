# Task A: the goal and the design, read end to end

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

Read end to end: `docs/prd/README.md`, `docs/prd/00-system.md`, `docs/prd/05-extraction.md`, `docs/prd/06-views.md`,
`docs/prd/07-final-verdict.md`, `docs/prd/08-pull-mode.md`, `docs/prd/10-filing-phase.md`,
`docs/prd/11-production-experiments-from-split.md`, the design page's data (`docs/system-design/new-design.js`,
`new-facts.js`), the signed extraction standard (`docs/prd/05-extraction-standard.html`, with
`05-extraction-standard-corrections.md`), `clean-arch/README.md`, `clean-arch/PRD.md` (sections 1 to 11 and 15 to 19 in full;
skim the prompt sections 12 and 13), `clean-arch/HANDOFF-2026-11-10.md`, `AGENTS.md` (sections 7 and 8 and "Where to look
first"), `docs/CURRENT_STATE.md`, and `docs/research/2026-11-14-use-acceptance/NEW-SYSTEM-FRAME.md` with `ACCEPTANCE-DESIGN.md`.
Search `docs/DECISIONS.md` for the words goal, production, acceptance, pass line, lines.

## Answer

1. **What is the system for, in a user's terms?** What does a hedge-fund analyst open, read and do with it? Quote the design.
2. **What is the written goal the work is trying to reach?** List every place that states a goal, a pass line or an
   acceptance for "ready for production" or for a phase (with numbers where given, and who set them: Alex's words, a
   council, or a proposal). Do they agree with each other? Is there one quantified production goal, several, or none?
3. **Trace the goal to what is measured.** For each line or gate in force (find them), say which part of the goal in 1 it
   stands for, and which parts of the goal no line measures.
4. **The two systems.** What decision between them is owed, on what criterion, and what does the record say is still
   missing before it can be taken?
5. **What in the design has never been run or measured in the condition the design itself describes** (for example a
   library that persists across weeks, questions that reach their due day, a reader using the output)?
6. **Your own answer to Alex's three questions,** each in two or three sentences, with what would change your mind.

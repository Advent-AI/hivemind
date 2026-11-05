# Brief: classify every recorded decision by what still holds today (read-only first pass)

Repository: /Users/lchingen/hivemind (branch docs/consolidate-2026-11-05, identical to main at 20ab1bd). The decision log is
`docs/DECISIONS.md` (D1–D366, 365 entries; D90 does not exist; D275–D336 were renumbered from main's D181–D241/D258/D259 at the
2026-11-03 merge and D337–D352 are main's uncommitted decisions of 2026-10-27, so dates are not monotonic). Alex (the owner) asked
for the decisions and the working rules to be consolidated: the log is too long, out of hand and holds conflicting statements. This
pass produces the raw material: one record per decision in your range. Do not edit any file in the repository.

## What "today" is (2026-11-05, main at 20ab1bd)

- Replay default `poc/config/poc-v116.json` (D366) = `poc-v108` (frozen production extraction prompt v74i, D274) + the coverage-start
  reading (D363–D365). One-decider architecture (D264: the extraction files each statement under the day-start open questions; no
  placement call). Jev matching with the collision judge (D169, D190). Judging-v7 (D263). Steps 3 and 4 frozen (D354). Closing at the
  due day belongs to pull mode; no separate final verdict (D356). The code builds only extraction v74i, judging-v7, baseline-v3 (D359).
- The frozen ruler (D261, D262): extraction standard v3 (`docs/prd/05-extraction-standard.html`, signed D243, with D250's boundaries),
  golden-v5, seeds v2, the judgement gold (reader B). Never edited.
- Maintained English since D163. The service serves the sealed ledger `served-2026-10-28-v34-nvda-3m-through-0828` (D358); the Idea API
  runs `poc-v33-idea` (D290, D335). Frontend presentation rules: `docs/poc/thesis-ui.md#presentation-rules`.
- Governing documents: `docs/prd/00-system.md` … `10-filing-phase.md` (index `docs/prd/README.md`), the design page data
  `docs/system-design/new-*.js`, `docs/prd/05-extraction-standard.html`, `docs/poc/thesis-ui.md`, `docs/poc/idea-card.md`,
  `docs/poc/service.md`, `docs/poc/pipeline-plan.md`, `AGENTS.md` (working rules), `docs/CURRENT_STATE.md`.

## For each decision in your range, decide

1. **area** (one): `system` (PRD 00, the whole design) · `universe` (PRD 01) · `classification` (PRD 02) · `config` (PRD 03) ·
   `dispatch` (PRD 04) · `extraction` (PRD 05, the extraction prompts and standard as product behaviour) · `library` (PRD 06: questions,
   ladders, evidence records, matching, writing, judging, themes, dependencies) · `closing` (PRD 07 final verdict and PRD 08 pull mode) ·
   `review-pool` (PRD 09) · `filing-phase` (PRD 10, incl. the coverage-start reading) · `ruler` (golds, standards as measuring sticks,
   scoring, acceptance and measurement method) · `idea-service` (Idea API, service, MCP, idea card) · `frontend` (UI presentation) ·
   `data` (item databases, corpus, sources, cleaning) · `operations` (replay, parallel day, run settings, repository cleanups, servers,
   Docker, worktrees) · `working-rules` (how Claude works with Alex: authority, language, process, documentation method).
2. **status** (one): `in-force` (its rule still holds today, possibly amended) · `superseded` (a later decision replaced it; name it) ·
   `retired` (what it governed was removed or abandoned, with no replacement) · `record` (a record of an experiment, measurement, run,
   probe, version adoption later replaced, or one-off step: no standing rule of its own). A version-default decision ("poc-vNN is the
   default") is `superseded` by the next default decision. Check later mentions: grep the whole log for the decision number (e.g.
   `grep -n "D24\b" docs/DECISIONS.md`) and read what later decisions say about it; check the PRD or the code when the question is
   whether a mechanism still exists.
3. **rule**: if in-force, the standing rule in one or two present-tense sentences, faithful to the decision's own words (no new rule,
   no strengthening, no softening). Empty otherwise.
4. **by**: the later decision(s) that superseded, amended or retired it (list), and **amends**: earlier decisions it amends or replaces.
5. **authority**: `alex` (rests on Alex's own words or his reply to that exact question), `claude` (a detail Claude settled within a
   decision Alex made, or Claude's own process choice recorded without his words), `unconfirmed` (marked not confirmed / pending him).
6. **quote**: Alex's words the decision rests on, copied verbatim from the log (≤ 200 characters; empty if none).
7. **home**: where the standing rule belongs (a PRD file and section, `AGENTS.md §n`, `docs/poc/thesis-ui.md`, `docs/poc/idea-card.md`,
   the extraction standard page, code path) — and **home_agrees**: `yes`/`no`/`unchecked` (does that document currently state it
   consistently? check when cheap; say `no` with the sentence when it contradicts).
8. **conflicts**: in-force decisions (any range) or governing-document sentences that contradict this one, each with one line why.

## Output

JSON Lines, one object per decision, in log order, keys exactly:
`{"id","date","title","area","status","rule","by","amends","authority","quote","home","home_agrees","conflicts","note"}`
(`by`, `amends`, `conflicts` are lists; `note` ≤ 200 characters, only when needed). No prose before or after the JSON Lines.
Every decision in your range appears exactly once. Be exact; when unsure of a status, say so in `note`.

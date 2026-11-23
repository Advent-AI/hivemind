# Council gi: after the handoff of 2026-11-10, what is the next implementation step? (independent cold read; read-only)

You are an independent member of a council with Claude Code. Read-only: do not edit files, run model calls or start runs.
Claude is reading the same material in parallel and has written its own reflection, which you are not shown. Read the record cold.
Do not assume the earlier conclusions, the handoff's recommendation or the earlier council's verdict are right.

## The question

Alex's instruction for this session: take the handoff, review the recent learning history in full, and run the council to decide the
next step of implementation to tackle.

His last decision is D396 (2026-11-10): "设计新系统自己的“判断”环节" — design the clean system's own judging step (Step 4); its first
test is independent readers checking, against the sources, whether the system's answers to its own questions are well supported; a
build and any paid run wait for his word. The design was written and an earlier council found it NOT READY with four blocking items.

## Constraints (AGENTS.md governs; read it first)

- Frozen, never edited: the ruler (AGENTS §7.1); production extraction v74i and judging-v7 with their checks (D274, D354, D359); the
  clean Step 1 request c8 (D387, D391) — a change to it is a new version only Alex opens.
- D370 and Alex's 2026-11-08 ruling: no preset questions; financial figures are evidence, not questions.
- D38: a judged question has a fixed ladder (five rungs; two for a yes/no event) and a due date, never rewritten.
- AGENTS §7.3: every proposed change names its expected effect on a reader or the final judgement; one recommendation and one test go
  to Alex; no prompt is tuned on the cases of the 243-item window that the unseeded misses came from (council gf).
- "Add no mechanism, safeguard or substitute rule for a case no one has named" (AGENTS, Authority and scope).
- Out of scope, do not review: `clean-arch/step2-validation-2026-11-07/LOG.md` and `reports/step2-*` (another session's work);
  production modules Alex has not taken up; the frontend; the Idea API.

## Primary materials

- `clean-arch/HANDOFF-2026-11-10.md`; `docs/CURRENT_STATE.md` (top section and "One next task").
- The round log `clean-arch/step1-unfiled-2026-11-08/LOG.md` §§47–68 (the D388 line, the priorities council, the seeded and unseeded
  end-to-end measurements, q12, the Step 4 design).
- Decisions D38, D186, D191, D195, D198, D260, D354, D359, D368, D370, D382–D396 (`docs/DECISIONS.md` index and §7; full records in
  `docs/DECISIONS-log.md`).
- The design `clean-arch/step4-2026-11-10/DESIGN.md` and the earlier verdict `clean-arch/step1-unfiled-2026-11-08/council/gg-codex.md`.
- Production code the design leans on: `src/hivemind/prompts/role-v74i.txt` (lines 19–35), `src/hivemind/extraction.py`
  (`check_ladder`, `normalise_ladder`, `check_bounds`, `check_admission`, the candidate schema), `src/hivemind/views/writing.py`
  (`_create_view`), `src/hivemind/views/judging.py`, `src/hivemind/views/store.py`, `src/hivemind/prompts/judging-v7.txt`.
- The clean path: `clean-arch/PRD.md` §§4–7 and §12 (the c8 schema: a new thesis carries description, outcome, period, opens_as,
  settled_by, closest_open_thesis, why_a_separate_bet); `clean-arch/e2e-2026-11-09/adapter.py` and `budget.py`.
- Stored data ($0): the theses the three unseeded draws opened, `clean-arch/unseeded-2026-11-10/opened-u1.json`, `opened-u2.json`,
  `opened-u3.json` (34 theses); the matching and result files beside them; the draws in `poc/data/clean-unseeded-2026-11-10/`
  (open any SQLite file read-only).

## Deliver (under 1,400 words; facts and hypotheses kept apart; cite a file and line or a record for every fact)

1. **The lessons of §§47–68 at mechanism level**, and any conclusion in the handoff or the log that is weaker than it is stated.
2. **The remaining problems ranked by product impact**, each with its evidence. Say plainly whether Step 4 is the right next thing to
   build, or whether something else should come first, and why. If you would order the work inside Step 4 differently from the
   design, say how.
3. **The Step 4 design, read against the 34 stored theses.** Walk the stored theses through the proposed ladder call and the frozen
   judge as they stand in code: which thesis shapes would break or be distorted (compound questions, free-text periods, theme against
   asset, direction of a five-rung ladder, thresholds with no reference figure in the opening article, the judge's refusal classes)?
   Give counts on the 34, by class, and name two theses per class.
4. **For each of the earlier council's blocking items 1–3,** what a complete answer must contain, and which parts existing decisions
   already settle (cite the decision) against which are product choices only Alex can make.
5. **One recommendation and one test:** the next implementation step, the cheapest decisive check of it (stored data first), its
   denominators, and the result that would falsify it.

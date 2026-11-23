# Council A: design the Step 2 validation (independent investigation; read-only)

You are Codex, the second member of a council with Claude Code. Read-only: do not edit files, run model calls or start runs.
Investigate independently; Claude is designing in parallel and you will challenge each other. Read cold.

## Objective, contract, pass line, data
Read `clean-arch/step2-validation-2026-11-07/LOG.md` §0 (the frame). The design contract is `clean-arch/PRD.md` §§5–6 and §13 (the
Jev draft). The stored Step 1 output is `poc/data/clean-step1-takeover-2026-11-07/gold-k6b-flash/trace.sqlite` (table `trace`,
column `result` holds each article's kept evidence with links, `new_thesis_ids` maps local ids, `after_state` holds the library).
Existing code to reuse or not: `src/hivemind/search.py` (embeddings; it indexes theses), `src/hivemind/jev.py` (transport; one
request = one state and several typed questions), `src/hivemind/views/jev_matching.py` (`PIECES`, `piece_state`, `piece_question`
assume the stored piece is under the same thesis), `src/hivemind/views/matching.py` (`rank_evidence`, the production word-overlap
reference). Prior evidence on Jev comparisons: `poc/eval/gold/evidence-decisions-seed-2026-10-25.json`, `scripts/score_evidence_gold.py`,
and the decisions D168, D202, D204 in `docs/DECISIONS-log.md`.

## Deliver
1. How to build the pair ground truth so it does not inherit the system under test's blind spots: how candidate pairs are generated
   (independently of the embedding search being tested), how readers label them (repeat, revision, different-party forecast of the
   same quantity, different), how to estimate the pairs the generator missed, and what a reader must see.
2. The retrieval design to test: what text is embedded, what the query is ({thesis, evidence}), the entity-wide scope, strict
   forward order, and the production word-overlap reference arm.
3. The comparison design: how the Jev question must change for cross-thesis candidates, what fields the state carries (party, dates,
   tier, period), how several candidates with conflicting labels are resolved (open for Alex), and which existing decisions bound it.
4. Metrics and the pass line: is the proposed line right, and what else must be measured (wrong merges by type, revision taken as
   repeat, dossier size per thesis after dedup).
5. The cheapest decisive sequence: what is done at $0, what costs cents, what would falsify the plan at each step.
Facts and hypotheses apart, files cited. Under 1,500 words.

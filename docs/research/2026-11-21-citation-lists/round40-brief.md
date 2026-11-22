# Council round 40: the paid acceptance probe of judging-v12, design review (read-only)

Alex approved $0.50 for a paid acceptance step of the citation-only judge (D715; his words in `docs/DECISIONS-log.md` D715). Review
`docs/research/2026-11-21-citation-lists/PROBE-DESIGN.md` before any harness is written. Context: `DESIGN.md`, `RESULT.md`,
`probe_plan.py` and its output `probe-plan.json` (the planned requests), `src/hivemind/views/judging.py`, `src/hivemind/model.py`,
`clean-arch/e2e-comparison-2026-11-13/budget_replay.py` (the ledger). Out of scope: the frozen ruler, the prompt text, the link direction,
other modules. No paid call.

Questions:
1. Does each part answer its question, and is the reading rule exact enough to apply blind (targets frozen before answers are read;
   the classes; the Part C flag)? Find a case it misclassifies or a way it could pass while the format is harmful.
2. Is the outcome rule right (Q1; at most 2 misattributions of 48; no refusal; no confirmed Part C effect)? Is 2 of 48 defensible, or
   should it be stated differently?
3. Is the plan right: 16 distinct refused requests (8941 is 8938's retry), linked-1's v8-shaped requests sent with v12's builder's format,
   the matched requests, the fresh v7 control, the sealed request as a counting check, the order and the cost (about $0.43 of $0.50)? Is
   anything worth dropping to protect the margin, or missing?
4. The $0 proof before the send: enough?
Answer READY TO BUILD THE HARNESS or NOT READY with the blocking items.

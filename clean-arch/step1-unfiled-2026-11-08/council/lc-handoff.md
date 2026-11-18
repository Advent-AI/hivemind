You are an independent reviewer, read-only. Do not run model calls, start runs, or write files. You have not seen this work
before. Cite files and lines.

Context: repository `/Users/lchingen/hivemind`, branch `clean-arch`; rules in `AGENTS.md` (§1 diagnose, §2 design incl. "Code owns
identity, never importance" and "No case-fitted fix", §6 prompts incl. "Never grow a prompt to fix quality" and "move the rule to
its owner … the schema beside the field", §7.3 one class at a time). Alex chose (D432 in `docs/DECISIONS-log.md`) a diagnosis of
how clean Step 1 cuts a matter into theses, with one proposed change, before any build. Step 1 is c8 (D387), frozen.

The diagnosis and proposal: `clean-arch/step1-diagnosis-2026-11-12/DIAGNOSIS.md`. Its sources: the unseeded draws' Step 1
requests and raw answers `poc/data/clean-unseeded-2026-11-10/draw-d1|d2|d3/trace.sqlite` (table `trace`: `input_id`, `request`,
`result`; read-only), the opened theses `clean-arch/unseeded-2026-11-10/opened-u*.json`, `result.txt`, `adjudication-runs.md`,
round log `clean-arch/step1-unfiled-2026-11-08/LOG.md` §67, Stage B's no-ladder reasons in
`poc/data/clean-stage-b-2026-11-11/draw-u*/views.sqlite` (table `clean_ladders`), `clean-arch/step4-2026-11-10/stage_b/CONTROL_TRACE.md`,
the decisions D38, D248, D397 (`docs/DECISIONS-log.md`), and c8's prompt (`clean-arch/PRD.md` §12, or the `request` field above).

Out of scope: the frozen ruler, the judge, Step 2/3, the ladder step's text.

Challenge:
1. Read the raw Step 1 answers for the key articles (`gnews:92c7e54d38dc2916aa185568`, `gnews:d0f3f83296df884fae64921e`,
   `gnews:f8191f5bb960d79e47c73d6c`, `gnews:4d1677af37befd53ca3e7b45`) in all three draws. Is each row of the diagnosis right?
2. Is "two figures, periods or events in one thesis" really the largest class and the right first target, by product impact?
   Is D38 correctly quoted and still in force for theses (D397 makes Step 4 judge one question a thesis)? Does any decision
   (D248's "periods of one bet are one question", AGENTS §8) bound or contradict it?
3. Is the proposed change (a typed `tracks` field with D38's unit as its definition, a code check on shape only) sourced, general
   across companies, and the smallest structural lever? What could it break (trivia splits, recall, linking of evidence that
   spans years)? Is the falsifier adequate?
4. Anything larger the diagnosis misses?

End with one line: the diagnosis stands / stands with corrections / does not stand; and whether the proposal is ready to put to
Alex (yes / yes with changes / no).

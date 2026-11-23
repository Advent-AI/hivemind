You are an independent reviewer, read-only. Do not run model calls, start runs, or write files. You have not seen this work
before. Cite files and lines.

Context: repository `/Users/lchingen/hivemind`, branch `clean-arch`; rules in `AGENTS.md` §5 ("A re-sent request is the bytes
production sends"), §6 (prompts: "The prompt carries the standard, not new rules", "Check before the send, at no cost"), §7.3
("Council before every change is sent", "Small first"). Alex opened Step 1 candidate c14 (D433 in `docs/DECISIONS-log.md`): c8 with
two sentences changed, tested small first. The diagnosis behind it: `clean-arch/step1-diagnosis-2026-11-12/DIAGNOSIS.md`
(version 8, cleared by seven council rounds, `clean-arch/step1-unfiled-2026-11-08/council/lc`–`li-codex.md`).

Review before the first send:
- the changed request: `clean-arch/step1-unfiled-2026-11-08/arms/c14-system.txt`, `c14-closing.txt`, `c14-schema.json` against
  `c8-*` (diff them);
- the prompt audit: `clean-arch/step1-diagnosis-2026-11-12/PROMPT-AUDIT-c14.md`, against the frozen standard
  `docs/prd/05-extraction-standard.html` (§3 table row D, §4) and D38, D248, D397;
- the probe: `clean-arch/step1-diagnosis-2026-11-12/probe_c14.py` and its cases `cases-c14.json` (the stored c8 requests in
  `poc/data/clean-unseeded-2026-11-10/draw-d*/trace.sqlite`, read-only; the runner's checks in `clean-arch/step1/runner.py`);
- the plan and stop lines: DIAGNOSIS.md "The first test". Note the cost correction: the full design is about $2.0 at the stored
  mean output (9,490 tokens a call), not the $0.5 first stated; Alex approved "约 0.5 美元". The plan is now staged: the main case
  alone first (c8 and c14, three sends from each of three draws' stored state, 18 sends, about $0.25); the controls only after a
  pass, with Alex asked about their cost.

Questions:
1. Does c14 change exactly the two sentences D433 names, and nothing else? Does the probe send, for c8, the stored request as
   production sent it, and for c14 the same request with only those texts replaced?
2. Is the prompt audit right (each verdict against the standard's line)? Does c14 carry the standard, not a new rule?
3. Is the staged plan sound: is the main case alone with a c8 arm a fair first stage, with the pass line "c14 opens both years as
   separate theses in at least 8 of 9, c8 in at most 2 of 9", and does staging lose anything the controls were meant to catch
   before a decision is taken? Is anything in the probe's counting wrong (its automatic count is a lead; every send is read by hand)?
4. Anything that should stop the first send?

End with one line: ready to send the main case (yes / yes with changes / no).

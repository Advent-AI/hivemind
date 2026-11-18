You are an independent reviewer. Read-only: do not edit files or start runs.

**Context.** The answer-choice step was sent at two reasoning efforts, `medium` and `high`, three draws each, on 26 topics. Two model
reader families marked each answer with `/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md`
(the full gate form). The hard lines are Q, L, R and N.

**The files:**
- the run: `/Users/lchingen/hivemind/poc/data/clean-effort-probe-2026-11-16/` (each arm-draw's `outcomes.jsonl`);
- the reading: `reading/send-1/outcomes.jsonl` and `reading/readers/packet-*.json`;
- the two families' rows: `reading/readers-answers/reader-{codex,claude}-packet-*.jsonl`;
- the key from item to arm and topic: `/Users/lchingen/.hivemind-keys/effort-probe/key.json`, which you may read;
- the cases: `poc/data/clean-carried-run-2026-11-16/c1/cases/cases.json` and
  `poc/data/clean-second-week-2026-11-15/week-continued/c1/cases/cases.json`.

**The task.** Find every item where BOTH families mark a hard line (Q, L, R or N) as "fails". For each such item in the `high` arm,
and for each topic where the medium and high arms' agreed failures differ, read the item against its topic, its article and the
brief. Put each agreed failure down as one of:
- ANSWER ERROR: the answer breaks the rule as written;
- READER ERROR: the answer meets the rule and both readers misapplied it;
- UNRESOLVED.

Then say:
1. how many agreed failures of each arm are answer errors;
2. whether any reader error changes the medium-versus-high comparison (13 against 14 failed sends, counting one code refusal in each
   arm);
3. which fault classes dominate both arms, with their counts (for example, L: a part of the outcome not listed). Look for one shared
   mechanism behind most failures, and quote two examples.

Write a table, then the three answers. Be concise.

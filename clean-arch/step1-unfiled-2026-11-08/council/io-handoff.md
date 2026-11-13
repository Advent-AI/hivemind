# Council io: independent read of three changes to a request, before it is sent again on six cases (read-only)

A new step's request was sent once on six stored theses (a probe, decision D402 in `docs/DECISIONS-log.md`). The answers showed
three classes of fault; the model's own account located each; Alex decided (D404, D405) that the request gets one change for each,
that the check on a reference's words stays strict, and that the same six are then sent once more. Read the three changes before
that send. Do not edit files, run model calls or start runs.

## Read

- The request as first sent: `clean-arch/step4-2026-11-10/probe-2026-11-10/sent-system.txt`, `sent-closing.txt`, `sent-schema.json`.
- The request as it now stands: `clean-arch/step4-2026-11-10/ladder/candidate-system.txt`, `candidate-closing.txt`,
  `candidate-schema.json`. Diff them yourself; besides the three changes, the closing check and three schema descriptions
  repeat them.
- What the probe showed: `clean-arch/step4-2026-11-10/probe-2026-11-10/READING-claude.md`; the answers, `answers.jsonl`; the
  model's own accounts, `accounts.json`.
- The standard: `docs/DECISIONS-log.md` D38 (a theme's outcomes are named by outcome, "with no bull or bear"; a view is written
  once and judged later), D397, D398, D403, D404, D405; production's frozen sentences `src/hivemind/prompts/role-v74i.txt` lines
  20 to 26; the prompt principles of `AGENTS.md` §6 (a general hedge-fund brain, no sentence fitted to the covered company or a
  test article; a closing check that repeats only rules stated above it; a request never asks for what a check refuses).

## Answer, in under 400 words

1. For each of the three changes: does it say what its decision asks, and nothing wider or narrower? Does it contradict any
   other sentence of the request, the schema or the closing check?
2. Is any new wording fitted to NVIDIA or to one of the six test articles, rather than general?
3. Would the new sentences push the model to a new fault on the three cases that were right (a yes/no event; a topic that asks
   several things; a topic with no main thing)? Say which sentence and how.
4. First line of your answer: "send", or "hold" with the one thing to change and the exact words you would use.

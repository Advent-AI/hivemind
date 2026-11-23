# Question identity reading for a measured run (read-only)

You decide, for each question a system opened by itself in one run, whether it is the same question as one of 23 reference questions.

**Files** (in `clean-arch/e2e-comparison-2026-11-13/matching/`):
- `opened-p<N>.json`: the run's opened questions (run, id, the item where opened, description, outcome, period). N is the run
  number given below.
- `ruler-questions.json`: the 23 reference questions. Read each one's full entry in
  `docs/research/2026-11-01-e2e-loop/judgement-gold/questions-v1.json` when deciding.

**The rule.** Apply MATCHING-v2.md §1, read in full.
- An opened question is the same as a reference question when the same reported figure or event settles both.
- Three kinds of extra wording do not separate them:
  - a part, programme or single deal of a reference total;
  - the same event under another deadline;
  - a later milestone, variant or parenthetical widening that the question's own check does not rest on.
- An amount held at a different date is not the same.
- A yes/no signing question beside an amount question stays apart.
- Extra scope that is its own check and could resolve on its own stays apart.

**For every opened question, write one line of JSON:**

{"run": ..., "id": ..., "match": "q05" or "none", "relation": "same" | "broader" | "narrower" | "overlapping" | "unrelated", "reason": "<one sentence>"}

Judge from the texts alone; do not consider how either question would be scored. Output only the JSON lines.

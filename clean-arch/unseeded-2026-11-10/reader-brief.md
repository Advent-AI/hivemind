# Question identity reading (read-only)

You decide, for each question a system opened by itself, whether it is the same question as one of 23 reference questions.

**Files** (in `clean-arch/unseeded-2026-11-10/`):
- `opened-dev.json`: 28 opened questions from three runs, with run, id, the article where each was opened, description, outcome and
  period.
- `ruler-questions.json`: the 23 reference questions, with id, question, unit and due day.

**The identity rule.** Read AGENTS.md §8, "A senior analyst's granularity", and D248 in docs/DECISIONS-log.md first.
- Wordings, deadlines, milestones and periods of one bet are one question.
- Two questions stay apart only when their answers can move apart and an analyst would bet on each separately.

**For every opened question, write one line of JSON:**

{"run": ..., "id": ..., "match": "q05" or "none", "relation": "same" | "broader" | "narrower" | "overlapping" | "unrelated", "reason": "<one sentence>"}

- **"same":** the same bet. A different deadline or wording is allowed only when it cannot make the answers move apart in a way an
  analyst would bet on.
- **"broader", "narrower" or "overlapping":** related to the reference question named in "match", but a different bet. Name the nearest
  one.
- **"unrelated":** match "none".

Judge from the texts alone. Do not consider how either question would be scored. Output only the 28 JSON lines.

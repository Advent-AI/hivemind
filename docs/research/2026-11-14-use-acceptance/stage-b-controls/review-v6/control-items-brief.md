# Stage B: checking whether a reference's evidence reached the judge (read-only)

You are an independent reader. Everything you may use is in this message. Do not read any file or run any command.

Each item in this message gives a **judged question** that the system wrote for a thesis it opened. The question comes with its unit, its due
day and its rungs. The item also gives two lists:
- **The reference's decisive items:** the evidence that an independent analyst cited for their answer to this question. Each item has its id, its
  day, its title, its passage and its meaning.
- **The evidence shown to the judge:** every evidence entry that the system's judge was shown for this question, in any of its requests on or
  before 2026-07-14. The list is empty when there is none.

You are not told any answer, and you do not judge which answer is right.

For **each** of the reference's decisive items, by its id, answer one question:
- **shown** when its content is present in the evidence shown to the judge (the same fact or figure, in any wording, from any source);
- **not_shown** when it is absent.

Search the entries for the figure or the fact; do not mark an item shown because a related item is.

Return one JSON object per control, one per line, in the order given, and nothing else (no prose, no code fence):
`{"control": "c03", "items": {"i005": "shown"|"not_shown", ...}, "why": "one sentence naming what decides each not_shown"}`.

## Third reader (only where the two readers differ)

A third reader of each family gets this brief, the same items, and a list of the disputed points. Each point is a control id (c01 to c15) and an item id.
The third reader is not given the two readers' answers.

For each point, answer that one question afresh by the rule above. Return one JSON object per point, one per line, and nothing else:
`{"control": "c03", "field": "item i005", "ruling": "shown"|"not_shown", "why": "one sentence"}`.

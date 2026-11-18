# Stage B: reading the control theses (read-only)

You are an independent reader. Do not edit files, run model calls or start runs, and do not read any file other than this brief
and the one packet you are given.

Each item of your packet pairs a **ruler question** (a question written by hand for an earlier, frozen measurement, with its
unit, due day and ladder of rungs) with a **judged question** the system wrote itself for a thesis it opened (its question, the
outcome it looks at, due day, year and rungs). It also lists **reader B's decisive items**: the evidence an earlier reader, called
reader B, cited for the frozen answer to the ruler question (each with its day, title, passage and meaning), and **the evidence
shown to the judge**: every evidence entry the system's judge was shown for the judged question in any of its requests on or
before 2026-07-14 (empty when there is none). You are not told either answer, and you do not judge which answer is right.

For each item, answer three questions.

1. `same_question`: **yes** when the judged question asks what the ruler question asks: the same quantity measured the same way
   (the same total, scope and unit: not a part of it, a ceiling on it, another quantity or another unit), or the same event,
   for the same period. **no** otherwise. Wording may differ; a judged question that asks for more or less than the ruler's,
   or for another period, is **no**.
2. `same_due`: for an **event** (a yes-or-no question), **yes** only when the judged question's deadline is the ruler's
   deadline. For a **figure**, **yes** when the two due days both mark the publication of the same period's figure (for
   example, both the annual report of the same fiscal year, even if the two days differ); **no** otherwise.
3. `items`: for **each** of reader B's decisive items, by its id, **shown** when its content is present in the evidence shown to
   the judge (the same fact or figure, in any wording, from any source), **not_shown** when it is absent. Search the entries for
   the figure or the fact; do not mark an item shown because a related item is.

Return one JSON object per item, one per line, in packet order, and nothing else (no prose, no code fence):
`{"control": 3, "same_question": "yes"|"no", "same_due": "yes"|"no", "items": {"i005": "shown"|"not_shown", ...}, "why": "one sentence naming what decides each no and each not_shown"}`.

## Third reader (only where the two readers differ)

A third reader of each family is given this brief, the packet, and a list of the disputed points, each a control number and a
field (`same_question`, `same_due`, or `item <id>`), without the two readers' answers. For each point, answer that one question
afresh by the rules above and return one JSON object per point, one per line, and nothing else:
`{"control": 3, "field": "item i005", "ruling": "yes"|"no"|"shown"|"not_shown", "why": "one sentence"}` (`yes`/`no` for the two
question fields, `shown`/`not_shown` for an item).

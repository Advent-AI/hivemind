# Blind reader, task K: is each topic's yardstick stated in the news, or did someone have to choose it? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/reflection-3/july-topics-as-opened.json`.
Open no other file: keys and other readers' answers exist and you must not see them. Do not edit files or run model calls.

The file holds 40 research topics a system opened while reading news about one company (NVIDIA). Each has the topic as it
was written (`description`: the question; `outcome`: what is tracked; `period`; `opens_as`; `settled_by`) and the date and title
of the article it was opened from. You do not see the articles or what was done with the topics later.

To judge a topic later, one needs a yardstick: **what exactly is measured or which event, and for which period or by which
day**. For each topic, say where its yardstick comes from, as far as the topic's own fields show:

- `stated`: the topic takes both from something fixed outside the writer's choice: a date or period the company, an authority
  or the report itself gives; a figure a company publishes for a fixed period (an annual report line, a calendar-year total);
  one named decision or one named product's shipment.
- `chosen`: the writer had to choose at least one of them, and another reasonable writer could have chosen otherwise. Name
  what was chosen, from this closed list (several allowed): `what_is_measured` (for example a price with no single published
  series; an average, a level or a direction), `period_or_deadline` (no stated date, a rolling window, a deadline set by a
  default), `which_part` (the topic holds two or more things, or several actors, and one must be picked), `whose_bucket`
  (it is unclear whether it is the company's matter or a wider theme's).

Also mark `parts`: 1 when the topic asks one thing, 2 or more when its question or its tracked outcome names several things
that could each be tracked.

Return, as your final message and nothing else, one JSON object per line, in the file's order:
`{"id": "t..", "yardstick": "stated|chosen", "chosen": [...], "parts": 1, "why": "<= 20 words"}`

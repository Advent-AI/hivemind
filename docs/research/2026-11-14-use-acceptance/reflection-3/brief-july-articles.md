# Blind reader, task A: is each topic's opening article news about it, and is the matter new? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/reflection-3/july-articles-packet.json`.
Open no other file: keys and other readers' answers exist and you must not see them. Do not edit files or run model calls.

A research system follows one company (NVIDIA). Starting from an empty library, it read two weeks of news (2026-07-01 to
2026-07-14) and opened the 40 topics in the packet (three independent passes over the same news, mixed). Each has the topic as
written (`description`: the question; `outcome`: what is tracked; `period`; `opens_as`; `settled_by`) and the whole article it
was opened from.

For each topic answer two things.

**1. `article`**: what is the opening article to this matter?
- `news`: the article reports a new development on this matter (an event, a decision, a deal, a newly published figure or
  report), and the matter is what the article, or a main part of it, is about;
- `background`: the article is about something else or is a general piece (a stock comparison, a recommendation, an overview),
  and mentions the matter as context that was already known.

**2. `matter_is`**: `standing` (the matter existed well before the article: a yearly figure, a product programme already
announced, a long-running proceeding, a deal already signed) or `new` (the article, or news within about two weeks before it,
is where the matter starts).

Return, as your final message and nothing else, one JSON object per line, 40 lines, in the packet's order:
`{"id": "j..", "article": "news|background", "matter_is": "standing|new", "why": "<= 25 words, quoting the article where it decides"}`

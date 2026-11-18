# Blind reader, task C: was each topic's matter already followed, and is its opening article news about it? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/reflection-3/coverage-packet.json`.
Open no other file: keys and other readers' answers exist and you must not see them. Do not edit files or run model calls.

A research system follows one company (NVIDIA) by keeping a library of questions and reading news against it. The packet holds:
- `library_1`: 69 questions a library held, built only from news of 2026-07-01 to 2026-08-28 (id `v..`, the day opened, whose
  question, the question, its due day);
- `library_2`: 7 topics another library held, built only from news of 2026-09-22 to 2026-09-28 (id `w..`);
- `topics`: 20 topics that were opened later, each time **starting from an empty library**, each with the topic as written
  (`description`: the question; `outcome`: what is tracked; `period`; `opens_as`; `settled_by`) and the whole article it was
  opened from. `compare_with` says which libraries are dated before the topic's article: compare the topic with those only.

For each topic answer three things.

**1. `coverage`**: did a library dated before the article already hold a question on this topic's matter?
- `same_question`: a prior question asks the same thing (the same figure or the same event, for the same year or stage), so
  the article's facts would simply have been filed under it;
- `same_matter`: a prior question is on the same underlying matter (the same deal, product, programme, figure series or
  proceeding) but asks another part, stage, year or shape of it;
- `none`: no prior question is on this matter (a question on a neighbouring matter, for example another chip or another deal,
  does not count).
List the prior ids in `prior` (empty for `none`).

**2. `article`**: what is the opening article to this matter?
- `news`: the article reports a new development on this matter (an event, a decision, a deal, a newly published figure or
  report), and the matter is what the article, or a main part of it, is about;
- `background`: the article is about something else or is a general piece (a stock comparison, a recommendation, an overview),
  and mentions the matter as context that was already known.

**3. `matter_is`**: `standing` (the matter existed well before the article: a yearly figure, a product programme already
announced, a long-running proceeding, a deal already signed) or `new` (the article, or news within about two weeks before it,
is where the matter starts).

Return, as your final message and nothing else, one JSON object per line, 20 lines, in the packet's order:
`{"id": "k..", "coverage": "same_question|same_matter|none", "prior": ["v..", "w.."], "article": "news|background", "matter_is": "standing|new", "why": "<= 25 words, quoting the article where it decides"}`

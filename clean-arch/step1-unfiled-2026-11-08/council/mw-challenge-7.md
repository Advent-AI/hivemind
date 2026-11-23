# Council mw, round 8: the lean path (Alex chose "小步快跑"); step 1's result and step 2's design

Alex asked for a leaner plan than `ACCEPTANCE-DESIGN.md`, then set the goal: "一步步tackle, 使用council skill 讨论复盘，执行，看数据然后推进，不要drift
from PRD and scope". The frame and step 1 are in `docs/research/2026-11-14-use-acceptance/LEAN-LOG.md` (§0, §1), with `date-census.txt` and
`source-date-census.txt`.

**Step 1 (check its reading):** the "statement dated after its article" class is not a model error: the stored item day is one day early for
those items (the `published_at` shows the later date), and two flagged statements quote a page that carries later text. Nothing is built.

**Step 2 (proposed, about $3.60, ceiling $8):** one week, 2026-09-22..28 (232 never-sent articles; three of the six articles earlier Step 1
test sets sent fall in it: both systems process the whole week as a product would, and readers' samples exclude those three, disclosed); both
systems one draw each from an empty library through the full run's own drivers (`clean-arch/e2e-comparison-2026-11-13/run_fresh.py`,
`budget_replay.py`, the shared ledger), parameterized for the window (today they fix 2026-07-01..07-14 and a 243-item manifest; the change is a
window argument and a manifest built from the frozen fresh list, proved by rebuilding the stored full run's manifest byte for byte). Readings,
two families, keys outside the repository: A on 40 sampled articles (big questions; covered = opened or a narrower question carrying the main
outcome; one-family matters reported), and each system's opened questions marked worth / trivia / duplicate; B on every last judgement by
09-28 against the request as sent, with planted wrong judgements on requests not otherwise in the packet and supported controls confirmed
first. Not done here: B2 against articles, C. What it decides: which system carries forward, if the difference is clear; otherwise what the
next small step measures. One draw each is labelled one draw.

Agree, or name what would make step 2's result wrong or unreadable. End with: "Council position: <...>".

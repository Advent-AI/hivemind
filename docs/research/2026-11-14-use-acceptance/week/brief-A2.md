# Blind reader, reading A2: which big matters did each system open, and is each opened question worth holding? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY these files of `docs/research/2026-11-14-use-acceptance/week/`: `matters-A2.json` (big matters
readers listed from 40 articles, 2026-09-22..09-28, with an example question and the article numbers), `libraries-A2.json` (every question two
systems, X and Y, opened over that week, each with the article it was opened from) and `opening-articles-A2.json` (the text of every article a
question was opened from); and the signed standard `docs/prd/05-extraction-standard.html` §3 (the opening reasons and how a question is
written) and §4 (the opening tests, and "同一题、续期，还是另一题"). Open no other file in that folder or anywhere else: keys and other readers'
answers exist and you must not see them. The two systems write their periods in different styles; ignore style.

**Part 1, per matter and system.** Choose one: **opened** (a question the same outcome would settle, any reasonable wording, period or date
the articles support; name its id), **narrower** (a question on part of the matter), **broader** (the matter is folded into a wider
question), or **missed** (no question on it). For narrower and broader, say whether that question's outcome would still tell an analyst the
matter's main outcome (`main_outcome`: true or false). Do not count a reasonable alternative shape as missed: a different deadline the
article itself states, or the total where the matter names its largest segment, is "opened", "narrower" or "broader" with a note.

**Part 2, per question of each system.** Read the question beside the article it was opened from and choose one: **worth** (a big matter
under §3 that passes §4's opening tests: its answer can change a position, and a date and public material can settle it), **trivia** (a
small matter, or one whose answer would not change a position, or one no dated public material can settle; say which), or **duplicate**
(§4: the same outcome settles it and another question of the same system, and their answers cannot move apart; name the other id; mark the
later-numbered question of the pair as the duplicate and judge the earlier one on its own).

Write one JSON object per line:
- part 1: {"part": 1, "matter": "M01", "system": "X|Y", "status": "opened|narrower|broader|missed", "main_outcome": true|false|null,
  "ids": ["X-3"], "note": "<= 30 words"}
- part 2: {"part": 2, "id": "X-3", "verdict": "worth|trivia|duplicate", "duplicate_of": "X-1"|null, "why": "<= 30 words"}

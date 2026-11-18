# Blind reader, reading A2: which of these big matters did each system open? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/matters-A2.json` (big matters readers listed from 40
articles, 2026-07-01..07-14, with an example question and the article numbers), `libraries-A2.json` (every question two systems, X and Y,
opened by 2026-07-14, with the article it was opened from, by the same numbering when it is one of the 40) and, for what counts as the same
question, `docs/prd/05-extraction-standard.html` §4 ("同一题、续期，还是另一题"). Open no other file in that folder or elsewhere. The two systems
write their periods in different styles; ignore style.

For each matter and each system, choose one: **opened** (a question the same outcome would settle, any reasonable wording, period or date the
articles support; name its id), **narrower** (a question on part of the matter), **broader** (the matter is folded into a wider question), or
**missed** (no question on it). Note when the system's question was opened from an article outside the 40. Do not count a reasonable
alternative shape as missed: a different deadline the article itself states, or one year of a two-year matter, is "opened" or "narrower" with
a note.

Write one JSON object per line: {"matter": "M01", "system": "X|Y", "status": "opened|narrower|broader|missed", "ids": ["X-3"], "note": "<= 30
words"}

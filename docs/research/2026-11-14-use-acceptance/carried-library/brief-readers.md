# Blind reader: two reads of the same article by a research system (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/carried-library/reader-packet.json`.
Open no other file: keys and other readers' answers exist and you must not see them. Do not edit files or run model calls.

A research system follows one company (NVIDIA). It keeps a library of research questions. Reading an article, it keeps the
statements that matter, files each under a question it holds (or under a question it opens from this article, or nowhere),
and opens a new question only for a big matter it does not already follow: one that can change the company's revenue,
profit, cash or credit risk, which an analyst covering the company would hold a view on.

The packet holds 11 articles. Each was read twice by the same system, independently (reads A and B). Each read shows the
library it was shown before the article (`library_shown`: possibly empty), the questions it opened (`opened`) and every
statement it kept with where it filed it (`filed_under`: `library <id>` = a question of the library shown; `opened here: X` =
a question this read opened; `nowhere`). Read each article whole first.

Answer, for every article and both reads:

1. For each opened question (`ref` like `A-T1`): `in_library`: does the library this read was shown already hold a question on
   the same matter? `same_question` (the same thing asked for the same period or stage), `same_matter` (the same deal,
   product, programme, figure series or proceeding, asked in another shape), or `none`. And `worth`: is it a question worth
   holding (yes / no / unsure)?
2. For each statement filed under a question of the library shown (`filed_under` starts with `library`): `home`: is that
   question the right one for it? `right` (it bears on that question's answer), `wrong` (it does not, or another held
   question is clearly its home), `unsure`.
3. `missing`: matters in the article that deserve their own question and that this read neither opened nor already held in
   the library it was shown; a short name each, or none.

Return, as your final message and nothing else, JSON lines:
- per opened question: `{"ref": "<article>:<A-T1>", "in_library": "...", "worth": "...", "why": "<= 20 words"}`
- per statement filed under the library: `{"ref": "<article>:<A-S3>", "home": "...", "why": "<= 20 words"}`
- per read: `{"ref": "<article>:<A>", "missing": ["...", ...], "why": "<= 25 words"}`
where `<article>` is the article number in the packet.

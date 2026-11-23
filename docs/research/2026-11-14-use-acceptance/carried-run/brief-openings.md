# Blind reader, reading 1: what a research system did with each article, given the questions it already held (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/carried-run/packet-openings.json`.
Open no other file: keys and other readers' answers exist and you must not see them. Do not edit files or run model calls.

A research system follows one company (NVIDIA) by keeping a library of research questions. Reading an article, it keeps the
statements that matter, files each under a held question it bears on (or under a question it opens from this article, or
nowhere), and opens a new question only for a big matter it does not already follow: one that can change the company's
revenue, profit, cash or credit risk, which an analyst covering the company would hold a view on.

`questions` holds every question the library held at some point (id, the question, what it tracks, its period). Each entry of
`articles` is one article (read it whole) with: `library_held` (the ids of the questions held just before this article),
`opened` (the questions this article opened), and `statements` (every statement kept, with `filed_under`: question ids, or
`nowhere`).

For every article answer:
1. For each opened question (`ref` like `T1`): `in_library`: did the library held already hold a question on the same matter?
   `same_question` (the same thing for the same period or stage), `same_matter` (the same deal, product, programme, figure
   series or proceeding, in another shape), `none`, or `cannot_tell`; and `worth`: is it a question worth holding (yes / no /
   cannot_tell)?
2. `lost_questions`: matters in the article that deserve their own question and that are neither held nor opened (a short
   name each, or none).
3. `lost_facts`: statements filed `nowhere` (their `ref`) that bear on a held question, with that question's id, or none.
4. `wrong_homes`: statements filed under a held question that do not bear on it (their `ref`), or none.

Return, as your final message and nothing else, JSON lines:
- per opened question: `{"ref": "<article>:<T1>", "in_library": "...", "worth": "...", "why": "<= 20 words"}`
- per article: `{"ref": "<article>", "lost_questions": [...], "lost_facts": [{"ref": "S3", "question": "clean-2"}], "wrong_homes": ["S5"], "why": "<= 30 words"}`

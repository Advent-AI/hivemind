# Blind reader: would this further statement bear on the judgement? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/delivery-class/class-settle-v2-1.json`.
Open no other file in that folder or anywhere else, and use nothing you know from elsewhere.

The packet holds one research `question` (what it asks, what settles it, its possible answers), `what_the_judge_was_shown` (the whole
text a judge received when it last judged the question: the question, its possible answers and every piece of evidence under it),
the `articles` the items came from (number, date, publisher, title, text) and 15 `items`: statements a system stored from the
same week's news (its article, who said it, a one-line summary and the quote) that the judge was NOT shown under this question. A
statement may hold several facts: judge the one fact in it that bears most on this question, and name it.

Think as a hedge-fund analyst. Read all of what the judge was shown first. Then for each item decide:
- `fact`: at most 15 words naming the one fact in the statement you are judging;
- `in_article`: yes when the article states that fact with the source, the period and the qualification the summary gives it; no
  when the article says something else (say what);
- `already_shown`: yes when what the judge was shown already states this same fact (the same event, or the same figure for the same
  thing and period), in any wording, including the same underlying claim repeated by another outlet; no when the judge has no
  statement of it, or when this is a different source's own figure or a detail the judge lacks;
- `bears`: yes when, added to what the judge was shown, this fact can change the question's answer or how likely an answer is: it
  is the question's own event or figure, or a fact an analyst would reason onward from to the answer. No when it is background that
  would leave the judgement where it is. Say which answer it makes more or less likely and why, or why it does not bear. A
  judgement already on one answer can still become more or less likely to hold.
Judge `already_shown` and `bears` separately: a fact can be not shown and still not bear.

Write one JSON object per line and nothing else, with no code fence, one line per item (15 lines):
{"item": "v2:e000", "fact": "...", "in_article": "yes", "already_shown": "no", "bears": "yes", "why": "<= 30 words>"}

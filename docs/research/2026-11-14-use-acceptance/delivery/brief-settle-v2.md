# Blind reader: would this further figure bear on the judgement? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/delivery/settle-packet-v2.json`. Open no other
file in that folder or anywhere else, and use nothing you know from elsewhere.

The packet holds one research `question` (what it asks, what settles it, its possible answers), `what_the_judge_was_shown` (the whole
text a judge received when it last judged the question: the question, its possible answers and every piece of evidence under it),
some `articles` (number, date, publisher, title, text) and `items`: figures a system stored from those articles (with the stored
measure, value, period, kind, basis and source, and the passage it quoted) that the judge was NOT shown.

Think as a hedge-fund analyst. For each item decide:
- `in_article`: yes when the article states this figure with the stored source and period (or gives no period, as stored); no
  otherwise (say what the article says instead);
- `already_shown`: yes when what the judge was shown already states this same figure (the same value for the same thing, from the
  same source), in any wording; no otherwise;
- `bears`: yes when, added to what the judge was shown, this figure can change the question's answer or how likely an answer is: it
  is the question's own figure, or one an analyst would reason onward from to the answer (a component of the amount asked for; the
  price to go with a volume the judge already has; an assumption the question turns on). No when it is background that would leave
  the judgement where it is, or only repeats what the judge already has. Say which answer it makes more or less likely and why, or
  why it does not bear.

Write one JSON object per line and nothing else, with no code fence, one line per item:
{"item": "v2:T-000", "in_article": "yes", "already_shown": "no", "bears": "yes", "why": "<= 35 words>"}

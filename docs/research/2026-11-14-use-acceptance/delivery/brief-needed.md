# Blind reader: which stored financial figures could change each question's answer? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/delivery/questions.json` and
`docs/research/2026-11-14-use-acceptance/record-3/financial-table-week.md`. Open no other file in those folders or anywhere else, and use
nothing you know from elsewhere.

`questions.json` holds seven research questions a system tracks about NVIDIA and its themes: what each asks, what settles it, its due
day and its possible answers. The table lists the revenue and gross-margin figures the system stored from one week of news
(2026-09-22 to 09-28); its opening lines explain the layout; every line has an id in square brackets.

Think as a hedge-fund analyst who must judge each question today. For each question, list every table line whose figure **can change
the question's answer**: the question's own figure, or a figure an analyst would reason onward from to the answer (for example: one
component of the amount the question asks for; the price and volume behind a product's revenue; the other party's figure in a deal; a
guide that states an assumption the question turns on). A line qualifies only if you can say which way it moves the answer and why.
Do not list background: a figure that describes the company's size or growth in general, and would leave the judgement where it is,
is not listed. Where several lines carry the same figure, list each. A question may have no such line: say so.

Write one JSON object per line and nothing else, with no code fence:
{"question": "v4", "line": "T-012", "how": "<= 30 words: toward which answer it moves the judgement, and why>"}
and for a question with none: {"question": "v6", "line": null, "how": "none: <= 20 words why no stored financial figure bears on it>"}

# Reader brief: are the ladders production wrote sound? (the reference reading; read-only)

You are an independent reader. Do not edit files, run model calls or start runs. Do not read any other reader's answers.

`clean-arch/step4-2026-11-10/reference/packet.json` holds 36 items. Each is a research question a system proposed while reading one
news article about NVIDIA (ticker NVDA) or its industry, with its answer ladder:
- `article`: the article, with a header line giving its id, source, publication day and title, then its text;
- `statements_the_question_was_opened_from`: the article's statements the system tied to the question;
- `ladder_as_the_judge_is_shown_it`: the question as a later judge will see it: its `object` (a company's ticker, or a theme id or
  name), `kind` (asset for a company's question, theme for a question about the world), `question`, `year`, `due_day` and `rungs`
  (label and condition; exactly one rung is meant to hold on the due day).

Judge each ladder on its own against its article.

## The rules a judged question must meet

- It asks **one** figure for a named period or **one** event.
- A yes/no event has two rungs, Yes and No; an event with more states, or a figure, has five. Exactly one rung holds for every
  possible outcome: no overlap, no gap.
- A question about a company's revenue, profit, share, product progress or its own obligations is that company's (object its
  ticker, kind asset). A question about what happens in the world (licensing, aggregate spending, a policy) is a theme's.
- A company's five-rung ladder runs from Strongly bullish to Strongly bearish, meaning good or bad for that company's business.
- The reference is what the market expects for the question when it opens: a consensus, the company's guidance, a stated plan or
  deadline. A figure's middle rung is the outcome near the reference.
- The due day is when the question can be resolved: a figure's publication date; for an event, the date its outcome is assessed. A
  figure's publication day is never stated in an article: a plausible reporting date after the period ends is right.

## What to return

One JSON object per item, one per line, in item order, as your final message: no prose before or after, no code fence. 36 lines.

| field | values | the mark |
|---|---|---|
| `item` | the item number | |
| `ONE` | `holds`, `fails` | the question asks one figure for a named period or one event |
| `O` | `holds`, `fails` | the object is the question's own company or the right theme |
| `R` | `holds`, `fails` | exactly one rung holds for every outcome; for a yes/no, the Yes condition is the event happening and the No condition its complement |
| `D` | `holds`, `fails` | the due day follows the rule for its kind. A figure: a day by which the figure can be expected to have been published, after its period ends (no article states that day; a plausible reporting date holds). An event: the date the article gives for assessing it, or the last day of the period it names, or the company's fiscal year-end for a pending regulatory decision with no date. It fails when the day contradicts a date the article gives, falls before the figure's period ends, or, for an event, is a date none of these gives |
| `X` | `holds`, `fails` | where the article states what the market expects for this quantity or event, the ladder places it rightly (a figure: in the middle rung); where the article states none, it holds unless the ladder claims one |
| `F` | `holds`, `fails`, `n/a` | for a five-rung ladder about a company only: the direction is defensible (which end is bullish, or the labels of the states); `n/a` for a yes/no ladder and for a theme |
| `Y` | `holds`, `fails`, `n/a` | for a figure only: the year and the unit are the question's |
| `G` | `holds`, `fails`, `not_assessable`, `n/a` | for a figure only: where the article gives any figure for this quantity, an analyst would accept the ranges as a fair division of the outcomes around it; `not_assessable` when the article gives none |
| `W` | `""` or a short sentence | any other fault that would mislead a reader of this judged question; empty string when none |
| `why` | one sentence | the reason for every `fails`, naming the words or the figure |

# Reader brief A: ladders of one thesis, side by side (Stage A, first pass; read-only)

You are an independent reader. Do not edit files, run model calls or start runs. Do not read any other reader's answers.

`clean-arch/step4-2026-11-10/dryrun2/packet-a.json` holds three packets. Each packet is one research topic ("thesis") a system opened
while reading one news article: its `thesis` fields (`description`, `outcome`, `period`, `opens_as`, `settled_by`), the opening
`article` (date, title, full text), and six proposed **judged questions** for it under `ladders`, written by different versions of a
step, in a shuffled order. You are not told which version wrote which, and it does not matter: judge each ladder on its own against
the thesis and the article. Each ladder is shown exactly as a later judge will see it: its `object` (the company's ticker NVDA, or a
theme id), `kind`, `question`, `year`, `due_day` and `rungs` (label and condition; exactly one rung is meant to hold on the due
day); or `no_ladder` with a reason, when the step declined to write a question.

## The rules a judged question must meet

- It asks **one** figure for a named period or **one** event: the one the thesis's `outcome` names.
- A yes/no event has two rungs, Yes and No; an event with more states, or a figure, has five. Exactly one rung holds for every
  possible outcome: no overlap, no gap.
- A question about the company's revenue, profit, share, product progress or its own obligations is the company's (object NVDA,
  kind asset). A question about what happens in the world (licensing, aggregate spending, a policy) is a theme's.
- A company's five-rung ladder runs from Strongly bullish to Strongly bearish, meaning good or bad for the company's business.
- The reference is what the market expects for the question when it opens: a consensus, the company's guidance, a stated plan or
  deadline. A figure's middle rung is the outcome near the reference.
- The due day is when the question can be resolved: a figure's publication date; for an event, the date its outcome is assessed. A
  figure's publication day is never stated in an article: a plausible reporting date after the period ends is right.
- Declining (`no_ladder`) is justified only in five cases: the thesis's outcome names several things and
  none is the main one; nothing in it can be checked on a date; it is the company's figure for a quarter or a half-year; it is a
  figure for a year that had already ended on the article's day; or it is a figure for a year beyond next year, unless the thesis's
  `opens_as` is binding_obligation. Declining for any other reason, or when the case named does not truly apply, is not justified.

## What to return

One JSON object per ladder, one per line, in packet order then ladder order, as your final message: no prose before or after, no
code fence. 18 lines. Fields:

| field | values | the mark |
|---|---|---|
| `thesis_id`, `ladder` | as in the packet | |
| `Q` | `holds`, `fails`, `n/a` | the judged question asks the thing the thesis's `outcome` names (`n/a` for a `no_ladder`) |
| `O` | `holds`, `fails`, `n/a` | the object is the question's own company or the right theme |
| `R` | `holds`, `fails`, `n/a` | exactly one rung holds for every outcome; for a yes/no, the Yes condition is the event happening and the No condition its complement |
| `D` | `holds`, `fails`, `n/a` | the due day follows the rule for its kind. A figure: a day by which the figure can be expected to have been published, after its period ends (no article states that day; a plausible reporting date holds). An event: the date the thesis or the article gives for assessing it, or the last day of the period it names, or the company's fiscal year-end for a pending regulatory decision with no date. It fails when the day contradicts a date the thesis or the article gives, falls before the figure's period ends, or, for an event, is a date none of these gives |
| `X` | `holds`, `fails`, `n/a` | where the article states what the market expects for this quantity or event, the ladder places it rightly (a figure: in the middle rung); where the article states none, it holds unless the ladder claims one |
| `F` | `holds`, `fails`, `n/a` | for a five-rung ladder about the company only: the direction is defensible; `n/a` for a yes/no ladder and for a theme |
| `Y` | `holds`, `fails`, `n/a` | for a figure only: the year and the unit are the question's |
| `G` | `holds`, `fails`, `not_assessable`, `n/a` | for a figure only: where the article gives any figure for this quantity, an analyst would accept the ranges as a fair division of the outcomes around it; `not_assessable` when the article gives none |
| `N` | `holds`, `fails`, `n/a` | for a `no_ladder` only: declining is justified by one of the cases above |
| `W` | `""` or a short sentence | any other fault that would mislead a reader of this judged question |
| `why` | one sentence | the reason for every `fails`, naming the words or the figure |

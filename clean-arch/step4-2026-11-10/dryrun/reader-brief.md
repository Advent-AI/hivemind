# Reader brief: is each ladder a sound judged question for its thesis? (Stage A reading form; read-only)

You are an independent reader. Do not edit files, run model calls or start runs. Do not read any other reader's answers.

## What you are reading

`clean-arch/step4-2026-11-10/dryrun/packet.json` holds a list of items. Each item is one research topic ("thesis") a system opened
while reading one news article, with a proposed **judged question** for it:
- `thesis`: the fields the system wrote when it opened the topic: `description` (the topic's wording), `outcome` (what is tracked),
  `period`, `opens_as`, `settled_by`;
- `article`: the opening article's publication date, title and full text;
- `ladder_as_the_judge_is_shown_it`: the proposed judged question exactly as a later judge will see it: its `object` (the company's
  ticker NVDA, or a theme id), `kind`, `question`, `year`, `due_day` and its `rungs` (each a label and a condition; exactly one rung
  is meant to hold on the due day). Or `no_ladder` with a reason: the step declined to write a question;
- `other_fields`: what the step recorded beside the ladder and the judge does not see: `not_judged` (parts of the topic's wording
  the question leaves out, with why), `reference` (what the article says the market expects, quoted), `favourable_end`,
  `due_day_basis`.

Some items are sound and some carry a fault. Judge each on its own against its thesis and its article.

## The rules a judged question must meet

- One judged question asks **one** figure for a named period or **one** event: the one the thesis's `outcome` names. Every other
  figure or event the thesis's wording asks about must be listed in `not_judged`.
- A yes/no event has two rungs, Yes and No; an event with more states, or a figure, has five. Exactly one rung holds for every
  possible outcome: no overlap, no gap.
- A question about the company's revenue, profit, share, product progress or its own obligations is the company's (object NVDA,
  kind asset). A question about what happens in the world (licensing, aggregate spending, a policy) is a theme's.
- A company's five-rung ladder runs from Strongly bullish to Strongly bearish, meaning good or bad for the company's business.
- The reference is what the market expects for the question when it opens: a consensus, the company's guidance, a stated plan or
  deadline. A figure's middle rung is the outcome near the reference.
- The due day is when the question can be resolved: a figure's publication date; for an event, the date its outcome is assessed. A
  figure's publication day is never stated in an article: a plausible reporting date after the period ends is right.
- A step may decline (`no_ladder`) only when: the thesis's outcome names several things and none is the main one; nothing in it can
  be checked on a date; it is a company's quarterly or half-year figure; or a figure for a year beyond next year.

## What to return

One JSON object per item, one per line, in item order, as your final message: no prose before or after, no code fence. Fields:

| field | values | the mark |
|---|---|---|
| `item` | the item number | |
| `Q` | `holds`, `fails`, `n/a` | the judged question asks the thing the thesis's `outcome` names (`n/a` for a `no_ladder`) |
| `O` | `holds`, `fails`, `n/a` | the object is the question's own company or the right theme |
| `R` | `holds`, `fails`, `n/a` | exactly one rung holds for every outcome; for a yes/no, the Yes condition is the event happening and the No condition its complement |
| `D` | `holds`, `fails`, `n/a` | the due day follows the rule for its kind. A figure: a day by which the figure can be expected to have been published, after its period ends (no article states that day; a plausible reporting date holds). An event: the date the thesis or the article gives for assessing it, or the last day of the period it names, or the company's fiscal year-end for a pending regulatory decision with no date. It fails when the day contradicts a date the thesis or the article gives, falls before the figure's period ends, or, for an event, is a date none of these gives |
| `X` | `holds`, `fails`, `n/a` | where the article states what the market expects for this quantity or event, the ladder places it rightly (a figure: in the middle rung); where the article states none, it holds unless the ladder claims one |
| `F` | `holds`, `fails`, `n/a` | for a five-rung ladder about the company only: the direction is defensible (which end is bullish, or the labels of the states); `n/a` for a yes/no ladder and for a theme |
| `Y` | `holds`, `fails`, `n/a` | for a figure only: the year and the unit are the question's |
| `G` | `holds`, `fails`, `not_assessable`, `n/a` | for a figure only: where the article gives any figure for this quantity, an analyst would accept the ranges as a fair division of the outcomes around it; `not_assessable` when the article gives none |
| `L` | `holds`, `fails`, `n/a` | every other figure or event the thesis's wording asks about is listed in `not_judged` |
| `XR` | `holds`, `fails`, `n/a` | the `reference` field quotes what the article states the market expects, with the right number, and is null only when the article states none |
| `N` | `holds`, `fails`, `n/a` | for a `no_ladder` only: the refusal is justified by one of the allowed cases |
| `W` | `""` or a short sentence | any other fault that would mislead a reader of this judged question; empty when none |
| `why` | one sentence | the reason for every `fails`, naming the words or the figure |

Read each item's article before answering it. Judge only what is in the item.

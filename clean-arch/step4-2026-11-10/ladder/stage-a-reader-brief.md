# Stage A reading form: is each answer a sound judged question for its thesis, or a justified refusal? (read-only)

You are an independent reader. Do not edit files, run model calls or start runs. Do not read any other reader's answers.

## What you are reading

The packet you are given holds a list of items. Each item is one research topic ("thesis") a system opened
while reading one news article, with a proposed **judged question** for it:
- `thesis`: the fields the system wrote when it opened the topic: `description` (the topic's wording), `outcome` (what is tracked),
  `period`, `opens_as`, `settled_by`;
- `article`: the opening article's publication date, title and full text;
- `fiscal_year_note`: how the company names its fiscal years and which is this year and which next year on the article's day,
  the same note the step was given. Use it wherever a mark turns on a year;
- `ladder_as_the_judge_is_shown_it`: the proposed judged question exactly as a later judge will see it: its `object` (the company's
  ticker NVDA, or a theme id), `kind`, its `focus` (the line the judge is shown beside the question: the thesis's `outcome`),
  `question`, `year`, `due_day` and its `rungs` (each a label and a condition; exactly one rung
  is meant to hold on the due day). An event's rungs are `Yes`, then `Ruled out` when the step named something that can rule
  the event out, then a last rung that code writes as the complement of the others (`Still open`, or `No` when there are
  two rungs). In the `Ruled out` rung the step wrote the first sentence; the sentence after it is code's ("This rung
  holds when that, or any other decision against the event of rung 1 as a whole taken after <the article's day>, or a formal
  abandonment or withdrawal of it as a whole after that day, stands on <due day>, and only when rung 1 does not"), so that a
  rejection the step did not name is still `Ruled out`, and one that was lifted, that concerns only a part of the event, or
  that was already in place when the article appeared, is not. Or `no_ladder` with a reason: the step
  declined to write a question;
- `other_fields`: what the step recorded beside the ladder and the judge does not see: `not_judged` (parts of the topic's wording
  the question leaves out, with why), `reference` (what the question is measured against, quoted from the article: its `kind` is `expected` for what
  the article says the market expects, or `last_reported` for the amount most recently reported for a figure when the article
  states no expectation; its number when the article states one, with `value_to` as the upper end when the article states a
  range; when it has a number, the judge also sees the quoted passage, inside the middle rung's condition, introduced as "the
  reference" or as "the amount last reported"), `favourable_end` and
  `favourable_why` (for a company's figure: which end is good for the business, and the reason given), `ruled_out_by` (for
  an event with a `Ruled out` rung: who the step names as the one whose decision would rule the event out; the first sentence
  of that rung is the decision it names for them), `due_day_basis`.

Some items are sound and some carry a fault. Judge each on its own against its thesis and its article.

## The rules a judged question must meet

- One judged question asks **one** figure for a named period or **one** event: the one the thesis's `outcome` names. Every other
  part of the thesis's wording that the question leaves out (a second figure or event, a condition, a comparison) must be listed
  in `not_judged`.
- An event has at most three outcomes: it has happened by the due day; it is ruled out by the due day though it has not happened
  (decided against, or formally abandoned or withdrawn); neither. The step writes the first condition and, when something can
  rule the event out, the way it names for that; the rest is code's, so every outcome has exactly one rung. An event that has
  happened by the due day is `Yes` even if it is undone afterwards, unless the question asks whether it still stands. What
  rules an event out is a decision by someone (the company, an authority, a court, a party): the due day arriving without the
  event, or a decision to go on waiting, is no ruling out, and the step names who decides in `ruled_out_by` (D416). A proceeding
  an authority conducts, where the question asks for its published decision or conclusion, always has a ruling out: a published
  closing decision, with or without a penalty, is `Yes`; the authority formally abandoning or withdrawing the proceeding without
  that decision or conclusion is `Ruled out`; the proceeding still going on the due day is the last rung (D420). A
  difference inside an outcome (an approval with conditions against one without) is not a rung; when the thesis's wording names
  it, it belongs in `not_judged`. A figure has five ranges,
  and exactly one holds for every value: no overlap, no gap.
- A question about the company's revenue, profit, share, product progress or its own obligations is the company's (object NVDA,
  kind asset). A question about what happens in the world (licensing, aggregate spending, a policy) is a theme's. A question
  whose tracked outcome is a government's or regulator's decision to permit, restrict or ban a class of products or trade is the
  theme's that covers it, also when the product is the company's own; when the tracked outcome is the company's own sales,
  shipments or revenue under such a decision, or a proceeding against the company itself (an investigation of its conduct, a
  fine), the question is the company's (D418).
- A company's figure runs from Strongly bullish to Strongly bearish, meaning good or bad for the company's business. An event's
  rungs carry no such labels.
- The reference is what the question is measured against when it opens. Its kind is `expected` for what the market expects: a
  consensus, the company's guidance, a stated plan or deadline. For a figure, where the article states no expectation and gives
  the amount most recently reported for the same quantity, that amount is the reference and its kind is `last_reported`; a
  reported amount is never called an expectation (D411). When the article states a number, the field carries it and a
  figure's middle rung holds it; a stated range is carried by its two ends, and the middle rung runs from at or below its lower end to at or above its upper end. When the
  article states it in words alone, the field carries the words and no number, and the ranges are the step's own estimate.
- The due day is when the question can be resolved: a figure's publication date; for an event, the date its outcome is assessed. Where
  the thesis or the article states the day a figure is published, that day is right. Where neither does (`due_day_basis` is
  `expected_publication`), code sets the day and the step's own estimate is not shown: 60 days after the company's fiscal
  year-end for a company's figure, 90 days after the calendar year-end for a theme's (D414). That day is right when the figure
  is a figure for that year; it is wrong when the figure the question asks for is not a year's figure (a quarter, a survey's
  rolling twelve months), which is then a fault of the question's period and of the due day both.
- A company's figure for a quarter or a half-year is never a judged question: the step must decline it. A ladder written for
  one is wrong even when it asks exactly what the thesis names (mark `Y`). An annual figure that only names quarterly reports as
  the material that settles it is not such a case.
- A step may decline (`no_ladder`) only in the seven cases its instructions allow: the thesis has no main figure or event (its
  outcome names none, or several things and none is the main one); nothing in it can be checked on a date (for an event:
  neither the thesis nor the article gives a date, and the thesis names no period, unless it is a pending regulatory decision,
  which is due at the company's fiscal year-end); it is the company's figure for a
  quarter or a half-year; it is a figure for a period that is not one fiscal or calendar year, such as a survey's rolling twelve
  months, and neither the thesis nor the article gives the day it is published (D417); it is a figure for a year that had already
  ended on the article's day; it is a figure for a year beyond
  next year, unless the thesis's `opens_as` is binding_obligation; or the question belongs to another company, or to a matter that
  none of the listed themes covers (the listed themes are given with the packet). Declining for any other reason, or when the case
  named does not truly apply, is not justified.

## What to return

One JSON object per item, one per line, in item order, as your final message: no prose before or after, no code fence. Fields:

| field | values | the mark |
|---|---|---|
| `item` | the item number | |
| `Q` | `holds`, `fails`, `n/a` | the judged question is worded as a question, not as an assertion, and asks the thing the thesis's `outcome` names. For a figure it also names the period the figure covers, or the day it is measured at, and the material that settles it. And it does not ask something other than its `focus` line (a focus that also names parts listed in `not_judged` is expected and is not a conflict). It can be understood by a reader who never sees the article: it never says "this item" or leans on a figure or a name it does not give. A group named as the trade names it ("the big four AI hyperscalers", "the top five hyperscalers") is a name the question gives: a question is not failed for not listing the group's members. `n/a` for a `no_ladder` |
| `O` | `holds`, `fails`, `n/a` | the object is the question's own company or the right theme, by the rule above: a tracked government decision on a class of products is the theme's; the company's own sales under it, and a proceeding against the company, are the company's |
| `R` | `holds`, `fails`, `n/a` | exactly one rung holds for every outcome. For a figure: the ranges meet end to end. For an event, where code writes the last rung: the `Yes` condition is the event the question asks about; the first sentence of the `Ruled out` condition, when there is one, is a decision against that event as a whole, or its abandonment or withdrawal as a whole, taken after the article's day and standing on the due day, and not the event's merely being still awaited, the refusal of one part of it, or a bar already in place when the article appeared (it need not list every way: code's sentence takes the others); and where the event can plainly be ruled out before the due day (a formal refusal, a block, an announced abandonment; for an authority's proceeding, its formal abandonment or withdrawal without the asked-for decision or conclusion) and the answer has no `Ruled out` rung, the mark fails; it fails too when `ruled_out_by` names no one who decides, or when the decision named is the day arriving, the event not having happened, or a decision to go on with a proceeding. Every condition is concrete and can be checked on the due day: none rests on a target or a threshold that is not yet set |
| `D` | `holds`, `fails`, `n/a` | the due day follows the rule for its kind. A figure: the day the thesis or the article states, or, where neither states one, the day code sets from the year the figure covers (60 days after the company's fiscal year-end; 90 days after the calendar year-end for a theme's figure), which holds when the figure asked for is that year's figure. An event: the date the thesis or the article gives for assessing it, or the last day of the period it names, or the company's fiscal year-end for a pending regulatory decision with no date. It fails when the day contradicts a date the thesis or the article gives, falls before the figure's period ends, or, for an event, is a date none of these gives And `due_day_basis` says truly where the day comes from: `stated` only when the thesis or the article gives that day; `period_end` only when it is the last day of the period the thesis names, or the fiscal year-end for a pending regulatory decision; `expected_publication` when the step set the day it expects the figure to be published. For a thesis whose `opens_as` is binding_obligation: an obligation already taken on is due at its next annual filing, and one not yet signed on the day by which the signing can be checked; another day fails |
| `X` | `holds`, `fails`, `n/a` | a figure: a number the `reference` carries lies in the middle rung, as the judge will read it (for a stated range: the middle rung runs from at or below its lower end to at or above its upper end); a reference with no number, or none, has nothing to place and holds, unless the ladder presents as expected something the article does not state. An event: the ladder presents as expected only what the article states |
| `F` | `holds`, `fails`, `n/a` | for a company's figure only: the direction is defensible (which end is bullish), and the reason given in `favourable_why` supports the favourable end. For an amount the company owes, guarantees or has committed to pay, where neither the thesis nor the article settles which end is good for the business (they argue both ends or say nothing on it), the lower end is the favourable one (D413), and "higher" fails unless the thesis's own words say that more of it is good. `n/a` for an event and for a theme |
| `Y` | `holds`, `fails`, `n/a` | for a figure only: the year, the unit and the scale of the numbers are the question's (an amount in full; a percentage as 31, not 0.31), and the figure is a whole year's. A company's figure for a quarter or a half-year fails, whatever the thesis asks |
| `G` | `holds`, `fails`, `not_assessable`, `n/a` | for a figure, always one of the first three: where the article gives any figure for this quantity, `holds` when an analyst would accept the ranges as a fair division of the outcomes around it and `fails` when not; `not_assessable` when the article gives none. `n/a` only for an event's ladder and for a `no_ladder` |
| `L` | `holds`, `fails`, `n/a` | every other part of the thesis's wording that the question leaves out (a second figure or event, a condition, a comparison) is listed in `not_judged`, each with a reason that says why it is left out; a wording that asks nothing else holds with an empty list |
| `B` | a list | exactly one entry for each part listed in `not_judged`, in its order: `"bet"` when an analyst would hold a separate view on it, `"not_a_bet"` when it is a detail of the judged question; `[]` when nothing is listed and for a `no_ladder` |
| `XR` | `holds`, `fails`, `n/a` | the `reference` field quotes what the article states the market expects, with `kind` `expected`, or, for a figure where the article states no expectation, the amount most recently reported for the same quantity (the same thing measured the same way: not a part of it, a ceiling on it or another quantity), with `kind` `last_reported`; the kind says truly which. It carries the number when the article states one (a range by its two ends), and no number the article does not state. It is null only when the article states no expectation and, for a figure, no amount last reported for the same quantity either; an event's is null whenever the article states no expectation |
| `N` | `holds`, `fails`, `n/a` | for a `no_ladder` only: the refusal is justified by one of the allowed cases, and that case truly applies. A refusal because the question belongs to another company or to a matter no listed theme covers names that company or matter. Which year is this year and which next year is read from the `fiscal_year_note` |
| `W` | a string | any other fault that would mislead a reader of this judged question, in a short sentence; the empty string `""` when there is none. The field is always present |
| `why` | a string | one sentence giving the reason for every `fails` and for a non-empty `W`, naming the words or the figure; it may be empty only when no mark fails and `W` is empty |

Read each item's article before answering it. Judge only what is in the item.

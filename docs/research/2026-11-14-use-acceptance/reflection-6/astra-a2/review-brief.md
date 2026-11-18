# A source-backed product review (read-only)

Each item in the packet holds:
- **`thesis`:** a research topic an analyst system opened on NVIDIA: `description` (the question asked), `outcome` (what is tracked),
  `period`, `opens_as` (its kind) and `settled_by`;
- **`article`:** the article the topic came from;
- **`fiscal_year_note`:** NVIDIA's fiscal calendar;
- **`ladder_as_the_judge_is_shown_it`:** what a step wrote and the product stores. It is either one judged question with its answer
  choices (`rungs`) and the stored `due_day`, the day the judge records the answer on (code sets it for a year's figure), or
  `{"no_ladder": <the reason>}` when the step declined;
- **`other_fields`:** the parts the question leaves out (`not_judged`), the reference quoted from the article, and the basis of the
  due day.

The listed themes are: chip-export-controls, ai-capex, custom-silicon, semiconductor-cycle, fed-policy-rate, us-inflation,
us-recession-risk, us-china-tariffs, taiwan-strait, middle-east-conflict, russia-ukraine-war, supply-chain-shift.

**The step's own rule for declining,** quoted from its instructions:

> - Return no_ladder with the reason, and ladder null, in seven cases: the topic has no main figure or event, naming none, or naming several with none of them the main one; nothing in the topic can be checked on a date, which for an event means that neither the topic nor the item gives a date and the topic names no period, unless it is a pending regulatory decision, for which use the company's current fiscal year-end; the figure is a company's figure for a quarter or a half-year, which is evidence to a yearly question; the figure covers a period that is not one fiscal or calendar year, such as a survey's rolling twelve months, and neither the topic nor the item gives the day it is published; the figure is for a year that has already ended on the item's day; the figure is for a year beyond next year, unless the topic's opens_as is binding_obligation; or the question belongs to another company or to a matter that no theme in the request's themes covers, in which case name that company or matter in the reason. Do not rewrite a figure for a year beyond next year as an event to keep it; a numeric completion target may define the state of an event that is itself the topic.

**The rule for the due day:**
- an event's day is the date the topic or the article gives for assessing it, or the last day of the period the topic names (the
  company's fiscal year-end for a pending regulatory decision with no date);
- a figure's day falls after the period it covers, when the figure is published.

**For each item, judge it against the topic and the article:**
1. **A written question:**
   - **period:** does it keep the topic's period or check date?
   - **measure:** is the thing measured the one the topic tracks, and is any constructed measure supported by the topic or the
     article?
   - **conditions:** are they kept or listed as not judged?
   - **choices:** can the judge apply them on the due day (no overlap, no gap, right unit and scale)?
   - **record day:** is the stored due day the right day for what the topic tracks?
2. **A decline:** is its reason one of the cases above, truly applying to this topic? If not, it is an `unjustified_decline`,
   material.

**Return one JSON line per item, in item order:**
- `item`;
- `verdict`: `"sound"` or `"defect"`;
- `class`: `null`, or one of `unjustified_decline`, `period_changed`, `measure_invented`, `measure_changed`, `condition_lost`,
  `condition_added`, `choices_unusable`, `other`;
- `material`: true only if the defect would change what the judge records or what an analyst concludes;
- `evidence`: the exact words that show it, quoted;
- `why`: one sentence.

Judge each item on its own text; similar items may differ. Return exactly one line per item of the packet, nothing else.

# Reader brief: can each opened thesis become one judged question? (Step 4 census, $0, read-only)

You are an independent reader. Do not edit files, run model calls or start runs. Do not read any other reader's answers.

## What you are reading

`clean-arch/step4-2026-11-10/census/packet.json` holds 34 cases (`packet.md` is the same content for reading). Each case is one
research question ("thesis") that a system opened while reading one news article, with:
- the fields the system wrote for it: `description` (the question), `outcome` (what is tracked), `period` (the period or check date,
  with how it was set), `opens_as` (why it opened), `settled_by` (the public material that settles it);
- the opening article: its publication date, title and full text;
- the statements that article gave as evidence for the thesis.

A later step must give each thesis a fixed **ladder** and a **due day**, by these rules (quoted from the decisions and the production
request that govern ladders; apply them as written, add none):

- **One thing (D38).** "A view looks at one thing: a question that needs a number and an event is two views … a question whose parts
  can move in opposite directions is two views." A number is "ranges of one number in its stated year"; an event is "the states one
  thing can be in on the due date".
- **Ladder type (D38; request line 25).** "Use five rungs; only a yes/no question about an event has two." "Conditions must not
  overlap or leave gaps: exactly one must hold when resolved."
- **Due day (D38; request line 26; D356).** "The due date is when the debate is settled … a number's due date is the day it is
  published." "For an event, name the date at which its outcome is assessed." "A due day falls on or after the day the result is
  published."
- **Asset or theme (request line 22).** "A question about a company's revenue, profit, share or product progress is an asset thesis
  … even when policy or macroeconomics drives it. A theme thesis asks what happens in the world, such as licensing, interest rates or
  aggregate spending, rather than the resulting effect on one company." The company here is NVIDIA.
- **Reference (request lines 24–25).** "Define concrete, verifiable conditions now. Do not propose a ladder whose thresholds depend
  on an unspecified future target." "State the neutral comparison in its condition."
- **Direction (D38).** A five-rung asset ladder runs "strongly bullish to strongly bearish, meaning good or bad for the business".

## What to return

One JSON object per case, one per line, in case order, written to the output file you are given. Read the article text for every
case; do not answer from the thesis fields alone. Fields, each a closed set:

| field | values | what it records |
|---|---|---|
| `case` | 1–34 | the case number in the packet |
| `things` | `one`, `several` | whether the thesis's wording (`description` with `outcome`) asks about one number or event, or several |
| `parts` | list of short strings | when `several`: each number or event it asks about; else `[]` |
| `parts_can_move_apart` | `true`, `false`, `null` | when `several`: could one part come out high or yes while another comes out low or no? `null` when `one` |
| `settling_outcome` | short string | the one number or event that `outcome` and `settled_by` together name as what is checked; `""` when they name several and none is primary |
| `ladder_type` | `yes_no`, `states`, `number` | for the `settling_outcome` (or the thesis when `one`): `yes_no` for an event that happens or not by the due day; `states` for one thing that can be in more than two states on the due day (D38: "the states one thing can be in"); `number` for ranges of one number |
| `due_day_basis` | `stated`, `period_end`, `expected_publication`, `none` | `stated`: the thesis gives a calendar date. `period_end`: it gives a calendar or fiscal period whose last day is a date (name which). `expected_publication`: it is settled by a publication (a filing, an earnings release, a survey) whose date neither the thesis nor the article states. `none`: no date can be read from the thesis or the article |
| `due_day` | `YYYY-MM-DD`, `null` | the date, for `stated` and `period_end` only |
| `kind` | `asset`, `theme` | by the rule above |
| `reference` | quoted text, `null` | for a `number`: a figure in the article that states what is expected, planned, guided or last reported for this same quantity; for a `yes_no`: the stated plan or deadline. Quote it exactly. `null` when the article states none |
| `favourable_end` | `higher`, `lower`, `yes`, `no`, `unclear`, `n/a` | for an `asset`: which end of the outcome is good for NVIDIA's business; `unclear` when the thesis and article do not settle it; `n/a` for a `theme` |
| `one_ladder_keeps_the_question` | `yes`, `drops_a_part`, `no` | can one ladder on the `settling_outcome` answer the question the thesis asks? `drops_a_part`: yes, but a part an analyst would want answered is left out (name it in `note`). `no`: any single ladder asks a different question |
| `note` | one or two sentences | the reason for any `several`, `none`, `unclear`, `drops_a_part` or `no` |

Judge only what the thesis and its article say. Do not judge whether the thesis should have been opened, and do not propose ladders.

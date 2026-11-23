# Splitting, reviewed at $0 against D397, D436 and D38 (D614), 2026-11-16

## The sources

- **D38 (Alex, 2026-10-20):** a view looks at one number in its stated year. "Number views carry their year … at most this year's and
  next year's are open at once": one view a year.
- **D397 (Alex):** a topic gets at most one judged question, and none when it has no main part. For a topic holding two real bets,
  "this departs from D38 until splitting is built. It is an open defect."
- **D436 (Alex):** a second side of the same bet ("the AI-chip share beside the chip total", the shortage beside the shipments) is one
  question, with the second side shown as not judged.

## The cases (`two_year_census.py` → `two-year-census-output.txt`; `refusal-census/RESULT.md`)

- **One quantity tracked for two years, refused in every send:**
  - global AI capital spending in calendar 2026 and 2027 (9 sends);
  - the five largest hyperscalers' capex in calendar 2026 and 2027 (9 sends; the readers call the refusal unjustified);
  - mixed with several products, so a year split alone is not enough: AI memory contract prices "through 2026-2027" (12 sends).
- **The other 20 topics naming two years** track one year, the other being a base or context, and the step wrote a ladder for that year.
- **The official gate's line-4 failures** (Alex's 44, run 4) are not year pairs:
  - acc/clean-9 is D436's own example (global semiconductor revenue with its AI-chip part), refused although D436 makes it one question;
  - u3/clean-11 is a spending split with a capacity split in brackets.
- **The guards:** the Intel stake (amount and ownership share) and Firmus (amount and stake). Neither is a year pair.

## The two paths, restricted to years

| | Separate topics before judging (split by year at the step's entry) | Two judged questions under one topic |
|---|---|---|
| Source | D38's one view a year; D397's "until splitting is built" | the same, but D397 decides at most one judged question per topic |
| How it decides | **Identity only:** the step names a typed refusal case "one quantity for two periods" with the two years; code re-asks it once per year with the topic restricted to that year | the step writes a list of ladders, one per year |
| Guards | kept: no year pair, so Intel and Firmus still meet the main-part rule | kept the same way |
| Materially different from the boundary study's "a question for each thing" | **yes:** it splits only by the period (identity, D38), never by kind of figure, so a second side (D436) and a two-thing stake are untouched | the same restriction |
| Measurable against the frozen gate | **yes:** each half is an ordinary one-year topic, read by the unchanged gate-1 form | **no:** the form reads one ladder per send |
| What it changes | a new version of the frozen answer-choice step (D426): one enum value in the refusal schema, and code that splits | a new output shape, the writer and the form |
| Effect on the official gate | **none:** the 44's failing sends are not year pairs | none |

## What the review gives

- **The year split** (separate topics, by code, on the step's own typed refusal):
  - a general, sourced way (D38) to recover worthwhile bets (two capex matters, central to the product);
  - it keeps the guards, differs materially from the refused "a question for each thing", and is measurable without changing the ruler;
  - **it closes part of D397's open defect** within D397's own terms.
  - **It moves no gate:** the 44 are untouched, gate 2's controls are July-bound, and gate 3's capex losses were one-year theses with
    the other year as a base, not refusals.
  - Its class on the stored readings is small: 2 topics, 18 sends.
- **The official gate's line-4 refusals are the D436 kind.** The existing candidate for them, A2 (D436's clause in the step), was
  negative on its fixed rule (D583), and tuning on the 44 is stopped (D426).
- **Two judged questions under one topic** is not measurable by the frozen gate's form and needs D397 changed. Not recommended.

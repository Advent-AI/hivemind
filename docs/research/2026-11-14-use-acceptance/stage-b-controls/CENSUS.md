# Stage B's control line: can it be exercised within its fixed population? (D575, 2026-11-16, $0)

**Answer: not by re-sending the judge on these inputs.** The line needs 8 of the 15 control theses (Ohio listed apart) eligible
with reader B's material shown; 4 are. Eligibility and the material shown were fixed before the judge ran, so an unchanged
judge-only re-send stays at 4. On paper, if the ladder step and the delivery of three items were each repaired, the count could
reach 8 (exercising the line, not passing it); that bound is conditional and untested.

**This census repeats an earlier trace.** `clean-arch/step4-2026-11-10/stage_b/CONTROL_TRACE.md` (2026-11-12, reviewed) traced the
same eleven controls from the opening article to what the judge saw. I did not read it before this census (the fifth miss of the
search-earlier-traces rule). Its attributions govern; the table below follows it. What this census adds is only the bound above.

Script and output: `control_census.py` → `control-census.txt` (the readers' verdicts from
`clean-arch/step4-2026-11-10/stage_b/result/control-count.txt`; the thesis as Steps 1 to 3 opened it, from `stage_a/cases.json`; the
question the ladder step wrote, from each draw's `clean_ladders`). The census reproduces the stored count: counted 4, eligible 7.

## The 15 controls by blocker (attributions from CONTROL_TRACE.md)

| Blocker | Controls | Where the difference first appears |
|---|---|---|
| none: counted | u1/clean-3, u2/clean-2, u3/clean-3 (Rubin by 2026, q07); u2/clean-5 (Kyber by 2027, q18) | — |
| eligible, a decisive item not shown | u1/clean-4, u3/clean-6 (2027 hyperscaler capex, q13); u2/clean-4 (2026 capex, q04) | below |
| in the opened thesis | u1/clean-1, u3/clean-1 (q09: one programme inside the total); u2/clean-7 (q16: four named companies, one not a cloud provider); u3/clean-7 (q18: the article's reported 2028 date) | Step 1's thesis; the ladder keeps it |
| in the opened thesis's outcome | u2/clean-3, u3/clean-5 (q08: NVIDIA's own sales or disclosure can settle it without an authorization) | Step 1's outcome |
| both | u1/clean-6 (q18: Step 1's period 2028 became the ladder's due day; the ladder's "during calendar 2027" adds a restriction) | Step 1 and the ladder step |
| the ladder step's wording, disputed | u1/clean-11 (q08: company scope; third readers split) | the ladder step, unresolved |

## The three items not shown (CONTROL_TRACE.md, re-checked in the stores)

- **Analysts' 82% and 41% NVIDIA revenue growth (q13):** kept in each draw (u1 e86, e131; u2 e97, e141; u3 e88, e135), filed under
  no question. In u1 and u3 one copy was stored by the very call that opened the capex question.
- **Half of 2027 data-centre spend going to memory (q13):** kept in each draw (u1 e145, u2 e155, u3 e149), filed under no question,
  by a later call while the capex question was open.
- **Management's "accelerating growth rates" near $100 billion a quarter (q04):** kept in u1 (e486, unfiled); no record in u2 or u3.
  Its source article left no record in u2; whether it was read is not traced, so no extraction failure is claimed.
- **Both q13 controls agree with reader B without these items** (as does u2/clean-4): delivering them would make the controls count;
  on this record it would not change their answers.

## What would reach 8, within the fixed population (paper bounds)

- An unchanged judge-only re-send: 4.
- Plus u1/clean-6, if both its opened thesis (period 2028) and the ladder step's question and day matched the ruler and its shown
  material held: 5. A ladder repair alone cannot supply it; this is an unproved combined change.
- Plus the three eligible controls, if their items were delivered: 8, which would exercise the line, not pass it (all but one of the
  eight must agree). u3/clean-5 and u1/clean-11 also lack material and would need their own traced changes.
- Each step assumes the readers' marks carry over to changed questions, days and requests; none is demonstrated.

## What this means for the next step

No unchanged judge-only paid send of Stage B is proposed. Any later Stage B test on a changed upstream version or another population
needs its own reviewed design and decision, and a reconciliation with the frame's "no further paid test on the frozen ruler". The
12 of 15 agreement with reader B includes differently worded questions: it is an overlap with the reference, not evidence that those
answers are right, and the four counted controls alone cannot establish the judge's quality.

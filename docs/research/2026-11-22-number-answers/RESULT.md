# Why the number answers cannot be trusted: council round 45/45b (2026-11-22, consensus, $0)

Alex asked to step back and find which part of the design produces the unreliable numbers. The record:
- `round45-brief.md`;
- `claude-r45.md` (written before Codex);
- `codex-r45.md` (an independent investigation, fresh thread `01a20501…`, read-only, no model calls);
- `round45b-brief.md` and `codex-r45b.md` (the challenge round).

## The answer

The system has no single, checked calculation behind its related numbers:
- **Each number question is judged alone.** It rebuilds the company's numbers from its own slice of evidence, with its own bases and
  its own reference.
- **It publishes the result as prose.** Code cannot tell a sourced figure from an assumption, and never recomputes anything.

Contradictions between related questions and unsupported figures are what this design produces. They are not one prompt sentence's
fault.

## What the traces show (three finished poc-v118 draws, 07-01..09-20)

- **Cross-question contradictions:**
  - old-2 at 09-20: Data Center Q4 is about $146B, the whole company's Q4 about $127B. In old-1 on 09-20 it is $126B against $112.2B.
  - A stated segment Q4 above the company Q4 on at least 13 of 26 paired post-earnings days in old-1, and at least 1 in old-2.
  - Data Center's full year above total revenue's full year on 20 consecutive days in old-2 (08-26..09-14). Claude checked 08-28, 09-05
    and 09-12: $419B, $422B and $414B against $407B.
- **Different bases for the same quarter:** on 17 of 18 paired days, 09-15..09-20, Data Center used the $108B Q3 guide while total
  revenue used a beat-adjusted Q3 of about $113.5B.
- **Disjoint inputs:** old-2's two questions share 106 of about 1,300 linked evidence items. Their 09-20 requests share 5 entries and
  cite none in common. Across draws, total against CPU shares 0–5%. The SemiAnalysis uplift was filed under Data Center only.
- **Unsupported arithmetic:** in 17 of the 24 answers both readers rejected, the figures came from:
  - adding amounts of unknown overlap (#36: $25B + $18B);
  - another scope's figure scaled by a mismatched ratio (#38: 730/800 × $1.3T);
  - a stacked uplift (#44);
  - an unsized trim (#48);
  - the system's own earlier figure presented as the market's (old-2 v9: $414B; 44 of 2,375 flagged).
- **The production check passes them:** six saved answers still pass with a contradictory forecast or an invented reference
  substituted. Only a citation outside the request fails (`judging.check_answer`: rung range, ids, pushes, non-empty fields).

## The design causes, ranked

1. **Answers are prose with one answer-wide citation list.** No figure is tied to its source, and nothing recomputes. This explains
   most of the 24.
2. **Related questions compute shared quantities separately.** The judging unit is one question, with 0 dependencies in 139
   questions. This explains the contradictions.
3. **Filing (narrowest question) and the evidence in view (D198) give related questions different inputs.** The previous conclusion
   carries figures without provenance, which is the self-made reference.
4. **Opening's bands and pull mode amplify a bad figure:** where the boundary sits decides when the error shows.

Linking passed one question's conclusion to another, but not its assumptions. Data Center stopped exceeding the total in the pilot, but
the total added a CPU forecast whose overlap was unresolved (D721).

## The converged design (for a new judge version Alex opens)

- **One judging call per related family.** Same company and fiscal year, overlapping quantities. Each question keeps its own answer,
  and every answer reads from one calculation.
- **The judge labels the figures it uses:** what each measures (population, scope, period) and whether it is a source figure, a
  calculation or an assumption. Extraction v74i is unchanged.
- **Code checks identity and arithmetic only:**
  1. a source figure appears in the shown passage it cites;
  2. the arithmetic recomputes;
  3. a declared part fits within its whole for the same period and scenario;
  4. one value per shared quantity, role and scenario across the family;
  5. a market reference points to shown external material, or says none.

  The model keeps importance: drivers, weights, discounts, and overlap stated as an assumption. A blind reader judges whether an
  assumption that crosses a boundary is supported.
- **When figures cannot be reconciled, the forecast shows as unresolved,** not as two incompatible answers.
- **Bounded to the figures the open questions consume** (D24, D28).
- **Families:** declared from stored cases for the test. Production would need a matching version that names the relationship.
- **The frozen gold's reasoning is kept:** q01 (upside drivers without a fixed increment), q02 (a segment from the shared total and a
  sourced mix), q19 (an execution discount), q22 (FY2028 from q01's base, widened by judgement).

## The interim for a first release

Publish questions, evidence and events, and show number questions as "Forecast unavailable": the band, the forecast text and its
history withheld together (`bundle.py`).

## The one test (registered with the design)

- **The $0 gate.** Hand-reconstruct, in the new format:
  - old-2 8729/8737, 8734 and 8595, and old-3 9166;
  - the four gold controls;
  - three planted errors (an amount absent from its quote, a wrong sum, an internal forecast labelled consensus).

  The format must expose every defect, represent every control, and fail every plant. Any miss stops the line.
- **The paid gate** (Alex's ceiling; 36 calls, about $0.2–0.4 estimated):
  - **The arms:** the 09-20 total and Data Center pair in each draw, three samples each, judged jointly and separately under the same
    format and checks. Plus three samples each on the O, S and E requests. Every output is read against its source with the arm
    hidden.
  - **Pass:** the joint arm publishes both answers usable and source-supported in at least 8 of 9 pairs, at least 2 of 3 per snapshot,
    and at least 3 more usable pairs than the separate arm. Zero published hard contradictions, internal-as-market references, or
    unresolved overlap, scope or unsized adjustments that decide the band.
  - **Stop:** any such published defect, either coverage line missed, or an incomplete comparison.

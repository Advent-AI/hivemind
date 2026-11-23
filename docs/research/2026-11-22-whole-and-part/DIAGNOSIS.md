# A part added to a whole that already holds it: diagnosis (D720, $0)

> **Superseded in part (D721, council round 43b).** The frozen judgement gold (q01) lists the Vera CPU target among the drivers
> above consensus, so §1's premise that the basis "already contains it" is Claude's view, not the ruler's, and §4's edits have no
> source. old-1 has 26 explicit additions, not 32 (`codex-r43.md`). The design is recommended closed with nothing built; the
> surviving findings are listed in D721.

Alex opened the design of the double-count fix (D720). In the linking pilot, the total-revenue judge added the stand-alone CPU
forecast it read through a link to a total that already contained it (D711, H4). AGENTS §1 asks for the whole class before a design.
This file is that diagnosis. Nothing is built or sent.

## 1. The class, counted on stored data

**Class:** a judgement of a quantity that contains others (a company's total revenue) builds its figure from a company-wide basis
(consensus, or guidance carried forward) and then adds all or part of a component's forecast (here NVIDIA's stand-alone CPU target)
as if the basis did not already contain it.

**Population:** every distinct judgement of a total-revenue, total-revenue-growth, Data Center or total-CPU question in the five
comparable stores: old-1, old-2 and old-3 (three draws of poc-v118 over 07-01..09-20), and the fresh reader rows of the two pilot arms
(control-1 poc-v118, linked-1 poc-v120). Pilot rows copied from old-2 are excluded. Total: 1,354 judgements.

**Listing:** `census_candidates.py` lists the 746 of them that name a component (CPU, Vera, Grace, Rubin, networking). Claude read:
- all 209 whose implied outcome names a component together with an arithmetic or inclusion word;
- for the instrument check, the reasons of every other total-revenue candidate that puts an addition word within 80 characters of
  "CPU" or "stand-alone" (76 answers). That check found 6 more old-1 answers (07-22, 07-23, 07-24, 08-15) and the old-3 mentions.

| Store | Total-revenue answers after the CPU target was in view | Target added into the figure | Rung decided by it (own arithmetic) | Mentioned as upside, not in the figure |
|---|---|---|---|---|
| old-1 (v4) | 77 (from 07-05) | **32** (07-07..08-25) | **4** certain (07-15, 07-16, 07-17, 08-21), 11 possible | 0 |
| old-2 (v14) | 0 (the target was filed under the stand-alone CPU question v8) | 0 | 0 | 0 |
| old-3 (v3) | 77 (from 07-05) | 0 | 0 | 2 (07-11, 07-22) |
| control-1 (v14) | 0 | 0 | 0 | 0 |
| linked-1 (v14, through the link to v8) | 71 (from 07-10) | **4** (07-15..07-18) | **4** (rung 3 to 2) | 1 (v21, 07-26) |
| linked-1 (v9 reading v14) | 71 | 4, copied from v14's reasons (07-16..07-19) | 0 | 0 |

- "Certain": the answer's own arithmetic puts the figure below the boundary before the addition and above it after. On old-1
  07-15: "$430 billion — just below rung 1 … allowing for partial contribution and possible consensus inclusion, a net few billion
  dollars takes the implied result to roughly $435 billion, above the $431.2 billion boundary". On 08-21: $404B plus $20B for CPU plus
  $10B for SpaceX, giving $434B. Without the CPU it is $414B, rung 2.
- "Possible": rung 1 within a few billion of $431.2B, with the CPU share not sized (07-30, 07-31, 08-06..08-12, 08-14, 08-15).
- **Since when:** from the first day the component target is in the whole's view, as evidence filed under it or as a linked
  dependency. Filing decides exposure. In old-1 and old-3 the target ($20B stand-alone CPU, e65) was filed under total revenue at seq
  49, because no CPU question was open yet. In old-2 the stand-alone CPU question opened at seq 49 and took it.
- **Not the class** (read, then set aside):
  - **Total CPU = stand-alone Vera $20B + Grace above $5B trailing 12 months**, about 100 answers in all five stores from 08-26
    (rung 1, above $25B). The sources name two different products: e2542 is "Our Grace CPU introduced in 2021 … exceeding $5 billion",
    and e897 is the CEO's "The $20 billion is for standalone CPU". Summing them is a defensible reading, not a basis that already
    contains the part. Recorded as a boundary case; a reader could still question whether stand-alone Grace sales sit in both.
  - **A quantified revision of one component applied to its share of the total** (SemiAnalysis's 20% second-half compute uplift,
    e.g. old-1 07-10, old-3 08-12). The prompt asks for this: "a quantified revision … shift[s] it".

## 2. The mechanism (one case end to end, then the request)

- **The trace: linked-1 v14 on 07-15** (call 8756).
  - The request shows the dependency as `v8 (open; first_is_bullish) How much revenue will NVIDIA generate from stand-alone CPU
    sales in FY2027?`, its comparison point, and "The system's forecast for it (our own judgement, not evidence): About $19.5
    billion".
  - Nothing in the request says whether that quantity is inside this one.
  - The answer: "Adding the dependency's roughly $19.5 billion FY2027 stand-alone CPU forecast, which is distinct from the existing
    revenue run-rate, gives about $407 billion and crosses into rung 2."
  - The previous day's answer to the same request shape said the opposite: "included within total revenue, not added on top". So
    did 07-20's ("a component of total revenue, not an amount to add to this company-wide run-rate").
  - 07-16..07-18 repeat the addition, carried by the previous conclusion.
- **The trace: old-1 v4 on 07-07** (no link). The CPU target (e65) is evidence under total revenue. The answer: "the $20 billion
  stand-alone CPU FY2027 forecast adds some upside but is heavily discounted because the planned fall launch leaves few selling
  quarters and no volume in hand." That is the request's own product-target sentence, applied to a whole.
- **The request sentences** (judging-v7, the frozen product judge; judging-v8 has the same text):

| Failure | The request sentence | The standard on the case | Verdict |
|---|---|---|---|
| A component's target taken into a whole's figure | "A target for a product with no shipments yet is discounted by default; it is taken in full only when the evidence shows the volume in hand." It is written for a question about that product, but nothing limits it, so on a total it reads as "add a discounted share". | D260: judge against the reference (consensus, guidance). A company-wide basis formed after the company published the target already contains it. | **keeps wider**: the sentence's scope is narrower than its wording |
| No rule for a whole reading its part | "check it against the dependencies' conclusions shown (a part cannot exceed its whole …)"; "a component cannot exceed its whole". Both cover only the part's side. | PRD 06: one ladder per thing, dependencies connect them. Whether a part is inside a whole is identity of the quantities, not weight. | **missing** (one direction only) |
| Sticky after one draw | "The previous conclusion is supplied only for comparison." | none | **not the prompt's class**: carry-over spreads any error until a judge reverses it, so it is not a fix for this class |

## 3. Step back

- **Product, not measurement:** the frozen product judge does it in one of three product draws (old-1), with its rung decided by
  the addition on at least 4 days. The linking version only adds a second route in: the dependency block.
- **Not a link-direction problem:** banning a whole from reading a part would leave old-1's route open. D702/D703 also rejected a
  blanket ban; Alex's D703 option said "no blanket ban on a whole reading its part". And D711: the keys label stand-alone CPU
  `other`, so code cannot tell part from whole.
- **The frozen ruler does not see it:** the judgement gold reads 07-14. old-1's first decisive day is 07-15, and linked-1's is
  07-15.
- **Prior decisions searched** ("double count", "already includ", "component", "its whole"): none rules on a judge adding a part
  to a whole. D191's shared quantity and D186's rungs against guidance do not cover it.

## 4. Where a fix belongs, and its cheapest proof (for the council; nothing written yet)

- **Owner:** the judge's text. It is the one place that decides how a figure is built, and both routes (filed evidence, a
  dependency) meet there.
- **Two candidate edits, both general (any company, any total and its parts):**
  - make the existing consistency clause two-sided: a whole built from company-wide figures already holds its parts, so a part's
    forecast or target moves it only by the gap the evidence shows against what that basis assumed;
  - scope the product-target sentence to a question about that product.

  Line 9's "a component cannot exceed its whole" duplicates line 4's clause and can be cut to pay for the growth.
- **Versions:** a new version of the frozen product judge (judging-v7) and, if the linking line resumes, of judging-v8. Both
  Alex's to open.
- **Cheapest proof** (paid, cents, Alex's ceiling):
  - **The class:** re-send the stored requests where the addition decided the rung, under the old text and under the changed text,
    three draws each: old-1 v4 07-15, 07-16, 07-17, 08-21 and linked-1 v14 07-15..07-18. The old-text sends give the base rate:
    07-14 shows the same request shape going either way.
  - **Controls that must not move:**
    - the SemiAnalysis share uplift (old-1 v4 07-10, old-3 v3 08-12);
    - the total-CPU sum of two named products (one old-2 v16 day after 08-26);
    - a part reading its whole (linked-1 v9 07-14 and 07-21).
- **The share** the fix can remove: all 36 additions (32 + 4) and the 4 copied ones, if the judge follows the sentence. A sampler
  can still slip, so the proof counts slips per draw.

## 5. Out of scope

The citation format (D719), the link-question wording (D705 forbids a third wording on the same 105 pairs), the sticky previous
conclusion, the frozen ruler, the total-CPU boundary case beyond its control role.

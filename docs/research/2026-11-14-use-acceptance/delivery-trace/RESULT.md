# The company's own figures on the carried fortnight: where they went (D609's trace), 2026-11-16, $0

**Material:** the stored carried fortnight (`poc/data/clean-carried-run-2026-11-16/`), with its Step 1 trace, the Step 3 library
(`step2/library.json`), the writer's store and all 95 judging requests.

## Identity, by code (`trace_figures.py` → `trace-output.txt`, `pairs.jsonl`, `groups.txt`)

- **Population:** every kept statement whose party is NVIDIA and which carries any figure, with no measure list: 325 statements.
  - All 325 match a store record (0 unmatched).
  - They fall in 88 repeat groups.
- **Against the 12 judged questions:** 3,773 fact-question pairs available by each question's last judgement.
  - Of these, 3,534 never reached that question: 835 because they were linked to another question, and 2,699 because they were
    linked to none.
  - Most are about matters other than the question. Code makes no claim about bearing.

## Bearing, read by hand (`groups.txt`, then each candidate's source quote and the question's last request)

**49 of the 88 groups are linked to no question.** They are the company's own results: revenue, net income, margins, EPS, buybacks,
dividends, cash flow. None of the 12 questions asks about them; under D382 and D384, figures are evidence, not questions. So they
have no home in this library: a matter of which questions exist (D559, gate 4), not of delivery.

**Bearing and not delivered: 5 statements on 3 questions over 2 matters.**

| Question | Statement | In the last request? | What kept it away (the library's own record) |
|---|---|---|---|
| v12, a residual-value guarantee finalized | e990: Nvidia "could carry a residual-value guarantee of no more than 25%" | partly: Morningstar's estimate of 25% is shown | **Step 3's look-back rule:** linked to v1 on 2026-10-03, and a group that arrived under another question is not reconsidered for a question opened later (D514) |
| v12 | e995: Nvidia "previously provided a residual-value guarantee" for SB Energy's Ohio financing (S&P, Moody's; no figure, read because it shares e990's day and link) | no | the same look-back rule |
| v5 and v9, top-five hyperscalers' data-center capex (2026, 2027) | e489: NVIDIA's projected share of their IT capex, 11% to 44% by 2027 | no | **model judgements:** Step 1 linked it to nothing while v5 was open; the look-back judge said no for v9 |
| v5 and v9 | e648: sales to the largest cloud companies, $49 billion in a quarter | no | the same two judgements |
| v5 and v9 | e767: hyperscale revenues $48.71 billion, +117% | no | the same |

Weaker leads, not counted: revenue per gigawatt for the U.S. gigawatt question (v10), and the 45% consensus beside the 70% growth
outlook for the Vera Rubin question (v4).

## The independent second reader (`brief-second-reader.md` → `codex-second-reader.jsonl`; key outside the repository)

A fresh Codex session read the three questions' last requests and 14 statements blind, with a negative control (a dividend raise) and
a positive control (a statement already shown) per question.

- **Controls:** all three negatives "does not bear"; all three positives "already in the request".
- **Candidates:**
  - every one "bears", agreeing with my own reading (`own-read-before-reader.md`);
  - "not in the request", except e990, "partly";
  - **every one "unlikely" to move the answer.** For example, e995: "a relevant precedent, but the request already favors a finalized
    guarantee."
  - The fortnight's reading 4 found the same: confidence only.

## What it gives (D609's criterion)

- **Delivery of the company's own figures is largely established where they bear.** The bearing groups are linked and shown: the
  credit-support, purchase-commitment, Vera Rubin, export, memory and Hugging Face figures.
- **The undelivered bearing ones are few** (5 statements on 3 questions). **They come from two mechanisms:**
  - Step 3's look-back boundary, a code rule;
  - the model's link judgements.
- **Neither reader predicts any of them would move an answer.**
- **This closes the company-figure repair route.** The look-back boundary now has a third instance: the fresh week's MIIT stop order
  (D508) and v12's two here. Its effect on an answer is still not shown (D511 was inconclusive). D517's reason not to widen it
  ("reach and effect not established") is narrowed on reach and unchanged on effect.
- **The 49 homeless groups are the opening question, not delivery.** Under Alex's D382 and D384 they get no question of their own.

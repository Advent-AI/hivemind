# q12 (capital spending): why its fact never reaches the judge, and the candidate c12

Alex, 2026-11-09, asked what to do after Stage 2 of D392: "先修“现金花在哪里”那题". The option he chose said that this changes the
clean system's reading step, which is frozen on c8 (D391), and so needs his approval.

## 1. The class (counted on stored data, $0)

q12 is "How much will NVIDIA spend on capital expenditures in FY2027?" (gold v1: $7–11bn).
- **The reference.** Reader B's reference is i131 (Zacks, 2026-07-06, `gnews:25d0b1d2a9dfe0bb99432e1a`): "During the first quarter,
  NVIDIA generated $50.3 billion in operating cash flow and $48.6 billion in free cash flow." That is about $1.7bn of capital spending
  a quarter.
- **Stage 2 delivery** (`clean-arch/e2e-2026-11-09/stage2-delivery-audit.txt`):
  - The $50.3bn figure is never stored in any of the six runs.
  - v12 has no evidence and is never judged in any run.
  - Of q12's other gold items, the clean system stores i007, i006, i145, i001, i120, i301 and i052, and links them to v9 (NVIDIA's
    investments and commitments in partners), where they belong. None reaches v12.
- **The decisive missing fact is one sentence.** With i131 alone, the Q1 run-rate is about $7bn a year, which sits on rungs 4 and 3 of
  v12's ladder (5–8 and 8–12). Both overlap the gold $7–11bn.

## 2. The mechanism (traced)

**In all three seeded clean draws, the Zacks answer keeps:**
- revenue and EPS (linked to v1 and v11);
- the data-center segment (v2 and v20);
- Q2 guidance (v1 and v3);
- the buyback and dividends (v11).

**The cash-flow sentence is not in the answer at all:** not written, rather than refused by a check.

**The model's own account** (`account.json`: the stored conversation continued with the fixed question, $0.012), the same in 3 of 3:
> "a cash-rich company's cash balance or cash flow usually changes none of these when the item ties it to nothing," reinforced by the
> closing check: "a cash-rich company's balance or cash flow that the item ties to nothing usually cannot." … The $50.3 billion
> operating and $48.6 billion free cash flow are tied to no thesis.

**The request read as the model reads it** (c8, `clean-arch/step1-unfiled-2026-11-08/arms/c8-system.txt`, CONDITION):
1. Company figures "inform an open thesis about its revenue or earnings path when they bear on that path". No other open thesis is
   named as one a company figure informs.
2. "a cash-rich company's cash balance or cash flow usually changes none of these when the item ties it to nothing". The model reads
   "the item ties it to nothing" as: the article does not tie it. It does not read it as: no open thesis uses it. Yet operating cash
   flow less free cash flow is capital spending, by definition, and an open thesis asks for capital spending.

## 3. Step back: the decision and the standard

**Alex's ruling on this exact sentence** (round log §11, 2026-11-08, his reply to that question): the library then held "a 'Vera Rubin
shipping and revenue growth' thesis open; no profit or cash thesis". His answer: "丢掉" (drop).
- My reading at the time: "A backward figure that does not move that question's answer (a cash balance, operating cash flow) is
  dropped."
- The ruling was given for a library in which no open thesis the figure informs existed.
- c8 wrote it as "when the item ties it to nothing", which drops the figure even when an open thesis asks for what it states. That is
  wider than the ruling.

**The standard** (AGENTS §8, from the signed standard's sources):
- "Ask what revenue, profitability, cash risk or competitive position the information can change; then separately decide whether it
  supports an existing question or merits a new one."
- c8's own rule: "Link one statement to every thesis it informs."
- The CONDITION's "an open thesis about its revenue or earnings path" keeps narrower than both.

**PRD 10 §2** names this class: "the operating-margin and NVIDIA capital-spending questions received nothing at all and were never
judged" (the narrow questions starve). c8 now delivers for operating margin and custom chips (Stage 2); capital spending is the one
left.

**Prior decisions on the mechanism:**
- **D371:** keeping financial information does not require a question per line. c12 opens no question.
- **D389 and D390:** about opening, untouched.
- **D391:** c8 closed. A change is a new version that Alex opens, and he opened this one with the reply above.
- **The D388 line was stopped for chasing programme cases one by one.** This change is not a case rule. It restores the ruling's own
  scope and the standard's "every thesis it informs".

## 4. Prompt audit rows (AGENTS §6)

| failure class | request sentence | the standard's line or decision | verdict |
|---|---|---|---|
| a company figure that states what an open non-revenue thesis asks (capital spending from operating and free cash flow) is not linked | CONDITION: "inform an open thesis about its revenue or earnings path when they bear on that path" | AGENTS §8 "then separately decide whether it supports an existing question"; c8 "Link one statement to every thesis it informs" | keeps narrower |
| the same figure is then dropped | CONDITION and closing check: "…when the item ties it to nothing" / "…that the item ties to nothing usually cannot" | Alex's ruling 2026-11-08, given where no open thesis the figure informs existed | keeps wider than the ruling: it drops where the ruling did not speak |

## 5. The candidate c12 (three sentences; `arms/c12-*`; the schema is c8's, unchanged)

1. **CONDITION.** c8's clause stays word for word: "inform an open thesis about its revenue or earnings path when they bear on that
   path". It gains ", and any other open thesis whose figure follows from them by a standard definition (two reported balances give the
   change between them; a reported total less one of its parts gives the other part)". Both examples are generic arithmetic; neither
   names cash flow or capital spending.
2. **CONDITION.** "…when the item ties it to nothing" becomes "…when it informs no open thesis".
3. **Closing check.** "…that the item ties to nothing usually cannot" becomes "…that informs no open thesis usually cannot".

**Size:** the system prompt grows from 15,828 to 16,025 characters (+197); the closing check shrinks from 8,638 to 8,636. Prompt tokens
per arm are reported from the probe's usage.
- **Why it grows:** the derivation case had no clause at all. The model linked company figures only to a revenue or earnings thesis,
  and read "ties it to nothing" literally. Two generic examples carry it (AGENTS §6: a classification is written with examples).

**Blind whole-request audit** (a fresh reader on c12's system text, closing check and schema; its report is a lead, and each point
below was checked against the text):
- **The first draft would have been rejected.** It wrote "inform every open thesis whose answer they bear on, its revenue or earnings
  path included". The reader showed this could read as "every result bears on the revenue thesis", which invites linking cash figures
  to a revenue thesis in Alex's library. The rewrite keeps c8's revenue clause unchanged and adds only the derivation case.
- **Pre-existing in c8, not changed here, recorded:**
  - "covers", "bear on" and "informs" name one concept. The "covers" split was probed and stopped as c9.
  - The section 3 lines that keep unlinked figure statements sit against the closing read-back, which may not return them.
  - The closing check's "a valuation is not kept, even with its assumptions" follows Alex's 2026-11-08 ruling, against standard 5.3's
    conditional valuation. It is recorded under D373.
- **The remaining risk the reader names:** a model may still decide that a capital-spending thesis does not "cover" a cash-flow
  sentence. Line A tests exactly that.

**Expected effect on the judgement** (AGENTS §7.3): v12 receives the Q1 cash-flow sentence, is judged, and lands on 5–8 or 8–12, which
agrees with gold $7–11bn. No other question should lose a delivered fact. The risk is wider linking of company figures to theses they
do not inform.

## 6. The probe (frozen before the send: `probe-frozen.md`)

**Cases** (stored before-states, so the arms differ only in the request):
- **A. Zacks, seeded:** clean d1 of Stage 2 (segment 2, sequence 12), with v12 open.
- **B. Zacks, Alex's library:** dev d1 article 57, with no capex or cash thesis open; the ruling case.
- **C. Regression:** the 13 Stage 1 articles, at their stored seeded states in clean d1 of Stage 2.

**Arms:** c8, whose rebuild must equal the stored sent request byte for byte where the stored run is c8, and c12. Three draws each.
That is 84 calls over 14 cases, about $0.88 estimated.

**Lines:** as frozen in `probe-frozen.md`. That file governs; it was tightened after council A's first round: case B checks both
cash sentences against c8, and the added links go to a blind reader.

# Phase 2, step 1: why the old system never opens 16 of the 32 matters ($0, D685)

**Source:** `opening_census.py`, written to `poc/data/hybrid-2026-11-20/opening-census.json`. For each matter's articles in each old
draw it records:
- the candidate questions the extraction proposed, and what matching did with each;
- where the evidence from those articles was linked;
- the mapping readers' verdict (`reading-diagnostic/mapping-out/map-L*-*.txt`).

Claude read every row.

## The answer
None of the 16 is lost because the old system failed to see the facts. In every draw it wrote evidence from those articles, between 2
and 138 items a matter, and linked most of it to questions it holds. There are three causes, and **two of them are design rules Alex
set.**

| Cause | Matters | What happens | Rule behind it |
|---|---|---|---|
| **A. One bet, one question.** The scoring list splits a bet that the system keeps as one question | M02, M03, M24 (five-company capex, total and data-center), M26, M28 (the EU and U.S. review stages of the Hugging Face deal), M27 (the Hugging Face obligation amount), M12 (the Ohio lease-guarantee amount), M20 ($125B residual-value support), M32 (neocloud capacity commitments), M07 (FY2028 data-center revenue) | The extraction proposes the variant, and matching merges it into the held question. old-1 proposed "top five hyperscalers' capex" 8 times; each merged into the four-company question. Otherwise the variant's evidence goes to the held question: the Ohio guarantee's to "will NVIDIA sign the guarantee", the $125B's and the capacity commitments' to "credit support, guarantees and capacity backstops", FY2028 data-center revenue's to FY2028 total revenue. The mapping readers mark these "broader" or "missed": old-2 Q43 joins the U.S. and EU clearances by 2027-06-30, and the list asks for each review stage at 2027-01-31 | D248, "one bet, one question" (Alex). The comparison's frozen matter list (D671) is finer than D248 for these 10 |
| **B. The library's subject is NVIDIA only** | M01, M22 (Broadcom's AI revenue, FY2027 and FY2026), M23 (CoreWeave's revenue), M29 (Marvell's revenue), M21 (Alphabet's capex) | Every request says "[Subjects] The objects this item concerns: NVDA". The prompt puts a company's own figure under that company's ticker. The old draws proposed 0 candidates with any company object other than NVDA. The evidence went to NVIDIA's revenue questions | The corpus tags NVDA as the only subject. Broadcom, CoreWeave and Alphabet are on the research list (`poc/universe.json`); Marvell is not. D187: a company's own quantity is a thesis under that company |
| **C. A theme proposed under the wrong name, or not proposed** | M16 (DRAM prices in 2027); M05 (2026 semiconductor sales, served in 1 of 3 draws) | M05: old-2 proposed it under the object "Semiconductor sales worldwide", and the research-list check refused it. old-3 used `semiconductor-cycle` and opened it. old-1 did not propose it. M16 was proposed in no draw | Within the standing decisions |

## The attainable ceiling (council K's falsifier)
- **Within the standing decisions:**
  - the judge, +2 (M08 and M14), not reached by any tested change;
  - cause C, up to +2 (M05 steadied, M16);
  - the matters served in only 1 of 3 draws (M09, M25, M30), whose share is uncertain.

  **That is about 4 to 6 at best, every piece uncertain, against D665's lead of 5.** The hybrid cannot be shown better than old
  without one of Alex's rules changing.
- **The generous ceiling:** if cause A were opened as separate questions (+10) or cause B's companies were tagged (+5), it is well
  above 5. So the falsifier does not fire as worded. **The constraints that set the ceiling are D248 and the library's NVIDIA-only
  subject, both Alex's**, together with D382 (company figures: 7 of the 32 are company figures, and old serves 5 or 6 of them).
- **The concern is recorded, as D373 requires, and the frozen list is not changed.** For cause A, the comparison's matter list is
  finer than D248. Splitting five-company from four-company capex, or the EU stage of a review from the U.S. stage, is the
  "wordings, deadlines, milestones and periods of one bet" that D248 keeps as one question.

## Council L (`council-l-codex.md`, DISAGREE) and the corrected classes
**Verified against the trace.** In every draw, M07, M12 and M20 had no candidate proposed. They were not merged; they were never
proposed. D248 allows them as separate questions:
- FY2028 data-center revenue can move apart from total revenue;
- the guarantee's year-end amount can move apart from whether it is signed;
- the $125B support is one agreement, which an aggregate balance cannot settle.

M24 and M27 were not proposed either.

**Withdrawn:** "none of the 16 is lost because the old system failed to see the facts". The trace counts evidence and links by article.
It cannot show that the decisive facts were kept.

| Cause (corrected) | Matters | Within the standing decisions? |
|---|---|---|
| **A. Merged into a held question, or a variant of one** (code-owned shared-quantity key, D197; one bet, D248) | M02, M03, M24 (five-company capex variants); M26, M28 (old-2 opened one joint U.S.-and-EU clearance question); M32 (old-2 merged it into "credit support, guarantees and capacity backstops") | No: the list is finer than the key |
| **B. Library subject is NVIDIA only** | M01, M22 (Broadcom), M23 (CoreWeave), M21 (Alphabet), M29 (Marvell, not on the research list) | No: a scope choice |
| **C. Never proposed, though D248 allows a separate question** | M07, M12, M20, M27, M16; also M05, refused once under a wrong name and not proposed once | Yes. A fix is a new version of the frozen extraction (D274), which only Alex or the council opens |

**The ceiling, counted the way D665 counts it.**
- The named opportunities within the standing decisions are gross gains:
  - the judge, +2, not reached;
  - cause C, up to +6, which needs a new extraction version;
  - the 1-of-3 matters, uncertain.
- D665 needs 5 net gains and at least twice as many wins as losses. A gross count does not establish that.
- Before any send, the test must show that 5 net gains are attainable.

**First question for Alex (council L): D382.** Should a company's own figure (NVIDIA's revenue, margin and segments) get its own
forecast in the hybrid, or serve only as evidence?
- 7 of the 32 matters are company figures, and old serves 5 or 6 of them.
- Under D382, the hybrid loses those by construction, so it cannot beat old whatever opening does.
- Recommendation (council L and Claude): keep a company figure as its own forecast when it is material and separately answerable.

## After D687: the attainable check before any opening test ($0)
**Alex (D687, "单独开题吧"):** in the hybrid a company's own material figure keeps its own question, as old's opening does.

**How old serves each matter, per draw.** "Served" follows the PRD's rule: a covering question both reader families mark worth
tracking, with its latest answer marked supported, in at least 2 of 3 draws. Counts below are from `deck/readings.json` and
`mapping-out/mapping.json`, under counting 1 and counting 2:
- 3 of 3: M11, M13, M15, M18, M31; M04 under counting 2.
- 2 of 3: M04 under counting 1, M06, M10, M17, M19.
- 1 of 3: M05, M09, M25; M30 under counting 2.

**Noise alone, before any change.** Suppose a hybrid with old's opening repeats old's per-draw rates:
- A matter served in 2 of 3 draws stays served with probability 20/27, so each of the five is lost with probability about 0.26. That
  is about 1.3 losses.
- A matter served in 1 of 3 draws becomes served with probability 7/27, about 0.26 each. That is about 0.8 to 1 gains.

**The 22 matters old does not serve, by what it would take.** Each mechanism was read in the stored requests and answers of old-1..3:

| Mechanism | Matters | Within D687 and the standing rules? |
|---|---|---|
| **The judge answers a held question wrongly** | M08, M14 | Only by changing D198 (Alex's); the line is paused (D685) |
| **An obligation's held question in one form absorbs a statement that, by the frozen prompt's own `binding_obligation` rule, calls for the other form** | M12: the Ohio guarantee was agreed ("agreed last month to provide a guarantee of up to $105 billion"), so its amount at the next annual filing is a question; old keeps linking to "will NVIDIA sign the guarantee" and to the aggregate credit support. M27: the $12.9B Hugging Face acquisition was agreed, and its amount is a question; old holds only completion. M20: "may also put up as much as $125 billion in residual-value support" is not yet signed, so it is a yes/no question; old links it to the aggregate | Yes. It is a misread of the frozen prompt's rule, not yet confirmed by the model's own account. A fix is a new extraction version (D274) |
| **A theme quantity proposed under a free name, or not proposed** | M05: refused once as "Semiconductor sales worldwide" while the request lists `semiconductor-cycle`; not proposed once | Yes, coin flip |
| **A sub-line or a framing variant, opened in 1 draw of 3** | M09 (networking revenue), M30 (Vera CPU revenue): the prompt says "Not every reported or guided line". M25: opened in all 3 draws, under different framings and deadlines | Partly. Steadying M09 and M30 means widening which lines open, against D248's granularity |
| **Outside the prompt's four reasons, or no figure stated** | M16: a DRAM contract price change is not an aggregate quantity of named companies. M07: the 16 articles state no FY2028 data-center figure; old holds FY2028 total revenue and FY2027 data-center revenue, with data center 92% of sales | No: needs a wider opening rule or D248 |
| **The list is finer than D248** | M02, M03, M24: five against four hyperscalers; the prompt says "A different population … is the same question". M26, M28: the review stages. M32 | No (D373 concern recorded) |
| **Library subject is NVIDIA only** | M01, M21, M22, M23, M29 | No: library scope, Alex's |

**The arithmetic, against D665 (a − b ≥ 5, a ≥ 2b):**
- **Best case within the rules:** 3 obligation-form gains, plus M05, plus M09, M30 and M25 made steady, gives 7 gross with no loss.
  That passes on paper, but only if every one converts in 2 of 3 draws.
- **Expected:**
  - The 3 obligation forms, at an assumed 0.6 per draw after a fix, give 0.65 each in 2 of 3 draws: about 2.
  - M05 adds about 0.65.
  - M09, M30 and M25 stay near 0.26 each: about 0.8.
  - So a is about 3.4, against b of about 1.4 from noise, plus whatever a new extraction version breaks.
  - The expected net is about +2, and a "no practical winner" verdict is the likely outcome.
- **Conclusion (Claude, before council M):** the falsifier "5 net gains attainable" holds only in the best case. The expected result of
  an opening test within the standing rules cannot decide release. What binds is the matter list's granularity against D248 (6 to 8
  matters) and the library's NVIDIA-only subject (5 matters), both Alex's.

## Council M (D688): the corrected attainable check
Claude's first attainable check, above, counted M12, M27 and M16 as gains within the rules. After reading the decisions, and after
council M's three rounds (`council-m-*`), the corrected classes are:

| Matter | Corrected class | Source |
|---|---|---|
| M12 | Not a miss: a signed deal under a plan tracked by amount is evidence for the total (M31, served 3 of 3) | D248 boundary 1, D388 |
| M27 | Separately answerable in principle (a deal closing in May 2027 answers M19 and still leaves an obligation at January year-end), but its public settlement source is unproven; out of the gains | Council M round 2 |
| M07 | A distinct segment forecast, but the 16 articles state no FY2028 data-center figure; a missed opening is not established | Council M round 2 |
| M16 | Allowed by the signed standard (memory contract prices), but the wording lever failed (0 memory candidates in 45 sends); out of the ceiling until a different mechanism has evidence | D480, D481 |
| M20 | A real miss: a $125B unsigned obligation keeps its own signing question; old folds it into the total, and old-1's Q29 (platform agreements by August 15) does not settle it | D388, D389 |
| M05 | A real miss, one draw in three: proposed under a free name and refused | research-list check |

**Decided (D688):** the census found no credible path to a D665 lead through opening changes alone. No opening test and no M20 account
probe are sent for release. To Alex: keep poc-v118 as production and pause the hybrid's release line.

**Answered (D689):** Alex chose option 1. poc-v118 stays production, and the hybrid's release line is paused. Council N then closed
the judge and c8 lines for now (`PLAN.md`, "Status after D689").

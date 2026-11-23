# Council R, round 2 — Challenge

**Use one matching mechanism for both opening orders, keep the later-addition case separately reviewed, and run July only.** The July ledger already contains a $393B Bloomberg-compiled projection for all of NVIDIA. On July 12, total revenue used that figure as its reference and forecast about $387B. Data Center saw neither figure and forecast $400–410B. That gives the first test both a real contradiction and a way to check whether the link delivers an outside estimate without confusing it with the system’s forecast. [Stored matching case](/Users/lchingen/hivemind/docs/research/2026-11-20-production-readiness/dependency-design/selection-census.md:59) · [Reference trace](/Users/lchingen/hivemind/docs/research/2026-11-20-production-readiness/self-reference/RESULT.md:25)

## 2. One mechanism for both opening orders — Agree, with a separate acceptance case

A later item that opens total revenue can also propose that the existing Data Center question read it. That is within D191 point 2. A three-way matching choice can handle both opening orders without a second selection mechanism. Apply it to the final question identities, after matching decides which candidates actually open. The current writer accepts dependencies only from newly opened **readers**, so the second outcome requires a real write path for the existing reader, including queuing it that day. D368 item 2 still calls for the later addition to be designed and measured as its own slice. Shared code is compatible with that. [D191](/Users/lchingen/hivemind/docs/DECISIONS-log.md:2503) · [D368](/Users/lchingen/hivemind/docs/DECISIONS-log.md:3968) · [Matching check](/Users/lchingen/hivemind/src/hivemind/views/matching.py:332) · [Writer](/Users/lchingen/hivemind/src/hivemind/views/writing.py:175)

The candidate-based choice leaves out a later article that reveals a connection between **two already-open questions**. D191 permits that case too. The July test can exercise the existing-reader/new-target case. It cannot accept the full later-addition feature. [D191](/Users/lchingen/hivemind/docs/DECISIONS-log.md:2503) · [PRD 06](/Users/lchingen/hivemind/docs/prd/06-views.md:129)

## 3. Derive the ladder label from the sign — Agree for decidable numeric ladders

Ask the matcher whether a higher value in the read question pushes the reading question’s quantity higher or lower through the stated relationship. Code can then map that answer to the existing label using the read question’s high and low ends **and the reading asset question’s favourable end**. Higher company revenue and higher financing obligations can have different implications for the company. For a theme reader, map the sign through both ladders’ numeric order to `same` or `opposite`. Compute the label from the final stored order, after any successor reversal. [PRD 06](/Users/lchingen/hivemind/docs/prd/06-views.md:118) · [Ladder direction](/Users/lchingen/hivemind/src/hivemind/views/matching.py:72) · [Successor ordering](/Users/lchingen/hivemind/src/hivemind/views/writing.py:72)

Use typed bounds for the automatic mapping. `ladder_direction` can return `None` and can fall back to numbers in prose. The first version should require a defensible sign and a decidable mapping. A numerical ceiling alone gives no sign. If Alex wants that kind of link, he needs to choose how the product expresses it. [Ladder direction](/Users/lchingen/hivemind/src/hivemind/views/matching.py:72) · [Existing label vocabulary](/Users/lchingen/hivemind/src/hivemind/vocabulary.py:13)

## 4. Filing exposure in the product — Agree on 106, with a count correction

I independently counted **106 shared items out of 1,329 items linked to total revenue** in old-2. None of `e4061`, `e4097` or `e4348` is linked to Data Center. This strengthens the recommendation to keep chosen reading links out of D265’s removal rule.

The 106 are the **stored overlap exposed to the rule**. The exact loss requires replay. D265 filters incoming links against the day-start list, and the writer can also inherit links from earlier evidence when writing revisions. D538’s seven were observed removals after replaying the filing step. Use the same test on the product before claiming it would lose all 106. [Product count](/Users/lchingen/hivemind/docs/research/2026-11-20-production-readiness/dependency-design/claude-r1.md:10) · [D265](/Users/lchingen/hivemind/docs/DECISIONS-log.md:3084) · [Filing snapshot](/Users/lchingen/hivemind/src/hivemind/extraction.py:42) · [Revision links](/Users/lchingen/hivemind/src/hivemind/views/writing.py:255) · [D538 replay](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/dependency-selection/EDGE-PROOF-RESULT.md:35)

## 5. Carry both figures — Agree on delivery, disagree on the “market reference” label and shared root

Show **“Comparison point stated by the judgement for [read question]”** and **“System forecast for [read question]”**. Carry both stored values separately from the bounded reasons. The first label preserves the scope and attribution. It makes no claim that the comparison point came from the market. Old-1’s credit-support question explicitly said no aggregate consensus was supplied while carrying its own $10–11B base as a comparison point. An unqualified market label would upgrade it. The same risk exists in the reasons excerpt, so the $0 check should exercise both paths. Include a case where the comparison point changes while the forecast and rung stay fixed, since the reader may need that update. [Reference census](/Users/lchingen/hivemind/docs/research/2026-11-20-production-readiness/self-reference/reference-census.md:14) · [Stored judgement fields](/Users/lchingen/hivemind/src/hivemind/views/judging.py:234) · [Change rule](/Users/lchingen/hivemind/docs/DECISIONS-log.md:1265)

The defects meet at a missing input, then diverge. One judge can contradict another because it never sees the other forecast. A judge can also mislabel its own earlier estimate because the previous reasons are visible and their figures have no source mark. The link delivered $411B in the September probe, yet two of three linked answers kept the carried $414B. [Reference mechanism](/Users/lchingen/hivemind/docs/research/2026-11-20-production-readiness/self-reference/RESULT.md:25) · [Probe answers](/Users/lchingen/hivemind/docs/research/2026-11-20-production-readiness/dependency-probe/claude-marks.md:19)

## 6. Link first, measure the remaining reference defect — Agree

Open one judging version for the link. Bring the sourced-reference change to Alex separately after measuring what remains. The **33 of 44** are Data Center cases flagged by the strict census, not repairs demonstrated by a link. The census checks the first figure and whether it appears outside the previous conclusion. After linking, that figure could appear in another judgement’s text and clear the test while still originating inside the system. Read the source of the figure in the linked answer before calling a case repaired. [Trace and candidate fixes](/Users/lchingen/hivemind/docs/research/2026-11-20-production-readiness/self-reference/RESULT.md:44) · [Census implementation](/Users/lchingen/hivemind/docs/research/2026-11-20-production-readiness/self-reference/reference_census.py:68)

A future sourced-reference design can check that the cited ID was shown. A dependency ID by itself identifies another judgement. To support a claim about what the market expects, the amount must trace to a shown outside statement about the relevant quantity and period, or the answer must say no such reference was supplied. That distinction needs its own measurement. [PRD 06 on dependency conclusions](/Users/lchingen/hivemind/docs/prd/06-views.md:129) · [D260](/Users/lchingen/hivemind/docs/DECISIONS-log.md:3049)

## 7. First send and pass rule

**(a) Disagree with adding September to the first send.** July can test delivery of the $393B Bloomberg-compiled total-revenue estimate from `e195`. I checked the archived requests. Total revenue saw it on July 10–12. Data Center’s July 10 and 12 requests did not. July does not test whether an already-entrenched $414B figure is displaced. Price the July pair at **$0.06–$0.07 estimated** before retries. September 14–20 would add **about $0.36** at stored uncached token sizes for 84 judge calls. Even September 19–20 would add **about $0.10** for 24 calls. Those September prices cover a switch from a stored September state. Carrying the July link forward as a live sequence would require paying for affected intervening days as well. [Published rates used by replay](/Users/lchingen/hivemind/src/hivemind/model.py:26) · [September trace](/Users/lchingen/hivemind/docs/research/2026-11-20-production-readiness/self-reference/RESULT.md:44) · [Sequence requirement](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/dependency-selection/SEPARATION-DESIGN.md:285)

**(b) Agree on six fresh sequences and propose this rule now.** July 12 decides reconciliation. July 10–11 exercise selection and carry-forward and count toward the harm check. Two independent readers check the answers against the material available on their day.

| Mark | Rule |
|---|---|
| **A. Comparable answers** | Both July 12 answers give a FY2027 forecast in USD for their own quantity. Use the stated endpoints for ranges. Record quarters wherever both answers give comparable figures. A missing annual figure leaves reconciliation untested. |
| **B. Arithmetic and sources** | Reported figures retain their amount and scope. The arithmetic follows from the stated inputs within their rounding. Each assumption that materially sizes the result is disclosed and supported by the material available that day. Treat a linked calculation as a forecast with assumptions. |
| **C. Room for the rest** | The high end of the Data Center forecast leaves at least **$6B** below the low end of the company forecast. This conservative test floor comes from Q1 alone, about $81.6B total minus $75.25B Data Center. Each comparable quarter must also leave the segment within the company total. |
| **D. The link did work** | For a linked sequence to pass, matching must choose the intended link, the writer must commit it at the item, and Data Center must use the available total-revenue forecast in its calculation or as a stated bound. Record delivery and use of the $393B reference separately. A mention or citation alone earns no credit. |

**Pass** if at least two of three linked sequences meet A–D, at most one control meets A–C, and the linked arm introduces no first-attempt refusal or new material grounding error on either question across the window. Relabelling a system forecast as a market estimate, or treating $393B as a Data Center consensus, is a grounding error. **Inconclusive** if the control reconciles in at least two sequences, or missing annual figures leave fewer than two sequences comparable in either arm. **Fail** on a new material error, an added refusal, fewer than two correct link selections, or any other miss of the pass rule. Failures take precedence over an inconclusive comparison when they independently trigger one of those guards. [Earlier probe’s reading rule](/Users/lchingen/hivemind/docs/research/2026-11-20-production-readiness/dependency-probe/reading-rule.md:12)

## Decisions and work before the send

**The council can settle now**

- Specify one matching chooser and one writer contract for both opening orders, with separate acceptance cases. Settle the sign-to-label mapping, dated resolution, cycle correction, closing, theme presentation, citation and historical-reader rules from round 1.
- Register July as the sole first send. Use the reference trace as a grounding check and measure the remaining reference defect before designing its own version.

**Choices for Alex**

- **Approve the D265 interpretation.** I recommend that a chosen reading link leave evidence filing alone.
- **Open the frozen matching and judging versions.** I recommend authorizing both opening orders through the shared mechanism, with the July test explicitly accepting only the existing-reader/new-target case. Keep the full two-existing-question workflow for its own reviewed slice.
- **Authorize the bounded July comparison after the $0 proof.** I recommend the six sequences above. Bring the sourced-reference version back separately with evidence of what the link left unresolved. [D354](/Users/lchingen/hivemind/docs/DECISIONS-log.md:3685) · [D692](/Users/lchingen/hivemind/docs/DECISIONS-log.md:10398)

**$0 work, in order**

1. Complete the four design tables and audit the exact matching and judging requests. Fix the allowed endpoints, signs, labels and correction outcomes in writing.
2. Rebuild the July control by exact request identity. Replay the 106-item overlap through filing, keeping the known seven-link case and an unrelated pair as controls.
3. Exercise real matching checks and writing with fixed transport answers for both opening orders. Cover a cycle through a waiting link, a conflicting label, close and successor, one theme shown once, historical reads at the transition, and resume after a partial round.
4. Inspect the built July requests for the distinction between the $393B outside estimate and the forecast. Exercise the old-1 credit-support example and the reference-only change case. Freeze the reading rule and set the spending cap from the actual rebuilt requests before seeking send authorization.

**DISAGREE as written.** Keep the shared chooser, preserve separate acceptance for later addition, label the linked comparison point as the other judgement’s statement, and send July alone after the $0 proof.
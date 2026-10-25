# Two-step extraction: more content selected, end-to-end acceptance still fails

2026-10-25 · D162 · No default promotion. All six registered sequences completed: 45 fresh calls, estimated list-price cost **$0.6928525**, 454.7 seconds summed model-call time. Original prompts, inputs and raw answers remain frozen. The later request to switch the project to English did not change this comparison.

The split helped the model select the project cost, but it did not reliably turn that content into correctly linked, accurate evidence. For example, the third experimental sequence read the $500 billion cost correctly, then supplied an empty company field. The existing company check rejected the question, leaving all eight linked items unstored.

## Every sample

“Cost” means retained after the first article, not recovered later. “Risk” means Goldberg's substantive judgement is retained as third-party evidence. A generic statement that he is cautious is listed separately. These are assistant annotations checked against the original articles, not independent human gold.

| Sample | First cost selected / stored | Risk content stored | Ohio grouping | Additional result | Calls | Estimated cost |
|---|---|---|---|---|---:|---:|
| Control 1 | Yes / yes | Yes | Correct | Core criteria pass | 6 | $0.10618125 |
| Control 2 | No / no | Only generic caution | Correct | Cost recovered in article 2; substantive risk reasons omitted | 6 | $0.07932250 |
| Control 3 | No / no | Yes | Correct | Cost never recovered | 6 | $0.08658375 |
| Two-step 1 | Yes / yes | Yes | Correct | Wrong $30 billion translation; mixed-source item; one funding-risk item explicitly omitted | 9 | $0.12965000 |
| Two-step 2 | Yes / yes | Yes | Correct group, duplicate question | Code overruled a correct merge and stored the repeated report as new evidence | 9 | $0.16273625 |
| Two-step 3 | Yes / no | Yes, under the wrong group | Rubin chosen incorrectly | Empty object loses article 1; invalid quote loses article 2's guarantee statement; chip-financing amount never recovered | 9 | $0.12837875 |

The three experimental sequences do **not** meet the registered end-to-end bar. First-article cost selection is 3/3 versus control 1/3; first-article storage is 2/3 versus 1/3. Substantive risk content is stored in 3/3 versus 2/3, but in one experiment it belongs to a question incorrectly placed under Rubin. Correct group placement is 2/3 versus 3/3. These small samples are not population accuracy estimates.

The original O1–O6 labels are in `review-labels.json`: O1 first project preserved; O2 amount meanings preserved; O3 substantive risk reachable from that project; O4 article 2 adds a source for the same report; O5 project questions remain together; O6 no unrelated Rubin/SK membership. Article 3 duplicate handling and first-article cost are reported separately. A criterion whose required earlier item was lost is not counted as passed.

## Where content was lost or changed

The nine first-step calls selected **80 items**. The second step explicitly omitted **22**, forwarding 58. Original quote checking rejected one, leaving 57. The missing-company question caused eight more items to have no surviving destination. The database therefore received **49 source writes** from the experimental arm. All nine handoffs preserved exactly the selected text they forwarded; this proves the transport, not the quality of selection.

1. **The second step still treats some useful reasons as irrelevant to a narrow event question.** In `grouped-1/item1`, source e5 states that OpenAI is unprofitable and may struggle to fund its commitments. The organizer omits it because it does not directly describe signing the guarantee. The other two source calls also selected this concern; one organizer kept it successfully, and the other lost it with its invalid question. The split exposes the choice but does not repair the judgement.
2. **A valid group reference can still be the wrong group.** Of 11 raw candidates, two in `grouped-3` declare a new Ohio group t1 but cite existing Rubin g1 instead. One becomes a stored wrong membership; the other is rejected because its object is empty. The schema checks which identifiers exist, not whether the relation is true. There is one empty-object candidate among the 11.
3. **The event identity rule turns a review date into a different event.** In `grouped-2/item3`, the model correctly chooses existing v1. Its proposed review date is July 28, 2027, versus July 26 on v1. `identity.conflicts` treats the period difference as a conflict; `matching.check` changes “merge” into “new.” Both scopes are marked model-written, so the scope wording is not the refusing condition. A stored-data counterfactual changing only the candidate period makes the conflict disappear. The result is duplicate v3 and new WSJ evidence e19. This is the one merge-to-new override in the 18 inputs; the other changed outcome is the correct rejection of the empty object. Unlike the preceding comparison, this run actually exercised a later candidate merge.
4. **Correct quotes do not guarantee correct summaries.** Four outputs quote the same $30 billion equity-investment sentence. Three translate it correctly; `grouped-1/item2/source.json` e12 translates it as $3 billion. It is stored as database e15. The existing sift checks that the quote occurs in the article; it does not compare the summary's units with the quote. The second step faithfully preserves the error.
5. **The source item itself can contain multiple claims.** `grouped-1/item3` e3 combines the WSJ report and the Jefferies interpretation. Matching attaches the entire item to the existing WSJ evidence. The Jefferies interpretation has no separate source addition. Separately, `grouped-3/item2` e1 removes “(NVDA)” from within the original sentence, and the quote check correctly rejects it. No quotation rule was weakened to make the experiment pass.

Counts and the period counterfactual are recorded in `failure-census.json`. These findings do not authorize another paid arm or a new measurement standard.

## Cost and verification

The experimental arm used 27 calls versus 18, 110,300 input tokens versus 81,894, and 28,289 output tokens versus 16,972. Estimated cost was $0.420765 versus $0.2720875, about 55% more. Model-call time was 282.9 versus 171.8 seconds. Both selection and construction are included. Estimates use the repository's list prices, not an invoice or a claim about provider prompt-cache billing.

The two prompt texts total 2,596 characters versus the control's 2,409. The 187-character increase is the declared cost of separate responsibilities and the explicit handoff. `offline.json` records representative full-request sizes; actual request lengths and tokens are retained for every call. The archive rounds each call's estimated cost to six decimal places, producing a $0.0000005 total rounding difference from the transport ledger. The audit checks that formula rather than requiring falsely exact aggregate equality.

Free preflight replayed 315 historical extraction answers and 155 matching records with no changed refusal share. All 18 D161 answers survive the split conversion with their previous accepted content and previous single quote refusal unchanged. The 23 targeted tests passed. Scratch mutations that corrupt a quote or bypass a missing disposition fail the intended assertions. The final artifact audit verifies **10 stored memberships, 94 source writes, 17 previously stored member appearances, and nine two-step handoffs**. A corrupt-source scratch copy fails its explicit preservation assertion. History and resend checks pass in all six sequences.

The full-suite result and final documentation check are recorded in `verification.md` when complete. This is a developer experiment through extraction, matching and storage; it does not run judgement, UI, or a full cross-category acceptance.

## Consequence

Keep the split as an experiment, not the default. It gives better visibility and selected more of the important content in this case, but it is not the clean end-to-end fix. The next functional fix needs to distinguish an event's identity from the date we choose to review it; that rule currently defeats a correct model decision. Group-reference meaning, valid question ownership and summary accuracy remain open. Switching to English may remove a translation step, but this run provides no evidence that English alone fixes those defects.

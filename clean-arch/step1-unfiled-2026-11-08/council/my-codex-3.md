**The page is not ready for Alex: its recommendation favors the new system more strongly than the evidence supports, and its proposed acceptance test is not yet an acceptance design.**

The clearest example is “its open losses are one kind of work.” The new system also has missed questions, inaccurate source labels and an unfinished test of how it constructs answer choices. Fixing delivery alone would not resolve those problems.

**1. Numbers and claims**

- **“235 articles that no earlier run had read” is wrong.** The fresh-week record says 232 were never sent and three had appeared in earlier Step 1 tests. Say that explicitly. [Week result](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/week/WEEK-RESULT.md)
- **449 and 196 are links, not distinct statements.** One statement can be linked to more than one question. Say “links between statements and questions.”
- **“389 kept but read by no judgement” needs a time boundary.** The record counts statements with no question at the end of the week. Say “389 had no question at week’s end and were therefore not delivered through a question”; do not imply a separate audit proved that none appeared in any earlier request.
- **The cost row is a priced estimate, not the recorded bill.** Applying the current full input/output rates to archived tokens reproduces approximately $0.47 and $2.31. The archives’ recorded costs are lower because they reflect cached-token pricing; the new run’s ledger charged $2.52 under its reservation and settlement rules. Label the row “estimated model-token cost at current listed rates, before cache discounts,” and state whether failed attempts and embedding costs are included. The clean draw also ran **three answer-choice passes**, so this is the cost of the measured setup, not necessarily the cost of one operating pass.
- **D505 makes the financial-question difference relevant, but does not establish a winner.** “Not a point the old system wins by default” is fair if paired with the other side: excluding those questions also leaves no direct judgement on those numbers, which is a product consequence Alex can see. Do not recalculate D489 or treat 2 versus 1 on the remaining two matters as a new acceptance result.
- **“Nobody has read” the 278 discarded statements is too broad.** State only that this week did not establish how many harmed an answer. Earlier work did examine classes of production’s dropped facts. [Current state](/Users/lchingen/hivemind/docs/CURRENT_STATE.md)
- **The delivery paragraph mixes populations and units.** The census covered **567 kept statements**, including statements linked elsewhere, not just the 389 unlinked ones. Its findings were five statements representing **three fact–question pairs**, with **23 unresolved candidate statement–question pairs**. [Census](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/delivery-class/CLASS-CENSUS-RESULT.md)
- **“Changed nothing visible” overstates D511.** All six answers stayed “yes,” confidence readings overlapped, and the added fact was marked against “yes” in all three treatment answers and cited twice. The result was inconclusive. [Effect test](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/effect/EFFECT-TEST-RESULT.md)
- **“A statement read before a question existed is never placed under it later” is too broad.** One confirmed missing fact had previously been linked elsewhere. The record also reports a later-linking process that considered 516 earlier statements and linked two. The precise scope of that process matters; report the observed miss, not “never.” [Main-numbers result](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/main-numbers/RESULT.md)
- **“Not run since on anything but this week” is false.** The clean path also ran the 14-day comparison on November 13. Its answer-choice tests remained unpassed; the later comparison did not cure that. [Current state](/Users/lchingen/hivemind/docs/CURRENT_STATE.md)
- **“Same matching” is misleading.** The clean path has its own frozen search, comparison and grouping path. It shares the frozen judge; describe the matching paths as different. [Clean architecture](/Users/lchingen/hivemind/clean-arch/README.md)
- **Add the old system’s standing:** it is the current default with a frozen historical acceptance baseline, not proof of present production readiness or a head-to-head win on the new week. Add that the new system is not integrated with production storage.

**2. Recommendation**

I recommend **no system-selection recommendation yet**. The honest recommendation is: **keep production as the default and preserve both paths while preparing a fair comparison**. That is a recommendation for what to do now, not a claim that production is better.

The draft’s reasons for selecting clean do not support that selection:

- 6/7 versus 8–9/15 is useful evidence about this week’s question lists, but a small, partly overlapping product judgement—not a complete quality comparison.
- Keeping a statement makes it available for later inspection; it does not prove the system kept every relevant fact. Conversely, production’s discarded outputs are stored and can be inspected.
- Clean’s problems are not one kind of work. Its answer-choice step has not passed, and it has source and opening losses.
- Both systems contain frozen pieces. Saying only production needs new versions presents an asymmetric cost that the record does not establish.

**3. The proposed test**

The second week is **not wholly unseen**: c8 and c22 each read 40 selected articles in D499, against a constructed week-end library. That does not mean the model learned from those calls or the system changed, but the research team saw outputs and findings from those articles. Disclose the exposure, identify the 40 in the manifest, and do not call the whole week unseen. If independent unseen acceptance is required, select and check a new window rather than silently excluding inconvenient articles. [Record test](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/record-2/RECORD-TEST-2-RESULT.md)

The proposed test also changes the earlier design materially:

- Three clean draws versus one production draw can describe clean variability; it cannot compare variability fairly. If the purpose is choosing between systems, design matched draws or explicitly say the production draw is context only.
- With seven judgements, **90% requires 7/7**; with 15, it requires 14/15. Report counts and the per-draw rule, account for reader disagreement, and establish minimum exercised cases. Do not imply the proposed threshold is calibrated.
- “No kept fact … would change a judgement” is narrower than the PRD: it ignores facts never extracted and treats a reader’s prediction of a changed answer as established effect. The earlier design also proposed checking cited statements against articles; the draft drops that check. [Acceptance design](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/ACCEPTANCE-DESIGN.md)
- $7.50 plus $0.50 is a rough extrapolation, not a priced run or ceiling. Three times $2.31 plus $0.47 is **about $7.40** before allowances; article count, retries, caching, passes, and any unpriced calls can change it. Size the actual manifest and all components, then set a separate ceiling.

I would name **one reviewed comparison design** as the next test, not promise that the proposed week or thresholds are ready. Passing it would still not automatically waive the existing answer-choice acceptance requirements.

**4. Plain words and the trace**

Replace “placements” with “links to questions,” “last judgement” with “the latest answer to each question at week’s end,” and “reader families” with “two independent reviewing teams.” Explain that “from an empty start” means neither system began with existing questions. Replace “number cards” and “Stage B” with the product behavior being judged.

I agree that another full judgement trace is not justified merely to turn the known 25% case into a class. One **targeted $0 check** could still change a page line: verify the exact scope of later linking against the previously linked missing fact and the 516/2 record. Until then, remove the “never placed later” claim; the decision does not depend on asserting a mechanism.

**5. Remove these claims**

Remove “235 unseen,” “same matching,” “nobody has read” the discarded statements, “never placed under it later,” “changed nothing visible,” “only one kind of work,” “old losses are in frozen pieces” as a contrast, and “only this week since acceptance.” Remove the recommendation to select clean as though its merits are established, and do not call the proposed test an acceptance of unseen news.

Council position: Revise the page to recommend retaining the current default while a fair comparison is designed, not selecting either system; correct the evidence and exposure claims, preserve D489 and D505, and make no paid test or new acceptance claim until its inputs, controls, thresholds and cost are reviewed.
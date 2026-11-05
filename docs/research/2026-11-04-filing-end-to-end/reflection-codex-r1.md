**v74l failed because the reviews established that the instructions sounded defensible—not that the model would follow them. Claude’s explanation also overstates how much filing improved and misattributes the loss of new-question references.**

For example, one article lost all 20 references to a proposed Rubin Ultra question, yet almost all its evidence survived under the existing Rubin Ultra question. That is largely duplicate-question removal, not lost research.

1. **The deleted role sentence is a plausible contributor, not an established cause.**

   I reproduced 70 → 17 candidate-linked evidence entries and 20 → 9 surviving candidates—but those are **development-set counts**, despite the reflection labelling them as both sets. Across all 69 articles, the counts are 82 → 26 and 25 → 12.

   More importantly, counting references does not identify lost facts. Comparing each development control entry bearing a candidate link with all three variant answers, using source-text overlap, produces 210 comparisons: 105 find the fact linked to an existing question, 41 still find a candidate link, and 64 find no matching raw statement. These are repeated comparisons, not 210 independent observations.

   The clearest counterexample is article `c75f16…`: candidate-linked entries fall 20 → 0, but total raw entries fall only 20 → 19. Its candidate duplicates existing question v18; the variant files the facts there.

   Nor does the earlier experiment isolate the role sentence: **definition alone**, without role edits, already reduced candidate-linked entries 31 → 17. The later control itself rose to 70. Also, the saved `candidates` are proposals surviving extraction checks—not questions actually opened by matching. Claude cannot infer an opening regression of that size from this file. [Answers](docs/research/2026-11-04-filing-end-to-end/answers-links.json), [earlier experiment](docs/research/2026-11-04-filing-end-to-end/answers.json), [saving/filtering code](docs/research/2026-11-04-filing-end-to-end/resend_filing.py)

2. **“Filed more accurately” survives only as a narrower claim.**

   I reproduced the complete classification of gold-used facts, summed over three sends:

   | Outcome | Control | v74l |
   |---|---:|---:|
   | Reached a gold-used question | 224 | 230 |
   | Retained elsewhere | 59 | 36 |
   | Written but homeless | 12 | 19 |
   | Absent or refused | 71 | 81 |

   The fall of 23 wrong destinations is real, but **not 23 repaired deliveries**. Averaging every control/variant pairing within each fact, its decomposition is eight net wrong-to-right improvements and fifteen net movements from wrong destinations into absent/refused/homeless outcomes. Among comparisons where both answers retain the fact, correct destinations improve from 604/715 to 628/715—84.5% → 87.8%, under the existing matcher.

   There is genuine improvement, but deletion explains most of the smaller wrong-destination count. Calling this “the filing fix works” conceals that distinction. The development gain remains +7, p≈0.26; that establishes neither improvement nor equivalence to the earlier +9 draft. [Scorer](docs/research/2026-11-04-filing-end-to-end/measure_filing.py), [registered result](docs/research/2026-11-04-filing-end-to-end/decide-links.txt)

3. **The mechanism evidence is narrower than Claude’s narrative.**

   The rack-price failure is well supported: all three variant answers choose hyperscaler capex, and the follow-up explanation invokes the buyer-spending clause while rejecting product revenue because rack price is not revenue itself. The intended indirect reasoning did not displace literal matching.

   However, “six failures caused by keyword matching” is stronger than the evidence. The other cases show outputs consistent with that hypothesis; they do not provide six independent accounts of causation. Likewise, a prompted admission that Micron “should have been included” does not explain why it was omitted. Calling unexplained omissions “sampler” is not a diagnosis.

   The audit also says the rack error was “corrected when asked,” but the recorded answer still rejects the intended product-revenue destination. That is not correction. [Recorded explanations](docs/research/2026-11-04-filing-end-to-end/probe-links-account.md), [audit](docs/research/2026-11-04-filing-end-to-end/design-links.md:150)

4. **The process failure was predictable, not merely unfortunate.**

   The reviewers did useful work repairing contracts and measurement. But rounds six and seven explicitly reviewed the counting procedure; “seven rounds” should not be presented as seven validations of model behaviour. The decisive rack example received human reasoning and a hand-written passing answer, not a behavioural probe of the final instructions.

   Meanwhile, D355 had already recorded failure to supply unstated industry connections; D264 had already recorded suppressed candidate proposals when open questions became context. Those were known interaction risks. Bundling five relation classes, a tie rule, splitting instructions, fallback removal and role edits prevented attribution. The strongest empirical precursor remained the earlier draft’s insufficient +9 result. Predicting “pass” from readers’ intended interpretation was unjustified. [Design checks](docs/research/2026-11-04-filing-end-to-end/design-links.md), [review history](docs/research/2026-11-04-filing-end-to-end/log.md), [decisions](docs/DECISIONS.md)

**Structural root cause:** The system makes an uncertain, single-pass choice of a fact’s destination also determine whether that fact survives for judgement, while leaving the connection between indirect evidence and each question largely for the model to reconstruct.

5. **Of the three breakthroughs, C is the best hypothesis—but only after changing its proposed form.**

   | Candidate | Assessment |
   |---|---|
   | **A: separate writing and filing** | Separates retention from destination errors and has historical support in D207. But separate placement also failed on indirect relationships, and D264 explicitly replaced it. Reopening it requires Alex’s architectural decision. |
   | **B: question-centric filing** | Gives each question focused attention. It need not violate one-home storage if a final choice arbitrates competing destinations, but independent selectors would. A separate retrieval stage changes D264; scanning questions within one extraction call does not inherently do so. Neither version yet has decisive evidence. |
   | **C: enrich each question’s context** | Best aligned with Alex’s D264 instruction: “透过适当的Prompt 和引入已经开的题，和题的叙述来决定抽取”. It addresses D355’s missing connection while preserving one decision-maker. |

   **My recommendation is C as short causal explanations, not lists of names to match.**

   Each existing question would receive a versioned explanation of how indirect observations inform its answer, including limits. For custom-silicon spending: relevant suppliers’ sales provide evidence about customer purchases, but supplier revenue may include networking, different customers and different periods. For product revenue: price and shipments are inputs; whole-system cost is only partial evidence.

   Named companies and products may illustrate those relationships **only when independently sourced before the evaluated articles**, never selected from benchmark misses. The company-independent preparation procedure must preserve unexpected evidence, as D208 requires. Otherwise C merely turns v74l’s five keyword classes into company-specific keyword lists.

   This is promising because the model demonstrably handles concrete relationships better once the relevant material is present. It is unproven because broad wording was already available. Moving more prose beside a question could still fail.

   **Cheapest decisive test, after authorization:** prepare and freeze that context without consulting test answers; then resend six stored extraction requests, control versus context-only change, three times each. Include indirect spending, rack pricing, supplier economics, duplicate candidates, a long article and unrelated news. Use the frozen base; do not simultaneously remove fallback or edit roles. About 36 extraction calls should cost roughly five cents at the stored experiment’s rates.

   Require the preselected missing relationships to reach their intended questions in at least two of three sends, without losing their facts, existing correct destinations or unrelated candidate proposals. Repeated failure, success dependent on copying test-specific wording, or new name-driven false links refutes this version of C. A small pass justifies further testing, not acceptance.

   **Main risk:** an incomplete or wrong contextual explanation becomes a hidden gate. Separately storing it does not evade the freeze: enriching question descriptions exceeds this phase’s authorized links-only change and needs Alex’s explicit scope decision. [PRD constraints](docs/prd/10-filing-phase.md), [D208/D264/D355](docs/DECISIONS.md)

6. **Filing is a proven bottleneck for one question—not yet the dominant bottleneck for the phase.**

   The frozen runs agree with 15, 15 and 16 gold answers. Their reported denominator of 17 excludes two unjudged questions and the unopened Ohio question. Revenue already agrees in all three runs; cleaning its evidence pile has no demonstrated accuracy benefit in this window.

   Supplying missing facts to custom silicon changes all nine judgements, but **only three of nine then agree with reader B**, the frozen gold. The other six remain below its range. This proves evidence delivery matters; it does not prove delivery is sufficient.

   Operating margin and capex have zero linked evidence in all three stored runs, but no equivalent intervention establishes their response. The recorded question-dependency problem also limits what one-home improvements deliver downstream. Keep those limits visible; do not reopen judging, opening or the ruler without Alex. [Frozen results](docs/research/2026-11-01-e2e-loop/judgement-gold/score-r9-frozen-v108-d1.txt), [intervention results](docs/research/2026-11-04-filing-end-to-end/one-test-result.json)

No files edited; no model calls sent.
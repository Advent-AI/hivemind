**The phase should change its lever. More filing-rule prose is not justified by the remaining failures. First measure whether complete, source-faithful evidence lets the frozen judge answer operating margin and capex correctly.**

A concrete example: the extractor sometimes writes NVIDIA’s 66% operating margin and chooses the correct question, but invents the quotation’s wording. The code then rejects it. Better destination instructions cannot repair that failure.

**1. The remaining opportunity is small, specific, and split across different mechanisms.**

The frozen runs answer 15, 15 and 16 questions correctly. Their reported denominator of 17 excludes operating margin, capex and the unopened Ohio question. Twenty questions have answers in the frozen gold.

| Question | Verified bottleneck | Demonstrated upside |
|---|---|---|
| Custom silicon, q16 | Relevant supplier figures reach other questions; interpretation still differs after delivery | Supplying facts changes 9/9 answers, but only 3/9 agree with reader B |
| Operating margin, q10 | Omission, inaccurate quotations and missing delivery | No judgement in any frozen run; potential gain of one answer, unmeasured |
| NVIDIA capex, q12 | Cash-flow operands omitted or homeless; the judge must derive capex | No judgement in any frozen run; potential gain of one answer, unmeasured |

Thus fixing all three could **at most add three correct answers per run**, reaching 18, 18 and 19 out of twenty. That is an upper bound, not a forecast. China share and opening remain separate.

For q16, I verified i234 reaches v16 in all three v74l answers, versus v2/v2/v6 in the contemporary control. But the existing intervention supplied several facts, not i234 alone. Its 3/9 agreement cannot be attributed to this one routing improvement. Six answers remained below reader B’s range because they discounted the supplier figure for broader product coverage and timing. All three gold answers are low-confidence estimates; disagreement remains a gap against the frozen reference, but is not proof of broken arithmetic. [Intervention results](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/one-test-result.json)

**The new i163 account needs correction.** Across the six arms in the two answer files—18 responses to its article—the NVIDIA 66% claim is:

- Absent from eight raw answers.
- Written but rejected for quotation mismatch in five.
- Written with a valid quotation but homeless in two.
- Successfully delivered to v10 in three.

In particular, contemporary control send 2 and v74l send 1 both write the 66% claim, choose v10, and fail `quote not in item`. The source says “Micron’s operating margin … compared with Nvidia’s roughly 66 percent”; the answers manufacture “Nvidia’s operating margin was roughly 66 percent.”

`measure_filing.expressing` also matches Micron’s separate 84.6% statement to composite item i163. Therefore “i163 reached v5” does **not** establish delivery of NVIDIA’s operating margin. Its “v3” matches likewise need fact-level inspection. [Raw answers](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/answers-links.json), [earlier answers](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/answers.json), [matcher](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/measure_filing.py)

The i131 finding holds: never delivered in those arms; all six contemporary responses omit it. Also, i084’s **quoted gold span is net income**, although its meaning includes gross margin. The article’s actual 74.9% gross-margin statement reaches v3 in all six contemporary responses. Its route cannot be inferred from the net-income match.

The bottleneck is therefore **finding the necessary facts, preserving their source wording, delivering them, then making the inference**. Filing is one part. Cleaning the revenue pile has no demonstrated accuracy gain here: revenue already agrees in every frozen run.

**2. I withdraw C as the preferred next experiment.**

There is no direct evidence that question-specific causal prose would be followed more reliably than v74l’s generic causal prose. Moving instructions beside a question may help attention; that remains a hypothesis. It does not establish better writing or faithful quotations.

The historical evidence supports **providing suitable destinations**, not the stronger claim I made. Routing-analysis §11 added six driver questions to a **separate placer**, which received already-written statements:

- Correct placements rose from 9/9/10 to 16/15/13.
- Core placements rose from 6/6/7 to 9/9/9.
- Weekly statements admitted rose from 134 to 176.

But destinations and the reference mapping changed together. The experiment neither measured new extraction nor tested explanatory prose attached to today’s existing questions. Its inspected memory-cost placements also do not establish that a downstream margin judgement improved. [Original experiment](/Users/lchingen/hivemind/docs/research/2026-10-28-extraction-quality/routing-analysis.md:165)

D264 provides contrary evidence worth taking seriously: showing questions to extraction suppressed candidate proposals and coincided with more supporting facts being unwritten. Question context can steer attention away as well as toward. C might help, but currently has no demonstrated advantage on the largest unmeasured opportunity—q10 and q12.

**3. Removing the coupling is possible, but it requires an explicit architectural decision.**

A direct design would retain facts because they pass the standard’s evidence test, then let a reader focused on one question select relevant facts. Destination uncertainty would no longer erase valid evidence.

That is not automatically compatible with the existing decisions:

- **D207:** a single final destination can remain, but question-focused selections require resolving competing claims. Independent selectors do not themselves enforce one home.
- **D209:** permanently retaining evidence without a destination reverses the explicit no-home discard decision.
- **D264:** adding a separate selection decision departs from Alex’s chosen one-decider architecture.
- **D273:** the fallback mitigated the coupling by supplying a destination; it did not remove it.

A temporary extraction batch followed by placement could reduce premature omissions while retaining D209’s final discard. But that only postpones the coupling. It does not eliminate it. These distinctions require Alex’s decision, not implementation under a new name. [Decisions](/Users/lchingen/hivemind/docs/DECISIONS.md:2630)

Nor does this design guarantee faithful quotations or correct financial inference. We should not rebuild the architecture before measuring their downstream value.

**4. One recommendation, one test for Alex.**

**Recommendation:** change this phase from “improve filing wording” to “establish whether complete evidence fixes the unanswered financial questions.” Stop designing another extraction variant until that uncertainty is resolved.

**Test:** one bounded oracle experiment: q10 and q12 at the July 14 endpoint, **three sends each**, using one preselected frozen run.

Build requests with the frozen judge and production formatter. Supply the source passages cited by each gold answer, including counterevidence, with accurate attribution and surrounding context. Include the actual margin comparison and both cash-flow operands. Do **not** supply reader B’s reasoning, predicted range, or the capex calculation. Preserve the distinction between the reported margin and the question’s non-GAAP target.

Neither question has an archived judgement request: production skips questions with zero evidence, which I verified in all three ledgers. These must therefore be labelled **constructed endpoint requests**, not exact request replays. Their unchanged control outcome is already established: no judgement.

Read every answer. Require at least two of three for **each question** to agree with the frozen gold through source-supported reasoning. Failure on either question refutes the claim that perfect delivery alone reliably solves both. Success establishes downstream headroom; it does not validate C or any architecture.

**Cost:** six calls; roughly a six-cent budget at the repository’s recorded Luna rates, confirmed from the prepared requests before sending.

**Decision needed:** Alex must authorize this diagnostic after the failed-test stop and amend PRD 10’s filing-only scope. No frozen prompt or gold changes are needed. Any subsequent architecture change must separately reopen D209/D264; extraction or judgement changes require new versions under D274/D354.

No files edited; no model calls sent.
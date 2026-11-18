**I would run the $0 duplicate-question trace next.** The judge note correctly stops short of a send, but it needs corrections before it goes to Alex. I do **not** endorse “the council’s lean is B”: my earlier wording identified a possible choice, not a recommendation to show a label.

The two day-by-day tables match the stored answers I checked. One sentence after them is wrong: the July credit-support band also moved on **July 6**, from band 3 to band 5, when the $4.88 billion comparable arrived. The later move on July 14 followed the one-fifth discount. Say the two *disputed* movements on September 27 and July 14 coincided with newly introduced estimates; do not say they were the only band movements. [Stored-answer note](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/unsupported/DESIGN-NOTE.md)

The product options also need a more even presentation:

- **A** can keep an unsupported answer visible; it does not establish that the cost stays *mostly* in early days across the product.
- **B** is not yet shown to give a reliable label. A forecast can legitimately use a calculation or assumption, so a label could mislead or become routine.
- **C** should distinguish **no amount is sized** from **an estimate uses an unsupported step**. Withholding the band in the latter case is an additional choice, not necessarily implied by the former.

Remove “the council’s lean is B.” I have not reached that conclusion, and the keyword count cannot establish that B would work. It counts words such as “estimate” and “scaled,” not whether a labelled assumption is unsupported. It is a useful warning against treating every calculation as an error, not proof that a plain list cannot help a reader.

The decision **not to send** is right. The present code does not carry a new field into the next request, the proposed classification has not been shown to work, and the product behavior remains open. These are limits of the proposed design, not proof that no design could preserve provenance. Also, section 5’s “about 100 calls” is not supported by its own description: 36 failing answers plus an equal number of passing answers, two conditions and three sends each would be **432 calls**, before any exclusions or retries. Size a concrete selected set before quoting cost.

For the duplicate trace, I reproduced the link counts: `v14/v15` have 8 and 3 links with none shared; `v9/v11` 13 and 6 with 5 shared; `v3/v5` 47 and 43 with 19 shared. But **different record IDs do not prove different facts or missing facts in the actual judge request**. In the RTX pair, several records on both sides repeat reports about the same companies’ purchase plans. The second question opened after the first, and their latest answers are from different days. [Fresh-week comparison](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/side-by-side/SIDE-BY-SIDE-WEEK.md)

I would scope the next step to the **three pairs both teams marked duplicate in the fresh week**:

1. Compare each pair’s actual judgement requests at the relevant dates, not just its final link lists. Match repeated reports by the claim they convey, with source and time preserved.
2. Have two independent readers check whether a fact present for one answer was absent **in substance** from the other request and could bear on that question. Preserve differences in wording: for example, `v14` asks about Alibaba **and** ByteDance, whereas `v15` asks about domestic firms.
3. Read the answers and reasons for any concrete consequence. A reader saying a fact could matter does not establish that supplying it would have changed the answer.

**Stop:** if no distinct, answer-bearing fact is found missing from the relevant request, record that this reading found no delivery loss in these pairs. Do not conclude duplicates cost *only* clutter, or that agreeing answers prove the split had no effect. If a candidate is found, report it and its uncertainty before designing a change. July can supply earlier independently marked pairs where available; do not assume the frozen-reference matching provides a complete duplicate census.

One correction to the proposed cause: D354’s “about one in five” came from **one H200 collision request resent ten times**. It establishes that case’s variability, not that the three fresh-week pairs were split by the same mechanism or that one in five encounters generally duplicates. Trace those pairs before attributing their cause. [D354](/Users/lchingen/hivemind/docs/DECISIONS-log.md:3685)

I rank this trace first because it is unpaid and directly asks whether facts reach the answers a reader sees. I rank a judge-field proof below it until the product choice and provenance problem are resolved. I would not send a paid run now.

Council position: Correct the judge note and remove the unagreed lean toward B; keep the judge change unsent, and trace the three agreed duplicate pairs through their actual dated requests, stopping without a change if no distinct answer-bearing omission is established.
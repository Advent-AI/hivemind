# Phase 1, step 1: census of the judge's rejected answers ($0, read by Claude, 2026-11-20)

**Scope.** 49 answers in the 5 stored draws of the release comparison that the readers rejected or split, among questions rated worth
tracking (`rejected-answers.md`). The frozen judging-v7 gave all of them. Planted reader controls are excluded: they were filtered by the
deck key's role, `product` only.

## Two populations
| Group | Count | What it is |
|---|---|---|
| **Reader-threshold splits** (Claude supported, Codex insufficient) | 23 | Mostly deadline yes/no questions answered with the status quo ("still open", "not passed"). Codex asks for a base rate that the material does not hold; Claude accepts the status quo. This is the families' known threshold gap, not a judge fault agreed by both. **Not the target** |
| **Genuine splits** (supported against unsupported) | 2 | #13 France, #16 the Groq-licensed China chip |
| **Rejected by both readers** (unsupported or insufficient on both sides) | 24 | **The target** |

## The 24, by mechanism (one primary class each)
| Class | Count | Cases (number in `rejected-answers.md`) | Example |
|---|---|---|---|
| **O: adds amounts that overlap, or counts a factor twice** | 6 | 32, 40 (Grace's trailing revenue added to a "total CPU" outlook); 36, 45 ($18B added to a $25B balance that likely holds it); 44 (an above-consensus uplift stacked on an above-consensus run-rate); 47 (memory costs already inside guidance) | old-3 Q3: $446B revenue by stacking uplifts, where consensus and run-rate sit in rung 2 |
| **S: a figure that measures something else** | 6 | 31, 38, 49 (five companies' total capex and NVIDIA's own forecast for four companies' data-center capex); 28 (a cumulative investment estimate for an outstanding balance); 5 (a lease NVIDIA holds as lessee counted as a guarantee); 8 (a partner outside the question's four) | old-2 Q6: NVIDIA's $1.3T top-five forecast scaled by a 2026 share, against $1.08T consensus for five |
| **E: an estimate or adjustment with no basis** | 5 | 39 (+46% sequential Q4); 48 (an arbitrary trim to just below $40B); 4 (28% with no denominator); 17 (a sum $0.1B under a boundary, from approximate parts); 1 (one state, with none qualifying) | old-3 Q41: guidance points above $40B; trimmed to $38–39B on unquantified risk |
| **W: reports of talks taken as a likely completion** | 2 | 30, 42 | old-3 Q23: early-stage financing talks turn the status-quo "No" into "Yes" |
| **R: a rung's definition misapplied** | 2 | 12, 20 (rung 2 needs a formal decision after the opening date; the reported delay predates it) | new-2 Q5 Kyber |
| **M: too little material, default chosen** | 3 | 6, 15 (both readers: too thin); 11 (status quo against rich material) | — |

## What cuts across the classes
- **The answer leaves the reference's rung on a weak step of its own, in about 16 of 24.** The reference is the consensus, guidance or
  status quo that the judge itself names first. Cases: 5, 8, 12, 17, 20, 28, 30, 31, 32, 38, 40, 42, 44, 47, 48 and 49. The readers'
  rejections say, in effect, that the reference rung was right and the step off it is not justified.
- **The step lands just across a boundary in 7:** 5, 17, 32, 40, 44, 48 and 49. Examples are $24.9B against $25B, "just above $25B",
  "just above $1.1T" and $38–39B against $40B.
- **The step off is asymmetric.** The same answers refuse to move on unquantified downside ("does not quantify a reduction sufficient to
  cross"), yet move on unquantified upside (31, 38, 44, 49), and the reverse in 47 and 48.
- **On the 32 matters:** M08 (36, 45, 28) is O or S, and M14 (31, 38, 49) is S. Both are in the target's two largest classes.

## Not yet established (next step: mechanism)
- Which sentence of judging-v7 lets the answer leave the reference on its own arithmetic, and whether the request defines overlap,
  scope or the boundary.
- Whether the judge's own account names the same sentence.
- Whether a re-send gives the same answer. The judge is a sampler: the 24 are one draw each, though M08 and M14 recur across draws.

## Errors found while doing this
- My report to Alex on 2026-11-19 cited an old-2 answer that "chose $75–100B against its own estimate of about $53B". That card, C140,
  is a planted reader control. The real old-2 answer, C153, chose $50–75B and was rejected for overlap. Corrected in the merge test's
  `RESULT.md` and in `PLAN.md`.

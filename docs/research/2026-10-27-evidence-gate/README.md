# The evidence gate at extraction (2026-10-27, run paused at 2026-08-24 on Alex's instruction)

Alex: "做但是你深度思考怎么做法最好 … 和一个hedge fund analyst 的行为类似而不是积累大量杂音，你深度思考先尝试一下小范围是不是work，
我们先停止继续抽取".

## The audit of the request as the model reads it (`role-v12.txt`, what the run uses)

| line | said | effect | role-v15 |
|---|---|---|---|
| 1 | "Link statements and numbers that support or weaken an existing thesis" | fine | kept |
| 4 | "Every statement and number is, by default, evidence linked to a shown thesis. Use the existing theses first." | written against candidate sprawl, read as "keep everything" | "Use the existing theses first: a statement that bears on a shown thesis's answer is evidence to it, not a new question." |
| 6 | "a customer's deployment plan is evidence to the supplier's demand and product theses" | every deployment anecdote lands on the revenue thesis | "a customer's deployment, contract or purchase that carries a size is evidence to the supplier's thesis it bears on" |
| 9 | "Game releases, software features, tool/driver updates, promotions and individual peripherals are evidence for relevant theses." | names noise as evidence | removed (role-v14 had removed it too) |
| 23 | "Link evidence only to the thesis it directly concerns … Omit statements with no thesis to link to." | the only restraint, with no test of "concerns" | the analyst's definition: the quantity itself (reported, guided, estimated, for the period or a part of it), its drivers that carry a size (orders, backlog, contracts, capacity, ramps, supply limits, prices, share shifts, policy), facts that settle part of it; not technical performance, features, benchmarks, valuation arithmetic, share-price calls, power or cooling details, awards, deployments without a size |
| user block 5 | "[Existing theses …] Link evidence to them by id" | unchanged (code text shared by all versions) | unchanged |

Characters 7,458 → 7,893 (+435): the growth is the definition that was missing; the three sentences that said the opposite are gone.
A first wording ("only when it moves or holds the answer … large enough to move the answer", `role-v15-wording1.txt`,
`pinned-results-wording1.md`) over-pruned: it dropped a $104bn backlog, Q3 estimates and the Vera Rubin ramp, 11 of 16 cited
pieces. The second wording names the kinds in and out instead of asking the model to judge magnitude.

## Measurement (`samples.py`, `samples-wording2.md`; 7 stored articles, 3 samples per arm, $0.03)

Control = the unchanged stored request re-sent; arm = the same request with role-v15 as the system message. A stored piece
"cited" = some judgement of the run cited it.

| arm | pieces per article | cited pieces kept (of 17) | never-cited kept (of 51) | pieces on the revenue theses per article |
|---|---|---|---|---|
| control (role-v12) | 5.4 | 11.0 | 22.0 | 5.0 |
| arm (role-v15) | 3.3 (−39%) | 8.7 (79% of control) | 15.3 (70% of control) | 2.9 (−42%) |

Cited pieces the control keeps in some sample and the arm in none: "Reuters reported that the financial terms of Bristol Myers
Squibb's purchase were not disclosed" and "Google Cloud's first Vera Rubin A5X instance is running for Ineffable Intelligence":
neither is evidence for a revenue quantity. Pure-noise articles now answer with no evidence (Bristol Myers buying a system:
0, 0, 1 pieces).

## A finding the test exposed: extraction is a loud sampler

The same request re-sent gives 0 to 19 pieces for one article ([6, 8, 19] for a Rest of World piece; [0, 0, 4] for a 24/7 Wall
St piece; the stored run answer for the CoreWeave article had 8, five fresh sends 0, 0, 6, 3, 3). The stored run answers
averaged 9.7 pieces per article, fresh sends of the same requests 5.4. Settings: temperature 0.2, reasoning_effort low. Which
pieces the library holds depends on the draw. Not changed here; it is the next thing to measure (reasoning medium on the same
seven articles, three samples each, ≈ $0.05).

## Recommendation

Resume with `poc-v31` (role-v15, categories-v15, judging-v5): about 40% less new evidence per article, the judge's useful
material kept at four fifths of the control's own rate, the two consistent losses not evidence. Then measure reasoning_effort
medium on the same articles. Both are Alex's call; the run stays paused until he decides.

# The 630 statements the acceptance week threw away for having no home, read one by one (2026-10-28 evening)

Material: `thrown-away-v36b-week1.md` (numbered 1–630, grouped by article). Reader: the agent, as the analyst; the standard is
gold-standard.md (a statement is material when a judge of an NVDA question would cite it). Every number below is a count of my
own labels, ±1 on the arithmetic; no script decided a label.

| class | what it is | count | share |
|---|---|---|---|
| junk | bears on no NVDA question (consumer GPU prices, game drivers, supplier PR, the Singapore smuggling case ×4 articles, hires, robotics blogs, Hesai, Palantir) | 393 | 62% |
| admission miss | bears on a question this week's own articles raised and the run did not open: the AI Compute Partnership guarantees (~90) and H200/China permission (~6) | 96 | 15% |
| placement miss | bears on a question that WAS open in this ledger and the placer did not file it | 38 | 6% |
| no standing question | bears on a driver no article opens as a thesis: competition/China substitution (~55: Huawei capacity, DeepSeek chips, ASICs, AMD, Broadcom, survey), capital/obligations (~15: $119B supply commitments, debt raise, equity stakes, IREN contract), supply/memory (~10), demand (~10), pricing/product (~12) | 102 | 16% |

Statement numbers:
- admission miss, ACP: 5–14, 16, 17, 19, 20, 54, 55–58, 97–103, 150–152, 154–160, 161–166, 169–177, 216–223, 227, 228, 252–257,
  303–307, 312, 320–325, 328, 330, 331, 385, 386–388, 391, 394, 603, 604. H200/China: 136, 180, 181, 182, 193, 372.
- placement miss: 44, 137, 138, 139–144, 153, 240, 241, 247, 274, 277–281, 296, 352–354, 356, 381, 382, 384, 395, 396, 400–402, 422,
  425, 446, 447, 496, 626. Decisive among them (22): 138 ($1T Rubin+Blackwell orders through 2027 → revenue), 281 and 425 (SemiAnalysis
  H2 FY27 data-center compute 20% above consensus → DC revenue), 277–280, 384, 400–402, 422 (the Kyber delay story: NVL576, NVL72x2
  scrapped, no scale-up solution, CPO at Feynman, "roadmap intact" → Kyber), 241 ($20B CPU sales → CPU revenue), 247 and 382 (GM 74.9%
  → gross margin), 446, 447 (memory 25–30% of the VR200 rack BOM → memory share), 496 (Google 2026 capex $190B → 2026 capex),
  395, 396 (82%/41% growth → revenue), 137 (Vera Rubin in full production, ships 2026 → Rubin shipping), 153 (Meta $145B → capex).
  Marginal (10): the Valar/Utah statements 44, 139–144, 352–354.
- no standing question: 15, 82, 86, 104, 105, 107, 113, 167, 168, 178, 179, 183–192, 194, 229–231, 235, 297–302, 339, 341–348, 367,
  370, 373, 392, 393, 404, 405–414, 417, 418, 427, 445, 448, 475–483, 486–490, 492–495, 497, 563, 564, 568–571, 574, 575, 576–578,
  605, 606, 607, 621–625, 627, 628.
- everything else: junk.

What this says: throwing away is right for 62%. Of the 38% that is material, one question (ACP) alone is 14% of everything thrown
away, and it was lost because admission did not open it in this draw (the same article opened it in two of four sends across the
three runs). The placer's own misses are 6%, and 22 of the 38 are decisive; the driver layer (D208) would take 16%.

## Mechanisms behind the 236 material statements thrown away (checked on the ledger, $0 except five probes at a cent each)

Control for the checks: the dump's numbering was rebuilt and tested on three known cases (138 = fool.com, 277 = cnbc, 425 = tikr); a
placed capex statement was shown to carry v3 in its own placement request before the "home shown" test was trusted. (A first run of
both checks used the wrong numbering and was discarded; `results/ask_placer_week.json` holds only the rerun.)

| mechanism | statements | share of the material 236 | what fixes it |
|---|---|---|---|
| no standing question existed: ACP (96, the same request bytes sent in three runs proposed 1 / 2 / 0 candidates; where it opened, 52 and 79 pieces found that home), root quantities opened only days later (7: DC revenue, gross margin, CPU revenue, capex, Rubin shipping), drivers no article opens (102) | 205 | 87% | the library written once at coverage start: roots and drivers (D208 seeding); admission by a per-article coin flip cannot do this |
| the article that opens a question cannot file its own statements under it: the placer never sees the item's candidates, only the extraction's in-call c-links survive (138 $1T orders → total revenue; 277–280 the Kyber delay story → Kyber, all from the two opening articles) | 5 | 2% | show the item's candidates to the placer as homes, with takes lines from the candidate's key |
| the placer saw the home and left the statement out. Its own account on five: two "my mistake, vX was right" (425 the SemiAnalysis DC-revenue estimate, 402 CPO at Feynman); three "NVL72x2 is not identified as Kyber NVL144 or Rubin Ultra" (384, 400, 401: the takes line names the rack, the stopgap rack for the same scale-up is not in the group's aliases) | 10 | 4% | one arm on the takes line (the group's scope sentence is already shown; the aliases are the analyst's), measured on gold; the two self-admitted mistakes are the sampler |
| marginal (Valar/Utah context, duplicate quarter figures) | 16 | 7% | nothing |

The 393 junk statements were thrown away rightly, but the extractor wrote them and the placer read them: ~62% of extraction output
and placer input this week carried nothing. That is a cost, not a loss; it is the "傻逼观点" Alex named, and it is not touched here.

## Correction (Alex, 2026-10-28 night: "你这么粗暴的把这些都先写好那岂不是lookahead了")

The fix column above said "D208 seeding" for the 205 statements with no standing question. Writing the ACP question into a 07-01
seed after reading July's articles is lookahead; that recommendation is withdrawn. What the evidence supports without lookahead:
- The extractor rarely proposes: 7–10% of the week's sends propose any candidate in all three runs; the 12 ACP articles were sent 13,
  11 and 13 times and each run proposed an ACP question exactly once. In v36b that one proposal (mlq.ai, 07-03, "Did Nvidia take on
  binding obligations to rent back idle GPUs…") was dropped by the code check `due_day 2026-07-03 not after the item`: a question
  phrased about the past, refused as not a forecast. So the ACP loss is admission: one proposal per ~13 sends, single-shot, and that
  one killed by a check the request did not warn it about.
- A seed, if any, may hold only what was public before the start day (roots from the last 10-Q and call; driver classes as a fixed
  skeleton), written by the model from those documents and frozen, never by me after reading the period. It cannot hold an instance
  that the period's news creates; the ACP question is exactly such an instance, and every month brings one.

## The same read on the D210 week (`english-v37-nvda-1w-2026-10-28`, 705 drops, `results/dropped-v37-week1.md`)

Read one by one again, same standard. Counts are my labels, ±5.

| class | v36b (630) | v37 (705) | what changed |
|---|---|---|---|
| junk, thrown away rightly | 393 | ~470 | the same articles (Singapore ×6, DOOM ×2, Hesai, robotics blogs, Beersheva, hires); one page (aa.com.tr) is a world-news digest with nothing about NVIDIA at all |
| ACP statements with no home | 96 | ~33 | the question opened on 07-01 and holds 29 pieces, judged five times with an analyst's reasons; of the 33 left, ~8 are the opening article's own statements (the placer never sees the item's candidates), ~25 are retellings of the announcement without a size, which the narrow rule leaves out; the clear misses are the CoreWeave $6.3bn / Lambda $1.5bn precedents (167) and Sharon AI's six-year 8-K terms (115) |
| Kyber / Rubin Ultra delay story | 0 (v5 held 46) | ~56 | the one Kyber proposal of the week (the-decoder, 07-06) was in the item's FIRST send; the parallel day re-sent the item (its shown list had changed) and the second answer proposed nothing; the handover is the second answer. 34 of 98 items were re-sent this week and 9 candidates vanished this way (Kyber, gross margin ×2, operating margin, global AI capex, Ohio signing, …) |
| Valar reactor data centre | 0 (v1 held 23) | 41 | not opened this run; marginal either way |
| Rubin shipping, root-quantity figures the placer left out (the $1T order book, GM 74.9% ×2, SemiAnalysis DC revenue above consensus ×2, 82%/41% growth, Google $190bn and Meta $145bn capex) | 22 | ~18 | same classes as before |
| no standing question (China/H200 ~52, competition ~15, capital ~7, supply/memory ~12, demand ~5, product claims ~18) | 102 | ~100 | unchanged; the driver layer's share |

New theses this run that should not exist: "equity investment in Intel" (v1, $5bn, 2 pieces) and "equity investment in Verkada" (v3, undisclosed, 1 piece). The amended sentence inherits D184's list "a guarantee, financing, an equity stake, a purchase commitment" and now gives an equity stake an amount form; an analyst does not track either. Two of nine theses.

Mechanisms, by what fixes them:
1. **A re-send re-rolls admission** (Kyber and 8 others, ~60 statements): the parallel day's stale-request recompute replaces the first answer with a fresh sample and the first answer's candidates are discarded. The candidate decision is not stale (it does not depend on the shown list the way links do); a re-send should keep the union of proposed candidates, or admission should not be re-sampled at all.
2. **The placer never sees the item's own candidates** (ACP ~8, the $1T order book): show them as homes.
3. **Equity stakes open as amount questions** (2 theses): the amount form belongs to guarantees, backstops and purchase commitments, not to an equity stake; one word out of the list.
4. The narrow rule leaves sized-less retellings out (~25): acceptable; the judge did not need them.
5. The driver layer (~100) and the junk the extractor writes (~470 of 705, 67%): unchanged, not this slice.

## The same read on the D211 week (`english-v38-nvda-1w-2026-10-28`, 685 drops, `results/dropped-v38-week1.md`)

| class | v36b (630) | v37 (705) | v38 (685) |
|---|---|---|---|
| junk, thrown away rightly | 393 | ~470 | ~415 (+ Valar ~40 marginal) |
| a story with no page (admission) | ACP 96 | Kyber ~56 | **0**: ACP, Kyber, Rubin shipping, H200 and the capex aggregates all have pages |
| the placer left it out with a home shown | ~10 | ~10 | ~60: ACP ~20 (Sharon AI's 8-K terms, the SemiAnalysis lender economics, the buildout blog's own lines), Kyber ~24 (NVL576, NVL72x2, the four-die cut: the stopgap-not-named class, worse with three near-identical Kyber pages to choose among), root figures ~15 (Q2 guidance $91bn, the $20bn CPU figure, 82%/41% growth under a growth page that exists, SemiAnalysis's DC-revenue estimate ×2) |
| no standing question (China/competition ~62, supply/memory ~16, capital ~12, product/pricing ~17, demand ~6) | 102 | ~100 | ~113 |

Pages that should not exist, by my read: v3 and v7 (ACP, beside v1), v17 (Kyber shipment, beside v11/v13), v10 (revenue growth, beside v4);
v13 (Kyber by 2028) is a succession of v11 (by 2027) after the delay, which is the designed shape (D168). The match records say how they
opened: Jev scored v3 against v1 `same_quantity_or_event 0.63` and v7 `part_of 0.81`, and the collision judge answered
`distinct_question_same_matter` each time; v10 against v4 `same_matter_different_quantity 0.69`, no judge; v17 against v13
`same_quantity_or_event 0.41` and the judge let it open. With a ledger-blind extractor every article words the same question its own
way, and the judge's verdict `distinct_question_same_matter` opens a page for each wording. That verdict is the next mechanism
(D190's contract), not extraction's.

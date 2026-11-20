# Merge test result (D679), 2026-11-19

**Verdict, by the lines written before any send: the registered test did not pass.** It missed two lines (council e,
`council-e-codex.md`, consensus).
- **P2 missed on its second clause.** Both hybrid capex answers use total capex to answer a data-center capex question without naming it a
  proxy. The plan wrote that clause as a higher bar than old met, and old's answers miss it too. It is the frozen judge's behaviour, not
  something the merge's wiring added, but it is a miss.
- **V missed.** Both readers rejected the rebuilt control's v47 answer. Three re-sends of its 09-16 request (rungs 2, 1, 2) show that the
  request can give either answer. They cannot set the odds or rule out an effect of the reconstruction: the theme block and the
  previous-answer wording differ.

**What did hold:**
- P1, delivery: verified on all 4 primary questions in both draws.
- P3, talks stay talks: 2/2.
- P5: both readers support all 4 hybrid answers.
- P4 (diagnostic): 0 standalone NVIDIA-figure questions proposed.
- The capex answers' scope: no five-company or 2027 figure was taken as the four-company 2026 answer. This is P2's first clause.

**What it shows, and what it does not:**
- The wiring (c8 filing under the old questions) delivers the matters' statements to the judge. On the two Anthropic questions, which
  opened in the window, it carries the whole answer.
- It does not show that the merge answers better than the old system. Old's answers to these questions were already supported, and the
  capex band was already set by 09-06 history.

**Spend:** $2.13 of the $5 ledger.
- 140 c8 sends: about $1.75.
- Judging two arms × 2 draws, 98 calls: about $0.34.
- 15 noise re-sends: about $0.04.

**Closed** at that, per the council. No further sends.

## Answers at 09-20
| Draw / question | Old (archived) | Control (old evidence, rebuilt) | **Hybrid (c8 filing)** |
|---|---|---|---|
| old-2 v5: four hyperscalers' 2026 data-center capex | rung 4 ($700–800B), supported | rung 4, supported | **rung 4, supported** |
| old-2 v40: NVIDIA $10B Anthropic IPO anchor by 09-20 | No, supported | No, supported | **No, supported** |
| old-3 v6: same as v5 | rung 4, supported | rung 4, supported | **rung 4, supported** |
| old-3 v47: anchor agreed by 09-20 | No, supported | **Yes, unsupported** (both readers) | **No, supported** |
| old-3 v48: anchor agreed by 2027-03-14 (negative control) | rung 1, unsupported; worth split | rung 1, unsupported; worth split | rung 1; answer split (Codex unsupported, Claude supported) |

- **Readers:** Codex and Claude, blind under shuffled labels, with the comparison's card form and brief.
- **Their controls:** the 3 plants were marked unsupported and the 2 supported controls supported, by both readers. A repeated card
  (diagnostic C016 is the old v6 card) was marked the same.
- **All primary marks settled in round 0.** Two debate marks, both on v48's worth, stayed void: Codex's reasons went over the
  instrument's 40-word limit, which was left unchanged.

## The lines, read by Claude in the traces
| Line | Result | Evidence |
|---|---|---|
| P1 Delivery | 4/4 | The final requests of hybrid v5 and v6 carry c8's 09-14 Zacks item: "the four top hyperscalers … roughly $720 billion to $745 billion … 2026". Hybrid v40 and v47 carry c8's Reuters items: considering, or in advanced talks, on the $10B anchor (c8 tiered them `rumour`) |
| P2 No meaning drift | **Missed** on its second clause; held on its first | First clause held: "the nearly $800 billion … figures cover five companies, including Oracle, so they cannot be assigned in full to the four-company total". Second clause missed: total capex is used for data-center capex without being named a proxy. Old misses it the same way |
| P3 Talks stay talks | 2/2 | v40: "reports of talks, not a signed or completed investment". v47: "consideration, negotiations, or discussions—not a signed agreement … NVIDIA's separate existing investment agreement … does not establish an IPO anchor commitment" (c8 had filed that older filing item, and the judge did not take it) |
| P4 Opening rule (diagnostic) | 0 of 7 proposals | c8 proposed 7 theses on the 140 sends: DRAM ×3, H100 rental rate, AI-lab revenue run rate, Anthropic anchor ×2. None is a standalone NVIDIA financial figure. None was opened |
| P5 Supported answer | 4/4 | Both readers, round 0 |
| V Validity | **Missed**: 3/4 control cards supported; the reader controls pass | The control's v47 flipped to "Yes" on 09-16 and stayed there (below) |

## How much of each final answer rests on c8's filing (counted from the hybrid's final requests)
| Question | Items shown | From c8 (window) | From old history (to 09-06) | Older items in force not shown | Items cited | Cited from c8 |
|---|---|---|---|---|---|---|
| old-2 v5 capex | 46 | 26 | 20 | 123 | 20 | 7 |
| old-3 v6 capex | 43 | 27 | 16 | 113 | 13 | 5 |
| old-2 v40 Anthropic | 12 | 12 | 0 | 0 | 12 | 12 |
| old-3 v47 Anthropic | 7 | 7 | 0 | 0 | 7 | 7 |

- **The capex answers rest partly on old's history.** Rung 4 was reached before 09-06. On capex the test shows that c8's filing added the
  latest four-company estimate without breaking the answer or drifting its scope.
- **The two Anthropic questions opened in the window, and their answers rest wholly on c8's filing.** They are the cleanest evidence that
  the wiring works.

## The V exception, traced ($0.04 of re-sends)
- **The final requests are stable.** Each arm's final v47 request, re-sent 3 times unchanged, gives its own answer 3/3: old No, control
  Yes, hybrid No.
- **The fork is 09-16.**
  - The control's 09-16 request, re-sent 3 times, gives rungs 2, 1, 2.
  - Old's 09-16 request gives 2, 2, 2.
  - The two requests differ only in the theme block (other questions held at 09-06 in the copy) and in the wording of the previous
    conclusion. Their evidence is identical.
- **Reading (council e).** The request can give either answer, and the previous conclusion then carried the control's "Yes" forward.
  Three sends neither set the odds nor rule out a reconstruction effect, since the theme block and the previous wording differ. V stays
  missed.
- **It does show that v47 is sampler-sensitive:** one draw of the hybrid's "No" is not proof that the hybrid is more stable there.

## Evidence cleanliness (descriptive, one draw: old-2 v5's window material, read by Claude)
| Window material, 09-07..09-20 | Old (23 items) | Hybrid (26 items) |
|---|---|---|
| Direct: the four companies, or one of them, on 2026 capex | 2 | 3–4 |
| Adjacent and useful: leases, cloud backlog | 0 | 4 |
| Five-company totals (context, other scope) | 8 | 8 |
| Unclear period | 1 | 1 |
| Off-question | 12 (4 on AI-lab safety) | 9 (Western Digital results, AI-lab revenue, PwC to 2050) |

c8 also links loosely: the merge cleans this pile only slightly. Step 2–3 grouping was not run.

## What this decides, and what it does not
- **Decided:** wiring c8 under the old questions delivers the matters' decisive statements to the judge, with no five-company or 2027
  figure taken as the answer. Both readers support the hybrid answers on M04 and M17, as they support old's. The registered test still
  did not pass: P2's proxy clause and V missed.
- **Not decided:**
  - whether the merge serves *more* matters: the new-only matters need the clean opener;
  - Steps 2–3 grouping;
  - the other 30 matters;
  - cost.
- **Cost, priced from tokens.** The merge pays the old pipeline plus c8 reading: about $0.0125 per article at $1.75 / 140. Over the
  82-day window's 1,884 articles that is about $24 on top of old's about $9.
- **The sampler-sensitive v47 question needs more than one draw** before stability is claimed.

## Errors of mine in this test (logged)
- **I read the census article numbers as positions in `kept-articles.json`.** They are numbers in `census/numbering.json`. Codex caught it
  in round c. My first claim, that old filed none of the census articles, was wrong: 8 of 11 reached the old questions.
- **The first article list included custom-chip and DRAM theses** as "capex" (the same misreading in PATH-TO-PASS's census C, to be
  re-checked).
- **The first judging copy failed.** The store's append-only triggers refused the cut; Codex found it in round d before any send.

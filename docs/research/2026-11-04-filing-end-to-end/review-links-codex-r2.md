**Serious issues remain. Draft 2 resolves the main coverage and role conflicts from round 1, but it still leaves the known rack-price choice unsettled and reuses a retired configuration name.**

For example, the $7.8 million rack-price estimate fits both the new price-to-revenue category and the buyer-spending category. The instruction to choose the “narrowest” question does not choose between them.

1. **The two-sided filing problem was removed from the text, rather than resolved.**  
   [The exact rule](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/links-v74l.json:4) permits the rack price under both Blackwell/Rubin revenue (`v20`) and hyperscaler spending (`v4`). Neither question is simply a broader version of the other. “Compare the specific questions before a company-wide revenue or margin question” does not distinguish these two specific questions.

   [Design §2.3](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/design-links.md:39) drops the two-sided instruction to preserve D207. That removes its ambiguous wording, but leaves [PRD §5.2](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md:82) unanswered. The model can still make the previously observed move from product revenue to buyer spending while following the new categories.

   This needs a settled instruction consistent with the governing decision. I am not treating category order as an unstated priority.

2. **The configuration-name finding remains unresolved.**  
   [Design line 4](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/design-links.md:4) says `poc-v112` was never used. It already identifies the retired v74i configuration with `reasoning_effort: max` and a 32,000-token output budget. I verified its contents directly in the retirement archive; its hash is in [the manifest](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/retired-2026-11-03/manifest-sha256.txt:51). Reusing it would give two different experiments the same identity, contrary to AGENTS §3.

The other substantive round-1 findings are resolved: all three conflicting role sentences change; the explicit comparison instruction returns; costs, accounting inputs, backlog and market forecasts now have routes; the audit correctly distinguishes abstract guidance from missing guidance and acknowledges the D273 reversal. Every category now has at least two examples. I found no further serious coverage gap in the five categories against the requested standard, decisions and frozen closing check.

I opened the database read-only and read extraction calls **370, 204 and 212**, including their articles, complete request instructions and raw answers. Their role and closing-check texts match frozen v74i. These destinations are my reading of draft 2, **not model-test results**.

| Broadcom article — call 370 | Destination under draft 2 |
|---|---|
| Kyber delayed from 2027 to 2028; NVIDIA’s denial; PCB manufacturing obstacle | Rubin Ultra shipment, `v18` |
| NVL576 likely delayed or limited to initial volumes | `v18`, as a related configuration |
| Q1 Data Center revenue | Data Center revenue, `v2`, if retained as an optional retold actual |
| Lisa Su’s customer forecasts exceeding expectations | Accelerator share, `v6`, through competition |
| Broadcom’s $10.8 billion revenue and $16 billion guidance | Custom-silicon spending, `v16`; inputs to an estimate, not identical spending totals |
| ASIC-market growth forecast through 2033 | `v16`, through the market-forecast category; preserve its different measure and horizon |
| Google Cloud revenue and backlog | Hyperscaler spending, `v4`, through demand behind spending |
| Google’s 2026 capex guidance | `v4` |
| NVIDIA “still” holding 81% | The unchanged common-knowledge check rejects this familiar-position restatement; if independently retained, its destination is `v6` |
| Stock moves, generic competitive-window commentary, specifications alone, biography and unrelated preview | Rejected by the unchanged closing check |
| Optional market-cap/valuation details | No suitable shown question; no automatic revenue fallback |

| Morgan Stanley article — call 204 | Destination under draft 2 |
|---|---|
| $7.8 million rack price versus approximately $4 million previously | **Unsettled: `v20` versus `v4`**, as described above |
| $55,000 Rubin GPU price | Blackwell/Rubin revenue, `v20` |
| $5,000 Vera CPU price | Vera revenue, `v19`, as a pricing input. The stored answer combines both prices; a single-home instruction still leaves that combined record’s destination unsettled |
| $2 million memory content, its increase, and changing bill-of-materials shares | Gross margin, `v3`, through input costs; these are not themselves contract-memory-price measurements |
| Q3 shipments and Q4 volume ramp | Rubin shipment, `v7` |
| Rising contract DDR5 prices | Memory prices, `v5`; preserve the reported period |
| Self-sourcing memory reducing rack price to $6.7 million | The same unresolved `v20`/`v4` choice. This statement was absent from the stored answer |
| Generic budgeting advice, performance praise, marketing and unrelated previews | Rejected by the unchanged closing check |

| Kyber-delay article — call 212 | Destination under draft 2 |
|---|---|
| Delay to 2028 and defective PCB manufacturing | `v18` |
| Scrapped NVL72x2 and customer objections to its form factor | `v18`, as a stopgap and its cancellation |
| Four-die Rubin Ultra cancelled; smaller version remains | `v18`, as a configuration change |
| CPO-NVSwitch postponed until Feynman; resulting lack of a proven large-system connection | `v18`, through the key-part and schedule-change category |
| More Oberon-Rubin racks planned to compensate | `v18`, as the replacement plan; revenue implications do not justify adding a broader revenue question |
| Supplier stock declines and prior gains | Rejected |
| Profit-taking explanations and general “competitors gain room” commentary | Rejected where they add no new fact or calculation |

The expanded categories address the earlier indirect-relevance omissions. **The remaining behavioral blocker is choosing between distinct valid destinations without silently abandoning either D207 or PRD §5.2.** No files were edited and no model calls were sent.
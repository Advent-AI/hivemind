The design should change before its test. It targets the proven problem, but the proposed closed list leaves valid indirect relationships unclear, and the role edit does not fully remove the conflicting instruction.

For example, the rule explains how Broadcom’s sales can inform buyers’ spending. It does not clearly explain how the stored article’s rising memory costs should inform NVIDIA’s gross margin.

1. Serious: the five categories are not a complete replacement for the standard’s rule.

The proposed text says: “A statement bears on a question in one of these ways.”

That makes the list exhaustive. But category (3) permits “a price or volume of a product, for that product’s revenue question,” while category (5) requires “a named customer’s, supplier’s or competitor’s move.”

The Morgan Stanley request contains: “memory content per rack at about $2 million, a 435% jump.” Its relationship to NVIDIA’s gross margin is through input costs. It is neither the margin’s own figure, a product price assigned to its revenue question, nor clearly a named supplier’s action.

The frozen closing check expressly recognizes “a supplier’s capacity, output, prices or revenue on supply and input costs.” D259 also permits evidence behind a figure, rather than only that figure itself.

This is a reverse-direction audit failure: individual examples have sources, but the replacement does not clearly preserve everything those sources permit. The same uncertainty affects costs informing operating margin, customer backlog informing capital spending, and accounting figures from which another quantity can be derived.

Before testing, the categories need to cover these relationships without requiring the statement to name the answer’s own quantity.

2. Serious: the role still gives the takes lines authority over filing.

The edit removes “the narrowest open question whose takes line covers it,” but retains:

“each with its takes line, which says what belongs in that question’s file”

and:

“A takes line says where a material statement goes”.

Meanwhile, the stored numeric line still says:

“takes: gross_margin figures, guidance, estimates and revisions…”

A literal reader can therefore continue rejecting a cost figure because it is not a gross-margin figure. Removing one occurrence helps, but the design’s claim that “the rule is stated once, in the field” is not yet true.

There is also an unlisted deletion. The old field says:

“compare the specific questions before a company-wide revenue or margin question”.

The replacement retains “narrowest” and a prohibition on broader same-company links, but removes that explicit comparison procedure. This should appear in the audit, because it concerns the very choice that failed.

3. Serious: the two-sided exception is justified as a proposal, but its instructions remain ambiguous.

The proposed instruction is:

“file it under the question about the party it describes, and also under the other side’s question when that is open”.

Neither stored request contains a Broadcom revenue question. The useful destination is the buyers’ aggregate custom-silicon spending question. The text should not leave the reader wondering whether an unavailable seller-side question is a prerequisite.

Similarly, the Morgan Stanley article describes NVIDIA’s rack price, while the buyer-side question covers aggregate hyperscaler capital spending. The rule needs to work explicitly with such aggregate questions, rather than implying two individual counterparties with matching questions.

Yes, allowing a second home departs from D207’s “one home, the narrowest question.” D355’s failed “one fact, two uses” test does not authorize that departure. PRD §5 explicitly asks for the two-sided design, so proposing it is within this phase. The design is right to identify the D207 exception for Alex’s decision; it should not present it as already settled by the standard.

4. The audit overstates “missing” and blurs a deliberate reversal with a contradiction.

Design §1 says:

“nothing in the request says where such a statement goes: missing for filing.”

That is inaccurate. The frozen links field already permits filing “through the demand, supply, competition or pricing behind its answer.” The closing check also says the analyst supplies the connection.

The missing part is a concrete explanation the model reliably applies. The existing rule is abstract and conflicts with the takes-line reading; filing instructions are not absent.

Likewise, deleting the fallback returns to the standard’s no-home rule, but D273 deliberately introduced that fallback and D274 froze it. The audit should describe this as the PRD-authorized removal of that later exception, rather than making D273 disappear behind “contradicts §6.”

5. Before implementation, the design needs the remaining contract checks.

AGENTS §2 requires the changed value’s readers and the new path’s existing checks. Design §5 identifies one important interaction, but does not cover the full path already present in extraction.py:

“a candidate left with none of its evidence is dropped too”

and:

“the same sentence read out twice is one piece with both links”.

Those matter when changing filing and permitting additional links. The design should cover valid open links, candidate-only links, rejected candidates, duplicate quotes, pruning, and eventual no-home removal.

The character counts are correct: links 1,226 → 2,079; role 11,028 → 10,943; net +768. Prompt-token counts required by AGENTS §6 are absent.

Clause-by-clause result

- “decided after you have decided it is evidence”: consistent with the standard’s separation of keeping and filing, subject to the existing no-home drop.
- “narrowest open question … makes more or less likely”: sourced by §5.1, D207 and D265.
- (1), own figure, step or estimate: sourced. The lender example is appropriate.
- (2), the other side’s sales or orders: a reasonable explanation of demand and supply under §5.1 and D259. It permits a relationship, not equality between differently timed or scoped totals.
- (3), price or volume informing product revenue: sourced, but too narrow as the list’s only explicit price route.
- (4), variants, stopgaps, parts and schedules informing an event: sourced by D259 and the product-progress boundary. The phone example states the relevant connection.
- (5), named customer, supplier or competitor moves: valid examples, but not a complete substitute for the broader permitted relationships. Partners and input-cost figures are particularly unclear.
- Both sides of a sale: the acknowledged D207 departure; ambiguity described above.
- “never a broader question of the same company”: preserves part of the old restriction. The removed explicit comparison instruction needs auditing separately.
- Shared company, industry, event or ecosystem is insufficient: consistent with D250.
- Alternate names and variants count: consistent with the frozen request and event takes lines.
- Speaker, missing period, basis or amount do not automatically exclude: consistent with §5.2 and D259.
- Another period or population: preserves the frozen wording. D248 supports the fiscal/calendar case; D268 supports the wider existing allowance. It does not make different quantities interchangeable.
- Candidate links and empty links: consistent with D264 and D209, including the code’s later removal of invalid candidate links.
- Role shortening: sensible direction, but incomplete because the two retained sentences still define takes lines as the filing authority.

Thus the forward audit mostly holds; the reverse audit does not yet hold.

Reading the two stored requests

I opened archive.sqlite read-only. These are calls 370 and 204. Their stored system text and links descriptions match the frozen files. The destinations below are my reading of the proposed rule, not model-test results.

Broadcom article, call 370

- Kyber delay from 2027 to 2028 → Rubin Ultra shipping, v18.
- NVIDIA’s “roadmap is intact” denial → v18.
- The PCB manufacturing difficulty identified as the delay’s cause → v18.
- NVL576 “likely delayed or limited to small initial volumes” → v18 through the sibling/variant relationship. The stored answer wrote this with empty links.
- Q1 Data Center revenue → v2, if retained under the unchanged rule for retold actual figures.
- Lisa Su’s customer forecasts exceeding expectations → NVIDIA accelerator share, v6, through competition. The stored answer used total revenue, v1.
- Broadcom’s $10.8 billion revenue and $16 billion guidance → custom-silicon spending, v16, as supplier-side evidence. These are inputs to an estimate, not identical measurements of calendar-year ASIC spending. The stored answer used v1 for both.
- Bloomberg Intelligence’s “27% CAGR … through 2033” → potentially supporting evidence for v16. The new list does not clearly explain this different-measure, long-range forecast relationship. The existing period allowance alone does not resolve it.
- Google Cloud revenue and backlog → potentially v4 through demand behind infrastructure spending. This is not the opposite side of the same capital purchases: Google is selling cloud services. Category (5)’s “move” leaves the route uncertain.
- Google’s 2026 capex guidance → v4 directly.
- NVIDIA’s approximately 81% share → v6 if retained; the unchanged common-knowledge check still decides whether this restatement belongs.
- Share-price moves, general “competitive window” commentary, specifications without business significance, and author biography remain subject to the unchanged rejection rules.

The rule clearly helps Broadcom and NVL576. It does not yet give equally clear treatment to Google’s backlog or the market-growth forecast.

Morgan Stanley article, call 204

- $7.8 million rack-price estimate → Blackwell/Rubin revenue, v20, through price. Under the proposed exception, it can also inform hyperscaler capex, v4.
- $55,000 Rubin GPU price → v20.
- $5,000 Vera CPU price → standalone Vera revenue, v19. The stored answer combined both prices and linked only v20. The design should address two distinct seller-side quantities, not assume every multiple-destination case is a two-sided sale.
- $2 million memory content and its increase → gross margin, v3, through input costs. The proposed exhaustive list leaves this route unclear.
- Q3 first shipments and Q4 volume ramp → Rubin shipping, v7.
- Memory’s rising bill-of-materials share and GPU’s falling share → v3, with their actual meaning preserved. Again, the new categories do not clearly say this.
- Rising contract DDR5 prices → memory prices, v5. The unchanged allowance handles a different period, but the list still needs to explain related input-price evidence.
- Self-sourcing memory reducing the rack price to approximately $6.7 million → v20 and potentially v4 under the proposed exception. The original answer did not write this statement, so filing changes alone cannot guarantee its recovery.
- Generic budgeting advice, performance praise, marketing material and unrelated article previews remain outside the evidence list.

One useful boundary: higher rack prices do not, by themselves, establish higher aggregate capex. They can inform that question; volumes and other spending still matter.

Generality

The examples use ordinary relationships across lending, pharmaceuticals, aviation, cars and phones. None names NVIDIA, its products, a test-party name or a test number. I found no direct bench-specific example.

The generality problem is coverage: the categories explain the observed sales/spending and product-launch cases better than costs, margins and other indirect relationships.

Also, classes (1), (4) and (5) each have only one example. That falls short of AGENTS §6’s “two or three examples per class.”

Additional predicted effects beyond design §5

- Useful input-cost evidence could lose its home because the new list is narrower than the old general relationship rule.
- One fact could cause additional questions to be judged, increasing downstream work even if extraction size barely changes.
- Candidate retention can change when evidence loses its last valid link; the code explicitly couples these outcomes.
- “Use only this item’s information” remains alongside “you supply the connection as the analyst.” This need not conflict, but the intended distinction matters: infer relevance without inventing source facts.
- The proposed v74k and poc-v111 identifiers were already used and retired, according to D274. Reusing them would conflict with AGENTS §3’s identity rule; choose unused identifiers before building.

My recommendation is to revise this one design before testing: preserve the full range of permitted indirect relationships, make the schema’s authority unambiguous, and finish the two-sided exception’s contract. No files were edited and no model calls were sent.
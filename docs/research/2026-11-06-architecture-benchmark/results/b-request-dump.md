# The whole B request as the model reads it (window draw 1, item gnews:3df0bbc8aff2c1d008bc0a32)

## System

You are a senior investment-research analyst. Read the whole article and the questions supplied from immediately before the item. Your task is to find article statements that help answer an existing question. Return evidence only; a separate call discovers new questions.

Research judgment
Read as an analyst following the company, not as a collector of financial lines. Ask what the article adds to the business and which research answer it could change: revenue, profitability, cash or credit risk, or competitive position. A customer, supplier, competitor, partner, regulator or economy can affect an answer through demand, supply, competition or pricing. Judge that connection from the supplied material and the question; shared names or an ecosystem alone do not establish it.

Distinguish the source's statement from the analyst's inference; do not invent missing context. Uncertainty, indirect relevance, missing detail or a quarterly period alone do not disqualify evidence; apply the closing check.

Find evidence for existing questions
Walk the article from beginning to end. Identify each research matter and what the source actually says, including who made the statement, its period, conditions and uncertainty. Consider both supporting and opposing information, including logically connected indirect drivers. A forecast or claim is not an achieved result.

For each matter, compare the exact question, subject, period and any accounting basis shown. A relevant quarterly actual or forecast can inform an annual question; different accounting bases are not the same figure, but may still inform a question through a clear connection. Use the schema's link-field rules to select the narrowest applicable supplied question. Do not infer that two named programmes are identical merely because they are similar. Do not invent an ID or force an unrelated link. When no supplied question is connected, leave links empty; do not create a question. The later matching step decides whether a source statement repeats stored evidence; the existence of a question does not establish that its evidence is already known.

Evidence: what to keep
Keep every statement an analyst would note that passes the closing check: if eight pass, return eight. Fitting a type below is not sufficient on its own.

Statements often take four forms:
1. The company's own figure, guidance or decision: quarterly same-store sales rose 4.2%; management guided full-year revenue to $12–13 billion; the board approved a $10 billion buyback.
2. A customer, supplier, competitor or partner's action or published figure with a name, date or size that bears on demand, supply, costs, competition, pricing or products: a bank selected a rival's system; a software firm is integrating the company's model; the largest customer plans to cut orders by a fifth. A new step may be taken, decided, planned or under way. A passage that only describes an existing use or arrangement and its benefits, without a new step, is background; the party's own revenue, capacity, orders or contracted amounts are figures to assess under this type. The closing check sets the boundary for newly reported steps and still-effective guidance, forecasts and plans.
3. A named party's claim or estimate about the company or its industry, with or without a figure: a CFO says decade-old plants still run at full capacity; an analyst raises next-year EPS estimates; an analyst says loan losses will exceed consensus. Preserve the identity and nature of the claim.
4. A policy or regulatory decision or step, including one still in force: the regulator approved a drug for a second indication; a government requires export licences; a regulator still bars sales of a drug in a country.

How to write evidence
- One evidence item records one statement, and that statement is what you judge: a figure, date or comparison in the neighbouring words does not make another claim in the same quote new or material. Copy its quote verbatim, without translation. Separately write a standalone summary in one_line: who did or said what, how much and for which period, naming the measure even when a neighbouring sentence gives it.
- Identify the speaker and, for a retelling, the original speaker and statement day. Use the schema's tier: fact for official actions, published actual figures or completed transactions; party_statement for company guidance, management statements or officials' remarks; third_party_view for analyst, media or expert opinions; rumour for claims the item credits to unnamed sources, calls unconfirmed, or that have no source and fit no other tier. An announcement or completed deal is a fact when the reporter names no source but does not call it unconfirmed or attribute it to unnamed sources.
- A record mixing a confirmed main fact and an unconfirmed secondary detail follows the main statement's tier; label the secondary detail as unconfirmed. Keep a market consensus distinct from the company's own forecast. Use only this item's information. Report plans as plans; do not infer committed funding, orders, deliveries or revenue.


## User

[Category and how to read it] T8. Opinion and analysis: sell-side or independent research, commentary and personal posts. The author's opinions and estimates are third-party views, not facts; quoted company statements are party statements.

[Subjects] The objects this item concerns: NVDA. Theme identifiers:
  - chip-export-controls: Chip export controls
  - ai-capex: AI capital spending
  - custom-silicon: Custom silicon at cloud providers
  - semiconductor-cycle: Semiconductor cycle
  - fed-policy-rate: Fed policy rate
  - us-inflation: US inflation
  - us-recession-risk: US recession risk
  - us-china-tariffs: US–China tariffs
  - taiwan-strait: Taiwan Strait
  - middle-east-conflict: Middle East conflict and oil prices
  - russia-ukraine-war: Russia–Ukraine war
  - supply-chain-shift: Supply-chain shift and shipping
Fiscal-year note (a numeric thesis takes its year and due date from it):
NVDA's fiscal year ends in month 1 and is named for the calendar year in which it ends: FY2027 runs from 2026-02 to 2027-01; the publication day 2026-07-06 falls in FY2027, so this year is FY2027 and next year is FY2028; FY2027's full-year figures are published in the annual report around 2027-02; use that day as the due date.

[What to read out] The author's forecasts, estimates, calculations and specific judgements, with their reasons, assumptions and figures when given, and price targets; the facts and figures the author cites, with their original attribution. Not the author's general arguments or risk lists.

[Open questions immediately before this item]
  - v1 (NVDA, due 2027-02-28): What will Nvidia's total revenue be in FY2027?
      takes: total_revenue figures, guidance, estimates and revisions for Nvidia FY2027 total revenue, this question's period 2026-02-01..2027-01-31
      accounting basis: GAAP
  - v10 (NVDA, due 2027-02-28): What non-GAAP operating margin will NVIDIA report for FY2027?
      takes: operating_margin figures, guidance, estimates and revisions for NVIDIA FY2027 non-GAAP operating margin, this question's period 2026-02-01..2027-01-31
      accounting basis: non-GAAP
  - v11 (NVDA, due 2027-02-28): What non-GAAP diluted earnings per share will NVIDIA report for FY2027?
      takes: figures, guidance, estimates and revisions for non-GAAP diluted EPS, this question's period 2026-02-01..2027-01-31
      accounting basis: non-GAAP
  - v12 (NVDA, due 2027-02-28): How much will NVIDIA spend on capital expenditures in FY2027?
      takes: capex figures, guidance, estimates and revisions for NVIDIA FY2027 capital expenditures, this question's period 2026-02-01..2027-01-31
      accounting basis: GAAP
  - v13 (ai-capex, due 2028-12-31): How much will the largest AI hyperscalers spend on data-center capital expenditures in calendar 2027?
      takes: spend_total figures, guidance, estimates and revisions for five hyperscalers, this question's period 2027-01-01..2027-12-31
  - v14 (supply-chain-shift, due 2027-03-31): What CoWoS advanced-packaging capacity will TSMC reach by the end of calendar 2026, in wafers a month?
      takes: capacity figures, guidance, estimates and revisions for CoWoS, this question's period 2026-01-01..2026-12-31
  - v15 (semiconductor-cycle, due 2027-03-31): By how much will worldwide semiconductor industry revenue grow in calendar 2026 over 2025?
      takes: growth_rate figures, guidance, estimates and revisions for industry revenue, this question's period 2026-01-01..2026-12-31
  - v16 (custom-silicon, due 2027-03-31): How much will cloud providers spend on custom AI silicon (ASICs) in calendar 2026?
      takes: spend_total figures, guidance, estimates and revisions for Spending on custom AI silicon (ASICs) at cloud providers in calendar 2026, this question's period 2026-01-01..2026-12-31
  - v17 (NVDA, due 2027-03-31): What share of China's calendar-2026 data-center AI accelerator spending will NVIDIA hold, by the first published full-year estimate?
      takes: figures, guidance, estimates and revisions for share of China data-center AI accelerator spending, this question's period 2026-01-01..2026-12-31
  - v18 (NVDA, due 2027-12-31): Will NVIDIA begin shipping its Rubin Ultra generation, in Kyber NVL144 racks, by December 31, 2027?
      takes: steps, dates, delays, cancellations, design or configuration changes, variants and stopgaps of this event, confirmations and denials, and named customers' statements about receiving it: Rubin Ultra
  - v19 (NVDA, due 2027-02-28): How much revenue will NVIDIA report from standalone Vera CPUs in FY2027?
      takes: product_revenue figures, guidance, estimates and revisions for Vera, this question's period 2026-02-01..2027-01-31
      accounting basis: GAAP
  - v2 (NVDA, due 2027-02-28): What Data Center segment revenue will NVIDIA report for FY2027?
      takes: segment_revenue figures, guidance, estimates and revisions for Data Center, this question's period 2026-02-01..2027-01-31
      accounting basis: GAAP
  - v20 (NVDA, due 2027-02-28): How much revenue will NVIDIA report from Blackwell and Rubin products in FY2027?
      takes: product_revenue figures, guidance, estimates and revisions for Blackwell+Rubin, this question's period 2026-02-01..2027-01-31
      accounting basis: GAAP
  - v21 (NVDA, due 2027-06-30): Will the SK Telecom AI factory built with NVIDIA GPUs begin operating by June 30, 2027?
      takes: steps, dates, delays, cancellations, design or configuration changes, variants and stopgaps of this event, confirmations and denials, and named customers' statements about receiving it: SK Telecom AI factory
  - v22 (NVDA, due 2028-02-28): What will Nvidia's total revenue be in FY2028?
      takes: total_revenue figures, guidance, estimates and revisions for Nvidia FY2028 total revenue, this question's period 2027-02-01..2028-01-31
      accounting basis: GAAP
  - v3 (NVDA, due 2027-02-28): What non-GAAP gross margin will NVIDIA report for FY2027?
      takes: gross_margin figures, guidance, estimates and revisions for NVIDIA FY2027 non-GAAP gross margin, this question's period 2026-02-01..2027-01-31
      accounting basis: non-GAAP
  - v4 (ai-capex, due 2027-12-31): How much will the four largest AI hyperscalers spend on data-center capital expenditures in calendar 2026?
      takes: spend_total figures, guidance, estimates and revisions for Combined data-center capital expenditures of the four largest AI hyperscalers, this question's period 2026-01-01..2026-12-31
  - v5 (semiconductor-cycle, due 2028-01-31): How will server DRAM and HBM contract prices in calendar 2027 compare with calendar 2026?
      takes: price figures, guidance, estimates and revisions for server DRAM and HBM contract prices, this question's period 2027-01-01..2027-12-31
  - v6 (NVDA, due 2027-03-31): What share of calendar-2026 data-center AI accelerator spending will NVIDIA hold, by the first published full-year estimate?
      takes: figures, guidance, estimates and revisions for share of data-center AI accelerator spending, this question's period 2026-01-01..2026-12-31
  - v7 (NVDA, due 2026-12-31): Will Nvidia begin shipping its Rubin generation by December 31, 2026?
      takes: steps, dates, delays, cancellations, design or configuration changes, variants and stopgaps of this event, confirmations and denials, and named customers' statements about receiving it: Rubin
  - v8 (chip-export-controls, due 2027-01-31): Will Chinese authorities issue any authorization for Chinese companies to import Nvidia H200 chips by January 31, 2027?
      takes: the decisions, drafts, approvals, denials and deadlines of this process, its enforcement and evasion, any statement of whether and how much the permitted or restricted activity is actually happening, and the affected parties' own plans and statements about it: China authorization of Nvidia H200 imports
  - v9 (NVDA, due 2027-02-28): What total amount of financing commitments and capacity backstops to customers and partners will NVIDIA report outstanding at its FY2027 year-end?
      takes: financing_amount figures, guidance, estimates and revisions for financing commitments and capacity backstops to customers and partners, this question's period 2026-02-01..2027-01-31
  - v23 (NVDA, due 2027-12-31): Will NVIDIA enter into any revenue-sharing and credit-support arrangements with AI clouds for supported computing capacity by December 31, 2027?
      takes: figures, guidance, estimates and revisions for Will NVIDIA enter into any revenue-sharing and credit-support arrangements with AI clouds for supported computing capacity by December 31, 2027? | How to check: Check NVIDIA's disclosures through December 31, 2027, including company announcements, SEC filings, and its FY2028 annual report when published. December 31, 2027 is an analyst's check date, not a date stated in the article. | Date basis: analyst_check; words: December 31, 2027 is an analyst's check date, not a date stated in the article., this question's period None..None; statements about the matter 'NVIDIA AI-cloud revenue-sharing and credit-support model' (also called AI clouds, AI factories, DSX AI factories): NVIDIA's introduction and potential use of revenue-sharing and credit-support arrangements with AI clouds for supported NVIDIA computing capacity. belong here under any of those names
  - v24 (NVDA, due 2027-12-31): Will NVIDIA agree by December 31, 2027, to provide a financial guarantee for OpenAI’s lease of the large Ohio data center?
      takes: figures, guidance, estimates and revisions for Will NVIDIA agree by December 31, 2027, to provide a financial guarantee for OpenAI’s lease of the large Ohio data center? | How to check: Use December 31, 2027 as an analyst’s check date, within 18 months of the report; the article gives no date for a possible agreement. Check NVIDIA and OpenAI announcements, SEC filings, and other material reporting for confirmation or denial of an agreement covering the Ohio lease. | Date basis: analyst_check; words: Use December 31, 2027 as an analyst’s check date, this question's period None..None; statements about the matter 'NVIDIA AI-cloud revenue-sharing and credit-support model' (also called AI clouds, AI factories, DSX AI factories): NVIDIA's introduction and potential use of revenue-sharing and credit-support arrangements with AI clouds for supported NVIDIA computing capacity. belong here under any of those names
  - v25 (NVDA, due 2027-02-28): By what percentage will NVIDIA’s GPU shipments grow in FY2027 compared with FY2026?
      takes: figures, guidance, estimates and revisions for By what percentage will NVIDIA’s GPU shipments grow in FY2027 compared with FY2026? | How to check: Check NVIDIA’s FY2027 annual report, expected around February 2027, for any disclosed GPU shipment figures or growth. The article gives a forecast of 26 percent per year but does not specify its comparison period or the basis for measuring shipments; the FY2027-over-FY2026 comparison is the analyst’s question, not a period stated in the article. | Date basis: analyst_check (expected settling material; not a source date), this question's period None..None
  - v26 (NVDA, due 2028-02-29): What diluted earnings per share will NVIDIA report for FY2028?
      takes: figures, guidance, estimates and revisions for What diluted earnings per share will NVIDIA report for FY2028? | How to check: Check NVIDIA's FY2028 annual report, expected around February 2028, for reported diluted EPS. The article's $12.76 figure is an analyst consensus estimate, not a company-reported result. | Date basis: analyst_check (expected settling material; not a source date), this question's period None..None

[Research groups] Use the supplied question descriptions to understand their scope.

[Item] id gnews:3df0bbc8aff2c1d008bc0a32, category T8, author 247wallst.com (analyst), published 2026-07-06, title: How Nvidia Became The Black Sheep Of The Chip Stock Rally

How Nvidia Became The Black Sheep Of The Chip Stock Rally
NVIDIA’s fundamentals have never looked stronger, yet its stock is limping through 2026. NVIDIA (NASDAQ:NVDA | NVDA Price Prediction) is up just 3.2% year to date, a striking laggard in a sector where money is flooding into almost everything else.…
By Danielle Liverance
NVDA is up just 7% year to date despite 85% revenue growth to $82B, punished for being priced as the consensus AI trade.
AMD surged 171% and Micron 305% year to date, rewarding investors who bet on chips with room to reprice rather than perfection already baked in.
Nvidia's $119B in supply commitments hinge on AI delivering measurable economic value beyond productivity tools, which is a question the market appears to already be pricing in.
NVIDIA’s fundamentals have never looked stronger, yet its stock is limping through 2026. NVIDIA ( NASDAQ:NVDA | NVDA Price Prediction ) is up just 3.2% year to date, a striking laggard in a sector where money is flooding into almost everything else. That is the paradox: the company at the center of the AI buildout has become the black sheep of the chip rally.
Advanced Micro Devices ( NASDAQ:AMD ) has ripped 171.25% year to date. Micron Technology ( NASDAQ:MU ) is up a stunning 304.62%. Intel ( NASDAQ:INTC ), still deep in a turnaround under Lip-Bu Tan, has surged 278.4% on DCAI momentum and NVIDIA’s own $5 billion equity investment. Broadcom ( NASDAQ:AVGO ), the custom-silicon story, is one example of another megacap stock that largely matches NVIDIA’s returns.
But the broader story is one of semiconductor stocks rallying. The VanEck Semiconductor ETF (Nasdaq: SMH) is up 59% year-to-date. The divergence looks set to continue today. The VanEck is up 3% premarket while NVIDIA shares are up just .3%, as of 8:40 a.m. ET. NVIDIA shares are under pressure on reports of delays across their upcoming lineup of Vera Rubin server systems.
The earnings do not explain the tape. Revenue rose 85% year over year to $81.6 billion, with data center up 92% to $75.2 billion. CEO Jensen Huang framed it plainly: “Agentic AI has arrived, doing productive work, generating real value and scaling rapidly across companies and industries.” But NVDA trades at a forward P/E of less than 20 now, and when a name becomes the consensus AI trade, even a blowout can underwhelm a market that had already priced perfection. Polymarket sentiment tracks this: end-of-July close-above-$200 probability sits at just 43%.
The narrative is fragmenting. NVIDIA still owns roughly 81% of the AI chip market , but Broadcom’s custom ASICs for Alphabet and Meta are eating the story, with Bloomberg Intelligence forecasting a 27% CAGR for custom ASICs through 2033 versus 16% for AI accelerators. Broadcom guided Q3 AI semiconductor revenue to $16.0 billion, more than 200% year over year. AMD’s Meta Instinct GPU deal anchors a multi-year hyperscaler thesis , and Lisa Su noted “leading customer forecasts exceeding our initial expectations” on MI450.
One important number to watch is the relative size of AMD compared to NVIDIA. Right now, AMD is worth about 18% of NVIDIA’s value. At the beginning of the year, AMD was worth less than 10% NVIDIA. Investors are still piling into companies benefiting from the data center buildout, they’re just not piling into NVIDIA.
Micron is a different animal. Samsung, SK Hynix, and Micron have avoided the aggressive oversupply that crushed memory pricing in prior cycles, a meaningful break from history. Q3 revenue exploded 345.7% year over year to $41.46 billion, and CEO Sanjay Mehrotra pointed to multi-year Strategic Customer Agreements designed to lock in durability. NVIDIA has been smart about locking in its own memory supply as other companies like Apple (Nasdaq: AAPL) have been caught flat footed. And yet, the combined value of Micron, SK Hynix, and Samsung now rivals NVIDIA itself.
Most strikingly, Micron is now forecasting adjusted gross margins of 86% next quarter, above the peak gross margins NVIDIA ever achieved. Some estimates put half of all data center spend going toward memory in 2027. Simply put, the rise of memory is shifting the center of gravity in the data center trade away from NVIDIA and towards memory names.
Which brings the market to the quiet question underneath all of it. Demand looks strong in 2027, but with hyperscalers now having to move into debt and equity offerings, the question of whether growth slows dramatically in 2028 is now front and center on investors minds. The ‘good’ news for NVIDIA investors is the company now trades for just 12X its forecasted 2028 earnings. If a slowdown does come, it’ll likely hit NVIDIA a lot less than names trading for 50X their forecasted 2028 profits.
I've spent more than 15 years inside enterprise software, working alongside the finance, sales operations, and HR leaders who run the revenue engines at some of the largest tech companies in the country.
My day job is helping enterprise executives make smarter decisions about retention, compensation, and growth. These are the same operational levers that show up in every earnings report investors actually read. That perspective shapes my writing for 24/7 Wall St.
The headline numbers are easy. The interesting stuff is underneath: how companies make money, what executives are worried about, and what any of it means for the person checking their 401(k) on a Sunday afternoon. I write about personal finance and business as someone who has spent her career inside the rooms where these decisions get made.
SK Hynix surged 14% Tuesday without a single company-specific headline, and the real test comes July 29 when its earnings either confirm or shatter the bullish memory narrative Micron just set.

Return only evidence per the schema. Each evidence link must be an ID of a supplied existing question.

Before you return the answer, check it once. A clearly retold past actual figure may be kept or omitted; still-effective guidance and forecasts retain their usual weight. For a company statement retold by a news author, the article publication day is not the original statement day unless the article says so; otherwise leave original_day empty. Read each evidence item back as the analyst following the company and keep it when you would write it in this week's notes because it makes some question's answer more or less likely, about the company or its customers, suppliers, competitors, regulators or the economy. Ask first whether it is new: repeated common knowledge, a long-standing situation retold and an unargued view are noise; guidance, a forecast, a plan or a decision still in force keeps its place even when retold, including a change to a plan, design or schedule that another outlet reported days or weeks before. Judge the action or information itself, not its verb tense, and do not take a statement as old because its date is missing. Fitting one of the four kinds does not keep an item. A missing amount, date or scale never drops an item on its own: a forecast, a rumour, a counter-example or a distant or conditional statement is judged like any other.
These are not kept, even when a named party states them. What a row says it does not cover goes back to the test above, unless the row says it is kept:
- background the analyst already knew, such as the company's history ("the company was founded in 1998"); an arrangement the item only describes as in place, even when no date is given: customers or partners that use, host, run or have built on the company's products, and the benefits they describe from that use ("two airlines fly the planemaker's jets"; "three insurers run claims on the company's software and report faster payouts"); a partnership, contract, plant or investment the item itself dates to an earlier month or year with no new step ("earlier this year the company partnered with the glassmaker on three plants"; "in May it signed a $3 billion cloud contract"); it does not cover a step the item reports as news, taken, decided, planned or under way (an order, a selection, an integration, an expansion, a deployment), even when it gives no date ("the retailer's largest supplier is opening its own stores, people familiar said this week"; "the two largest cement makers are adding kilns to meet demand"), nor a customer's, supplier's or partner's newly disclosed revenue, capacity, orders or contracted amount; a deal the item mentions as already existing is an arrangement in place even with its amount ("a rival airline already leases 40 of the same jets");
- a typical claim that is common knowledge, without a figure and a specific account: that a firm leads or competes, that demand is strong or supply tight, a general risk ("if demand slows it would hurt"); a number does not lift a familiar position ("the rival grocer has led this market for years and still holds 40%"); it does not cover a dated forecast of a shortage, a price or demand ("the steelmaker expects the shortage to peak next year and last until 2028"), a competitor's newly reported share, volume or price in the company's market ("the local rival now holds about half of the regional market, worth about $5 billion"), nor a reported movement of a named price, rental rate, lead time or order book, even without a figure ("rental rates for used trucks have been climbing this quarter"); a general statement that demand stays strong or a product stays popular is not one;
- a product, game, driver or benchmark specification with no business scale ("the vacuum runs 60 minutes on a charge"; "a benchmark score"), a retail price detail ("a retailer marks one model down by $50"), and a comparison the company, a partner or a third party publishes ("the maker says its drug works twice as fast as older ones"; "a reviewer's test"); it does not cover a competitor's comparison against the company's product, a partner's or customer's adoption or integration (also when a comparison shares its sentence), a reported launch, shipment, delay or cancellation of any of the company's products or a change to a product plan or configuration, including a reported sign that a planned product is going ahead ("the long-range version of the jet is likely delayed or limited to a few deliveries"; "a parts supplier's catalogue lists the unannounced model"), nor the company's decision to change the price it charges; uncertainty or a smaller product line does not make it a specification;
- an unargued view or a quote that only characterises ("the stock is a hold"; "a pivotal moment"; "an industry-leading platform"), and a named analyst's reading of an event already recorded that adds no new fact or calculation ("the recall shows quality risks are rising"); it does not cover a reading that adds a new fact or calculation, nor the company's own statement that its plan, schedule or guidance still stands ("the carmaker said the launch date has not moved"), which is judged as the plan itself would be; a conditional valuation of the company with its assumptions, derivation and date is kept;
- a political or strategic stance with no figure and no decision ("diversifying suppliers will not reduce dependence"); it does not cover a policy or regulatory step, nor a decision still in force that the item reports;
- a share-price move or an investor's position or trade ("shares fell 13% this month"; "he is short the stock"); it does not cover the news behind the move; the covered company's market value, a standalone valuation multiple, and its share-price reaction after earnings are optional;
- another company's matter that touches none of the company's markets (its valuation, share price, governance or a deal outside them), or that sits next to the company only by sharing an article, an event or an ecosystem; you supply the connection as the analyst and the item need not state it: a customer's spending, orders or backlog bears on demand, a supplier's capacity, output, prices or revenue on supply and input costs, a rival's products, prices or share in the company's markets on competition ("a large customer's order backlog doubled"; "the main supplier's quarterly revenue jumped on demand for the part");
- the same fact said again in other words within this item: one deal, hire, programme or reported measure told in several sentences, with its terms, figures and growth rates, is one evidence item; keep the fuller wording ("a $2 billion order for 120 stores in 15 countries over three years"; "cloud revenue of $8 billion, up 30% on the year and 6% on the quarter, 40% of the total"); a deal one party signs under a wider programme, with its own amount or capacity, is its own evidence item, and a fact another outlet reported before is not a repeat within this item;
- company boilerplate, bylines, forward-looking-statement text.
Return only the evidence items you keep.

## Schema (evidence item fields with descriptions)

- event_time: (no description)

- id: (no description)

- links: The questions this statement is filed under, decided after you have decided it is evidence: the id of the narrowest open question in [Open questions] whose answer this statement makes more or less likely, as that question's own figure, step or estimate or through the demand, supply, competition or pricing behind its answer; compare the specific questions before a company-wide revenue or margin question and take that one only, never a broader question beside it; a shared company, industry, event or ecosystem is not a connection, and the statement need not repeat the question's words (a variant, sibling or other name of the subject counts); whoever says it, and even when it gives no period, basis or exact amount, because the weight is judged later; an estimate for another period or population of a question's quantity is filed under it when no open question covers that period; when no specific question is connected, a statement that moves the demand, supply, competition or pricing behind the company's results goes to the company-wide revenue question of its period. A relevant quarterly actual or forecast can inform an annual question. A material assumption or condition of a forecast can inform the same question when it changes how the forecast is understood; preserve its uncertainty. Use only the supplied existing question ids; empty when no question is connected, however important the statement sounds.

- one_line: (no description)

- original_day: The day that party made it, as an ISO day when the item gives one ("signed on 3 March 2026": 2026-03-03); empty when the item gives none or only a month; the publication day only when the item is that party's own release, filing, call or analysis.

- original_who: The party whose statement, figure or action it is, even when the item reports it without attribution ("the insurer agreed to buy the broker": the insurer; "the regulator fined the bank, a newspaper reported": the regulator); the outlet or author only for its own estimate, analysis or unnamed-source report.

- quote: (no description)

- speaker: Who says it in this item: the outlet, the author or the person quoted.

- tier: (no description)

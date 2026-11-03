# Ledger census, granularity reading and extraction-gold candidates (NVDA corpus, poc-v23 Jev ledger)

Reader note: every judgement below is the analyst reading of an assistant (Claude, 2026-10-26), not a human gold. Read-only work; nothing under `poc/` was changed.

Sources (cited as `L:` and `I:` below):
- `L:` = `/Users/lchingen/hivemind/poc/data/english-v23-jev-2026-10-25/views.sqlite` (tables `views`, `rungs`, `view_keys`, `view_switches`, `evidence`, `evidence_links`, `evidence_sources`, `thesis_groups`, `thesis_group_members`, `judgements`, `successions`, `dependencies`, `handovers`, `processing_steps`, `match_records`, `review_pool_entries`, `late_statements`, `days_completed`).
- `I:` = `/Users/lchingen/hivemind/poc/data/items-window-tags2-2026-10-24.sqlite` (table `items`: `input_id`, `title`, `text`, `publisher`, `publication_day`, `channel`, `klass`, `text_chars`).
- Rules read: `/Users/lchingen/hivemind/AGENTS.md` §8; `/Users/lchingen/hivemind/docs/prd/06-views.md` (Purpose, Rationale, Two thesis kinds, Ladder, Open questions); `/Users/lchingen/hivemind/docs/research/2026-10-22-granularity/A-thesis-anatomy.md` "Synthesis (15 lines)".
- Matching golds (shape reference only): `/Users/lchingen/hivemind/poc/eval/gold/week-benchmark-v23-2026-10-25.json` and seven siblings (listed in Q4 gaps).

Corpus and run facts (`L:days_completed`, `L:processing_steps`, `I:items`): the ledger covers publication days 2026-02-25 to 2026-08-15 (172 days completed); 537 inputs processed, 480 extracted, 244 reached matching, 31 merged as copies. 2,205 items in `I:`, dated 2026-02-25..2026-10-22, so items after 2026-08-15 (for example the 2026-08-18..20 H200-to-China stories) were never processed. Of 737 Google-News items, 221 are headline-only (text under 200 chars); none of those reached extraction.

---

## Q1. What is in the ledger: full census of the 90 theses

### Takeaway
90 theses, all open (`L:view_switches` has no `open=0` row), 716 evidence links, 227 judgements, 18 research groups, zero successions and zero dependencies. Half of all evidence links (356/716) go to two theses, NVDA FY2027 total revenue (v2, 126 links) and NVDA FY2027 data-center revenue (v3, 230 links). 22 theses are NVDA, 17 are `ai-capex` theme theses.

### Cited Findings

Totals by measure (`L:view_keys.measure`): event 18; spend_total 14; total_revenue 12; segment_revenue 11; growth_rate 7; tax_rate 5; capex 4; shipments_or_capacity 2; run_rate 2; product_revenue 2; other 2; operating_expense_growth 2; capacity 2; total_expenses 1; policy_event 1; operating_margin 1; operating_loss 1; gross_margin 1; financing_amount 1; design_wins 1.

Totals by object (`L:views.object_id`): NVDA 22; ai-capex (theme) 17; AMD 10; MSFT 10; META 8; CRWV 7; AMZN 6; TSM 4; INTC 2; SMCI 2; chip-export-controls (theme) 1; us-recession-risk (theme) 1.

Other counts: evidence 534 by tier (`L:evidence.tier`): third_party_view 216, party_statement 199, fact 97, rumour 22. Evidence linked to more than one thesis: 155 of 534. Match outcomes over all `L:match_records`: candidates new 95, merge 7; evidence new 567, repeat 294, replace 26. Theses per source item (`L:views.created_from_input`): MSFT call 2026-07-29 → 9; NVDA call 2026-02-25 → 8; AMD call 2026-08-04 → 8; CRWV call 2026-08-11 → 6; META call 2026-07-29 → 5; AMZN call 2026-07-30 → 4; everything else 1–2 per item.

Census table. Columns: id | object | question (verbatim, `L:views.question`) | key = measure / scope / period (`L:view_keys`) | groups (`L:thesis_groups.name`) | links (`L:evidence_links`) | judgements | open | class (Q2 letter). Due day in brackets after the id when it matters.

| id | object | question | key | groups | links | judg | open | class |
|---|---|---|---|---|---|---|---|---|
| v1 [due 2027-02-28] | ai-capex | Will combined 2026 capital expenditure by the top five cloud providers and hyperscalers approach or exceed $700 billion? | spend_total / Top five cloud providers and hyperscalers / 2026 | Cloud and hyperscaler AI-capex cycle | 7 | 3 | yes | a |
| v2 [2027-02-24] | NVDA | Can sustained sequential growth through calendar 2026 lift NVIDIA FY2027 total revenue into which range? | total_revenue / – / FY2027 | – | 126 | 24 | yes | d (of v3) |
| v3 [2027-02-24] | NVDA | Can continued AI infrastructure demand and sequential growth through calendar 2026 lift NVIDIA FY2027 data-center revenue into which range? | segment_revenue / Data Center / FY2027 | – | 230 | 24 | yes | a |
| v4 [2027-02-24] | NVDA | Can NVIDIA sustain full-year non-GAAP gross margin around management's mid-70s expectation in FY2027? | gross_margin / – / FY2027 non-GAAP | – | 19 | 12 | yes | a |
| v5 | NVDA | Can NVIDIA keep FY2027 non-GAAP operating expense growth near management's low-40s expectation? | operating_expense_growth / – / FY2027 | – | 6 | 3 | yes | b |
| v6 | NVDA | Can NVIDIA's FY2027 non-GAAP effective tax rate remain within management's stated 7%–19% range? | tax_rate / – / FY2027 non-GAAP | – | 5 | 2 | yes | b |
| v7 [2026-12-31] | NVDA | Will NVIDIA commence Vera Rubin production shipments by December 31, 2026? | event / Rubin / shipment | Vera Rubin platform rollout | 21 | 12 | yes | a |
| v8 [2027-01-31] | NVDA | Will U.S. authorities allow H200 imports into China by the end of NVIDIA FY2027? | event / H20/H200 China / licence | H200 China import authorization | 12 | 6 | yes | a (wording defect) |
| v9 [2028-02-24] | NVDA | Can continued growth in NVIDIA's Compute & Networking business bring FY2027 Compute & Networking segment revenue into which range? | segment_revenue / Compute & Networking / FY2027 | – | 9 | 3 | yes | d (of v3) |
| v10 [2028-02-24] | NVDA | Can NVIDIA's increased investment to support business growth bring FY2027 capital expenditures into which range? | capex / – / FY2027 | – | 5 | 4 | yes | b |
| v11 [2028-02-24] | NVDA | Can demand for Vera standalone CPUs bring NVIDIA FY2027 standalone Vera CPU revenue into which range? | product_revenue / Vera standalone CPUs / FY2027 | – | 25 | 10 | yes | a |
| v12 | NVDA | Can NVIDIA keep its FY2027 GAAP effective tax rate within the company's stated 16%–18% expectation? | tax_rate / GAAP effective tax rate / FY2027 | – | 1 | 1 | yes | d (of v6) |
| v13 | INTC | Can higher product revenue, despite supply constraints, bring Intel FY2026 total revenue into which range? | total_revenue / – / 2026 | – | 4 | 2 | yes | b |
| v14 | INTC | Can higher client average selling prices and product demand bring Intel's FY2026 CCPG segment revenue into which range? | segment_revenue / CCPG / 2026 | – | 1 | 1 | yes | b |
| v15 [2027-12-31] | NVDA | Will SK Telecom bring its first NVIDIA-powered AI factory online by December 31, 2027? | event / SK Telecom AI factory / deployment | SK Telecom–NVIDIA AI factory buildout; Vera Rubin platform rollout | 4 | 2 | yes | e (→ v3) |
| v16 [2028-12-31] | NVDA | Will NAVER and NVIDIA complete the expansion of the GAK Sejong NVIDIA DSX AI factory to 200 megawatts by December 31, 2028? | event / NAVER GAK Sejong … 200 MW / deployment | NAVER GAK Sejong AI factory expansion; Vera Rubin platform rollout | 7 | 3 | yes | e (→ v3) |
| v17 [2028-02-24] | NVDA | Can demand for Blackwell and Rubin chips bring NVIDIA's combined booked revenue from these products in calendar 2025–2027 into which range? | product_revenue / Blackwell and Rubin chips combined / 2025–2027 | Vera Rubin platform rollout | 56 | 17 | yes | c |
| v18 [2027-12-31] | ai-capex | Can tech giants’ AI infrastructure spending exceed $700 billion in calendar 2026? | spend_total / Tech giants’ AI infrastructure spending / 2026 | Cloud and hyperscaler AI-capex cycle | 8 | 4 | yes | d (of v1) |
| v19 [2028-12-31] | NVDA | Will NVIDIA launch its Rosa CPU by December 31, 2028? | event / Rosa CPU / launch | NVIDIA Feynman platform and Rosa CPU launch | 1 | 1 | yes | e |
| v20 [2027-02-01] | ai-capex | Will Alphabet's AI infrastructure investment bring its 2026 capital expenditures into which range? | spend_total / Alphabet capital expenditures / 2026 | Cloud and hyperscaler AI-capex cycle | 2 | 1 | yes | a (object should be GOOGL) |
| v21 [2026-10-31] | NVDA | Will NVIDIA commence RTX Spark system shipments by October 31, 2026? | event / RTX Spark systems / shipment | NVIDIA RTX Spark rollout | 3 | 3 | yes | e |
| v22 [2028-02-24] | ai-capex | Will AI hyperscaler data-center capital expenditures in calendar 2027 reach which range? | spend_total / AI hyperscalers' data-center capital expenditures / 2027 | Cloud and hyperscaler AI-capex cycle | 3 | 3 | yes | a |
| v23 [2027-01-31] | NVDA | Will Taiwan adopt tighter restrictions on AI chip sales to China by January 31, 2027, potentially affecting NVIDIA's annual revenue? | event / Taiwan restrictions … / other | Taiwan AI chip export-policy review | 3 | 2 | yes | e (→ China question) |
| v24 | META | Can Meta's business momentum bring FY2026 total revenue into which range? | total_revenue / – / 2026 | – | 1 | 1 | yes | b |
| v25 | META | Can Meta's Family of Apps business momentum bring FY2026 Family of Apps revenue into which range? | segment_revenue / Family of Apps / 2026 | – | 3 | 2 | yes | d (of v24; identical ladder) |
| v26 | META | Can Meta's expense discipline keep FY2026 total expenses within which range? | total_expenses / – / 2026 | – | 2 | 1 | yes | b |
| v27 [2027-03-31] | META | Can Meta's infrastructure investment produce FY2026 capital expenditures within which range? | capex / – / 2026 | Cloud and hyperscaler AI-capex cycle | 2 | 1 | yes | a |
| v28 | META | Can Meta keep its FY2026 tax rate within which range? | tax_rate / – / 2026 | – | 1 | 1 | yes | b |
| v29 | MSFT | Can continued commercial momentum bring Microsoft FY2027 total revenue into which range? | total_revenue / – / FY2027 | – | 3 | 1 | yes | b |
| v30 [2027-07-29] | MSFT | Can continued Azure demand and capacity delivery bring Microsoft Intelligent Cloud FY2027 revenue into which range? | segment_revenue / Intelligent Cloud / FY2027 | – | 6 | 1 | yes | a |
| v31 | MSFT | Can Microsoft's continued investment in R&D compute capacity, talent, and data keep FY2027 operating-expense growth within which range? | operating_expense_growth / – / FY2027 | – | 2 | 1 | yes | b |
| v32 [2027-07-29] | MSFT | Can Microsoft's infrastructure efficiencies and revenue growth limit the FY2027 operating-margin decline to less than one percentage point? | operating_margin / – / FY2027 | – | 4 | 1 | yes | a |
| v33 | MSFT | Can Microsoft keep its FY2027 effective tax rate near the approximately 20% expectation? | tax_rate / – / FY2027 | – | 2 | 1 | yes | b |
| v34 | MSFT | Can the timing of long-duration M365 contracts offset the launch-timing comparison and keep FY2027 M365 Commercial products revenue growth within which range? | growth_rate / M365 Commercial products / FY2027 | – | 1 | 1 | yes | b |
| v35 | MSFT | Can customer demand and the launch-timing comparison keep FY2027 Server products revenue growth within which range? | growth_rate / Server products / FY2027 | – | 1 | 1 | yes | b |
| v36 | MSFT | Can lower PC-market demand and component-cost-driven device pricing keep FY2027 Windows OEM and Devices revenue growth within which range? | growth_rate / Windows OEM and Devices / FY2027 | – | 1 | 1 | yes | b |
| v37 | MSFT | Can Microsoft's portfolio and operational reset return the Xbox business to revenue growth in FY2027? | growth_rate / Xbox business / FY2027 | – | 1 | 1 | yes | b |
| v38 | META | Can Meta's operating performance bring FY2026 income from operations into which range? | other / income from operations / 2026 | – | 2 | 1 | yes | b |
| v39 | MSFT | Can continued growth in Microsoft's Productivity and Business Processes business bring FY2027 segment revenue into which range? | segment_revenue / Productivity and Business Processes / FY2027 | – | 1 | 1 | yes | b |
| v40 [2027-02-01] | ai-capex | Will major cloud infrastructure providers spend about $1 trillion on AI and data-center infrastructure in calendar 2026? | spend_total / Major cloud infrastructure providers, incl. hyperscalers, OpenAI, Anthropic / 2026 | Cloud and hyperscaler AI-capex cycle | 3 | 2 | yes | d (of v1) + c |
| v41 [2027-03-31] | ai-capex | Will combined 2026 capital expenditures by Alphabet, Amazon, Meta Platforms, Microsoft and Oracle reach which range, amid accelerating AI infrastructure spending? | spend_total / Combined capex by Alphabet, Amazon, Meta, Microsoft, Oracle / 2026 | 2026 hyperscaler capital-spending cycle; Cloud and hyperscaler AI-capex cycle | 4 | 3 | yes | d (of v1) |
| v42 | META | Can Meta's Reality Labs business keep its FY2026 operating loss near the FY2025 level? | operating_loss / Reality Labs / 2026 | – | 1 | 1 | yes | b (in this corpus) |
| v43 [2026-09-30] | META | Will Meta close the El Paso data-center campus co-development transaction by September 30, 2026? | event / El Paso … transaction / deal_close | Cloud and hyperscaler AI-capex cycle | 1 | 1 | yes | e (→ v27) |
| v44 [2027-03-31] | AMZN | Can AWS's accelerating growth bring FY2026 segment revenue into which range? | segment_revenue / Amazon Web Services / 2026 | – | 3 | 2 | yes | a |
| v45 [2027-03-31] | AMZN | Can Amazon's AI and AWS investment plans, including higher memory costs, bring FY2026 cash CapEx into which range? | capex / cash CapEx / 2026 | 2026 hyperscaler capital-spending cycle; Cloud and hyperscaler AI-capex cycle | 3 | 2 | yes | a |
| v46 [2027-12-31] | AMZN | Will AWS reach at least double its 2025 power capacity by the end of 2027? | shipments_or_capacity / AWS power capacity / 2027 | Cloud and hyperscaler AI-capex cycle | 1 | 1 | yes | e (→ v45) |
| v47 | AMZN | Will Amazon Leo begin initial satellite internet service by 2026-12-31? | event / Amazon Leo … / launch | – | 1 | 1 | yes | e (out of corpus purpose) |
| v48 | AMZN | Can continued sales growth bring Amazon FY2026 total revenue into which range? | total_revenue / – / 2026 | – | 4 | 2 | yes | b (ladder inverted) |
| v49 | AMZN | Will Amazon close its acquisition of Globalstar by December 31, 2027? | event / Amazon acquisition of Globalstar / deal_close | Amazon acquisition of Globalstar | 2 | 1 | yes | e (out of corpus purpose) |
| v50 [2027-12-31] | ai-capex | Will total AI spending reach which range in calendar 2027, against Jensen Huang's expectation of $1 trillion? | spend_total / Total AI spending worldwide / 2027 | Cloud and hyperscaler AI-capex cycle | 1 | 1 | yes | c |
| v51 [2026-12-31] | ai-capex | Will Alphabet and Amazon's combined spending on upgrading their AI platforms reach which range in calendar 2026, against the article's estimate of around $400 billion? | spend_total / Alphabet and Amazon combined … / 2026 | Cloud and hyperscaler AI-capex cycle; 2026 hyperscaler capital-spending cycle | 1 | 1 | yes | d (sum of v20+v45) |
| v52 | AMD | Can sustained AI-driven demand and growth across AMD's businesses bring AMD's FY2027 total revenue into which range? | total_revenue / – / 2027 | – | 4 | 1 | yes | b |
| v53 [2027-03-31] | AMD | Can demand for EPYC processors and Instinct accelerators bring AMD Data Center segment FY2026 revenue into which range? | segment_revenue / Data Center / 2026 | – | 3 | 1 | yes | a |
| v54 [2028-03-31] | AMD | Can the ramp in Helios and MI450 deployments bring AMD Data Center segment FY2027 revenue into which range? | segment_revenue / Data Center / 2027 | AMD Helios and MI450 customer rollout | 5 | 2 | yes | a |
| v55 | AMD | Can strong server CPU demand and improved supply bring AMD server revenue growth in FY2027 into which range? | growth_rate / AMD server revenue / 2027 | AMD Helios and MI450 customer rollout | 1 | 1 | yes | d (inside v54) |
| v56 | AMD | Can broad customer wins bring the value of AMD's new design wins in 2026 into which range? | design_wins / new design wins / 2026 | – | 1 | 1 | yes | c |
| v57 | AMD | Can Ryzen demand and commercial adoption bring AMD Client business revenue growth in FY2026 into which range? | growth_rate / Client business revenue / 2026 | – | 2 | 1 | yes | b |
| v58 [2026-09-30] | AMD | Will AMD begin initial Helios shipments by September 30, 2026, as management expects? | event / Helios / shipment | AMD Helios and MI450 customer rollout | 3 | 2 | yes | a |
| v59 [2027-06-30] | AMD | Will Anthropic begin deploying at least one gigawatt of MI450 GPUs in Helios by June 30, 2027? | event / MI450 / deployment | AMD Helios and MI450 customer rollout | 2 | 2 | yes | e (→ v54) |
| v60 | AMD | Can continued revenue growth bring AMD's FY2026 total revenue into which range? | total_revenue / – / 2026 | – | 8 | 2 | yes | b |
| v61 | AMD | Can AMD keep its FY2026 non-GAAP tax rate within which range of its stated 13% projection? | tax_rate / – / 2026 non-GAAP | – | 1 | 1 | yes | b |
| v62 [2027-12-31] | NVDA | Will SpaceX begin launching its Starmind AI satellite, using an optimized Vera Rubin NVL72 computer, by December 31, 2027? | event / SpaceX Starmind … / launch | Vera Rubin platform rollout | 7 | 3 | yes | e (→ v3, v7) |
| v63 [2026-08-27] | chip-export-controls | Will BIS’s directive allocation order requiring domestic allocation of black mass and tungsten waste and scrap take effect on August 27, 2026? | policy_event / Domestic sales allocation … / other | Recoverable critical minerals domestic allocation order | 3 | 1 | yes | e (out of corpus purpose) |
| v64 [2027-06-30] | NVDA | Will Zankore by Indosat bring approximately 200 MW of NVIDIA GB300 NVL72-powered AI capacity online by June 30, 2027? | event / Zankore by Indosat … / deployment | NAVER GAK Sejong AI factory expansion | 3 | 1 | yes | e (→ v3; wrong group) |
| v65 [2027-12-31] | ai-capex | Will Amazon's 2026 capital expenditures fall into which range, given its $220 billion projection? | spend_total / Amazon capital expenditures / 2026 | 2026 hyperscaler capital-spending cycle; Cloud and hyperscaler AI-capex cycle | 1 | 1 | yes | d (of v45) |
| v66 [2027-01-31] | us-recession-risk | Will the average U.S. unemployment rate in calendar 2026 be higher than, near, or lower than July 2026's 4.1% reading, as measured by the average of the monthly rates published for 2026? | growth_rate / U.S. unemployment rate, annual average / 2026 | – | 3 | 1 | yes | a (macro theme, no dependants) |
| v67 [2026-12-31] | ai-capex | Will SpaceX's AI infrastructure buildout bring its year-end 2026 compute capacity to which range, relative to the stated expectation of more than 2 gigawatts? | capacity / SpaceX compute capacity / 2026 | – | 1 | 1 | yes | a (object should be SpaceX) |
| v68 [2027-12-31] | NVDA | Will Firebird deploy more than 70,000 NVIDIA Rubin and Blackwell GPUs and 300 megawatts of AI infrastructure in Armenia by December 31, 2027, supporting NVIDIA product revenue? | event / Firebird AI factory deployment in Armenia / deployment | Firebird AI factory rollout; Vera Rubin platform rollout | 1 | 1 | yes | e (→ v3) |
| v69 [2027-03-31] | TSM | Can the 37.0% January–July 2026 revenue growth sustain FY2026 consolidated revenue in a range around NT$4.92 trillion? | total_revenue / consolidated / 2026 TWD | – | 3 | 2 | yes | a |
| v70 [2027-12-31] | ai-capex | Will hyperscaler capital expenditure on AI reach which range in calendar 2027, relative to the reported forecast of more than $1 trillion? | spend_total / Hyperscaler capital expenditure on AI / 2027 | 2026 hyperscaler capital-spending cycle; Cloud and hyperscaler AI-capex cycle | 2 | 2 | yes | d (of v22) |
| v71 [2026-12-31] | TSM | Will the required regulatory approvals for the Sony Semiconductor Solutions–TSMC joint venture be received by FY2026 year-end? | event / Required regulatory approvals … / approval | Sony–TSMC next-generation image-sensor joint venture | 2 | 1 | yes | e (out of corpus purpose) |
| v72 [2027-03-31] | CRWV | Can customer demand and execution bring CoreWeave's FY2026 total revenue into which range? | total_revenue / – / 2026 | – | 9 | 2 | yes | a |
| v73 | CRWV | Can customer demand and operating leverage bring CoreWeave's FY2026 adjusted operating income into which range? | other / adjusted operating income / 2026 non-GAAP | – | 1 | 1 | yes | b |
| v74 [2027-03-31] | CRWV | Can customer capacity deliveries and recent wins bring CoreWeave's FY2026 capital expenditures into which range? | capex / – / 2026 | Cloud and hyperscaler AI-capex cycle | 3 | 2 | yes | a |
| v75 | CRWV | Can customer growth and expanding platform demand bring CoreWeave's annualized run-rate revenue at FY2026 year-end into which range? | run_rate / annualized revenue / 2026 | – | 3 | 1 | yes | b |
| v76 | CRWV | Can CoreWeave's capacity deployment bring active power at FY2026 year-end into which range? | shipments_or_capacity / active power / 2026 GW | – | 2 | 1 | yes | b |
| v77 | CRWV | Can expanding managed inference demand bring CoreWeave's managed inference ARR at FY2026 year-end into which range? | run_rate / managed inference ARR / 2026 | – | 1 | 1 | yes | b |
| v78 [2027-07-30] | SMCI | Can strong orders and AI/IT infrastructure demand bring SMCI's FY2027 total revenue into which range? | total_revenue / – / FY2027 | – | 4 | 1 | yes | a |
| v79 | SMCI | Can continued growth in OEM appliance and large data center demand bring SMCI's FY2027 OEM appliance and large data center revenue into which range? | segment_revenue / OEM appliance and large data center / FY2027 | – | 1 | 1 | yes | d (of v78) |
| v80 [2026-12-31] | ai-capex | Can the NVIDIA-partnered coalition source at least $500 billion in financing for AI infrastructure by December 31, 2026? | financing_amount / Coalition financing for AI infrastructure / 2026 | NVIDIA-partnered AI infrastructure financing coalition | 4 | 1 | yes | c |
| v81 [2027-02-28] | ai-capex | Will the four largest hyperscalers’ combined calendar-2026 capital spending fall into which range, given the article’s estimate that it is tracking near $745 billion? | spend_total / Combined capital spending by the four largest hyperscalers / 2026 | 2026 hyperscaler capital-spending cycle; Cloud and hyperscaler AI-capex cycle | 1 | 1 | yes | d (of v1) |
| v82 [2027-03-31] | NVDA | Will IBM bring its planned NVIDIA HGX B300 cluster for Together AI online on IBM Cloud by March 31, 2027? | event / IBM Cloud deployment … / deployment | IBM Cloud–Together AI HGX B300 cluster deployment | 1 | 1 | yes | e (→ v3) |
| v83 [2028-03-31] | CRWV | Can continued customer demand and capacity deployment bring CoreWeave's FY2027 total revenue into which range? | total_revenue / – / 2027 | – | 6 | 1 | yes | a (succession of v72, unrecorded) |
| v84 [2026-12-31] | ai-capex | Will AI investment in calendar 2026 reach which range, given Goldman Sachs' estimate that it is approaching $600 billion? | spend_total / AI investment / 2026 | – | 1 | 1 | yes | d (of v1) |
| v85 [2027-12-31] | ai-capex | Will Amazon, Microsoft, and Google together spend which amount on CapEx in calendar 2026? | spend_total / Amazon, Microsoft, and Google combined CapEx / 2026 | Cloud and hyperscaler AI-capex cycle; 2026 hyperscaler capital-spending cycle | 1 | 1 | yes | d (of v1) |
| v86 [2027-03-31] | TSM | Can the strong first-half 2026 revenue growth sustain TSMC’s foundry segment revenue above NT$4.8 trillion in FY2026? | segment_revenue / foundry segment / 2026 TWD | – | 2 | 1 | yes | d (of v69) |
| v87 [2028-03-31] | TSM | Can the revenue growth reported in the first half of 2026 support continued growth in TSMC consolidated revenue in FY2027? | total_revenue / consolidated / 2027 TWD | – | 1 | 1 | yes | a (succession of v69, unrecorded) |
| v88 [2027-01-01] | ai-capex | Will total AI-related capital expenditures exceed $1 trillion in calendar 2026? | spend_total / Total AI-related capex / 2026 | Cloud and hyperscaler AI-capex cycle; 2026 hyperscaler capital-spending cycle | 1 | 1 | yes | d (of v1) |
| v89 [2027-12-31] | ai-capex | Can SpaceX's AI infrastructure investment bring cumulative compute capacity online to the stated 5–10 GW range by the end of 2027? | capacity / SpaceX cumulative compute capacity online / 2027 GW | SpaceX AI compute infrastructure expansion | 1 | 1 | yes | a (succession of v67; object should be SpaceX) |
| v90 [2027-12-31] | NVDA | Will NVIDIA and Uber reach the stated target of 100,000 Level 4-ready vehicles by December 31, 2027, supporting NVIDIA's automotive business? | event / NVIDIA-Uber Level 4-ready vehicle deployment / deployment | NVIDIA-Uber Level 4-ready vehicle rollout | 1 | 1 | yes | e |

Data defects seen while building the table (each is a lead, cited to the row):
- Due day one year late on FY2027 quantities: v9, v10, v11 have `due_day` 2028-02-24 while v2–v6 for the same fiscal year have 2027-02-24 (`L:views.due_day`). v18, v65, v85 (calendar-2026 quantities) are due 2027-12-31; v88 is due 2027-01-01.
- Inverted ladder: v48 rung 1 "Strongly bullish :: FY2026 total revenue is below $800 billion" and rung 5 "Strongly bearish :: … at least $920 billion" (`L:rungs` view_id v48).
- Identical ladders for two "different" theses: v24 and v25 both run $280/260/240/220 bn (`L:rungs`).
- Stale bogey: v6 asks about the 7%–19% range; the May guidance 16%–18% (e33) replaced e15 on v6 but also opened v12 as a new thesis (`L:replacements`, `L:views` v12).
- Grouping: v64 (Indonesia) sits in group "NAVER GAK Sejong AI factory expansion" (`L:thesis_group_members` g5).
- Empty tables: `L:successions` 0 rows and `L:dependencies` 0 rows, although v83/v87/v89 are next-year successors and the per-company capex theses (v20, v27, v45) are components of v1.
- 3 candidates were refused as "year FY2028 is beyond next year: not opened (06-views 不开)" (`L:handovers.dropped`), yet event theses due in 2028 (v16, v19) were opened; the year rule bites numeric candidates only.

### Inferences
- The two NVDA revenue theses absorb half of all evidence because the extractor links nearly every NVDA-positive sentence to "FY2027 total revenue" and "FY2027 data-center revenue" (the Morningstar note alone adds six third_party_view links to both; `L:evidence` e136–e140). With 24 judgements each, these two theses are also the only ones re-judged often.
- 59 of 90 theses have exactly one judgement and one to three links, which means most of the ledger is single-source theses opened from one sentence and never revisited.

### Gaps
- `L:view_switches.open` is 1 for every row; the pull-mode close is not built, so "open/closed" carries no information yet.
- I did not read all 227 judgement texts; the rung column is from the latest row per thesis only where quoted in Q4.

---

## Q2. Classification of each thesis (analyst reading, not gold)

### Takeaway
Of 90 theses, 25 are debates an analyst would track (class a), 27 are financial lines that are evidence not theses (b), 4 are too coarse or cannot be settled on a dated print (c), 17 duplicate another thesis in the ledger (d), and 17 are named projects or events that belong as evidence to a bigger question (e). Only about 28% of the ledger is at hedge-fund granularity, and even the 25 "a" rows include 7 with an object, wording or due-date defect.

### Cited Findings
Tests applied (from `A-thesis-anatomy.md` "Synthesis", lines 1–8 and 13): one disagreement on one driver with a dated settling print; split when settled by different prints, merge when always resolving together; too coarse when it cannot be put on a dated print, too fine when nobody prices it; themes as one dated ladder plus a stated link to each company view.

Class (a) — a real debate an analyst would track; settling print in brackets. 25 rows.
- v1 top-five 2026 capex [each company's Q4-2026 report, Jan–Feb 2027]. The one aggregate to keep (see Q3).
- v3 NVDA FY27 data-center revenue [NVDA Q4 FY27 release, Feb 2027]. The central NVDA debate; the extractor's own hub.
- v4 NVDA FY27 non-GAAP gross margin [same print]. Synthesis line 6 names margin as a separate debate.
- v7 Vera Rubin production shipments by 2026-12-31 [NVDA Q3 FY27 call, Nov 2026]. Timing debate (Hopper→Blackwell→Rubin).
- v8 H200 to China [FY27 close]. Real debate, defective wording: asks whether the U.S. "allows imports", but the quote behind it (e10) says the U.S. approved licences and "we do not know whether any imports will be allowed into China" — the open side is Beijing's. The latest judgement set rung 1 "established" on a U.S. licence report (`L:judgements` v8, 2026-08-12), so the thesis settled on the half that was never in doubt.
- v11 NVDA FY27 standalone Vera CPU revenue vs ~$20 bn [FY27 release; may be "no data to verify" if not disclosed]. A new product line with a management bogey; priced.
- v20 Alphabet 2026 capex [GOOGL Q4-2026 release]. Real, but filed under object `ai-capex` instead of GOOGL; a component of v1, not a theme.
- v22 2027 hyperscaler data-center capex [companies' FY2027 reports, Feb 2028]. The 2027 question that decides NVDA FY28; one is enough.
- v27 META FY26 capex [META Q4-2026, late Jan 2027]. Component of v1.
- v30 MSFT Intelligent Cloud FY27 revenue [MSFT Q4 FY27, Jul 2027]. The Azure proxy; a demand print.
- v32 MSFT FY27 operating margin [same]. Margin dilution from AI capex is MSFT's live debate.
- v44 AWS FY26 revenue [AMZN Q4-2026]. The AWS growth debate.
- v45 AMZN FY26 cash capex ~$220 bn [same]. Component of v1.
- v53, v54 AMD Data Center FY26 / FY27 [AMD Q4 reports]. The share-vs-NVDA debate; this-year and next-year are both allowed (06-views Ladder rule 5).
- v58 Helios initial shipments by 2026-09-30 [AMD Q3-2026 call, early Nov 2026]. AMD's Rubin-timing analogue.
- v66 U.S. 2026 average unemployment [BLS January 2027 release]. A legitimate macro theme ladder; nothing depends on it (`L:dependencies` empty).
- v67, v89 SpaceX compute capacity end-2026 / end-2027 [SpaceX Q4 reports]. SpaceX as a "sixth hyperscaler" buying NVDA exclusively (e519) is priced; object should be SpaceX/SPCX, not `ai-capex`.
- v69, v87 TSMC FY26 / FY27 consolidated revenue (TWD) [TSMC January revenue reports]. TSMC's print; v87 is the next-year successor but `L:successions` has no row.
- v72, v83 CoreWeave FY26 / FY27 revenue [CRWV Q4 reports]. Neocloud demand; v83 likewise an unrecorded successor.
- v74 CoreWeave FY26 capex $35–39 bn [same]. What CRWV buys from NVDA.
- v78 SMCI FY27 revenue $65–72 bn [SMCI Q4 FY27, Aug 2027]. The company's own guided print.

Class (b) — a financial line, evidence not thesis (too fine). 27 rows: v5 (NVDA opex growth), v6 (NVDA tax), v10 (NVDA capex), v13, v14 (Intel revenue lines from a 10-Q run rate, no argued view), v24 (META revenue), v26 (META expenses), v28 (META tax), v29 (MSFT revenue), v31 (MSFT opex), v33 (MSFT tax), v34, v35, v36, v37 (M365, Server, Windows OEM, Xbox growth lines), v38 (META operating income from annualised H1), v39 (MSFT PBP segment), v42 (Reality Labs loss; a META debate, not one in an NVDA corpus), v48 (AMZN revenue, inverted ladder), v52, v60 (AMD total revenue — AMD's debate is Data Center), v57 (AMD Client), v61 (AMD tax), v73 (CRWV adjusted operating income), v75 (CRWV run-rate), v76 (CRWV active power; a KPI that resolves with v74), v77 (CRWV inference ARR). Common mark: every one of these came out of a transcript or filing's guidance list; none has a disagreement attached (synthesis line 1).

Class (c) — too coarse or no dated print. 4 rows:
- v17 "combined booked revenue from Blackwell and Rubin in calendar 2025–2027" — the $1 trillion bogey is a real street number, but "booked revenue" across three calendar years is not a reported line; it cannot be put on a print. Reframe as FY27 and FY28 data-center revenue (v3 already holds FY27).
- v50 "total AI spending worldwide 2027" — no owner, no print.
- v56 AMD "value of new design wins in 2026 > $18 bn" — a management talking point, never reported as a line.
- v80 "coalition sources at least $500 billion in financing by 2026-12-31" — no print reports "financing sourced"; the real debate (vendor/circular financing) has a dated print only as NVDA's disclosed guarantees and commitments in its 10-Q/10-K.

Class (d) — duplicate or near-duplicate. 17 rows: v2 (of v3: NVDA total and data-center revenue always resolve together, DC ≈ 90% of revenue), v9 (of v3: Compute & Networking ≈ Data Center plus a sliver), v12 (of v6), v18, v41, v81, v84, v85, v88, v40 (all of v1, see Q3), v51 (sum of v20 + v45), v65 (of v45: same Amazon $220 bn, object `ai-capex` instead of AMZN), v70 (of v22), v25 (of v24; identical ladder), v55 (inside v54), v79 (of v78; the segment is most of SMCI revenue), v86 (of v69; the ledger's own evidence e518 says TSMC "has only one operating segment, the foundry segment").

Class (e) — named project or event that is evidence to a bigger question. 17 rows, with the question it feeds: v15 SK Telecom first factory (→ v3 and a sovereign-AI/Korea demand question); v16 NAVER 200 MW by 2028 (→ v3; 2028 is beyond the 6–12-month horizon in 06-views Ladder rule 6); v19 Rosa CPU 2028 (→ roadmap/v11); v21 RTX Spark shipments (→ gaming, nobody prices); v23 Taiwan restrictions (→ the China question; one clause in a smuggling story); v43 El Paso closing (→ v27); v46 AWS power doubling (→ v45); v47 Amazon Leo, v49 Globalstar, v63 BIS black-mass order, v71 Sony–TSMC JV (→ nothing in this corpus; out of purpose); v59 Anthropic 1 GW MI450 (→ v54); v62 Starmind launch (→ v3/v7, curiosity); v64 Zankore 200 MW, v68 Firebird 300 MW, v82 IBM B300 cluster (→ v3; each under 1% of a year's data-center revenue); v90 Uber 100k L4 vehicles (→ automotive, not DC).

Counts: a 25, b 27, c 4, d 17, e 17 = 90.

### Inferences
- Under the 2–4-per-name rule (synthesis lines 9–11), the NVDA set should be about four: data-center revenue (v3), gross margin (v4), Rubin timing (v7), China (v8 fixed plus a numeric China-revenue sibling). The ledger holds 22 NVDA rows; 18 are b/c/d/e.
- Class (b) is produced almost entirely by the guidance paragraph of a call or press release: the MSFT call alone yielded nine theses, seven of them (b), and missed MSFT's capex (see Q5).
- Class (e) is produced by NVIDIA newsroom/blog "AI factory" announcements: five deployment events (v15, v16, v64, v68, v82) all of which are the same phenomenon, sovereign/neocloud buildouts feeding v3.

### Gaps
- Whether a thesis is "priced" is my judgement from the texts and the synthesis, not a measurement of sell-side coverage; no estimate-dispersion data exists in the corpus.

---

## Q3. The ai-capex aggregate problem

### Takeaway
Nine calendar-2026 aggregate-spending theses sit side by side under `ai-capex`, each from one sentence in one article, with different populations (3, 4, 5, "tech giants", "AI investment", "total AI-related", "incl. OpenAI and Anthropic") and different rung boundaries; the same ~$730–745 bn estimate lands in rung 4, rung 4 and rung 3 on three of them. An analyst keeps one 2026 aggregate (v1) and one 2027 aggregate (v22), with the per-company guidance theses (GOOGL, AMZN, META, and a missing MSFT and ORCL) as components linked by dependency; the other seven 2026 rows and v70/v50 are evidence to those, not theses.

### Cited Findings

Side by side (`L:views`, `L:view_keys`, `L:rungs`, `L:evidence_sources`; period = calendar 2026 unless stated):

| id | population (scope) | bogey in question | neutral rung | due | source item | links/judg | latest rung |
|---|---|---|---|---|---|---|---|
| v1 | Top five cloud providers and hyperscalers | ~$700 bn (analyst expectations, said by NVDA CFO) | r3 $600–700 bn; r4 $700–800 bn | 2027-02-28 | NVDA call 2026-02-25 (e9) | 7/3 | 4 |
| v18 | Tech giants’ AI infrastructure spending | >$700 bn | r3 $600–800 bn | 2027-12-31 | Reuters 2026-07-26 `gnews:b25b5b3109fbe06f1a394164` (e102, a background clause in the Ohio story) | 8/4 | 3 |
| v40 | Major cloud infrastructure providers incl. hyperscalers, OpenAI, Anthropic | ~$1 tn (Futuriom: "$3 trillion over the next few years, or about an average of $1 trillion per year") | r3 $900 bn–1.1 tn | 2027-02-01 | Futuriom 2026-07-29 `gnews:e6eab7a05d5c77130cb231ca` (e239) | 3/2 | – |
| v41 | Alphabet, Amazon, Meta, Microsoft, Oracle | >$690 bn (FactSet) | r3 $650–730 bn; r4 $730–800 bn | 2027-03-31 | Yahoo 2026-07-29 `gnews:b5b9996d85745b7ba41d94a7` (e244) | 4/3 | 4 |
| v51 | Alphabet and Amazon combined "spending on upgrading their AI platforms" | ~$400 bn | r3 $380–420 bn | 2026-12-31 | Fool 2026-08-01 `gnews:f0ded626a98986d022fd2c30` (e307) | 1/1 | – |
| v81 | Four largest hyperscalers | ~$745 bn (24/7 Wall St.) | r3 $700–790 bn | 2027-02-28 | 247wallst 2026-08-11 `gnews:61ba718265df905f5dcc9dad` (e459) | 1/1 | 3 |
| v84 | "AI investment" | ~$600 bn (Goldman) | r3 $500–700 bn | 2026-12-31 | Fortune 2026-08-12 `gnews:c24969942ce8886f9557c571` (e483) | 1/1 | – |
| v85 | Amazon, Microsoft, Google | ~$600 bn (UncoverAlpha) | r3 $550–650 bn | 2027-12-31 | UncoverAlpha 2026-08-13 `gnews:dcc5556122de8bb36a458f29` (e512) | 1/1 | – |
| v88 | Total AI-related capex | >$1 tn (Goldman, via Fool) | r3 $900 bn–1 tn | 2027-01-01 | Fool 2026-08-15 `gnews:4a6db5f4d17bc985e47b0e49` (e526) | 1/1 | – |
| 2027: v22 | AI hyperscalers' data-center capex | ≥$1 tn (attributed to NVDA) | r3 $900 bn–1.1 tn | 2028-02-24 | Fool 2026-07-28 `gnews:12a7091502c000f87f96eca1` (e187) | 3/3 | – |
| 2027: v50 | Total AI spending worldwide | $1 tn (Jensen Huang) | r3 $950 bn–1.05 tn | 2027-12-31 | Fool 2026-08-01 (e306) | 1/1 | – |
| 2027: v70 | Hyperscaler capital expenditure on AI | >$1 tn (unattributed) | r3 $900 bn–1.1 tn | 2027-12-31 | PYMNTS 2026-08-10 `gnews:76e151efcc88dd5dbb954869` (e410) | 2/2 | – |

Per-company 2026 capex theses that are the aggregate's components: v20 Alphabet $195–205 bn (object `ai-capex`), v27 META $130–145 bn (object META), v45 AMZN cash capex ~$220 bn (object AMZN), v65 AMZN $220 bn again (object `ai-capex`), v74 CoreWeave $35–39 bn. Missing: MSFT, although the MSFT call stated "CY2026 CapEx expectation to approximately $175 billion" (e218, linked to v1 and v18, no MSFT thesis); Oracle, although 11 Oracle-titled items exist in `I:items`.

Same estimate, three rungs: Wall Street's ~$733 bn (e502) put v41 at rung 4 ("above the rung's $730 billion threshold", `L:judgements` v41 2026-08-13); the $745 bn estimate put v81 at rung 3; Reuters' ">$730 bn" kept v18 at rung 3; v1 sits at rung 4 on the same family of numbers.

The ledger's own matching gold already decided these are different populations: `week-benchmark-v23-2026-10-25.json` labels `gnews:b25b5b3109fbe06f1a394164|c1` gold "new" with reason "tech giants' AI infrastructure spending vs top-five cloud capex: related populations, not the same (identity gold 2026-10-25)", and `gnews:12a7091502c000f87f96eca1|c2` "either succession or new" (`/Users/lchingen/hivemind/poc/eval/gold/week-benchmark-v23-2026-10-25.json`).

### Inferences
- The matching gold answers the identity question correctly for a code-owned matcher (different populations are not byte-identical quantities). The granularity question is upstream of it: an analyst never opens "tech giants' AI spending" as a second thesis in the first place; it is one more estimate of the same debate ("how much will the big spenders spend in 2026"), with the population difference recorded on the evidence. Keeping v1 as the one 2026 question, with each per-company guidance (v20, v27, v45, MSFT $175 bn, ORCL) as a dependant component, follows synthesis line 13.
- What an analyst would keep separate from v1: the 2027 aggregate (v22; different print year), SpaceX capacity (v67/v89; a different buyer class), and the financing question (v80 reframed; a different driver: who pays, not how much).
- What is one question: v1 = v18 = v41 = v81 = v85 = v84 = v88 = v40 (all 2026 big-spender capex, populations 3/4/5/"tech giants"/"total AI"); v22 = v70 (= v50 if "total AI spending" is read as hyperscaler capex, which the source sentence does not support).
- The rung-boundary drift (r3 top at $700, $730, $790, $800 bn across duplicates) means the duplicates also disagree about the state of the same world; a merged thesis with one ladder removes the disagreement at no cost.

### Gaps
- No item in the processed window carries Oracle's own FY2027 capex guidance in a form the extractor saw (the 11 Oracle-titled items were not inspected one by one).

---

## Q4. Candidate golden examples for an extraction gold (14)

### Takeaway
Fourteen source items from `I:items` cover the cases the team asked for. The gold pattern that repeats across them: a company's own annual guidance for its main driver is a thesis; a journalist's aggregate, a quarterly outlook, an analyst's view, and a named deployment are evidence; a project milestone becomes its own question only when it is 6–12 months out and its size would move the company's print. Every gold below is an assistant's analyst reading, to be checked by a human before use.

### Cited Findings

Format per example: item (id, title, publication day); key passage (verbatim, ≤60 words); gold thesis/theses; attach-as-evidence targets; must NOT be extracted; what the system did (`L:views.created_from_input`, `L:evidence_sources`, `L:evidence_links`, `L:processing_steps`).

G1. NAVER GAK Sejong — `I:items nvidianews:naver-nvidia-and-brookfield-to-expand-koreas-national-ai-factory-infrastructure-buildout`, "NAVER, NVIDIA and Brookfield to Expand Korea’s National AI Factory Infrastructure Buildout", 2026-07-24.
- Passage: "NAVER and NVIDIA team plan to expand the initial NVIDIA DSX AI factory buildout at GAK Sejong data center from 55 megawatts to 200 megawatts by 2028. … NVIDIA plans to invest $1 billion into NAVER Corp. Brookfield has entered into a nonbinding term sheet to fund up to $9 billion."
- Gold theses: none new. (If a sovereign-AI demand question existed, e.g. "NVDA FY2027 sovereign AI revenue vs the >$30 bn FY2026 base" from the Feb call, this is evidence to it.)
- Attach as evidence: v3 (FY27 data-center revenue; party_statement, demand), v7 (Rubin: "expected to feature … Vera Rubin and Blackwell platforms"), and a vendor-financing/strategic-investment thesis (the $1 bn NAVER stake) once one exists (see G3).
- Must not extract: a 2028 200 MW milestone thesis (v16); the 55 MW base; Brookfield's $9 bn nonbinding term sheet; the 1 GW intent.
- System did: opened v16 (due 2028-12-31) and group g5; evidence e56, e57, e58 each linked to v16 and v3; the $1 bn investment and the HBM/financing angle were not extracted; a later Bloomberg retelling (`gnews:c46e192520be10cb02a54ca8`) was handled as "late older statement, not linked" (`L:late_statements` id 2).

G2. SK Group AI factory partnership — `I:items nvidianews:sk-group-and-nvidia-expand-strategic-partnership-across-ai-factories-and-next-generation-memory`, 2026-07-24.
- Passage: "SK Group and NVIDIA today announced plans for a $500-billion-plus comprehensive partnership … This cloud will use the NVIDIA DSX platform and deploy NVIDIA Vera Rubin accelerated computing powered by SK hynix HBM4, with the first AI factory planned to come online in 2027."
- Gold theses: none new. "First factory online in 2027" is a milestone 17 months out with no size attached; "$500-billion-plus" is a letter-of-intent headline, not a quantity with a print.
- Attach as evidence: v3 (demand), v7 (Rubin rollout; the first factory is Vera Rubin), v4 (gross margin: a long-term HBM4 supply partnership is a memory-cost input).
- Must not extract: v15 (SK Telecom first factory by 2027-12-31); a $500 bn thesis; 2 GW as a quantity thesis.
- System did: opened v15 and group g4; e53 (the $500 bn LOI) linked only to v15; e54 linked to v15, v7, v17; e55 to v15; nothing to v4.

G3. Ohio data-center financing: three items on one story.
- `I:items gnews:9e7560cfe0a707f9c14c7071`, Tom's Hardware, 2026-07-27, "Nvidia weighs $250 billion guarantee so OpenAI can lease SoftBank's 10-gigawatt Ohio campus … $350 billion deal to finance chips". Passage: "The $250bn guarantee covers the lease for the centre but does not cover the chips within the centre, which are worth another $350bn. However, Jensen Huang-led Nvidia said it is also in talks for that as well."
- `I:items gnews:3561dee8ab82ef4e42d8e315`, Quartz, 2026-07-27. Passage: "the full cost — including chips — could exceed $500 billion … Under the terms being discussed, the $250 billion commitment would apply to the lease and construction financing, leaving the cost of the chips themselves outside it."
- `I:items gnews:b25b5b3109fbe06f1a394164`, Reuters, 2026-07-26. Passage: "The deal underscores a broader shift as tech giants increasingly tap debt and equity markets to fund AI infrastructure, with spending set to top $700 billion this year."
- Gold thesis (one, asset, NVDA, yes/no): "Will NVIDIA have entered a financing guarantee or backstop for OpenAI's Ohio (SB Energy, Piketon) data-center campus by 2026-12-31?" Settling print: NVDA's announcement or the commitments-and-contingencies note of the next 10-Q/10-K. This is the "circular financing" debate the whole week was about (`I:items` has 20+ items on it, 2026-07-26..29).
- Attach as evidence: the $250 bn guarantee (lease/construction), the separate $350 bn chip-financing talks, and the >$500 bn total project cost are three facts about one deal — evidence on the one thesis, tiers rumour/third_party_view; Reuters' ">$700 billion" clause is evidence to v1; NVIDIA's $30 bn OpenAI stake and $62.6 bn cash are evidence (fact) to the same financing thesis, not to v2.
- Must not extract: a "tech giants' spending > $700 bn" thesis (v18); separate theses for $250 bn, $350 bn, $500 bn; OpenAI's "$750 bn compute spend through 2030".
- System did: Reuters item → opened v18 from the background clause and nothing on the financing story; Tom's Hardware → 4 evidence (e126, e127, e166 → v3; e167 → v2), 0 candidates, 2 evidence dropped ("links to nothing shown"); Quartz → 0 evidence, 0 candidates ("nothing to match"). No financing thesis exists in the ledger until v80 on 2026-08-11 (G12).

G4. Hyperscaler capex figures (the aggregate family).
- `I:items truenorth:transcript:NVDA:2026-02-25`, "NVDA Q4 FY2026 Earnings Call". Passage: "Analyst expectations for 2026 CapEx across the top 5 cloud providers and hyperscalers who collectively account for a little over 50% of our data center revenue are up nearly $120 billion since the start of the year and approaching $700 billion."
- `I:items gnews:61ba718265df905f5dcc9dad`, 247wallst, 2026-08-11. Passage: "Combined 2026 capital spending across the four largest hyperscalers is tracking near $745 billion".
- `I:items gnews:b5b9996d85745b7ba41d94a7`, Yahoo, 2026-07-29. Passage: "FactSet estimates combined 2026 capital expenditures by Alphabet (GOOGL), Amazon (AMZN), Meta Platforms (META), Microsoft (MSFT), and Oracle (ORCL) could exceed $690 billion."
- `I:items gnews:4a6db5f4d17bc985e47b0e49`, Fool, 2026-08-15. Passage: "those hyperscalers are forecast to invest about $800 billion in AI infrastructure in 2026, while total AI-related capex is projected to top $1 trillion, according to Goldman Sachs."
- Gold thesis: one, v1 as written (theme, top-five 2026 capex, five rungs around $700 bn, due at the last of the five Q4-2026 reports). Per-company guidance theses (GOOGL, AMZN, META, MSFT, ORCL 2026 capex) as asset theses on their own objects, each a dependant of v1.
- Attach as evidence: every later aggregate estimate ($690 bn FactSet, $745 bn, $733 bn, Goldman $800 bn/$1 tn, UncoverAlpha $600 bn for three) → v1 as third_party_view with the population named in the evidence line; the company's own guidance (Alphabet $195–205 bn, Amazon $220 bn, Microsoft ~$175 bn, Meta $130–145 bn) → its own company thesis and, as a part, v1.
- Must not extract: a new theme per population (v18, v40, v41, v51, v81, v84, v85, v88).
- System did: nine 2026 aggregate theses (Q3 table); MSFT's own $175 bn guidance (e218) linked to v1 and v18 but opened no MSFT thesis; Amazon's $220 bn opened both v45 (AMZN) and v65 (ai-capex).

G5. China H20/H200 — `I:items truenorth:transcript:NVDA:2026-02-25` and `I:items edgar:NVDA:0001045810-26-000051:q1fy27cfocommentary.htm` (NVDA 8-K EX-99.2, 2026-05-20).
- Passages: "While small amounts of H200 products for China-based customers were approved by the U.S. government, we have yet to generate any revenue. And we do not know whether any imports will be allowed into China." (Feb call, e10). "No shipments of Data Center Hopper products to China occurred during the quarter, compared with $4.6 billion in the first quarter of fiscal year 2026." and "We are not assuming any Data Center compute revenue from China in our outlook." (May CFO commentary.)
- Gold theses (two): (i) asset, NVDA, numeric: "How will NVDA FY2027 China data-center compute revenue compare with FY2026?" — the PRD's own example (06-views, Two thesis kinds), five rungs, due at the FY27 Q4 release; (ii) theme, chip-export-controls: the PRD's five-stage licensing ladder ("Full ban … Licences no longer required") as of a dated check, with (i) depending on it.
- Attach as evidence: the Feb and May statements (party_statement) to both; "$4.6 billion in Q1 FY2026 vs none" (fact) to (i); the $4.5 bn H20 inventory charge (fact) to v4 (gross margin), not to a thesis of its own; the Aug 18–20 "H200 chips reach China" stories (`gnews:85ac2808476ce47e9567242b`, `gnews:47ea36611625c4c711fca5ee`) to both — they are outside the processed window and headline-only (60 chars), so the system never saw them.
- Must not extract: a yes/no on "U.S. authorities allow imports" (v8's wording conflates the U.S. licence, already granted, with China's import permission); Taiwan "weighing tighter policies" as a thesis (v23) — it is one clause in a smuggling story and belongs as evidence to (ii).
- System did: v8 only (yes/no, group g3), judged "Rung 1 is established" on 2026-08-12 from a Bloomberg licence report (e268); e41 ("not assuming any Data Center compute revenue from China") linked to v2, v8, v3, v4, v11; no numeric China thesis; v23 opened from `gnews:f02b5d42ede081d1514a4777`.

G6. Quarterly earnings press release — `I:items edgar:NVDA:0001045810-26-000051:q1fy27pr.htm` (NVDA 8-K EX-99.1, 2026-05-20) with its CFO commentary (EX-99.2).
- Passage: "Revenue is expected to be $91.0 billion, plus or minus 2%. NVIDIA is not assuming any Data Center compute revenue from China in its outlook. • GAAP and non-GAAP gross margins are expected to be 74.9% and 75.0%, respectively … For the full year fiscal 2027, NVIDIA expects GAAP and non-GAAP tax rates to be between 16.0% and 18.0%".
- Gold theses: none new (06-views Ladder rule 6: "Intermediate quarterly reports are evidence, not separate theses").
- Attach as evidence: Q2 revenue guide $91.0 bn → v3 (and v2 if kept); GM guide 75.0% → v4; Q1 data-center $75.2 bn (fact) → v3; "not assuming China" → the China theses (G5); FY27 tax 16–18% → replaces the Feb 7–19% statement on v6 if v6 is kept at all.
- Must not extract: a second tax-rate thesis on a GAAP basis (v12); a Compute & Networking segment thesis (v9, from the Q4 FY26 commentary); Q2 opex $8.5 bn; the dividend increase and $80 bn buyback as theses.
- System did: press release → 7 evidence, 0 candidates (correct), with e41 fanned to five theses and e40 (Q1 revenue) to v2, v3, v4; CFO commentary → opened v12 (GAAP tax) and linked e37 (C&N $74.55 bn) to v9; e33 replaced e15 on v6 and was also linked to v12 (`L:replacements`).

G7. Analyst-opinion news piece — `I:items gnews:ba8e52b6f010b77f770e4483`, Morningstar, "Nvidia: Reported OpenAI Deal Raises Circular Deal Fears, but We Think the Stock Is Undervalued", 2026-07-27.
- Passage: "We maintain our $280 fair value estimate for wide-moat Nvidia … Our understanding is that Nvidia is providing backstops to some neoclouds, enabling them to receive better financing terms for buildouts in exchange for sharing some of their AI hosting revenue with Nvidia. Sharon AI and Firmus are two such deals".
- Gold theses: none. A fair-value estimate is a view on the stock, not a question with a print; the product rule (AGENTS §8) says a thesis is an argued view about the business, and the arguments here are about demand and financing, which already have homes.
- Attach as evidence: one third_party_view line on demand ("token usage continues to rise … hosting companies appear computing constrained") → v3; one on the neocloud backstops (Sharon AI, Firmus) → the financing thesis (G3); the $280 fair value → nothing.
- Must not extract: six separate evidence rows each linked to both v2 and v3 (the same opinion restated five ways); any thesis.
- System did: 6 evidence (e119 rumour; e136–e140 third_party_view) every one linked to v2 and v3; 0 candidates; 2 evidence dropped. The MarketWatch sibling `gnews:bb0d23846735c94b7c1722d2` (Seaport's Jay Goldberg: "These kinds of financing usually don't end well") produced 0 evidence, 3 dropped — the opposing view on the same debate was lost while the supportive one was linked six times.

G8. SpaceX compute capacity — `I:items gnews:c475c48b857a2b98a73dd2c4`, Zacks, 2026-08-07; `I:items gnews:4a6db5f4d17bc985e47b0e49`, Fool, 2026-08-15; `I:items gnews:f2bbeb9e369dca841a5a0381`, Tom's Hardware, 2026-08-05.
- Passages: "SpaceX’s CapEx climbed to $18.4 billion in the second quarter from $10.1 billion in Q1, with approximately $15.8 billion earmarked for AI infrastructure … expects year-end compute capacity to exceed 2 gigawatts" (Zacks). "We expect to end this year with over 2 gigawatts of compute. And probably our cumulative compute online by the end of next year will be several times higher. It may … be closer to 10 gigawatts of compute than 5 gigawatts" (Musk, via Fool). "With respect to the Starmind AI satellite, which will be essentially an optimized Vera Rubin NVL72 computer … we expect to start launching this next year" (Tom's).
- Gold thesis (one, asset, object SpaceX/SPCX): "SpaceX compute capacity online at 2026-12-31 vs the stated >2 GW" — five rungs, due at SpaceX's Q4-2026 report; the 2027 5–10 GW statement is the next-year successor once 2026 closes (06-views rule 5 allows this year and next year).
- Attach as evidence: "exclusively NVIDIA chips" (e519, e345) → v3 and v7 (demand, Rubin); Q2 capex $18.4 bn and the $15.8 bn AI share → the SpaceX thesis; Starmind/NVL72-in-orbit → v7 as a Rubin-adoption statement, not a thesis.
- Must not extract: a Starmind-launch thesis (v62); Morgan Stanley's "$110 billion in 2028" estimate as a thesis; an `ai-capex` object for a company quantity.
- System did: v67 (object `ai-capex`, due 2026-12-31) from Zacks; v89 (object `ai-capex`) from the Fool piece; v62 (object NVDA) from Tom's; e345/e357 linked to v17, v62, v3; `L:review_pool_entries` also holds two "suggested_theme" rows for SpaceX compute capacity and 2027 data-center spending (ids 4, 7).

G9. TSMC FY-revenue succession — `I:items edgar:0001046179-26-000471:tsm-revenue20260810.htm` (TSM 6-K, 2026-08-10) and `I:items edgar:0001046179-26-000541:a2026q2consolidatedreport-.htm` (TSM 6-K EX-99.1, 2026-08-14).
- Passages: "revenue for July 2026 was approximately NT$467.58 billion … Revenue for January through July 2026 totaled NT$2,872.06 billion, an increase of 37.0 percent compared to the same period in 2025." / "The Company has only one operating segment, the foundry segment."
- Gold theses: one, TSMC FY2026 consolidated revenue (TWD) with a neutral rung around the run rate (v69 as written is acceptable). FY2027 may be opened as the next-year thesis only with a recorded succession to v69 (`L:successions`), and not from an H1 report that says nothing about 2027.
- Attach as evidence: the monthly revenue report (fact) → v69; H1 net sales NT$2,404.5 bn (fact) → v69.
- Must not extract: a "foundry segment" thesis (v86) when the filing itself states there is one segment; a FY2027 thesis from an H1 2026 report with no 2027 statement (v87).
- System did: v69 from the 6-K; v86 and v87 from the H1 report; e423 linked to v69, v86, v87; `L:successions` has 0 rows.

G10. CoreWeave: transcript and 10-Q — `I:items truenorth:transcript:CRWV:2026-08-11`, "CRWV Q2 FY2026 Earnings Call"; `I:items edgar:0001769628-26-000366:crwv-20260630.htm` (CRWV 10-Q, 2026-08-12).
- Passage: "raising our full year 2026 revenue guidance to $12.4 billion to $13.2 billion and adjusted operating income to $960 million to $1.15 billion … we now expect 2026 CapEx in the range of $35 billion to $39 billion. … raising our expected end of year annualized run rate revenue to $18.5 billion to $19.5 billion." / "We expect to exit 2026 with at least $250 million of managed inference ARR." / "Revenue backlog was approximately $104 billion as of June 30, 2026."
- Gold theses (two): CRWV FY2026 revenue vs guidance (v72 as written) and CRWV FY2026 capex $35–39 bn (v74 as written; it is NVDA GPU demand). FY2027 revenue (v83) only as a recorded succession.
- Attach as evidence: adjusted operating income, run-rate revenue, active power 1.85 GW, inference ARR, $104 bn backlog, OpenAI $6.5 bn and Meta $21 bn commitments → v72/v74 as party_statement or fact.
- Must not extract: v73, v75, v76, v77 (four KPI theses from one guidance paragraph).
- System did: six theses from the call (v72–v77), v83 from the 10-Q; e437 (backlog) linked to v72, v75, v83.

G11. MSFT transcript (the capex miss) — `I:items truenorth:transcript:MSFT:2026-07-29`.
- Passage: "Capital expenditures were $41 billion, including the impact from higher component pricing … Roughly 2/3 of our CapEx was for short-lived assets, primarily CPUs and GPUs" and, per the extracted evidence e218, Amy Hood's "CY2026 CapEx expectation to approximately $175 billion".
- Gold theses (two or three): MSFT CY2026 capex ~$175 bn (component of v1); Intelligent Cloud/Azure growth (v30 as written); optionally FY27 operating margin (v32).
- Attach as evidence: the $41 bn quarter, the 2/3 short-lived split, finance leases $5.6 bn → the capex thesis; all other guidance lines → v30/v32 or nothing.
- Must not extract: total revenue, opex growth, tax rate, M365, Server, Windows OEM, Xbox, PBP segment (v29, v31, v33–v37, v39: seven (b) theses and one (b) from the 8-K).
- System did: nine theses, none on capex; e218 ($175 bn) linked to v1 and v18 only.

G12. Financing coalition — `I:items gnews:3c4e68045b4ddbbf33c0c232`, Fortune/Bloomberg, "Nvidia taps Wall Street for $500 billion funding commitment", 2026-08-11.
- Passage: "US investment giants including Apollo Global Management Inc., Blackstone Inc., BlackRock Inc. and Brookfield Asset Management are partnering with Nvidia Corp. to source $500 billion in financing for artificial intelligence infrastructure … The deals will use compute power as collateral for the debt".
- Gold thesis: the one financing question from G3, reframed on a print: e.g. "Will NVIDIA's disclosed guarantees, backstops and financing commitments to customers at FY2027 year-end exceed [X]?" (five rungs on the 10-K commitments note), or the yes/no on the Ohio guarantee. The coalition's "$500 billion sourced by 2026-12-31" has no print.
- Attach as evidence: the coalition statement, the collateral structure, the "few details on timing and structure" caveat → that thesis.
- Must not extract: v80 as written (financing_amount with no reporting line); nine near-copies of the same story (`gnews:c1d38bc1f4b7826a67f9e3be` produced 0 evidence; `gnews:c24969942ce8886f9557c571` produced v84 from the Goldman aside).
- System did: v80 (object `ai-capex`), e444–e447 → v80; 18 later evidence rows were dropped with "links to nothing shown: ['v80']" (`L:handovers.dropped`), i.e. extractors kept pointing at v80 when it was not among the shown theses.

G13. META transcript — `I:items truenorth:transcript:META:2026-07-29`.
- Passage: "Capital expenditures, including principal payments on finance leases, were $31.1 billion, driven by investments in servers, data centers and network infrastructure." (Full-year guide $130–145 bn per v27's ladder.)
- Gold theses (one): META FY2026 capex (v27 as written), as a component of v1.
- Attach as evidence: Q2 capex $31.1 bn → v27; expense guide, tax, FoA revenue → nothing (or v27's context).
- Must not extract: v24, v25 (identical ladders), v26, v28; from the 8-K/10-Q: v38 (operating income from annualised H1), v42 (Reality Labs loss), v43 (El Paso closing → evidence to v27).
- System did: five theses from the call, three more from filings.

G14. AMD transcript — `I:items truenorth:transcript:AMD:2026-08-04`.
- Passage (from the extracted evidence lines): server revenue growth "more than 70%" in FY2027; new design wins "more than $18 billion" in 2026; "Initial Helios shipments" expected by Q3 2026; Anthropic "at least one gigawatt of MI450 GPUs in Helios".
- Gold theses (three): AMD Data Center FY2026 and FY2027 revenue (v53, v54) and Helios initial shipments by 2026-09-30 (v58).
- Attach as evidence: Anthropic 1 GW, OpenAI commitments, server growth >70%, design wins → v54/v58.
- Must not extract: v52, v60 (total revenue), v55 (server growth inside v54), v56 (design wins, no print), v57 (Client), v59 (Anthropic milestone), v61 (tax).
- System did: eight theses from the call, two more from the slides 8-K.

### Inferences
- Across G1–G14 the correct count of new theses is about 14 where the system opened 55; the rest of the system's output is evidence misfiled as theses. The matching stage then does its job on those: 95 of 102 candidates were "new", and the gold for the week agrees they are not the same quantity — the duplication is decided at extraction, not matching.
- A usable extraction gold needs three labels per candidate, not one: thesis / evidence-to-[id] / discard. Items G3, G5 and G7 also need an "opposing view, same thesis" label (06-views Rationale: "Opposing views move the same state's direction rather than creating opposite duplicate theses").

### Gaps
- The Aug 18–20 H200-to-China items are headline-only in `I:items` (60 chars) and outside the ledger's window; a China gold needs the NVDA Q2 FY27 call (`truenorth:transcript:NVDA:2026-08-26`, present in `I:` but not processed) or a full-text source.
- No Oracle guidance item was checked one by one; the ORCL component of v1 is asserted from the FactSet population, not from an Oracle filing in the corpus.
- The existing golds (`poc/eval/gold/*.json`: august-benchmark-v23, evidence-decisions-seed ×3, grouping-identity-gold, idea-gold, week-benchmark ×2) label matching and grouping decisions per candidate id; none labels whether a candidate should have been a candidate. Their shape (`"gold": "new"|"merge"|"succession"|"skip"`, `"why"`) can be reused with a new value set.

---

## Q5. Patterns: what the extractor over- and under-extracts

### Takeaway
Over-extraction is systematic in three forms: a thesis per guidance line (27 class-b theses, 23 of them from six transcripts), a thesis per published aggregate (9 of the 17 `ai-capex` rows), and a thesis per announced deployment (8 class-e deployment/launch events). Under-extraction is the mirror image: the drivers the street debates — China revenue as a number, MSFT and ORCL capex, the vendor-financing question, the opposing analyst view — were either never opened or opened late and unverifiably.

### Cited Findings

Over-extraction, with counts (`L:views`, `L:view_keys`, `L:handovers`):
1. Guidance-line theses from calls: transcripts are 8 of 480 extracted items but produced 43 of 102 candidates (`L:processing_steps` 'extracted' reasons by item class). The MSFT call → 9 theses (7 class b), AMD → 8 (6 b/d/e), CRWV → 6 (4 b), META → 5 (4 b/d), NVDA Feb → 8 (3 b), AMZN → 4 (2 b/e). Tax-rate theses alone: 5 (v6, v12, v28, v33, v61).
2. One thesis per aggregate estimate: 9 calendar-2026 spend_total theses and 3 for 2027 (Q3). Each has 1–8 links; all but v1 and v18 have a single judgement.
3. One thesis per deployment press release: v15, v16, v64, v68, v82 (AI-factory buildouts), v19, v21 (product launches), v62, v90 (SpaceX satellite, Uber vehicles). Eight of these have exactly one or three links and one judgement.
4. Duplicate quantities through basis or scope wording: v2/v3/v9 (total vs data-center vs Compute & Networking), v6/v12 (non-GAAP vs GAAP tax), v45/v65 (cash capex vs capex; object AMZN vs ai-capex), v69/v86 (consolidated vs the single "foundry segment"), v24/v25 (identical ladders).
5. Evidence fan-out to the two hub theses: 356 of 716 links go to v2/v3; 155 of 534 evidence rows are linked to more than one thesis; the Morningstar note's five opinion sentences became five rows each linked to both hubs (e136–e140).
6. Out-of-purpose objects: v47, v49, v63, v71 (Amazon Leo, Globalstar, BIS black mass, Sony–TSMC JV) and the macro v66 have no dependants and no connection to the corpus's question.

Under-extraction, with counts:
1. The China number: the PRD's own example thesis ("NVDA FY2027 China revenue vs FY2026", 06-views Two thesis kinds) does not exist; only the yes/no v8 does, and it was judged "established" on the U.S. licence half (`L:judgements` v8 2026-08-12). The disclosed facts that would feed it ("$4.6 billion in the first quarter of fiscal year 2026" vs none; "not assuming any Data Center compute revenue from China") were linked to v2/v3/v4/v8/v11 instead (e41).
2. Hyperscaler components: MSFT's stated CY2026 capex ~$175 bn (e218) opened no thesis while four journalists' aggregates did; Oracle has no thesis although it is named in v41's population and 11 Oracle-titled items exist.
3. The financing debate: 20+ items on 2026-07-26..29 about the $250 bn Ohio backstop produced no thesis; the Quartz and Spokesman items produced 0 evidence; v80 arrived 16 days later on an unverifiable "financing sourced" measure, after which 18 evidence rows were dropped as "links to nothing shown: ['v80']" (`L:handovers.dropped`).
4. Opposing views: the bearish analyst piece (`gnews:bb0d23846735c94b7c1722d2`, 0 evidence, 3 dropped) was lost; the bullish one (`gnews:ba8e52b6f010b77f770e4483`) got six links. Of 254 dropped handover rows, 249 are evidence ("links to nothing shown" ≈ 200; "quote not in item" ≈ 45) and only 5 are candidates (3 "year FY2028 beyond next year", 2 "due_day not after the item").
5. Memory/HBM cost as a margin input: the SK hynix HBM4 partnership (G2) and Amazon's "higher memory chip costs" (e370) were linked to deployment or capex theses, never to v4.
6. Successions and dependencies: `L:successions` and `L:dependencies` are empty although v83/v87/v89 are next-year successors and v20/v27/v45 are parts of v1; the 06-views design ("Succession", "Dependencies") is not exercised by this ledger.

### Inferences
- The extractor's unit is the sentence with a number and a period, not the disagreement. That one choice explains over-extraction forms 1–4 and the duplicate aggregates at once; a rule at the extraction decision ("open a thesis only for a company's own annual guidance on its main driver, an industry aggregate once per year, or a policy stage; everything else is evidence to a named thesis") would have cut the ledger from 90 to roughly 25–30 without losing a debate.
- The hub-linking (form 5) and the empty dependencies table are the same gap: with no dependency from "hyperscaler capex" or "China licensing" to "NVDA data-center revenue", the extractor expresses every indirect argument as a direct link to v3.

### Gaps
- Counts of dropped evidence by reason are approximate (reasons were tallied by prefix over `L:handovers.dropped`; exact split "links to nothing shown" vs "quote not in item" was not computed to the row).
- I did not re-send any model call or read the extraction prompts (`src/hivemind/prompts/`); the mechanism statements above are inferred from outputs, per the brief's read-only scope.

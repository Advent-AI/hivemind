# Extraction gold `extraction-admission-2026-10-26` against `/Users/lchingen/hivemind/poc/data/english-v23-jev-2026-10-25/views.sqlite`

Cases judged: 20; fail 10, full 3, partial 7; not processed 0

| case | title | score | baseline (v23) | missing must-open | extra opened | missing links | forbidden links | opened by items |
|---|---|---|---|---|---|---|---|---|
| A01 | One guidance paragraph is not one thesis per line (NVDA FY2027 gross margin) | **partial** | partial |  | Operating-expense growth thesis from the same paragraph (v5); Tax-rate thesis from the same paragraph (v6; v12 GAAP variant later); FY2027 total revenue beside the Data Center thesis (v2: the segment carries the value, the total is its shadow) |  |  | v1, v2, v3, v4, v5, v6, v7, v8 |
| A02 | Samples shipped is not production started (Vera Rubin) | **full** | full |  |  |  |  | v1, v2, v3, v4, v5, v6, v7, v8 |
| A03 | Export licence, import permission and revenue are three things (China H200) | **fail** | fail | NVDA FY2027 China data-center compute revenue vs FY2026 | "Will U.S. authorities allow H200 imports into China" (v8: mixes the granted U.S. licence with the open China permission) | 4\.6 billion; not assuming any Data Center compute revenue from China; 4\.5 billion charge associated with H20 |  | v1, v2, v3, v4, v5, v6, v7, v8, v12 |
| A04 | Five, four and three companies of capex are one aggregate | **partial** | fail |  | "About $1 trillion per year over the next few years" made into a 2026 $1tn thesis (v40) |  |  | v1, v2, v3, v4, v5, v6, v7, v8, v40, v41 |
| A05 | NAVER project announcement: zero new theses | **partial** | partial |  | 200 MW by 2028 milestone thesis (v16); Same milestone written on 2027 |  |  | v16 |
| A06 | SK project announcement: zero new theses, gross-margin input kept | **fail** | fail |  | SK Telecom first AI factory online by 2027-12-31 (v15) | HBM4 |  | v15 |
| A07 | Ohio: the lease guarantee and chip financing are NVDA's own risk | **fail** | fail | NVDA signs a binding lease or financing guarantee for the OpenAI Ohio (SB Energy, Piketon) campus by 2026-12-31 | "Tech giants' AI spending > $700bn" from the Reuters background clause (v18) | 250 ?b(illio)?n; 350 ?b(illio)?n; top \$700 billion | 62\.6 billion | v18 |
| A08 | Quarterly press release: all evidence, no new thesis | **partial** | partial |  | A second tax-rate thesis on a GAAP basis (v12) |  |  | v12 |
| A09 | Analyst opinion: one evidence line, not six; the opposing view is not dropped | **fail** | fail |  |  | Sharon AI|Firmus; don't end well |  |  |
| A10 | SpaceX compute: evidence to NVDA data-center demand, not three events | **fail** | fail |  | Starmind satellite launch as a thesis (v62); SpaceX capacity under the ai-capex object (v67); SpaceX 2027 capacity under the ai-capex object, opened early (v89) | 18\.4 billion; exclusively; Starmind|NVL72 |  | v62, v67, v88, v89 |
| A11 | TSMC: one segment, one revenue thesis; FY2027 only with a 2027 statement | **partial** | fail |  | "Foundry segment" revenue thesis when the filing says there is one segment (v86); FY2027 revenue thesis from an H1 2026 report with no 2027 statement (v87) |  |  | v69, v86, v87 |
| A12 | CoreWeave: keep the two crossings the street watches | **partial** | partial |  | Year-end annualized run-rate revenue as a parallel thesis (v75; it is the FY2027 starting point) |  |  | v72, v73, v74, v75, v76, v77, v83 |
| A13 | MSFT call: the one line the street argues about was not opened | **fail** | fail | MSFT calendar-2026 capex ~$175bn (component of the five-company aggregate) | Total revenue (v29); Opex growth (v31); Tax rate (v33); M365, Server, Windows OEM, Xbox growth lines (v34-v37) | 175 billion; 41 billion |  | v29, v30, v31, v32, v33, v34, v35, v36, v37 |
| A14 | AMD call: three core theses, five to seven extras | **partial** | partial |  | Total revenue FY2027 (v52); Design wins, no reporting line (v56); Anthropic first-gigawatt milestone as a thesis (v59) |  |  | v52, v53, v54, v55, v56, v57, v58, v59 |
| A15 | META call: capex is the one thesis this corpus needs | **fail** | partial |  | Total revenue (v24; same ladder as v25); Total expenses (v26); Tax rate (v28) | 31\.1 billion |  | v24, v25, v26, v27, v28 |
| A16 | CoreWeave managed-inference ARR: acceptable thesis, not required (alternatives only) | **full** | full |  |  |  |  | v72, v73, v74, v75, v76, v77 |
| A17 | Four-company $745bn is evidence to the five-company aggregate, not a new aggregate | **fail** | fail |  | Any new calendar-2026 aggregate from this article (v81: four largest hyperscalers) | 745 billion |  | v81 |
| A18 | Bloomberg retelling of the NAVER investment: a late statement, zero theses | **full** | full |  |  |  |  |  |
| A19 | Taiwan "weighing tighter policies": one clause in a smuggling story, evidence not thesis | **fail** | fail |  | Taiwan restrictions as an NVDA event thesis (v23); Same on the calendar year | weighing tighter policies |  | v23 |
| A20 | Goldman aggregates via the Fool: evidence to the 2026 aggregate; no new aggregate, no early 2027 | **fail** | fail |  | "Total AI-related capex > $1tn" as a tenth 2026 aggregate (v88); SpaceX 2027 capacity opened early under ai-capex (v89) | 800 billion |  | v88, v89 |

## Census

- theses: 90
- by object: {'AMD': 10, 'AMZN': 6, 'CRWV': 7, 'INTC': 2, 'META': 8, 'MSFT': 10, 'NVDA': 22, 'SMCI': 2, 'TSM': 4, 'ai-capex': 17, 'chip-export-controls': 1, 'us-recession-risk': 1}
- by measure: {'capacity': 2, 'capex': 4, 'design_wins': 1, 'event': 18, 'financing_amount': 1, 'gross_margin': 1, 'growth_rate': 7, 'operating_expense_growth': 2, 'operating_loss': 1, 'operating_margin': 1, 'other': 2, 'policy_event': 1, 'product_revenue': 2, 'run_rate': 2, 'segment_revenue': 11, 'shipments_or_capacity': 2, 'spend_total': 14, 'tax_rate': 5, 'total_expenses': 1, 'total_revenue': 12}
- by admission reason (handover candidates carrying opens_as): {}
- candidates that named a thesis in folds_into and still opened: 0
- one object, quantity and year held by several theses: {'CRWV run_rate 2026': 2, 'MSFT growth_rate FY2027': 4, 'MSFT segment_revenue FY2027': 2, 'NVDA segment_revenue FY2027': 2, 'NVDA tax_rate FY2027': 2, 'ai-capex spend_total 2026': 11, 'ai-capex spend_total 2027': 3}

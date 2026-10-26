# Extraction gold `extraction-admission-2026-10-26` against `/Users/lchingen/hivemind/poc/data/pinned-matching-2026-10-26/arm-v26-par/views.sqlite`

Cases judged: 20; fail 15, full 5; not processed 0

| case | title | score | baseline (v23) | missing must-open | extra opened | missing links | forbidden links | opened by items |
|---|---|---|---|---|---|---|---|---|
| A01 | One guidance paragraph is not one thesis per line (NVDA FY2027 gross margin) | **full** | partial |  |  |  |  | v1, v2, v3, v4, v5 |
| A02 | Samples shipped is not production started (Vera Rubin) | **full** | full |  |  |  |  | v1, v2, v3, v4, v5 |
| A03 | Export licence, import permission and revenue are three things (China H200) | **fail** | fail | NVDA FY2027 China data-center compute revenue vs FY2026 |  | 4\.6 billion; not assuming any Data Center compute revenue from China; 4\.5 billion charge associated with H20 |  | v1, v2, v3, v4, v5 |
| A04 | Five, four and three companies of capex are one aggregate | **fail** | fail |  |  | 690 billion |  | v1, v2, v3, v4, v5, v31 |
| A05 | NAVER project announcement: zero new theses | **full** | partial |  |  |  |  | v18 |
| A06 | SK project announcement: zero new theses, gross-margin input kept | **fail** | fail |  |  | HBM4 |  |  |
| A07 | Ohio: the lease guarantee and chip financing are NVDA's own risk | **fail** | fail |  |  | 350 ?b(illio)?n; top \$700 billion |  |  |
| A08 | Quarterly press release: all evidence, no new thesis | **fail** | partial |  |  | 91\.0 billion |  |  |
| A09 | Analyst opinion: one evidence line, not six; the opposing view is not dropped | **fail** | fail |  |  | Sharon AI|Firmus |  |  |
| A10 | SpaceX compute: evidence to NVDA data-center demand, not three events | **fail** | fail |  |  | 18\.4 billion; Starmind|NVL72 |  |  |
| A11 | TSMC: one segment, one revenue thesis; FY2027 only with a 2027 statement | **fail** | fail |  |  | 2,404,483,690|2,404\.5 |  | v42, v53, v54 |
| A12 | CoreWeave: keep the two crossings the street watches | **fail** | partial |  |  | 104 billion|103\.7 billion |  | v44, v45 |
| A13 | MSFT call: the one line the street argues about was not opened | **fail** | fail | MSFT calendar-2026 capex ~$175bn (component of the five-company aggregate); MSFT Intelligent Cloud FY2027 revenue, Azure proxy (v30) |  | 175 billion; 41 billion |  |  |
| A14 | AMD call: three core theses, five to seven extras | **fail** | partial | AMD Data Center segment FY2026 revenue (v53); AMD initial Helios shipments by 2026-09-30 (v58) |  | first gigawatt|2 gigawatts of MI450; Helios is now in production |  | v36, v37 |
| A15 | META call: capex is the one thesis this corpus needs | **full** | partial |  |  |  |  | v28 |
| A16 | CoreWeave managed-inference ARR: acceptable thesis, not required (alternatives only) | **fail** | full |  |  | 250 million |  | v44, v45 |
| A17 | Four-company $745bn is evidence to the five-company aggregate, not a new aggregate | **fail** | fail |  |  | 745 billion |  |  |
| A18 | Bloomberg retelling of the NAVER investment: a late statement, zero theses | **full** | full |  |  |  |  |  |
| A19 | Taiwan "weighing tighter policies": one clause in a smuggling story, evidence not thesis | **fail** | fail |  |  | weighing tighter policies |  |  |
| A20 | Goldman aggregates via the Fool: evidence to the 2026 aggregate; no new aggregate, no early 2027 | **fail** | fail |  |  | 800 billion |  |  |

## Census

- theses: 56
- by object: {'AMD': 3, 'AMZN': 2, 'CRWV': 2, 'INTC': 5, 'META': 1, 'MSFT': 1, 'NVDA': 22, 'SMCI': 3, 'TSM': 4, 'ai-capex': 4, 'chip-export-controls': 9}
- by measure: {'capex': 5, 'event': 19, 'gross_margin': 5, 'growth_rate': 2, 'operating_margin': 1, 'policy_event': 9, 'product_revenue': 1, 'segment_revenue': 7, 'spend_total': 4, 'total_revenue': 3}
- by admission reason (handover candidates carrying opens_as): {'binding_obligation': 19, 'industry_aggregate': 9, 'main_driver': 25, 'policy_stage': 18}
- candidates that named a thesis in folds_into and still opened: 0
- one object, quantity and year held by several theses: {'AMD growth_rate 2027': 2, 'INTC segment_revenue 2026': 2, 'NVDA segment_revenue FY2027': 2, 'ai-capex spend_total 2026': 3}

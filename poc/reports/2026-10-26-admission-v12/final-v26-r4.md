# Extraction gold `extraction-admission-2026-10-26` against `/Users/lchingen/hivemind/poc/data/english-v26-collision-r4-2026-10-26/views.sqlite`

Cases judged: 20; fail 16, full 4; not processed 0

| case | title | score | baseline (v23) | missing must-open | extra opened | missing links | forbidden links | opened by items |
|---|---|---|---|---|---|---|---|---|
| A01 | One guidance paragraph is not one thesis per line (NVDA FY2027 gross margin) | **full** | partial |  |  |  |  | v1, v2, v3, v4, v5 |
| A02 | Samples shipped is not production started (Vera Rubin) | **fail** | full | NVDA begins Vera Rubin production shipments by 2026-12-31 (second half of the year) |  | first Vera Rubin samples |  | v1, v2, v3, v4, v5 |
| A03 | Export licence, import permission and revenue are three things (China H200) | **fail** | fail | NVDA FY2027 China data-center compute revenue vs FY2026 |  | 4\.6 billion; not assuming any Data Center compute revenue from China; 4\.5 billion charge associated with H20 |  | v1, v2, v3, v4, v5 |
| A04 | Five, four and three companies of capex are one aggregate | **fail** | fail |  |  | 690 billion |  | v1, v2, v3, v4, v5 |
| A05 | NAVER project announcement: zero new theses | **fail** | partial |  |  | 55 megawatts to 200 megawatts |  | v13 |
| A06 | SK project announcement: zero new theses, gross-margin input kept | **fail** | fail |  |  | HBM4 |  |  |
| A07 | Ohio: the lease guarantee and chip financing are NVDA's own risk | **fail** | fail |  |  | top \$700 billion |  | v14 |
| A08 | Quarterly press release: all evidence, no new thesis | **full** | partial |  |  |  |  |  |
| A09 | Analyst opinion: one evidence line, not six; the opposing view is not dropped | **fail** | fail |  |  | Sharon AI|Firmus |  |  |
| A10 | SpaceX compute: evidence to NVDA data-center demand, not three events | **fail** | fail |  |  | 18\.4 billion |  |  |
| A11 | TSMC: one segment, one revenue thesis; FY2027 only with a 2027 statement | **fail** | fail |  |  | 2,404,483,690|2,404\.5 |  | v38 |
| A12 | CoreWeave: keep the two crossings the street watches | **fail** | partial | CRWV FY2026 total revenue vs the $12.4-13.2bn guidance (v72) |  | 12\.4 billion; 104 billion|103\.7 billion |  | v42 |
| A13 | MSFT call: the one line the street argues about was not opened | **fail** | fail | MSFT Intelligent Cloud FY2027 revenue, Azure proxy (v30) |  | 41 billion |  | v21 |
| A14 | AMD call: three core theses, five to seven extras | **fail** | partial | AMD Data Center segment FY2026 revenue (v53); AMD initial Helios shipments by 2026-09-30 (v58) |  | first gigawatt|2 gigawatts of MI450; Helios is now in production |  | v30, v31 |
| A15 | META call: capex is the one thesis this corpus needs | **fail** | partial |  |  | 31\.1 billion |  | v20 |
| A16 | CoreWeave managed-inference ARR: acceptable thesis, not required (alternatives only) | **fail** | full |  |  | 250 million |  | v42 |
| A17 | Four-company $745bn is evidence to the five-company aggregate, not a new aggregate | **full** | fail |  |  |  |  |  |
| A18 | Bloomberg retelling of the NAVER investment: a late statement, zero theses | **full** | full |  |  |  |  |  |
| A19 | Taiwan "weighing tighter policies": one clause in a smuggling story, evidence not thesis | **fail** | fail |  |  | weighing tighter policies |  |  |
| A20 | Goldman aggregates via the Fool: evidence to the 2026 aggregate; no new aggregate, no early 2027 | **fail** | fail |  |  | 800 billion |  |  |

## Census

- theses: 45
- by object: {'AMD': 4, 'AMZN': 3, 'CRWV': 1, 'INTC': 3, 'META': 2, 'MSFT': 3, 'NVDA': 19, 'SMCI': 2, 'TSM': 2, 'ai-capex': 3, 'chip-export-controls': 3}
- by measure: {'capex': 4, 'event': 16, 'gross_margin': 4, 'growth_rate': 2, 'policy_event': 3, 'product_revenue': 1, 'segment_revenue': 6, 'spend_total': 3, 'total_revenue': 6}
- by admission reason (handover candidates carrying opens_as): {'binding_obligation': 15, 'industry_aggregate': 11, 'main_driver': 24, 'policy_stage': 15}
- candidates that named a thesis in folds_into and still opened: 9
- one object, quantity and year held by several theses: {'AMD growth_rate 2027': 2, 'NVDA segment_revenue FY2027': 2, 'ai-capex spend_total 2026': 2}

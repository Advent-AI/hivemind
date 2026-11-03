# Extraction gold `extraction-admission-2026-10-26` against `/Users/lchingen/hivemind/poc/data/english-v25-admission-r3-2026-10-26/views.sqlite`

Cases judged: 20; fail 7, full 6, not processed 7

| case | title | score | baseline (v23) | missing must-open | extra opened | missing links | forbidden links | opened by items |
|---|---|---|---|---|---|---|---|---|
| A01 | One guidance paragraph is not one thesis per line (NVDA FY2027 gross margin) | **full** | partial |  |  |  |  | v1, v2, v3, v4, v5 |
| A02 | Samples shipped is not production started (Vera Rubin) | **full** | full |  |  |  |  | v1, v2, v3, v4, v5 |
| A03 | Export licence, import permission and revenue are three things (China H200) | **fail** | fail | NVDA FY2027 China data-center compute revenue vs FY2026 |  | 4\.6 billion; not assuming any Data Center compute revenue from China; 4\.5 billion charge associated with H20 |  | v1, v2, v3, v4, v5 |
| A04 | Five, four and three companies of capex are one aggregate | **full** | fail |  |  |  |  | v1, v2, v3, v4, v5, v32, v33 |
| A05 | NAVER project announcement: zero new theses | **full** | partial |  |  |  |  | v18 |
| A06 | SK project announcement: zero new theses, gross-margin input kept | **fail** | fail |  |  | HBM4 |  |  |
| A07 | Ohio: the lease guarantee and chip financing are NVDA's own risk | **fail** | fail |  |  | top \$700 billion |  |  |
| A08 | Quarterly press release: all evidence, no new thesis | **fail** | partial |  |  | 91\.0 billion |  |  |
| A09 | Analyst opinion: one evidence line, not six; the opposing view is not dropped | **fail** | fail |  |  | Sharon AI|Firmus |  |  |
| A10 | SpaceX compute: evidence to NVDA data-center demand, not three events | **not processed** | fail |  |  |  |  |  |
| A11 | TSMC: one segment, one revenue thesis; FY2027 only with a 2027 statement | **not processed** | fail |  |  |  |  |  |
| A12 | CoreWeave: keep the two crossings the street watches | **not processed** | partial |  |  |  |  |  |
| A13 | MSFT call: the one line the street argues about was not opened | **fail** | fail | MSFT calendar-2026 capex ~$175bn (component of the five-company aggregate); MSFT Intelligent Cloud FY2027 revenue, Azure proxy (v30) |  | 175 billion; 41 billion |  |  |
| A14 | AMD call: three core theses, five to seven extras | **not processed** | partial |  |  |  |  |  |
| A15 | META call: capex is the one thesis this corpus needs | **full** | partial |  |  |  |  | v29 |
| A16 | CoreWeave managed-inference ARR: acceptable thesis, not required (alternatives only) | **not processed** | full |  |  |  |  |  |
| A17 | Four-company $745bn is evidence to the five-company aggregate, not a new aggregate | **not processed** | fail |  |  |  |  |  |
| A18 | Bloomberg retelling of the NAVER investment: a late statement, zero theses | **full** | full |  |  |  |  |  |
| A19 | Taiwan "weighing tighter policies": one clause in a smuggling story, evidence not thesis | **fail** | fail |  |  | weighing tighter policies |  |  |
| A20 | Goldman aggregates via the Fool: evidence to the 2026 aggregate; no new aggregate, no early 2027 | **not processed** | fail |  |  |  |  |  |

## Census

- theses: 37
- by object: {'AMZN': 2, 'INTC': 4, 'META': 1, 'MSFT': 1, 'NVDA': 18, 'ai-capex': 3, 'chip-export-controls': 8}
- by measure: {'capex': 4, 'event': 12, 'gross_margin': 2, 'operating_margin': 1, 'policy_event': 8, 'product_revenue': 1, 'segment_revenue': 6, 'spend_total': 3}
- by admission reason (handover candidates carrying opens_as): {'binding_obligation': 11, 'industry_aggregate': 3, 'main_driver': 15, 'policy_stage': 14}
- candidates that named a thesis in folds_into and still opened: 6
- one object, quantity and year held by several theses: {'INTC segment_revenue 2026': 2, 'NVDA segment_revenue FY2027': 2, 'ai-capex spend_total 2026': 2}

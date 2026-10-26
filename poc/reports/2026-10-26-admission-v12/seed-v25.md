# Extraction gold `extraction-admission-2026-10-26` against `/Users/lchingen/hivemind/poc/data/english-v25-admission-r2-2026-10-26/views.sqlite`

Cases judged: 20; fail 4, full 1, not processed 15

| case | title | score | baseline (v23) | missing must-open | extra opened | missing links | forbidden links | opened by items |
|---|---|---|---|---|---|---|---|---|
| A01 | One guidance paragraph is not one thesis per line (NVDA FY2027 gross margin) | **full** | partial |  |  |  |  | v1, v2 |
| A02 | Samples shipped is not production started (Vera Rubin) | **fail** | full | NVDA begins Vera Rubin production shipments by 2026-12-31 (second half of the year) |  | first Vera Rubin samples |  | v1, v2 |
| A03 | Export licence, import permission and revenue are three things (China H200) | **fail** | fail | NVDA FY2027 China data-center compute revenue vs FY2026 |  | 4\.6 billion; not assuming any Data Center compute revenue from China |  | v1, v2 |
| A04 | Five, four and three companies of capex are one aggregate | **fail** | fail |  |  | 690 billion |  | v1, v2 |
| A05 | NAVER project announcement: zero new theses | **not processed** | partial |  |  |  |  |  |
| A06 | SK project announcement: zero new theses, gross-margin input kept | **not processed** | fail |  |  |  |  |  |
| A07 | Ohio: the lease guarantee and chip financing are NVDA's own risk | **not processed** | fail |  |  |  |  |  |
| A08 | Quarterly press release: all evidence, no new thesis | **fail** | partial |  |  | 91\.0 billion; 75\.0% |  |  |
| A09 | Analyst opinion: one evidence line, not six; the opposing view is not dropped | **not processed** | fail |  |  |  |  |  |
| A10 | SpaceX compute: evidence to NVDA data-center demand, not three events | **not processed** | fail |  |  |  |  |  |
| A11 | TSMC: one segment, one revenue thesis; FY2027 only with a 2027 statement | **not processed** | fail |  |  |  |  |  |
| A12 | CoreWeave: keep the two crossings the street watches | **not processed** | partial |  |  |  |  |  |
| A13 | MSFT call: the one line the street argues about was not opened | **not processed** | fail |  |  |  |  |  |
| A14 | AMD call: three core theses, five to seven extras | **not processed** | partial |  |  |  |  |  |
| A15 | META call: capex is the one thesis this corpus needs | **not processed** | partial |  |  |  |  |  |
| A16 | CoreWeave managed-inference ARR: acceptable thesis, not required (alternatives only) | **not processed** | full |  |  |  |  |  |
| A17 | Four-company $745bn is evidence to the five-company aggregate, not a new aggregate | **not processed** | fail |  |  |  |  |  |
| A18 | Bloomberg retelling of the NAVER investment: a late statement, zero theses | **not processed** | full |  |  |  |  |  |
| A19 | Taiwan "weighing tighter policies": one clause in a smuggling story, evidence not thesis | **not processed** | fail |  |  |  |  |  |
| A20 | Goldman aggregates via the Fool: evidence to the 2026 aggregate; no new aggregate, no early 2027 | **not processed** | fail |  |  |  |  |  |

## Census

- theses: 5
- by object: {'NVDA': 4, 'ai-capex': 1}
- by measure: {'capex': 1, 'event': 1, 'gross_margin': 1, 'product_revenue': 1, 'spend_total': 1}
- by admission reason (handover candidates carrying opens_as): {'guidance_on_main_driver': 4, 'industry_aggregate': 1}
- candidates that named a thesis in folds_into and still opened: 0
- one object, quantity and year held by several theses: {}

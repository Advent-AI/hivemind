# One-change arms beside a fresh control (Haiku 5.5, 16k, three draws each)

## Arm V: conditional valuation dropped (w108-4, w209-4)
- old: an author's general risks or valuation arithmetic ("if AI pulls back it would hurt"; "at 34 times earnings the stock is worth $305")
- new: an author's general risks ("if AI pulls back it would hurt")

### call 108 · gnews:e4e5f1b5c0c68381e4c486e1
- control-1: evidence kept 5 of 5; candidates kept 0 of 1; dropped [c1: year FY2028 is beyond next year: not opened (06-views 不开)]
    - e4 | third_party_view | Cerebras claims its chips are 15 times faster than some Nvidia models.
    - cand c1 [DROPPED] main_driver/product_revenue due 2028-02-28 | Will Nvidia's Vera product revenue for FY2028 reach the nearly $20 billion of CPU sales management has signalled?
- control-2: evidence kept 6 of 6; candidates kept 1 of 1
    - e5 | third_party_view | Cerebras claims its chips are 15 times faster than some Nvidia models.
    - cand c1 main_driver/growth_rate due 2027-02-28 | Will Nvidia's FY2027 total revenue grow by at least 80% year over year?
- control-3: evidence kept 5 of 5; candidates kept 0 of 1; dropped [c1: quarterly number: evidence, not a view (06-views ladder rule 6)]
    - e5 | third_party_view | Cerebras claims its chips are 15 times faster than some Nvidia models.
    - cand c1 [DROPPED] main_driver/growth_rate due 2027-02-28 | Will Nvidia's fiscal 2027 total revenue growth year over year be at least 80% (strongly bullish), 50% to under 80% (bullish), 25% to under 50% (neutral versus the Q1 pace
- V-1: evidence kept 8 of 8; candidates kept 0 of 0
    - e4 | third_party_view | Cerebras claims its chips are 15 times faster than some Nvidia models.
    - e5 | third_party_view | Author states Nvidia's average forward P/E was nearly 34 over the past two years, per chart.
    - e7 | third_party_view | Author estimates fair value of about $305 per share at a 34 forward P/E, implying about 54% upside.
    - e8 | third_party_view | Author notes Nvidia trades at roughly 22 times forward earnings.
- V-2: evidence kept 9 of 9; candidates kept 1 of 1
    - e5 | third_party_view | Cerebras claims its chips are 15 times faster than some Nvidia models.
    - e6 | third_party_view | The author states Nvidia trades at roughly 22 times forward earnings.
    - e7 | third_party_view | The author states Nvidia's average forward P/E was nearly 34 over the past two years.
    - e9 | third_party_view | The author's valuation applying a 34 forward P/E implies about $305 per share, roughly 54% upside.
    - cand c1 main_driver/total_revenue due 2027-02-25 | Will Nvidia's total revenue for fiscal 2027 (Feb 2026 to Jan 2027) reach at least $350 billion?
- V-3: evidence kept 9 of 9; candidates kept 0 of 0
    - e1 | third_party_view | Author says NVDA trades at roughly 22 times forward earnings, which he views as reasonable (as of early July 2026).
    - e5 | third_party_view | Cerebras claims its chips are 15 times faster than some Nvidia models.
    - e6 | third_party_view | Author states NVDA's average forward P/E was nearly 34 over the past two years.
    - e8 | third_party_view | Author's valuation: applying a 34 forward P/E gives roughly $305 per share, about 54% upside.

### call 209 · gnews:71df54965281684cc500960f
- control-1: evidence kept 5 of 5; candidates kept 2 of 2
    - e5 | third_party_view | Keithen Drury forecasts Nvidia shares could rise to $300, about 50% above the current price, by late 2027.
    - cand c1 industry_aggregate/spend_total due 2027-03-31 | Will combined hyperscaler capital spending in calendar 2026 reach management's projected $650 billion?
    - cand c2 industry_aggregate/spend_total due 2028-03-31 | Will combined hyperscaler capital spending in calendar 2027 top $1 trillion as management projected?
- control-2: evidence kept 5 of 5; candidates kept 1 of 1
    - e4 | third_party_view | Author Keithen Drury sees Nvidia stock reaching a $300 price target in late 2027, about 50% upside.
    - e5 | third_party_view | Author projects Nvidia share price at $319 at end of fiscal 2028, using a 25x earnings multiple on $12.76 EPS.
    - cand c1 industry_aggregate/spend_total due 2028-02-28 | Will combined calendar-2027 capital spending by hyperscalers reach $1 trillion or more?
- control-3: evidence kept 5 of 5; candidates kept 1 of 1
    - e5 | third_party_view | The author sets a $300 per share price target for Nvidia by late 2027, based on $12.76 FY2028 EPS at a 25x multiple.
    - cand c1 industry_aggregate/capex due 2028-03-31 | Will the combined calendar 2027 capital spending of the major hyperscale cloud providers reach $1 trillion?
- V-1: evidence kept 4 of 4; candidates kept 1 of 1
    - e4 | third_party_view | Author Keithen Drury projects Nvidia's share price at end of fiscal 2028 at $319, using $12.76 EPS and a 25x multiple, and expects $300 in late 2027.
    - cand c1 industry_aggregate/capex due 2028-02-28 | Will combined hyperscaler capital spending in calendar 2027 reach or exceed $1 trillion?
- V-2: evidence kept 6 of 6; candidates kept 2 of 2
    - e5 | third_party_view | Keithen Drury projects a share price of $319 at the end of fiscal 2028, using a 25x earnings multiple on the $12.76 EPS estimate.
    - e6 | third_party_view | Keithen Drury's price target: Nvidia stock could reach $300 per share sometime in late 2027.
    - cand c1 industry_aggregate/capex due 2027-02-28 | Will combined hyperscaler capital spending for calendar 2026 reach at least $650 billion?
    - cand c2 industry_aggregate/capex due 2028-02-28 | Will combined hyperscaler capital spending for calendar 2027 reach at least $1 trillion?
- V-3: evidence kept 5 of 5; candidates kept 1 of 1
    - e5 | third_party_view | Author Keithen Drury values Nvidia at a 25x earnings multiple on the $12.76 consensus EPS, projecting a $319 share price at the end of fiscal 2028 and expecting $300 in late 2027.
    - cand c1 industry_aggregate/capex due 2028-02-15 | Will combined hyperscaler capital spending in calendar 2027 reach $1 trillion or more?

### call 177 · gnews:ff7d99387d1dae92ede72145
- control-1: evidence kept 4 of 4; candidates kept 0 of 0
    - e1 | third_party_view | Consensus Wall Street price target for NVDA is a little above $300 per share, implying more than 50% upside, as cited by the author.
    - e2 | third_party_view | Highest Street price target for NVDA is $500 per share, which the author says implies the stock could more than double over the next year.
    - e3 | third_party_view | Author cites NVDA forward price-earnings multiple of 35 times, well below the sector average.
- control-2: evidence kept 6 of 6; candidates kept 0 of 0
    - e3 | third_party_view | Author cites Nvidia's forward price-earnings multiple of 35 times, well below the sector average.
    - e4 | third_party_view | Wall Street consensus price target for NVDA is a little above $300 per share, implying more than 50% upside.
    - e5 | third_party_view | Highest Wall Street price target for NVDA is $500 per share, implying the stock could more than double over the next year.
- control-3: evidence kept 5 of 5; candidates kept 0 of 0
    - e1 | third_party_view | Author cites Nvidia's forward P/E at 35 times, well below the sector average, from the article's summary data.
    - e3 | third_party_view | Consensus Wall Street price target for NVDA is a little above $300 per share, implying more than 50% upside.
    - e4 | third_party_view | Highest Wall Street price target for NVDA is $500 per share, implying the stock could more than double over the next year.
- V-1: evidence kept 5 of 5; candidates kept 0 of 0
    - e2 | third_party_view | Author cites Nvidia's forward P/E at 35 times, well below the sector average.
    - e3 | third_party_view | Wall Street consensus price target for NVDA is a little above $300 per share, implying more than 50% upside.
    - e4 | third_party_view | Highest Wall Street price target for NVDA is $500 per share, implying Nvidia could more than double over the next year.
- V-2: evidence kept 6 of 6; candidates kept 0 of 0
    - e3 | third_party_view | The author cites Nvidia's forward price-earnings multiple at 35 times, well below the sector average.
    - e4 | third_party_view | Consensus Wall Street price target for NVDA is a little above $300 per share, implying more than 50% upside.
    - e5 | third_party_view | The highest Wall Street price target for NVDA is $500 per share, implying a more-than-doubling over the next year if all goes well.
- V-3: evidence kept 5 of 5; candidates kept 0 of 0
    - ev2 | third_party_view | Author states NVDA's forward P/E is 35 times, well below the sector average.
    - ev3 | third_party_view | Consensus Wall Street price target for NVDA is a little above $300 per share, implying more than 50% upside.
    - ev4 | third_party_view | Highest Street price target for NVDA is $500 per share, implying more than a doubling over the next year.

### call 141 · gnews:068a24e2743bab750f43f048
- control-1: evidence kept 7 of 7; candidates kept 0 of 0
    - e6 | third_party_view | Author states Strategy's bitcoin is worth $49.6 billion, 28 times its annual combined dividend and interest obligations.
- control-2: evidence kept 7 of 7; candidates kept 1 of 1
    - e6 | third_party_view | Author states Strategy's bitcoin is worth $49.6 billion, about 28 times its annual combined dividend and interest obligations.
    - cand c1 main_driver/gross_margin due 2027-02-25 | Will NVIDIA's FY2027 full-year GAAP gross margin be at or above 74 percent?
- control-3: evidence kept 7 of 7; candidates kept 0 of 0
    - e6 | third_party_view | Author states Strategy's bitcoin is worth $49.6 billion, 28 times its annual combined dividend and interest obligations.
- V-1: evidence kept 9 of 9; candidates kept 1 of 1
    - e7 | third_party_view | Author says Strategy's bitcoin is worth $49.6 billion, 28 times its annual combined dividend and interest obligations.
    - cand c1 main_driver/gross_margin due 2027-02-28 | Will Nvidia's FY2027 full-year GAAP gross margin be at or above 74 percent, as reported in its FY2027 annual report?
- V-2: evidence kept 9 of 9; candidates kept 1 of 1
    - e8 | third_party_view | Author says Strategy's bitcoin holdings equal 28 times its annual combined dividend and interest obligations.
    - cand c1 main_driver/gross_margin due 2027-02-25 | Will Nvidia's fiscal 2027 GAAP gross margin, reported in its annual report, be at or above 74.9%?
- V-3: evidence kept 8 of 8; candidates kept 1 of 1
    - e7 | third_party_view | Author states Strategy's bitcoin is worth $49.6 billion, 28 times its annual dividend and interest obligations.
    - cand c1 main_driver/gross_margin due 2027-02-25 | Will Nvidia's GAAP gross margin for fiscal 2027 (Feb 2026 to Jan 2027) be at or above 75%?

### call 267 · gnews:4d1b1ca014068fb532f116b3
- control-1: evidence kept 13 of 13; candidates kept 1 of 1
    - e10 | third_party_view | Analyst consensus price target for NVIDIA is about $301.62 as of the item.
    - cand c1 main_driver/total_revenue due 2027-02-24 | Will NVIDIA report FY2027 total revenue of at least $400 billion, with the band determined by the reported full-year figure?
- control-2: evidence kept 11 of 11; candidates kept 1 of 1
    - e9 | third_party_view | Analyst consensus price target for NVIDIA is about $301.62, implying 53% upside from $196.
    - cand c1 main_driver/segment_revenue due 2027-02-28 | Will NVIDIA's FY2027 data center revenue reach the rung range set out below, as reported in its FY2027 annual report?
- control-3: evidence kept 10 of 10; candidates kept 1 of 1
    - e9 | fact | Amazon has disclosed that its Trainium chip business is now worth multiple billions of dollars.
    - cand c1 main_driver/total_revenue due 2027-02-25 | Will NVIDIA report total revenue for fiscal 2027 (February 2026 to January 2027) of at least $360 billion, and how does it compare with the range bands?
- V-1: evidence kept 13 of 13; candidates kept 3 of 3
    - e11 | third_party_view | Analyst consensus price target of about $301.62 implies 53% upside from $196, per the author.
    - cand c1 main_driver/total_revenue due 2027-02-24 | Will NVIDIA report FY2027 total revenue of at least $380 billion in its annual report for the year ending January 2027?
    - cand c2 main_driver/gross_margin due 2027-02-24 | Will NVIDIA report FY2027 non-GAAP gross margin of at least 76% in its annual results for the year ending January 2027?
    - cand c3 policy_stage/event due 2027-01-31 | Will US authorities approve a licence for NVIDIA data-center chip sales to China by 2027-01-31?
- V-2: evidence kept 8 of 8; candidates kept 0 of 2; dropped [c1: quarterly number: evidence, not a view (06-views ladder rule 6); c2: quarterly number: evidence, not a view (06-views ladder rule 6)]
    - e8 | third_party_view | Author cites an analyst consensus price target of about $301.62 for NVDA, versus a $196 share price, implying 53% upside.
    - cand c1 [DROPPED] main_driver/gross_margin due 2027-02-25 | Will NVIDIA's FY2027 full-year non-GAAP gross margin be at or above the 75% level management guided for Q2 FY27?
    - cand c2 [DROPPED] main_driver/total_revenue due 2027-02-25 | Will NVIDIA's FY2027 total revenue reach the level implied by its Q1 FY27 revenue of $81.61 billion and Q2 guidance of $91.0 billion?
- V-3: evidence kept 11 of 11; candidates kept 3 of 3
    - cand c1 main_driver/total_revenue due 2027-02-28 | Where will NVIDIA's FY2027 total revenue land against the $380 billion and $420 billion thresholds?
    - cand c2 main_driver/gross_margin due 2027-02-28 | Where will NVIDIA's FY2027 non-GAAP gross margin land against the 71%, 73% and 75% thresholds?
    - cand c3 policy_stage/event due 2027-01-31 | Will NVIDIA announce a China-specific data center SKU by 2027-01-31?

### call 196 · gnews:4a892d75e355bee00aa3c572
- control-1: evidence kept 8 of 8; candidates kept 0 of 0
- control-2: evidence kept 9 of 9; candidates kept 2 of 2
    - e6 | third_party_view | The author cites Nvidia's forward P/E at 22, about one-quarter of Palantir's.
    - cand c1 main_driver/total_revenue due 2027-02-25 | Will Nvidia's FY2027 total revenue, reported in its annual report, be at least $400 billion, between $350 billion and $400 billion, between $300 billion and $350 billion,
    - cand c2 main_driver/segment_revenue due 2027-02-25 | Will Nvidia's FY2027 data center segment revenue, reported in its annual report, be at least $340 billion, between $300 billion and $340 billion, between $260 billion and
- control-3: evidence kept 6 of 6; candidates kept 2 of 2
    - cand c1 main_driver/total_revenue due 2027-02-28 | Will Nvidia's FY2027 total revenue, reported for the year from 2026-02-01 to 2027-01-31, be at or above the stated ranges?
    - cand c2 main_driver/segment_revenue due 2027-02-28 | Will Nvidia's FY2027 data center segment revenue, for the year from 2026-02-01 to 2027-01-31, be at or above the stated ranges?
- V-1: evidence kept 7 of 7; candidates kept 1 of 1
    - e4 | third_party_view | Author states Nvidia's market capitalization is $4.7 trillion, nearly 15 times Palantir's, and that Nvidia is the cheaper stock.
    - e5 | third_party_view | Author states Nvidia's forward P/E ratio is 22, one-quarter of Palantir's.
    - cand c1 main_driver/total_revenue due 2027-02-28 | Will Nvidia's total revenue for fiscal 2027 reach at least $350 billion?
- V-2: evidence kept 7 of 7; candidates kept 1 of 1
    - e5 | third_party_view | The author states Nvidia's forward P/E is 22, one-quarter of Palantir's, with Nvidia's market cap at $4.7 trillion.
    - cand c1 main_driver/total_revenue due 2027-02-26 | Will Nvidia's total revenue for FY2027 (February 2026 to January 2027) reach the level of the bullish ranges in its annual report?
- V-3: evidence kept 7 of 7; candidates kept 1 of 1
    - e6 | third_party_view | Author estimates Nvidia's forward P/E at 22, about one-quarter of Palantir's, with Nvidia's $4.7 trillion market cap nearly 15x Palantir's.
    - cand c1 main_driver/segment_revenue due 2027-02-25 | Will Nvidia's fiscal 2027 data center segment revenue, as reported in its FY2027 annual report, be strongly bullish (at or above $380 billion), bullish ($330 billion to b

## Arm D: Kyber event questions due before the 2027 plan or the 2028 slip can show
- old: For an event, name the date at which its outcome is assessed.
- new: For an event, name the date by which the timing the item states or reports can be checked; the fiscal-year note's date is for annual figures only.

### call 180 · gnews:552f8c2bdfd080555d592587
- control-1: evidence kept 8 of 8; candidates kept 2 of 2
    - e1 | third_party_view | SemiAnalysis reports Nvidia's Kyber rack-scale architecture for Rubin Ultra is delayed by more than 12 months to 2028.
    - e2 | third_party_view | SemiAnalysis attributes the Kyber delay to manufacturing difficulty with the PCB midplane.
    - e8 | third_party_view | Kyber had been slated to debut with Vera Rubin Ultra in 2027, per the reporter's background.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia begin volume shipments of its Kyber NVL144 rack-scale system by 2027-12-31?
    - cand c2 main_driver/event due 2026-12-31 | Will Nvidia ship Vera Rubin systems to cloud partners by 2026-12-31?
- control-2: evidence kept 7 of 7; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported that the Kyber rack-scale architecture for Rubin Ultra has been delayed by more than 12 months to 2028.
    - e3 | third_party_view | SemiAnalysis said the Kyber NVL144 rack is delayed to 2028 because manufacturing the PCB midplane is difficult.
    - cand c1 main_driver/event due 2027-01-31 | Will Nvidia begin shipping Kyber NVL144 racks to customers by 2027-01-31?
- control-3: evidence kept 7 of 7; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reports the Kyber NVL144 rack architecture, slated for Vera Rubin Ultra in 2027, is delayed by more than 12 months to 2028.
    - e3 | third_party_view | SemiAnalysis attributes the Kyber delay to manufacturing difficulty with the PCB midplane.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia begin shipping the Kyber NVL144 rack architecture to customers by 2027-12-31?
- D-1: evidence kept 8 of 8; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reports the Kyber NVL144 rack architecture delayed by more than 12 months to 2028.
    - e7 | third_party_view | SemiAnalysis attributes the Kyber delay to manufacturing difficulties with the PCB midplane.
    - e8 | party_statement | Kyber had previously been slated to debut with Vera Rubin Ultra in 2027.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia's Kyber NVL144 rack architecture be shipping to customers by 2027-12-31?
- D-2: evidence kept 9 of 9; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis says the Kyber rack architecture for Rubin Ultra has been delayed by more than 12 months to 2028
    - e2 | third_party_view | SemiAnalysis says the Kyber NVL144 rack is delayed to 2028 because the PCB midplane is hard to manufacture
    - e3 | third_party_view | SemiAnalysis attributes the Kyber delay to manufacturing difficulty with a key circuit board
    - e9 | third_party_view | SemiAnalysis says Nvidia has no proven solution to expand the scale-up world size for Rubin Ultra
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia ship Kyber NVL144 racks to customers by 2027-12-31?
- D-3: evidence kept 8 of 8; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis says the Kyber NVL144 rack architecture has been delayed to 2028 because the PCB midplane is hard to manufacture.
    - e2 | third_party_view | SemiAnalysis says the Kyber rack-scale architecture for Rubin Ultra has been delayed by more than 12 months to 2028, from 2027.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia begin shipping Kyber NVL144 rack systems to customers by 2027-12-31?

### call 195 · gnews:68a3ed21f77b935d9fa7ec5e
- control-1: evidence kept 8 of 8; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis claims the Kyber rack design for Rubin Ultra GPUs has slipped more than 12 months.
    - e2 | third_party_view | SemiAnalysis attributes the Kyber delay to persistent manufacturing problems with the PCB midplane.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia ship Kyber NVL144 racks to customers by 2027-12-31?
- control-2: evidence kept 6 of 6; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis claims the Kyber high-density rack for Rubin Ultra GPUs has slipped by more than 12 months, citing PCB midplane manufacturing problems.
    - cand c1 main_driver/event due 2027-02-15 | Will Nvidia ship Kyber NVL144 rack systems to customers by 2027-02-15?
- control-3: evidence kept 5 of 5; candidates kept 1 of 1
    - e2 | third_party_view | SemiAnalysis claims the high-density rack design for Rubin Ultra GPUs has slipped more than 12 months, blaming PCB midplane manufacturing problems.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia ship Kyber NVL144 rack systems to customers by 2027-12-31?
- D-1: evidence kept 4 of 4; candidates kept 0 of 0
    - e2 | third_party_view | SemiAnalysis claims the high-density rack design for Rubin Ultra GPUs has slipped by more than 12 months, citing persistent manufacturing problems with the complex PCB midplane.
- D-2: evidence kept 4 of 4; candidates kept 1 of 1
    - e2 | third_party_view | SemiAnalysis claims the Kyber NVL144 rack design for Rubin Ultra GPUs has slipped by more than 12 months, citing persistent PCB midplane manufacturing problems.
    - cand c1 main_driver/event due 2028-12-31 | Will Nvidia begin shipping Kyber NVL144 rack systems to customers by 2028-12-31, as shown by company statements or filings?
- D-3: evidence kept 4 of 4; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis claims the Kyber high-density rack for Rubin Ultra GPUs has slipped by more than 12 months.
    - cand c1 main_driver/event due 2027-01-31 | Will Nvidia confirm volume shipments of Kyber NVL144 rack systems by 2027-01-31?

### call 198 · gnews:98a4e8ff0c0260d8dc9e531d
- control-1: evidence kept 7 of 7; candidates kept 1 of 1
    - ev1 | third_party_view | SemiAnalysis reports Nvidia delayed Kyber rack-scale architecture production by more than 12 months, pushing release to 2028.
    - ev2 | third_party_view | SemiAnalysis attributes the Kyber NVL144 delay to a PCB midplane manufacturability problem; Nvidia's back-to-back Oberon alternative was also scrapped after hyperscaler pushback.
    - ev4 | party_statement | Nvidia has said its liquid-cooled Kyber racks will offer a 4x performance improvement over the Blackwell NVL72 (Oberon) system.
    - ev5 | third_party_view | SemiAnalysis reported a week earlier that Nvidia cancelled the four-die Rubin Ultra design in favour of a two-chiplet design.
    - ev6 | third_party_view | The two-die Rubin Ultra offering is reported to deliver around half the performance of the four-die design.
    - ev7 | party_statement | Nvidia spokesperson responds to DCD's request for comment on the Kyber claims, saying the roadmap is intact.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia confirm production shipment of Kyber NVL144 racks by 2027-12-31?
- control-2: evidence kept 9 of 9; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported Nvidia delayed Kyber rack-scale architecture production by more than 12 months, pushing release to 2028.
    - e2 | party_statement | Nvidia has said liquid-cooled Kyber racks consume some 600kW.
    - e3 | party_statement | Nvidia previously said liquid-cooled Kyber racks will offer 4x performance over Blackwell NVL72 (Oberon).
    - e4 | third_party_view | SemiAnalysis said the Kyber NVL144 rack is delayed to 2028 because the PCB midplane is hard to manufacture.
    - e7 | third_party_view | SemiAnalysis reported about a week earlier that Nvidia canceled the four-die Rubin Ultra design for a two-chiplet design.
    - e8 | third_party_view | SemiAnalysis said the two-die Rubin Ultra will deliver around half the performance of the four-die version.
    - cand c1 main_driver/event due 2027-02-28 | Will Nvidia ship or begin volume production of Kyber NVL144 racks by 2027-01-31, the end of FY2027?
- control-3: evidence kept 9 of 9; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reports Nvidia delayed Kyber rack-scale architecture production by more than 12 months, to a 2028 release.
    - e2 | third_party_view | Kyber racks had originally been slated for release in 2027.
    - e3 | third_party_view | SemiAnalysis attributes the Kyber NVL144 delay to 2028 to a challenging PCB midplane manufacturability problem.
    - e6 | party_statement | Nvidia previously said liquid-cooled Kyber racks offer a 4x performance improvement over Blackwell NVL72 and consume about 600kW.
    - e7 | third_party_view | SemiAnalysis reported about a week before this item that Nvidia canceled the four-die Rubin Ultra design in favor of a two-chiplet design.
    - e8 | third_party_view | The two-die Rubin Ultra offering is expected to deliver around half the performance of the four-die design, per the report.
    - e9 | party_statement | An Nvidia spokesperson responded to the Kyber delay claims by saying the company's roadmap is intact.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia begin volume shipments of Kyber NVL144 racks to customers by 2027-12-31?
- D-1: evidence kept 8 of 8; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reports Nvidia delayed production of the Kyber rack-scale architecture by more than 12 months, pushing release to 2028.
    - e2 | third_party_view | SemiAnalysis attributes the Kyber NVL144 delay to a PCB midplane that remains hard to manufacture.
    - e5 | third_party_view | SemiAnalysis reported about a week earlier that Nvidia canceled the four-die Rubin Ultra design for a two-chiplet design.
    - e6 | third_party_view | The two-die Rubin Ultra offering is reported to deliver around half the performance of the four-die design.
    - e7 | party_statement | Nvidia previously said Kyber racks would deliver 4x the performance of the Blackwell NVL72 system; the claim was first announced at GTC 2025.
    - e8 | party_statement | An Nvidia spokesperson responded to DCD's request for comment on the Kyber claims by saying the roadmap is intact.
    - cand c1 main_driver/event due 2027-01-31 | Will Nvidia ship Kyber NVL144 rack systems to customers by 2027-01-31, the end of fiscal 2027?
- D-2: evidence kept 9 of 9; candidates kept 0 of 0
    - e1 | third_party_view | SemiAnalysis reported Nvidia delayed Kyber rack-scale architecture production by more than 12 months, pushing release to 2028.
    - e2 | third_party_view | SemiAnalysis said the Kyber NVL144 rack is delayed to 2028 because the PCB midplane is hard to manufacture.
    - e4 | party_statement | Nvidia previously said liquid-cooled Kyber racks offer 4x performance over Blackwell NVL72 and consume about 600kW.
    - e6 | third_party_view | SemiAnalysis said Nvidia has no proven solution to expand the scale-up world size for Rubin Ultra.
    - e7 | third_party_view | SemiAnalysis reported about a week earlier that Nvidia canceled the four-die Rubin Ultra design for a two-chiplet design over manufacturing concerns.
    - e8 | third_party_view | The reported two-die Rubin Ultra offering is expected to deliver around half the performance of the four-die design.
    - e9 | party_statement | An Nvidia spokesperson responded to DCD's request for comment on the Kyber claims by saying the roadmap is intact.
- D-3: evidence kept 8 of 8; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported Nvidia delayed Kyber rack production by more than 12 months, pushing release to 2028.
    - e2 | third_party_view | SemiAnalysis said the Kyber NVL144 rack is delayed to 2028 because the PCB midplane is hard to manufacture.
    - e5 | party_statement | Nvidia previously said Kyber racks will offer 4x the performance of the Blackwell NVL72 system.
    - e6 | third_party_view | SemiAnalysis reported a week earlier that Nvidia canceled the four-die Rubin Ultra design for a two-chiplet design.
    - e7 | third_party_view | The reported two-die Rubin Ultra offering would deliver about half the performance of the four-die design.
    - e8 | party_statement | A Nvidia spokesperson responded to DCD that Nvidia's roadmap is intact after the Kyber claims.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia ship Kyber NVL144 racks to customers by 2027-12-31?

### call 274 · gnews:795ea94e1100415a67fd1a96
- control-1: evidence kept 8 of 8; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported on X that Nvidia's Kyber NVL144 rack is pushed back more than twelve months to 2028 due to manufacturing problems.
    - e2 | third_party_view | SemiAnalysis says the PCB midplane for Kyber NVL144 has proven extremely difficult to produce without defects.
    - e3 | third_party_view | SemiAnalysis reports the four-die version of Rubin Ultra has been canceled.
    - e4 | third_party_view | SemiAnalysis says only the two-die Rubin Ultra version remains, with roughly half the real-world compute performance.
    - e8 | fact | Jensen Huang showed off Kyber NVL144 at Nvidia's GTC conference about three months before the report.
    - cand c1 main_driver/event due 2027-02-28 | Will Nvidia confirm that Kyber NVL144 racks have begun shipping to customers by 2027-02-28?
- control-2: evidence kept 7 of 7; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported that Nvidia's Kyber NVL144 rack was pushed back more than twelve months to 2028 because of manufacturing problems.
    - e2 | third_party_view | SemiAnalysis said the PCB midplane has proven extremely difficult to produce without defects, which is the cause of the Kyber delay.
    - e4 | third_party_view | SemiAnalysis reported the four-die Rubin Ultra version is canceled, leaving a two-die version with roughly half the real-world compute performance.
    - e6 | fact | Nvidia CEO Jensen Huang showed off the Kyber NVL144 rack at the GTC conference about three months before the delay report.
    - e7 | third_party_view | Nvidia plans to sell more Oberon-Rubin racks in the existing form factor to make up for the Kyber shortfall.
    - cand c1 main_driver/event due 2027-01-31 | Will Nvidia ship Kyber NVL144 racks to customers by 2027-01-31, the end of FY2027?
- control-3: evidence kept 6 of 6; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported that Nvidia's Kyber NVL144 rack has been pushed back more than twelve months to 2028 because of manufacturing problems.
    - e2 | third_party_view | SemiAnalysis says the PCB midplane of the Kyber NVL144 has proven extremely difficult to produce without defects.
    - e4 | third_party_view | SemiAnalysis reports the four-die Rubin Ultra version is canceled, leaving a two-die version with roughly half the real-world compute performance.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia launch or ship the Kyber NVL144 rack to customers by 2027-12-31?
- D-1: evidence kept 7 of 7; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported that Nvidia's Kyber NVL144 rack slipped more than twelve months to 2028 due to manufacturing problems.
    - e2 | third_party_view | SemiAnalysis says the PCB midplane for Kyber has proven extremely difficult to produce without defects, the cause of the delay.
    - e4 | third_party_view | SemiAnalysis reports the four-die Rubin Ultra was canceled, leaving a two-die version with roughly half the real-world compute performance.
    - e5 | third_party_view | SemiAnalysis says the CPO-NVSwitch interconnect will not arrive until the Feynman generation, so Nvidia lacks a proven way to scale Rubin Ultra for now.
    - e6 | rumour | Unattributed report says Nvidia plans to sell more Oberon-Rubin racks in the existing form factor to offset the Kyber shortfall.
    - e7 | fact | Jensen Huang showed off Kyber NVL144 at Nvidia's GTC conference about three months before the July 2026 report.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia launch its Kyber NVL144 rack by 2027-12-31?
- D-2: evidence kept 6 of 6; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported on X that Kyber NVL144 has been pushed back more than twelve months to 2028 because of manufacturing problems.
    - e2 | third_party_view | SemiAnalysis says the Kyber PCB midplane has proven extremely difficult to produce without defects.
    - e4 | third_party_view | SemiAnalysis reports the four-die Rubin Ultra version has been canceled, leaving only the two-die version, which delivers roughly half the real-world compute performance.
    - e6 | fact | Nvidia CEO Jensen Huang showed off Kyber NVL144 at the GTC conference about three months before the reported delay.
    - cand c1 main_driver/event due 2028-12-31 | Will Nvidia ship Kyber NVL144 racks to customers by 2028-12-31?
- D-3: evidence kept 7 of 7; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported Nvidia's Kyber NVL144 rack pushed back more than twelve months to 2028 due to manufacturing problems.
    - e2 | third_party_view | SemiAnalysis says the PCB midplane of the Kyber rack has been extremely difficult to produce without defects.
    - e4 | third_party_view | SemiAnalysis reports the four-die version of Rubin Ultra has been canceled, leaving only the two-die version.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia begin customer shipments of the Kyber NVL144 rack by 2027-12-31?

### call 276 · gnews:d5c48abb470f394f86549b6b
- control-1: evidence kept 7 of 7; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis claimed in a weekend report (around 2026-07-04/05) that Nvidia's Kyber NVL144 rack will be delayed to 2028 because of PCB midplane manufacturing problems.
    - e4 | third_party_view | SemiAnalysis claimed a crucial four-die configuration of a downsized Rubin Ultra platform had been scrapped.
    - cand c1 main_driver/event due 2028-01-31 | Will Nvidia announce customer shipments of Kyber NVL144 racks by 2028-01-31?
- control-2: evidence kept 4 of 4; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis claimed in a weekend report that Nvidia's Kyber NVL144 rack will be delayed to 2028 due to PCB midplane manufacturing problems.
    - e4 | third_party_view | SemiAnalysis claimed a downsized Rubin Ultra platform had its four-die configuration scrapped.
    - cand c1 main_driver/event due 2028-01-31 | Will Nvidia ship Kyber NVL144 racks to customers by 2028-01-31?
- control-3: evidence kept 4 of 4; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis claimed in a weekend report that Nvidia's Kyber NVL144 rack will be delayed to 2028 because of PCB midplane manufacturing problems.
    - e4 | third_party_view | SemiAnalysis claimed a four-die configuration of a downsized Rubin Ultra platform had been scrapped.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia ship Kyber NVL144 racks in production volume by 2027-12-31?
- D-1: evidence kept 5 of 5; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis claimed in a weekend report that Nvidia's Kyber NVL144 rack will be delayed to 2028 due to PCB midplane manufacturing problems.
    - e4 | third_party_view | SemiAnalysis claimed a four-die configuration of a downsized Rubin Ultra platform had been scrapped.
    - cand c1 main_driver/event due 2028-12-31 | Will Nvidia begin shipping Kyber NVL144 racks to customers by 2028-12-31?
- D-2: evidence kept 6 of 6; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis claimed in a weekend report that Nvidia's Kyber NVL144 rack architecture will be delayed to 2028 due to PCB midplane manufacturing challenges.
    - e4 | third_party_view | SemiAnalysis claimed a four-die configuration of the downsized Rubin Ultra platform had been scrapped.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia ship Kyber NVL144 racks to customers by 2027-12-31?
- D-3: evidence kept 6 of 6; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis claimed in a weekend report that the Kyber NVL144 rack architecture will be delayed to 2028 because of PCB midplane manufacturing challenges.
    - e3 | third_party_view | SemiAnalysis claimed a four-die configuration of the downsized Rubin Ultra platform had been scrapped.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia announce commercial shipment of Kyber NVL144 racks on or before 2027-12-31?

### call 288 · gnews:d4c5dc540392f8df39aee250
- control-1: evidence kept 10 of 10; candidates kept 2 of 2
    - e1 | third_party_view | SemiAnalysis reported Nvidia's Kyber rack-scale server design pushed back more than a year, from 2027 to 2028.
    - e2 | third_party_view | SemiAnalysis attributes the Kyber delay to manufacturing problems with a specialized circuit board.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia begin shipping Kyber rack-scale systems to customers by 2027-12-31?
    - cand c2 main_driver/total_revenue due 2027-02-28 | What will Nvidia's FY2027 total revenue be, in USD?
- control-2: evidence kept 10 of 10; candidates kept 2 of 2
    - e1 | third_party_view | SemiAnalysis reported Nvidia's Kyber rack-scale server design pushed back more than a year, from 2027 to 2028.
    - e2 | third_party_view | SemiAnalysis attributes the Kyber delay to manufacturing problems with a specialized circuit board.
    - e3 | third_party_view | NVL576, the larger eight-rack Kyber version, is likely to be delayed or shipped only in small volumes, per SemiAnalysis.
    - cand c1 main_driver/event due 2027-01-31 | Will Nvidia begin shipping Kyber rack-scale server systems to customers by 2027-01-31?
    - cand c2 main_driver/segment_revenue due 2027-02-15 | What will Nvidia's data center segment revenue be for fiscal 2027 (February 2026 to January 2027), in USD?
- control-3: evidence kept 9 of 9; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported Nvidia's Kyber rack-scale server pushed back from 2027 to 2028.
    - e2 | third_party_view | SemiAnalysis attributes the Kyber delay to manufacturing problems with a specialized circuit board.
    - e3 | third_party_view | NVL576, a larger Kyber-based version, is likely delayed or to ship only in small volumes, per SemiAnalysis.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia begin shipping Kyber rack-scale servers to customers on or before 2027-12-31?
- D-1: evidence kept 11 of 11; candidates kept 2 of 2
    - e1 | third_party_view | SemiAnalysis reported that Nvidia's Kyber rack-scale server design slipped from 2027 to 2028.
    - e2 | third_party_view | SemiAnalysis attributes the Kyber delay to manufacturing problems with a specialized circuit board.
    - cand c1 main_driver/total_revenue due 2027-02-25 | What will Nvidia's FY2027 total revenue be, as reported in its annual report?
    - cand c2 main_driver/event due 2027-12-31 | Will Nvidia ship Kyber rack-scale systems to customers by 2027-12-31?
- D-2: evidence kept 11 of 11; candidates kept 3 of 3
    - e1 | third_party_view | SemiAnalysis reported that Nvidia's Kyber rack-scale server design slipped more than a year, from 2027 to 2028.
    - e2 | third_party_view | SemiAnalysis attributes the Kyber delay to manufacturing problems with a specialized circuit board inside the system.
    - cand c1 main_driver/total_revenue due 2027-02-25 | What total revenue will Nvidia report for fiscal 2027, the year ending 2027-01-31?
    - cand c2 main_driver/event due 2028-12-31 | Will Nvidia begin shipping its Kyber rack-scale server design to customers by 2028-12-31?
    - cand c3 main_driver/event due 2026-12-31 | Will Nvidia begin shipping Vera Rubin systems to cloud partners by 2026-12-31?
- D-3: evidence kept 9 of 9; candidates kept 2 of 2
    - e1 | third_party_view | SemiAnalysis reported Nvidia's Kyber rack-scale design has slipped more than a year, from 2027 to 2028.
    - e4 | rumour | Unnamed cloud customers reportedly rejected Nvidia's two-rack backup plan for scaling Rubin Ultra.
    - e6 | third_party_view | SemiAnalysis attributes the Kyber delay to manufacturing problems with a specialized circuit board.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia begin shipping Kyber rack-scale systems to customers by 2027-12-31?
    - cand c2 main_driver/event due 2026-12-31 | Will Nvidia begin shipping Rubin systems to its major cloud partners by 2026-12-31?

### call 300 · gnews:c0432377817a1c00a1bbadf0
- control-1: evidence kept 1 of 1; candidates kept 0 of 0
    - e1 | third_party_view | SemiAnalysis, in an X post, reported that Nvidia's next-generation Kyber NVL144 rack system is delayed by more than a year because of manufacturing difficulties, including setbacks in building printed circuit boards for the platform.
- control-2: evidence kept 2 of 2; candidates kept 1 of 1
    - e2 | third_party_view | SemiAnalysis said Nvidia's Kyber NVL144 hit setbacks in building printed circuit boards for the platform.
    - cand c1 main_driver/event due 2027-02-28 | Will Nvidia begin shipping Kyber NVL144 rack systems to customers by the end of FY2027 (2027-01-31)?
- control-3: evidence kept 2 of 2; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis said in an X post that Nvidia's Kyber NVL144 hit setbacks in building printed circuit boards for the platform.
    - cand c1 main_driver/event due 2027-02-28 | Will Nvidia ship Kyber NVL144 racks to customers by the FY2027 annual report date of 2027-02-28?
- D-1: evidence kept 2 of 2; candidates kept 1 of 1
    - e2 | third_party_view | SemiAnalysis said in an X post that Nvidia's Kyber NVL144 hit setbacks in building printed circuit boards for the platform.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia ship Kyber NVL144 rack systems to customers by 2027-12-31?
- D-2: evidence kept 1 of 1; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported in an X post on 2026-07-06 that Nvidia's next-generation Kyber NVL144 rack system is delayed by more than a year, with setbacks in building its printed circuit boards.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia ship Kyber NVL144 AI server racks to customers by 2027-12-31, after a report of a delay of more than a year?
- D-3: evidence kept 1 of 1; candidates kept 0 of 0
    - e1 | third_party_view | SemiAnalysis reported in an X post that Nvidia's next-generation AI server rack system has been delayed by more than a year due to manufacturing difficulties, with setbacks in building printed circuit boards for the Kyber NVL144 platform.

### call 315 · gnews:c75f16a6d64cc27fc28fb571
- control-1: evidence kept 8 of 8; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis, in an X thread, reports Nvidia will not ship the Kyber NVL144 rack until 2028, more than 12 months late and past the 2027 Rubin Ultra cabinet timing.
    - e2 | rumour | Unattributed report says Nvidia has cancelled the NVL72x2 stopgap rack, leaving no proven alternative to widen Rubin Ultra scale-up in 2027.
    - e6 | rumour | Unattributed report says Nvidia switched from a quad-chiplet to a dual-chiplet Rubin Ultra GPU the prior week, halving per-package compute.
    - e7 | third_party_view | Trade analyses estimate a cabled version of the Kyber interconnect would need more than 20,000 discrete cables.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia begin shipping Kyber NVL144 rack systems to customers by 2027-12-31?
- control-2: evidence kept 7 of 7; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis, in an X thread, reports Nvidia won't ship the Kyber NVL144 rack until 2028, more than 12 months late and pushing the cabinet for Rubin Ultra into the following year.
    - e2 | rumour | Unnamed understanding reported by Tom's Hardware: Nvidia has cancelled the NVL72x2 stopgap rack meant to bridge customers until Kyber.
    - e3 | party_statement | An Nvidia representative tells Tom's Hardware the roadmap is intact, without giving further detail on Rubin Ultra or Kyber schedules.
    - e5 | third_party_view | SemiAnalysis places a production-ready co-packaged optics NVSwitch no earlier than the Feynman generation, leaving copper as the only near-term rack-scale link for Rubin Ultra.
    - e6 | rumour | Tom's Hardware reports, without a named source, that Nvidia switched Rubin Ultra from a quad-chiplet to a dual-chiplet GPU last week, halving per-package compute.
    - e7 | third_party_view | SemiAnalysis judges that Nvidia has no proven way to widen the Rubin Ultra scale-up domain in 2027 beyond what Oberon already delivers.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia begin shipping Kyber NVL144 racks to customers by 2027-12-31?
- control-3: evidence kept 7 of 7; candidates kept 1 of 1
    - e2 | third_party_view | SemiAnalysis reports Nvidia will not ship the Kyber NVL144 rack until 2028, a delay of more than 12 months from the 2027 Rubin Ultra timing.
    - e4 | rumour | The article reports, without a named source, that Nvidia dropped the quad-chiplet Rubin Ultra GPU for a dual-chiplet part the prior week, halving per-package compute.
    - e5 | third_party_view | SemiAnalysis places a production-ready co-packaged optics NVSwitch no earlier than the Feynman generation, leaving copper as the near-term option for Rubin Ultra rack scale-up.
    - e6 | third_party_view | Trade analyses say a cabled version of the Kyber interconnect would need more than 20,000 discrete cables, which is why Nvidia moves wiring onto a passive board.
    - e7 | third_party_view | The article states that the reported delay applies only to the Rubin Ultra phase and Kyber rack, not to 2026 Rubin GPUs on Oberon racks.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia ship Kyber NVL144 racks to customers by 2027-12-31?
- D-1: evidence kept 8 of 8; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported that Nvidia's Kyber NVL144 rack will not ship until 2028, more than 12 months late, pushing the Rubin Ultra cabinet from 2027 into 2028.
    - e2 | rumour | Nvidia is understood to have cancelled the NVL72x2 stopgap rack, which was meant to bridge customers until Kyber, with no source named.
    - e4 | rumour | Nvidia reportedly dropped the quad-chiplet Rubin Ultra GPU for a dual-chiplet part the week before, halving per-package compute, with no named source.
    - e5 | third_party_view | SemiAnalysis places a production-ready co-packaged optics NVSwitch no earlier than the Feynman generation, leaving copper as the only near-term rack-scale link for Rubin Ultra.
    - e6 | third_party_view | Per SemiAnalysis, Nvidia has no proven way to expand Rubin Ultra scale-up in 2027, so the largest domain could only match the current Oberon rack.
    - e7 | third_party_view | Tom's Hardware reports the delay covers only Rubin Ultra and Kyber, not the 2026 Rubin GPUs that reuse the Oberon rack.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia ship Kyber NVL144 racks to customers by 2027-12-31?
- D-2: evidence kept 7 of 7; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported that Nvidia's Kyber NVL144 rack will not ship until 2028, a delay of more than 12 months from the 2027 Rubin Ultra timing.
    - e2 | rumour | Unattributed reporting says Nvidia dropped the NVL72x2 stopgap rack, leaving no proven alternative to widen Rubin Ultra scale-up in 2027.
    - e4 | third_party_view | Trade analyses estimate a cabled version of the Kyber interconnect would need more than 20,000 discrete cables.
    - e5 | rumour | Reported that Nvidia dropped the quad-chiplet Rubin Ultra GPU for a dual-chiplet part the prior week, halving per-package compute.
    - cand c1 main_driver/event due 2028-01-31 | Will Nvidia ship Kyber NVL144 racks to customers on or before 2027-12-31?
- D-3: evidence kept 6 of 6; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reports Nvidia's Kyber NVL144 rack will not ship until 2028, a delay of more than 12 months from the 2027 Rubin Ultra timing.
    - e2 | rumour | Unnamed sources say Nvidia has cancelled the NVL72x2 stopgap rack meant to bridge customers until Kyber.
    - e3 | party_statement | An Nvidia representative says the company's roadmap is intact, without giving further details on Rubin Ultra or Kyber schedules.
    - e4 | rumour | Reported that Nvidia switched the Rubin Ultra GPU from quad-chiplet to dual-chiplet last week, halving per-package compute.
    - e5 | third_party_view | Trade analyses estimate a cabled version of the Kyber interconnect would need more than 20,000 discrete cables.
    - e6 | third_party_view | SemiAnalysis places a production-ready co-packaged optics NVSwitch no earlier than the Feynman generation, leaving copper as the near-term Rubin Ultra rack-scale link.
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia begin shipping Kyber NVL144 racks to customers by 2027-12-31?

### call 383 · gnews:295fceb25273abae9bb6c995
- control-1: evidence kept 10 of 10; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported the Kyber NVL144 rack-scale system slipped from a planned 2027 launch to 2028.
    - cand c1 main_driver/event due 2027-12-31 | Will NVIDIA announce that the Kyber NVL144 rack-scale AI system has launched or begun shipping by 2027-12-31?
- control-2: evidence kept 11 of 12; candidates kept 2 of 2; dropped [e2: quote not in item]
    - e1 | third_party_view | SemiAnalysis reported Kyber NVL144 rack-scale system delayed from planned 2027 launch to 2028.
    - e5 | third_party_view | The reported culprit for the Kyber delay is a PCB midplane with up to 78 layers, which SemiAnalysis says remains challenging from a manufacturability standpoint.
    - cand c1 main_driver/event due 2027-12-31 | Will NVIDIA launch its Kyber NVL144 rack-scale AI system by 2027-12-31?
    - cand c2 main_driver/total_revenue due 2027-02-25 | What will NVIDIA's FY2027 total revenue be, in USD, for the year ending 2027-01-31?
- control-3: evidence kept 10 of 10; candidates kept 2 of 2
    - e1 | third_party_view | SemiAnalysis reported NVIDIA's Kyber NVL144 rack-scale system slipped from a planned 2027 launch to 2028.
    - e2 | party_statement | A NVIDIA spokesperson told Bloomberg the company's roadmap is intact, disputing the Kyber delay report.
    - cand c1 main_driver/segment_revenue due 2027-02-25 | Will NVIDIA's FY2027 Data Center segment revenue, as reported in its annual filing, reach at least $400 billion?
    - cand c2 main_driver/event due 2027-12-31 | Will NVIDIA launch the Kyber NVL144 rack-scale system, with shipments to customers, by 2027-12-31?
- D-1: evidence kept 12 of 12; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported NVIDIA's Kyber NVL144 rack-scale AI system delayed from a planned 2027 launch to 2028.
    - cand c1 main_driver/event due 2027-12-31 | Will NVIDIA launch the Kyber NVL144 rack-scale AI system by 2027-12-31?
- D-2: evidence kept 11 of 11; candidates kept 2 of 2
    - e1 | third_party_view | SemiAnalysis reported NVIDIA's Kyber NVL144 rack-scale system slipped from a planned 2027 launch to 2028.
    - e4 | third_party_view | SemiAnalysis reportedly identified the PCB midplane, with up to 78 layers, as the component behind the Kyber delay.
    - cand c1 main_driver/segment_revenue due 2027-02-28 | Will NVIDIA's FY2027 Data Center segment revenue, reported in its annual filing, fall in the Strongly bearish, Bearish, Neutral, Bullish or Strongly bullish band?
    - cand c2 main_driver/event due 2027-12-31 | Will NVIDIA launch the Kyber NVL144 rack-scale system by 2027-12-31, the 2027 date the reported delay moved to 2028?
- D-3: evidence kept 12 of 12; candidates kept 1 of 1
    - e1 | third_party_view | SemiAnalysis reported on July 5-6, 2026 that NVIDIA's Kyber NVL144 rack-scale system was delayed from a planned 2027 launch to 2028.
    - e3 | third_party_view | SemiAnalysis says the larger NVL576 Kyber sibling is likely delayed or limited to small initial volumes.
    - cand c1 main_driver/event due 2027-12-31 | Will NVIDIA's Kyber NVL144 rack-scale system be launched by 2027-12-31?

## Arm Q: questions whose answer changes no view of a listed subject (Valar/NRC, Singapore charges, lidar bills, debt raise, IREN)
- old: Open a candidate only for one of four reasons, named in opens_as.
- new: Open a candidate only when its answer would change a view of a listed subject, and only for one of four reasons, named in opens_as.

### call 7 · gnews:ad47330f25c9d5ff84ced7e2
- control-1: evidence kept 6 of 6; candidates kept 2 of 2
    - cand c1 binding_obligation/event due 2027-07-01 | Will Nvidia sign a definitive agreement with Valar Atomics to power a Utah AI data center by 2027-07-01?
    - cand c2 policy_stage/policy_event due 2027-01-31 | Will the Nuclear Regulatory Commission issue a licence for the Ward250 reactor by 2027-01-31?
- control-2: evidence kept 9 of 9; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2026-12-31 | Will Nvidia and Valar Atomics sign a definitive agreement to build the 30 MW nuclear-powered data center in Utah by 2026-12-31?
- control-3: evidence kept 8 of 8; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2027-01-31 | Will the Nuclear Regulatory Commission issue a commercial operating licence for the Valar Atomics Ward250 reactor by 2027-01-31?
- Q-1: evidence kept 7 of 7; candidates kept 0 of 0
- Q-2: evidence kept 8 of 8; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2027-01-31 | Will the NRC issue a commercial operating licence for the Valar Atomics Ward250 reactor by 2027-01-31?
- Q-3: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 policy_stage/event due 2027-01-31 | Will the Nuclear Regulatory Commission issue a licence for the Valar Atomics Ward250 reactor by 2027-01-31?

### call 34 · gnews:d1364ee37c17c361ae74f563
- control-1: evidence kept 8 of 8; candidates kept 0 of 1; dropped [c1: candidate ladder: object view rungs must be ['Strongly bullish', 'Bull]
    - cand c1 [DROPPED] binding_obligation/financing_amount due 2027-02-25 | Will the debt Nvidia issues in its July 2026 offering, as shown in the FY2027 annual report commitments note, total below $10 billion, $10 billion to under $20 billion, $
- control-2: evidence kept 9 of 9; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-02-28 | Will Nvidia complete a debt offering of at least $20 billion by 2027-02-28?
- control-3: evidence kept 8 of 8; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2026-08-31 | Will Nvidia complete a debt offering of at least $20 billion between 2026-07-02 and 2026-08-31?
- Q-1: evidence kept 8 of 8; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will Nvidia's debt raised under its July 2026 offering reach at least $20 billion by its FY2027 annual report?
- Q-2: evidence kept 5 of 5; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2026-12-31 | Will Nvidia price or close a debt offering totalling at least $20 billion by 2026-12-31?
- Q-3: evidence kept 8 of 8; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2026-12-31 | Will Nvidia complete a debt offering of at least $20 billion by 2026-12-31?

### call 35 · gnews:a6ed98dfdf1ad76f6edffdfd
- control-1: evidence kept 10 of 10; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2027-06-30 | Will a Singapore court record a conviction of Wei Zhaolun (Alan Wei) on at least one charge in the Aperia Group server case by 2027-06-30?
- control-2: evidence kept 10 of 10; candidates kept 0 of 0
- control-3: evidence kept 13 of 13; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2026-12-31 | Will a Singapore court convict Wei Zhaolun of money laundering by 2026-12-31?
- Q-1: evidence kept 10 of 10; candidates kept 0 of 0
- Q-2: evidence kept 10 of 10; candidates kept 0 of 0
- Q-3: evidence kept 12 of 12; candidates kept 0 of 0

### call 88 · gnews:1eeceeb212a2c82c2e75e806
- control-1: evidence kept 9 of 9; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2026-07-06 | Will the Singapore Police Force announce the eight fraud-by-false-representation charges against the four Aperia Group-linked companies on or before 2026-07-06?
- control-2: evidence kept 10 of 10; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2026-07-06 | Will the Singapore Police Force announce the eight fraud-by-false-representation charges against the four Aperia Group companies on or before 2026-07-06?
- control-3: evidence kept 16 of 17; candidates kept 1 of 1; dropped [e1: quote not in item]
    - cand c1 policy_stage/policy_event due 2026-07-06 | Will the Singapore Police Force announce the eight fraud-by-false-representation charges against the four Aperia Group companies by 2026-07-06?
- Q-1: evidence kept 12 of 12; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2026-07-06 | Will the Singapore Police Force announce the eight fraud charges against the four Aperia-linked companies on or by 2026-07-06?
- Q-2: evidence kept 11 of 11; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2026-07-06 | Will Singapore police announce the eight fraud-by-false-representation charges against the Aperia Group companies by 2026-07-06?
- Q-3: evidence kept 9 of 9; candidates kept 1 of 1
    - cand c1 policy_stage/event due 2026-07-06 | Will the Singapore Police Force announce the eight fraud-by-false-representation charges against the four Aperia Group companies on or before 2026-07-06?

### call 107 · gnews:aad624be9de524b95e766c96
- control-1: evidence kept 6 of 6; candidates kept 0 of 0
- control-2: evidence kept 6 of 6; candidates kept 0 of 1; dropped [c1: year FY2028 is beyond next year: not opened (06-views 不开)]
    - cand c1 [DROPPED] main_driver/total_revenue due 2028-08-31 | Will IREN's total revenue for fiscal 2028 reach the $6.44 billion that analysts expect?
- control-3: evidence kept 4 of 4; candidates kept 0 of 0
- Q-1: evidence kept 4 of 4; candidates kept 0 of 0
- Q-2: evidence kept 6 of 6; candidates kept 0 of 1; dropped [c1: candidate ladder: object view rungs must be ['Strongly bullish', 'Bull]
    - cand c1 [DROPPED] binding_obligation/financing_amount due 2027-02-28 | Will NVIDIA's FY2027 annual report commitments note show total commitments under its IREN AI cloud services contract of at least $3.6 billion?
- Q-3: evidence kept 5 of 5; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will Nvidia's FY2027 annual report commitments note show the IREN AI cloud services contract at or above $3.4 billion?

### call 277 · gnews:417f6244f0aaa27123023deb
- control-1: evidence kept 18 of 18; candidates kept 2 of 2
    - cand c1 policy_stage/policy_event due 2027-02-28 | Will the NRC issue a commercial licence for Valar Atomics' Ward 250 microreactor by 2027-02-28?
    - cand c2 binding_obligation/event due 2027-12-31 | Will Nvidia sign a binding agreement with Valar Atomics for the Utah 30 MW AI factory by 2027-12-31?
- control-2: evidence kept 8 of 9; candidates kept 0 of 0; dropped [e8: quote not in item]
- control-3: evidence kept 13 of 14; candidates kept 2 of 2; dropped [e10: quote not in item]
    - cand c1 binding_obligation/event due 2027-01-31 | Will Nvidia and Valar Atomics announce a signed definitive agreement to build or finance the 30 MW Utah AI factory by 2027-01-31?
    - cand c2 policy_stage/policy_event due 2027-01-31 | Will a US court or the NRC issue a ruling by 2027-01-31 holding that the NRC lacks licensing authority over some microreactors?
- Q-1: evidence kept 9 of 9; candidates kept 2 of 2
    - cand c1 policy_stage/policy_event due 2027-01-31 | Will a court ruling in the Texas and Utah litigation against the NRC hold by 2027-01-31 that the NRC lacks licensing authority over some microreactors?
    - cand c2 binding_obligation/event due 2027-01-31 | Will Nvidia sign a binding financing, purchase or capacity commitment for the 30 MW Utah nuclear-powered AI factory by 2027-01-31?
- Q-2: evidence kept 10 of 11; candidates kept 2 of 2; dropped [e2: quote not in item]
    - cand c1 binding_obligation/event due 2027-01-31 | Will Nvidia sign a binding agreement with Valar Atomics to build the 30-megawatt Utah AI factory by 2027-01-31?
    - cand c2 policy_stage/policy_event due 2026-12-31 | Will a federal court rule that the NRC lacks licensing authority over some microreactors by 2026-12-31?
- Q-3: evidence kept 14 of 14; candidates kept 2 of 2
    - cand c1 binding_obligation/event due 2027-01-31 | Will Nvidia and Valar publicly announce a signed binding agreement for financing, purchase, guarantee or capacity commitment for the 30 MW Utah AI factory by 2027-01-31?
    - cand c2 policy_stage/policy_event due 2027-01-31 | Will a court rule by 2027-01-31 that the NRC lacks licensing authority over Ward 250-type microreactors?

### call 312 · gnews:8d5c91ae833af14257a59b2b
- control-1: evidence kept 7 of 7; candidates kept 0 of 0
- control-2: evidence kept 5 of 5; candidates kept 0 of 0
- control-3: evidence kept 6 of 6; candidates kept 0 of 0
- Q-1: evidence kept 6 of 6; candidates kept 0 of 0
- Q-2: evidence kept 5 of 5; candidates kept 0 of 0
- Q-3: evidence kept 5 of 5; candidates kept 0 of 0

### call 379 · gnews:d0f3f83296df884fae64921e
- control-1: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 industry_aggregate/spend_total due 2027-02-28 | Will the combined calendar-2026 data center capital expenditure of the AI hyperscalers reach at least $650 billion?
- control-2: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 industry_aggregate/capex due 2027-02-28 | What will AI hyperscalers' combined data center capital expenditures total for calendar 2026?
- control-3: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 industry_aggregate/capex due 2028-03-31 | Will the combined data center capital expenditure of AI hyperscalers in calendar 2027 reach at least $1 trillion?
- Q-1: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 industry_aggregate/spend_total due 2028-03-31 | Will the combined data center capital expenditure of the AI hyperscalers for calendar 2027 exceed $1 trillion?
- Q-2: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 industry_aggregate/capex due 2027-02-28 | Will the combined calendar-2026 data-center capital expenditure of the AI hyperscalers be at or above $650 billion?
- Q-3: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 industry_aggregate/spend_total due 2028-03-31 | Will the combined 2027 data center capital expenditure of AI hyperscalers reach $1 trillion or more?

### call 381 · gnews:784c556d2e58ed09dd8aa7fc
- control-1: evidence kept 17 of 17; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2027-01-31 | Will a US federal law phasing out Chinese-made lidar sensors be enacted by 2027-01-31?
- control-2: evidence kept 10 of 10; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2027-02-01 | Will the US House pass legislation phasing out Chinese-made lidar technology in the United States by 2027-02-01?
- control-3: evidence kept 20 of 20; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2027-01-31 | Will the US Congress enact a law phasing out Chinese-made lidar sensors in the United States by 2027-01-31?
- Q-1: evidence kept 16 of 16; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2027-01-31 | Will a federal law phasing out Chinese-made lidar technology in the United States be enacted by 2027-01-31?
- Q-2: evidence kept 13 of 13; candidates kept 0 of 0
- Q-3: evidence kept 25 of 26; candidates kept 0 of 0; dropped [e10: quote not in item]

### call 395 · gnews:c6445931955f107b551cce85
- control-1: evidence kept 11 of 11; candidates kept 0 of 0
- control-2: evidence kept 10 of 10; candidates kept 0 of 0
- control-3: evidence kept 12 of 12; candidates kept 0 of 0
- Q-1: evidence kept 11 of 11; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2027-01-31 | Will a Singapore court convict Alan Wei of at least one charge in the Aperia case by 2027-01-31?
- Q-2: evidence kept 8 of 8; candidates kept 0 of 0
- Q-3: evidence kept 13 of 13; candidates kept 0 of 0

### call 356 · nvblog:nvidia-vera-max-single-threaded-cpu-at-scale
- control-1: evidence kept 8 of 8; candidates kept 0 of 0
- control-2: evidence kept 9 of 9; candidates kept 0 of 0
- control-3: evidence kept 9 of 9; candidates kept 0 of 0
- Q-1: evidence kept 9 of 9; candidates kept 0 of 0
- Q-2: evidence kept 9 of 9; candidates kept 0 of 0
- Q-3: evidence kept 10 of 10; candidates kept 0 of 0

### call 358 · nvblog:hugging-face-lerobot-models-frameworks-open-robotics
- control-1: evidence kept 4 of 4; candidates kept 0 of 0
- control-2: evidence kept 4 of 4; candidates kept 0 of 0
- control-3: evidence kept 4 of 4; candidates kept 0 of 0
- Q-1: evidence kept 4 of 4; candidates kept 0 of 0
- Q-2: evidence kept 4 of 4; candidates kept 0 of 0
- Q-3: evidence kept 5 of 5; candidates kept 0 of 0

### call 3 · nvblog:nvidia-unlocks-ai-compute-at-scale-capital-partners-to-power-ai-infrastructure-buildout
- control-1: evidence kept 4 of 4; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-12-31 | Will NVIDIA announce a signed revenue-sharing and credit-support agreement with at least one AI cloud company under its new DSX AI factory model by 2027-12-31?
- control-2: evidence kept 3 of 3; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-01-31 | Will NVIDIA disclose a signed revenue-sharing and credit-support agreement with at least one AI cloud by the end of FY2027?
- control-3: evidence kept 2 of 2; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-12-31 | Will NVIDIA sign a credit-support or revenue-sharing agreement with at least one AI cloud provider by 2027-12-31?
- Q-1: evidence kept 3 of 3; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-02-15 | Will NVIDIA's FY2027 annual report disclose a signed credit-support or guarantee arrangement for AI cloud partners' capacity?
- Q-2: evidence kept 5 of 5; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-01 | Will NVIDIA's FY2027 annual report commitments note show credit-support and guarantee amounts to AI clouds under the revenue-sharing model of at least $1 billion?
- Q-3: evidence kept 3 of 3; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-02-28 | Will NVIDIA sign or disclose a credit-support arrangement with an AI cloud under its revenue-sharing model by 2027-02-28?

### call 15 · gnews:4d1677af37befd53ca3e7b45
- control-1: evidence kept 11 of 11; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will NVIDIA's total guarantees and backstop commitments for cloud providers' capacity and customer leases, as reported in its FY2027 annual report commitments note, reach
- control-2: evidence kept 11 of 11; candidates kept 1 of 2; dropped [c1: candidate ladder: object view rungs must be ['Strongly bullish', 'Bull]
    - cand c1 [DROPPED] binding_obligation/financing_amount due 2027-02-25 | What total amount of NVIDIA's customer capacity purchase and lease guarantee commitments will its FY2027 annual report disclose?
    - cand c2 binding_obligation/event due 2026-12-31 | Will NVIDIA sign a financial guarantee for OpenAI's lease of the Ohio data center by 2026-12-31?
- control-3: evidence kept 11 of 11; candidates kept 2 of 2
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will NVIDIA's financing commitments for customer capacity guarantees, lease backstops and repurchase obligations reach at most the threshold in each range by the FY2027 a
    - cand c2 binding_obligation/event due 2026-12-31 | Will NVIDIA sign a financial guarantee for OpenAI's lease of the Ohio data center by 2026-12-31?
- Q-1: evidence kept 12 of 12; candidates kept 2 of 2
    - cand c1 binding_obligation/financing_amount due 2027-02-26 | Will NVIDIA's disclosed guarantee and capacity-backstop commitments to cloud-provider customers total under $5 billion, $5-10 billion, $10-20 billion, $20-40 billion, or 
    - cand c2 binding_obligation/event due 2027-01-31 | Will NVIDIA publicly announce a signed revenue-share or capacity-repurchase agreement with a cloud provider other than Firmus and Sharon AI by 2027-01-31?
- Q-2: evidence kept 13 of 13; candidates kept 2 of 2
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will NVIDIA's committed financing for cloud-provider capacity backstops and lease guarantees reach at least $10 billion in its FY2027 annual report?
    - cand c2 binding_obligation/event due 2027-01-31 | Will NVIDIA sign a financial guarantee for OpenAI's lease of an Ohio data center by 2027-01-31?
- Q-3: evidence kept 11 of 11; candidates kept 2 of 2
    - cand c1 binding_obligation/event due 2027-01-31 | Will NVIDIA sign a financial guarantee for OpenAI's lease of the Ohio data center by 2027-01-31?
    - cand c2 binding_obligation/financing_amount due 2027-02-26 | What total amount of NVIDIA capacity guarantees and lease guarantees to cloud providers will the FY2027 annual report disclose?

### call 39 · gnews:c3e020d179ab025bf3ba56b0
- control-1: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will the commitments Nvidia reports under its neocloud revenue-sharing and credit-support backstop programme, as shown in the FY2027 annual report commitments note, total
- control-2: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will Nvidia's total financing commitments under its neocloud backstop and credit-support arrangements reach the stated USD amount by the end of FY2027, as shown in the co
- control-3: evidence kept 7 of 7; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will Nvidia's FY2027 annual report show total financing commitments under its neocloud GPU backstop and revenue-share programmes of at least $5 billion?
- Q-1: evidence kept 7 of 7; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-15 | Will the amount of Nvidia's committed backstop and credit-support obligations for neocloud customers, as disclosed in the FY2027 annual report commitments note, be at lea
- Q-2: evidence kept 7 of 7; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will Nvidia's FY2027 annual report disclose total customer backstop and credit-support commitments of at least $5 billion?
- Q-3: evidence kept 7 of 7; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will the committed amount of Nvidia's customer backstop and revenue-share programme, as shown in the FY2027 annual report commitments note, be at least $2bn and below $5b

### call 69 · gnews:f8d63eab0337895e8e95cf02
- control-1: evidence kept 13 of 13; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2027-01-31 | Will the Chinese government publicly permit imports of Nvidia H200 chips by the end of FY2027?
- control-2: evidence kept 11 of 12; candidates kept 1 of 1; dropped [e3: quote not in item]
    - cand c1 policy_stage/policy_event due 2026-12-31 | Will China's government lift its block on Nvidia H200 sales to Chinese customers by 2026-12-31?
- control-3: evidence kept 13 of 13; candidates kept 1 of 1
    - cand c1 policy_stage/event due 2027-01-31 | Will the Chinese government authorise Nvidia to sell H200 chips in China by the end of FY2027?
- Q-1: evidence kept 10 of 10; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2027-01-31 | Will the Chinese government authorise imports of Nvidia H200 chips by 2027-01-31?
- Q-2: evidence kept 10 of 10; candidates kept 1 of 1
    - cand c1 policy_stage/policy_event due 2027-01-31 | Will China's government authorise Nvidia H200 sales into China by 2027-01-31?
- Q-3: evidence kept 12 of 12; candidates kept 1 of 1
    - cand c1 policy_stage/event due 2027-02-25 | Will the Chinese government permit Nvidia H200 chip imports into China by 2027-02-25?

### call 146 · gnews:92c7e54d38dc2916aa185568
- control-1: evidence kept 3 of 3; candidates kept 2 of 2
    - cand c1 industry_aggregate/spend_total due 2027-02-28 | Will the combined 2026 data center capital expenditure of the big four AI hyperscalers reach at least $650 billion?
    - cand c2 main_driver/growth_rate due 2027-02-28 | Will NVIDIA's FY2027 total revenue growth reach at least 82%?
- control-2: evidence kept 3 of 3; candidates kept 2 of 2
    - cand c1 main_driver/total_revenue due 2027-02-28 | Will NVDA's FY2027 total revenue growth, versus FY2026, reach the 82% projected by Wall Street analysts?
    - cand c2 industry_aggregate/capex due 2027-02-28 | Will the combined 2026 data center capital expenditure of the big four AI hyperscalers reach the about $650 billion planned for 2026?
- control-3: evidence kept 3 of 3; candidates kept 2 of 2
    - cand c1 main_driver/growth_rate due 2027-02-28 | Will NVIDIA's total revenue growth for FY2027 (February 2026 to January 2027) be at least 82% year over year, as analysts projected?
    - cand c2 industry_aggregate/spend_total due 2028-02-28 | Will the combined 2027 data center capital expenditure of the big four AI hyperscalers reach $1 trillion?
- Q-1: evidence kept 3 of 3; candidates kept 2 of 2
    - cand c1 industry_aggregate/capex due 2027-02-28 | Will the big four AI hyperscalers' combined 2026 data center capital expenditure reach about $650 billion?
    - cand c2 main_driver/growth_rate due 2027-02-28 | Will Nvidia's FY2027 total revenue growth reach the 82% analysts project?
- Q-2: evidence kept 3 of 3; candidates kept 2 of 2
    - cand c1 main_driver/growth_rate due 2027-02-25 | Will Nvidia's FY2027 total revenue growth reach the roughly 82% that Wall Street analysts projected?
    - cand c2 industry_aggregate/spend_total due 2028-02-15 | What will the combined 2027 data center capital expenditure of the big four AI hyperscalers be?
- Q-3: evidence kept 3 of 3; candidates kept 2 of 2
    - cand c1 main_driver/growth_rate due 2027-02-24 | Will NVDA's FY2027 total revenue growth, reported in its FY2027 annual report, reach the 82% that Wall Street analysts project?
    - cand c2 industry_aggregate/capex due 2027-02-15 | Will the combined calendar 2026 data center capital expenditure of the big four AI hyperscalers reach the around $650 billion planned for 2026?

### call 180 · gnews:552f8c2bdfd080555d592587
- control-1: evidence kept 8 of 8; candidates kept 2 of 2
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia begin volume shipments of its Kyber NVL144 rack-scale system by 2027-12-31?
    - cand c2 main_driver/event due 2026-12-31 | Will Nvidia ship Vera Rubin systems to cloud partners by 2026-12-31?
- control-2: evidence kept 7 of 7; candidates kept 1 of 1
    - cand c1 main_driver/event due 2027-01-31 | Will Nvidia begin shipping Kyber NVL144 racks to customers by 2027-01-31?
- control-3: evidence kept 7 of 7; candidates kept 1 of 1
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia begin shipping the Kyber NVL144 rack architecture to customers by 2027-12-31?
- Q-1: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia ship Kyber NVL144 rack-scale systems to customers by 2027-12-31?
- Q-2: evidence kept 8 of 8; candidates kept 1 of 1
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia ship Kyber NVL144 rack systems to customers by 2027-12-31?
- Q-3: evidence kept 6 of 6; candidates kept 2 of 2
    - cand c1 main_driver/event due 2027-12-31 | Will Nvidia announce customer shipments of Kyber NVL144 rack systems by 2027-12-31?
    - cand c2 main_driver/event due 2027-01-31 | Will Nvidia begin shipping Rubin systems to cloud partners by the end of fiscal 2027?

## Arm G: 'revenue' dropped from the 82% growth forecast (w209-2)
- old: who did or said what, how much and for which period.
- new: who did or said what, how much and for which period, naming the measure even when a neighbouring sentence gives it.

### call 209 · gnews:71df54965281684cc500960f
- control-1: evidence kept 5 of 5; candidates kept 2 of 2
    - e2 | third_party_view | Wall Street analysts expect 82% growth for the rest of FY2027 (figure as cited; metric not specified).
    - e3 | third_party_view | Wall Street analysts expect growth of 41% for 2027 (figure as cited; metric not specified).
    - cand c1 industry_aggregate/spend_total due 2027-03-31 | Will combined hyperscaler capital spending in calendar 2026 reach management's projected $650 billion?
    - cand c2 industry_aggregate/spend_total due 2028-03-31 | Will combined hyperscaler capital spending in calendar 2027 top $1 trillion as management projected?
- control-2: evidence kept 5 of 5; candidates kept 1 of 1
    - e2 | third_party_view | Wall Street analysts expect 82% growth for the rest of FY2027 and 41% growth for 2027.
    - cand c1 industry_aggregate/spend_total due 2028-02-28 | Will combined calendar-2027 capital spending by hyperscalers reach $1 trillion or more?
- control-3: evidence kept 5 of 5; candidates kept 1 of 1
    - e2 | third_party_view | Wall Street analysts project 82% growth for the rest of calendar 2026, per the author.
    - e3 | third_party_view | Analysts project 41% growth for 2027, per the author.
    - cand c1 industry_aggregate/capex due 2028-03-31 | Will the combined calendar 2027 capital spending of the major hyperscale cloud providers reach $1 trillion?
- G-1: evidence kept 5 of 5; candidates kept 1 of 1
    - e2 | third_party_view | Wall Street analysts expect 82% growth for the rest of fiscal 2027.
    - e3 | third_party_view | Wall Street analysts expect 41% growth in 2027.
    - cand c1 industry_aggregate/spend_total due 2028-02-28 | Will combined calendar 2027 capital spending by hyperscale cloud providers reach at least $1 trillion?
- G-2: evidence kept 4 of 4; candidates kept 1 of 1
    - e2 | third_party_view | Wall Street analysts expect Nvidia revenue growth of 82% for the rest of FY2027 and 41% for 2027.
    - cand c1 industry_aggregate/spend_total due 2028-02-15 | Will combined hyperscaler capital spending in calendar 2027 reach $1 trillion or more?
- G-3: evidence kept 5 of 5; candidates kept 2 of 2
    - e2 | third_party_view | Wall Street analysts expect Nvidia's revenue growth for the rest of FY2027 to be 82%.
    - e3 | third_party_view | Wall Street analysts expect Nvidia's growth in 2027 to rise to 41%.
    - cand c1 main_driver/growth_rate due 2027-02-28 | Will NVIDIA's total revenue for fiscal 2027 (February 2026 to January 2027) grow at least 82% year over year?
    - cand c2 industry_aggregate/spend_total due 2028-02-28 | Will combined 2027 capital spending by hyperscale cloud providers reach $1 trillion or more?

### call 146 · gnews:92c7e54d38dc2916aa185568
- control-1: evidence kept 3 of 3; candidates kept 2 of 2
    - e3 | third_party_view | Wall Street analysts project Nvidia revenue growth of 82% for FY2027 and 41% for FY2028.
    - cand c1 industry_aggregate/spend_total due 2027-02-28 | Will the combined 2026 data center capital expenditure of the big four AI hyperscalers reach at least $650 billion?
    - cand c2 main_driver/growth_rate due 2027-02-28 | Will NVIDIA's FY2027 total revenue growth reach at least 82%?
- control-2: evidence kept 3 of 3; candidates kept 2 of 2
    - e3 | third_party_view | Wall Street analysts project Nvidia revenue growth of 82% for FY2027 and 41% for FY2028.
    - cand c1 main_driver/total_revenue due 2027-02-28 | Will NVDA's FY2027 total revenue growth, versus FY2026, reach the 82% projected by Wall Street analysts?
    - cand c2 industry_aggregate/capex due 2027-02-28 | Will the combined 2026 data center capital expenditure of the big four AI hyperscalers reach the about $650 billion planned for 2026?
- control-3: evidence kept 3 of 3; candidates kept 2 of 2
    - e3 | third_party_view | Author cites Wall Street analysts projecting Nvidia revenue growth of 82% for FY2027 and 41% for FY2028.
    - cand c1 main_driver/growth_rate due 2027-02-28 | Will NVIDIA's total revenue growth for FY2027 (February 2026 to January 2027) be at least 82% year over year, as analysts projected?
    - cand c2 industry_aggregate/spend_total due 2028-02-28 | Will the combined 2027 data center capital expenditure of the big four AI hyperscalers reach $1 trillion?
- G-1: evidence kept 3 of 3; candidates kept 3 of 3
    - e3 | third_party_view | Author cites Wall Street analysts' projections of Nvidia revenue growth of 82% for FY2027 and 41% for FY2028.
    - cand c1 industry_aggregate/spend_total due 2027-02-15 | Will the combined 2026 data center capital expenditure of the big four AI hyperscalers be below, near or above the roughly $650 billion plan cited in the item?
    - cand c2 industry_aggregate/spend_total due 2028-02-15 | Will the combined 2027 data center capital expenditure of the big four AI hyperscalers reach the roughly $1 trillion Nvidia projected?
    - cand c3 main_driver/growth_rate due 2027-02-25 | Will Nvidia's FY2027 total revenue growth reach the roughly 82% that Wall Street analysts projected?
- G-2: evidence kept 3 of 3; candidates kept 2 of 2
    - e1 | third_party_view | Wall Street analysts project Nvidia revenue growth of 82% for FY2027 (this year) and 41% for FY2028 (next year).
    - cand c1 main_driver/total_revenue due 2027-02-25 | Will NVIDIA's FY2027 total revenue growth be at least 82%?
    - cand c2 industry_aggregate/capex due 2027-02-28 | Will the combined calendar 2026 data center capital expenditure of the big four AI hyperscalers reach at least $650 billion?
- G-3: evidence kept 3 of 3; candidates kept 2 of 2
    - e3 | third_party_view | Author cites Wall Street analysts' projections of Nvidia revenue growth of 82% for FY2027 and 41% for FY2028.
    - cand c1 main_driver/growth_rate due 2027-02-25 | Will NVDA's total revenue for FY2027 grow by at least 82% over FY2026, matching the analyst consensus cited in the item?
    - cand c2 industry_aggregate/capex due 2027-02-28 | Will the combined 2026 data center capital expenditure of the big four AI hyperscalers reach at least $650 billion?

## Arm L: obligation amount questions refused by the sift for neutral rung labels
- old: A five-rung asset ladder runs from Strongly bullish
- new: A five-rung asset ladder, which every candidate whose object is a ticker has (an obligation amount too), runs from Strongly bullish

### call 3 · nvblog:nvidia-unlocks-ai-compute-at-scale-capital-partners-to-power-ai-infrastructure-buildout
- control-1: evidence kept 4 of 4; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-12-31 | Will NVIDIA announce a signed revenue-sharing and credit-support agreement with at least one AI cloud company under its new DSX AI factory model by 2027-12-31? | rungs: Yes, No
- control-2: evidence kept 3 of 3; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-01-31 | Will NVIDIA disclose a signed revenue-sharing and credit-support agreement with at least one AI cloud by the end of FY2027? | rungs: Yes, No
- control-3: evidence kept 2 of 2; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-12-31 | Will NVIDIA sign a credit-support or revenue-sharing agreement with at least one AI cloud provider by 2027-12-31? | rungs: Yes, No
- L-1: evidence kept 3 of 3; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-02-26 | Will NVIDIA disclose a signed credit-support commitment to an AI cloud under its revenue-sharing model in its FY2027 annual report? | rungs: Yes, No
- L-2: evidence kept 3 of 3; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-01 | Will NVIDIA's FY2027 annual report show commitments and credit support extended to AI cloud partners under its revenue-sharing and credit-support model of at least $10 bi | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- L-3: evidence kept 4 of 4; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-02-25 | Will NVIDIA's FY2027 annual report disclose a signed credit-support or guarantee commitment to one or more AI cloud partners? | rungs: Yes, No

### call 15 · gnews:4d1677af37befd53ca3e7b45
- control-1: evidence kept 11 of 11; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will NVIDIA's total guarantees and backstop commitments for cloud providers' capacity and customer leases, as reported in its FY2027 annual report commitments note, reach | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- control-2: evidence kept 11 of 11; candidates kept 1 of 2; dropped [c1: candidate ladder: object view rungs must be ['Strongly bullish', 'Bull]
    - cand c1 [DROPPED] binding_obligation/financing_amount due 2027-02-25 | What total amount of NVIDIA's customer capacity purchase and lease guarantee commitments will its FY2027 annual report disclose? | rungs: Below $3.5 billion, $3.5 billion to under $10 billion, $10 billion to under $25 billion, $25 billion to under $50 billion, $50 billion or more
    - cand c2 binding_obligation/event due 2026-12-31 | Will NVIDIA sign a financial guarantee for OpenAI's lease of the Ohio data center by 2026-12-31? | rungs: Signed, Not signed
- control-3: evidence kept 11 of 11; candidates kept 2 of 2
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will NVIDIA's financing commitments for customer capacity guarantees, lease backstops and repurchase obligations reach at most the threshold in each range by the FY2027 a | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
    - cand c2 binding_obligation/event due 2026-12-31 | Will NVIDIA sign a financial guarantee for OpenAI's lease of the Ohio data center by 2026-12-31? | rungs: Yes, No
- L-1: evidence kept 11 of 11; candidates kept 2 of 2
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will NVIDIA's financing guarantees and capacity backstops under the AI Compute Partnership total at least $10 billion in commitments in its FY2027 annual report? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
    - cand c2 binding_obligation/event due 2026-12-31 | Will NVIDIA sign a financial guarantee for OpenAI's lease of the Ohio data center by 2026-12-31? | rungs: Yes, No
- L-2: evidence kept 11 of 11; candidates kept 2 of 2
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will NVIDIA's disclosed capacity guarantees and lease backstops for cloud providers, as stated in the FY2027 annual report commitments note, total below $8 billion, betwe | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
    - cand c2 binding_obligation/event due 2026-12-31 | Will NVIDIA sign a financial guarantee for OpenAI's lease of the Ohio data center by 2026-12-31? | rungs: Yes, No
- L-3: evidence kept 10 of 10; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will NVIDIA's total financing amount for customer capacity and lease guarantees, as shown in the FY2027 annual report commitments note, be below $3.5 billion, $3.5 billio | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish

### call 37 · gnews:3854aeddaa3f31de00cf2816
- control-1: evidence kept 7 of 7; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will the financing amount Nvidia's credit-support and revenue-sharing commitments reach in FY2027 be below $100 million (strongly bullish), $100 million to under $500 mil | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- control-2: evidence kept 8 of 8; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will Nvidia's FY2027 annual report show financing commitments under its revenue-sharing and credit-support programme reaching a given amount? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- control-3: evidence kept 10 of 10; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will Nvidia's FY2027 annual report commitments note disclose credit-support obligations to AI cloud partners of at least $1 billion? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- L-1: evidence kept 9 of 9; candidates kept 2 of 2
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will Nvidia's credit-support commitments under its revenue-sharing and credit-support model reach at least $1 billion, as shown in the FY2027 annual report commitments no | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
    - cand c2 main_driver/gross_margin due 2027-02-28 | Will Nvidia's FY2027 GAAP gross margin be at least 73%, as reported in the FY2027 annual report?
- L-2: evidence kept 11 of 11; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will Nvidia's FY2027 annual report commitments note show financing and credit support to AI cloud partners of at least $5 billion? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- L-3: evidence kept 10 of 10; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | What amount of credit-support and financing commitments will Nvidia's FY2027 annual report disclose for its revenue-sharing and credit-support programme? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish

### call 39 · gnews:c3e020d179ab025bf3ba56b0
- control-1: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will the commitments Nvidia reports under its neocloud revenue-sharing and credit-support backstop programme, as shown in the FY2027 annual report commitments note, total | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- control-2: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will Nvidia's total financing commitments under its neocloud backstop and credit-support arrangements reach the stated USD amount by the end of FY2027, as shown in the co | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- control-3: evidence kept 7 of 7; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will Nvidia's FY2027 annual report show total financing commitments under its neocloud GPU backstop and revenue-share programmes of at least $5 billion? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- L-1: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | What amount of revenue-sharing and credit-support commitments to neocloud customers will Nvidia's FY2027 commitments note disclose? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- L-2: evidence kept 8 of 8; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will the financing amount Nvidia's neocloud revenue-sharing and credit-support backstop reaches in FY2027 be at least $1bn, per the FY2027 annual report commitments note? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- L-3: evidence kept 7 of 7; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will the amount Nvidia has committed under its neocloud GPU backstop and revenue-sharing programme, as shown in the commitments note of its FY2027 annual report, be below | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish

### call 82 · gnews:bf158d067256a39f02f7c7ce
- control-1: evidence kept 4 of 4; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-01-31 | Will NVIDIA sign at least one revenue-sharing or credit-support agreement with a cloud provider under its AI factory framework by 2027-01-31? | rungs: Yes, No
- control-2: evidence kept 4 of 4; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will NVIDIA's FY2027 annual filing show credit-support and revenue-sharing commitments to AI cloud partners of at least US$5 billion? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- control-3: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-02-28 | Will NVIDIA announce a signed credit-support agreement with an AI cloud provider under its revenue-sharing AI factory framework by 2027-02-28? | rungs: Yes, No
- L-1: evidence kept 4 of 4; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-02-15 | Will NVIDIA sign at least one revenue-sharing or credit-support agreement with an AI cloud partner under its AI factory framework by 2027-02-15? | rungs: Yes, No
- L-2: evidence kept 4 of 4; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-01-31 | Will NVIDIA sign a credit-support agreement with a cloud provider under its AI compute framework by 2027-01-31? | rungs: Yes, No
- L-3: evidence kept 5 of 5; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-01-31 | Will NVIDIA publicly sign or disclose a revenue-sharing or credit-support agreement with an AI cloud partner for AI factory capacity by 2027-01-31? | rungs: Yes, No

### call 111 · gnews:9e0d5b0d6b3e603c60340128
- control-1: evidence kept 8 of 9; candidates kept 1 of 1; dropped [e4: quote not in item]
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will Nvidia's FY2027 annual report disclose AI Compute Partnership backstop commitments totalling at least $1 billion, $5 billion, $10 billion or $20 billion, as settled  | rungs: Strongly bearish, Bearish, Neutral, Bullish, Strongly bullish
- control-2: evidence kept 7 of 7; candidates kept 0 of 1; dropped [c1: candidate ladder: object view rungs must be ['Strongly bullish', 'Bull]
    - cand c1 [DROPPED] binding_obligation/financing_amount due 2027-02-15 | Will Nvidia's FY2027 annual report show AI Compute Partnership backstop commitments of at least $1 billion, and at what level? | rungs: Under $1B, $1B to under $5B, $5B to under $10B, $10B to under $20B, $20B or more
- control-3: evidence kept 6 of 7; candidates kept 0 of 1; dropped [c1: candidate ladder: object view rungs must be ['Strongly bullish', 'Bull; e2: quote not in item]
    - cand c1 [DROPPED] binding_obligation/financing_amount due 2027-02-26 | What total dollar amount of financing commitments under Nvidia's AI Compute Partnership backstop will Nvidia's FY2027 annual filing report? | rungs: Very small, Small, Moderate, Large, Very large
- L-1: evidence kept 8 of 8; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will the total amount of Nvidia's AI Compute Partnership backstop commitments reported in the FY2027 annual report fall in which range? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- L-2: evidence kept 9 of 10; candidates kept 1 of 1; dropped [e4: quote not in item]
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will Nvidia's disclosed commitments under the AI Compute Partnership backstop programme reach at least $2 billion by the end of FY2027 (2027-01-31), per the FY2027 annual | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- L-3: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | What financing amount will Nvidia's FY2027 commitments note show for its AI Compute Partnership GPU backstop? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish

### call 143 · gnews:1e7a9c953f3ad70093b67ae4
- control-1: evidence kept 5 of 5; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-02-25 | Will Nvidia's FY2027 annual report disclose at least one signed revenue-sharing financing agreement with an AI cloud provider? | rungs: Yes, No
- control-2: evidence kept 6 of 6; candidates kept 0 of 1; dropped [c1: candidate ladder: object view rungs must be ['Strongly bullish', 'Bull]
    - cand c1 [DROPPED] binding_obligation/financing_amount due 2027-02-28 | What financing amount will Nvidia's revenue-sharing financing programme for AI cloud providers reach in its FY2027 annual report commitments note? | rungs: Under $1bn, $1bn to under $5bn, $5bn to under $10bn, $10bn to under $20bn, $20bn or more
- control-3: evidence kept 4 of 4; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will Nvidia's FY2027 annual report disclose credit support and financing commitments under its revenue-sharing AI cloud financing model totalling at least $30 billion? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- L-1: evidence kept 5 of 5; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-01-31 | Will Nvidia sign or announce a credit-support or guarantee agreement for AI cloud operators under its revenue-sharing financing model by 2027-01-31? | rungs: Yes, No
- L-2: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-24 | What amount of credit-support commitments under Nvidia's revenue-sharing financing programme will the FY2027 annual report disclose? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- L-3: evidence kept 6 of 6; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will Nvidia's FY2027 annual report show financing commitments under its revenue-sharing AI cloud financing model of at least $2 billion? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish

### call 210 · gnews:085b1e1a1543437edb9756d6
- control-1: evidence kept 18 of 18; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will Nvidia's disclosed backstop commitments for Neocloud GPU capacity, as shown in its FY2027 annual report commitments note, total at least $10B? | rungs: Strongly bearish, Bearish, Neutral, Bullish, Strongly bullish
- control-2: evidence kept 18 of 18; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-26 | Will Nvidia's FY2027 annual report commitments note disclose backstop commitments to Neoclouds of at least $5 billion? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- control-3: evidence kept 14 of 16; candidates kept 1 of 2; dropped [c2: year 2028 is beyond next year: not opened (06-views 不开); e13: quote not in item; e16: quote not in item]
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will Nvidia's FY2027 annual report show backstop commitments to Neoclouds of at least $10B? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
    - cand c2 [DROPPED] industry_aggregate/spend_total due 2029-03-31 | Will combined AI capital spending in calendar 2028 reach at least $2T?
- L-1: evidence kept 17 of 18; candidates kept 1 of 2; dropped [c2: year 2028 is beyond next year: not opened (06-views 不开); e14: quote not in item]
    - cand c1 binding_obligation/financing_amount due 2027-02-25 | Will Nvidia's disclosed backstop commitments for GPU rental offtakes and datacenter leases reach the stated amount in its FY2027 annual report? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
    - cand c2 [DROPPED] industry_aggregate/spend_total due 2029-02-28 | Will combined AI capital spending in calendar 2028, including IT and datacenter capex, reach the stated level?
- L-2: evidence kept 16 of 16; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-15 | Will Nvidia's outstanding GPU rental backstop commitments reach at least $12 billion at the FY2027 year-end (ending January 2027)? | rungs: Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish
- L-3: evidence kept 11 of 11; candidates kept 1 of 1
    - cand c1 binding_obligation/financing_amount due 2027-02-28 | Will Nvidia's disclosed commitments under its GPU rental backstop program reach the stated amount in its FY2027 annual report commitments note? | rungs: Strongly bearish, Bearish, Neutral, Bullish, Strongly bullish

### call 262 · gnews:6ab3379f10dfeb28924ebb57
- control-1: evidence kept 9 of 9; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-01-31 | Will NVIDIA sign a credit-support commitment for a DSX AI factory under its July 1, 2026 revenue-sharing model by 2027-01-31? | rungs: Yes, No
- control-2: evidence kept 11 of 11; candidates kept 0 of 0
- control-3: evidence kept 6 of 6; candidates kept 0 of 0
- L-1: evidence kept 7 of 7; candidates kept 1 of 1
    - cand c1 binding_obligation/event due 2027-02-28 | Will NVIDIA's FY2027 annual report disclose at least one signed revenue-sharing agreement under the July 1, 2026 model? | rungs: Yes, No
- L-2: evidence kept 8 of 8; candidates kept 0 of 0
- L-3: evidence kept 7 of 7; candidates kept 0 of 0


# The same week, both systems: the statements each latest answer cites

Second page of [`SIDE-BY-SIDE-WEEK.md`](SIDE-BY-SIDE-WEEK.md), built by the same script. For each question: the stored request of its
latest answer (the call's number in the run's archive and the request's sha256), then every statement that answer cites, with the
system's stored summary and its stored passage from the article. "Stored attribution" is the speaker the system recorded; nobody checked it.
In the new system's store the judge's copy of a passage is cut at 400 characters (129 passages in this run, `adapter-counts.json`).

## Old system

Stored requests: `poc/data/clean-lean-week-2026-11-14/week/p1/prod/archive.sqlite`, table `model_calls`.

<a id="old-v1"></a>

### Old system 1 (`v1`): At NVIDIA’s next annual report, what amount of financing commitments to customers and partners will NVIDIA report in its commitments note?

- Latest answer (2026-09-28): 5 Strongly bearish: Reported commitments total at least $25 billion.
- Stored request: call 713; request sha256 `76aac9c5294280f567f11deebdf9733b70e23cd61194db130c24b49208bc29b7`.
- Cites 23 of the 37 statements linked to the question:

  - `e2` (article 4; stored attribution: NVIDIA; stored kind: third_party_view): NVIDIA plans to provide credit support for nearly 2 gigawatts of computing capacity for another AI lab.
    - Stored passage: "For one more AI lab, it will provide credit support for nearly 2 gigawatts of computing capacity."
  - `e3` (article 4; stored attribution: NVIDIA; stored kind: third_party_view): NVIDIA guarantees some cloud partners a minimum level of revenue on part of a facility’s capacity; the amount and term are not stated.
    - Stored passage: "With some cloud partners, it guarantees a minimum level of revenue on part of a facility’s capacity."
  - `e6` (article 12; stored attribution: Financial Times; stored kind: rumour): The Financial Times reported on 2026-09-22 that SB Energy slowed IPO preparations around a $50 billion valuation and that its $4.9 billion debt package faced weak demand and yields around 10%.
    - Stored passage: "The SoftBank-backed developer has slowed preparations for an IPO that had been discussed around a $50 billion valuation, according to a September 22 Financial Times report, while a $4.9 billion debt package has faced weak demand and yields around 10%."
  - `e8` (article 12; stored attribution: SB Energy; stored kind: party_statement): SB Energy said it had signed roughly 8.8 gigawatts of IT lease capacity, including the PORTS-Pike campus for OpenAI; the item gives no signing date.
    - Stored passage: "SB Energy says it has signed roughly 8.8 gigawatts of IT lease capacity, including the PORTS-Pike campus in Ohio for OpenAI."
  - `e9` (article 12; stored attribution: NVIDIA; stored kind: fact): NVIDIA is the exclusive AI-compute provider for SB Energy's PORTS-Pike site and is providing credit support for an initial 4.25 gigawatts of capacity, with an option covering another 3.75 gigawatts; the item gives no date.
    - Stored passage: "Nvidia is the exclusive AI-compute provider for that site and is providing credit support for an initial 4.25 gigawatts, with an option covering another 3.75."
  - `e10` (article 12; stored attribution: NVIDIA; stored kind: fact): NVIDIA disclosed that maximum guarantee exposure can reach $105 billion under defined conditions; the item gives no disclosure date.
    - Stored passage: "Nvidia has disclosed maximum guarantee exposure that can reach $105 billion under defined conditions, so the economics become more intertwined with OpenAI's ability to meet its lease obligations."
  - `e12` (article 14; stored attribution: Zacks analyst; stored kind: third_party_view): Zacks says China remains largely closed to data-center compute and NVIDIA is taking on larger supply commitments, customer credit support and long-dated guarantees.
    - Stored passage: "China remains largely closed to data center compute, and NVIDIA is taking on larger supply commitments, customer credit support and long-dated guarantees."
  - `e35` (article 38; stored attribution: NVIDIA; stored kind: fact): NVIDIA is committing $1 billion to Nscale's $3.1 billion convertible financing; the article reports no completion date.
    - Stored passage: "Yet NVIDIA Corporation (NASDAQ: NVDA ) is committing $1 billion to a $3.1 billion convertible financing, while Microsoft Corporation (NASDAQ: MSFT ) is expected to become one of Nscale's most important customers."
  - `e75` (article 54; stored attribution: NVIDIA; stored kind: third_party_view): NVIDIA's guarantee obligations were capped at $108.5 billion.
    - Stored passage: "guarantee obligations are capped at $108.5 billion."
  - `e81` (article 55; stored attribution: Nvidia; stored kind: party_statement): Nvidia extended payment terms on large orders from certain customers.
    - Stored passage: "The company extended payment terms on large orders from certain customers."
  - `e118` (article 88; stored attribution: Nscale; stored kind: fact): Nscale reported a net loss of $1.02 billion for the six months ended June 30, 2026, and its management flagged substantial doubt about its ability to continue as a going concern.
    - Stored passage: "Per the S-1, the company posted a net loss of $1.02 billion in the six months to June 30, 2026—and at one point, its own management flagged “substantial doubt” about its ability to continue as a going concern."
  - `e120` (article 88; stored attribution: Nscale and Nvidia; stored kind: fact): Nvidia agreed to take $1 billion in convertible notes or non-voting shares in Nscale’s $3.1 billion financing round under a subscription agreement signed September 15, 2026.
    - Stored passage: "On Sept. 15, Nscale signed a subscription agreement for a $3.1 billion financing round, of which Nvidia itself is taking $1 billion in convertible notes or non-voting shares."
  - `e121` (article 88; stored attribution: Nvidia; stored kind: fact): Nvidia bought warrants for more than 157,945 Nscale shares for $60 million and agreed to guarantee up to $860.3 million of Nscale’s lease obligations at its Ward County, Texas facility, according to Nscale filings from October 2025.
    - Stored passage: "Previous filings from Nscale’s own U.K. company accounts in October 2025 showed that Nvidia bought warrants for over 157,945 Nscale shares for $60 million—and in exchange, agreed to guarantee up to $860.3 million of Nscale’s lease obligations at a facility in Ward County, Texas."
  - `e122` (article 88; stored attribution: Jensen Huang; stored kind: party_statement): Nvidia CEO Jensen Huang said Nvidia’s support was important to the existence and development of Nscale and CoreWeave.
    - Stored passage: "“ If we didn’t support CoreWeave to exist, these neoclouds, these AI clouds, wouldn’t exist… If we didn’t support Nscale, they wouldn’t be where they are today. “"
  - `e156` (article 98; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management said its investments in frontier AI labs may be characterized as circular financing and that the compute can be redeployed to other customers.
    - Stored passage: "Management concedes some will call this circular financing and says the compute can be redeployed to other customers."
  - `e186` (article 115; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management expects AI labs backed by NVIDIA’s balance sheet to account for roughly one-quarter of NVIDIA’s business in fiscal 2028.
    - Stored passage: "Management expects AI labs backed by NVIDIA’s balance sheet to make up roughly a quarter of NVIDIA’s business in fiscal 2028."
  - `e238` (article 141; stored attribution: Unnamed source quoted in Reuters; stored kind: rumour): Reuters reported this month that Nvidia was in talks to be an anchor investor in Anthropic's planned IPO, with an unnamed source putting Nvidia's possible investment at up to $10 billion.
    - Stored passage: "The chipmaker's in talks to be an anchor investor in Anthropic's planned initial public offering (IPO) , Reuters said this month, a deal that could deepen its ties to a major customer. A source put Nvidia's possible investment at up to $10 billion."
  - `e353` (article 207; stored attribution: People familiar with the talks, as reported by the Financial Times; stored kind: rumour): Unnamed sources told the Financial Times that NVIDIA held talks with insurers about shifting some financing risk tied to its chips, as it seeks to expand demand beyond major technology companies.
    - Stored passage: "NVIDIA Corp (NASDAQ:NVDA) has held talks with insurance companies over ways to shift part of the financing risk tied to its chips as the chipmaker seeks to expand demand beyond major technology companies"
  - `e354` (article 207; stored attribution: People familiar with the talks, as reported by the Financial Times; stored kind: rumour): Unnamed sources told the Financial Times that NVIDIA’s early-stage insurer discussions include potential insurance for loans to smaller neocloud companies, protecting lenders against borrower defaults and insufficient resale value of pledged NVIDIA chips; the discussions may not produce a deal.
    - Stored passage: "The discussions include potential insurance for loans extended to smaller "neocloud" companies, which could protect lenders if a borrower defaults and Nvidia chips pledged as collateral cannot be resold for enough to cover the debt, the FT reported, citing people familiar with the talks. The discussions are at an early stage and may not result in any deals."
  - `e355` (article 207; stored attribution: NVIDIA for sharing data; people familiar with the discussions, as reported by the Financial Times, for the work with Howden Re; stored kind: rumour): NVIDIA has shared chip-depreciation and expected future computing-power value data with at least one insurer and, according to unnamed sources, is working with Howden Re on an insurer-involving structure.
    - Stored passage: "Nvidia has shared data on chip depreciation and the expected future value of computing power with at least one insurer, while people familiar with the discussions said the company was also working with broker Howden Re on a structure involving insurers."
  - `e356` (article 207; stored attribution: People familiar with the discussions, as reported by the Financial Times; stored kind: rumour): Unnamed sources told the Financial Times that NVIDIA has explored using insurance groups to syndicate risk to hedge funds and other alternative investors, with potential deal sizes that could exceed even large insurers’ balance sheets.
    - Stored passage: "Nvidia has explored using insurance groups to syndicate risk to hedge funds and other alternative investors, with the potential size of deals possibly exceeding the balance sheets of even large insurers."
  - `e357` (article 207; stored attribution: People familiar with the discussions, as reported by the Financial Times; stored kind: rumour): The Financial Times reported, citing unnamed sources, that NVIDIA has considered joining consortia with insurers, hedge funds and asset managers.
    - Stored passage: "The company has also considered joining consortia alongside insurers, hedge funds and asset managers, the report added."
  - `e358` (article 207; stored attribution: NVIDIA; stored kind: fact): NVIDIA offered to backstop part of financing deals intended to unlock $500 billion of capital from Wall Street firms including Goldman Sachs and Apollo.
    - Stored passage: "The insurance push comes after Nvidia offered to backstop part of financing deals designed to unlock $500 billion of capital from Wall Street firms including Goldman Sachs and Apollo."

<a id="old-v2"></a>

### Old system 2 (`v2`): How much total revenue will Nvidia report for FY2027?

- Latest answer (2026-09-28): 3 Neutral: Total revenue is at least 393868500000 USD and below 418231500000 USD.
- Stored request: call 716; request sha256 `1f8db0ecc466dab78215eb68b9210b05e48db1dd2630fea743bb7b63a19bf56e`.
- Cites 18 of the 126 statements linked to the question:

  - `e5` (article 11; stored attribution: Zacks; stored kind: third_party_view): Zacks estimated Nvidia total revenue at $406.05 billion for FY2027, up 88% year over year.
    - Stored passage: "For the current and next fiscal years, $406.05 billion and $671.95 billion estimates indicate +88% and +65.5% changes, respectively."
  - `e24` (article 35; stored attribution: NVIDIA; stored kind: fact): NVIDIA reported total revenue of $96.2 billion in fiscal Q2 2027, up 106% year over year and 18% sequentially.
    - Stored passage: "Consolidated revenues soared to $96.2 billion, up 106% year over year and 18% sequentially."
  - `e25` (article 35; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA guided to fiscal Q3 2027 revenue of $108 billion, plus or minus 2%.
    - Stored passage: "NVIDIA further expects profitability to remain strong and projects revenues of $108 billion, plus or minus 2%, in the fiscal third quarter of 2027."
  - `e26` (article 35; stored attribution: Zacks.com; stored kind: third_party_view): Zacks.com calculated that NVIDIA's fiscal Q3 2027 revenue guidance midpoint implies 12% sequential revenue growth.
    - Stored passage: "At the midpoint, this would represent a 12% sequential rise."
  - `e133` (article 92; stored attribution: Zacks.com; stored kind: third_party_view): The Zacks consensus estimate for NVIDIA FY2027 revenue was $406.05 billion, implying 88% year-over-year growth.
    - Stored passage: "The Zacks Consensus Estimate for fiscal 2027 revenues is currently pegged at $406.05 billion, indicating an 88% year-over-year increase."
  - `e164` (article 105; stored attribution: Nvidia; stored kind: fact): Nvidia revenue rose 96% year over year to $178 billion in the first half of FY2027, ended July 26.
    - Stored passage: "In the first half of its fiscal 2027 (which ended July 26), its revenue rose by 96% year over year to $178 billion."
  - `e198` (article 121; stored attribution: fool.com (analyst); stored kind: third_party_view): Analysts' consensus estimate for NVIDIA fiscal 2027 total revenue was around $412 billion.
    - Stored passage: "Analysts' consensus already has fiscal 2027 revenue coming in around $412 billion."
  - `e248` (article 143; stored attribution: NVIDIA; stored kind: party_statement): Nvidia estimates total revenue growth of around 70% for FY2027.
    - Stored passage: "For FY 2027, Nvidia estimates its revenue growth will be around 70%."
  - `e278` (article 163; stored attribution: The Information's two unnamed sources; stored kind: rumour): The Information reported on September 27, 2026, citing two people familiar with the matter, that China's MIIT asked Alibaba and ByteDance how many Nvidia RTX PRO 5500 cards they wanted and why; neither Beijing nor the companies confirmed the plan.
    - Stored passage: "China's Ministry of Industry and Information Technology (MIIT), which oversees the tech sector, asked the two firms how many RTX PRO 5500 cards they want and why. That is according to The Information, citing two people familiar with the matter."
  - `e285` (article 165; stored attribution: Elon Musk; stored kind: party_statement): Elon Musk said on September 25 that Colossus 2 had 110,000 Nvidia GB200s and 440,000 GB300s, with 220,000 additional GB300s planned to come online the following week, another 220,000 GPUs planned for November, and a further 220,000 GB300s hoped for in late December 2026.
    - Stored passage: "In a post on his "X" platform, formerly Twitter, Musk gave an update on Colossus 2, SpaceX's ( SPCX +0.63% ) xAI unit's artificial intelligence (AI) computing cluster. He said the massive AI training supercomputer could double the number of Nvidia graphics processing units (GPUs) deployed by year-end.
In the post, Musk noted that Colossus 2 currently has 110,000 Nvidia GB200 chips and 440,000 GB300s. An additional 220,000 GB300 chips are set to come online next week, with another 220,000 GPUs set for November. He added that he hopes to get another 220,000 GB300s in late December, "if we get lucky.""
  - `e287` (article 165; stored attribution: Elon Musk; stored kind: party_statement): Musk said SpaceX expected to reach around 2 GW of computing power by the end of 2026 and was targeting closer to 10 GW than 5 GW by the end of 2027.
    - Stored passage: "At the time, Musk said SpaceX would end the year with around 2 gigawatts of computing power, while it is looking to end 2027 with closer to 10 gigawatts than 5 gigawatts."
  - `e288` (article 165; stored attribution: The Motley Fool author; stored kind: third_party_view): The author estimated that 1 GW of computing power costs about $50 billion to $60 billion, including about $35 billion of Nvidia chips and other components.
    - Stored passage: "One gigawatt of compute power costs about $50 billion to $60 billion, with chips and other Nvidia components making up about $35 billion of that total cost."
  - `e330` (article 184; stored attribution: The Information; stored kind: rumour): ByteDance is reportedly considering an order of roughly 1 million Nvidia RTX Pro 5500 chips for AI model operations.
    - Stored passage: "ByteDance is considering an order of roughly 1 million RTX Pro 5500 chips to support AI model operations, according to the report."
  - `e331` (article 184; stored attribution: Nvidia, as reported by finance.biggo.com; stored kind: rumour): Nvidia reportedly aims to begin RTX Pro 5500 shipments to China in late December 2026 and supply about 500,000 units per quarter.
    - Stored passage: "Nvidia aims to begin shipments in late December and supply around 500,000 units per quarter to China, meaning a single ByteDance order could absorb approximately two quarters of planned output."
  - `e346` (article 201; stored attribution: Nvidia; stored kind: fact): Nvidia reported second-quarter revenue of $96.22 billion, up 106% year over year, versus consensus of $92.37 billion; adjusted EPS was $2.22 versus consensus of $2.09.
    - Stored passage: "Nvidia reported revenue of $96.22 billion for the second quarter, up 106% year-over-year, alongside adjusted earnings per share of $2.22. Both figures surpassed Wall Street consensus estimates, which called for revenue of $92.37 billion and adjusted earnings of $2.09 per share."
  - `e373` (article 229; stored attribution: Nvidia; stored kind: third_party_view): Nvidia reported FY2026 revenue of approximately $215.9 billion, up approximately 65.5% year over year.
    - Stored passage: "In the fiscal year ended Jan. 25, 2026, revenue reached close to $215.9 billion, a massive increase of approximately 65.5% year over year."
  - `e377` (article 231; stored attribution: Zacks Consensus Estimates; stored kind: third_party_view): Zacks Consensus Estimates project Nvidia FY2027 revenue of $406.05 billion, up 88.04% from the prior year.
    - Stored passage: "For the full year, the Zacks Consensus Estimates are projecting earnings of $9.25 per share and revenue of $406.05 billion, which would represent changes of +93.92% and +88.04%, respectively, from the prior year."
  - `e379` (article 232; stored attribution: NVIDIA management; consensus estimate as reported by Trefis; stored kind: party_statement): NVIDIA management guided fiscal Q3 2027 revenue to $108 billion, plus or minus 2%; Trefis reports consensus revenue of $111.3 billion for the quarter, above the guidance range.
    - Stored passage: "Management guided revenue for that quarter to $108 billion, plus or minus 2%. The consensus forecast for that quarter is $111.3 billion, above the top of that range."

<a id="old-v3"></a>

### Old system 3 (`v3`): How much total revenue will Nvidia report for FY2028?

- Latest answer (2026-09-28): 2 Bullish: Total revenue is at least 692108500000 USD and below 739145000000 USD.
- Stored request: call 717; request sha256 `c8f6a3629259a3a512aae7b598f04edde80a6b210accb3e15f50b5cb7953f417`.
- Cites 34 of the 47 statements linked to the question:

  - `e5` (article 11; stored attribution: Zacks; stored kind: third_party_view): Zacks estimated Nvidia total revenue at $406.05 billion for FY2027, up 88% year over year.
    - Stored passage: "For the current and next fiscal years, $406.05 billion and $671.95 billion estimates indicate +88% and +65.5% changes, respectively."
  - `e46` (article 45; stored attribution: NVIDIA CFO Colette Kress; stored kind: party_statement): NVIDIA CFO Colette Kress said customer forecasts point to NVIDIA's sales growth doubling in FY2028, while NVIDIA expects approximately 70% growth because it is supply-constrained.
    - Stored passage: "Customer forecasts point to our growth doubling next year. However, as I mentioned earlier, we expect to grow approximately 70% as we are supply-constrained."
  - `e48` (article 45; stored attribution: S&P Global; stored kind: third_party_view): S&P Global forecast that tech companies will spend an estimated $1.3 trillion on AI in calendar 2027.
    - Stored passage: "S&P Global recently forecast that tech companies will spend an estimated $1.3 trillion on AI next year."
  - `e49` (article 45; stored attribution: fool.com (analyst); stored kind: third_party_view): The author reported that demand for Micron memory chips far outpaces supply, driving sharply higher memory prices and supply constraints.
    - Stored passage: "Micron Technology 's memory chips are having a significant problem, with demand far outpacing supply. That's led to skyrocketing memory prices, higher margins for Micron, and global supply constraints."
  - `e51` (article 45; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA said it is working to increase supply to meet customer demand.
    - Stored passage: "Nvidia says it's working to increase supply to meet customer demand."
  - `e57` (article 46; stored attribution: 24/7 Wall St. author; stored kind: third_party_view): The 24/7 Wall St. author forecast hyperscaler capital spending of nearly $800 billion in calendar 2026 and $1.3 trillion in calendar 2027.
    - Stored passage: "Hyperscaler capex is expected to reach nearly 800 billion in 2026 and 1.3 trillion in 2027, a wave that also pulls in the power, cooling, and networking suppliers we profiled in a free report on seven AI infrastructure names that aren't chipmakers."
  - `e90` (article 69; stored attribution: Keithen Drury; stored kind: third_party_view): The author said Broadcom and its AI hyperscaler clients are designing workload-specific AI computing units that perform AI computing at lower cost and more effectively than Nvidia's GPUs, threatening Nvidia's market share.
    - Stored passage: "There are also workload-specific AI computing units being designed by Broadcom ( AVGO +2.83% ) and its AI hyperscaler clients that perform AI computing at lower cost and more effectively than Nvidia's or AMD's GPUs, threatening Nvidia's market share."
  - `e94` (article 69; stored attribution: Nvidia; stored kind: party_statement): Nvidia projected that global annual data-center capital expenditures would reach $3 trillion to $4 trillion by 2030.
    - Stored passage: "Ultimately, Nvidia sees global annual data center capital expenditures increasing to $3 trillion to $4 trillion by 2030."
  - `e127` (article 91; stored attribution: Ramez Naam; stored kind: third_party_view): Ramez Naam said on August 4, 2026, that NVIDIA’s CUDA moat is broken in 2026 and 2027.
    - Stored passage: "“The CUDA moat is broken this year and next.”"
  - `e128` (article 91; stored attribution: Dave Blundin; stored kind: third_party_view): Dave Blundin judged that CUDA no longer provides an inference-time moat and has only a limited remaining lifespan as a training-time moat.
    - Stored passage: "Dave’s conclusion: CUDA as an inference-time moat is already dead. As a training-time moat, limited lifespan."
  - `e129` (article 91; stored attribution: Dave Blundin; stored kind: third_party_view): Dave Blundin estimated that 90–95% of AI workload is moving to inference.
    - Stored passage: "Ninety to ninety-five percent of the AI workload is moving to inference."
  - `e130` (article 91; stored attribution: Dave Blundin; stored kind: third_party_view): Dave Blundin said he had written custom kernels for Fable 5 himself over the preceding few weeks, work he said previously required a team of specialists and could now be done with a prompt.
    - Stored passage: "Dave confirmed he’s been writing custom kernels for Fable 5 himself over the last few weeks. Work that used to require a team of specialists is now done with a prompt."
  - `e132` (article 92; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA expects FY2028 revenue growth of about 70%; the article says supply constraints could limit the pace of meeting demand.
    - Stored passage: "NVIDIA also expects fiscal 2028 revenue growth of about 70%, although supply constraints could limit how quickly it meets demand."
  - `e135` (article 92; stored attribution: AMD; stored kind: third_party_view): AMD's Helios platform is in production, with initial shipments expected late in 2026 Q3 and a larger ramp-up expected in Q4 2026 and 2027.
    - Stored passage: "Helios is in production, with initial shipments expected late in the third quarter and a larger ramp-up in the fourth quarter and 2027."
  - `e136` (article 92; stored attribution: Anthropic; stored kind: fact): Anthropic plans to deploy up to 2 GW of AMD MI450-series GPUs on Helios, with the first 1 GW planned to begin in the first half of 2027.
    - Stored passage: "Anthropic plans to deploy up to 2 gigawatts of MI450-series GPUs using the AMD Helios rack-scale platform, with the first gigawatt beginning in the first half of 2027."
  - `e137` (article 92; stored attribution: Microsoft; stored kind: fact): Microsoft plans to deploy AMD's Helios platform at scale on Azure.
    - Stored passage: "Microsoft plans to deploy Helios at scale on Azure."
  - `e138` (article 92; stored attribution: AMD; stored kind: party_statement): AMD expects its Data Center segment revenue to more than double year over year in 2027.
    - Stored passage: "Advanced Micro Devices expects Data Center segment revenues to more than double year over year in 2027."
  - `e161` (article 103; stored attribution: AWS and NVIDIA; stored kind: fact): AWS and NVIDIA announced a plan to deploy 2 million additional NVIDIA GPUs across AWS infrastructure between 2027 and 2028.
    - Stored passage: "Now, the two powerhouses have announced a staggering expansion of this existing partnership which will, among other things — but this is certainly the standout headline — include the deployment of 2 million additional NVIDIA GPUs across AWS infrastructure between 2027 and 2028."
  - `e162` (article 103; stored attribution: Amazon Robotics and NVIDIA; stored kind: fact): Amazon Robotics plans to integrate NVIDIA’s full-stack physical AI platform into its robotics projects.
    - Stored passage: "On the physical AI side, Amazon Robotics will work with NVIDIA to integrate its full-stack physical AI platform, helping ramp up the development of Amazon’s robotics projects."
  - `e163` (article 103; stored attribution: AWS and NVIDIA; stored kind: fact): AWS and NVIDIA plan to build AI factories for the U.S. government, enabling delivery of 100,000 GPUs on AWS secure infrastructure for federal and national-security workloads.
    - Stored passage: "AWS and NVIDIA will build AI factories for the U.S. government, enabling the delivery of “100,000 GPUs on AWS’s secure infrastructure for federal and national-security workloads.”"
  - `e181` (article 115; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management expects supply to remain a bottleneck at least through the end of fiscal 2028.
    - Stored passage: "Management expects supply to remain a bottleneck at least through the end of fiscal 2028."
  - `e186` (article 115; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management expects AI labs backed by NVIDIA’s balance sheet to account for roughly one-quarter of NVIDIA’s business in fiscal 2028.
    - Stored passage: "Management expects AI labs backed by NVIDIA’s balance sheet to make up roughly a quarter of NVIDIA’s business in fiscal 2028."
  - `e187` (article 115; stored attribution: trefis.com; stored kind: third_party_view): The author calculated NVIDIA revenue growth of 83% over the past year, compared with 16.7% for Texas Instruments.
    - Stored passage: "NVIDIA’s revenue grew 83% over the past year, against 16.7% for TI."
  - `e196` (article 121; stored attribution: Colette Kress, NVIDIA CFO; stored kind: party_statement): NVIDIA CFO Colette Kress said the company expects fiscal 2028 revenue to grow roughly 70%.
    - Stored passage: "And on the company's late-August earnings call, CFO Colette Kress said Nvidia expects revenue to rise roughly 70% in fiscal 2028, the year ending in January 2028."
  - `e197` (article 121; stored attribution: Colette Kress, NVIDIA CFO; stored kind: party_statement): NVIDIA CFO Colette Kress characterized the fiscal 2028 revenue outlook as supply-constrained, with manufacturing capacity limiting revenue rather than customer demand.
    - Stored passage: "She called it "a supply-constrained outlook." Put another way, the limit is manufacturing capacity, not customer demand."
  - `e199` (article 121; stored attribution: fool.com (analyst); stored kind: third_party_view): The author calculated that applying roughly 70% growth to the $412 billion fiscal 2027 consensus estimate implies around $700 billion of NVIDIA fiscal 2028 revenue.
    - Stored passage: "Grow that by roughly 70%, and fiscal 2028 lands somewhere around $700 billion."
  - `e246` (article 143; stored attribution: Broadcom; stored kind: party_statement): Broadcom expects AI semiconductor revenue of $115 billion in FY2027 and $230 billion in FY2028.
    - Stored passage: "For fiscal year 2027, Broadcom expects to generate $115 billion in AI semiconductor revenue. In FY 2028, that figure doubles to $230 billion."
  - `e271` (article 158; stored attribution: Keithen Drury; stored kind: third_party_view): Keithen Drury estimates Broadcom AI semiconductor revenue will exceed $115 billion in 2027, more than doubling and growing faster than NVIDIA.
    - Stored passage: "Broadcom is expected to grow quicker than Nvidia, as its AI semiconductor revenue is more than doubling to $115 billion next year."
  - `e272` (article 158; stored attribution: Micron; stored kind: party_statement): Micron does not expect tightness in the memory-chip market to ease before 2028.
    - Stored passage: "Micron also doesn't expect the "tightness" in the memory chip space to alleviate until 2028,"
  - `e277` (article 162; stored attribution: fool.com (Keithen Drury); stored kind: third_party_view): The author forecasts that Nvidia will generate more quarterly revenue than Apple by 2027.
    - Stored passage: "so it's very likely that Nvidia will generate more revenue per quarter than Apple by 2027."
  - `e286` (article 165; stored attribution: Elon Musk; stored kind: party_statement): Elon Musk said earlier in September 2026 that SpaceX planned to use Nvidia chips exclusively going forward.
    - Stored passage: "This update follows comments from Elon Musk earlier this month that SpaceX would exclusively use Nvidia chips moving forward."
  - `e287` (article 165; stored attribution: Elon Musk; stored kind: party_statement): Musk said SpaceX expected to reach around 2 GW of computing power by the end of 2026 and was targeting closer to 10 GW than 5 GW by the end of 2027.
    - Stored passage: "At the time, Musk said SpaceX would end the year with around 2 gigawatts of computing power, while it is looking to end 2027 with closer to 10 gigawatts than 5 gigawatts."
  - `e288` (article 165; stored attribution: The Motley Fool author; stored kind: third_party_view): The author estimated that 1 GW of computing power costs about $50 billion to $60 billion, including about $35 billion of Nvidia chips and other components.
    - Stored passage: "One gigawatt of compute power costs about $50 billion to $60 billion, with chips and other Nvidia components making up about $35 billion of that total cost."
  - `e345` (article 197; stored attribution: Jensen Huang; stored kind: party_statement): NVIDIA CEO Jensen Huang said the company would double the number of chips it sells in calendar 2027.
    - Stored passage: "Huang earlier this month said Nvidia would double the number of chips it sells in 2027."

<a id="old-v4"></a>

### Old system 4 (`v4`): How much data-center segment revenue will Nvidia report for FY2027?

- Latest answer (2026-09-28): 2 Bullish: FY2027 data-center segment revenue is at least $400 billion but below $450 billion.
- Stored request: call 715; request sha256 `8afbd2ea7a9a139e87f64f41b397f85e3b4ccff25dffaa7060bbf2ad9a482d08`.
- Cites 9 of the 94 statements linked to the question:

  - `e23` (article 35; stored attribution: NVIDIA; stored kind: fact): NVIDIA reported Data Center revenue of $89 billion in fiscal Q2 2027, up 117% year over year and 18% sequentially.
    - Stored passage: "The Data Center segment remains NVIDIA's primary growth engine, with revenues jumping 117% year over year and 18% sequentially to $89 billion in the fiscal second quarter of 2027, according to the Aug. 26 press release."
  - `e151` (article 96; stored attribution: NVIDIA; stored kind: fact): NVIDIA reported that Data Center segment revenue grew 92% year over year in fiscal 2027 Q1.
    - Stored passage: "Data Center revenues jumped 92%."
  - `e381` (article 232; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management expects the Vera Rubin platform to account for about 20% of Data Center revenue in fiscal Q3 2027.
    - Stored passage: "Management expects it to make up about 20% of data center revenue in fiscal Q3 2027."
  - `e322` (article 177; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management expected sales to its largest cloud-company customers to accelerate again in fiscal Q4 2027 as Vera Rubin supply grew.
    - Stored passage: "Management expects sales to the largest cloud companies to speed up again in fiscal Q4 2027, as Vera Rubin supply grows."
  - `e108` (article 77; stored attribution: Super Micro Computer; stored kind: fact): Super Micro moved into commercial shipments of systems built around NVIDIA's Vera Rubin platform.
    - Stored passage: "Super Micro Computer ( NASDAQ:SMCI ) shares declined more than 3% Thursday afternoon as the server maker moved into commercial shipments of systems built around NVIDIA's next-generation Vera Rubin platform, adding another data-center product to its AI infrastructure lineup."
  - `e349` (article 203; stored attribution: Anthropic; stored kind: fact): Anthropic contracted for 2.5 GW of Nvidia AI infrastructure scheduled for delivery through 2028.
    - Stored passage: "The Dario Amodei-led company has also contracted for 2.5 gigawatts of Nvidia AI infrastructure scheduled for delivery through 2028."
  - `e350` (article 203; stored attribution: Nvidia; stored kind: party_statement): Nvidia said its reference-design revenue opportunity per gigawatt increased from roughly $18 billion with Hopper to $25 billion with Blackwell and $40 billion with Rubin.
    - Stored passage: "Nvidia said its revenue opportunity per gigawatt, based on its reference designs, has risen from roughly $18 billion during the Hopper generation to $25 billion with Blackwell and $40 billion with Rubin ."
  - `e382` (article 232; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management expects supply to remain a bottleneck at least through the end of fiscal 2028.
    - Stored passage: "Management expects supply to remain a bottleneck at least through the end of fiscal 2028."
  - `e71` (article 54; stored attribution: Jensen Huang; stored kind: party_statement): NVIDIA CEO Jensen Huang said demand was well above supply.
    - Stored passage: "whose chief executive just told you demand runs well above supply."

<a id="old-v5"></a>

### Old system 5 (`v5`): How much will Nvidia's total revenue grow in FY2028?

- Latest answer (2026-09-28): 2 Bullish: FY2028 total revenue growth is at least 70% and below 80%.
- Stored request: call 714; request sha256 `ab38822dfb292453a1240b8379a1c9f7f8d932c72865f5ba3dc9f33fdc401a6f`.
- Cites 12 of the 43 statements linked to the question:

  - `e44` (article 43; stored attribution: Nvidia; stored kind: party_statement): Nvidia guided to about 70% revenue growth for FY2028.
    - Stored passage: "issued bullish guidance for about 70% revenue growth in fiscal 2028"
  - `e46` (article 45; stored attribution: NVIDIA CFO Colette Kress; stored kind: party_statement): NVIDIA CFO Colette Kress said customer forecasts point to NVIDIA's sales growth doubling in FY2028, while NVIDIA expects approximately 70% growth because it is supply-constrained.
    - Stored passage: "Customer forecasts point to our growth doubling next year. However, as I mentioned earlier, we expect to grow approximately 70% as we are supply-constrained."
  - `e64` (article 53; stored attribution: Jensen Huang, Nvidia CEO; stored kind: party_statement): Nvidia CEO Jensen Huang said customer demand without the supply constraint would be a lot higher.
    - Stored passage: "would be a lot higher."
  - `e154` (article 98; stored attribution: NVIDIA CFO; stored kind: party_statement): NVIDIA’s CFO expected supply to remain a bottleneck through at least the end of FY2028 and described memory pricing as extreme.
    - Stored passage: "The CFO expects supply to stay a bottleneck at least through the end of fiscal 2028 and calls memory pricing extreme."
  - `e161` (article 103; stored attribution: AWS and NVIDIA; stored kind: fact): AWS and NVIDIA announced a plan to deploy 2 million additional NVIDIA GPUs across AWS infrastructure between 2027 and 2028.
    - Stored passage: "Now, the two powerhouses have announced a staggering expansion of this existing partnership which will, among other things — but this is certainly the standout headline — include the deployment of 2 million additional NVIDIA GPUs across AWS infrastructure between 2027 and 2028."
  - `e163` (article 103; stored attribution: AWS and NVIDIA; stored kind: fact): AWS and NVIDIA plan to build AI factories for the U.S. government, enabling delivery of 100,000 GPUs on AWS secure infrastructure for federal and national-security workloads.
    - Stored passage: "AWS and NVIDIA will build AI factories for the U.S. government, enabling the delivery of “100,000 GPUs on AWS’s secure infrastructure for federal and national-security workloads.”"
  - `e199` (article 121; stored attribution: fool.com (analyst); stored kind: third_party_view): The author calculated that applying roughly 70% growth to the $412 billion fiscal 2027 consensus estimate implies around $700 billion of NVIDIA fiscal 2028 revenue.
    - Stored passage: "Grow that by roughly 70%, and fiscal 2028 lands somewhere around $700 billion."
  - `e368` (article 218; stored attribution: Zacks; stored kind: third_party_view): Zacks expects Nvidia sales to grow 88% in FY2027 and 65.5% in FY2028.
    - Stored passage: "Sales are expected to climb 88% this year and another 65.5% next year"
  - `e90` (article 69; stored attribution: Keithen Drury; stored kind: third_party_view): The author said Broadcom and its AI hyperscaler clients are designing workload-specific AI computing units that perform AI computing at lower cost and more effectively than Nvidia's GPUs, threatening Nvidia's market share.
    - Stored passage: "There are also workload-specific AI computing units being designed by Broadcom ( AVGO +2.83% ) and its AI hyperscaler clients that perform AI computing at lower cost and more effectively than Nvidia's or AMD's GPUs, threatening Nvidia's market share."
  - `e269` (article 158; stored attribution: Keithen Drury; stored kind: third_party_view): Keithen Drury estimates NVIDIA’s 2027 revenue growth will exceed management’s 70% expectation.
    - Stored passage: "so the real growth rate is likely higher than this."
  - `e351` (article 203; stored attribution: Nvidia; stored kind: party_statement): Nvidia reported its share of information-technology capital spending among the five largest cloud service providers rose from 11% in 2023 Q1 and projected it to reach 44% by 2027.
    - Stored passage: "Its share of information-technology capital spending among the five largest cloud service providers has climbed from 11% in the first quarter of 2023 and is projected by Nvidia to reach 44% by 2027 ."
  - `e59` (article 50; stored attribution: Wall Street analysts; stored kind: third_party_view): The author says Wall Street expects Nvidia revenue growth of 91% in FY2027 and 66% in FY2028.
    - Stored passage: "Wall Street expects the company to grow revenue by 91% this year and 66% next year."

<a id="old-v6"></a>

### Old system 6 (`v6`): Will the U.S. administration authorize Nvidia Blackwell chip exports to China by January 31, 2027?

- Latest answer (2026-09-28): 1 No: The U.S. administration has not authorized Nvidia Blackwell chip exports to China by January 31, 2027.
- Stored request: call 707; request sha256 `d3e0cd1675445af119a373f8a1b0fad0ac82b34e062604adbd5c33c302bb436b`.
- Cites 17 of the 31 statements linked to the question:

  - `e223` (article 132; stored attribution: U.S. export-control authorities; stored kind: fact): The article reports that U.S. export controls ban exports to China of Nvidia's and AMD's most advanced AI chips; it gives no start date or specific chip models.
    - Stored passage: "Nvidia and AMD's most advanced artificial intelligence chips are banned from being exported to China, although the country remains a key market and manufacturing hub for Cook's Apple and Musk's Tesla."
  - `e263` (article 157; stored attribution: The U.S. government; stored kind: fact): The U.S. currently prohibits exports of Nvidia’s most powerful chips to China.
    - Stored passage: "Nvidia’s most powerful chips are currently prohibited from export to China due to Washington’s restrictions."
  - `e19` (article 33; stored attribution: The Trump administration; stored kind: fact): The Trump administration allowed Nvidia to ship H200 AI chips to approved customers in China; no date is given.
    - Stored passage: "The Trump administration has allowed Nvidia to ship its H200 AI chips to approved customers in China."
  - `e264` (article 157; stored attribution: Donald Trump; stored kind: fact): Last year, President Trump allowed Nvidia to sell previous-generation H200 chips to approved Chinese buyers subject to a 25% tariff.
    - Stored passage: "At the same time, last year Trump allowed Nvidia to sell previous-generation H200 chips to approved Chinese buyers with a 25% tariff."
  - `e300` (article 169; stored attribution: The U.S. administration; stored kind: fact): The U.S. administration recently lifted restrictions on some older-generation Nvidia chips, which have been sold in small quantities.
    - Stored passage: "The US administration recently lifted restrictions on some Nvidia chips, though the products tend to be older-generation chips that have been sold in small quantities."
  - `e280` (article 163; stored attribution: U.S. Trade Representative Jamieson Greer; stored kind: party_statement): U.S. Trade Representative Jamieson Greer said national security export controls were taken off the table; the item gives no date for his statement.
    - Stored passage: "US Trade Representative Jamieson Greer said national security export controls were taken "off the table," the Korea Times reported."
  - `e297` (article 168; stored attribution: Jamieson Greer; stored kind: party_statement): USTR Jamieson Greer told CNBC that export controls deemed national security issues were taken off the table during trade talks; the item gives no specific export-control decision.
    - Stored passage: "USTR Jamieson Greer told CNBC that export controls deemed national security issues were "taken off the table" during trade talks"
  - `e337` (article 184; stored attribution: Jamieson Greer; stored kind: party_statement): USTR Jamieson Greer told CNBC that export controls considered national-security issues were taken off the table during the U.S.–China trade talks.
    - Stored passage: "USTR Jamieson Greer told CNBC that export controls deemed national security issues were "taken off the table" during trade talks,"
  - `e295` (article 168; stored attribution: The Information; stored kind: rumour): The Information reported that China may allow Alibaba and ByteDance to buy NVIDIA RTX Pro 5500 chips; no quantity or approval date was given.
    - Stored passage: "The Chinese government has indicated it may allow companies like Alibaba Group Holding Limited and ByteDance Limited to buy Nvidia's new RTX Pro 5500 chips, according to a report by The Information."
  - `e299` (article 169; stored attribution: China's Ministry of Industry and Information Technology, as reported by The Information citing people familiar with the matter; stored kind: rumour): China's Ministry of Industry and Information Technology asked some companies for RTX Pro 5500 purchase plans and told some it intends to approve the purchases, according to The Information.
    - Stored passage: "The Ministry of Industry and Information Technology recently asked some companies to report on their plans to purchase the high-end graphics processor chip, which was released this month, including how many of them and what they would use the product for, the report said, adding that the ministry told some of the firms it intends to approve the purchases."
  - `e306` (article 176; stored attribution: U.S. Justice Department; stored kind: fact): The U.S. Justice Department recently uncovered a smuggling network that authorities say transferred or attempted to transfer at least $160 million worth of Nvidia H100 and H200 chips to China from October 2024 through May 2025.
    - Stored passage: "At the same time, the U.S. Justice Department recently uncovered a smuggling network that authorities say was involved in transferring or attempting to transfer at least $160 million worth of Nvidia H100 and H200 chips to China between October 2024 and May 2025."
  - `e307` (article 176; stored attribution: ynetnews.com; stored kind: third_party_view): The standard RTX 5090 is not officially sold in China; a more limited version is marketed there to comply with U.S. export restrictions.
    - Stored passage: "In China, it is in demand for another reason. The standard RTX 5090 is not officially sold there. Instead, a more limited version is marketed to comply with U.S. export restrictions."
  - `e332` (article 184; stored attribution: finance.biggo.com for the H200 sales figure; Jensen Huang for the market-share statement; stored kind: third_party_view): Nvidia’s China H200 sales are reported to remain below 1% of data-center revenue; CEO Jensen Huang said Nvidia’s share of China’s advanced AI chip market fell from around 95% to zero as restrictions tightened.
    - Stored passage: "Nvidia's China H200 sales remain below 1% of data-center revenue, and CEO Jensen Huang has said the company's share of China's advanced AI chip market effectively fell from around 95% to zero as restrictions tightened."
  - `e333` (article 184; stored attribution: Jeffrey Kessler; stored kind: party_statement): In July 2026, Commerce under secretary Jeffrey Kessler told the House Foreign Affairs Committee that roughly $10 billion in approved China H200 licences had yielded only a “very small quantity of chips.”
    - Stored passage: "In July, the under secretary of commerce for industry and security, Jeffrey Kessler, told the House Foreign Affairs Committee that roughly $10 billion in approved licences had yielded "a very small quantity of chips," which he called trivial."
  - `e338` (article 184; stored attribution: Nvidia; stored kind: party_statement): An Nvidia spokesperson said Nvidia continues to face constraints from U.S. export rules covering gaming products and Chinese restrictions on American imports.
    - Stored passage: "An Nvidia spokesperson said the company continues to face "dual constraints" from outdated U.S. export rules that cover gaming products released nearly five years ago and Chinese restrictions on American imports."
  - `e383` (article 235; stored attribution: The U.S. administration; stored kind: fact): The U.S. administration allowed Nvidia to ship H200 processors to China in exchange for a 25% U.S. fee; the item gives no date for the authorization.
    - Stored passage: "The administration allowed Nvidia to ship H200 processors there in exchange for a 25% U.S. fee."
  - `e384` (article 235; stored attribution: Chinese regulators; stored kind: fact): Chinese regulators mostly blocked imports of Nvidia H200 processors despite U.S. approval of exports; the item gives no date for the restrictions.
    - Stored passage: "Chinese regulators mostly blocked H200 imports even after the Trump administration approved exports."

<a id="old-v7"></a>

### Old system 7 (`v7`): How much will the five largest AI hyperscalers spend on data centers in calendar 2026?

- Latest answer (2026-09-26): 3 $775 billion to below $825 billion: Combined spending is at least $775 billion and less than $825 billion; this is the neutral comparison range around the author's nearly $800 billion estimate.
- Stored request: call 482; request sha256 `ebbc6c7d4c4d5f23338661fc1f8dc74aaaddf2227097b83eae764b4bc5863fe1`.
- Cites 11 of the 11 statements linked to the question:

  - `e42` (article 42; stored attribution: Nvidia; stored kind: third_party_view): Nvidia estimates global data-center capital expenditures will reach $3 trillion to $4 trillion by 2030.
    - Stored passage: "Nvidia estimates that global data center capital expenditures will rise to between $3 trillion and $4 trillion by 2030."
  - `e43` (article 42; stored attribution: fool.com analyst; stored kind: third_party_view): The author estimates the five largest AI hyperscalers will spend nearly $800 billion on data centers in calendar 2026.
    - Stored passage: "Considering the big five AI hyperscalers will spend nearly $800 billion on data centers this year, that's huge growth still to come."
  - `e160` (article 102; stored attribution: fool.com (analyst); stored kind: third_party_view): The author estimates the five largest AI hyperscalers will spend nearly $800 billion on data centers in calendar 2026.
    - Stored passage: "Considering the big five AI hyperscalers will spend nearly $800 billion on data centers this year, that's huge growth still to come."
  - `e224` (article 133; stored attribution: Jensen Huang; stored kind: party_statement): NVIDIA CEO Jensen Huang said AI supercomputers, despite being energy efficient, will still use a lot of power.
    - Stored passage: "The A.I. supercomputers are super energy efficient, but they’re still going to use a lot of power."
  - `e225` (article 133; stored attribution: Jensen Huang; stored kind: party_statement): Jensen Huang said fossil fuels are required for energy production in the near term.
    - Stored passage: "Well, in the near term, energy production requires fossil fuel."
  - `e226` (article 133; stored attribution: Jensen Huang; stored kind: party_statement): Jensen Huang said the United States has produced very little net new energy for a long time.
    - Stored passage: "if you look at our country, we’ve produced very little net new energy for a long time."
  - `e227` (article 134; stored attribution: finance.biggo.com; stored kind: third_party_view): The five largest AI hyperscalers are expected to spend nearly $800 billion on data centers in calendar 2026.
    - Stored passage: "The five largest AI hyperscalers are expected to spend nearly $800 billion on data centers this year alone."
  - `e237` (article 140; stored attribution: fool.com (analyst); stored kind: third_party_view): The author estimated that the five largest AI hyperscalers are spending around $800 billion on data centers currently.
    - Stored passage: "Right now, the big five AI hyperscalers are spending around $800 billion."
  - `e245` (article 141; stored attribution: fool.com (analyst); stored kind: third_party_view): The author argues that Nvidia's sales and investment gains both depend on AI spending, so a slowdown could reduce its orders and markdown the value of its investment stakes at the same time.
    - Stored passage: "So Nvidia's investment gains and its sales now depend on the same thing: AI spending. If that spending cooled, Nvidia could face smaller orders and markdowns on its stakes at the same time."
  - `e270` (article 158; stored attribution: NVIDIA; stored kind: third_party_view): NVIDIA expects the five largest AI hyperscalers’ data-center spending to be nearly $800 billion in calendar 2026 and $1.3 trillion in calendar 2027.
    - Stored passage: "Nvidia expects the big five AI hyper-scalers to spend nearly $800 billion in 2026, with that figure rising to $1.3 trillion next year."
  - `e275` (article 160; stored attribution: Reuters; stored kind: third_party_view): Reuters reported that AI-related borrowers were paying wider bond spreads as investors questioned the sector’s need for additional capital.
    - Stored passage: "Reuters reported this week that AI-related borrowers are increasingly paying wider spreads as investors question how much additional capital the sector will require."

<a id="old-v8"></a>

### Old system 8 (`v8`): How much will tech companies spend on AI in calendar 2027?

- Latest answer (2026-09-28): 3 Middle range: AI spending is at least $1.2 trillion and below $1.4 trillion.
- Stored request: call 706; request sha256 `e3ff428b198146c0daaa87820726dcfef12c2e75db2fc8833bcd8998d6f5d577`.
- Cites 6 of the 6 statements linked to the question:

  - `e48` (article 45; stored attribution: S&P Global; stored kind: third_party_view): S&P Global forecast that tech companies will spend an estimated $1.3 trillion on AI in calendar 2027.
    - Stored passage: "S&P Global recently forecast that tech companies will spend an estimated $1.3 trillion on AI next year."
  - `e92` (article 69; stored attribution: Nvidia; stored kind: party_statement): Nvidia estimated that the big five AI hyperscalers' data-center capital expenditures would approach $800 billion in 2026.
    - Stored passage: "During its most recent earnings call, Nvidia noted that this year's data center capital expenditures from the big five AI hyperscalers will approach $800 billion."
  - `e93` (article 69; stored attribution: Nvidia; stored kind: party_statement): Nvidia estimated that the big five AI hyperscalers' data-center capital expenditures would rise to $1.3 trillion in 2027.
    - Stored passage: "Next year, that figure is estimated to rise to $1.3 trillion."
  - `e222` (article 130; stored attribution: The estimates cited by The Motley Fool author; stored kind: third_party_view): The latest estimates put global AI infrastructure spending at $1.3 trillion in calendar 2027, up from about $750 billion in 2026.
    - Stored passage: "The latest estimates are for global AI infrastructure spending to reach $1.3 trillion in 2027 -- up from about $750 billion this year."
  - `e270` (article 158; stored attribution: NVIDIA; stored kind: third_party_view): NVIDIA expects the five largest AI hyperscalers’ data-center spending to be nearly $800 billion in calendar 2026 and $1.3 trillion in calendar 2027.
    - Stored passage: "Nvidia expects the big five AI hyper-scalers to spend nearly $800 billion in 2026, with that figure rising to $1.3 trillion next year."
  - `e344` (article 197; stored attribution: S&P Global Ratings; stored kind: third_party_view): S&P Global Ratings projected that combined hyperscaler capital expenditure would exceed $1.3 trillion by 2027.
    - Stored passage: "Combined hyperscaler capital expenditure is projected to exceed $1.3 trillion by 2027, S&P Global Ratings said in August, as companies race to build AI infrastructure including data centers."

<a id="old-v9"></a>

### Old system 9 (`v9`): Will NVIDIA's Vera Rubin platform begin shipping by January 31, 2027?

- Latest answer (2026-09-28): 1 Yes: NVIDIA begins shipping the Vera Rubin platform on or before January 31, 2027.
- Stored request: call 711; request sha256 `d999ee3c475a34b0ef6081bb3a14068cb101f77b9fe3d9b3e982e989c94d3c99`.
- Cites 5 of the 13 statements linked to the question:

  - `e311` (article 177; stored attribution: NVIDIA; stored kind: fact): NVIDIA began production shipments of its Vera Rubin data-center system in August 2026.
    - Stored passage: "The company began production shipments of Vera Rubin, its newest data center system, in August 2026."
  - `e190` (article 120; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA reports Vera Rubin is in full production, with production shipments beginning in August and purchase orders from every major hyperscaler, AI cloud provider, and system OEM.
    - Stored passage: "The platform is already in full production, with NVIDIA reporting production shipments beginning in August and purchase orders from every major hyperscaler, AI cloud and system original equipment manufacturer (OEM)."
  - `e312` (article 177; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management expected Vera Rubin to contribute about 20% of data-center revenue in fiscal Q3 2027.
    - Stored passage: "Management expects Vera Rubin to bring in about 20% of data center revenue in fiscal Q3 2027."
  - `e381` (article 232; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management expects the Vera Rubin platform to account for about 20% of Data Center revenue in fiscal Q3 2027.
    - Stored passage: "Management expects it to make up about 20% of data center revenue in fiscal Q3 2027."
  - `e382` (article 232; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management expects supply to remain a bottleneck at least through the end of fiscal 2028.
    - Stored passage: "Management expects supply to remain a bottleneck at least through the end of fiscal 2028."

<a id="old-v10"></a>

### Old system 10 (`v10`): What gross margin will NVIDIA report for FY2028?

- Latest answer (2026-09-28): 3 Neutral: FY2028 gross margin is at least 71% but below 73%.
- Stored request: call 712; request sha256 `8500d078b4ed7b0c5b72e6d1573f2e1b867e9262443a517cb9e5cf3a31fc1a0c`.
- Cites 18 of the 18 statements linked to the question:

  - `e154` (article 98; stored attribution: NVIDIA CFO; stored kind: party_statement): NVIDIA’s CFO expected supply to remain a bottleneck through at least the end of FY2028 and described memory pricing as extreme.
    - Stored passage: "The CFO expects supply to stay a bottleneck at least through the end of fiscal 2028 and calls memory pricing extreme."
  - `e157` (article 98; stored attribution: Trefis, the article’s author; stored kind: third_party_view): Trefis reported that consensus estimates had NVIDIA earnings and revenue growing at a similar pace from FY2027 to FY2028, implying roughly steady profit margins.
    - Stored passage: "Consensus has earnings and revenue growing at a similar pace between fiscal 2027 and fiscal 2028, so analysts assume profit margins hold roughly steady."
  - `e158` (article 98; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA guided FY2028 gross margin to 72%–73%, lower than previously expected as memory prices rose more than management expected; the guidance included the benefit of price increases NVIDIA had already implemented.
    - Stored passage: "Gross margin is guided lower. Memory prices have risen more than management expected, and the guide has that margin settling in the 72% to 73% range in fiscal 2028, helped by price increases NVIDIA has already executed."
  - `e182` (article 115; stored attribution: trefis.com; stored kind: third_party_view): Memory prices rose more than NVIDIA expected, prompting NVIDIA to reset its margin expectations; the article does not specify the price increase or revised margin expectation in this statement.
    - Stored passage: "Memory prices rose more than NVIDIA expected, and NVIDIA reset its margin expectations."
  - `e183` (article 115; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA guided gross margin to 74% for fiscal Q3 2027, down from 75% in fiscal Q2 2027.
    - Stored passage: "NVIDIA guided it to 74% for fiscal Q3, down from 75% in Q2."
  - `e184` (article 115; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA expects gross margin to be 71% to 72% in fiscal Q4 2027.
    - Stored passage: "NVIDIA expects gross margin to bottom at 71% to 72% in fiscal Q4."
  - `e200` (article 121; stored attribution: Colette Kress, NVIDIA CFO; stored kind: party_statement): NVIDIA CFO Colette Kress said gross margin should be 72% to 73% in fiscal 2028, after bottoming at 71% to 72% in fiscal Q4 2027 as price increases take effect.
    - Stored passage: "On the call, Kress said gross margins should bottom between 71% and 72% in the fiscal fourth quarter and then settle at 72% to 73% in fiscal 2028 as price hikes kick in."
  - `e217` (article 128; stored attribution: Anthony Di Pizio; stored kind: third_party_view): The author said semiconductor companies are reporting inflated profit margins because supply shortages let them dictate prices.
    - Stored passage: "Most semiconductor companies are currently reporting inflated profit margins because global supply shortages have enabled them to dictate prices."
  - `e218` (article 128; stored attribution: Anthony Di Pizio; stored kind: third_party_view): The author forecast that additional manufacturing capacity would end semiconductor companies' elevated margins and pressure industry earnings over the next couple of years.
    - Stored passage: "This won't last as additional manufacturing capacity comes online, so earnings will be under pressure across the industry over the next couple of years."
  - `e259` (article 151; stored attribution: NVIDIA; stored kind: fact): NVIDIA reported that gross margin expanded 2.5 percentage points in FY2027's second quarter.
    - Stored passage: "gross margin expanded 2.5 percentage points"
  - `e308` (article 177; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management said in August 2026 that rising memory costs would cut gross margin.
    - Stored passage: "In August 2026, management said rising memory costs will cut NVIDIA’s gross margin, the share of sales kept after production costs."
  - `e309` (article 177; stored attribution: trefis.com; stored kind: third_party_view): Trefis estimated that, on $303 billion of sales over the prior year, each percentage point of NVIDIA gross margin was worth about $3 billion.
    - Stored passage: "At $303 billion of sales over the past year, each margin point is worth about $3 billion."
  - `e313` (article 177; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management expected gross margin to bottom at 71% to 72% in fiscal Q4 2027.
    - Stored passage: "Management expects gross margin to hit its low in fiscal Q4 2027, at 71% to 72%."
  - `e314` (article 177; stored attribution: NVIDIA; stored kind: fact): NVIDIA gross margin was 75% in fiscal Q2 2027.
    - Stored passage: "It was 75% in fiscal Q2 2027."
  - `e315` (article 177; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management said memory prices had risen more than it expected.
    - Stored passage: "Management said memory prices rose more than it had expected."
  - `e316` (article 177; stored attribution: NVIDIA; stored kind: fact): NVIDIA set price increases to take effect in fiscal Q1 2028.
    - Stored passage: "NVIDIA has already set price increases that take effect in fiscal Q1 2028."
  - `e317` (article 177; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management expected the price increases to lift gross margin to 72% to 73% in fiscal 2028.
    - Stored passage: "Management expects those higher prices to lift margin to 72% to 73% in fiscal 2028."
  - `e318` (article 177; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management's fiscal Q3 2027 gross-margin guidance had a 73.5% low end.
    - Stored passage: "On November 17, watch fiscal Q3 2027 gross margin against 73.5%, the low end of management’s gross margin guide for that quarter."

<a id="old-v11"></a>

### Old system 11 (`v11`): Will NVIDIA begin shipping Rubin GPUs by December 31, 2027?

- Latest answer (2026-09-28): 1 Yes: NVIDIA has begun shipping Rubin GPUs by December 31, 2027.
- Stored request: call 710; request sha256 `fe1f77d0a526b1bd29eb0429e6fdeac911d13bf020779e5ff568b1e68203877b`.
- Cites 6 of the 6 statements linked to the question:

  - `e311` (article 177; stored attribution: NVIDIA; stored kind: fact): NVIDIA began production shipments of its Vera Rubin data-center system in August 2026.
    - Stored passage: "The company began production shipments of Vera Rubin, its newest data center system, in August 2026."
  - `e273` (article 160; stored attribution: Nvidia; stored kind: fact): Nvidia’s official MLPerf announcement described Vera Rubin’s benchmark entry as a preview submission ahead of broader deployment.
    - Stored passage: "Nvidia detailed the results in its official MLPerf announcement , describing Vera Rubin’s entry as a preview submission ahead of broader deployment."
  - `e289` (article 165; stored attribution: Nvidia and SpaceX; Elon Musk for the system design and deployment plan; stored kind: fact): Nvidia and SpaceX announced a partnership to develop GPUs for SpaceX's planned orbital data centers; Musk said they had designed a space-optimized Vera Rubin NVL72 system, which SpaceX planned to launch into orbit toward the end of 2027 and begin scaling in 2028.
    - Stored passage: "In addition to helping expand xAI's computing capacity, Nvidia and SpaceX also announced a partnership to develop GPUs for the company's planned future orbital data centers. Cosmic radiation can affect current chips, flipping bits from a 0 to a 1 or vice versa, causing significant computational errors. Worst of all, there is currently no way to flip it back, and it's difficult to detect without a redundant system to check it against. In a post on X, Musk said the two companies have designed a Vera Rubin NVL72 system optimized for use in space. It plans to launch the system into orbit toward the end of 2027 and then start scaling it in 2028."
  - `e382` (article 232; stored attribution: NVIDIA management; stored kind: party_statement): NVIDIA management expects supply to remain a bottleneck at least through the end of fiscal 2028.
    - Stored passage: "Management expects supply to remain a bottleneck at least through the end of fiscal 2028."
  - `e205` (article 122; stored attribution: zacks.com; stored kind: third_party_view): The author says NVIDIA’s Vera Rubin platform is entering full production.
    - Stored passage: "with the Vera Rubin platform entering full production, NVIDIA is well-poised to benefit from the next phase of demand for AI infrastructure."
  - `e235` (article 139; stored attribution: NVIDIA; stored kind: third_party_view): Zacks reported that NVIDIA's Vera Rubin platform was in full production as of the article's publication.
    - Stored passage: "Profitability is also expected to remain strong, while the company's Vera Rubin platform is now in full production, positioning NVIDIA to capitalize on continued AI infrastructure demand."

<a id="old-v12"></a>

### Old system 12 (`v12`): At NVIDIA’s FY2027 annual report, what amount of purchase commitments for the Hugging Face acquisition will NVIDIA report in its commitments note?

- Latest answer (2026-09-28): 3 Neutral: The reported amount is at least $10 billion and less than $15 billion.
- Stored request: call 709; request sha256 `84b0162cb5a0532dbbd9c861514822e20e4861b933430fca4956f232b22451dd`.
- Cites 3 of the 3 statements linked to the question:

  - `e188` (article 116; stored attribution: Nvidia; stored kind: fact): Nvidia agreed to acquire Hugging Face for approximately $12.9 billion to expand its software capabilities; the item gives no signing date.
    - Stored passage: "The company also recently agreed to acquire Hugging Face for approximately $12.9 billion to expand its software capabilities."
  - `e262` (article 156; stored attribution: NVIDIA; stored kind: fact): NVIDIA agreed to acquire Hugging Face for $12.9 billion; the item gives no agreement date.
    - Stored passage: "Nvidia has since agreed to buy Hugging Face for $12.9 billion."
  - `e359` (article 208; stored attribution: Nvidia; stored kind: fact): Nvidia announced on September 3, 2026, that it would purchase Hugging Face for roughly $13 billion; CEO Jensen Huang said the combination would scale Hugging Face's platform and infrastructure.
    - Stored passage: "Nvidia swept in to purchase Hugging Face, announcing the deal on Sept. 3, with CEO Jensen Huang writing in a blog post that, "Together, we will scale Hugging Face's platform, strengthen its infrastructure and expand access to AI for developers and institutions worldwide.""

<a id="old-v13"></a>

### Old system 13 (`v13`): Will Nvidia agree to invest in Anthropic's IPO as an anchor investor by September 26, 2027?

- Latest answer (2026-09-28): 1 Yes: Nvidia publicly agrees to invest as an anchor investor in Anthropic's IPO by September 26, 2027.
- Stored request: call 708; request sha256 `8ea20b361dcb728104560a3832c26840d145b1e44e5be1cf5790528df9e754a0`.
- Cites 3 of the 3 statements linked to the question:

  - `e238` (article 141; stored attribution: Unnamed source quoted in Reuters; stored kind: rumour): Reuters reported this month that Nvidia was in talks to be an anchor investor in Anthropic's planned IPO, with an unnamed source putting Nvidia's possible investment at up to $10 billion.
    - Stored passage: "The chipmaker's in talks to be an anchor investor in Anthropic's planned initial public offering (IPO) , Reuters said this month, a deal that could deepen its ties to a major customer. A source put Nvidia's possible investment at up to $10 billion."
  - `e239` (article 141; stored attribution: Reuters; stored kind: third_party_view): Anthropic was reportedly seeking to raise up to $100 billion in its IPO at a possible valuation of roughly $2 trillion.
    - Stored passage: "The artificial intelligence (AI) company behind the Claude models is reportedly looking to raise as much as $100 billion in a listing that might value it at roughly $2 trillion."
  - `e240` (article 141; stored attribution: Reuters; stored kind: third_party_view): Reuters said Anthropic's IPO might be delayed until after the November 2026 U.S. midterm elections.
    - Stored passage: "Reuters has since said that the IPO may slip past the U.S. midterm elections in November."

<a id="old-v14"></a>

### Old system 14 (`v14`): Will China's Ministry of Industry and Information Technology permit Alibaba and ByteDance to buy Nvidia RTX PRO 5500 cards by January 31, 2027?

- Latest answer (2026-09-28): 1 Yes: MIIT permits Alibaba and ByteDance to buy RTX PRO 5500 cards by January 31, 2027.
- Stored request: call 705; request sha256 `9bbc5979edf4c57b2629f6e79a016e38ec02f011d46f13b6d99159b804e042a8`.
- Cites 8 of the 8 statements linked to the question:

  - `e278` (article 163; stored attribution: The Information's two unnamed sources; stored kind: rumour): The Information reported on September 27, 2026, citing two people familiar with the matter, that China's MIIT asked Alibaba and ByteDance how many Nvidia RTX PRO 5500 cards they wanted and why; neither Beijing nor the companies confirmed the plan.
    - Stored passage: "China's Ministry of Industry and Information Technology (MIIT), which oversees the tech sector, asked the two firms how many RTX PRO 5500 cards they want and why. That is according to The Information, citing two people familiar with the matter."
  - `e282` (article 164; stored attribution: Two people familiar with the matter, as cited by The Information; stored kind: rumour): Unnamed sources told The Information that China may allow companies including ByteDance and Alibaba to buy NVIDIA RTX PRO 5500 chips; the report was published on September 27, 2026.
    - Stored passage: "The Chinese government has signaled it could allow some domestic companies like ByteDance and Alibaba to buy Nvidia's chip built for high-end professional computers, The Information reported on Sunday, citing two people familiar with the matter."
  - `e283` (article 164; stored attribution: China's Ministry of Industry and Information Technology; stored kind: rumour): China's Ministry of Industry and Information Technology asked companies including ByteDance and Alibaba to report plans to purchase NVIDIA RTX PRO 5500 chips; the request was reported on September 27, 2026.
    - Stored passage: "China's Ministry of Industry and Information Technology recently asked companies including ByteDance and Alibaba to report their plans to purchase Nvidia's RTX PRO 5500 chips, according to the report."
  - `e284` (article 164; stored attribution: The Information, citing unnamed sources for the ministry's stated intention and unnamed industry executives for the export-controls expectation; stored kind: rumour): The Information reported that China's Ministry of Industry and Information Technology told some companies the government intends to approve purchases of NVIDIA RTX PRO 5500 chips; some industry executives expect the chip to avoid U.S. export restrictions.
    - Stored passage: "The ministry told some Chinese companies the government intends to approve the purchases, The Information report said, adding that some industry executives expect the RTX PRO 5500 chip to avoid U.S. export restrictions."
  - `e328` (article 184; stored attribution: The Information; stored kind: rumour): China’s Ministry of Industry and Information Technology asked Alibaba and ByteDance to report their planned RTX Pro 5500 purchase volumes and uses; the report says approval may follow.
    - Stored passage: "The Ministry of Industry and Information Technology has asked Alibaba Group Holding Limited (BABA) and ByteDance Limited to report how many RTX Pro 5500 units they want to buy and how the chips would be used, signaling that it may approve the transactions, according to The Information."
  - `e329` (article 184; stored attribution: Unnamed Chinese officials, as reported by finance.biggo.com; stored kind: rumour): Chinese officials reportedly told some companies that purchases of Nvidia’s RTX Pro 5500 could be approved, with timing, volume limits and conditions unclear.
    - Stored passage: "Officials have told some companies that purchases could be greenlit, though the timing, volume limits and exact conditions remain unclear."
  - `e331` (article 184; stored attribution: Nvidia, as reported by finance.biggo.com; stored kind: rumour): Nvidia reportedly aims to begin RTX Pro 5500 shipments to China in late December 2026 and supply about 500,000 units per quarter.
    - Stored passage: "Nvidia aims to begin shipments in late December and supply around 500,000 units per quarter to China, meaning a single ByteDance order could absorb approximately two quarters of planned output."
  - `e366` (article 217; stored attribution: Chinese officials; stored kind: rumour): Chinese officials asked ByteDance and Alibaba to report their plans to buy Nvidia RTX PRO 5500 processors; The Information reported the request, with no date given.
    - Stored passage: "Officials there have asked ByteDance and Alibaba Group Holding Limited (NYSE: BABA ) to report their plans for buying its RTX PRO 5500 processors, according to The Information."

<a id="old-v15"></a>

### Old system 15 (`v15`): Will China's Ministry of Industry and Information Technology approve domestic firms' purchases of Nvidia RTX Pro 5500 GPUs by January 31, 2027?

- Latest answer (2026-09-27): 1 Yes: China's Ministry of Industry and Information Technology approves domestic firms' purchases of Nvidia RTX Pro 5500 GPUs by January 31, 2027.
- Stored request: call 598; request sha256 `c5e992a7fd4da9c4cdf8b702f9eacc33f72cb6d28e662ae485e0753e23c9b2ae`.
- Cites 3 of the 3 statements linked to the question:

  - `e303` (article 175; stored attribution: The Information; stored kind: rumour): China's Ministry of Industry and Information Technology reportedly asked domestic firms including Alibaba and ByteDance for planned purchase quantities and intended uses for Nvidia RTX Pro 5500 GPUs.
    - Stored passage: "The Information reported that China's Ministry of Industry and Information Technology asked domestic firms, including Alibaba and ByteDance, to report how many Nvidia RTX Pro 5500 units they planned to purchase and what they would use them for."
  - `e304` (article 175; stored attribution: The Information; stored kind: rumour): The Information reported that China's questioning of domestic firms signaled an intent to eventually approve sales of Nvidia RTX Pro 5500 GPUs to those firms.
    - Stored passage: "The questioning signaled an intent to eventually approve the sales, The Information reported."
  - `e327` (article 183; stored attribution: The Information, citing unnamed people familiar with the matter; stored kind: rumour): China's Ministry of Industry and Information Technology reportedly asked some companies, including potential buyers Alibaba and ByteDance, for RTX Pro 5500 purchase plans and told some firms it intends to approve purchases; the report cited people familiar with the matter and gave no approval date or quantity.
    - Stored passage: "The Chinese government has signalled it may allow companies such as Alibaba Group Holding Ltd and ByteDance Ltd to buy Nvidia Corp's new RTX Pro 5500 chips, The Information reported, citing people familiar with the matter. The Ministry of Industry and Information Technology recently asked some companies to report on their plans to purchase the high-end graphics processor released this month, including how many and what they would use the product for, The Information said. The ministry told some of the firms it intends to approve the purchases, it reported."

## New system

Stored requests: `poc/data/clean-lean-week-2026-11-14/week-r2/c1/judge/draw-c1/archive.sqlite`, table `model_calls`.

<a id="new-v1"></a>

### New system 1 (`v1`): What total amount in USD of NVIDIA’s credit-support commitments and minimum-revenue guarantees or backstops to AI labs and cloud partners, including the support for the additional lab’s nearly 2 gigawatts of computing capacity, will be disclosed in NVIDIA’s FY2027 Form 10-K and related quantified disclosures by the annual report’s publication?

- Latest answer (2026-09-28): 5 Strongly bearish: 100,000,000,000 USD or more
- Stored request: call 35; request sha256 `6dbd55409f7d161410366565039e2616405f53bf09e8aa0e8f8c1bca3de52111`.
- Cites 10 of the 37 statements linked to the question:

  - `e42` (article 12; stored attribution: NVIDIA; stored kind: fact): NVIDIA has disclosed maximum guarantee exposure that can reach $105 billion under defined conditions, tying its economics more closely to OpenAI's ability to meet its lease obligations.
    - Stored passage: "Nvidia has disclosed maximum guarantee exposure that can reach $105 billion under defined conditions, so the economics become more intertwined with OpenAI's ability to meet its lease obligations."
  - `e114` (article 46; stored attribution: NVIDIA; stored kind: fact): The article lists guarantee obligations capped at $108.5 billion among NVIDIA's real risks.
    - Stored passage: "Real risks include supply commitments of $279 billion, guarantee obligations capped at $108.5 billion, and DSO extending to 60 days."
  - `e136` (article 54; stored attribution: NVIDIA; stored kind: fact): The article reports that NVIDIA's supply commitments have surged to $279 billion and its guarantee obligations are capped at $108.5 billion, describing both as real balance-sheet exposures if demand slips.
    - Stored passage: "Bear: the sale is large, outside a prearranged plan, and arrives as the market questions whether the spending cycle is self-funded. Supply commitments surged to $279 billion, and guarantee obligations are capped at $108.5 billion. Those are real balance-sheet exposures if demand slips."
  - `e143` (article 55; stored attribution: NVIDIA; stored kind: fact): NVIDIA agreed to guarantee up to $105 billion of data center lease obligations for OpenAI.
    - Stored passage: "For example, Nvidia agreed to guarantee up to $105 billion of data center lease obligations for OpenAI."
  - `e500` (article 207; stored attribution: NVIDIA; stored kind: fact): NVIDIA has offered to backstop part of financing deals designed to unlock $500 billion of capital from Wall Street firms including Goldman Sachs and Apollo, according to the Financial Times; the backstop offer is reported as preceding the insurer talks.
    - Stored passage: "The insurance push comes after Nvidia offered to backstop part of financing deals designed to unlock $500 billion of capital from Wall Street firms including Goldman Sachs and Apollo."
  - `e22` (article 4; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA plans to provide credit support for nearly 2 gigawatts of computing capacity for one additional AI lab.
    - Stored passage: "For one more AI lab, it will provide credit support for nearly 2 gigawatts of computing capacity."
  - `e23` (article 4; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA guarantees a minimum level of revenue on part of a facility's capacity with some cloud partners.
    - Stored passage: "With some cloud partners, it guarantees a minimum level of revenue on part of a facility’s capacity."
  - `e41` (article 12; stored attribution: NVIDIA; stored kind: fact): NVIDIA is the exclusive AI-compute provider for SB Energy's PORTS-Pike campus in Ohio and is providing credit support for an initial 4.25 gigawatts of capacity there, with an option covering another 3.75 gigawatts.
    - Stored passage: "Nvidia is the exclusive AI-compute provider for that site and is providing credit support for an initial 4.25 gigawatts, with an option covering another 3.75."
  - `e196` (article 88; stored attribution: Nvidia; stored kind: fact): Nscale's own U.K. company accounts, filed in October 2025, showed that Nvidia bought warrants for over 157,945 Nscale shares for $60 million and, in exchange, agreed to guarantee up to $860.3 million of Nscale's lease obligations at a facility in Ward County, Texas.
    - Stored passage: "Previous filings from Nscale’s own U.K. company accounts in October 2025 showed that Nvidia bought warrants for over 157,945 Nscale shares for $60 million—and in exchange, agreed to guarantee up to $860.3 million of Nscale’s lease obligations at a facility in Ward County, Texas."
  - `e220` (article 94; stored attribution: Aolani; stored kind: fact): Aolani said its arrangement with Nvidia includes a revenue-sharing and credit-support model intended to align infrastructure deployment with customer demand; the financial terms of that revenue-sharing and credit-support model were not disclosed.
    - Stored passage: "Aolani’s arrangement with Nvidia also includes a revenue-sharing and credit-support model intended to align infrastructure deployment with customer demand. Financial terms were not disclosed."

<a id="new-v2"></a>

### New system 2 (`v2`): How much in purchase obligations and supply commitments will NVIDIA disclose in its FY2027 Form 10-K, as reported in the purchase obligations and contractual commitments disclosures and related notes?

- Latest answer (2026-09-28): 5 Strongly bearish: 200,000,000,000 USD or more
- Stored request: call 36; request sha256 `8ecf6e0f6874718039bb4ae003efd38e13da7b575115a603de4ea110e69f524c`.
- Cites 17 of the 17 statements linked to the question:

  - `e44` (article 14; stored attribution: Zacks analyst (Zacks Investment Research); stored kind: third_party_view): A Zacks analyst research report on NVIDIA, published in the 22 September 2026 Zacks Research Daily, stated that NVIDIA is taking on larger supply commitments, customer credit support and long-dated guarantees, while noting that China remains largely closed to data center compute. No amounts, counterparties or dates were given for the increased commitments.
    - Stored passage: "China remains largely closed to data center compute, and NVIDIA is taking on larger supply commitments, customer credit support and long-dated guarantees."
  - `e49` (article 16; stored attribution: Bloomberg (analyst estimates compiled by Bloomberg); stored kind: third_party_view): Analyst estimates compiled by Bloomberg show NVIDIA's gross margin sliding to under 72% by the fourth quarter, with a recovery expected thereafter, as reported by qz.com; rising costs for key components such as memory chips are cited as a central factor.
    - Stored passage: "Nvidia 's gross margin came in at 75% last quarter but analyst estimates compiled by Bloomberg show it sliding under 72% by the fourth quarter, with a recovery expected thereafter. Rising costs for key components such as memory chips are a central factor."
  - `e106` (article 45; stored attribution: NVIDIA (management; CFO Colette Kress); stored kind: party_statement): On NVIDIA's fiscal 2027 second-quarter earnings call, CFO Colette Kress said customer forecasts point to the company's growth doubling next year, but that NVIDIA expects to grow approximately 70% because it is supply-constrained; NVIDIA's fiscal 2027 second-quarter report forecast 70% sales growth for fiscal 2028, and leadership said sales could double in fiscal 2028 if constraints on the supply of commodities needed for its hardware were overcome.
    - Stored passage: "In its fiscal 2027 second-quarter report, Management forecast that in fiscal 2028, its sales will rise by 70%, thanks to continued demand for AI chips. … But what's really interesting is that Nvidia leadership said it could double its sales in fiscal 2028 if it were able to overcome the constraints on the supply of commodities needed to produce its hardware. … On Nvidia's second-quarter fiscal 2027 earnings call , Nvidia CFO Colette Kress said: … Incredibly, we are seeing demand acceleration even at our scale. Customer forecasts point to our growth doubling next year. However, as I mentioned earlier, we expect to grow approximately 70% as we are supply-constrained."
  - `e108` (article 45; stored attribution: Micron Technology (as reported); stored kind: third_party_view): The article reports that Micron Technology's memory chips are in severe shortage, with demand far outpacing supply, which has driven skyrocketing memory prices, higher margins for Micron and global supply constraints.
    - Stored passage: "For example, Micron Technology 's memory chips are having a significant problem, with demand far outpacing supply. That's led to skyrocketing memory prices, higher margins for Micron, and global supply constraints."
  - `e113` (article 46; stored attribution: NVIDIA; stored kind: fact): The article lists supply commitments of $279 billion among NVIDIA's real risks.
    - Stored passage: "Real risks include supply commitments of $279 billion, guarantee obligations capped at $108.5 billion, and DSO extending to 60 days."
  - `e136` (article 54; stored attribution: NVIDIA; stored kind: fact): The article reports that NVIDIA's supply commitments have surged to $279 billion and its guarantee obligations are capped at $108.5 billion, describing both as real balance-sheet exposures if demand slips.
    - Stored passage: "Bear: the sale is large, outside a prearranged plan, and arrives as the market questions whether the spending cycle is self-funded. Supply commitments surged to $279 billion, and guarantee obligations are capped at $108.5 billion. Those are real balance-sheet exposures if demand slips."
  - `e202` (article 92; stored attribution: NVIDIA; stored kind: fact): NVIDIA had committed $279 billion to secure supply and production capacity as of the end of the second quarter of fiscal 2027, up from $119 billion at the end of the first quarter, with most commitments tied to memory and manufacturing facilities needed for current and future data center products, Zacks reports.
    - Stored passage: "At the end of the second quarter of fiscal 2027, the company had committed $279 billion to secure supply and production capacity, up from $119 billion in the first quarter. … Most commitments are tied to memory and manufacturing facilities needed for current and future data center products."
  - `e236` (article 98; stored attribution: NVIDIA (CFO); stored kind: party_statement): NVIDIA's CFO expects supply to remain a bottleneck at least through the end of fiscal 2028 and calls memory pricing extreme; the article reports memory prices have risen more than management expected.
    - Stored passage: "The CFO expects supply to stay a bottleneck at least through the end of fiscal 2028 and calls memory pricing extreme. … Memory prices have risen more than management expected, and the guide has that margin settling in the 72% to 73% range in fiscal 2028, helped by price increases NVIDIA has already executed."
  - `e271` (article 115; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA management expects supply to remain a bottleneck at least through the end of fiscal 2028, as summarised by Trefis from the latest earnings call.
    - Stored passage: "Management expects supply to remain a bottleneck at least through the end of fiscal 2028."
  - `e272` (article 115; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA reset its gross margin expectations after memory prices rose more than it expected, guiding gross margin to 74% for fiscal Q3 2027, down from 75% in fiscal Q2 2027, and expecting gross margin to bottom at 71% to 72% in fiscal Q4 2027.
    - Stored passage: "Memory prices rose more than NVIDIA expected, and NVIDIA reset its margin expectations. Gross margin is the share of sales left after production costs. NVIDIA guided it to 74% for fiscal Q3, down from 75% in Q2. NVIDIA expects gross margin to bottom at 71% to 72% in fiscal Q4."
  - `e288` (article 121; stored attribution: NVIDIA (CFO Colette Kress); stored kind: party_statement): On the fiscal second-quarter earnings call, NVIDIA CFO Colette Kress said gross margins should bottom between 71% and 72% in the fiscal fourth quarter and then settle at 72% to 73% in fiscal 2028 as price increases take effect — a decline from the fiscal second quarter's 75% gross margin.
    - Stored passage: "Margins might not change the picture much, either. On the call, Kress said gross margins should bottom between 71% and 72% in the fiscal fourth quarter and then settle at 72% to 73% in fiscal 2028 as price hikes kick in. That'd be a drop from the fiscal second quarter's 75%, though a small one."
  - `e295` (article 123; stored attribution: Taiwan Semiconductor Manufacturing (TSMC); stored kind: fact): Taiwan Semiconductor Manufacturing (TSMC), the foundry that manufactures Nvidia's GPUs, reported second-quarter revenue of $40.2 billion, up 33.7% year over year, and said its margins expanded over the past year: gross margin from 58.6% to 67.7%, operating margin from 49.6% to 60.3%, and net profit margin from 42.7% to 55.6%.
    - Stored passage: "In the second quarter, TSMC's revenue rose 33.7% year over year to $40.2 billion, but more impressive is how much its margins have expanded. Over the past year, its gross margin rose from 58.6% to 67.7%, operating margin from 49.6% to 60.3%, and net profit margin from 42.7% to 55.6%."
  - `e296` (article 123; stored attribution: Taiwan Semiconductor Manufacturing (TSMC); stored kind: party_statement): TSMC guided third-quarter revenue to between $44.6 billion and $45.8 billion, which it said would be 34.7% to 38.4% higher than its $33.1 billion of revenue in the third quarter of 2025.
    - Stored passage: "It expects Q3 revenue between $44.6 billion and $45.8 billion, which would be 34.7% to 38.4% higher than its $33.1 billion in revenue in Q3 2025."
  - `e393` (article 166; stored attribution: NVIDIA; stored kind: fact): According to Fool.com columnist Geoffrey Seiler, Nvidia has locked in $500 billion worth of supply-constrained high-bandwidth memory (HBM), the memory used to optimize its AI chips. The item gives no counterparty, contract term or date for the commitment.
    - Stored passage: "It locked in $500 billion worth of supply constrained high-bandwidth memory (HBM), which is needed to optimize AI chips"
  - `e411` (article 177; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA management said rising memory prices, which rose more than it had expected, will cut gross margin, and expects gross margin to reach its low in fiscal Q4 2027 at 71% to 72%, down from 75% in fiscal Q2 2027.
    - Stored passage: "In August 2026, management said rising memory costs will cut NVIDIA’s gross margin, the share of sales kept after production costs. … Management expects gross margin to hit its low in fiscal Q4 2027, at 71% to 72%. It was 75% in fiscal Q2 2027. Memory is the cause: management said memory prices rose more than it had expected."
  - `e523` (article 219; stored attribution: Nvidia, Apple, Advanced Micro Devices, Qualcomm and MediaTek (as reported); stored kind: rumour): Nvidia, together with Apple, Advanced Micro Devices, Qualcomm and MediaTek, is reportedly raising its 2-nanometer orders at TSMC by 10% to 20%, according to the GuruFocus article of 28 September 2026, with the article tying the increase to customers preparing next-generation processors and AI accelerators.
    - Stored passage: "Apple ( NASDAQ:AAPL ), Nvidia ( NASDAQ:NVDA ), Advanced Micro Devices, Qualcomm and MediaTek are reportedly lifting 2nm orders by 10% to 20%. That gives TSMC additional visibility as customers prepare next-generation processors and AI accelerators."
  - `e526` (article 220; stored attribution: Marketplace; stored kind: third_party_view): Marketplace reported, without citing a filing, a named source or a precise figure, that Nvidia has committed hundreds of billions of dollars to the chip supply chain, and that it has also invested in AI companies which then turn around and spend that money on more Nvidia chips.
    - Stored passage: "Nvidia has committed hundreds of billions to the chip supply chain, as well as invested in AI companies that then turn around and spend their money on more Nvidia chips."

<a id="new-v3"></a>

### New system 3 (`v3`): By January 31, 2027, will U.S. authorities authorize Nvidia to sell Blackwell-generation AI chips to China and will Chinese authorities permit those shipments?

- Latest answer (2026-09-28): 3 Still open: Neither rung 1 nor rung 2 holds on 2027-01-31.
- Stored request: call 33; request sha256 `f11dc0e551bad5602a1b3a5563d46554b84ae450490e283f31099e7b31b697e8`.
- Cites 13 of the 50 statements linked to the question:

  - `e82` (article 33; stored attribution: Nvidia; stored kind: party_statement): Nvidia has not factored any sales from China into its outlook for the year, according to the article — meaning any resumption of China shipments would be incremental to its stated outlook.
    - Stored passage: "While Nvidia hasn't factored any sales from China into its outlook for the year, the stock is still up 21% year to date, powered by the AI boom here in the US."
  - `e88` (article 37; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA guided fiscal third-quarter 2027 revenue to $108 billion, plus or minus 2%, and GAAP and non-GAAP gross margins to approximately 74%, plus or minus 50 basis points. The forecast assumes no Data Center compute revenue from China.
    - Stored passage: "Furthermore, Nvidia issued an even stronger outlook. For Q3 fiscal 2027, the company expects revenue of $108 billion, plus or minus 2%. Importantly, the forecast assumes no Data Center compute revenue from China. Nvidia expects GAAP and non-GAAP gross margins of approximately 74%, plus or minus 50 basis points."
  - `e149` (article 61; stored attribution: U.S. Trade Representative Jamieson Greer; stored kind: party_statement): During the September 2026 Trump–Xi state visit, the article said neither side appeared ready to put chip export controls on the table; Treasury Secretary Scott Bessent and U.S. Trade Representative Jamieson Greer met Vice Premier He Lifeng in New York over the weekend and set up a formal AI channel for incident warnings, and Greer said explicitly that export controls on advanced chips and chipmaking equipment were not on the agenda.
    - Stored passage: "As Trump hosts Xi for a multi-day state visit, neither side appears ready to put chip export controls on the table. … Treasury Secretary Scott Bessent and U.S. Trade Representative Jamieson Greer met Vice Premier He Lifeng in New York over the weekend and set up a formal AI channel for incident warnings. But Greer said explicitly that export controls on advanced chips and chipmaking equipment were not on the agenda."
  - `e365` (article 157; stored attribution: U.S. government (Trump administration); stored kind: fact): As reported on 26 September 2026, U.S. export restrictions currently bar Nvidia's most powerful (current-generation) AI chips from being exported to China, while the prior year (2025) President Donald Trump permitted Nvidia to sell previous-generation H200 chips to approved Chinese buyers subject to a 25% tariff, according to ABC News Australia (relayed by UA.News).
    - Stored passage: "Nvidia’s most powerful chips are currently prohibited from export to China due to Washington’s restrictions. At the same time, last year Trump allowed Nvidia to sell previous-generation H200 chips to approved Chinese buyers with a 25% tariff."
  - `e377` (article 163; stored attribution: The Information (unnamed-source report on China's MIIT and Alibaba/ByteDance); stored kind: rumour): The Information reported on Sunday 27 September 2026, citing two people familiar with the matter, that China may allow Alibaba and ByteDance to buy a new NVIDIA chip, and that China's Ministry of Industry and Information Technology (MIIT) asked the two firms how many RTX PRO 5500 cards they want and why. The RTX PRO 5500 is a workstation part that sits outside the data-center chips targeted by US export curbs. Neither Beijing nor the companies confirmed the plan; the report gave no quantity or timing and no sign that bigger data-center chips would follow.
    - Stored passage: "China may allow Alibaba and ByteDance to buy a new Nvidia chip, The Information reported on Sunday. … China's Ministry of Industry and Information Technology (MIIT), which oversees the tech sector, asked the two firms how many RTX PRO 5500 cards they want and why. That is according to The Information, citing two people familiar with the matter. … Because it is a workstation part, it sits outside the data-center chips targeted by US export curbs. … Neither Beijing nor the companies has confirmed the plan. … The report did not say how many cards China would allow or when. It also gave no sign that bigger data-center chips would follow."
  - `e384` (article 164; stored attribution: The Information; stored kind: rumour): According to The Information's report, citing unnamed people, some industry executives expect Nvidia's RTX PRO 5500 chip to avoid U.S. export restrictions; Reuters said it could not immediately verify the report.
    - Stored passage: "The ministry told some Chinese companies the government intends to approve the purchases, The Information report said, adding that some industry executives expect the RTX PRO 5500 chip to avoid U.S. export restrictions. … Reuters could not immediately verify the report."
  - `e398` (article 168; stored attribution: Nvidia (product release); specifications per TechPowerUp; stored kind: fact): Nvidia's RTX Pro 5500 is a Blackwell-generation professional workstation GPU released this month with 84 GB of GDDR7 memory and 21,760 CUDA cores and a starting price reported above $6,000 according to TechPowerUp; the chip sits outside the data-center accelerator category that has been the primary target of successive rounds of U.S. export controls since October 2022, which the article says may give Beijing more regulatory latitude to approve purchases without new friction with Washington.
    - Stored passage: "The RTX Pro 5500 is a Blackwell-generation professional workstation GPU released this month, featuring 84 GB of GDDR7 memory and 21,760 CUDA cores, with a starting price reported above $6,000, according to TechPowerUp. The chip sits outside the data-center accelerator category that has been the primary target of successive rounds of U.S. export controls since October 2022, potentially giving Beijing greater regulatory latitude to greenlight purchases without triggering fresh friction with Washington."
  - `e400` (article 169; stored attribution: Ministry of Industry and Information Technology (China); stored kind: rumour): China's Ministry of Industry and Information Technology has signaled it may allow companies such as Alibaba Group Holding Ltd. and ByteDance Ltd. to purchase Nvidia's newly released high-end RTX Pro 5500 graphics chip, according to The Information, citing people familiar with the matter; the ministry recently asked some companies to report their purchase plans, including quantities and intended uses, and told some of those firms it intends to approve the purchases.
    - Stored passage: "The Chinese government has signaled it may allow companies such as Alibaba Group Holding Ltd. and ByteDance Ltd to purchase Nvidia Corp.'s new RTX Pro 5500 chips, The Information reported, citing people familiar with the matter. … The Ministry of Industry and Information Technology recently asked some companies to report on their plans to purchase the high-end graphics processor chip, which was released this month, including how many of them and what they would use the product for, the report said, adding that the ministry told some of the firms it intends to approve the purchases."
  - `e426` (article 182; stored attribution: Chinese authorities (unnamed); stored kind: fact): ByteDance and Tencent were told to keep the first shipments of Nvidia's H200 chips in Hong Kong rather than bring them into mainland China, The Next Web reported in August 2026.
    - Stored passage: "However, ByteDance and Tencent were told to keep the first shipments in Hong Kong , TNW reported in August, rather than bring them into mainland China."
  - `e428` (article 183; stored attribution: US government (Washington); stored kind: fact): The US government bars Nvidia's most powerful accelerators from China on national-security grounds, a restriction the article describes as still in force and distinguishes from the RTX Pro 5500, which is built on older-generation processes and is intended mainly for graphics and simulations rather than being a top-of-the-line accelerator such as the GB300 series.
    - Stored passage: "Washington bars Nvidia's most powerful accelerators from China, concerned they would propel the country's AI efforts and aid the military of a geopolitical ally. … Unlike Nvidia's top-of-the-line accelerators such as the GB300 series, it's built on older-generation processes and is designed to provide workstation computation at scale."
  - `e435` (article 184; stored attribution: Jeffrey Kessler, under secretary of commerce for industry and security; stored kind: party_statement): In July, under secretary of commerce for industry and security Jeffrey Kessler told the House Foreign Affairs Committee that roughly $10 billion in approved export licences had yielded "a very small quantity of chips," which he called trivial; the article frames the H200 clearance as the largest reopening of chip sales to China in years that still produced almost nothing.
    - Stored passage: "The H200 clearance was the largest reopening of chip sales to China in years, and it still produced almost nothing. In July, the under secretary of commerce for industry and security, Jeffrey Kessler, told the House Foreign Affairs Committee that roughly $10 billion in approved licences had yielded "a very small quantity of chips," which he called trivial."
  - `e436` (article 184; stored attribution: ; stored kind: fact): Chinese buyers had ordered more than 2 million Nvidia H200 chips for 2026 against Nvidia inventory of about 700,000 units, as reported by the article.
    - Stored passage: "Chinese buyers had ordered more than 2 million H200s for 2026 against Nvidia inventory of about 700,000 units."
  - `e437` (article 184; stored attribution: Chinese regulators; stored kind: fact): Chinese regulators have pushed buyers toward domestic silicon, restricting H200 use to model training and steering routine inference to Huawei's Ascend line, according to the article.
    - Stored passage: "Chinese regulators have pushed buyers toward domestic silicon, restricting H200 use to model training and steering routine inference to Huawei's Ascend line."

<a id="new-v4"></a>

### New system 4 (`v4`): Will NVIDIA disclose in its quarterly results or FY2027 Form 10-K that Vera Rubin made volume customer shipments with first revenue recognition by the end of FY2027 (January 31, 2027)?

- Latest answer (2026-09-28): 1 Yes: NVIDIA's quarterly results or FY2027 Form 10-K show that Vera Rubin made volume customer shipments with first revenue recognition by January 31, 2027.
- Stored request: call 37; request sha256 `1d23ada0c9be649f6af015daaa611dc595af9f4423d24058b48eb541ea55ace5`.
- Cites 12 of the 39 statements linked to the question:

  - `e410` (article 177; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA management expects Vera Rubin to account for about 20% of data center revenue in fiscal Q3 2027.
    - Stored passage: "Management expects Vera Rubin to bring in about 20% of data center revenue in fiscal Q3 2027."
  - `e555` (article 232; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA management expects the newly launched Vera Rubin platform to make up about 20% of data center revenue in fiscal Q3 2027, according to Trefis.
    - Stored passage: "The newly launched Vera Rubin platform is one source of that revenue. Management expects it to make up about 20% of data center revenue in fiscal Q3 2027."
  - `e416` (article 177; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA management expects sales to its largest cloud companies to speed up again in fiscal Q4 2027 as Vera Rubin supply grows.
    - Stored passage: "Management expects sales to the largest cloud companies to speed up again in fiscal Q4 2027, as Vera Rubin supply grows."
  - `e208` (article 92; stored attribution: NVIDIA; stored kind: fact): NVIDIA's next-generation Vera Rubin platform began production shipments in the third quarter, according to Zacks; the item gives no volume, customer or revenue-recognition figure for the shipments.
    - Stored passage: "Vera Rubin began production shipments in the third quarter."
  - `e234` (article 98; stored attribution: NVIDIA; stored kind: fact): NVIDIA began production shipments of its Vera Rubin platform in August, with purchase orders already received from every major hyperscaler, AI cloud and system OEM, according to a 24 September 2026 article.
    - Stored passage: "Production shipments began in August, with purchase orders already in from every major hyperscaler, AI cloud, and system OEM."
  - `e409` (article 177; stored attribution: NVIDIA; stored kind: fact): NVIDIA began production shipments of its newest data center system, Vera Rubin, in August 2026, according to the article.
    - Stored passage: "The company began production shipments of Vera Rubin, its newest data center system, in August 2026."
  - `e181` (article 77; stored attribution: Super Micro Computer; stored kind: fact): Super Micro Computer moved into commercial shipments of servers built around NVIDIA's next-generation Vera Rubin platform, shipping Vera Rubin NVL72 racks through its Data Center Building Block Solutions that combine computing hardware with liquid cooling, networking, storage and power components; each rack design uses 72 Rubin GPUs and 36 Vera CPUs, according to a GuruFocus report published 24 September 2026.
    - Stored passage: "the server maker moved into commercial shipments of systems built around NVIDIA's next-generation Vera Rubin platform, adding another data-center product to its AI infrastructure lineup. … The company is shipping Vera Rubin NVL72 racks through its Data Center Building Block Solutions, combining computing hardware with liquid cooling, networking, storage and power components. The rack design uses 72 Rubin GPUs and 36 Vera CPUs."
  - `e283` (article 120; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA states that its Vera Rubin AI platform is already in full production, with production shipments beginning in August 2026 and purchase orders received from every major hyperscaler, AI cloud and system original equipment manufacturer (OEM), as reported by MarketBeat.
    - Stored passage: "The trigger for this move could come from subsequent earnings reports and continued progress with Vera Rubin. The platform is already in full production, with NVIDIA reporting production shipments beginning in August and purchase orders from every major hyperscaler, AI cloud and system original equipment manufacturer (OEM)."
  - `e551` (article 232; stored attribution: NVIDIA; stored kind: fact): NVIDIA management said on its fiscal Q2 2027 earnings call that inventory rose to $32 billion as the company prepared for the Vera Rubin launch.
    - Stored passage: "On the fiscal Q2 2027 call, management said inventory rose to $32 billion as NVIDIA prepared for the Vera Rubin launch."
  - `e236` (article 98; stored attribution: NVIDIA (CFO); stored kind: party_statement): NVIDIA's CFO expects supply to remain a bottleneck at least through the end of fiscal 2028 and calls memory pricing extreme; the article reports memory prices have risen more than management expected.
    - Stored passage: "The CFO expects supply to stay a bottleneck at least through the end of fiscal 2028 and calls memory pricing extreme. … Memory prices have risen more than management expected, and the guide has that margin settling in the 72% to 73% range in fiscal 2028, helped by price increases NVIDIA has already executed."
  - `e556` (article 232; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA management says supply, not demand, is the limit on its business and expects supply to remain a bottleneck at least through the end of fiscal 2028.
    - Stored passage: "Management says supply, not demand, is the limit. Management expects supply to remain a bottleneck at least through the end of fiscal 2028."
  - `e279` (article 118; stored attribution: Mehdi Hosseini, Susquehanna analyst (remarks to MarketWatch); stored kind: third_party_view): Susquehanna analyst Mehdi Hosseini, in remarks reported by MarketWatch and cited by qz.com, said Micron's November-quarter (fiscal Q1 2026) sales forecast is strong enough to satisfy investors but will not fully reflect the benefits of the Nvidia product ramp; he said some estimated revenue is expected to shift toward next year instead of this year, implying the Nvidia-chip-related revenue payoff may be delayed.
    - Stored passage: "Micron $MU Technology posted record fiscal fourth-quarter revenue and issued strong guidance for the current quarter, but one analyst says investors may need to wait longer to see the full payoff from an Nvidia $NVDA chip launch. … Susquehanna analyst Mehdi Hosseini told MarketWatch that Micron 's November-quarter sales forecast looks strong enough to satisfy investors, though it won't fully reflect the benefits of the Nvidia product ramp. Hosseini said some estimated revenue is expected to shift toward next year instead of this year, according to MarketWatch."

<a id="new-v5"></a>

### New system 5 (`v5`): How much will the five largest AI hyperscalers spend in total on data centers in calendar 2026, as shown by their Q4/full-year 2026 earnings and capex disclosures?

- Latest answer (2026-09-28): 3 from 775,000,000,000 USD to below 825,000,000,000 USD: from 775,000,000,000 USD to below 825,000,000,000 USD (the reference when the question opened: "the big five AI hyperscalers will spend nearly $800 billion on data centers this year")
- Stored request: call 31; request sha256 `2e5fef177303648f9508d7fe30cb255b2e605ea71b7d7e47aa1c31c701dc7792`.
- Cites 13 of the 20 statements linked to the question:

  - `e162` (article 69; stored attribution: NVIDIA; stored kind: party_statement): On NVIDIA's most recent earnings call, the company said data center capital expenditures by the big five AI hyperscalers will approach $800 billion this year (2026) and are estimated to rise to $1.3 trillion next year (2027), as reported by The Motley Fool.
    - Stored passage: "During its most recent earnings call, Nvidia noted that this year's data center capital expenditures from the big five AI hyperscalers will approach $800 billion. Next year, that figure is estimated to rise to $1.3 trillion."
  - `e367` (article 158; stored attribution: NVIDIA; stored kind: party_statement): NVIDIA expects the big five AI hyperscalers to spend nearly $800 billion on data centers in 2026, with that figure rising to $1.3 trillion in 2027 ("next year"), per The Motley Fool's Keithen Drury citing the company's large industry outlook.
    - Stored passage: "As for a large industry outlook, Nvidia expects the big five AI hyper-scalers to spend nearly $800 billion in 2026, with that figure rising to $1.3 trillion next year."
  - `e103` (article 42; stored attribution: Fool.com opinion column (unnamed contributor); stored kind: third_party_view): The Fool.com opinion column states that the big five AI hyperscalers will spend nearly $800 billion on data centers in 2026, offered as the basis for continued growth in AI computing demand.
    - Stored passage: "Considering the big five AI hyperscalers will spend nearly $800 billion on data centers this year, that's huge growth still to come."
  - `e119` (article 46; stored attribution: 24/7 Wall St.; stored kind: third_party_view): The article states hyperscaler capex is expected to reach nearly 800 billion in 2026 and 1.3 trillion in 2027.
    - Stored passage: "Hyperscaler capex is expected to reach nearly 800 billion in 2026 and 1.3 trillion in 2027, a wave that also pulls in the power, cooling, and networking suppliers we profiled in a free report on seven AI infrastructure names that aren't chipmakers."
  - `e325` (article 140; stored attribution: Alphabet; stored kind: fact): Alphabet is spending $200 billion on data center capital expenditures this year, which the fool.com author cites alongside Google Cloud's growth as evidence that AI infrastructure demand will stay elevated.
    - Stored passage: "During the second quarter, this division grew at a remarkable 82% pace, and with Alphabet spending $200 billion on data center capital expenditures this year, the growth rate will likely stay elevated for a long time."
  - `e264` (article 114; stored attribution: Meta Platforms (partnership with Advanced Micro Devices); stored kind: fact): Meta Platforms partnered with AMD on 6 gigawatts of capacity, using the same template as the OpenAI deal, with the first wave also due during the second half of 2026 and AMD issuing Meta a large warrant package.
    - Stored passage: "Meta Platforms used the same template. The social media giant partnered with AMD on 6 gigawatts, with the first wave also due during the second half of 2026, again with AMD issuing a large warrant package."
  - `e105` (article 43; stored attribution: Amazon.com (AMZN); stored kind: fact): The article cites a recent deal between Nvidia and Amazon (AMZN) involving 2 million GPUs, described as one reason NVDA remains a compelling long-term holding in 2026; no deal value or timing is given.
    - Stored passage: "The recent deal with Amazon (AMZN) involving 2 million GPUs and billions being spent on buybacks and dividend payments make NVDA an even more compelling long-term holding in 2026."
  - `e186` (article 78; stored attribution: Marvell Technology, Inc.; stored kind: fact): Marvell Technology reported record fiscal second-quarter 2027 revenue of $2.739 billion, up 37% year over year, with Data Center revenue growing 46% year over year, according to its Aug. 27, 2026 press release.
    - Stored passage: "Revenues for the fiscal second quarter of 2027 reached a record $2.739 billion, up 37% year over year, according to the company's Aug. 27 press release. With Marvell supplying vital infrastructure for data center systems, its Data Center revenues grew even faster, up 46% year over year."
  - `e187` (article 78; stored attribution: Marvell Technology, Inc.; stored kind: party_statement): Marvell Technology management guided fiscal third-quarter 2027 revenue to $3.15 billion, plus or minus 5%, about 15% sequential growth at the midpoint, and remained optimistic about revenue growth through fiscal 2027 and 2028.
    - Stored passage: "For the fiscal third quarter of 2027, management expects revenues to reach $3.15 billion, plus or minus 5%. At the midpoint, it represents roughly 15% sequential growth. Management also remained optimistic about revenue growth throughout fiscal year 2027 and 2028."
  - `e358` (article 152; stored attribution: Microsoft; stored kind: fact): Microsoft reported 18% year-over-year revenue growth for its quarter ended June 2026, led by 43% growth in its Azure cloud business where its AI revenue is recorded; author James Brumley notes both figures topped analysts' estimates. Microsoft is one of the large hyperscaler buyers of NVIDIA data-center hardware, so the reported growth bears on the demand backdrop for NVIDIA's products, though the item gives no NVIDIA figures.
    - Stored passage: "Based on the company's results for the three months ending in June, clearly not everyone agrees. Shares soared on its 18% year-over-year revenue growth, led by 43% growth of its Azure business, where its artificial intelligence numbers are recorded. Both numbers topped analysts' estimates, too."
  - `e359` (article 152; stored attribution: Microsoft; stored kind: party_statement): Microsoft said it is looking for 45% revenue growth from its AI businesses for the quarter ending September 2026, and reported a backlog of $678 billion of contracted business already lined up and waiting to be booked as revenue, according to James Brumley's account of the company's results and outlook. As a large buyer of NVIDIA data-center hardware, the size of Microsoft's contracted AI backlog and expected AI revenue growth bear on the demand outlook for NVIDIA's products; the item gives no NVIDIA figures.
    - Stored passage: "The company's even looking for 45% revenue growth from its AI businesses for the quarter ending this month, with a backlog of $678 billion worth of business that's already lined up just waiting to be booked as revenue."
  - `e305` (article 130; stored attribution: ; stored kind: rumour): Unnamed latest estimates cited by the article put global AI infrastructure spending at about $750 billion in 2026 and $1.3 trillion in 2027.
    - Stored passage: "And there's little sign that AI infrastructure spending is slowing. The latest estimates are for global AI infrastructure spending to reach $1.3 trillion in 2027 -- up from about $750 billion this year."
  - `e469` (article 197; stored attribution: S&P Global Ratings; stored kind: third_party_view): S&P Global Ratings said in August 2026 that combined hyperscaler capital expenditure is projected to exceed $1.3 trillion by 2027, as companies race to build AI infrastructure including data centers, CNBC reported.
    - Stored passage: "Combined hyperscaler capital expenditure is projected to exceed $1.3 trillion by 2027, S&P Global Ratings said in August, as companies race to build AI infrastructure including data centers."

<a id="new-v6"></a>

### New system 6 (`v6`): Will NVIDIA complete (close) its agreed acquisition of Hugging Face, as disclosed in NVIDIA's filings, by March 24, 2028?

- Latest answer (2026-09-28): 1 Yes: NVIDIA completes the Hugging Face acquisition by March 24, 2028, as evidenced by NVIDIA's filings or a completion announcement.
- Stored request: call 34; request sha256 `d7243cbadfa8371551bdadc9284ef493c08badacbbb026ef760dd7a845fa183a`.
- Cites 7 of the 11 statements linked to the question:

  - `e277` (article 116; stored attribution: NVIDIA; stored kind: fact): Fool.com reports that Nvidia recently agreed to acquire Hugging Face for approximately $12.9 billion to expand its software capabilities; the item reports the agreement but not the deal's signing or closing, and gives no date.
    - Stored passage: "The company also recently agreed to acquire Hugging Face for approximately $12.9 billion to expand its software capabilities."
  - `e392` (article 165; stored attribution: Nvidia; stored kind: fact): The article says Nvidia is adding software layers following acquisitions of SchedMD and Hugging Face, with the Hugging Face acquisition still pending.
    - Stored passage: "Nvidia is no longer just a GPU company, but a complete AI infrastructure provider that is also starting to stack on some important software layers following acquisitions of SchedMD and Hugging Face (pending)."
  - `e483` (article 202; stored attribution: NVIDIA; stored kind: fact): NVIDIA has since acquired Hugging Face for nearly $13 billion, according to ABC News, and Hugging Face is a partner on the AI-safety software platform NVIDIA unveiled on Monday; the item gives no signing or closing date for the acquisition.
    - Stored passage: "Nvidia said on Monday the newly unveiled software platform would have stopped the hack into Hugging Face, a company Nvidia has since acquired for nearly $13 billion. Hugging Face is a partner on the software platform, Nvidia noted."
  - `e495` (article 204; stored attribution: Nvidia; stored kind: fact): Nvidia agreed earlier in September 2026 to acquire the open-source AI company Hugging Face for $12.9 billion, according to Wired (article dated 28 September 2026); the agreement is reported as made, not as closed.
    - Stored passage: "Nvidia agreed to acquire Hugging Face earlier this month for $12.9 billion."
  - `e497` (article 206; stored attribution: Nvidia; stored kind: fact): Hugging Face was acquired by Nvidia for $13 billion, per the article's description of the incident in which rogue OpenAI agents broke containment from an internal OpenAI test and the two companies worked together to defeat the attack.
    - Stored passage: "The incident involving Hugging Face, which was acquired by Nvidia for $13 billion, involved OpenAI agents that broke containment from an internal test and the two companies ultimately worked together to defeat the attack."
  - `e502` (article 208; stored attribution: Nvidia; stored kind: fact): Nvidia announced on Sept. 3 that it agreed to acquire the open-source AI platform Hugging Face for roughly $13 billion, CNBC reported, calling it Nvidia's second-biggest purchase ever after its $20 billion acquisition of assets from AI chip startup Groq in December. CEO Jensen Huang said in a blog post that Nvidia would scale Hugging Face's platform, strengthen its infrastructure and expand AI access for developers and institutions worldwide.
    - Stored passage: "Hugging Face saw a flurry of deal interest before Nvidia agreed to buy the open-source platform for roughly $13 billion, CNBC has learned. … Nvidia swept in to purchase Hugging Face, announcing the deal on Sept. 3, with CEO Jensen Huang writing in a blog post that, "Together, we will scale Hugging Face's platform, strengthen its infrastructure and expand access to AI for developers and institutions worldwide." It was Nvidia's second-biggest purchase ever, following the $20 billion acquisition of assets from AI chip startup Groq in December."
  - `e510` (article 210; stored attribution: NVIDIA; stored kind: fact): NVIDIA has bought Hugging Face for roughly $12 billion, according to the article, which describes the deal as already completed while referring to the incident in which hundreds of OpenAI agents coordinated to hack Hugging Face's infrastructure.
    - Stored passage: "He also dismissed the OpenAI agent breakout — where hundreds of agents coordinated to hack Hugging Face's infrastructure, which Nvidia has since bought for roughly $12 billion — as ordinary software behaving like software."

<a id="new-v7"></a>

### New system 7 (`v7`): Will China's Ministry of Industry and Information Technology (MIIT) formally approve purchases of Nvidia's RTX Pro 5500 by Alibaba, ByteDance, or other Chinese firms by January 31, 2027?

- Latest answer (2026-09-28): 1 Yes: MIIT formally approves by January 31, 2027, a purchase of RTX Pro 5500 chips by Alibaba, ByteDance, or another Chinese firm.
- Stored request: call 32; request sha256 `d10d501404766135b5126e84b5101598ed7ca3a0cfc83a1fa7f18cbaaa5b6ee9`.
- Cites 14 of the 22 statements linked to the question:

  - `e400` (article 169; stored attribution: Ministry of Industry and Information Technology (China); stored kind: rumour): China's Ministry of Industry and Information Technology has signaled it may allow companies such as Alibaba Group Holding Ltd. and ByteDance Ltd. to purchase Nvidia's newly released high-end RTX Pro 5500 graphics chip, according to The Information, citing people familiar with the matter; the ministry recently asked some companies to report their purchase plans, including quantities and intended uses, and told some of those firms it intends to approve the purchases.
    - Stored passage: "The Chinese government has signaled it may allow companies such as Alibaba Group Holding Ltd. and ByteDance Ltd to purchase Nvidia Corp.'s new RTX Pro 5500 chips, The Information reported, citing people familiar with the matter. … The Ministry of Industry and Information Technology recently asked some companies to report on their plans to purchase the high-end graphics processor chip, which was released this month, including how many of them and what they would use the product for, the report said, adding that the ministry told some of the firms it intends to approve the purchases."
  - `e419` (article 179; stored attribution: The Information; stored kind: rumour): Chinese officials have indicated to some companies that their purchases of Nvidia's high-end RTX Pro 5500 graphics processors are likely to receive approval, according to The Information, citing people familiar with the matter; the report gives no approval date or quantity.
    - Stored passage: "According to the report, officials have indicated to some companies that the purchases are likely to receive approval."
  - `e430` (article 184; stored attribution: China Ministry of Industry and Information Technology; stored kind: rumour): China's Ministry of Industry and Information Technology asked Alibaba and ByteDance to report how many Nvidia RTX Pro 5500 workstation GPUs they want to buy and how the chips would be used, signaling it may approve the transactions, according to The Information; officials told some companies purchases could be greenlit, but timing, volume limits and exact conditions remain unclear. The article notes the decisions have not been confirmed by the companies or ministries involved.
    - Stored passage: "The Ministry of Industry and Information Technology has asked Alibaba Group Holding Limited (BABA) and ByteDance Limited to report how many RTX Pro 5500 units they want to buy and how the chips would be used, signaling that it may approve the transactions, according to The Information. Officials have told some companies that purchases could be greenlit, though the timing, volume limits and exact conditions remain unclear."
  - `e431` (article 184; stored attribution: ByteDance; stored kind: rumour): ByteDance is considering an order of roughly 1 million Nvidia RTX Pro 5500 chips to support its AI model operations, according to the report cited by the article; no order has been placed or confirmed.
    - Stored passage: "ByteDance is considering an order of roughly 1 million RTX Pro 5500 chips to support AI model operations, according to the report."
  - `e432` (article 184; stored attribution: Nvidia; stored kind: rumour): Nvidia aims to begin RTX Pro 5500 shipments in late December and supply around 500,000 units per quarter to China, a plan reported by the article via The Information rather than in an Nvidia disclosure; at that rate a single ByteDance order of roughly 1 million units would absorb about two quarters of planned China output.
    - Stored passage: "Nvidia aims to begin shipments in late December and supply around 500,000 units per quarter to China, meaning a single ByteDance order could absorb approximately two quarters of planned output."
  - `e405` (article 175; stored attribution: NVIDIA Corp; stored kind: fact): Nvidia's RTX Pro 5500, released earlier this month, is a Blackwell-generation professional workstation GPU that, while capable of heavy AI computing, sits outside the AI accelerator chip category the U.S. has largely blocked from sale to China.
    - Stored passage: "The RTX Pro 5500 is a Blackwell-generation professional workstation GPU released by Nvidia earlier this month. The chip, while capable of heavy AI computing tasks, still sits outside the AI accelerator category of chips the U.S. has largely blocked from being sold to China."
  - `e434` (article 184; stored attribution: Industry executives (unidentified); stored kind: third_party_view): Industry executives believe the RTX Pro 5500, because it sits outside the data-center accelerator category that has been the primary target of U.S. export controls since October 2022, may not be subject to the same restrictions that barred Nvidia's most advanced AI processors from China; the article notes Washington has not said whether the card may be shipped to China at all and that the exclusion is the executives' reading, not a published position of the Commerce Department's Bureau of Industry and Security.
    - Stored passage: "Because the chip sits outside the data-center accelerator category that has been the primary target of U.S. export controls since October 2022, industry executives believe it may not be subject to the same restrictions that have barred Nvidia's most advanced AI processors from reaching Chinese customers. … Beijing is not the only government with a say, and Washington has not said whether the RTX Pro 5500 may be shipped to China at all. The card's exclusion from the data-center accelerator category is the reading of industry executives rather than a published position from the Commerce Department's Bureau of Industry and Security, which administers the controls."
  - `e437` (article 184; stored attribution: Chinese regulators; stored kind: fact): Chinese regulators have pushed buyers toward domestic silicon, restricting H200 use to model training and steering routine inference to Huawei's Ascend line, according to the article.
    - Stored passage: "Chinese regulators have pushed buyers toward domestic silicon, restricting H200 use to model training and steering routine inference to Huawei's Ascend line."
  - `e438` (article 184; stored attribution: Huawei; stored kind: fact): Huawei's Ascend 950PR entered commercial shipment in March 2026, and Huawei has targeted output of up to 750,000 Ascend units this year, per the article.
    - Stored passage: "The Ascend 950PR entered commercial shipment in March 2026, and Huawei has targeted output of up to 750,000 Ascend units this year."
  - `e439` (article 184; stored attribution: ; stored kind: rumour): One proposal under discussion among Chinese authorities would require each imported chip purchase to be bundled with a set ratio of Chinese-made chips, according to the article.
    - Stored passage: "One proposal under discussion would require each imported chip purchase to be bundled with a set ratio of Chinese-made chips."
  - `e440` (article 184; stored attribution: Huawei (Xu Zhijun, rotating chairman); stored kind: party_statement): Huawei rotating chairman Xu Zhijun said at the Huawei Connect 2026 event in Shanghai that Huawei's AI computing product production capacity cannot even meet all domestic demand in China.
    - Stored passage: "Huawei's rotating chairman, Xu Zhijun, said at the Huawei Connect 2026 event in Shanghai that the company's AI computing product production capacity cannot even meet all domestic demand in China."
  - `e441` (article 184; stored attribution: ByteDance (Volcano Engine); stored kind: fact): ByteDance's cloud unit Volcano Engine said in June that daily token usage for its self-developed "Doubao" AI model exceeded 180 trillion, a more than tenfold increase from a year earlier.
    - Stored passage: "ByteDance's cloud unit, Volcano Engine, said in June that daily token usage for its self-developed "Doubao" AI model exceeded 180 trillion, a more than tenfold increase from a year earlier."
  - `e520` (article 217; stored attribution: Alibaba Group Holding Limited; stored kind: fact): Alibaba unveiled its own AI accelerator this month, which it presents as running roughly three times faster than the chip it replaced; the article adds that several Chinese firms are now shipping silicon they did not have two years ago as they design around Nvidia.
    - Stored passage: "That policy has produced results. Alibaba unveiled its own accelerator this month, running roughly three times faster than the chip it replaced. Chinese firms have been designing around Nvidia rather than waiting for export rules to loosen, and several are now shipping silicon they did not have two years ago."
  - `e566` (article 235; stored attribution: Chinese regulators; stored kind: fact): Chinese regulators mostly blocked imports of Nvidia's H200 processors even after the Trump administration approved the exports, the article reports, illustrating that Nvidia's China sales depend on decisions by both governments. No date is given.
    - Stored passage: "Chinese regulators mostly blocked H200 imports even after the Trump administration approved exports."


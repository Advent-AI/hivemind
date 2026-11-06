# Source-only reader A: model-authored diagnostic map

This is a **source-only diagnostic map**, not gold and not a grade. It identifies statements that may help answer the questions supplied with each article; it does not decide the final answer to those questions.

For example, the July 6 financing article reports a six-year NVIDIA backstop for SharonAI. That is relevant to **v1**, but the article alone does not establish every part of v1’s test—particularly whether a publicly verifiable **binding** commitment is under the named partnership.

**Disclosure:** I did not open model-answer files or previous POC result files. While following the repository’s instruction to read the phase PRD, its checklist and surrounding text exposed summaries of earlier POC results. I have not used those results to make this map.

### How to read the map

- **Kept** means I judge the statement relevant under the signed standard and D369/D371. It does not mean the statement is verified or that it settles the question.
- **Optional** means the standard expressly allows omission, such as a clearly repeated past actual figure.
- **Excluded** means the statement is product detail, general background, a repeat, or lacks a sufficiently clear connection to an existing question.
- **Uncertain** means the connection or the treatment under the cited rules needs a human decision. It does not mean the source is false.
- Multiple question IDs show **possible relevance**, not a decision to file one statement under every ID. The production rule still calls for the narrowest appropriate home.
- Dates below are publication dates unless a different event or reporting period is stated. An original statement date is **unknown** unless the article gives it.
- I have not compared these articles with the frozen gold. Therefore I cannot establish whether an individual gold entry conflicts with this map. **If a gold entry conflicts with the signed standard or D369/D371, STOP and resolve it with Alex; do not silently change the gold or invent a rule.** D371 expressly changes treatment for a separately versioned evaluation while leaving the historical standard and gold frozen.

The questions are those in [source-only-inputs.json](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/source-only-inputs.json). The August articles each have 69 questions; the July 6 financing article has v1–v8; the remaining July articles have v1–v10. The question wording for a given ID is the same across these snapshots.

## 1. Microsoft cloud growth and HUMAIN partnership

**Article:** `gnews:d144b91986c520ea36e718cf` · August 29, 2026 · question snapshot 1228.

| Exact short quote | Question and assessment | Timing, attribution and limits |
|---|---|---|
| “Azure and other cloud services revenue increased 43% year-over-year” | **v4, v5, v10 — optional / uncertain.** Strong customer cloud demand can support future infrastructure spending and thus NVIDIA data-center demand. The inference is indirect. | Microsoft FY2026 Q4, ended June 30; presented as a recent analysis of published results. It is a repeated past actual; optional under the old restatement boundary. It does not measure Microsoft’s NVIDIA purchases. |
| “a commercial backlog that reached $678 billion” | **v4, v5, v10 — optional / uncertain.** Cloud commitments can indicate future demand and potential infrastructure requirements. | Reported alongside the ended quarter; backlog is not all AI, data-center capex, or NVIDIA orders. Its status as a restated past actual and its indirectness make the placement uncertain. |
| “Azure growth is anticipated to be about 45% in constant currency” | **v4, v5, v10 — kept.** Forward cloud growth supports a possible need for capacity and NVIDIA products. | Management guidance, FY2027 Q1. It is a forecast, not an expenditure or hardware order. |
| “did not materially raise its data center spending guidance for the year” | **v4 — kept.** Directly bears on one member’s spending outlook and therefore the four-company total. | Article’s description of guidance after fiscal Q4. The amount and exact calendar-versus-fiscal scope are not supplied; unchanged guidance is not zero spending. |
| “a newly announced multi-year AI partnership with HUMAIN” | **v10, v4, v5 — uncertain.** New AI deployments could require cloud capacity and, indirectly, NVIDIA equipment. | Announced August 27; Azure Foundry and Microsoft 365 Copilot for Arabic-language models. No NVIDIA hardware, project size, deployment date, or capex is specified. D369 allows an unquantified logical connection but does not make a specific NVIDIA sale a fact. |
| “management projects revenue in a range of $89.85 billion to $90.95 billion” | **v4, v10 — uncertain.** It describes the customer’s overall financial outlook, but the causal link to data-center spending or NVIDIA demand is weaker than the Azure-specific guidance. | Microsoft FY2027 Q1 guidance, all-company revenue; not an NVIDIA figure. |
| “Microsoft stock traded at $515.30” | **Excluded.** Microsoft’s share price does not answer the listed NVIDIA or hyperscaler-spending questions. | Article reports an August 29 intraday quote. |
| “Microsoft 365 Copilot uses large language models” | **Excluded.** Existing product description; no new deployment or quantified business action. | Background, not evidence of an NVIDIA purchase. |

The article repeats several of these figures and the HUMAIN announcement. Repetition does not create additional statements. The article’s claim that Copilot contributed to segment growth is its interpretation; segment growth does not establish Copilot’s individual contribution.

## 2. Wissner-Gross on NVIDIA financing and competition

**Article:** `gnews:8f8a2d115ab834c7026aefd1` · August 29, 2026 · snapshot 1223.

| Exact short quote | Question and assessment | Timing, attribution and limits |
|---|---|---|
| “$96.2 billion in revenue, up 106% year-over-year” | **v2 — kept.** A current quarter informs the FY2027 total under D371. | Latest quarter as reported; published actual, not full-year revenue. |
| “Net income of $59.7 billion” | **v13 — kept.** Current-quarter profit informs the annual profit question. | Latest quarter; the article says net income, so do not substitute operating profit. |
| “A forward guidance of $108 billion” | **v2 — kept.** Management’s next-period revenue outlook informs the FY2027 total. | Article calls it forward guidance but does not state the period in this sentence; do not supply a period from another article as if this one stated it. |
| “roughly 70% sales growth in fiscal 2028” | **v70 — kept.** Directly addresses the growth question. | Article attributes this to NVIDIA management; it also reports Wall Street consensus of 44%. Forecast, not reported FY2028 growth. The article’s standalone graphic lacks a visible value, so the prose is the usable statement. |
| “without supply constraints, growth would exceed 100%” | **v70 — kept.** A conditional upside estimate for the same growth question. | Attributed to management; explicitly conditional on no supply constraints. It is not a forecast that the constraint will disappear. |
| “financing of their customers” | **v2, v10 — kept.** Wissner-Gross’s specific concern is that customer financing may support demand and could expose revenue if funding-dependent demand weakens. | Third-party concern, framed as a question; he explicitly stops short of calling it a wash-trade scheme. The article describes checks of $5–20 billion but does not identify a particular binding obligation under v1. |
| “could involve acquiring Hugging Face” | **v64 — uncertain.** The statement concerns the exact target, but it is Ismail’s speculation about a possible playbook, not a reported negotiation, agreement, or NVIDIA plan. | Third-party conjecture on a podcast; no transaction date or terms. |
| “1.5 to 1.9 times more AI work per watt” | **v10, v2 — excluded as stated.** The claimed Jalapeno comparison sounds relevant to competition, but the article presents a third-party comparison, which §5.3 excludes as product detail. | Reported claims versus GB200/GB300, with additional latency and throughput claims; the article does not establish an independently verified test. |
| “The chip moved from idea to production in months” | **v10, v2 — uncertain.** A competing OpenAI/Broadcom chip reaching production could affect demand for NVIDIA inference hardware. | Article’s assertion, with no exact production date, volume, source, or sales. Keep it separate from the excluded performance comparison. |
| “video generation now represents roughly 70% of all AI token consumption in China” | **Excluded for the supplied questions.** The article does not connect this figure to an NVIDIA-specific sale or to the H200 permission questions. | A report cited by the podcast; not a government permission decision. |
| “SpaceX revenue of $3.5 trillion by 2033” | **Excluded.** A distant SpaceX projection has no clear path to these existing questions. | Musk projection as reported; not NVIDIA revenue. |

## 3. NVIDIA margin and memory costs

**Article:** `gnews:69d682468e018e0065df5180` · August 29, 2026 · snapshot 1210.

| Exact short quote | Question and assessment | Timing, attribution and limits |
|---|---|---|
| “Total revenue reached $96.2 billion” | **v2 — kept.** FY2027 Q2 revenue contributes to the annual total. | Published quarterly actual; 106% year-on-year and 18% sequential growth. |
| “data center segment generated $89 billion” | **v10 — kept.** The quarter contributes to FY2027 data-center revenue. | Published actual, FY2027 Q2. |
| “hyperscale customers contributed $48.7 billion of revenue” | **v10 — kept.** Shows the current customer mix and demand within data-center sales. | FY2027 Q2; up 102% year-on-year. It is NVIDIA revenue, not hyperscaler capex. |
| “revenue of $108 billion, plus or minus 2%” | **v2 — kept.** Next-quarter guidance informs the annual total. | NVIDIA FY2027 Q3 guidance, assuming **no China compute sales**. Do not turn the assumption into a finding that China has refused H200 permission. |
| “gross margin … 74%, plus or minus 50 basis points” | **v6 — kept.** Direct quarterly guidance informs the annual margin. | FY2027 Q3; article says both GAAP and non-GAAP. It is not full-year guidance. |
| “bottom somewhere between 71% and 72% by the fourth quarter” | **v6 — kept.** Management’s expected Q4 low and subsequent FY2028 recovery inform the FY2027 margin trajectory. | Forward-looking and approximate; recovery is expected, not achieved. |
| “commitments for critical components increased from $119 billion last quarter to $279 billion” | **v6, v25 — kept.** CFO says the increase is “primarily related to the procurement of memory”; the article links higher memory costs to gross-margin pressure. | Kress statement as reported; original speaking date not given. Commitment amount is not necessarily cash paid, a single-period expense, or a binding SK Hynix purchase under v29. Operating-margin connection is indirect. |
| “Operating income rose … to $63.7 billion” | **v25 — kept.** Together with Q2 revenue, it provides current-quarter context for operating profitability. | FY2027 Q2; income is not itself a margin and cannot be substituted for the FY2027 annual margin. |
| “net income was $59.7 billion” | **v13 — kept.** Current-quarter profit informs annual profit. | FY2027 Q2 actual; distinct from operating income. |
| “higher commitments … are, by definition, higher realized average selling prices” | **Excluded / unsupported inference.** A larger total commitment can reflect quantity, price, timing, or a mix; the article supplies no calculation proving realized memory prices. | Author’s interpretation, not the CFO’s statement. |
| “Micron is positioned for the kind of print that should reset expectations” | **Excluded.** General investment opinion about Micron; no listed Micron question. | Author’s forecast without a specific quantified NVIDIA effect. |

## 4. Early DLSS 5 experience

**Article:** `gnews:6dcaad557a1b21d7b867fe34` · August 29, 2026 · snapshot 1214.

| Exact short quote | Question and assessment | Timing, attribution and limits |
|---|---|---|
| “isn't due for an official release until sometime later this year” | **v22 — kept.** The stated planned release window directly bears on whether DLSS 5 launches by December 31. | Author’s description; no precise date or named source. It is a plan or expectation, not an official launch. |
| “an unfinished version that slipped out with NBA 2K27” | **v22 — kept.** An early accidental availability is relevant progress, but it does **not** establish the official launch asked by v22. | Reported by the author; the RenoDX community made it work with games. No precise date is given. |
| “there will be tools that give developers control over intensity, color grading, and masking” | **v22 — uncertain.** NVIDIA’s stated developer tools may describe work remaining or the planned release, but no launch date or dependency is established. | Attributed to NVIDIA; original statement date unknown. |
| “dropped from about 170FPS … to around 115FPS” | **Excluded.** This is an individual game benchmark, not evidence of a release date or business scale. | Author’s test on an RTX 5070 Ti in Cyberpunk 2077; unfinished build, frame generation on. |
| “True DLSS 5 will probably be restricted to 50-series GPUs” | **Excluded.** The author’s product-compatibility speculation does not establish launch timing. | Prediction, not NVIDIA confirmation. |
| “DLSS 5 is the future” | **Excluded.** General opinion and product description. | No additional concrete launch information. |

## 5. GPU debt backstops and AI financing

**Article:** `gnews:085b1e1a1543437edb9756d6` · July 6, 2026 · snapshot 54; only **v1–v8** exist in this input.

| Exact short quote | Question and assessment | Timing, attribution and limits |
|---|---|---|
| “Nvidia has stepped in and has started backstopping GPU rental offtakes” | **v1 — kept.** Direct evidence that NVIDIA is reported to be offering the type of support the question asks about. | SemiAnalysis report, as of mid-2026. It describes take-or-pay minimum revenue and revenue sharing; the article does not by itself establish the named partnership’s legal identity or a particular publicly verifiable binding commitment. |
| “typically six years in length” | **v1 — kept, with the preceding statement.** Describes the reported program’s duration and NVIDIA’s readiness to purchase compute at pre-agreed prices. | SemiAnalysis description; terms are expected to be negotiated individually. Illustrative pricing is not a signed contract. |
| “SharonAI’s 72MW AI factory in Australia” | **v1 — kept.** A named project with a reported six-year NVIDIA backstop is directly relevant. | Announced June 2026; up to 40,000 GB300s. Sharon disclosed a **$4.88 billion total backstop value**. Preserve “up to,” the six-year period and disclosed attribution; do not claim all GPUs are already deployed or the contract’s legal status is independently verified here. |
| “Firmus’s 360MW AI Cluster in Batam, Indonesia” | **v1 — kept.** Another announced project with an NVIDIA backstop supports the possibility of the event. | Announced June 29, 2026, according to the article. Firmus expects $25–30 billion in customer revenue over six years; that is **not** stated as NVIDIA’s guarantee amount. |
| “Many Neoclouds are already deep in negotiations with Nvidia” | **v1 — kept.** Reported negotiations are relevant forward evidence. | SemiAnalysis claim; unnamed counterparties, no dates or binding outcome. |
| “it has started backstopping datacenter leases” | **v1 — uncertain.** A lease backstop demonstrates similar financial support, but v1 specifically asks about the named compute partnership and financial guarantees or unsold-capacity purchases. | Article’s assertion; no project or amount in this sentence. Do not automatically count it as a qualifying v1 commitment. |
| “general market is still materially lower on shipment volumes and revenue estimates for Nvidia” | **v2 — kept.** SemiAnalysis says its supply-chain tracking implies higher NVIDIA shipments and revenue than market estimates for the second half of 2026. | Third-party comparison; neither its estimate nor the market figure is quantified in the article. Calendar half-year is not the whole FY2027. |
| “Annual AI Capex … will be well north of $2T in 2028” | **v5 — uncertain.** A broader infrastructure forecast could inform the demand environment but is not the four named hyperscalers’ **2027 data-center** capex. | SemiAnalysis forecast includes GPUs, networking, storage, CPUs and data centers across a broader population and a different year. Do not present it as v5’s answer. |
| “revenue above the backstop level will be shared with Nvidia” | **v1 — kept as program terms; v2 — uncertain.** Potential incremental revenue exists if such agreements are executed and revenue exceeds the floor. | General program description; Firmus revenue sharing is the author’s expectation, not confirmed contract terms. |
| “at an average of $2.36 over the six-year period” | **Excluded as an actual obligation.** The article explicitly calls this an illustrative lower-end pricing curve. | Scenario assumption; not a disclosed signed price or guarantee. |
| “AI Debt Financing … over $7T of debt outstanding by 2029” | **Excluded for the supplied questions.** Broad market forecast, different population and year; no clear quantified connection to v1–v8. | SemiAnalysis forecast, not incurred debt. |

## 6. NVIDIA as the “black sheep” of the chip rally

**Article:** `gnews:3df0bbc8aff2c1d008bc0a32` · July 6, 2026 · snapshot 62.

| Exact short quote | Question and assessment | Timing, attribution and limits |
|---|---|---|
| “Revenue rose 85% year over year to $81.6 billion” | **v2 — optional.** A quarter contributes to the FY2027 revenue question, but the article is revisiting a previously reported actual. | Quarter not named in this sentence; article’s timing and wording indicate a repeated result. D371 makes current financial context relevant; the older standard makes clearly restated past actuals optional. See the boundary note below. |
| “data center up 92% to $75.2 billion” | **v10 — optional.** Same quarter’s data-center actual informs the annual figure. | Repeated historical actual; not the full year. |
| “Broadcom guided Q3 AI semiconductor revenue to $16.0 billion” | **v10, v2 — kept.** A large competing AI semiconductor business serving hyperscalers can affect NVIDIA’s share of their spending. | Broadcom guidance, Q3, more than 200% year-on-year according to the article. The figure includes AI semiconductors; it is not wholly a measure of custom chips displacing NVIDIA. |
| “AMD’s Meta Instinct GPU deal” | **v10, v2 — kept.** A named customer adopting a competing GPU may divert some AI infrastructure demand from NVIDIA. | Article describes a multi-year deal but gives no deal amount or date. Do not infer the amount displaced. |
| “leading customer forecasts exceeding our initial expectations” | **v10, v2 — uncertain.** AMD CEO’s reported MI450 customer forecasts may indicate competitive demand. | Lisa Su statement; date, unit quantities and customer identities are not given. A forecast is not shipments. |
| “reports of delays across their upcoming lineup of Vera Rubin server systems” | **v8 — uncertain.** A reported delay could affect the Rubin Ultra launch, but this sentence does not identify Rubin Ultra or its revised date. | Unspecified reports; do not turn a broad lineup claim into proof that v8 misses its deadline. |
| “Some estimates put half of all data center spend going toward memory in 2027” | **v5, v6 — uncertain.** A larger memory share might affect both the composition of spending and NVIDIA input costs, but the estimate’s source, denominator and scope are unspecified. | Anonymous estimates, calendar 2027; not necessarily the four hyperscalers’ data-center capex or NVIDIA’s actual cost. |
| “forward P/E of less than 20” | **Optional in general; unrelated to these question answers.** It describes NVIDIA valuation, not annual revenue or margin. | Article’s valuation measure; not a forecast of the underlying metric. |
| “AMD … up 171.25% year to date” | **Excluded.** A competitor’s share-price movement does not establish its sales or displacement of NVIDIA. | Market performance, not operating evidence. |
| “Micron … Q3 revenue … $41.46 billion” | **Uncertain / excluded for these questions.** Memory demand is relevant in principle, but the article does not quantify how this sales figure affects NVIDIA’s margins or named hyperscaler spending. | Micron actual as reported. Preserve the reported number without treating it as independently verified. |

**Boundary:** D371 says present financial performance should be tracked and a quarter is not excluded merely because an annual question is open. The signed standard separately makes **clearly restated past actuals optional**. I have marked the July recap optional rather than silently erase that distinction. If the intended new evaluation treats even clearly repeated past actuals as mandatory, **STOP**: that treatment needs an explicit decision or correction and separate evaluation version.

## 7. Customers seeking alternatives to NVIDIA prices

**Article:** `gnews:4d1b1ca014068fb532f116b3` · July 6, 2026 · snapshot 64.

| Exact short quote | Question and assessment | Timing, attribution and limits |
|---|---|---|
| “Q1 FY27 revenue came in at $81.61 billion” | **v2 — optional.** Quarterly actual informs annual revenue, subject to the restatement boundary described above. | Published Q1 FY2027 actual, repeated in this July article. |
| “data center revenue of $75.25 billion” | **v10 — optional.** Quarterly segment actual informs FY2027 data-center revenue. | Same reported Q1; not a full-year number. |
| “guided Q2 FY27 revenue to $91.0 billion” | **v2 — kept.** Still-relevant guidance for the next quarter informs the annual total. | Management guidance as reported; not realized revenue. |
| “non-GAAP gross margin holding at 75%” | **v6 — kept.** Q2 guidance informs the annual margin. | Non-GAAP; preserve the basis and quarter. |
| “Networking revenue grew 199% year over year to $14.8 billion” | **v10 — optional.** A reported component of current data-center sales. | Quarterly actual as presented; snapshot has no separate networking question. Not all networking revenue should be treated as GPU sales. |
| “Amazon has disclosed Trainium is now a multi-billion-dollar business” | **v10, v2 — kept.** A named hyperscaler’s alternative chip business can compete for AI-compute spending. | Amazon disclosure as reported; no exact date or amount and no quantified NVIDIA displacement. |
| “Amazon, Google, Microsoft, and Meta are all building proprietary silicon” | **v10, v2 — uncertain.** Relevant competitive direction, but the article does not date the actions or establish new commitments beyond the Trainium disclosure. | Existing arrangements may be background; do not infer new orders or specific lost NVIDIA revenue. |
| “China data center compute revenue is effectively zero” | **v10, v2 — kept.** Current absence of that revenue affects the sales outlook. | Article’s description, not a quantified fiscal-period actual. It does not establish a Chinese decision on H200 under v3. |
| “losing that market … would be material” | **v10, v2 — kept.** Kress’s reported view and NVIDIA’s future market estimate of close to $50 billion explain the potential revenue exposure. | Conditional loss; “future” period is not specified. The market estimate is not NVIDIA’s forecast revenue. |
| “Supply commitments of $119 billion” | **v6 — uncertain.** Supply commitments could affect cost exposure if demand slows, but the article does not identify the composition, unit prices, or margin impact. | Reported amount; not proof of an SK Hynix binding commitment. |
| “NVIDIA trades at $196 against an analyst consensus target” | **Optional valuation / excluded from question evidence.** It does not answer the supplied operating questions. | Market quote and target, not an operating forecast. |

## 8. Kyber delay reported by SemiAnalysis

**Article:** `gnews:795ea94e1100415a67fd1a96` · July 6, 2026 · snapshot 68.

| Exact short quote | Question and assessment | Timing, attribution and limits |
|---|---|---|
| “pushed back more than twelve months to 2028” | **v8, v9 — kept.** A reported Kyber NVL144 delay bears directly on Rubin Ultra’s 2027 rack launch and Kyber’s 2028 release. | SemiAnalysis report on X; attributed to manufacturing problems with the PCB midplane. A 2028 target is not proof of either launch or failure. |
| “NVL72x2 … has been scrapped entirely” | **v8 — kept.** Loss of the alternative rack affects the available path for the Rubin Ultra generation. | SemiAnalysis report; cloud and data-center customers reportedly objected to form factor and operating overhead. |
| “four compute dies has also been canceled” | **v8 — kept.** A reported change to the main product configuration affects what the generation can ship. | SemiAnalysis report; article says the two-die version remains and estimates roughly half the real-world compute performance. Do not convert this into a confirmed launch cancellation. |
| “CPO-NVSwitch … won't arrive until … Feynman” | **v8, v9 — kept.** A reported delay in a critical interconnect affects the ability to scale the rack. | SemiAnalysis report; Feynman timing is not specified. |
| “plans to make up for the shortfall by selling more Oberon-Rubin racks” | **v8, v10 — kept.** A reported alternative affects the product transition and possible sales mix. | Article’s description of NVIDIA’s plan; no quantity, timing or company confirmation is provided. |
| “could give competitors like AMD's MI500X … room to move in” | **Excluded as a separate statement.** This is commentary on the already-described delay, without an additional competitor action or estimate. | The delay itself remains kept. |
| “Ibiden … dropped as much as ten percent” | **Excluded.** Supplier stock-price reaction is not proof of NVIDIA’s launch timing. | Market reaction to the report. |

## 9. Kyber delay report, with NVIDIA response

**Article:** `gnews:c75f16a6d64cc27fc28fb571` · July 6, 2026 · snapshot 74.

| Exact short quote | Question and assessment | Timing, attribution and limits |
|---|---|---|
| “won't ship its Kyber NVL144 rack until 2028” | **v8, v9 — kept.** The reported shipping delay bears on both launch questions. | SemiAnalysis thread as reported; over 12 months beyond the intended 2027 Rubin Ultra phase. |
| “Our roadmap is intact.” | **v8, v9 — kept as counterevidence.** NVIDIA’s response may challenge the reported delay. | NVIDIA representative, article update July 6 at 4:10 p.m. PT. The article says it is unclear whether “roadmap” means the original schedule and hardware or an already revised plan. Do not resolve that ambiguity. |
| “abandoned the stopgap after its largest customers balked” | **v8 — kept.** Reported cancellation of NVL72x2 removes a potential 2027 alternative. | SemiAnalysis attribution; customers objected to operating two linked cabinets as one. |
| “NVL576 … is likely to slip too or ship in low volume” | **v8, v9 — kept.** A possible delay or constrained volume in another scale-up configuration affects the rack transition. | Forecast, not a confirmed cancellation; tied to optical technology maturity. |
| “dropped the quad-chiplet Rubin Ultra GPU for a dual-chiplet part” | **v8 — kept.** A reported product configuration change affects the generation’s intended offering. | Article reports the change occurred the previous week because of manufacturing execution concerns; exact original date and confirmation are not given. |
| “2026 Rubin GPUs … aren't part of the reported delay” | **v8 — kept as a qualification.** The reported setback is specifically the Ultra/Kyber phase, not all Rubin products. | Article’s distinction; does not prove the earlier Rubin shipment question in this snapshot, which has no v20/v21. |
| “three 26-layer sections laminated into one 78-layer stack” | **Excluded.** Engineering detail explains the mechanism but is not itself a separate investment-scale event or launch date. | Third-party board analysis. |
| “the largest single Rubin Ultra domain in 2027 could match, but not exceed, what Oberon already delivers” | **v8 — kept.** The reported consequence describes a specific limit on the 2027 product configuration. | Conditional inference from the reported cancellations and lack of a proven alternative, not a confirmed final specification. |

Articles 8 and 9 report the same underlying SemiAnalysis claims. They should not be treated as independent confirmation merely because two outlets repeat them. Article 9 adds NVIDIA’s response, which must remain alongside the report.

## 10. Micron and AI infrastructure spending

**Article:** `gnews:d0f3f83296df884fae64921e` · July 7, 2026 · snapshot 89.

| Exact short quote | Question and assessment | Timing, attribution and limits |
|---|---|---|
| “AI hyperscalers plan to spend $650 billion on data center capital expenditures this year” | **v4 — kept.** Directly relevant to 2026 hyperscaler data-center spending. | Article’s statement; no original source or list of companies is given. Do not assume the total is exactly the four companies in v4. “Plan” is not incurred spending. |
| “next year that figure could be over $1 trillion” | **v5 — kept.** Forward estimate directly bears on 2027 hyperscaler spending. | Article’s conditional estimate; same population and sourcing limitations. It is not a firm plan or completed expenditure. |
| “tight market conditions could last until 2028” | **v6 — kept.** Memory supply tightness could raise NVIDIA input costs and affect gross margin. | Article attributes the outlook to Micron’s recent announcement, but does not give the original statement date or a price forecast. The margin effect is an inference. |
| “new capacity for many in this industry won't be online until 2027 or later” | **v6 — kept.** Supply timing supports the risk that memory remains costly during FY2027. | Author’s industry assertion; unspecified producers and capacities. Not a guarantee of a shortage or specific margin. |
| “Next quarter, it expects $50 billion in revenue” | **v6 — uncertain.** Micron’s outlook may indicate memory demand, but the article does not translate that revenue estimate into NVIDIA’s cost or purchase volume. | Micron guidance as reported; not NVIDIA revenue. The unusually large figure is preserved as printed and has not been verified. |
| “Micron's stock could be valued at $6.2 trillion” | **Excluded.** A conditional valuation of another company does not answer the supplied NVIDIA operating questions. | Author’s scenario depends on EPS and a 25× multiple; it is not a company forecast or transaction. |
| “DRAM is used for high-speed memory, as needed by Nvidia's GPUs” | **Excluded as background.** It explains the supply link but is not itself a new market or business development. | General technical description. |

The signed standard and decisions used are [extraction standard §§5.1–5.5](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/prd/05-extraction-standard.html) and [D369/D371](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/DECISIONS-log.md:3990). No files were edited and no paid calls were made.

# Making SEC XBRL financial data accurate and comparable with code: concept normalization, extensions, segments, data quality (state as of Oct 2026)

Notes for the report writer. Two kinds of evidence are used: (1) published sources, each cited inline; (2) my own $0 measurements on stored SEC data downloaded in this session, labelled **[own measurement]**. The measurements ran on the SEC Financial Statement Data Sets for 2026q3 ([SEC FSDS](https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets); 5,607 10-K/10-Q filings filed Jul–Sep 2026, 3.39M facts) and on the SEC companyfacts JSON for AAPL, MSFT, AMZN, NVDA, TSLA, META and GOOGL ([companyfacts API](https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json)). The script (`measure_fsds.py`, output `measure_out.txt`) ran in the research session's temporary scratchpad and is not kept in this repository. One scope fact about FSDS matters for every number below. I checked it: 100% of FSDS `num.txt` facts in 10-K/10-Q filings use a tag that also appears in that filing's primary-statement presentation rows. So FSDS covers **concepts shown on the face statements**, including their dimensional (segment) facts from the notes, but not concepts that appear only in the notes, such as `SegmentExpenditureAdditionToLongLivedAssets`. FSDS also strips namespace prefixes from axes and drops the "Statement…Axis" wrapper (for example `BusinessSegments=AmericasSegment`), so you cannot tell custom axes from standard ones using that field alone.

---

## Q1. What share of facts and line items in large-company 10-K/10-Qs are extension (custom) elements, and how has this changed?

### Takeaway
Custom line-item tags are a minority but always present. The SEC's own 10-K trend analysis puts them at about 16–22% of a filing's line-item tags (2014–2020), with filer categories flat or slightly falling through 2024. XBRL US says about 19% of concepts each year are extensions. My 2026q3 measurement of face-statement concepts finds a mean of 8.1% of distinct tags (median 6.7%) for large accelerated filers, and 6.2% of facts. Customs cluster in the cash-flow statement (12%) and the equity statement (12%) and are rare on the balance sheet (4%). For mega-caps it is 0.4% (Apple) to 8.5% (Amazon) of face-statement facts. The larger comparability problem is not extensions but **different standard tags for the same thing**, both across companies and across time.

### Cited Findings
- SEC custom-tag rate trend for Forms 10-K (rate = custom line-item tags as a share of line-item tags; abstract, member and domain tags excluded). FY2014→2016 all filers 20%→19%. FY2015→2017 all filers 19%→18%, large accelerated filers (LAF) 19%→18%, non-accelerated 22%→21%. FY2018/2019/2020: LAF 18%/16%/20%, accelerated 18%/18%/20%, non-accelerated 18%/17%/21%, smaller reporting companies 16%/17%/19%. — [SEC, US GAAP XBRL custom tags](https://www.sec.gov/data-research/gaap-xbrl-custom-tags)
- Later SEC analyses state only directions. Fiscal 2021 versus 2020: LAF, accelerated and non-accelerated rates fell, SRCs rose. 2023: LAF and accelerated flat. 2024 versus 2023: rates fell for all filer statuses except LAF, which stayed flat. — [SEC, US GAAP XBRL custom tags](https://www.sec.gov/data-research/gaap-xbrl-custom-tags); [SEC custom tags trend page](https://www.sec.gov/data-research/structured-data/us-gaap-xbrl-custom-tags-trend)
- The SEC trend page now covers fiscal years 2012–2025 for 10-K, split into "financial statements" and "financial statements and notes" (page dated Aug 10, 2026). The numbers are only in charts, not in the page text. — [SEC custom tags trend page](https://www.sec.gov/data-research/structured-data/us-gaap-xbrl-custom-tags-trend)
- The SEC Office of Structured Disclosure list shows trend reports published June 28, 2024 (2021–2023) and June 2, 2025 (2022–2024). — [SEC OSD staff observations, guidance and trends](https://www.sec.gov/page/osdstaffobsandguide)
- XBRL US (Mar 4, 2025): "approximately 19% of concepts across reports annually are non-standard extensions". — [XBRL US, Why normalize data](https://xbrl.us/why-normalize-data/)
- Custom axes (SEC staff, Mar 29, 2016; data 2013–2015): about 50% of filers create one or more custom axis tags in each 10-K. The average exhibit uses 20–25 axis tags out of more than 300 standard axes. The mean custom-axis rate across 29 filing agents was 5.9%, with outliers at 21% and 31%. Smaller companies used custom axes less than half as often as LAFs. Staff found custom axes that duplicated standard ones (for example a custom "type of debt" axis). — [SEC staff observations of custom axis tags](https://www.sec.gov/about/divisions-offices/division-economic-risk-analysis/office-structured-disclosure-staff/staff-observations-custom-axis-tags); earlier 2014 version summarized at [Colonial Filings](https://www.colonialfilings.com/blog/sec-observations-xbrl-segment-tags/)
- The rule on extensions is 17 CFR 232.405(c)(1)(iii)(B): a filer "must create and use a new special element if and only if an appropriate tag does not exist in the standard list of tags for reasons other than or in addition to an inappropriate standard label." — quoted in [Du, Huddart & Jiang, "Lost in Standardization" (Sept 2021 draft)](https://business.columbia.edu/sites/default/files-efs/imce-uploads/CEASA/Events%20Page/revisiting_accounting-based_return_anomalies.pdf)
- Kim & Lee, *International Journal of Accounting Information Systems* vol. 56, article 100742 (Dec 2025). Firms with weak internal controls create more custom tags. Excessive custom-tag use is associated with a higher likelihood of SEC comment letters, and firms cut their custom-tag share after SEC scrutiny. The sample and the definition of "excessive" were not visible in the abstract. — [Nova Southeastern scholars page](https://scholars.nova.edu/en/publications/excessive-custom-xbrl-tag-usage-in-10-k-filings-and-sec-oversight/); [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1467089525000181)
- Older academic claim (via search snippet of Du, Vasarhelyi & Zheng, *Journal of Information Systems*): "previous research found that 40 percent of all extensions were unnecessary because the corresponding elements existed in the US GAAP taxonomy". This is early-mandate era (about 2009–2011) and I did not verify it in the full text. — [Semantic Scholar entry](https://www.semanticscholar.org/paper/XBRL-Mandate:-Thousands-of-Filing-Errors-and-So-Du-Vasarhelyi/5b5d4ac0dbf2dc57a3ec4e9698812ddded232263)
- Taxonomy size for context: the 2020 US GAAP taxonomy has 643 unique balance-sheet tags, 574 income-statement tags and 766 cash-flow tags, against about 900 data items in Compustat Fundamentals Annual. — [Du, Huddart & Jiang 2021](https://business.columbia.edu/sites/default/files-efs/imce-uploads/CEASA/Events%20Page/revisiting_accounting-based_return_anomalies.pdf). edgartools describes the space as "~18,000 possible SEC GAAP taxonomy tags". secfsdstools says "over 3000 tags which can be used in a balance sheet". — [edgartools docs](https://edgartools.readthedocs.io/en/latest/xbrl/concepts/standardization/); [secfsdstools repo](https://github.com/HansjoergW/sec-fincancial-statement-data-set)
- **[own measurement]** FSDS 2026q3, 10-K+10-Q, face-statement concepts only. Custom share of a filing's distinct non-abstract tags, mean/median: LAF (n=1,966) 8.1%/6.7%; accelerated (n=679) 8.4%/7.4%; non-accelerated (n=2,962) 12.8%/11.2%. Custom share of facts, mean/median: LAF 6.2%/4.8%; accelerated 6.1%/4.9%; non-accelerated 9.6%/7.7%. — [SEC FSDS](https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets)
- **[own measurement]** LAF pooled custom share of (filing, statement, tag) rows: BS 3.9% (3,032/76,980), IS 6.9% (2,973/43,226), CF 12.2% (8,637/70,806), equity statement 11.7% (2,779/23,854), comprehensive income 5.2% (564/10,938). — [SEC FSDS](https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets)
- **[own measurement]** Custom share of face-statement facts in the latest filing of each company: AAPL 10-Q 0.4% (2/450), MSFT 10-K 2.3% (12/517), GOOGL 3.8% (21/558), NVDA 3.9% (15/388), META 4.3% (16/368), AMZN 8.5% (46/541). — [SEC FSDS](https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets)
- **[own measurement]** Even top-line revenue is spread across standard tags. In 1,845 LAF filings, the first revenue-like income-statement line was tagged `RevenueFromContractWithCustomerExcludingAssessedTax` in 1,104 (59.8%), `Revenues` in 401 (21.7%), `RevenueFromContractWithCustomerIncludingAssessedTax` in 150 (8.1%), a custom tag in 69 (3.7%), and industry tags in the rest (for example `OperatingLeaseLeaseIncome` 21, `RegulatedOperatingRevenue` 6, `BrokerageCommissionsRevenue` 8). — [SEC FSDS](https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets)
- **[own measurement]** The same company's total revenue moves between standard concepts over time (companyfacts, USD facts):
  - **Apple:** `SalesRevenueNet` (10-K FY2009–2017), then `Revenues` (FY2018), then `RevenueFromContractWithCustomerExcludingAssessedTax` (FY2019–2025).
  - **Microsoft and Amazon:** `SalesRevenueNet` (through FY2017), then `RevenueFromContractWithCustomerExcludingAssessedTax` (FY2018 on). Amazon also used `SalesRevenueGoodsNet` and `SalesRevenueServicesNet`.
  - **NVIDIA:** `RevenueFromContractWithCustomerExcludingAssessedTax` for FY2019–2022, then back to `Revenues` through 2026.
  - **Alphabet:** both, with `RevenueFromContractWithCustomerExcludingAssessedTax` for periods through 2025-03-31 and `Revenues` for periods through 2026-06-30.

  — [SEC companyfacts API](https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json)
- SEC data-quality reminder (Dec 8, 2022): some filers "use different elements to tag the same reported line item on the income statement from one period to the next", and sometimes use one element in a 10-Q and another in the 10-K. A related reminder followed on Nov 3, 2023, "Changing Labels for the Same Reported Item on the Income Statement over Multiple Periods". — [SEC reminder 2212](https://www.sec.gov/structureddata/announcement/2212-dqreminder-different-tags-same-labels); [SEC OSD list](https://www.sec.gov/page/osdstaffobsandguide)

### Inferences
- "How many extensions" depends on scope: face statements versus notes, 10-K versus 10-Q, tags versus facts. My 8% (face statements, mostly 10-Q, LAF, 2026) and the SEC's 16–20% (10-K, line items, 2014–2020) are not directly comparable. Both say most facts a research system needs are standard tags.
- For an identity key, extensions are the smaller problem. The bigger ones are (a) several standard tags for one economic item across companies and years (Apple revenue: 3 concepts over 17 years), and (b) one concept carrying many distinct facts that differ only by dimension. Apple's `RevenueFromContractWithCustomerExcludingAssessedTax` in one 10-Q holds 1 consolidated value, 5 geographic-segment values and 6 product/service values per period. A key of caption plus row label folds these together or splits them. The facts become unique when the key is (concept QName, full axis=member set, period start/end or instant, unit, entity/co-registrant).
- Labels are not stable either: the SEC flagged label changes for the same item (Nov 2023). So label text is a poor identity for the same reason concept choice alone is.

### Gaps
- I could not get the numeric SEC custom-tag rates for fiscal 2021–2025, which are only in charts, or the separate "financial statements only" versus "statements and notes" values.
- I found no study that measures what share of facts **in notes** are custom, or how often custom **members** (as opposed to axes) are used, for 2024–2026. FSDS cannot answer this: no notes concepts, and axis/member prefixes are stripped. The SEC "Financial Statement and Notes" data sets would; my download of that file was corrupt (not a valid zip).
- Kim & Lee (2025): sample period, the measured custom-tag proportions and the effect sizes were not accessible (paywall).

---

## Q2. How do open-source tools and vendors standardize concepts (hand mappings, calculation linkbase, anchoring), and how good is the result?

### Takeaway
Every working open-source normalizer I found relies mainly on a **hand-curated tag-to-standard-line-item map** (edgartools: 95 standard concepts, about 2,000–2,900 tag mappings). Some add **arithmetic rules** that use the taxonomy's or the filing's calculation relationships (secfsdstools: rename/sum/subtract plus balance checks; Du-Huddart-Jiang: take the highest-level taxonomy tag and impute it from calculation children). Ambiguous tags are resolved from statement context. **Anchoring is not a US requirement.** ESMA requires it under ESEF; US GAAP filers may anchor voluntarily, so it cannot be relied on for SEC filings. Published quality figures are self-reported and thin. The best number is secfsdstools' self-check: 93.7% of balance sheets satisfy Assets = Liabilities + Equity exactly after standardization.

### Cited Findings
- **edgartools** (open-source Python): 95 standard concepts. `gaap_mappings.json` maps 2,900+ XBRL tags to them in the latest docs; the stable docs say 2,067 mappings. `display_names.json` holds the 95 labels. About 206 of the 2,900 tags (~7%) are "ambiguous" and resolved by context (calculation parent, bottom-up section scanning, statement type, `is_total`). About 270 tags are explicitly excluded ("DropThisItem"). The docs claim "~95% coverage of common financial statement tags", "tested on 390+ companies", and credit a contributor's "production taxonomy" (GitHub issue #494). No independent accuracy or failure rate is published, and company extensions are not addressed beyond the ambiguity handling. — [edgartools standardization (latest)](https://edgartools.readthedocs.io/en/latest/xbrl/concepts/standardization/); [edgartools standardization (stable)](https://edgartools.readthedocs.io/en/stable/xbrl/concepts/standardization/); [customizing standardization](https://edgartools.readthedocs.io/en/latest/advanced/customizing-standardization/)
- **secfsdstools** (open-source Python over the SEC Financial Statement Data Sets) has `BalanceSheetStandardizer`, `IncomeStatementStandardizer` and `CashFlowStandardizer`. Rule types are rename, copy, sum-up of children, subtract (for example equity derived from assets minus liabilities) and post-rules, in PRE / MAIN / POST / FINALIZE phases. Rules are user-customizable. A "segments" column has been supported since Dec 2024, and v2.4.0 adds experimental daily updates. — [secfsdstools repo](https://github.com/HansjoergW/sec-fincancial-statement-data-set); [BS standardizer notebook](https://nbviewer.org/github/HansjoergW/sec-fincancial-statement-data-set/blob/main/notebooks/07_01_BS_standardizer.ipynb); [customize notebook](https://nbviewer.org/github/HansjoergW/sec-fincancial-statement-data-set/blob/main/notebooks/07_04_customize_standardizer.ipynb)
- secfsdstools self-validation on 346,570 standardized balance-sheet rows. Share exact ("Category 0"): AssetsCheck (Assets = Current + Noncurrent) 98.47%, LiabilitiesCheck 94.99%, EquityCheck 93.78%, AssetsLiaEquCheck (Assets = Liabilities + Equity) 93.70%. For AssetsCheck, about 0.10% are <1% off, about 0.18% ≤5%, about 0.14% ≤10%, and about 1.11% are >10% off. — [raw notebook](https://raw.githubusercontent.com/HansjoergW/sec-fincancial-statement-data-set/main/notebooks/07_01_BS_standardizer.ipynb)
- **Taxonomy calculation hierarchy as the mapping** (academic, deterministic): Du, Huddart & Jiang map each Compustat item to the "highest-level tags in the FASB taxonomy" (for example operating-capital change → `IncreaseDecreaseInOperatingCapital`, `at` → `Assets`, `dpc` → `DepreciationDepletionAndAmortization`). When the parent is missing they impute it from children "using the hierarchical relations specified by the [standard] linkbase", and say this involves no subjective judgment. For custom tags they rebuild the cash-flow statement from each filer's **presentation linkbase**: customs between `IncreaseDecreaseInOperatingCapitalAbstract` and `NetCashProvidedByUsedInOperatingActivities` are treated as accrual components. Otherwise they use the filer's **calculation linkbase** to place a custom tag under a standard parent. On average 7.483 tags go into one firm's accruals. — [Du, Huddart & Jiang 2021](https://business.columbia.edu/sites/default/files-efs/imce-uploads/CEASA/Events%20Page/revisiting_accounting-based_return_anomalies.pdf)
- **XBRL US** publishes a normalized view built with XULE rules on a Standardized Statement Taxonomy (XUSSS) for commercial and industrial companies (BS, IS, CF). It is queryable in XBRL API with `report.source-name=NORM`. XBRL US notes that "working with normalized data uncovers outliers" (Mar 2025). — [XBRL US, Why normalize data](https://xbrl.us/why-normalize-data/)
- **Calcbench** (vendor) standardizes "+1000 metrics to handle differences in filers' tagging" from 10-K/Q face statements, footnotes, press releases and 8-Ks. It offers point-in-time mode with a record per revising filing. The mapping method is not public. — [Calcbench API docs](http://calcbench.github.io/python_api_client/html/numeric-data.html)
- **Intrinio** (vendor, Jan 2017 blog) says it maps all XBRL data to a standard syntax, corrects revenue-tag mismatches from extensions, cash-flow sign (debit/credit) errors and tag changes across periods, and validates that line items sum to parents. It publishes no accuracy figures. — [Intrinio blog](https://intrinio.com/blog/normalized-xbrl-data)
- **Anchoring**: ESMA's ESEF requires extensions to be anchored to a wider or narrower base-taxonomy element, for face statements only. — [XBRL International, anchoring](https://www.xbrl.org/enhancing-comparability-with-anchoring/). For US GAAP, the April 2020 XBRL US DQC meeting notes say filers are "not prohibited" from anchoring links. FASB staff were reviewing which extensions are anchoring candidates and discussing possible EDGAR Filer Manual changes with the SEC. — [DQC meeting notes, Apr 2020](https://xbrl.us/wp-content/uploads/2020/02/DQCMeetingNotes040120.pdf)
- **Fundamental Accounting Concepts** (Charles Hoffman): rule sets checking that filings keep basic accounting relationships, used to grade filing agents. In July 2015, 84% of DataTracks-produced filings conformed versus a 70% industry average. DataTracks and RR Donnelley averaged fewer than 0.2 FAC errors per filing. These are vendor-published and dated. — [DataTracks news](https://datatracks.com/us/news/datatracks-adjudged-no-1-in-quality-for-xbrl-filings/); [DataTracks blog](https://www.datatracks.com/blog/perfect-xbrl-a-never-ending-journey)
- **SEC's own free APIs**: companyfacts fact records carry only `accn, end, filed, form, fp, frame, fy, start, val`. There is no dimension field, and only standard namespaces appear (for example Apple: `dei` and `us-gaap` only; NVIDIA: `dei`, `invest`, `us-gaap`, `srt`, `ecd`, `ffd`). Segment/dimensional facts and company-extension facts are therefore **absent** from companyfacts and frames. — **[own measurement]** on [companyfacts JSON](https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json)
- **[own measurement]** Pitfall in companyfacts: `fy` and `fp` describe the **filing**, not the fact's period. Apple's `Revenues` facts tagged 10-K "fy 2018" have period ends from 2016-09-24 to 2018-09-29, which are prior-year comparatives in the same filing. — [companyfacts JSON](https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json)

### Inferences
- How much hand mapping a research system needs: a curated map from about 2–3k standard tags to about 100 standard line items covers face statements for most filers. Every open-source tool converges on this, and it can be seeded from edgartools' published JSON. Industry tags (banks, insurers, REITs, utilities) need their own blocks. Revenue alone hits 15+ tags in LAF filings in my 2026q3 sample.
- What code can decide instead of a hand map: (1) taxonomy calculation parents, to roll children up or impute a missing total; (2) the **filer's own calculation and presentation linkbases**, to place each custom tag under its standard parent. That covers the ~4–12% custom share without a per-company map. A mapping that falls back to label text recreates the collisions the old system had.
- Use the deprecation relationships the FASB ships, which map deprecated concepts to replacements (see Q4), to join time series across concept changes such as `SalesRevenueNet` → `RevenueFromContractWithCustomerExcludingAssessedTax`. This is a code-held mapping, not a hand one.
- For segments, companyfacts/frames is not usable (no dimensions). Use FSDS (face-statement concepts with dimensions), the Financial Statement and Notes data sets, or the raw inline-XBRL instance.

### Gaps
- No independent, published accuracy measurement of edgartools, secfsdstools, OpenBB or FinGPT/FinRL pipelines against a known truth set. OpenBB and FinGPT/FinRL appear to consume provider APIs (FMP, SEC) rather than normalize XBRL themselves, but I found no primary source documenting this, so treat it as unverified.
- Calcbench, FMP, sec-api.io and Fiscal.ai do not publish their mapping methods or error rates in material I could reach.
- I could not confirm whether the SEC or FASB adopted any US anchoring requirement after 2020. I found none, and US GAAP extensions are generally treated as not requiring anchors.

---

## Q3. How is segment and disaggregation data tagged (incl. ASU 2023-07 and ASU 2023-09), and how hard is it to rebuild, e.g., "segment operating income by geography"?

### Takeaway
Segment facts are standard line-item concepts (`Revenues`, `OperatingIncomeLoss`, `CostOfRevenue`, and so on) qualified by `us-gaap:StatementBusinessSegmentsAxis`, optionally together with `srt:ConsolidationItemsAxis` (OperatingSegments / CorporateNonSegment / IntersegmentElimination / reconciling items). Products use `srt:ProductOrServiceAxis` and geography uses `srt:StatementGeographicalAxis`. Segment members are almost always company extensions. ASU 2023-07 added `SegmentReportingOtherItemAmount`, its composition description, `SegmentExpenditureAdditionToLongLivedAssets` and a CODM title element. Significant segment expenses are tagged with ordinary expense elements, or with extension line items where none fits; the FASB's own example uses extensions. Two models coexist (one-axis and two-axis), so code must accept both. "Operating income by geography" mostly **does not exist** in filings: ASC 280 requires geography only for revenue and long-lived assets. Segment profit by geography exists only where segments are geographic (Apple).

### Cited Findings
- ASU 2023-07 requires annual and interim disclosure of significant segment expenses regularly provided to the CODM and included in each reported measure of segment profit or loss. It also requires "other segment items" by segment with a description of their composition, and the CODM's title and position. It is effective for fiscal years beginning after Dec 15, 2023 and interim periods in fiscal years beginning after Dec 15, 2024. — [FASB ASU 2023-07](https://storage.fasb.org/ASU%202023-07.pdf); [Deloitte Heads Up](https://dart.deloitte.com/USDART/home/publications/deloitte/heads-up/2023/fasb-asu-reportable-segment-disclosures); [KPMG handbook](https://kpmg.com/kpmg-us/content/dam/kpmg/frv/pdf/2024/handbook-segment-reporting-post-asu-2023-07.pdf)
- Taxonomy: elements for ASU 2023-07 and ASU 2023-09 were added in the **2024** GAAP taxonomy. Elements for ASU 2024-03 (income-statement expense disaggregation, DISE) were added in the **2025** taxonomy. — [FASB 2026 GAAP Taxonomy Release Notes](https://xbrl.fasb.org/resources/annualrelease/2026/GAAP_Financial_Reporting_Taxonomy_Release_Notes.pdf)
- FASB proposed Taxonomy Implementation Guide "Segment Reporting (After Adoption of ASU 2023-07)", v1.0 issued Jan 27, 2025 on the 2025 taxonomy, comments due Mar 25, 2025:
  - **Models.** "Segments [Axis]" (`StatementBusinessSegmentsAxis`) alone is used when there are no reconciling items. When there are reconciling items it is a **two-axis model**: `StatementBusinessSegmentsAxis` plus `ConsolidationItemsAxis` with `OperatingSegmentsMember`, `IntersegmentEliminationMember`, `CorporateNonSegmentMember` and reconciling-item members.
  - **Segment members.** They are entity extensions. The standard members are Corporate Segment, Other Operating Segment (`AllOtherSegmentsMember`), Reportable Segment Aggregation before Other Operating Segment, and Corporate plus Other.
  - **Segment profit.** Segment profit is the consolidated profit element named in the reconciliation (for example net income or pretax income) tagged with `OperatingSegmentsMember`.
  - **New elements.** Other items use `SegmentReportingOtherItemAmount` and `SegmentReportingOtherItemCompositionDescription`. Capex uses `SegmentExpenditureAdditionToLongLivedAssets`.
  - **Single-segment entities.** The Segments axis should be applied "regardless of the number of reportable segments". Extensible-enumeration segment names do not apply to Topic 280.
  - **Extensions in the FASB's own example.** Several significant expenses (`ContractorExpense`, `OccupancyAndEquipmentExpense`, `OtherProfessionalServiceExpense`) are coded as **extension** line items, while others use standard elements (`LaborAndRelatedExpense`, `CostOfRevenue`, `ResearchAndDevelopmentExpense`, `ProfessionalFees`).

  — [FASB segment TIG (PDF)](https://xbrl.fasb.org/impguidance/SG1_TIG/segmentreporting.pdf); [SEC notice of proposed TIGs](https://www.sec.gov/newsroom/whats-new/2502-proposed-taxonomy-implementation-guides-accounting-changes-segments)
- CODM element in use: `SegmentReportingCODMIndividualTitleAndPositionOrGroupDescription` (text, for example "Chief Executive Officer" or an "Executive Committee"). — [example filing R74](https://www.sec.gov/Archives/edgar/data/1490349/000121390025120913/R74.htm)
- ASC 280 entity-wide disclosures: revenues from external customers attributed to the country of domicile and to all foreign countries, with material individual countries shown separately, plus long-lived assets by the same split. These follow standard criteria, not the management approach. — [Deloitte Roadmap 5.5](https://dart.deloitte.com/USDART/home/codification/presentation/asc280-10/roadmap-segment-reporting/chapter-5-entity-wide-disclosures/5-5-information-about-geographic-areas)
- ASU 2023-09 (income taxes): prescribed rate-reconciliation categories (state/local, foreign tax effects by jurisdiction, credits, changes in law, and so on), a 5% threshold for separate disclosure, and income taxes paid disaggregated by jurisdiction. It is effective for PBEs for fiscal years beginning after Dec 15, 2024, so the first calendar-year 10-Ks were filed in early 2026. — [Deloitte Heads Up 2025](https://dart.deloitte.com/USDART/home/publications/deloitte/heads-up/2025/income-tax-disclosure-considerations-related-adoption-asu-2023-09); [KPMG Hot Topic](https://kpmg.com/kpmg-us/content/dam/kpmg/frv/pdf/2025/hot-topic-income-tax-discl-asu-2023-09.pdf)
- **[own measurement]** Axis use in 1,966 LAF 10-K/10-Q filings (2026q3, face-statement concepts), as share of filings: EquityComponents 97.5%, BusinessSegments 75.3%, ProductOrService 64.9%, ConsolidationItems 54.2%, Geographical 42.5%, BusinessAcquisition 33.3%, DebtInstrument 32.5%, LongtermDebtType 27.3%. There are 647 distinct axis names across LAF filings. The most common combinations by fact count are BusinessSegments+ConsolidationItems (61,659 facts), BusinessSegments alone (33,377), ConsolidationItems alone (26,288), ProductOrService (22,275), BusinessSegments+ProductOrService (11,268), Geographical (10,986) and BusinessSegments+ConsolidationItems+ProductOrService (9,340). — [SEC FSDS](https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets)
- **[own measurement]** How mega-caps tag segment operating income (`OperatingIncomeLoss`) in their latest 2026 filing:
  - **Two-axis model** (BusinessSegments + ConsolidationItems=OperatingSegments, plus ConsolidationItems=CorporateNonSegment for the reconciling line):
    - Apple: Americas, Europe, Greater China, Japan, Rest of Asia Pacific.
    - Alphabet: Google Services, Google Cloud, AllOtherSegments.
    - NVIDIA: Compute & Networking, Graphics.
  - **BusinessSegments only:**
    - Amazon: North America, International, AWS.
    - Meta: Family of Apps, Reality Labs.
    - Microsoft 10-K: Productivity & Business Processes, Intelligent Cloud, More Personal Computing.
  - **Revenue** is additionally tagged on ProductOrService (AAPL, AMZN, MSFT, NVDA) and on Geographical (META, MSFT, NVDA). MSFT also uses `ProductsOrServicesSecondaryCategorization`.
  - **Apple's significant segment expense** `CostOfGoodsAndServicesSold` is tagged by segment with the same two axes (for example Americas $21.507bn for the quarter ended June 2026).

  — [SEC FSDS](https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets)
- **[own measurement]** Apple 10-Q for the quarter ended 2026-06-27. One concept, `RevenueFromContractWithCustomerExcludingAssessedTax`, carries consolidated $109.417bn; segments Americas 45.781, Europe 29.395, Greater China 18.816, Japan 6.554, Rest of APAC 8.871 (sum 109.417); and product/service iPhone 54.252, Mac 10.352, iPad 6.191, Wearables 7.883, Services 30.739, with a Product subtotal of 78.678. — [SEC FSDS](https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets)
- SEC data-quality reminder (Mar 19, 2026): "Inappropriate Use of Consolidated Entities [Axis]". The axis is misused in practice. — [SEC OSD list](https://www.sec.gov/page/osdstaffobsandguide)

### Inferences
- A deterministic segment extractor can key on (line-item concept, StatementBusinessSegmentsAxis member, ConsolidationItemsAxis member or absent). It should treat "BusinessSegments only" and "BusinessSegments + ConsolidationItems=OperatingSegments" as the same segment amount. Both are sanctioned by the FASB TIG and both appear in the mega-cap sample.
- It can check itself with code: segment members on one concept and period should sum, together with CorporateNonSegment, IntersegmentElimination and reconciling members, to the undimensioned consolidated fact. This holds exactly for Apple's revenue.
- Segment members are company-specific extensions, so labels from the member's label linkbase are needed for display. Identity should use the member QName, which is stable within a company unless it is renamed. A renamed member is a new member and needs an explicit link across periods.
- "Segment operating income by geography" can only be built where the reportable segments are geographic (Apple) or a company volunteers it. For most companies the filing contains geographic **revenue** (srt:StatementGeographicalAxis) and **long-lived assets** only. Any geographic profit split would be an estimate the system makes, not data.
- ASU 2023-07 makes cross-company comparison of segment expenses harder rather than easier. Expense categories follow what each CODM sees, and the FASB's own example uses extension line items. Expect custom concepts on segment-expense rows. Place them by their calculation or presentation parent rather than mapping them by hand.

### Gaps
- I did not obtain the exact element list for ASU 2023-09 (rate-reconciliation category elements and the jurisdiction axis/members for taxes paid) from a FASB primary source.
- No published census of how many filers use the one-axis versus two-axis segment model, or how often significant segment expenses are custom versus standard, for FY2024–2025. My sample covers only face-statement concepts.
- No source found on SEC staff observations specific to ASU 2023-07 tagging errors (none listed on the OSD page for 2025–2026).

---

## Q4. Measured XBRL error rates, known error types, and the checks people run

### Takeaway
Gross errors were common early in the mandate: a quarter of the first 400 large filers had calculation inconsistencies in 2009. They have fallen sharply under XBRL US DQC rules, which numbered 196 approved rules in ruleset v30.0.5 (Sept 2026), with 90 shipped inside the FASB taxonomy. In my 2026q3 sample the balance-sheet identity never failed (0 of 5,424 filings) and negative period-end revenue appeared in 8 of 7,159 facts. The residual error classes the SEC still flags in 2023–2026 are:
- sign (negative versus positive);
- scale (thousands versus whole numbers);
- inconsistent tags or labels for the same item across periods;
- unnecessary custom tags;
- wrong elements in specific areas (EPS, credit losses, noninterest income, Schedule III);
- axis misuse.

### Cited Findings
- Debreceny, Farewell, Piechocki, Felden & Gräning, *Journal of Accounting and Public Policy* 29(3) 296–306 (June 2010): one quarter of the filings by the first 400 large companies in the first round (2009) had calculation errors, where reported totals differed from the sum of facts bound in calculation relationships. The primary cause was mishandled debit/credit (sign) assumptions. — [IDEAS/RePEc](https://ideas.repec.org/a/eee/jappol/v29y2010i3p296-306.html)
- Du, Vasarhelyi & Zheng, "XBRL Mandate: Thousands of Filing Errors and So What?" (*Journal of Information Systems*, about 2013): 4,532 filings with 4,260 errors identified by XBRL Cloud. Errors per filing fall significantly as a company files more (a learning curve). — [Semantic Scholar](https://www.semanticscholar.org/paper/XBRL-Mandate:-Thousands-of-Filing-Errors-and-So-Du-Vasarhelyi/5b5d4ac0dbf2dc57a3ec4e9698812ddded232263)
- XBRL US DQC first-year effect: errors for all filers fell 64% in Q1 2016 versus Q1 2015 (LAF −70%, SRC −60%). — [XBRL US DQC results](https://xbrl.us/home/priorities/data-quality/filing-results/dqc-results/dqc-results-2/)
- The DQC ruleset is at 196 approved rules, version 30.0.5 (Sept 2026). Rules by error type:
  - **Sign:** DQC_0015 (elements that should not be negative); DQC_0128 (dimensional value larger than the default).
  - **Period/context:** DQC_0005 (dates after period end limited to subsequent events), DQC_0006, DQC_0033, DQC_0036 (document period end date), DQC_0146 (incorrect period reported).
  - **Axis/member:** DQC_0001 (axes allowed only certain members), DQC_0041, DQC_0053, DQC_0054.
  - **Calculation:** DQC_0004 (Assets = Liabilities + Equity), DQC_0008 (reversed calculation), DQC_0009 (A ≤ B), DQC_0043 (operating cash-flow calc weights), DQC_0118 (FS table calculation check of required context), DQC_0126 (FS calculation check with non-dimensional data).
  - **Scale:** DQC_0091 (invalid percentage values), DQC_0095 (common shares outstanding), DQC_0139 (bank ratios).
  - **Element choice:** DQC_0018 (deprecated element), DQC_0120 (incorrect line-item reference), DQC_0136 (caption value matches financial statements).

  — [XBRL US approved rules](https://xbrl.us/home/priorities/data-quality/rules-guidance/)
- XBRL US: "over 150 validation rules", a growing number of them included in the FASB taxonomy and in SEC EDGAR submission processing (Mar 2025). — [XBRL US](https://xbrl.us/why-normalize-data/)
- FASB 2026 taxonomy:
  - 30 additional DQC rules added to the DQC Rules Taxonomy, for 90 in total. DQC_0015 (negative values) was modified.
  - 120 new GRT elements.
  - Deprecations: 337 (ASU/SEC), 130 (topical/reference) and 97 (public comment/internal).
  - Deprecated elements stay for two annual versions and are then deleted; 266 elements deprecated in 2023 were removed.
  - Deprecation relationships (`dep-concept-deprecatedConcept`, `dep-aggregateConcept-deprecatedPartConcept`, and others) point to replacements where one exists.

  — [FASB 2026 Release Notes](https://xbrl.fasb.org/resources/annualrelease/2026/GAAP_Financial_Reporting_Taxonomy_Release_Notes.pdf)
- SEC Division of Corporation Finance sample XBRL comment letter (Sept 7, 2023) covers six areas:
  - missing Inline XBRL;
  - cover-page shares tagged with materially different values because of scale (whole versus thousands);
  - pay-versus-performance tagging;
  - separate tags required for combined items;
  - different elements for the same income-statement line item from period to period;
  - custom tags where a US GAAP element exists.

  — [Cooley PubCo](https://cooleypubco.com/2023/09/08/sample-comment-letter-xbrl/). A search snippet (not fetched) also lists sign errors, scaling (billions versus millions), incomplete tagging of parenthetical numbers and missing calculations as recurring staff issues. — [Free Writings & Perspectives](https://www.freewritings.law/2023/09/sec-staff-issues-sample-comment-letter-regarding-xbrl-disclosures/)
- SEC data-quality reminders, 2022–2026:
  - Changing Tags for the Same Reported Items on the Income Statement (Dec 8, 2022)
  - Operating-activities children incorrectly using investing tags (Jun 30, 2023)
  - Credit-loss write-off tagging (Aug 11, 2023)
  - Changing Labels for the Same Reported Item (Nov 3, 2023)
  - Cash Flow Statement Data Element Presentation (Mar 8, 2024)
  - Incorrect Tagging for EPS Data (May 30, 2024)
  - Inappropriate Custom Tags for Provision for Credit Losses (Sep 24, 2024)
  - Public Float Tagging Errors (Jul 21, 2025)
  - Inappropriate Use of Consolidated Entities [Axis] (Mar 19, 2026)
  - Common Noninterest Income Tagging Errors (May 14, 2026)
  - Common Tagging Errors in Schedule III (Sep 9, 2026)

  — [SEC OSD list](https://www.sec.gov/page/osdstaffobsandguide)
- The FASB segment TIG states the sign convention: values "generally entered as positive, with the exception of certain concepts such as net income (loss) or gain (loss)". Sign is set by the element's balance type and calculation weight, not by how the HTML shows it. — [FASB segment TIG](https://xbrl.fasb.org/impguidance/SG1_TIG/segmentreporting.pdf)
- **[own measurement]** FSDS 2026q3, 10-K/10-Q, undimensioned consolidated USD facts at the period end:
  - `Assets` versus `LiabilitiesAndStockholdersEquity`: 5,424 filings checked, **0** differing by more than 0.05%.
  - Revenue facts (`Revenues` or `RevenueFromContractWithCustomerExcludingAssessedTax`): 7,159 checked, **8 negative** (0.11%). These are candidates and were not traced.

  — [SEC FSDS](https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets)
- Du, Huddart & Jiang used DQC rule output to find filings with errors in accrual-related tags. Excluding them did not change their anomaly results, which suggests residual DQC-flagged errors are not large enough to move aggregate research measures (2012–2018 sample). — [Du, Huddart & Jiang 2021](https://business.columbia.edu/sites/default/files-efs/imce-uploads/CEASA/Events%20Page/revisiting_accounting-based_return_anomalies.pdf)

### Inferences
- Checks a research pipeline should run in code, each mapped to a known error class:
  - **Sign:** run the DQC_0015 element list against each fact's sign, and compare the sign against the balance type (debit/credit) of the mapped standard concept.
  - **Scale:** compare the same item across the 10-Q/10-K series and against the `decimals` attribute. A jump of about 1,000 times signals a scale error.
  - **Period:** check that the context period matches the statement period and duration in quarters, and that a 10-K's FY duration is about 4 quarters.
  - **Calculation:** apply the filer's own calculation linkbase within tolerance (XBRL Calculations 1.1 handles rounding), plus fixed identities such as A = L + E and segment sum = consolidated total.
  - **Duplicates:** detect the same concept, context and unit with different values, and refuse or flag them.
  - **Time-series concept switches:** compare the prior-period comparative in the new filing with the value originally filed.
- The XBRL US DQC rules are open source (Arelle plugin) and the FASB ships 90 of them as a rules taxonomy. A pipeline can run the published rules rather than re-deriving them.
- Because large filers now pass DQC rules before filing, the residual risk for research is less about wrong numbers. It is mostly about **inconsistent concept choice over time and across companies**, which the SEC has flagged repeatedly since 2022, and **domain-specific mis-tagging** (banks, BDCs, REITs).

### Gaps
- I found no recent (2022–2026) published **rate** of DQC errors per filing or per fact. The XBRL US filing-results pages hold per-filing results and timelines but no headline numbers in text.
- No measured 2024–2026 rates for duplicate facts, wrong-period contexts or scale errors across all filers. The 8 negative-revenue facts were not traced to tell genuine values from sign errors.
- Calculation-inconsistency rates under Calculations 1.1 for SEC filings (as opposed to ESEF) were not found.

---

## Q5. How do XBRL-derived fundamentals compare with Compustat and other vendors (match rates, discrepancies)?

### Takeaway
Studies from 2011–2018 find as-filed XBRL agrees with the 10-K text far more closely than aggregator data does. Compustat departs from the filed numbers for many items by design (standardization adjustments, aggregations, omissions). Totals such as `Assets` agree, but components and derived measures differ enough to change research results: about 32% of stock-years land in a different accruals quintile. I found no 2023–2026 match-rate study comparing a modern open-source XBRL normalizer with Compustat.

### Cited Findings
- Chychyla & Kogan, *Journal of Information Systems* 29(1), Spring 2015: the first large-scale comparison, covering 30 accounting items for about 5,000 companies with filings from Oct 1, 2011 to Sep 30, 2012. Compustat values of 17 of the 30 variables differ significantly from the 10-K values. The amount and size of the alterations depend on item type, industry and size. — [ResearchGate](https://www.researchgate.net/publication/272304077_Using_XBRL_to_Conduct_a_Large-Scale_Study_of_Discrepancies_between_the_Accounting_Numbers_in_Compustat_and_SEC_10-K_Filings); [U. Miami record](https://scholarship.miami.edu/esploro/outputs/journalArticle/Using-XBRL-to-Conduct-a-Large-Scale/991031575973402976)
- Boritz & No, "How Significant are the Differences in Financial Data Provided by Key Data Sources? A Comparison of XBRL, Compustat, Yahoo! Finance, and Google Finance" (SSRN 2253638; search snippet, page not fetchable). For items in both XBRL and the aggregators, "all but 0.01 percent of the XBRL data amounts agree with the 10-K filings, whereas 6.5 percent to 7.7 percent of the amounts provided by aggregators/distributors do not". Aggregators omit more than 50% of the face-statement items available in XBRL. — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2253638)
- A search summary also attributes to this literature "Compustat data resulted in the largest percentage of mismatches (44.3%) and the lowest number of omissions (50.9%)". I could not tie this to a specific paper (possibly the AABRI manuscript "Data differences — XBRL versus Compustat"), so treat it as unverified. — [AABRI manuscript](https://www.aabri.com/manuscripts/11798.pdf)
- Du, Huddart & Jiang, "Lost in Standardization" (Sept 2021 draft), 19,615 firm-years 2012–2018 from the SEC Financial Statement and Notes data sets:
  - Total assets do not differ significantly between XBRL and Compustat, but accrual components (`recch`, `invch`, `apalch`, `txach`, `aoloch`, `dpc`) mostly do (for example `dpc` mean difference −0.005, t = −16.32).
  - About 68% of stock-years fall in the same accruals quintile under both sources; the other 32% drive different hedge returns. The as-filed hedge return is 0.673%/month versus 0.296% for Compustat.
  - Discrepancies are larger where peers' reporting differs, where industry-specific tags are more common, and for deeper tags in the taxonomy hierarchy.
  - S&P's white paper is quoted saying "different data providers use different methodologies for standardization".

  — [Du, Huddart & Jiang 2021](https://business.columbia.edu/sites/default/files-efs/imce-uploads/CEASA/Events%20Page/revisiting_accounting-based_return_anomalies.pdf)
- A summary of the Chychyla/Kogan line of work says more than 90% of data items from third-party aggregators contain discrepancies against XBRL data. This is a secondary-source paraphrase (Penn State Smeal magazine / search summary) and I did not verify it against the paper. — [Penn State Smeal magazine](https://magazine.smeal.psu.edu/richer-data-better-decisions/)

### Inferences
- "Accuracy versus Compustat" is the wrong measuring stick for a system that must reproduce what the company filed. Compustat deliberately reclassifies. Match against Compustat measures agreement with S&P's standardization, not correctness. The right stick is the filed statement itself: XBRL agrees with the 10-K text in about 99.99% of amounts per Boritz & No. Self-consistency checks (calc linkbase, A = L + E, segment sums) come next.
- Where agreement with a vendor is needed (for example for factor research), expect totals to match closely and components and derived items to diverge. Budget for an item-by-item reconciliation map like Du-Huddart-Jiang's Table C.1 rather than expecting one tag per vendor item.

### Gaps
- No 2023–2026 study comparing standardized fundamentals from edgartools, secfsdstools, XBRL US NORM, Calcbench or FMP against Compustat or Bloomberg, with match rates per item.
- The Boritz & No sample period and journal version could not be confirmed (SSRN returned 403).
- No published vendor accuracy figures (Calcbench, FMP, sec-api.io, Fiscal.ai) found.

# Deterministic extraction of financial numbers from SEC filings via XBRL / inline XBRL (state as of October 2026)

Method note. Facts marked "measured 2026-10-16" come from my own requests to SEC endpoints and files on that date (script output in the session scratchpad, not kept in the repo). Each measured fact cites the exact URL the data came from. Each measurement covers one filing or one file, so it is a single case and not a census. Library metadata (versions, dates, stars, licenses) was read on 2026-10-16 from the PyPI JSON API (`https://pypi.org/pypi/<name>/json`) and the GitHub REST API (`gh api repos/<owner>/<repo>`).

## Q1. SEC's own structured sources: what each contains, cadence, limits, size

### Takeaway
The SEC publishes four layers of XBRL data, each built from the same filer-submitted XBRL:
- **The data.sec.gov JSON APIs** (submissions, companyconcept, companyfacts, frames) update in real time (XBRL APIs within about a minute). They hold only standard-taxonomy facts that apply to the whole entity: no dimensions, no custom extensions, no table placement.
- **The Financial Statement Data Sets (FSDS, quarterly)** hold only the face statements. Since December 2024 they carry a `segments` column.
- **The Financial Statement and Notes Data Sets (FSNDS, monthly)** hold every tagged number and text block, including notes, dimensions (`dim`), custom tags, presentation (`pre`), rendering/table list (`ren`) and calculations (`cal`).
- **The per-filing raw files** (iXBRL `.htm`, extracted instance `_htm.xml`, `.xsd`, `_pre/_cal/_def/_lab.xml`, `FilingSummary.xml`, `R*.htm`, `MetaLinks.json`) are complete and available as soon as the filing is accepted, but need an XBRL parser.

### Cited Findings

**data.sec.gov APIs (official documentation)**
- Endpoints:
  - `https://data.sec.gov/submissions/CIK##########.json` (10-digit CIK with leading zeros).
  - `https://data.sec.gov/api/xbrl/companyconcept/CIK##########/us-gaap/AccountsPayableCurrent.json`: "all the XBRL disclosures from a single company (CIK) and concept".
  - `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`: "all the company concepts data for a company into a single API call".
  - `https://data.sec.gov/api/xbrl/frames/us-gaap/AccountsPayableCurrent/USD/CY2019Q1I.json`: "aggregates one fact for each reporting entity that is last filed that most closely fits the calendrical period".
  - [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- Scope of the XBRL APIs: facts from "us-gaap, ifrs-full, dei, or srt" taxonomies. Facts must "Use a non-custom taxonomy" and "Apply to the entire filing entity", so that "facts have a consistent context and meaning across companies". — [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- Frames period syntax:
  - "CY#### for annual data (duration 365 days +/- 30 days)", "CY####Q# for quarterly data (duration 91 days +/- 30 days)" and "CY####Q#I for instantaneous data".
  - Compound units are written like "USD-per-shares".
  - [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- Latency:
  - Submissions: "typical processing delay of less than a second".
  - XBRL APIs: "typical processing delay of under a minute".
  - "JSON structures are updated throughout the day, in real time."
  - [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- Bulk files:
  - `companyfacts.zip` "contains all the data from the XBRL Frame API and the XBRL Company Facts API".
  - `submissions.zip` contains the filing history.
  - Both are "updated and republished nightly at approximately 3:00 a.m. ET".
  - No authentication or API key. data.sec.gov "does not support Cross Origin Resource Scripting (CORS)".
  - [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- Fair-access policy:
  - "Current max request rate: 10 requests/second."
  - Clients must "declare your user agent in request headers", for example `User-Agent: Sample Company Name AdminContact@<sample company domain>.com`, `Accept-Encoding: gzip, deflate`.
  - The SEC "reserves the right to limit request rates". No block duration is stated.
  - Filing folders are laid out as `/Archives/edgar/data/[CIK]/[accession-number]/`, with `index.html/index.xml/index.json`, plus `/Archives/edgar/daily-index/` and `/Archives/edgar/full-index/`.
  - [SEC Accessing EDGAR Data](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data)

**companyfacts and submissions shape (measured 2026-10-16)**
- Apple companyfacts:
  - The file is 3.79 MB.
  - Top-level keys: `cik, entityName, facts`. Taxonomies present: `dei` (2 concepts) and `us-gaap` (503 concepts).
  - Each concept has `label, description, units`.
  - Every fact record has exactly the fields `start, end, val, accn, fy, fp, form, filed, frame`. There is no field for axis, member, segment, context or presentation role.
  - [companyfacts CIK0000320193](https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json)
- Apple submissions JSON: the `filings.recent` arrays include `accessionNumber, filingDate, reportDate, acceptanceDateTime, act, form, fileNumber, filmNumber, items, core_type, size, isXBRL, isInlineXBRL, isXBRLNumeric, primaryDocument, primaryDocDescription`. Example: the FY2025 10-K is `0000320193-25-000079`, filed 2025-10-31, `aapl-20250927.htm`, isInlineXBRL=1. — [submissions CIK0000320193](https://data.sec.gov/submissions/CIK0000320193.json)

**Financial Statement Data Sets (FSDS, the "compact" set)**
- Scope:
  - "Numeric data on the primary financial statements as rendered by the Commission (Balance Sheet, Income Statement, Cash Flows, Changes in Equity, and Comprehensive Income) and page footnotes on those statements".
  - Covers submissions "which include financial statements rendered by the Commission (e.g., 10-K, 10-Q, 20-F, 40-F)", from 4/15/2009.
  - Updated quarterly.
  - Sources: readme.htm inside [2026q3.zip](https://www.sec.gov/files/dera/data/financial-statement-data-sets/2026q3.zip) and [FSDS readme PDF](https://www.sec.gov/files/aqfs.pdf).
- The FSDS NUM key now includes `segments` ("Tags used to represent axis and member reporting", ALPHANUMERIC 1024) and `coreg`. — readme.htm inside [2026q3.zip](https://www.sec.gov/files/dera/data/financial-statement-data-sets/2026q3.zip). The older PDF readme [aqfs.pdf](https://www.sec.gov/files/aqfs.pdf) still lists the NUM key without `segments`, so the PDF is stale on this point.
- secfsdstools says the "segments" column "was added in December 2024". The same README elsewhere says "introduced in January 2025", so the two statements disagree. — [secfsdstools README](https://github.com/HansjoergW/sec-fincancial-statement-data-set)
- 2026q3.zip (measured 2026-10-16), from [2026q3.zip](https://www.sec.gov/files/dera/data/financial-statement-data-sets/2026q3.zip):
  - Size: 65.1 MB zipped, 986 MB unzipped. Files: `sub.txt` 1.97 MB, `pre.txt` 89.7 MB, `num.txt` 875 MB, `tag.txt` 18.7 MB, `readme.htm`. File timestamps inside the zip are 2026-10-05, about 5 days after quarter end.
  - Column headers:
    - `num.txt`: `adsh, tag, version, ddate, qtrs, uom, segments, coreg, value, footnote`.
    - `pre.txt`: `adsh, report, line, stmt, inpth, rfile, tag, version, plabel, negating`.
    - `tag.txt`: `tag, version, custom, abstract, datatype, iord, crdr, tlabel, doc`.
  - 3,905,397 NUM rows, of which 2,346,825 have a non-empty `segments` value.
  - NVIDIA 10-Q (adsh 0001045810-26-000075, period 2026-07-31, filed 2026-08-26): 388 NUM rows, 146 of them dimensional. The dimensional rows are face-statement members such as `EquityComponents=AdditionalPaidInCapital;`.
  - Microsoft 10-K (0001193125-26-323660, FY2026, filed 2026-07-29): 517 NUM rows, 257 of them dimensional.

**Financial Statement and Notes Data Sets (FSNDS)**
- Cadence and coverage:
  - Monthly since November 2020, quarterly before that. Data spans January 2009 to September 2026.
  - "Effective March 2024, monthly data sets will be consolidated into quarterly files after a year".
  - Data filed after 5:30 PM Eastern on the month's last day goes into the next posting.
  - [SEC FSNDS page](https://www.sec.gov/data-research/sec-markets-data/financial-statement-notes-data-sets)
- Readme content, from [FSNDS readme PDF](https://www.sec.gov/files/aqfsn_1.pdf):
  - Eight tab-delimited tables: SUB, TAG, DIM, NUM, TXT, REN, PRE, CAL.
  - NUM "includes, for every submission, all line item values as rendered by the Commission Viewer/Previewer".
  - Scope: XBRL exhibits "to all forms other than 485BPOS, 497, SDR, SDR/A, SDR-A and SDR/W", submitted from 4/15/2009.
  - Each quarterly set comes with a W3C tabular-data metadata file.
- Key definitions, from [FSNDS readme PDF](https://www.sec.gov/files/aqfsn_1.pdf):
  - TAG holds "all standard taxonomy tags ... and also includes all custom taxonomy tags defined in the submissions". `custom`=1 when version=adsh. `doc` is truncated to 2048 characters.
  - DIM holds "all of the combinations of XBRL axis and member used to tag any submission":
    - The key `dimh` is the MD5 of the `segments` text, which is written as `{axis}={member};` pairs in lexical order.
    - Prefixes are dropped, and the "Axis", "Member"/"Domain" and "Statement" affixes are truncated (example `LegalEntity=Xyz;Scenario=Restated;`).
    - `segt` flags truncation at 1024 characters.
  - The NUM key is `adsh, tag, version, ddate, qtrs, uom, dimh, iprx`:
    - `ddate` is the end date "rounded to the nearest month end"; `qtrs` is the duration rounded to whole quarters.
    - `iprx` distinguishes duplicates ("For most purposes, data with iprx greater than 1 are not needed").
    - `value` is not scaled and is rounded to 4 decimals. Also present: `dimn`, `coreg`, `durp`, `datp`, `dcml` (INF=32767).
  - TXT is "the plain (no HTML) text of each non-numeric XBRL fact". Text blocks have their markup removed, and `value` is truncated (field max 2048; `txtlen` records the original length).
  - REN describes each presentation group (R file): `report, rfile, menucat` (C=Cover, S=Statements, N=Notes, P=Policies, T=Tables, D=Details, O, U), `shortname, longname, roleuri, parentroleuri, parentreport, ultparentrpt`. Report numbering follows the EDGAR Renderer version current at publication.
  - PRE has one row per tagged line: `report, line, stmt` (CP/BS/IS/CF/EQ/CI/UN), `inpth` (parenthetical), `tag, version, prole, plabel` (preferred label text), `negating`.
  - CAL holds calculation arcs: `grp, arc, negative, ptag, pversion, ctag, cversion`.
- The FSNDS readme Overview still says "The information will be updated quarterly", which contradicts the monthly cadence on the FSNDS page. — [FSNDS readme PDF](https://www.sec.gov/files/aqfsn_1.pdf) vs [SEC FSNDS page](https://www.sec.gov/data-research/sec-markets-data/financial-statement-notes-data-sets)
- 2026_08_notes.zip (measured 2026-10-16), from [2026_08_notes.zip](https://www.sec.gov/files/dera/data/financial-statement-notes-data-sets/2026_08_notes.zip):
  - The working URL path is `/files/dera/data/financial-statement-notes-data-sets/` (a path containing `-and-notes-` returns 404).
  - Size: 312.7 MB zipped, 2.46 GB unzipped. Files: `sub.tsv` 3.3 MB, `tag.tsv` 90 MB, `dim.tsv` 62 MB, `ren.tsv` 66 MB, `cal.tsv` 63 MB, `pre.tsv` 396 MB, `num.tsv` 1.14 GB, `txt.tsv` 637 MB, plus `readme.htm` and `notes-metadata.json`. File timestamps are 2026-09-03, about 3 days after month end.
  - Headers:
    - `num.tsv`: `adsh, tag, version, ddate, qtrs, uom, dimh, iprx, value, footnote, footlen, dimn, coreg, durp, datp, dcml`.
    - `pre.tsv`: `adsh, report, line, stmt, inpth, tag, version, prole, plabel, negating`.
    - `ren.tsv`: `adsh, report, rfile, menucat, shortname, longname, roleuri, parentroleuri, parentreport, ultparentrpt`.
    - `txt.tsv`: `... escaped, srclen, txtlen, footnote, footlen, context, value`.
    - The `dim.tsv` key column is named `dimhash`, not `dimh` as the readme says (actual header `dimhash, segments, segt`). The no-dimension hash appears as `0x00000000`.

**Raw per-filing XBRL (measured 2026-10-16)**
- Apple FY2025 10-K folder (from [Apple 10-K index.json](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/index.json)):
  - Primary iXBRL document `aapl-20250927.htm` (1.52 MB) and SEC-extracted instance `aapl-20250927_htm.xml` (1.42 MB).
  - Extension schema `aapl-20250927.xsd` (56 KB) and linkbases `_cal.xml` (153 KB), `_def.xml` (225 KB), `_lab.xml` (764 KB), `_pre.xml` (496 KB).
  - SEC renderer outputs `FilingSummary.xml` (43 KB), `MetaLinks.json` (1.12 MB) and `R1.htm`…`R70.htm`, plus `-xbrl.zip` (399 KB) and the full `.txt` submission.
- Apple instance (from [aapl-20250927_htm.xml](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927_htm.xml)):
  - 1,131 facts; 452 have explicit dimension members in their contexts (Arelle counts 460 dimensional, see Q3).
  - Fact namespaces: us-gaap 969, the Apple custom extension `http://www.apple.com/20250927` 83, dei 59, `cyd` (cybersecurity) 15, `ecd` (executive comp / insider trading) 5.
  - Most frequent axes: FairValueByFairValueHierarchyLevelAxis 170, FinancialInstrumentAxis 152, srt:ConsolidationItemsAxis 69, StatementBusinessSegmentsAxis 60, StatementEquityComponentsAxis 54, srt:ProductOrServiceAxis 27.
- `FilingSummary.xml` per-report fields: `IsDefault, HasEmbeddedReports, HtmlFileName, LongName, ReportType, Role, ShortName, MenuCategory, Position`. Apple has 71 reports (Details 33, Notes 16, Tables 12, Statements 6, Cover 2, Policies 1). `_pre.xml` has 72 presentation roles. — [Apple FilingSummary.xml](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/FilingSummary.xml)

### Inferences
- **Latency and completeness.** The per-filing raw XBRL is the only source that is both available at acceptance and complete. FSNDS is equally complete but arrives roughly 3–30 days late (monthly). companyfacts arrives within about a minute but is incomplete by design.
- **Size.** Both bulk sets are large enough (FSNDS about 2.5 GB unzipped per month, FSDS about 1 GB per quarter) that a team would load them into columnar storage (secfsdstools does this with parquet) rather than read them ad hoc.
- **Dates.** FSNDS/FSDS round `ddate` to month end and `qtrs` to whole quarters. Exact period start/end dates (for example NVIDIA's 2026-07-26 quarter end) are only in the instance contexts and in companyfacts (`start`/`end`). FSNDS keeps `datp`/`durp` deltas, from which the exact date can only be approximated, not recovered.

### Gaps
- No SEC document states a numeric rate limit for data.sec.gov separately from www.sec.gov. The 10 req/s policy is stated for EDGAR generally.
- I did not measure companyfacts.zip or submissions.zip sizes.
- The FSDS readme does not say whether the new `segments` rows include all face-statement dimensional facts or only some.

## Q2. companyfacts omits dimensional facts: confirmation, and which source gives segment data

### Takeaway
Confirmed, both by SEC's own wording and by measurement. companyfacts and frames hold only facts that "apply to the entire filing entity" in non-custom taxonomies. Apple's FY2025 iPhone, Services and Americas-segment figures and segment operating income appear zero times in Apple's companyfacts JSON. Segment and disaggregation data (operating income by geography, revenue by product) must come from FSNDS (`num`+`dim`+`pre`+`ren`) or from the filing's own XBRL instance and linkbases, read directly or through a parser.

### Cited Findings
- SEC's scope rule for the XBRL APIs: facts must "Use a non-custom taxonomy" and "Apply to the entire filing entity". Custom taxonomies are excluded. — [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- Measured 2026-10-16 in [companyfacts CIK0000320193](https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json):
  - Exact-value search across every concept and unit:
    - Total FY2025 net sales 416,161,000,000: 1 occurrence (`RevenueFromContractWithCustomerExcludingAssessedTax`, accn 0000320193-25-000079, frame CY2025).
    - iPhone FY2025 209,586,000,000: 0. Services 109,158,000,000: 0. Americas segment net sales 178,353,000,000: 0. Americas segment operating income 72,480,000,000: 0. Corporate non-segment operating income -42,627,000,000: 0. US net sales 151,790,000,000: 0.
  - The same check on FY2024 values (iPhone 201,183M, Americas 167,045M, Services 96,169M) also found 0, while total FY2024 net sales 391,035M appears twice, once each from the FY2024 and FY2025 10-Ks.
  - The FY2024 iPhone/Americas/Services amounts were taken from memory of Apple's FY2024 10-K and not re-verified in this session. The FY2025 amounts were read from the instance.
- Values the instance does contain (measured 2026-10-16, [aapl-20250927_htm.xml](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927_htm.xml)), for FY2025 (2024-09-29 to 2025-09-27):
  - `RevenueFromContractWithCustomerExcludingAssessedTax` on `srt:ProductOrServiceAxis`: `aapl:IPhoneMember` 209,586M; `aapl:MacMember` 33,708M; `aapl:IPadMember` 28,023M; `aapl:WearablesHomeandAccessoriesMember` 35,686M; `us-gaap:ServiceMember` 109,158M; `us-gaap:ProductMember` 307,003M.
  - The same tag on `srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember` × `us-gaap:StatementBusinessSegmentsAxis`: Americas 178,353M; Europe 111,032M; Greater China 64,377M; Japan 28,703M; Rest of Asia Pacific 33,696M.
  - `OperatingIncomeLoss` by segment: Americas 72,480M; Europe 47,739M; Greater China 26,917M; Japan 13,955M; RoAP 14,586M; `ConsolidationItemsAxis=CorporateNonSegmentMember` -42,627M.
  - Revenue on `srt:StatementGeographicalAxis`: `country:US` 151,790M; `country:CN` 64,377M; `aapl:OtherCountriesMember` 199,994M.
  - The product and segment members are Apple custom extension members (`aapl:` prefix).
- FSNDS holds the segment and disaggregation facts with their table placement (measured 2026-10-16 on NVIDIA's 10-Q, adsh 0001045810-26-000075, quarter ended 2026-07-26, [2026_08_notes.zip](https://www.sec.gov/files/dera/data/financial-statement-notes-data-sets/2026_08_notes.zip)):
  - 1,002 NUM rows (487 with dimensions, 72 on NVIDIA custom tags).
  - `Revenues` for the quarter: total 96,221M. By `ProductOrService=`: DataCenter 89,023M; Hyperscale 48,710M; AICloudsIndustrialEnterprise 40,313M; EdgeComputing 7,198M. By `Geographical=`: US 60,074M; TW 26,985M; ChinaIncludingHongKong 7,880M; OtherCountries 1,282M. By `BusinessSegments=`: ComputeAndNetworkingSegment 88,299M; GraphicsSegment 7,922M (with `ConsolidationItems=OperatingSegments`).
  - `OperatingIncomeLoss`: consolidated 63,734M; Compute & Networking 62,696M; Graphics 3,899M.
  - PRE/REN placement: `OperatingIncomeLoss` sits in report 2, `stmt=IS`, plabel "Operating income", "Condensed Consolidated Statements of Income", menucat S. It also sits in reports 63 and 64, `stmt` blank, "Segment Information", menucat D.
  - NVIDIA's 70 REN reports: D 36, N 15, T 11, S 6, C 1, P 1. In `pre`, 508 of NVIDIA's rows have blank `stmt` (notes/details); the rest are CF 38, BS 36, CP 29, EQ 25, IS 18, CI 8.
- edgartools' own guide agrees: its Company Facts API (built on SEC companyfacts) has "Segment/dimension data: No" and "Custom concepts: No". Its per-filing XBRL API (`filing.xbrl()`) has "Yes" for both and is the route for "segment data, dimensions, or detailed breakdowns". — [edgartools choosing-the-right-api.md](https://github.com/dgunning/edgartools/blob/main/docs/xbrl/getting-started/choosing-the-right-api.md)
- XBRL US API (third-party, built on SEC filings): queries the XBRL US Public Filings Database, "updated approximately every 15 minutes from the SEC's EDGAR system". It needs a free API key. — [xbrlus/xbrl-api README](https://github.com/xbrlus/xbrl-api)

### Inferences
- **Segment and product data.** FSNDS is the cheapest bulk route: tab-delimited, no XBRL parser needed, one join of `num`→`dim` by hash and `num`→`pre`→`ren` by adsh/tag/version/report. Its cost is latency (monthly). For same-day data, the filing's `_htm.xml` instance (plain XBRL 2.1 XML, parseable with the standard library, as done above) plus `_pre.xml`/`FilingSummary.xml` gives the same facts at acceptance.
- **Cross-company comparison.** Because product members are company extensions (`aapl:IPhoneMember`, NVIDIA `DataCenter`), product revenue is never comparable across companies without a mapping. Each company's member set must be read from its own filing.
- **Shape is independent of layout.** Apple's ASU 2023-07 segment layout appears in XBRL as the same tag on the same two axes (`ConsolidationItemsAxis` × `StatementBusinessSegmentsAxis`) whatever the HTML layout.

### Gaps
- I did not check whether `frames` ever returns dimensional values. The SEC's scope sentence implies it does not.
- I did not measure how many of the FSNDS NUM rows for 10-K/10-Q are dimensional across the whole data set; the counts above are per filing.

## Q3. Open-source libraries: what they parse, reconstruction, standardization, maintenance, license, issues

### Takeaway
Two tools stand out in 2026:
- **edgartools**: MIT, weekly releases (5.62.0 on 2026-10-11), full linkbase parsing, statement resolution, dimension classification and a 95-concept standardization layer.
- **Arelle**: Apache-2.0, maintained by Workiva, 2.46.1 on 2026-10-08. It is the reference XBRL processor, and the SEC's own EDGAR renderer and validation plugins run on it.

Also current:
- **py-xbrl**: GPL-3.0, 3.0.3 in March 2026, with open crash issues. A lower-level parser.
- **secfsdstools**: Apache-2.0, 2.4.3 in September 2025. Built around the FSDS bulk files (face statements), with segments support since v2.

Older tools are inactive: python-xbrl (no release since 2016) and OpenEDGAR (no push since 2022). sec-edgar-downloader and secedgar only download filings.

### Cited Findings

**edgartools (dgunning/edgartools)**
- Maintenance: PyPI `edgartools` 5.62.0 uploaded 2026-10-11, 450 releases, MIT, Python ≥3.10. GitHub: 2,795 stars, last push 2026-10-16. Recent releases v5.62.0 (2026-10-11), v5.61.1 (2026-10-06), v5.61.0 (2026-10-06), v5.60.0 (2026-10-02), v5.59.1 (2026-09-26). Issue counts: 864 total, 42 open (GitHub search API). — [PyPI edgartools](https://pypi.org/project/edgartools/); [GitHub dgunning/edgartools](https://github.com/dgunning/edgartools)
- It requires `set_identity("email")` because "EDGAR requires a contact email on every request". It keeps to SEC's 10 req/s limit and has caching and offline storage. A hosted platform (edgar.tools) is built on it, with the promise "No feature is ever removed from the library to sell the platform". — [edgartools README](https://github.com/dgunning/edgartools)
- Three data routes — [choosing-the-right-api.md](https://github.com/dgunning/edgartools/blob/main/docs/xbrl/getting-started/choosing-the-right-api.md):
  - Company Facts (SEC companyfacts: multi-year history, primary three statements only, no segments).
  - Financials (latest annual filing, named getters).
  - XBRL (`filing.xbrl()`: single filing, all statements, dimensions, footnotes, custom concepts).
- Parsers: modules for instance, schema, labels, presentation, calculation and definition linkbases (`edgar/xbrl/parsers/*.py`), plus `statement_resolver.py`, `dimensions.py`, `notes.py`, `standardization/`. — [edgartools source tree](https://github.com/dgunning/edgartools/tree/main/edgar/xbrl)
- It exposes `calculation_linkbase()` as a DataFrame of parent→child arcs with weights and role URIs. — [edgartools docs/api/xbrl.md](https://github.com/dgunning/edgartools/blob/main/docs/api/xbrl.md)
- Dimension handling — [dimension-handling.md](https://github.com/dgunning/edgartools/blob/main/docs/xbrl/concepts/dimension-handling.md):
  - The default statement view "Shows values that belong on the face of the statement (including dimensional face values)" and "Hides breakdown details that belong in notes disclosures (geographic, segment, etc.)". `view="detailed"` shows everything.
  - Classification is tiered: (1) the definition linkbase ("If declared in the definition linkbase, it's a face value"); (2) curated axis lists, with `ProductOrServiceAxis`, `DebtInstrumentAxis` as face and `StatementGeographicalAxis`, `StatementBusinessSegmentsAxis`, `BusinessAcquisitionAxis` as breakdown; (3) pattern matching (for example `FairValue*Axis`).
  - The guide lists filers that report face lines only through dimensions, for example COGS for BA 2023+, RTX 2019+, WDAY 2019+, and debt for CAT 2020–2025 on `ConsolidationItemsAxis`.
- Standardization: 95 standard concepts and "2,900+" XBRL tag mappings, with a self-reported "~95% of common financial statement tags" coverage. Original labels are preserved, and a `standard_concept` column is added. — [standardization.md](https://github.com/dgunning/edgartools/blob/main/docs/xbrl/concepts/standardization.md)
- Open issues and recent fixes relevant to segments:
  - #1449 (open, 2026-10-06): "Member-qualified mappings for face-statement lines FASB now tags on members: related parties, segments (ASU 2023-07), expense disaggregation (ASU 2024-03)".
  - #1209 (open): "Clarify and bridge XBRL-only Notes and disclosure role routing".
  - #1331 (closed 2026-09): "Explicit DETAILED view omits certain reportable-segment revenue observations returned by the default view".
  - #1188 (closed): "`InstanceParser` collapses distinct expanded QNames when namespace URIs share a trailing segment".
  - [edgartools issues](https://github.com/dgunning/edgartools/issues)
- Performance (measured 2026-10-16, single cold run, Apple FY2025 10-K, edgartools 5.62.0, macOS): `find(accession)` + `filing.xbrl()` + income statement + facts DataFrame took 23.0 s wall time including import and network downloads, with 213 MB max RSS.
  - The facts DataFrame had 1,044 rows (the instance has 1,131 fact elements; I did not investigate the difference).
  - Its columns include `concept, context_ref, value, unit_ref, decimals, numeric_value, period_type, period_start, period_end, fiscal_period, fiscal_year, is_dimensioned, label, original_label, balance, preferred_sign, statement_type, statement_role`.
  - The rendered income statement matched Apple's reported totals: net sales 416,161; products 307,003; services 109,158; operating income 133,050; net income 112,010 ($M).
  - Measured against [Apple 10-K](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm).

**Arelle (Arelle/Arelle) and the SEC EDGAR plugin**
- Maintenance: PyPI `arelle-release` 2.46.1 uploaded 2026-10-08, 402 releases, Python ≥3.10. GitHub: 253 stars, last push 2026-10-15, 80 open issues. The LICENSE says "Copyright © 2011-present Workiva, Inc. Licensed under the Apache License, Version 2.0" (GitHub's detector shows NOASSERTION). — [PyPI arelle-release](https://pypi.org/project/arelle-release/); [Arelle LICENSE.md](https://github.com/Arelle/Arelle/blob/master/LICENSE.md)
- Features: "Fully-featured XBRL processor with GUI, CLI, Python API and Web Service API". Supports XBRL v2.1, XBRL Dimensions v1.0, XBRL Formula v1.0, Taxonomy Packages v1.0, xBRL-JSON v1.0, xBRL-CSV v1.0, Inline XBRL v1.1 and Units Registry. Plugins include `inlineXbrlDocumentSet`, `saveLoadableOIM`, `xbrlDB`, `EdgarRendererAllReports`. — [Arelle README](https://github.com/Arelle/Arelle); [Arelle plugin dir](https://github.com/Arelle/Arelle/tree/master/arelle/plugin)
- EdgarRenderer:
  - The `Arelle/EdgarRenderer` repo is archived: "has been deprecated and will no longer receive updates. Please use the Arelle/EDGAR repository". It was "created by staff of the U.S. Securities and Exchange Commission" and produces the viewer/R-file renderings. — [EdgarRenderer README](https://github.com/Arelle/EdgarRenderer)
  - `Arelle/EDGAR` (CC0-1.0, last push 2026-09-11) is "developed and maintained by the staff of the U.S. Securities and Exchange Commission". It provides traditional and inline XBRL viewers. "The current version of Arelle in use at the SEC is: 2.44.2", and XULE version 30052. It will use the XULE DQCRT rules for us-gaap/2025 and newer. — [Arelle/EDGAR README](https://github.com/Arelle/EDGAR)
- Performance (measured 2026-10-16, Apple FY2025 10-K loaded by URL via `Cntlr.modelManager.load`):
  - Cold cache: 55.0 s, 216 MB max RSS. Most of the time is taxonomy download into Arelle's web cache.
  - Warm-cache rerun: 0.7 s, 206 MB.
  - Both runs reported 1,131 facts and 460 dimensional facts.
  - Single runs. I did not verify that the warm run resolved the full DTS beyond the fact count and relationship sets being present.
  - Measured against [Apple 10-K](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm).

**py-xbrl (manusimidt/py-xbrl)**
- PyPI 3.0.3 uploaded 2026-03-08, 40 releases, GPL-3.0, Python ≥3.10. GitHub: 154 stars, last push 2026-09-13, 26 open issues. It parses "XBRL and iXBRL files (instance documents, taxonomy schemas, taxonomy linkbases)" following "the XBRL 2.1 Specification (2003)" or "the iXBRL 1.1 Specification (2013)". — [PyPI py-xbrl](https://pypi.org/project/py-xbrl/); [py-xbrl README](https://github.com/manusimidt/py-xbrl)
- Issues in 2025–2026:
  - Open: "v3.0.0 - Fails to extract facts for Older FIlings" (2026-01-29). "TaxonomyParser: Implement functionality for custom namespace schemaURL maps". "Parse facts without value instead of ignoring them". "(instance.py) ValueError when casting empty string to float".
  - Closed: "Py-xbrl crashes when taxonomy has circular dependency". "RecursionError: maximum recursion depth exceeded". "Maximum depth on recursion on get_schema_urls() - Filings are NOT getting processed".
  - [py-xbrl issues](https://github.com/manusimidt/py-xbrl/issues)

**secfsdstools (HansjoergW/sec-fincancial-statement-data-set)**
- PyPI 2.4.3 uploaded 2025-09-20, Apache-2.0, Python ≥3.10. GitHub: 85 stars, last push 2025-09-20, 1 open issue. — [PyPI secfsdstools](https://pypi.org/project/secfsdstools/)
- Workflow — [secfsdstools README](https://github.com/HansjoergW/sec-fincancial-statement-data-set):
  - Downloads the FSDS zips and converts them to parquet, for "bulk processing of the data without the need to do countless API calls to sec.gov".
  - A "Joined" representation joins `pre.txt` and `num.txt` on adsh/tag/version.
  - Has BS/IS/CF standardizers.
  - "version 2 supports the new 'segments' column", with `show_segments` on `StandardStatementPresenter`.
  - Experimental daily updates via `secdaily` since 2.4.0.
- The changelog lists a 2.2.0 notebook "09_00_segments_basics" for working with the segment column. — [secfsdstools CHANGELOG](https://github.com/HansjoergW/sec-fincancial-statement-data-set/blob/main/CHANGELOG.md)

**Other tools**
- python-xbrl (greedo): last PyPI release 1.1.1 on 2016-12-27, Apache-2.0, 235 stars. The repo was pushed 2026-04-21, but there has been no release in nearly 10 years. — [PyPI python-xbrl](https://pypi.org/project/python-xbrl/); [GitHub greedo/python-xbrl](https://github.com/greedo/python-xbrl)
- OpenEDGAR (LexPredict): MIT, 332 stars, last push 2022-12-26. — [GitHub LexPredict/openedgar](https://github.com/LexPredict/openedgar)
- sec-edgar-downloader: 5.1.0 on 2026-02-02, MIT, 717 stars. "Download SEC filings from the EDGAR database". — [PyPI sec-edgar-downloader](https://pypi.org/project/sec-edgar-downloader/); [GitHub](https://github.com/jadchaar/sec-edgar-downloader)
- secedgar (sec-edgar/sec-edgar): Apache-2.0, 1,418 stars, last push 2025-12-09. "Download all companies periodic reports, filings and forms from EDGAR database." — [GitHub sec-edgar/sec-edgar](https://github.com/sec-edgar/sec-edgar)
- ixbrlparse (kanedata/ixbrl-parse): 0.11.2 on 2025-11-04, MIT, 72 stars, last push 2026-10-09. "A lightweight python module for getting useful data out of iXBRL™ and XBRL™ files. The library is at an early stage". — [GitHub kanedata/ixbrl-parse](https://github.com/kanedata/ixbrl-parse)
- ixbrl-parse (cybermaggedon): 0.11.0 on 2026-03-23, Apache-2.0, 9 stars. "iXBRL parsing library in Python. Also outputs to RDF and CSV." — [GitHub cybermaggedon/ixbrl-parse](https://github.com/cybermaggedon/ixbrl-parse)
- divbzero `xbrl`: 0.0.1 from 2019. — [PyPI xbrl](https://pypi.org/project/xbrl/)
- finagg: 2.0.0 on 2026-03-22, Apache-2.0, 548 stars. "Data aggregation with popular and free financial APIs." — [GitHub theOGognf/finagg](https://github.com/theOGognf/finagg)
- edgar-crawler: GPL-3.0, 552 stars, last push 2025-07-18. It extracts textual item sections (for example MD&A text) to JSON, not XBRL. — [GitHub lefterisloukas/edgar-crawler](https://github.com/lefterisloukas/edgar-crawler)
- sec-api (sec-api.io): commercial API with an MIT Python client, 1.0.36 on 2026-04-13. — [PyPI sec-api](https://pypi.org/project/sec-api/)
- XBRL US:
  - The XBRL API needs an OAuth2 account. Non-members get "100" records per query, a "1,000" record offset and "100,000 queries" per account, for "individual, private, non-commercial and non-distributable research and development" only. Users "shall not use the XBRL API to copy or transfer data ... to another database". Members get up to 5,000 records per query. — [XBRL US XBRL API page/agreement](https://xbrl.us/xbrl-api/)
  - XBRL US open tools: XULE processor (Apache-2.0, last push 2026-09-21) — [xbrlus/xule](https://github.com/xbrlus/xule); DQC rules (last push 2026-10-05) — [DataQualityCommittee/dqc_us_rules](https://github.com/DataQualityCommittee/dqc_us_rules).

### Inferences
- **Choice by need:**
  - Arelle: a standards-complete parser. It is the same engine the SEC runs, and the cold cost is a one-time taxonomy cache.
  - edgartools: an opinionated end-to-end Python API with statement resolution and dimension classification already built. Its default view deliberately hides segment and geographic breakdowns, so segment work must use `view="detailed"` or the facts API.
  - FSNDS directly, or a small loader: zero-parse bulk tables at monthly latency. secfsdstools covers the FSDS face statements, not the notes.
- **edgartools risk.** Weekly releases and many 2026 fixes in parsing (QName collapse, detailed-view segment omissions) mean its outputs can change between versions. Pinning a version and recording it with each extraction is prudent.
- **License.** py-xbrl's GPL-3.0 matters for any code that is distributed. edgartools (MIT), Arelle (Apache-2.0) and secfsdstools (Apache-2.0) are permissive.

### Gaps
- Not covered in this session:
  - Whether secfsdstools supports the FSNDS (notes) data set. The README I read refers only to the "Financial Statement Data Sets".
  - Performance figures for py-xbrl, or a census-level reliability measurement for any library across many filings.
  - Any independent practitioner comparison of these tools from 2025–2026.
- No reliable source found for a successor to OpenEDGAR.

## Q4. How tools rebuild a statement or a note table from XBRL (presentation linkbase role), and how reliable it is

### Takeaway
Every route rebuilds a table from the filer's presentation linkbase: each table is one extended-link role (for example `http://www.apple.com/role/SegmentInformationandGeographicDataInformationbyReportableSegmentDetails`), and the role's tree gives row order and the preferred labels.
- **SEC's renderer** turns each role into one R file and categorises it (Cover/Statements/Notes/Policies/Tables/Details). FSNDS publishes that result as `ren` + `pre`.
- **edgartools** finds the primary statements by scoring roles on abstract concepts, key concepts and role-URI regexes. Role naming is filer-chosen and varies, and its code carries fixes for specific misses (issues #581, #673).
- **Reliability.** Placement and values are as filed and exact. Identifying which role is the income statement, or which note table holds "net sales by category", is heuristic.

### Cited Findings
- FSNDS PRE "provides the text assigned by the filer to each line item in the primary financial statements, the order in which the line item appeared, and the tag assigned to it". `line` "Represents the tag's presentation line order for a given report", and `report` "refers to the 'R file' as computed by the renderer". — [FSNDS readme PDF](https://www.sec.gov/files/aqfsn_1.pdf)
- REN fields: `roleuri` ("The XBRL 'roleuri' of the role"), `longname` ("The space-normalized text of the XBRL link 'definition' element content"), `menucat`, and `parentreport`/`ultparentrpt` (which link a Details table back to its note). In rare cases the number of reports depends on the EDGAR Renderer version. — [FSNDS readme PDF](https://www.sec.gov/files/aqfsn_1.pdf)
- PRE "may have more than one row per entry in NUM because the same tag can appear in more than one statement". Measured: NVIDIA's `OperatingIncomeLoss` sits in the income statement (report 2) and in two Segment Information detail reports (63, 64). — [FSNDS readme PDF](https://www.sec.gov/files/aqfsn_1.pdf); [2026_08_notes.zip](https://www.sec.gov/files/dera/data/financial-statement-notes-data-sets/2026_08_notes.zip)
- Apple FY2025 10-K roles for revenue and segments, measured 2026-10-16 in [Apple FilingSummary.xml](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/FilingSummary.xml):
  - R10 "Revenue" (Notes).
  - R21 "Segment Information and Geographic Data" (Notes).
  - R26/R37 "(Tables)".
  - R38 "Revenue - Disaggregated Net Sales and Portion of Net Sales That Was Previously Deferred (Details)", role `http://www.apple.com/role/RevenueDisaggregatedNetSalesandPortionofNetSalesThatWasPreviouslyDeferredDetails`.
  - R68 "Segment Information and Geographic Data - Information by Reportable Segment (Details)".
  - R69 "... Net Sales for Countries that Individually Accounted for More than 10% of the Total (Details)".
  - Each LongName carries a sortable code, for example "9955524 - Disclosure - ...".
- edgartools `statement_resolver.py` "provides a robust system for identifying and matching XBRL financial statements, notes, and disclosures regardless of taxonomy variations and company-specific customizations". — [statement_resolver.py](https://github.com/dgunning/edgartools/blob/main/edgar/xbrl/statement_resolver.py)
  - The IncomeStatement type matches on:
    - `primary_concepts=["us-gaap_IncomeStatementAbstract"]`, with alternatives `us-gaap_StatementOfIncomeAbstract` and IFRS equivalents.
    - `concept_patterns` (for example `.*_CondensedConsolidatedStatementsOfIncomeUnauditedAbstract$`).
    - `key_concepts` (`us-gaap_Revenues`, `us-gaap_NetIncomeLoss`).
    - `role_patterns` regexes.
  - Code comments tie patterns to past misses: "Issue #581: Match both singular and plural (Statement/Statements)"; "Issue #581: Make Operations pattern more specific to avoid matching tax disclosures"; "Issue #673: IFRS P&L role names".
  - A comment on cash flow describes Vale S.A.'s 20-F, whose operating total was in a company extension, so that "find_statement raised 'No statements…'".
- edgartools issue #1209 (open): "Clarify and bridge XBRL-only Notes and disclosure role routing". Issue #1449 (open): face-statement lines that FASB now tags on members under ASU 2023-07 (segments) and ASU 2024-03 (expense disaggregation). — [edgartools issues](https://github.com/dgunning/edgartools/issues)
- The edgartools dimension guide notes that many filers report face lines only through dimensions (for example Workday COGS "exclusively via `ProductOrServiceAxis`"; "Without dimensional handling: COGS would show as NaN/missing"). — [dimension-handling.md](https://github.com/dgunning/edgartools/blob/main/docs/xbrl/concepts/dimension-handling.md)

### Inferences
- **Mapping the old system's failures** (inference, not tested on those exact filings):
  - Header text ("Jul 26, 2026", "Years ended") does not matter in XBRL, because each fact's period comes from its context's ISO `startDate`/`endDate`/`instant`.
  - An untitled HTML table still has a presentation role with a `definition` (`longname`) and a `menucat`, so it can be found by role and by the tags and axes it contains.
  - Apple's ASU 2023-07 segment table is found by facts on `StatementBusinessSegmentsAxis` × `ConsolidationItemsAxis`, not by layout.
- **Lowest-risk ways to find a note table:**
  - Select facts by tag plus axis/member (for example `RevenueFromContractWithCustomerExcludingAssessedTax` on `srt:ProductOrServiceAxis`), and use the role only to report where the table sits.
  - Matching role names or titles by regex is the fragile step, as edgartools' issue-numbered patterns show.
- **Remaining reliability limits** (inference from the data shapes seen above):
  - Filers choose different tags and members for the same idea (company extension members; `Revenues` at NVIDIA vs `RevenueFromContractWithCustomerExcludingAssessedTax` at Apple).
  - The same fact appears in several roles.
  - FSNDS rounds periods to month end, so exact dates need the instance.

### Gaps
- No published, census-level accuracy figure was found for presentation-based statement reconstruction by any tool, and none was measured here.
- I did not open Microsoft's FY2026 10-K roles to confirm how its HTML "untitled" tables appear in `ren`/FilingSummary.

## Q5. What share of 10-K/10-Q numbers is XBRL-tagged; the SEC rule; MD&A; 8-K

### Takeaway
- **What the rule tags.** Inline XBRL must cover the cover page and the financial statements, including footnotes and schedules (and auditor information in annual reports). Rule 405 detail tagging of notes means every number in the statements and notes is tagged.
- **Newer additions** tag certain narrative items: the cybersecurity Item 1C (`cyd` taxonomy) for fiscal years ending on or after 2024-12-15, and `ecd` items.
- **MD&A is not tagged.** The SEC never required it, and in two measured filings the MD&A contains zero tagged numbers.
- **8-K earnings releases** (EX-99.1) are not tagged; only the 8-K cover page is.
- **Rough share.** About three-quarters of the numeric tokens in a 10-Q or 10-K body are tagged (single-filing regex estimates). Almost all of the untagged numbers sit in MD&A.

### Cited Findings
- SEC tagged content for operating companies: "cover page and financial statement information (including footnotes, schedules, and, in annual reports, auditor information)" in Forms 10-Q, 10-K, certain registration statements, Form 8-K (revised financials) and proxy statements. Inline XBRL phase-in: large accelerated filers for US GAAP fiscal periods ending after June 15, 2019, accelerated filers in 2020, all others by 2021. — [SEC Inline XBRL](https://www.sec.gov/data-research/structured-data/inline-xbrl)
- Rulemaking history — [SEC structured disclosure history](https://www.sec.gov/data-research/structured-data/structured-disclosure-sec-history-rulemaking):
  - XBRL for operating companies became mandatory in 2009.
  - The 2018 rule required Inline XBRL ([33-10514](https://www.sec.gov/rules/final/2018/33-10514.pdf)).
  - "In 2019, the Commission required the cover pages of certain operating company filings to be tagged in Inline XBRL" ([33-10618](https://www.sec.gov/rules/final/2019/33-10618.pdf)).
- Rule 405 notes tagging, as described by a secondary source: all filings must "block and detail tag" the financial statements and footnotes in four levels (each footnote, each significant accounting policy, each table block-tagged; each number in text and tables detail-tagged), effective June 15, 2012 for all filers. — [Colonial Stock Transfer, Basics of XBRL Tagging](https://colonialstock.com/xbrl-tagging.htm). This is a secondary source; I did not read Rule 405's primary text in this session.
- MD&A: in 2020 the SEC's MD&A proposal "did not recommend that the MD&A be formatted in XBRL". XBRL US asked the SEC to "require XBRL block tagging of these topic areas". — [XBRL US comment, April 28, 2020](https://xbrl.us/news/xbrlus-comment-sec-mda/)
- Cybersecurity: for 10-K/20-F, Inline XBRL tagging of Item 1C disclosures begins with annual reports for fiscal years ending on or after December 15, 2024. EDGAR Release 24.3 (September 16, 2024) added the CYD taxonomy. — [Toppan Merrill](https://www.toppanmerrill.com/blog/ixbrl-tagging-of-cybersecurity-disclosures-in-sec-filings-enhances-transparency) (secondary); [SEC 2024 CYD taxonomy notice](https://www.sec.gov/newsroom/whats-new/2409-2024-cyd-taxonomy)
- Measured 2026-10-16, Apple FY2025 10-K instance: 15 `cyd` facts and 5 `ecd` facts, beside 969 us-gaap, 83 custom and 59 dei facts. — [aapl-20250927_htm.xml](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927_htm.xml)
- Tagged share (measured 2026-10-16). Method: regex count of `ix:nonFraction` elements, then numeric-looking tokens outside them (comma-grouped numbers, decimals, percentages ≥2 digits). It is a heuristic over one filing each, and the MD&A boundary is found by the second "Item 2/7 Management's Discussion and Analysis" heading.
  - NVIDIA 10-Q (period 2026-07-26) — [nvda-20260726.htm](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm):
    - 1,002 `ix:nonFraction`, 109 `ix:nonNumeric`, and about 313 untagged numeric-looking tokens, so about 76% of numeric tokens are tagged.
    - The MD&A section has 0 tagged numbers and 236 untagged numeric tokens.
    - The 1,002 tagged numbers equal the 1,002 NUM rows FSNDS holds for this filing.
  - Apple 10-K FY2025 — [aapl-20250927.htm](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm):
    - 969 `ix:nonFraction`, 140 `ix:nonNumeric`, and about 326 untagged numeric-looking tokens, so about 75% are tagged.
    - The MD&A section has 0 tagged numbers and 88 untagged numeric tokens.
- 8-K earnings (measured 2026-10-16), NVIDIA 8-K 0001045810-26-000073 filed 2026-08-26 (Items 2.02, 9.01), isInlineXBRL=1:
  - The cover document `nvda-20260826.htm` has 22 ix tags. The press release `q2fy27pr.htm` (341 KB) and `q2fy27cfocommentary.htm` (257 KB) have 0 ix tags.
  - The filing has a single `R1.htm` (cover page).
  - [NVIDIA 8-K index.json](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000073/index.json); [submissions CIK0001045810](https://data.sec.gov/submissions/CIK0001045810.json)

### Inferences
- **What XBRL replaces.** XBRL covers every number in the statements and notes, including segment, product and geographic tables, which is the class the old regex pipeline failed on. It does not cover MD&A (KPIs, non-GAAP measures, explanations of change) or earnings press releases. Those still need text or table parsing, or a model, and on the earnings day the 8-K press release comes before the 10-Q's tagged numbers.
- **Untagged numbers.** The about 25% of untagged numeric tokens are mostly MD&A. The rest (about 77 tokens at NVIDIA, about 238 at Apple outside MD&A by subtraction) are likely in Items 1A/5/9B, exhibits and the like. I did not classify them.

### Gaps
- I did not read the primary text of Regulation S-T Rule 405 or EDGAR Filer Manual Vol. II Chapter 6 in this session. The four-level detail-tagging description comes from a secondary source.
- No census of the tagged share across many filings was found or run. The 75–76% figures are single-filing regex estimates.
- I did not confirm which other narrative items are now tagged in 10-K/10-Q (for example Item 408 insider-trading arrangements in the `ecd` taxonomy, pay-versus-performance in proxies) or their effective dates. Apple's 5 `ecd` facts show some are present.
- Exceptions where financial statements might be untagged (for example certain non-operating-company forms) were not investigated.

# Extracting numbers from untagged SEC filing tables (MD&A, EX-99.1 earnings releases, other exhibits), 2025–2026

Scope: US SEC filers, state as of October 2026. Besides the web sources, these notes rest on three probes I ran this session at no cost, on public EDGAR data:
- **P1, edgartools earnings parser.** edgartools 5.26.1 (released 2026-03-26) and 5.62.0 (the latest, released 2026-10-11), run on the latest Item 2.02 8-K of NVDA, AAPL and MSFT, plus offline calls to its header and number parsers. Both versions gave identical table output.
- **P2, binding census.** Untagged table cells in the latest 10-Q of AAPL, NVDA and MSFT, matched against the same filing's iXBRL facts.
- **P3, timing census.** For 20 large caps, the gap from each earnings 8-K to the next 10-Q or 10-K, 2024-01 to 2026-10.

The probe scripts (`probe_latest.py`, `binding_census.py`, `binding_census_large.py`, `release_lag_census.py`) ran in the research session's temporary scratchpad and are not kept in this repository.

## 1. Which parts of 10-K/10-Q/8-K carry no XBRL tags, and has the SEC ever required or proposed XBRL for earnings releases?

### Takeaway
Inline XBRL covers the cover page and the financial statements (with notes and schedules) in 10-K and 10-Q. In an 8-K it covers only the cover page and "certain revised financial statements". MD&A tables, the EX-99.1 earnings release and the EX-99.2 presentation or commentary are not tagged. The SEC asked about structuring earnings releases in XBRL in its December 2018 request for comment, but I found no rule or proposal since then that requires it. The May 2026 semiannual-reporting proposal makes the 10-Q itself optional.

### Cited Findings
- The SEC's Inline XBRL page lists what must be tagged for domestic operating companies. It covers the "cover page and financial statement information (including footnotes, schedules, and auditor information in annual reports)" in 10-Q, 10-K and certain registration statements, plus "the cover page and certain revised financial statements in a Form 8-K", proxy pay-versus-performance, resource extraction and filing-fee data. EX-99 press releases are not on the list. Governing releases: 33-10514 (June 28, 2018, Inline XBRL) and 33-10618 (Mar. 20, 2019, FAST Act and cover-page tagging) — [SEC Inline XBRL page](https://www.sec.gov/data-research/structured-data/inline-xbrl)
- MD&A is not on that list either. P2 confirms this on real 10-Qs. AAPL's 10-Q of 2026-07-31 has 9 numeric tables with no `ix:nonFraction` tag, against 19 tagged tables. NVDA's 10-Q of 2026-08-26 has 14 untagged and 32 tagged. MSFT's 10-Q of 2026-04-29 has 13 untagged and 38 tagged — [P2 on AAPL 10-Q](https://www.sec.gov/Archives/edgar/data/320193/000032019326000020/aapl-20260627.htm), [NVDA 10-Q](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm), [MSFT 10-Q](https://www.sec.gov/Archives/edgar/data/789019/000119312526191507/msft-20260331.htm)
- In an earnings 8-K, the XBRL holds only cover-page metadata. NVIDIA's Q2 FY27 8-K (0001045810-26-000073) carries EX-99.1 (`q2fy27pr.htm`), EX-99.2 (`q2fy27cfocommentary.htm`) and only EX-101.SCH/LAB/PRE for the cover page — [P1 attachment listing, NVDA 8-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000073/q2fy27pr.htm). The edgartools source says the same: "8-K filings typically contain only DEI (Document and Entity Information) XBRL metadata, not full financial statements in XBRL format. Actual financial data is in HTML tables within EX-99.1 exhibits" — [edgartools earnings.py](https://github.com/dgunning/edgartools/blob/main/edgar/earnings.py)
- Earnings releases are furnished under Form 8-K Item 2.02, which sits alongside the quarterly reporting requirements — [lawcast / securities-law-blog, Jan 2019](https://securities-law-blog.com/2019/01/15/sec-solicits-comment-on-earnings-releases-and-quarterly-reports/). Information furnished under Item 7.01, including an EX-99.1, is "not deemed filed" for Section 18 purposes — [example 8-K text, CSX 2023](https://www.sec.gov/Archives/edgar/data/277948/000095010323013406/dp199805_8k.htm)
- On December 18, 2018 the SEC published a request for comment (File S7-26-18) on the "nature, content, and timing of earnings releases and quarterly reports". It covered overlap between 8-K earnings releases and the 10-Q, removing duplication, and flexibility in reporting frequency — [Sidley, Dec 2018](https://www.sidley.com/en/insights/newsupdates/2018/12/sec-requests-public-comment-on-earnings-releases-and-quarterly-reports); [Deloitte Heads Up, 2018](https://dart.deloitte.com/USDART/home/publications/archive/deloitte-publications/heads-up/2018/sec-seeks-input-quarterly-reports-earnings)
- That request asked directly (question 10, part 3): "How would the costs of structuring earnings releases in XBRL compare to the costs of complying with the XBRL requirements for Form 10-Q?" XBRL US answered on March 21, 2019. It named obstacles to tagging earnings releases: about 30% of the items in the releases it analysed were non-GAAP and not in the US GAAP taxonomy, and many were industry- or company-specific ("tons of coal sold", "funds from operations"), which would need extension elements. It also opposed letting the 8-K replace the 10-Q, because untagged 8-K data "would adversely affect investors" — [XBRL US comment letter S7-26-18, 2019-03-21](https://sec.gov/comments/s7-26-18/s72618-5177727-183527.pdf)
- The same XBRL US letter, citing Calcbench, says about 60% of public companies file an earnings-announcement 8-K, which is not required. On average, 70% of the elements in releases were GAAP measures that would reappear in the 10-Q — [XBRL US comment letter](https://sec.gov/comments/s7-26-18/s72618-5177727-183527.pdf)
- On May 5, 2026 the SEC proposed letting companies file semiannual reports on a new Form 10-S instead of 10-Qs. The second half would be subsumed in the 10-K, the election is made annually by a box on the 10-K cover, and comments were due July 6, 2026 — [JD Supra summary](https://www.jdsupra.com/legalnews/form-10-q-may-become-optional-sec-5561712/); [Debevoise, May 2026](https://www.debevoise.com/insights/publications/2026/05/breaking-the-quarterly-cycle-sec-proposes-optional); [Deloitte Heads Up 2026](https://dart.deloitte.com/USDART/home/publications/deloitte/heads-up/2026/sec-proposes-semi-annual-reporting)
- EDGAR accepts PDF only as an "unofficial copy" alongside the official filing. HTML documents may embed only GIF and JPG images, so slide decks filed as EX-99.2 can arrive as images inside HTML, or as unofficial PDF copies — [EDGAR Filer Manual Vol. II (search excerpt)](https://sec.gov/file/efmvol2-v25)

### Inferences
- What is reliably untagged: MD&A and other narrative-section tables in 10-K/10-Q, every EX-99.x exhibit in an 8-K (earnings release, CFO commentary, investor presentation), and the non-GAAP and KPI content those carry (about 30% of release items by the 2019 XBRL US count).
- No source shows the 2018 question on XBRL for earnings releases led to any rule. The SEC's current Inline XBRL requirement list (above) still leaves out EX-99.
- If the 10-S proposal is adopted, opting-in companies would have no tagged Q1 or Q3 report. For those quarters, a voluntary earnings release would be the only quarterly source, so the cost of skipping untagged releases would grow. This is not yet final.

### Gaps
- I did not read the full text of the 2026 Form 10-S proposal, so I cannot say whether it raises XBRL for earnings releases or any change to Item 2.02.
- I did not verify which other narrative items (for example Item 1C cybersecurity block-text tagging) now carry tags. The SEC page fetched lists only the categories above.
- I did not measure how often EX-99.2 presentations are image-only versus HTML text.

## 2. Open-source tools that parse EDGAR HTML tables, and which table features they handle

### Takeaway
edgartools is the only maintained open-source library with a dedicated earnings-release table parser. It handles colspan and rowspan, spacer cells, split `$` cells, parenthesised negatives and caption-based scale. On the latest NVDA, AAPL and MSFT releases, though, it reproduces nearly every failure class the old system had: plural "Years ended", abbreviated or split dates, fiscal-calendar periods, same-label rows folded into one, and percent cells shifting columns. The other tools either split filings into sections and leave tables as blobs (sec-parser, the sec-api Extractor, EDGAR-CORPUS), or are generic grid readers (pandas.read_html), or PDF-only (camelot, tabula).

### Cited Findings
**edgartools (Dwight Gunning, MIT licence; latest 5.62.0 released 2026-10-11)**
- API: `eight_k.has_earnings` is "True if Item 2.02 + parseable EX-99.1 exhibit". `eight_k.earnings` returns an `EarningsRelease` with `financial_tables`, `income_statement`, `balance_sheet`, `cash_flow_statement`, `segment_data`, `eps_reconciliation` and `guidance`. Each `FinancialTable` has `dataframe`, `scaled_dataframe` and `scale` (UNITS, THOUSANDS, MILLIONS or BILLIONS); "EdgarTools detects the scale from the document text". Stated caveat: "Some earnings 8-Ks only have narrative text" — [edgartools 8-K docs](https://edgartools.readthedocs.io/en/latest/eightk-filings/)
- The docs' "95%" figure is about 8-K *section detection* ("new parser's section detection (95% accuracy for modern filings)"), not table accuracy. The parser's goals file lists "Table extraction accuracy >95% on validation set" as an unchecked target — [edgartools source: company_reports/current_report.py, documents/docs/goals.md, v5.62.0](https://github.com/dgunning/edgartools/tree/main/edgar)
- Features declared in the source: "Smart column collapsing (removes spacer cells)", "Currency symbol merging ($13,674 instead of $ | 13674)", "Multi-level header preservation", dates in body rows when there is no `<thead>`, and "split date rows where month/day is on one row and year is on the next (e.g., Nvidia's 'October 26,' + '2025')". Statements are classified by keyword scores. Scale is found in this order: caption, headers, first three rows, footer, index labels, then up to three preceding sibling paragraphs. Row labels map to XBRL concepts by exact match against `concept_mappings.json`, with a PascalCase fallback — [edgartools earnings.py](https://github.com/dgunning/edgartools/blob/main/edgar/earnings.py)
- P1 offline parser calls, identical on 5.26.1 and 5.62.0 — [edgartools earnings.py `_parse_period_header`, `_parse_numeric`](https://github.com/dgunning/edgartools/blob/main/edgar/earnings.py):
  - Not parsed (empty period): "Years Ended September 27, 2025" (plural), "Jul 27, 2025" (bare abbreviated month), "13 Weeks Ended March 29, 2025", "Q2 FY26", "Three Months Ended June 30, - 2026" (the joined multi-row header form).
  - Wrong fiscal period. "Three Months Ended Jul 27, 2025" parses as start 2025-05-01, fiscal_period Q3, fiscal_year 2025; NVIDIA calls that quarter Q2 FY2026. "Three Months Ended January 26, 2025" parses as Q1 FY2025; it is NVIDIA's Q4 FY2025. "Six Months Ended Jul 27, 2025" parses as H2. The period start is always the first of a calendar month, never the actual 52/53-week start.
  - Numbers: "(1,234)" gives -1234 and "$(0.09)" gives -0.09, both correct. But "1,234(1)", a value followed by a footnote marker, gives **-12341.0**, a silent wrong number. "—" and "-" give None, not 0. "1,234 (a)" is returned as a string.
- P1 on NVIDIA's Q2 FY27 release (8-K filed 2026-08-26) — [NVDA EX-99.1](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000073/q2fy27pr.htm):
  - 11 tables found. `release.income_statement` returned the GAAP-to-non-GAAP reconciliation table (28×10), not the condensed income statement.
  - The real income-statement table's columns lost the year ("Three Months Ended - July 26,").
  - In the reconciliation table, the "Three Months Ended / Six Months Ended" spanning row stayed as a data row. Bare-date columns were never given a duration, so flow items came out as `period_type='instant'`, and two columns are both named "July 26, 2026" (3-month and 6-month).
  - "GAAP gross margin" shows `75.0 | % | 74.9 | %`: a "%" in its own cell shifted values by one column.
  - The two different rows labelled "Acquisition-related and other costs (A)" (under cost of revenue and under operating expenses) both became concept `AcquisitionrelatedAndOtherCostsA`.
  - April 26, 2026 got fiscal_year 2026; NVIDIA calls it Q1 FY2027.
- P1 on Apple's fiscal Q3 2026 release (8-K 0000320193-26-000018) — [AAPL EX-99.1](https://www.sec.gov/Archives/edgar/data/320193/000032019326000018/a8-kex991q3202606272026.htm):
  - The 3 statements were found and the values are correct.
  - "Products" and "Services" under net sales and again under cost of sales all mapped to the same concepts `Products` and `Services`.
  - "Total net sales (1)" became concept `TotalNetSales1`, keeping the footnote marker.
  - "Gross margin", a dollar amount ($54,770M), was typed as a percentage: unit `pure`, numeric_value 54770, unscaled.
  - The quarter ended June 27, 2026 was labelled fiscal_period **Q2**, with period_start 2026-04-01.
- P1 on Microsoft's FY26 Q4 release (8-K 0001193125-26-323632) — [MSFT EX-99.1](https://www.sec.gov/Archives/edgar/data/789019/000119312526323632/msft-ex99_1.htm):
  - The income-statement values are correct, but every fact has period_type, period_end and fiscal_year = None, because the joined header "Three Months Ended June 30, - 2026" does not parse.
  - One "Three Months Ended / Twelve Months Ended" table was classified BALANCE_SHEET.
  - "Gross margin" was again typed `pure`. Cost-of-revenue "Product" and revenue "Product" share the concept `Product`.
- Version note: 5.26.1 returned `has_earnings=None` on these 8-Ks because `items` was None; 5.62.0 returns True. The table output was otherwise the same — [P1, both versions](https://github.com/dgunning/edgartools/blob/main/edgar/earnings.py)

**sec-parser (alphanome-ai)**
- It parses EDGAR HTML into a tree of semantic elements (section titles, paragraphs, `TableElement`) and is aimed at 10-Q and 10-K. Its sample output summarises a table only as "TableElement: Table with 24 rows, 80 numbers, and 1058 characters". The docs say nothing about cell-level or merged-header parsing, and the project carries a Beta badge — [sec-parser docs](https://sec-parser.readthedocs.io/en/stable/)
- The last PyPI release is 0.58.1, dated 2024-06-09 — [PyPI JSON for sec-parser](https://pypi.org/pypi/sec-parser/json)

**sec-parsers (John Friedman) and doc2dict**
- sec-parsers, "A package to parse SEC filings" into structured XML for LLM, NLP and text use. Last release 0.549 on 2024-07-29 — [PyPI sec-parsers](https://pypi.org/project/sec-parsers/0.536); [PyPI JSON](https://pypi.org/pypi/sec-parsers/json)
- doc2dict's latest release is 0.7.3 (2026-10-05); its PyPI page has no description — [PyPI JSON for doc2dict](https://pypi.org/pypi/doc2dict/json)

**sec-api.io Extractor (commercial, for contrast)**
- It returns any section of a 10-K, 10-Q or 8-K as cleaned text, with tables marked `##TABLE_START`/`##TABLE_END`, or as cleaned HTML with the tables kept. It covers filings since 1994 and claims availability within 300 ms of publication. It extracts sections; it does not parse tables into cells — [sec-api Extractor docs](https://sec-api.io/docs/sec-filings-item-extraction-api)

**EDGAR-CORPUS / EDGAR-CRAWLER (Loukas et al., 2021)**
- 38,009 10-Ks (1993–2020), 6.5B tokens, split into items. The authors "removed all tables to keep only the textual data", so it holds nothing for table extraction — [EDGAR-CORPUS paper](https://ar5iv.labs.arxiv.org/html/2109.14394); [edgar-crawler repo](https://github.com/nlpaueb/edgar-crawler/)

**pandas.read_html / lxml / BeautifulSoup**
- pandas 3.0.6 `read_html` "attempts to properly handle colspan and rowspan attributes". It builds headers from `<thead>`, or else from rows of only `<th>` cells, and warns: "Expect to do some cleanup … We try to assume as little as possible about the structure of the table and push the idiosyncrasies of the HTML contained in the table to the user" — [pandas.read_html docs](https://pandas.pydata.org/docs/reference/api/pandas.read_html.html)
- EDGAR tables often have no `<thead>`, with dates in ordinary body rows (the reason edgartools scans the first 8–10 rows for date-only rows) — [edgartools earnings.py `_extract_date_headers_from_rows`](https://github.com/dgunning/edgartools/blob/main/edgar/earnings.py)

**PDF and image tools (camelot, tabula, table-structure models)**
- These apply only to unofficial PDF copies or image renderings, since official EDGAR documents are HTML or text (see Q1). Camelot and tabula-py are PDF table extractors — [camelot repo](https://github.com/camelot-dev/camelot); [tabula-py repo](https://github.com/chezou/tabula-py) (not tested here)

### Inferences
- edgartools gives a reasonable HTML-to-grid layer: span expansion, `$` and parenthesis merging, spacer removal and scale cues. Its *meaning layer* — period parsing, statement choice, label-to-concept, row typing — fails on exactly the classes that broke the old system. Plural headers, abbreviated or split dates, fiscal calendars, same label under different parents, and "%" in separate cells all appear in P1 on three mega-cap releases. Adopting it would not remove those failure classes; it would move them into a dependency.
- Two silent-wrong-number behaviours make any code path unsafe without a verifying check: `1,234(1)` → -12341, and gross margin typed as a percentage. A code path needs a closed set of accepted cell shapes, where anything else is refused rather than guessed.
- None of these open-source tools emits (metric, period, unit) facts for MD&A tables with a correctness guarantee.

### Gaps
- I did not test edgartools on 10-Q MD&A tables (its `TenQ` and `documents` path), only on 8-K earnings tables.
- I did not test sec-parser, doc2dict or sec-parsers on real tables.
- I found no documentation for ExtractTable (commercial OCR) and did not check `secedgar` (believed to be a downloader with no table parsing).
- I did not check how edgartools handles tables split across a page break in HTML (repeated header rows).

## 3. Reported accuracy and benchmarks for financial table extraction

### Takeaway
The public benchmarks measure table structure from PDF or images (FinTabNet, TEDS scores of 93–99%), or question answering over tables already extracted (TAT-QA, FinQA, FinanceBench). None measures parsing EDGAR HTML tables into (metric, period, unit) facts. The closest is FinTagging (2025, 2024 10-K iXBRL). There, LLMs find numbers fairly well (best F1 0.72) but map them to US-GAAP concepts poorly (best accuracy about 17%).

### Cited Findings
- **FinTabNet** (IBM, v1.0.0, Nov 2020): 89,646 pages and 112,887 tables from S&P 500 annual reports, split 91,596 / 10,656 / 10,635. Cell-structure labels came from token matching between the PDF and HTML versions of each filing — [IBM FinTabNet](https://developer.ibm.com/exchanges/data/all/fintabnet)
- **TableFormer** on FinTabNet (image input): TEDS 93.6% overall (95.4 simple, 90.1 complex) — [TableFormer, arXiv 2203.01017](https://arxiv.org/pdf/2203.01017). A secondary review reports TABLET at 98.54% TEDS on the original FinTabNet test set and 98.87% on a refined one — [review of TABLET](https://www.themoonlight.io/en/review/tablet-table-structure-recognition-using-encoder-only-transformers) (secondary source; not checked against the paper)
- **TAT-QA** (ACL 2021): 16,552 questions over 2,757 hybrid table-and-text contexts from annual reports. The TAGOP baseline scored 58.0 F1 against 90.8 F1 for human experts — [TAT-QA, arXiv 2105.07624](https://arxiv.org/pdf/2105.07624). A 2026 summary says a fine-tuned LLaMA-2 Extractor→Reasoner→Executor pipeline (TAT-LLM) beat zero-shot GPT-4 on TAT-QA and FinQA in 2024 — [Bean Labs TAT-QA log, 2026-05-14](https://beancount.io/bean-labs/research-logs/2026/05/14/tat-qa-hybrid-tabular-textual-financial-question-answering)
- **FinQA** (EMNLP 2021): 8,281 QA pairs built from 2,789 pages of S&P 500 earnings reports, 1999–2019. Human experts reached 91.16% execution accuracy — [Bean Labs FinQA log, 2026-05-13](https://beancount.io/bean-labs/research-logs/2026/05/13/finqa-numerical-reasoning-financial-data); [FinQA ACL anthology](https://preview.aclanthology.org/setup/2021.emnlp-main.300)
- **FinanceBench** (Patronus AI, Nov 2023): 10,231 questions on public filings, 16 model setups tested on 150 cases (2,400 answers reviewed by hand). GPT-4-Turbo with retrieval "incorrectly answered or refused to answer 81% of questions" — [FinanceBench, arXiv 2311.11944](https://arxiv.org/abs/2311.11944v1)
- **FinTagging** (May 2025): 30 10-K reports filed in 2024, holding 81,325 facts, 5,450 tables, 3,245 annotated table sequences and 52,740 numeric entities linked to 2,288 US-GAAP concepts. Numeric identification: best F1 0.7238 (DeepSeek-V3: P 0.63, R 0.85) and 0.6022 for GPT-4o. Concept linking accuracy: 0.1715 (DeepSeek-V3), 0.1664 (GPT-4o), 0.1072 (Qwen2.5-14B). LLMs "struggle with fine-grained concept alignment, particularly in disambiguating closely related taxonomy entries" — [FinTagging, arXiv 2505.20650 v1 HTML](https://arxiv.org/html/2505.20650v1)
- Vendor claims (Reducto, 2026-06-08; sources not checked): on FinTabNet, models get "the exact table structure right only 42% of the time". AI misread numeric scale ">8%" of the time on plain text versus "0.11%" on XBRL. On FinCriticalED, GPT-4o scored 59.6% on numeric-fact questions despite >90% text accuracy — [Reducto blog](https://reducto.ai/blog/10k-document)

### Inferences
- TEDS measures structure, not whether the right number lands under the right period and label. A 93–99% TEDS score does not translate to fact-level accuracy, and EDGAR HTML already has the structure that image models have to recover.
- The FinTagging split mirrors the decision ahead. Models find the numbers but cannot reliably name them in taxonomy terms, which argues for letting code or XBRL own identity and units rather than a model.
- No measured accuracy exists for any tool on EDGAR HTML MD&A or EX-99.1 tables. A team that needs one has to build a small gold set itself, for example by withholding 10-Q iXBRL facts, as in P2.

### Gaps
- I found no EDGAR-HTML-specific table parsing evaluation, academic or practitioner.
- I did not find PubTabNet's own headline numbers or current TAT-QA and FinQA leaderboard scores for 2025–2026 frontier models.

## 4. How practitioners map an untagged table cell to (metric, period, unit) deterministically, and the pitfalls of "binding" to XBRL facts

### Takeaway
The deterministic recipe has five parts: expand spans into a grid; push spanning headers ("Three Months Ended") down onto the date cells under them; parse dates in any month form and join split rows; take scale from caption, header or nearby paragraph; and type each row (amount, per-share, shares, percent). Each part has failure classes that P1 confirms on mega caps. Binding untagged cells to iXBRL facts in the same 10-Q by equal displayed value labels 60–78% of cells with three or more digits, with 0–8% ambiguous. It labels only about half to three-quarters of all cells, and small numbers collide often.

### Cited Findings
- Header-normalisation pitfalls, shown on edgartools (P1):
  - **Plural and variant headers.** "Years Ended" (Apple's form), "13 Weeks Ended" and "Q2 FY26" do not parse.
  - **Abbreviated or split dates.** Bare "Jul 27, 2025" does not parse. The partial-date matcher accepts full month names only. A multi-row header joined as "June 30, - 2026" does not parse.
  - **Fiscal calendars.** Quarter numbers come from the calendar month (NVIDIA's July quarter becomes Q3, its January quarter Q1), and fiscal_year is the end-date year — [edgartools earnings.py](https://github.com/dgunning/edgartools/blob/main/edgar/earnings.py)
- Scale pitfalls: scale is matched as the substring "million" or "thousand" anywhere in a header cell. Per-row typing decides what to scale: "per share" rows become PER_SHARE, but any label containing "margin" becomes PERCENTAGE. Apple's and Microsoft's dollar "Gross margin" came out unscaled with unit `pure` — [P1, edgartools 5.62.0 on AAPL and MSFT](https://github.com/dgunning/edgartools/blob/main/edgar/earnings.py)
- Same-label pitfall: when labels are not qualified by their parent rows, repeated labels collapse. Apple's "Products" and "Services" under net sales and under cost of sales, NVIDIA's "Acquisition-related and other costs (A)" under cost of revenue and under opex, and Microsoft's "Product" all collapse. This is the same class as the old system's "Percentage of total net sales" fold — [P1](https://github.com/dgunning/edgartools/blob/main/edgar/earnings.py)
- Cell-shape pitfalls: footnote markers glued to values (`1,234(1)` → -12341), "%" in separate cells shifting columns, and dashes read as null rather than zero — [P1](https://github.com/dgunning/edgartools/blob/main/edgar/earnings.py)
- Binding census (P2). A cell counted when it is a number in a table with no `ix:nonFraction`. A match means its displayed digits equal the displayed digits of at least one iXBRL fact in the same 10-Q, ignoring period, sign and scale:
  - **AAPL** (10-Q 2026-07-31): 140 cells; 86 matched (61%); 6 of those (7%) matched facts of more than one concept. Among cells with 3 or more integer digits: 87 cells, 68 matched (78%), 0 ambiguous — [AAPL 10-Q](https://www.sec.gov/Archives/edgar/data/320193/000032019326000020/aapl-20260627.htm)
  - **NVDA** (10-Q 2026-08-26): 258 cells; 128 matched (50%); 33 ambiguous (26% of matched). With 3 or more digits: 151 cells, 90 matched (60%), 7 ambiguous (8%) — [NVDA 10-Q](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm)
  - **MSFT** (10-Q 2026-04-29): 213 cells; 158 matched (74%); 20 ambiguous (13%). With 3 or more digits: 169 cells, 131 matched (78%), 5 ambiguous (4%) — [MSFT 10-Q](https://www.sec.gov/Archives/edgar/data/789019/000119312526191507/msft-20260331.htm)
  - **Ambiguity examples:** small integers such as "3", "4" and "6" equal unrelated facts at once (for example `AvailableForSaleDebtSecuritiesAccumulatedGrossUnrealizedLossBeforeTax`, `OtherCommitmentDueInFourthYear` and `RevenueRemainingPerformanceObligationPercentage`) — [P2](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm)
- Earnings-release values can differ from the later 10-Q or 10-K, so binding a release cell to a later XBRL fact can disagree on real data. Calcbench's example via XBRL US: AmerisourceBergen's fiscal 2017 net income was $50M (12%) lower in the 10-K ($364.5M) than in the earnings 8-K, because severance and litigation expense rose — [XBRL US comment letter](https://sec.gov/comments/s7-26-18/s72618-5177727-183527.pdf)

### Inferences
- **Binding works for GAAP lines of three or more digits that MD&A repeats from the statements.** It labels them and checks them at the same time. It cannot label values found only in MD&A, such as segment KPIs, percent changes and constant-currency rows, which made up 22–40% of cells with three or more digits in P2. It also cannot label small numbers on value alone. Equal values do not prove identity, so a binding should also require the same period (from the column header) and the same scale before it is accepted.
- **A rule set that holds:** (a) a full grid with spanning headers propagated; (b) each row's label path = parent heading(s) + label, so same-label rows stay distinct; (c) period = a closed set of header forms (Three/Six/Nine/Twelve Months, Quarter, Year or Years, N Weeks Ended; full or abbreviated month; split rows joined), with fiscal period taken from the filer's own fiscal-year end in XBRL dei or the 10-K, not the calendar; (d) a closed set of numeric cell shapes, with everything else refused; (e) scale from caption or nearby text, with per-share, share-count and percent rows exempt by unit rather than by label word.
- The old system's failures fall into these classes: NVIDIA's abbreviated months (c), Apple's "Years ended" (c), Microsoft's untitled tables (statement choice), segments as columns (header propagation), and the folded "Percentage of total net sales" rows (b). The same classes appear in the maintained open-source tool (P1), so they are properties of the documents, not one-off bugs.

### Gaps
- P2 ignores periods and contexts and was run on three filings. A period-aware census across many filings is needed before treating 60–78% as a rate.
- I found no published practitioner write-up of value-equality binding between untagged MD&A cells and XBRL facts.

## 5. Hybrid approaches: code extracts structure and a model labels it, or a model extracts and code verifies

### Takeaway
Practitioner reports agree on one point: most wrong numbers come from parsers that flattened the table before the model saw it. They recommend keeping the structure and verifying every number. There are few measured results. Published hybrids either constrain model output to a strict schema (dottxt/Outlines), validate with the table's own totals hierarchy (an ICAIF 2025 paper on fiscal PDFs), or add citation-backed verification (Reducto, a vendor). None reports fact-level accuracy on EDGAR HTML.

### Cited Findings
- dottxt converts 10-K HTML to markdown (`markdownify`), classifies which pages hold the income statement, then uses Outlines structured generation with Phi-3.5-mini to emit a regex-constrained CSV (`year,revenue,operating_income,net_income`). It was tested on Microsoft, NVIDIA and Alphabet against hand-extracted values, with no accuracy figure given. It warns that LLMs "can invent information" — [dottxt blog](https://blog.dottxt.ai/extracting-financial-data.html)
- Reducto (vendor, 2026-06-08) lists the 10-K failure modes as scale loss, parenthetical negatives misread, headers split from data across pages, footnote links cut by chunking, and multi-column interleaving. It recommends a vision model for layout, a VLM for reading, and "an agentic verification layer" with bounding-box and page citations — [Reducto blog](https://reducto.ai/blog/10k-document)
- A search summary of practitioner reports states that numbers coming back from 10-Ks were wrong "because the parser had already lost the structure before the LLM ever touched the data". It also cites a case where three commercial extractors gave $8.4 billion, $8.4 million and a value not in the document for the same line item. I could not trace this to a primary page; Reducto's article does not contain it — [search results incl. Reducto, Superlinked](https://reducto.ai/blog/10k-document) (unverified)
- Aggarwal et al. (ICAIF 2025 workshop; Karnataka fiscal PDFs, not SEC filings) use LLM extraction plus "multi-level validation checks" built on "the inherent structure of fiscal tables, with totals at each level of the hierarchy" — [arXiv 2511.10659](https://arxiv.org/abs/2511.10659v1)
- FinTagging shows models extract numbers better than they label concepts (F1 0.72 versus accuracy 0.17), which supports keeping labelling decisions out of the model where code or XBRL can make them — [FinTagging](https://arxiv.org/html/2505.20650v1)
- edgartools offers model-ready output, "markdown prose plus financial statements as lossless HTML, preserving every reported value" (its MCP recipe) — [edgartools search summary / app.edgar.tools recipe](https://app.edgar.tools/mcp/recipes/earnings_release_decoder)

### Inferences
- **The hybrid best supported by the evidence:**
  1. Code builds the grid from HTML, with spans expanded, cell text kept verbatim, and each cell given a stable (table, row, column) id.
  2. Code labels everything it can decide: period from a closed header grammar, scale, and binding to same-filing XBRL where value, period and scale all match.
  3. A model is asked only for what is left (which row is which non-GAAP metric, which column is which segment) and must answer with cell ids, not numbers.
  4. Code checks every model claim against the grid (the cited cell exists and its parsed value is the one used) and against the totals (components sum to the total, within rounding).

  This keeps numbers out of the model, which is the failure every source warns about. It is an inference: no source measures this exact design on EDGAR.
- "A model extracts, then code verifies by searching the source text" catches invented numbers. It does not catch a correct number attached to the wrong period or the wrong row, the dominant failure in P1. Verification therefore has to be cell-addressed, not by substring.

### Gaps
- I found no measured comparison of code-only, model-only and hybrid on EDGAR earnings releases or MD&A tables, nor any Hacker News or Reddit thread with numbers. The r/algotrading thread found is about XBRL deduplication, not tables — [r/algotrading thread](https://lr.eu.psf.lt/r/algotrading/comments/1ha15eo/parsing_edgar_xbrl)

## 6. Timing: are earnings releases published before the 10-Q, and by how much for large caps?

### Takeaway
Yes, but for most mega caps the gap is 0–1 days. In P3 the median for 20 large caps from 2024 to 2026 was 1 day to the 10-Q and 9.5 days to the 10-K. A tail of companies waits 1–4 weeks: Walmart, UnitedHealth, JPMorgan, Home Depot, Costco, Chevron and J&J. Using only 10-Q XBRL mainly loses (a) non-GAAP and KPI content, about 30% of release items, which never reaches XBRL, and (b) days to weeks of lead time for the tail companies and for Q4, where the 10-K arrives later.

### Cited Findings
- XBRL US, citing Calcbench, gives the average lag from earnings 8-K to 10-Q as 3.4 days in 2018 and 3.7 days in 2017. In 2018 the 8-K came on average 33.6 days after period end and the 10-Q 37 days after — [XBRL US comment letter, 2019](https://sec.gov/comments/s7-26-18/s72618-5177727-183527.pdf)
- Society for Corporate Governance (Feb 2023, 30 SV150 companies): the spread from earnings release averaged one day for the 10-Q (range 0–14 days) and about 15 days for the 10-K (range 0–44). Releases come mostly midweek, 10-Qs and 10-Ks mostly on Fridays — [SCG blog, 2023-02](https://www.societycorpgov.org/blogs/randi-morrison/2023/02/21/earnings-releases-and-forms-10-q10-k-timing-practi)
- P3 (EDGAR submissions API; each Item 2.02 8-K filed 2024-01-01 to 2026-10-16 paired with the first 10-Q or 10-K filed on or after it, within 60 days; 20 large caps) — [data.sec.gov submissions API, e.g. AAPL](https://data.sec.gov/submissions/CIK0000320193.json):
  - **10-Q:** n=165, median 1 day, mean 5.3, range 0–28, same day 15%.
  - **10-K:** n=58, median 9.5 days, mean 13.7, range 0–55.
  - **Same day:** MSFT (all), NVDA (all but one 7-day gap), PG.
  - **+1 day:** AAPL, AMZN, GOOGL, META, V, ORCL.
  - **+2–8 days:** XOM (3), KO (1–6), HD (7–8), COST (6–7), AVGO (6–8), CVX (5–6, once 28), JNJ (mostly 8).
  - **+8–25 days:** WMT (8–22), UNH (13–25; 10-K 34–47), JPM (17–23).
  - **10-K lags in the tail:** WMT 22–24, HD 22–24, JNJ 21–24, CVX 21–55, UNH 34–47.
- XBRL US's 2019 summary: "the earnings announcement is typically published sooner than the 10-Q" and "contains non-GAAP data" that the 10-Q does not; about 30% of release items were non-GAAP — [XBRL US comment letter](https://sec.gov/comments/s7-26-18/s72618-5177727-183527.pdf)

### Inferences
- For a product that tracks mega-cap tech, 10-Q XBRL usually arrives within a day of the release, so little *time* is lost. What is lost is *content*: non-GAAP measures, guidance, KPIs and segment detail found only in the release. That loss persists whatever the timing.
- **P3 caveats.** Item 2.02 also covers pre-announcements and operational updates, so some gaps are not earnings-to-10-Q. Tesla's alternating 21–22 and 1-day gaps fit a deliveries 8-K about 3 weeks before the 10-Q and an earnings 8-K 1 day before. JPM had only 3 pairs because its "recent" filings array is cut short by its volume of filings. Treat P3 as a census of 20 names, not a market rate.

### Gaps
- I did not measure the gap for mid and small caps, or compute the share of the S&P 500 filing the 10-Q on the same day.
- I did not measure how often release numbers are revised before the 10-Q beyond the single 2017 Calcbench example.

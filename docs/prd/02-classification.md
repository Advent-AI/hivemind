# Classification (upstream)

> Status: first version frozen, October 18, 2026. English edition: October 25, 2026 (D163).
> Design page: `docs/system-design.html` → New → Classification. Recorded decisions take precedence over this PRD.

## Purpose

Upstream labels each item with a classification result, text/table form and related subjects. Most results are one of 16 categories; others are duplicate, not source material or invalid. Upstream follows this specification. Dispatch checks completeness and category validity without classifying again.

The old system defined categories in nine modules and twelve collections, which disagreed. This design owns one definition; consumers read the category and its attributes.

## Scope

Produce exactly one result, identify related subjects and specify input fields. Do not use a model, decide research scope (the universe owns that), or read incidentally mentioned companies from the body (extraction owns that).

## The 16 categories

<!-- generated: tags -->
| ID | Category | Form | Family | Decision rule | Example |
|---|---|---|---|---|---|
| T1 | Earnings releases | Text and tables | Company publications and filings | Text: exhibits named by 8-K Item 2.02, fiscal-results exhibits in 6-K, exchange earnings announcements and sources labelled as earnings. Tables: datasets registered as earnings figures. | Apple quarterly earnings release, Tesla update deck, guidance history |
| T2 | Periodic reports | Text and tables | Company publications and filings | Text: 10-K, 10-Q, 20-F, 40-F and ARS, including /A amendments; exchange annual, interim and quarterly reports; sources labelled as periodic reports. Tables: standardised financial statements. Do not separately ingest XBRL facts already in the filing. | Meta 10-K, 10-K/A, standardised income statement |
| T3 | Legal and capital-markets documents | Text | Company publications and filings | Proxy, financing, M&A and tender-offer filings regardless of filer; exhibits numbered 2, 3, 4 or 10; exchange circulars; sources labelled as legal documents. | DEF 14A, activist DEFC14A, 424B5, merger agreement, credit agreement |
| T4 | Company-call transcripts | Text | Company publications and filings | Transcripts of company-hosted calls or company presentations at investor conferences; merger calls in 425 filings. | MSFT earnings call, NVDA fireside chat at a broker conference |
| T5 | Presentations | Text | Company publications and filings | Company slides: presentations under 8-K Item 7.01 or in 425 filings, and IR-site slides that are not earnings releases. | Investor-day deck, IR-site presentation not labelled as earnings |
| T6 | Other company publications | Text and tables | Company publications and filings | Text: remaining company files, including 8-K bodies and other exhibits, remaining 6-K content, SEC response letters, late-filing notices, press releases and official posts. Tables: IR supplements and monthly operating data. | Executive-change 8-K, quarterly delivery announcement, IR KPI table |
| T7 | News | Text | Media reporting | Material authored by media, with no registered publication series and no opinion or analysis section. A missing section defaults to news. | Reuters report, CNBC CEO interview, DigiTimes supply-chain report |
| T8 | Opinion and analysis | Text and tables | Opinion and dialogue | Text: registered forecast, outlook or research series regardless of author; media opinion/analysis sections; analyst-authored text other than dialogue records; all individual-authored text; investor letters to boards in filings. Tables: forecasts, ratings, price targets, consensus and investor-sentiment surveys. | Sell-side initiation, short report, IMF World Economic Outlook, Reddit post, FY2027 EPS consensus, personal earnings model |
| T9 | Interview records | Text | Opinion and dialogue | Analyst-authored transcripts or meeting notes. | Expert-network interview, CFO meeting notes |
| T10 | Official actions and records | Text and tables | Official actions and macro statistics | Text: official series registered as actions or records; official authors without a registered series; SEC comment letters and court dockets. Tables: government-published records. | European Commission decision, FTC complaint, SEC comment letter, defence contract award, patent grant |
| T11 | Macro policy and statistics | Text and tables | Official actions and macro statistics | Text: registered monetary-policy or statistical series, whether public or private. Tables: macro statistics and policy rates. | FOMC statement, Beige Book, CPI and payrolls, ISM PMI, federal funds rate |
| T12 | Market prices and trading | Table | Market and measurement data | Datasets registered as prices and trading. | Daily prices, option implied volatility, 10-year Treasury yield |
| T13 | Holdings and flows | Table | Market and measurement data | Datasets registered as holdings and flows; table versions of ownership filings. | Institutional holding changes, insider sales |
| T14 | Calendar | Table | Market and measurement data | Datasets registered as scheduled dates. | Next earnings date, FOMC meeting date |
| T15 | Third-party measurements | Table | Market and measurement data | Datasets registered as measured activity. | App downloads, card-spending data |
| T16 | Reference data | Table | Market and measurement data | Datasets registered as identities and classifications. | Ticker-to-CIK mapping, GICS classification, S&P 500 weights |
<!-- /generated: tags -->

### Category definitions

<!-- generated: definitions -->
- **T1 Earnings releases**: Earnings releases for a quarter, half-year or full year. Text includes exhibits named by 8-K Item 2.02 (earnings releases, shareholder letters, CFO commentary, update decks), explicitly identified fiscal-results exhibits in 6-K, exchange earnings announcements and sources labelled as earnings. Tables include release-day results and guidance, including guidance history. Monthly operating data belongs to T6. Merge republications of the same release with the original.
- **T2 Periodic reports**: Text: 10-K, 10-Q, 20-F, 40-F and ARS, including amendments that name the replaced version; exchange annual, interim and quarterly reports; sources labelled as periodic reports. Tables: vendor-standardised statements and segment data, identifying the source report. Do not separately supply XBRL facts already in those reports. Annual versus quarterly is an attribute.
- **T3 Legal and capital-markets documents**: Proxy materials, including both sides of a proxy contest; financing, M&A and tender-offer filings and amendments, including acquirer and private-equity filings, regardless of filer. Include SEC exhibit categories 2, 3, 4 and 10 (acquisition agreements, charters, security/debt instruments and material contracts), exchange circulars and sources labelled as legal documents. Read terms and each party's statements; attribute statements to the submitting party.
- **T4 Company-call transcripts**: Company-hosted earnings calls, investor days and company podcasts; company presentations at investor conferences; merger calls in 425 filings. Media-hosted events belong to T7. Venue and transcript provider are attributes.
- **T5 Presentations**: Company slide decks and PDF presentations under 8-K Item 7.01 or in 425 filings, and IR-site decks that are not earnings releases. Sources labelled as earnings belong to T1.
- **T6 Other company publications**: Text not covered above: 8-K bodies, exhibits not named in the earnings item, other items, remaining 6-K content, SEC response letters and late-filing notices; press releases, operating updates, ESG reports, newsrooms, blogs, IR/product pages and official company social posts. Tables: company-published supplementary information and monthly operating data, such as IR Excel or CSV files.
- **T7 News**: Media publications other than opinion and analysis: news, interviews, podcast transcripts, media-hosted events such as WSJ Tech Live, and media-account posts. General, financial and trade media all qualify. A missing section defaults to news. Opinion and analysis sections belong to T8. Registered media series follow their registered category, such as Reuters economist surveys in T8.
- **T8 Opinion and analysis**: Attributed opinions and analysis regardless of author, length or platform. Text includes sell-side and independent research, rating agencies, industry research, think tanks and academia; official and international-organisation forecasts, outlooks and research such as the IMF World Economic Outlook, CBO Budget Outlook and central-bank working papers; fund letters, short reports and investor letters to boards in filings; media opinion; personal posts and essays; and the user's investment memos. Tables include analyst forecasts and revisions, ratings, targets, consensus, credit/ESG ratings, economist and official forecasts including GDPNow nowcasts, investor-sentiment surveys, industry estimates and forecast upload templates. Opinions and estimates remain attributed statements, not completed facts. The user's own opinions become candidate theses, not evidence.
- **T9 Interview records**: Dialogue recorded by analysts: expert-network interviews, management meetings arranged by the user and channel checks. The form is a transcript or notes. Attribute statements to the original speaker; the recorder is an attribute. Company-hosted events and company presentations at investor conferences belong to T4.
- **T10 Official actions and records**: Official material not classified elsewhere. Text includes regulatory, judicial, legislative, administrative and exchange documents and proceedings: rulings, approvals, recalls, regulations, sanctions, export controls, tariffs, contract awards, hearing/trial transcripts, SEC comment letters and court dockets. Tables include government records of contracts, lobbying, political donations, patents, litigation, recalls and customs bills of lading. Official forecasts, outlooks and research belong to T8; statistics belong to T11. Officials' personal accounts count as official during their tenure, such as a president announcing tariffs. Attribute quoted statements to their original speaker or submitting party.
- **T11 Macro policy and statistics**: Text registered as monetary policy or statistics, regardless of publisher: central-bank statements, minutes, speeches, dot plots and Beige Books; official CPI/jobs releases and private ISM PMI, ADP employment and Michigan sentiment releases. Tables: economy-wide or industry-wide statistics and policy rates, public or private, each with a publication date; retain earlier revisions. Include composite measures we cannot calculate because weights are unavailable, such as LEI and financial-conditions indices. Market interest and exchange rates belong to T12; measurements of specific companies, products, locations, chains and protocols belong to T15.
- **T12 Market prices and trading**: Prices and trading in stocks, ETFs, option chains, futures, interest rates, FX, commodities, cryptocurrencies, credit spreads, CDS and prediction markets; corporate actions such as dividends and splits; share capital.
- **T13 Holdings and flows**: Market-participant holdings and flows: table versions of Form 4, 13D/G, 13F and 144; short interest, borrow fees and utilisation; ETF/fund flows; CFTC positioning; cryptocurrency whale and smart-money holdings.
- **T14 Calendar**: Scheduled dates for earnings, investor days, launches, macro releases, central-bank meetings, court/regulatory deadlines, index rebalancing, lock-up and token unlocks, and option expiries.
- **T15 Third-party measurements**: Vendor-measured activity for specific companies, products, locations, chains and protocols: card spending, app usage, web/search/foot traffic, satellite and shipping data, hiring, scraped prices, reviews and on-chain usage/revenue. These are measurements, not estimates. Industry estimates and forecasts belong to T8; economy-wide or industry-wide statistics belong to T11.
- **T16 Reference data**: Company and asset identities, industry classifications, corporate structure, supply-chain relationships, index constituents and weights. No subject tracks this category by default. Upstream uses identity references to resolve subjects.
<!-- /generated: definitions -->

## Decision order

<!-- generated: routing -->
1. First validate: missing required metadata, malformed subject identifiers, unreadable text or the system's own output → invalid. Previously received identical content without an explicit replaced version → merge with the original.
2. Table data: register each dataset's category once at onboarding rather than judging every record. Split registration by field when an interface returns multiple kinds of content. All later records use that category. Unregistered datasets are invalid and go to human review.
3. Text filings (SEC, exchange, court): use the filing-system code table regardless of filer. Unknown codes are invalid and go to human review.
4. Other text with a registered publication series: use the series table (T8, T10 or T11), regardless of author type. An unregistered series name goes to human review while classification continues normally.
5. Remaining text: resolve author type from the author table valid on the publication day, falling back to the channel default; then use section or genre. Official authors without a registered series → T10. Unresolved author type → invalid and human review.
<!-- /generated: routing -->

## The four lookup tables

<!-- generated: lookup -->
| Table | Lookup input and result | Example |
|---|---|---|
| Dataset table | Dataset → category or not source material | Daily prices → T12; financial statements → T2; ISM PMI and LEI → T11; GDPNow → T8; technical indicators and fear/greed index → not source material |
| Filing-code table, one per filing system | Filing code → category; 8-K, 6-K, 425 and ownership filings require additional rules | 10-K → T2; DEF 14A → T3; 8-K → inspect items and exhibits |
| Publication-series table | (author, series) → T8, T10 or T11. Any author can register a series; T10 is official only. | FOMC statements, Beige Book, ISM PMI → T11; IMF World Economic Outlook, CBO Budget Outlook → T8; OFAC sanctions announcements → T10 |
| Author table | Author → company, media, analyst, official or individual, with a validity period. Fall back to the channel default when unresolved. | Reuters → media; Morgan Stanley → analyst; IMF → official; president's personal account during tenure → official |

- Keep all four tables in one JSON file read by production and tests. Changing a table creates a new classification version.
- The first three tables return a result directly: category, not source material, or further rules such as 8-K. No intermediate name. The author table returns author type, not category: Reuters news is T7 and opinion is T8; section, genre or series still matters.
- Dataset and series registration follow the same principles: public/private statistics → T11; central-bank monetary-policy/economic statements, minutes, speeches, dot plots and Beige Books → T11; central-bank research and working papers → T8; forecasts, outlooks and research → T8; actions and records → T10, official only. For measured activity datasets, economy/industry-wide → T11; specific company, product, location, chain or protocol → T15.
- Validate table values at load: dataset → one of 16 categories or not source material; filing code → category or rule; series → T8, T10 or T11, with T10 official only; author → one of five author types. Invalid values prevent startup.
- Do not guess missing datasets, filing codes or series; send them to human review for registration. Missing authors use channel defaults first and reach human review only if still unresolved.
- Identifier-to-subject mappings, such as AAPL → Apple, are not classification tables. They resolve subjects and validate the universe, not categories. Upstream owns this mapping; details are deferred.
<!-- /generated: lookup -->

## Related subjects

<!-- generated: objects -->
1. Four subject kinds, matching the research universe: company, cryptocurrency, commodity and theme. An item may concern several subjects or none.
2. Use only channel-supplied identifiers and their stated reasons, plus the author when it is a company: the issuing company for a release or the company speaking at its meeting. Record why each subject is attached. An empty or unsupported identifier kind or reason invalidates the whole item.
3. Keep identifier kinds separate because equal strings can mean different subjects: companies use CIK, ticker or company name; cryptocurrencies and commodities use their own symbols; themes use theme IDs.
4. Themes have only two origins: upstream delivery for that theme or explicit identification at upload. Do not infer them from the body text.
5. Read identifiers, not body text or URLs. A filing agent's identifier can appear in a URL; an old Amazon 8-K URL contains agent ID 1104659.
6. Resolve company, cryptocurrency and commodity identifiers through reference data. Pad CIK to 10 digits; resolve tickers as of publication day (FB identified Meta before June 9, 2022); accept only registered company aliases. Resolve theme IDs through the theme library. Preserve unresolved identifiers as received, mark them unresolved and continue processing; fill them after registration.
7. A non-company author (media, analyst, official or individual) is not itself a subject. Preserve both filer and filing subject with their roles: in a 13D, the activist is the filer and the held company is the subject.
8. Do not label incidentally mentioned companies or themes here. Extraction associates them with specific theses and evidence.
9. When merging a duplicate, union both items' subjects and deduplicate them. Subjects do not affect category. Invalid items and non-source material receive no subjects.
<!-- /generated: objects -->

## Time rules

<!-- generated: time -->
1. Use the New York publication day. Time of day matters only for SEC filing-day calculation (rule 4). Processing order follows dispatch sequence, not publication time.
2. Each item uses one date: publication day. Its described fiscal or observation period is an attribute. The stream has no concept of today's date; only pull mode acts on time.
3. Do not separately record a channel delay of several days. No rule uses the computer clock; receipt time is for audit only.
4. SEC publication day is the legal filing day. Acceptance before 5:30 p.m. uses that day; after 5:30 p.m., SEC publication is next business morning, so use the next business day.
5. Merged duplicates use the earliest publication day: knowledge begins when the market could first see it.
6. Corrections, updates, restatements, edits and category changes create new versions without overwriting old ones.
7. An item without publication time cannot be placed on the timeline and is invalid.
<!-- /generated: time -->

## Classification rules

<!-- generated: rules -->
1. Category describes what the information is. Text/table form, length, platform and channel are attributes. A category can have both forms; form only determines whether classification uses the dataset table or text rules.
2. Each item has exactly one result: a category, merge with the original, not source material, or invalid with a reason. Use fixed rules and lookup tables, not a model.
3. The author is responsible for the content. Wires, republication sites, transcript providers, data vendors, social/contributor platforms, EDGAR filing agents and user uploads are delivery channels.
4. Resolve author type from the author table, then channel defaults: news indices default to media, wires to company, and social/contributor/newsletter accounts to individual. Only an unresolved result after both is invalid. Registration is an attribute. International organisations such as IMF, World Bank, OECD, OPEC and WTO are official.
5. Author-table entries have validity periods evaluated on publication day. Status follows tenure, not influence: an account is official during office and individual during campaigning, before inauguration or after leaving office.
6. Registered publication series take precedence over author type: ISM PMI → T11; Reuters economist survey → T8; CBO Budget Outlook → T8; CBO monthly deficit data → T11.
7. Transcript authorship follows the event host: company-hosted and investor-conference company presentations count as company; media-hosted as media; hearings/trials as official; expert-network events as expert network; user-arranged meetings as user.
8. Resolve filings from a complete code table for each system (EDGAR, exchange, court), regardless of filer. /A amendments share their original category. Unknown filing codes are invalid and go to human review before registration and acceptance.
9. Only exhibits explicitly named by 8-K Item 2.02 count as earnings releases. Classify each other exhibit separately.
10. A filing body and each exhibit are separate items. Do not separately ingest XBRL facts already in the filing. Ownership filings (Form 4, 13D/G, 13F, 144) use their table form and belong to T13.
11. Previously received identical content, matched by fingerprint or to the original, without an explicit replaced version, becomes another source of the original and retains its category. An explicit replacement, including a category-only correction, is a new version, not a duplicate.
12. The same kind of opinion or analysis keeps its category regardless of author, length or platform. Broker, rating agency, columnist, investor, individual or user identity is an attribute. Attribute opinions and estimates to their author.
13. Manual uploads must specify text genre or upload template; otherwise they are invalid. The system's own output is also invalid (classification step 1).
14. A table release is one item, such as an entire 13F or statistical release, and enters as a batch. Split an interface's different kinds of content into separate items. Derived indicators we can calculate from existing information and file listings are not source material.
15. Attribute quoted statements to their original speaker at the evidence level. The containing item's category does not change.
16. Keep incidental differences as attributes: channel, platform, length, summary/full text, venue, annual/quarterly, holding status, executive status and registration. The host of an oral event does determine transcript authorship (rule 7).
<!-- /generated: rules -->

## Excluded material and invalid inputs

<!-- generated: not-inputs -->
- Vendor-derived indicators we can calculate from available information are not source material: valuation multiples, factor exposures, technical indicators and sentiment derived from price/volume such as fear/greed indices. If weights or underlying data are unavailable, classify by content: LEI and financial-conditions indices → T11; nowcasts such as GDPNow → T8.
- File listings, such as EDGAR lists and news search results, locate information but are not source material themselves.
- Audio, video, images and scans without readable text are invalid. Once a transcript or text layer exists, apply normal classification.
- The system's own reports, exports and republished output are invalid, preventing self-citation.
- Stock universes and watchlists belong to the research universe. The user's holdings, trades, P&L and investment permissions are not source material; their destination is deferred.
<!-- /generated: not-inputs -->

## Required input fields

These field names are the actual upstream contract.

<!-- generated: fields -->
| Group | Field | Meaning | Required | Used for classification |
|---|---|---|---|---|
| Identity | `input_id` | The item's stable identifier | Required |  |
| Identity | `content_sha256` | A content fingerprint identifies identical content. Without an explicit replaced version, accept identical content only once. | Required | ✓ |
| Identity | `copy_of` | When the same content was received before and no replaced version is named, identify the original item and merge with it. | Identical content without an explicit replaced version | ✓ |
| Identity | `supersedes` | An update names its previous version: updated news, 10-K/A, edited posts, data revisions or category corrections. Do not overwrite the previous version or merge the update as a duplicate. | When a previous version exists | ✓ |
| Source | `channel` | Delivery channel: data interface, press-release wire, republication site, EDGAR, social/contributor platform or user upload | Required | ✓ |
| Source | `source_uri` | Original location; use an accession number for SEC filings and a post ID for posts | Required |  |
| Source | `publisher` | The author responsible for the content, not the channel forwarding it; use the account for social posts | Required | ✓ |
| Source | `publisher_type` | Author type: company, media, analyst, official or individual. Resolve using the author table valid on the publication day, then the channel default. | Lookup table or channel | ✓ |
| Source | `event_organizer` | Host of an oral event: company, investor conference, media, official body, expert network or user. This determines transcript authorship. | Transcripts | ✓ |
| Source | `authors` | Named individual or real identity behind an account, used to attribute opinions | Optional |  |
| Source | `derived_from` | The source item, such as the 10-K underlying standardised financial statements | When a source exists |  |
| Source | `context` | Post context: reply target, quoted post, thread or forum | Optional |  |
| Time | `period` | Period described by the content: fiscal period, observation window or event date | Periodic reports and data |  |
| Time | `published_at` | When the author made it public; use the New York publication day. For duplicates, use the earliest day. | Required | ✓ |
| Time | `filing_date` | SEC legal filing day: acceptance after 5:30 p.m. counts as the next business day, matching SEC publication. Use it as the SEC filing's publication day. | SEC filings | ✓ |
| Time | `retrieved_at` | When we received it, kept for audit only and never used for decisions | Required |  |
| Classification | `is_structured` | Table or text is a form, not a category. Tables contain fixed-field records (JSON, XBRL, XML, CSV, upload templates) and use the dataset table. Text follows classification rules. | Required | ✓ |
| Classification | `has_readable_text` | Whether readable text exists; audio, video, images and scans without a text layer do not qualify | Required for text | ✓ |
| Classification | `dataset` | Dataset, data interface or upload template; register its category once at onboarding and use it for every record | Tables | ✓ |
| Classification | `filing_system` | Filing system: EDGAR, HKEX, court docket, etc.; each has its own code table | Filings | ✓ |
| Classification | `filing_form` | Filing code: 10-K, 10-K/A, 8-K, DEF 14A, 425, etc. | Filings | ✓ |
| Classification | `filing_items` | 8-K items and the exhibits named by earnings Item 2.02 | 8-K | ✓ |
| Classification | `exhibit` | Exhibit number and description: 99.1 earnings release, 4.1 indenture, 10.1 material contract, etc. | Exhibits | ✓ |
| Classification | `document_format` | Genre: transcript, notes, memo, report, slides, article, letter or post. The channel identifies it; uploads must specify it. Length and platform are attributes. | Text | ✓ |
| Classification | `channel_category` | Source section: media news, opinion, analysis or republished press release; IR/wire/data-room earnings, periodic report or legal document | Optional; use the default if absent | ✓ |
| Classification | `series` | Publication series from any public or private author, such as FOMC statements, Beige Book, ISM PMI or World Economic Outlook. Applies only if registered; unregistered names go to human review. | Optional; use author rules if absent | ✓ |
| Content | `media_type` | File format: web page, PDF, JSON, XML, CSV, Excel, audio, video or image | Required |  |
| Content | `language` | Language | Required |  |
| Subject | `object_identifiers` | Channel-supplied subject identifiers, each with kind (CIK, ticker, company name, cryptocurrency symbol, commodity symbol or theme ID), value and reason (filing subject, filer, data field, channel tag, upstream delivery for that subject or explicit upload). May be empty. | Optional | ✓ |

**Classification returns**: One category, merge with the original, not source material, or invalid with a reason. Categorised items also include resolved subjects (ID, kind, reason) and unresolved identifiers preserved as received.
<!-- /generated: fields -->

## Boundary examples

| Material | Result | Reason |
|---|---|---|
| Apple 8-K exhibit 99.1 named by Item 2.02 | T1 earnings | Resolve the filing code first |
| Amazon 8-K filed via agent; URL contains agent 1104659 | Subject is Amazon | Read identifiers, not URL |
| Activist letter to a board in a 13D | T8; investor is filer, held company is subject | Retain both roles |
| FOMC statement, dot plot, Beige Book | T11 | Central-bank policy/economic material |
| Fed working paper | T8 | Central-bank research |
| IMF World Economic Outlook, CBO Budget Outlook | T8 | Forecasts and outlooks |
| CBO monthly deficit, Treasury monthly statement | T11 | Statistics |
| ISM PMI text report | T11 | Registered series precedes author; private statistics count |
| ADP employment, Michigan sentiment data | T11 | Economy-wide measurement |
| Card spending for one brand | T15 | Specific-company measurement |
| AAII investor-sentiment survey | T8 | Aggregated opinions |
| Fear/greed index | Not source material | Can be calculated from prices |
| OPEC output-cut decision / monthly report | T10 / T8 | Action / outlook |
| Reuters economist survey / report about IMF outlook | T8 / T7 | Registered series / ordinary news |
| President's tariff post during tenure / campaign post | T10 / T8 | Author status follows tenure |
| 2021 news tagged FB / tagged META | Meta / unresolved | Resolve ticker on publication day |
| Apple news incidentally mentioning Samsung | Label Apple only | Extraction handles body mentions |
| Amazon 10-Q accepted July 30, 2026 at 6:11 p.m. | Publication day July 31, 2026 | After 5:30 p.m., SEC publishes next business day |

## Acceptance

- The classification simulation must pass its recorded populations: 412 real items, 161 hand-written cases and 24 company-subject cases. Script category IDs/names must match the page.
- Every item receives exactly one result without a model.
- All lookup values are valid; one invalid value prevents using the table version.
- Every boundary example must become a test. The current simulation covers company subjects only; added macro rules and cryptocurrency, commodity and theme resolution remain known coverage gaps.
- Resolve tickers on the New York publication day. The current simulator uses UTC dates; this known mismatch remains for implementation work.

## Open questions

- Upstream acquisition and labelling, reference data and identifier-to-subject mapping.
- Where the user's holdings, trades, P&L and investment permissions belong.

## Related decisions

- D1/D11: subjects and four subject kinds. D8: four tables in one JSON file with direct results.
- D9: New York publication day. D15: macro rules, series precedence, private statistics and tenure-based author status.
- D16: unresolved items go to human review. D19/D37: first-version freeze and decision requirement for changes.
- D32: one table release per item; no separate filing XBRL ingestion. D34: SEC legal filing day is its publication day.
- D56: the stream has no concept of today; only pull mode acts on time (D14/D54).

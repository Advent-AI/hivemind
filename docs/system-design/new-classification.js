// The New design's input classification module: a top-down issue tree that gives every input exactly one outcome (a
// tag, "not an input", or a refusal), the tag schema, and the input schema the tree reads. Edit the data at the top;
// the drill-down renders it. docs/system-design/simulate_classification.py runs the same rules over test inputs.
(function () {
  'use strict';

  // ------------------------------------------------------------------ the tags: rule = what puts an input here

  const TAGS = {
    T1: { name: 'results_release', label: "Earnings releases", forms: "Both", decide: "Text: exhibits named by 8-K Item 2.02, fiscal-results exhibits in 6-K, exchange earnings announcements and sources labelled as earnings. Tables: datasets registered as earnings figures.", rule: "A fiscal period's earnings release, shareholder letter and release-day figures", definition: "Earnings releases for a quarter, half-year or full year. Text includes exhibits named by 8-K Item 2.02 (earnings releases, shareholder letters, CFO commentary, update decks), explicitly identified fiscal-results exhibits in 6-K, exchange earnings announcements and sources labelled as earnings. Tables include release-day results and guidance, including guidance history. Monthly operating data belongs to T6. Merge republications of the same release with the original.", examples: "Apple quarterly earnings release, Tesla update deck, guidance history" },
    T2: { name: 'periodic_report', label: "Periodic reports", forms: "Both", decide: "Text: 10-K, 10-Q, 20-F, 40-F and ARS, including /A amendments; exchange annual, interim and quarterly reports; sources labelled as periodic reports. Tables: standardised financial statements. Do not separately ingest XBRL facts already in the filing.", rule: "10-K, 10-Q, 20-F, 40-F, ARS and vendor-standardised financial statements", definition: "Text: 10-K, 10-Q, 20-F, 40-F and ARS, including amendments that name the replaced version; exchange annual, interim and quarterly reports; sources labelled as periodic reports. Tables: vendor-standardised statements and segment data, identifying the source report. Do not separately supply XBRL facts already in those reports. Annual versus quarterly is an attribute.", examples: "Meta 10-K, 10-K/A, standardised income statement" },
    T3: { name: 'legal_and_capital_markets', label: "Legal and capital-markets documents", forms: "Text", decide: "Proxy, financing, M&A and tender-offer filings regardless of filer; exhibits numbered 2, 3, 4 or 10; exchange circulars; sources labelled as legal documents.", rule: "Proxy, financing, M&A and tender offers; exhibits 2, 3, 4 and 10", definition: "Proxy materials, including both sides of a proxy contest; financing, M&A and tender-offer filings and amendments, including acquirer and private-equity filings, regardless of filer. Include SEC exhibit categories 2, 3, 4 and 10 (acquisition agreements, charters, security/debt instruments and material contracts), exchange circulars and sources labelled as legal documents. Read terms and each party's statements; attribute statements to the submitting party.", examples: "DEF 14A, activist DEFC14A, 424B5, merger agreement, credit agreement" },
    T4: { name: 'call_transcript', label: "Company-call transcripts", forms: "Text", decide: "Transcripts of company-hosted calls or company presentations at investor conferences; merger calls in 425 filings.", rule: "Transcripts of meetings where the company is speaking", definition: "Company-hosted earnings calls, investor days and company podcasts; company presentations at investor conferences; merger calls in 425 filings. Media-hosted events belong to T7. Venue and transcript provider are attributes.", examples: "MSFT earnings call, NVDA fireside chat at a broker conference" },
    T5: { name: 'presentation', label: "Presentations", forms: "Text", decide: "Company slides: presentations under 8-K Item 7.01 or in 425 filings, and IR-site slides that are not earnings releases.", rule: "Slide decks and PDF presentations", definition: "Company slide decks and PDF presentations under 8-K Item 7.01 or in 425 filings, and IR-site decks that are not earnings releases. Sources labelled as earnings belong to T1.", examples: "Investor-day deck, IR-site presentation not labelled as earnings" },
    T6: { name: 'company_communication', label: "Other company publications", forms: "Both", decide: "Text: remaining company files, including 8-K bodies and other exhibits, remaining 6-K content, SEC response letters, late-filing notices, press releases and official posts. Tables: IR supplements and monthly operating data.", rule: "Remaining company publications and data", definition: "Text not covered above: 8-K bodies, exhibits not named in the earnings item, other items, remaining 6-K content, SEC response letters and late-filing notices; press releases, operating updates, ESG reports, newsrooms, blogs, IR/product pages and official company social posts. Tables: company-published supplementary information and monthly operating data, such as IR Excel or CSV files.", examples: "Executive-change 8-K, quarterly delivery announcement, IR KPI table" },
    T7: { name: 'news', label: "News", forms: "Text", decide: "Material authored by media, with no registered publication series and no opinion or analysis section. A missing section defaults to news.", rule: "Media reporting and other media material not classified elsewhere", definition: "Media publications other than opinion and analysis: news, interviews, podcast transcripts, media-hosted events such as WSJ Tech Live, and media-account posts. General, financial and trade media all qualify. A missing section defaults to news. Opinion and analysis sections belong to T8. Registered media series follow their registered category, such as Reuters economist surveys in T8.", examples: "Reuters report, CNBC CEO interview, DigiTimes supply-chain report" },
    T8: { name: 'opinion_analysis', label: "Opinion and analysis", forms: "Both", decide: "Text: registered forecast, outlook or research series regardless of author; media opinion/analysis sections; analyst-authored text other than dialogue records; all individual-authored text; investor letters to boards in filings. Tables: forecasts, ratings, price targets, consensus and investor-sentiment surveys.", rule: "Attributed opinions, analysis, forecasts and ratings", definition: "Attributed opinions and analysis regardless of author, length or platform. Text includes sell-side and independent research, rating agencies, industry research, think tanks and academia; official and international-organisation forecasts, outlooks and research such as the IMF World Economic Outlook, CBO Budget Outlook and central-bank working papers; fund letters, short reports and investor letters to boards in filings; media opinion; personal posts and essays; and the user's investment memos. Tables include analyst forecasts and revisions, ratings, targets, consensus, credit/ESG ratings, economist and official forecasts including GDPNow nowcasts, investor-sentiment surveys, industry estimates and forecast upload templates. Opinions and estimates remain attributed statements, not completed facts. The user's own opinions become candidate theses, not evidence.", examples: "Sell-side initiation, short report, IMF World Economic Outlook, Reddit post, FY2027 EPS consensus, personal earnings model" },
    T9: { name: 'interview_notes', label: "Interview records", forms: "Text", decide: "Analyst-authored transcripts or meeting notes.", rule: "Dialogue transcripts or notes", definition: "Dialogue recorded by analysts: expert-network interviews, management meetings arranged by the user and channel checks. The form is a transcript or notes. Attribute statements to the original speaker; the recorder is an attribute. Company-hosted events and company presentations at investor conferences belong to T4.", examples: "Expert-network interview, CFO meeting notes" },
    T10: { name: 'official_record', label: "Official actions and records", forms: "Both", decide: "Text: official series registered as actions or records; official authors without a registered series; SEC comment letters and court dockets. Tables: government-published records.", rule: "Official documents, proceedings and records", definition: "Official material not classified elsewhere. Text includes regulatory, judicial, legislative, administrative and exchange documents and proceedings: rulings, approvals, recalls, regulations, sanctions, export controls, tariffs, contract awards, hearing/trial transcripts, SEC comment letters and court dockets. Tables include government records of contracts, lobbying, political donations, patents, litigation, recalls and customs bills of lading. Official forecasts, outlooks and research belong to T8; statistics belong to T11. Officials' personal accounts count as official during their tenure, such as a president announcing tariffs. Attribute quoted statements to their original speaker or submitting party.", examples: "European Commission decision, FTC complaint, SEC comment letter, defence contract award, patent grant" },
    T11: { name: 'macro_policy_statistics', label: "Macro policy and statistics", forms: "Both", decide: "Text: registered monetary-policy or statistical series, whether public or private. Tables: macro statistics and policy rates.", rule: "Monetary policy and macro statistics, public or private", definition: "Text registered as monetary policy or statistics, regardless of publisher: central-bank statements, minutes, speeches, dot plots and Beige Books; official CPI/jobs releases and private ISM PMI, ADP employment and Michigan sentiment releases. Tables: economy-wide or industry-wide statistics and policy rates, public or private, each with a publication date; retain earlier revisions. Include composite measures we cannot calculate because weights are unavailable, such as LEI and financial-conditions indices. Market interest and exchange rates belong to T12; measurements of specific companies, products, locations, chains and protocols belong to T15.", examples: "FOMC statement, Beige Book, CPI and payrolls, ISM PMI, federal funds rate" },
    T12: { name: 'market_data', label: "Market prices and trading", forms: "Table", decide: "Datasets registered as prices and trading.", rule: "Stocks, options, rates, FX, commodities, cryptocurrencies and CDS", definition: "Prices and trading in stocks, ETFs, option chains, futures, interest rates, FX, commodities, cryptocurrencies, credit spreads, CDS and prediction markets; corporate actions such as dividends and splits; share capital.", examples: "Daily prices, option implied volatility, 10-year Treasury yield" },
    T13: { name: 'positioning', label: "Holdings and flows", forms: "Table", decide: "Datasets registered as holdings and flows; table versions of ownership filings.", rule: "13F, Form 4, 13D/G, short positions and flows", definition: "Market-participant holdings and flows: table versions of Form 4, 13D/G, 13F and 144; short interest, borrow fees and utilisation; ETF/fund flows; CFTC positioning; cryptocurrency whale and smart-money holdings.", examples: "Institutional holding changes, insider sales" },
    T14: { name: 'calendar', label: "Calendar", forms: "Table", decide: "Datasets registered as scheduled dates.", rule: "Earnings dates, meetings and deadlines", definition: "Scheduled dates for earnings, investor days, launches, macro releases, central-bank meetings, court/regulatory deadlines, index rebalancing, lock-up and token unlocks, and option expiries.", examples: "Next earnings date, FOMC meeting date" },
    T15: { name: 'third_party_measurement', label: "Third-party measurements", forms: "Table", decide: "Datasets registered as measured activity.", rule: "Card spending, apps, traffic, satellites and on-chain activity", definition: "Vendor-measured activity for specific companies, products, locations, chains and protocols: card spending, app usage, web/search/foot traffic, satellite and shipping data, hiring, scraped prices, reviews and on-chain usage/revenue. These are measurements, not estimates. Industry estimates and forecasts belong to T8; economy-wide or industry-wide statistics belong to T11.", examples: "App downloads, card-spending data" },
    T16: { name: 'reference', label: "Reference data", forms: "Table", decide: "Datasets registered as identities and classifications.", rule: "Identities, classifications and index constituents", definition: "Company and asset identities, industry classifications, corporate structure, supply-chain relationships, index constituents and weights. No subject tracks this category by default. Upstream uses identity references to resolve subjects.", examples: "Ticker-to-CIK mapping, GICS classification, S&P 500 weights" },
  };

  // ------------------------------------------------------------------ the issue tree: the taxonomy, each tag once
  // A branch has a label and either children or tags (its leaves). The tree shows what kinds of information there are;
  // ROUTING says how one input finds its leaf.

  const TREE = {
    label: "All incoming items", question: "Which category is this item?", field: "First check validity and duplication (step 1 below). Each item has exactly one classification result and, if categorised, exactly one category.",
    children: [
      { label: "Company publications and filings", question: "Which disclosure?", field: "Use filing code, source section and genre", tags: ['T1', 'T2', 'T3', 'T4', 'T5', 'T6'] },
      { label: "Media reporting", question: "Media reports", field: "Media author", tags: ['T7'] },
      { label: "Opinion and dialogue", question: "Opinion or dialogue record?", field: "Analyst/individual author, or registered forecast/research series", tags: ['T8', 'T9'] },
      { label: "Official actions and macro statistics", question: "Action/record or policy/statistics?", field: "Use the publication series. T10 is official only; T11 includes public and private sources.", tags: ['T10', 'T11'] },
      { label: "Market and measurement data", question: "What is measured?", field: "Use the dataset table", tags: ['T12', 'T13', 'T14', 'T15', 'T16'] },
    ],
  };

  // How one input finds its leaf, in order. Text or structured only decides which table answers.
  const ROUTING = [
    "First validate: missing required metadata, malformed subject identifiers, unreadable text or the system's own output → invalid. Previously received identical content without an explicit replaced version → merge with the original.",
    "Table data: register each dataset's category once at onboarding rather than judging every record. Split registration by field when an interface returns multiple kinds of content. All later records use that category. Unregistered datasets are invalid and go to human review.",
    "Text filings (SEC, exchange, court): use the filing-system code table regardless of filer. Unknown codes are invalid and go to human review.",
    "Other text with a registered publication series: use the series table (T8, T10 or T11), regardless of author type. An unregistered series name goes to human review while classification continues normally.",
    "Remaining text: resolve author type from the author table valid on the publication day, falling back to the channel default; then use section or genre. Official authors without a registered series → T10. Unresolved author type → invalid and human review.",
  ];

  // ------------------------------------------------------------------ the input schema

  // Every input carries this envelope. `classify` marks the fields the tree reads; the rest place the input in time and
  // provenance. A required field that is missing refuses the input before the tree runs.
  const INPUT_SCHEMA = [
    { group: "Identity", field: 'input_id', meaning: "The item's stable identifier", required: "Required" },
    { group: "Identity", field: 'content_sha256', meaning: "A content fingerprint identifies identical content. Without an explicit replaced version, accept identical content only once.", required: "Required", classify: true },
    { group: "Identity", field: 'copy_of', meaning: "When the same content was received before and no replaced version is named, identify the original item and merge with it.", required: "Identical content without an explicit replaced version", classify: true },
    { group: "Identity", field: 'supersedes', meaning: "An update names its previous version: updated news, 10-K/A, edited posts, data revisions or category corrections. Do not overwrite the previous version or merge the update as a duplicate.", required: "When a previous version exists", classify: true },
    { group: "Source", field: 'channel', meaning: "Delivery channel: data interface, press-release wire, republication site, EDGAR, social/contributor platform or user upload", required: "Required", classify: true },
    { group: "Source", field: 'source_uri', meaning: "Original location; use an accession number for SEC filings and a post ID for posts", required: "Required" },
    { group: "Source", field: 'publisher', meaning: "The author responsible for the content, not the channel forwarding it; use the account for social posts", required: "Required", classify: true },
    { group: "Source", field: 'publisher_type', meaning: "Author type: company, media, analyst, official or individual. Resolve using the author table valid on the publication day, then the channel default.", required: "Lookup table or channel", classify: true },
    { group: "Source", field: 'event_organizer', meaning: "Host of an oral event: company, investor conference, media, official body, expert network or user. This determines transcript authorship.", required: "Transcripts", classify: true },
    { group: "Source", field: 'authors', meaning: "Named individual or real identity behind an account, used to attribute opinions", required: "Optional" },
    { group: "Source", field: 'derived_from', meaning: "The source item, such as the 10-K underlying standardised financial statements", required: "When a source exists" },
    { group: "Source", field: 'context', meaning: "Post context: reply target, quoted post, thread or forum", required: "Optional" },
    { group: "Time", field: 'period', meaning: "Period described by the content: fiscal period, observation window or event date", required: "Periodic reports and data" },
    { group: "Time", field: 'published_at', meaning: "When the author made it public; use the New York publication day. For duplicates, use the earliest day.", required: "Required", classify: true },
    { group: "Time", field: 'filing_date', meaning: "SEC legal filing day: acceptance after 5:30 p.m. counts as the next business day, matching SEC publication. Use it as the SEC filing's publication day.", required: "SEC filings", classify: true },
    { group: "Time", field: 'retrieved_at', meaning: "When we received it, kept for audit only and never used for decisions", required: "Required" },
    { group: "Classification", field: 'is_structured', meaning: "Table or text is a form, not a category. Tables contain fixed-field records (JSON, XBRL, XML, CSV, upload templates) and use the dataset table. Text follows classification rules.", required: "Required", classify: true },
    { group: "Classification", field: 'has_readable_text', meaning: "Whether readable text exists; audio, video, images and scans without a text layer do not qualify", required: "Required for text", classify: true },
    { group: "Classification", field: 'dataset', meaning: "Dataset, data interface or upload template; register its category once at onboarding and use it for every record", required: "Tables", classify: true },
    { group: "Classification", field: 'filing_system', meaning: "Filing system: EDGAR, HKEX, court docket, etc.; each has its own code table", required: "Filings", classify: true },
    { group: "Classification", field: 'filing_form', meaning: "Filing code: 10-K, 10-K/A, 8-K, DEF 14A, 425, etc.", required: "Filings", classify: true },
    { group: "Classification", field: 'filing_items', meaning: "8-K items and the exhibits named by earnings Item 2.02", required: '8-K', classify: true },
    { group: "Classification", field: 'exhibit', meaning: "Exhibit number and description: 99.1 earnings release, 4.1 indenture, 10.1 material contract, etc.", required: "Exhibits", classify: true },
    { group: "Classification", field: 'document_format', meaning: "Genre: transcript, notes, memo, report, slides, article, letter or post. The channel identifies it; uploads must specify it. Length and platform are attributes.", required: "Text", classify: true },
    { group: "Classification", field: 'channel_category', meaning: "Source section: media news, opinion, analysis or republished press release; IR/wire/data-room earnings, periodic report or legal document", required: "Optional; use the default if absent", classify: true },
    { group: "Classification", field: 'series', meaning: "Publication series from any public or private author, such as FOMC statements, Beige Book, ISM PMI or World Economic Outlook. Applies only if registered; unregistered names go to human review.", required: "Optional; use author rules if absent", classify: true },
    { group: "Content", field: 'media_type', meaning: "File format: web page, PDF, JSON, XML, CSV, Excel, audio, video or image", required: "Required" },
    { group: "Content", field: 'language', meaning: "Language", required: "Required" },
    { group: "Subject", field: 'object_identifiers', classify: true, meaning: "Channel-supplied subject identifiers, each with kind (CIK, ticker, company name, cryptocurrency symbol, commodity symbol or theme ID), value and reason (filing subject, filer, data field, channel tag, upstream delivery for that subject or explicit upload). May be empty.", required: "Optional" },
  ];

  const OUTPUT_FIELDS = "One category, merge with the original, not source material, or invalid with a reason. Categorised items also include resolved subjects (ID, kind, reason) and unresolved identifiers preserved as received.";

  // Which objects an input concerns (D1, D11). Read off the identifiers the channel gives, never off the text; no model.
  const OBJECT_RULES = [
    "Four subject kinds, matching the research universe: company, cryptocurrency, commodity and theme. An item may concern several subjects or none.",
    "Use only channel-supplied identifiers and their stated reasons, plus the author when it is a company: the issuing company for a release or the company speaking at its meeting. Record why each subject is attached. An empty or unsupported identifier kind or reason invalidates the whole item.",
    "Keep identifier kinds separate because equal strings can mean different subjects: companies use CIK, ticker or company name; cryptocurrencies and commodities use their own symbols; themes use theme IDs.",
    "Themes have only two origins: upstream delivery for that theme or explicit identification at upload. Do not infer them from the body text.",
    "Read identifiers, not body text or URLs. A filing agent's identifier can appear in a URL; an old Amazon 8-K URL contains agent ID 1104659.",
    "Resolve company, cryptocurrency and commodity identifiers through reference data. Pad CIK to 10 digits; resolve tickers as of publication day (FB identified Meta before June 9, 2022); accept only registered company aliases. Resolve theme IDs through the theme library. Preserve unresolved identifiers as received, mark them unresolved and continue processing; fill them after registration.",
    "A non-company author (media, analyst, official or individual) is not itself a subject. Preserve both filer and filing subject with their roles: in a 13D, the activist is the filer and the held company is the subject.",
    "Do not label incidentally mentioned companies or themes here. Extraction associates them with specific theses and evidence.",
    "When merging a duplicate, union both items' subjects and deduplicate them. Subjects do not affect category. Invalid items and non-source material receive no subjects.",
  ];

  const TIME_RULES = [
    "Use the New York publication day. Time of day matters only for SEC filing-day calculation (rule 4). Processing order follows dispatch sequence, not publication time.",
    "Each item uses one date: publication day. Its described fiscal or observation period is an attribute. The stream has no concept of today's date; only pull mode acts on time.",
    "Do not separately record a channel delay of several days. No rule uses the computer clock; receipt time is for audit only.",
    "SEC publication day is the legal filing day. Acceptance before 5:30 p.m. uses that day; after 5:30 p.m., SEC publication is next business morning, so use the next business day.",
    "Merged duplicates use the earliest publication day: knowledge begins when the market could first see it.",
    "Corrections, updates, restatements, edits and category changes create new versions without overwriting old ones.",
    "An item without publication time cannot be placed on the timeline and is invalid.",
  ];

  const RULES = [
    "Category describes what the information is. Text/table form, length, platform and channel are attributes. A category can have both forms; form only determines whether classification uses the dataset table or text rules.",
    "Each item has exactly one result: a category, merge with the original, not source material, or invalid with a reason. Use fixed rules and lookup tables, not a model.",
    "The author is responsible for the content. Wires, republication sites, transcript providers, data vendors, social/contributor platforms, EDGAR filing agents and user uploads are delivery channels.",
    "Resolve author type from the author table, then channel defaults: news indices default to media, wires to company, and social/contributor/newsletter accounts to individual. Only an unresolved result after both is invalid. Registration is an attribute. International organisations such as IMF, World Bank, OECD, OPEC and WTO are official.",
    "Author-table entries have validity periods evaluated on publication day. Status follows tenure, not influence: an account is official during office and individual during campaigning, before inauguration or after leaving office.",
    "Registered publication series take precedence over author type: ISM PMI → T11; Reuters economist survey → T8; CBO Budget Outlook → T8; CBO monthly deficit data → T11.",
    "Transcript authorship follows the event host: company-hosted and investor-conference company presentations count as company; media-hosted as media; hearings/trials as official; expert-network events as expert network; user-arranged meetings as user.",
    "Resolve filings from a complete code table for each system (EDGAR, exchange, court), regardless of filer. /A amendments share their original category. Unknown filing codes are invalid and go to human review before registration and acceptance.",
    "Only exhibits explicitly named by 8-K Item 2.02 count as earnings releases. Classify each other exhibit separately.",
    "A filing body and each exhibit are separate items. Do not separately ingest XBRL facts already in the filing. Ownership filings (Form 4, 13D/G, 13F, 144) use their table form and belong to T13.",
    "Previously received identical content, matched by fingerprint or to the original, without an explicit replaced version, becomes another source of the original and retains its category. An explicit replacement, including a category-only correction, is a new version, not a duplicate.",
    "The same kind of opinion or analysis keeps its category regardless of author, length or platform. Broker, rating agency, columnist, investor, individual or user identity is an attribute. Attribute opinions and estimates to their author.",
    "Manual uploads must specify text genre or upload template; otherwise they are invalid. The system's own output is also invalid (classification step 1).",
    "A table release is one item, such as an entire 13F or statistical release, and enters as a batch. Split an interface's different kinds of content into separate items. Derived indicators we can calculate from existing information and file listings are not source material.",
    "Attribute quoted statements to their original speaker at the evidence level. The containing item's category does not change.",
    "Keep incidental differences as attributes: channel, platform, length, summary/full text, venue, annual/quarterly, holding status, executive status and registration. The host of an oral event does determine transcript authorship (rule 7).",
  ];

  // The lookup tables the tree reads (D8). Each is looked up by its key; what comes out is a tag, or an author type.
  const LOOKUP_TABLES = [
    { table: "Dataset table", lookup: "Dataset → category or not source material", example: "Daily prices → T12; financial statements → T2; ISM PMI and LEI → T11; GDPNow → T8; technical indicators and fear/greed index → not source material" },
    { table: "Filing-code table, one per filing system", lookup: "Filing code → category; 8-K, 6-K, 425 and ownership filings require additional rules", example: "10-K → T2; DEF 14A → T3; 8-K → inspect items and exhibits" },
    { table: "Publication-series table", lookup: "(author, series) → T8, T10 or T11. Any author can register a series; T10 is official only.", example: "FOMC statements, Beige Book, ISM PMI → T11; IMF World Economic Outlook, CBO Budget Outlook → T8; OFAC sanctions announcements → T10" },
    { table: "Author table", lookup: "Author → company, media, analyst, official or individual, with a validity period. Fall back to the channel default when unresolved.", example: "Reuters → media; Morgan Stanley → analyst; IMF → official; president's personal account during tenure → official" },
  ];

  const LOOKUP_RULES = [
    "Keep all four tables in one JSON file read by production and tests. Changing a table creates a new classification version.",
    "The first three tables return a result directly: category, not source material, or further rules such as 8-K. No intermediate name. The author table returns author type, not category: Reuters news is T7 and opinion is T8; section, genre or series still matters.",
    "Dataset and series registration follow the same principles: public/private statistics → T11; central-bank monetary-policy/economic statements, minutes, speeches, dot plots and Beige Books → T11; central-bank research and working papers → T8; forecasts, outlooks and research → T8; actions and records → T10, official only. For measured activity datasets, economy/industry-wide → T11; specific company, product, location, chain or protocol → T15.",
    "Validate table values at load: dataset → one of 16 categories or not source material; filing code → category or rule; series → T8, T10 or T11, with T10 official only; author → one of five author types. Invalid values prevent startup.",
    "Do not guess missing datasets, filing codes or series; send them to human review for registration. Missing authors use channel defaults first and reach human review only if still unresolved.",
    "Identifier-to-subject mappings, such as AAPL → Apple, are not classification tables. They resolve subjects and validate the universe, not categories. Upstream owns this mapping; details are deferred.",
  ];

  const NOT_SOURCES = [
    "Vendor-derived indicators we can calculate from available information are not source material: valuation multiples, factor exposures, technical indicators and sentiment derived from price/volume such as fear/greed indices. If weights or underlying data are unavailable, classify by content: LEI and financial-conditions indices → T11; nowcasts such as GDPNow → T8.",
    "File listings, such as EDGAR lists and news search results, locate information but are not source material themselves.",
    "Audio, video, images and scans without readable text are invalid. Once a transcript or text layer exists, apply normal classification.",
    "The system's own reports, exports and republished output are invalid, preventing self-citation.",
    "Stock universes and watchlists belong to the research universe. The user's holdings, trades, P&L and investment permissions are not source material; their destination is deferred.",
  ];

  // ------------------------------------------------------------------ the drill-down

  const FORM_LABELS = { "Both": "Text and tables", "Text": "Text", "Table": "Tables" };

  const CIRCLED = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨'];

  // Every path to each tag, read off the tree, for the schema table.
  function tagPaths(branch, trail, paths) {
    const here = trail.concat(branch.label);
    (branch.tags || []).forEach((code, index) => {
      const path = here.slice(1).join(' › ') + (branch.ordered ? ` › ${CIRCLED[index]}` : '');
      (paths[code] = paths[code] || []).push(path);
    });
    (branch.children || []).forEach((child) => tagPaths(child, here, paths));
    return paths;
  }

  function branchBox(branch, escapeHtml, isRoot) {
    return `<div class="org-node${isRoot ? ' org-node--root' : ''}">`
      + (branch.family ? `<span class="org-node__family">${escapeHtml(branch.family)}</span>` : '')
      + `<span class="org-node__label">${escapeHtml(branch.label)}</span>`
      + (branch.question ? `<span class="org-node__question">${escapeHtml(branch.question)}</span>` : '')
      + (branch.field ? `<span class="org-node__note">${escapeHtml(branch.field)}</span>` : '')
      + (branch.merge ? `<span class="org-node__refuse">${escapeHtml(branch.merge)}</span>` : '')
      + (branch.refuse && branch.children ? `<span class="org-node__refuse">${escapeHtml(branch.refuse)}</span>` : '')
      + '</div>';
  }

  function tagCard(code, order, branchLabel, escapeHtml) {
    const tag = TAGS[code];
    const rule = tag.rule;
    return `<button class="org-tag" type="button" data-tag="${code}">`
      + (order ? `<span class="org-tag__order">${order}</span>` : '')
      + `<span class="org-tag__top"><span class="org-tag__code">${code}</span><span class="org-tag__label">${escapeHtml(tag.label)}</span></span>`
      + `<span class="org-tag__rule">${escapeHtml(rule)}</span>`
      + '</button>';
  }

  function renderBranch(branch, escapeHtml, isRoot) {
    let below = '';
    if (branch.children) {
      below = `<ul>${branch.children.map((child) => `<li>${renderBranch(child, escapeHtml, false)}</li>`).join('')}</ul>`;
    } else if (branch.tags) {
      below = '<div class="org-stack">'
        + branch.tags.map((code, index) => tagCard(code, branch.ordered ? CIRCLED[index] : '', branch.label, escapeHtml)).join('')
        + (branch.notInput ? `<div class="org-tag org-tag--outcome">${escapeHtml(branch.notInput)}</div>` : '')
        + (branch.refuse ? `<div class="org-tag org-tag--refuse">${escapeHtml(branch.refuse)}</div>` : '')
        + '</div>';
    }
    return branchBox(branch, escapeHtml, isRoot) + below;
  }

  // Scale the tree down, never up, so the whole of it is in view.
  function fitTree(container) {
    const frame = container.querySelector('.org');
    const tree = container.querySelector('.org-tree');
    tree.style.zoom = '1';
    const scale = Math.min(1, (frame.clientWidth - 8) / tree.scrollWidth);
    tree.style.zoom = String(scale);
  }

  const design = window.HIVEMIND_DESIGNS.new;
  design.drilldowns = design.drilldowns || {};
  design.classification = { TAGS, TREE, INPUT_SCHEMA };
  design.drilldowns.classify = {
    button: "Explore classification: the 16 categories",
    kicker: "Classification · Details",
    size: 'full',
    render(container, context) {
      const escapeHtml = context.escapeHtml;
      const paths = tagPaths(TREE, [], {});
      const total = Object.keys(TAGS).length;
      const schemaRows = Object.keys(TAGS)
        .sort((first, second) => Number(first.slice(1)) - Number(second.slice(1)))
        .map((code) => {
          const tag = TAGS[code];
          return `<tr id="tag-row-${code}"><td><span class="org-tag__code">${code}</span></td>`
            + `<td><code>${escapeHtml(tag.name)}</code><div class="schema-table__label">${escapeHtml(tag.label)}</div></td>`
            + `<td>${escapeHtml(FORM_LABELS[tag.forms])}</td><td>${(paths[code] || []).map(escapeHtml).join('<br>')}</td><td>${escapeHtml(tag.decide)}</td>`
            + `<td>${escapeHtml(tag.definition)}</td><td class="schema-table__quiet">${escapeHtml(tag.examples)}</td></tr>`;
        }).join('');
      const schemaFieldRows = INPUT_SCHEMA.map((row, index) => {
        const firstOfGroup = index === 0 || INPUT_SCHEMA[index - 1].group !== row.group;
        return `<tr class="${firstOfGroup ? 'schema-table__group-start' : ''}"><td class="schema-table__group">${firstOfGroup ? escapeHtml(row.group) : ''}</td>`
          + `<td><code>${escapeHtml(row.field)}</code></td><td>${escapeHtml(row.meaning)}</td>`
          + `<td class="schema-table__quiet">${escapeHtml(row.required)}</td><td>${row.classify ? '✓' : ''}</td></tr>`;
      }).join('');

      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">Classification: assign each item a category</h2>
          <p class="drill__intro">Upstream classifies every item and identifies its subjects under these rules; we validate it. Upstream supplies only the research universe. The ${total} categories are organised into five families by content, each appearing once. Text or table is a form that determines how classification works. Select a category to read its definition.</p>
          <p class="drill__status"><span class="pill pill--strong">First version frozen · 2026-10-18</span>Simulation passed 412 real items and 161 hand-written cases. Subject resolution passed 24 company cases. Added macro rules and cryptocurrency, commodity and theme resolution remain untested. The simulator still differs from current rules; see CURRENT_STATE. Rule changes need a new decision and a rerun of <code>python3 docs/system-design/simulate_classification.py</code> (all cases must pass), or a fresh reasoning review of boundary cases.</p>
          <div class="org"><div class="org-tree"><ul><li>${renderBranch(TREE, escapeHtml, true)}</li></ul></div></div>
          <section>
            <h3 class="drill__heading">Decision order: find the category</h3>
            <ol class="drill__rules">${ROUTING.map((step) => `<li>${escapeHtml(step)}</li>`).join('')}</ol>
          </section>
          <section>
            <h3 class="drill__heading">The four classification lookup tables</h3>
            <table class="schema-table schema-table--compact">
              <thead><tr><th>Table</th><th>Lookup input and result</th><th>Example</th></tr></thead>
              <tbody>${LOOKUP_TABLES.map((row) => `<tr><td>${escapeHtml(row.table)}</td><td>${escapeHtml(row.lookup)}</td><td class="schema-table__quiet">${escapeHtml(row.example)}</td></tr>`).join('')}</tbody>
            </table>
            <ul class="drill__rules">${LOOKUP_RULES.map((rule) => `<li>${escapeHtml(rule)}</li>`).join('')}</ul>
          </section>

          <div class="drill__columns drill__columns--schema">
            <section>
              <h3 class="drill__heading">Fields supplied with each item</h3>
              <table class="schema-table schema-table--compact">
                <thead><tr><th>Group</th><th>Field</th><th>Meaning</th><th>Required</th><th>Used for classification</th></tr></thead>
                <tbody>${schemaFieldRows}</tbody>
              </table>
              <p class="drill__output"><strong>Classification returns: </strong>${escapeHtml(OUTPUT_FIELDS)}</p>
            </section>
            <section>
              <h3 class="drill__heading">Time rules</h3>
              <ol class="drill__rules">${TIME_RULES.map((rule) => `<li>${escapeHtml(rule)}</li>`).join('')}</ol>
              <h3 class="drill__heading drill__heading--spaced">Classification rules</h3>
              <ol class="drill__rules">${RULES.map((rule) => `<li>${escapeHtml(rule)}</li>`).join('')}</ol>
              <h3 class="drill__heading drill__heading--spaced">Related subjects</h3>
              <ol class="drill__rules">${OBJECT_RULES.map((rule) => `<li>${escapeHtml(rule)}</li>`).join('')}</ol>
              <h3 class="drill__heading drill__heading--spaced">Excluded source material and invalid items</h3>
              <ul class="drill__rules">${NOT_SOURCES.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
            </section>
          </div>

          <section>
            <h3 class="drill__heading">${total} categories</h3>
            <table class="schema-table">
              <thead><tr><th>ID</th><th>Category</th><th>Form</th><th>Family</th><th>Decision rule</th><th>Definition</th><th>Example</th></tr></thead>
              <tbody>${schemaRows}</tbody>
            </table>
          </section>
        </div>`;

      container.querySelectorAll('[data-tag]').forEach((card) => card.addEventListener('click', () => {
        const row = container.querySelector(`#tag-row-${card.dataset.tag}`);
        row.scrollIntoView({ behavior: 'smooth', block: 'center' });
        row.classList.remove('schema-table__row--flash');
        void row.offsetWidth;
        row.classList.add('schema-table__row--flash');
      }));
      requestAnimationFrame(() => fitTree(container));
      window.addEventListener('resize', () => { if (container.isConnected) fitTree(container); });
    },
  };
})();

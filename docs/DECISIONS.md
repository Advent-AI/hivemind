# Decisions

Recorded choices of the rebuild, newest last. A decision names who made it, what it decides and where it is enforced.
A later decision that changes one names the one it replaces.

## D1 · 2026-10-15 · Input classification carries each input's related companies

- By: Alex ("好，补进分类模块，仿真跑通先").
- Decides: every classified input carries `companies` (entity ids, each with its basis) and `unresolved_companies`.
  They are read only from the identifiers the channel gives and from the author when the author is a company; never
  from the text or the URL. A ticker resolves on its publication day; an unresolved identifier is kept, never a refusal.
  Related companies never change the tag.
- Enforced: `docs/system-design/new-classification.js` (`COMPANY_RULES`, `INPUT_SCHEMA`) and
  `docs/system-design/simulate_classification.py` (`related_companies`, `COMPANY_CASES`, the old ledger's 17
  independently derivable inputs). The simulation must PASS.
- Changed by D11: related companies became related objects (company, crypto, commodity, theme); the page's
  `COMPANY_RULES` became `OBJECT_RULES`.

## D2 · 2026-10-15 · Config holds only the choices a person makes

- By: Alex, in the Config discussion.
- Decides: Config holds the companies researched, the tags processed and the model settings of text extraction.
  Facts (tag, form, times, related companies) come from Input classification; mechanisms (when work runs, retries,
  rounds, due triggers) belong to code; fetch parameters are derived from the companies and the processed tags and are
  not written. Whether an input is read by code or by a model follows from its form (structured or text), which
  classification gives; Config does not choose it.
- Enforced: `docs/system-design/new-config.js`.
- Changed by D6: the companies researched moved out of Config into the universe module.
- Changed by D10: there is no fetch step in the system; the fetch parameters belong to the upstream pipeline.
- Changed by D18: the tags processed moved out of Config into the universe (what each object tracks); Config
  holds only the extraction policy.
- Changed by D25: the form no longer chooses a reader. Every item that belongs to a category goes to the one
  extraction module and is read by its category; Config holds one model setting per category.
- Changed by D27 and D29: Config holds three kinds of model setting: reading, one per category; matching; and the
  final verdict.

## D3 · 2026-10-15 · Config has no budget or concurrency limits

- By: Alex ("我觉得3 不是一个重点可以完全干掉").
- Decides: the limits section (budget per policy, total budget, concurrency) is not part of Config. Where limits live,
  if anywhere, is not decided.
- Enforced: `docs/system-design/new-config.js`.

## D4 · 2026-10-15 · Dispatch is by tag only, never by company

- By: Alex ("不看公司，因为这个pipeline 应该不管公司的，就是按照tag的种类来分发").
- Decides: an input whose tag is not processed is stored only; a processed structured input goes to code; a processed
  text input goes to model extraction. The input's related companies play no part in dispatch. The list of companies
  is used only to decide what to fetch.
- Enforced: `docs/system-design/new-config.js`.
- Changed by D7: an input whose tag is not processed is not processed and not stored by us (it stays in the source
  database).
- Changed by D18: dispatch no longer filters by tag at all; every item that arrives is within the universe's scope
  and is processed. Dispatch still never reads related objects.

## D5 · 2026-10-15 · Time is the material's own time and the run's day

- By: Alex ("是的，用材料的时间，不要陷入之前的问题").
- Decides: time is two things: the time a material became public (`published_at`, carried by the material) and the
  day a run stands on (T, given by the run command: today for a live run; a replay walks T forward one day at a time
  from its first day). One rule: standing on T, the system sees only materials with `published_at ≤ T`. T moves
  forward every day, a day without new material included, and never moves back. No rule reads the computer's clock;
  `retrieved_at` is for audit only. Input classification no longer writes `admitted_on`: what an input's visibility
  needs is its `published_at`. The old design's knowledge date, log order and clock patches are not carried over.
- Enforced: `docs/system-design/new-classification.js` (`TIME_RULES`, `OUTPUT_FIELDS`) and the run node of
  `docs/system-design/new-design.js`.
- Changed by D7: replay is not part of the system design.
- Changed by D9: `published_at ≤ T` compares days, cut in New York time.
- Changed by D10: T is no longer given by a run command; it is the stream's current New York day, moved by the
  stream's day markers.
- Changed by D12: there is no current day T and no day markers; each item carries its own publication day.
- Seal note (2026-10-16): the run node named above no longer exists (D12); the time rules live in `TIME_RULES`.

## D6 · 2026-10-15 · The research universe is its own module

- By: Alex ("公司主题名单可以单独管理，我们有500多个us euqity, crypto commodity etc. 所以模块上这个需要写进某个地方").
- Decides: the list of what is researched (500+ US equities, crypto assets, commodities and other asset classes) is a
  module of its own with its own versions, managed apart from Config; Config no longer holds a company list (this
  changes D2). Each entry is an entity id from the reference data (T16) and its asset class. Only fetch reads the
  universe, to decide what to pull; dispatch never reads it (D4). A run records the universe version it used.
- Enforced: the universe node of `docs/system-design/new-design.js`.
- Changed by D10: nothing in the system fetches; the universe is handed to the upstream pipeline as the scope it
  feeds, and is not a filter inside the system.
- Changed by D18: the universe also states which kinds of information (tags) each object tracks; the supply scope
  is objects × tracked tags.

## D7 · 2026-10-15 · No input store; replay is a test database, not a design concern

- By: Alex ("不会消失，我们自己有自己的database and pipeline 不会消失"; on replay: "那和系统设计无关啊，只是一个test
  database").
- Decides: the system keeps no copy of the materials it reads: they stay in the team's own database. The system keeps
  only a processing record: which material (its id and version in that database) was processed, how, and with what
  result; whether an input arrived before (a copy) is answered from it. An input whose tag is not processed is simply
  not processed (dispatch's "store only" becomes "not processed"); when the tag is turned on later, the material is
  read from the database again. The system knows one thing about time: given a day T and a database, run that day.
  Testing the past is running it on a test database with a past T; the system's logic does not change.
  (Changed by D10: the system consumes a stream instead of running a day; testing is a test feeder streaming a test
  database.)
  (Changed by D10: copies, the same content arriving again under another id, are found by upstream classification
  and arrive as "merged into the original"; the processing record answers only whether the same id and version was
  processed, dispatch's second question, D17.)
  (Changed by D18: "when the tag is turned on later" becomes "when the universe starts tracking it": a new
  universe version, and upstream feeds the past items of the new scope.)
- Enforced: `docs/system-design/new-config.js` (`DISPATCH_TREE`) and the run, dispatch, code and extract nodes of
  `docs/system-design/new-design.js`.
- Seal note (2026-10-16): the run node no longer exists (D12).
- Changed by D26: besides the processing record, the system keeps the views database; materials are still not
  copied, and every view and piece of evidence names the material it came from by id, version, location and quote.

## D8 · 2026-10-16 · Classification's lookup tables: one data file, results are tags

- By: Alex ("其实可以映射到classification 的品类 … 这样能一起联动update"; "你要做一份json数据文件或是yaml 好查找maintain的统一数据结构").
- Decides: classification reads four lookup tables: datasets → tag (or "not an input"), form codes → tag (one table
  per filing system; 8-K and 6-K, 425 and ownership forms go on to a rule), official series → tag, and authors →
  author type (the tag then follows from the type with the category, format or series, since one author lands in
  different tags). They live in one JSON data file that production and tests both read; a changed table is a new
  classification version. Reading the file checks one thing: every value is valid (one of the 16 tags, "not an
  input", a named rule or one of the five author types). The code ↔ company table (AAPL ↔ Apple) is not a
  classification table; where it comes from is open.
- Not decided: a duplicate-entry check (rejected by Alex as unneeded).
- Changed by D15: the official series table becomes the publication series table, open to any publisher; author
  entries carry validity dates.
- Enforced: the "对照表" section of `docs/system-design/new-classification.js`. Design only: no data file is built at the
  architecture-POC stage.

## D9 · 2026-10-16 · A day is cut in New York time; only the day counts

- By: Alex ("好按照纽约时间切，不要再产生什么时间戳漂移的问题，那几分钟几秒其实根本没差，不要自己给自己制造麻烦").
- Decides: each material belongs to the New York calendar day it was published on (its publication day). Standing on
  T, the system sees materials whose publication day is T or earlier. The hour and minute play no part in any rule, and
  materials of the same day are not ordered. An SEC filing's day is the New York day EDGAR accepted it, not its
  statutory filing date. A copy merged into its original gives the original the earliest day among them.
- Enforced: `TIME_RULES` and `INPUT_SCHEMA` of `docs/system-design/new-classification.js`; the run node of
  `docs/system-design/new-design.js`.
- Changed by D12: there is no T; an item belongs to its publication day, and how a reader takes the state as of a
  day is decided with the thesis design. The run node is gone.
- Changed by D34: an SEC filing's day is the day SEC makes it public (its statutory filing date), not its
  acceptance day. Changed by D31: inside one day, items are ordered by their arrival number; no rule reads the hour.

## D10 · 2026-10-16 · The system starts at a stream of classified items

- By: Alex ("现在就是assume 又一个pipeline 会不断的feed 打好classification tag 的信息进来，这个系统应该怎么处理；这才是我们的
  PRD … 和之前的系统思路不同，务必明确记录好不要再混淆"; "测试的时候你当然是可以从一个test bd 例如你现在的cache 去读取然后
  stream in and build the bd … 所以不是"拉"").
- Decides: the system's boundary is a stream. An upstream pipeline keeps feeding items that already carry their
  classification (tag, text or structured, attributes, related objects). The system receives each item, dispatches it
  by tag, processes it by code or model, and builds its research store. Fetching and classifying happen upstream and
  are discussed later; Input classification is the stream's contract: upstream produces it, the system validates it.
  This differs from the old system, which pulled sources itself by date and processed them in batches; nothing in the
  new system pulls. Testing is a test feeder reading a test database (for example the old system's cache) in
  publication-day order and streaming it in through the same path.
- Receive: validates the contract and refuses a malformed item with its reason; does not process the same item (same
  upstream id and version) twice, by the processing record; a corrected item is a new version and is processed. The
  current day T is a New York day that moves with day markers in the stream, empty days included, never backwards
  (who sends the markers is proposed, not confirmed: upstream live, the test feeder in tests, one per day).
  (Changed by D12: no current day and no day markers.)
  (Changed by D17: receive is not a step of its own; its checks are dispatch's first two questions.)
- Enforced: `docs/system-design/new-design.js` (summary, the classify, receive and store nodes, the overview view) and
  the intro of `docs/system-design/new-classification.js`.

## D11 · 2026-10-16 · Related objects and the theme library

- By: Alex ("我觉得主题是必要的。你可能得跨政治经济战争地缘政治通胀等各种宏观因素做这个主题库"; "我同意").
- Decides: the universe holds four kinds of object: company, crypto, commodity and theme; the theme library is the
  theme part of the universe, not a separate list. Rates, FX and indices are not objects of their own; they are data
  that themes track. Classification's related companies become related objects (any of the four kinds), with
  identifiers written by kind (CIK, ticker, name; crypto symbol; commodity code; theme id). A theme comes only from
  the object upstream fed the item for, or from an upload's declaration, never from the text. Macro items need no new
  tag: they already fall in T7, T10, T11, T12 and T14; what differs is the related object. Facts are attached to
  objects at extraction; a stock is linked to a theme through its thesis's drivers (thesis not designed yet). The
  classification simulation covers companies only.
- Enforced: `OBJECT_RULES` and `INPUT_SCHEMA` of `docs/system-design/new-classification.js`;
  `docs/system-design/new-universe.js`.
- Changed by D18: each theme lists the tags it tracks; companies, crypto and commodities have a default per kind.
- Changed by D26: a stock is linked to a theme through the premise of its view, which names a theme view.
- Changed by D38: a company reaches a theme through a dependency on a theme view (premises are not used).

## D12 · 2026-10-16 · No current-day clock in the system

- By: Alex ("没有新的thesis 或日期为什么要硬推进").
- Decides: the system keeps no "current day" and no day markers. Each item carries its own publication day (New York,
  D9), and processing an item reads only that item; when no item arrives, nothing happens. How date-driven work
  (a prediction falling due, reading the research store as of a day without seeing later facts) is triggered is
  decided with the thesis design, not before. This drops D5's "T moves forward every day" and D10's day markers.
- Enforced: the receive and store nodes of `docs/system-design/new-design.js`; `TIME_RULES` of
  `docs/system-design/new-classification.js`.
- Seal note (2026-10-16): the receive node became dispatch's first two questions (D17).
- Changed by D31: processing an item may read the state left by earlier items (a smaller number and a publication
  day not after its own); it still never reads the wall clock. Pull mode's "now" is an input (D29).
- Changed by D56: classification's time rule 2 says the stream has no "today"; pull mode, the only place that acts
  on time, gets its "now" as an input (D14, D54).

## D13 · 2026-10-16 · The system is driven by information, not by the calendar

- By: Alex ("时间是一直往前推进，但是增额推荐是现实的时间，你抽取出来未来会成为thesis 或是ladder, evidence 的东西是会被这些
  streming events 影响的，不是按照每一天来的 … 不需要按部就班的推日期，有相关的信息抽取出现，自然会影响整个系统抽取的thesis
  向前").
- Decides: the system moves forward only when an item arrives. Its facts are attached to objects, and the theses,
  ladders and evidence that depend on those objects move forward from them. There is no daily step anywhere in the
  system, including the layers not designed yet; a day without items changes nothing. Later designs (thesis, ladder,
  evidence) are built on this.
- Enforced: the summary and the store node of `docs/system-design/new-design.js`.
- Scope (D14): this is the stream mode. Date- or schedule-triggered work exists only in the pull mode.

## D14 · 2026-10-16 · Two modes, designed apart: stream and pull

- By: Alex ("下面肯定会探讨到例如thesis 里面的laddar /evidence 有些可能到期日就需要看下证据或是甚至主动的run 一个cron 来看下是否
  满足。这是stream的相反模式，也就是pull mode (agent 主动查找）这个我们后面设计，但是我希望你分的很清楚这两种模式").
- Decides: the system has two modes. Stream mode (designed now): items arrive and their facts move dependent theses,
  ladders and evidence forward; it never reads the calendar (D13). Pull mode (designed later): at a ladder's or an
  evidence's due date, or on a cron schedule, an agent in the system actively looks for evidence and checks whether a
  condition is met; it is the only place where time triggers work. "Pull" names only this agent-initiated checking;
  the upstream pipeline that feeds the stream is called upstream supply, not pull.
- Enforced: the summary, the thesis and pull nodes and the overview view of `docs/system-design/new-design.js`.
- Changed by D29 and D31: pull mode sends due views to the final verdict, re-checks views whose weakened premise
  was not seen within 7 days, and periodically merges and splits drivers.
- Changed by D54: pull mode runs at the end of the day or on a cron interval, goes through the views proactively
  and freezes the state of the views due that day.

## D15 · 2026-10-16 · Macro, political and economic material in the classification

- By: Alex, after the walk-through of theme material ("你继续再深度推演一次"; "你持续思考反思直到solid. 不要乱加戏，但是千万注重细节").
- Decides:
  1. The publication series table is checked before the author type and is open to any publisher (official, private,
     media, company). It is keyed by (publisher, series) and yields only T8, T10 or T11; T10 only for an official
     publisher. Registration principles, the same for the dataset table: statistics, official or private, → T11; a
     central bank's material on monetary policy and the economy (statements, minutes, speeches, dot plot, Beige Book)
     → T11, its research and working papers → T8; forecasts, outlooks and research → T8; actions and records → T10.
     A text without a registered series follows the author type as before; an official author without one → T10.
  2. T11 is macro policy and statistics whoever publishes them. Measures of the whole economy or a whole industry →
     T11; measures of specific companies, products or places → T15.
  3. Author entries carry validity dates, looked up on the publication day and counted by term of office, not by
     influence (the same account is official in office and individual before and after). International organizations
     (IMF, World Bank, OECD, OPEC, WTO) are official.
  4. "Not an input" covers only indicators the system can compute from inputs it already has (valuation multiples,
     technical indicators, the Fear & Greed index). An indicator it cannot compute is classified by what it is (LEI and
     financial conditions indices → T11; GDPNow → T8). Investor sentiment surveys are aggregated views → T8.
- Checked by reasoning over 14 boundary materials (Fed statements and papers, IMF, CBO, ISM, ADP, card panels, AAII,
  Fear & Greed, OPEC, a Reuters poll, a president's posts in and out of office); the expected outcomes of the existing
  412 real inputs and 161 cases do not change. Not simulated: no code at the POC stage.
- Enforced: `TAGS` (T8, T10, T11, T15), `TREE`, `ROUTING`, `INPUT_SCHEMA` (`series`), `RULES`, `LOOKUP_TABLES`,
  `LOOKUP_RULES` and `NOT_SOURCES` of `docs/system-design/new-classification.js`.

## D16 · 2026-10-16 · A human review pool for what the tables do not know

- By: Alex ("如果是新的指标或是在classification 里面出现不存在的company theme 应该要有一个机制可以自动的给人review 并认为的更新这个
  系统 … 把他认为是一个exception handling pool for human review").
- Decides: what the tables do not know is not guessed but goes to a human review pool: unregistered form codes and
  datasets and undetermined author types (the item is refused); unregistered series, i.e. new indicators (the item is
  classified by the author-type fallback and goes on); unresolved object identifiers (processed, object unresolved);
  facts about an object that does not exist, found at extraction (attached to "unknown object"); contract violations
  (upstream's defect). Only real gaps enter: an identifier found in the reference data or the theme library but not in
  the universe is not an exception. One entry per gap, with its count and examples. After a human registers it, the
  table or the universe gets a new version, the affected items are fed again from upstream, and an item whose tag
  changes is a new version. The pool's delivery, reviewers and how a review takes effect are designed later.
- Changed by Alex (2026-10-16, "复核池不要画虚线出来，再module 写明白这个部分先不设计output"): only what enters the
  pool is designed now; its output, including the steps after registration above, is not designed yet, and the
  overview draws no lines out of the pool.
- Enforced: the review node and the overview view of `docs/system-design/new-design.js`; `ROUTING` and `LOOKUP_RULES`
  of `docs/system-design/new-classification.js`.
- Changed by D27 and D31: the pool also receives matches the model is unsure of, proposed new themes and items
  that fail repeatedly.
- Changed by D33: an object outside the universe is found when the views database writes a view, not at extraction.

## D17 · 2026-10-16 · Receive is merged into dispatch

- By: Alex ("接受和分发什么区别？你在给自己加戏吗？").
- Decides: there is no separate receive step. Dispatch is the system's single entry and one decision tree asks, in
  order: does the item meet the contract (no → refused, to the review pool); was this item, same id and version,
  processed before (yes → skipped, D7); the classification outcome; is the tag processed; text or structured. Every
  item reaches exactly one destination.
- Enforced: the dispatch node and the overview view of `docs/system-design/new-design.js`; `DISPATCH_TREE` of
  `docs/system-design/new-config.js`.
- Changed by D18: the question "is the tag processed" is removed; the tree asks four questions.

## D18 · 2026-10-16 · One switch: the universe decides what is processed

- By: Alex, on two switches that could disagree (the universe tracks a theme while Config leaves its tags unprocessed):
  "那你不觉得这是个设计问题吗？你应该怎么做你深度思考"; "那你就这样改 … 一定要严谨".
- Why: whether a kind of information matters depends on the object researched (a tariff theme needs official
  notices; a stock needs filings and calls; a crypto asset needs on-chain data and social posts). A global "tags
  processed" switch in Config cuts across every object and can contradict the universe; two lists that must agree is
  the defect the rebuild set out to remove.
- Decides: the universe states, for each object, the kinds of information (tags) it tracks: a default per kind
  (company: T1–T10 and T12–T15; crypto: T7, T8, T10, T12–T15; commodity: T7, T8, T10–T15) and, for each theme, its own
  list (at least one). Tracked tags must be valid tags. The supply scope is objects × tracked tags; upstream pushes only
  items within it, and the test feeder streams by the same scope; the rule is kept by whoever writes the stream, not
  checked by dispatch. Every item that arrives is processed: dispatch drops the "is the tag processed" question and asks
  four: contract, processed before, classification outcome, text or structured; it still never reads related objects
  (D4). Config drops `processed_tags` and holds only the extraction policy. A new object or tracked tag is a new
  universe version, and upstream feeds the past items of the new scope (as D7).
- Enforced: `TRACKING_DEFAULTS`, `TRACKING_EXAMPLES` and `RULES` of `docs/system-design/new-universe.js`;
  `CONFIG_SCHEMA`, `RULES` and `DISPATCH_TREE` of `docs/system-design/new-config.js`; the universe, config and dispatch
  nodes and the overview view of `docs/system-design/new-design.js`; the stream contract in the intro of
  `docs/system-design/new-classification.js`.

## D19 · 2026-10-16 · Freeze v1: everything up to classification

- By: Alex ("我们当前为止到classification 的模块和定义都可以freeze了吗，做最后一次review"; "是改一轮").
- Before the freeze, a final review fixed seven text defects, none a design change: the time rules still read "as of
  T" (D12 removed T); D1 and D9 lacked their change notes; the code ↔ object table and T16 were open items of
  classification though classification is upstream (D10); the lookup tables had several names each (now: dataset
  table, form-code table, publication series table, author table); the tree's refusal text missed malformed object
  identifiers and the review pool; T7's condition missed "no registered series"; T12, T13, T14 and T15 did not name
  crypto (assets, whale and smart-money positions, token unlocks, on-chain activity of chains and protocols).
- Decides: the research universe (structure, object kinds, tracking defaults, rules), the Input classification
  contract (16 tags, tree, routing, input schema, object rules, time rules, lookup tables and their registration
  principles, what is not an input), Config (extraction policy only), dispatch (the four-question tree) and the human
  review pool (as an exception pool) are frozen as v1. A later change needs a new decision, and the simulation is run
  again or the boundary materials are reasoned through again.
- Not frozen: the theme library's concrete themes (draft); the extraction policy's granularity; the review pool's
  mechanism; upstream supply and classification, including the code ↔ object table and T16; pull mode; where
  positions, trades and P&L belong.
- Known limits: the classification simulation covers companies only; the macro rules (D15) and crypto, commodity and
  theme objects (D11) are reasoned, not simulated; the script resolves tickers on the UTC date, not the New York day
  (D9). No code is changed at the POC stage.
- Enforced: the status of the classify, universe, config, dispatch and review nodes and the summary of
  `docs/system-design/new-design.js`; the status line of `docs/system-design/new-classification.js`.
- Changed by D24: the universe's company default no longer tracks financial reports (T1, T2, T4).
- Changed by D25: dispatch asks three questions (the text-or-table question goes); Config's open item is settled
  (one model setting per category); classification's wording "the form decides model or code" became "the form
  decides how the category is looked up".
- Sealed 2026-10-16: after a final check (simulation PASS; every node placed, every edge and code reference valid,
  every detail page renders; no stale wording on the page; decisions whose enforced place moved carry a seal note) and
  the plain-language rewrite of all page texts (wording only, rules unchanged), the design is copied to
  `docs/archive/2026-10-16-v1/` with `SHA256SUMS`. The archived simulation is a record: it reads the old ledger by a
  path relative to the live tree and runs only from `docs/system-design/`.
- Changed by D27–D31 (2026-10-18): the universe's company default tracks financial reports again (D28); Config
  holds the matching and final-verdict settings as well; dispatch numbers each item; the review pool has three more
  sources. The boundary materials were reasoned through again; the classification wording now says views and
  evidence instead of facts.
- Changed by D32: a filing's XBRL numbers are not pushed as items; table data is one release per item.
- Changed by D34: classification time rule 4 dates an SEC filing by the day SEC makes it public.
- Wording aligned 2026-10-18 (a consistency review; no rule changed): inside one day items are ordered by their
  arrival number (D31); length no longer decides how an item is cut (items are read whole, D27); an author missing
  from the author table falls back to the channel's default type before the review pool (as rule 4 already said);
  only indicators we can compute from our own inputs are "not material" (D15); dispatch's first question checks the
  classification outcome, since merged, not-material and refused items carry no category.
- Changed by D37 (2026-10-18): frozen again together with extraction, in the 2026-10-18 text.

## D20 · 2026-10-16 · A PRD per module, in Markdown, viewable from the design page

- By: Alex ("你现在应该针对每个模块写prd，并且归档好，并且在FE的地方点进去模块能再打开预览PRD，PRD就用 .md来写就好，FE解析呈现好看就好").
  Claude had suggested waiting until the main line was designed, to keep one source; Alex decided to write them now.
- Decides: `docs/prd/` holds one PRD per module (`00-system.md` and ten modules) and an index (`README.md`). Frozen
  modules have full PRDs (what it is, why, scope, inputs, outputs, rules, examples, acceptance criteria, open
  questions, decisions); undesigned modules list only what is decided and what is open. Their tables (categories,
  rules, fields, dispatch tree, universe defaults) were generated from the design page's own data, so they start
  identical to it. The design page opens a module's PRD from its detail ("查看 PRD") and the system PRD from the intro,
  rendered by its own small Markdown renderer (`markdown.js`, no external library). Opened from disk the page shows
  the copy bundled by `docs/prd/build_bundle.py` (`prd-bundle.js`); served over HTTP it reads the .md files.
  Precedence: Alex, then DECISIONS, then the PRDs and the page. A change to the page or a new decision updates the PRD
  in the same change, and the bundle is rebuilt; `python3 docs/prd/build_bundle.py --check` finds a stale bundle.
- The sealed copy `docs/archive/2026-10-16-v1/` is refreshed to include the PRDs and the viewer; its checksums are
  regenerated.
- Enforced: `docs/prd/*.md`, `docs/prd/build_bundle.py`; `docs/system-design/markdown.js`, `prd-bundle.js`, the `prd`
  fields of `new-design.js`, `openPrd` in `render.js`.
- Changed 2026-10-18 (Alex: "在这些模块里面，要有一个link可以展开看PRD (编译.md)"): every detail page also opens its
  module's PRD from the top of the sheet, and that PRD goes back to the detail page (`openDrilldown`, `openPrd` and the
  sheet's click handler in `render.js`). Detail pages draw processes as step cards and decisions as trees; the PRDs show
  the same trees, generated from the same data (`ascii_tree`, `step_flow` in `docs/check.py`).

## D21 · 2026-10-16 · Any change refreshes everything, by one command

- By: Alex ("嗯如果有改动需要全部刷一遍").
- Decides: after any change to the design page, a PRD or a decision, `python3 docs/refresh.py` runs before the change is
  done. It rewrites the PRD blocks generated from the page's data (marked `<!-- generated: NAME -->`; the hand-written
  parts around them are kept), rebuilds the PRD bundle, and checks the classification simulation, the page (every node
  placed, every edge and code reference valid, every detail page renders, every module has a PRD) and the bundle. It
  exits 1 on any failure, and a change is not finished while it fails. DECISIONS and CURRENT_STATE are still updated by
  hand in the same change. The sealed copies in `docs/archive` are not refreshed; a new freeze gets a new dated copy.
- Checked: on a scratch copy, a changed Config rule reached `03-config.md` and the bundle, and a removed marker was
  reported with exit 1.
- Enforced: `docs/refresh.py`; the generated-block markers in `docs/prd/01-universe.md`, `02-classification.md`,
  `03-config.md` and `04-dispatch.md`.
- Changed by D22: refreshing is a reasoning pass by Claude, not a script; `refresh.py` became the check-only
  `docs/check.py`.

## D22 · 2026-10-16 · Refreshing is a reasoning pass; the script only checks

- By: Alex ("你跑refresh.py有什么鸟用，这个是需要reason的需要llm跑").
- Decides: after any change, Claude refreshes everything by reasoning, module by module in a fixed order (universe →
  classification → Config → dispatch → code processing → model extraction → research store → research conclusions →
  pull mode → review pool → system overview). For each module, against DECISIONS: does the change touch it; do the
  page and the PRD say the same thing; do the examples still hold; do the acceptance criteria and open questions need
  to change. Inconsistencies are fixed in the same change and listed in the reply with their reason. The script
  `docs/check.py` is only the last, mechanical step: it reports (never rewrites) a generated PRD block that differs
  from the page, rebuilds the bundle, runs the classification simulation and checks that the page loads. Its passing
  does not mean the refresh is done.
- First pass (2026-10-16) fixed ten inconsistencies the script could not see: the system's first principle ignored
  pull mode; "we check" in classification read as re-classifying (it means checking completeness and category
  validity at dispatch); who reads the lookup file; the Config version was recorded on every processing record though
  code processing does not use Config (now only on model reads; page and PRDs); the open items of dispatch (how a
  returned item reaches upstream), the research store (records for items not processed), the conclusions (whether a
  theme has its own conclusion) and the universe (its existence check depends on upstream's reference data); a
  placeholder number in the code-processing example; the PRD index still described the removed refresh script.
- Enforced: `docs/prd/README.md` (the procedure), `docs/check.py`.
- Changed by D25: the order reads universe → classification → Config → dispatch → extraction → research store →
  research conclusions → pull mode → review pool → system overview.
- Changed by D26 and D29: the order reads universe → classification → Config → dispatch → extraction → views
  database → final verdict → pull mode → review pool → system overview.
- Changed by D36: `docs/check.py` also runs the wording check over the four input and extraction modules.

## D23 · 2026-10-16 · Tables without XBRL tags are read by the model

- By: Alex ("可以交给模型", answering whether the untagged tables of MD&A and earnings releases get a code path of their
  own; then "这个地方就是系统设计问题了，怎么抽取关键数据，怎么存取关键信息等，这个你给我在FE画出来我们一起看").
- Context: an evaluation of the old system's code extraction, on its stored data, found that parsing the flattened
  text of 10-Q/10-K tables read every value faithfully at its position but read too little and broke silently: no
  NVIDIA table at all (abbreviated months), half of Microsoft's tables dropped (no caption), Apple's 10-K statements
  missed ("Years ended"), Apple's segment operating income stopped after FY2025 Q3 (new layout), and 64 of 71
  "restatements" were different rows sharing one id. The research report `reports/SEC 财报 代码抽取 开源方案.md` found
  that statements and notes carry inline XBRL, that MD&A and earnings releases carry none, and that no open-source
  parser reads untagged tables reliably (edgartools' release parser repeats the old failure classes).
- Decides: code processing reads structured data only. The untagged tables inside text documents (MD&A, EX-99.1 and
  EX-99.2) are read by model extraction; there is no separate code path that parses them. This applies D2 (the form
  decides the reader) to tables inside text.
- Not decided (a draft for discussion on the design page): that filings reach code processing as each filing's own
  complete XBRL; a number's identity (object, concept or metric, segment members, start and end, unit) and one
  observation per item that reports it; how the model is given a table (raw text or a grid of cells) and how its
  numbers are checked against the source; how the store serves "as of a day" reads and whether derived values are
  stored.
- Enforced: the code, extract and store detail pages in `docs/system-design/new-facts.js`; the code, extract and store
  nodes of `docs/system-design/new-design.js`; `docs/prd/05-code-processing.md`, `06-model-extraction.md`,
  `07-research-store.md`.
- Changed by D24: financial reports are no longer streamed, so filings do not reach code processing in stream mode;
  the fact-path drafts are paused until the research conclusions are designed. The rule still holds for any text that
  arrives.
- Changed by D25: there is no code processing module; extraction reads every item, tables inside text included.
- Changed by D27: every item goes whole to the model, tables and table items included.

## D24 · 2026-10-16 · Financial reports are not streamed; pull mode reads them when a thesis needs them

- By: Alex ("这个system的核心是抽取thesis, 所以我在想这样刷财报是真的有意义的吗？"; on designing the research
  conclusions first: "我同意，我们不应该再stream 财报了，这个没有意义。应该是在我们还没设计的pull mode 里面采用。这个记录下来，
  和我们之前旧版的设计思路有很大的区别").
- Why: the system exists to form and test theses, and a thesis is an argued view whose few drivers name the numbers
  it needs; financial-report lines are evidence, never its definition. Reading every reported number as it streams
  in builds a store the theses then search, and lets the available numbers shape the theses. The old system's stored
  data shows it: for three companies it kept 11,841 numbers, of which the theses cited 543 (4.6%); of the 21 KPIs the
  theses watched, 9 appear in no table at all and none of those 9 got a number.
- Decides: financial reports are not part of the stream. When a thesis's ladder or evidence needs a number from a
  report (for example "if Apple's iPhone revenue turns negative year over year next quarter, the view fails"), pull
  mode fetches that number at the due date and checks it. Stream mode keeps the items that move theses as they arrive.
  The research conclusions (thesis, ladder, evidence) are designed next; extraction and the research store follow
  from what a thesis needs (the fact-path drafts of D23 are paused, not deleted: a number's identity and "the same
  value again is a confirmation" may be reused).
- Differs from the old system: the old system fetched each company's whole financial statements on every refresh
  (provider statements plus the tables of every 10-Q/10-K), kept every line and its derived growth, and offered the
  lines to the model calls that formed theses as a menu. The new system starts from the thesis and asks for a number
  only when a thesis names it.
- Scope (Alex, "你说的这些都算"): financial reports are periodic reports (T2: 10-K, 10-Q and their XBRL), earnings
  releases (T1) and earnings calls (T4). The universe's company default (frozen in D19) changes from T1–T10, T12–T15
  to T3, T5–T10, T12–T15, and the US–China tariffs example from T1–T6 to T3, T5, T6. This is the only change: the
  universe is the single switch (D18); classification and dispatch stay as they are, and the tags still exist for pull
  mode. Because the universe tracks tags, everything in T4 leaves the stream, not only earnings calls: investor days
  and conference talks too (telling them apart would need a classification change). Earnings slides in T5 stay.
  What stays in the stream for code processing (prices, holdings, calendar, consensus, official records, macro
  statistics) is decided with the research conclusions, by the same thesis-first test.
- Enforced: the summary and the universe, code, extract, store and pull nodes of `docs/system-design/new-design.js`;
  `TRACKING_DEFAULTS` and `TRACKING_EXAMPLES` of `docs/system-design/new-universe.js`; the paused status of the detail
  pages in `docs/system-design/new-facts.js`; `docs/prd/00-system.md`, `01-universe.md`, `05-code-processing.md`,
  `06-model-extraction.md`, `07-research-store.md`, `08-thesis.md`, `09-pull-mode.md`.
- Changed by D28: financial reports stream again and are read into views and evidence; the no-number-warehouse
  point stays.

## D25 · 2026-10-16 · One extraction module, read by category from a senior hedge fund analyst's view

- By: Alex ("我感觉这个环节的抽取应该貌似要全部让LLM来了。。。只是每种类型文件的prompt 可能是不一样的"; "嗯可以这样做，但是你写在这个
  模块好了。首先删掉代码这个模块，就是一个模块叫抽取，然后按照classification 品类分别抽取不一样的东西，可以有一套template
  prompt, persona 就是用senior hedge fund analyst 视角来做thesis 或是观点抽取").
- Decides: code processing is removed; model extraction becomes the single module "extraction". Dispatch hands every
  item that belongs to a category to extraction, with its category; its last question ("text or table") goes, so it
  asks three. Extraction reads each item by its category with one template prompt for all categories, assembled in
  this order: a fixed persona (a senior hedge fund analyst who reads to form and test views), the category's
  definition and reading rule taken from classification (not rewritten), the item's related objects, what this
  category should yield (one line per category in the extraction module), and later the object's thesis drivers
  (after the research conclusions are designed). Every item yields facts, views (whose), the analyst's reading of what
  it means for the object (marked as inference), and anything that could change the view, each with its source. The
  program, not the prompt, owns the output shape and checks every number and quote against the source.
- Config: one model setting per category (its open item is settled). What each category reads and the template live
  in the extraction module, as Alex asked; Config keeps its frozen role of recording which model and prompt version
  each category uses.
- Not decided: whether table data (T12–T15 and the table forms of T6, T8, T10, T11) still streams and is read here,
  or, like financial reports, is fetched by pull mode when a thesis needs it. Financial reports (T1, T2, T4) do not
  stream (D24); their rows in the per-category table are kept for pull mode.
- Files: the PRDs are renumbered (05-extraction.md, 06-research-store.md, 07-thesis.md, 08-pull-mode.md,
  09-review-pool.md); file names in earlier decisions refer to the old numbering. The code-processing detail page and
  PRD are deleted.
- Enforced: `CATEGORY_READS`, `TEMPLATE`, `EVERY_ITEM_YIELDS`, `PROGRAM_DOES` of `docs/system-design/new-facts.js`;
  `DISPATCH_TREE`, `TREE_NOTES`, `CONFIG_SCHEMA`, `OPEN` of `docs/system-design/new-config.js`; the nodes and the
  overview view of `docs/system-design/new-design.js`; the generated blocks of `docs/prd/05-extraction.md` (checked by
  `docs/check.py`).
- Changed by D26 and D27: extraction yields views and evidence with sources, not facts, views and a separate
  analyst's reading (the view is the analyst's judgment); the template's last part is the objects' existing drivers;
  extraction also matches against the drivers. Table items are read too (D27).
- Changed by D35: extraction v1 is final; each category has its own prompt from the one template.
- Changed by D33: matching against the drivers belongs to the views database; extraction only reads, checks sources
  and hands over.

## D26 · 2026-10-18 · The views database is the system's core

- By: Alex ("其实整个system做的事情就是建构，更新，删除这个data structure"; on whose views: "就是你的模型抽取出来的观点，谁说的
  什么这些是客观的信息，你的模型抽取出来的东西才是真的"; "这个观点其实也是因子，只是他可能是一系列量化+非量化的evidence来支撑的";
  on closing: "一个thesis 如果被证伪了，应该被invalidate, 或是过期了，被invalidate, 但是应该存在这个db里面以供历史查询"; on
  levels: "我觉得分开。之前也说过宏观类型的thesis 其实是公司层次之外的"; on drivers: "前者，need be specific"; on sources:
  "你的观点抽取一定要附带这个观点的source 是哪里来的，这样可以未来快速查找文件/数据源来做reason"; and "1. 这个没问题" to the
  views database being thesis · ladder · evidence).
- Decides: the system builds, updates and closes a views database; it is the thesis · ladder · evidence of the design
  page, and the research store merges into it (the store's paused draft of number identities and observations is
  dropped; processing records stay). Structure: object (company, crypto, commodity, theme, all from the universe) →
  driver (specific: who does what to what; its definition is never rewritten, a change is a new driver with a
  redirect) → view. A view has a one-sentence claim that is never rewritten (a change is a new view that supersedes
  it), a direction (up or down), a horizon class (short or long) with a due date, for object views a stance on the
  object, a rationale that cites evidence, an optional premise, confirm and falsify conditions (the ladder), evidence,
  a status (active, confirmed, falsified, expired, merged, superseded, no longer tracked) and versions. Views are the
  model's judgments; evidence is objective (who said what, where). Two levels: theme views say what will happen in the
  world; object views say what will happen to the object, and name a theme view (or another object's view) as their
  premise. Every view, piece of evidence and change carries its source: upstream id and version, category,
  publication time, location in the document (section and paragraph, table cell; for data, dataset and record) and the
  quote; code refuses a source it cannot find or a quote not in the document, and both directions can be looked up
  (a view's documents; a document's views). Closed views and old versions are kept for history.
- Enforced: the views node and the overview view of `docs/system-design/new-design.js`; `VIEW_TREE`, `VIEW_FIELDS`,
  `EVIDENCE_FIELDS`, `LEVEL_RULES`, `LEVEL_TREE` and `SOURCE_TREE` of `docs/system-design/new-facts.js`; `docs/prd/06-views.md`
  (replaces `06-research-store.md` and `07-thesis.md`).
- Changed by D33: matching and writing what extraction hands over run in the views database.
- Wording aligned 2026-10-18: an object view's "利好还是利空" is the driver's direction of effect on the object, not a
  buy or sell stance (AGENTS section 8: a stance is weighed against what is priced).
- Changed by D38: the structure is rebuilt (a view is a question, a five-rung ladder and a due date; drivers,
  claims, horizon classes, conditions and premises are not used).

## D27 · 2026-10-18 · Extraction reads the whole item by category, then matches it against the drivers

- By: Alex ("就是他妈的整个文档丢给llm去解读就好了，不用再分什么有的没得"; "我们按照不同分类做不同prompt tempalte 的LLM抽取";
  "不是，应该和一个观点database 做对比"; "我觉得dedup 和match 应该是要用embegging 来查找的，你觉得呢，这个你可以reseach web";
  "你觉得这是最有效的做法吗？我觉得你要把我们这边的PRD去web serch别人是怎么解决这个问题的，再讨论").
- Research: `reports/观点库 向量检索 去重匹配.md` (embeddings cannot tell direction, numbers or periods apart; choosing
  among a few ranked candidates beats pairwise judging; agent memory systems moved to append-only with invalidation)
  and `reports/观点库匹配 业界做法对比.md` (mature systems put identity on a fixed key and use similarity only for
  recall; "new" is the harder half and models under-report it; a small set given in full beats retrieval).
- Decides: every item, whatever its form, goes whole to the model. Steps: (0) dispatch numbers it; (1) read, with the
  category's template (persona, the category's reading rule from classification, the related objects, what the
  category yields, and the names only of the objects' existing drivers), writing candidate views and evidence with
  sources; (2) code merges evidence with the same original source, subject and date or period; (3) code lists every
  driver of the related objects in full, plus a keyword and embedding search over all theme drivers; (4) a short call
  without the document names, for each candidate, its driver, a new driver or "unsure", its premise and any duplicate
  evidence; (5) code decides: one active view per driver and horizon class; same direction is supporting evidence,
  opposite direction is weakening evidence (no opposite view is created), no active view is a new view; a new driver
  is created and revisited by pull mode's periodic merge; "unsure" is created, flagged and sent to the review pool;
  theme writes come before object writes; unknown objects go to the review pool; numeric conditions use fixed forms
  (metric, period, calculation, comparison, threshold) judged by one shared piece of code; ids outside the candidate
  list are refused; (6) code sends views that meet a final-verdict trigger to the final verdict. Config gains one
  setting for the matching call.
- Not decided: how large one table item is (a whole batch or one record) and whether prices stream (proposed: one
  filing's XBRL or one object's day of prices is one item; prices off by default, read by pull mode when a condition
  needs them); how an item too long for one call is cut; measurements on stored data before building (drivers per
  object, agreement of two independent "same driver" labelings, accuracy of "new driver", position bias).
- Enforced: the extract and config nodes of `docs/system-design/new-design.js`; `TEMPLATE`, `CATEGORY_READS`,
  `EXTRACT_STEPS`, `WRITE_STEPS`, `DECIDE_TREE`, `SOURCE_TREE` of `docs/system-design/new-facts.js`; `CONFIG_SCHEMA` of
  `docs/system-design/new-config.js`; `docs/prd/05-extraction.md`.
- Changed by D32: the open item is settled (one release per item; no separate XBRL; no price-specific rule).
- Changed by D33: extraction is reading and checking sources; the evidence merge, candidate drivers, matching,
  deciding and verdict triggers run in the views database.
- Changed by D39: matching against drivers (steps 2–5) is replaced by matching candidates to open views.

## D28 · 2026-10-18 · Financial reports stream again

- By: Alex ("我觉得新的财报应该还是可以推进来，但是观点就变成抽取新的 + 验证当前的").
- Decides: earnings releases (T1), periodic reports (T2) and earnings calls (T4) are back in the stream; the
  universe's company default is T1–T10, T12–T15 again and the US–China tariffs example T10, T7, T8, T1–T6. They are
  read like every other item into views and evidence (D27). D24's thesis-first point stands: no number warehouse.
- Enforced: `TRACKING_DEFAULTS` and `TRACKING_EXAMPLES` of `docs/system-design/new-universe.js`; the universe node of
  `docs/system-design/new-design.js`; `docs/prd/01-universe.md`.

## D29 · 2026-10-18 · A final verdict before any view is closed

- By: Alex ("确实让模型完整看一遍再关掉是稳妥的，这边可以多画一个环节block就是来做final verdict").
- Decides: a view is closed only by the final verdict, a model call that reads the view, all its evidence, its
  premise's state and why it was sent. Triggers: a confirm or falsify condition met (code); the due date (pull mode,
  only after every item published on or before it is processed); the premise's status changed (at once); the premise
  weakened (at the object's next item, at the latest after 7 days by pull mode); weakening evidence of the "happened"
  tier; a disagreement between independent sources in one tier; a corrected item that removes a view's basis.
  Outcomes: closed as confirmed or falsified (citing evidence), closed as expired ("no data to verify" when no evidence
  can decide), or kept (a premise removed or replaced, conditions added). Only conditions plus evidence of the
  "happened" tier can close a view. A verdict is a new version of the view with its sources; when a view closes,
  every view resting on it is sent again. Pull mode's "now" is an input: real time live, the replay time in tests.
  Config gains one setting for the verdict.
- Enforced: the verdict and pull nodes of `docs/system-design/new-design.js`; `VERDICT_TRIGGERS`, `VERDICT_TREE`,
  `VERDICT_RULES` of `docs/system-design/new-facts.js`; `docs/prd/07-final-verdict.md`, `docs/prd/08-pull-mode.md`.
- Wording aligned 2026-10-18: "only conditions plus 'happened' evidence" governs closing as confirmed or falsified;
  expiry at the due date is not a judgment of right or wrong. The premise statuses that send dependents at once
  include "no longer tracked".
- Changed by D41: the final verdict is an old draft to be redone on the rebuilt views database (D38).
- Changed by D54: at the due date the state is frozen and the view closes, with no answer apart from it; nothing
  waits for the items published on or before the due date.

## D30 · 2026-10-18 · Conflicting sources and the consensus

- By: Alex ("even for the same thesis, you should be prepared that given different sources that streamed it at
  different time frames, there should be conflicting views … as a hedge fund analyst, how would you deal with these
  conflicting views? Or … what is the consensus view that you think would make sense in terms of determining whether
  or not to validate or invalidate the evidence within the thesis").
- Decides: evidence has four tiers (happened; said by the party itself; third-party view; rumour). Views are not
  decided by vote: only the "happened" tier can meet a condition, the others only strengthen or weaken. Sources are
  counted by original source (twenty outlets relaying one scoop are one). A disagreement inside a tier sends the view
  to the final verdict, which may only keep it and add the decisive fact as a condition unless "happened" evidence
  decides it. Conditions are added, never removed or loosened. When a fact answers a condition, code marks the earlier
  statements on it confirmed or denied, which builds each source's record; the record is shown, not used to weight
  evidence. The consensus of a view is computed by code from the latest stance of each independent third-party source;
  the view may state where it differs.
- Enforced: `TIERS` and `CONFLICT_RULES` of `docs/system-design/new-facts.js`; `docs/prd/06-views.md`.
- Changed by D38: tiers and counting by original source stay; add-only conditions, the conflict trigger and the
  consensus by code are replaced (the consensus is open again).
- Changed by D51: consensus is not part of the design at all; third-party views stay evidence of their tier.
## D31 · 2026-10-18 · Order, one writer, and the link between the levels

- By: Alex ("你觉得公司层级link 到宏观thesis 的方式是类似symbolic link 还是怎么处理两者之间可能存在的async /sync 关系？";
  "反正是stream, 理论上时间是以前走到近期，所以应该要time sorted").
- Decides: a premise is a link by id that follows merges, plus the version last seen; a newer version means the
  dependent view is behind. When the premise's status changes, every dependent view goes to the final verdict at once;
  a merge repoints the link; a weakened premise sends dependents to the verdict at the object's next item or after 7
  days; a supported premise changes nothing. Only items produce evidence; views pass notices, never evidence. Dispatch
  numbers each item in arrival order (never the wall clock). Each view has one writer, its object's queue; evidence
  from another item reaches it as a message carrying that item's number. An item reads only the state left by items
  with a smaller number and a publication day not after its own (inside one day the number decides; no rule reads
  the hour); the result must equal one-at-a-time processing,
  and a parallel read that changed before commit is judged again. A late item reads the versions of its publication
  day and is written last with its real date. A corrected item's evidence replaces the old version's. A failed item
  records the step it reached and retries from it, replacing only its own result; repeated failures go to the review
  pool. A view whose object leaves the universe is kept as no longer tracked and not judged at its due date. This
  changes D12: processing an item may read the state left by earlier items.
- Enforced: `PROPAGATION_TREE` and `ORDER_RULES` of `docs/system-design/new-facts.js`; `DISPATCH_TREE` and `TREE_NOTES` of
  `docs/system-design/new-config.js`; the dispatch node of `docs/system-design/new-design.js`;
  `docs/prd/04-dispatch.md`, `docs/prd/06-views.md`.
- Changed by D38 and D39: dependencies replace premises (pinned years, chains); a late item is re-judged when it
  arrives and does not read the versions of its publication day.
- Changed back by D45: the change of the late-item rule by D38 and D39 is a proposal Alex has not decided; this
  rule stands: a late item reads the state of its publication day and is written with its real date, and a view
  whose object leaves the universe is kept as no longer tracked and not judged at its due date.
- Changed by D46: the late-item rule is replaced by D46 item 13 (the timeline only grows forward); the rule for a
  view whose object leaves the universe stands.
- Changed by D55: a view whose object is taken off the list (by hand) is flagged no longer tracked and no longer
  updated; "not judged at its due date", written for the old final verdict, is replaced by that.

## D32 · 2026-10-18 · Table data comes one release at a time; XBRL is not pushed again

- By: Alex (on XBRL: "如果是财报直接进来，那就不用重复XBRL了啊，这不是废话吗"; on one release per item: "这是废话吧"; on
  Claude's proposal to keep prices out of the stream: "我觉得这个还是交给模型判断吧，因为有些时候股价的信息会带观点，这个很难说，我们先
  不要做一些特殊处理", then "the news or whatever you streamed in may have a title that contains stock price or move
  but body with reasoning, you can't just not pass it … keep the shape of the pipeline as is, don't 自己加戏").
- Measured: the stored SEC companyfacts give 203–640 tagged numbers per recent 10-Q or 10-K for Apple, NVIDIA and
  Amazon (Apple's 10-Q of 2026-07-31: 112 concepts, 283 numbers, revenue alone four periods), and companyfacts leaves
  out the segment and product breakdowns. They are the numbers of the filing's own tables.
- Decides: a filing's XBRL numbers are not pushed as items of their own; the filing, read whole (D27), already carries
  them, and pull mode looks up an exact tagged value when a condition needs one. Table data is pushed one release per
  item (for example one 13F, one statistics release), whole. Nothing gets a price-specific rule: the pipeline keeps its
  shape, and whatever the universe streams goes whole to the model.
- Changes D19 (two classification rules: a filing no longer yields XBRL records to push; one release is one item) and
  settles D27's open item.
- Enforced: `RULES` of `docs/system-design/new-classification.js`; `CATEGORY_NOTE` of
  `docs/system-design/new-facts.js`; the classify node of `docs/system-design/new-design.js`;
  `docs/prd/02-classification.md`, `docs/prd/05-extraction.md`.

## D33 · 2026-10-18 · Extraction only reads; matching and writing belong to the views database

- By: Alex ("你确保抽取环节就只是抽取thesis 理解不，我们探讨的都只是不同classification 该怎么抽取或是走什么数据").
- Decides: extraction reads each item, whole, with its category's template, and hands candidate views and evidence,
  each with its source, to the views database; it never changes the database. Its steps: build the template, read
  (model), check the sources (code), hand over. The views database does the rest of D27: merge duplicate evidence,
  list candidate drivers, match (a short model call), decide by direction and horizon class, send views to the final
  verdict, and route unsure matches, unknown objects and proposed themes to the review pool. The matching setting in
  Config belongs to the views database.
- Enforced: `EXTRACT_STEPS`, `WRITE_STEPS`, `EXTRACT_EXAMPLE_TREE` and `WRITE_EXAMPLE_TREE` of
  `docs/system-design/new-facts.js`; the extract, views and config nodes and the overview edges of
  `docs/system-design/new-design.js`; `docs/prd/05-extraction.md`, `docs/prd/06-views.md`.
- Changed by D39: after extraction the views database matches candidates to open views (D39), not to drivers.
- Changed by D42: extraction attaches each piece of evidence to an existing view it was shown, or to a candidate view,
  as it reads; it still never changes the database, and matching stays in the views database.
## D34 · 2026-10-18 · An SEC filing is dated by the day SEC makes it public

- By: Alex ("ok 可以", to Claude's proposal on classification time rule 4).
- Why: time rule 4 dated an SEC filing by its EDGAR acceptance day, but filings accepted after 17:30 ET are disseminated
  only the next business day morning (Regulation S-T Rule 13). Amazon's 10-Q accepted 2026-07-30 18:11 ET became public
  2026-07-31 06:01 ET, so the rule dated it a day early: it would be ordered before news written that evening, and a
  replay would know it a day early.
- Decides: an SEC filing's publication day is the day SEC makes it public, which is its statutory filing date:
  accepted before 17:30 ET, that day; after, the next business day. The input field `filing_date` already carries
  it. The hour still plays no part in any other rule (D9).
- Known limit: `simulate_classification.py` dates items by `published_at` and does not model this rule; the script is
  not changed at the POC stage.
- Enforced: `TIME_RULES` and `INPUT_SCHEMA` of `docs/system-design/new-classification.js`; the classify node of
  `docs/system-design/new-design.js`; `docs/prd/02-classification.md`.

## D35 · 2026-10-18 · Extraction v1 is final

- By: Alex ("抽取你最后review 一次可以定稿了吗"; on prompts: "不同类型文件是不是都有自己的LLM prompt 这个部分有写明白在PRD").
- Final review (2026-10-18): extraction only reads (D33); every item goes whole to the model with its category's
  prompt; the prompt is one template whose part 2 (the category's reading rule, from classification) and part 4 (what
  the category yields) change per category, part 1 is shared and parts 3 and 5 are filled by code; each of T1–T15 has
  its own prompt (T16 is not tracked by default); the output format is enforced by code, not written in the prompt;
  every view and piece of evidence carries a checked source; failures retry from their step. One assembled prompt
  (T7 news) is drawn on the page and in the PRD.
- Decides: extraction is frozen as v1. Not frozen: how an item too long for one call is cut; the exact wording of each
  category's prompt, written and tested on stored items when it is built, each version recorded in Config. A later
  change needs a new decision.
- Enforced: the extract node's status and `PROMPT_EXAMPLE`, `PROMPT_NOTES` of `docs/system-design/new-facts.js`;
  `docs/prd/05-extraction.md`.
- Changed 2026-10-18 (Alex: "应该不会context 太长这不是一个问题，pass"): cutting a long item is not an open item;
  the only part not frozen is each category's prompt wording. A wording review aligned the page and the PRD: one
  template, one prompt per category; step 2 names what a candidate view and its evidence carry, which the views
  database reads; the source check is split between extraction (the quote is in the item) and the views database
  (the source is in the processing record).
- Changed by D37: frozen together with the input side; the page and the PRDs say 已冻结, not 定稿.

## D36 · 2026-10-18 · One word per concept in the input and extraction modules

- By: Alex ("你和codex 要一起完全对齐用字用词，这个非常重要，不然我们的PRD就是瞎几把写的，你深度的抠").
- Why: rounds of review kept finding new wording mismatches, because each fix changed only the instance named. Claude
  and Codex each took an independent inventory of every wording per concept in scope (universe, classification and
  tagging, dispatch, extraction, and the sentences at their boundaries), and merged them into one glossary.
- Decides: the glossary in `docs/prd/00-system.md` (section "用词") names one word per concept and the words not to use.
  Notable choices: 信息 is the unit, 文件 is a text-form 信息 and 表格数据 a table-form one; 申报 and 申报代码 (not 表格代码,
  which collided with 表格数据); 体裁 for transcript, minutes and the like (形式 is only text or table); 提示词模板 and
  上传模板 (never a bare 模板); 角色 for the prompt's persona (身份 is the identity fields); 看法 for what authors in a
  document think and 观点 only for the system's views; 说法 for what parties say and 主张 only for a view's claim;
  主题层 and 对象层 for a view's level, separate from an evidence tier; 作者 (not 发布方). No rule changed.
- Second pass, same day: Codex checked the scope against the glossary and every flagged wording was counted over the
  whole scope. 代码 is only the party that does the work (程序 is not used); an identifier is an 对象标识 (CIK, 股票代码,
  公司名, 加密货币代码, 商品代码, 主题编号), so classification rule "只看代码" now reads "只看对象标识"; 作者类型 is
  the one name for the author's kind; 类型 is not used for 类别; 相关对象 covers any object found in the reference data,
  in the universe or not (D16); T10 is renamed 官方行动与记录 so the category, its group 官方行动与宏观统计 and the
  universe use one word; a SEC filing's source is its 申报编号 (accession number). No rule changed.
- Third pass, same day (Codex on the result): an object kind is written in full, 公司 and 加密货币 (not 股票 or 加密),
  and 股票代码 replaces ticker in prose; 代码 also covers code not yet written or to be changed. No rule changed.
- Enforced: `AVOIDED_WORDS` and `wording_scope` in `docs/check.py` scan the in-scope page data and PRDs (the glossary
  section itself excluded) and fail on any avoided word, with a control sentence the check must catch.
- Changed by D41: the wording scope also covers the views database and the labels node.
- Changed by D52: 对上 → 比对 (比对记录, 比对标注), 并进 → 归入, and the pull-mode proposal's 并入 → 合并; ruled out with
  control pairs.
## D37 · 2026-10-18 · Freeze v1 of the input side and extraction

- By: Alex ("好你把写完的freeze了在html 上……我们要继续move on").
- Decides: the research universe, classification, Config, dispatch, extraction and the human review pool are frozen
  as v1 in their 2026-10-18 text, which includes D25–D36. What each PRD lists under "还没定的" stays open, among them the
  themes in the theme library, upstream supply and the identifier tables, the review pool's output, each category's prompt
  wording. A change to a frozen module needs a new decision. The views database and the final verdict stay in design
  and pull mode is partly decided; the work moves on to them as Alex takes them up.
- Enforced: the six nodes' `status` in `docs/system-design/new-design.js` (the page marks each 已冻结), the status
  lines of their PRDs and of `docs/prd/README.md`; 已冻结 replaces 定稿 in the glossary and the wording check.
- Changed by D41: extraction, Config, the universe and the review pool were changed for the rebuilt views database.

## D38 · 2026-10-20 · The views database rebuilt: a view is a question with a five-rung ladder and a due date

- By: Alex, over the rebuild discussion logged in `docs/views-rebuild-log.md` (steps 1–13). On the unit: "这个 hypo 更像是一个
  thesis with a state"; on rungs: "我们用 5 个 state 吧 very bullish, bullish, neutral, bearish, very bearish"; on kinds: "有些事情不一定对所有人都是
  bull / bear，有可能完全相反！……这个需要明确分开来看"; on one layer: "一条观点一定是有一个明确的 ladder 和到期日，这样才构成一个观点呀";
  on periods: "这个肯定要写清楚日期", then yes to one view per year (this year and next); on chains: "是不是用 linked list 来存储 lineage 就好";
  on the reading rule and the remaining fixes: "looks right".
- Decides:
  - A view is one question, a ladder of five fixed rungs and a due date, never rewritten. It looks at one number (which
    year, whether a period amount or a point-in-time value, and the source it is answered from) or the state of one
    thing (scope and stage). An object view's identity is its object plus what it looks at; a theme view's identity is
    only what it looks at (the theme is where it is filed), so theme views are compared across all themes. A view looks
    at one thing: a question that needs a number and an event is two views joined by a dependency; a question whose
    parts can move in opposite directions is two views, joined only if one really depends on the other.
  - Object views (companies, crypto, commodities) have the rungs strongly bullish to strongly bearish, meaning good or
    bad for the business, fixed at creation. Theme views have five outcomes on one axis, named by outcome, with no
    bull or bear; each dependent object view's arrow says which end is bullish for it. The stance on the price is our
    state against the consensus, which is not designed yet.
  - Each rung is an observable yes-or-no condition; rungs do not overlap, cover every outcome, and exactly one holds at
    the due date; there is no "partial". A number ladder is ranges of one number in its stated year, judged by code;
    an event ladder is the states one thing can be in on the due date, judged by the model from "happened" evidence
    only, citing it. The model sets the rungs when the view is created; they do not change before the due date.
  - The due date is when the debate is settled, usually 6–12 months out; a number's due date is the day it is
    published; quarterly reports in between are evidence. Number views carry their year (fiscal year for companies,
    calendar year otherwise) and at most this year's and next year's are open at once. The year counts from the latest
    publication day among the items processed so far, which only moves forward (never the wall clock); a year whose
    period has ended gets no new view. An event view is one open view per thing. (Claude's reading of "this year", to be
    confirmed by Alex.)
  - Two positions on a ladder: where it is now (a fact; only "happened" evidence moves it; a point-in-time number takes
    the latest published value, a period amount has none before it is published) and the state (where we think it
    lands; re-judged by the model each time from all of the view's evidence and its dependencies' current state, never
    stepped from the last state; citations checked by code; temperature set in Config). A replay reads the stored
    judgements; it does not call the model again.
  - Evidence is a sentence or number, stored once, with its source and tier (happened, said by a party, third-party
    view, rumour); independent sources are counted by original source; the direction it pushes is written on the link
    between evidence and view by each re-judgement.
  - A dependency B → A carries one direction (which end of A is bullish for B; between themes, same or opposite). A
    relation that looks good-then-bad means a middle view is missing. Notices pass, evidence never does; code marks
    B's evidence that is also linked to A. A number dependency is pinned to its year (a closed A is read by its answer;
    an A not yet created is waited for and connected when created; an unanswerable A is a missing input, never
    neutral); an event dependency follows A's chain. A new view may depend on theme views (found by search) or on
    another object's views (supply chain). B is told when A changes rung, when what B reads changes, or when A cannot
    be answered. No cycles, checked on the graph each
    round reads. A new theme view that succeeds nothing is checked against every open view for missing arrows.
  - Succession: the next view on the same thing succeeds the last one, forming a chain that holds the lineage; no
    forks; the successor keeps the rung orientation; a wrong succession is revoked by an appended record; a successor
    proposes its predecessor's dependencies one year on.
  - A view ends answered (the first published value from its stated source; the score compares it with the last state
    committed before the item carrying the answer was processed), unanswerable (with its reason, not scored; a
    processing failure is retried, not unanswerable) or merged. A view whose object leaves the universe is closed as
    unanswerable for now; whether it is scored is open.
    A number view past its period and waiting for its answer does not count against the two open years.
- Replaces: D26's structure (object → driver → view with a claim, direction, horizon class, confirm and falsify
  conditions and a premise); D30's add-only conditions, conflict trigger and consensus-by-code (open again); D31's
  premise links with a seen version.
- Enforced: `VIEW_TREE`, `VIEW_KINDS`, `KIND_NOTE`, `LADDER_EXAMPLES`, `LADDER_RULES`, `POSITIONS`, `TIERS`, `TIER_RULES`,
  `DEPENDENCY_TREE`, `DEPENDENCY_RULES`, `CHAIN_RULES`, `LIFECYCLE_TREE`, `LIFECYCLE_NOTES`, `VIEW_FIELDS`, `EVIDENCE_FIELDS`
  of `docs/system-design/new-facts.js`; the views node of `docs/system-design/new-design.js`; `docs/prd/06-views.md`.
- Changed by D42: a yes-or-no question has two rungs; a re-judgement reads the view's evidence that has not been
  replaced, and a round that brought only repeats and no dependency change does not re-judge; "replaced" also covers a
  later statement by the same speaker and an official confirmation or denial of a rumour; a dependency links only an
  input (B's answer uses A's answer), and a cycle is rewritten.
- Changed by D45: what stands is what points to Alex's words or an earlier decision: a view as a question, a
  ladder of five rungs (two for yes or no) and a due date where the debate resolves; object and theme views; the
  state judged by the model from all evidence not replaced and from the dependencies; evidence stored once with its
  push on the link; tiers (D30); dependencies with arrows read by kind; succession as a chain; this year's and next
  year's number. Where it is now, how rungs are written and judged, answer sources, how the years are counted, the
  details of log step 13, unanswered and waiting views, and how answers are scored are proposals (D45).
- Changed by D51: B is re-judged when what it reads changed (its evidence, or a dependency's conclusion marked
  changed), not only when A changes rung.
## D39 · 2026-10-20 · Writing into the views database: match by where a candidate belongs, then one round of re-judging

- By: Alex ("已经存在的观点就 merge，日期遵照之前已经存在的期限"; "我们来深度聊一下 thesis 被抽取之后我们怎么和现有的数据结构做对比和整体的纳入、合并机制";
  "it's very similar to like a search engine … then what is the best judge"; steps 11, 14 and 15 of the log).
- Research: `reports/观点库重建 去重 证据 血缘（Codex 调研）.md`, `reports/观点库重建 接续 依赖 到期（Codex 调研）.md`, and the two
  D27 reports, which still hold: identity sits on a key and similarity only finds candidates; choosing from a few
  candidates beats judging pairs; "new" is the harder half; small sets given whole beat retrieval.
- Decides: one item is one round, in dispatch order. Code checks sources; stores evidence once (a retry reuses it, a
  corrected version replaces the old one, which is kept and marked replaced); matches by key (a number candidate with
  the same answer source and year as an open view is that view); builds the list (all open views of the tagged
  objects plus each chain's last closed view; for themes, five more from a keyword and embedding search over all open
  theme views; number candidates beyond next year dropped; an empty list still goes to the model, which only decides
  new view or not opened). One model
  call without the document decides, for each candidate, attach to #k (the same thing or a part of it), succeed #k,
  new view, not opened (too broad), or unsure, with a reason, and for each piece of evidence which views it pushes.
  Code accepts only listed ids, the succession rules and the open-view limits. Each object's queue writes its own
  views, themes first; a list that changed before the write is matched again. New views pick their dependencies
  (model; code checks cycles). Then every touched view is re-judged once, upstream before downstream; a change of rung
  passes on. Merges happen three ways: attach (at matching), succeed (at matching), merge (a daily duplicate check
  started by pull mode: the later view closes as merged into the earlier one, its links are added there and arrows
  follow the merge). Evidence that links to no view is not stored; the processing record notes it. Records are
  append-only: matching, re-judging, succession, closing, merging and labels each add a record with the dispatch
  number, so any past day can be replayed from the records. An item reads the state left by items with smaller
  numbers plus what its own round has already written (upstream views judged earlier in the round). A late item is
  re-judged when it arrives and does not rewrite past states. A corrected item touches every view linked to its old or
  new evidence. A merge re-checks the direction of the arrows it redirects against the kept view's rungs, and cycles. Storage is one relational database with append-only tables; full-text and vector indexes live in
  it and can be rebuilt; no separate vector or graph database; the product is chosen at build time.
- Open: what to do with "unsure" (create and let the duplicate check merge, or attach to the closest view).
- Replaces: D27's steps 2–5 (candidate drivers, matching to a driver, deciding by direction and horizon class) and
  D33's list of what the views database does after extraction; D31's rule that a late item reads the versions of its
  publication day.
- Enforced: `INTAKE_STEPS`, `MATCH_OUTCOMES`, `MATCH_NOTES`, `MERGE_KINDS`, `INTAKE_EXAMPLE_TREE`, `ORDER_RULES`, `STORE_NOTE`
  of `docs/system-design/new-facts.js`; the views node and the overview edges of `docs/system-design/new-design.js`;
  `docs/prd/06-views.md`.
- Changed by D42: evidence arrives attached to the views it bears on, or to a candidate view, so matching no longer
  decides which views a piece pushes; the same call instead compares each piece with the evidence its view holds
  (repeat, replacement, new evidence); a repeat is one more source of the piece it repeats; a corrected version changes
  only its own source, so "its evidence replaces the old version's" holds only when the item is itself the original
  source.
- Changed by D44: no key is matched by code. Whether a candidate is an open view, a part of it or its next period is
  decided only by the model in the matching call; code builds the list and accepts only listed ids and the succession
  rules. "One open view per thing" is the rule the model applies when matching, not a code check.
- Changed by D45: matching searches a few existing views and the model decides the same view, its next period or a
  new view (no match, or only a weak one, is new). How the list is made, the year filter, the outcomes "part of an open
  view" and "not opened", the daily duplicate check, the "already counted" mark, the order inside a round,
  re-judging a late item on arrival and the storage are proposals.
## D40 · 2026-10-20 · The matching judge: a general model first, every match recorded, humans label, a small model later

- By: Alex ("let's do a general LLM at this point because we need to make it work first and … for the traces that we collect
  essentially that just have a logging system so that we can do RLHF in the process to human label and then use that data
  to train a small model classifier that's faster in the future for this purpose").
- Research: LLM-labelled training sets train small matchers about as well as hand-labelled ones, at 34–459 times less
  inference time (Steiner and Bizer 2026, arXiv 2606.28823); fine-tuned matchers reach high F1 with labelled pairs
  (Ditto); selecting among candidates suffers position bias as the list grows (ComEM).
- Decides: matching (step 5 of D39) uses a general model through Config's matching setting. Every match writes a
  matching record: the item, the candidates as handed over, the list in the order shown and how each entry got there,
  who decided (code, the general model, later the small model, or a person), the request, the raw answer and the Config
  version, the decision with reasons and code's checks, what was written, and later records pointing back (a merge by
  the duplicate check, a human label that differs). Code samples records for labelling: every unsure one, every one a
  later merge reversed, every one code refused, and a weekly random sample started by pull mode. A person labels with the same options plus
  "can't tell", with a reason; Alex sets the standard on a first batch. Labels for the test set are made without seeing
  the model's answer; the test set is fixed and scored once per change of judge. Labels measure the matching (precision
  and recall of "new", wrong attachments, order sensitivity) and, with the model's own decisions, train a small
  matcher; it decides only where it is confident and its agreement with human labels on the test set passes a bar Alex
  sets, and the general model decides the rest. Labelling never blocks the stream and never changes the database
  directly; duplicates it finds go to the duplicate check. This is human labelling and supervised training; no
  reinforcement learning is needed. Requests and answers of the other model calls are recorded too; only matching is
  labelled in v1.
- Open: who labels, how many are sampled each week, the labelling screen, the bar for the small model.
- Enforced: the labels node and its edge in `docs/system-design/new-design.js`; `JUDGE_STEPS`, `TRACE_FIELDS`, `LABEL_RULES`
  of `docs/system-design/new-facts.js`; `docs/prd/06-views.md`.
- Changed by D42: matching and its labels also cover the evidence outcomes (repeat, replacement, new evidence).
- Changed by D44: code never decides a match; "who decided" is the general model, later the small model, or a
  person.
- Changed by D45: the general model, the records, human labels and a small model later stand; which records are
  sampled, the test set, measuring with labels, the training data and "no reinforcement learning" are proposals.
## D41 · 2026-10-20 · What the rebuilt views database changes outside it

- By: Alex ("you need to add it to the current PRD, you need to add it to the current system design … put everything into context").
- Why: D38–D40 change what extraction hands over, which model settings Config holds, how the universe describes macro
  links, what the review pool receives, and make the final verdict and pull mode drafts obsolete. Leaving them would
  leave the page and the PRDs saying two things.
- Decides:
  - Extraction (frozen, D37): a candidate view now carries its object, kind, what it looks at, the question, five rungs,
    due date and answer source; evidence carries when the thing happened and which candidate or existing view it
    belongs to (or neither; matching decides). Prompt part 1 adds the writing rules for views (one thing; a number's
    year and answer source; a theme view's scope set by the rule or decision that governs it). Prompt part 5 gives the
    objects' existing views (question and what they look at, no state or evidence) instead of driver names.
    The category reads no longer mention conditions (T1, T10, T12, T14), and the example shows a theme view and an
    object view, with the filing's own English sentences as the checked quotes.
  - Config (frozen): the views database has one setting per model call (matching, picking dependencies, re-judging,
    the duplicate check); a setting includes the temperature; every model call records the Config version.
  - Universe (frozen): rule 8 says macro and geopolitics reach a company through dependencies.
  - Review pool (frozen): from the views database it receives the themes proposed when a candidate is about something
    in the world with no theme in the universe, and failed items; unsure matches no longer go there. A candidate about a
    company outside the universe is not built and only noted in the processing record.
  - The final verdict and pull mode are old drafts to be redone when Alex takes them up; until then their pages carry
    the note. Pull mode's role in the rebuilt design is the due date, the daily duplicate check and the periodic labelling sample.
  - The wording scope (D36) covers the views database and the labels node; the retired words are 驱动, 检验条件 (证实条件,
    证伪条件), 前提, 期限档, 主题层 and 对象层, 主张, 已证实 and 已证伪, and 分发序号 (the glossary's word is 顺序号).
- Enforced: `TEMPLATE`, `PROMPT_EXAMPLE`, `CATEGORY_READS`, `CATEGORY_NOTE`, `EXTRACT_STEPS`, `SOURCE_NOTES`,
  `EXTRACT_EXAMPLE_TREE` of `docs/system-design/new-facts.js`; `CONFIG_SCHEMA` of `docs/system-design/new-config.js`; `RULES`
  of `docs/system-design/new-universe.js`; the extract, config, review, verdict, pull nodes and the summary of
  `docs/system-design/new-design.js`; `AVOIDED_WORDS`, `VIEWS_CONSTANTS` and `wording_scope` of `docs/check.py`; the glossary in
  `docs/prd/00-system.md`; `docs/prd/00-system.md`, `01-universe.md`, `03-config.md`, `05-extraction.md`, `07-final-verdict.md`,
  `08-pull-mode.md`, `09-review-pool.md`, `README.md`.
- Changed by D42: the last prompt part also lists the views the related objects' views depend on; evidence is attached
  to a view on that list or to a candidate view, never to neither; universe rule 8 links a company to a theme view whose
  answer its own answer uses.
- Changed by D45: Config has no duplicate-check setting while the duplicate check is a proposal; extraction's prompt
  asks for one thing per view and a number's year, not for answer sources or a theme view's scope; how complete a
  candidate view is when extraction hands it over is open.
- Changed by D51: the views database has two model settings in Config (matching, re-judging); dependencies are
  chosen in the matching call.
## D42 · 2026-10-20 · Extraction hands over evidence and candidate views as two things; evidence is matched to what its view already holds

- By: Alex, over steps 17–30 of `docs/views-rebuild-log.md`. On attaching evidence: "evidence 怎么在抽取的时候不挂钩
  thesis？这怎么可能。"; on two rungs: "如果只有是否就不用硬分，可以 binary"; on cycles: "我觉得这个应该是 thesis 的定义问题"; on the evidence path: "It's
  not clear to me how this logic is similar to thesis", then "我觉得差不多了"; on writing it up: "抽取现在分成了 evidence / thesis,
  你要特别分开讨论和解释这部分的设计". The first write-up grew new words and rules for edge cases raised in review
  ("卡片又是什么。。。你为什么又给自己加了一堆戏？"); the cut-back then dropped four rules that real cases need ("那你本来提的一些东西难道都没用吗？"). Kept:
  what he decided, plus those four ("可以吧"); log steps 31–33.
- Research: `reports/观点库重建 抽取后的证据和观点怎么进库（Codex 调研）.md`, `reports/观点库重建 证据和观点的逻辑仿真（Codex）.md`,
  `reports/观点库重建 对抗式审查：做不到和说不通的地方（Codex）.md`, `reports/观点库重建 证据怎么作用到库里（Codex 调研）.md`; a count on a stored run of the old
  system (log step 30): of 2,499 numbers it read, 383 matched one already read, 214 of them elsewhere in the same
  document. Reviews of the first write-up: `reports/观点库重建 D42 审稿第 1 轮（Codex）.md` to `第 5 轮`.
- Decides:
  - Extraction (frozen; changes D41's hand-over). Prompt part 5 lists the related objects' open views and the views they
    depend on (question and what each looks at, no state or evidence). One read hands over two things, each with its
    source: evidence, attached to the views on that list it bears on or to a candidate view of the same item; and
    candidate views, for important matters none of those views covers, written as D41 has it and carrying the evidence
    that raised them. The same thing said in several places of one item (text and table) is one piece with several
    sources. Evidence attached to nothing is not extracted; code checks the attachments.
  - Views database (changes D39 and D40). The one matching call also compares each piece of evidence with the evidence
    its view holds that has not been replaced; a piece attached to several views is stored once and compared once. A
    repeat (a reprint, the same number in text and table, the same speaker saying it again) adds one more source to that
    piece. A replacement (two statements of the same thing: the same speaker's later number or wording, an official
    confirmation or denial of a rumour, the original source's own corrected sentence) keeps the one said later, by the
    day it was said, and marks the earlier replaced, kept as history, so a late older statement goes straight into
    history; views still linked to the replaced piece are linked to the new one too. Anything else, and anything unsure,
    is new evidence. An upstream corrected version changes only its own source: a corrected reprint leaves the piece it
    reprinted alone; the original source's corrected version replaces a changed sentence through matching and marks a
    deleted one replaced. Matching records and labels cover these outcomes.
  - Re-judging (changes D38). A re-judgement reads the view's evidence that has not been replaced, each piece with the
    one it replaced, and its dependencies' current state; a round that brought only repeats and no dependency change
    does not re-judge the view.
  - Ladders (changes D38). A yes-or-no question has two rungs: bullish and bearish for an object view, named by outcome
    for a theme view.
  - Dependencies (changes D38). B depends on A only when B's answer uses A's answer; the other side's reaction to what
    has already happened is evidence. Two questions that are each other's input are badly cut and are rewritten; code
    refuses an arrow that closes a cycle.
  - Wording: 重复, 替代, 新证据 and 被替代 enter the glossary; a ladder has five rungs or two; 个股 is written 公司; a bare 候选 had two
    meanings and is split into 候选观点 and 清单; prompt part 5 is 第 5 块 (not 最后一块). 五格的梯子, 个股 and a bare 候选 are checked by
    `docs/check.py`.
- Not decided (PRD 05 and 06 under 还没定的): opening views when an object starts empty (a start-of-coverage step that sets
  two or three key debates); changes inside a rung that do not reach dependents; whether theme views take companies'
  views of the macro; sampling extraction's attachments for review. The other questions raised in steps 25–27 stay in
  the log.
- Enforced: the extraction and views constants and pages of `docs/system-design/new-facts.js`; `RULES` of
  `docs/system-design/new-universe.js`; the summary and the extract, views, labels and universe nodes of
  `docs/system-design/new-design.js`; `AVOIDED_WORDS` and the generated blocks of `docs/check.py`; the glossary in
  `docs/prd/00-system.md`; `docs/prd/00-system.md`, `01-universe.md`, `05-extraction.md`, `06-views.md`, `README.md`.
- Changed by D45: the dependency definition (only an input; a cycle is rewritten) is a proposal; Alex said a cycle
  is a problem of how the theses are defined.
- Changed by D58: prompt part 5 also gives each view's due date; a view covers what happens up to its due date, and
  what happens after it goes in as a candidate view, so a closed view a dependent still points to is succeeded.

## D43 · 2026-10-20 · A second stable version of the design is sealed

- By: Alex ("完整的刷一遍，我要又一个稳定版本的html fe system design and prd").
- Decides: after a full reasoning refresh of every module in the D22 order and `python3 docs/check.py` passing, the
  design page, its data, the PRDs, DECISIONS, CURRENT_STATE and the views rebuild log are copied to
  `docs/archive/2026-10-20-v2/` with `SHA256SUMS`; the archived page opens from that folder. Module statuses do not
  change: the input side and extraction stay frozen v1 as amended by D41 and D42, the views database stays in design
  with D38–D42 decided, the final verdict and pull mode stay old drafts to redo. Like v1, the sealed copy is never
  edited; a later stable version gets a new dated copy.
- Enforced: `docs/archive/2026-10-20-v2/` and its `SHA256SUMS`; the status in `docs/CURRENT_STATE.md`.
- Changed by D44: v2 still shows a key matched by code before the model; the current stable version is v3
  (`docs/archive/2026-10-20-v3/`).
## D44 · 2026-10-20 · Matching is the model's alone: no key matched by code

- By: Alex, at log step 16 ("let's do a general LLM at this point because we need to make it work first"), and after v2
  was sealed ("I just want LLM to do the matching? Why is it still matching by the key with code? … I told you to make
  it easy so that we can prototype in the beginning").
- Why: the key was Claude's proposal in log step 15 (four layers: a key matched by code, the list, the model as judge, a
  small model later). Alex's answer chose the general model to make the system work first; D39 still wrote the key as
  a code step before the model, and its check on open-view limits needs the same key to tell "the same number" or "the
  same thing". In log step 26 Claude found the key does not hold (one answer source serves different questions, an
  amount and a growth rate; one number gets two names) and proposed dropping it; the step stayed through steps 31–33
  and v2 (D43) was sealed with it.
- Decides: whether a candidate view is an open view, a part of it or its next period is decided only by the model in
  the matching call, from the short list. Code builds the list (as in D39) and accepts only listed ids and the
  succession rules. "One open view per thing (a number: this year and next)" is the rule the model applies when
  matching, not a code check. Writing into the views database has eight steps; matching is step 4. The matching
  record's "who decided" is the general model, later the small model, or a person. A number view keeps its answer
  source: it says where the answer is read at the due date.
- Seals: the corrected design is sealed as v3 in `docs/archive/2026-10-20-v3/` with `SHA256SUMS`, as D43 sealed v2;
  v2 stays as sealed and is superseded.
- Enforced: `INTAKE_STEPS` and `TRACE_FIELDS` of `docs/system-design/new-facts.js`; the views and labels nodes of
  `docs/system-design/new-design.js`; `docs/prd/00-system.md` (principle 7, the glossary), `docs/prd/06-views.md`;
  `docs/check.py` fails on the word "钥匙".
- Changed by D45: the answer source of a number view is a proposal (who judges a rung, and how), not decided.
- Changed by D58: "one open view per thing" is the rule matching keeps when it opens views; a view a person reopens
  by hand is outside it.
## D45 · 2026-10-20 · Only what Alex said or decided is decided; Claude's proposals are listed apart

- By: Alex ("我明明就很清楚的告诉你了我过去所有的讨论和思路，你不要 diverge and make shit up, review this shit"; to the
  rule "写成‘已定’的，每一条都要指得到你的一句原话；指不到的，一律放进‘没确认的’": "要，我们重点搞定观点库模块好吧，
  然后抽取 thesis /edvdence 在前面的逻辑分清楚，把这两个干 solid").
- Why: checked against his 46 messages of the views rebuild (`reports/观点库 设计和 Alex 原话对照（2026-10-20）.md`),
  D38–D44 wrote as decided proposals he had answered in part or not at all, details from Codex reviews, and log lines
  recording his agreement where he had said "ok" and asked for a recap. Applying the rule also found that D39 had
  replaced D31's late-item rule without him.
- Decides: in the views database and in what extraction hands to it, a rule is decided only when it points to Alex's
  own words, his reply to that question, or a decision in force from before the rebuild (D11, D14, D16, D30, D31,
  D33, D37). Everything else is a proposal: the page and `docs/prd/06-views.md` list Claude's 17 proposals apart
  ("Claude 提的、Alex 还没定的"), and none is built until he decides it. On his words: a candidate that matches nothing,
  or only weakly, is a new view, so there is no "unsure" outcome; evidence tiers and counting by original source stand
  (D30), and only "happened" evidence settles which rung holds; a late item reads the state of its publication day and
  is written with its real date, and a view whose object leaves the universe is kept as no longer tracked (D31). The
  proposals: where it is now; how rungs are written; who judges a rung, with answer sources; how this year and next are
  counted, with a code filter; how the list is made and a theme view's identity; the outcomes "part of an open view"
  and "not opened"; dependency as input only, with the cycle refusal; the succession and notice details of log step
  13; the order inside a round; unanswered and waiting views; the daily duplicate check (with Config's setting for it
  and pull mode's daily start); the "already counted" mark; the code check on cited evidence and replay; how answers
  are scored; re-judging a late item on arrival; the labelling details; the storage. Open in extraction: how complete a
  candidate view is when extraction hands it over (log step 30's object, what it looks at and evidence, or D41's
  question, ladder and due date); the prompt no longer asks for answer sources or a theme view's scope.
- Changes: D31 (its late-item rule stands again), D38, D39, D40, D41, D42, D44 (notes under each).
- Checked: Codex read-only against the same 46 messages; six sentences still pointing past Alex's words were fixed
  (the calendar year for numbers other than a company's, searching only open views, re-judging once per round, "which
  item comes first does not shape the view", the late February report in the example, and examples that assumed a
  complete candidate view); none of the 17 proposals turned out to be something he had agreed to.
- Seals: the design is sealed as v4 in `docs/archive/2026-10-20-v4/` with `SHA256SUMS`, as D43 sealed v2.
- Enforced: `VIEWS_PROPOSED`, the views constants, `TEMPLATE`, `EXTRACT_TWO`, `EXTRACT_SORT_TREE`, `EXTRACT_EXAMPLE_TREE`
  and `EXTRACT_OPEN` of `docs/system-design/new-facts.js`; the summary, the extract, views, labels, config and pull
  nodes and the overview edges of `docs/system-design/new-design.js`; `docs/system-design/new-config.js`;
  `docs/prd/00-system.md`, `03-config.md`, `05-extraction.md`, `06-views.md`, `08-pull-mode.md`, `README.md`;
  `docs/check.py` renders the proposals into `06-views.md`.
- Changed by D46: Alex settled the proposals one by one; the ones he decided are in D46, the three about due dates,
  unanswered views and the daily duplicate check wait for pull mode, and the rest stay listed apart.
## D46 · 2026-10-20 · Alex decides Claude's views proposals one by one

- By: Alex, asked item by item. (1) "A thesis has a state. That's it … There's only one state." (2) "ok". (3) "Just
  use the … model and right now we're only talking about data streaming in … the next financials come in, it will
  basically have evidence that will validate or invalidate that thesis … We're talking about like push mode, streaming
  data, not the pull mode that we have that has not been designed yet." (4) "when they say by this year, it just means
  by this … year, December 31st. If it's next year, just next year, December 31st." (5) "It's going to trigger a search
  engine that is overlaid on top of this database. It's going to return maybe like top n, n being 5 or 10 … semantic
  search … Elasticsearch. And then you basically let the model check which one is the matching thesis or relevant
  evidence"; "Yes, and the recall criteria or the search criteria needs to be designed … this is the final decision."
- Decides:
  1. A view has one state: where it sits on its ladder, our view, pushed toward bullish or bearish by evidence and
     judged by the model on facts. There is no second position.
  2. How a ladder is written: each rung a result that can be checked, rungs neither overlapping nor leaving gaps, so
     exactly one holds at the due date; no vague "partial" rung, a partial outcome is spelled out as its own rung;
     neutral says what it is compared with; one ladder holds one kind of thing, and a question needing a number and
     an event is two views linked by a dependency.
  3. The model reads the information that brings an answer like any other evidence; there is no answer source and no
     code judging a rung. Due dates and answers belong to pull mode, not designed yet; the proposals on unanswered
     and waiting views, the daily duplicate check and how answers are scored wait for it.
  4. A number view names its year: this year is the year the item comes in, to December 31, and next year the one
     after; a company's numbers follow its fiscal year (the one the item falls in is this year). At most this year's
     and next year's are open; a candidate beyond that is not opened. No code filter.
  5. Matching: a search engine over the views database (like Elasticsearch; semantic, keyword or both is to be
     designed) searches the
     whole database, open and closed views, for a candidate view and returns the top N (N in Config, 10 to start); the
     model decides the same view (evidence attached, ladder and due date kept), its next period (succession), or a new
     view (no match, or only a weak one). A piece of evidence searches only the evidence of the view it is attached to,
     top N, and the model decides repeat, replacement or new evidence. How the search ranks is to be designed.
  6. A candidate that is a part of an open view goes into that view ("H20 in China" into "China revenue"). Alex: "行
     但是这个观点的颗粒度我们需要之后明确，例如 nv 中国区收入就很关键肯定不能 bundle 到总收入；而且如果太粗那你会
     发现所有观点都基本是财务指标这是不行的". How big a view is stays open, with a research task: what a thesis looks
     like from a hedge fund's side, what to combine and what to carve out.
  7. A candidate that bundles several things that may move in opposite directions is not opened; its evidence counts
     only where it is also attached to a specific view. Alex: "Yes, I think it's okay … make note that the granularity
     of these theses matters … we need to run a full research on what a thesis actually looks like from a hedge fund
     perspective."
  8. Dependencies: the model decides, like an analyst, which views' conclusions a new view needs and in which
     direction; what has already happened is evidence, not a dependency. Code keeps the graph free of loops: an arrow
     that would close a loop (a new arrow, or one moving to the next period) is refused and sent back to the model,
     which decides how to rewrite it.
     Alex: "这个的判断不是 LLM 来吗？…hedge fund analyst 会怎么做？"; "你自己要有 circular dependency avoidance 机制".
  9. Succession: one view has at most one next period, and the next period keeps the ladder's direction (thresholds may
     change). The other succession details Claude proposed are dropped. Alex: "可以".
  10. One item's changes are one round: upstream views are judged first, then downstream ones, which read the upstream
      state judged in this round; each view is judged once per round. Alex: "global thesis is impact everything …
      like a celebrity … it connects to everyone."
  11. Views relate in one way only: B refers to A's conclusion (its state and reasons), which is not stored as B's
      evidence, so the system cannot prove itself with its own judgements. A message counts once: about A, it is A's
      evidence and reaches B through A's conclusion; about B, it is B's; if B does not refer to A, a message about A
      is B's evidence too. Whom a view refers to is set when it is built. The "already counted" mark is dropped. Alex:
      "我觉得什么特殊处理代码这种都是非常 dirty 的解法，你现在给我想清楚 what is the best way"; "可以".
  12. Every judgement cites its evidence by number in a fixed answer field; code looks each number up (it belongs to
      this view and is not replaced); if one fails, the judgement is not written, the reason is recorded and the model
      judges again. What was judged on a past day is read from the stored records, never asked again. Alex: "就是有
      source 注解和 lookup 对吧，那你要写明白这个机制".
  13. The timeline only grows forward, in the order we learned things. A late message about a matter that already has
      a newer statement does not count: it is not added to the view, only noted in the processing record; a late
      message about something we did not know counts, with its real date. This replaces D31's late-item rule. Alex:
      "if data is coming in out of order … it shouldn't be appended … Think about this entire relation of building a
      time lineage"; "go ahead".
  14. Labels: every match is recorded; people label two kinds, the ones code refused and a few drawn at random from
      time to time; the rest is filled in later. Alex: "是，之后细节在补，把这个模块画出来就好".
  15. Where the data is stored is decided when the build starts. Alex: "可以".
  Still Claude's proposals, for pull mode: unanswered and waiting views, the daily duplicate check, how answers are
  scored at the due date.
  Checked by Codex against the 76 messages: the rewrite of a loop is left to the model; the search method is open
  (N starts at 10); a view also re-judges when a view it waits for is built (log step 13's tree); prompt part 5
  says who refers to whom, so extraction can keep a message about A off B.
  16. Extraction writes a candidate view in full on the spot: question, ladder and due date, with its evidence; the
      model has the whole document then, and new views are few. Alex: "写全".
- Seals: the design is sealed as v5 in `docs/archive/2026-10-20-v5/` with `SHA256SUMS`.
- Changes: D45's list of proposals (settled except three for pull mode); D3 and D41 (Config also holds the
  search size N).
  D31 (the late-item rule is replaced by item 13).
- Enforced: `LADDER_RULES`, `POSITIONS`, `VIEW_TREE`, `INTAKE_STEPS`, `INTAKE_SHAPE`, `MATCH_NOTES`, `EVIDENCE_NOTES`,
  `TRACE_FIELDS`, `VIEWS_OPEN`, `VIEWS_PROPOSED` of `docs/system-design/new-facts.js`; the views and config nodes of
  `docs/system-design/new-design.js`; `docs/system-design/new-config.js`; `docs/prd/00-system.md`, `03-config.md`,
  `06-views.md`; `docs/check.py` rules out 检索 for 搜索.
- Changed by D51: item 9's re-judging on succession comes back as a case of the one re-judging rule; Config's
  views settings are matching and re-judging.
- Changed by D54: there is no answer apart from the state, which is frozen at the due date; the proposal on how
  answers are scored is dropped.
- Changed by D58: item 4 limits which years a candidate may open (this year and next, one view per year); last
  year's view stays open until its due date. Item 8: a dependent theme view writes whether the two ladders run the
  same way or opposite.
## D47 · 2026-10-20 · End-to-end consistency from the universe to the views database

- By: Alex ("now you have everything, you have every log … do end-to-end consistency test … up until the model db
  module … make sure the terms, the usage, the logic, the details … consistently reflected in the PRD and in the front
  end HTML … in multiple rounds. Fire codex sub-agents to check for you, and you also review holistically yourself and
  just make it work").
- How: three Codex read-only reviews (wording, logic with two worked examples, page against PRD against DECISIONS)
  and Claude's own read of every in-scope PRD and the page; every finding was checked against the text before a fix.
- Decides, wording (one word per concept): the attach word is split by its three senses: evidence 连到 a view, a
  candidate view 并进 an open view, a view 属于 an object (classification: an object is 标 on an item), and `docs/check.py`
  rules the old word out; views relate only by 依赖 (the everyday 参考 is gone from the documents); the rules written
  this round say 证据 or 信息, not 消息; evidence repeats are 转述 (a whole reprint is merged by classification and never
  reaches the views database); the state is 我们的判断 (看法 is what authors say) and is pushed to either end of the
  ladder; a rung is a result that can be checked (能核对); 答案 is only the rung at the due date; the whole item is not
  stored, evidence keeps its one sentence; "one layer" reads "not split into periods"; 链 covers replacements too; the
  view field is "开着还是关了"; the item duplicate in dispatch is "重复的信息"; the glossary gains 并进, 共识, 出处, 原始来源,
  一句话说清; an upstream id names one version (an update is a new item that says which one it replaces).
- Decides, logic: evidence carried by a candidate view is compared after the candidate's place is known (one more
  model call when it goes into an open view); a judgement may cite the views it depends on, which code checks against
  its dependencies; two candidates from one item: a sentence goes to the one it is about; prompt part 5 says who
  depends on whom; the Reuters examples are Reuters' own stories retelling the filing; the universe sends unknown
  identifiers and themes outside the universe to the review pool, not known companies outside it; Config holds the
  choices a person makes (model settings and the search size); T1 and the category note no longer speak of 判卷, and
  T14 no longer of 催化剂.
- Enforced: the page data (`new-facts.js`, `new-design.js`, `new-config.js`, `new-universe.js`, `new-classification.js`),
  `docs/prd/00`–`06`, `README.md`, `docs/CURRENT_STATE.md`; `docs/check.py` rules out 挂 and 消息.
- Second round (Codex, one combined review): rung boundaries say which side each edge falls on; a replacement
  re-judges and a dropped late statement does not; step 4 is one call plus one more only for a candidate that goes
  into an open view; the state is pushed to either end of the ladder everywhere; Config's table names the search
  size beside the model settings; D31 notes that D46 replaced its late-item rule; 转述 in every example; 消息 becomes
  说法 (T7, the rumour tier) and 报道 (classification's example); classification and dispatch show the D47 wording change.
- Third round: the review pool takes themes outside the universe (as suggested themes) and leaves out known
  companies, crypto assets and commodities outside it; classification's rule 13 says the system's own output is not
  accepted (不合格), as its first rule does; a judgement's cited sources include the views it depends on in the
  acceptance and the source notes; the universe node and the extraction page show D47.
- Fourth round: the export-licence ladder's rungs exclude each other (none issued / issued, some with conditions /
  issued, none with conditions); the hand-over table says part 5 shows who depends on whom; the review pool's
  exclusion says only what stays out (known items); dependents read A's state and reasons, not a separate "现状";
  the AMD example says the item is about AMD; classification's cross-reference points to the first step of its
  order. "Usually 6–12 months" stays: Alex agreed to it in log step 10.
- Fifth round: "not opened" also covers a number view beyond next year; an item reads the state left by earlier
  items plus what its own round has written; the review pool leaves out known companies, crypto assets and
  commodities outside the universe (themes outside it come in); the review-pool, Config and extraction statuses show
  the later decisions.
- Sixth round: one finding, CURRENT_STATE's order line now includes what an item's own round has written. The
  rounds found 20+, 11, 4, 6, 4 and 1 issues; the pass ends here.
- Changed by D52: a plain-language pass over the same scope.
## D48 · 2026-10-20 · The views database, with match labelling, is frozen as version 1

- By: Alex ("现在这个 db 模块算是 freeze 了吗还是你需要最后 review"; "Is there any inconsistencies and can we freeze? You
  need to change the front-end module to be frozen, right? … you need to read overall end-to-end because we added a
  lot of details and stuff, so you need to make sure").
- Decides: after the six rounds of D47 and a last read of the system diagram and the front-page summary, the views
  database and match labelling are frozen as v1 in their current text; a change needs a new decision. What
  `docs/prd/06-views.md` lists under 还没定的 stays open (the granularity of a view, to be researched first; big changes
  inside a rung that do not reach dependents; opening views when an object starts empty; consensus; …), and the
  three pull-mode proposals wait for pull mode. The diagram now shows search in the views step, part 5 as questions,
  what each looks at and who depends on whom, failed items from the views database to the review pool, the
  classification result "并到原来那条", frozen statuses on the views and labels nodes, and the final verdict and pull
  mode as old drafts to redo.
- Enforced: the statuses of the views, labels, verdict and pull nodes, the caption, two edges, the summary and the
  classification subtitle in `docs/system-design/new-design.js`; the views page status in `new-facts.js`;
  `docs/prd/06-views.md`, `00-system.md`, `README.md`; `docs/CURRENT_STATE.md`; the sealed copy
  `docs/archive/2026-10-20-v6/`.
- Changed by D51: Alex settled Claude's open items of the frozen views database (2026-10-21).
## D49 · 2026-10-20 · Code review of the frozen views database: contradictions fixed, no new mechanism

- By: Alex ("你可以 freeze 然后 run code review and clean up then push").
- How: a code review of the whole diff against the last commit (the `code-review` skill, run as a separate agent);
  every finding was checked against the text. It fixes only contradictions with decided rules and slips; a finding
  that would need a new mechanism is listed as open, and two that Alex had dropped stay dropped.
- Fixed: another queue's change reaches a view as a notice on its own queue, with that item's sequence number (D31's
  hand-off, lost in the rewrite); the search result counts as something an item reads, so a change before commit
  redoes the work (D31); this year and next count from the item's publication day, never the clock (D12, the
  glossary); prompt part 1 carries the decided rules for writing a view (ladder, due date, year), since extraction
  writes candidates in full; only an open view takes a merge, a closed one can only be succeeded (log step 10); a
  candidate about something outside the universe is not opened (a missing theme goes to the review pool as a suggested
  theme, a known company is only noted; D16, D41, universe rule 7); code checks a dependency names a view that exists
  or a year it waits for; a refused retry follows the failure rule; the labelling sample is the matching answers code
  refused; an upstream id names one version everywhere; the final verdict's note and the diagram no longer say who
  sets an answer; the wording check's message for "NVDA 层" points to 对象观点（NVDA）, and each newer ruled-out word has a
  control pair that must be caught and a corrected sentence that must pass (16 pairs, shown to catch a broken rule).
- Opened instead of built: a waiting arrow can count a sentence twice (the claim that it cannot is removed); which views
  the model chooses dependencies from.
- Left as Alex decided: no notice when a dependency closes or moves to its next period (dropped in D46 item 9); no
  same-day order between two statements (dropped in log step 32).
- Notes: `MERGE_KINDS` and `LABEL_RULES`, named by D39 and D40, were removed by D45 and D46; older "Enforced" lines name
  constants of their time.
- Seals: v7 in `docs/archive/2026-10-20-v7/` with `SHA256SUMS`, the version pushed.
- Changed by D51: the two open items it added are settled (dependencies chosen from the views shown; the double
  count through a waiting arrow does not occur).
## D50 · 2026-10-20 · Clean-up after the freeze

- By: Alex ("都做掉，然后提交推送", to Claude's list: the repository README, the superseded sealed copies, the stale
  end of the views rebuild log, the duplicated constant lists in `docs/check.py`, the local page server).
- Decides: the repository `README.md` describes the current design (the flow up to the views database, one state per
  view, dependencies, the module statuses with the views database frozen, D1–D50). The sealed copies v2–v6
  (`docs/archive/2026-10-20-v2` to `-v6`) are removed from the tree; each is kept in commit `94622a5` and can be
  restored from it. `docs/archive/` keeps v1 (the earlier design, 2026-10-16) and v7 (the current design, D49); D43's
  rule that a sealed copy is never edited stands, and this removal is the one exception, made at Alex's request. The
  views rebuild log's "合成" and "暂时放着的问题" sections, not updated since log step 16, are replaced by a pointer to
  the page, the PRDs and DECISIONS. `docs/check.py` writes each page-data file's constant list once (`PAGE_CONSTANTS`,
  passed into the embedded script) and fails when `new-facts.js` defines a constant no list names, since the wording
  check reads that file one constant at a time.
- Enforced: `README.md`; `docs/archive/`; `docs/views-rebuild-log.md`; `PAGE_CONSTANTS` and `unlisted_constants` in
  `docs/check.py`; `docs/CURRENT_STATE.md`.
## D51 · 2026-10-21 · Claude's open items settled: one re-judging rule, dependencies chosen in the matching call, no consensus

- By: Alex, item by item. Asked which items were his to decide, he had Claude re-check the twelve open items Claude
  had written in, against the latest design ("for yourself to reiterate the issue in case you made stupid mistakes that
  are not issues anymore in the latest version"). Then: "好，一个一个来问我" (the nine no longer issues dropped); on
  re-judging, "A 可以但是设计逻辑要干净点；你思考下和我说", then "ok"; on which views dependencies are chosen from,
  "ok"; on consensus, "What … is a consensus that you're talking about … Every time the evidence updates or whatever,
  the ladder needs to be run by the model to determine whether it's going to shift from neutral to bearish or from
  neutral to bullish … That's the logic"; then "可以你再仔细的对齐一次逻辑". On the page: "那你 FE 为什么写定稿了，这不是瞎写吗？"
- Decides:
  1. Re-judging has one rule: a view is re-judged when what it reads changed. It reads its own evidence and the
     conclusions (state and reasons) of the views it depends on. Its evidence changed when new evidence came or
     evidence was replaced (a repeat alone does not count); a dependency's conclusion changed when that view's
     judgement says so. Every judgement answers "结论变不变" in its fixed form: changed when the rung moved or a key fact
     or number behind the state changed (AMZN's capex guidance from +12% to +25% inside one rung), unchanged when the
     same thing is said again. Code checks only that a judgement that moved a rung, and the first judgement of a new
     view, say changed. This gives Alex's "如果美联储有重大的改动……确实需要重判" (log step 10) to the model and
     replaces the notice on a rung change only. A waiting view just built, and a dependency moving to its successor,
     are cases of the same rule, so B is re-judged when its arrow moves to the next period (one of the details dropped
     in D46 item 9, back as a case of this rule, as Claude told Alex before his "ok").
  2. A new view's dependencies are chosen in the matching call (step 4), from the views the model already has in front
     of it: the search results, the views listed in prompt part 5, and the views new in the same item; there is no
     other search. In step 5 code checks that each is one of the views shown (or a year it waits for) and that no loop
     forms. Writing into the views database has seven steps. Config holds two settings for the views database's model
     calls (matching, re-judging), no longer a separate one for dependencies. A dependency on a view in none of the three
     is missed, like a match the search misses; the records and the labels show it.
  3. Consensus is not part of the design: a view has one state, judged by the model from its evidence whenever that
     evidence changes (D46 item 1). The glossary row, the views notes and extraction's "用来算共识" go. Third-party views
     stay evidence of their tier.
  4. Open items are only what Alex deferred: how search ranks; the granularity of views, researched first (how many
     questions per object is part of it); the labelling details (with how to check evidence that extraction attached
     wrongly or missed); who sets an answer at the due date (with pull mode and the final verdict). Removed as no
     longer issues on the current design: when an event counts as a successor (the model decides in matching); dates
     between now and a due date (the stream reads no dates; what happens on them arrives as evidence); futures on rates,
     currencies and indices (theme views whose rungs are outcome ranges); measuring before the build (a build practice,
     AGENTS.md); a double count through a waiting arrow (a sentence about A counts only on A, so once or not at all);
     opening views on an empty database (stored history streams through the same path); companies' macro opinions
     crowding a theme view (tiers and counting by original source, D30); a hard-coded notice on rung change only
     (settled by item 1); which views dependencies are chosen from (settled by item 2).
  5. The design page tags a module 已冻结 only for a frozen status; the final verdict and pull mode carry a `draft` line
     and a 旧稿 tag. D48 had given them a status line, which the page drew as 已冻结.
- Changes: D30, D38, D41, D46 item 9, D49; the frozen views database (D48) and the frozen Config, extraction and
  universe (D37), through this decision.
- Review: Codex read the change read-only and found three, all fixed: the list check in step 5 and the acceptance
  criteria covered every id, which would refuse a dependency on a view from prompt part 5 or new in the same item (the
  list check now covers where a candidate or a piece of evidence goes; dependencies have their own); extraction's node
  still listed the two removed open items; a re-judgement did not see the view's last conclusion, so "结论变不变" had
  nothing to compare with (the model now compares with the last conclusion, used only for the comparison, never as a
  base to add to). The labels' "refused by code" now reads "failed step 5's check".
- Seals: v8 in `docs/archive/2026-10-21-v8/` with `SHA256SUMS`.
- Enforced: `STATE_RULES`, `POSITIONS`, `DEPENDENCY_TREE`, `DEPENDENCY_RULES`, `INTAKE_STEPS`, `INTAKE_EXAMPLE_TREE`, `JUDGE_STEPS`,
  `TRACE_FIELDS`, `LIFECYCLE_TREE`, `ORDER_RULES`, `VIEW_FIELDS`, `KIND_NOTE`, `VIEWS_OPEN`, `CATEGORY_READS`,
  `EXTRACT_OPEN` of `docs/system-design/new-facts.js`; the views, extract, config and universe nodes and the `draft`
  field of `docs/system-design/new-design.js` and `render.js`; `new-config.js`; rule 8 of `new-universe.js`; the
  glossary of `docs/prd/00-system.md` (结论 added, 共识 removed); `docs/prd/01`, `03`, `05`, `06`; `README.md`.
- Changed by D54: item 4's "who sets an answer at the due date" is settled: the state is frozen at the due date.
- Changed by D58: an existing piece newly linked to a view counts as its evidence changing; a piece that only gains a
  source does not by itself trigger re-judging; "changed or unchanged" compares with the conclusion before this
  round, retries included.

## D52 · 2026-10-21 · Plain, consistent wording across the design page and PRDs

- By: Alex ("you gotta write in a consistent manner that's more understandable across … You have a lot of like
  AI-ish shit jargon that is just very hard for humans to comprehend"; "don't add any additional shit that was not
  intended … need to scrub everything clean"; review with several Codex sub-agents).
- How: four read-only Codex reviews over the universe, classification, Config, dispatch, extraction, the views
  database with match labelling, the review pool, the system overview and the repository README: wording of the views
  database, wording of the rest, logic, and rules not traceable to Alex's words or a decision. The final verdict and
  pull mode are old drafts and were left out. Every finding was checked against the text before a change. The
  traceability review found nothing written as decided that Alex had not decided.
- Renamed, one word per concept: 对上 → 比对 (比对记录, 比对标注; "对上" implied a match even when the result is a new
  view or not opened); 并进 → 归入 (a candidate view joins an existing one), and the pull-mode proposal's 并入 → 合并, so
  the three no longer sound alike (classification's 并到 stays for duplicates); "upstream / downstream" for views →
  被依赖的观点 / 依赖它的 (上游 stays the data supplier only); 血缘 → 前后期关系 or 查来历; 写入者 → 由一个队列来写;
  只追加 → 只加不改; 一条轴上的结果 → 从一头排到另一头的结果; the module title drops "thesis · ladder · evidence";
  table cells are 单元格 and output fields 栏, so 格 means a rung only; 新指标 → 没登记的发布系列. Kept, being explained
  where first used: 格, 层 (the four tiers are ordered), 接续, 连线, 一轮, 顺序号, and 颗粒度 (Alex's word).
- Fixed, no rule changed: the dependency check and acceptance criteria now also allow a year a view waits for; the
  views node's re-judging said only evidence, now evidence and the dependencies' conclusions; the PRD's "重大改动才重判"
  bullet read as the condition for all re-judging, now it is the condition for a dependency and the one rule follows;
  the first classification check refuses a missing readable text only for text items; a correction that names the
  version it replaces (for example only the category changed) is a new version, not a duplicate; step 4 says plainly
  what the one call judges and that a candidate joining a view gets one more call for its evidence; the Reuters example
  relays NVDA's 8-K; decision numbers are taken out of rule sentences (status lines and decision lists keep them).
- Second round: two more read-only Codex reviews of the result found fourteen, all checked and fixed. Two were
  Claude's own slips in this pass: a time rule rewritten as "排先后、算日期只看发布日", which contradicted processing in
  sequence-number order (now "每条信息只用一个日期：它的发布日", ordering untouched); and the not-a-duplicate case fixed in one
  rule but not in the first check and the field table (now in all three, and `supersedes` is used in classification).
  The rest were wording: a few 格 still meaning a table cell, 官方动作 / 官方行动, "叠在观点库上", 答不出 / 等答案 / 合并 listed
  differently in two places, the PRD index title, an example's subject.
  A third, short Codex check of those fixes found one more place, the `copy_of` field, now with the same condition.
- Enforced: `docs/check.py` rules out 对上, 并进, 血缘, 写入者, 只追加, 一条轴上 (22 control pairs); the page data, the
  in-scope PRDs and `README.md`.
- Seals: v9 in `docs/archive/2026-10-21-v9/` with `SHA256SUMS`.
## D53 · 2026-10-21 · A full line-by-line read of the page and PRDs, in rounds

- By: Alex ("再 review 几轮你做的不够仔细需要完整的全部看过").
- How: each round splits the in-scope files among five read-only Codex reviews; each reads its files from the first
  line to the last and reports the line ranges it read, checking wording, consistency, logic, examples and anything
  not decided. Claude reads every PRD in full in the same round. Every finding is checked against the text first; a
  round follows a round until one finds nothing that would make a reader do the wrong thing or fail to understand.
- Round 1: five reviews and Claude's read found about a hundred items. Changed, no rule added: a view's dependents read
  its conclusion (state and reasons), not its state alone; the glossary's 依赖 covers two theme views (same or opposite
  direction) and dependencies are not only from object to theme views; prompt part 1 says company numbers follow the
  fiscal year; the ladder is written by extraction and kept when the view opens; the late February report in the AMZN
  example drops only its outdated forecast; a correction of an item is described without an ambiguous "it"; the
  matching call is said to also choose dependencies wherever the labels describe it; classification's time rule
  says processing follows the sequence number, not the publication time; T2 includes exchanges' quarterly reports; an
  IR deck marked as results is T1, other IR decks T5; T9 sends company-hosted talks to T4 by organizer, as rule 7 says;
  rule 12 is about views and analysis; the measurement split T11/T15 applies to activity measurements only; scans
  with a text layer are classified by the rules; "不算材料的东西" is titled for what it holds; companies, crypto and
  commodities outside the universe are all kept out of the review pool; a re-sent item is skipped only when processing
  finished; Config's settings cell is split into sentences; the system diagram no longer shows the final verdict
  "writing back"; English labels on the page are Chinese; decision numbers left the explanatory text; the
  classification page and node say what the simulation does and does not cover.
- Round 2: five reviews found 24. Two were Claude's own slips in round 1, now fixed: a correction re-judged every
  view linked to the item's evidence, also where only a relayed source changed (now only views linked to changed or
  deleted sentences); and extraction's check named only a sentence, which would refuse evidence from a table cell
  (now a sentence or a table cell). Also: the views node lists every case not opened and that a candidate joins only
  an open view; the structure tree gives a theme-to-theme dependency its same or opposite direction; the state check
  is described as checking the citations against those rules, not their mere existence; a number dependency reads
  that year's view; four classification fields are marked as used in classifying; Config's summary separates the
  search size from the three model settings; labels on the page are Chinese.
- Round 3: three of five reviews found nothing; two items fixed (the current state lists every case not opened;
  extraction stores the cited sentence or table cell).
- Round 4: four of five reviews found nothing; the system overview's review found three, fixed: the glossary's 归入
  says the view must still be open; its 出处 includes a table cell; the README example sets the dependency in the views
  database, not in extraction. A fifth read of those files found nothing. Every in-scope file has now been read in
  full by a review that found nothing.
- Round 6, six cross-cutting reviews (one item followed end to end; the glossary word by word; every number and
  list; a new reader answering sixteen questions; the rules against the decisions; Claude's own D52 and D53 edits):
  the new-reader and own-edits reviews found nothing. Fixed: the NVDA example quoted "charges of up to approximately
  $5.5 billion", which the 8-K does not say (it says "up to approximately $5.5 billion of charges"), so by the
  extraction check that evidence would have been refused; "留下的状态" for what earlier items wrote, where 状态 means
  a rung; an English "upstream views" left in CURRENT_STATE; the identifiers field marked as used in classifying; the
  review pool row in the views PRD names crypto and commodities too. Not changed: D40's request and raw answer are
  required for matching records, not for every model call, so Config's acceptance line stands.
- Round 7, the same six reviews: five found nothing; the glossary review found two, fixed ("状态" for how far a
  matter has got, in the replacement row; "template" for a category's prompt in CURRENT_STATE). Round 8, the glossary
  review again: nothing.
- Round 9, a final full line-by-line read by five reviews: nothing (two reviews were rerun after the model was
  at capacity).
- Not changed in round 2: missing fields go back to upstream and wrong identifiers are not valid, as the rules say,
  so the review pool's "信息缺东西 → 退回" stands; the simulation's 13F sample joins the open defects.
- Not changed: dispatch's completeness check lists what dispatch itself needs; the required fields are checked in
  classification's first step, so the two do not conflict.
- Found in the simulation script, which is not changed at the POC stage (CURRENT_STATE, open defects): it merges a
  copy without looking at the replaces-version field; it does not check fields required only in some cases; one
  sample is a single XBRL fact, which is not pushed in; one branch treats a same-issuer, same-day item as a copy.
- Seals: v10 in `docs/archive/2026-10-21-v10/` with `SHA256SUMS`.
- Seals: v11 in `docs/archive/2026-10-21-v11/` with `SHA256SUMS`, after rounds 6–9.

## D54 · 2026-10-21 · A view's state is frozen at its due date; pull mode runs at the end of the day

- By: Alex. Asked how the final verdict fits the rebuilt views database, Claude set an "answer" apart from the
  state and asked whether to wait for the due date's items before closing. Alex: "为什么会有状态和答案的区别？最后到期日的
  状态就定格就好，为什么会有答案？"; "为什么要等？不合理啊"; "just like run it at the end of the day … the other mode
  will proactively run through theses and update holistically by end of day, or like a certain cron job with a
  certain time interval. All you're dealing with right now is streaming data … you don't need to care about this";
  "pull再做啊，记录起来".
- Decides:
  1. A view has one state (D46 item 1) and no answer apart from it. At the due date the state is frozen where it
     stands: that rung is the view's conclusion, and the view closes. What settles the debate (the annual report,
     the official action) comes in as evidence and moves the state like any other (D46 item 3). A view that depends
     on a closed view reads its frozen state.
  2. Pull mode runs at the end of the day, or on a cron interval: it goes through the views proactively and updates
     them as a whole. Freezing the views due that day is part of that run. Nothing waits for the day's items.
  3. Stream mode handles no timing: due dates, freezing and when pull mode runs are pull mode's (D14). Pull mode,
     with what is left of the final verdict, is designed later.
- Dropped: Claude's pull-mode proposal on how an answer is set at the due date (the first published value; scoring
  the state before the item that brought the answer; waiting for every item published on or before the due date),
  since there is no answer apart from the state and nothing waits; D29's wait for those items; the sentence "到期拿答案
  对一下，就知道判得准不准", which read as scoring against a separate answer (scoring was Claude's proposal, D45).
- Open, for pull mode: how its run works (D14); Claude's two remaining proposals (views that cannot be answered or
  wait for a number to be published; the daily duplicate check); whether the final verdict stays a step of its own
  (Claude proposed folding it into pull mode, since every re-judgement already reads all of a view's evidence; not
  confirmed). Config's one setting for the final verdict (D29, frozen) stands until that is decided.
- Wording: 定格 replaces 答案 (the glossary's row; `docs/check.py` rules out 答案, with a control pair); Claude's
  proposal "等答案" is called 等公布.
- Changes: D14, D29, D46, D51 item 4 (who sets an answer at the due date is settled); the frozen views database (D48)
  through this decision.
- Pages: the final verdict and pull mode PRDs lead with what D54 decided and keep the old draft in a section of its
  own; on the system map pull mode points to the views database (freezing) and to the final verdict (whether it stays a
  step is open). "收盘后" in a first draft was corrected to the end of the day, as Alex said.
- Checked: Codex read the change read-only (every in-scope file in full) and found three, all fixed: two places
  explained "no wait" as if the settling item were always processed before freezing; the final verdict page opened
  with the old flow as the current one; the system overview's module table left D54 out of the views status.
- Enforced: `DEPENDENCY_TREE`, `LIFECYCLE_TREE`, `LIFECYCLE_NOTES`, `VIEW_FIELDS`, `VIEWS_OPEN`, `VIEWS_PROPOSED`, the views
  page's introduction and the verdict page's status line in `docs/system-design/new-facts.js`; the summary, the views,
  verdict and pull nodes and the system view of `docs/system-design/new-design.js`; `docs/prd/00-system.md`,
  `05-extraction.md`, `06-views.md`, `07-final-verdict.md`, `08-pull-mode.md`; `AVOIDED_WORDS` and `WORD_CONTROLS` of
  `docs/check.py`.

## D55 · 2026-10-22 · The final verdict checked against the rebuilt views database; a removed object's views stop updating

- By: Alex. He asked "最终判定模块已经定稿了吗？你来review 一下和我们最新改的模块的consistency", then "你一个一个和我核对，讲人话".
  On a view whose object leaves the list: "这个我自己定就好了，我们manual改名单，如果不update的name 就放个flag 不要继续更新即可".
  On the other two findings: "可以".
- Decides:
  1. The research list is edited by hand. A view whose object is taken off it is kept, flagged no longer tracked, and
     no longer updated. This replaces D31's "not judged at its due date", written when the old final verdict judged
     every view at its due date; since D54 nothing is judged then. Claude's "not frozen at the due date either" is not
     written: no longer updated covers it. The D31 rule was Claude's addition, not Alex's words.
  2. The final verdict card's inputs, outputs and checks start with "旧稿：", as its purpose does: they still name
     premises and conditions.
  3. The final verdict PRD's opening note, and the same list on the page (the card's open item, the detail page's
     status line), name every part of the old draft no longer used, adding the 7-day backstop for a weakened premise
     (already retired in the pull mode PRD) and sending a view on a disagreement within a tier (replaced by D38).
- Checked: Claude read the final verdict, pull mode, views database, system overview and Config against D51 and D54.
  The final verdict is not final: only D54's freezing is decided, and whether it stays a step waits for pull mode
  (D54). Each trigger of the old draft has a place in the rebuilt design (re-judging, D51; freezing, D54; the rule for
  corrected items); nothing is decided from that. Three inconsistencies were found and gone through with Alex one by
  one; all three are fixed. No mechanism is added.
- Changes: D31 (the rule for a view whose object leaves the list); the frozen views database (D48) through this
  decision.
- Enforced: `LIFECYCLE_TREE`, `VIEW_FIELDS` and the verdict page's status line in `docs/system-design/new-facts.js`;
  the views and verdict nodes of `docs/system-design/new-design.js`; `docs/prd/00-system.md`, `06-views.md`,
  `07-final-verdict.md`, `README.md`.
- Changed by D57: "no longer tracked" is gone; a view has one switch, open or closed, and a person closes or
  reopens it by hand.

## D56 · 2026-10-22 · A full sweep before sealing v12

- By: Alex ("你准备freeze 但是完整扫一遍"), then, as Claude went through the findings one by one: "可以", "ok",
  "可以", "ok".
- How: seven read-only Codex reviews, five split by module as in D53's rounds, one on the final verdict and pull
  mode's current parts, one on every change since v11 (`git diff 35bb392`: the UI redo 9886c79, D54, D55); Claude
  read every PRD and the repository README in full. Three reviews found nothing; the diff review confirmed the UI
  redo changed no text. Four findings remained after checking each against the text.
- Decides:
  1. Only open views are re-judged: a view frozen at its due date or flagged no longer tracked is not re-judged when
     what it reads changes. This follows D54 (frozen) and D55 (no longer updated); the rule said "a view is re-judged
     when what it reads changes" without the scope, so a correction or a dependency's change would have re-judged a
     frozen view. Written in the re-judging rule, intake step 7, the views acceptance criteria and the glossary's 重判.
     Changed by D57: the scope reads "only open views"; closed covers both frozen and closed by hand.
  2. The decision lists that still described old-draft content as current now say so: the final verdict PRD's D30
     (conditions, replaced by D38) and D31 (premises, replaced by dependencies), the system overview's D29. D55 item 3
     had fixed only the final verdict PRD's opening note; these lines are the same class.
  3. Classification's time rule 2 says the stream has no "today"; pull mode, the only place that acts on time, gets
     its "now" as an input. "系统里没有‘今天是哪天’" read as if pull mode could not act on dates (D14, D54).
  4. The repository README follows D54 and D55: the decision range, the log's step count, pull mode's run and
     freezing, the final verdict and pull mode statuses, and v12 as the current sealed design. D54 had left it out.
- No mechanism is added.
- Changes: D12's enforcement in classification (frozen, D19, D37) and the frozen views database (D48), through this
  decision.
- Enforced: `DEPENDENCY_RULES` and `INTAKE_STEPS` of `docs/system-design/new-facts.js`; `TIME_RULES` of
  `docs/system-design/new-classification.js`; the views node of `docs/system-design/new-design.js`;
  `docs/prd/00-system.md`, `02-classification.md`, `06-views.md`, `07-final-verdict.md`, `docs/prd/README.md`; the
  repository `README.md`.

## D57 · 2026-10-22 · A view has one switch: open or closed

- By: Alex, when Claude asked where to write "only open views are re-judged": "So, a thesis basically can have like
  an active and inactive flag. That's it. … It's very simple system design. The active flag can be turned on and off
  by me if … the asset gets delisted."
- Decides:
  1. A view has one switch, open (active) or closed (inactive), and nothing else; D55's "no longer tracked" label is
     gone. The design's existing words 开着 and 关了 name the two positions; no new word.
  2. Only open views are updated: a closed view is not re-judged, keeps the state it had when it closed, and stays in
     the database, searchable. A view that depends on it reads that state and its reasons.
  3. At the due date pull mode freezes the state and closes the view (D54). A person can close or reopen a view by
     hand, for example when the asset is delisted; the research list is edited by hand too (D55).
- Not changed: when a superseded piece of evidence is still linked to a closed view, the new piece is linked there
  too; a link is a record, not an update of the view's state, and adding a refusal would be a new mechanism.
- Checked: the second round of Codex reviews (five, on the files D56 touched) found the "only open views" scope
  missing in five more places: the views node, the system overview's two-modes table, the README, and the rules for
  superseded evidence and for corrections. All five now say open views; Claude's question on where to write the scope
  is answered by the one switch. Two of the five reviews found nothing.
- Wording: 开着、关了 gets a glossary row; `docs/check.py` rules out 不再跟踪, with a control pair.
- Changes: D55 item 1, D56 item 1; the frozen views database (D48) through this decision.
- Enforced: `LIFECYCLE_TREE`, `LIFECYCLE_NOTES`, `VIEW_FIELDS`, `DEPENDENCY_TREE`, `DEPENDENCY_RULES`, `INTAKE_STEPS`,
  `EVIDENCE_NOTES`, `ORDER_RULES` of `docs/system-design/new-facts.js`; the views node of
  `docs/system-design/new-design.js`; `docs/prd/00-system.md`, `06-views.md`, `docs/prd/README.md`; the repository
  `README.md`; `AVOIDED_WORDS` and `WORD_CONTROLS` of `docs/check.py`.
- Changed by D58: each manual close or reopen is a record (who, after which item number); the rule that every
  change carries a source covers the changes items cause.
- Seals: v12 in `docs/archive/2026-10-22-v12/` with `SHA256SUMS`: the design after D54–D57 and the full sweep of D56.

## D58 · 2026-10-22 · A deep review before freezing everything but pull mode

- By: Alex ("你为什么不跑一个非常长且细致的 overall read and reasoning of this system deisgn so far - consistency in
  wording - consistency in logic - specifity in writing and description - system design flow and state 你自己要超级深度的研究以及多轮的反攻来自洽。
  不要自己加戏，我们当前的设计需要完整的freeze (除了 pull mode) 你现在就深入的review，直到你自己满意可以定稿，不要偷懒或是不真的读代码，做仿真").
- How: Claude read every PRD, the page data, the renderer's visible text and D38–D57, traced items through the stream
  and wrote down eight candidate problems of its own. Eight rounds of read-only Codex reviews followed, by angle: an
  end-to-end simulation of eighteen items (dispatch, extraction, the seven intake steps, the due date and manual
  switches); state-by-event tables for a view, a piece of evidence, a candidate and an item; wording against the
  glossary; whether an engineer could build each step from the text; every decided rule against Alex's words and the
  decisions; an attack on Claude's own candidates; the input side with `simulate_classification.py` run; a new reader
  answering seventeen questions; every change since v11 read in context; and line-by-line reads split by module.
  Each finding was checked against the text before a change. The rounds found about 20, 7, 5, 7, 3, 2, 1 and 1;
  in the last two rounds eight of nine reviews found nothing, and the last finding was a cross-reference.
- Decides (written out, no mechanism added; each follows a decision in force):
  1. A dependent object view writes which end of the other view is bullish for it; a dependent theme view writes
     whether the two ladders run the same way or opposite (it was written only for two theme views).
  2. A waiting arrow records which chain (that of a view shown to the model) and which year; it connects when that
     year's view is succeeded on that chain.
  3. A view covers what happens up to its due date. Prompt part 5 gives each listed view's question, what it looks
     at and its due date (no state or evidence); what happens after the due date goes in as a candidate view, so a
     closed view a dependent still points to is succeeded rather than given evidence it will not use.
  4. Matching shows each existing view's question, what it looks at, ladder, due date and whether it is open. A
     candidate that is the same thing and period as a closed view is not opened ("a closed view can only be
     succeeded"). A successor's ladder runs the way its predecessor's did, with the candidate's thresholds.
  5. Evidence linked to a candidate view, even if also linked to existing views, is compared once, after the
     candidate's place is known, under every existing view it links to; evidence only on a new view is new.
  6. Re-judging: only open views; an existing piece newly linked to a view counts as its evidence changing; a piece
     that only gains a source does not by itself trigger re-judging; "changed or unchanged" compares with the
     conclusion before this round, retries included. Writing puts themes before objects; judging follows the
     dependencies. Universe rule 8 says dependents still open are re-judged.
  7. "This year and next" limits which years a candidate may open, one view per year; last year's view stays open
     until its due date (counting all open views would close it before its due date, against D54).
  8. A conclusion is a state with its reasons: at the due date the rung and its reasons are the view's last
     conclusion, and dependents read the state and reasons a closed view had when it closed.
  9. Each manual close or reopen is a record (who, after which item number); the rule that every change carries a
     source covers the changes items cause. "One open view per thing" is the rule matching keeps when it opens views
     (D44); a view a person reopens is outside it.
  10. Wording: 官方行动, not 官方动作; decision numbers out of body text; the headings 一条观点开着还是关了 and 已经定的;
      the page's open items are called 还没定的, as in the PRDs; the map edge between extraction and the views
      database says what goes each way; pull mode "only decided when it runs"; 并进 out of the final verdict and pull
      mode.
- Rejected after review: Claude's own idea to list only open views in prompt part 5 (it changes D42's input; the due
  date answers the case instead); adding a dependency to the AMD example (the model chooses, and #3 is judged as new
  anyway); a pull-mode open item on number views whose publication day is not known yet (pull mode is not designed).
  Kept as is: a manually closed view whose source is later corrected loses the old sentence and does not take the
  new one (closed views are not updated).
- Recorded, not changed (the script is not changed at this stage): three gaps in `simulate_classification.py`, in
  `docs/CURRENT_STATE.md` under open defects.
- Open, for Alex (in extraction's 还没定的): how a candidate view names its object when the item's tags do not carry
  it (a theme not tagged, another company named in the text), since step 5 checks the object is in the universe;
  and what a candidate view read from his own memo does without other evidence, since classification counts the memo
  as a view to track, not evidence, and a candidate view carries at least one piece of evidence.
- Freeze: every module except pull mode and the final verdict, which is designed with it, is frozen in this text; a
  change needs a new decision.
- Changes: D42, D44, D46, D51, D57 (notes under each); the frozen universe, extraction and views database through this
  decision.
- Enforced: the page data (`new-facts.js`, `new-design.js`, `new-universe.js`), `render.js`; `docs/prd/00`, `01`, `05`,
  `06`, `07`, `08`, `README.md`; `docs/CURRENT_STATE.md`, `README.md`.
- Seals: v13 in `docs/archive/2026-10-22-v13/` with `SHA256SUMS`.
- Changed by D59: Alex answered both open questions; the freeze holds, with D59's text.

## D59 · 2026-10-22 · How a candidate view names its object; a view from Alex's own memo

- By: Alex, to the two questions D58 left open, each with two options and Claude's lean: "1 选 A，2 选 A，然后再做一次".
- Decides:
  1. A candidate view names its object as follows. Prompt part 3 carries the item's related objects and, appended,
     every theme in the research universe (a few dozen); a candidate about a theme picks it from that list. A company,
     crypto asset or commodity is written by ticker, crypto symbol, commodity code or name, and code looks it up the
     way classification looks up object identifiers. What is found but outside the universe, what is not found, and a
     theme not in the universe keep their existing outcomes (noted only; the review pool; a suggested theme). Step 5
     checks the object this way.
  2. Alex's own memo (T8 with him as the author): its judgements are read as candidate views, not as evidence (as
     classification says). Such a candidate may carry no evidence; once opened, its state is "还没判" until evidence
     first links to it, when it is judged for the first time; a view that depends on it reads "还没判" until then. The
     code check that a judgement says "changed" now covers a view's first judgement, whenever that comes.
- Changes: D42 and D46 item 16 (a candidate carries evidence, except one read from Alex's own memo); the frozen
  universe (its themes also go to extraction), extraction and views database, through this decision.
- Enforced: `TEMPLATE`, `PROMPT_EXAMPLE`, `PROMPT_NOTES`, `EXTRACT_TWO`, `EXTRACT_OPEN`, `STATE_RULES`,
  `DEPENDENCY_RULES`, `INTAKE_STEPS`, `VIEW_FIELDS` of `docs/system-design/new-facts.js`; the extract, views and
  universe nodes and an edge from the universe to extraction in `docs/system-design/new-design.js`;
  `docs/prd/00-system.md` (the glossary's 状态, the side lines), `01-universe.md`, `05-extraction.md`, `06-views.md`.
- Changed by D60: written out wherever it applies (the second deep review); the code-or-name lookup follows registered
  names in the reference data.

## D60 · 2026-10-22 · The deep review again, after D59

- By: Alex ("1 选 A，2 选 A，然后再做一次").
- How: as D58, from the top, with D59's cases added: the flow simulation took 21 items (a theme the tags do not
  carry, another company named in the text, a memo of Alex's with no facts, then evidence for it, a view depending
  on a view still "还没判"); the state tables took the state "还没判"; the new reader answered two more questions;
  one review attacked only what D59 had written. Five rounds: 13, 8, 7, 6 and 7 read-only Codex reviews, each
  finding checked against the text first. They found about 8, 5, 3, 1 and 0; the last round's seven reviews found
  nothing.
- Decides (no mechanism added; D59 written out where it applies, and wording):
  1. Alex's memo: its judgements all go in as candidate views, may carry no evidence and are not evidence. This is
     now in prompt part 1, extraction step 2, the hand-over table, the "读到一句话或一个数" tree (memo judgements do
     not go through it), the extraction page, the nodes, the glossary and the summaries; "only what the views do not
     cover" governs other items.
  2. A candidate's object: a theme from the universe's themes in part 3, or written out when the universe has none;
     a company, crypto asset or commodity by code or name, as Alex chose, looked up in the reference data, a name
     only as registered (as classification does for company names). A first-round narrowing to company names only
     was Claude's slip, reverted.
  3. "还没判" is in the state's definitions; a closed view keeps the state it had; the lifecycle and the re-judging
     summaries say a memo view without evidence is not judged. Universe rule 8 now says dependents are re-judged by
     the views database's rule rather than restating its conditions, so they live in one place.
  4. Matching shows each existing view's object too; code checks whether a cited piece is marked replaced (which
     also covers deleted sentences); writing puts theme views before object views, and an object view is written by
     its company's, crypto asset's or commodity's queue; a manual switch counts "after the item with which sequence
     number"; only the sentence or cell a view's or a piece's source cites is stored.
  5. On the map the universe → extraction edge (themes) and the views → review pool edge run between the rows,
     not through other modules.
- Recorded, not changed: the classification simulation reads related objects from an old field name, so its pass
  does not test the current field (`docs/CURRENT_STATE.md`, open defects).
- The freeze of D58 holds, now with D59 and this text.
- Enforced: the page data (`new-facts.js`, `new-design.js`, `new-universe.js`); `docs/prd/00`, `01`, `05`, `06`,
  `README.md`; `docs/CURRENT_STATE.md`, `README.md`.
- Seals: v14 in `docs/archive/2026-10-22-v14/` with `SHA256SUMS`.

## D61 · 2026-10-22 · Clean-up: a code review, bloat removed, superseded seals out of the tree

- By: Alex ("你跑一个code reveiw 移除不必要的垃圾和bloat, 更新好所有文档，readme, agents.md 然后push").
- How: three read-only Codex reviews (code, text bloat, the repository); each finding checked against the files; a
  read-only review of the result for meaning lost or changed.
- Decides (no rule changed):
  1. Sealed copies v7–v14 leave the tree; v1 (the earlier design) and v15 (the frozen design) stay. Each removed copy
     is in Git: v2–v7 in `94622a5`, v8 `7830a18`, v9 `267c89d`, v10 `8d617c7`, v11 `35bb392`, v12–v14 `3da83a9`. D50
     called its removal of v2–v6 a one-time exception; this is a second, at Alex's request.
  2. Text: status lines keep the frozen date and what is open, the change history being in each PRD's decision list
     and here; the front summary is shortened; summaries point to the one re-judging rule and to the memo note
     instead of restating them, and the glossary's 重判 points to the rule; a sentence the map caption said twice is
     said once; `docs/CURRENT_STATE.md` keeps the status, the open defects and the next task and points to the PRDs
     for the design.
  3. Code: styles and two colour tokens no page uses (`design-system.css`); edge label coordinates `render.js`
     computed and never read; the font script's note on a `fonts.css` that does not exist.
  4. `AGENTS.md`: the sentence on scripts made true; three lessons written at their decisions: bring Alex only the
     choices that change what the system does; a rule's text has one owner and other places point to it; before a
     freeze, review in rounds by angle until a round finds nothing.
- Not changed: `copy_old_design.py` copies 113 configuration fields the Old tab never reads; trimming them needs a rerun
  against the old repository's snapshot to save 5 KB, so they stay.
- Seals: v15 in `docs/archive/2026-10-22-v15/` with `SHA256SUMS`, the design as frozen after D58–D61.

## D62 · 2026-10-23 · The POC build: Alex's choices, in his words

- Build started on the frozen design (2026-10-23): "数据准备好了之后，你清洗干净就可以准备开始去建这个 POC 的管线", "尽量按照那个系统设计来……当然没有这么复杂……做简洁一点". The simplifications are listed in `docs/poc/pipeline-plan.md`; nothing in the frozen PRDs changed.
- No cap on the number of views: "不一定要二到四个问题啊". The model decides; code checks only the shape (ladder, due day, quarter, year).
- The corpus first, whole and original: "先建好这个素材库……再尝试来建构这个管线"; "要像是原始数据……不能是你自己已经处理过的". Industry, macro, geopolitics and noise added: "起码多两倍的数据".
- Test small before any full run: "你最好小范围的测试下不要全部跑完然后完全不 work 或是质量有问题再全部重跑". The first week, then August: "你别全跑，到 8 月底先。我们来完整的看下结果".
- Extraction variance is fixed in the prompt, not by sampling several times: "太浪费钱和时间了，那你的 prompt 就应该改成可以抽的出来的方式". The v2 extraction prompt replaces taste words and the company-specific line with rules checkable against the material (the firm's total and largest-segment full-year numbers, every full-year number the firm guides, dated pending events); measured on the same transcript three times, the core set is stable (`docs/poc/pipeline-plan.md`).
- Model: gpt-6-luna stays: "那我觉得还是用 luna 吧，记录这个比较结果". The comparison with DeepSeek-V4.1-Flash-1017 (the `deepseek-flash` endpoint) is in `docs/poc/pipeline-plan.md`: the only way to get schema-valid JSON from it was a strict tool call with thinking off (3/3; json_object 2/3 and 1/3; thinking-mode forbids a forced tool_choice); about five times cheaper (≈$0.01 against ≈$0.05 per transcript), 18–22 s against 26–31 s, three times more evidence, the candidate set a little less stable; matching and re-judging were not tested on it.

## D63 · 2026-10-24 · Re-judging once a day; the first window ends on 2026-08-15

- Alex, shown that re-judging was half the cost (a hot view re-judged after every item, each call carrying all its evidence): "是的应该要一天一次". Re-judging moves from each item's round to one round per day: the day's items are extracted, matched and written in sequence as before; after the last item, and before pull mode freezes the views due that day, one judging round runs over every open view whose reading changed that day, dependencies first, each view once, dependants added when a dependency's conclusion changed. The judgement is recorded under the day's own processing record (`day:<date>`) at the day's last sequence number. This amends 06-views step 7 / D51 for the POC; the design text is updated when Alex takes the module up. The stream still never reads the calendar: the day comes from the replay (in production, from pull mode).
- Reasoning effort stays medium: "可以之后试试看比较质量，这次先别改".
- The window: "嗯改成 8/15 吧；然后已有的结果封存，然后改一下重判的设置，然后继续跑完剩下的". The results through the last completed day are sealed in `poc/data/sealed-2026-10-24-run3-through-0728/` with `SHA256SUMS`; the same views database continues from the next day to 2026-08-15 with daily re-judging.

## D64 · 2026-10-24 · Hide the mock header's date label

- Alex: "remove this", pointing to the "As of 2026-08-15" label. Remove that label from the mock header; replay dates and the stored data window stay as they are.

## D65 · 2026-10-24 · Remove black focus outlines from the mock

- Alex: "remove this pattern from the UI", pointing to the black outline around the claim slider while dragging. Disable focus outlines throughout the mock, including both sliders and buttons, in its own stylesheet.

## D66 · 2026-10-24 · Remove the canvas hint and shorten the search field

- Alex asked to remove the bottom canvas hint and make the search bar shorter. Remove the hint and cap the input at 480px, allowing it to shrink when space is limited.

## D67 · 2026-10-24 · Simplify the view card headers

- Alex asked to remove the unnecessary counters and questioned the "Thesis view" / "Factor" badges. Remove the rounds, evidence and facts counters and both role badges from canvas card headers. The underlying relationships and detail-panel history remain available.

## D68 · 2026-10-24 · Put the current judgment in the card header

- Alex asked to move the score and label, such as "+1 Bullish", into an upper-right pill on the card. Move the existing state display into the header; replay continues to update it.
- Alex then asked for centered, consistent pills. Use equal padding and a common height; hide an empty label so a Yes/No state has no spare gap beside its text.

## D69 · 2026-10-24 · Use matching score circles on charts and state pills

- Alex specified black-filled number circles for +2/+1, grey for neutral, and white-filled circles for bearish scores. The chart axes and current-state pills share the same icon and palette, including in the detail panel. Chart rows have enough room for separate circles. Yes/No remains text.
- Superseded by D70 after Alex rejected how the circles looked.

## D70 · 2026-10-24 · Simplify the score display after visual review

- Alex rejected the stacked circles and tiny circle inside the header pill, asking for a better design. The axis now uses quiet score labels and highlights only the current state. The header uses a single badge with a readable score and a separated label. The current axis marker and badge share black for positive, grey for neutral, and outlined white for negative; Yes/No uses the neutral treatment. This replaces D69's circles on both the canvas and detail chart.

## D71 · 2026-10-24 · Use black for Yes and white for No

- Alex specified that binary states use black for Yes and white for No. The shared state palette applies this to both the header badge and highlighted axis label, including the detail panel, replacing D70's neutral treatment of binary states.

## D72 · 2026-10-24 · Remove redundant card footer tags

- Alex called the object and view-kind tags redundant. Remove these two tags from canvas view cards; retain the due date. Object and kind remain available in the detail panel.

## D73 · 2026-10-24 · Use one title style across canvas cards

- Alex asked for consistent card-title font sizes. Thesis and view titles share one CSS rule: 16px, weight 500, 22px line height; card-specific size overrides are removed.

## D74 · 2026-10-24 · Remove the change-summary line from view cards

- Alex called the "1 change | since…" line redundant. Remove it, including the "no change since…" form, from canvas view cards. The chart and detail panel retain the change history.

## D75 · 2026-10-24 · Give daily evidence volume its own chart band

- Alex asked for a clearer X axis and more height for the evidence bars. Canvas cards now separate the state history from a 52px evidence band labelled "Evidence / day". Each bar counts the stored evidence records arriving that day, with a labelled zero and upper count scale; it does not count distinct real-world events. A single set of aligned month-and-day labels serves both plots. The replay reveals both plots together. Cards are 392px tall to fit the band, and binary views use the same plot height as five-state views.

## D76 · 2026-10-24 · Hivemind is a database with a search engine on top; the caller chooses

- Alex: "我们不要这样 POC，我觉得把我们的 poc 现在打包成一个 MCP 或是 API" … "现在我们的观点库上面需要 overlay 一个 search engine interface 能解析语意，返回例如 top-10 对应观点之类的，然后让 llm 分析看选那几个" … "agent 调用这个工具，返回的是观点，他自己选择要那些观点不就完事了吗" … "hivemind 就是一个数据库上面有个搜索引擎，你理解 scope 了吗？写好，然后让 codex subagent review".
- Decided: the views ledger gets a read-only service: `search` (semantic top-k over each view's own text; evidence is anchored under the view and is not indexed), readers (`views`, `view`, `history`, `evidence`, `record`, `changes`) and `evaluate` (a threshold against the judged band), all as of a calendar day (D12, D13). Hivemind does not pick or arrange views for the caller (no issue-tree tool), does not know users and stores no theses; the agent that calls it does that. Two thin fronts: MCP (stdio) and HTTP (127.0.0.1). The search index is a derived file beside the ledger, never a write to it. Design: `docs/poc/service.md`.
- An idea no view covers: settled in D91 (null).

## D77 · 2026-10-24 · Label the state chart

- Alex asked for an "AI score" title above the top chart, matching "Evidence / day". Both titles use one shared style and align to the same left edge.

## D78 · 2026-10-24 · Name the user input Idea and stored questions Thesis

- Alex: "these should be called Thesis not view, the initial card is called Idea" and "now scrub the FE and logic". Apply Idea to the input card and Thesis to matched questions throughout frontend labels, placeholders, empty states, tooltips, detail headings, judgment display text, CSS and helper names. A single frontend adapter maps the existing ledger's `views`, `view_id` and kind values into the UI terminology; the service's wire format stays compatible. This clarifies D76's wording: Hivemind stores the questions now displayed as theses, not user ideas.

## D79 · 2026-10-24 · Align plot headings to the number column

- Alex asked to left-align "AI score" and "Evidence / day" with the chart numbers. Both titles start at the left edge of the number-label column, and the evidence scale uses that same edge.

## D80 · 2026-10-24 · Give the due date a separate card footer

- Alex asked for the due date below a divider matching the header. Thesis cards have a dedicated 40px footer with a full-width top border; the date is outside the chart body. Cards are 408px tall to retain the plot space.

## D81 · 2026-10-24 · Simplify the thesis detail panel

- Alex asked for a clean, minimal detail panel following the canvas design. The old panel put metadata, counters, score definitions, the full history, repeated reasons and all evidence into one scroll. The mock contains 42 theses, 375 assessments and 1,089 evidence links; the new layout applies to all of them.
- The header shows the thesis question, current score and assessment date. The due date belongs to the footer. Overview shows the current band, a four-line assessment preview and at most three recent cited records. Full explanations and source quotes expand on request. Metadata and related theses are collapsed.
- Evidence has text search, a type filter and 20 records at a time. History has a calendar chart shared with the canvas, a selector for every assessment, previous/next controls and expandable reasons, citations and score definitions. The old independent chart and duplicate rendering paths are removed.

| Event | Result |
|---|---|
| Open a thesis | Pause replay, capture its date, show Overview using only assessments and evidence available by that date. |
| Switch tab | Show the selected panel; initialize Evidence or History once for this opening. |
| Search or change evidence type | Reset the visible limit to 20 and filter the same dated evidence snapshot. |
| Show more evidence | Reveal the next 20 matching records. |
| Select an assessment | Update its date, score, explanation and citations without changing the current-score header. |
| Open before the first assessment | Show that no assessment is available; History and Evidence handle an empty snapshot. |
| Close or open a related thesis | Close the panel, or open a fresh snapshot for the related thesis at the same replay date. |

## D82 · 2026-10-24 · Use the same font for dates and labels

- Alex: "所有的日期和pill 内日期字体不要用特殊的font, just use the same throughout". The mock uses its regular sans-serif font for dates, numeric labels, pills, charts and detail text; monospace overrides are removed.

## D83 · 2026-10-24 · Center the fan-out and animate connected edges on hover

- Alex asked for the tree to grow symmetrically above and below the middle, with connections at the midpoints of card edges. The Idea and primary Thesis share the vertical center of the supporting-card group. Child cards keep their 24px gap; horizontal spacing leaves room for curves.
- Every connector records its source and target. Hovering any card highlights all directly connected incoming and outgoing edges with moving black dashes; unrelated edges stay quiet. The Idea participates in the same hover behavior.
- Layout verification covers zero through four child cards; stored-data browser checks cover two- and three-child fan-outs, midpoint endpoints, no-match layout, and root/parent/child hover behavior.

## D84 · 2026-10-24 · Use right-angle connectors

- Alex asked for more right-angled connectors. Replace the sweeping curves with horizontal–vertical–horizontal paths and small rounded elbows. He then clarified that branches should leave the parent at separate positions, as in the reference: space the outgoing ports 24px apart around the parent’s middle, rather than sharing one point. Child inputs remain at their midpoints; centered fan-out and hover animation stay the same. This amends D83’s shared midpoint for outgoing branches.

## D85 · 2026-10-24 · Thin connectors with directional arrowheads

- Alex asked for thinner lines and arrowheads at their endpoints. Connectors use a 1px stroke in both normal and hover states, with a 10px arrowhead pointing into the destination card (enlarged at Alex’s follow-up request); the arrow follows the line color and the hover dashes keep moving.

## D86 · 2026-10-24 · Replace Idea and Thesis header icons

- Alex asked to redo both icons. Idea uses an outline light bulb; Thesis uses an outline document. Both use the same 16px size, rounded joins and 1.5px stroke.

## D87 · 2026-10-24 · Hover highlights only the path into a card

- Alex clarified that hovering a card must highlight only its preceding connection hierarchy, never outgoing branches. Follow incoming edges recursively back to the Idea. Hovering the Idea highlights no edges; hovering the primary Thesis highlights only Idea → Thesis; hovering a supporting Thesis highlights that full upstream path. Clear the highlight on pointer exit. This replaces D83’s incoming-and-outgoing rule.

## D88 · 2026-10-24 · Refine detail controls, dates and source presentation

- Alex asked for the Thesis icon in the panel header, an X close control, and "Last updated:" followed by a full date. The header uses the existing Thesis icon and an accessible icon-only close button.
- Replace the moving "Full assessment" disclosure with one paragraph and a button underneath it. The button stays after the text and switches between "Read more" with a down chevron and "Read less" with an up chevron. The Overview and History use the same renderer.
- Evidence dates show month, day and year. Expanded records put the quoted text in an italic, light-grey block. One "Source document" group contains the publisher and linked title; a separate "Original source" row names the cited original where it differs. Remove the repeated source title, loose attribution and separate "Open source" link.

## D89 · 2026-10-24 · Give the detail panel a clear visual hierarchy

- Alex asked for an overall hierarchy rather than similarly styled headings, prose and controls. The detail title is 20px semibold, section headings 16px semibold, body and evidence text 14px with 24px line height, and metadata 12px. Shared local font tokens keep body, action and metadata roles consistent across Overview, Evidence and History.
- The current assessment has a light background; sections have consistent spacing and dividing rules. Read more/Read less, navigation and links use one restrained blue accent, making actions distinct from text. This adds an interaction color to the mock; black/grey/white score meanings stay unchanged.

## D91 · 2026-10-24 · An idea the library holds no view on gets null

- Alex, asked what Hivemind returns for an idea no view covers: "没有观点就返回null 啊，然后就代表我们没有记录观点".
- Decided: `search` answers `results: null` when the library holds no view on anything the idea names as of that day: none of the companies or themes the universe lists is named in it, and the ledger's own text index matches no view. Null means "Hivemind has no recorded view on this". Otherwise the ranked list comes back whole and the caller judges which views, if any, correspond (D76). The envelope (`as_of`, `mode`) stays, so the caller knows which day and which mode said so.
- Measured before building, on 25 sentences (the four examples, the 16 day-0 sentences, five unrelated ones): a similarity cutoff cannot draw the line, because "NVDA 的 logo 比 AMD 好看" scores 0.49 while real theses on CUDA or China re-opening score 0.35–0.40. The name-or-text rule nulls six of the nine no-view sentences (Tesla, Apple, Bitcoin, a house, the Fed, "黄仁勋是个天才") and none of the sixteen with a view; the three nonsense ideas that name NVDA (a logo, a dream, a split) get NVDA's views back for the caller to reject.

## D92 · 2026-10-24 · Keep the existing monochrome theme

- Alex rejected the added blue and required the existing theme colors only. D89’s typography, spacing and section grouping stay; actions use the existing charcoal tokens with underlines, and neutral backgrounds use theme tokens. This supersedes D89’s blue accent.

## D93 · 2026-10-24 · Simplify detail sections and move the due date

- Alex asked to remove "Browse evidence", remove extra dividers at the bottoms of sections, and move the due date to the right of "Last updated". Remove the duplicate evidence shortcut and its handler. Keep separators only between evidence rows, not after the last row; section and related-thesis boundaries use spacing. The detail footer is removed, and the due date appears beside the update date in the header. Canvas card footers are unchanged.

## D94 · 2026-10-24 · Merge the current assessment and its reasoning

- Alex asked for one unboxed "Current assessment" section: the current assessment is the first, bold sentence, followed by the reasoning and its Read more/Read less control. Remove the separate "Why this assessment" heading. The first cited evidence and first related-thesis item use the same 12px heading-to-content gap as prose sections, without extra row padding.

## D95 · 2026-10-24 · Keep one divider at each section boundary

- Alex clarified D93: keep dividers between sections and between list items; remove only the extra bottom border on the final item that doubled the next section’s divider. Section boundaries use a top border, and list rows use a top border only after the first row. The last row has no bottom border, in both collapsed and expanded states.

## D96 · 2026-10-24 · Present the current assessment as a quote

- Alex asked for the leading assessment sentence to look like a Markdown `>` quote. Use a bold blockquote with a slim grey left border and no surrounding box, followed by the reasoning in the same section.

## D97 · 2026-10-24 · Make the lower detail sections consistent accordions

- Alex asked for Recent evidence cited, Related theses and About this thesis to share the same heading size and expand/collapse behavior. All use the same 16px semibold disclosure heading, spacing and single section divider, and start closed. Remove nested "Depends on" / "Used by" headings; related theses form one deduplicated navigable list.

## D98 · 2026-10-24 · Highlight the assessment row with a quote accent

- Alex asked for a light-grey highlight across the assessment row, then clarified that the left line should fill its height from top to bottom. Use the existing wash color, bold text and a full-height vertical accent; no surrounding card border.

## D99 · 2026-10-24 · Put the related-thesis arrow before the title

- Alex asked for the navigation arrow on the left as an icon, not appended to the question. Each related-thesis row starts with a small outline arrow, aligned with its first text line.

## D100 · 2026-10-24 · Animate all detail expansions consistently

- Alex asked for smooth show/hide transitions for Read more/Read less and every dropdown. Use one 240ms eased height transition for assessment text and all detail/evidence disclosures, with matching chevron motion. Controls stay after their content; the final height returns to automatic sizing.
- A repeated click cancels the running transition and continues from its visible height toward the new target. Closing a parent settles any running child transition first. The operating system's reduced-motion preference skips the animation.

## D101 · 2026-10-24 · Separate the header dates with vertical bars

- Alex requested "| Last updated: xxx | Due: xxxx". Put each separator with its date label so it stays together if the metadata row wraps.

## D102 · 2026-10-24 · Shorten the evidence heading and use solid disclosure triangles

- Alex asked for "Recent evidence" and solid triangle indicators on section dropdowns. All detail-section headings share a filled triangle pointing right when closed and down when open, preserving the existing smooth rotation and monochrome theme.

## D103 · 2026-10-24 · Align detail labels and values at one readable size

- Alex rejected the smaller labels and loose stacked layout in About this thesis. Definition lists use compact, aligned label/value rows: both 14px with 24px line height, labels semibold, values regular, and a 12px row gap. The shared layout also keeps Score definitions consistent.

## D105 · 2026-10-24 · Animate disclosure content without moving its heading

- Alex reported that Related theses and About this thesis still opened abruptly. The shared handler covered seven disclosure templates, but opened the native details contents before animating the whole details element. Its open-only heading margin and expanded evidence-summary height changed at the same time.
- Each disclosure now wraps its contents in a clipped region and animates that region from zero to its natural height, keeping the heading and its spacing fixed. Evidence summaries animate their own height when the text expands. Closing keeps contents mounted until the transition ends; repeated clicks and parent/child transitions retain D100's behavior. Disable scroll anchoring inside the detail viewport so the browser does not reposition it during an expansion.
- Browser verification on About this thesis kept the heading at y=692 through opening and closing; content height was observed at 6.75px while opening toward 108px and 102.14px while closing toward zero. Related theses, keyboard activation, and closing a parent during a nested evidence transition were also exercised.

## D104 · 2026-10-24 · A theme holds a document only if it can move a thesis; Commerce anti-dumping notices do not

- Asked why Commerce anti-dumping and countervailing notices on Chinese goods are not filed under 中美关税, Alex gave the test instead of a ruling: "你自己评价下是不是会有影响的 thesis".
- Applied on stored data: 89 Commerce notices naming China in the corpus (29 in the run window); none mentions semiconductor, server, data center, GPU, chip, NVIDIA or printed circuit (the one "heat sink" is the aluminum-extrusions scope clause); in the sealed ledger their evidence sits only under five procedural views ("will Commerce publish X by date Y": v44, v64, v65, v66, v85; 0 dependants) and under no view of the 15 companies or other themes.
- Decided: the rule stays (`official_objects`: the Commerce feed carries no object). The test is general: a document belongs to a theme when it can move a thesis of the universe, not when a case number or keyword matches.

## D106 · 2026-10-24 · Reserve scrollbar space without a track divider

- Alex asked for dropdowns to leave the assessment width and text wrapping unchanged. The shared detail viewport always reserves the same scrollbar gutter across Overview, Evidence and History. Its track is transparent and borderless; only a slim neutral thumb appears when scrolling is possible.
- Browser verification: opening Recent evidence and its first quote increased scroll height from 602px to 795px while the viewport stayed 709px wide and the assessment text stayed 653px wide. The computed track background is transparent and its border is 0px.

## D107 · 2026-10-24 · Put expanded evidence dates after its sources

- Alex asked to place the date below Original source when an evidence row is expanded and enclose the quoted passage in “ ”. The shared evidence renderer keeps date/type metadata beneath the summary when collapsed, shows it after the source details when expanded, and adds the quotation marks while retaining the existing quote styling.

## D108 · 2026-10-24 · Combine source, type and date on one attribution line

- Alex asked for "Goldman Sachs | Third-party view | date" on the Original source row instead of a separate date line. Expanded evidence appends type and full date to its original-source attribution; where no separate original source exists, it appends them to the source publisher. Collapsed rows keep their existing metadata line.

## D109 · 2026-10-24 · Show the source in collapsed evidence rows too

- Alex asked for the collapsed metadata to include Goldman Sachs or the relevant source. Both states now use source, type and full date in the same order. Prefer the recorded original source; otherwise use the source publisher. The shared evidence renderer applies this across Overview, Evidence and History.

## D110 · 2026-10-24 · Show thesis status in a pill

- Alex asked for Open, Closed and other thesis statuses to use a pill. About this thesis now renders the existing status value in the shared neutral outlined chip; status calculation is unchanged.

## D111 · 2026-10-24 · Use an in-page evidence type menu

- Alex rejected the native operating-system menu for All types. Replace that menu with a white, bordered list directly below the control, using existing theme colors and typography. The selected row has a checkmark, and opening uses a short transition.
- States: closed → trigger click or arrow key opens; open → option selection writes the existing `detail.tier`, resets pagination and redraws evidence, then closes; outside click, focus leaving, Tab or Escape closes without changing the filter. Escape closes this menu before the drawer. Arrow keys and Home/End move through the options; Enter/Space selects. Accepted values stay exactly All types (empty) plus the tiers already present in this thesis. Only `drawEvidence` reads the chosen tier; data and filter rules do not change.

## D112 · 2026-10-24 · The service runs in Docker; the FE asks it to read an idea; the user's thesis is the idea card

- Alex: "我们来这样做，你用 docker 起一个 mcp /api service, 然后我们的 FE 就是一个调用 luna 然后去访问这个 endpoint 来做出我们现在的 FE" … "我们需要的返回其实是这些 thesis 的各种信息可以 overlay 在 FE 上面" … "还有 user thesis 要能够变成一个 idea card" … "这边有蛮多需要思考和你先自己测试的，我们开始做吧".
- Decided: the HTTP and MCP fronts run as two services of one Docker image (local ports only). One new route, `POST /ideas`: the service searches (D76, D91), luna reads the top-k and chooses the views that bear on the idea with one line why each and a short reading, code evaluates a number the idea states, and the answer carries the chosen views in the FE's existing data shape so the FE overlays them under the idea card. The model key stays in the service (the credentials file mounted read-only), never in the browser. Hivemind still stores no idea (D76). Design and tables: `docs/poc/idea-card.md`.
- Measured first, before the FE is wired: the example theses and the day-0 sentences through the route once (cost, seconds, chosen views against the leads).

## D113 · 2026-10-24 · Add the colon to canvas due dates

- Alex requested "Due:" on canvas card footers, matching the detail header label. Date values and formatting stay unchanged.

## D114 · 2026-10-24 · Present score definitions as a table

- Alex asked to replace the loose score-definition list with a table. History now uses aligned Score, State and Definition columns, a neutral header and thin row separators. When the score already names the state (Yes/No), omit the redundant State column. The underlying rungs and their order are unchanged. About this thesis keeps its compact label/value rows.

## D115 · 2026-10-24 · Use a uniform Score change heading

- Alex asked for the history change section to be titled "Score change" consistently. Both previous heading variants use that title; the explanation remains in the body.

## D116 · 2026-10-24 · Simplify history navigation to two right-aligned buttons

- Alex asked to remove the long assessment selector and keep only left/right buttons at the lower right. Place Previous and Next together below the chart, aligned to its right edge. The selected date and score remain in the assessment heading. Buttons still visit every stored assessment and disable at the first/last record; chart selection is unchanged.

## D117 · 2026-10-24 · Strengthen chart headings and separate the two plots

- Alex asked for larger AI score and Evidence / day headings and more space between their plots. The shared chart uses 14px semibold titles and a 36px inter-plot gap (previously 11px medium and 24px). Canvas cards gain the same 12px of height, to 420px, keeping the plot and footer spacing intact. Data, scales and date alignment are unchanged.

## D118 · 2026-10-24 · Keep canvas chart subtitles smaller than detail headings

- Alex clarified that the larger chart titles are too big on the main canvas cards. Canvas AI score and Evidence / day titles use 11px medium; detail-panel chart headings stay 14px semibold. The increased spacing between plots remains.

## D119 · 2026-10-24 · Inspect and anchor history by date

- Alex asked for a hover crosshair and click-to-anchor state in History. Hover previews the calendar date, the last assessment on or before that date, and that day's evidence count; it never changes the selected assessment. A vertical guide spans both plots, with a horizontal guide and dot at the score when one exists.
- Clicking pins the date and selects that assessment; leaving the chart restores the pinned preview. Previous/Next selects and pins the corresponding assessment date. A date before the first assessment shows "No assessment" rather than borrowing a future state; Next moves to the first assessment. Arrow keys/Home/End move the preview and Enter/Space pins it. Opening another thesis starts without a pinned crosshair. Only History changes; canvas charts and stored data do not.

## D120 · 2026-10-24 · Remove the History hover label and navigation buttons

- Alex asked to remove the floating date/score/evidence label and the Previous/Next buttons. Remove those elements and their unused styling and handlers; retain crosshair hover, click-to-pin and keyboard date selection. The selected assessment date and score remain in the content below the chart, and the chart's accessible value still describes the inspected date.

## D121 · 2026-10-24 · Make quiet-day History selection explicit

- Alex rejected the persistent right-edge crosshair and the confusing behavior between dated events. History omits the canvas replay playhead and the separate assessment marker; its only inspection crosshair is the hovered or pinned date.
- A click anchors the exact calendar day, even without a new assessment. The content heading shows that day and the active score; a quiet-day note names the assessment date carried forward, and says "No new evidence on this date" only when the selected day's stored evidence count is zero. Dates before the first assessment retain the explicit no-assessment state. Canvas replay stays unchanged.

## D122 · 2026-10-24 · Lock clicked History anchors and keep endpoint dots whole

- Alex clarified that a click must leave a visible vertical dashed line and dot, a quiet-day click should select the closest earlier assessment, and the latest dot needs more right-side room. Pointer movement previously reused and moved the clicked guide. The final clip boundary also passed through the last dot's center (observed x=643 and clip width=643, radius=3.5).
- Hover previews until a click pins an assessment. After a click, pointer movement does not move that anchor; another click selects a new one. Snap both guide and dot to the last assessment on or before the clicked date, and show that assessment date below. Dates before the first assessment still show no assessment. Use a dark dashed guide and a filled pinned dot.
- Increase the chart's right inset from 10px to 18px. At the final date, extend the clip to the SVG edge so the whole endpoint circle fits; intermediate canvas replay frames retain their time cutoff. This supersedes D121's exact quiet-day anchor and carried-forward note.

## D123 · 2026-10-24 · Remove the current-date dashed line from canvas cards

- Alex asked to remove the rightmost current-state dashed line from the outer cards too. Canvas charts omit the replay playhead and the final-date vertical grid line; the endpoint dot, date label and intermediate grid lines remain. Replay still updates the score, clip and dot without a vertical cursor.

## D124 · 2026-10-24 · Remove canvas card footers

- Alex asked to remove the due-date pill and the entire bottom footer from the main cards. Remove the footer markup and its unused styles, and reduce card height by its 40px to 380px so no empty footer space remains. Due dates remain in the detail header. Chart dimensions and centered fan-out layout are preserved.

## D125 · 2026-10-24 · Center the initial graph in the usable canvas

- Alex asked for newly created cards to appear around the middle of the canvas rather than at its top. Fit now measures the actual card bounds and centers them horizontally and vertically inside the viewport, reserving space above for the replay toolbar and 24px at the other edges. The Fit control uses the same calculation.
- First creation is fitted even when only an unmatched Idea card exists. A different matched graph is fitted again; updates to the same graph preserve the user's pan. The parent-centered fan-out inside the graph is unchanged.

## D126 · 2026-10-24 · Add the black TrueNorth mark beside Hivemind

- Alex asked for the black TrueNorth logo to the left of Hivemind in the header. Reuse `web/hivemind-logo.svg`, which matches the old repository's TrueNorth mark, display it at 20px with a 9px gap, and render it black through a local style. The shared source asset is unchanged.

## D127 · 2026-10-24 · Balance the Hivemind wordmark with its logo

- Alex asked for slightly larger Hivemind text to match the 20px logo. Increase the mock header wordmark from 15px to 18px, retaining its weight and alignment.

## D128 · 2026-10-24 · Enlarge and center canvas navigation controls

- Alex asked for larger zoom buttons and larger centered icons. Use 44px square buttons with 22px outline SVG icons, centered with grid layout, and 6px spacing. Zoom in, Zoom out and Fit to view keep their existing actions and receive explicit accessible labels.

## D129 · 2026-10-24 · Keep only Full and Last 30 days

- Alex asked to remove the From Jul 24 range. The replay range control now offers only Full and Last 30 days, using their existing date calculations.

## D130 · 2026-10-24 · Modular Thesis UI with a versioned data contract

- Alex asked to clean and modularize the Thesis components for data returned by an agent/MCP, leaving the Idea card for later. Use one versioned, closed schema, one adapter for existing bundles, pure dated selectors, and separate card/chart/detail/canvas components. Keep the agreed visual design. Components take data and callbacks and own their event cleanup; no UI component calls a model or reads global application state.
- Source uses ES modules. The existing standalone mock remains a generated artifact; esbuild bundles the modules and Ajv compiles the JSON schema at build time, avoiding a hand-written bundler or schema engine. These are build-only dependencies. Scope, state/reader tables and budgets: `docs/poc/thesis-ui.md`.
- The existing bundle writer now includes stable judgement IDs and event dates. `thesis_bundles` (MCP) and `GET /thesis-bundles?ids=...` expose that same complete read-only envelope, so the agent need not reconstruct UI inputs from partial reads. No model call or write is added. ESLint and Prettier provide development checks only.

## D131 · 2026-10-24 · Remove native hover text from card UI

- Alex asked to remove the repeated full-title tooltip that appears over a card. Card titles remain visible and clickable, but have no native title tooltip. The shared chart and navigation controls use accessible labels instead of native hover-title text.

## D132 · 2026-10-24 · Probing the idea route: aliases from the universe, Chinese text terms, a floor under null

- Alex: "do more matching of how an idea could use the endpoints to go about finding the right theses … see where, for example, the search engine retrieval may be lacking". 49 realistic ideas were run through search and the model (`docs/research/2026-10-24-idea-probes/findings.md`).
- Decided (implementation of D76 search and D91 null, not a change to either decision): an object is named only by its id, its full name or an alias the universe lists (`poc/universe.json` now carries product and Chinese names per company and theme; single words of a name are never aliases); the ledger's text index is asked for Latin words and three-character Chinese windows; `results` is null only when no object is named, no view text matches and the top similarity is below 0.30 (measured: every idea with a view scores 0.33 or more; a house purchase 0.19). Ideas above the floor that name nothing go to the model, which answers "none".
- Open, for Alex (findings §Choices): k above 10 or a per-object cap; evaluating percent, gigawatt and count ladders; the card naming objects without a view; a role per chosen view.

## D133 · 2026-10-24 · Everything in data and code is English from now on, natively

- Alex: "从现在开始所有数据和代码里面的各种都要是英文" … "不要再做什么转译。原生全部是英文理解了不".
- Decided: code (identifiers, strings, comments, docstrings), everything the system writes (ledger text, answers, labels, card fields) and every model output are English, written in English at the source. No translation layer anywhere: a Chinese text is not turned into English after the fact. The sealed ledger of 2026-10-24 is Chinese and is not rebuilt (Alex, same evening: "千万不要 rebuild 这个 db"); it stays as it is, and the page shows its text as stored, until the next run writes English natively. That run needs the pipeline's prompts to ask for English (role, categories, matching, judging), a new config version, and the service's ladder parser to read English conditions; it is a paid run Alex launches. The design documents stay in plain Chinese for Alex (AGENTS §11).

## D134 · 2026-10-24 · The idea is read by an agent that calls Hivemind, the way a fresh Luna with the MCP would

- Alex: "imagine it's just like a fresh Luna loaded with the MCP of HiveMind … what the users ask as an idea, how to break it down into mapping theses … it's going to break down into a couple ways, which … are basically just query endpoints or whatever API or MCP calls to the HiveMind to retrieve whatever is necessary so that the agent can actually determine what are the final theses that need to go in to support the idea … That's the flow." Earlier the same evening: "你现在映射的观点都比较少，这个也是一个问题" and "idea 的拆解，映射这个可能有一定的系统提示词需求，可以写在这个 mcp 或是我们 api loading 时候就给到的系统提示词".
- Decided: `POST /ideas` runs that flow inside the service: luna gets the same tools the MCP front offers (search, view, evaluate) plus finish, and a system prompt (`prompts/idea-v4.txt`) that says how to work: break the idea into two to four parts (the thing itself, its drivers, what could break it), search for each part, read what matters, map each part to every view that answers or moves it, evaluate a dollar number, finish with the reading. Code runs the tools, remembers which views the agent has actually seen (a finish may name no other), evaluates the claim itself, and archives every turn so a card replays for $0. The MCP front's instructions carry the same recipe for an external agent. Measured before this change: one call over the top-10 of one search mapped a median of one view per idea (49 probes); the two-step prompt over 20 candidates mapped a median of two.

## D136 · 2026-10-24 · Slide the Thesis detail drawer open and closed

- Alex asked for smooth slide-in and slide-out when opening and closing a Thesis. Use a shared 280ms drawer motion controller: the panel slides from the right while the scrim fades, and stays mounted until the closing motion finishes.
- X, scrim and Escape use the same close path. Reopening during a close reverses from the current visual position; repeated closes do not restart it. Focus returns after the exit finishes. Dataset replacement and destruction cancel pending motion; reduced-motion preference skips it.

## D135 · 2026-10-24 · The service does the looking up; the model is asked twice

- Alex, after the agent version was measured (27,000 input tokens per idea, a quarter of them a catalog re-sent every turn, the same mapped count as one call): "But isn't this return very, very inefficient in terms of the context bloat? … Measure it and realistically tell me if this is the right way." Then, shown the split: "不是本来就应该这样做吗？"
- Decided: `POST /ideas` asks the model twice and nothing else. Call 1 breaks the idea into two to four typed parts (object from the library's object list, what to look for, period, a search query) and reads a dollar claim. The service searches once per part (8 candidates each, id + what it looks at + judged position), follows the ledger's dependency graph from the first part's views to their upstream and downstream views, and evaluates the claim. Call 2 maps each part to its candidates and writes the summary; the service admits only candidate ids. The agent loop (D134) is removed from the service; the MCP front keeps the recipe for an external agent, with the object list instead of a catalog. Measured on the first three ideas: 2,640–2,750 input tokens per idea against 27,000.
- Confirmed by Alex after the 49-probe comparison (5 views mapped per idea against 2, 2,704 input tokens against 27,048): "可以，你确认这个方向是对的，先定论，然后再继续想要怎么优化 1. 速度 2. 成本 3. 质量和稳定的结果". The split is the design; what follows is tuning, each change measured against a fresh control on the same ideas.

## D137 · 2026-10-24 · Keep card connectors separate and attached to their cards

- Alex asked for the reference's rounded orthogonal routes, without overlapping lines or attachment points outside a card. This amends D84's fixed 24px outgoing-port spacing: 24px is the maximum; compress the spacing to keep the ports at least 24px inside the top and bottom corners. Each path begins exactly on the source's right edge and ends on the target's left midpoint. Keep D85's arrows and D87's incoming-path highlight.
- Diagnosis: the three stored Idea response fixtures contain one 12-child graph, with 30 overlapping vertical-segment pairs; the other two are empty. The 42 stored default graphs have no overlapping branch pairs because their fan-outs are smaller. Every route currently turns at the same horizontal midpoint; with 17 or more children the fixed port spacing also exceeds the 380px card height. Card-only entry translation briefly detaches connectors from their cards.
- Route ownership is `poc/ui/src/components/connectors.js`: order destinations vertically, nest the outer destinations' turns nearest the source, and give successive turns 12px lanes. Upper and lower routes can reuse a lane only where their vertical spans do not touch. Increase the inter-column gap when the lanes need it. Fade cards into place without translating them independently of their lines.

| State / event | Result |
|---|---|
| Empty / zero destinations | No paths. |
| Render / one or many destinations | Measure unscaled card rectangles, assign bounded ports and nested lanes, then draw rounded paths. |
| Replay or range change | Preserve the same graph attachments; a graph redraw recomputes from its card rectangles. |
| Pan, zoom, fit | Cards and paths share the world transform; attachments stay aligned. |
| Replace data or graph | Rebuild paths with the new card set; retain no old lanes. |
| Destroy | Existing canvas cleanup removes cards, paths and handlers. |

| Value / writer | Readers and checks |
|---|---|
| Card rectangles / canvas placement | Shared route function; source and destination edge assertions. |
| Bounded ports, lanes and rounded path / route function | SVG renderer, stored-fixture and all 0–93 child-count intersection checks. |
| Expanded column gap / route function | Supporting-card placement and fit bounds; existing pan, zoom and hover handlers. |

- Before implementation, the proposed geometry was replayed over every 1–93 child fan-out supported by the 94-thesis ledger: no intersections and no ports outside the source. The browser check must exercise the stored 12-child response and compare real path endpoints to card bounds. No schema, data, model prompt or thesis relationship changes.

## D138 · 2026-10-24 · Idea cards share the Thesis header and connect every mapped thesis directly

- Alex asked to match the Thesis header, remove the redundant decomposition list, and explain/fix why every thesis was drawn after the first. The stored response has three analysis parts, eight distinct chosen theses and five related theses. Its third part maps to none. Across the three stored response fixtures, one has this graph and two have no chosen theses. The FE made the first chosen thesis the parent of the other seven and all five related theses; four of the five related paths ignored their actual `via` source. The backend already supplies each related source, so no backend or model change is needed.
- The Idea and Thesis use one header renderer and a non-shrinking 40px header. Remove the decomposition rows and their IDs from the Idea card; keep its question, verdict and reading. `reading.parts` stays in the response for analysis, not as card rows.
- All distinct `reading.chosen` IDs are peer roots directly connected to the Idea. Only `related` entries connect after a root, using their supplied `via`; neither list order nor the first chosen thesis creates a dependency. Keep related nodes in separate, vertically reserved groups after their actual source. Null/empty responses still show the Idea alone. This replaces the first-thesis-as-parent UI rule recorded in D112/D135 integration notes; it does not change which theses the service chooses.

| State / event | Result |
|---|---|
| Pending, failed, null, or no chosen theses | One Idea card, shared header, no invented thesis or edge. |
| Answer with chosen theses and related entries | One direct edge per chosen thesis; one related edge from its supplied `via`. |
| Replay or time-range redraw | Keep the explicit graph; update the same dated card contents. |
| New answer or dataset | Validate known IDs before rendering; retire graph nodes no longer loaded. |
| Pan, zoom, hover, detail open/close | Preserve attachments and incoming-path highlighting for each branch. |

| Value / owner | Readers and checks |
|---|---|
| `rootIds` and `branches[{sourceId,targetId}]` / Idea graph adapter | Shared graph validation, layout and canvas; stored response must map each chosen ID and `related.via` exactly. |
| Card rectangles and edges / pure graph layout | Renderer and connector planner; reserve each source's related group, bounded ports, no overlapping routes. |
| Header HTML / shared primitives | Both card renderers; browser compares height, padding and icon placement. |

- Existing standalone `primaryId`/`supportingIds` callers are normalized into the same layout. The new explicit graph accepts only loaded, unique root IDs and single-parent related nodes with a root source; malformed graphs fail before replacing the visible graph. D130's data contract, D137's attachments, and the existing empty/replay/instance checks remain in force. Uneven groups need lanes based on the actual upward/downward routes, rather than assuming half the roots lie on each side of the Idea.

## D139 · 2026-10-24 · Evaluate overarching main theses before building the next layer

- Alex clarified that the desired result is an overarching main thesis exposed to agents, with linked supporting theses underneath, potentially spanning companies and industries. He asked for small POCs of the different approaches on existing NVIDIA data and a written technical proposal before implementation.
- Scope authorized: isolated experiment code and new dated outputs. Do not rebuild the sealed ledger, change production extraction, or switch the UI while evaluating. The experiment compares vector density, recorded-graph communities, global LLM grouping, incremental grouping, and a separately declared argument-first approach; a targeted revisit diagnostic checks the observed orphaning mechanism.
- Plan, raw-output locations, findings and proposed interfaces are in `docs/research/2026-10-24-hierarchy-poc/`. This decision authorizes research, not adoption of a production grouping method, main-thesis ladder, or scoring rule. The draft uses supported/challenged qualitative arguments without a new numerical score; that choice remains a product decision.

## D140 · 2026-10-24 · Validate only two main-thesis update paths

- Alex: “开始实验，不要随便乱加戏，scope creep. 好好的做好核心验证.” The authorized follow-up is only Rubin commercialization and cloud capex → NVIDIA revenue, replayed over three stored historical snapshots with three independent samples and fresh-generation controls.
- This is an isolated research follow-up to D139. No extraction, production schema, MCP, UI, automatic clustering, identity discovery, or recursive hierarchy is added. Invalid results are retained without repair or replacement sampling; dependent update chains stop.
- Results: 25 completed requests, estimated $0.546144 under repository prices; 14 of 23 synthesis outputs rejected for real evidence IDs paired with the wrong view. The only complete Rubin update chain omitted supplied delay risk. Findings: `docs/research/2026-10-24-main-thesis-replay/findings.md`. No production approach is adopted; the proposed citation-representation follow-up is not implemented.

## D141 · 2026-10-24 · Validate code-owned sources and current evidence before summaries

- Alex authorized the follow-up after the failure analysis: “好你思考清楚了就下手跑验证”. Scope remains the same two questions, three historical snapshots, same model, and three independent samples. No production or UI changes.
- The experiment gives each real source one immutable reference with code-owned origin paths. It assesses every current source before a final summary, without reading old summary text; fresh direct-synthesis controls share the same source format. Both final cards are read by an agent.
- Completed 42 requests, estimated $1.059854 at repository prices. All 822 source-assessment instances and all 24 summary/reader outputs passed structural checks. Rubin's delay risk reached the summaries and readers in all three samples of both methods. Full basis processing did not show better core outcomes than direct synthesis; its final-round cost was 2.52 times as high. Findings: `docs/research/2026-10-24-main-thesis-basis/findings.md`.
- This records research, not production adoption. The recommendation is to prefer code-owned provenance and synthesis from current material, without making a full per-source basis table mandatory yet. Automatic clustering, stable main-thesis matching and bounded streaming updates remain outside the experiment.

## D142 · 2026-10-24 · Test organization inside ingestion, not after extraction

- Alex corrected the research direction: thesis associations should emerge during extraction and streaming ingestion. He authorized a short original-article replay through extraction, matching and writing, with no separate full-library clustering pass.
- The isolated POC uses three original articles, three independent samples and ordinary-ingestion controls. New grouping fields are part of existing extraction/matching calls; original checks and writer are reused. No sealed database, production prompt, MCP or UI changes.
- Completed 37 requests, estimated $0.512881. All three extraction samples linked the new SK deployment thesis to the existing Rubin shipment thesis, but all three matching answers placed them in separate narrow groups. A zero-call replay resolves and retains those three extracted relations. This diagnoses the duplicated relationship decision; it does not adopt a production group hierarchy.
- The experiment's affected-group bookkeeping defect was fixed and verified by replaying all 37 identical requests without network calls. Findings: `docs/research/2026-10-24-ingestion-groups/findings.md`.

## D143 · 2026-10-24 · Test one owner for ingestion relationships

- Alex asked which PRD must change, for a clean end-to-end repair, a logical simulation, then another POC. Amend the extraction and views PRDs with an explicitly experimental relationship contract. This authorizes the isolated experiment, not a production rollout.
- Extraction proposes the shared research question, members and source evidence. Matching resolves thesis identity without rewriting group membership. The writer resolves all temporary references and saves the group, members and provenance in the same transaction as the original thesis/evidence writes. A new group requires two distinct resolved theses; a single thesis stays independent. Group membership does not create a causal dependency or a scored parent thesis.
- Keep the same three original articles, three fresh paired samples, existing model/settings, and a total ceiling of 48 calls/$8 estimated. The control is D142's grouping path. No sealed-data rebuild, production prompt change, extra clustering call, summary, MCP or UI work. Plan and acceptance: `docs/research/2026-10-24-relation-handoff/design.md`.

- Result: all six streams completed; 36 requests, estimated $0.561000, no extra clustering calls. Fresh automatic shipment/deployment grouping succeeded in 1/3 new samples and 1/3 controls. New-arm risk evidence reached the original shipment thesis in 3/3 samples, but reached a shared group in only 1/3. Acceptance failed; no production adoption or further arm. Findings: `docs/research/2026-10-24-relation-handoff/findings.md`.

## D144 · 2026-10-25 · Research continuing subject identity inside ingestion

- Alex rejected the two failed grouping attempts as an unclean design and explicitly asked for deeper research and another run within the current pipeline. Scope remains isolated research, not production adoption.
- Proposed experiment: extraction gives every candidate thesis a required reference to a continuing business subject; the existing matching call separately resolves subject identity and thesis identity. Code preserves those references when writing. A subject can start with one thesis; membership is not an optional afterthought or causal claim. This replaces D143's experimental two-member creation condition, not the frozen production schema.
- Keep the three original articles, three fresh paired samples against D143, the same model/settings, and the existing maximum of 48 calls/$8 estimated. If the three new core grouping samples pass, use one predetermined additional Rubin customer-deployment article per new stream (as late arrival) to test another milestone; no new comparison claim. Full contract, prior decisions, research sources and fixed criteria: `docs/research/2026-10-25-ingestion-threads/plan.md`.

- Result: 23 attempts, 22 returned and one extraction timeout. Both returned new-arm first-article match answers used self-targets for all six local threads and were rejected by the registered identity contract; none of the three new streams reached the later grouping test. All three D143 controls completed but formed no shared group. Returned-call estimated cost was $0.315563; the timeout has unknown usage and retains a $0.2327375 budget reservation. No extra article or replacement samples ran.
- A zero-call diagnostic changed only those six self-targets to the required empty new-target representation; both first articles then wrote three theses and three threads. This isolates a format-boundary failure, not successful automatic grouping. No production adoption. A proposal to replace local pointer chains with direct identity groups remains unimplemented and needs a revised experiment contract. Findings: `docs/research/2026-10-25-ingestion-threads/findings.md`.

## D145 · 2026-10-25 · The idea card keeps the full mapping contract

- Alex, after the night's tuning report (13 measured iterations, `docs/poc/idea-tuning-log.md`): "用完整版吧". The
  service's mapping call keeps the per-part reason (prompt idea-v7, the `MAP` schema), at reasoning effort none:
  `poc/config/poc-v9.json` is the default of the API and the scripts. The lean contracts (idea-v8: no reason, each
  candidate once; idea-v9: no reason, full briefs) stay in `CONTRACTS` as measured arms, not as the product.
- Why (measured): the reason the page never shows is what steadies the mapping. 8 ideas × 3 fresh samples, canvas
  overlap median: with the reason 0.58 and 0.65, without it 0.55 and 0.50; first view 8 of 8 against 7 of 8. The
  reason costs ≈ 2 s and ≈ $0.003 per idea (10.9 s and $0.0098 against 8.6 s and $0.0070).
- Kept with it, all code: direct / driver / context tiers with at most three drivers per part; the direct pick made
  among the model's direct views in search order with the year check; the market-price guard; the English re-ask;
  the canonical second query per part; one embeddings round trip per idea.
- Next arms, in order, each measured the same way (49 probes, 8 × 3 stability, serial timing): the reason capped
  at twelve words; six candidates per part instead of eight. Target $0.005; the 6 s target is below the floor of
  two serial calls on this network and is not pursued.


## D147 · 2026-10-25 · Continue grouping POCs with direct subject identity results

- Alex explicitly asked to keep testing from different angles, read the system design and code, and improve barriers within the existing pipeline. This authorizes continued isolated diagnosis and development POCs; no production, sealed ledger, Idea, UI, deploy or model/provider change.
- Replace D144's model-authored local pointer graph with direct groups of local subject IDs whose destination is either new or a displayed stored subject ID. Keep extraction-owned required thesis membership, original thesis identity/evidence rules, and one transaction. Schema restricts destinations; code resolves final IDs without recursion.
- Three fresh paired original-article streams against D144, followed by the predetermined extra deployment article only after correct core grouping; same gpt-6-luna/settings, shared maximum 48 calls/$8 estimated. Preserve failed variants and fixed measurements; do not silently replace samples. Plan, state tables and scope: `docs/research/2026-10-25-direct-subjects/plan.md`.

- The first direct-group variant completed 20 requests ($0.334354 estimated). One new stream omitted its required groups; two completed but treated the customer deployment as a different subject from Rubin and split it. All three D144 controls failed subject-count checks. The displayed old group was present in both split cases, so retrieval was not the cause.
- Continue within the same 48-request/$8 ceiling with extraction-owned membership: retrieve existing group descriptions before reading the full article, require every candidate to cite a shown old group or declared new group, and remove group identity decisions from matching entirely. Matching still resolves the thesis and evidence identities. This asks whether a thesis belongs under a business process, not whether two business processes are identical. The narrower required-output-format draft is not implemented because it would leave this semantic defect intact. Contract and tables: `docs/research/2026-10-25-direct-subjects/extraction-membership-plan.md`.
- Extraction-owned membership reached the old Rubin group in all three second-article answers, but all returned duplicate g1 references and an unused local t1, so all three were rejected. Nine new calls brought the shared total to 29 ($0.447565 estimated). Continue with a strictly equivalent reference-schema spelling, without changing the prompt, accepted values or local checks; fresh second-article calls use copies of their successful first-article states. This is a representation diagnostic, not proof of a provider defect. Contract: `docs/research/2026-10-25-direct-subjects/flat-reference-plan.md`.
- The equivalent single-pattern schema produced valid distinct old/new references in all three second-article samples. Two completed the core relation/risk path; one valid old-group assignment was rejected solely for an unused proposed new-group definition. Remove that redundant rejection: unreferenced definitions already never reach the writer. Keep nonempty, unique and valid membership references, unique definition IDs, and all original evidence checks. This changes the experimental input contract, not the semantic acceptance criteria. Replay identical stored requests into new databases, call only missing steps, and keep the same shared ceiling; 38 requests/$0.560701 estimated have been used. Contract and census: `retained-membership-plan.md`, `unused-census.json` in the D147 research directory.
- Final core result: all three recorded streams preserve separate shipment and SK-deployment theses in the same Rubin group and route later supply risk to it. The three preselected satellite continuations also reuse that group without changing historical snapshots or removing the earlier risk. The code-only final correction replayed original answers; it did not obtain three replacement samples. Total: 47 returned requests, estimated $0.641424. 121 tests and targeted mutants passed. No production adoption; overall group counts (1, 4, 3), large-library recall, cross-company boundaries and an argued main-thesis layer remain unvalidated. Findings: `docs/research/2026-10-25-direct-subjects/findings.md`.

## D146 · 2026-10-25 · The idea gold set: twenty ideas judged as an analyst, authored by Claude, sealed

- Alex, asked for twenty gold ideas with the right views written beside each: "做。然后3.的标准就是hedge fund analyst
  /investor 会看的观点，你来进入角色做golden 然后封存". The standard is the views a hedge-fund analyst or investor would
  want to see for the idea; Claude writes the gold in that role, from the view texts of the sealed ledger as judged on
  2026-08-15, and seals it.
- The file: `poc/eval/gold/idea-gold-2026-10-25.json`, digest in `poc/eval/gold/SHA256SUMS`, never edited; a revision
  is a new dated file. Twenty ideas: six on NVIDIA, seven on other companies (TSMC, Meta, CoreWeave ×2, AMD,
  Microsoft, Intel), six on themes (hyperscaler capex, Big Tech AI spend, H100 prices, the AI trade, 232 tariffs,
  data-center demand), two in Chinese, two the library does not cover (232 tariffs on semiconductors, chip export
  controls and NVIDIA's China revenue), whose right card shows no direct view. Each idea carries the accepted direct
  views, the one a stated amount is judged against, the drivers an analyst wants beside it, acceptable neighbours,
  and traps (a view that looks like the answer and is not: total revenue for a segment, total expenses for capex,
  TSMC revenue for TSMC capex).
- Labelled model-authored gold (AGENTS §7): it measures the service against an analyst's reading written by the same
  model family, not against Alex's hand; a disagreement with Alex's own reading is settled by a new dated file.
- `scripts/idea_gold.py` scores a configuration against it: direct view right, traps shown as direct, driver recall,
  canvas noise, claims right; it refuses a gold file whose digest is not the sealed one.


## D148 · 2026-10-25 · Check grouping consistency by research meaning, not identical group counts

- Alex asks to keep working on grouping consistency while Claude Code works on Idea consistency: results need not match exactly every time, but must not be far off. Keep grouping and Idea work separate until their findings can be combined.
- First replay the three completed D147 streams from stored answers and separate extraction coverage from membership variation. Keep distinct questions and their real evidence links; names, local identifiers and extra small groups alone are not errors. Do not add a group-count target or delete small groups to make the counts agree.
- Run the unchanged D147 process on two previously unused full articles, one about AMD growth and one about Google Cloud's Rubin deployment, starting from copies of the three different D147 states. Report missing connections, unrelated memberships, extraction gaps and rejected calls separately. This is descriptive boundary research with assistant-authored semantic checks, not a new overall quality acceptance threshold or a claim that the method improved.
- New bounded continuation experiment: at most 18 requests/$2 estimated, same model/provider/settings. The completed D147 budget and artifacts stay unchanged. No production, Idea, UI, summary or separate clustering-call change. A failure is retained and reported without replacement samples. Contract and scope handoff: `docs/research/2026-10-25-grouping-consistency/plan.md`.
- Before paid calls, source-level review corrected an earlier classification: sample 2's OpenAI deployment explicitly uses Rubin but belongs only to its new OpenAI group. This is one real missed membership among ten reviewed Rubin-related thesis instances, alongside two samples that did not extract that extra thesis. Pause the new-article continuation and first test the narrower cause: D147 stopped showing existing theses' stored group memberships. Run three fresh unchanged controls and three fresh requests that add only those already-stored membership IDs to the displayed theses, through the original matching/writing path, within the same 18-request/$2 ceiling. Preserve the earlier plan and review; no new prompt, schema, production rule or acceptance target.
- Result: all six samples completed in 12 fresh requests, estimated $0.202629. Context samples preserved the OpenAI-to-Rubin link in 3/3, but one also placed the unrelated PC thesis in Rubin and another omitted delay evidence. Controls showed an omitted extraction, a rejected altered quote, and an OpenAI membership in the SK-specific group. Both controls that actually proposed OpenAI already referenced Rubin, so the original missed-membership mechanism is not proven repaired. The context variant is not adopted. All history/resend checks pass; the known semantic defects remain explicit. Findings and the proposed joint review with Claude's Idea work: `docs/research/2026-10-25-grouping-consistency/`.

## D149 · 2026-10-25 · Group association is required during extraction

- Alex asks to refresh the relevant PRDs so group association is implicitly needed during extraction. Organization is part of reading incoming information, not an optional later whole-library clustering step. Every proposed thesis carries structured membership in a continuing business subject; evidence-only updates follow the existing thesis memberships.
- Preserve the D33 responsibility boundary: extraction decides membership while reading the full source; matching resolves thesis/evidence identity and dependencies without deciding membership again; the views writer preserves the association against final thesis IDs. The complete target contract is owned by `06-views.md`, with extraction's responsibility in `05-extraction.md` and summaries in the system overview and design page.
- A group organizes related questions, including across companies, without turning them into the same question or automatically making one a scored parent. A single thesis can start a group. The longer-term overarching investment thesis for agents remains separate work, not a capability delivered by this refresh. D148's tolerance for minor naming or optional subgroup differences remains; wrong members and missing core connections still matter.
- This changes the documented target, not the running pipeline. Keep D147's isolated handover implementation visibly separate from the required behavior and D148's rejected context variant. No production prompt/schema change, stored-data migration, new paid run, group-summary generation, MCP or UI change is authorized by this documentation slice. Adding a short reason for each membership remains an unvalidated proposal.
- Record current implementation gaps in `docs/poc/pipeline-plan.md`; refresh status and the PRD bundle. Change census and reasoning refresh: `docs/research/2026-10-25-grouping-doc-refresh.md`.

## D150 · 2026-10-25 · Test a source-based membership explanation within extraction

- Alex asks to continue working on a clean grouping-consistency solution while Claude works on Idea. Continue isolated grouping research; do not change Idea or the default pipeline.
- The census is 18 saved extraction answers, 19 candidates and 27 membership references. Wrong PC→Rubin and OpenAI→SK references are already in raw extraction; matching and storage retain them. Test whether requiring a short source-to-scope explanation before each chosen group ID reduces these errors. This is a hypothesis, not an adopted fix.
- Keep the full original article, fixed two-article prefix, original model/settings, and original identity/source checks. Three fresh controls and three fresh explanation samples; only if the registered development conditions hold, measure the predefined Google article once with three samples per arm. New independent maximum: 24 HTTP attempts/$1 estimated; prior study budgets and records are untouched. Stop without replacement samples or automatic new arms.
- The new output is validated before projection to the old membership IDs; explanations are archived, never treated as evidence or sent to identity matching. No separate clustering call, group-count target, production schema migration, or claim that rationale helps because Claude used it. Claude's latest per-driver rationale arm did not improve consistency.
- Contract, state/event and value/reader tables, unchanged measurement definitions and read-only review: `docs/research/2026-10-25-grouping-basis/plan.md`.
- Result: 12 fresh calls, estimated $0.199548. The basis arm had one correct OpenAI→Rubin result, one omission, and one PC→Rubin error; controls repeated OpenAI→SK and also produced PC→SK. No adoption or conditional Google run. Across D147/D148/D150, five wrong references and one missed membership remain visible; three wrong-reference answers also declare an appropriate new group but reference a different old one. A zero-call one-ID correction confirms the writer preserves the supplied reference. This does not establish why the model selected it or validate the next representation. All 135 tests and targeted mutants pass; source, history and resend checks pass. Findings: `docs/research/2026-10-25-grouping-basis/findings.md`.

## D151 · 2026-10-25 · Before the NVDA rerun: the two sessions merged, two prompt rules corrected and proven on stored requests

- Alex: "codex 做完了，你合并，然后解决你上面的顺序问题，开始跑小的验证快速的收敛这些问题。确认是真实的问题，不是你自己看错或是理解错误；务必不要scope creep乱搞". The merge is commit 7033c87 (one tree, both sessions' work, every suite passing).
- Verified on the sealed run (`docs/poc/pipeline-plan.md`, 重跑前的基本面): nine product-trivia views and no H200 licence view (60 items mention it); two of 465 judgements read "no fact confirms" as the lowest rung; eight theme views that are anti-dumping or scrap-metal notices; the English requirement is a contract migration (137 Chinese literals in the pipeline's code, 13 KB of prompts, a Chinese-only ladder parser), not a prompt change.
- Adopted for the rerun as `poc/config/poc-v14.json`: `role-v3` (a dated event opens a view only when it moves a full-year number or a segment; pending regulatory decisions open without a date, due at the fiscal year end) and `judging-v2` (missing confirmation is not the lowest rung). Proof on the stored requests with only the prompt changed: the three trivia items open nothing in 6 of 6 samples, the May 10-Q opens the H200 import-licence view in 2 of 2; the two misjudged cases move to rungs 4 and 3, the rung-5 control holds.
- Not changed: grouping (D149, Codex's slice, still not in the default pipeline); the language (Alex's call: run in Chinese now or migrate first). The rerun reads the relabelled corpus `items-window-tags2-2026-10-24.sqlite`. A one-week run comes first.

## D152 · 2026-10-25 · The rerun runs in Chinese first; grouping passes to Claude

- Alex, on the language: "1. 可以吧。" The NVDA rerun runs on the Chinese pipeline with the corrected rules (poc-v14);
  the English migration (137 Chinese literals in the pipeline's code, the four prompts, the ladder parser; D133) is a
  separate slice, scheduled after it, measured on its own.
- Alex, on grouping: "2. codex 已经停止了，要靠你来接着把这部分整好，你单独的把这块搞对". Grouping at extraction
  (D142–D150) is Claude's slice from here, worked on its own: Codex's experiments, reports and handoff
  (`docs/research/2026-10-25-grouping-basis/`, `poc/hierarchy_study/`) are the starting record; the default pipeline
  stays without grouping until a measured design is accepted.

## D153 · 2026-10-25 · Keyed views: the structural correction is the direction; the week run is read first

- Alex, after the structural review (`docs/research/2026-10-25-structural-review.md`): "好就这么做。你需要看完trace 给出非常干净
  的系统修正方案来解决我们上叙述的问题，从完整的写log 和计划按照这个来小范围的测试和改进，并量化的测量其效果".
- Direction: A, the one-week run with poc-v14 finishes and its trace is read in full; B, the correction is designed as
  one plan before any pipeline code changes: a view carries a key written by extraction and owned by code (measure
  from a closed list, period as a date span, basis, unit, rung bounds as numbers), research subjects become objects of
  the universe with aliases, each object carries the analyst's list of the quantities to watch, identity is a key
  match in code and the model only fills keys or chooses among shown names. The full-night rerun waits for the keyed
  design; the sealed ledger and the week run's data stay as they are.
- Record: `docs/poc/keyed-views-plan.md` (the plan and its tables), `docs/poc/pipeline-tuning-log.md` (one row per
  small test with its numbers). This decision departs from the frozen extraction and views design (D37, D58–D60) in
  the direction stated; the detailed contract is recorded as its own decision when Alex accepts the plan.

## D154 · 2026-10-25 · The keyed view contract as built and measured on the bootstrap documents (T1–T2d)

- Under D153 (Alex: "T2可以按照你看完T1的结果自己思索之后开始动工…我要看的就是量化的结果收敛"), the contract of
  `docs/poc/keyed-views-plan.md` was built into the default pipeline behind prompt version v4 (`poc/config/poc-v15.json`):
  every candidate view carries `measure` (closed list), `scope`, `period_start/end`, `basis`, `unit`, `event_type`; every rung
  carries numeric `lo/hi`; the ledger stores them (`view_keys`, rung bounds); the service judges claims on the numbers.
- What the four small runs on the same twenty bootstrap documents taught, each turned into a code rule and a test
  (`docs/poc/pipeline-tuning-log.md` T1–T2d): the key is a necessary, not a sufficient, condition of identity (T1: exact
  keys over-merged a run-rate into revenue); the model must not spell the scope or convert the fiscal year (T2: four tax-rate
  views, a wrong Compute & Networking period); a watched scope is recognised by the list's aliases (T2b: hyperscaler capex and
  the H200 licence refused on spelling); the unit belongs to the key (a level and a growth rate collided); the model's answer
  to "same quantity?" on a same-key pair is not stable between samples (T2c), so where code owns the key (scope from the
  list or none) code decides identity, and a merge across periods or quantities is refused whatever the model says.
- Result on the twenty documents: 11 views, 0 duplicate keys, 0 product-trivia views, the H200 licence, the Rubin shipment,
  hyperscaler capex and the export rule all open (the sealed run opened 10 views with duplicates; poc-v14 opened 15 with four
  duplicates). The watch-list gate was not exercised by filings (review pool empty); the week run (T4) exercises it.
- Known limits recorded, not patched: a basis of n/a on an existing view accepts both GAAP and non-GAAP candidates (right for
  NVIDIA's joint guidance, to be re-read on a company with distinct guidance); a statement about another year can still be
  linked as evidence to this year's view by the extraction when no view of that year exists (an evidence-link class, not a
  candidate class); grouping (research subjects as universe objects, 2.3) is not yet in the default pipeline.

## D155 · 2026-10-25 · 清单是参考，先修身份，再按顺序验证归组

- Alex 明确：公司清单可以作为初始参考，但清单外不能忽略；随后要求“总体的重新看一次系统设计”“完整的写一个 improvement plan”“一步一步的来解决并量化验证”。Codex 接手这一修复范围，保留 Claude 的并行修改。
- 改进计划与每步的证据在 `docs/poc/grouping-improvement-plan.md`。D154 的清单门槛取消；范围别名可以帮助找候选，不能单凭部分文字命中改写范围并自动合并观点。完整单年与明确自然年分开处理，多年不再抓首个年份转财年。
- 自动认定同一观点须完整键相同，包含事件类型；含糊的口径不能作为自动合并通配符。同一次交接中代码确定的同一问题只写一次，保留所有证据。搜索的宽松召回与身份判断分开。
- D149 归组要求不变。先验证同次抽取的归属交接，再接入按分发顺序读写的新路径；当天开始的快照不能证明后续抽取看到了当天新主线。小实验不证明全市场搜索能力。
- 当前只实施并验证计划中合同已完整的步骤；归组表示、原子写入与恢复的具体合同经原答验证和设计审查后再建。旧数据不回填，Idea、前端、交易、分类、Pull 和最终判定不在本次修改范围。

## D156 · 2026-10-25 · 先校正归组验收，再评价模型方案

- Alex 看过验收审查后要求「好你开始吧，我们一起看」。先修验收定义和离线检查入口，用已存结果及受控反例验证，不把旧关系保留或零次判断报成新归组成功。
- 当前验收定义、已数清的测量缺陷、状态表和案例卡由 `docs/research/2026-10-25-grouping-acceptance.md` 统一维护。它替代名字实验旧计划的推广通过线；旧计划与原答保留为历史。
- 本轮不修改产品的抽取、归组表示、身份、写入或提示词，不启动新的付费实验。业务样本按原文和已有研究分别判断应新增、更新证据、重复或不抽；语义未审不报正确，三次样本不推断总体可靠率。
- D149、D155 的产品边界不变。修好测量之后再固定下一轮真实案例的逐项预期和对照；上层投资论点、跨市场规模能力不由本轮获证。

## D157 · 2026-10-25 · 用当前中文管线验证 Ohio 两篇连续报道

- Alex 要求「开始继续做」，继续 D156 留下的 Ohio 案例。登记、接口和验收见 `docs/research/2026-10-25-ohio-grouping-poc.md`；各三次新鲜对照和归组序列，固定两篇全文，不延用旧缓存前缀或英文抽取。
- 只在隔离 POC 复用当前抽取、身份和证据写入，再由抽取携带业务组引用。下一篇能读组内真实成员；不凭相同名称合并组，不让比对替抽取补分组。归组不增加模型调用。
- 本次限 30 次请求、$1.50 估算保留额；不自动重试不明请求、不提高预算。逐项核对风险判断、同源转述和金额口径，失败停止推广，不私改验收或续开新臂。默认管线与其它模块不变。
- 实测已结束且业务验收失败：20 次调用、估算 $0.373923；三次归组只有一次接回风险判断，仍有错归与错连。实验自身漏传的编号 schema 约束已在原答上修正，未付费复测。原答和结果在 `poc/reports/2026-10-25-ohio-grouping-01/`；关于改变观点入口的建议尚未决定，不启动下一臂。

## D158 · 2026-10-25 · 追查 Ohio 入口并在同一归组流程内对照

- Alex 在 D157 失败后要求「根因是什么」「务必深度的看代码，trace 思考」「再重新尝试是否能解决」。据此重新诊断并做隔离实验，不沿用 D157 的失败配置直接推广。
- 全链路诊断、事前设计与同一验收在 `docs/research/2026-10-25-ohio-root-cause.md`。两臂都使用已修编号 schema、相同连续归组读取和写入；唯一模型差异是把枚举数字的入口段改为先提出重要且可核对的业务问题。没有官方承诺日期时使用明确的研究检查日。仅供实验，默认 role-v5 不变；不增建存储类型或上层 thesis。
- 另修已由原答证明的代码偏差：06 的次年限制针对数字，明确的 event / policy_event 不应被同一年度检查拒绝。其它检查照旧，重放全部范围列出差异。此修复不能解释或解决 Ohio 原答没提出事件的问题，独立报告。
- 各三次新鲜完整两篇序列，原 O1–O6 不变；本轮独立 30 次请求、$1.50 估算保留额、30 分钟，不加预算、不自动重试，不从失败中私自续开第三臂。默认归组、前端、Idea、分类、Pull、最终判定和上层论点均不在本次工作范围。

- D158 运行结果：免费重放 326 个答案，事件年度修复仅恢复 NAVER 一条部署事件及三条证据；两个反向修改和完整 211 项测试通过。在线第一条对照请求 180.342 秒超时，无模型回答；其余五个序列未开始，$0.105535 未知用量保留额不释放。新入口尚无在线效果结论，不推广、不自动重发。结果：`poc/reports/2026-10-25-ohio-grouping-02/results.md`。

## D159 · 2026-10-25 · 从抽取到入库重放，先修读取顺序，单独检验身份所需来源

- Alex 要求重新看完整抽取、找已有观点、去重和归组流程，找结构性原因后修复，不做个案调参。诊断、表、固定案例与验证方案见 `docs/research/2026-10-25-pipeline-replay.md`。
- 八个 v15 库有 834 次日初预抽取，其中 576 次之前已有同日新观点；此数是上下文暴露，不是错误数。删除预抽取，让一条写完下一条再抽，恢复 D31/D63 的顺序要求。D155 中这一顺序修复不再等待分组语义试验；分组仍不因此启用。未完成的旧并行交接明确拒绝恢复，保留原数据，不静默重抽。
- Ohio 所查的既有问题均已搜到，不能统称数据库没召回。原拟用四个比对请求检验补充双方原句和来源，审查在调用前发现：165 的候选已变成年度实际出资，与旧担保金额不同；不能把合并算成功。该实验不运行，先把抽取改变含义与身份拆分分开评价。不换搜索、不增加专用合并规则、不改默认提示词。
- 每个案例每臂三次，最多 24 次请求、$1.50 估算保留额、30 分钟；与 D158 超时请求及其未知费用分开，不自动重发。原文审阅形成的开发预期不是人工金标，结果不充当完整分组验收。前端、Idea、分类、Pull、最终判定和上层论点均不在本次范围。
- 结果：顺序修复的 3 项入口测试、31 项相关测试、完整 214 项套件通过；恢复旧并行的反向修改被调用顺序断言抓住。身份试验的 24 次是草案上限，实际没有开始，生成费用为零。下一步先确认“同问题去重、同项目不同问题归组、原意改变归抽取”的验收界限，再固定最小实验；不得按被审查否决的预期启动。

## D160 · 2026-10-25 · 按原意检验三篇连续抽取，不用错误合并掩盖提问失真

- Alex 同意 D159 的界限并要求继续完整修复。以同一可核对问题判去重，以同一业务过程判归组；拟议担保改成当年实际付款属于抽取失真，不能强行合并算修复。
- 最小下一步见 `docs/research/2026-10-25-extraction-continuity.md`：三个真实 Ohio 输入、两臂各三次连续样本，两臂都沿用已有组成员上下文、身份与原子保存，仅改变实验角色的阅读入口。默认角色和归组仍不改变；本轮不声称验证大库检索。
- 独立登记最多 54 次请求（18 次抽取、最多 36 次比对），费用上限仍 $1.50，30 分钟。旧预算、超时记录和未知费用不动；不自动重试，不用失败样本改尺或续开臂。无关产品模块和上层投资论点仍不在范围内。

- D160 实测结果：六个序列全部完成，36 次调用，估算 $0.51142625。新入口三次均把两项融资问题分别保留且归在同组，但风险论据和三种金额口径完整保留均只有 2/3，与对照覆盖相同；完整验收失败，不推广、不自动续开臂。18 条成员、54 次出处交接全部对应；完整 216 项 Python 测试通过。后两篇没有新候选，不能声称检验了旧身份拆分问题。结果和剩余合同问题见 `poc/reports/2026-10-25-ohio-grouping-03/results.md`。

## D161 · 2026-10-25 · 继续修抽取，把保留论据与新开问题分开

- Alex 在 D160 失败后要求继续改进抽取和后续运行，为封存做准备。当前合同能够保存遗漏的风险论据；不采用前一轮提出但未获证的新证据存储层。
- 设计、计数、阅读机制和固定验证见 `docs/research/2026-10-25-extraction-evidence.md`。以 D160 角色为新鲜对照，仅重排并明确证据选择：关键条款及支持/反对理由可归入同一个问题，不因无需新开问题而丢掉。原问题边界、引用检查及存储保持。
- 六个独立三篇序列，每臂三次；原 O1–O6 不变，另报首篇总成本是否保留。最多 54 次请求、$1.50、30 分钟；不自动重试或超额。通过这个开发案例不等于全部抽取封存，也不启用默认归组。失败按原标准报告，不补采改尺。
- 实测失败：36 次调用、估算 $0.497585。新角色批评论据 3/3（对照 2/3），但首篇总成本只保留 1/3（对照 0/3），两臂各有一次把 Ohio 问题放进 Rubin 组。11 条成员及 66 次出处交接全部对应，说明错误已在原答，不是保存丢失。217 项测试通过。默认不变，抽取未封存；分两步读内容再建问题的建议尚未决定或实施。结果：`poc/reports/2026-10-25-extraction-evidence-01/results.md`。

## D162 · 2026-10-25 · 先验证分两步抽取的假设

- Alex 明确同意先测试 D161 的下一步假设。仅在隔离 POC 把抽取分为读取原文内容、组织问题及归属两个内部步骤；第二步须交代第一步每条内容的去向。最终仍交现有证据、候选观点及归属，不增加产品数据层。
- 注册设计见 `docs/research/2026-10-25-source-first.md`。对照为 D161 的证据优先角色，三篇原文、每臂三个独立新鲜序列，原语义标准保持；不同时改原文引用表示、模型或搜索。
- 最多 63 次请求，独立上限仍 $1.50、30 分钟；不自动重试、不调整旧预算。通过开发案例才谈后续验证，不直接启用默认管线或封存；失败报告，不自行改尺续开臂。

- D162 result: the registered comparison failed end to end. All six sequences completed, 45 calls, estimated $0.6928525. First-step cost selection improved, but invalid ownership, wrong grouping, a period-check merge override and an inaccurate numerical summary remain. No default promotion. 227 Python tests passed. Evidence: `poc/reports/2026-10-25-source-first-01/results.md`.

## D163 · 2026-10-25 · English for the maintained project

- Alex: “let’s also use this chance to convert everything into english from chinese.” English becomes the language for maintained prompts, generated explanations, UI text and current documentation. Original source quotations and historical records retain their original language and identity.
- The D162 experiment finishes under its original frozen requests. Language conversion is a separate change, not an unregistered experimental arm and not evidence that the extraction defects are fixed.
- Inventory exact schema values and their readers before conversion. Preserve the ability to read existing records; no in-place rewriting of historical databases, frozen prompts, raw answers or prior decisions. New decisions and reports are written in English.
- Alex additionally requires prompt translations to be well written and structured, with terminology matching the PRD and no drift. Audit complete requests against the glossary, schema and readers; use the actually adopted prompt versions, not later experimental filenames. Candidate English prompts remain inactive until compatibility checks are complete. Existing PRD/implementation gaps must be reported separately from translation corrections.
- Alex selected a fresh English library: “yes start an english library work. how was this lib constructed previously, and how should we do it noe”. Start from original sources and an empty, separately named ledger; preserve the old Chinese ledgers and their raw answers. Do not copy translated thesis rows or append English ingestion to the old library. The [build plan](research/2026-10-25-english/english-library.md) records the old construction, selected source population and staged verification. This selection does not promote D162, enable default grouping, or authorize a larger spending cap.

## D164 · 2026-10-25 · Claude builds the English library on Codex's plan; the watch list is a reference, not a gate

- Alex stopped the keyed-views line as Claude had built it overnight, on seeing that the per-object watch list decided what may open: "你这个做法难道不是非常的限死吗？永远都是一堆财务指标，真正的观点呢？", "你现在是写死一些一定需要关注的证据吧？", then "停了吧，codex 再重整呢". The code-owned key (identity: is this the same quantity?) stays; what is worth a thesis is the analyst-model's judgement (00-system: 候选观点是抽取交出去的、已有观点管不到的要紧事). Codex had already recorded the same correction as D155.
- Alex then handed the English library build (D163, [english-library.md](research/2026-10-25-english/english-library.md)) to Claude: "好那你按照codex 需求来重建，然后开始充分的测试，一定要仔细的看结果以及评量". The build log with one row per measured step, costs and mistakes is [build-log.md](research/2026-10-25-english/build-log.md).
- Implementation choices recorded there and settled by Claude: canonical English values live in `src/hivemind/vocabulary.py` and are applied where an answer or a stored record is read for comparison (`extraction.sift`, `matching.check`, `judging._record`, the service's tier counts, the UI adapter), never by rewriting rows; the prompt version is the one switch between the Chinese and English contracts (extraction v6, `matching-v2`, `judging-v3`, `idea-v11`; `poc/config/poc-v17.json`); the Chinese versions keep their request text byte for byte, including the universe's `legacy_name` theme names, so stored requests replay at no cost; `direction` is an enum in the English matching schema; a view's year is stored in one canonical spelling (a fiscal form becomes FY2027 or 2027 for a December year-end, a calendar form 2026, a bare year keeps its digits and is never reinterpreted) so that a waiting dependency joins its year; the half-year filter admits the same questions in both languages; successor orientation and the UI's score orientation read the rungs' numeric bounds first.
- The seed build runs on the 20 NVIDIA documents of 2026-02-25..07-23 with a $5 cap, then the week 2026-07-24..31 and August 1–15 on the same ledger, each stage read before the next; the API and UI are pointed at the English ledger only after that. Grouping stays out of the default pipeline (D149, D162 unchanged).

## D165 · 2026-10-25 · Research groups enter the default pipeline; a group is an ongoing matter, a company's own financial lines carry none

- Alex, on learning that the grouping research (D142–D150, D156–D162) had not reached the pipeline: "把我要做的grouping逻辑充分地scope in 做第一周管线的验证". Claude put the D149 contract in D147's final form into the default pipeline (`thesis_groups`, `thesis_group_members`, extraction v7 with `group_refs` and `new_groups`, the writer resolving local ids and storing memberships with the theses, matching deciding none), config `poc-v19`.
- The first grouped seed day showed the company-folder failure (eight NVDA financial theses in one "AI infrastructure demand" group) because every candidate had to cite a group. Alex chose the correction from the two offered ("看起来可以你深度思考计划之后改再跑"): a research group is one ongoing matter in the world that several questions track together (a product rollout and its deployments, a financing or acquisition deal, a policy process, an investment or demand cycle), usually across companies and themes; a company's own reported or guided financial lines (total or segment revenue, margins, expenses, tax rate, capex) belong to the company and carry no group unless the line itself tracks such a matter. Code guards it: a declared group is created only when a written thesis that tracks a matter cites it; the lines may join a group another thesis founded. This amends D149's "every proposed thesis carries structured membership" and 06-views' "every candidate needs nonempty references". Config `poc-v20` (`role-v8`).
- Validation is on real data, not the three-article experiments: the seed, then the week 2026-07-24..27 on `poc/data/english-groups2-2026-10-25/`, read group by group (Rubin shipment with its customer deployments; the OpenAI–NVIDIA financing and Ohio campus; the hyperscaler capex cycle; China chip export controls; PC and other companies' own lines outside those). Alex: stop and report as soon as the groups look wrong ("如果你跑了前几天就发现grouping 有问题或是实现出来的质量有问题就停止来和我说").
- Alex's standing note (same day): the pipeline is brute-force LLM prototyping on purpose; it must work and replicate stably before any cost, speed or throughput optimisation.

## D166 · 2026-10-25 · Group identity and membership by names, in code

- After the grouped seed and two week days (poc-v20) the model still declared a group of its own for each customer deployment (SK Telecom, NAVER) although the Rubin rollout group was shown, the research's recurring failure; the trace confirmed the request, schema and stored answers were right. Alex approved the code-owned alternative with a warning: "可以但是你要小心不要步上crazy bloat prompt 和overfitting prompt 的后尘，想清楚架构问题再下手快速小范围的验证".
- A research group carries aliases, the names the matter goes by (products, projects, programmes, parties; never a company's id, name or alias). The model's only new output is that alias list on a declared group (one schema field, `role-v9`). Code decides: a declaration whose names hit a stored group is that group and creates nothing; a thesis whose own focus, question or scope carries a group's name joins it (membership basis `alias:<name>`), next to the groups the model cited (basis `model`); a company's financial lines still cannot found a group. Matching is unchanged.
- Validation stays small: the seed and the first two week days on a fresh ledger (`poc/data/english-groups3-2026-10-25/`, poc-v21), read group by group before anything larger.

## D167 · 2026-10-25 · No hard-coded identity for aggregates; the judge gets the evidence, the vocabulary gets the missing measures, the writer owns replacement

- Alex, after the Jev benchmark showed three theses opened for one ~$700bn spending figure under three scope wordings: "我不要 hardcode 解法 it's premature optimization, not general root fix, you need to make sure then poc then measure result". Claude had proposed a named list of aggregate scopes and then a key rule "under a theme, same measure and period = one thesis"; the first is a list of what matters (the kind D154 rejected), the second fails the old checks (`test_a_model_written_scope_is_wording_not_identity`, D155) and the gold's own counter-example under one theme, measure and period: the $250bn guarantee and the $350bn chip financing are two quantities. Neither is built.
- Decided: identity over a model-written scope stays a judgement (D155). The judge is given the material the judgement needs, the candidate's own quotes and the target thesis's defining quotes, and its `same quantity or event` criterion says what the word means here: two estimates or figures of one quantity are one question. Code gates stay on typed fields only.
- The measure vocabulary gains `market_size` and `project_cost` from extraction version 10 (the week filed an accelerator TAM and a data-center project's cost as `spend_total`); version-gated so earlier requests stay byte-identical.
- The writer owns the replacement rule (06-views, the Replace row): a piece may replace one in force only with a stated day not earlier than the stored one's, a tier at least the stored one's (fact and party statement above third-party view above rumour), and, between two third-party views, the same party; otherwise it is stored as new. Found when Jev's `supersedes` let analysts' reactions retire reported facts (log rows 39–41); the rule applies to both matching engines.
- Measured as two arms on identical extraction (`poc-v23-llm`, `poc-v23`) over the seed, the week and August 1–15, per state (`scripts/benchmark_states.py`), with the retrieval stage quantified apart.

## D168 · 2026-10-25 · Four corrections found by the D167 measurement: one repeat rule, one replace definition, one succession rule, one missing answer

Found while measuring the two D167 arms (log rows 44–48); each is general, follows the PRD, and was measured on stored data or by re-sending stored requests before it entered the code.
- **A repeat may name the piece shown for the same evidence under another of its theses** (`matching.check`). 06-views step 6: a repeat adds a source and any new thesis link; the writer already resolves a piece to one stored identity for all its theses. The check required the target under the destination thesis and failed an item twice (9 of 17 such refusals over four ledgers were this case). A replacement still stays within its thesis.
- **The Jev replace criterion carries the PRD's full definition**: a later version of the same statement or number, changed (the same speaker revises it, an official confirms or denies that claim, the original source revises it); another statement on the same topic is not this (06-views lines 191, 197, 306). Probed against a fresh control, three samples: wrong replacements 10 of 10 removed on the seed and week, 6 of 7 out of sample on August; the right ones that stay are the guidance revisions and a source revising its own figure. A second wording ('the same party') was rejected by its pre-registered rule.
- **The writer's replacement rule, generalised from the PRD**: an incoming third-party view or rumour replaces only the same party's earlier piece (subsumes the view-over-view rule of D167). On every stored ledger it refuses 6 written replacements, all a commentator's view over another party's rumour, none right.
- **Succession**: the code's rule uses the shared typed-field rule (`identity.conflicts`: 'n/a' matches any basis or unit), so an unstated basis no longer blocks a succession (adds exactly 2 over all ledgers, both right); and the Jev relation question gains the answer 'the same defined quantity or event series for another period', with the direction, the typed fields and the successor check in code, so a succession between differently worded model scopes can be judged (probe: recovers the one such case, changes nothing gold-labelled for the worse).

## D169 · 2026-10-25 · Jev is the default matching engine

- Asked "要不要把 Jev 定为默认的匹配引擎" after the D167/D168 measurement (log rows 44–49), Alex answered: "要的。你的抽取，trace和当前抽好的db都很宝贵，这些都留下来然后开始做这个阶段的收尾".
- Decided: `poc-v23` (extraction v10, `matching.engine: "jev"`, model `jev-1.14.0`, with D168) is the default configuration of the replay (`scripts/replay.py`, which now also requires the ledger and archive it writes). The service's idea route keeps its adopted configuration `poc-v9` (D135/D145) on the sealed ledger and its search index; moving the service to the English library needs a new index and is a separate step. The generative matcher stays a configured alternative (`engine: "llm"`); old configurations and stored archives replay unchanged.
- The phase's extractions, traces and ledgers are kept (data manifest `docs/research/2026-10-25-english/data-manifest.md`, two backups outside the repository); the close-out is a code review for stale code and bloat, then the documents, then a push.
- Not decided here: moving group membership from extraction to matching (D149/D166), which the queued day-batch shape needs; it comes with that task.

## D170 · 2026-10-25 · Phase close-out: what the code review removed, fixed and left

Alex: "我们跑一个code review 清理一下过程中stale code 和 bloat 然后准备写好文档push". Two read-only Codex reviews (product code with its tests; tooling), each finding checked against the code before acting (log row 50). The full measured state is commit `f4ff787`; everything removed here is there.
- Removed: the retired research harness `poc/hierarchy_study/` (17 experiments and 15 test files, D146–D162, none adopted; its tests wrote three SQLite files to the repository root through a module-named path, also removed); five finished one-off scripts (`jev_poc.py`, `supersedes_probe.py`, `succession_probe.py`, `key_views.py`, `review_keyed_run.py`; results in the build log and `poc/reports/`); six product functions with no caller (`judging.judge_one`, `matching.same_orientation`, `Universe.canonical_scope`, `testdb.days_with_items`, `store.lineage_of_view`, `store.replaced_by`) and six unused constants.
- Fixed: the preflight's matching section now judges Jev records (it had skipped all 250 of the Jev ledger) and fails when every record of a ledger is skipped; the cost reports read the one price table (`model.PRICES`) and refuse an unpriced model; the benchmark stops when its evidence scorer fails; Jev succession eligibility has one rule (`jev_matching.can_succeed`); a test no longer reads the real credentials file, another no longer writes the real service archive; the newsroom category rule has one owner that its test exercises; the replay requires the ledger and archive it writes and defaults to `poc-v23` and the current item window; the compose file uses the adopted idea configuration `poc-v9`.
- Left, with the reason: the dependency-cycle pass in `matching.check` (its refusal wording reaches stored retry requests, so merging it would change replayed requests); the two ladder validators (admission of a new ladder and reading of a stored one are different jobs); splitting `matching.check`, `writing._write` and `idea.read_idea` (behaviour-preserving refactors of the core without a measurement round); unused parameters and result fields (signature churn across many call sites); the corpus harvesters' shared fetch code; the test-only `search.fake_embed` in the search module; `scripts/review_english_run.py` counting equal model-written scopes as a breach (D155 makes them a lead, not identity). The reviewers' lead that the API's `poc-v9` default was stale was wrong: it is the adopted idea configuration (D135/D145).

## D171 · 2026-10-25 · Review and free proofs for the day-batch acceleration proposal

- Alex asked to review the extraction/Jev/per-day acceleration plan deeply and test it against the stored golds and result databases. Scope is review and isolated offline proofs; no product-contract change, runtime adoption or paid comparison follows automatically.
- The [review](research/2026-10-25-day-batch-review/review.md) and its scripts reconstruct 960/960 extraction requests from the two saved v23 ledgers. Day-start context differs for 214/480 Jev-arm requests and 168/480 control requests; rechecking the same raw answers with day-start IDs loses 73/797 and 62/744 evidence items. Extraction depends on earlier theses as well as groups. The Jev arm has 86/320 final repeat/replace decisions targeting same-day evidence, and Jev membership alone cannot declare the 26 new groups.
- At 32 workers, a three-wave schedule using recorded Jev call durations projects 8.6× on July 27 and 3.2× over 31 nonempty days, before reconciliation/rate-limit overhead. This replaces the unsupported general 10× claim, not the speed target. It is a schedule estimate, not fresh measured latency. Judging already uses six workers per dependency level.
- Recommendation awaiting Alex's choice: concurrent request preparation with exact read validation before sequential commits, retaining D149/D159 semantics; re-run requests whose inputs changed. A more aggressive day-start extraction contract must be decided and tested separately. The review defines both boundaries, failure/recovery states, local-ID namespacing, evaluation limits and staged tests.
- Verification: 128 product/corpus/diagnostic tests passed; two diagnostic mutants were caught; preflight judged 250 stored Jev records with no skipped records. Existing golds remain unchanged. No batching runtime or fresh model-quality pass is claimed.
- A read-only review independently reproduced the 960 request message pairs and schemas, the stale-reference losses and the timing projection; no serious finding against the proposed contract. Runtime implementation and live measurement remain the next, separate steps.

## D172 · 2026-10-25 · Build the isolated ordered-concurrency POC

- Alex accepted the D171 recommendation: “yes be super careful about the logic ... do not fuck up the order ... flag it immediately”. Implement concurrent preparation with current-prefix validation and one ordered writer. Keep the default serial path and its tests unchanged. Group ownership and thesis/evidence semantics do not move.
- Speculative calls may precede earlier commits in the experimental path; accepted handovers and writes may not. Stale prepared requests are recomputed; earlier failure cancels pending work and drains running calls without accepting later results. This scheduling distinction is explicit, not an accidental weakening of D159.
- The [first implementation slice](research/2026-10-25-day-batch-review/implementation.md) covers offline coordinator, independent Jev calls and failure/restart verification on temporary storage. No paid call, new spending cap or default activation is authorized by this slice. The current per-item spend check is not safe reservation accounting for concurrent paid calls; resolve it before a live comparison.
- Offline slice result: [ordered-concurrency POC](../poc/reports/2026-10-25-concurrency-poc/results.md). Shared request identity prevents conflicting concurrent answers under one archive ID. Bounded Jev submission cancels pending work on failure; the daily cost log includes discarded speculative work. Default replay remains serial. 143 tests pass; five intended mutants fail; 3,595 historical request hashes are unchanged. Final focused review finds no serious issue. Live accounting, fresh controls and speed measurement remain outstanding; no paid ingestion calls were made.

## D173 · 2026-10-25 · Isolated provider smoke before a larger concurrency test

- Alex approved proceeding with a small test and required preserving the working database: “don't contaminate the current working db ... check the batch API usage correctly ... small scale test before moving forward”. All existing databases remain read-only; no merge or production activation is authorized.
- The [registered smoke](research/2026-10-25-api-smoke/plan.md) repeats two unchanged extraction requests and two unchanged Jev requests, with three fresh samples of two serial controls and one two-worker arm. Maximum 36 requests; conservative $1.50 reservation ceiling; no automatic retries. This is ordinary API concurrency, not OpenAI's asynchronous Batch API, and is not end-to-end or 10x acceptance.
- The isolated transport reserves money before dispatch, retains unknown usage after failures, and closes admission on any worker failure or cancellation. A synchronized dispatch decision separates work not yet committed to sending from in-flight work. The provider endpoints, pinned models, response shapes and price envelopes were checked against the official documentation. Existing prompts, product behavior, golds and default transports remain unchanged.
- Result: [36-request smoke](../poc/reports/2026-10-25-api-smoke/results.md) completed with valid responses, no retries, and all 122 pre-existing database files unchanged. Median two-request speed ratios were 1.08x extraction and 1.77x Jev. Fresh extraction varied between controls; one of 27 Jev categorical comparisons differed. This passes API integration, not semantic or 10x acceptance. A small end-to-end comparison remains next; no production promotion.

## D174 · 2026-10-25 · Three-document end-to-end concurrency diagnostic

- Alex asked to keep going. The [registered comparison](research/2026-10-25-ingestion-smoke/plan.md) uses the whole SK, NAVER and follow-up documents from July 24 against the ordered pre-July-24 baseline. It runs through the product's replay path on separate scratch ledgers, with fresh archives, three serial controls and three concurrent trials; the first control is read before the next trial. This is diagnostic, not production acceptance.
- The study shares at most two provider requests across all stages. It keeps the $1.50 total conservative ceiling and a 144-call ceiling, stops on failure, and does not alter production prompts, grouping rules, default transports or source/gold databases. Reservation now uses the existing request's actual output cap while retaining the full model input bound and conservative published rates.
- Before paid calls, the snapshot was corrected for this study to explicitly omit unordered sequence-zero audit rows; the source records are retained untouched. The audit rebuilds each accepted request from its committed prefix and rechecks that exact archived answer into the saved handover. Worker-side schema checks close admission before releasing a slot, including during daily judging. Free full-path controls and a substituted-handover mutant pass/fail as intended; 156 tests passed. Read-only design and code follow-up reviews found no serious issue.
- The first live serial control completed structurally but failed the NAVER-project check. The model expressed the 2028 expansion as capacity, which the numeric horizon refused; the older library expressed it as an event and accepted it. Evidence and its group disappeared with the candidate. The [result and census](../poc/reports/2026-10-25-ingestion-smoke/results.md) record the trace. No concurrent live trial followed; the journal is closed. Eligibility and the gold remain unchanged pending a product decision. This is not a concurrency acceptance failure or a measured speed regression.

## D175 · 2026-10-25 · Publish sequential cleanup separately from experiments

- Alex asked to commit and push fixes/cleanup that relate to the current sequential version. The pure request-construction cleanup was isolated in a separate worktree and pushed as `07aaff0` on `cleanup/sequential-requests`. It centralizes existing request and hash construction without changing payloads or processing behavior; all 3,595 archived request identities and 123 sequential product/corpus tests pass.
- The branch contains no concurrent runner, parallel matching, experimental transport or project-eligibility change. It is pushed, not merged into `main`. Experimental work remains local in the original worktree.

## D176 · 2026-10-25 · Judge business-question coverage, not mandatory project cards

- After the D174 result, Alex asked for the hedge-fund-analyst interpretation and then a systematic clean solution. The clarified criterion is whether material source information informs an appropriate, testable business question, retaining attribution and distinguishing plans from orders or realized revenue. A named project does not automatically require its own thesis or group.
- The earlier D174 mandatory-project-card interpretation is not itself sufficient to establish an extraction defect. Preserve that experiment and its original criterion; review evidence coverage, unsupported implications, wrong links and duplicate questions before changing the gold.
- The [admission proposal](research/2026-10-25-thesis-admission/proposal.md) identifies the numeric-card recipe and overloaded measure/horizon decision, and proposes a minimal instruction-only causal comparison before any new schema. This records the investigation scope, not approval of the proposed schema, a wider numeric horizon, a production prompt change or another paid run.

## D177 · 2026-10-25 · Modify and test NAVER admission on one frozen context

- Alex explicitly asked: “那你改了然后验证这一条啊”. The [NAVER-only test](research/2026-10-25-naver-admission/plan.md) changes the experimental T6 role to v11, retains the same category text, schema, model, horizon check, matching and writer, and compares three fresh controls with three fresh treatments. The original v23 configuration remains the default.
- The treatment removes mandatory numeric-card instructions, asks first for a material uncovered business question, and distinguishes an announced milestone's quantitative completion criterion from an annual forecast. It names no NAVER-specific facts. The system message shrinks by 172 characters; non-system request content is identical.
- Six isolated single-item rounds use the exact pre-NAVER state from the failed serial control, with a new $0.60/36-call ceiling and no network retries. Their scope ends after matching/writing; daily judging and wider extraction quality are not tested. The existing working databases remain read-only. No schema or general horizon-policy change is authorized by this experiment.

- Result: [six fresh samples](../poc/reports/2026-10-25-naver-admission/results.md) retained appropriate project coverage in 3/3 treatments versus 2/3 controls. The other control attached platform-use evidence to Rubin production instead; the two passing controls also proposed discarded annual-capacity questions. Treatment preserved plan attribution and the 200 MW / 2028 milestone without that extra question. Twelve physical requests used $0.009831 at Standard list prices and $0.031480 conservative accounting; all 124 protected databases were unchanged. This supports the candidate on this source only; the default remains v23, with no schema or horizon-policy change.
- Publication: the versioned prompt, T6-only test configuration and measured outputs are pushed on `fix/thesis-admission-v11` as `884866055cc265455bb72d25cd22e71db10e6558`, based on the sequential cleanup. The paid experiment harness and concurrency runtime remain isolated in the original worktree; no merge or default activation.

## D178 · 2026-10-25 · Resume the isolated acceleration POC with the tested T6 role

- Alex asked to push the change and return to the acceleration POC. The prompt candidate is already pushed as `8848660`; it remains inactive by default. The [resumed comparison](research/2026-10-25-ingestion-v11/plan.md) uses the identical `poc-v24-admission-test` configuration in both modes, the same three complete source items and ordered baseline, and fresh scratch ledgers and archives.
- Keep D174's two-request outbound limit, $1.50 conservative ceiling and 144-call maximum. No provider/model, production schema, horizon, grouping or writer changes. Add only an explicit study `--config` path whose path/content are frozen before any live call. The prior stopped journal is not resumed.
- Read each trial before the next. Apply D176/D177's material coverage, direct attachment and faithful status criterion, preserving D174's original result. A failed control, structural error, unsupported material assertion or duplicate counting stops the comparison. Six small trials can measure this workload, not establish general 10x acceleration or production readiness.

- Result: the first sequential control completed in 60.65 seconds and retained both project questions, but failed the direct-link criterion on three of six new links (NAVER future deployment to FY2027 revenue and 2026 Rubin shipments; SK partnership size to FY2027 revenue). The [trace and source review](../poc/reports/2026-10-25-ingestion-v11/results.md) locate the incorrect targets in raw extraction; matching only compares evidence identity inside those targets. The journal is halted before any concurrent trial. Twelve physical requests cost $0.007102 at Standard list prices ($0.020530 conservative accounting); all 138 protected databases remain unchanged. No speed comparison or new default is established.

- Attribution correction after Alex challenged the repeated blocker: the accepted v23 Jev ledger already carries three NAVER-source evidence links to the FY2027 revenue question (archived extraction call 687). The direct-link finding is not established as introduced by acceleration or v11. Reconcile existing baseline issues and fresh-sample variation with introduced regressions before proposing another extraction work order. The study remains halted and no acceptance criterion is changed here.

## D179 · 2026-10-25 · Roll back the unrelated extraction prerequisite

- Alex explicitly requested that the mistaken change be undone. Withdraw D178's use of an existing evidence-association issue as a requirement to repair extraction before continuing the acceleration POC. Restore D171/D172's comparison of sequential behavior with concurrent preparation; report existing semantic issues, sampler variation and introduced regressions separately. Keep the structural correctness requirements.
- No evidence-link repair had entered product code. Preserve the validated D177 NAVER prompt, the existing matcher/writer and source/gold databases. The historical plans, measurements and reviews remain; the [effective continuation](research/2026-10-25-ingestion-v11/resume.md) supersedes the withdrawn work order.
- The only runtime state restored is the assistant-set semantic `settings.halted` flag in the isolated study budget journal. A backup precedes the update; all 12 completed attempts, charges and the original limits are unchanged. No unknown-usage or technical-failure state is reopened. The next trial is concurrent-1; no paid request is part of this rollback.

- Continuation result: concurrent-1 completed in 43.03 seconds versus control-1 at 60.65 seconds. Both projects remain and structural checks pass; two stale preparations were recomputed. The single pair has different judgment workloads, so it is not an isolated speedup estimate. Concurrent-2 stopped on a TLS EOF before any new product record. One unknown-usage request retains its $0.517 reservation; no automatic retry or cap increase. The [continuation summary](../poc/reports/2026-10-25-ingestion-v11/continuation-summary.json) preserves all measured results. The next task remains acceleration measurement, not extraction modification.

## D180 · 2026-10-25 · Execute the existing implementation plan on the complete busy day

- Alex reiterated that the task is the parallel POC, instructed reading the existing implementation plan and told the assistant to complete it. Continue D172's implementation, not a source-first redesign or another extraction-quality work order.
- Use all 53 July 27 items in the preserved v23 Jev library. First build a current-code canonical response fixture, reusing exact archived requests and completing only missing current requests. Older stored Jev calls predate D168 criterion wording and cannot be claimed as exact current requests. Keep the original files read-only. Fixture completion is not a fresh latency control.
- Run the actual sequential and eight-worker coordinator over that full day with identical recorded responses and real scratch storage. Every accepted extraction must match a recorded request; unknown speculative responses cannot become authoritative. Compare all logical records and measure actual executor overlap. Synthetic timing is labelled synthetic, not model speed.
- Any additional live checks retain the original combined $1.50 and 144-attempt limits: the earlier unknown reservation remains held; allocate only the remainder to a separate journal. No provider, model, prompt, schema, grouping or identity change, and no cap increase.

- D180 result: [full-day proof and live matching measurement](../poc/reports/2026-10-25-full-day-parallel-r4/results.md). All 53 July 27 inputs complete in sequential and eight-worker recorded-response runs; 10 logical tables match, 106 handovers bind to exact requests/answers, and the deliberately altered nonempty handover is rejected. Ten stale preparations are recomputed. Separately, five identical Jev jobs across three serial and three parallel samples measure 3.959 versus 1.185 seconds median (3.340x), with five actual simultaneous provider calls. One near-threshold decision differs in two parallel samples; that variation is preserved. No whole-pipeline 10x or new semantic acceptance is claimed. 156 tests pass; all 138 protected databases remain unchanged. Combined use stays within the original 144-attempt/$1.50 cap, retaining unknown usage.

## D181 · 2026-10-26 · The parallel day, measured end to end on live APIs, and promoted as an opt-in replay mode

- Alex: "finish the entire POC of parallelization ... the results are correct compared to the golden that we ran sequentially and the speed up end-to-end is measured and benchmarked"; "我是要你真的implement 下去跑"; then "do code review, clean up the code and push the parallelized version and update all documentation". D180 left the whole-day live measurement open.
- Scheduling change inside D172: a waiting request that a commit changed is prepared again right after that commit, not at its turn; the turn still accepts only a byte-identical request. Recorded replay of the full day stays identical in all ten tables (ingestion chain 154 s → 95 s at recorded durations, 16 workers). Preparing the whole day ahead, ordered by item, left the chain unchanged and was not kept: the remaining waits are real dependencies between items.
- [Registered study](research/2026-10-26-e2e-parallel/plan.md) and [result](../poc/reports/2026-10-26-e2e-parallel/results.md): July 27, 53 items, three serial against three parallel live trials interleaved. Median 501.8 s → 112.5 s, **4.46× end to end**, 5.91× for item work; daily judging (~37–40 s, D63) is the same code in both. Every trial's audit is clean, the runner's accepted request equals the rebuilt exact-prefix request 53/53 in each parallel trial, and each trial's answers replayed through the other mode give an identical ledger (12 tables, ~1,000 rows). Drift from the recorded golden (29–30 of 53 items identical for parallel, 27–34 for serial) is inside the serial trials' own spread. Cost +24% at published rates for re-prepared requests ($0.086 against $0.070 a day).
- Budget: a new journal for this study, $4.00 conservative and 2,000 attempts, request-sized input bound, up to three attempts on failures without a reply with each failed attempt's reservation held; used $1.712 conservative, $0.467 published, plus $0.09 for one run of the product entry point. The D173–D180 journal and its held reservation were not reused.
- Promotion: the runner is `hivemind.parallel_day.ParallelDay`, opt-in through `scripts/replay.py --workers N [--jev-workers M]`; the serial path stays the default; worker counts are run arguments, not Config (D3). The product entry point ran the live day in 135.5 s, audit clean, cross-replay identical. The Jev client now retries a dropped connection like the OpenAI client (two such failures in one parallel trial); a final status is not retried.
- Code review (Codex, read-only): fixed the study's pass rule (a failed cross-replay audit now stops the study), a signal handler that could wait on the journal lock, duplicated handover binding (one check in `poc/concurrency_study/proof.py`, now also binding the runner's accepted request), and a schema-identity test that did not test the schema. Not changed, with the reason: a serial restart after a parallel failure resumes exactly as a serial restart after a serial failure (accepted handovers are serial-equivalent); the product cap counts archived calls, as the OpenAI client's retries already did. Superseded study harnesses (`ingestion`, `smoke`, `summarize`, `within_item`, `poc/naver_admission.py`) were removed; commit `6ed66ca` holds them as they ran.
- Limits: ten times end to end on this day would need daily judging and dependency chains to shrink, neither a scheduling change. The spend cap is checked per committed item, so in-flight early requests can pass it by at most the worker count's calls. Making parallel the default is Alex's choice.

## D182 · 2026-10-26 · The parallel day over fifteen consecutive days, against the serial path, with no network

- Asked after D181 whether the optimisation is "super solid": D181's evidence covered one day (July 27), so the parallel day had never run several days in a row, where a day's judging and its last commits feed the next day's first requests.
- The recorded August run predates D168 (its Jev requests lack one relation option and carry the older replace wording, and D168 changed matching and writing), so its answers cannot serve the current code for more than one item. [Study](../poc/reports/2026-10-26-multi-day-oracle/results.md) (`poc/concurrency_study/multi_day.py`, $0): the serial path and the parallel day (16 extraction, 8 Jev workers) each replay August 1–15 (221 items) from the July 31 ledger, every call answered by one deterministic oracle of the request bytes (the item's recorded extraction answer with each evidence line tagged by the request digest; Jev choices drawn from the digest; a valid judgement).
- Result: the two ledgers are identical in all 12 compared tables (3,418 rows; 1,458 written over the fifteen days), the parallel turns accepted exactly the serial run's 221 extraction requests, and 121 early requests were changed by an earlier commit and prepared again; a mutant without re-preparation and turn check was caught (11 of 12 tables differ). The same holds with answers served instantly.
- Speed, estimated at recorded call durations (not live): 2,512 s → 900 s over the fifteen days, **2.79×** end to end, 3.66× for item work; per day from 1.5× (4 items) to 4.5× (19 items). Small days gain little because their own dependency chain and judging dominate. The extraction requests rose 55% under the oracle (live July 27: +15% to +45%).
- A rerun of a day whose answers are all archived (July 27, no network, calls counted): the serial path sends no paid call and takes 0.2 s; the parallel day takes 1.3–1.4 s and sends the early requests the archive does not hold (8 on the serial trial's archive, 0 on a parallel trial's). Parallel pays only where the models are called afresh.
- Nothing in the code changed. Lean on the default, revised: keep the serial path the default, which reruns on saved answers free and fastest, and pass `--workers 16` to runs that call the models afresh (new days, or a changed prompt or configuration). Alex's choice.

## D183 · 2026-10-26 · The replay runs the parallel day by default

- Alex, after the comparison of the two modes (same ledger for the same answers; about 4× faster on a busy day of fresh calls; about 24% more cost; a rerun on saved answers free and fastest serially): "没事我们先都跑parallel, 这样可以快速的收敛。" This replaces D182's lean.
- `scripts/replay.py` now runs each day with `hivemind.parallel_day` unless told otherwise: `--workers` defaults to 16, `--jev-workers` to 8 when the configuration matches with Jev and to 1 for another matching engine (the parallel day refuses parallel matching outside Jev). `--workers 1` runs the serial path; it is needed to resume a day a serial run left unfinished, which the parallel day refuses without its manifest. Worker counts stay run arguments, not Config (D3); `replay.run` itself keeps `day_runner=None` as its serial path.
- Cost of the default, as measured: early requests a later commit changes are paid and discarded (+24% a busy day live), and a rerun on saved answers sends the early requests its archive lacks (0–8 on July 27) and takes about a second longer.
- Test: the entry point with its defaults runs the parallel day and writes the serial ledger; with `--workers 1` it runs serially (a mutant that asks a non-Jev matcher eight questions at a time is caught).
- Code review before the push ([request](research/2026-10-26-e2e-parallel/review-2-request.txt), [Codex, read-only](research/2026-10-26-e2e-parallel/review-2.txt); no correctness defect in request identity, commit order, matching order or thread ownership). Fixed, each with a test that failed first: (1) a restart under `--max-items-per-day` counted only the remaining items, so it dispatched an item beyond the day's limit (serial) or was refused by the manifest (parallel); the items an earlier run of the day wrote now count toward the limit. (2) The study and test comparison read 12 of the ledger's 20 tables; one comparison (`proof.ledger_rows`) now reads every product table without row ids, call ids and wall-clock times, and recomparing every stored pair found them identical (D180's recorded day, the 16-worker recorded run, the product-entry live run, the six D181 cross-replays, D182's fifteen days: 5,805 rows), the D182 mutant differing in 16 tables. (3) The entry point is tested with no arguments on the default Jev configuration (16 and 8 workers, serial ledger; a mutant default is caught). (4) A stale sentence in the current state. Found by Claude: a manifest left by another ledger in the same folder refused a fresh ledger that had written nothing of that day; such a manifest is now replaced, and a ledger that has written part of the day still refuses a changed contract.

## D184 · 2026-10-26 · A candidate thesis opens for one of four reasons, stated in the answer

- After the granularity research ([report](../reports/对冲基金论点粒度与金标.md); four notes in `research_notes/对冲基金论点粒度与金标/`): the ledger's 90 theses hold 25–32 at analyst granularity by two independent readings; the rest are financial lines, duplicates of one aggregate, customer deployments or unsettleable questions. The mechanism is one: the extractor's unit was "a sentence with a number and a period", not a disagreement; matching then rightly judged nine populations of one aggregate as nine quantities. Alex, on the clean version of option B (prompt plus schema-enforced fields, no dedup key): "可以".
- Decided: from extraction version 12 the default output for a statement is evidence to a shown thesis. A candidate opens only for one of four reasons, a closed schema enum `opens_as`: `main_driver` (an annual quantity that carries the company's value, whether or not the company guides it; first named `guidance_on_main_driver`, which the seed run showed excludes NVIDIA's data-center revenue because NVIDIA guides only quarterly), `industry_aggregate` (one aggregate quantity per calendar year; a later estimate or another population of it is evidence), `policy_stage` (a stage of a policy process with its authority named), `binding_obligation` (a guarantee, financing, equity stake or purchase commitment a universe company takes on). Every candidate also carries `settled_by` (the public material that resolves it), `folds_into` (the shown thesis it would otherwise attach to, or empty; the schema pattern is built from the shown ids) and `lost_if_folded` (the investment implication lost if it only attached there). Code checks shape (`extraction.check_admission`): blank text, an unshown `folds_into` and a binding obligation beyond its horizon are refused; the judgement of importance stays with the model (D154/D155). No key rule is added (log row 43 stands). Versions ≤ 11 are unchanged.
- The prompt `role-v12` replaces v11's "which questions to propose" with the four reasons and the three fields (7,357 characters / 1,482 o200k tokens against v11's 6,567 / 1,312: growth of 790 characters, the definitions of the three required fields and the four reasons; the recipe lines were already removed in v11, and the user message is unchanged). Configuration `poc-v25` = `poc-v23` with every category on v12. Measured against the extraction gold (D188) on the seed, week and August windows; results in `poc/reports/2026-10-26-admission-v12/`.
- Closes the open question "thesis granularity" of 05-extraction and 06-views: the research synthesis's "split when settled by different prints" and "2–4 per name" are not rules; the eight labeller rules of the report §1 are the standard, and a count is an outcome.
- Result ([results](../poc/reports/2026-10-26-admission-v12/results.md)): two false starts diagnosed on stored data ($0.08 together: a check that demanded a reason not to fold when there was nothing to fold into; reason 1 named as guidance, which excluded NVIDIA's data-center revenue), then one run over seed, week and August ($1.31 against the baseline's $1.01, the three fields and re-prepared requests). Theses 90 → 60, financial-line theses 29 → 3, evidence 534 → 710; gold full 3 → 9, partial 7 → 0, fail 10 → 11, every v12 failure a miss and none an extra. Remaining, counted: six theses for one 2026 aggregate, about seven small binding obligations, three proceedings opened as policy stages; eight candidates named a thesis in `folds_into` and opened anyway, six of them duplicates. A read-only code review's two wording findings on the role (a milestone on the main product under `main_driver`; the D185 exception beside the year limit) go to a v13 arm with the rule-2 wording for obligations and policy stages, Alex's call. Branch `feat/thesis-admission-v12`, not merged.

## D185 · 2026-10-26 · A binding obligation is due within 18 months and is exempt from the next-year rule

- Alex chose option B ("可以"): the current/next-year window keeps bounding quantities; a thesis on a binding obligation a universe company takes on (guarantee, financing, equity, purchase commitment) may set its own check day up to 18 months after the item (`extraction.BINDING_HORIZON_DAYS = 548`), because the signing can be checked long before the project it finances is built (Ohio: the guarantee in 2026, the campus in 2028). Due with no reliable material: "no data to verify", never a pass or a fail (AGENTS §8). Amends 06-views ladder rule 5 for this reason only.

## D186 · 2026-10-26 · Asset-thesis rungs describe business outcomes; the favourable end is registered per thesis

- Alex chose option C ("可以"): rungs of an asset thesis state the business outcome (above, near or below guidance), and each thesis registers which end is favourable for the company, as a theme thesis's dependants already state a direction. Reason: results and direction separate (NVDA beat four quarters and fell; capital spending can build capacity or hurt returns). Recorded; not implemented in this slice: it changes `check_ladder`, the writer, judging, the UI adapter and the Idea route (value × reader), so it is its own slice with its own measurement.

## D187 · 2026-10-26 · A company's own quantity sits under that company's object, private companies included

- Alex chose option C ("可以"): any company's own quantity is a thesis under that company (SpaceX's compute capacity under SpaceX, Alphabet's capital spending under GOOGL), consistent with 06-views rule 5 ("company figures use the fiscal year"); a macro theme opens only when a thesis depends on it. Recorded; not implemented in this slice: it needs a private-company object kind in the universe and the one switch (01-universe), its own slice. Until then the gold accepts the Codex reading (evidence to NVDA data-center revenue) for SpaceX.

## D188 · 2026-10-26 · The extraction gold: twenty cases labelled by the assistant this round, human review later

- Alex: "不是你要标吗？之后我们可以human in the loop, but this time in the beginning just use the research you just did"; "标20条". The gold `poc/eval/gold/extraction-admission-2026-10-26.json` holds 20 cases from the real items (the report §5's 15 plus five: CoreWeave managed-inference ARR, the four-company $745bn figure, the Bloomberg NAVER retelling, the Taiwan smuggling clause, the Goldman 2027 aggregate), each with the theses that must open (typed keys: object, measure, year, event type, scope pattern, with acceptable alternatives), the theses that must not open, the evidence links that must exist and the baseline's score. Scoring (`scripts/score_admission_gold.py`): fail when a must-open thesis or an evidence target is missing; partial when all are present but a must-not-open thesis was created; full otherwise; "not processed" when the run never saw the item. Labelled `assistant`; a human pass with two labellers and a reported agreement is the next protocol step, not this one.

## D189 · 2026-10-26 · poc-v25 is the replay default; the trace review names the next mechanisms

- Alex, after the measurement: "你可以取代，但是看所有的 trace 然后告诉我我们怎么持续做的更好接近 golden … We don't want to overfit … It needs to act exactly like a very senior hedge fund analyst". `scripts/replay.py` now defaults to `poc/config/poc-v25.json` (extraction v12, Jev matching); `poc-v23` stays as a configuration and replays unchanged.
- The [trace review](research/2026-10-26-thesis-admission-v12/trace-review.md) reads every thesis, every gold failure and the duplicate aggregates to their raw requests, answers and matching decisions, and names the root causes by design layer: thesis identity is a quantity where the analyst's unit is a question (six 2026 aggregates, each judged "new" correctly under the current criterion); the contract under-produces on first contact with a company (AMD 2 theses, MSFT 0); the role states categories where the labeller applies tests; theme candidates name no dependant; the extractor never sees the current view. Six general mechanisms are proposed with the class and count each moves, in the order: matching's "another estimate or population of the same question" option and theme dependants (code and schema, no prompt growth), then role v13 (tests instead of lists, the first-contact rule, quarterly statements as evidence; net shorter), then showing the view in block 5 as an A/B, then the daily duplicate check as pull-mode design. Each is Alex's call; none is built here.

## D190 · 2026-10-26 · The collision judge: Jev for identity, the generative model for the analyst's question when a question may be held twice

- Alex: "查重是用的 Jev 吗？… 你可以先单独跑这个，重新 review 一次 Jev 的提示词，然后优化他，不仅达到你的目的，也更贴近 hedge fund analyst 的大脑，你有黄金集做标准". Jev answers every candidate-to-thesis relation and every evidence comparison since D169.
- Review of Jev's relation criteria against the r3 ledger ([probe](../poc/reports/2026-10-26-admission-v12/jev-relation-probe/probe.md), 31 stored candidate calls whose list holds a thesis of the same object and measure, 18 labelled by the assistant): under the current options Jev calls a population variant of one aggregate `part_of` (0.4–0.9) and the code maps that to "new"; under an analyst's option set ("one question: the same outcome settles both; another estimate, population or proxy of one aggregate is the same question") it answers `distinct_question_same_matter` 0.5–0.9 on the same pairs. Both wordings: 8 of 18 right. Jev compares wording; it does not hold the decision. No change to Jev's criteria is made: the measured criteria stay (D167–D169).
- The generative model asked the same analyst question on the same 18 ([records](../poc/reports/2026-10-26-admission-v12/jev-relation-probe/llm-records.json), 3 samples each, $0.02): 11 of 18 right by majority, and 5 of the 6 aggregate duplicates merged; the misses are the debatable pairs (a reporting segment beside the business segment, the same deal under two names).
- Decided to build and run alone: `matching` keeps Jev; a configuration may add a `collision` setting (model, prompt `collision-v1`). When a candidate's list holds a thesis of its own object and measure, one generative call answers the analyst question for those theses and its verdict replaces Jev's on them (`jev_matching.collision_peers`, `ask_collision_judge`); every other relation stays Jev's. `poc-v26` = `poc-v25` plus the judge. Measured by one run over seed, week and August against the extraction gold and the census (ledger `english-v26-collision-r4-2026-10-26`); result appended here.
- General, not a list: the routing rule is a structural fact of the library (two theses of one object and quantity), and the question is the one a desk asks. The cost is one call per collision (31 of 69 candidates on r3), about $0.002 each.
- Result (run r4, `poc-v26`, seed + week + August, $1.33): 26 collision verdicts, 9 merges or successions, all on aggregate variants; 2026 aggregate theses 6 → 2 (v23: 11); theses 60 → 45; no merge removed a thesis the gold wants and A17 (the four-company figure as evidence to the five-company aggregate) turns full. The gold's overall score moved 9 → 4 full, and every lost case is an extraction difference between two fresh runs of the same v12 prompt (Rubin not opened from the call this time, the NAVER and META lines not extracted), not a matching decision. Recorded as the measurement rule for later arms: a matching change is judged on stored candidates and the duplicate census; an extraction change needs three fresh runs or pinned extraction answers; a one-run gold score carries about ±5 cases of sampler noise on this corpus. `poc-v25` stays the replay default until the judge is measured that way.
- Confirmation with extraction pinned (same recorded extraction answers in both arms, ids translated, Jev live, judging synthetic; `pinned_matching_study.py`): control reproduces r3 (60 theses, gold 9 full); the judge arm 56 theses, 2026 aggregates 6 → 3, evidence equal (711 vs 707 rows), gold 8 full with the one difference a repeat the scorer cannot see; 31 verdicts, 6 merges, $0.011; no required thesis lost. Alex: "有效果我们可以做". `poc-v26` becomes the replay default; `poc-v25` stays as a configuration. Open: the judge leaves 2 of 5 aggregate duplicates apart on one sample; a majority of three samples on collisions would cost three cents a run.

## D191 · 2026-10-26 · Theme theses reach every company; no named dependant is required to open one

- On the theme-dependency design (`docs/research/2026-10-26-theme-dependencies/design.md`), Alex decided the four points:
  1. A theme candidate does **not** have to name the company thesis it feeds. Alex: "我觉得这个非常难，有时候一个政策影响非常的广，你这种做法基本不可行，不可能所有的公司都 map 到，你可以默认这些宏观的东西和所有公司都有影响，我觉得这个 1 to all mapping 比较 make sense，至于这个 thesis 的 state 对每个不同公司的影响需要别的方法来判断". Decided: a theme thesis is context for every company thesis (one to all); how its state bears on each company is decided when that company's thesis is judged, not by an edge written at extraction. Explicit dependencies stay for the cases a document states (a company thesis on another thesis), and may be added to an existing thesis later (point 2).
  2. A dependency may be added to an existing thesis by a later item ("可以").
  3. From a macro-only item, a theme opens only when the theme is in the universe's list ("是"); an unlisted theme waits for a company item.
  4. `industry_aggregate` is renamed `shared_quantity`: a quantity or price outside any one company that several move on ("好").
- Consequences for the design, to be worked before any build: the judge of a company thesis reads the current state and reasons of the open theme theses of the themes its items were tagged with (block of the judging request), and states the sign it applies; a changed theme conclusion does not fan out to every company thesis in the same round (06-views: a repeated Fed statement must not trigger hundreds), it is read at each thesis's next judgement; proceedings that move no line are kept out by the admission test on themes (the model's judgement), not by a missing edge. The `feeds` field of the design is withdrawn for themes.

## D192 · 2026-10-26 · Role v13 (tests instead of lists) fails its probe; wording is exhausted as a lever

- Alex: "接着做下一步，不要 scope creep, just solve the core problems on improving quality for the extraction". Role v13 replaced the four category definitions and the ban list by the labeller's three tests (swing, independence, loss), added the first-contact rule (two to four questions for a company with no thesis shown) and named quarterly or run-rate statements as evidence; 7,580 characters against v12's 7,458.
- Probe ([role_probe.py](research/2026-10-26-thesis-admission-v12/role_probe.py), `poc/reports/2026-10-26-admission-v12/role-probe/`): the gold's 20 items re-sent with the stored v12 request's user message and v13's system prompt and schema, three samples each, sifted and scored at the candidate level against the gold's must-open and must-not-open keys; the stored v12 answers of two runs (r3, r4) are the controls. Must-open keys proposed: v12 9/15 and 8/15, v13 26/45 (8.7 per sample); must-not-open keys proposed: v12 0 and 1, v13 11/174 (3.7 per sample: a tax-rate thesis from the press release in two samples, a Taiwan proceeding in two, a run-rate thesis); candidates 30, 30, 33 per sample. $0.09.
- Read: the tests moved two cases the right way (the Helios milestone 3/3 against 1/3; the Ohio guarantee 2/3 against 0/2) and others the wrong way (the press release and the proceeding); coverage did not rise. The consistent misses (a numeric China-revenue thesis 0/5, Microsoft's capex 1/5, AMD's data-center FY2026 line) are judgements the model makes the same way under both wordings, not a reading of a list. Not adopted; `poc-v27` stays a configuration.
- A narrower v14 (role-v12 plus only the milestone clause the Helios gain came from, the D191 rename and the D185 exception, minus the peripherals sentence) is probed the same way; result appended here. Result: worse than v12 in the other direction: must-open keys proposed 14/45 (4.7 per sample against 9 and 8), candidates 17 per sample against 30; the February 25 call opened neither data-center revenue nor gross margin in any of three samples (two candidates each), while Helios rose to 2/3 and Ohio to 1/3. Twenty-five characters of wording moved coverage by half. Not adopted; `poc-v28` stays a configuration.
- Decided: role v12 stays. Two audited wordings moved the extractor in opposite directions on the same items; the extractor's behaviour is more sensitive to wording than to meaning, and a single sample at temperature 0.2 is the unit being measured. The levers that remain are structural, each Alex's call: (1) show the current view in block 5 so the swing test has an input; (2) sample the extraction three times and keep the candidates a majority proposes (identity by typed key), which turns the variance into a vote at three times the extraction cost (about +$1.7 over this window); (3) the first-contact pass as its own call on a company's first item. None is built here.
 Beyond that, the remaining lever for extraction is not wording: the extractor never sees the current view (05-extraction block 5 shows question, focus and due date only), which is the input the swing test needs (trace review §5).

## D193 · 2026-10-26 · Extraction coverage is at the model's steady state; the phase closes on v12 with the collision judge

- Alex: "太贵了抽 N 次 … 其他的点你自己深度思考啊 … 你深度的研究思考小范围尝试，给我结果让我清晰的做决策". Sampling several times per item is ruled out on cost.
- Two structural arms probed on the gold's 20 items with the stored v12 user messages, three samples each ($0.22): extraction at `reasoning_effort: medium` (configuration only) and block 5 carrying each shown thesis's current rung and last reasons. Neither moves coverage: 8.3 of 15 must-open keys per sample against 9 and 8 for the two stored v12 runs; medium reasoning proposes fewer candidates (25 against 30) at 1.8× the time; the view block adds a little clutter (1.7 against 0–1). With D192's v13 and v14, five arms give the same picture: the gold's must-open coverage is the model's steady state on these texts, about 8–9 of 15, and the six misses are the same judgements under every arm.
- Decided: extraction stays on v12 with the collision judge (`poc-v26`, D190). No further extraction arm is run without new information: a human pass on the six persistent misses (three of which the gold could accept as alternatives) decides whether they are the gold's or the model's; the next build is the D191 theme block in judging. Recorded probes: `poc/reports/2026-10-26-admission-v12/role-probe/`.

## D194 · 2026-10-26 · The six persistent misses read against the transcripts: one gold key removed, five stand

- Alex: "你自己看完是怎么归类评价的" … "好那你既然有判断了，那来改吧". The pass D193 left open was done by the assistant against the source texts and the stored candidates of every v12 run (r1–r4), not by a second labeller.
- The yardstick: does the text give a number or a date an analyst would track to a due day, and did the model open the same decision through another admission reason. Read that way:
  - **AMD data-center FY2026 (A14): the gold's.** The call gives no full-year 2026 data-center figure (only the Q3 guide, "server revenue more than 80% in the second half" and "data-center revenue more than double in 2027"); the model opens the 2027 line in every run. The key came from v23's `v53`, not from the transcript. Removed; the gold's must-open keys go from 15 to 14; resealed.
  - **NVDA China (A03): the model's, by authority, not by granularity.** The policy reading is already an accepted alternative, but every policy candidate the model wrote ("will the U.S. government allow H200 imports into China", r1 and r4) names the U.S. as the authority the text leaves open ("we do not know whether any imports will be allowed into China" after "approved by the U.S. government"). The gold's rule that the China key cannot match a U.S.-licence thesis stands; in r2 and r3 the model opened nothing on China.
  - **MSFT calendar-2026 capex (A13): the gold stands.** The call states the figure. The model links it as evidence to the five-company aggregate (r3) or opens FY2027 capex (r4); both are defensible, but a Microsoft page without its own capex question is the wrong product. Kept as must-open with the fiscal-year alternative.
  - **Helios first shipments (A14), Intelligent Cloud FY2027 (A13), CoreWeave FY2026 revenue (A12): the model's.** Each is a stated number or date ("initial shipments on track to begin later this quarter"; Intelligent Cloud guided to $40.95–41.25bn, Azure +45%; revenue guidance raised to $12.4–13.2bn). The three share one shape: the first call of a company in the window, where the model opened one or two theses and stopped. That is the first-contact pattern v13 tried (D192: +0.7 must-open, +3.7 must-not-open), so it is a known limit of v12, recorded here, not an open arm.
- Scores do not move: every reported ledger scores the same against the corrected gold (v23 3 full / 7 partial / 10 fail; r3 9/0/11; r4 4/0/16; pinned control 9/0/11, pinned arm 8/0/12), because A14 still fails on Helios. The probes' per-sample coverage in D192/D193 was counted on the 15-key gold; the removed key was proposed by no stored run, so the readings there are 8–9 of 14.
- Decided: the gold is corrected as above and stays assistant-labelled (D188's two-labeller pass remains Alex's); extraction stays closed on v12 with the collision judge (D193); the next build is the D191 theme block in judging.

## D195 · 2026-10-26 · The theme block: every asset thesis is judged with the open theme theses in view, and a changed theme conclusion reaches them in the same round

- Alex: "做，先零成本数完再改；然后你得确认这个架构和逻辑是对的", then on the one open choice "A 但是仔细思考怎么做才是正确的". Census and design: `docs/research/2026-10-26-theme-dependencies/design.md` §8 (`theme_block_census.py`; Codex read-only review, 12 findings, each read against the code, §8.8).
- What the ledgers said ($0): every company judgement would carry a block (175 of 175 in r4, 2–6 theme lines); the narrow reading by item tags shows a block in 14 of 175, so Alex's one-to-all rule is the only one with data; in 9 judgements the theme was judged after the company thesis in the same round; without propagation 109 of 228 theme changes are never read inside the window; with it, 141 more judgement calls, about $0.24 on the window.
- Decided (A): under `judging-v4` (`poc-v29`) an asset thesis's request carries `[Themes in force]`: every open theme thesis with a current state, its rung, the reasons of its last judgement and whether it changed since this thesis was last judged; the answer carries `theme_pushes` (view id, push in the evidence-push vocabulary), checked by code against the block and stored as `judgements.theme_pushes_json`, served as `theme_pushes`. Theme theses are judged before asset theses in a round; a theme judgement that says changed queues every open asset thesis with evidence in force, once per round, the rule explicit dependants follow (`changed` is the PRD's filter: a repeat does not fire it, a facts-only change does). The round's queue is derived from the ledger (the day's changed views, the dependants of views judged at this sequence number with a changed conclusion, the asset theses a changed theme queued), which also closes a hole the review found: a round interrupted after some judgements committed lost what they had queued. Everything is gated on the prompt version; v3 ledgers replay unchanged.
- This replaces the consequence note under D191 ("a changed theme conclusion does not fan out to every company thesis in the same round"): that sentence was the assistant's, and the census priced both sides. Explicit dependencies, D191 point 2 and the UI are unchanged. A theme conclusion is never evidence (06-views) and is never cited in `cites`.
- Three r4 asset theses re-judged once under v4 ($0.009, `poc/reports/2026-10-26-theme-block/resend-three.txt`): the signs read as an analyst would give them (hyperscaler capex toward the bullish end for NVIDIA data-center revenue, AMD data-center growth and TSMC revenue; the H200 permission toward it for NVIDIA; the overseas-computing restriction away; a tungsten-scrap allocation ignored by all three). One replay of the window under `poc-v29` (r5) measures it beside r4; adoption as the replay default waits for that measurement.

## D196 · 2026-10-27 · `poc-v29` (the theme block) is the replay default

- Measured once over the r4 window (`poc/reports/2026-10-26-theme-block/results.md`): 245 asset judgements carried the block, 194 named a theme push with signs that follow each thesis's own ladder; propagation added 121 judgements (+$0.20) and changed a conclusion one time in ten; reasons read the same or better on the five theses with the same question in both ledgers; one judge call in 307 ran out of output on the largest thesis and answered on resume. The whole run cost $1.46 against $1.21 with cached input at its published rate ($1.59 against $1.33 with every input token at the input rate; the cost column priced cached input at the full rate until 2026-10-27, build-log row 57).
- Decided: `scripts/replay.py` defaults to `poc/config/poc-v29.json`; `poc-v26` stays as the control configuration. Not built: the block on the UI; a tighter aggregate-theme identity (the near-duplicate aggregates each take a line in every block).

## D197 · 2026-10-27 · A shared quantity is one thesis per theme, measure and period; its wording is not identity

- Alex: "先把合计资本开支的重复主题题解决掉; 你小范围验证就好这个问题不要全部重跑，你能不能快速收敛".
- The class ($0, `docs/research/2026-10-27-shared-quantity/proof.py`): every AI-capex aggregate candidate of r3, r4 and r5 (9, 11, 11) against the theses that existed before it. r3 (no collision judge) opened six 2026 aggregates; r4 and r5, with the judge, each opened one duplicate: the judge read "Big Tech AI outlays" against "the top five's total capex" (r4 seq 351) and "the five named companies' capex" against "industrywide AI infrastructure spending" (r5 seq 200) as distinct questions in one matter, and later candidates then merged into the duplicate (r4: two). The contract already says what identity is: `industry_aggregate` is "one aggregate quantity for one calendar year … another population or another wording of the same aggregate is evidence to the shown aggregate thesis" (role-v12), and D155 puts identity in code where it is fully determined.
- Decided: a candidate admitted as `industry_aggregate` / `shared_quantity` with a quantity measure is keyed by (theme, measure, period) with no scope (`identity.automatic_key`); the writer records its key with `scope_source = 'shared'`; on the Jev path code decides its destination before any judge (`jev_matching.shared_quantity_target`): the open thesis of the same key is the same thesis (merge), the latest earlier period without a successor is its predecessor (succession), otherwise new. Policy stages and other events keep their event-typed identity; a company's own line (MSFT capex) is another object and never the aggregate; a theme quantity without the admission reason (the pre-D184 financing-amount case of T4) stays the model's. Tests: `tests/test_shared_quantity.py` (3, red first), suite 187.
- Proof on stored data: the rule flips every duplicate to a merge (r3: 5 merges + 1 succession; r4: 1; r5: 1), touches no other object, and changes no stored matching check (preflight C: 618 judged, 9 refused, as before). Small-scale validation (Alex: no full rerun): the r5 window replayed with extraction pinned to r5's answers and matching live (`docs/research/2026-10-27-shared-quantity/pinned_arm.py`, `poc/data/pinned-shared-2026-10-27/`): one 2026 aggregate thesis (v22, 33 evidence links; r5 had two theses with 40 links between them) and one 2027 successor (v29, succeeding v22); the rule decided 10 aggregate candidates (8 merges, 1 succession, 1 opened), the collision judge was asked 17 times about other peers, cost $0.21 (Jev) + $0.01 (judge).
- Codex read-only review of the branch's code (D195–D197, `scratchpad codex-code-review-d195-d197.out.md`), seven findings, each fixed with a failing test first: an unknown measure (`other`) is never a shared identity; two wordings of the next year's aggregate in one answer are one successor (coalesced by key, not refused as a second successor); a shared candidate's comparison list holds every thesis of its theme and measure, so a predecessor outside the search window is a valid target; the judgement's theme ids are checked against the block the request carried, not the ledger's state at check time; Jev is not asked a relation question about a shared candidate; a ledger written before the theme block gains the column at the write boundary (test that fails without the migration); one propagation rule (`queued_by_change`) serves live and resumed rounds. Suite 192.

## D198 · 2026-10-27 · A judgement reads the evidence in view, not everything in force

- Alex, 2026-10-27, on the finding that evidence in force grows without bound (v6, NVIDIA FY2027 Data Center revenue: 574 pieces after six weeks, 415 never cited by any of its 33 judgements; 40 of 316 judge requests over 30k tokens, max 67k; judging 38% of spend and rising; the run's stall came from enumerating 300+ ids): "这是什么问题你深度思考之后改".
- What the problem is (design: `docs/research/2026-10-27-evidence-in-view/design.md`): two mechanisms. (1) Extraction links wide: `role-v14.txt` says "every statement and number is, by default, evidence linked to a shown thesis" and also "link only to the thesis it directly concerns; omit statements with no thesis"; the model attaches every business mention to the broadest thesis (2.5 pieces per item on v6; a liquid-cooling note, a SuperPOD purchase, a rack R&D story). Not changed here; the prompt audit is reported to Alex as the next slice. (2) Judging-v4 reads everything in force every time ("Rejudge from all evidence currently in force"); an analyst keeps what his view rests on and reads what arrived.
- Decided: from judging-v5 (`poc-v30`) a judgement of a thesis is shown, of its evidence in force, the arrivals (pieces linked after the thesis's fifth most recent judgement, READINGS = 5; everything when it has fewer) and the basis (pieces cited by one of its last ten judgements, BASIS = 10). The rest stays in force in the ledger; the request names the count ("[Not shown: N more pieces in force, read in earlier judgements; the previous conclusion carries them]"); the answer may cite and push only shown ids, checked against the request that was sent (`judging.evidence_shown_in`, as the theme block is). Nothing leaves the ledger; the repeat / replace / new rules, "in force", the rejudgement triggers, eligibility, the theme block and dependencies are unchanged. Gated on the prompt version: v4 ledgers and configurations read in force as before.
- Measured ($0, `census.py`, two ledgers): among judgements after a thesis's first, the rule would have hidden 1.5% (nvda-3m) and 1.1% (r5) of the citations the judge actually made (22 of 325 and 7 of 261 judgements lose one cite, mostly third-party risk mentions listed in a "pull the other way" sentence); shown mean 95 and 109 pieces where in force averaged 225 and 178. Tighter rules hid 16% (cited last time + new since) or kept growing (ever cited + three readings). Arm beside control (`ab.py`, $0.03): v6, v11, v22 from the same ledger state, v4 fresh against v5: the same rung and `changed` on all three, reasons consistent, request tokens 76,476 → 12,516, 53,151 → 11,204, 25,806 → 8,425. Tests: `tests/test_evidence_in_view.py` (4, red first); suite 199.
- Applied to the three-month run at a day boundary: 2026-08-18 finished under `poc-v29` on the serial path (the parallel runner refuses a half-done day after a code change), `poc-v30` from 2026-08-19. Prompt `judging-v5` is `judging-v4` with the first rule reworded (2,264 → 2,437 characters; the growth is the sentence that says what is not shown and who carries it).
- Also in this slice, from the stall at 2026-08-07: a code-refused judgement answer is retired from the archive's lookup (`model.Archive.retire`; the row stays; schema-refused and malformed rows already carried a suffix), so a resume re-samples instead of replaying the refused answer; and the request's closing line names a closed set that exists ("cites_views must be empty: this thesis depends on no other thesis"; "a theme id goes only in theme_pushes, never in cites or cites_views"): 4 of the run's 5 retried first answers had put theme ids into cites_views.

## D199 · 2026-10-27 · One extraction call stays; its gate rule becomes decidable and the empty-answer exit goes (v16, poc-v32)

- Alex, on the instability trace: "不这个一次一定是可以搞过的 → 读明白，抽取 … 这一定是prompt 的问题，你如果再拆成两步这个消耗的luna calls 太多了"; then "你要反思自己的错误，然后下去改然后马上测试啊，不要一直diverge scope". The two-call design (`docs/research/2026-10-27-two-step-extraction/design.md`, two review rounds) is recorded and not built.
- Found ([log](research/2026-10-27-single-call/log.md)): the run's 493 empty extraction answers in 1,553 calls (32%; 65% of the first week's items) were the model following the written rules: "every statement is, by default, evidence" against "link only to the thesis it directly concerns … omit statements with no thesis", decided once per page, so a customer, partner or product page was omitted whole (asked directly, the model names that rule: a national lab buying Vera Rubin CPU servers "describes a customer project, not NVIDIA's reported sales"). The five-send benchmarks before this were sent with an alphabetised schema (the archive stores sorted keys; production sends the dict as built) and overstated the empties; in production order no send of three articles was empty. A second mistake stopped the first week test: code edited while the parallel runner was mid-day.
- Decided: extraction v16 (`role-v16.txt`: one rule, "a statement is evidence to each shown thesis whose answer its fact or figure makes more or less likely", with the customer/supplier/competitor/regulator and policy cases and the omit cases; the closing line "Return empty arrays only for a page with no business content", `extraction.EMPTY_LINE_FROM`; v12's admission reasons, `V12_REASON_VERSIONS`). `poc-v32.json` is the configuration. Measured on the same 98 items of 2026-07-01..07 against the paused run (v12, whole pages): empty handovers 65% → 32%, the model's own empties 55 → 8, evidence per item 1.1 → 2.7, candidates 9 → 11, week cost $0.22. v17 (`poc-v33`, an account per mandatory paragraph in the same call) held the piece set across sends (A3: Jaccard 0.6–0.8 against 0.4–0.5) but tripled the pieces with court-case minutiae and opened 5 theses where v16 opened 11, at twice the extraction and matching cost: refuted for production, kept as the record of the shape.
- The three-month run restarts from 2026-07-01 with poc-v32 on the cleaned database (D256) in `poc/data/english-v32-nvda-3m-2026-10-27/`; the poc-v29/v30 run stays paused and untouched. Open, named: links read widely (every piece to three or four theses; D198's "links wide"), candidates for product and gaming news (no thesis list entry fits them), the cold start's "no thesis fits" drops.

- Amendment, 2026-10-27 23:20: Alex stopped the restarted run ("我不是要你看下step 1抽取到底行不行？") and asked for the prompt to be read and fixed, with examples ("什么叫重要陈述，你也没给例子"). Arms B1–B6 ([log](research/2026-10-27-single-call/log.md) §10–17) rewrote the role as the model reads it: evidence first; four kinds of material statement with examples; a walk over the whole page ("a page with eight such statements yields eight evidence items"); a reject list with examples; links decided statement by statement; a rumour bears on a thesis as a confirmed statement does; T8's reading block narrowed to forecasts, ratings, targets and cited figures. Extraction v18 (`role-v18.txt`, `categories-v18.json`, `poc-v34.json`) supersedes v16 as the candidate configuration: on six articles sent five times each every material statement is present in every send; at scale (243 items of the run, one send each) 2% of answers are empty against 32% under v12 and 7–8 material statements come out per page, of which the theses that exist absorb 18% in the first week and 48% in the last. v17 and the two-call design stay refuted and unbuilt. The restarted run (`english-v32-nvda-3m-2026-10-27`, $0.215, 119 items) is paused; whether a run resumes, and with poc-v34, is Alex's call.

## D200 · 2026-10-27 · Extraction v18 (`poc-v34`) is the production default

- Alex, after the step 1 verdict (D199 amendment): "is step one and step two done? … whatever latest fixed version that you have, it just needs to be on production for these two. Do it, and then we move to step three and four."
- Decided: `poc/config/poc-v34.json` (extraction T*-v18; matching, collision judge and judging as `poc-v30`) is the replay default (`scripts/replay.py --config`, README). Evidence: the arms B3–B6 and the two extraction-only scale tests in the [log](research/2026-10-27-single-call/log.md) §12–17 (243 items, 4 empty answers against 32% under v12, 7–8 material statements per page), recounted from the scratch archive before this decision.
- Acceptance on the product's own path: one week (2026-07-01..07, NVDA, cleaned database) replayed through extraction, matching and judging with `poc-v34` in `poc/data/english-v34-nvda-week-2026-10-27/`, compared with the v16 week (`compare_week.py`). The result is appended to the log; a defect found there is diagnosed under §1 before any further change.
- Step 2 on the review page (the complete retrieval entry point of D250, main branch) is verified as a component and has no production consumer until step 3 (question selection) exists; nothing of it goes to production in this decision. The paused runs (`english-v29/v30`, `english-v32`) stay paused; whether a three-month run resumes with `poc-v34` is Alex's call.
- Found while switching the default, before the acceptance run: `extraction.ACCOUNT_FROM = 17` made v18 send v17's per-paragraph account shape in production, while arms B3–B6 and both scale tests were sent with the flat shape (`arm.py` restores the stored request and replaces only the role, the closing line and T8's reading block). The harness bytes were not the production bytes (AGENTS §5). Fixed at the owner: `ACCOUNT_VERSIONS = (17,)` and `extraction.accounts(version)`; test `test_v18_sends_the_flat_answer_shape…` (red on the old code, green after); the production `poc-v34` request now equals the scale test's bytes for all 243 items (system, schema keys and evidence item, user text from the item header). Suite 205 pass; preflight exit 0.

## D201 · 2026-10-27 · Steps 3 and 4: Jev gives opinions only, the library keeps sources and research arguments, a new question needs an independent investment judgement; gold first, small scope, root cause before any change

- Alex, to the three choices on the review page (`docs/research/2026-10-27-pipeline-review/index.html`, main branch): "我都同意但一样你的黄金标准要有然后自己下去改和量化测试，先小范围验证可行，深度解读错误的trace不要乱做test和乱改一定要知道问根因".
- Decided: (1) Jev's output is an opinion with a score (same statement / revision / different; direct result / business lead / background / unrelated / uncertain); whether a source is kept, merged or placed is decided by the analysis step that reads the complete old and new content. (2) The library keeps both the source records (immutable, for tracing) and the research argument each question carries, updated as a new version with what changed, its supporting and opposing sources, whether they are independent, and its limitations; the judgement reads the argument and its sources, not only the flat evidence list. (3) A new question opens only on an independent investment judgement with the full admission contract; a new product, a new figure or a narrower scope alone does not open one.
- Method, Alex's: a written gold before the first send (reference answers for every case, held-out cases included), one small scope (about 20 incoming records at their historical library state) measured against a fresh control of the current path, quantified per case; a failure is traced to its raw answer and its mechanism before any test or change; no tuning on the cases that were read.
- This decision changes the thesis-library PRD (06-views: the argument record and its writer/reader) and the matching PRD (Jev as opinion); the PRD text follows the measured build, not before it. No production change and no paid call in this decision itself.
- Acceptance result ([log §18](research/2026-10-27-single-call/log.md)): the v18 week through the whole path, 98 items, 361 calls, none failed, $0.22 (equal to the v16 week). The model left 4 answers empty against 8; 222 evidence rows against 213; 9 theses against 11, the two missing being v16's noise theses (Xeon 6 host CPU, Intel 18A wafers). Items that end with no evidence rise from 32% to 51% because v18 writes 506 statements with empty links where v16 stretched them to the nearest financial thesis, and the code drops them (D42); read on the eight largest items, every extra v16 piece was such a stretch. The one real loss is the cold start (the CNBC Kyber-delay statements of 07-05 dropped a day before the Kyber question opens) and 14 capex pieces pointing at theme theses the extraction request does not show: both on D199's open list, neither new. v18 is accepted and stays the default.
- Measured ([results](research/2026-10-27-stage34-gold/results.md), 2026-10-27 23:05–23:30, $0.24): the 24-case gold was written, then re-read as a hedge-fund analyst's standard (eight rules in `gold.md`, Alex: "做一个 hedge fund analyst 的专业视角去看怎么做这一步的标准"). One send per case of the new path (step 2 reader → Jev opinions → one gpt-6-luna call with the complete context): step 4 places and merges right on 20 of 21 development and 3 of 3 held-out cases, never retires a different statement; two misses (G09 the denial not written into the argument, G11 a bank's echo taken as independent). Jev's piece opinions are right on 7 of 18; the product's replace class has its mechanism in the `supersedes` criterion ("an official confirms or denies that reported claim"): re-sending the 47 stored replacements, 16 do not reproduce and 7 flip to a `contradicts` class once the clause is split out. Two harness contradictions of the assistant's (a check refusing what the prompt asked; the record's own id) were fixed at $0, and nine gold rows were corrected from verified ledger ids (the gold had been written from a ranked excerpt, not the complete expansion). No production change yet: the writer still acts on Jev's label.

## D202 · 2026-10-27 · The writer retires nothing on a matching label: a replacement is recorded as a revision and both pieces stay in force

- Alex, on the arm1 result and the proposal: "你接着做，需要非常严谨的看结果和测量". Census first ([labels](research/2026-10-27-stage34-gold/replacements-47-labels.json), every pair read): of the run's 47 retirements, 22 are the owner's later value or status of the same claim (right under rule E), 20 retired a statement that should have stayed (10 a contradiction or qualification, among them a denial erasing the delay report, "subject to final agreements" erasing the $500bn announcement; 10 a different matter), 5 were restatements mislabelled. Jev's `supersedes` label does not separate them: 17 of 22 right and 12 of 20 wrong carry it; with "confirms or denies" split out (`jev_contradicts.py`) 4 wrong ones flip to `contradicts` but so do 3 right ones. No label the matcher gives is safe to retire on.
- Decided: `writing` no longer calls `store.replace`. A `replace` decision stores the incoming piece, links it wherever the target is linked, and records the pair in a new `revisions` table (old, new, said day, seq); both pieces stay in force. `replacement_refused` becomes `revision_refused` with the same conditions (a stated day, a tier at least the old piece's, the same party for views and rumours): refused means stored as new without the relation, as before. The late-older-statement rule is unchanged. `replacements` is history: read by every present reader as before, never written again. `store.evidence_in_force` carries `revises` (the predecessor by revision) and judging prints "It revises eX (both in force)" so the judge sees the path; the library UI and service do not show revisions yet (open). The Jev criteria are unchanged: the split was measured and not adopted (3 false `contradicts` on right revisions against 4 catches).
- The decision word stays `replace` in matching records, schemas and the generative matcher's prompt; its meaning in the writer is "revises". Renaming it across prompts, records and scripts is a separate wording slice (D36).
- Not decided here: the step 4 analysis call in production (D201's reader of both texts), which would decide `same_as` / `revises` / `opposes` itself; until it exists the matcher's label is recorded as an opinion and nothing is lost to it.
- Regression week ([results](research/2026-10-27-stage34-gold/results.md), `english-v34b-nvda-week-2026-10-27`, $0.23, 98 items, none failed): the whole path runs with the revision rule; `replacements` gains no row. Counts differ from the v18 week (129 against 176 evidence rows, 12 against 9 theses) because extraction is a sampler, not because of the writer; the writer's effect is proved on the decisions themselves. Reading the week's one `replace` decision found a second silent loss in the same code path: an incoming statement said before its target was logged in `late_statements` and linked nowhere (both weeks dropped SemiAnalysis's Kyber delay report this way; the three-month run dropped the SharonAI backstop figure; 1 of 3,216 decisions, each a material statement). Fixed in the same slice: an older statement is stored and linked as one more piece, no revision recorded, the log row kept. Test red on the old writer, green after; suite 209. Observed, not fixed here: 34 of 1,530 stored pieces carry a non-ISO `original_day` ("2026-07-05 to 2026-07-06", "2026-03"), which is what made the Kyber report "older"; an extraction-contract item for the next pass.

## D203 · 2026-10-28 · A statement day is an ISO day or unknown; the writer never fills it with the publication day

- Found while reading D202's regression week: the extraction answer's `original_day` is a free string (54 of the three-month run's 2,369 raw pieces carry a month, a range or text; 1,445 are empty) and the writer filled every empty day with the item's publication day, against D245's rule that an unknown stays unknown. A range read as "older than" the denial it answered dropped SemiAnalysis's Kyber delay report from the week ledger.
- Decided, at the owners: `extraction.statement_day` keeps an ISO day and blanks anything else when the answer is sifted (the quote and `event_time` keep the period as written); `writing._store_piece` stores the stated day or '' and the revision path stores the stated day too (the ordering day `new_day` orders the revision only). Readers print the blank; matching's `said_day` still falls back to the publication day for ordering, never for storage. Tests: `test_a_statement_day_is_an_iso_day_or_unknown…` (red on the old sift), `test_an_unknown_statement_day_is_stored_unknown…` (red on the old writer); suite 211; preflight B/C/D unchanged.
- The judge's revision note is labelled as what it is: "Opinion, not verified: the matcher read it as a later version of eX; both are in force" (D202's census: 19 of 37 recorded revisions carry a wrong label).
- Census of the other silent loss in the same path, read pair by pair ([labels](research/2026-10-27-stage34-gold/repeats-40-labels.json)): of 40 sampled `repeat` decisions (1,034 in the run), 32 are pickups, 8 merged a different or richer statement into an old piece and lost its content (an estimated 200 of 1,034). The mechanism is D202's: a one-sample label triggers an irreversible write (a repeat adds a source and discards the incoming text). The fix is the argument record's reader side (store every source record, relate `same_as`, collapse same-claim groups for the judge); not built here.
- D201 measured further ([results](research/2026-10-27-stage34-gold/results.md), 2026-10-28 00:00–01:20, $0.85): a fresh 16-case gold written from the complete expansions before any send (action 11/12 and 4/4 held out; nothing wrongly retired 16/16; same-claim 8/12 with one class: a second outlet's own reporting treated as independent, which the contract could not express); arm 2 split claim identity from source independence (the class is gone; two new judgement weaknesses appeared); three draws per disagreeing case under both prompts show the arm-to-arm differences are within one draw's noise, while in 144 draws no must-not-touch piece was ever marked same or revised. Decided: the contract keeps arm 2's split; prompt arms stop here; the variable fields are annotations under D202 and the next build is the argument record (steps 5 and 6), where a wrong relation in one draw is corrected by the next instead of being frozen into the ledger.

## D204 · 2026-10-28 · A repeat is stored as its own source record; the merge becomes a labelled relation

- Alex: "补那个洞，跑一周验收，仔细思考很重要". The hole (D203's census): on a `repeat` decision the writer adds the incoming item as an outlet of the old piece and discards the incoming text; 8 of 40 sampled repeats (20%, about 200 of 1,034 in the run) had merged a different or richer statement, and its content was gone. The mechanism is D202's: a one-draw label (same_statement ≥ 0.5) triggers an irreversible write.
- Choice weighed. (A) Store the incoming piece, link it to its own destinations, record the pair in `same_claims`, show both to the judge with the relation labelled as the matcher's opinion. (B) Keep the merge and store the text as a variant of the old piece, hidden from the judge. Under (A) true pickups (about 80%) appear twice in view for their first readings, labelled; under (B) the 20% wrong merges stay hidden from the judge. The standard (rule A: an outlet, not a fact; rule C: support counts sources) is served by the label; losing content is the failure that is not recoverable at read time. Decided: (A).
- Decided: `writing` stores every incoming piece once with all its destination links; a `repeat` decision records (target, new, seq) in `same_claims`; the old piece gains no source row and no new link (the new piece carries the outlet and the links; a link written on a one-draw label is a write like any other). `store.evidence_in_force` carries `same_as` (the in-force pieces of its group); the judge's request prints "Opinion, not verified: the matcher read this as the same claim as eX; the argument counts one claim". Readers of `evidence`, `evidence_links` and `evidence_sources` keep their shapes; the library UI's per-row outlet count now counts one row's sources (the claim's outlets are its `same_claims` group), an open UI item.
- Acceptance: tests red on the old writer (`test_a_repeated_statement_is_stored_as_its_own_record…`, the two D167 tests whose assertions pinned the merge, changed with this decision), a mutant that merges again fails them; the 40 sampled repeat decisions replayed through the new writer at $0 (40/40 stored, relation recorded, the 8 lost contents present); then one week through the whole path (`english-v34c-nvda-week`), counting `same_claims` rows, pairs both in the judge's view, and judgements citing both members of a pair (the double-count exposure the label must hold).
- Accepted ([results](research/2026-10-27-stage34-gold/results.md)): 40 of 40 sampled repeat decisions replayed through the new writer keep the piece, the relation and both pieces in force (the 8 lost contents are present); the week through the whole path ran with none failed at $0.23, wrote 45 same-claim relations and no merge, and the judge's reasons where a pair was in view treat the relays as one source ("ultimately trace to SemiAnalysis", "not independent confirmation"). The three-month run may resume on `poc-v34` with D202–D204 in the writer; that is Alex's call.

## D205 · 2026-10-28 · The judging call's output budget is 16,000 tokens

- Found in the three-month resume (`english-v34-nvda-3m-2026-10-28`, 01:32): the judgement of v10 (Data Center revenue, a 24,150-token request) came back empty with `finish_reason` length: all 8,000 completion tokens were reasoning tokens, so the code read a malformed answer and the day halted (resumable; the re-send passed). Census over every archive: 2 of 793 judge answers hit the cap this way (the other in `english-v29-nvda-3m`, a 56k-token request), 13 of 793 used 6,000 or more. The archive books such a call at $0 while it costs its tokens (about $0.006 each).
- Alex: "嗯你加倍吧". Decided: `rejudging.max_output_tokens` 8,000 → 16,000 in `poc-v34.json`, nothing else changed; a normal judgement costs the same, only a long-reasoning one may spend more. Applied from day 2026-07-22 of the run (days 1–21 ran under 8,000; the archive records the configuration checksum per call).
- Also from this run: the Mac slept at about 02:00 and a Jev call failed with URLError during a dark wake; the run's `launch.sh` now wraps the run in `caffeinate -i -s`.


## D206 · 2026-10-28 · Every open theme thesis is shown to every item's extraction (extraction v19, `poc-v35`)

- Alex: "你可以改A然后尝试". The class ($0, `docs/research/2026-10-28-extraction-quality/report.md`): every one of the run's 1,414 extraction requests named the H200 key in its reference list while the H200 thesis (a theme) was never in the shown list; 48 pieces linked only to theme ids the groups block printed and the link check refused; three H200 theses opened for one matter.
- Decided: `store.views_for_prompt(themes=True)` lists every open theme thesis after the objects' own, in creation order; `extraction.shown_views` is the one owner of the shown list (the stream and the parallel runner both read it); the groups block prints only member ids the answer may link to. Gated on the prompt version (`THEMES_SHOWN_FROM = 19`): v18 requests are byte-for-byte as before.
- Measured: frozen gold (`gold-standard.md`, 26 articles, 26 statements, 11 core; `ab_gold.py`): control (production bytes, 26/26 identities archived) 9/11/7 kept right against the arm's 13/15/14 over three sends, core 6/6/5 → 9/8/8, written-dropped 13/12/13 → 8/7/8, extra flat; two weeks through the whole path (`english-v35-nvda-2w-2026-10-28`, $0.59): one H200 thesis instead of three, 14 pieces and 3 judgements on it, capex themes 7 pieces / 4–5 judgements each against 2 / 2, zero drops for an unshown id (17 in the control weeks). Tests `tests/test_theme_shown.py`.

## D207 · 2026-10-28 · Statements are filed by a separate placement call under the one-home rule; an unfiled statement is kept (extraction v20, `poc-v36`)

- Alex, on the root cause ("你还是没有根因的去解决这个问题 … 要么挂不到，要么挂多"; "跑那个归档实验"; "你看着结果来做"; "一样的标准开始测"). The mechanism ([routing-analysis.md](research/2026-10-28-extraction-quality/routing-analysis.md)): the in-call link decision was a coin flip (36% right on the gold, 46–78 pieces kept from the same bytes) and the gate at once (an unlinked statement was dropped: 60% of all statements, ~15–30% of them material); the link rule routed demand news to the company-wide quantities (six root theses held 66% of all links; v2's pieces 86% double-linked, 26% cited); the thesis list had no driver layer.
- Decided, three parts measured one at a time on the frozen gold (three draws each, 8 threads, $0.04–0.05 an arm) and on the first week's 255 in-call pieces: (1) `placement.py`: one call per item with the title line, the statements and the open questions, each with a code-written 'takes' line (key, event type, research-group names; aggregates admit other populations); the sift keeps statements without a link (`keep_unlinked`); the placer's links replace the extraction's, candidate links survive; a statement filed nowhere is stored in `unplaced_statements` with the handover. (2) The rule is the placement prompt: `placement-narrow-v1` — one home, the narrowest question; company-wide figure questions take only their own figures, guidance and management statements. (3) D42's "evidence is linked at extraction" becomes: the extraction's links are its first opinion; placement decides. Gated on the prompt version (`PLACEMENT_FROM = 20`); `cfg.placement` is required from v20.
- Measured: core statements filed right 6/6/5 → 9/9/9 (with six seeded driver questions shown) and 9/10/9 under the old rule; wrong links 9 → 3; links to the two sinks 63/60/44 → 6/1/5; junk placed 53/48/32 → 39/27/35; every decisive matter statement (the Kyber/Rubin Ultra rack delay cluster, the AI Compute Partnership participants, Goldman's capex estimate) placed; one week through the whole path (`english-v36-nvda-1w-2026-10-28`, $0.22 against $0.22) kept 580 statements the old path dropped. Arms retired by measurement: the extraction's links shown as a hint (junk and sink links returned), group aliases alone (the groups lack the press names). Tests `tests/test_placement.py`, suite 222.
- Not built here: re-placement of unplaced statements when a thesis opens later (the cold-start class, 12% of gold cells); the driver layer (D208).

## D208 · 2026-10-28 · The thesis tree: root quantities, a seeded driver layer per company, shared macro themes with declared channels (design, not built)

- Alex: "可以，但是不能因为有了这层我们的抽取就是非常的模版化缺少了hedge fund analyst 的灵魂"; on macro: "算是个global factor to all, 但影响正反面不一定". Measured before the decision (routing-analysis.md §11): with six analyst-seeded driver questions shown to the narrow placer, recall equals the old rule's (core 9/9/9), the sinks stay empty (6/1/5) and the neocloud, competitor-share and memory-cost statements land in their drivers (every landing read).
- Decided as design: (1) every company's library has the same skeleton — root quantities (its reported lines), a driver layer of seven fixed classes (demand, supply/inputs, competition/share, pricing/installed base, product cycle, policy, capital/obligations), and shared themes; the instances are the analyst's, written once at coverage start (the universe watch list completed), keys by code, each driver declaring the root it feeds through `dependencies`. (2) The template routes; it never gates: material statements are found as before, new questions open from articles as before, the judgement writes the argument. Two counts guard this: candidates outside the template must not fall; every driver's junk and citation share is counted like v2's. (3) Macro factors are shared theme theses judged once on their own (T11) evidence; direction per company is a declared dependency with a channel sentence the judge reads; macro evidence is filed only under the macro theme. Root judgements read driver and theme conclusions, not their evidence (the D195 theme block extended).
- To build, in this order, each with the same gold and a one-week whole-path run: bootstrap seeding with dependencies, the judge's "drivers in force" block, re-placement of unplaced statements; then the macro themes with channels.

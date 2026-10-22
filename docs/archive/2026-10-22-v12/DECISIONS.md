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
- Seals: v12 in `docs/archive/2026-10-22-v12/` with `SHA256SUMS`: the design after D54–D57 and the full sweep of D56.

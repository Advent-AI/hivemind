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

## D12 · 2026-10-16 · No current-day clock in the system

- By: Alex ("没有新的thesis 或日期为什么要硬推进").
- Decides: the system keeps no "current day" and no day markers. Each item carries its own publication day (New York,
  D9), and processing an item reads only that item; when no item arrives, nothing happens. How date-driven work
  (a prediction falling due, reading the research store as of a day without seeing later facts) is triggered is
  decided with the thesis design, not before. This drops D5's "T moves forward every day" and D10's day markers.
- Enforced: the receive and store nodes of `docs/system-design/new-design.js`; `TIME_RULES` of
  `docs/system-design/new-classification.js`.
- Seal note (2026-10-16): the receive node became dispatch's first two questions (D17).

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
- Sealed 2026-10-16: after a final check (simulation PASS; every node placed, every edge and code reference valid,
  every detail page renders; no stale wording on the page; decisions whose enforced place moved carry a seal note) and
  the plain-language rewrite of all page texts (wording only, rules unchanged), the design is copied to
  `docs/archive/2026-10-16-v1/` with `SHA256SUMS`. The archived simulation is a record: it reads the old ledger by a
  path relative to the live tree and runs only from `docs/system-design/`.

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

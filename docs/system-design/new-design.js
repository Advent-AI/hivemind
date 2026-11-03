// The new system design, built one piece at a time from the Old tab. Edit, save, refresh the page.
//
// nodes:   id → { title, kind, from, subtitle?, status?, draft?, purpose?, inputs?, outputs?, checks?, inspect?,
//          verified?, open?, refs? }
//          kind is one of control, external, model, code, mixed, store. `from` lists the Old node ids this node
//          carries over or replaces. `status` marks a frozen piece and puts a Frozen tag on it; `draft` marks a piece
//          not yet decided with Alex and puts a Earlier draft tag on it. Only the fields present are shown, so a node can
//          start as a title and its open questions.
// views:   [{ id, title, kind?, caption?, nodes: [[nodeId, column, row]], edges: [[from, to, label?, style?]] }]
//          style is '' (data), 'control' (control / feedback) or 'candidate' (local only). An edge written as an
//          object may also name a route (bottom, left, right, down). The inspection order is the node list's order
//          unless `order` is given; the canvas sizes itself.
// dropped: Old node id → why it does not come over.
//
// Every Old node is then carried over (named by a `from`), dropped, or not yet decided; the migration list shows which.
// The texts are for a reader who has not followed the discussion: plain words and an example, no field names; the
// decision behind each text is in docs/DECISIONS.md.
window.HIVEMIND_DESIGNS = window.HIVEMIND_DESIGNS || {};
window.HIVEMIND_DESIGNS.new = {
  id: 'new',
  title: 'New',
  heading: "New system design",
  summary: "This is the target design; every module has a PRD. Implementation gaps are in docs/poc/pipeline-plan.md. The system maintains a thesis library: create theses, update their judgement and close them when due. Upstream supplies classified items. Dispatch validates them, assigns sequence numbers and sends them to extraction. Extraction reads each whole item as a senior hedge-fund analyst, alongside existing theses, and returns sourced evidence, candidate theses and their research-group associations (D149). The library preserves those associations. Identity remains a search-then-match decision: merge a candidate, continue a previous period, open it or skip it; repeat, replace or add evidence. Each thesis has a question, ladder and due date. Evidence moves its state; dependencies connect conclusions and succession connects periods. Records are append-only. Matching records support human labelling and a future smaller model. Pull mode owns schedules and due dates; unresolved items go to human review. All modules except final verdict and pull mode are frozen; changes require a decision in docs/DECISIONS.md. The old system pulled dated batches and split reports into many numbers. The new system processes incoming items from the needs of a thesis.",
  repositoryRoot: '../',
  prd: 'docs/prd/00-system.md',
  prdTitle: "System overview",
  nodeHeight: 200,
  gridRowStep: 235,
  subtitleLines: 6,
  documents: [
    { label: "Working rules (AGENTS.md)", path: 'AGENTS.md' },
    { label: "Decisions (DECISIONS.md)", path: 'docs/DECISIONS.md' },
    { label: "Current state (CURRENT_STATE.md)", path: 'docs/CURRENT_STATE.md' },
  ],
  nodes: {
    classify: {
      title: "Classification (upstream)",
      prd: 'docs/prd/02-classification.md',
      subtitle: "Upstream labels each item with its classification result, text/table form and subjects. The result is usually one of 16 categories, or duplicate, not source material, or invalid. This module specifies those rules.",
      kind: 'external',
      status: "First version frozen · 2026-10-18",
      from: [],
      purpose: "Upstream labels each item before sending it: a category such as earnings, news or macro data (16 in total), or duplicate, not source material, or invalid; its text/table form; and its subjects. This module defines the rules upstream follows. We do not classify again; dispatch checks completeness and category validity.",
      inputs: "Original source material and its metadata: author, publication time, channel and subjects.",
      outputs: "A labelled item, or a duplicate to merge with the original, material to exclude (such as derived indicators we can calculate ourselves), or an invalid item with its reason.",
      checks: "Use rules and lookup tables, not a model. Classify the material itself: government and private macro data share a category. Use the publication day in New York. Do not guess missing lookup values: use the channel default for author type and send other unresolved values to human review.",
      inspect: [
        "Check metadata completeness: author, publication time and channel.",
        "Walk the rules and confirm exactly one classification result and, where applicable, one category.",
        "For invalid items, inspect the reason: missing metadata, unreadable text or unresolved lookup values.",
      ],
      verified: [
        "The simulation passed 412 real items from the old system and 161 hand-written examples. It still differs from current rules, including explicit replacement versions and conditionally required fields. See the known defects in CURRENT_STATE.",
        "Subject resolution passed 24 hand-written cases and agreed with the old system on 17 independently checkable records. Only companies were tested. Tickers still resolve by UTC date rather than New York publication day; cryptocurrency, commodity and theme cases are untested.",
        "Macro rules, including central-bank material, IMF forecasts and private statistics, were reasoned through individually but have not been tested.",
        "All 54 TrueNorth data interfaces can be assigned a category.",
      ],
      open: [
        "Upstream acquisition and labelling are deferred. Upstream also owns identifier-to-subject lookup tables.",
      ],
      refs: [
        { path: 'docs/system-design/new-classification.js', symbol: 'TAGS · TREE · INPUT_SCHEMA · LOOKUP_TABLES · RULES · OBJECT_RULES · TIME_RULES' },
        { path: 'docs/system-design/simulate_classification.py', symbol: 'classify · related_companies · CASES · COMPANY_CASES' },
      ],
    },
    dispatch: {
      title: "Dispatch",
      prd: 'docs/prd/04-dispatch.md',
      subtitle: "System entry point: is the item complete, has it been processed, and what is its classification? Return, skip, exclude, merge with the original, or send it to extraction with a sequence number.",
      kind: 'code',
      status: "First version frozen · 2026-10-18",
      from: [],
      purpose: "For each incoming item, ask in order: is it complete, has it been processed, and what is its classification? There is exactly one destination: return, skip, exclude, merge with the original, or extract. Extraction receives the category and sequence number. Sequence follows arrival order, not the computer clock; later steps use it too.",
      inputs: "Upstream items and previous processing records.",
      outputs: "Each item's destination. Missing or unresolved information also goes to the human review pool.",
      checks: "Return incomplete items as upstream problems. Skip a completed upstream ID without paying again; resume unfinished work from its recorded step. An updated version has its own ID and is processed normally. Do not filter by subject here. With no incoming item, do nothing.",
      inspect: [
        "For an unprocessed item, walk the three questions and locate where it stopped.",
      ],
      refs: [
        { path: 'docs/system-design/new-config.js', symbol: 'DISPATCH_TREE' },
      ],
    },
    extract: {
      title: "Extraction",
      prd: 'docs/prd/05-extraction.md',
      subtitle: "Read each whole item with its category prompt as a senior hedge-fund analyst. Return sourced evidence linked to existing theses and candidate theses with research-group associations.",
      kind: 'model',
      status: "Foundation frozen; D149 adds extraction-time grouping, not yet in the default pipeline; category prompts still need validation",
      from: [],
      purpose: "The only module that reads incoming information; it is read-only. Give the model the whole item, including embedded tables, or a whole table-data batch. Each category has its own prompt with the same structure. Block 5 contains open theses for the subjects and their dependencies, showing questions, focus, due dates and dependency links, plus available research groups. Return evidence supporting or weakening existing theses and candidate theses for important uncovered questions, with their initiating evidence; personal memos follow their prompt rule. Candidates carry associations under the library's grouping contract. Every item retains its source. Code checks the output; the library owns matching and storage. For example, NVIDIA's April 15, 2025 8-K opens complete candidates for China export licences and NVDA FY2026 China revenue. In July, NVIDIA's statement that the US assured licence approval can link directly to the existing licence thesis.",
      inputs: "The item, category and sequence number from dispatch; category settings from Config; existing subject theses and their dependencies with questions, focus, due dates and links; available research groups under the library contract.",
      outputs: "Sourced evidence linked to existing or candidate theses, and candidates with initiating evidence (personal memos may omit it). Candidates include group associations and any necessary new group definitions. Repeated processing failures go to human review.",
      checks: "A quotation or table cell must exist in the item; cited numbers must appear there. Evidence links must target shown theses or current candidates. Reject invalid output and record why. Check group references under the library's complete handoff contract.",
      inspect: [
        "Trace a thesis through its sources and use the upstream ID to retrieve the original from the team's library.",
      ],
      open: [
        "Validate each category prompt on stored items before settling its wording; record versions in Config.",
      ],
      refs: [
        { path: 'docs/system-design/new-facts.js', symbol: 'TEMPLATE · PROMPT_EXAMPLE · CATEGORY_READS · EXTRACT_STEPS · EXTRACT_TWO · EXTRACT_SORT_TREE · EXTRACT_RELATIONS · SOURCE_TREE · EXTRACT_EXAMPLE_TREE' },
      ],
    },
    views: {
      title: "Thesis library",
      prd: 'docs/prd/06-views.md',
      subtitle: "The system's core: each thesis has a question, ladder and due date. Evidence moves its state, which freezes when due. Search then match candidates against theses and evidence against evidence within its thesis. Preserve extraction's group associations.",
      status: "Foundation frozen; D149 adds group storage, not yet in the default pipeline; existing open questions remain",
      kind: 'store',
      from: [],
      purpose: "Create theses, update their judgement and close them here. A thesis's question, ladder and due date are immutable. Asset theses concern companies, cryptocurrencies or commodities and range from strongly bullish to strongly bearish. Theme theses name outcomes without judging them good or bad. A ladder usually has five rungs, or two for yes/no. The model judges the state from evidence still in force and dependency conclusions, giving reasons that code checks against records. Store evidence once with sources and tier; its push belongs to the link to a thesis. Dependencies read another thesis's conclusion: use the specified year for numeric theses and follow succession for event theses. Preserve extraction's group associations under this module's contract. Search the whole library for the top N candidate matches, then let the model merge into an open thesis (including a narrower part), continue a period, open a distinct question, or skip an overly broad question, a number beyond this or next year, the same period of a closed thesis, or an out-of-universe subject. New theses select dependencies. Search evidence within its thesis to identify repeats (another source), replacements (old evidence becomes history) or new evidence. Rejudge open theses when their inputs change under the rejudgement rule, dependencies first. For example, NVIDIA's filing opens licence and China-revenue theses; AMD's MI308 filing can merge into the licence thesis, while Reuters retelling NVIDIA's filing requires no rejudgement. Every match, judgement, succession and closure appends a record, preserving historical state. Pull mode freezes and closes the thesis at its current rung when due. These are Alex's recorded decisions; two remaining pull-mode proposals are listed separately.",
      inputs: "Extraction's sourced evidence, candidates, associations and new group definitions; Config's matching and rejudgement settings and search result count; due-date freezing from pull mode; human matching labels.",
      outputs: "Existing theses and available groups for extraction block 5; current states and frozen due-date states; matching records for labelling; proposed out-of-universe themes and repeated failures for human review.",
      checks: "Destinations must be shown IDs or evidence within the relevant thesis. Merge only into open theses. Check judgement reasons against records. Every judgement declares whether its conclusion changed; a first judgement or rung change must say yes. Dependencies must refer to shown theses or an explicitly awaited year on their chain, without cycles. Only one queue writes each thesis. Only incoming items create evidence; theses send notifications, not evidence. Append records without rewriting history. Store group associations against the final thesis under the grouping contract.",
      open: [
        "Search method and ranking: semantic, keyword or both. Initial result count is 10.",
        "Labelling details and checks for omitted or mislinked extraction evidence remain to be defined.",
        "Two proposals remain for pull-mode design; see the end of the detailed page.",
      ],
      refs: [
        { path: 'docs/system-design/new-facts.js', symbol: 'VIEW_TREE · VIEW_KINDS · LADDER_RULES · POSITIONS · TIERS · DEPENDENCY_TREE · CHAIN_RULES · INTAKE_SHAPE · INTAKE_STEPS · MATCH_OUTCOMES · EVIDENCE_OUTCOMES · LIFECYCLE_TREE · ORDER_RULES · VIEWS_PROPOSED · GROUP_RELATIONS' },
      ],
    },
    labels: {
      title: "Matching labels",
      prd: 'docs/prd/06-views.md',
      subtitle: "Record every match. Have people label a subset's correct destinations, then train a faster, smaller model when enough labels exist.",
      status: "First version frozen · 2026-10-20; details deferred",
      kind: 'mixed',
      from: [],
      purpose: "A general-purpose model initially matches candidates, chooses dependencies and classifies evidence as repeat, replacement or new. Record the input shown, raw answer, code-check result and final writes. Have people label code-refused cases and periodic random samples. Once enough labels exist, train a faster smaller model to take over matching. Details remain deferred.",
      inputs: "Library matching records and human labels.",
      outputs: "A future trained smaller model that takes over matching.",
      checks: "Record who made each decision: the large model, future smaller model or a person.",
      open: [
        "Define label owners, volume and interface; model evaluation and training use; and when the smaller model takes over.",
      ],
      refs: [
        { path: 'docs/system-design/new-facts.js', symbol: 'JUDGE_STEPS · TRACE_FIELDS' },
      ],
    },
    verdict: {
      title: "Final verdict",
      prd: 'docs/prd/07-final-verdict.md',
      subtitle: "Freeze and close a thesis when due. Whether a separate final-verdict step remains is deferred to pull-mode design. Below is the earlier draft: a complete model review before closure.",
      draft: "Earlier draft · Due-date freezing decided; remaining design deferred with pull mode (D41, D54)",
      kind: 'model',
      from: [],
      purpose: "Earlier draft (D29, before the library redesign): send possible closure to a model rather than letting one evidence item or condition decide. It reads the thesis, all evidence, current premises and trigger, then closes or keeps it. Only verification conditions plus factual evidence can establish confirmation or falsification; opinions and rumours cannot. At expiry without sufficient evidence, record “no data to verify”, neither success nor failure. For example, reported H20 licence issuance in August 2025 falsifies a tightening-controls theme; a dependent NVDA thesis is reviewed again and remains open because reported Chinese procurement restrictions still prevent revenue recovery, with a new premise.",
      inputs: "Earlier draft: triggered thesis, all evidence, premise states, trigger from code or pull mode, and final-verdict settings.",
      outputs: "Earlier draft: a new thesis version, closed with reasons or kept with revised premises or verification conditions. Closure triggers another review of each dependent thesis.",
      checks: "Earlier draft: cite evidence and sources for the decision; retain closed theses for historical lookup.",
      open: [
        "Requires redesign. Verification conditions, confirmation/falsification, premises, a seven-day fallback review and escalation on same-tier disagreement no longer apply after the library rebuild. Due-date freezing and closure are decided, without a separate result or extra wait. Whether this is a separate step remains for pull-mode design; retain its Config settings for now.",
      ],
      refs: [
        { path: 'docs/system-design/new-facts.js', symbol: 'VERDICT_TRIGGERS · VERDICT_TREE · VERDICT_RULES' },
      ],
    },
    pull: {
      title: "Pull mode",
      prd: 'docs/prd/08-pull-mode.md',
      subtitle: "The only time-driven module. Run at day-end or on a schedule to revisit and update theses; freeze and close those that are due.",
      draft: "Earlier draft · Scheduling and due-date freezing decided; other details deferred (D41, D54)",
      kind: 'mixed',
      from: [],
      purpose: "The incoming stream processes one item at a time and never reads the calendar. Pull mode owns time-driven work: revisit and update theses at day-end or on a schedule. Freeze due theses at their current rung and close them without a separate result. Decisive information enters normally as evidence; freezing does not wait for it. For example, NVDA FY2027 China earnings move its thesis to “down at least 80%”; day-end pull freezes that state and closes it. Dependencies read its closing state and reasons. Pass “now” into pull mode: real time in production, replay time in tests. Other behaviour is deferred; earlier verification-condition, fallback-review and driver merge/split proposals no longer apply.",
      inputs: "Library theses and their due dates; an externally supplied “now”.",
      outputs: "Freeze and close due theses. Write overall updates back to the library; their design is deferred.",
      open: [
        "Define the day-end/scheduled run and what an overall review and update does.",
        "Decide whether final verdict remains separate. Claude proposed putting it in pull mode; this is not approved. Retain final-verdict Config settings for now.",
        "Two proposals: handling unknown results and pending publication; daily duplicate checks. See the library detail page.",
        "Decide whether to fetch exact settlement data (prices, XBRL), from where, and whether it enters through dispatch.",
      ],
    },
    review: {
      title: "Human review pool",
      prd: 'docs/prd/09-review-pool.md',
      subtitle: "Hold unresolved items for people, such as unknown publication series, identifiers and out-of-universe themes. Handling after review is not yet designed.",
      kind: 'store',
      status: "First version frozen · 2026-10-18; intake defined, output deferred",
      from: [],
      purpose: "Do not guess when lookup tables or rules cannot resolve an item. Put it in the human review pool. Only intake is defined; what happens after review is deferred.",
      inputs: "New filing codes or datasets; unresolved author types; unregistered publication series; unresolved company, cryptocurrency, commodity or theme identifiers; proposed themes outside the universe found during matching; repeated processing failures; missing upstream information.",
      outputs: "Deferred.",
      checks: "Exclude resolvable companies, cryptocurrencies and commodities that are merely outside the universe. Samsung mentioned in Apple news is an example. Keep one record per issue with its occurrence count and examples.",
      open: [
        "How review updates lookup tables or the universe, and how changes take effect, is deferred.",
        "Notifications and review ownership are deferred.",
      ],
    },
    universe: {
      title: "Research universe",
      prd: 'docs/prd/01-universe.md',
      subtitle: "Subjects include over 500 US-listed companies, cryptocurrencies, commodities and macro themes. Each specifies tracked categories. Upstream supplies only this scope.",
      kind: 'control',
      status: "First version frozen · 2026-10-18; specific themes remain a draft",
      from: [],
      purpose: "Define subjects and tracked categories. Subjects include over 500 US-listed companies, cryptocurrencies, commodities and macro themes such as US inflation and US–China tariffs. Companies track financial reports, news and announcements; tariff themes track government notices. Upstream supplies only this scope and every supplied item is processed. This is the sole owner of what to process.",
      inputs: "A list maintained by people.",
      outputs: "A versioned universe with one row per subject and its tracked categories. Companies, cryptocurrencies and commodities have defaults; themes specify their own. All themes go to extraction block 3, where theme candidates select one.",
      checks: "Categories must come from the set of 16; each theme needs at least one. Unresolved subjects invalidate the version. Changes create a new version and upstream backfills relevant history. Rates, exchange rates and indices belong to themes, such as the US Treasury yield curve. Do not automatically add subjects: unresolved identifiers and out-of-universe themes go to human review; resolvable out-of-universe companies, cryptocurrencies and commodities do not.",
      open: [
        "The specific theme library remains a draft.",
        "Upstream delivery under the universe is deferred.",
        "Storage location and maintenance ownership remain open.",
      ],
      refs: [
        { path: 'docs/system-design/new-universe.js', symbol: 'OBJECT_KINDS · TRACKING_DEFAULTS · THEME_LIBRARY · TRACKING_EXAMPLES' },
      ],
    },
    config: {
      title: 'Config',
      prd: 'docs/prd/03-config.md',
      subtitle: "Human-selected settings only: extraction model and prompt per category, matching and rejudgement settings and search count, and final-verdict settings. Each change creates a new version.",
      kind: 'control',
      status: "First version frozen · 2026-10-18",
      from: ['config'],
      purpose: "Config owns human-selected settings: extraction model and prompt per category, separate matching and rejudgement settings, final-verdict settings and search count. Extraction owns category content and prompt assembly. Every change creates a new version; every model-call record identifies the version used.",
      inputs: "Set by a person.",
      outputs: "A configuration version used by extraction, the thesis library and final verdicts.",
      checks: "A reference to nonexistent model settings invalidates the entire version. Config does not set spending or concurrency limits.",
      refs: [
        { path: 'docs/system-design/new-config.js', symbol: 'CONFIG_SCHEMA · RULES' },
      ],
    },
  },
  views: [
    {
      id: 'system',
      title: "System overview",
      kind: "What passes between modules",
      caption: "Middle row: upstream → dispatch → read-only extraction → thesis library (search, match, write, rejudge). Matching labels sit on the right, collecting records for people and a future smaller model. Below: pull mode freezes due theses at day-end or on a schedule; human review holds unresolved items. The dashed upstream box is outside this system. Above: the research universe determines upstream scope and supplies themes to extraction. Config supplies settings to extraction, the library and final verdicts; only the extraction edge is drawn. Final verdict and pull mode remain earlier drafts to redesign together.",
      nodes: [['universe', 0, 0], ['config', 1, 0], ['classify', 0, 1], ['dispatch', 1, 1], ['extract', 2, 1], ['views', 3, 1], ['labels', 4, 1], ['review', 1, 2], ['verdict', 3, 2], ['pull', 4, 2]],
      order: ['classify', 'dispatch', 'extract', 'views', 'labels', 'verdict', 'pull', 'review', 'universe', 'config'],
      edges: [
        ['universe', 'classify', "Subjects and categories to supply", 'control'],
        { source: 'universe', target: 'extract', label: "All universe themes (prompt block 3)", style: 'control', route: 'down' },
        ['classify', 'dispatch', "Labelled items"],
        ['config', 'extract', "Model settings version", 'control'],
        ['dispatch', 'extract', "Categorised items with sequence numbers"],
        ['extract', 'views', "Extraction → library: sourced evidence, candidates with group associations and necessary new group definitions. Library → extraction: existing questions, focus, due dates, dependency links and available research groups (prompt block 5)."],
        ['views', 'labels', "Matching records and human labels for training the future smaller matching model"],
        ['pull', 'views', "Day-end or scheduled review and update; freeze due theses", 'control'],
        ['pull', 'verdict', "Decide with pull mode whether this remains separate", 'control'],
        ['dispatch', 'review', "Unresolved or invalid items"],
        { source: 'extract', target: 'review', label: "Repeated failures", route: 'bottom' },
        { source: 'views', target: 'review', label: "Proposed themes and repeated failures", route: 'down' },
      ],
    },
  ],
  dropped: {},
};

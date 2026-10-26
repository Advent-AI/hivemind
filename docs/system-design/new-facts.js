// The New design's extraction module, the views database and the final verdict (decisions D26-D45). Extraction reads
// every item whole, by its category, as a senior hedge fund analyst, with the open views of the item's objects and the
// views they depend on (prompt part 5), and hands over two things with their sources: evidence attached to one of those
// views or to a candidate view, and candidate views with extraction-owned subject memberships (D149). A view is a question with a
// ladder and a due date; the model matches each candidate to views found by search (the same view, its next period, or
// a new view) and each piece of evidence to the evidence its view already holds (repeat, replacement, or new evidence);
// evidence pushes the view's state, which is frozen at the due date (D54), and views are linked by dependencies and
// chained by succession. Only what Alex said or decided is written as decided (D45); Claude's proposals he has not
// decided are kept apart in VIEWS_PROPOSED. The final verdict is still the old draft and is to be redone with pull mode
// (D41, D54). Edit the data at the top; the three drill-downs render it. The texts are for a reader who did not follow
// the discussion: plain words and an example, no field names.
(function () {
  'use strict';

  // ------------------------------------------------------------------ extraction

  // The template prompt of the read step: the same parts for every category, in this order.
  const TEMPLATE = [
    { part: "Role", content: "You are a senior hedge-fund analyst. Read this item to test and form theses: link supporting or opposing statements and numbers as evidence to existing theses. For important questions not covered, return complete candidates with a question, ladder, due date, research-group association and initiating evidence. Judgements in the user's own memo become candidates, may lack evidence and are not themselves evidence. Each thesis concerns one thing. Its ladder has five rungs, or two for yes/no, with concrete, verifiable, non-overlapping and exhaustive outcomes, never vague “partial” outcomes. Set the due date when the issue can be resolved; for a number, use its publication date. Name the year. This year and next year are relative to the item's publication day; company numbers use its fiscal year.", source: "Shared by all categories; thesis rules come directly from the library" },
    { part: "What this category is and how to read it", content: "The category definition and reading method; for example, attribute opinions and estimates to their author rather than treating them as completed facts.", source: "Owned by classification; not redefined here" },
    { part: "Subjects", content: "The item's related subjects plus every theme in the research universe. Select an existing theme for a theme candidate when applicable; otherwise describe the new issue clearly.", source: "Item metadata; themes from the research universe" },
    { part: "What to extract from this category", content: "One row per category in the table below.", source: "Extraction module" },
    { part: "Existing theses and research groups", content: "Open theses for the item's subjects and their dependencies, with dependency links. Supply only question, focus and due date, not states or evidence. Also supply available research groups under the library's grouping contract.", source: "Thesis library" },
  ];

  // D149 requires extraction-owned membership; D147/D148 remain isolated implementations and measurements.
  const EXTRACT_RELATIONS = [
    "D149 requirement: while reading the full text, decide which continuing business process each candidate belongs to, called a research group. Rubin shipments and SK factory deployment retain separate questions while sharing the Rubin rollout group. Group during extraction, not in the frontend or a later whole-library clustering pass.",
    "Return evidence and candidates separately. Each candidate also carries structured associations; new groups have a name and scope. Mentioning a relationship only in prose is not a complete handoff. Extraction is read-only; the library's “Research groups: associate during extraction” section owns the full handoff and storage contract.",
    "Grouping remains a target requirement, not a default-pipeline handoff. D155 fixed reference-list vetoes, period/scope rewriting and same-batch duplicates; that does not prove grouping works. See docs/poc/grouping-improvement-plan.md for steps and measurements."
];

  const GROUP_RELATIONS = [
    "D149 requirement: organise theses by the continuing business process they discuss, called a research group. Vera Rubin readiness and customer deployment can share a group while shipment dates, SK factory launch and OpenAI deployment retain separate questions, ladders and due dates. A group may start with one thesis; a thesis may belong to several groups. A group has no state or ladder, creates no automatic dependency and is not an overarching investment thesis for an agent.",
    "Associate by business process, across companies and industries, not merely by company. A customer deployment explicitly using Rubin can join Rubin; NVIDIA PC chips cannot join just because they share a company. OpenAI deployment cannot join an SK-specific group merely because both involve Rubin. A group does not replace a research-universe theme.",
    "Before the full-text call, code supplies available group IDs, names and scopes. Search is not restricted by company. During that call, extraction references shown groups or declares new named and scoped groups. A candidate that tracks an ongoing matter (a product rollout and its deployments, a deal, a policy process, an investment or demand cycle) cites one or more groups, each shown or declared, without repeats; a company's own reported or guided financial lines (total or segment revenue, margins, expenses, tax rate, capex) belong to the company and cite none unless the line itself tracks such a matter (D165). Code validates the references before writing, and creates a declared group only when a written thesis that tracks a matter cites it, so a company's lines alone never found a group. Declare a new group if none fits; do not force an approximate fit.",
    "Matching still decides thesis/evidence identity and dependencies; it does not reread association fields to regroup. After creation, succession or merging, the writer resolves candidate IDs to final thesis IDs and local group IDs to stored group IDs, then stores membership. Candidates failing source checks or ultimately skipped do not become members. Do not create empty groups for unused declarations or reject other valid memberships because of them.",
    "Store each group/member pair once, with input ID and sequence number under the library's ordering and historical-read rules. Commit groups and memberships atomically with theses and evidence; roll all back on failure. Never mark a partial write complete. Redelivery must not duplicate membership; use existing dispatch and recovery.",
    "Groups do not copy evidence. Read sources through members' real evidence links, filtered by the requested sequence and excluding evidence already replaced at that point. No link means no evidence. A new member or an existing thesis change flag updates its groups. A repeated quote only adds a source and does not trigger an update. Evidence-only articles update existing memberships without inventing theses or groups.",
    "Acceptance measures source-supported membership and evidence retention, not identical names, IDs or group counts on every run. Report omissions, check refusals, missed associations and wrong associations separately. Preserve Rubin shipment/customer-deployment relationships and check wrong links to unrelated products or customer-specific groups. Multi-company and large-library behaviour is not yet validated.",
    "Implementation reference remains an isolated experiment: D147 supplies existing_subjects; threads declares id, name and scope; candidates[].thread_ids holds references. Local IDs are t plus a positive integer; stored IDs are g plus a positive integer. Prototype search uses title/full-text words against a global name/scope index, taking N from existing Config. These are prototype fields and search choices, not default-pipeline capabilities or evidence of large-library recall.",
    "See docs/poc/grouping-improvement-plan.md for gaps and steps. D148 member context and D150 reason-first output did not solve wrong grouping. D152's four name-selection responses to the third article created no candidates, so new membership was unexercised. Preserve all prior responses and results. Overarching thesis generation, MCP presentation and historical backfill are outside that implementation scope."
];

  // What each category should yield, and in which tier its evidence usually sits. The category's own definition and
  // reading rule come from the classification page and are not repeated here.
  const CATEGORY_READS = {
    T1: { read: "Actual figures, guidance and management explanations", tier: "Actual figures are facts; guidance and explanations are party statements" },
    T2: { read: "Actual and segment figures; risks and changes in risk factors and business descriptions", tier: "Figures are facts; described risks and changes are party statements" },
    T3: { read: "Transaction terms: price, consideration, closing conditions and timetable; parties' statements and demands", tier: "Terms are facts; statements are party statements" },
    T4: { read: "Management answers to key questions, changes in wording and analysts' follow-up concerns", tier: "Answers are party statements; analysts' questions are third-party views" },
    T5: { read: "Management's medium/long-term targets, capital-allocation framework and new-business scale", tier: "Party statement" },
    T6: { read: "Events such as executive changes, acquisitions, products and buybacks; published operating figures such as deliveries", tier: "Fact" },
    T7: { read: "What happened, when and who was involved; attribution and original sources", tier: "Official confirmation is fact; unnamed-source claims are rumours" },
    T8: { read: "The author's opinions, arguments, forecasts, ratings and targets, and changes to them", tier: "Third-party view" },
    T9: { read: "The speaker's account of orders, prices, share and inventory, and how they know", tier: "Third-party view" },
    T10: { read: "The decision/action, effective date and affected parties; subsequent appeals and deadlines that may set the due date", tier: "Fact" },
    T11: { read: "Published figures and policy decisions versus the previous release; changes in official wording", tier: "Figures and decisions are facts; wording is a party statement" },
    T12: { read: "Changes in prices and trading", tier: "Fact" },
    T13: { read: "Who buys, who sells and at what scale", tier: "Fact" },
    T14: { read: "Scheduled dates that can set due dates", tier: "Fact" },
    T15: { read: "Measured operating data as quantitative evidence", tier: "Fact; identify the third-party measurement" },
    T16: { read: "Not tracked by default", tier: '—' },
  };

  const CATEGORY_NOTE = "Read every whole file, including tables. A table release is one item and is read as a whole batch. Do not separately ingest XBRL facts already in the filing. Whether to fetch exact settlement numbers is deferred to pull-mode design.";

  // Every category has its own prompt: the same template with that category's parts. One assembled example.
  const PROMPT_EXAMPLE = {
    label: "T7 news prompt", note: "The same template, with news-specific blocks 2 and 4",
    children: [
      { answer: "1 Role", label: "Senior hedge-fund analyst", note: "Read to test and form theses. Link evidence to existing theses; for important uncovered questions, return complete candidates with question, ladder, due date and research-group association." },
      { answer: "2 How to read this category", label: "Media reporting", note: "From classification: opinion and analysis belong to T8; registered publication series use their category; remaining media material belongs here." },
      { answer: "3 Subjects", label: "Subjects of this report", note: "Filled by code, such as NVDA and AMD, plus all universe themes" },
      { answer: "4 What to extract", label: "What happened, when and who was involved; attribution and original sources", note: "Official confirmation is fact; unnamed-source claims are rumours" },
      { answer: "5 Existing theses and research groups", label: "Open theses for the report's subjects and their dependencies", note: "Filled by code with dependency links, questions, focus and due dates. For example, NVDA FY2027 China revenue versus FY2026 and its chip-export-licence dependency. Also include available research groups." },
    ],
  };

  const PROMPT_NOTES = [
    "Each category has its own prompt using the same template. Blocks 2 and 4 vary by category; block 1 is shared; code fills blocks 3 and 5 for the item.",
    "One prompt per tracked category T1–T15. T16 is not tracked by default; write its prompt when needed.",
    "For theme candidates, select from block 3 or describe a new issue if absent. For companies, cryptocurrencies and commodities, provide the relevant symbol or name. Code resolves reference data and accepts registered names only, as classification does.",
    "The user's own memo (T8 authored by the user) yields candidate judgements, not evidence. These candidates may have no evidence. Once opened, their state is “not yet judged” until evidence first links to them.",
    "Code defines and validates output fields for evidence, candidates and associations, necessary new groups and sources. Do not restate the shape in prompts.",
    "Test each category's prompt on stored items before settling its wording. Config records each version; a change creates a new version.",
  ];

  // Extraction, step by step: it only reads; matching and writing happen in the views database.
  const EXTRACT_STEPS = [
    { code: '1', name: "Build the prompt", who: "Code", does: "Use the category's content in the shared template. The library supplies block 5: open subject theses, their dependencies and existing groups needed for association." },
    { code: '2', name: "Read", who: "Model", does: "Read the whole item. Return evidence linked to block-5 theses or current candidates, and candidates for important uncovered questions with their initiating evidence. Personal memos follow their special rule. Decide each candidate's group association and return references under the library contract. Retain sources." },
    { code: '3', name: "Check sources and group references", who: "Code", does: "Check that the quote or cell exists in the item and that cited numbers appear there. Evidence must link to block-5 theses or current candidates. Reject source mismatches with reasons. Validate association references under the library's complete handoff contract." },
    { code: '4', name: "Hand off to the library", who: "Code", does: "Hand off evidence, candidates, associations and necessary group definitions with the sequence number. Matching decides identity; writing preserves membership." },
  ];

  // The two things one read hands over, side by side.
  const EXTRACT_TWO = [
    { aspect: "What it is", evidence: "A statement or number from the item: who said what or what happened", candidate: "A complete question to track: subject, question, ladder, due date and research-group association" },
    { aspect: "How common", evidence: "Present in almost every item", candidate: "Few: important questions uncovered by block 5; also all judgements from the user's memo" },
    { aspect: "Links", evidence: "One or more block-5 theses, or current candidates", candidate: "Carries initiating evidence; candidates from the user's memo may omit it" },
    { aspect: "In the library", evidence: "Compare against its thesis's existing evidence: repeat, replacement or new", candidate: "Decide existing identity or a part of it, succession, new thesis or skip. Preserve associations with the final thesis; matching does not regroup." },
    { aspect: "Example", evidence: "The 8-K statement that H20 exports to China require a licence", candidate: "What will the China export-licence regime for chips covered by the April 2025 rule be on April 15, 2026?" },
  ];

  // How the model sorts what it reads: against the open views in prompt part 5.
  const EXTRACT_SORT_TREE = {
    label: "Read a statement or number", question: "Which thesis does it concern?", note: "Judgements in the user's memo bypass this tree: all become candidates and may lack evidence",
    children: [
      { answer: "A thesis in block 5", label: "Evidence: link to that thesis", note: "Link only to the thesis directly discussed, not also to theses that depend on it", act: true },
      { answer: "Not in block 5, but important", label: "Candidate thesis with this statement as evidence", note: "Return its group association during extraction. The library later decides existing identity or new thesis. A thesis covers only up to its due date; events after that date belong here too.", act: true },
      { answer: "Neither", label: "Do not extract", note: "Background or boilerplate" },
    ],
  };

  // What one source records; every view, piece of evidence and change carries one.
  const SOURCE_TREE = {
    label: "A source reference",
    children: [
      { answer: "Which item", label: "Upstream ID", note: "Each version has its own ID; use it to retrieve the original from the team's library" },
      { answer: "Category and day", label: "Category and publication day" },
      { answer: "Where in the item", label: "Section, paragraph or table cell", note: "For table data, record dataset and record IDs" },
      { answer: "Which statement", label: "The original sentence or table cell", note: "Code verifies the quote exists in the item and the cited number appears there", act: true },
    ],
  };

  const SOURCE_NOTES = [
    "Every thesis, evidence item and information-triggered change retains sources. Each state change identifies its supporting evidence, plus dependency theses when their changes triggered rejudgement.",
    "Extraction checks quote/cell presence, number presence and links to block-5 theses or current candidates. Reject output failing any check. The library refuses sources absent from processing records. Both record reasons.",
    "Trace in both directions: thesis to all source items, and item to every thesis and evidence item it created or changed.",
    "Do not store the whole source item; retrieve it from the team's library by upstream ID. Store only the quoted sentence or cell supporting the thesis or evidence.",
    "Repeated statements of the same fact within one item, such as a number in text and a table, become one evidence item with multiple references.",
  ];

  const EXTRACT_EXAMPLE_TREE = {
    label: "What two items yield", note: "Illustration",
    children: [
      {
        answer: "NVIDIA 8-K, April 15, 2025", label: "Empty library; no theses in block 5", question: "Two candidate theses",
        note: "T6 other company publication: H20 exports to China require a licence; expected charges up to approximately $5.5 billion",
        children: [
          { answer: "Candidate: theme thesis", label: "What will China export licensing for chips covered by the April 2025 rule, including H20 and MI308, look like on April 15, 2026?", note: "Event thesis. Five rungs: full ban; licences required and none issued; licences issued with some conditions; all issued licences unconditional; no licence required. Due April 15, 2026. Quote: “…requires a license for export to China … of the Company’s H20 integrated circuits…”. NVIDIA discloses the licence requirement, classified as fact. The library opens thesis #1.", act: true },
          { answer: "Candidate: NVDA asset thesis", label: "How will NVDA FY2026 China revenue compare with FY2025?", note: "Numeric thesis. Five rungs: up at least 50%; up 10% to under 50%; change under 10% either way; down 10% to under 80%; down at least 80%. Due on the FY2026 annual earnings date. Quote: “…up to approximately $5.5 billion of charges…”. This is a company expectation, classified as a party statement. The library opens #2, dependent on #1.", act: true },
        ],
      },
      {
        answer: "NVIDIA statement, July 14, 2025", label: "Block 5 contains #2 and its dependency #1", question: "One evidence item, no candidate",
        children: [
          { answer: "Evidence", label: "Link to #1", note: "Party statement: NVIDIA says the US government assured it that H20 export licences to China will be granted (July 14, 2025)", act: true },
        ],
      },
    ],
  };

  const EXAMPLE_NOTE = "Each evidence item records upstream ID, paragraph and exact quotation. Code checks that “$5.5 billion” appears in the quoted sentence. The first item sees an empty library, so important questions become candidates. The second sees the licence thesis and links NVIDIA's statement directly. The library compares candidates with searched theses and evidence within its thesis. Both candidates join the chip-licensing-and-China-business group; the evidence-only second item updates existing membership. Grouping does not replace #2's dependency on #1. The NVDA example uses the same process as equities, futures and cryptocurrencies.";

  const EXTRACT_OPEN = [
    "Validate each category prompt on stored items before settling it; record its version in Config.",
  ];

  // ------------------------------------------------------------------ views database (D38–D45)

  // What the views database holds.
  const VIEW_TREE = {
    label: "Thesis library",
    children: [
      {
        answer: "Subject", label: "Companies, cryptocurrencies, commodities and themes in the universe",
        children: [
          {
            answer: "Thesis", label: "A question + a ladder + a due date", note: "Immutable once written. Five rungs, or two for yes/no. When matching opens a thesis, only one may be open for the same subject and focus at a time.",
            children: [
              { answer: "State", label: "The thesis's current ladder rung", note: "Evidence pushes towards either end; the model judges from facts. A thesis from the user's memo is not yet judged until evidence first links to it.", act: true },
              { answer: "Link", label: "Evidence", note: "Store evidence once with sources and tier. Its push belongs to the link. Replaced evidence remains in history and no longer counts.", act: true },
              { answer: "Dependency", label: "Another thesis", note: "Direction specifies which end of the other thesis is bullish for an asset thesis, or whether the two ladders have the same or opposite orientation for a theme thesis.", act: true },
              { answer: "Succession", label: "The previous period's thesis", note: "Successive periods of the same focus form a chain", act: true },
            ],
          },
        ],
      },
      { answer: "Research group", label: "Organise theses by a continuing business process", note: "Associate during extraction; full rules are in “Research groups: associate during extraction”" },
      { answer: "Append-only records", label: "Matching, rejudgement, succession, closure, reopening and labelling records", note: "Append at every step, without editing or deleting. Read records up to a historical date to recover its judgement." },
    ],
  };

  // The two kinds of view: the same structure, rungs that mean different things.
  const VIEW_KINDS = [
    { kind: "Asset thesis", on: "Tradable subjects: companies, cryptocurrencies and commodities", rungs: "Five rungs: strongly bullish, bullish, neutral, bearish, strongly bearish. Two for yes/no: bullish and bearish. These describe the business impact; set them at creation and keep them fixed.", example: "How will NVDA FY2027 China revenue compare with FY2026?" },
    { kind: "Theme thesis", on: "Macro, policy and industry themes", rungs: "Ordered outcomes from one end to the other: five rungs, or two for yes/no. Name outcomes without judging them good or bad. Dependent asset theses specify which outcome benefits them.", example: "How will the Fed's target-rate upper bound after its last 2026 meeting compare with now? (Large cut … large hike)" },
  ];

  const KIND_NOTE = "The same event can affect assets differently: rate cuts can be bullish for Ethereum and bearish for JPM net interest income. Theme theses therefore do not label outcomes good or bad.";

  // Two ladders, one of each kind (ranges are illustrative).
  const LADDER_EXAMPLES = {
    label: "Two kinds of ladder", note: "Illustrative ranges",
    children: [
      {
        answer: "Asset thesis: numeric", label: "NVDA FY2027 China revenue versus FY2026", question: "Five rungs describing NVDA's business impact",
        note: "Due on the FY2027 annual earnings date",
        children: [
          { answer: "Strongly bullish", label: "Up at least 50%" },
          { answer: "Bullish", label: "Up at least 10% but under 50%" },
          { answer: "Neutral", label: "Up or down by less than 10%" },
          { answer: "Bearish", label: "Down at least 10% but under 80%" },
          { answer: "Strongly bearish", label: "Down at least 80%", note: "At most one fifth remains" },
        ],
      },
      {
        answer: "Theme thesis: event", label: "China export licensing for chips covered by the April 2025 rule, including H20 and MI308, as of April 15, 2026",
        question: "Five ordered outcomes, without good/bad labels", note: "Use the rules in force on that date",
        children: [
          { answer: "Rung 1", label: "Full ban; licence applications no longer accepted" },
          { answer: "Rung 2", label: "Licences required; none issued" },
          { answer: "Rung 3", label: "Licences required and issued; some conditional" },
          { answer: "Rung 4", label: "Licences required and issued; all unconditional" },
          { answer: "Rung 5", label: "Licences no longer required" },
        ],
      },
    ],
  };

  const LADDER_RULES = [
    "A ladder has five rungs. Asset theses run from strongly bullish to strongly bearish, describing business impact; theme theses name five ordered outcomes without good/bad labels. Use two rungs for yes/no rather than forcing five: bullish/bearish for assets; named outcomes for themes, such as signed by the deadline/not signed.",
    "Each rung is verifiable: a numeric interval or event stage. Rungs must be exhaustive and non-overlapping, so exactly one applies at expiry. For example: up at least 50%; up 10% to under 50%; change under 10% either way; down 10% to under 80%; down at least 80%. Every boundary belongs to one rung. “Up a lot/a little” cannot be checked. Avoid vague partial outcomes; specify the partial state, such as conditional licences, as a distinct rung. State the comparison underlying neutral.",
    "One ladder concerns one thing. Separate numeric and event questions and connect them with dependencies. Likewise, separate components that can move in opposite directions, such as H20 and Blackwell chip classes.",
    "The extraction model writes the candidate's ladder. A new thesis adopts it unchanged until expiry. A merged candidate uses the existing thesis's ladder and due date.",
    "Numeric theses name a year. Non-company quantities use calendar years: the publication year is this year and the following year is next year, each ending December 31. Company quantities use the fiscal year containing publication day and its successor. Never use the computer clock. For a given quantity, open at most one thesis for each of this year and next year; do not open later years. The due date is the quantity's publication date.",
    "Set the due date when the debate can be resolved, usually 6–12 months away. Intermediate quarterly reports are evidence, not separate theses.",
  ];

  // The state on a ladder (D45: where it is now is a proposal, in VIEWS_PROPOSED).
  const POSITIONS = [
    { position: "State", means: "Our judgement of the thesis's current rung; evidence pushes toward either end", moves: "The model judges at low temperature from facts. Reconsider all evidence still in force, including each item's replaced predecessor to show the change, plus current dependency states and reasons and, for an asset thesis, the theme block. Do not increment or decrement the previous score. Cite evidence and compare with the conclusion before this round to state whether it changed. Do not rejudge if only source references were added and dependency conclusions did not change.", example: "After the 8-K: strongly bearish" },
  ];

  // How a judgement shows its sources and how code checks them (D46).
  const STATE_RULES = [
    "Every judgement states its basis in a fixed response shape: evidence IDs such as e12 and e15, plus dependency thesis IDs such as #1 when their changes triggered rejudgement.",
    "Code checks cited IDs against records: evidence must belong to this thesis and not be replaced; cited theses must be its dependencies. Accept only if all checks pass. Otherwise record the reason and ask for one corrected judgement. If that also fails, use normal failure handling: retry from this step, then human review after repeated failure. This checks references, not whether the judgement is correct, like verifying a cited page exists.",
    "Each judgement also declares whether the conclusion changed and explains why, comparing with the state and reasons before this round, including during retries. That earlier conclusion is for comparison, not incremental scoring. A rung change or a material change in the supporting facts/numbers counts: AMZN capex guidance moving from 12% to 25% growth changes the conclusion even within one rung. Repetition does not. A changed conclusion triggers dependent theses in the same round. Code requires changed=true for a first judgement or rung change; otherwise refuse under the same correction rules.",
    "For historical judgement, read the records saved on that date. Do not ask the model again; a new sample can differ.",
  ];

  const TIERS = [
    { tier: "Fact", examples: "Official actions, published figures and completed transactions", counts: "Can establish which rung holds and move the state" },
    { tier: "Party statement", examples: "Company guidance, management statements and official speeches", counts: "Can move the state only" },
    { tier: "Third-party view", examples: "Sell-side analysts, media analysis and experts", counts: "Can move the state only" },
    { tier: "Rumour", examples: "Unnamed-source claims and unattributed statements", counts: "Can move the state only" },
  ];

  const TIER_RULES = [
    "The model determines the size of the push and gives reasons. No tier has a fixed score.",
    "Count independent original sources. Twenty outlets retelling one exclusive are twenty references to one evidence item, not twenty independent confirmations.",
    "Tier follows who confirmed it. An unnamed-source report that Commerce is issuing licences is a rumour. An official or company confirmation is factual evidence replacing it. The rumour remains a rumour in history.",
    "Store evidence once without an intrinsic direction. Each rejudgement writes its push on the evidence–thesis link. One statement can affect multiple theses differently.",
  ];

  // How B reads A when B depends on A.
  const DEPENDENCY_TREE = {
    label: "B depends on A", question: "What kind of thesis is A?", note: "For an asset thesis B, state which end of A is bullish for B. For a theme thesis B, state whether their ladders have the same or opposite orientation.",
    children: [
      {
        answer: "Numeric thesis", label: "Read the specified year's thesis", note: "Example: JPM 2027 net interest income → Fed year-end 2027 rate",
        children: [
          { answer: "A is open", label: "Read A's state and reasons", act: true },
          { answer: "A is closed", label: "Read A's closing state and reasons", note: "The frozen outcome is what B needs; keep reading it", act: true },
          { answer: "A does not exist yet", label: "Wait for it", note: "Record the awaited year on the chain containing the shown thesis. When that year's successor is created, bind the dependency and rejudge B once." },
        ],
      },
      {
        answer: "Event thesis", label: "Follow succession", note: "Example: NVDA FY2027 China revenue → chip export licensing to China",
        children: [
          { answer: "A is open", label: "Read A's state and reasons", act: true },
          { answer: "A is closed with a successor", label: "Read the successor", note: "Record the change. The successor changes B's input, so rejudge B once.", act: true },
          { answer: "A is closed without a successor", label: "Read A's closing state and reasons, marked “historical only”" },
        ],
      },
    ],
  };

  const DEPENDENCY_RULES = [
    "Theme theses do not judge outcomes as good or bad. Each dependent asset thesis records its direction: rate cuts are bullish for Ethereum and bearish for JPM.",
    "A dependency has one direction. An apparent “good first, bad later” relationship needs an intermediate thesis: steel tariffs raising domestic steel prices and weakening downstream steel demand are separate paths.",
    "Dependencies and the theme block are the two ways theses influence each other; succession only orders periods. B depending on A means B reads A's conclusion. The theme block (D191, D195) shows every open, judged theme thesis to every asset thesis's judgement, one to all, and the judgement states which way each theme it weighed pushes it; no edge is written for it. Keep B's direct evidence separate from dependency states and reasons. A's conclusion can affect B like evidence but is not stored as evidence: external events and statements are evidence, whereas A is our own judgement. Treating it as evidence would let the system convince itself.",
    "Count a statement once. A statement about A is A's evidence, including when two candidates arise from one item. B learns it through A's conclusion. Only statements directly about B are B's evidence. If B does not depend on A, the statement may also directly evidence B. Choose dependencies only when B is created.",
    "Rejudge an open thesis when its inputs change: new evidence, replacement, a new link to existing evidence, a dependency declaring a changed conclusion, or (for an asset thesis) a theme thesis declaring one. Additional source references alone do not count. Binding an awaited A or moving to its successor also changes B's inputs. Closed theses do not update. A memo-derived thesis is first judged when evidence first links to it; before that, it and its dependants see “not yet judged”.",
    "The matching model chooses dependencies when opening a thesis, stating which conclusions it relies on and each direction. Choose only among searched theses, extraction block-5 theses and candidates opened from the same item; no extra search. Completed events are evidence, not dependencies: today's oil price influencing OPEC output is evidence for the OPEC-output thesis.",
    "Before adding an edge or following it to a successor, code checks for cycles. Refuse a cycle and ask the model to correct it; persistent cycles follow normal failure handling. Apparently mutually dependent questions indicate poorly defined theses.",
  ];

  // Succession: the same thing, period after period.
  const CHAIN_RULES = [
    "Successive periods of the same focus form a chain, such as Fed year-end 2026 rate → 2027 rate → 2028 rate. The chain records period order. Dependency traversal follows the rules above.",
    "One thesis has at most one successor: FY2026 cannot produce two FY2027 successors.",
    "Keep ladder orientation across succession: a strongly bullish first rung remains strongly bullish, although thresholds can change. Dependencies retain their direction; reversing the ends would break it.",
  ];

  // Writing what extraction hands over, one item per round: candidate views first, then evidence.
  const INTAKE_STEPS = [
    { code: '1', name: "Check sources", who: "Code", does: "Reject sources absent from processing records and record the reason" },
    { code: '2', name: "Receive evidence", who: "Code", does: "Retries do not duplicate evidence. A revised input updates only its own source reference. A revised retelling does not alter the original evidence. If the revision is from the original source, compare its statements normally and replace changed statements." },
    { code: '3', name: "Search", who: "Code", does: "Use a search engine such as Elasticsearch; semantic versus keyword search remains open. Search all open and closed theses for each candidate and take top N, initially 10 in Config. Search evidence only within its linked thesis, also top N. Evidence linked to candidates waits for their destinations, even if also linked to existing theses. Empty lists still proceed to matching." },
    { code: '4', name: "Match", who: "Model", does: "The model does not read the original item. Show each existing thesis's subject, question, focus, ladder, due date and open/closed state. In one call: (1) decide candidate identity or a narrower part, succession with unchanged ladder orientation but new thresholds, new thesis for distinct or merely similar questions, or skip overly broad questions, numbers beyond this/next year and the same period of a closed thesis; give reasons; (2) choose dependencies and directions among searched, block-5 and same-item new theses; (3) compare evidence linked only to existing theses. Evidence linked to candidates waits for their destinations, then searches all linked existing theses together and uses one further comparison call. Evidence linked only to new theses is new evidence." },
    { code: '5', name: "Validate", who: "Code", does: "Destination IDs must be in the shown lists or the relevant thesis's evidence. Merge only into open theses. New subjects must resolve within the universe using classification's identifier rules; otherwise skip. Dependencies must reference shown theses or an explicit awaited chain/year and remain acyclic. Return invalid answers for correction." },
    { code: '6', name: "Write to the library", who: "Code", does: "Resolve extraction's group associations to final theses and save them in this step. Each subject has its own writing queue; write theme theses before asset theses. Save new theses with their dependency edges. A repeat adds a source reference and any new thesis link. For replacement, order by when the statement was made: later statements supersede earlier ones. A late-arriving older statement is logged, not inserted. Carry the old evidence's other thesis links to its replacement. An original-source revision that omits a statement without replacing it marks it replaced. If compared data changes before writing, repeat matching only for the affected part." },
    { code: '7', name: "Run a rejudgement round", who: "Model", does: "Rejudge only open theses whose inputs changed: new/replaced/newly linked evidence, or a changed dependency conclusion, newly created awaited thesis or successor. Judge dependencies first, then theme theses before asset theses, and each thesis once per round. Extra source references alone do not trigger it. Memo-derived theses without evidence stay not yet judged. Each judgement declares whether its conclusion changed; changed conclusions propagate to dependants, and a theme's to every open asset thesis (D195). The round's queue is read from the ledger, so a resumed round recovers what an earlier commit queued." },
  ];

  // Two lanes, one shape: a candidate view and a piece of evidence are each compared with what is already there.
  const INTAKE_SHAPE = [
    { aspect: "Comparison set", views: "Top N search results from the entire thesis library", evidence: "Top N evidence results within its thesis" },
    { aspect: "Decision", views: "Existing identity or part, succession, new thesis or skip", evidence: "Repeat, replace or new evidence" },
    { aspect: "Chain", views: "Succession: Fed year-end 2026 rate → 2027 → 2028", evidence: "Replacement: AMZN capex guidance 12% growth → 25%" },
    { aspect: "What counts as current", views: "Open theses on the chain; numeric theses may have one for this year and one for next year", evidence: "Evidence not replaced; replacements also form a chain" },
    { aspect: "Search scope", views: "Entire thesis library, open and closed", evidence: "Only evidence within its thesis, not the entire library" },
  ];

  // Step 4: where a candidate goes.
  const MATCH_OUTCOMES = [
    { outcome: "Merge into existing", when: "The candidate concerns the same focus or a part of it, such as H20 China revenue within China revenue. Merge only into open theses; closed theses can only be succeeded.", writes: "Compare its evidence within the target thesis and preserve grouping under this section's rules. Use the existing ladder and due date." },
    { outcome: "Succession", when: "The next period of the same focus: the next year for numbers, or continued tracking after an event thesis closed", writes: "Create a thesis and record succession" },
    { outcome: "New thesis", when: "Distinct or merely similar: Blackwell export licences and H20 export licences are different questions", writes: "Create a thesis with its ladder and due date fixed from now on" },
    { outcome: "Skip", when: "Too broad or mixed, bundling questions that can move oppositely, such as all US chip controls on China; numbers beyond this/next year; the same focus and period as a closed thesis; or an out-of-universe subject. Proposed themes go to human review; out-of-universe companies receive only a processing-log entry.", writes: "Do not create it. Evidence also linked to a specific valid thesis still counts; evidence linked only to the skipped candidate is not stored." },
  ];

  const MATCH_NOTES = [
    "The D155 POC uses code for fully determined duplicate identity and model comparison when scope or legacy identity needs judgement. A shared quantity (an aggregate opened under its admission reason) is one thesis per theme, measure and period: its population or wording is not identity, so code merges another wording into the open one and succeeds it for the next period (D197). Reference lists guide research without vetoing candidates. Same group does not mean same thesis. See docs/poc/grouping-improvement-plan.md for the contract and measured scope.",
    "Search finds plausible candidates; the model handles semantic comparison. H20 and Blackwell export licences can look similar but are separate questions. Bullish and bearish accounts of one question share its identity.",
    "Search includes closed theses, allowing an FY2027 candidate to find closed FY2026 and be classified as succession.",
  ];

  // Step 4: where a piece of evidence goes, against the evidence its view already holds.
  const EVIDENCE_OUTCOMES = [
    { outcome: "Repeat", when: "The same evidence already exists under the thesis: a retelling, the same number in text and table, or the same speaker repeating the same statement", writes: "Add a source reference, not another evidence item. Existing links do not trigger rejudgement; a new thesis link changes that thesis's inputs and does." },
    { outcome: "Replace", when: "A later account of the same matter: a speaker revises guidance, forecast or event progress; an official confirms/denies a rumour; or the original source revises its statement", writes: "Order by statement date. Later statements replace earlier ones, which remain in history; rejudge. A late-arriving older statement is only logged and does not trigger rejudgement." },
    { outcome: "New evidence", when: "Anything else: a new event, another period's figure or another speaker's statement, including disagreement. Uncertainty also means new evidence.", writes: "Add it alongside existing evidence and rejudge" },
  ];

  const EVIDENCE_NOTES = [
    "First resolve the evidence's thesis destination from extraction or candidate matching. Search the top N evidence items still in force within that thesis and ask the model to compare. Unlike candidate-thesis search, evidence search never spans the whole library.",
    "Store evidence once even when linked to several theses. Compare all those theses' evidence together. If any link is to a candidate, wait for that candidate's destination.",
    "Carry other thesis links from replaced evidence to the replacement and rejudge open linked theses; otherwise they would retain only an obsolete statement.",
    "Replacement applies to a statement or number, not the whole report. A revised sell-side revenue forecast replaces that forecast while other arguments remain in force.",
    "Matching reads the evidence summary, speaker, original source and statement date, not the full original item. When uncertain, treat it as new evidence; both then remain available for judgement.",
  ];


  const INTAKE_EXAMPLE_TREE = {
    label: "Three items, starting with an empty library", note: "Illustration",
    children: [
      {
        answer: "NVIDIA 8-K, April 15, 2025", label: "Empty library; two candidates arrive", question: "Empty comparison lists; open both as new theses",
        children: [
          { answer: "#1 Theme thesis", label: "China export licensing for this chip class: event", note: "Evidence: H20 exports to China require a licence (fact)", act: true },
          { answer: "#2 NVDA asset thesis", label: "FY2026 China revenue: numeric", note: "Evidence: expected charges up to approximately $5.5 billion (party statement); depends on #1, with easing bullish", act: true },
        ],
      },
      {
        answer: "AMD 8-K, April 16, 2025", label: "AMD has no existing theses; two candidates arrive", question: "Match",
        children: [
          { answer: "Candidate: MI308 export licensing to China", label: "Merge into #1", note: "Search finds #1. The model identifies the same question: the same chip class under the same rule. AMD's MI308 statement is new evidence. #1 is rejudged but declares its conclusion unchanged: an additional affected model does not change the key facts or rung. #2 is therefore not rejudged.", act: true },
          { answer: "Candidate: AMD 2025 China revenue", label: "New thesis #3", note: "AMD has no open thesis; evidence is expected charges up to approximately $800 million (party statement)", act: true },
        ],
      },
      {
        answer: "Reuters, April 16, 2025, retelling NVIDIA's 8-K", label: "Existing context: #2 and its dependency #1", question: "Match",
        children: [
          { answer: "Evidence links to #1 and #2", label: "Both are repeats", note: "The original source is the same NVIDIA 8-K and both statements already exist under #1 and #2. Add a source reference to each; neither thesis is rejudged.", act: true },
        ],
      },
    ],
  };

  // One view's evidence over half a year: how repeats and replacements keep it current (numbers illustrative).
  const EVIDENCE_EXAMPLE = [
    { item: "February 5 call: capex guidance up 12%", matched: "New evidence; none previously under this thesis", store: "Add g1", rejudge: "Rejudge" },
    { item: "February 6 Reuters report retells the guidance", matched: "Repeat of g1", store: "Add a source reference to g1", rejudge: "No rejudgement" },
    { item: "March 10 Morgan Stanley forecast: up 18%", matched: "New evidence from another speaker", store: "Add m1", rejudge: "Rejudge" },
    { item: "April 30 call: guidance revised to 25% growth", matched: "Replace g1", store: "g2 is in force; g1 is replaced", rejudge: "Rejudge, reading “12% → 25%”" },
    { item: "May 2 Morgan Stanley forecast revised to 27%", matched: "Replace m1", store: "m2 is in force; m1 is replaced", rejudge: "Rejudge" },
    { item: "Arrives May 20: Morgan Stanley's February forecast", matched: "Late older statement; Morgan Stanley already revised it in March (m1) and May (m2)", store: "Do not insert this forecast. Log it as superseded and unused; m2 remains in force.", rejudge: "No rejudgement" },
    { item: "June 10 meeting reiterates “still around 25%”", matched: "Repeat of g2", store: "Add a source reference to g2, latest June 10", rejudge: "No rejudgement" },
  ];

  const EVIDENCE_EXAMPLE_NOTE = "After six months the thesis may have dozens of evidence items. Rejudgement reads those still in force: company guidance of 25% growth (12% in February), Morgan Stanley's 27% forecast (18% in March), plus other speakers and events.";

  // The judge of step 4, its records, and the labels that will train a faster model.
  const JUDGE_STEPS = [
    { code: '1', name: "Large-model matching", who: "Model", does: "Start with a general-purpose model using Config's matching settings" },
    { code: '2', name: "Record every comparison", who: "Code", does: "Record what the model saw, what it returned and what was ultimately stored" },
    { code: '3', name: "Human labelling", who: "Person", does: "Label two sets: code-refused decisions from validation step 5 and periodic random samples. People supply the correct outcome." },
    { code: '4', name: "Train a smaller model", who: "Code", does: "Use human labels to train a faster, smaller model" },
    { code: '5', name: "Smaller model takes over", who: "Code", does: "A smaller model eventually handles matching; the handover criterion is not yet decided" },
  ];

  const TRACE_FIELDS = [
    { part: "Which item", meaning: "Upstream ID and sequence number" },
    { part: "Received input", meaning: "Preserve extraction's candidates, associations, new group definitions and evidence exactly. Separately record the matching-model input." },
    { part: "Shown to the model", meaning: "Ranked top N thesis matches per candidate; top N evidence matches within each thesis; extraction block-5 theses and same-item new theses available for dependency selection" },
    { part: "Decision maker", meaning: "Large model, future smaller model or person" },
    { part: "Request and response", meaning: "Actual request, raw response and Config version identifying model, prompt and temperature" },
    { part: "Decision", meaning: "Each candidate's destination and reason; new-thesis dependencies and directions; evidence repeat/replacement/new decisions; validation results and refusal reasons" },
    { part: "Stored result", meaning: "What was finally written to the library" },
  ];


  // How a view ends.
  const LIFECYCLE_TREE = {
    label: "A thesis", question: "Open or closed?", note: "This is the only lifecycle switch",
    children: [
      { answer: "Open", label: "Rejudge when its inputs change, under the rejudgement rule", note: "When matching opens theses, only one for the same focus at a time; numeric quantities may have one each for this year and next year" },
      { answer: "Closed", label: "No updates or rejudgement", note: "Retain its closing state: the last rung if judged, otherwise not yet judged. Keep it searchable in the library.", act: true },
    ],
  };

  const LIFECYCLE_NOTES = [
    "Pull mode closes it when due. The current rung and reasons become its frozen final conclusion. To keep tracking, create a successor. Pull mode runs at day-end or scheduled intervals; the incoming stream does not manage time. Remaining pull-mode design is deferred.",
    "People may manually close or reopen a thesis, for example after a delisting. Append a record naming the person and the sequence after which it applies. The matching rule of one open thesis per focus does not restrict manual reopening. People also maintain the research universe.",
  ];

  const VIEW_FIELDS = [
    { part: "Subject", meaning: "The subject in the research universe", example: 'NVDA' },
    { part: "Kind", meaning: "Asset thesis or theme thesis", example: "Asset thesis" },
    { part: "Focus", meaning: "Numeric: which quantity and year; event: which event", example: "FY2027 China revenue" },
    { part: "Question", meaning: "One sentence, immutable once written", example: "How will NVDA FY2027 China revenue compare with FY2026?" },
    { part: "Ladder", meaning: "Five rungs, or two for yes/no; each is a verifiable outcome, immutable once written", example: "Up at least 50% … down at least 80%" },
    { part: "Due date", meaning: "When the debate can be resolved; for numbers, their publication day", example: "FY2027 annual earnings date" },
    { part: "State", meaning: "Current rung; append each judgement with reasons and whether the conclusion changed. A memo-derived thesis is not yet judged until evidence first links to it.", example: "Strongly bearish" },
    { part: "Dependency", meaning: "Dependency targets and directions; for uncreated targets, the awaited chain and year", example: "→ China chip export licensing: easing is bullish" },
    { part: "Research-group association", meaning: "Group memberships, stored under this section's grouping rules", example: "China licensing and business for this chip class" },
    { part: "Succession", meaning: "Predecessor, if any", example: "Succeeds FY2026" },
    { part: "Origin", meaning: "The item that created it", example: "NVIDIA FY2026 annual earnings release, February 25, 2026 (illustration)" },
    { part: "Open or closed", meaning: "One switch: open or closed. Pull mode freezes and closes at expiry; people may close or reopen manually, such as after a delisting. Closed theses do not update.", example: "Open" },
  ];

  const EVIDENCE_FIELDS = [
    { part: "Quotation", meaning: "The original sentence or table cell" },
    { part: "Standalone summary", meaning: "A sentence understandable without the original: who, what, how much and which period. Matching and rejudgement read it." },
    { part: "Source", meaning: "Upstream ID, category, publication day and location. Retellings, repeated numbers in text/tables and repeated statements add source references to the same evidence item." },
    { part: "Speaker", meaning: "The person or organisation making the statement" },
    { part: "Original source", meaning: "For a retelling, identify who originally said it and on which day. Count independent sources and order replacements by that origin." },
    { part: "Tier", meaning: "Fact, party statement, third-party view or rumour" },
    { part: "Event time", meaning: "When the event happened or takes effect; for a number, the period it describes" },
    { part: "Replaced", meaning: "The replacing evidence, where a speaker revises a statement/number, an official confirms/denies a rumour, or the original source revises/deletes it. Deletion has no replacement evidence. Replaced evidence no longer counts but remains in history." },
  ];

  const ORDER_RULES = [
    "Only incoming information creates evidence. Theses send notifications, not evidence, so they cannot prove themselves.",
    "One queue writes each thesis: the theme's queue for theme theses; the company, cryptocurrency or commodity queue for asset theses. Within an item, write themes before assets. Rejudgement order follows dependencies under the round rule. Other queues send requests, such as dependency changes or replacement links, to the owning queue with the item's sequence number.",
    "Order by sequence, never the computer clock. An item reads only records from earlier sequences plus its own round's writes. The result must match serial processing. If concurrent work changes anything it read, including search lists, before commit, redo the affected work.",
    "One item's changes form a round. Finish evidence links, thesis creation, succession and dependencies, then rejudge in dependency order. Dependants read conclusions freshly judged in that round. Judge each thesis once. A widely depended-on thesis such as the Fed rate triggers each dependant once only if it declares its conclusion changed; otherwise propagation stops.",
    "Append-only records: questions, ladders and due dates are immutable. Matching, rejudgement, succession, closure, reopening and labels append records with sequence numbers.",
    "The timeline only appends, never rewrites past knowledge. A late statement already superseded by a newer one is logged as superseded and unused, not added to the thesis. Previously unknown information counts normally with its true date. The evidence-matching model distinguishes these cases; add no separate rule.",
    "A revised input changes only its own source reference. Revising a retelling does not change original evidence. For an original-source revision, changed statements are replaced and deleted statements marked replaced. Rejudge each open thesis linked to affected statements once. A retelling-reference change alone does not trigger rejudgement. Keep old judgement records unchanged.",
    "On failure, record the item's completed step and retry from the failed step, replacing only that attempt's own result. Repeated failures go to human review.",
    "Trace both directions: a thesis to all information that affected it; an item to theses it created and all evidence it sourced, including repeats.",
  ];

  const STORE_NOTE = "Choose storage location and database during implementation.";

  const VIEWS_OPEN = [
    "Search method and ranking remain open: semantic, keyword or both. Test on stored information during implementation. Start with top 10 and adjust during experiments.",
    "Labelling details remain open: who, how many, which interface, model evaluation and training, handover to a smaller model, and checks for omitted or mislinked extraction evidence.",
    "Design pull mode later: day-end/scheduled execution, overall review, and whether final verdict remains a separate step.",
  ];

  // Claude's proposals that Alex has not decided (D45). None of them is built until he decides it.
  const VIEWS_PROPOSED = [
    "Proposal for later pull-mode design: besides due-date freezing, distinguish an unavailable answer (quantity no longer disclosed or event ceases to exist; dependants lack that input) and pending publication (period ended but the number is not yet released).",
    "Proposal for later pull-mode design: daily pairwise duplicate checks among open theses of a subject; merge the later thesis into the earlier, move links and dependencies, check cycles and rejudge. Add separate duplicate-check settings to Config.",
  ];

  // ------------------------------------------------------------------ final verdict (old draft, to be redone: D41)

  const VERDICT_EXAMPLE_NOTE = "Earlier-draft example: July evidence points both ways, with NVIDIA's statement weakening the thesis and analyst A supporting it. They are different tiers and no factual weakening evidence has arrived, so no final verdict is triggered. In August, reported Commerce licence issuance meets the old falsification condition; the tightening-controls theme is judged falsified. Its dependent NVDA thesis is reviewed again and remains open because reported Chinese procurement restrictions prevent revenue recovery, with a new premise.";


  const VERDICT_TRIGGERS = [
    { trigger: "Confirmation or falsification condition met", who: "Code" },
    { trigger: "Deadline reached", who: "Pull mode, after all items published no later than the deadline have been processed" },
    { trigger: "Premise status changes: falsified, expired, confirmed, superseded or no longer tracked", who: "Code, immediately" },
    { trigger: "Premise weakened", who: "At the subject's next item, or within seven days via pull mode" },
    { trigger: "Weakening evidence arrives in the fact tier", who: "Code" },
    { trigger: "Disagreement: independent sources within one tier support and weaken the thesis", who: "Code" },
    { trigger: "A revised source item removes the thesis's basis", who: "Code" },
  ];

  const VERDICT_TREE = {
    label: "Final verdict", question: "Does this thesis still hold?", note: "The model reads the thesis, all evidence, premise states and trigger",
    children: [
      { answer: "Confirmation condition met with factual evidence", label: "Close: confirmed", note: "Identify the evidence used", act: true },
      { answer: "Falsification condition met with factual evidence", label: "Close: falsified", note: "Identify the evidence used", act: true },
      { answer: "Deadline reached without decisive evidence", label: "Close: expired", note: "Record “no data to verify”, neither success nor failure", act: true },
      { answer: "Other cases", label: "Keep open", note: "May remove or replace premises and add verification conditions specifying decisive facts and when they can be known", act: true },
    ],
  };

  const VERDICT_RULES = [
    "The model reviews the thesis, all evidence, current premises and trigger in one judgement.",
    "Only verification conditions plus factual evidence can establish confirmation or falsification. Third-party views and rumours alone cannot. Expiry is not a correctness judgement.",
    "Write a new thesis version citing evidence and sources. Retain closed theses for historical lookup.",
    "Closing a thesis sends each thesis that uses it as a premise to another final verdict.",
    "Pass “now” into pull mode: real time in production, replay time in tests. The system owns no clock.",
  ];

  // ------------------------------------------------------------------ rendering

  function listItems(items, escapeHtml) {
    return items.map((item) => `<li>${escapeHtml(item)}</li>`).join('');
  }

  function table(headers, rows, escapeHtml) {
    return '<table class="schema-table schema-table--compact">'
      + `<thead><tr>${headers.map((header) => `<th>${escapeHtml(header)}</th>`).join('')}</tr></thead>`
      + `<tbody>${rows.map((row) => `<tr>${row.map((cell) => `<td>${escapeHtml(cell)}</td>`).join('')}</tr>`).join('')}</tbody>`
      + '</table>';
  }

  function status(pill, note, escapeHtml) {
    return `<p class="drill__status"><span class="pill pill--mixed">${escapeHtml(pill)}</span>${escapeHtml(note)}</p>`;
  }

  // Step cards; a card is { code?, title, who?, note?, strong? }. Joined by '→' (steps in order) or '+' (parts put
  // together) the cards stack top to bottom; joined by '·' they sit side by side. A short `who` is a tag, a sentence
  // is plain text.
  function flow(cards, separator, escapeHtml) {
    const code = (card) => (card.code !== undefined ? `<span class="flow__code">${escapeHtml(card.code)}</span>` : '');
    const who = (card) => (card.who
      ? `<span class="flow__who${card.who.length > 6 ? ' flow__who--text' : ''}">${escapeHtml(card.who)}</span>` : '');
    const cardClass = (card) => `flow__card${card.strong ? ' flow__card--strong' : ''}`;
    if (separator === '·') {
      return '<div class="flow flow--set">' + cards.map((card) => `<div class="${cardClass(card)}">`
        + `<div class="flow__top">${code(card)}<span class="flow__title">${escapeHtml(card.title)}</span></div>`
        + who(card)
        + (card.note ? `<p class="flow__note">${escapeHtml(card.note)}</p>` : '')
        + '</div>').join('') + '</div>';
    }
    return `<ol class="flow flow--steps${separator === '+' ? ' flow--parts' : ''}">` + cards.map((card) => `<li class="${cardClass(card)}">`
      + `${code(card) || '<span></span>'}`
      + `<div class="flow__head"><span class="flow__title">${escapeHtml(card.title)}</span>${who(card)}</div>`
      + `<p class="flow__note">${escapeHtml(card.note || '')}</p>`
      + '</li>').join('') + '</ol>';
  }

  function renderBranch(branch, escapeHtml, isRoot) {
    const isOutcome = !branch.children;
    const classes = ['org-node', isRoot ? 'org-node--root' : '', isOutcome ? (branch.act ? 'org-node--act' : 'org-node--leaf') : '']
      .filter(Boolean).join(' ');
    const box = `<div class="${classes}">`
      + (branch.answer ? `<span class="org-node__family">${escapeHtml(branch.answer)}</span>` : '')
      + `<span class="org-node__label">${escapeHtml(branch.label)}</span>`
      + (branch.question ? `<span class="org-node__question">${escapeHtml(branch.question)}</span>` : '')
      + (branch.note ? `<span class="org-node__note">${escapeHtml(branch.note)}</span>` : '')
      + '</div>';
    const below = isOutcome ? ''
      : `<ul>${branch.children.map((child) => `<li>${renderBranch(child, escapeHtml, false)}</li>`).join('')}</ul>`;
    return box + below;
  }

  function tree(root, escapeHtml) {
    return `<div class="org"><div class="org-tree"><ul><li>${renderBranch(root, escapeHtml, true)}</li></ul></div></div>`;
  }

  // Scale each tree down, never up, so the whole of it is in view.
  function fitTrees(container) {
    container.querySelectorAll('.org').forEach((frame) => {
      const inner = frame.querySelector('.org-tree');
      if (!inner) return;
      inner.style.zoom = '1';
      inner.style.zoom = String(Math.min(1, (frame.clientWidth - 8) / inner.scrollWidth));
    });
  }

  function keepFitted(container) {
    requestAnimationFrame(() => fitTrees(container));
    window.addEventListener('resize', () => { if (container.isConnected) fitTrees(container); });
  }

  const design = window.HIVEMIND_DESIGNS.new;
  design.drilldowns = design.drilldowns || {};

  design.drilldowns.extract = {
    button: "Explore extraction: from each category to evidence and candidates",
    kicker: "Extraction · Details",
    size: 'full',
    render(container, context) {
      const escapeHtml = context.escapeHtml;
      const tags = (design.classification || {}).TAGS || {};
      const categoryRows = Object.keys(CATEGORY_READS)
        .sort((first, second) => Number(first.slice(1)) - Number(second.slice(1)))
        .map((code) => [`${code} ${(tags[code] || {}).label || ''}`, CATEGORY_READS[code].read, CATEGORY_READS[code].tier]);
      const stepCards = EXTRACT_STEPS.map((step) => ({ code: step.code, title: step.name, who: step.who, note: step.does, strong: step.who === "Model" }));
      const templateCards = TEMPLATE.map((part, index) => ({ code: String(index + 1), title: part.part, who: part.source, note: part.content }));
      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">Extraction: read each category into evidence and candidates</h2>
          <p class="drill__intro">Give the model the entire item and its category prompt, alongside existing theses, to read as a senior hedge-fund analyst. Return evidence supporting or weakening existing theses or current candidates, and candidates for important uncovered questions with their initiating evidence. Personal memos follow their prompt rule. Each candidate carries a group association under the contract below. Retain sources. The library owns matching and writing.</p>
          <p class="drill__status"><span class="pill pill--strong">First version frozen · 2026-10-18</span>Decided: whole-item reading, one prompt per category with a shared structure, model-judged theses and objective evidence, source references, read-only extraction, evidence separate from complete candidates. Category prompt wording still needs validation.</p>
          <h3 class="drill__heading drill__heading--spaced">Determine group associations during extraction</h3>
          <ul class="drill__rules">${listItems(EXTRACT_RELATIONS, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">One item, step by step</h3>
          <p class="flow-legend">Black boxes are model steps; grey boxes are code.</p>
          ${flow(stepCards, '→', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">Two outputs: evidence and candidate theses</h3>
          ${table(['', "Evidence", "Candidate thesis"], EXTRACT_TWO.map((row) => [row.aspect, row.evidence, row.candidate]), escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">Classify a statement or number</h3>
          ${tree(EXTRACT_SORT_TREE, escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">Step 1: five shared prompt blocks</h3>
          ${flow(templateCards, '+', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">Category prompt example: the five blocks for T7 news</h3>
          ${tree(PROMPT_EXAMPLE, escapeHtml)}
          <ul class="drill__rules">${listItems(PROMPT_NOTES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">What to extract from each of 16 categories (block 4)</h3>
          ${table(["Category", "What to extract from this category", "Typical evidence tier"], categoryRows, escapeHtml)}
          <p class="drill__footnote">${escapeHtml(CATEGORY_NOTE)}</p>
          <h3 class="drill__heading drill__heading--spaced">Example: outputs from two items</h3>
          ${tree(EXTRACT_EXAMPLE_TREE, escapeHtml)}
          <p class="drill__footnote">${escapeHtml(EXAMPLE_NOTE)}</p>
          <div class="drill__columns">
            <section>
              <h3 class="drill__heading drill__heading--spaced">Source-reference fields</h3>
              ${tree(SOURCE_TREE, escapeHtml)}
              <ul class="drill__rules">${listItems(SOURCE_NOTES, escapeHtml)}</ul>
            </section>
            <section>
              <h3 class="drill__heading drill__heading--spaced">Open questions</h3>
              <ul class="drill__rules">${listItems(EXTRACT_OPEN, escapeHtml)}</ul>
            </section>
          </div>
        </div>`;
      keepFitted(container);
    },
  };

  design.drilldowns.views = {
    button: "Explore the thesis library: structure, storage, links and labelling",
    kicker: "Thesis library · Details",
    size: 'full',
    render(container, context) {
      const escapeHtml = context.escapeHtml;
      const stepCards = (steps) => steps.map((step) => ({ code: step.code, title: step.name, who: step.who, note: step.does, strong: step.who === "Model" }));
      const tierCards = TIERS.map((tier, index) => ({ code: String(index + 1), title: tier.tier, note: `${tier.examples}。${tier.counts}`, strong: index === 0 }));
      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">Thesis library</h2>
          <p class="drill__intro">Create, update and close theses here. A thesis has a question, ladder and due date; evidence moves its state, which freezes when due. Search and compare both extraction outputs: candidates against existing theses for merge, succession, creation or skip; evidence within its thesis for repeat, replacement or addition. An extra source reference alone does not trigger rejudgement. Preserve sources and extraction-owned group associations under the rules below. Records are append-only.</p>
          <p class="drill__status"><span class="pill pill--strong">First version frozen · 2026-10-20</span>Only recorded decisions are included. Changes need a new decision. Open questions and two pull-mode proposals are listed at the end.</p>
          <h3 class="drill__heading drill__heading--spaced">Research groups: associate during extraction</h3>
          <ul class="drill__rules">${listItems(GROUP_RELATIONS, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">Structure</h3>
          ${tree(VIEW_TREE, escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">Two thesis kinds: shared structure, different rung meanings</h3>
          ${table(["Kind", "Subject kind", "Ladder rungs", "Example"], VIEW_KINDS.map((row) => [row.kind, row.on, row.rungs, row.example]), escapeHtml)}
          <p class="drill__footnote">${escapeHtml(KIND_NOTE)}</p>
          <h3 class="drill__heading drill__heading--spaced">Ladders: five verifiable outcomes, or two for yes/no</h3>
          ${tree(LADDER_EXAMPLES, escapeHtml)}
          <ol class="drill__rules">${listItems(LADDER_RULES, escapeHtml)}</ol>
          <h3 class="drill__heading drill__heading--spaced">State: the current rung</h3>
          ${table(['', "What it is", "Decision maker", "Example"], POSITIONS.map((row) => [row.position, row.means, row.moves, row.example]), escapeHtml)}
          <ul class="drill__rules">${listItems(STATE_RULES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">Four evidence tiers</h3>
          ${flow(tierCards, '·', escapeHtml)}
          <ul class="drill__rules">${listItems(TIER_RULES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">Dependencies: reading the arrows</h3>
          ${tree(DEPENDENCY_TREE, escapeHtml)}
          <ul class="drill__rules">${listItems(DEPENDENCY_RULES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">Succession: the same focus over successive periods</h3>
          <ul class="drill__rules">${listItems(CHAIN_RULES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">Intake: search then compare candidates and evidence</h3>
          ${table(['', "Candidate thesis", "Evidence"], INTAKE_SHAPE.map((row) => [row.aspect, row.views, row.evidence]), escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">One item entering the library: a round</h3>
          <p class="flow-legend">Black boxes are model steps; grey boxes are code.</p>
          ${flow(stepCards(INTAKE_STEPS), '→', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">Step 4: candidate destinations</h3>
          ${table(["Destination", "When", "Writes"], MATCH_OUTCOMES.map((row) => [row.outcome, row.when, row.writes]), escapeHtml)}
          <ul class="drill__rules">${listItems(MATCH_NOTES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">Step 4: evidence destinations</h3>
          ${table(["Destination", "When", "Writes"], EVIDENCE_OUTCOMES.map((row) => [row.outcome, row.when, row.writes]), escapeHtml)}
          <ul class="drill__rules">${listItems(EVIDENCE_NOTES, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">Example: three items entering the library</h3>
          ${tree(INTAKE_EXAMPLE_TREE, escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">Example: evidence updates for AMZN 2026 capex (illustration)</h3>
          ${table(["Item", "Evidence comparison", "Library result", "Rejudgement"], EVIDENCE_EXAMPLE.map((row) => [row.item, row.matched, row.store, row.rejudge]), escapeHtml)}
          <p class="drill__footnote">${escapeHtml(EVIDENCE_EXAMPLE_NOTE)}</p>
          <h3 class="drill__heading drill__heading--spaced">Matching and labelling: start with a large model, train a smaller one later</h3>
          <p class="flow-legend">Black boxes are model steps; grey boxes are code or people.</p>
          ${flow(stepCards(JUDGE_STEPS), '→', escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">Matching-record fields</h3>
          ${table(["Part", "Recorded content"], TRACE_FIELDS.map((row) => [row.part, row.meaning]), escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">Open or closed</h3>
          ${tree(LIFECYCLE_TREE, escapeHtml)}
          <ul class="drill__rules">${listItems(LIFECYCLE_NOTES, escapeHtml)}</ul>
          <div class="drill__columns">
            <section>
              <h3 class="drill__heading drill__heading--spaced">Thesis fields</h3>
              ${table(["Part", "Writes", "Example"], VIEW_FIELDS.map((row) => [row.part, row.meaning, row.example]), escapeHtml)}
            </section>
            <section>
              <h3 class="drill__heading drill__heading--spaced">Evidence fields</h3>
              ${table(["Part", "Writes"], EVIDENCE_FIELDS.map((row) => [row.part, row.meaning]), escapeHtml)}
              <h3 class="drill__heading drill__heading--spaced">Ordering, concurrency and traceability</h3>
              <ul class="drill__rules">${listItems(ORDER_RULES, escapeHtml)}</ul>
              <p class="drill__footnote">${escapeHtml(STORE_NOTE)}</p>
            </section>
          </div>
          <h3 class="drill__heading drill__heading--spaced">Open questions</h3>
          <ul class="drill__rules">${listItems(VIEWS_OPEN, escapeHtml)}</ul>
          <h3 class="drill__heading drill__heading--spaced">Proposals awaiting Alex’s decision</h3>
          <ol class="drill__rules">${listItems(VIEWS_PROPOSED, escapeHtml)}</ol>
        </div>`;
      keepFitted(container);
    },
  };

  design.drilldowns.verdict = {
    button: "Explore final verdicts: triggers and outcomes",
    kicker: "Final verdict · Details",
    size: 'full',
    render(container, context) {
      const escapeHtml = context.escapeHtml;
      container.innerHTML = `
        <div class="drill">
          <h2 class="drill__title">Final verdict (earlier draft): does the thesis still hold?</h2>
          <p class="drill__intro">Current decision: pull mode freezes and closes the thesis at its current rung when due. Whether a separate final verdict remains is deferred. The earlier draft below instead asks a model to review the whole thesis and its evidence before deciding closure.</p>
          ${status("Earlier draft · Requires redesign", "The library was rebuilt under D38–D40. Verification conditions, confirmation/falsification, premises, seven-day fallback review and same-tier-disagreement escalation no longer apply (D38, D41). Each thesis has one state, frozen and closed when due, with no separate outcome. Pull mode runs at day-end or on a schedule without an extra wait (D54). Other details will be redesigned with pull mode.", escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">Triggers</h3>
          ${table(["Trigger", "Detected by"], VERDICT_TRIGGERS.map((trigger) => [trigger.trigger, trigger.who]), escapeHtml)}
          <h3 class="drill__heading drill__heading--spaced">Outcomes</h3>
          ${tree(VERDICT_TREE, escapeHtml)}
          <div class="drill__columns">
            <section>
              <h3 class="drill__heading drill__heading--spaced">Rules</h3>
              <ol class="drill__rules">${listItems(VERDICT_RULES, escapeHtml)}</ol>
            </section>
            <section>
              <h3 class="drill__heading drill__heading--spaced">Example</h3>
              <p class="drill__footnote">${escapeHtml(VERDICT_EXAMPLE_NOTE)}</p>
            </section>
          </div>
        </div>`;
      keepFitted(container);
    },
  };
})();

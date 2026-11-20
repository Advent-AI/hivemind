# Decisions

What is decided now, by module. Each entry states the core of the rule in force and the decisions it rests on (the first decided it,
later ones amended it); the module's PRD, or the document named, holds it in full, and each decision's record in the log governs its
conditions, thresholds and exceptions where an entry is shorter. An entry may be shorter than its decisions; it never says otherwise. An entry marked *(Claude)* rests on a detail Claude settled
inside a decision Alex made, not on his own words; *(not built)* means decided and waiting for its build. Proposals never decided are
not here.

- The full record of every decision (Alex's words, what was decided, what was done), in number order: [DECISIONS-log.md](DECISIONS-log.md).
- The frontend's presentation decisions in force: [DECISIONS-frontend.md](DECISIONS-frontend.md).
- Every decision number with its status: the [index](#index) at the end.
- How a new decision is recorded: AGENTS §11.

<a id="consolidation"></a>Consolidated on 2026-11-05 (D367) from the log's 365 decisions (D1–D366; D90 does not exist): 266 stand in force, 110 of them
frontend presentation; the others were superseded by a later decision, retired with what they governed, or are records of a run, a
measurement or a version later replaced. One reader classified every decision and a second (Codex) checked each classification
against the log; the conflicts they found are below, settled or open.

Numbering is one sequence. At the 2026-11-03 merge, `main`'s D181–D241, D258 and D259 became D275–D336, and `main`'s uncommitted
D242–D257 became D337–D352; the log gives both mappings in the notes that head D275 and D337. Decisions written on `main` before the
merge may cite the old numbers: D199, D200, D203 and D227 do, and D366's "since D256" means D351.

## Open for Alex

Nothing is open. The seven items this consolidation left for Alex were answered on 2026-11-05 (D368) and are written into the sections
below: the next extraction version's two changes (§6), the three rules to build (§7), pull mode's day-end scope (§8), the seed questions'
arrows (§7), PRD 10's two corrections (§10), the correction record beside the frozen standard page (§11) and English for the pages written
for Alex's review (§1).

## Settled in this consolidation

Conflicts the readers found that a later decision or a reading of the decisions together settles; the entries below state the result.

- **Daily judging and the stream.** D14 confines D13's "no daily step" to the stream, and D63 keeps the calendar outside it: at the end
  of each day, after its last item, one round judges the open questions whose reading changed (new or newly linked evidence, a
  dependency's or a theme's changed conclusion), then pull mode closes the questions due that day (D356). D39 and D46's per-item round are amended by D63.
- **The final verdict** (D29, D55's final-verdict part): retired by D356; PRD 07 is "Closing at the due day".
- **Identity.** D44's "no key matched by code" is amended by D155, D166 and D197: code owns identity on typed keys and names; identity
  over a model-written scope stays the model's judgement (D167).
- **Filing.** D42's "one or more" and the standard page's "several questions" against D207's "one home": the daily filing is one home,
  the narrowest open question, plus the same answer's own candidates (D207, D259, D264, D265); the former coverage-start exception is retired (D370).
- **The Idea's theses.** D282's "the model cannot assign weights or alter the selected theses" is amended by D288–D290: the model adopts
  and weights the theses.
- **Citations.** D92's "theme colours only" is amended by D284 (plain blue citations).
- **Services.** D112 packages the two services for Docker; on this Mac they are tested on the host because the VPN blocks container
  networking (AGENTS §9). Both hold.
- **Defaults.** Each "`poc-vNN` is the default" decision is superseded by the next; D370 replaces D366 as the replay-default decision.

## 1. System (PRD 00)

- **Two modes** (D10, D12, D13, D14, D56): the stream moves the library only when an item arrives and never reads the calendar; pull
  mode is the only place where time triggers work, with its "now" passed in. The boundary is a stream of classified items from
  upstream; nothing pulls sources; an upstream id and version is processed once.
- **Time** (D5, D9, D34): an item's time is its own publication time, cut to its New York calendar day; no rule reads the computer's
  clock (`retrieved_at` is for audit); the time of day orders nothing; an SEC filing's day is its filing date (accepted before 17:30 ET,
  that day; after, the next business day).
- **No input store** (D7): the materials stay in the team's database; the system keeps a processing record of each item and version
  processed; testing streams a test database through the same path.
- **Order and one writer** (D31, D375): dispatch numbers items in arrival order; each question has one writer. Before each item,
  extraction reads the latest committed questions from smaller sequences, including earlier same-day writes. The split calls share that snapshot.
- **Daily judging** (D63): the day's items are extracted, matched and written in order; after the last item one round judges every open
  question whose reading changed that day, dependencies first, each once; then pull mode closes the questions due that day (D356).
- **Thesis-first** (D24 as kept by D28): data paths are designed from what a question needs; no number warehouse.
- **Freezes** (D19, D37, D48, D58): the universe, classification, Config, dispatch, extraction, the review pool's intake and the thesis
  library were frozen as v1 between 2026-10-16 and 10-22; later decisions amended them, and every further change needs a new decision.
  D58 also fixes how a dependent states which end of another question is favourable for it and that a question covers what happens up to
  its due date.
- **Language** (D133, D163): code, stored values and model output are English, written in English at the source; maintained prompts, UI
  text and current documentation are English, the pages written for Alex's review included (D368); source quotations and historical
  records keep their language, and nothing historical (databases, frozen prompts, raw answers, decisions) is rewritten in place.
- **The POC** (D62): it follows the frozen design in a simpler form, its simplifications listed in `docs/poc/pipeline-plan.md`; the model
  decides how many questions open (no cap; code checks the shape only); the corpus is whole and original; a small test comes before any
  full run.

## Latest decision: remove the separate earnings-report import (D370)

Alex removed the separate coverage-start earnings-report reading and report background added to news extraction. He retained extraction's lookup of the existing research library. An earnings release itself can still enter as an ordinary source item (D28). D363–D366's separate report-import requirement is superseded; their historical evidence and frozen materials remain historical. The small real-news comparison tested appended extraction context, not the distinct coverage-start mechanism. The implementation status is recorded in `CURRENT_STATE.md`.

## Latest decision: current and future financial evidence (D371)

Alex: “收入和财务这边对于当下，未来应该都是需要track 的，你应该要修改”. Financial information on present performance and future expectations is to be tracked for relevant investment questions. A quarterly period is not a reason to exclude supporting evidence from an annual question; this does not by itself require a separate question for every financial line. The research model judges relevance; no company-specific rule is introduced. The old frozen ruler and its historical scores remain unchanged. Implementation and evaluation status are in `CURRENT_STATE.md`.

## Latest decision: continue scoring on the existing gold (D373)

Alex removed the gold-inconsistency stop and asked to score the new split prompts on a few cases first, reusing existing old results where comparable. Keep frozen gold unchanged; record and disclose the three disputed question entries with any relevant score rather than stopping. D372 remains the evidence counting rule. This does not resolve the disputed entries or authorize production deployment.

## Latest decision: read the current library for each item (D375)

Alex confirmed that each article must use the latest committed question library, including topics opened earlier that day. The new-viewpoint and existing-evidence calls for the same article share that per-item snapshot. This supersedes the once-daily snapshot in D251. The production implementation and acceptance are pending; historical runs and the frozen gold remain unchanged.

## Latest decision: return complete evidence without the 1 MB rejection (D376)

Alex directed removal of the research reader's 1 MB evidence-expansion rejection. The reader returns all evidence and source details for the selected questions, without truncation. D377 subsequently removes the separate question-catalog limit. The implementation was changed and tested in the main worktree; the running seven-day diagnostic retains its pinned code and does not call this reader.

## Latest decision: return the full question catalog without the 150 KB rejection (D377)

Alex directed removal of the separate 150 KB question-catalog rejection. The research reader returns the complete in-scope catalog without truncation, while preserving the existing historical boundary and dependencies. The main worktree has the change; the live seven-day diagnostic retains its pinned code.

## 2. Research universe (PRD 01)

- A module of its own, versioned apart from Config: what is researched, by entity id and asset class; a run records the universe version
  it used (D6).
- Four kinds of object: company, crypto asset, commodity, theme; rates, FX and indices are data that themes track; a theme comes only from
  the object upstream fed the item for or an upload's declaration, never from the text (D11).
- The universe is the one switch: each object's tracked tags define the supply scope (objects × tracked tags), kept by whoever writes the
  stream; every item that arrives is processed; a new object or tag is a new universe version (D18).
- Earnings releases, periodic reports and earnings calls are in the stream like every other item (D28).
- A document belongs to a theme when it can move a thesis of the universe, not because a case number or keyword matches (D104).

## 3. Classification (PRD 02)

- A classified input carries its related objects (entity ids with their basis) and its unresolved identifiers, read only from the
  channel's identifiers and a company author, never from the text or the URL; a ticker resolves on its publication day; invalid items and
  non-source material carry none (D1).
- Four lookup tables in one JSON data file that production and tests read; a changed table is a new classification version (D8). The
  publication-series table is checked before the author type and yields only T8, T10 or T11 (D15, *(Claude)*).
- A filing's XBRL numbers are not items of their own; table data is pushed one release per item, whole; nothing gets a price-specific
  rule; pull mode looks up an exact tagged value when a condition needs one (D32).

## 4. Config (PRD 03)

- Model requests have no configurable sampling temperature (D374). Historical configuration files and their checksums remain evidence.

- Config holds only the choices a person makes: model settings (one per extraction category and one per model call: matching, the
  collision judge and re-judging) and the search size; mechanisms belong to code and what is researched to the
  universe (D2, D41, D190, D370).
- No limits section: no budget and no concurrency in Config; worker counts are run arguments (D3, D181, D183).

## 5. Dispatch (PRD 04)

- Dispatch is the single entry: one decision tree asks whether the item meets the contract (no: refused, to the review pool), whether
  the same id and version was processed (yes: skipped) and what its classification outcome is; every item reaches one destination (D17).
- An item's related objects play no part in dispatch (D4). Known departure: the POC's `dispatch.route` filters by related object and
  tracked category, a scope D18 gives to upstream.
- Items published before coverage start are not dispatched; the separate report import was retired (D370).

## 6. Extraction (PRD 05 and the extraction standard)

- **Existing production design: one module, one call per item** (D25, D27, D33, D199): every item of a tracked category is read whole by its category's template, a
  senior hedge-fund analyst's prompt; tables without tags are read by the model with no separate parsing code (D23); the program owns
  the output shape and checks every quote against the source; extraction never changes the library. One call per item; repeated calls measure stability and never vote or combine into one answer (D193, D338).
- **What it hands over** (D42, D209, D264, D375): evidence, each piece with its source, filed under the questions open immediately before the item
  (shown with their takes lines) or under the same answer's candidates; candidate questions for important matters no open question
  covers, each with the evidence that raised it; a statement neither takes is dropped as "no home", and evaluation reads the drops.
  Alex's own memo is read as candidate questions, not evidence (D59, D60).
- **Filing** (D207, D254, D259, D264, D265, D268, D273): a statement goes under the narrowest open question it bears on, as that
  question's own figure, step or estimate or through the demand, supply, competition or pricing behind its answer, never a broader
  question beside it; a launch, shipment or deployment event also takes its variants and stopgaps, a policy process its enforcement,
  evasion and the affected parties' plans and statements; an estimate for another period or population of a question's quantity goes
  under it when no open question covers that period; a statement linked to a question and to one it depends on keeps the narrower (code);
  when no specific question is connected, a statement that moves the demand, supply, competition or pricing behind the company's results
  goes to the company-wide revenue question of its period (the fallback, D273, kept by D361).
- **Opening a question** (D184, D185, D210, D236, D248, D158): a candidate opens for one of four reasons (main driver, industry aggregate,
  policy stage, binding obligation) and names what settles it; the main driver includes the launch or ship date of the product generation
  that carries the company's value; a binding obligation not yet signed opens a yes/no question due within 18 months, one already taken
  on an amount question at the company's next annual filing (never for its own borrowing); a deal, product or project opens one only when
  its scale can change revenue, profit, cash or credit risk; event and policy candidates are exempt from the next-year check.
- **The item's snapshot** (D375, superseding D251): each item reads the latest committed research questions before that item. The experimental A and B split calls use the same snapshot and may run in parallel; an earlier same-day write is visible to later items. The existing selection is the item's subjects' open questions and all open theme questions. Dispatch sequence establishes the boundary.
- **The request** (D237, D249, D252): a general hedge-fund brain, its rules and examples reading the same for any company and naming no
  covered company or test article; a closing check at the end of the same request reads the evidence list back by the standard's test and
  its not-kept rows; noise is taught by general paired examples; a future version scores whether evidence is helpful, without requiring separate core/supporting scores (D372).
- **Quotes** (D236, D266 *(Claude: the thresholds)*): a quote a word or two off the source (function words, pronouns, the company's
  generic name or own name, anchored at one end) is stored as the exact source passage.
- **Statement fields** (D203 *(Claude)*, D218): a statement's original day is an ISO day or unknown, never filled with the publication
  day; an analyst's inference is never presented as a source fact, and material unknowns stay.
- **Frozen** (D274, D359): extraction v74i at low reasoning on `gpt-6-luna` (D234: Haiku parked): the role, the closing check, the
  category blocks, the takes lines, the filing rule and the evidence schema, pinned by `tests/test_frozen_extraction_prompt.py`; the code
  builds no other version. What is kept follows the frozen standard (§11 below).
- **The next extraction version** (D368): asset-thesis rungs stated against guidance, each thesis naming its favourable end (D186), and
  `industry_aggregate` renamed `shared_quantity` (D191 point 4) are built in it, measured against the frozen v74i.

## 7. Thesis library (PRD 06)

**Questions**
- A question is one question with a fixed ladder and a due date, never rewritten: five checkable, non-overlapping rungs covering every
  outcome (an asset question strongly bullish to strongly bearish for the business, a theme question named by outcome), two for a yes/no
  question (D38, D46; the outcome rungs against guidance of D186 come with the next extraction version, §6).
- A number question names its period; a company's figures use its fiscal year; at most this year and next open (D46, D248 boundary 4).
- Any company's own quantity is a thesis under that company, private companies included (D187); *(not built; to be built, D368: it needs
  a private-company object kind in the universe)*.
- One state per question; one switch, open or closed; only open questions are judged; a closed question keeps its state and stays
  searchable; a person can close or reopen one by hand (D54, D57). The research list is edited by hand; a question whose object is taken
  off it is kept and no longer updated (D55, its flag replaced by the open/closed switch of D57).
- **One bet, one question** (D248): two questions are one when the same outcome settles both and stay apart only when their answers can
  move apart and an analyst would bet on each separately; wordings, deadlines, milestones and periods of one bet are one question (a
  later deadline is evidence while the earlier is open; one question per product generation, at the step that brings revenue); a small
  matter opens no question; the same statement carried by several outlets (the same known original speaker, original day and figures; an
  unknown speaker or day never matches) is shown to the judge once with the outlet count, every piece still stored (boundary 7, a chosen
  exception to "equal values never establish identity", switched on only after its merge risk on the gold and the accuracy of the
  original speaker and day are measured; D204 holds until then).
- **Seeds retired** (D370): new replay does not insert the 22 preset questions and refuses old seeded ledgers. Historical seed files and their measured results remain frozen. Existing article-created questions remain context.

- **The thesis tree** (D208): every company's library has root quantities (its reported lines), a driver layer of seven fixed classes
  (demand, supply and inputs, competition and share, pricing and installed base, product cycle, policy, capital and obligations) whose
  instances the analyst writes once at coverage start, each declaring the root it feeds, and shared macro themes, each company's
  direction a declared dependency with a channel sentence the judge reads, macro evidence filed only under the macro theme; roots read
  the drivers' and themes' conclusions; the template routes and never gates. The historical seeds were retired by D370; the rest *(not built)*.
- **Themes** (D191, D195): a theme question is context for every company question (one to all); explicit dependencies stay where a
  document states them; a macro-only item opens a theme only when it is listed; an asset judgement carries the block of open themes and
  answers how they push; themes are judged before assets, and a changed theme queues every open asset question with evidence in force.
- **Research groups** (D149, D165, D166, D257): extraction declares a statement's group while reading; a group is one ongoing matter several
  questions track, usually across companies; code decides group identity and membership from the group's names; a company's own
  financial lines carry no group unless the line tracks such a matter; Jev also answers membership (D169).

**Evidence**
- Evidence is objective (who said what, where), each piece with its source; code refuses a source it cannot find or a quote not in the
  document (D26). Four tiers (happened, said by the party itself, a third party's view, rumour); sources are counted by original source
  (D30).
- Records are append-only; evidence linked to no question is not stored (D39).
- **The writer retires nothing** (D202, D204, D168): a revision stores the incoming piece beside the old one, both in force, the pair
  recorded; a repeat is stored as its own source record with the pair recorded; an older statement arriving later is stored and linked.
  A revision is a changed later version of the same statement or number by its speaker, an official or the original source (D168
  *(Claude)*).

**Matching**
- Jev is the matching engine (D169); its output is an opinion with a score, not the decision to keep or merge (D201). Code owns identity
  on typed keys: a complete key equal, event type included (D154 *(Claude)*, D155, D164); a shared quantity is one question per theme,
  measure and period, decided by code before any judge (D197); identity over a model-written scope stays a judgement (D167). When a
  candidate's list holds a question of its own object and measure, the collision judge answers the analyst's question and its verdict
  replaces Jev's (D190, D258).
- A new thesis's dependencies are chosen in matching (D51); the default Jev path does not ask for them, so a thesis opened from an article
  has none of its own *(to be built, D368)*; a later item may add a dependency to an existing thesis (D191 point 2) *(to be built, D368)*.
- Every match writes a matching record, kept for human labels and a later smaller model (D40).

**Judging**
- A question is re-judged when what it reads changed: new or newly linked evidence, a dependency whose conclusion changed, a changed theme
  (D51, D191, D195); daily, in one round (D63).
- A judgement is a forecast against a reference (D260 *(Claude)*, D263): the outcome the evidence in force makes most likely at the due day,
  against consensus, guidance or the stated plan; "not established" is never a reason to stay; the answer states its reference and implied
  outcome; a gap to the frozen judgement gold is closed in the judge's rule.
- A judgement reads the evidence in view (D198): the arrivals since its fifth most recent judgement and the basis its last ten cited; the
  rest stays in force.
- A judgement may cite the questions it depends on, checked by code against its dependencies; evidence a candidate carries is compared
  after the candidate's place is known (D47 *(Claude)*).
- The judging call's output budget is 16,000 tokens (D205).
- **Frozen** (D354): the collision judge (`collision-v2`), the judge (`judging-v7`), the matching prompt (`matching-v3`), the judge's
  answer schema and the three Jev questions, pinned by `tests/test_frozen_questions_and_judgement.py`.

## 8. Closing and pull mode (PRD 07, PRD 08)

- At its due day a question freezes at the rung it stands on and closes; that rung is its conclusion; nothing waits for the result (D54,
  D356).
- Closing belongs to pull mode, at the end of each day; there is no separate final verdict and no day-end re-judging without new
  evidence; a due day falls on or after the day the result is published, set when the question opens; the closing record names the frozen
  rung or "no data to verify", is shown from the closing day and never gates; a closing on a day without items gets its own sequence
  number (D356).
- A question that depends on a closed one reads its frozen state and reasons (D54, D57).
- Pull mode does nothing else at day end: D248 boundary 2's step that opened the next-deadline successor of an event question falling due
  unresolved is dropped (D368).

## 9. Review pool (PRD 09)

- What the tables do not know is not guessed but goes to a human review pool: unregistered codes and datasets and undetermined author types
  refuse the item; unregistered series and unresolved identifiers are processed and recorded; contract violations, proposed themes outside
  the universe and repeatedly failed items enter; one entry per gap with its count and examples (D16, D41). Only the intake is designed.

## 10. Current phase: filing that links facts the way an analyst does (PRD 10)

- PRD 10 is the phase's single source, opened on Alex's words on 2026-11-04, amended on his "go" (D360) and, on 2026-11-05, translated
  into English with §4's standard version and a §5 status line corrected (D368); every step starts with its §0 checklist. Its steps and results are in §8 and `docs/research/2026-11-04-filing-end-to-end/log.md`.
- The filing topic of 2026-11-03 closed without a change: filing is about 85% right; the misses are known defects (D355).
- The phase's filing rules and decision rule (D360): a statement bearing on two specific questions goes under the one whose quantity it
  measures most directly; a statement giving a separate figure for each of two questions is written as two evidence items, which code
  stores as one record linked to both when they quote one sentence; a filing change is accepted on totals tested against luck by
  reassigning answers between arms and on per-question limits. The links-rule version carrying these rules (v74l) failed its one test
  and is not in the product (§8 step 5); the fallback stays (D361); the two narrow delivery fixes stopped (D362).
- **Separate report import retired** (D370): no coverage-start report reading and no report appended to each news request. Reports can still arrive as ordinary source items. The historical starting-figure tests measured a different mechanism from the real-news report-context comparison; their results remain historical.

- **Evidence capture going forward** (D369, D372): score future evidence as helpful or not helpful, without requiring separate core versus supporting scores. The MXC example is retained as helpful evidence; a model may judge a clear logical indirect connection. Use the same frozen gold for these combined counts; its files and historical scores remain unchanged.

- **Future evidence scoring** (D372): Alex chose helpful / not helpful as the scoring distinction, without requiring separate core/supporting scores. Use the existing frozen gold as-is: count its core and supporting entries together as helpful, its not-kept entries as unhelpful, and keep optional entries neutral. The D250 unit remains one research matter in one article. Combining the counts does not require a new gold. Frozen golden-v5 and historical scores remain unchanged.

- **One ruler** (D241, D243, D242): the signed extraction standard page `docs/prd/05-extraction-standard.html` is the one standard for
  extraction and its PRD; while standards diverge, prompt work and sends stop until the standard is settled with Alex.
- **The frozen ruler** (D261, D262): the extraction standard (its version 5: version 3 signed in D243, with D248's seven boundaries and
  D250's four evidence boundaries), golden-v5, the seeds v2 and the judgement ruler with reader B's gold; never changed; a later defect is
  a dated correction record printed with every score and never merged; a new version only by Alex's decision, with its own gold and no
  comparison with old scores. Pieces and hashes: AGENTS §7.1; `tests/test_frozen_rulers.py`. The page's three statements that later
  decisions changed are noted in the dated record beside it, `docs/prd/05-extraction-standard-corrections.md` (D368).
- **Measuring** (D244, D214): the 118 seen bench articles are the development set; a fresh test set from a later window is frozen before
  its first send and scored once per configuration; every measurement has a score and the traces are read; the scorer hard-codes no rule,
  prints the gold's and the page's sha256 and refuses a mismatched gold; meaning is judged by readers, structure and counts by code.
- **Reading the standard** (D216, D220 *(Claude)*, D221 *(Claude)*, D226, D231, D233, D240, D250): a far-off forecast is not dropped for
  being far off; the required parts of a statement's meaning are those that change its interpretation, valuation, risk, scope or
  evidential nature; evidence is assessed by the conclusion it can support; reasonable ambiguity is allowed and gold examples teach the
  reasoning; "this year" as the fiscal or the calendar year keeps the meaning; a named party's relevant action is kept without an amount,
  its weight judged apart. Not kept (D250): an arrangement retold with no new step; another company's matter of which one cannot say
  how it moves a question about the company through a path such as demand, supply, competition or pricing; a comparison the company, a partner or a third party
  publishes (a competitor's comparison with the company's product, and a partner's or customer's adoption in the same sentence, are
  judged under the evidence rule); a named analyst's reading of an already-recorded event with no new fact or calculation.
- **Other golds**: the idea gold (twenty ideas, model-authored, sealed with its digest; D146); grouping is judged by research meaning, not
  identical group counts (D148).

## 12. Idea API and service (docs/poc/idea-card.md, docs/poc/service.md)

- Hivemind is a thesis database with a read-only search service on top: semantic search over each thesis's own text, readers and
  evaluation, all as of a calendar day; the core service picks no theses for a caller and stores no user data (D76). A search returns
  `null` only when the idea names no object, no thesis text matches and the top similarity is below 0.30; an idea above that floor that
  names nothing still goes to the model (D91, D132 *(Claude)*); an object is named only by its id, full name or a listed alias (D132).
- The HTTP and MCP services run as two Docker services on local ports; the model key stays in the service (D112). The MCP front gives an
  external agent the workflow recipe and the object list; the service itself runs no agent loop (D134, amended by D135).
- `POST /ideas` looks up in code: one call breaks the idea into typed parts, the service searches per part and follows the dependency
  graph, one call maps parts to candidates (D135, D145); the endpoint can stream its real progress stages (D281); clicking the Idea card
  opens its detail, and `summary` is the single analyst-written TL;DR (D280).
- Every covered Idea returns a composite plan and chart (D282); the final call adopts the theses and gives each a positive integer weight,
  a nonempty plan totalling 100, with no excluded or zero-weight branch; code checks the totals and computes the weighted history; fresh
  answers may vary and are recorded, not repaired (D288–D290); confidence = 50 + 25 × the weighted aggregate on 0–100%, a defined index,
  not a probability (D291).
- `poc-v33-idea` / `idea-summary-v8`: each candidate's entry in the final call is pinned by the request schema to its id and its own two
  endpoint positions (D335).

## 13. Data (README, "Local requirements and data")

- Fed pages are cleaned by `poc/corpus/scripts/clean_pages.py` into a new dated database that keeps the whole pages in `text_page`; the
  cleaned database holds the canonical name, `items-nvda-2026-07-01-10-27.sqlite`, and cleaning is a step of every future freeze (D351).
- The TrueNorth event index is set aside as a source; its backfilled databases stay as a record (D352).
- The served data is the sealed three-month ledger `served-2026-10-28-v34-nvda-3m-through-0828`; evidence bloat over a long window is an
  open problem (D358).

## 14. Operations (README, AGENTS §9)

- **The parallel day** (D172, D181, D183): `scripts/replay.py` prepares requests concurrently and commits through one ordered writer; a
  turn accepts only a byte-identical request, recomputing a stale one; `--workers 16` and `--jev-workers 8` by default, `--workers 1` the
  serial path; worker counts are run arguments, not Config.
- **One path in the code** (D359): the code builds only the frozen versions and refuses a configuration that names another before any
  request; older versions are read from their stored runs.
- **The replay default** (D370, D374): `poc/config/poc-v118.json`, without seeded questions or the separate coverage-start report import. It retains the frozen v108 extraction, matching and judgement settings. End-to-end acceptance is pending.

- **Repository** (D353, D357): documents, code and every file a reader names stay in Git; run databases, logs and model archives stay on
  disk, located by the data manifest; configurations and prompts nothing current names leave (Git keeps them).

## 15. Working rules (AGENTS.md)

The decisions on how Claude works are written at the decision they govern in AGENTS.md: a rule is decided only with Alex's words (D45;
Authority and scope); one PRD per module, the precedence Alex, decisions, PRDs (D20; §11); refresh by reasoning in a fixed module order
(D22; §11); one word per concept, checked by `docs/check.py` (D36, D52; §3); a sealed copy of the design is never edited (D43 *(Claude)*;
§11); both analyst standards applied before a prompt, evaluation or change (D228; §8); a direct-read pass locates mechanisms, its counts
one draw (D238; §7.3); the extraction standard page is the step's PRD and AGENTS §6–§7 carry the principles (D242; §6, §7).

## Index

Every decision number, its date, its title as recorded, its status today and the section that holds it (§) or, for one no longer in force, its topic. "Record" means a run, a measurement, a probe or a version adoption later replaced, with no standing rule of its own; its full text is in the [log](DECISIONS-log.md).

| D | Date | Decision | Status | Section |
|---|---|---|---|---|
| D1 | 2026-10-15 | Input classification carries each input's related companies | in force (amended by D11) | §3 Classification |
| D2 | 2026-10-15 | Config holds only the choices a person makes | in force (amended by D6, D10, D18, D25, D27, D29, D41, D47, D51, D356, D190, D364) | §4 Config |
| D3 | 2026-10-15 | Config has no budget or concurrency limits | in force (amended by D46) | §4 Config |
| D4 | 2026-10-15 | Dispatch is by tag only, never by company | in force (amended by D7, D18, D25) | §5 Dispatch |
| D5 | 2026-10-15 | Time is the material's own time and the run's day | in force (amended by D7, D9, D10, D12) | §1 System |
| D6 | 2026-10-15 | The research universe is its own module | in force (amended by D10, D18, D59) | §2 Research universe |
| D7 | 2026-10-15 | No input store; replay is a test database, not a design concern | in force (amended by D10, D17, D18, D26) | §1 System |
| D8 | 2026-10-16 | Classification's lookup tables: one data file, results are tags | in force (amended by D15) | §3 Classification |
| D9 | 2026-10-16 | A day is cut in New York time; only the day counts | in force (amended by D12, D31, D34) | §1 System |
| D10 | 2026-10-16 | The system starts at a stream of classified items | in force (amended by D12, D17) | §1 System |
| D11 | 2026-10-16 | Related objects and the theme library | in force (amended by D18, D26, D38, D59) | §2 Research universe |
| D12 | 2026-10-16 | No current-day clock in the system | in force (amended by D31, D56) | §1 System |
| D13 | 2026-10-16 | The system is driven by information, not by the calendar | in force (amended by D14) | §1 System |
| D14 | 2026-10-16 | Two modes, designed apart: stream and pull | in force (amended by D29, D31, D54, D356) | §1 System |
| D15 | 2026-10-16 | Macro, political and economic material in the classification | in force | §3 Classification |
| D16 | 2026-10-16 | A human review pool for what the tables do not know | in force (amended by D27, D31, D33, D41, D45, D47) | §9 Review pool |
| D17 | 2026-10-16 | Receive is merged into dispatch | in force (amended by D18, D25) | §5 Dispatch |
| D18 | 2026-10-16 | One switch: the universe decides what is processed | in force (amended by D24, D25, D28) | §2 Research universe |
| D19 | 2026-10-16 | Freeze v1: everything up to classification | in force (amended by D24, D25, D27, D28, D29, D30, D31, D32, D34, D37) | §1 System |
| D20 | 2026-10-16 | A PRD per module, in Markdown, viewable from the design page | in force (amended by D242) | §15 Working rules |
| D21 | 2026-10-16 | Any change refreshes everything, by one command | superseded by D22 | Working rules |
| D22 | 2026-10-16 | Refreshing is a reasoning pass; the script only checks | in force (amended by D25, D26, D29, D36, D356) | §15 Working rules |
| D23 | 2026-10-16 | Tables without XBRL tags are read by the model | in force (amended by D24, D25, D27) | §6 Extraction |
| D24 | 2026-10-16 | Financial reports are not streamed; pull mode reads them when a thesis needs them | superseded by D28 | Universe |
| D25 | 2026-10-16 | One extraction module, read by category from a senior hedge fund analyst's view | in force (amended by D26, D27, D33, D35, D41, D42, D59, D264) | §6 Extraction |
| D26 | 2026-10-18 | The views database is the system's core | in force (amended by D33, D38) | §7 Thesis library |
| D27 | 2026-10-18 | Extraction reads the whole item by category, then matches it against the drivers | in force (amended by D32, D33, D39, D351) | §6 Extraction |
| D28 | 2026-10-18 | Financial reports stream again | in force | §1 System |
| D29 | 2026-10-18 | A final verdict before any view is closed | superseded by D41, D54, D356 | Closing and pull mode |
| D30 | 2026-10-18 | Conflicting sources and the consensus | in force (amended by D38, D45, D51, D260, D263) | §7 Thesis library |
| D31 | 2026-10-18 | Order, one writer, and the link between the levels | in force (amended by D38, D39, D42, D45, D46, D55, D57, D251, D264) | §1 System |
| D32 | 2026-10-18 | Table data comes one release at a time; XBRL is not pushed again | in force | §3 Classification |
| D33 | 2026-10-18 | Extraction only reads; matching and writing belong to the views database | in force (amended by D39, D42) | §6 Extraction |
| D34 | 2026-10-18 | An SEC filing is dated by the day SEC makes it public | in force | §1 System |
| D35 | 2026-10-18 | Extraction v1 is final | superseded by D37, D274 | Extraction |
| D36 | 2026-10-18 | One word per concept in the input and extraction modules | in force (amended by D41, D47, D52, D54, D57, D163) | §15 Working rules |
| D37 | 2026-10-18 | Freeze v1 of the input side and extraction | in force (amended by D41, D51, D58, D59) | §1 System |
| D38 | 2026-10-20 | The views database rebuilt: a view is a question with a five-rung ladder and a due date | in force (amended by D42, D45, D46, D51, D54, D57, D58, D185, D186, D198, D260) | §7 Thesis library |
| D39 | 2026-10-20 | Writing into the views database: match by where a candidate belongs, then one round of re-judging | in force (amended by D42, D44, D45, D46, D51, D63, D155, D169, D202, D204) | §7 Thesis library |
| D40 | 2026-10-20 | The matching judge: a general model first, every match recorded, humans label, a small model later | in force (amended by D42, D44, D45, D46, D169, D190) | §7 Thesis library |
| D41 | 2026-10-20 | What the rebuilt views database changes outside it | in force (amended by D42, D45, D51, D54, D190, D191, D195, D356, D374) | §4 Config |
| D42 | 2026-10-20 | Extraction hands over evidence and candidate views as two things; evidence is matched to what its view alre… | in force (amended by D45, D58, D59, D198, D202, D204, D207, D264, D360, D364) | §6 Extraction |
| D43 | 2026-10-20 | A second stable version of the design is sealed | in force (amended by D44, D50, D61) | §15 Working rules |
| D44 | 2026-10-20 | Matching is the model's alone: no key matched by code | superseded by D45, D58, D153, D155, D169, D197 | Thesis library |
| D45 | 2026-10-20 | Only what Alex said or decided is decided; Claude's proposals are listed apart | in force (amended by D46, D54) | §15 Working rules |
| D46 | 2026-10-20 | Alex decides Claude's views proposals one by one | in force (amended by D51, D54, D58, D63, D155, D169, D185, D191, D197, D198, D202, D204) | §7 Thesis library |
| D47 | 2026-10-20 | End-to-end consistency from the universe to the views database | in force (amended by D52, D163, D169, D190) | §7 Thesis library |
| D48 | 2026-10-20 | The views database, with match labelling, is frozen as version 1 | in force (amended by D51, D54, D55, D56, D57, D58) | §1 System |
| D49 | 2026-10-20 | Code review of the frozen views database: contradictions fixed, no new mechanism | record | Thesis library |
| D50 | 2026-10-20 | Clean-up after the freeze | record | Operations |
| D51 | 2026-10-21 | Claude's open items settled: one re-judging rule, dependencies chosen in the matching call, no consensus | in force (amended by D54, D58, D63, D190, D191, D195, D368) | §7 Thesis library |
| D52 | 2026-10-21 | Plain, consistent wording across the design page and PRDs | in force (amended by D163) | §15 Working rules |
| D53 | 2026-10-21 | A full line-by-line read of the page and PRDs, in rounds | record | Working rules |
| D54 | 2026-10-21 | A view's state is frozen at its due date; pull mode runs at the end of the day | in force (amended by D356) | §7 Thesis library |
| D55 | 2026-10-22 | The final verdict checked against the rebuilt views database; a removed object's views stop updating | in force (amended by D57, D356) | §7 Thesis library |
| D56 | 2026-10-22 | A full sweep before sealing v12 | in force (amended by D57) | §1 System |
| D57 | 2026-10-22 | A view has one switch: open or closed | in force (amended by D58) | §7 Thesis library |
| D58 | 2026-10-22 | A deep review before freezing everything but pull mode | in force (amended by D59, D60, D185) | §1 System |
| D59 | 2026-10-22 | How a candidate view names its object; a view from Alex's own memo | in force (amended by D60) | §6 Extraction |
| D60 | 2026-10-22 | The deep review again, after D59 | in force | §6 Extraction |
| D61 | 2026-10-22 | Clean-up: a code review, bloat removed, superseded seals out of the tree | record | Operations |
| D62 | 2026-10-23 | The POC build: Alex's choices, in his words | in force (amended by D217, D234, D351) | §1 System |
| D63 | 2026-10-24 | Re-judging once a day; the first window ends on 2026-08-15 | in force | §1 System |
| D64 | 2026-10-24 | Hide the mock header's date label | in force | [frontend](DECISIONS-frontend.md) |
| D65 | 2026-10-24 | Remove black focus outlines from the mock | in force (amended by D313, D314) | [frontend](DECISIONS-frontend.md) |
| D66 | 2026-10-24 | Remove the canvas hint and shorten the search field | in force (amended by D277, D313) | [frontend](DECISIONS-frontend.md) |
| D67 | 2026-10-24 | Simplify the view card headers | in force | [frontend](DECISIONS-frontend.md) |
| D68 | 2026-10-24 | Put the current judgment in the card header | in force (amended by D285, D287) | [frontend](DECISIONS-frontend.md) |
| D69 | 2026-10-24 | Use matching score circles on charts and state pills | superseded by D70 | Frontend |
| D70 | 2026-10-24 | Simplify the score display after visual review | in force (amended by D71, D285, D287) | [frontend](DECISIONS-frontend.md) |
| D71 | 2026-10-24 | Use black for Yes and white for No | in force (amended by D335, D336) | [frontend](DECISIONS-frontend.md) |
| D72 | 2026-10-24 | Remove redundant card footer tags | in force (amended by D124) | [frontend](DECISIONS-frontend.md) |
| D73 | 2026-10-24 | Use one title style across canvas cards | in force | [frontend](DECISIONS-frontend.md) |
| D74 | 2026-10-24 | Remove the change-summary line from view cards | in force | [frontend](DECISIONS-frontend.md) |
| D75 | 2026-10-24 | Give daily evidence volume its own chart band | in force (amended by D80, D117, D124) | [frontend](DECISIONS-frontend.md) |
| D76 | 2026-10-24 | Hivemind is a database with a search engine on top; the caller chooses | in force (amended by D78, D91, D112, D132) | §12 Idea API and service |
| D77 | 2026-10-24 | Label the state chart | in force (amended by D79, D117, D118) | [frontend](DECISIONS-frontend.md) |
| D78 | 2026-10-24 | Name the user input Idea and stored questions Thesis | in force | [frontend](DECISIONS-frontend.md) |
| D79 | 2026-10-24 | Align plot headings to the number column | in force | [frontend](DECISIONS-frontend.md) |
| D80 | 2026-10-24 | Give the due date a separate card footer | retired (D124) | Frontend |
| D81 | 2026-10-24 | Simplify the thesis detail panel | in force (amended by D88, D93, D94, D97, D116, D119, D120, D275) | [frontend](DECISIONS-frontend.md) |
| D82 | 2026-10-24 | Use the same font for dates and labels | in force | [frontend](DECISIONS-frontend.md) |
| D83 | 2026-10-24 | Center the fan-out and animate connected edges on hover | in force (amended by D84, D87, D137, D295, D316, D138, D290) | [frontend](DECISIONS-frontend.md) |
| D84 | 2026-10-24 | Use right-angle connectors | in force (amended by D137) | [frontend](DECISIONS-frontend.md) |
| D85 | 2026-10-24 | Thin connectors with directional arrowheads | in force (amended by D293, D323) | [frontend](DECISIONS-frontend.md) |
| D86 | 2026-10-24 | Replace Idea and Thesis header icons | in force | [frontend](DECISIONS-frontend.md) |
| D87 | 2026-10-24 | Hover highlights only the path into a card | in force | [frontend](DECISIONS-frontend.md) |
| D88 | 2026-10-24 | Refine detail controls, dates and source presentation | in force (amended by D94, D100, D107, D108, D109, D275) | [frontend](DECISIONS-frontend.md) |
| D89 | 2026-10-24 | Give the detail panel a clear visual hierarchy | in force (amended by D92, D103, D94, D95, D96, D98) | [frontend](DECISIONS-frontend.md) |
| D91 | 2026-10-24 | An idea the library holds no view on gets null | in force (amended by D132) | §12 Idea API and service |
| D92 | 2026-10-24 | Keep the existing monochrome theme | in force (amended by D284) | [frontend](DECISIONS-frontend.md) |
| D93 | 2026-10-24 | Simplify detail sections and move the due date | in force (amended by D95, D101) | [frontend](DECISIONS-frontend.md) |
| D94 | 2026-10-24 | Merge the current assessment and its reasoning | in force (amended by D96, D98) | [frontend](DECISIONS-frontend.md) |
| D95 | 2026-10-24 | Keep one divider at each section boundary | in force | [frontend](DECISIONS-frontend.md) |
| D96 | 2026-10-24 | Present the current assessment as a quote | in force (amended by D98) | [frontend](DECISIONS-frontend.md) |
| D97 | 2026-10-24 | Make the lower detail sections consistent accordions | in force (amended by D102, D275) | [frontend](DECISIONS-frontend.md) |
| D98 | 2026-10-24 | Highlight the assessment row with a quote accent | in force | [frontend](DECISIONS-frontend.md) |
| D99 | 2026-10-24 | Put the related-thesis arrow before the title | retired (D275) | Frontend |
| D100 | 2026-10-24 | Animate all detail expansions consistently | in force (amended by D105) | [frontend](DECISIONS-frontend.md) |
| D101 | 2026-10-24 | Separate the header dates with vertical bars | in force | [frontend](DECISIONS-frontend.md) |
| D102 | 2026-10-24 | Shorten the evidence heading and use solid disclosure triangles | in force | [frontend](DECISIONS-frontend.md) |
| D103 | 2026-10-24 | Align detail labels and values at one readable size | in force (amended by D114) | [frontend](DECISIONS-frontend.md) |
| D104 | 2026-10-24 | A theme holds a document only if it can move a thesis; Commerce anti-dumping notices do not | in force | §2 Research universe |
| D105 | 2026-10-24 | Animate disclosure content without moving its heading | in force | [frontend](DECISIONS-frontend.md) |
| D106 | 2026-10-24 | Reserve scrollbar space without a track divider | in force | [frontend](DECISIONS-frontend.md) |
| D107 | 2026-10-24 | Put expanded evidence dates after its sources | in force (amended by D108, D109) | [frontend](DECISIONS-frontend.md) |
| D108 | 2026-10-24 | Combine source, type and date on one attribution line | in force (amended by D109) | [frontend](DECISIONS-frontend.md) |
| D109 | 2026-10-24 | Show the source in collapsed evidence rows too | in force | [frontend](DECISIONS-frontend.md) |
| D110 | 2026-10-24 | Show thesis status in a pill | in force | [frontend](DECISIONS-frontend.md) |
| D111 | 2026-10-24 | Use an in-page evidence type menu | in force | [frontend](DECISIONS-frontend.md) |
| D112 | 2026-10-24 | The service runs in Docker; the FE asks it to read an idea; the user's thesis is the idea card | in force (amended by D134, D135, D280, D290, D335) | §12 Idea API and service |
| D113 | 2026-10-24 | Add the colon to canvas due dates | retired (D124) | Frontend |
| D114 | 2026-10-24 | Present score definitions as a table | in force | [frontend](DECISIONS-frontend.md) |
| D115 | 2026-10-24 | Use a uniform Score change heading | in force | [frontend](DECISIONS-frontend.md) |
| D116 | 2026-10-24 | Simplify history navigation to two right-aligned buttons | in force (amended by D120) | [frontend](DECISIONS-frontend.md) |
| D117 | 2026-10-24 | Strengthen chart headings and separate the two plots | in force (amended by D118, D124) | [frontend](DECISIONS-frontend.md) |
| D118 | 2026-10-24 | Keep canvas chart subtitles smaller than detail headings | in force | [frontend](DECISIONS-frontend.md) |
| D119 | 2026-10-24 | Inspect and anchor history by date | in force (amended by D120, D121, D122) | [frontend](DECISIONS-frontend.md) |
| D120 | 2026-10-24 | Remove the History hover label and navigation buttons | in force | [frontend](DECISIONS-frontend.md) |
| D121 | 2026-10-24 | Make quiet-day History selection explicit | in force (amended by D122) | [frontend](DECISIONS-frontend.md) |
| D122 | 2026-10-24 | Lock clicked History anchors and keep endpoint dots whole | in force | [frontend](DECISIONS-frontend.md) |
| D123 | 2026-10-24 | Remove the current-date dashed line from canvas cards | in force | [frontend](DECISIONS-frontend.md) |
| D124 | 2026-10-24 | Remove canvas card footers | in force | [frontend](DECISIONS-frontend.md) |
| D125 | 2026-10-24 | Center the initial graph in the usable canvas | in force (amended by D315, D316, D328) | [frontend](DECISIONS-frontend.md) |
| D126 | 2026-10-24 | Add the black TrueNorth mark beside Hivemind | in force | [frontend](DECISIONS-frontend.md) |
| D127 | 2026-10-24 | Balance the Hivemind wordmark with its logo | in force | [frontend](DECISIONS-frontend.md) |
| D128 | 2026-10-24 | Enlarge and center canvas navigation controls | in force | [frontend](DECISIONS-frontend.md) |
| D129 | 2026-10-24 | Keep only Full and Last 30 days | in force | [frontend](DECISIONS-frontend.md) |
| D130 | 2026-10-24 | Modular Thesis UI with a versioned data contract | in force (amended by D275) | [frontend](DECISIONS-frontend.md) |
| D131 | 2026-10-24 | Remove native hover text from card UI | in force | [frontend](DECISIONS-frontend.md) |
| D132 | 2026-10-24 | Probing the idea route: aliases from the universe, Chinese text terms, a floor under null | in force | §12 Idea API and service |
| D133 | 2026-10-24 | Everything in data and code is English from now on, natively | in force (amended by D152, D163) | §1 System |
| D134 | 2026-10-24 | The idea is read by an agent that calls Hivemind, the way a fresh Luna with the MCP would | in force (amended by D135) | §12 Idea API and service |
| D135 | 2026-10-24 | The service does the looking up; the model is asked twice | in force (amended by D145, D280, D290, D335) | §12 Idea API and service |
| D136 | 2026-10-24 | Slide the Thesis detail drawer open and closed | in force | [frontend](DECISIONS-frontend.md) |
| D137 | 2026-10-24 | Keep card connectors separate and attached to their cards | in force (amended by D295) | [frontend](DECISIONS-frontend.md) |
| D138 | 2026-10-24 | Idea cards share the Thesis header and connect every mapped thesis directly | in force (amended by D290, D307) | [frontend](DECISIONS-frontend.md) |
| D139 | 2026-10-24 | Evaluate overarching main theses before building the next layer | record | Thesis library |
| D140 | 2026-10-24 | Validate only two main-thesis update paths | record | Thesis library |
| D141 | 2026-10-24 | Validate code-owned sources and current evidence before summaries | record | Thesis library |
| D142 | 2026-10-24 | Test organization inside ingestion, not after extraction | record | Thesis library |
| D143 | 2026-10-24 | Test one owner for ingestion relationships | record | Thesis library |
| D144 | 2026-10-25 | Research continuing subject identity inside ingestion | record | Thesis library |
| D145 | 2026-10-25 | The idea card keeps the full mapping contract | in force (amended by D280, D289, D290, D335) | §12 Idea API and service |
| D146 | 2026-10-25 | The idea gold set: twenty ideas judged as an analyst, authored by Claude, sealed | in force | §11 The ruler and measurement |
| D147 | 2026-10-25 | Continue grouping POCs with direct subject identity results | record | Thesis library |
| D148 | 2026-10-25 | Check grouping consistency by research meaning, not identical group counts | in force (amended by D149) | §11 The ruler and measurement |
| D149 | 2026-10-25 | Group association is required during extraction | in force (amended by D165, D166, D211, D257) | §7 Thesis library |
| D150 | 2026-10-25 | Test a source-based membership explanation within extraction | record | Thesis library |
| D151 | 2026-10-25 | Before the NVDA rerun: the two sessions merged, two prompt rules corrected and proven on stored requests | record | Extraction |
| D152 | 2026-10-25 | The rerun runs in Chinese first; grouping passes to Claude | superseded by D163, D165 | Operations |
| D153 | 2026-10-25 | Keyed views: the structural correction is the direction; the week run is read first | superseded by D155, D164 | Thesis library |
| D154 | 2026-10-25 | The keyed view contract as built and measured on the bootstrap documents (T1–T2d) | in force (amended by D155, D164, D167, D197, D258) | §7 Thesis library |
| D155 | 2026-10-25 | 清单是参考，先修身份，再按顺序验证归组 | in force (amended by D164, D167, D197, D248, D258) | §7 Thesis library |
| D156 | 2026-10-25 | 先校正归组验收，再评价模型方案 | record | Ruler and measurement |
| D157 | 2026-10-25 | 用当前中文管线验证 Ohio 两篇连续报道 | record | Thesis library |
| D158 | 2026-10-25 | 追查 Ohio 入口并在同一归组流程内对照 | in force | §6 Extraction |
| D159 | 2026-10-25 | 从抽取到入库重放，先修读取顺序，单独检验身份所需来源 | superseded by D211, D251, D264 | Extraction |
| D160 | 2026-10-25 | 按原意检验三篇连续抽取，不用错误合并掩盖提问失真 | record | Extraction |
| D161 | 2026-10-25 | 继续修抽取，把保留论据与新开问题分开 | record | Extraction |
| D162 | 2026-10-25 | 先验证分两步抽取的假设 | record | Extraction |
| D163 | 2026-10-25 | English for the maintained project | in force (amended by D368) | §1 System |
| D164 | 2026-10-25 | Claude builds the English library on Codex's plan; the watch list is a reference, not a gate | in force (amended by D359) | §7 Thesis library |
| D165 | 2026-10-25 | Research groups enter the default pipeline; a group is an ongoing matter, a company's own financial lines c… | in force (amended by D166, D211, D257) | §7 Thesis library |
| D166 | 2026-10-25 | Group identity and membership by names, in code | in force (amended by D211, D257) | §7 Thesis library |
| D167 | 2026-10-25 | No hard-coded identity for aggregates; the judge gets the evidence, the vocabulary gets the missing measure… | in force (amended by D168, D197, D202) | §7 Thesis library |
| D168 | 2026-10-25 | Four corrections found by the D167 measurement: one repeat rule, one replace definition, one succession rul… | in force (amended by D202, D204) | §7 Thesis library |
| D169 | 2026-10-25 | Jev is the default matching engine | in force (amended by D189, D190, D201, D359) | §7 Thesis library |
| D170 | 2026-10-25 | Phase close-out: what the code review removed, fixed and left | record | Operations |
| D171 | 2026-10-25 | Review and free proofs for the day-batch acceleration proposal | record | Operations |
| D172 | 2026-10-25 | Build the isolated ordered-concurrency POC | in force (amended by D181, D183) | §14 Operations |
| D173 | 2026-10-25 | Isolated provider smoke before a larger concurrency test | record | Operations |
| D174 | 2026-10-25 | Three-document end-to-end concurrency diagnostic | record | Operations |
| D175 | 2026-10-25 | Publish sequential cleanup separately from experiments | record | Operations |
| D176 | 2026-10-25 | Judge business-question coverage, not mandatory project cards | superseded by D243, D261 | Ruler and measurement |
| D177 | 2026-10-25 | Modify and test NAVER admission on one frozen context | record | Extraction |
| D178 | 2026-10-25 | Resume the isolated acceleration POC with the tested T6 role | record | Operations |
| D179 | 2026-10-25 | Roll back the unrelated extraction prerequisite | record | Operations |
| D180 | 2026-10-25 | Execute the existing implementation plan on the complete busy day | record | Operations |
| D181 | 2026-10-26 | The parallel day, measured end to end on live APIs, and promoted as an opt-in replay mode | in force (amended by D183) | §4 Config |
| D182 | 2026-10-26 | The parallel day over fifteen consecutive days, against the serial path, with no network | record | Operations |
| D183 | 2026-10-26 | The replay runs the parallel day by default | in force | §4 Config |
| D184 | 2026-10-26 | A candidate thesis opens for one of four reasons, stated in the answer | in force (amended by D185, D191, D210, D211, D236, D264) | §6 Extraction |
| D185 | 2026-10-26 | A binding obligation is due within 18 months and is exempt from the next-year rule | in force (amended by D210, D236) | §6 Extraction |
| D186 | 2026-10-26 | Asset-thesis rungs describe business outcomes; the favourable end is registered per thesis | in force (amended by D368) | §6 Extraction |
| D187 | 2026-10-26 | A company's own quantity sits under that company's object, private companies included | in force (amended by D191, D368) | §7 Thesis library |
| D188 | 2026-10-26 | The extraction gold: twenty cases labelled by the assistant this round, human review later | superseded by D243, D250, D261, D262 | Ruler and measurement |
| D189 | 2026-10-26 | poc-v25 is the replay default; the trace review names the next mechanisms | record | Extraction |
| D190 | 2026-10-26 | The collision judge: Jev for identity, the generative model for the analyst's question when a question may… | in force (amended by D196, D197, D258) | §4 Config |
| D191 | 2026-10-26 | Theme theses reach every company; no named dependant is required to open one | in force (amended by D195, D368) | §7 Thesis library |
| D192 | 2026-10-26 | Role v13 (tests instead of lists) fails its probe; wording is exhausted as a lever | record | Extraction |
| D193 | 2026-10-26 | Extraction coverage is at the model's steady state; the phase closes on v12 with the collision judge | in force (amended by D199, D200) | §6 Extraction |
| D194 | 2026-10-26 | The six persistent misses read against the transcripts: one gold key removed, five stand | record | Ruler and measurement |
| D195 | 2026-10-26 | The theme block: every asset thesis is judged with the open theme theses in view, and a changed theme concl… | in force | §7 Thesis library |
| D196 | 2026-10-27 | `poc-v29` (the theme block) is the replay default | record | Thesis library |
| D197 | 2026-10-27 | A shared quantity is one thesis per theme, measure and period; its wording is not identity | in force | §7 Thesis library |
| D198 | 2026-10-27 | A judgement reads the evidence in view, not everything in force | in force | §7 Thesis library |
| D199 | 2026-10-27 | One extraction call stays; its gate rule becomes decidable and the empty-answer exit goes (v16, poc-v32) | in force (amended by D200) | §6 Extraction |
| D200 | 2026-10-27 | Extraction v18 (`poc-v34`) is the production default | superseded by D210 | Extraction |
| D201 | 2026-10-27 | Steps 3 and 4: Jev gives opinions only, the library keeps sources and research arguments, a new question ne… | in force (amended by D202, D204) | §7 Thesis library |
| D202 | 2026-10-27 | The writer retires nothing on a matching label: a replacement is recorded as a revision and both pieces sta… | in force (amended by D203) | §7 Thesis library |
| D203 | 2026-10-28 | A statement day is an ISO day or unknown; the writer never fills it with the publication day | in force | §6 Extraction |
| D204 | 2026-10-28 | A repeat is stored as its own source record; the merge becomes a labelled relation | in force (amended by D248) | §7 Thesis library |
| D205 | 2026-10-28 | The judging call's output budget is 16,000 tokens | in force | §7 Thesis library |
| D206 | 2026-10-28 | Every open theme thesis is shown to every item's extraction (extraction v19, `poc-v35`) | superseded by D211, D264 | Extraction |
| D207 | 2026-10-28 | Statements are filed by a separate placement call under the one-home rule; an unfiled statement is kept (ex… | in force (amended by D209, D254, D259, D264, D265, D360, D364) | §6 Extraction |
| D208 | 2026-10-28 | The thesis tree: root quantities, a seeded driver layer per company, shared macro themes with declared chan… | in force (amended by D209, D253, D273, D368) | §7 Thesis library |
| D209 | 2026-10-28 | A statement no open question takes is dropped at extraction; evaluation reads the dropped record, not a sid… | in force (amended by D264; for the clean path by D382, D383) | §6 Extraction |
| D210 | 2026-10-28 | A binding obligation already taken on opens as an amount at the next annual filing (role-v21, `poc-v37`) | in force (amended by D236, D238, D239) | §6 Extraction |
| D211 | 2026-10-28 | The extraction request shows no thesis and no group: one sample per item, filing at the turn (role-v22, `po… | superseded by D251, D264 | Extraction |
| D212 | 2026-10-28 | Measure retained content from source through final writing before another quality change | record | Ruler and measurement |
| D213 | 2026-10-28 | Trace the largest losses and restore a trustworthy preflight before comparisons | record | Ruler and measurement |
| D214 | 2026-10-28 | Reconcile the analyst standard before interpreting scores | in force (amended by D229, D244, D261) | §11 The ruler and measurement |
| D215 | 2026-10-29 | Record Alex's eleven analyst judgements without rewriting frozen data | record | Ruler and measurement |
| D216 | 2026-10-29 | Clarify that the FY2028 EPS forecast may be retained | in force | §11 The ruler and measurement |
| D217 | 2026-10-29 | Haiku as the target model; improve extraction pipeline steps 1–4 against the analyst's standard | superseded by D234 | Extraction |
| D218 | 2026-10-29 | Continue independently after the failed development acceptance | in force (amended by D228, D242) | §6 Extraction |
| D219 | 2026-10-29 | 订立分析师金标准 v4，分开投资价值、原意和记录错误 | superseded by D220, D229 | Ruler and measurement |
| D220 | 2026-10-29 | Judge necessary meaning by its investment consequence | in force (amended by D233) | §11 The ruler and measurement |
| D221 | 2026-10-29 | Judge evidence by the conclusion it can support, then test one action-rule change | in force | §11 The ruler and measurement |
| D222 | 2026-10-29 | Restructure the fourth-step research prompt against existing decisions, then compare without changing gold | record | Thesis library |
| D223 | 2026-10-29 | Test a single research note with references instead of repeated admission narratives | record | Thesis library |
| D224 | 2026-10-29 | Separate model capability from further prompt changes in the research experiment | record | Thesis library |
| D225 | 2026-10-29 | Correct the measurement and compare both models on the same prompt change | record | Ruler and measurement |
| D226 | 2026-10-29 | Focus on Haiku and judge useful research reasoning with evidence-relative strength | in force (amended by D234) | §11 The ruler and measurement |
| D227 | 2026-10-29 | Restore investment relevance without tightening the gold | record | Thesis library |
| D228 | 2026-10-29 | Put both existing analyst standards at the decision to work; stop for handoff | in force | §15 Working rules |
| D229 | 2026-10-29 | The analyst standard for extraction is signed off and does not drift; measure Haiku against it | superseded by D243, D261 | Ruler and measurement |
| D230 | 2026-10-29 | Haiku's output cap is 16k tokens; its thinking shares the cap with the answer | retired (D234) | Extraction |
| D231 | 2026-10-29 | The Singapore case is optional evidence, no longer excluded | in force | §11 The ruler and measurement |
| D232 | 2026-10-29 | The ruler checked against the raw answers; reference v2; four one-sentence prompt changes work on their pages | record | Ruler and measurement |
| D233 | 2026-10-29 | "This year" written as the company's fiscal year is correct | in force | §11 The ruler and measurement |
| D234 | 2026-10-29 | Haiku is parked; extraction work continues on gpt-6-luna | in force | §6 Extraction |
| D235 | 2026-10-29 | gpt-6-luna one-sentence arms: three changes work, three classes go to Alex | record | Extraction |
| D236 | 2026-10-29 | Three proposals approved; every change stays general (a hedge-fund brain, not an NVIDIA rule) | in force (amended by D246, D248, D266) | §6 Extraction |
| D237 | 2026-10-29 | The extraction prompt is a general hedge-fund brain: scrub it, then measure the whole bench | in force | §6 Extraction |
| D238 | 2026-10-29 | Extraction prompt work moves to a direct-read loop; role-v29 is the loop's current request | in force (amended by D239, D241, D244) | §15 Working rules |
| D239 | 2026-10-29 | role-v29 (`poc-v45`) is the extraction request; the bench loop stops | superseded by D245 | Extraction |
| D240 | 2026-10-29 | A named party's action without an amount is kept; a reject rule never removes what the standard keeps | in force | §11 The ruler and measurement |
| D241 | 2026-10-29 | One unified definition of the ledger's types, question opening and evidence levels, with a traced golden se… | in force (amended by D243, D261) | §11 The ruler and measurement |
| D242 | 2026-10-29 | The standard becomes a web page, the extraction step's PRD; AGENTS.md and the README are cleaned and carry… | in force (amended by D243) | §11 The ruler and measurement |
| D243 | 2026-10-29 | The extraction standard is signed: proposal 5 stricter, the other eleven at their leans; lean cautious, cat… | in force (amended by D248, D250, D261, D369; #4 overridden for the system by D385, frozen files unchanged) | §11 The ruler and measurement |
| D244 | 2026-10-29 | Claude sets the dev/test split; scores are leads and Claude reads the traces every time; first the role-v29… | in force (amended by D261) | §11 The ruler and measurement |
| D245 | 2026-10-30 | role-v42 (`poc-v58`) is the extraction request; its must-not questions on small release dates are the next… | superseded by D246 | Extraction |
| D246 | 2026-10-30 | role-v51 (`poc-v67`) is the extraction request | superseded by D247 | Extraction |
| D247 | 2026-10-30 | role-v53 (`poc-v69`) is the extraction request: the attribution fields are defined in the schema | superseded by D265 | Extraction |
| D248 | 2026-10-30 | What counts as one question and one piece of evidence: seven boundaries, chosen one by one | in force (amended by D257, D258, D368) | §6 Extraction |
| D249 | 2026-10-30 | A test the model applies to each statement is a check at the end of the same request; role-v63 (`poc-v79`)… | in force (amended by D265, D274) | §6 Extraction |
| D250 | 2026-10-31 | Four evidence boundaries and the counting unit settled; the ruler is fixed before any further measurement (… | in force (amended by D261) | §11 The ruler and measurement |
| D251 | 2026-10-31 | The extraction request may read the open questions as a daily snapshot (architecture under test) | superseded by D375 | §1 System |
| D252 | 2026-10-31 | The extraction prompt teaches what noise looks like, with general paired counter-examples; useful theses an… | in force | §6 Extraction |
| D253 | 2026-10-31 | D208's first step is built: seed questions for a covered company, written before the run, as homes for evid… | superseded by D370 | §7 Thesis library |
| D254 | 2026-11-01 | Placement: a question's code-written 'takes' line is the one rule for its file; D207's "company-wide figure… | in force (amended by D259, D264, D268, D273, D274) | §6 Extraction |
| D255 | 2026-11-01 | The extraction's one-line summary names the matter the statement belongs to (the next arm after D254's) | superseded by D256 | Extraction |
| D256 | 2026-11-01 | D255's sentence refuted by its proof; the mechanism is the undefined `links` field. One decider with the ar… | superseded by D264 | Extraction |
| D257 | 2026-11-01 | A declaration that is a stored group under other names gives the group those names (D166, the alias half);… | in force | §7 Thesis library |
| D258 | 2026-11-02 | Question identity brought in line with D248: a part of an open question is filed under it; `event` and `pol… | in force (amended by D354) | §7 Thesis library |
| D259 | 2026-11-02 | The takes line takes the evidence that bears on a question's answer, not only its own figures: D254's "dire… | in force (amended by D265, D273, D274) | §6 Extraction |
| D260 | 2026-11-02 | A judgement is a forecast against a reference: the rung the evidence in force makes most likely, judged aga… | in force (amended by D263) | §7 Thesis library |
| D261 | 2026-11-02 | A ruler or gold that is built and reviewed is never changed again | in force | §11 The ruler and measurement |
| D262 | 2026-11-02 | The judgement ruler (D3) and its gold are fixed: the gold is reader B's answers; frozen at sha256 636c056d1… | in force | §11 The ruler and measurement |
| D263 | 2026-11-02 | The judge is written to the frozen gold's own reasoning (judging-v7, poc-v91); a gap to the gold is closed… | in force (amended by D354, D359) | §7 Thesis library |
| D264 | 2026-11-02 | The extraction reads the day's open questions with their takes lines and files the statements itself (extra… | in force (amended by D265, D274, D359, D375) | §6 Extraction |
| D265 | 2026-11-02 | Extraction v72 / poc-v92 is the version: the default configuration, the base every later change builds on,… | in force (amended by D267, D272, D274, D359, D366, D364) | §6 Extraction |
| D266 | 2026-11-02 | Three quick fixes on the v72 base, each proved on stored data in minutes, put together as poc-v94 and run o… | in force | §6 Extraction |
| D267 | 2026-11-02 | poc-v94 is the default; no further three-draw runs for now; the extraction's remaining failures are read fr… | superseded by D272 | Extraction |
| D268 | 2026-11-02 | The first prompt audit's six fixes, each a contradiction or a missing example in the request, built as extr… | in force (amended by D274, D359) | §6 Extraction |
| D269 | 2026-11-03 | The second prompt audit, on the v95 draw: the one large class left is a precedence contradiction; the sente… | record | Extraction |
| D270 | 2026-11-03 | The structural fix built three ways (v78, v79, v80): the keep decision as closed-set fields the model fills… | record | Extraction |
| D271 | 2026-11-03 | The deep-review fixes on the v94 request: extraction v74d (`poc-v103`) is the candidate; proved on stored a… | record | Extraction |
| D272 | 2026-11-03 | `poc-v103` (extraction v74d) is the default | superseded by D274 | Extraction |
| D273 | 2026-11-03 | Second review of the extraction request: five misread sentences fixed in text (v74e), the filing structure… | record | Extraction |
| D274 | 2026-11-03 | The extraction production prompt is frozen at v74i (`poc-v108`); the unadopted variants are retired | in force (amended by D359, D366) | §6 Extraction |
| D275 | 2026-10-26 | Rebuild the frontend around the collected English library | in force (amended by D358) | [frontend](DECISIONS-frontend.md) |
| D276 | 2026-10-26 | Sentence-case interface labels and bar-separated metadata | in force (amended by D327) | [frontend](DECISIONS-frontend.md) |
| D277 | 2026-10-26 | Inline send control for Idea input | in force | [frontend](DECISIONS-frontend.md) |
| D278 | 2026-10-26 | Inspect the returned Idea analysis | in force (amended by D280, D308, D311) | [frontend](DECISIONS-frontend.md) |
| D279 | 2026-10-26 | Calculate and preview a composite-history Idea card | record | Idea and service |
| D280 | 2026-10-26 | Whole-card analysis and an analyst-written default TLDR | in force (amended by D282) | §12 Idea API and service |
| D281 | 2026-10-26 | Show actual Idea progress as a connected timeline | in force | §12 Idea API and service |
| D282 | 2026-10-26 | Make the composite chart a default Idea requirement | in force (amended by D288, D289, D290) | §12 Idea API and service |
| D283 | 2026-10-26 | Simplify the Idea score chart caption | in force (amended by D291) | [frontend](DECISIONS-frontend.md) |
| D284 | 2026-10-26 | Plain blue inline citations | in force | [frontend](DECISIONS-frontend.md) |
| D285 | 2026-10-26 | Put card scores beside their chart title | in force (amended by D286, D287) | [frontend](DECISIONS-frontend.md) |
| D286 | 2026-10-26 | Put the score pill below the chart title | superseded by D287 | Frontend |
| D287 | 2026-10-26 | Restore the score pill beside AI score | in force | [frontend](DECISIONS-frontend.md) |
| D288 | 2026-10-26 | Model-returned impact percentages and weighted Idea history | in force (amended by D289, D290) | §12 Idea API and service |
| D289 | 2026-10-26 | Let the model choose the weighted thesis set | in force | §12 Idea API and service |
| D290 | 2026-10-26 | An Idea contains only its positively weighted theses | in force (amended by D335) | §12 Idea API and service |
| D291 | 2026-10-26 | Display Idea confidence on a 0–100% scale | in force | §12 Idea API and service |
| D292 | 2026-10-26 | Label and rank Idea thesis weights | in force (amended by D294) | [frontend](DECISIONS-frontend.md) |
| D293 | 2026-10-26 | Slightly stronger default connectors | in force | [frontend](DECISIONS-frontend.md) |
| D294 | 2026-10-26 | Remove the weight tooltip and align the icon | in force | [frontend](DECISIONS-frontend.md) |
| D295 | 2026-10-26 | Increase default horizontal card spacing | in force | [frontend](DECISIONS-frontend.md) |
| D296 | 2026-10-26 | Match chart typography and fit the Idea card to content | in force | [frontend](DECISIONS-frontend.md) |
| D297 | 2026-10-26 | Confidence and creation date under the Idea detail title | in force | [frontend](DECISIONS-frontend.md) |
| D298 | 2026-10-26 | Simplify the Idea analysis and structure thesis explanations | in force (amended by D299, D303) | [frontend](DECISIONS-frontend.md) |
| D299 | 2026-10-26 | Replace the confidence table and paragraph with contextual help | in force (amended by D306) | [frontend](DECISIONS-frontend.md) |
| D300 | 2026-10-26 | Refine explanation labels and popup placement | in force (amended by D301, D306) | [frontend](DECISIONS-frontend.md) |
| D301 | 2026-10-26 | Restore section dividers and remove stacked spacing | in force | [frontend](DECISIONS-frontend.md) |
| D302 | 2026-10-26 | Balance confidence help and centre its icon | retired (D306) | Frontend |
| D303 | 2026-10-26 | Put the weight before the thesis title | in force | [frontend](DECISIONS-frontend.md) |
| D304 | 2026-10-26 | Organise the reading trace into expandable steps | in force (amended by D310) | [frontend](DECISIONS-frontend.md) |
| D305 | 2026-10-26 | Match weight badge height and optically align help | in force (amended by D306) | [frontend](DECISIONS-frontend.md) |
| D306 | 2026-10-26 | Name the adopted-thesis section and remove its help | in force | [frontend](DECISIONS-frontend.md) |
| D307 | 2026-10-26 | Give Idea and Thesis cards the same width | in force | [frontend](DECISIONS-frontend.md) |
| D308 | 2026-10-26 | Give Idea details Overview, Trace and Response tabs | in force (amended by D310, D311) | [frontend](DECISIONS-frontend.md) |
| D309 | 2026-10-26 | Remove search-count and mode subtitles | retired (D311) | Frontend |
| D310 | 2026-10-26 | Prioritise reading steps in Trace | in force (amended by D311) | [frontend](DECISIONS-frontend.md) |
| D311 | 2026-10-26 | Remove the Search trace UI | in force | [frontend](DECISIONS-frontend.md) |
| D312 | 2026-10-26 | Clean up the frontend without changing behaviour | record | Frontend |
| D313 | 2026-10-26 | Float and fold the Idea input | in force (amended by D314, D315, D316) | [frontend](DECISIONS-frontend.md) |
| D314 | 2026-10-26 | Smaller white launcher without a border | in force | [frontend](DECISIONS-frontend.md) |
| D315 | 2026-10-26 | Centre the generated Idea at readable size | in force (amended by D316, D328) | [frontend](DECISIONS-frontend.md) |
| D316 | 2026-10-26 | Balance the whole tree horizontally | in force (amended by D328) | [frontend](DECISIONS-frontend.md) |
| D317 | 2026-10-26 | Reveal the completed Idea tree in sequence | in force (amended by D320, D322, D328) | [frontend](DECISIONS-frontend.md) |
| D318 | 2026-10-26 | Retain the current Idea across workspace tabs | in force | [frontend](DECISIONS-frontend.md) |
| D319 | 2026-10-26 | Add an Idea confidence Trigger card | in force (amended by D321, D322, D323, D324, D326) | [frontend](DECISIONS-frontend.md) |
| D320 | 2026-10-27 | Scan the thesis reveal from top to bottom | in force | [frontend](DECISIONS-frontend.md) |
| D321 | 2026-10-27 | Move the Trigger to the left of the Idea | in force (amended by D322) | [frontend](DECISIONS-frontend.md) |
| D322 | 2026-10-27 | Show the Trigger last and simplify its comparison control | in force (amended by D323) | [frontend](DECISIONS-frontend.md) |
| D323 | 2026-10-27 | Trigger connectors have no directional arrowhead | in force | [frontend](DECISIONS-frontend.md) |
| D324 | 2026-10-27 | Style AI confidence as a selectable Trigger metric | in force | [frontend](DECISIONS-frontend.md) |
| D325 | 2026-10-27 | Use a bar slider handle and a metric value readout | in force (amended by D326) | [frontend](DECISIONS-frontend.md) |
| D326 | 2026-10-27 | Separate the current-value marker from the round threshold handle | in force | [frontend](DECISIONS-frontend.md) |
| D327 | 2026-10-27 | Rename the workspace navigation | in force | [frontend](DECISIONS-frontend.md) |
| D328 | 2026-10-27 | Add the Action preview and real NVIDIA prices | in force (amended by D329, D330, D331, D332, D333) | [frontend](DECISIONS-frontend.md) |
| D329 | 2026-10-27 | Remove the Action header badge | in force (amended by D331, D332) | [frontend](DECISIONS-frontend.md) |
| D330 | 2026-10-27 | Simplify Action text and cancel unfinished allocation edits | in force | [frontend](DECISIONS-frontend.md) |
| D331 | 2026-10-27 | Show Monitoring in the Action header | in force (amended by D332) | [frontend](DECISIONS-frontend.md) |
| D332 | 2026-10-27 | Use a pulsing black Monitoring dot | in force | [frontend](DECISIONS-frontend.md) |
| D333 | 2026-10-27 | Default the Action chart to one year | in force | [frontend](DECISIONS-frontend.md) |
| D334 | 2026-10-27 | Clean up frontend component ownership | record | Frontend |
| D335 | 2026-10-30 | Each adopted thesis offers only its own two endpoints; two-rung cards show their own Yes/No | in force | §12 Idea API and service |
| D336 | 2026-10-30 | A yes/no ladder with named outcomes shows its outcome once | in force | [frontend](DECISIONS-frontend.md) |
| D337 | 2026-10-27 | Create the Singapore Lightsail development server | record | Operations |
| D338 | 2026-10-27 | Test single-call extraction stability by correcting the task and preserving the request | in force | §6 Extraction |
| D339 | 2026-10-27 | Measure a source/route extraction POC against Luna and DeepSeek | record | Extraction |
| D340 | 2026-10-27 | Specify the source stage and research routing/admission before more model runs | record | Extraction |
| D341 | 2026-10-27 | Review routing traces as an analyst, preserving and combining the important information | record | Thesis library |
| D342 | 2026-10-27 | Run the Vera case before settling Jev and routing order | record | Thesis library |
| D343 | 2026-10-27 | Present pipeline inputs and outputs for review | record | System |
| D344 | 2026-10-27 | Verify source extraction and database retrieval separately | record | Extraction |
| D345 | 2026-10-27 | Implement and measure source fidelity and complete scoped retrieval | record | Extraction |
| D346 | 2026-10-27 | Rebuild the extraction evaluation around complete investment meaning | record | Ruler and measurement |
| D347 | 2026-10-27 | Test the frozen analyst extraction criteria and prompt | record | Extraction |
| D348 | 2026-10-27 | Compare stronger instructions and code-filled word references | record | Extraction |
| D349 | 2026-10-27 | Isolate full input/output demonstrations in the source experiment | record | Extraction |
| D350 | 2026-10-27 | Audit actual source/output before drawing model-quality conclusions | record | Ruler and measurement |
| D351 | 2026-10-27 | Clean the fed pages before the experiments; a later data pipeline owns the real feed | in force | §13 Data |
| D352 | 2026-10-27 | TrueNorth event index backfilled by identity; the result is a measurement, not a replacement | in force | §13 Data |
| D353 | 2026-11-03 | Clean the repository after the merge: experiment outputs and one-off scripts leave; documents and everythin… | record | Operations |
| D354 | 2026-11-03 | Steps 3 and 4 (opening and matching questions, judging them) are frozen as `poc-v108` runs them, after thre… | in force (amended by D359) | §7 Thesis library |
| D355 | 2026-11-04 | The filing topic closes without a change: filing is about 85% right; the remaining misses are recorded as k… | record | Current phase |
| D356 | 2026-11-04 | Step 5: closing at the due day is pull mode's; no separate final verdict, no day-end re-judging, due days a… | in force | §1 System |
| D357 | 2026-11-04 | Clean the repository of configurations and prompts nothing current names; the code paths of retired version… | record | Operations |
| D358 | 2026-10-28 | The three-month run stops at 2026-08-28 and is sealed; evidence bloat is the next problem to solve | in force | §13 Data |
| D359 | 2026-11-04 | The code builds only the frozen prompts (extraction v74i, judging-v7); old worktrees removed; the preflight… | in force (amended by D364, D365) | §6 Extraction |
| D360 | 2026-11-04 | PRD 10: the one-home tie and split replace the second home (§5.2); the decision rule counts against luck an… | in force | §10 Current phase: filing that links facts the way an analyst does |
| D361 | 2026-11-04 | After v74l's failed test: size what complete evidence is worth at the judgement before more extraction desi… | record | Current phase |
| D362 | 2026-11-04 | The two narrow delivery fixes the complete-evidence test points to are piloted, one at a time, on their mot… | record | Current phase |
| D363 | 2026-11-05 | At coverage start, the company's latest reported figures enter once from its own latest report; restatement… | superseded by D370 | §10 Current phase: filing that links facts the way an analyst does |
| D364 | 2026-11-05 | The coverage-start reading is built into the product; a figure several questions read is one record linked… | superseded by D370 | §4 Config |
| D365 | 2026-11-05 | The coverage-start reading is the third version with the repaired check; built into the product behind poc-… | superseded by D370 | §10 Current phase: filing that links facts the way an analyst does |
| D366 | 2026-11-05 | `poc-v116` is the replay default; the branch is committed and opened for review | superseded by D370 | §10 Current phase: filing that links facts the way an analyst does |
| D367 | 2026-11-05 | Decisions and working rules consolidated: a register of what is in force, the log kept whole; README, AGENTS and the state page cleaned | in force | [this page, opening](#consolidation) |
| D368 | 2026-11-05 | Alex's answers to the seven items left open by the consolidation | in force | §1, §6, §7, §8, §10, §11 |
| D369 | 2026-11-05 UTC | Capture core and supporting evidence without a strict boundary; retain the MXC case | in force | §11 The ruler and measurement |
| D370 | 2026-11-05 UTC | Remove the separate earnings-report import and preset starting questions | in force | Extraction and replay |
| D371 | 2026-11-05 UTC | Track present and forward-looking financial evidence | in force | §6 Extraction |
| D372 | 2026-11-05 UTC | Future evidence scoring uses helpful / not helpful, not separate core and supporting | in force (count existing gold without rewriting it) | §11 The ruler and measurement |
| D373 | 2026-11-05 UTC | Continue scoring against unchanged gold when a concern is disclosed | in force | §11 The ruler and measurement |
| D374 | 2026-11-05 | Remove the misleading model sampling setting | in force | §4 Config |
| D375 | 2026-11-05 | Read the latest committed research library before each item | in force; implementation and acceptance pending | §1 System and §6 Extraction |
| D376 | 2026-11-05 | Remove the evidence reader's 1 MB rejection | in force; catalog provision superseded by D377 | §1 System |
| D377 | 2026-11-05 | Remove the question-catalog 150 KB rejection | in force; changed and tested in main | §1 System |
| D378 | 2026-11-06 | The split extraction is sealed as a failed experiment; its useful lessons become production experiments (PRD 11) | in force; experiments open only on Alex's word | §6 Extraction |
| D379 | 2026-11-06 | The current version is sealed; Alex re-plans the system design | in force | [CURRENT_STATE](CURRENT_STATE.md) |
| D380 | 2026-11-08 | Clean Step 1 runs on K6b with DeepSeek Flash; a format failure, a cut answer included, is retried once | in force | clean-arch PRD §12 |
| D381 | 2026-11-08 | Clean Step 2: a repeat joins only the group it is most like; three acceptance lines; repeats keep their own text | in force | clean-arch PRD §§5–6 |
| D382 | 2026-11-08 | Financial figures are conditions, not theses; a thesis is a view with a reason | in force | clean-arch PRD §12 |
| D383 | 2026-11-08 | D209 amended again: a material statement no thesis takes is kept unlinked and linked later | in force; amends D209 | clean-arch PRD §§5, 12 |
| D384 | 2026-11-08 | Clean Step 1 opens only the big matters, by the signed standard as the frozen gold applies it | in force | clean-arch PRD §12 |
| D385 | 2026-11-08 | Target prices and valuation conclusions are not kept; the conflict with D243 #4 is disclosed, the frozen files unchanged | in force | clean-arch PRD §12 |
| D386 | 2026-11-08 | Acceptance on fresh articles read by readers against the source; golden-v5 test no longer held out | in force | clean-arch PRD §12 |
| D387 | 2026-11-09 | Clean Step 1 adopts c8; the PRD carries its system prompt, closing check and schema | in force | clean-arch PRD §12 |
| D388 | 2026-11-09 | A material unsigned obligation gets its own signing question beside an open total of its kind (confirms D248 boundary 1's exception) | in force | clean-arch PRD §12 |
| D389 | 2026-11-09 | Under D388, an unsigned obligation is large enough for its own signing question at about 5% of the company's most recent annual profit; an unstated amount is judged qualitatively | in force (focused step under test) | round log §55; clean-arch PRD on adoption |
| D390 | 2026-11-09 | Under D388, a plan counts as undertaken (tracked by its total, no signing question) once a deal under it is reported signed; each single deal keeps its own status | in force (focused step under test) | round log §57; clean-arch PRD on adoption |
| D391 | 2026-11-09 | Close clean Step 1 on c8 (focused D388 call not adopted); every change states its expected effect on a reader or the final judgement first (AGENTS §7.3) | in force | AGENTS §7.3; round log §59 |
| D392 | 2026-11-09 | Seeded end-to-end diagnostic of the clean system: the 22 seeds as a measurement-only fixture, a same-day v108 control via a separate harness, Stages 0–2 approved (Stage 2 runs if Stage 1 meets its frozen line) | in force | round log §60; council/en-claude.md |
| D393 | 2026-11-09 | After Stage 2 of D392 (clean +5, inconclusive on q12), fix capital spending (q12) first; c8 may change for it as a new version measured against c8; the unseeded measurement waits | in force | `clean-arch/q12-capex-2026-11-09/DESIGN.md`; round log §63 |
| D394 | 2026-11-10 | Capital spending (q12) is a known gap after arms c12 and c13 failed (the model does not recall the cash-flow identity unprompted); c8 stays; the unseeded measurement starts with its $0 question-matching stage, an addition to the measurement, with the paid draw on Alex's word | in force | round log §§64–65 |
| D395 | 2026-11-10 | Run the unseeded clean measurement: three draws from an empty library, opened questions matched by the frozen rule (MATCHING-v2) through an independent reading, graded on q04, q05, q08, q09, q13, q18 and q23, every other question reported | in force | `clean-arch/unseeded-2026-11-10/MATCHING-v2.md` |
| D396 | 2026-11-10 | Design the clean system's own judging step (Step 4): ladders and judgements for its own questions; first test is independent readers checking its answers against the sources; design and council before any code or paid send | in force | round log §67 |
| D397 | 2026-11-10 | Clean Step 4's ladder step: a topic that asks more than one thing gets one judged question (the part its outcome names); the other parts are shown as not judged; a departure from D38 for topics with two real bets, recorded as an open defect | in force | `clean-arch/step4-2026-11-10/DESIGN.md` §4 |
| D398 | 2026-11-10 | Clean Step 4's ladder step carries D186 in full: ranges stated against the reference (D260's list), the favourable end registered with its reason, rungs ordered and labelled by code; a number question with no reference is marked so | in force | `clean-arch/step4-2026-11-10/DESIGN.md` §4 |
| D399 | 2026-11-10 | The clean ladder request may teach how to build an event's five states (outcomes that exclude one another, one or two divided by a property that holds or does not), with a general example | superseded by D409 | `clean-arch/step4-2026-11-10/DESIGN.md` §5.2 |
| D400 | 2026-11-10 | Stage A of the clean ladder step is read against Alex's absolute lines with no paid control arm (an exception to AGENTS §7.3 for this first measurement); the lines are fixed; every report says it does not compare with production | in force | `clean-arch/step4-2026-11-10/DESIGN.md` §8 |
| D401 | 2026-11-10 | Once a fresh review finds nothing serious, the ladder step is built and Stage A sent without asking again, capped at $3; a missed line stops and goes to Alex; Stage B needs his word again | in force | `clean-arch/step4-2026-11-10/DESIGN.md` §8 |
| D402 | 2026-11-10 | Before more review or the build, the clean ladder step's request is sent once on six stored theses for a few cents, and the answers read by hand and reported to Alex; what follows is his to choose; D401's conditions stand | in force | `clean-arch/step4-2026-11-10/DESIGN.md` §8 |
| D403 | 2026-11-10 | On the clean ladder step an event's due day is a date the thesis or the article gives, or the last day of the thesis's period; the model picks no other day (narrower than v74i line 26, by Alex's decision) | in force | `clean-arch/step4-2026-11-10/DESIGN.md` §4 |
| D404 | 2026-11-10 | After the six-request probe: the model is asked which instruction led to each fault, the request is changed for the probe's three classes and a theme's state names may not be the company's labels, the same six are sent once more, and when the classes are gone the ladder step is built and Stage A sent on D401's terms with no further design-review round; if not gone, back to Alex | in force | `clean-arch/step4-2026-11-10/DESIGN.md` §8 |
| D405 | 2026-11-10 | The clean ladder step accepts a reference's words only as an unbroken passage of the article (spacing, case and quote-mark forms aside); otherwise the answer is refused and sent back once, and a second refusal writes no question | in force | `clean-arch/step4-2026-11-10/DESIGN.md` §5.3, check 6 |
| D406 | 2026-11-10 | On the clean ladder step the decision to decline and the naming of a theme's states move from sentences into the answer's shape (first fields: what the topic's outcome names and which is the main one; separate shapes for a company's and a theme's states); then eight stored theses are sent three times each and read as counts; when steady, the build follows on D401's terms | in force; its first point (the fields naming the main thing) superseded by D407 | `clean-arch/step4-2026-11-10/DESIGN.md` §5.2 |
| D407 | 2026-11-10 | One last probe of the clean ladder request (the first request plus the exact-copy and stand-alone sentences and separate shapes for company and theme states; eight theses, three sends, beside the first request as control), then the build whichever way it comes out: met (no-main topics declined 8 of 9, the others answered 15 of 15) the build uses it; missed, the first request unchanged with the faults of writing refused by code | in force | `clean-arch/step4-2026-11-10/DESIGN.md` §5.2 |
| D408 | 2026-11-10 | Stage A of the clean ladder step missed its lines: the work stays at the step; the event answers are changed first, checked at no cost and reviewed, then the same Stage A is run once more within D401's $3; the other classes follow one at a time; Stage B is not started | in force | `clean-arch/step4-2026-11-10/stage_a/result/RESULT.md`; `DESIGN.md` §8 |
| D409 | 2026-11-10 | On the clean ladder step an event is answered in at most three outcomes: it has happened by the due day, it is ruled out, or neither, the third written by code; finer differences are listed as not judged | in force; supersedes D399 | `clean-arch/step4-2026-11-10/DESIGN.md` §5 |
| D410 | 2026-11-10 | A group named in a judged question as the trade names it ("the big four AI hyperscalers") and not listed member by member is not a fault of the question (mark Q of the Stage A form) | in force | `clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md` |
| D411 | 2026-11-10 | A figure's reference may be the amount last reported when the article states no expectation, named as that and never as the market's expectation; a reference stated as a range is carried as a range; built and measured after the event answers | in force; built and probed, not yet measured | `clean-arch/step4-2026-11-10/DESIGN.md` §5.2.2 |
| D412 | 2026-11-10 | Every round is reflected on in the council to a recorded consensus, then the next test goes straight ahead, held to the PRD and its quantified goals; every trace is read by Claude itself | in force | AGENTS §7.3; round log §69 |
| D413 | 2026-11-10 | Where neither the topic nor the item settles it, an amount the company owes, guarantees or has committed to pay is registered with the lower end favourable; a topic that says more is good keeps "higher"; a tie rule in the request, the decision stays the model's | in force; built, measured in the third Stage A | `clean-arch/step4-2026-11-10/DESIGN.md` §5.2.4 |
| D414 | 2026-11-10 | Code sets the due day of a year's figure whose day would be an estimate: the fiscal year-end plus 60 days for the company, the calendar year-end plus 90 for a theme; a stated day is kept; a figure that is not a year's is dealt with first, apart | in force; built, measured in the third Stage A | `clean-arch/step4-2026-11-10/DESIGN.md` §5.2.4 |
| D415 | 2026-11-10 | The third Stage A of the clean ladder step is sent without asking again once each change (D413, D414, the scope of a ruling out, D411) is proved small and reviewed; a change that does not pass stops and goes to Alex; Stage B needs his word | in force | `clean-arch/step4-2026-11-10/DESIGN.md` §8 |
| D416 | 2026-11-10 | Alex's six lines stay; the ruling out of an event is tried as a typed answer (who decides, what they decide) and proved small on the six product-deadline theses beside the present shape before anything else | in force; passed its second trial alone, in the working request, measured in the fourth Stage A | `clean-arch/step4-2026-11-10/DESIGN.md` §5.2.5 |
| D417 | 2026-11-10 | A figure for a period that is not one year (a rolling twelve months) with no publication day in the texts is declined, with that reason | in force; proved small, in the working request | `clean-arch/step4-2026-11-10/DESIGN.md` §5.2.5; mark N of the Stage A form |
| D418 | 2026-11-10 | A government's or regulator's permission, restriction or ban on a class of products or trade belongs to the theme that covers it, also for the company's own product; a proceeding against the company itself stays the company's | in force; narrowed, passed alone, in the working request | `clean-arch/step4-2026-11-10/DESIGN.md` §5.2.5; mark O of the Stage A form |
| D419 | 2026-11-10 | The fourth Stage A is sent without asking again once each change (D416, D417, D418) is proved small and reviewed; a change that does not pass stops and goes to Alex; Stage B needs his word | superseded by D421 for these changes | `clean-arch/step4-2026-11-10/DESIGN.md` §8 |
| D420 | 2026-11-10 | A proceeding an authority conducts: a published closing decision is the event happened; its formal abandonment or withdrawal without the asked-for conclusion is the event ruled out; its still going on is the wait; such an event always has a ruling out; the question stays the one the thesis names | in force; passed alone, in the working request | `clean-arch/step4-2026-11-10/DESIGN.md` §5.2.5; mark R of the Stage A form |
| D421 | 2026-11-10 | D417 into the working request; then D420's rule, D418's narrowed sentence and the typed ruling out are each tested alone and reviewed; all passing, the fourth Stage A is sent without asking again; one failing stops and goes to Alex | in force | `clean-arch/step4-2026-11-10/DESIGN.md` §8 |
| D422 | 2026-11-10 | A second look by the model at its own answer (one more call, one instruction that names no fault) is tested small on 66 stored answers of the fourth Stage A, as a candidate; pass and fail written beforehand; whether the step adopts it is Alex's after the result | done; not adopted (D425). Run on 76 answers (the council corrected the grouping: 18 agreed, 18 disputed, 10 held, 30 unfaulted): it did not pass (6 of the 18 mended against 9; 3 of the 30 counted against it, the page fails at 3). Adoption is Alex's and is not decided | `clean-arch/step4-2026-11-10/probe-second-look-2026-11-10/RESULT.md` |
| D423 | 2026-11-10 | Work on Jev's revision relation stops (open defect); "a later version does not take the older record's questions" accepted as a direction, measured by the council and withdrawn by its author: the writer's rule stays, pending Alex's word | in force for the stop; the rule settled by D424 | `clean-arch/step2-revision-links-2026-11-10/LOG.md`; Step 2 log §§15–16 |
| D424 | 2026-11-10 | The clean writer keeps giving a "later version" the older record's questions (D202's rule); removing it is closed without a change; the carried context links are a recorded defect; "a company's answer sits wherever its report is filed" is not decided | in force | `clean-arch/step2-revision-links-2026-11-10/LOG.md` §6; Step 2 log §16 |
| D425 | 2026-11-10 | The ladder step takes no second look: the test (D422) did not pass; the step stays as it ran in the fourth Stage A | in force | `clean-arch/step4-2026-11-10/probe-second-look-2026-11-10/RESULT.md` |
| D426 | 2026-11-10 | The ladder step is not tuned further on the 44 theses and no fifth Stage A is sent; Stage A has not passed (lines 1, 3, 4 missed by 1 to 3 answers of 131); by his word the preparation of Stage B opens on that step, its $0 baseline reading of the 159 stored judgements first; no paid Stage B send without his word again | in force (an exception to D401's stop at a missed line) | `clean-arch/step4-2026-11-10/DESIGN.md` §8 |
| D427 | 2026-11-11 | Clean Step 2 (search, Jev comparison, best-match grouping, forward runner, Step 3 library) closed and frozen; not moved into production alone; goes to production with the whole clean path after Step 4 meets its lines, through an end-to-end comparison against production on the frozen ruler (three draws each) | in force | `tests/test_frozen_clean_step2.py`; clean-arch PRD §5; Step 2 log §19 |
| D428 | 2026-11-11 | Stage B's lines: decided figure-question judgements UNSUPPORTED at most 5 points above the baseline's (12.7% to 14.4%), yes/no at most 5%, last judgements at most 3 in 30 UNSUPPORTED with INSUFFICIENT beside; no overall line | in force | `clean-arch/step4-2026-11-10/stage_b/RESULT.md` |
| D429 | 2026-11-11 | Build the adapter's ladder mode ($0, tests, mutants, fresh reviews until one finds nothing serious), then send Stage B's three draws without asking again (cap $2), read each judgement alone with the baseline's form, controls and count | in force | `clean-arch/step4-2026-11-10/DESIGN.md` §5, §8 |
| D430 | 2026-11-12 | Stage B line 3: a figure control's due day counts as the ruler's when both mark the same period's publication; an event's deadline must be the ruler's; the literal reading counted beside | in force | `clean-arch/step4-2026-11-10/stage_b/STAGE_B_READING.md` |
| D431 | 2026-11-12 | D427's end-to-end comparison is against production as it now runs (no preset questions, D370), frozen ruler, same day (for a run longer than a day, D667), three draws each; the seven graded questions beside; the seeded comparison stays a diagnostic | in force | `clean-arch/step1-unfiled-2026-11-08/council/kr-consensus.md` |
| D432 | 2026-11-12 | After Stage B: diagnose how Step 1 cuts a matter into theses (the nine unopened graded questions, the eight theses with no ladder, the remaining Stage A faults); the diagnosis and one change, as a new Step 1 version measured on fresh articles, go to Alex before any build | in force | `clean-arch/step4-2026-11-10/PROGRESS-2026-11-12.md` |
| D433 | 2026-11-12 | Open Step 1 candidate c14: D38's year boundary carried into two merge sentences (+151 characters); first a small probe of c8 and c14 on stored articles with fixed stop lines; prompt audit and council before its first send; c8 stays in force until c14 is shown better on fresh articles | in force | `clean-arch/step1-diagnosis-2026-11-12/DIAGNOSIS.md` |
| D434 | 2026-11-13 | c14 stopped (stage 1: 7 of 9 against 8), c8 stays; diagnose the second-thing shapes at $0, then combine the year boundary, the customer-spending collision and that class, each shown small on stored data, into one Step 1 version measured once against c8 on fresh articles; the plan goes to Alex first | in force | `clean-arch/step1-diagnosis-2026-11-12/STAGE1-RESULT.md` |
| D435 | 2026-11-13 | Gate 1 of the combined Step 1 plan runs: G1-a years and customers together, G1-b customers alone, G1-c the outcome definition alone (preservation lines fixed by blind source readers first); c8 on every state; ceiling $2; audit and council before the send; a failed proof stops and goes to Alex | in force | `clean-arch/step1-diagnosis-2026-11-12/COMBINED-PLAN.md` |
| D436 | 2026-11-13 | A second side of the same bet is one question (context, shown as not judged, D397); change 3 dropped; G1-a and G1-b run without it; later gates use c8 with changes 1 and 2 | in force | `clean-arch/step1-diagnosis-2026-11-12/gate1/PREREAD-RESULT.md` |
| D437 | 2026-11-13 | Changes 1 and 2 (c15yc) go to gate 2 although G1-a missed its line (5 of 9 against 8); the failure stays recorded; gate 2's lines shown to Alex before any send; c8 in force | in force | `clean-arch/step1-diagnosis-2026-11-12/gate1/G1A-READING.md` |
| D438 | 2026-11-13 | Gate 2 sent as written (126 sends, ceiling $2.2); a stop or an unexercised control goes to Alex; a pass leads to gate 3's design shown to him first | in force | `clean-arch/step1-diagnosis-2026-11-12/GATE2.md` |
| D439 | 2026-11-13 | While Alex is not active, the council (independent Codex review + Claude) decides by consensus on the data and the PRD's goals; recorded, executed, measured, traces read, each round logged with its lesson; AGENTS limits stay; paid spending within $40 (Claude's setting) | in force | AGENTS.md, Authority and scope |
| D440 | 2026-11-13 | Gate 2 failed (memory article); council consensus: a 108-send memory diagnostic with a frozen non-inferiority rule (margin 22.2 points, inconclusive keeps c8) decides whether c15yc goes on | in force | `clean-arch/step1-diagnosis-2026-11-12/gate2/MEMORY-DIAGNOSTIC.md` |
| D441 | 2026-11-13 | Memory diagnostic: thesis outcome inconclusive (17 vs 28 of 54), retention proceed; c15yc stops, c8 stays; the year change is not tuned further on these articles (D391) | in force | `clean-arch/step1-diagnosis-2026-11-12/gate2/MEMORY-RESULT.md` |
| D442 | 2026-11-13 | Next step (council consensus, D439): D431's same-day end-to-end comparison as a diagnostic (clean path against production as it now runs (poc-v118, D370; corrected from v116), unseeded, three draws each, graded questions one by one, every lost answer read back); design frozen, $0 replay, cost estimate and council review before any send | in force | `clean-arch/step1-unfiled-2026-11-08/council/mk-codex-2.md` |
| D443 | 2026-11-13 | Shape B' (council consensus, D439): the stored clean chain against fresh production v118 draws as an exploratory census of final-answer losses; one-day slice first; one $5 shared ledger (conditional on stated bounds); shape A stays owed for D427 | in force | `clean-arch/e2e-comparison-2026-11-13/DESIGN.md` |
| D444 | 2026-11-13 | D443's draws stopped at the $5 ledger (an over-conservative Jev charge, $4.999 ledger against $0.98 recorded); three fresh draws from empty under a new $3 ledger with Jev settled at three times its usage (council consensus, D439); stopped draws kept as records | in force | `clean-arch/step1-unfiled-2026-11-08/council/ml-codex-9.md` |
| D445 | 2026-11-13 | Census: level on graded questions, every loss at opening; next a $0 path trace of the clean path's 17 graded opening losses, memory first, no repair until a cause is found (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/RESULT.md` |
| D446 | 2026-11-13 | Trace: no single mechanism; 7 certain and 2 uncertain breaches of the standard's unit rules; next a $0 audit of a narrow typed-unit contract on stored losses and correct controls, with a stop rule (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/AUDIT-CONTRACT.md` |
| D447 | 2026-11-13 | Typed-unit line stopped (audit: 2 of 16 detectable, none recovered); next a reviewed $0 design for the ladder step wired end to end and a diagnostic same-day run; the send decided after its review (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/AUDIT-RESULT.md` |
| D448 | 2026-11-13 | Wiring contract settled (design v4); build the wiring and its $0 proof, then code review; the slice and the full run each by its own later decision (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/WIRING-DESIGN.md` |
| D449 | 2026-11-13 | Wiring code review: shared stops read before every send, launcher liveness by its registered lock, the agreed reservation bound, the real orchestration proved; redo of Step 1, Step 2, production only by a reasoned relaunch; a crash stops the run (council consensus, D439; across draws, replaced for the release comparison by one ledger per draw, D667) | in force | `clean-arch/e2e-comparison-2026-11-13/run_fresh.py` |
| D450 | 2026-11-13 | Launch the slice: 2026-07-01 through the wired clean path (ladder pass 1) and production v118, live, on its own $1.50 ledger; a wiring check, every trace read; the full run by a later decision (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/preflight/PREFLIGHT-SLICE.md` |
| D451 | 2026-11-13 | Launch the full run: clean c1–c3 (ladder three passes) and production p1–p3 for 2026-07-01..07-14, same day, ledger $14.84; readings committed before the send (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/READING-COMMITMENT.md` |
| D452 | 2026-11-13 | The full run's reading plan: census rules as written; Stage A line 5 scaled as a council-set diagnostic line (never Alex's); new planted answers for Stage B; two gates of fresh-input checks (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/READING-PLAN.md` |
| D453 | 2026-11-13 | Redo c2's Step 1 from empty after a dropped response at item 56 (an eligible transport failure under D449); no ceiling change (council consensus, D439) | in force | `poc/data/clean-e2e-full-2026-11-13/c2/run.json` |
| D454 | 2026-11-13 | Full run read so far: census clean ≈ production, every loss at opening; Stage A missed on fresh theses; readings continue: loss-trace marks, then Stage B (gate 2), then a reflection on question scope and deadline (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/CENSUS-FULL-RESULT.md` |
| D455 | 2026-11-13 | Full run: Stage B line 3 unexercised under every treatment (0 settled, at most 4 controls with material shown); the judgement reading stops (a recorded departure from D452/D454); next the reflection on question scope and deadline (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/CENSUS-FULL-RESULT.md` |
| D456 | 2026-11-13 | Next angle: trace at $0 production's kept-but-unlinked facts (phase 10's blocker) beside the clean path's delivery of the same facts; falsifiers stated; opening stays out of scope until established (council consensus, D439) | in force | `clean-arch/step1-unfiled-2026-11-08/council/mt-codex-2.md` |
| D457 | 2026-11-13 | Production's unlinked facts: three mechanisms, no final-answer loss shown in this window (D456's falsifier fired); next a $0 review of the opening losses, four outcomes per case, no automatic thresholds (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/unlinked-trace/UNLINKED-TRACE-RESULT.md` |
| D458 | 2026-11-13 | Opening review: shown breaches small and spread (M2 4, M4 3, M5 3, M6 2, M1 2 + 5 unresolved, M3 unresolved); largest classes left open by the standard; no opening phase; next a $0 trace of Stage A's agreed answer-choice failures (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/opening-review/OPENING-REVIEW.md` |
| D459 | 2026-11-13 | Stage A's first-pass faults: no class (D458's falsifier fired); next the standard's tests on q09, q18, q05 case by case and the model's account on seven unresolved cases, ceiling $0.50 (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/stage-a-trace/STAGE-A-TRACE-RESULT.md` |
| D460 | 2026-11-13 | Accounts make M1 (7 draws, both systems) and M4 (5 of 6 clean) strong leads; a standard line is missing from clean Step 1's request; next a whole-request $0 prompt audit of clean Step 1, identity first, with a blind second reader (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/opening-review/D459-RESULT.md` |
| D461 | 2026-11-13 | Prompt audit of clean Step 1: identity boundaries missing (F1, F2), the shared-quantity date sentence contradicts the standard (F6); F6 designed and falsified first, identity deferred (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/step1-audit/AUDIT.md` |
| D462 | 2026-11-13 | F6 (the shared-quantity date sentence) recorded as a contradiction with uncertain standalone effect (decisive in 1–2 of 26 declines); status report for Alex first, then the $0 identity comparison (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/step1-audit/f6/` |
| D463 | 2026-11-13 | Identity lever: a general clause in clean Step 1 first (candidate c16), written with narrowed boundaries and two or three general examples per class, and a frozen fresh-article probe, both reviewed before any send (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/step1-audit/IDENTITY-COMPARISON.md` |
| D464 | 2026-11-13 | Send the case-specific identity diagnostic (c16 v5 against c8; one fresh story per target, 7 merge and 9 negative stories, stored guards), 258 jobs under one $5 ledger; result goes back to the council, never to adoption (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/identity-probe/v2/PROBE-DESIGN-v2.md` |
| D465 | 2026-11-13 | Identity diagnostic: the year boundary moved its error (2026 swapped for 2027); line stopped, c16 not adopted, c8 stays; Ohio clause and F6 kept as leads (council consensus) | in force | `clean-arch/e2e-comparison-2026-11-13/identity-probe/v2/RESULT.md` |
| D466 | 2026-11-13 | Deep reflection: stop circling; two choices for Alex (a real prior research library or an empty start; the three open shapes as targets or concerns); the clean ladder step measured on the same questions and facts, prepared at $0, sent only on his word; new guard lines proposed (council consensus) | in force | `clean-arch/step1-unfiled-2026-11-08/council/mu-codex-2.md` |
| D467 | 2026-11-13 | Ladder-cost measurement: feasible only with four more $0 proofs and a same-day control; it changes no final answer by itself, so it goes to Alex as a candidate beside the two pending choices (council consensus) | in force | `clean-arch/e2e-comparison-2026-11-13/ladder-cost/FEASIBILITY.md` |
| D468 | 2026-11-13 | Ladder-cost measurement stops at its $0 proofs (control rebuild, ladder swap, blind-chosen case articles kept as tools); forward work waits on Alex's two D466 choices; the measurement offered as an option (council consensus) | in force | `clean-arch/e2e-comparison-2026-11-13/ladder-cost/` |
| D469 | 2026-11-13 | Provisional (Alex not answering, D439): empty-start measurement; the three open shapes stay concerns; the ladder-step refusal fix starts with a $0 boundary check of every "no main" refusal (council consensus) | in force | `clean-arch/step1-unfiled-2026-11-08/council/mu-codex-6.md` |
| D470 | 2026-11-13 | Ladder-refusal candidate stopped (readers split on the boundary); 41 Stage A splits recorded, eight read provisionally by D414; Stage A verdict unchanged; the written-ladder line question opened for the council (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/stage-a-splits/splits.json` |
| D471 | 2026-11-13 | Written-ladder line kept; ten right-by-refusal theses traced (period rule read as a horizon in three); c17 (period sentence clarified) probed on stored cases under frozen lines (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/period-probe/PERIOD-PROBE-DESIGN.md` |
| D472 | 2026-11-13 | Period probe budget exception: the nine never-sent jobs sent alone under a $0.50 ceiling before any answer is read; the timed-out send stays missing (council consensus, D439) | in force | `clean-arch/step1-unfiled-2026-11-08/council/mu-codex-14.md` |
| D473 | 2026-11-13 | Period candidate c17 fails (target 0 of 3; memory-price theses 10 → 3, federal 3 → 0); not adopted; Step 1 sentence changes on these articles stop (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/period-probe/RESULT.md` |
| D474 | 2026-11-13 | Unsigned-deal candidate c18 (D388 at the binding-obligation definition) probed on unseen articles against the acceptance library: one target story, six negatives, guards (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/unsigned-deals/PROBE-DESIGN.md` |
| D475 | 2026-11-13 | c18 not adopted (unseen target not moved: 4 of 6 against c8 3 of 6; no regression; Ohio 6 of 9 against 0); D473 federal line within c8 variance (correction note) | in force | `clean-arch/e2e-comparison-2026-11-13/unsigned-deals/RESULT.md` |
| D476 | 2026-11-13 | Ladder-cost comparison not sent; next: a $0 two-reader source check of the eleven first-pass refusals (worth asking apart from can be laddered), no automatic threshold (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/reachability/` |
| D477 | 2026-11-13 | Reflection rounds 19–22: Stage A not passed; six of eleven refusals right, four runs reachable on paper; no H100 theme or ladder change; no more Step 1 sentence changes here; production stays default; choices written for Alex (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/reachability/RESULT.md` |
| D478 | 2026-11-13 | Council takes choice 2 under D439: c19 (the first step writes each new thesis's settling figure or event and fixed outcomes, schema only) probed on 18 stored states against c8 (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/outcomes-at-opening/PROBE-DESIGN.md` |
| D479 | 2026-11-13 | c19 fails (outcomes written at opening fail the standard's checks, 1 of 21; one target opened less); council takes choice 3: production stays default, next test from production's own stored losses (council consensus, D439) | in force | `clean-arch/e2e-comparison-2026-11-13/outcomes-at-opening/RESULT.md` |
| D480 | 2026-11-13 | Production's opening rule probed with a price (D191.4, D368.1) on 30 stored requests: the memory-price question never opened in 6 of 6 production draws (council consensus, D439) | in force | `docs/research/2026-11-13-shared-quantity-price/PROBE-DESIGN.md` |
| D481 | 2026-11-13 | Production price change fails (no memory candidate in 45 sends; fewer candidates, more no-home drops) and stops; next a $0 census of opening losses by what the article states (council consensus, D439) | in force | `docs/research/2026-11-13-shared-quantity-price/RESULT.md` |
| D482 | 2026-11-13 | No further paid test on this ruler that day; production stays default; clean path unchanged, Stage A not passed; the measured map and open disputes go to Alex (council consensus, D439) | in force | `docs/research/2026-11-13-shared-quantity-price/CENSUS-BY-ARTICLE.md` |
| D483 | 2026-11-14 | Deep reflection council: the way to production is a use-oriented acceptance (an addition beside the frozen ruler), prepared first at $0 on stored runs; to Alex (not decided) | accepted by D484 | `clean-arch/step1-unfiled-2026-11-08/council/mw-codex-2.md` |
| D484 | 2026-11-14 | Alex: "Open it, trial run first" — the use-oriented acceptance is opened beside the frozen ruler; a $0 trial run on stored runs first; design and lines to him before any paid run | in force | `docs/DECISIONS-log.md` D484 |
| D485 | 2026-11-14 | Trial design v3 goes to the readers; stop rule: findings the trial would reveal are its questions, not blockers (council consensus) | in force | `docs/research/2026-11-14-use-acceptance/TRIAL-DESIGN.md` |
| D486 | 2026-11-14 | Trial run read (leads, not a calibration that holds); acceptance design v3 (fresh 09-22..10-05, three draws per system, about $22) goes to Alex for lines and budget (council consensus) | to Alex | `docs/research/2026-11-14-use-acceptance/ACCEPTANCE-DESIGN.md` |
| D487 | 2026-11-14 | Lean path (Alex: "小步快跑"): step 1 builds nothing (source dates); step 2 one fresh week 09-22..28, one draw a system, slice first, decision rule written before reading (council consensus) | in force | `docs/research/2026-11-14-use-acceptance/LEAN-LOG.md` |
| D488 | 2026-11-14 | Clean Step 1 resends a dropped connection up to three attempts, each on the ledger and recorded (7 of 52 Step 1 traces had stopped on one); the clean week draw relaunched from empty (council consensus) | in force | `docs/research/2026-11-14-use-acceptance/NETWORK-RETRY-DESIGN.md` |
| D489 | 2026-11-14 | The fresh week (one draw a system): not clear by the rule written before reading, no system chosen; production covers 4 of 5 big matters and the clean path 2 (it lacks revenue and margin, D382/D384); whether the new system holds questions on the company's main numbers goes to Alex with three options (council consensus) | in force; Alex chose the test (D490) | `docs/research/2026-11-14-use-acceptance/week/WEEK-RESULT.md` |
| D490 | 2026-11-14 | Alex opens a test arm of clean Step 1 that may open questions on the company's revenue and margin ("试开这类问题"): a probe of a few cents on the stored week first, the second fresh week only if it meets its lines; D382 and D384 stay in force for the adopted path | in force; the test ran and its arm was stopped (D491) | `docs/research/2026-11-14-use-acceptance/LEAN-LOG.md` §4 |
| D491 | 2026-11-14 | The revenue-and-margin test arm (c20) opens the three questions with no number cards but fails its probe on a line written beforehand (the Vera Rubin question not opened, 0 of 3 against 2 of 3; cause not settled); stopped, not adopted; the next step goes to Alex (council consensus) | in force | `docs/research/2026-11-14-use-acceptance/main-numbers/RESULT.md` |
| D492 | 2026-11-14 | Alex asks for a deep council review of the traces and then the next step to try, without going in circles or repeating a mistake; the reflection council's consensus sets the next step within the standing limits | in force | `docs/research/2026-11-14-use-acceptance/LEAN-LOG.md` §5 |
| D493 | 2026-11-14 | Reflection council (D492): every change from D439 to D491 was words in the one Step 1 call and moved a neighbour; the reader's loss is around the company's main numbers; no further request change now; next a $0 test of the kept figures assembled as a company record; the standing-question comparison stays a candidate that goes to Alex first (D370) | in force | `docs/research/2026-11-14-use-acceptance/record/RECORD-TEST-DESIGN.md` |
| D494 | 2026-11-14 | The kept figures assembled as a company record ($0): measure and value right in all 40 rows read and five of six questions answered as from the articles, but the usability line is missed on a wrong attribution (who a figure is from is stored per statement, not per figure); three choices to Alex, the council leaning to a tested new version with per-figure source and a fixed-form period | in force; Alex chose the new version (D495) | `docs/research/2026-11-14-use-acceptance/record/RECORD-TEST-RESULT.md` |
| D495 | 2026-11-14 | Alex opens a test arm of clean Step 1 (c21): each kept figure carries its own source and a fixed-form period, two fields and no rule change; a guarded probe on stored states first, the record test on unread articles only if it passes | in force; the probe ran and is undecided (D496) | `docs/research/2026-11-14-use-acceptance/LEAN-LOG.md` §6 |
| D496 | 2026-11-14 | The figure-fields arm (c21) repairs the attribution of mixed statements (wrong parties 2.1% against 8.2%) with nothing else seen to move, but its probe is undecided and stops: the arm writes sources and fiscal years that articles imply and do not state; a stricter second version is a new candidate whose cost goes to Alex first (council consensus) | in force | `docs/research/2026-11-14-use-acceptance/figure-fields/RESULT.md` |
| D497 | 2026-11-15 | Alex approves a second version of the figure fields (c22: a source or fiscal year the article does not state stays empty) and its probe on other stored articles, about $0.90; the unread-article record test is asked of him after a pass | in force; the probe ran and is not a pass (D498) | `docs/research/2026-11-14-use-acceptance/LEAN-LOG.md` §7 |
| D498 | 2026-11-15 | The figure fields, second version (c22): no invented fiscal year, no unattributed forecast given to the company, the first version's gain kept and nothing else seen to move; not a pass by one figure on the all-figure source line (10 of 185 by the strict reading, 4 by the cases as written); c8 stays adopted; the next step goes to Alex with the council's and Claude's positions (council consensus on the verdict) | in force | `docs/research/2026-11-14-use-acceptance/figure-fields-2/RESULT.md` |
| D499 | 2026-11-15 | Alex waives the one-figure miss of D498 and opens the record test on unread articles: c8 and c22 each read about forty articles of the second fresh week, and the company record built from each is tested as in D494 (about $1) | in force; the test ran (D500) | `docs/research/2026-11-14-use-acceptance/LEAN-LOG.md` §8 |
| D500 | 2026-11-15 | The record test on unread articles: c8's record meets the line, c22's is undecided, and the comparison is not separated (the disputed readings are in both records but one); c22 is not adopted and the figure-fields line stops; c8 stays adopted; whether to test a financial record as something the product shows goes to Alex (council consensus) | in force | `docs/research/2026-11-14-use-acceptance/record-2/RECORD-TEST-2-RESULT.md` |
| D501 | 2026-11-15 | Alex opens a $0 test of a financial record as something the product shows: a code-only table from the stored answers of the forty unread articles (the same figure on one line, the article's wording and source kept, an uncertain period left as written), read by fresh readers | in force; the test ran (D502) | `docs/research/2026-11-14-use-acceptance/LEAN-LOG.md` §9 |
| D502 | 2026-11-15 | The table test: no wrong join found in the ten joined lines, all four table readers meet the written answer line, no reliable saving of effort shown; the table goes to Alex as a tested mock, not as the accepted handling of revenue and margin; D489's comparison unchanged; the next step is his (council consensus) | in force | `docs/research/2026-11-14-use-acceptance/record-3/TABLE-TEST-RESULT.md` |
| D503 | 2026-11-15 | Alex reviews the mock table and opens a $0 reading on the fresh week of D489: the same table from that week's stored answers, read blind for the three matters the new system had no question for; a separate question, D489's count unchanged | in force; the test ran (D504) | `docs/research/2026-11-14-use-acceptance/LEAN-LOG.md` §10 |
| D504 | 2026-11-15 | The table on the fresh week: M01 undecided, M02 and M03 not findable by the line; eleven of twelve key figures are in the table, two of four readers found all eleven; the table passes on stored-label faults; D489 unchanged ("not clear"), nothing ranks the systems; one product question goes to Alex: see the figures, a tracked question with a judgement, kept figures reaching related judgements, or several (council consensus) | in force | `docs/research/2026-11-14-use-acceptance/record-3/TABLE-WEEK-RESULT.md` |
| D505 | 2026-11-15 | Alex: the kept financial figures should reach the judgements of related questions (not a table, not questions of their own; D382 and D384 stand); first a $0 check on the stored fresh-week run: is a kept financial figure a judgement should have received absent from its request | in force; the check ran (D506) | `docs/research/2026-11-14-use-acceptance/LEAN-LOG.md` §11 |
| D506 | 2026-11-15 | The delivery check: one kept financial fact (NVIDIA's revenue opportunity per gigawatt) did not reach the credit-support question it bears on; six open leads; no missing figure established for five questions; the effect on the judgement not measured; nothing is built on one instance; an open defect of the new system; reported to Alex (council consensus) | in force | `docs/research/2026-11-14-use-acceptance/delivery/DELIVERY-CHECK-RESULT.md` |
| D507 | 2026-11-15 | Alex opens a $0 census of the class on the stored fresh-week run of the new system: every kept statement (those linked elsewhere included) against the seven questions: which bear on a question and never reached its judgement; scope widened by his word beyond the financial figures | in force; the census ran (D508) | `docs/research/2026-11-14-use-acceptance/LEAN-LOG.md` §12 |
| D508 | 2026-11-15 | The census of the class on the stored fresh-week run: three confirmed missing fact-and-question pairs in three of seven questions (one bears against a stored answer), 23 unresolved candidate pairs, a minimum and no rate; the effect on a judgement unmeasured; nothing built; a six-call test of the effect on the strongest case is offered to Alex (council consensus) | in force | `docs/research/2026-11-14-use-acceptance/delivery-class/CLASS-CENSUS-RESULT.md` |
| D509 | 2026-11-15 | Alex goes inactive ("我要睡觉了，下来你自行按照我的准则操作，需要深度的审视每一轮run 用council"): D439 in force again; Claude carries the lean path and the open defect of D506/D508 forward by his rules, each round examined in depth with the council; paid calls within D439's $40 ceiling | in force | `docs/DECISIONS-log.md` D509 |
| D510 | 2026-11-15 | Under D439 (council consensus, rounds 21 and 22): the six-call test of the effect of one missing fact (Beijing's 2025 RTX Pro 6000D stop order) on the stored judgement of the RTX Pro 5500 question is sent; outcomes fixed in advance; ceiling $0.25 | in force; the test ran (D511) | `docs/research/2026-11-14-use-acceptance/effect/EFFECT-TEST-DESIGN.md` |
| D511 | 2026-11-15 | Under D439: the six-call test is inconclusive (all six answers "yes"; the firmness rankings overlap; the judge marked the added statement against "yes" without naming it); the delivery line pauses, the change is deferred, the defect stays open; a cold reflection council comes next (council consensus) | in force | `docs/research/2026-11-14-use-acceptance/effect/EFFECT-TEST-RESULT.md` |
| D512 | 2026-11-15 | Under D439 (reflection council "my"): neither system has earned the choice and D489 stays "not clear"; the next step is a decision page for Alex on which system carries forward, prepared and reviewed while he is away; no further reading or send before it; production stays the default (council consensus) | in force | `docs/research/2026-11-14-use-acceptance/DECISION-PAGE-2026-11-15.md` |
| D513 | 2026-11-15 | Correction to D506 and D508: the new system has a later-linking step that judges earlier statements with no link against a newly opened question (516 judged, 2 linked in the week); one already linked elsewhere is not reconsidered; no count changes; the class had been traced on 2026-11-13 (D456) and was not cited | in force | `docs/DECISIONS-log.md` D513 |
| D514 | 2026-11-15 | Correction to D513's wording: the look-back rule is on groups and on how the original arrived (checked when the original statement arrived without a question; excluded when it arrived under another question); production does not link an earlier record back, and D456's no-loss finding is bounded to its graded questions and window | in force | `docs/DECISIONS-log.md` D514 |
| D515 | 2026-11-15 | Under D439 (reflection council, three readings): the decision page on which system carries forward is left for Alex; advice: keep today's default and both systems, do not choose from this evidence; the one test that could decide it is a comparison written down before it runs, opened only on his word; nothing further is sent or run on the lean path until he answers | in force; its wait superseded by D516 | `docs/research/2026-11-14-use-acceptance/DECISION-PAGE-2026-11-15.md` |
| D516 | 2026-11-15 | Under D439 (reflection council round 6): D515's wait is superseded; the next step is a $0 sizing and decision-ready design of the comparison (from D484 version 3 and the stored draws), with a stop condition, reviewed by the council before a separate decision on any send | in force | `docs/research/2026-11-14-use-acceptance/comparison/` |
| D517 | 2026-11-15 | Under D439 (reflection council round 7): the comparison is sized and not sent (at the proposed size it may miss differences that matter; its reliability cannot be calculated from the stored readings); no answer-choice tests to resume; the look-back not widened now; next a $0 side-by-side of the two systems' output on the fresh week, then a bounded council decision | in force | `docs/research/2026-11-14-use-acceptance/comparison/COMPARISON-SIZING.md` |
| D518 | 2026-11-15 | Under D439 (reflection council round 8): production stays the default and both systems stay (what would change it is named); the side-by-side is corrected and rebuilt; the next investigation is a $0 census of the stored answers readers did not pass, with a stop condition before anything is built | in force | `docs/research/2026-11-14-use-acceptance/side-by-side/`, `unsupported/` |
| D519 | 2026-11-15 | Under D439 (reflection council round 9): the side-by-side is left for Alex beside the decision page; the census of unsupported answers stands as corrected (31 of 36 settled failures: an amount asked with nothing enough to size it); four neutral accounts are asked of the frozen judge on stored answers, ceiling $0.10, raw accounts back to the council before any design | in force | `docs/research/2026-11-14-use-acceptance/unsupported/UNSUPPORTED-CENSUS.md` |
| D520 | 2026-11-15 | Under D439 (reflection council rounds 10 and 11): the frozen judge's four accounts read and corrected; the judge line stops at a note for Alex with a product choice and no recommendation, nothing sent or changed; next a $0 trace of the old system's three agreed duplicate question pairs through their dated requests, with a stop rule | in force | `docs/research/2026-11-14-use-acceptance/unsupported/DESIGN-NOTE.md` |
| D521 | 2026-11-15 | Under D439 (reflection council round 12): the duplicate-pair trace stands as corrected (reader leads, no answer change tested); D375 (not D251) governs same-day visibility and is not yet built; the same-day candidates of four stored runs traced at $0: in four of four different-article cases the later article was read without being shown the earlier question | in force | `docs/research/2026-11-14-use-acceptance/duplicates/DUPLICATES-RESULT.md` |
| D522 | 2026-11-15 | Under D439 (reflection council round 13): the four-case same-day visibility finding is a lead; the stored-request probe is not sent; first a $0 check that the questions' state before each article can be reconstructed and the reading and filing checks exercised on it, else the limitation is reported and no probe proposed | in force | `clean-arch/step1-unfiled-2026-11-08/council/my-codex-13.md` |
| D523 | 2026-11-15 | Under D439 (reflection council round 14): the reading-step probe is withdrawn (its pass condition contradicted the frozen prompt); each duplicate's opening traced at $0 to the comparison step: one second question never compared with the first (keyed candidate skips the search; day-start list), the others compared and kept apart | in force | `docs/research/2026-11-14-use-acceptance/duplicates/DUPLICATES-RESULT.md` |
| D524 | 2026-11-15 | Under D439 (reflection council round 15): the lean path is not closed; the duplicate trace stands with qualifications; next a reviewed $0 design and deterministic proof of D375's per-article list on the historical state and the production entry point, with fake external comparisons and a stop rule; nothing frozen changes, nothing is sent | in force | `docs/CURRENT_STATE.md` (the one next task) |
| D525 | 2026-11-15 | Under D439 (reflection council round 16): the D375 proof's first design is not built; the state before the tested article is rebuilt at $0 by the production replay from stored answers; six revisions (synthetic request boundaries, real interruption and resume, the as-of list invariant, full state comparison, allowed differences) go back to the council as version 2 | in force | `docs/research/2026-11-14-use-acceptance/duplicates/D375-PROOF-DESIGN.md` |
| D526 | 2026-11-15 | Under D439 (reflection council round 17): the D375 proof's design is accepted for building with its recovery comparison corrected (same bounded comparison point, expected audit differences checked by content, a real mid-write failure with rollback verified); the unread dropped-statement lead does not come first | in force | `docs/research/2026-11-14-use-acceptance/duplicates/D375-PROOF-DESIGN.md` (version 3) |
| D527 | 2026-11-15 | Under D439 (reflection council round 18): the D375 proof's four stages recorded as case-specific wiring findings with labelled fake answers; the registered proof has not passed; its missing checks (same-day closure, groups and names as shown, failing checks for allowed differences, a later article behind an interrupted one) come first, then a separately reviewed, priced measurement design | in force | `docs/research/2026-11-14-use-acceptance/duplicates/D375-PROOF-RESULT.md` |
| D528 | 2026-11-15 | Under D439 (reflection council round 19): the D375 proof gets row-level checks and required failure records before it is called passed; the measurement of D375 is designed small, with a truthful request, complete days holding same-day openings, a same-day default control, a prediction on facts received by the final judgement and a harm control; the council reviews it before any send | in force | `clean-arch/step1-unfiled-2026-11-08/council/my-codex-19.md` |
| D529 | 2026-11-15 | Under D439 (reflection council round 20): the D375 proof accepted as a passed, bounded serial proof; the fresh week's identified same-day facts traced into the final judging requests at $0: most arrived within days; the data-center revenue question never received the next quarter's guidance or a market estimate of the year (the question whose answer both teams called unsupported); returned to the council as an eligible case | in force | `docs/research/2026-11-14-use-acceptance/d375-measure/SAME-DAY-CASES-RESULT.md` |
| D530 | 2026-11-15 | Under D439 (reflection council round 21): the data-center revenue answer is a confirmed missing-input case (cause and D375's effect unresolved); the six-call judge test is not sent; next a $0 sizing of that mechanism on the census's settled unsupported answers, with a stop rule | in force | `clean-arch/step1-unfiled-2026-11-08/council/my-codex-21.md` |
| D531 | 2026-11-15 | Under D439 (reflection council round 22): the missing-input sizing stands as corrected (three of ten answers on two matters; a later-linking decision in the new system); the two filing decisions traced at $0: each was made by a frozen piece's written rule working as written (takes lines at reading; the later-linking question's wording); a lead on unwritten dependencies in the old system | in force | `docs/research/2026-11-14-use-acceptance/missing-input/FILING-TRACE-RESULT.md` |
| D532 | 2026-11-15 | Under D439 (reflection council round 23): the two filing decisions stand as traced, no common mechanism established; D368 already decides the dependency selection the default path lacks; next a bounded $0 trace of the trial's 19 undelivered facts against stored relationships, D368's direction and the conclusion a judge would receive, with a stop rule | in force | `clean-arch/step1-unfiled-2026-11-08/council/my-codex-23.md` |
| D533 | 2026-11-15 | Under D439 (reflection council round 24): this stretch of the lean investigation is closed and consolidated on the decision page (section 7); the default and both systems stay; D375 and D368 are Alex's decisions awaiting implementation and acceptance; next a separate $0 assessment of D368's dependency channel on a stored, correctly directed case, with a stop rule | in force | `docs/research/2026-11-14-use-acceptance/DECISION-PAGE-2026-11-15.md` (section 7) |
| D534 | 2026-11-15 | Under D439 (reflection council round 25): the dependency-channel assessment corrected (its lines were built from conclusions judged after the receiver; eight edges into two questions); before any measurement design, a $0 chronology for the two receiving questions and an ordering-and-propagation proof with labelled fake judgement outputs, with a stop rule | in force | `docs/research/2026-11-14-use-acceptance/dependency-channel/CHANNEL-ASSESSMENT.md` |
| D535 | 2026-11-15 | Under D439 (reflection council round 26): the one-chain ordering proof of D368's direction accepted as a bounded wiring result; before any measurement design, a source-backed decision-relevant case among the supporting lines and a verified rebuild of the state of 2026-07-14 before its judging round, both at $0 | in force | `docs/research/2026-11-14-use-acceptance/dependency-channel/CHANNEL-ASSESSMENT.md` |
| D536 | 2026-11-15 | Under D439 (reflection council round 27): no measurement of the reversed reading direction is sent now (D368 item 4 stays recorded, awaiting build and measurement; the harness is kept); next, at $0, a design census of where dependency selection could act in the stored unseeded fresh week, with a stop rule | in force | `docs/research/2026-11-14-use-acceptance/dependency-channel/CHANNEL-ASSESSMENT.md` |
| D537 | 2026-11-15 | Under D439 (reflection council round 28): the dependency-selection census of the unseeded fresh week has one clear case (data-center revenue reading total revenue) and negative controls; before any send, a stored-data proof of the edge's effect on filing and judging, with a stop rule | in force | `docs/research/2026-11-14-use-acceptance/dependency-selection/DEPENDENCY-SELECTION-CENSUS.md` |
| D538 | 2026-11-15 | Under D439 (reflection council round 29): one dependency edge shows the intended conclusion to the judge (conditional proof) and removes seven filing links through the narrowest rule; the dependency slice's design is opened at $0, beginning with the separation of the edge's two uses; no send, no frozen piece changed | in force | `docs/research/2026-11-14-use-acceptance/dependency-selection/EDGE-PROOF-RESULT.md` |
| D539 | 2026-11-15 | Under D439 (reflection council round 30): the separation of a dependency edge's two uses (kind set by the writer; judging and filing each read one derived relation) is kept as a candidate; its design continues at $0 (duplicate and old-row contracts, the D265 and D207 reading with its cost, completed tables, a proof through real writers) | in force | `docs/research/2026-11-14-use-acceptance/dependency-selection/SEPARATION-DESIGN.md` |
| D540 | 2026-11-15 | Under D439 (reflection council round 31): the separation stays a provisional research candidate (not applying the narrowest rule to a chosen dependency is a provisional interpretation, not a product rule); no judge call; the filing and duplicate-label contracts are finished at $0 first, with a stop if homes cannot be expressed or a label's meaning would have to be invented | in force | `docs/research/2026-11-14-use-acceptance/dependency-selection/SEPARATION-DESIGN.md` |
| D541 | 2026-11-15 | Under D439 (reflection council round 32): the seed edge's label (`last_end`, defined nowhere) stops everything that touches a seed edge and is given no meaning; the filing finding is a bounded hand reading; the unseeded failure-and-reader contract is finished at $0 before the separation is called sound | in force | `docs/research/2026-11-14-use-acceptance/dependency-selection/SEPARATION-DESIGN.md` |
| D542 | 2026-11-15 | Under D439 (reflection council round 33): the dependency stretch (D533 to D542) is closed with the separation of an edge's two uses recorded as a provisional candidate, not sound for build; the status is consolidated to one next task; nothing sent; no general stopping rule adopted | in force | `docs/research/2026-11-14-use-acceptance/dependency-selection/SEPARATION-DESIGN.md` |
| D543 | 2026-11-15 | Under D439 (a cold reflection council on the whole lean path): D518 stands with its reasons (continuity; the new path not ready), the quality of the two systems' answers is not ranked, the choice of system is not made in Alex's place, and no investigation is opened; the pages corrected for a cold reader | in force, except its deferral of the choice of system, withdrawn by D544 | `docs/research/2026-11-14-use-acceptance/reflection-2/cold-codex-1.md` |
| D544 | 2026-11-15 | Under D439 (council consensus): the work toward production carries forward on the new system; the old system stays the running default until the new one passes its gates; both remain; reversal conditions and a $5 checkpoint recorded; next, a $0 review of the fresh week's answer choices against the six lines | in force | `docs/research/2026-11-14-use-acceptance/reflection-2/cold-codex-3.md` |
| D545 | 2026-11-15 | Under D439 (council consensus): the fresh week's answer choices read by two readers apart and traced to the judge; an omitted-clause fault of line 2 recorded, its repair deferred; ranges written without a figure and overrun by the first filed amount found on two questions (and one of the old system's); next, a $0 census of amount ranges in both systems | in force | `docs/research/2026-11-14-use-acceptance/fresh-ladders/FRESH-LADDERS-RESULT.md` |
| D546 | 2026-11-15 | Under D439 (council consensus): the census of 49 amount questions closes the general range design for now (12 opened without a comparable amount, 9 of them on an end range, mostly one matter; the trigger of three further matters not met); next, a prompt audit of the omitted-clause fault of the answer-choice step, ceiling $0.05 | in force | `docs/research/2026-11-14-use-acceptance/fresh-ladders/FRESH-LADDERS-RESULT.md` |
| D547 | 2026-11-15 | Under D439 (council consensus): the audit of line 2 finds an undefined term ("the topic's wording"); the description-only reading is refused (D397, D436); the recount against the July rulings finds no omission recurring on two questions under an agreed reading: no prompt change; the frozen step untouched | in force | `docs/research/2026-11-14-use-acceptance/fresh-ladders/PROMPT-AUDIT-LINE-2.md` |
| D548 | 2026-11-15 | Under D439 (council consensus): the gates the new system must pass, listed from the record (Stage A on Alex's lines; Stage B; the end-to-end comparison; use on unseen news as proposed lines; integration); the first blocker is the worthwhile questions its answer-choice step declines, framed at $0 | in force | `docs/research/2026-11-14-use-acceptance/NEW-SYSTEM-FRAME.md` (gate order superseded by D665) |
| D549 | 2026-11-15 | Under D439 (council consensus): no candidate change for the questions the answer-choice step declines; one more week of news is prepared for a diagnostic reading of the answer choices (rule fixed beforehand; ceiling $3.50), the send conditional on exposure, price and run checks | in force | `docs/research/2026-11-14-use-acceptance/second-week/DESIGN.md` |
| D550 | 2026-11-15 | Under D439 (council consensus): the one-week diagnostic of the answer choices is sent as its third design (the new week judged apart; a bounded exposure claim with two counts; outcomes as evidence; a reading sized to the population); pipeline ledger ceiling $3.95 in place of D549's $3.50 | in force | `docs/research/2026-11-14-use-acceptance/second-week/DESIGN.md` |
| D551 | 2026-11-15 | Under D439 (council consensus), with Alex's pause: the week's run stalled on a call cut by the machine sleeping and is frozen; at his return it is continued as a second part after $0 proofs, inside the unchanged $3.95 (the continuation's ledger about $2.70); the first step's unbounded call timeout is a defect, its fix decided apart | in force | `docs/research/2026-11-14-use-acceptance/second-week/RUN-STALL-2026-11-15.md` |
| D552 | 2026-11-15 | Under D439 (council consensus), on Alex's "continue": each call of the new system's first step waits at most 600 seconds on a silent connection (tests and a mutant); the week's run is continued as a second part on a ledger of $2.699577 after the $0 split and entry proofs; an unfinished second part stops before the matching step | in force | `clean-arch/step1/live.py`; `docs/research/2026-11-14-use-acceptance/second-week/split_proof.py` |
| D553 | 2026-11-15 | Under D439 (council consensus): after the continued first step only the topics and the answer choices are run, the matching and the judge recorded as not run (eight lost attempts charged at their reservations left no room for them); no ceiling raised; proved at $0 with a full positive control | in force | `docs/research/2026-11-14-use-acceptance/second-week/choices_full_control.py` |
| D554 | 2026-11-15 | Under D439: the one-week diagnostic of the answer choices is read and recorded as evidence, not as a gate: not clean on both counts (9 of 39 attempts declined on 4 of 13 topics; three zero-fault lines missed on agreed faults); the largest reason for declining, over every stored run, is a topic that asks two things, which is D397's known open defect | in force | `docs/research/2026-11-14-use-acceptance/second-week/RESULT.md` |
| D555 | 2026-11-15 | Under D439 (council consensus): the work stays on the new system; next a $0 study of the boundary of "no main part" on the nine declined topics and the D469/D470 cases, with a stop condition; Claude's first-named rule refused (D397, D469, D470); no change to the frozen step, no send | in force | `docs/research/2026-11-14-use-acceptance/second-week/RESULT.md` |
| D556 | 2026-11-15 | Under D439 (council consensus): no candidate for the "no main part" refusals among those considered; next, at $0, one map of every stored topic short of the first gate (104 topics, four readings kept apart), with overlapping and unresolved causes, reconciled to each report; it cannot by itself prove the gate out of reach or trigger D544's reversal | in force | `docs/research/2026-11-14-use-acceptance/second-week/NO-MAIN-BOUNDARY-STUDY.md` |
| D557 | 2026-11-15 | Under D439 (council consensus): the map of the first gate accepted with one correction; D400's lines stay as written and no pass is claimed; the record shows no bounded way to bring the four zero-fault lines to zero together (a delivery risk, not a reversal); next, at $0, one prompt audit of the event-reference class and the unlisted-part class with an independent second read | in force | `docs/research/2026-11-14-use-acceptance/second-week/FIRST-GATE-MAP.md` |
| D558 | 2026-11-15 | Under D439 (council consensus): the audit of the event-reference and unlisted-part classes finds no bounded, product-relevant repair ready; D400's lines unchanged, the first gate recorded as not met; put to Alex: that record and one request, to finish the unfinished week as a diagnostic (matching and judge, pipeline ledger at most $0.80) after a $0 proof of the continuation; nothing sent without his word | in force; its proposed next task superseded by D559 | `docs/research/2026-11-14-use-acceptance/second-week/PROMPT-AUDIT-TWO-CLASSES.md` |
| D559 | 2026-11-15 | Core-problem council (Alex's request; council consensus): the product problem is forming answerable questions, no single cause proven; the clean measurements examined start from empty, against the start-state record of 2026-11-05 (now numbered here; a contemporaneous account, to be confirmed by Alex); the empty-start results and the gate record stay; to Alex: confirm the return to a real starting library and, on his word, one small same-article comparison (carried library against empty) after five $0 proofs | in force | `docs/research/2026-11-14-use-acceptance/reflection-3/cold-codex-5.md` |
| D560 | 2026-11-15 | Reflection council (Alex's request; council consensus): the goal is a continuing research library whose answers show their reasons, with no single number for "ready"; the measuring method is a major part of the impasse beside real product defects, not apportioned; next a $0 pilot of Alex's own product-level review on the stored fresh week (16 cards, 3 repeats, controls, three completeness sheets), then D559's comparison; the role of the six answer-choice lines put to him after the pilot; nothing changes or is sent | in force | `docs/research/2026-11-14-use-acceptance/reflection-4/council-codex-3.md` |
| D561 | 2026-11-16 | Alex: "go": D559's small comparison is sent as designed (11 opening articles of the week of 10-06, each read from the week of 09-22's library and from empty, 22 reads, ledger ceiling $1.00); read as fixed in its design; his Deck 1 marks still wait; D559's wider confirmation asked again with the result | in force | `docs/research/2026-11-14-use-acceptance/carried-library/DESIGN.md` |
| D562 | 2026-11-16 | The small comparison (council consensus): with last week's library the first step re-opened none of the 4 held questions (16 questions opened from empty against 4, none duplicating the library; 17 of 27 homes right and 2 wrong by both readers); it did not open the equity-commitments question the empty read opened and lost a DOJ/FTC question; between the rule's two outcomes, reported as it is; nothing about final answers; next to Alex: Deck 1, then D559's wider question, then the six lines | in force | `docs/research/2026-11-14-use-acceptance/carried-library/RESULT.md` |
| D563 | 2026-11-16 | Alex: "think carefully, read the traces, council, then execute" (council consensus): the next step is the new system run unchanged over two weeks with the library kept (the stored week of 09-22, then 241 never-sent articles of 09-29..10-05), later steps regenerated over the fortnight; $0 proofs of a new extension, the downstream under the trap, order and handoff first; a one-day slice first; ledger fixed at $6; reading frozen before any answer; a diagnostic | in force | `docs/research/2026-11-14-use-acceptance/reflection-4/council-codex-7.md` |
| D564 | 2026-11-16 | The fortnight read (council consensus): no held question re-opened; gate 1 still not met in the product condition (7 or 5 of 13 right); no last answer unsupported by both readers, 6 of 12 contested; the page fix (processing steps and completed days at the writer) accepted for completed replays; the due-date class is one matter; next a $0 sizing of D505's company-figure delivery gap, facts linked elsewhere included | in force | `docs/research/2026-11-14-use-acceptance/carried-run/RESULT.md` |
| D565 | 2026-11-16 | Under D439 (council rounds 12 to 16): the six contested answers of the fortnight traced (no candidate read would move any; too little evidence and question forms); D520's open choice turned into one bounded diagnostic of the frozen judge's self-report on 45 Stage B figure answers, frozen design and decision rule, ceiling $0.45 | in force | `docs/research/2026-11-14-use-acceptance/self-report/DESIGN.md` |
| D566 | 2026-11-16 | Under D439 (council rounds 17 to 24): the D520 line closed (the judge's self-report does not separate; the readers' source check unclear; the choice stays Alex's); production's replay completes a day at the last sequence it wrote (a closing on a day without items was invisible at the next day's start); the new system's loop to close due questions as production does, one owner of the sequence, as designed | in force | `docs/research/2026-11-14-use-acceptance/carried-run/CLOSING-DESIGN.md` |
| D567 | 2026-11-16 | Under D439 (council rounds 25 and 26): the new system's daily loop closes due questions with production's closing step, walks calendar days and owns its store sequence; accepted on tests, mutants, the unchanged extension proof and a replay to 2027-04-02; next a $0 check of gate 1's reading method on independently established sound answer choices | in force | `docs/research/2026-11-14-use-acceptance/carried-run/CLOSING-DESIGN.md` |
| D568 | 2026-11-16 | Under D439 (council rounds 27 to 31): gate 1's reading of the fortnight repeated from the start by the unchanged tooling (identical packets, fresh readers and third readers of both families) and compared send by send by the gate's own accounting; it reports agreement and difference only; the lines unchanged | in force | `docs/research/2026-11-14-use-acceptance/gate1-stick/DESIGN.md` |
| D569 | 2026-11-16 | Under D439 (council round 32): gate 1's verdict reproduced by its method on the fortnight (not a validity proof); D397's 'shown beside the answer as not judged' is missing from the product's page; next a $0 design and proof of that display path, judgements unchanged | in force | `docs/research/2026-11-14-use-acceptance/gate1-stick/RESULT.md` |
| D570 | 2026-11-16 | Under D439 (council rounds 33 to 37): D397's parts not judged carried to the product's page (bundle, closed schema, adapter, snapshot, drawer; unit-proved, browser proof pending); the page refuses the new system's three-choice events (gate 5's third defect); next a $0 design of the page contract for the new system's answer shapes | in force | `docs/research/2026-11-14-use-acceptance/not-judged-display/DESIGN.md` |
| D571 | 2026-11-16 | Under D439 (council rounds 38 to 40): the product page reads the new system's events, theme ranges and unrecorded shapes without inventing a direction (neutral, outcome or range named, no composite) and shows D397's parts not judged; proved by tests, mutants and the fortnight's page in headless Chrome | in force | `docs/research/2026-11-14-use-acceptance/page-contract/RESULT.md` |
| D572 | 2026-11-16 | Under D439 (council rounds 41 to 43): the page slices of D570 and D571 accepted after round 41's four fixes and the drawer checks; next a $0 check of the API serving a new-system store to the page, before and after a closing | in force | `docs/research/2026-11-14-use-acceptance/page-contract/RESULT.md` |
| D573 | 2026-11-16 | Under D439 (council round 44): the API serves a new-system store to the page (dates, closings, shapes, the page's cards); the page's one-time read and date clamp observed; next a $0 check of serving while a stored replay writes | in force | `docs/research/2026-11-14-use-acceptance/page-contract/SERVE-RESULT.md` |
| D574 | 2026-11-16 | Under D439 (council rounds 45 to 50): a freshly opened page shows the served library's latest completed day (the startup read passes the served day; later replacements clamp as before); a live store's first day in progress is an open defect (a race-free guard not built); next, the $0 live-service design | in force | `docs/research/2026-11-14-use-acceptance/page-contract/LIVE-READ-DESIGN.md` |
| D575 | 2026-11-16 | Under D439 (council rounds 51 and 52): the live-service design paused as recorded input; one consolidated decision page for Alex now; then a $0 feasibility census of Stage B's control line within its fixed population, no paid send implied | in force | `docs/research/2026-11-14-use-acceptance/DECISION-PAGE-2026-11-16.md` |
| D576 | 2026-11-16 | Under D439 (council rounds 53 to 58): Alex's page stands; Stage B's control line cannot be exercised by re-sending the judge (4 of 8; the blockers set upstream); no delivery check; next, at $0, a census of the unlisted-parts class (line 2) now that the page reads the list, back to the council before any arm | in force | `docs/research/2026-11-14-use-acceptance/stage-b-controls/CENSUS.md` |
| D577 | 2026-11-16 | Under D439 (council rounds 59 to 65): the unlisted-parts probe of arm A (the topic's wording defined as its description and outcome) sent on 18 stored requests, unchanged and changed ×3 the same day, read blind with planted controls and scored by a rule fixed before the send; a diagnostic, not acceptance | in force | `docs/research/2026-11-14-use-acceptance/unlisted-parts/DESIGN.md` |
| D578 | 2026-11-16 | Under D439 (council round 66): arm A's probe negative under both countings (no unlisted parts in changed written answers against 4-5 control topics, but 2 unjustified refusals); the line stops; two bounded accounts of the refusals ($0.02 ceiling) before any further design | in force | `docs/research/2026-11-14-use-acceptance/unlisted-parts/RESULT.md` |
| D579 | 2026-11-16 | Under D439 (council round 67): the two refusal accounts apply line 6's decline rules to the outcome's words; the proposed outcome-only exemption refused (D397, D417); a bounded $0 audit of the decline rules and the outcome's extra parts, then a sourced rule or no candidate | in force | `docs/research/2026-11-14-use-acceptance/unlisted-parts/RESULT.md` |
| D580 | 2026-11-16 | Under D439 (council rounds 68 and 69): no reviewed repair for the unlisted parts (the decisions give no general rule for the main part of a multi-part topic; an independent reader left 29 of 63 open); arm A stays stopped; next, a $0 check of the Idea planner on new-system answer shapes | in force | `docs/research/2026-11-14-use-acceptance/unlisted-parts/DECLINE-AUDIT.md` |
| D581 | 2026-11-16 | Under D439 (council rounds 70 to 72): the Idea planner shows a three-choice event as Yes and Still open; the event-driver design parked as recorded input; no bounded gate-moving candidate on the record; paid work and new lines held until Alex returns or the council names one | in force | `docs/research/2026-11-14-use-acceptance/idea-planner/RESULT.md` |
| D582 | 2026-11-16 | Alex's standing instruction lifts D581's hold; arm A2 (arm A plus D436's second-side rule) probed on 28 topics against the same-day control, with refusal-retention and recovery-gain rules fixed before the send (council rounds 73 to 77) | in force | `docs/research/2026-11-14-use-acceptance/unlisted-parts/DESIGN-A2.md` |
| D583 | 2026-11-16 | Arm A2's probe negative under the fixed rule: no unlisted part and no refusal on the motivating topics (control 6 topics), refusal controls kept, recoveries met only counting for the answer; rule 2 failed, its one change-caused harm being over-listing (judged alternatives, settlement routes) | in force | `docs/research/2026-11-14-use-acceptance/unlisted-parts/RESULT-A2.md` |
| D584 | 2026-11-16 | Arm A3 built and sent by council consensus: A2 plus one closed-set sentence removing an event's restated outcomes (D409, D397); three arms, Reading A and a pre-registered diagnostic Reading B; a lead is provisional until a trace review | in force | `docs/research/2026-11-14-use-acceptance/unlisted-parts/DESIGN-A3.md` |
| D585 | 2026-11-16 | Arm A3's probe negative under the fixed rule; checked: two failing checks are measurement errors (classer, matter labels, a check counting the intended removal); the change-consistent effect is a named way of ruling out listed as not judged; line 2 at 0 in A2 and A3 | in force | `docs/research/2026-11-14-use-acceptance/unlisted-parts/RESULT-A3.md` |
| D586 | 2026-11-16 | Tuning of the not-judged list's edge stops on these topics (D391); A2 an unaccepted candidate; next a $0 provenance check and design for one fresh controlled A2 comparison on Alex's six lines | in force | `docs/research/2026-11-14-use-acceptance/unlisted-parts/RESULT-A3.md` |
| D587 | 2026-11-16 | A fresh controlled comparison of A2 (week of 10-13 from the 10-06 library, frozen vs A2, gate-1 form, two populations classed blind) is designed; its $0 proofs come next and the paid run is decided on their numbers | in force | `docs/research/2026-11-14-use-acceptance/unlisted-parts/FRESH-A2-DESIGN.md` |
| D588 | 2026-11-16 | The fresh A2 comparison's first step is sent on the week of 10-13 (383 articles) from the 10-06 library, frozen Step 1 under a $6.50 shared ledger, proven at $0 on the exact launcher; an incomplete run gives no verdict | in force | `docs/research/2026-11-14-use-acceptance/unlisted-parts/FRESH-A2-DESIGN.md` |
| D589 | 2026-11-16 | The fresh A2 comparison's first step is complete (383 articles, $3.45, 5 topics); population (b) has 3, under its minimum of 5, so no comparative verdict; the five topics are sent and read as registered (a fresh gate-1 reading), then the comparison closes; A2 stays unaccepted | in force | `docs/research/2026-11-14-use-acceptance/unlisted-parts/FRESH-A2-DESIGN.md` |
| D590 | 2026-11-16 | The fresh A2 comparison closes (no verdict; a fresh gate-1 reading of the frozen step: lines 2, 3, 5 missed, 4 met); the due-day mark's family split (133 Codex vs 0 Claude fails on code-set days) is a reader discrepancy: a D-only diagnostic held all 12 class items in both families, the brief is unchanged; next a $0 census of Ruled-out rungs that catch a postponement | in force | `docs/research/2026-11-14-use-acceptance/unlisted-parts/fresh-a2/d-diagnostic/RESULT.md` |
| D591 | 2026-11-16 | An announced "not by the due day" as a ruling out (37 company delays and 1 authority case in 296 frozen-step event answers): no decision settles the boundary; form and step unchanged, both readings recorded, 38 answers listed as candidates affected; the question on Alex's page (Claude's lean: it rules out); next a $0 design for the final-answer test's control shortfall | in force | `docs/research/2026-11-14-use-acceptance/unlisted-parts/fresh-a2/postponement/BOUNDARY-CASES.md` |
| D592 | 2026-11-16 | Stage B's control line: an unchanged re-send stays at 4 of 8, delivery of three facts reaches at most 7, the eighth needs an unproven two-step change; the 7-control course is not started for the line's sake; the live-service operating contract resumed as a $0 design (D575's rows, a falsifier), back to the council before any build | in force | `docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md` |
| D593 | 2026-11-16 | The live-store operating contract v9 (WAL, one transaction and connection per request, one bound resolver, first day refused, search over the visible corpus and a published index day, checkpoint and disk limits, crash bounds, an inode-named writer lock, §9 kept with P1 proposed) agreed for its $0 proof build on test stores; live operation not authorized | in force | `docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md` |
| D594 | 2026-11-16 | The bound resolver built and proven at $0 (one owner for every upper date bound; future explicit bounds refused; first day refused; the bundle functions' default reads the last completed day; ranges refuse only a start after their end); the served product store's half-processed 2026-08-29 is no longer returned; 308 + 164 tests and 8 mutants; nothing deployed | in force | `docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md`; `tests/test_bound_resolver.py` |
| D595 | 2026-11-16 | Slice 2 built and proven at $0: one pinned read transaction per API request and MCP call, MCP connections per call (overlapping searches never share the index), MCP's start-up object list labelled with its day, the streamed Idea route refusing a first-day store or future date before headers; 317 + 164 tests, 6 of 6 mutants; nothing deployed | in force | `tests/test_live_reads.py`; `docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md` |
| D596 | 2026-11-16 | Slice 3 built and proven at $0: lexical ranking over the views visible at the bound only; the index embeds only views visible at the last completed day (none on a first-day store); vectors keyed by view, embedding-input hash and model, checked over visible candidates; a backup of a WAL store must leave WAL mode before read-only readers; 327 + 164 tests, 4 of 4 mutants; nothing deployed | in force | `tests/test_search_live.py`; `docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md` |
| D597 | 2026-11-16 | Slice 4a built and proven at $0 on isolated test stores: the writer's store in WAL mode (set before its schema) with a 64 MB size limit on its connection; a stop before a day on low space or three failed checkpoints, recorded with its reason and last completed day and never resent; a partial-day exception inside the writer's process (not a killed process; that proof is 4b's) leaving answers equal to a backup at the last completed day; an orderly end; 327 + 172 tests, 7 of 7 mutants; no writer lock yet | in force | `clean-arch/step4-2026-11-10/stage_b/test_writer_store.py` |
| D598 | 2026-11-16 | Slice 4b built and proven at $0: an operating-system lock per store (device and inode) taken by the writer before its first write and by preflight before its one locked copy; path checks before each day; the connection closed (after leaving WAL mode when no reader holds it) before the lock is released on every exit; a killed writer's lock released by the system; `scripts/snapshot_store.py` never replaces; filesystem-full proof run separately (A crash keeps nine days; B stops first); 339 + 186 tests, 17 of 17 mutants; P1 still only proposed | in force | `src/hivemind/live_lock.py`; `live-service/OPERATING-CONTRACT.md` |
| D599 | 2026-11-16 | Round 137's corrections to slice 4b: `store.open_read_only` resolves symlinks and refuses a hard-linked store (API 500 and refusal at start; MCP at start and per tool; none of 702 stored files is hard-linked); the writer releases its lock only once its connection is closed; the snapshot closes its source on any failure; a stop takes its last day from the loop, not a moved store; 341 + 188 tests, 21 of 21 mutants | in force | `live-service/OPERATING-CONTRACT.md` (Round 137's corrections) |
| D600 | 2026-11-16 | Round 138's correction to slice 4b: the checkpoint answers done, busy or its error, and leaving WAL answers its mode and why it was kept; only a reader holding the store counts as one, any other failure stops or is recorded with its own error; the path is checked first; the moved-store trigger is stated as not understood; 341 + 190 tests, 24 of 24 mutants | in force | `live-service/OPERATING-CONTRACT.md` (Round 138's correction) |
| D601 | 2026-11-16 | Proof 10 passes at $0: the built writer re-judges c1 to 2027-04-02 while the API (first day 503), MCP's tools (module level), the lock, preflight and two snapshot states are checked at seven pauses, and 169 concurrent `/library` answers each serve a compatible completed day equal to its dated read; 23 of 23 checks | in force | `live-service/PROOF10-RESULT.md` |
| D602 | 2026-11-16 | Proof 2f passes at $0: with the live read successful the Idea and its bundles are asked as of the served day; with it failed, the embedded later day is refused (409) and the Idea error shows, the library unchanged and a second sentence sent; mutant caught; no product code changed | in force | `live-service/PROOF2F-RESULT.md` |
| D603 | 2026-11-16 | Slice 5 built and proven at $0: `service.open_pinned` (one pinned opener for the API and MCP, `StoreUnreadable` naming the path on an opening, `BEGIN` or pinning failure) and an explicit 5 s reader busy timeout; proofs 5a, 5b, 6a, 6b (stand-in), 7′ (88 outcomes against an independent pre-partial-day reference) and 8′; 346 + 192 tests, 6 of 6 mutants | in force | `live-service/OPERATING-CONTRACT.md` (Slice 5) |
| D604 | 2026-11-16 | Under D439 (council round 145): the next production step is a $0 trace of the fresh topics' line-5 failures (each topic's three control answers beside topic, source and settled marks; the mark that changes its status under each counting; family agreement; product visibility), mapped to existing censuses before any candidate; closes this route if no sourced common mechanism | in force | `reflection-4/council-codex-145.md` |
| D605 | 2026-11-16 | Under D439 (council rounds 146, 147): D604's line-5 route closes with no candidate (fresh misses are reference choices whose rule-following form gives the same answer choices, a stopped class, Alex's boundary, and a reader discrepancy on D414); the gate stays unmet; no paid send without a new reviewable candidate; resume on Alex's rulings or new evidence | in force | `unlisted-parts/fresh-a2/line5/RESULT.md` |
| D606 | 2026-11-16 | Under D439 (council round 148), reversibly: next product test from a real earlier library (empty starts as diagnostics); Alex's six lines and accounting stay in force; postponement provisionally reads Still open (reversed by D607); D520/D571 running behaviour retained; P1 not taken; next a $0 audit of the postponed-event class (by topic and matter, full rungs, guards) | in force | `reflection-4/council-codex-148.md` |
| D607 | 2026-11-16 | Under D439 (council round 149): D606's postponement reading reversed provisionally (a formal decision that a dated event will not happen by its due day rules it out; authorities by D420; forecast-versus-decision guard kept); the postponement repair route closes (no missing general rule; Taiwan p3 isolated); next a $0 audit of the shared fiscal-year note's consumers and effects | in force | `unlisted-parts/fresh-a2/postponement/AUDIT-RESULT.md` |
| D608 | 2026-11-16 | Under D439 (council round 150): the fiscal-note lead closes as cleanup-only (no demonstrated product effect; the clause is not inert because check 5 refuses a pre-year-end day; the reader split's cause not established); a reflection council (fresh Codex, cold read) follows | in force | `unlisted-parts/fresh-a2/fiscal-note/RESULT.md` |
| D609 | 2026-11-16 | Under D439 (reflection council, cold Codex read): the next production step is a $0 source-to-request trace of the company's own figures on the carried fortnight (D505), by member, with time, duplicate, population and relevance controls and an independent second reader on bearing cases; moves only on a shared, consequential delivery mechanism | in force | `reflection-5/codex-cold.md`, `reflection-5/codex-challenge-1.md` |
| D610 | 2026-11-16 | Under D439 (reflection council): the company-figure delivery route closes narrowly (5 bearing undelivered statements on 3 questions, two mechanisms, none predicted to move an answer by a blind second reader with working controls; 49 groups homeless by D382/D384); no v12 effect test; next a $0 feasibility review of a same-news product comparison from established libraries | in force | `delivery-trace/RESULT.md` |
| D611 | 2026-11-16 | Under D439: the same-news comparison from established libraries closes (D517's power arithmetic unchanged by a starting library; the old library ends 08-28; no exposure-free week remains from 09-21 to 10-26); nothing run | in force | `comparison-feasibility/RESULT.md` |
| D612 | 2026-11-16 | Under D439 (council round 151): paid work held on the currently supported candidates (every bounded route closed with evidence; A2 cannot be decided on stored topics); the running system stays the default; reopen on new consequential delivery cases, decidable comparison material, Alex's marks or decisions, or a new concrete reversible candidate | in force | `reflection-4/council-codex-151.md` |
| D613 | 2026-11-16 | Under D439 (council round 152): D611's exposure claim corrected (07-20..08-24 unread by any new-system Step 1 run); D612's hold stands; official gate 1 already meets lines 2 and 5 on the 44 and misses zero-fault lines 1, 3, 4 by 6 sends of 131 of different meanings; no code check or send on them | in force | `reflection-4/council-codex-152.md` |
| D614 | 2026-11-16 | Under D439 (council round 153): the refusal census (174 over 30 topics; 13 unjustified on 6, all 'none main') maps to the closed main-part class; D612 stands; next a $0 design review of splitting (separate topics vs two judged questions under one topic) against D397, D436, D38 with the guards; no version opened, D397 unchanged | in force | `refusal-census/RESULT.md` |
| D615 | 2026-11-16 | Under D439 (council round 154): the period split (D38's one view a year; the step names a typed 'one quantity for two periods' case, code splits by the years named) is developed at $0 as a lead on D397's open defect; no gate movement claimed; probe only after a reviewed design | in force | `splitting/DESIGN-REVIEW.md` |
| D616 | 2026-11-16 | Under D439 (council rounds 155 to 158): the period split's design v4 accepted for a $0 scratch build beside the frozen ladder step; the narrow D397 departure (one judged question per open year for one quantity over two open years) recorded as a reversible proposal, not in force; Stage B readers refuse split stores; nothing sent | in force | `splitting/DESIGN.md` |
| D617 | 2026-11-16 | The period split's $0 build is done beside the frozen step (unchanged): closed-set decline with the new case, period identity check, yearly re-asks, writer `period` key and `open_split` with digit-only view ids, Stage B readers refusing split stores; 32 new tests, 346 + 224 passing, mutants 8 of 8; nothing sent | superseded by D618 | `splitting/BUILD-RESULT.md` |
| D618 | 2026-11-16 | Round 159 refused D617's "proven"; fixed: crash proof kills the real replay process (found and fixed the writer's missing import), not-judged owner = the model via the yearly line (code adds only a year with no question; 746 of 3,335 stored parts name a year), detail page + Idea bundles + each Stage B reader's entry point on split and historical stores, topic numbers < 10,000; 35 tests, mutants 14 of 14; nothing sent | superseded by D619 | `splitting/BUILD-RESULT.md` |
| D619 | 2026-11-16 | Round 160: yearly view ids `v0<number><year>` (no ordinary id begins with 0; no size bound); the writer refuses a topic id other than Step 1's `clean-<number without leading zero>` (all 3,457 stored ids) and malformed split years; three more readers that map a view to its topic by id refuse a split store (entry points tested); 47 tests, mutants 20 of 20; nothing sent | in force | `splitting/BUILD-RESULT.md` |
| D620 | 2026-11-16 | Council round 161 accepted the split's scratch build for probe preparation only (caveats: three research readers not rerun end to end; mixed qualifications under the yearly line to be measured; $0.40 bound conditional on charges within reserves); next: the probe's $0 preparation, back to the council before any send | in force | `reflection-4/council-codex-161.md` |
| D621 | 2026-11-16 | Council rounds 162–165: the split probe is sent on 12 topics outside the 44 (T 2, C1 6, C2 2, C3 2; M dropped, its only instance being in the 44), both arms three sends, caps $0.15 + $0.25; reading bound to the sends by content; prompt audit 5 blind rounds; mutants 40 of 40; limits reported with the result | in force | `splitting/PROBE-PREP.md`, `reflection-4/council-codex-165.md` |
| D622 | 2026-11-16 | Split probe negative under its registered rule (both families: Q fails on c1/clean-12's 2027 pass-3 question, a GDP-share question for a total); counts passed (T 6/6 split, no control misuse), plants caught; candidate stopped, measure mismatch recorded as a case not a rule; no third readers; D397 stays open; D612's reopen conditions govern; $0.083 | in force | `splitting/RESULT.md` |
| D623 | 2026-11-16 | Reflection 6 (cold reviewer + challenge): gate 1's zero-fault lines are not a dependable target for the current step (outside-44 fault rates ≈3.8/3.3/1.4% a send); next, a blinded reference control outside the 44 at $0 API: independent writers' answer choices vs the frozen step's stored ones, same checks, both families, full gate form, every settled reference fault reviewed against source and rule; gate and D426 unchanged | in force | `reflection-6/` |
| D624 | 2026-11-16 | Reference control closes by its rule (no reader error; result 2 met on 1 topic of 4): reading valid, agreed hard-line faults of 26: frozen 3, Codex-writer refs 8, Claude-writer refs 0, all reviewed as answer errors; lead: prepare at $0 a matched medium-vs-high reasoning-effort comparison (3+3 fresh draws, 26 topics outside the 44, blind, outcomes fixed before), separate send decision | in force | `reflection-6/reference-control/RESULT.md`, `reflection-6/codex-challenge-2.md` |
| D625 | 2026-11-16 | Matched effort comparison sent after two council refusals were fixed (lost answers count as failures; <3 medium failures inconclusive; sound controls checked; byte-level request check) and a clean ladder preflight (83 stored answers, 5 refusals as in the stored runs); six interleaved arm-draws, caps $0.25 + $0.75 | in force | `reflection-6/effort/` |
| D626 | 2026-11-16 | Effort comparison closes by its rule (failed sends of 78: medium 13, high 14; reading valid; every agreed failure an answer error); dominant class L (part of the outcome neither judged nor listed), then Q (fused decisions); the frozen step fails an agreed hard line in ~1 of 6 fresh sends on 26 topics outside the 44 | in force | `reflection-6/effort/RESULT.md` |
| D627 | 2026-11-16 | Required outcome-parts field closed by construction (an omission from both lists passes); council: no accepted gate-1 candidate (not exhaustion); Alex's page reports the impasse, model switch an unproven lead; next a $0 feasibility design for a paired gate-3 comparison on the same matters | in force | `reflection-6/codex-challenge-6.md` |
| D628 | 2026-11-16 | Paired gate-3 comparison closes (~15–20 matched matters need 44–49 points for 80% power); council opens the same-provider model lever at $0: one read-only model-list call via the existing key reader, then one priced, matched candidate design (D625's shape, 26 topics outside the 44) for a separate send decision; credentials and caps untouched | in force | `reflection-6/codex-challenge-7.md` |
| D629 | 2026-11-16 | Same-provider model comparison sent: gpt-6-luna vs gpt-6.1-sol (published $2/$10, added to model.PRICES), D625's design with only the model changed, first sol topic alone, caps $0.25 + $4.50; a diagnostic on exposed topics, not a gate pass | in force | `reflection-6/model/` |
| D630 | 2026-11-16 | Model comparison inconclusive by its rule: failed sends of 78 luna 13, sol 5 (strict 29/20), no new harm, but sol refusals 24 vs 15 (bound luna+2); clean ladders 41 vs 50; next: trace the 24 sol refusals with luna's matched answers at $0 before any repair or Astra send | in force | `reflection-6/model/RESULT.md`, `reflection-6/codex-challenge-10.md` |
| D631 | 2026-11-16 | Sol refusal trace: 4 agreed-unjustified, 12 disputed, 8 justified; pattern "several, none the main one" (reasons differ); the description-priority sentence refused as an unconfirmed rule (D397: the judged part is the outcome's); next an independent $0 audit of the request and the rule against D397, D436 and stored cases | in force | `reflection-6/model/REFUSAL-TRACE.md`, `reflection-6/codex-challenge-11.md` |
| D632 | 2026-11-16 | Rule audit: sources silent on the main part when an outcome names several (five boundary topics go on Alex's page, unresolved); the Astra screen sent: astra vs fresh sol, 12 seeded topics × 3 draws, caps $1.20 + $5.50, verdict fixed before (closes at ≥3 astra failures; promising only at ≤1 below sol with strict and refusal conditions); a screen, never a gate-1 claim | in force | `reflection-6/model/rule-audit.md`, `reflection-6/astra/DESIGN.md`, `reflection-6/codex-challenge-12.md`–`14.md` |
| D633 | 2026-11-16 | Astra screen promising on 12 topics (failed sends sol 4, astra 1 of 36; all refusals; Hugging Face recovered; boundary declines shared); complementary 14 topics screened the same way (caps $1.20 + $5.00), halves reported separately | in force | `reflection-6/astra/RESULT.md`, `astra/DESIGN-REST.md`, `reflection-6/codex-challenge-15.md`, `-16.md` |
| D634 | 2026-11-16 | Complementary screen closes astra by its rule (sol 5, astra 3 of 42; halves 9 vs 4 of 78); every astra failure a main-part decline, 0 agreed faults on its 51 ladders; H20 is a sixth main-part case on Alex's page; next a $0 two-reader review of a narrower provisional main-part rule | in force | `reflection-6/astra/RESULT-REST.md`, `reflection-6/codex-challenge-17.md` |
| D635 | 2026-11-16 | Narrower main-part rule closes (reverses Hugging Face's sourced wrong decline into 'none', overrides outcomes where it recovers); main-part stays Alex's ruling; next a $0 source-backed review of astra's 51 written questions with a second reader | in force | `reflection-6/main-part/RESULT.md`, `reflection-6/codex-challenge-18.md` |
| D636 | 2026-11-16 | Astra review: 11 material defects in 51 written questions, none counted by gate 1 (completion dated at next annual filing ×4 from request line 23 wider than D210 and against D403; period-end events ×3 by D403's design, to Alex's page; model choices ×4); candidate narrows line 23 to amounts; matched due-day probe sent (astra frozen vs v2, 9 topics × 2, cap $3.20, two-reviewer blind reading with controls) | in force | `reflection-6/astra-review/RESULT.md`, `reflection-6/due-day/`, `reflection-6/codex-challenge-19.md`–`24.md` |
| D637 | 2026-11-16 | Due-day probe inconclusive by its rule (dates fixed 4/4 vs 0/4, controls unchanged; one MIIT listing split); v2 kept beside the frozen request as a proposed decision-supported correction, unadopted; MIIT and purchase-commitment leads closed ($0 traces); no paid send justified on present evidence | in force | `reflection-6/due-day/RESULT.md`, `MIIT-TRACE.md`, `COMMITMENTS-TRACE.md`, `codex-challenge-25.md`, `-26.md` |
| D638 | 2026-11-16 | Rubin 'this quarter' widening traces to the topic's own period field (the opener wrote two windows); luna follows the period per D403; no request sentence causes it; lead closed for the answer-choice step, recorded as an opening-step wording defect | in force | `reflection-6/due-day/RUBIN-TRACE.md`, `reflection-6/codex-challenge-27.md` |
| D639 | 2026-11-16 | Under D612(4): astra with arm A2 (D436's second-side sentences; closing aligned after a blind audit) sent as a bounded diagnostic against a fresh frozen arm, 10 exposed topics × 2 draws, cap $3.40; verdict fixed before with comparative, per-topic, justified-decline, harm (planted listing control), and replacement-soundness conditions | in force | `reflection-6/astra-a2/DESIGN.md`, `reflection-6/codex-challenge-29.md`–`32.md` |
| D640 | 2026-11-16 | Astra-with-A2 diagnostic VOID (Codex missed the planted already-judged listing); descriptive only: A2 wrote H20 2/2 and memory 2/2 where frozen declined, agreed hard-line fails 2 vs 0, H20 questions unflagged, memory flagged by one reviewer, listing harm unmeasured; a separate blinded H-only diagnostic registered at $0; A2 stays unadopted and provisional | in force | `reflection-6/astra-a2/`, `reflection-6/codex-challenge-33.md` |
| D641 | 2026-11-16 | H-only diagnostic VOID too (the fresh Codex reader missed both planted already-decided controls); astra with A2 stays provisional and unadopted (H20 written 2/2 where frozen declined, unflagged; memory disputed; listing harm unmeasured); route stopped | in force | `reflection-6/astra-a2/h-output.txt`, `reflection-6/codex-challenge-34.md` |
| D642 | 2026-11-16 | Stop hook rejected the hold again; council round 35: a 16-topic combined send would not decide (0 of 16 weak evidence for a 131-send zero-fault gate; cannot pool with the voided A2 reading); no decision-moving $0 step supported; running system stays default; reopen on D612's conditions | in force | `reflection-6/codex-challenge-35.md` |
| D643 | 2026-11-16 | Gate-1 launch prepared as an inert draft for Alex (`reflection-6/gate1-candidate/`): Stage A on the 44 × 3 with astra-frozen or astra-a2-v2, byte-checked, preflighted (148 stored attempts, 0 differ), refuses without authorization, NOT MEASURED on a stop, ~$4.90–6.60, cap ≥ ~$9 (beyond D439); mutants not run (permission refused) | in force | `reflection-6/gate1-candidate/README.md`, `reflection-6/codex-challenge-36.md`–`38.md` |
| D644 | 2026-11-16 | Council round 39: a fifth Stage A within the remaining budget (sol + A2 + v2) refused: D426 is Alex's specific decision not reversed by D439's general delegation, and the pair is unmeasured; no in-authority, in-budget step moves the production decision; the record waits on Alex | in force | `reflection-6/codex-challenge-39.md` |
| D645 | 2026-11-16 | Alex: astra is not used ("这个成本这么高怎么可能能work"); the answer-choice step stays on luna; the gate-1 handoff's astra configurations are withdrawn | superseded by D648 | D645 record |
| D646 | 2026-11-16 | Alex: try Claude Opus 5.5 on the answer-choice step ("你试试看opus"); adapter, trial and checks prepared at $0; waiting on the Anthropic key in the credentials file | in force | D646 record |
| D647 | 2026-11-16 | The Opus trial reads "inconclusive": agreed failures luna 7 / Opus 1, strict 9 / 7, Codex family alone 7 / 7; one real new Opus failure (H20); Opus about $0.058 a topic, not below astra | in force | D647 record |
| D648 | 2026-11-17 | Alex reverses D645 ("那就用astra 吧"): astra is the step's candidate; gate 1 on the 44 runs with astra-frozen, cap $9.50 | in force | D648 record |
| D649 | 2026-11-17 | Gate 1 with astra-frozen: lines 1, 3 and 6 met; line 4 missed by 7 (main figure plus sub-part declined); lines 2 and 5 depend on the due-day split; not passed | in force | D649 record |
| D650 | 2026-11-17 | DeepSeek V4.1 Flash trial: agreed failures luna 1 / flash 3, strict 3 / 4, inconclusive; luna's own count moved 7 → 1 between draws, so one 26-topic draw cannot rank models | in force | D650 record |
| D651 | 2026-11-17 | Council rounds 40-42: D436's two sentences (no examples) tested on astra outside the 44 (6 targets, 5 controls classified blind beforehand), frozen vs edited, 2 draws each; gate-1 rerun only on PASS | in force | D651 record |
| D652 | 2026-11-17 | Second-side diagnostic INCONCLUSIVE (2 exercised): the two sentences recover pool-7 (main figure plus a condition) with no harm on 9 topics; pool-17 (total plus its part) stays declined; no gate rerun; next: a cross-domain part-of-total example, audited, tested outside the 44 | in force | D652 record |
| D653 | 2026-11-17 | Deep council (reflection 8): gate 1 with astra = line 4 (D436's class, 7 recorded) + one disputed listing point once D414 is applied (labelled counterfactual); corrections to D648/D649/D651/D652; next: $0 audit of a narrow D436 implementation, then a paired exposed verification; for Alex: D592 and the cost (clean+astra ≈ 5–7× running) | in force | D653 record |
| D654 | 2026-11-17 | Alex: "立通用规则" — for a total with one kind's share, a volume with whether supply stays short, or demand with whether capacity keeps pace, the figure is the question and the other side is not judged; a share the outcome tracks itself is asked as the share | in force | D654 record |
| D655 | 2026-11-17 | Council consensus (D439, D654): send the paired test of the narrow passage v5.5 on astra (3 deciding targets, 2 reported, 5 controls, a share control; 52 sends, shared cap $3.60); verdict rules fixed before the send | in force | D655 record |
| D656 | 2026-11-17 | The paired test of v5.5: FAIL by the prewritten rule (an L fault on the share control, the same pre-existing astra omission in both arms); D654's class recovered on the exposed targets (frozen 0/9, edited 9/9, controls 10/10 held); v5.5 kept as an unaccepted candidate; next a $0 census of the listing defect | in force | D656 record |
| D657 | 2026-11-17 | Alex: "先别管成本，搞work先" — cost is not a gate until the new system works; recorded as a baseline only; per-test spending ceilings unchanged | in force | D657 record |
| D658 | 2026-11-17 | Alex: "第一条ok" — a new reference for the final-answer test's control line, written for the 15 control questions as the new system asks them; beside the frozen ruler, built by two blind readers, ruled against the source, signed by Alex, frozen; design through council first | in force | D658 record |
| D659 | 2026-11-17 | Correction of D658: the new reference's material is the frozen ruler's packet ("同样的材料" in Alex's option), not the judge's evidence; design version 2 to council round 2 | in force | D659 record |
| D660 | 2026-11-17 | Alex: for the new control-line reference, events compared on the three outcomes ("三选一要一致"); the system's quoted reference stripped from the rungs ("删掉"); null baselines reported only ("只作对照，标出高低"); D658's option text recorded word for word | in force | D660 record |
| D661 | 2026-11-17 | Open defect: Codex-family blind readers ran with Codex memories on (a probe shows project recall; off with three flags gives NOTHING); no past result relabelled; new blind Codex readings run with memories off and a memory probe; census queued | in force | D661 record |
| D662 | 2026-11-17 | Reflection council 9 (Alex's request): the work drifted from D560's way out; hold answer-choice changes, model trials and live-store/planner/integration work; Deck 1 to Alex first ("enough to design the next comparison?"); D658 asked separately; questions in order | in force | D662 record |
| D663 | 2026-11-17 | Alex: the council marks Deck 1 instead of him; both plants rejected, 3/3 repeats, 4/5 supported controls (one substantive split), both missed matters flagged: enough to design the product comparison (no ranking); next the comparison's design at $0, run on his word | in force | D663 record |
| D664 | 2026-11-17 | Alex: no budget needed for the comparison; D658 waits; the council determines whether the six lines still make sense and what decides readiness ("run your council to determine") | in force | D664 record |
| D665 | 2026-11-17 | Council (Alex: "run your council to determine"): the six lines stop blocking release (reported; code-decidable parts stay hard); one product comparison against poc-v118 decides readiness: big matters served, practical lead/loss/no winner written before the first send, guardrails, sizes; D431 frozen reading printed beside; Step 2 checks kept; gate 5 waits; back to Alex on any verdict | in force | D665 record; clean-arch/PRD.md §1.5 |
| D666 | 2026-11-17 | Alex: "write a run plan and monitor it carefully and don't scope drift": run D665's comparison once its plan passes council review; $250 runaway guard, not a budget (single ledger superseded for this run by D667); out-of-scope findings recorded only | in force | D666 record; docs/research/2026-11-17-product-comparison/RUN-PLAN.md |
| D667 | 2026-11-17 | Council (run-plan rounds 1–10): the release comparison's run plan v9; full exposure census by plan §1.2 (production-replay and raw-corpus-copy exemptions only); company figures in N, subgroup printed; one ledger per draw ($65 / $25, $270); D431's same day for a run over one day (six draws launched within an hour, sends within 72 h); no replacement counts; scoring rules plan §1.4; Step 2 lines hard; two floors not measured | in force | D667 record; docs/research/2026-11-17-product-comparison/RUN-PLAN-v9.md |
| D668 | 2026-11-17 | Under D667: every old replay reaching the span is a read (folder level, two blind readers); scored window 08-31..09-20 (narrowed by D669); warm-up 07-01..08-30 unfiltered; census reads every kept article in the window | in force | docs/research/2026-11-17-product-comparison/stage0/replay-folders.json |
| D669 | 2026-11-17 | Alex: "只排除真被读过的，比9/7–9/20": scored window 09-07..09-20; not reads = corpus storage, pool lists, code-only corpus censuses; everything else is a read (rule frozen in stage0/classify_reads.py after council check) | in force | D669 record |
| D670 | 2026-11-17 | Under D669 (council check): 410 of 502 articles of 09-07..09-20 kept and frozen (stage0/kept-articles.json); 4 reader-shown articles added as reads; 37 bulk-viewer-only articles stay excluded (split, safer course), disclosed | in force | D670 record |
| D671 | 2026-11-17 | Under D667/D668 (council): blind matter list frozen at N = 32 (7 company figures), stage0/census/matters.json; merges need both families' grouping or both blind adjudicators; two split pairs kept apart and disclosed | in force | D671 record |
| D672 | 2026-11-17 | Alex: "开始跑"; freeze-review fixes applied (per-pass check, verdict rule completed, card spec frozen, launcher git-clean/ledger/redo); scorer, card builder and §1.6 tools built during the run before any output is read (Codex refused, Claude reviewer accepted with conditions); the slice stands in for the dry run with id-order and day-state checks | in force | D672 record |
| D673 | 2026-11-17 | Under D672: the card blinding rule covers the form (fields, labels, notes, ids), not the systems' own wording; repeated form check by a closed reader; wording differences disclosed | in force | D673 record; stage0/card-spec.md |
| D674 | 2026-11-17 | Alex's goal: run and keep tackling until the comparison's criteria pass; council loop on the traces after each round that does not pass; no questions to Alex; no scope drift; frozen ruler and instruments never moved; every try logged in TRIES.md | in force | D674 record |
| D675 | 2026-11-18 | Under D672: the reading tools' council review found them not ready; fixed (six draws required, exact 10-point bar, redo store, neutral ids, debate rounds, card parsing); open readings of the frozen rule written down (guardrail shares exclude covering cards; mapping without the news) | in force | D675 record; stage0/ |
| D676 | 2026-11-19 | Release comparison (5-draw diagnostic): new loses (2–3 vs 10 of 32) for two known mechanisms, D382's figure exclusion and the Step 1→ladder bundled-question loss (D432); measurement sound; even repaired the new system ties at best; keep the old system; attainable verdict computed before any future paid comparison (council consensus) | in force | `docs/research/2026-11-19-comparison-review/` |
| D677 | 2026-11-19 | The release comparison's goal loop closed: the old system stays, no paid work continues; reversed only if Alex reverses D505 or funds a full run, with a written path to passing first (council consensus, D439/D544) | in force | `docs/research/2026-11-19-comparison-review/council-c-codex.md` |
| D678 | 2026-11-19 | Merge design (council consensus): old opens questions, clean Steps 1–3 read and organise evidence, the frozen judge answers; figures by D382/D505 unless Alex's exception; a 12-article test ($0.33–0.42, 5 lines) awaits Alex's approval | in force | `docs/research/2026-11-19-merge-council/MERGE-PLAN.md` |
| D679 | 2026-11-19 | Alex lifts D677's paid-send stop for the merge test only; 70 articles × old-2/old-3, c8 filing under the old questions, hybrid and control judging arms on a 09-06 cutoff copy; $5 ledger; lines P1–P3, P5 and V | in force | `docs/research/2026-11-19-merge-council/EXECUTION-PLAN.md` |


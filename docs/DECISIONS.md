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
  the narrowest open question, plus the same answer's own candidates (D207, D259, D264, D265); the coverage-start records link to every
  question that read them (D364).
- **The Idea's theses.** D282's "the model cannot assign weights or alter the selected theses" is amended by D288–D290: the model adopts
  and weights the theses.
- **Citations.** D92's "theme colours only" is amended by D284 (plain blue citations).
- **Services.** D112 packages the two services for Docker; on this Mac they are tested on the host because the VPN blocks container
  networking (AGENTS §9). Both hold.
- **Defaults.** Each "`poc-vNN` is the default" decision is superseded by the next; only D366 stands.

## 1. System (PRD 00)

- **Two modes** (D10, D12, D13, D14, D56): the stream moves the library only when an item arrives and never reads the calendar; pull
  mode is the only place where time triggers work, with its "now" passed in. The boundary is a stream of classified items from
  upstream; nothing pulls sources; an upstream id and version is processed once.
- **Time** (D5, D9, D34): an item's time is its own publication time, cut to its New York calendar day; no rule reads the computer's
  clock (`retrieved_at` is for audit); the time of day orders nothing; an SEC filing's day is its filing date (accepted before 17:30 ET,
  that day; after, the next business day).
- **No input store** (D7): the materials stay in the team's database; the system keeps a processing record of each item and version
  processed; testing streams a test database through the same path.
- **Order and one writer** (D31): dispatch numbers items in arrival order; each question has one writer; an item reads only the state
  left by smaller numbers, except that extraction reads the open questions of the start of the item's day (D251); the result equals
  one-at-a-time processing.
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

- Config holds only the choices a person makes: model settings (one per extraction category and one per model call: matching, the
  collision judge, re-judging, the coverage-start reading) and the search size; mechanisms belong to code and what is researched to the
  universe (D2, D41, D190, D364).
- No limits section: no budget and no concurrency in Config; worker counts are run arguments (D3, D181, D183).

## 5. Dispatch (PRD 04)

- Dispatch is the single entry: one decision tree asks whether the item meets the contract (no: refused, to the review pool), whether
  the same id and version was processed (yes: skipped) and what its classification outcome is; every item reaches one destination (D17).
- An item's related objects play no part in dispatch (D4). Known departure: the POC's `dispatch.route` filters by related object and
  tracked category, a scope D18 gives to upstream.
- Items published before coverage start are not dispatched; the coverage-start reading reads the latest report itself (D364).

## 6. Extraction (PRD 05 and the extraction standard)

- **One module, one call per item** (D25, D27, D33, D199): every item of a tracked category is read whole by its category's template, a
  senior hedge-fund analyst's prompt; tables without tags are read by the model with no separate parsing code (D23); the program owns
  the output shape and checks every quote against the source; extraction never changes the library. One call per item; repeated calls measure stability and never vote or combine into one answer (D193, D338).
- **What it hands over** (D42, D209, D264): evidence, each piece with its source, filed under the questions open at the start of its day
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
- **The day's snapshot** (D251): every item of a day sees the same open-question list, that of the start of the day; the archive key
  carries the snapshot; a day in flight never re-sends an item because the ledger moved.
- **The request** (D237, D249, D252): a general hedge-fund brain, its rules and examples reading the same for any company and naming no
  covered company or test article; a closing check at the end of the same request reads the evidence list back by the standard's test and
  its not-kept rows; noise is taught by general paired examples; a version is accepted on core and supporting recall first, then noise.
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
- **Seeds** (D253): a covered company's seed questions are written into an empty ledger before the first day from `poc/seeds/`, keyed by
  code so an article-born candidate for the same quantity merges into the seed. A seed's dependency arrow means "supports" (D368, by
  D208): for filing, the supporting (driver) question is the narrower one; for judging, the supported (root) question reads the
  supporting questions' conclusions, so drivers and themes are judged before their roots. The judging code reads the stored edge the
  other way today *(fix to be built and measured, D368)*.
- **The thesis tree** (D208): every company's library has root quantities (its reported lines), a driver layer of seven fixed classes
  (demand, supply and inputs, competition and share, pricing and installed base, product cycle, policy, capital and obligations) whose
  instances the analyst writes once at coverage start, each declaring the root it feeds, and shared macro themes, each company's
  direction a declared dependency with a channel sentence the judge reads, macro evidence filed only under the macro theme; roots read
  the drivers' and themes' conclusions; the template routes and never gates. Built: the seeds (D253); the rest *(not built)*.
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
- **The coverage-start reading** (D363–D366): at coverage start, after the seeds, each open question reads the company's latest earnings
  report once (prompt `baseline-v3`, frozen with its check: no further prompt version without Alex's decision, D365); code keeps a figure
  only when its quote is the report's own text with a label and the value printed
  (a table row quoted with a footnote mark left off or a cell left out is stored as the report's own text from the row's label to the
  figure); one record per item and quote,
  linked to every question that read it (the daily one-home and narrowest rules do not apply); the first day's round judges those
  questions; restatements stay out of the daily stream (standard §5.3). It runs in the replay default `poc/config/poc-v116.json` (D366),
  which refuses a run without `--seed`.

## 11. The ruler and measurement (AGENTS §7)

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
- **The replay default** (D366): `poc/config/poc-v116.json`, with the items database `poc/data/items-nvda-2026-07-01-10-27.sqlite`.
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
| D41 | 2026-10-20 | What the rebuilt views database changes outside it | in force (amended by D42, D45, D51, D54, D190, D191, D195, D356) | §4 Config |
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
| D209 | 2026-10-28 | A statement no open question takes is dropped at extraction; evaluation reads the dropped record, not a sid… | in force (amended by D264) | §6 Extraction |
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
| D243 | 2026-10-29 | The extraction standard is signed: proposal 5 stricter, the other eleven at their leans; lean cautious, cat… | in force (amended by D248, D250, D261) | §11 The ruler and measurement |
| D244 | 2026-10-29 | Claude sets the dev/test split; scores are leads and Claude reads the traces every time; first the role-v29… | in force (amended by D261) | §11 The ruler and measurement |
| D245 | 2026-10-30 | role-v42 (`poc-v58`) is the extraction request; its must-not questions on small release dates are the next… | superseded by D246 | Extraction |
| D246 | 2026-10-30 | role-v51 (`poc-v67`) is the extraction request | superseded by D247 | Extraction |
| D247 | 2026-10-30 | role-v53 (`poc-v69`) is the extraction request: the attribution fields are defined in the schema | superseded by D265 | Extraction |
| D248 | 2026-10-30 | What counts as one question and one piece of evidence: seven boundaries, chosen one by one | in force (amended by D257, D258, D368) | §6 Extraction |
| D249 | 2026-10-30 | A test the model applies to each statement is a check at the end of the same request; role-v63 (`poc-v79`)… | in force (amended by D265, D274) | §6 Extraction |
| D250 | 2026-10-31 | Four evidence boundaries and the counting unit settled; the ruler is fixed before any further measurement (… | in force (amended by D261) | §11 The ruler and measurement |
| D251 | 2026-10-31 | The extraction request may read the open questions as a daily snapshot (architecture under test) | in force (amended by D264) | §1 System |
| D252 | 2026-10-31 | The extraction prompt teaches what noise looks like, with general paired counter-examples; useful theses an… | in force | §6 Extraction |
| D253 | 2026-10-31 | D208's first step is built: seed questions for a covered company, written before the run, as homes for evid… | in force (amended by D368) | §7 Thesis library |
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
| D264 | 2026-11-02 | The extraction reads the day's open questions with their takes lines and files the statements itself (extra… | in force (amended by D265, D274, D359) | §6 Extraction |
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
| D363 | 2026-11-05 | At coverage start, the company's latest reported figures enter once from its own latest report; restatement… | in force | §10 Current phase: filing that links facts the way an analyst does |
| D364 | 2026-11-05 | The coverage-start reading is built into the product; a figure several questions read is one record linked… | in force (amended by D365, D366) | §4 Config |
| D365 | 2026-11-05 | The coverage-start reading is the third version with the repaired check; built into the product behind poc-… | in force (amended by D366) | §10 Current phase: filing that links facts the way an analyst does |
| D366 | 2026-11-05 | `poc-v116` is the replay default; the branch is committed and opened for review | in force | §10 Current phase: filing that links facts the way an analyst does |
| D367 | 2026-11-05 | Decisions and working rules consolidated: a register of what is in force, the log kept whole; README, AGENTS and the state page cleaned | in force | [this page, opening](#consolidation) |
| D368 | 2026-11-05 | Alex's answers to the seven items left open by the consolidation | in force | §1, §6, §7, §8, §10, §11 |
| D378 | 2026-11-06 | The split extraction is sealed as a failed experiment; its useful lessons become production experiments (PRD 11) | in force; experiments open only on Alex's word | §6 Extraction |

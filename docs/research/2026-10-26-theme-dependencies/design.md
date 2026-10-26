# Theme theses and their links to companies: design

> **Decided 2026-10-26 (D191).** Alex rejected the requirement that a theme name the company thesis it feeds: "一个政策影响非常的广 … 不可能所有的公司都 map 到 … 默认这些宏观的东西和所有公司都有影响 … 1 to all mapping … thesis 的 state 对每个不同公司的影响需要别的方法来判断". Points 2, 3 and 4 were accepted. §1 (`feeds` on theme candidates) and the first row of §2 are therefore withdrawn; the replacement is §7 below. The rest stands as the record of the alternatives considered.

Alex, 2026-10-26: macro, policy and cross-company themes ("geopolitics in the Middle East may impact prices positively but
inflation … cross-correlations … overarching themes … we didn't have a clean idea on how to design for that"); "可以的我觉得
可以做，你也并行的来做深度思考怎么做是最贴近系统设计，PRD 还有一个 hedge fund analyst brain 的". This is a design, not a
build. A Codex read-only proposal (scratchpad `codex-theme-design.out.md`) was read and challenged; where this document
differs from it, the difference is stated.

## What the PRD already has, and what has never run

| Piece | Where | Status on the r3 ledger |
|---|---|---|
| Theme thesis: a question about the world with an outcome ladder, no good/bad label | 06-views "Two thesis kinds" | 16 theme theses (9 export-control stages, 7 aggregates) |
| Dependency: thesis B reads thesis A's conclusion, with a direction per dependant (rate cuts: bullish for Ethereum, bearish for JPM) | 06-views dependency tree and rules | 0 rows, ever: the Jev matcher writes `dependencies: []` for every candidate (`jev_matching.py` line 249) and the extractor is never asked |
| Awaited dependency: B depends on A's next-period thesis that does not exist yet; bind when created | 06-views dependencies, `store.dependencies` (`wait_chain_view_id`, `wait_year`) | 0 rows |
| Research group: the folder for one continuing matter across companies and themes | 06-views research groups (D149) | 24 groups, 38 memberships |
| Rejudging propagates a changed conclusion to dependants | 06-views state rules | never exercised |

So the design exists; the part that makes a theme worth holding (its links) has no producer. Everything below is about
producing and checking links, not about new concepts.

## How a senior analyst holds a theme (the brain to copy)

- The unit is a dated, falsifiable question about the world with a few outcomes: "where is the Fed's upper bound after
  the December meeting", "does Commerce license H200 sales to China this year", "what do the five hyperscalers spend in
  2026". A regime name ("Middle East tension") is a folder, not a question; a scenario ("supply restored / partly / cut off")
  is a rung.
- A theme earns its place by the lines it moves. The analyst writes the chain explicitly: theme outcome → company line
  → sign. Oil up: producers' revenue up, airlines' fuel cost up. Same theme, two signs, each stated at the company.
- Few at a time: three to five live themes per desk, rotating. The count is an outcome of the test "does any name I
  hold move on this", never a cap.
- Links are added when the company is read, not when the theme is. The theme can be written first (from a macro
  document); the link appears the day a company document shows the mechanism.
- A proceeding (a prosecutor's charging decision) is not a theme unless it changes a line (market access, supply, a
  cash obligation). It can be evidence to a thesis that exists.

## The design

### 1. What a theme candidate must state

A theme candidate (`kind = theme`, reason `policy_stage` or `shared_quantity`, see §4) carries, beside the fields of D184:

```
feeds: [ {target: <shown asset thesis id | this answer's candidate id | typed target>, direction: <see below>, why: <one sentence, source-grounded>} ]
typed target = {object: <ticker in the universe>, measure: <vocabulary>, scope: <text>}   # for a company thesis that does not exist yet
```

- `direction` for an asset dependant: which end of the theme ladder is favourable for the company line (`first_end`,
  `last_end`), as the PRD's dependency rules already define; for a theme dependant: `same` or `opposite` orientation.
- At least one entry is required for a theme candidate (schema `minItems`-equivalent enforced in `sift`); a company
  candidate may carry `feeds` too (a company thesis that depends on a theme), optional.
- A typed target (no id) is allowed only from an item that shows no thesis of that company: the extractor names the
  line it would move; the writer records the dependency as awaited by key (object, measure, scope), the same table and
  mechanism as the awaited chain/year of today, and binds it when a thesis with that key opens (the writer checks at
  every write, as it checks awaited years today).

### 2. When a theme thesis opens

| Item | Rule |
|---|---|
| A company item (the company's theses are shown) | The theme candidate names a shown company thesis or a candidate of this answer; opens with its dependency in one write (06-views: theme theses are written before asset theses in one transaction) |
| A macro-only item (no company in the item) and the theme is in the universe's theme list | The candidate may open with a typed target; the universe's list is the analyst's standing map of what moves the names, and the typed target says which line |
| A macro-only item and the theme is not in the list | Not opened; the handover keeps the candidate and its evidence as a refused record with reason `theme without a dependant` (nothing is lost: the review pool already keeps refused samples, D26) |
| Any item | A theme candidate with no `feeds` entry is refused by code |

Codex proposed a third lifecycle state ("pending candidate" kept for later retrieval). Not adopted: it adds a state and a
retrieval path; the awaited-dependency mechanism already carries a typed, unbound link, and the universe's theme list
decides the cold case. If the measurement shows real themes lost to the "not in the list" rule, the list is the thing to
extend (a universe change, Alex's call), not the lifecycle.

### 3. How later items add links

- A later company item whose model reads a theme in its shown list (block 5 shows the theme theses linked to the
  item's objects today only through dependencies; it must also show the open theme theses of themes the item is
  tagged with, which classification already supplies as object identifiers) may answer `feeds` on an *existing*
  company thesis: `{target: v30, depends_on: v12, direction, why}`. This needs one change the PRD does not allow today:
  "choose dependencies only when B is created" becomes "when B is created or when an item first shows the mechanism";
  the writer adds the dependency with its sequence number, append-only, and rejudges B.
- A correction (an item shows the opposite sign) appends a new dependency record and marks the old one superseded
  (same shape as evidence replacement); history keeps both.
- A second company reading the same theme adds its own link with its own sign; nothing is copied across companies.

### 4. The admission reasons, amended

- `policy_stage`: a stage of a policy process, decided by a named authority, **whose outcome moves a company line the
  candidate names**. A proceeding with no such line is evidence or nothing.
- `industry_aggregate` becomes `shared_quantity`: a quantity or price outside any one company that several companies
  move on (an industry aggregate, an oil price, a policy rate, an exchange rate), one per calendar year, **with the
  company lines it moves named**. This absorbs Codex's proposed `macro_condition` without a fifth category: oil and the
  Fed are shared quantities; a licence regime is a policy stage.
- `main_driver`, `binding_obligation` unchanged. The four reasons stay a closed enum.

### 5. What code checks and what stays judgement

| Code refuses | The model judges |
|---|---|
| a `feeds` target that is neither shown, nor a candidate of this answer, nor a typed target whose object is in the universe | whether the mechanism is real and the sign right |
| a theme candidate with no `feeds` | whether the theme matters enough to hold |
| a direction value outside the enum, or a direction on a theme→theme link that is not same/opposite | whether two shared quantities are one question (matching's job) |
| a cycle (today's check), a self-link, a duplicate live link | when to retire a theme (pull mode, D63 due-date freeze) |
| a typed target from an item that shows a thesis of that company (it must name the id) | — |

### 6. Matching and writing

- Matching resolves the candidate's identity as today; the Jev path must carry the extractor's `feeds` into the
  matching answer's `dependencies` (today it writes `[]`). The generative path already has the field.
- Writing: theme theses first (as today), then company theses, then dependencies; a dependency on a candidate that
  was merged into an existing thesis is re-pointed to that thesis (today: re-pointed only to new views; a merged
  candidate's dependency is dropped with a note, which would lose most links).
- A dependency written on an existing thesis triggers its rejudgement (06-views: a new link changes inputs).

## State × event

| State | Event | Transition, what is written |
|---|---|---|
| no theme thesis; company item names a mechanism | theme candidate with `feeds` on a shown company thesis | theme opens; dependency (B→A, direction) written in the same transaction; A judged, then B rejudged |
| no theme thesis; macro-only item, theme in the universe list | candidate with a typed target | theme opens; awaited dependency by key written; no rejudgement yet |
| no theme thesis; macro-only item, theme not in the list | candidate | refused `theme without a dependant`; evidence kept in the handover's refused record |
| theme open, awaited link by key | a company thesis with that key opens | the writer binds the link, records the resolution, rejudges the company thesis |
| theme open | a second company's item shows the mechanism | a new dependency on that company's thesis, its own sign; rejudge it |
| theme open, dependants open | theme rejudged, conclusion changed | dependants rejudged in the same round (today's rule) |
| theme open | an item shows the opposite sign for one dependant | append a new dependency record superseding the old; rejudge that dependant |
| theme open | its last dependant closes | theme stays open until its own due date (an analyst keeps the macro question; a new name may link) |
| theme due | pull mode freezes the state (D63) | dependants read the frozen conclusion; an awaited successor follows the chain rules of today |
| any | crash mid-write | the transaction rolls back whole (today's atomic write); the item is re-dispatched |
| any | parallel day: an earlier commit opened the company thesis a typed target names | the stale request is re-prepared (D181); the candidate then sees the id and must name it |

## Value × reader

| Value | Writer | Readers today | Change needed |
|---|---|---|---|
| `dependencies` rows (view_id, depends_on, direction, wait_*) | writer, from the matching answer | judging (reads upstream conclusions in dependency order), service `/views` and the UI graph, idea route (upstream neighbours with direction; downstream direction `None`) | writer accepts links on existing theses and re-points merged candidates; service returns the direction both ways |
| `feeds` on a candidate | extractor (schema v13) | sift (shape), matching (carries), writer | new |
| typed target (object, measure, scope) | extractor | writer (awaited by key), the daily bind check | new column or reuse of `wait_chain_view_id`/`wait_year` with a key form; decide in the build |
| theme list of the universe | universe.json | extraction block 3, classification | gate for cold opening |
| dependency supersession | writer | judging (reads the live link), UI history | new record kind |

## New path × old checks

| Old check | New path |
|---|---|
| cycle check before an edge | unchanged; also on a later-added edge and on binding an awaited key |
| 06-views "count a statement once": a statement about A is A's evidence; B learns it through A | unchanged; the extractor links the policy statement to the theme candidate, the company thesis gets the dependency, not the evidence |
| rejudge order: dependencies before dependants | unchanged; a later-added edge enters the same ordering |
| D184 admission checks | theme candidates add the `feeds` check; company candidates unchanged |
| D155 identity | untouched: a typed target binds by key only when the key is exact (object, measure, code-owned scope); a model-worded scope waits for matching to resolve, as a candidate would |
| request identity of stored calls | schema v13 is version-gated; versions ≤ 12 unchanged |

## Worked examples from the ledger

1. **Export controls → NVDA China revenue.** The May 20 call opens `policy_stage` "Will the Chinese authorities allow any
   H200 imports by January 31, 2027" with `feeds: [{target: <NVDA China data-center revenue FY2027>, direction: last_end
   (imports allowed) favourable}]`. If that company thesis does not exist (it did not, A03), the candidate names it as a
   typed target `{NVDA, segment_revenue, China data center}` and the writer waits; the first-contact rule of the next
   role version would open it from the same call. A later MU or AMD item on the same stage adds its own link and sign.
2. **Hyperscaler capex 2026 → NVDA data-center revenue; MSFT capex as a component.** The Feb 25 call opens the
   `shared_quantity` aggregate with `feeds: [{target: v2 NVDA data-center revenue, direction: last_end (higher spend)
   favourable}]`. MSFT's own capex is MSFT's `main_driver` thesis (D187); the MSFT call adds `feeds: [{target: MSFT capex
   thesis → depends on the aggregate? no: the aggregate depends on the components}]`. Direction of composition is the
   open design point: the analyst reads the component as evidence to the aggregate, not as a dependency; this document
   keeps the PRD's rule (a statement about MSFT capex is MSFT's evidence; the aggregate learns it through the figure a
   later item reports), and records the question for Alex.
3. **Middle East / oil (hypothetical).** A `shared_quantity` "Brent average in Q4 2026" opens from a macro item with
   typed targets `{XOM, total_revenue}` (first end favourable: higher) and `{DAL, operating_margin}` (last end
   favourable: lower); each binds when that company's thesis exists; each company's later item may correct its sign.

## What to measure first, at no cost

- On the r3 archive: for the 25 theme candidates, re-send the extraction requests under a v13 schema with `feeds`
  required (3 samples each, about $0.10) and count how many name a shown company thesis, a typed target, or nothing;
  read the nothing cases: are they the proceedings?
- On the r3 ledger: how many company theses would have gained a link (the 9 export-control and 7 aggregate theses against
  the 23 NVDA theses) by the eight rules, read by hand; that is the gold for the first run.

## Decisions for Alex

1. Rename `industry_aggregate` to `shared_quantity` and require `feeds` on theme candidates (this document §1, §4).
2. Allow a dependency to be added to an existing thesis by a later item (changes 06-views "only when B is created").
3. The cold case: a theme from a macro-only item opens only when the theme is in the universe's list; otherwise refused.
4. Composition (component ↔ aggregate) stays evidence, not dependency, as the PRD has it.

## 7. The decided shape: one theme, every company; the sign decided at judgement

- A theme thesis opens on its own admission test (D184 `policy_stage` / `shared_quantity`: a stage or quantity outside any one
  company that several companies move on, with the authority or the settling figure named); from a macro-only item only when
  the theme is in the universe's list (point 3). No edge is written at extraction for themes.
- Every company thesis is judged with the open theme theses of its themes in view: the judging request gains a block "Themes in
  force" listing, for each open theme thesis of a theme the company's items were tagged with, its question, current rung and
  the reasons of its last judgement. The judge states, per theme it uses, the sign it applies to this company ("licences
  granted: favourable for China revenue") in the judgement's reasons; code checks that a cited theme is open and tagged, as it
  checks cited evidence today. This is the "别的方法": the sign lives in the company judgement, where the analyst decides it,
  not in a table written in advance.
- Propagation: a theme's changed conclusion is not fanned out to every company thesis in the same round (06-views: a repeated
  Fed statement must not trigger hundreds of dependants); each company thesis reads the current theme states at its next
  judgement, which its own evidence triggers. A theme whose state changed with no company item that day is caught by the daily
  judging round of its tagged companies' open theses (D63), bounded by the count of open theses, not of edges.
- Explicit dependencies remain for what a document states (a company thesis that reads another thesis's conclusion), may be
  added later (point 2), and keep the cycle check.
- Research groups keep organising; the admission test keeps proceedings out (a prosecutor's charging decision names no stage
  of a policy that several companies move on).
- Value × reader change: judging's request builder (new block), judging's answer check (cited themes), the UI (a company card
  can show the themes in force), the idea route (themes as context). The dependencies table is unchanged.
- What to measure first, at no cost: on the r3 ledger, for each of the 23 NVDA theses, list the open theme theses tagged to
  its items on each judgement day and the count of judgements that would have carried a theme block (today 185 judgements,
  0 with a theme in view); then re-send three judgements with the block and read whether the sign is stated and right.

## 8. Build design for the decided shape (2026-10-26, evening; AGENTS §2 tables; revised after the Codex review, 8.8)

Alex: "做，先零成本数完再改；然后你得确认这个架构和逻辑是对的". §§1–6 and their tables describe the withdrawn `feeds` shape and
stay as the record of what was rejected; this section is the design the build follows. One word: a **theme block** is the
part of a judging request that lists the open theme theses and their current conclusions.

### 8.1 What the stored ledgers say ($0, `theme_block_census.py`)

| | r3 (`poc-v25`) | r4 (`poc-v26`, the default) |
|---|---|---|
| judgements: company / theme | 162 / 23 | 175 / 11 |
| open theme theses in the window | 16 | 6 |
| company judgements that would carry a theme block, one to all | 162 of 162 | 175 of 175 |
| theme lines per block (min / median / max) | 1 / 11 / 16 | 2 / 3 / 6 |
| company judgements with a theme tagged on the items behind its evidence (the narrow reading) | 12 | 14 |
| theme judged in the same day round but after the company thesis | 88 | 9 |
| theme judgements with a changed conclusion (first judgements among them) | 22 (16) | 10 (6; the other four: 3 rung moves, 1 facts only) |
| theme change × open company thesis pairs; of them never judged again in the window | 525; 269 | 228; 109 |
| additional judgement calls under propagation (distinct thesis × round, not judged in that round anyway); from first theme judgements | 209; 194 | 141; 100 |
| judging cost of the window at `model.PRICES` | | 186 calls, $0.32; the additional calls about $0.24 |

Three findings decide the shape. The narrow reading ("the themes the company's items were tagged with", D191's consequence
note) shows a block in 14 of 175 judgements: items carry a ticker, rarely a theme, and the universe's themes list no members;
Alex's rule is one to all, and that is the only one with data behind it. Ordering matters: in r4 nine company judgements
would have read a theme's state from before the same round, because the round judges in dependency order only. Without
propagation, half the open company theses never read a changed theme conclusion inside the window; with propagation on the
`changed` flag the window's judging grows by 141 calls (100 of them because a theme thesis was judged for the first time,
which the code marks changed).

### 8.2 The shape

1. **The block.** When an asset thesis is judged under `judging-v4`, its request carries, after the dependencies,
   `[Themes in force, N]`: every open theme thesis with a current state, one line each: id, theme name, question, due day,
   current rung label, the reasons of its last judgement (first 300 characters), the day of that judgement. A theme thesis
   with no judgement yet, or closed, is not listed. A theme thesis's own judgement carries no block.
2. **The answer.** The judgement schema for v4 gains `theme_pushes: [{view_id, push}]`, `push` in the existing `PUSHES` enum
   (toward_first, toward_last, none): the same word as an evidence push, because it is the same thing, the direction this
   conclusion moves this thesis (Codex 8.8/8: the vocabulary and the readers allow it). Code refuses an id not in the block, a
   duplicate id, or a push outside the enum (one retry, then the item fails, as every judging error today). The judge lists
   the themes it weighed; an unlisted theme was not used. `cites` and `cites_views` keep their meaning; a theme conclusion is
   never cited as evidence (06-views: our own judgement is not evidence).
3. **Stored and served.** `judgements` gains the column `theme_pushes_json` (added by `ensure_writable_columns`, as `rungs`
   gained `lo`/`hi`). `service.state_as_of` (behind `service.view`) and `service.history` return it as `theme_pushes`; a
   ledger written before the column (opened read-only, no migration) returns `[]`. The UI is unchanged in this slice: its
   adapter keeps reasons and citations and drops `pushes` already (`poc/ui/src/adapters/bundle.js`), so the sign reaches a
   reader through the reasons; showing the block on the page is its own slice.
4. **Order in the round.** `round_of_judgements` judges theme theses before asset theses: an asset thesis waits while any
   pending theme thesis is unjudged, the way it waits for its upstream dependencies today; dependency order still comes
   first. A theme that depends on an asset thesis is a corner no current ledger can reach: the Jev matching path writes no
   dependencies (`dependencies` has 0 rows in every v23-jev, v25 and v26 ledger; only the generative-matching and the
   October 23 ledgers have any), so it is recorded in 8.3 as accepted, not designed around.
5. **Propagation.** A theme judgement whose `changed` is true queues every open asset thesis with evidence in force, the
   rule dependants follow today; each is judged once per round. `changed` already excludes a repeated statement (judging
   prompt: "repetition or another source for the same statement does not alone change the conclusion"), and 06-views wants
   a facts-only change to reach a dependant ("AMZN capex moving from 12% to 25% can trigger NVDA even within the same
   rung"), so `changed` is the PRD's filter. **This reverses the consequence note under D191** ("a changed theme conclusion
   does not fan out to every company thesis in the same round", written by the assistant, not Alex's words) and is the one
   choice for Alex in 8.6; the census gives its price (141 calls, $0.24 on the window) and what the alternative costs (109 of
   228 theme changes never read).
6. **The round's queue comes from the ledger, not memory.** Today a round's pending set lives in memory: a crash or a refusal
   after some judgements committed loses every dependant that a changed judgement had queued, and the resumed round (seeded
   from the day's written changes, skipping views judged at this seq) never recovers them (Codex 8.8/1, reproduced on a
   copy). The slice fixes it where the data is written: the round's starting set is the day's changed views ∪ the dependants
   of every view judged at this seq with `changed` ∪ (v4) every open asset thesis with evidence in force when a theme thesis
   was judged at this seq with `changed`; a view already judged at this seq is skipped. This is one derivation, used at
   start and at resume, and it fixes the existing hole for explicit dependants on the same path.
7. **Versioned.** `judging-v4` (prompt text: the block's reading rules; schema: `theme_pushes`), `poc-v29` = `poc-v26`
   with `rejudging.prompt_version: judging-v4`. The block, the field, the theme-first order and the propagation are all
   gated on the version (≥ 4): under v3 the round schedules exactly as today, so stored v3 requests and the "previous
   conclusion" text they carry replay byte-identical. (`scripts/preflight.py` has no judge replay: its part A checks only
   stored schema-refused answers; nothing here changes that.)
8. **Explicit dependencies are unchanged**, including D191 point 2 (a dependency added to an existing thesis later), which
   is not built in this slice.

### 8.3 State × event (an asset thesis B, the open theme theses T)

| State of B | Event | Transition; what is written; the date read |
|---|---|---|
| open, evidence in force, no judgement yet | its first judgement | request carries the block with every T judged so far; answer's `theme_pushes` stored on the judgement row; `changed` must be true (today's rule) |
| open, judged | new evidence or replacement (today's triggers) | rejudged with the block as of this round, themes first |
| open, judged | a T's judgement in this round says changed | B is queued in the same round (once); its request reads T's new state because T went first |
| open, judged | a T's judgement in this round says not changed | nothing; B's next judgement reads the same state |
| open, judged | a new T opens from today's item and is judged | T's first judgement says changed (rule) → B queued; B's block includes the new T |
| open, judged | a day where only theme theses changed | the round starts with themes only; a changed T queues the open asset theses; a day with no change judges nothing (today) |
| open, judged | a T closes (pull mode, D63 due-date freeze) | T leaves the block; B is not rejudged for the closure (nothing new was concluded); T's frozen outcome reaches B only through an explicit dependency (which reads a closing state, 06-views) or not at all. Accepted: a closed theme is history, as a closed asset thesis is |
| open, no evidence in force | a T changes | not judged (D59: no evidence, no judgement); the block is read when evidence first links |
| closed | anything | not judged (today's rule) |
| open, judged earlier in this round | a T that depends on B changes after B (dependency order put B first) | B is not judged twice (once per round); reads T's new state at its next judgement, which only its own evidence or another theme change triggers. Accepted: unreachable on the Jev path (8.2/4) |
| T open, evidence in force, never judged | B is judged | T is absent from the block (it has no state); T is judged in the round its evidence changed, so this is a crash corner that 8.2/6 closes |
| any | the judgement answer names a theme not in the block | refused, one retry with the note, then `JudgementRefused` (today's path) |
| any | crash or refusal mid-round | the day step fails; on resume the queue is re-derived from the ledger (8.2/6): judged views skipped, queued dependants and propagation targets recovered |
| any | configuration changed in between (v3 → v4) | requests from the switch on carry the block; earlier judgements keep their rows; `config_checksum` on each row records which; no rejudgement of T is forced by the switch |
| any | parallel day (D181) | judging is the day's serial step after the items (`replay.py`), then pull mode; unchanged |

### 8.4 Value × reader

| Value | Writer | Readers | Change |
|---|---|---|---|
| the theme block (request text) | `judging.build_prompt` for v4 and asset theses | the model; the archive (`request_json`); replay by sha | new, version-gated |
| `theme_pushes` (answer) | the model; `check_answer` refuses bad ids | `judging._record` | new |
| `judgements.theme_pushes_json` | `_record` | `service.state_as_of` / `view` and `service.history` (returned as `theme_pushes`); `bundle.py` (copies judgement rows for the UI bundle); the UI adapter (drops pushes today, unchanged); reports (`scripts/report.py`, `trace_items.py`, `show_views.py`, `review_english_run.py` read rung/reasons/changed only) | column by migration; explicit selects add it with an absent-column fallback |
| `changed` on a theme judgement | the model (as today) | `round_of_judgements` (now: queues open asset theses); `service.changes` (lists every changed judgement with its evidence; propagation-only judgements that say changed appear there, as they should) | new reader of an existing value |
| the number of judgements per thesis | the round | `service.state_as_of` (`rounds`), `service.record` (last check), `replay.py` day counters (`judged`, `changed`), `bundle.py`, the reports above; tests `test_service.py`, `test_english.py`, `test_sequential_replay.py` assert on these counts for v3 ledgers (unchanged under v3) | counts rise under v4 by the 8.1 numbers; no code change, the measurement reads them |
| `rejudging.prompt_version` | config file | `judging.schema_for`, `build_prompt`, `retry_note`, `round_of_judgements` (order and propagation gate) | `judging-v4` added; `is_english` unchanged |
| `object_kind` of a view | writer (`views` row) | `round_of_judgements` (theme first; propagation target set), `build_prompt` (block only for assets) | new readers of an existing value |

### 8.5 New path × old checks

| Old check | On the new path |
|---|---|
| `check_answer`: cites ⊆ evidence in force; cites_views ⊆ dependencies; rung in range; changed on the first judgement and on a rung move | unchanged; plus theme ids ⊆ block, no duplicates, push in the enum |
| one judgement per view per seq (unique index) | unchanged; propagation and the re-derived queue cannot judge a view twice in a round |
| dependency order (`topological`) and the upstream wait | unchanged; the theme-first wait is added after it |
| D59: no evidence, no judgement | unchanged; propagation and the re-derived queue filter by `eligible` |
| replay identity of stored requests (byte-identical under the same version) | v3 requests and scheduling unchanged; v4 is a new sha population |
| `docs/check.py` glossary words | "theme block" is added to the glossary with its ruled-out words ("theme context", "macro block") |
| tests of judging (`test_english.py`: v3 prompt text) | unchanged; v4 gets its own tests: the block lists only open judged themes; themes first in the round; a changed theme queues open asset theses once; a theme id outside the block is refused; the queue re-derived at resume recovers a queued dependant |

### 8.6 Prior decisions searched, and the one choice for Alex

- D191 (this design's decision): one to all; sign at judgement. Its consequence note (assistant's) says "a changed theme
  conclusion does not fan out to every company thesis in the same round"; 8.2/5 proposes the opposite on the census. **Alex
  decides:** (A) propagate on `changed`, as explicit dependants do today (141 extra calls, $0.24, on the window; every open
  asset thesis reads a theme change in the same round); (B) keep the note: no propagation, a theme change is read at each
  asset thesis's next own judgement (109 of 228 never inside the window); (C) propagate only on a rung move (3 of 10 events
  in r4; a facts-only change such as a higher aggregate estimate does not reach the companies, against 06-views' AMZN
  sentence). Lean: A; it is one rule for dependants and themes and the PRD's own filter.
- D63 (daily judging round, due-date freeze) and D59 (no evidence, no judgement): kept; the block does not create judgements.
- 06-views "Dependencies are the sole way theses influence each other" and "Choose dependencies only when B is created":
  the first sentence is amended by this slice (the theme block is the second way, read-only, with the sign decided at
  judgement); the second is amended by D191 point 2, not built here.
- D181 (parallel day): judging is the day's serial step; untouched. D186/D187: not touched. D19/D37 (frozen inputs and
  extraction): nothing here changes them (Codex 8.8/10).
- D154/D155 (code owns identity, the model owns importance): the block adds context, decides nothing in code.

### 8.7 Measurement for the slice

1. Stored data ($0): the census above; the unit tests on a temporary ledger, including the resume recovery.
2. Three stored v3 judgement requests of asset theses from r4 (one NVDA data-center revenue, one AMD, one a company whose
   item is unrelated to the themes), rebuilt under v4 from the ledger as of that seq and re-sent once each (about $0.01):
   read whether `theme_pushes` names the right themes with a sign a reader would give, and whether the reasons say why.
3. One replay of the window under `poc-v29` beside r4: judgements, judgements carrying a non-empty `theme_pushes`,
   propagation-only judgements and their `changed` share, judging cost, and ten reasons read side by side with r4's.

### 8.8 The Codex read-only review (scratchpad `codex-theme-block-review.out.md`) and what it changed

Twelve findings, each read against the code before acting: (1) a resumed round loses queued dependants (reproduced; pre-existing
for explicit dependants) → 8.2/6; (2) a theme depending on an asset thesis judged after it → 8.3 row, accepted and shown
unreachable on the Jev path; (3) "next round" not guaranteed → same row, stated plainly; (4) closure does not produce a successor
→ 8.3 closure row corrected; (5) missing states → three rows added; (6) propagation reverses D191's note → 8.6, Alex's choice;
(7) the census double-counted pairs and read tags from the day marker → script corrected, 8.1 numbers replaced (228 → 141
additional calls; tagged 0 → 14); (8) `theme_pushes` vocabulary fine, UI drops pushes → 8.2/3 and 8.4 corrected; (9) readers of
judgement counts missed → 8.4 rows; (10) frozen modules untouched; (11) `service.current` does not exist → `state_as_of`,
absent-column fallback; (12) order and propagation must be version-gated, preflight has no judge replay → 8.2/7.

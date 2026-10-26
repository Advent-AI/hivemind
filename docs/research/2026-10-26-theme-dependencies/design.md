# Theme theses and their links to companies: design

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

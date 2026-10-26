# Thesis library

> Status: foundation frozen, October 20, 2026. D149 adds extraction-owned grouping; D165 puts it in the default pipeline. D169: the matching step runs on Jev by default (`poc-v23`); D168 states the Replace row's full definition and the succession answer it needs. English edition: October 25, 2026 (D163). Only recorded decisions apply; open questions and two pull-mode proposals remain separate.
> Design page: `docs/system-design.html` → New → Thesis library → Details. This PRD also owns Matching labels. Recorded decisions take precedence. Historical discussion: `docs/views-rebuild-log.md`.

## Purpose

A thesis has an immutable question, ladder and due date. Evidence moves its state, which freezes when due. Search then compare candidates with existing theses to merge, continue, create or skip; compare evidence within its thesis to repeat, replace or add. Extra source references alone do not trigger rejudgement. Extraction determines group associations; the writer preserves them after resolving final thesis IDs under the [grouping contract](#research-groups-associate-during-extraction).

## Rationale

- Clear structures connect theses, ladders and evidence to source items.
- A thesis is a question with a state, not an assertion. Opposing views move the same state's direction rather than creating opposite duplicate theses.
- A fixed, verifiable ladder states in advance what would disprove the view, analogous to explicit analyst scenarios or predefined investment exit conditions. Do not change it after observing the outcome.
- The model judges from all evidence still in force and dependency conclusions, at low temperature, rather than adjusting its previous score. Replacement follows statement date, so late old statements do not restore obsolete evidence.
- A theme's outcome can help one asset and harm another. Theme ladders describe outcomes; asset dependencies specify their own direction.
- A thesis contains one period and one due date, generally 6–12 months; intermediate quarterly reports are evidence. A thesis on a binding obligation a universe company takes on (a guarantee, financing, an equity stake, a purchase commitment) may set its own check day up to 18 months after the item, because the signing can be checked long before what it finances is built (D185).
- Search finds plausible matches and the model compares their meaning. A match inherits the existing ladder and due date; a merely similar question is new. D155's current POC additionally gives code ownership of fully determined duplicate identity, with its limits in the improvement plan.
- Evidence needs the same search-then-compare discipline. Otherwise February's 12% capex guidance and April's 25% revision remain side by side, forcing every judgement to rediscover which is current.
- Record repeat/replacement decisions once. Keep replaced evidence in history. A retelling alone should not require another model judgement to establish that nothing changed.
- Use two rungs for yes/no instead of forcing five.
- The model chooses dependencies like an analyst; code rejects cycles. Apparently mutual dependencies indicate poorly defined questions.
- Rejudge when inputs change. A changed conclusion includes a new rung or materially changed supporting facts/numbers. A repeated Fed statement should not trigger hundreds of dependants; AMZN capex moving from 12% to 25% can trigger NVDA even within the same rung.
- Start matching with a general-purpose model, retain records, obtain human labels and later train a faster smaller model.

## Structure

<!-- generated: structure -->
```
Thesis library
├─ Subject → Companies, cryptocurrencies, commodities and themes in the universe
│   └─ Thesis → A question + a ladder + a due date (Immutable once written. Five rungs, or two for yes/no. When matching opens a thesis, only one may be open for the same subject and focus at a time.)
│       ├─ State → The thesis's current ladder rung (Evidence pushes towards either end; the model judges from facts. A thesis from the user's memo is not yet judged until evidence first links to it.)
│       ├─ Link → Evidence (Store evidence once with sources and tier. Its push belongs to the link. Replaced evidence remains in history and no longer counts.)
│       ├─ Dependency → Another thesis (Direction specifies which end of the other thesis is bullish for an asset thesis, or whether the two ladders have the same or opposite orientation for a theme thesis.)
│       └─ Succession → The previous period's thesis (Successive periods of the same focus form a chain)
├─ Research group → Organise theses by a continuing business process (Associate during extraction; full rules are in “Research groups: associate during extraction”)
└─ Append-only records → Matching, rejudgement, succession, closure, reopening and labelling records (Append at every step, without editing or deleting. Read records up to a historical date to recover its judgement.)
```
<!-- /generated: structure -->

## Two thesis kinds

<!-- generated: kinds -->
| Kind | Subject kind | Ladder rungs | Example |
|---|---|---|---|
| Asset thesis | Tradable subjects: companies, cryptocurrencies and commodities | Five rungs: strongly bullish, bullish, neutral, bearish, strongly bearish. Two for yes/no: bullish and bearish. These describe the business impact; set them at creation and keep them fixed. | How will NVDA FY2027 China revenue compare with FY2026? |
| Theme thesis | Macro, policy and industry themes | Ordered outcomes from one end to the other: five rungs, or two for yes/no. Name outcomes without judging them good or bad. Dependent asset theses specify which outcome benefits them. | How will the Fed's target-rate upper bound after its last 2026 meeting compare with now? (Large cut … large hike) |

The same event can affect assets differently: rate cuts can be bullish for Ethereum and bearish for JPM net interest income. Theme theses therefore do not label outcomes good or bad.
<!-- /generated: kinds -->

## Ladder

<!-- generated: ladder -->
```
Two kinds of ladder (Illustrative ranges)
├─ Asset thesis: numeric → NVDA FY2027 China revenue versus FY2026 | Five rungs describing NVDA's business impact (Due on the FY2027 annual earnings date)
│   ├─ Strongly bullish → Up at least 50%
│   ├─ Bullish → Up at least 10% but under 50%
│   ├─ Neutral → Up or down by less than 10%
│   ├─ Bearish → Down at least 10% but under 80%
│   └─ Strongly bearish → Down at least 80% (At most one fifth remains)
└─ Theme thesis: event → China export licensing for chips covered by the April 2025 rule, including H20 and MI308, as of April 15, 2026 | Five ordered outcomes, without good/bad labels (Use the rules in force on that date)
    ├─ Rung 1 → Full ban; licence applications no longer accepted
    ├─ Rung 2 → Licences required; none issued
    ├─ Rung 3 → Licences required and issued; some conditional
    ├─ Rung 4 → Licences required and issued; all unconditional
    └─ Rung 5 → Licences no longer required
```

1. A ladder has five rungs. Asset theses run from strongly bullish to strongly bearish, describing business impact; theme theses name five ordered outcomes without good/bad labels. Use two rungs for yes/no rather than forcing five: bullish/bearish for assets; named outcomes for themes, such as signed by the deadline/not signed.
2. Each rung is verifiable: a numeric interval or event stage. Rungs must be exhaustive and non-overlapping, so exactly one applies at expiry. For example: up at least 50%; up 10% to under 50%; change under 10% either way; down 10% to under 80%; down at least 80%. Every boundary belongs to one rung. “Up a lot/a little” cannot be checked. Avoid vague partial outcomes; specify the partial state, such as conditional licences, as a distinct rung. State the comparison underlying neutral.
3. One ladder concerns one thing. Separate numeric and event questions and connect them with dependencies. Likewise, separate components that can move in opposite directions, such as H20 and Blackwell chip classes.
4. The extraction model writes the candidate's ladder. A new thesis adopts it unchanged until expiry. A merged candidate uses the existing thesis's ladder and due date.
5. Numeric theses name a year. Non-company quantities use calendar years: the publication year is this year and the following year is next year, each ending December 31. Company quantities use the fiscal year containing publication day and its successor. Never use the computer clock. For a given quantity, open at most one thesis for each of this year and next year; do not open later years. The due date is the quantity's publication date.
6. Set the due date when the debate can be resolved, usually 6–12 months away. Intermediate quarterly reports are evidence, not separate theses.
<!-- /generated: ladder -->

## State

<!-- generated: positions -->
|  | Meaning | Decision maker | Example |
|---|---|---|---|
| State | Our judgement of the thesis's current rung; evidence pushes toward either end | The model judges at low temperature from facts. Reconsider all evidence still in force, including each item's replaced predecessor to show the change, plus current dependency states and reasons and, for an asset thesis, the theme block. Do not increment or decrement the previous score. Cite evidence and compare with the conclusion before this round to state whether it changed. Do not rejudge if only source references were added and dependency conclusions did not change. | After the 8-K: strongly bearish |

- Every judgement states its basis in a fixed response shape: evidence IDs such as e12 and e15, plus dependency thesis IDs such as #1 when their changes triggered rejudgement.
- Code checks cited IDs against records: evidence must belong to this thesis and not be replaced; cited theses must be its dependencies. Accept only if all checks pass. Otherwise record the reason and ask for one corrected judgement. If that also fails, use normal failure handling: retry from this step, then human review after repeated failure. This checks references, not whether the judgement is correct, like verifying a cited page exists.
- Each judgement also declares whether the conclusion changed and explains why, comparing with the state and reasons before this round, including during retries. That earlier conclusion is for comparison, not incremental scoring. A rung change or a material change in the supporting facts/numbers counts: AMZN capex guidance moving from 12% to 25% growth changes the conclusion even within one rung. Repetition does not. A changed conclusion triggers dependent theses in the same round. Code requires changed=true for a first judgement or rung change; otherwise refuse under the same correction rules.
- For historical judgement, read the records saved on that date. Do not ask the model again; a new sample can differ.
<!-- /generated: positions -->

## Four evidence tiers

<!-- generated: tiers -->
| Tier | Example | Role |
|---|---|---|
| Fact | Official actions, published figures and completed transactions | Can establish which rung holds and move the state |
| Party statement | Company guidance, management statements and official speeches | Can move the state only |
| Third-party view | Sell-side analysts, media analysis and experts | Can move the state only |
| Rumour | Unnamed-source claims and unattributed statements | Can move the state only |

- The model determines the size of the push and gives reasons. No tier has a fixed score.
- Count independent original sources. Twenty outlets retelling one exclusive are twenty references to one evidence item, not twenty independent confirmations.
- Tier follows who confirmed it. An unnamed-source report that Commerce is issuing licences is a rumour. An official or company confirmation is factual evidence replacing it. The rumour remains a rumour in history.
- Store evidence once without an intrinsic direction. Each rejudgement writes its push on the evidence–thesis link. One statement can affect multiple theses differently.
<!-- /generated: tiers -->

## Dependencies: reading the arrows

<!-- generated: dependencies -->
```
B depends on A | What kind of thesis is A? (For an asset thesis B, state which end of A is bullish for B. For a theme thesis B, state whether their ladders have the same or opposite orientation.)
├─ Numeric thesis → Read the specified year's thesis (Example: JPM 2027 net interest income → Fed year-end 2027 rate)
│   ├─ A is open → Read A's state and reasons
│   ├─ A is closed → Read A's closing state and reasons (The frozen outcome is what B needs; keep reading it)
│   └─ A does not exist yet → Wait for it (Record the awaited year on the chain containing the shown thesis. When that year's successor is created, bind the dependency and rejudge B once.)
└─ Event thesis → Follow succession (Example: NVDA FY2027 China revenue → chip export licensing to China)
    ├─ A is open → Read A's state and reasons
    ├─ A is closed with a successor → Read the successor (Record the change. The successor changes B's input, so rejudge B once.)
    └─ A is closed without a successor → Read A's closing state and reasons, marked “historical only”
```

- Theme theses do not judge outcomes as good or bad. Each dependent asset thesis records its direction: rate cuts are bullish for Ethereum and bearish for JPM.
- A dependency has one direction. An apparent “good first, bad later” relationship needs an intermediate thesis: steel tariffs raising domestic steel prices and weakening downstream steel demand are separate paths.
- Dependencies and the theme block are the two ways theses influence each other; succession only orders periods. B depending on A means B reads A's conclusion. The theme block (D191, D195) shows every open, judged theme thesis to every asset thesis's judgement, one to all, and the judgement states which way each theme it weighed pushes it; no edge is written for it. Keep B's direct evidence separate from dependency states and reasons. A's conclusion can affect B like evidence but is not stored as evidence: external events and statements are evidence, whereas A is our own judgement. Treating it as evidence would let the system convince itself.
- Count a statement once. A statement about A is A's evidence, including when two candidates arise from one item. B learns it through A's conclusion. Only statements directly about B are B's evidence. If B does not depend on A, the statement may also directly evidence B. Choose dependencies only when B is created.
- Rejudge an open thesis when its inputs change: new evidence, replacement, a new link to existing evidence, a dependency declaring a changed conclusion, or (for an asset thesis) a theme thesis declaring one. Additional source references alone do not count. Binding an awaited A or moving to its successor also changes B's inputs. Closed theses do not update. A memo-derived thesis is first judged when evidence first links to it; before that, it and its dependants see “not yet judged”.
- The matching model chooses dependencies when opening a thesis, stating which conclusions it relies on and each direction. Choose only among searched theses, extraction block-5 theses and candidates opened from the same item; no extra search. Completed events are evidence, not dependencies: today's oil price influencing OPEC output is evidence for the OPEC-output thesis.
- Before adding an edge or following it to a successor, code checks for cycles. Refuse a cycle and ask the model to correct it; persistent cycles follow normal failure handling. Apparently mutually dependent questions indicate poorly defined theses.
<!-- /generated: dependencies -->

## Succession: the same focus over successive periods

<!-- generated: chain -->
- Successive periods of the same focus form a chain, such as Fed year-end 2026 rate → 2027 rate → 2028 rate. The chain records period order. Dependency traversal follows the rules above.
- One thesis has at most one successor: FY2026 cannot produce two FY2027 successors.
- Keep ladder orientation across succession: a strongly bullish first rung remains strongly bullish, although thresholds can change. Dependencies retain their direction; reversing the ends would break it.
<!-- /generated: chain -->

## Intake: search then compare

<!-- generated: shape -->
|  | Candidate thesis | Evidence |
|---|---|---|
| Comparison set | Top N search results from the entire thesis library | Top N evidence results within its thesis |
| Decision | Existing identity or part, succession, new thesis or skip | Repeat, replace or new evidence |
| Chain | Succession: Fed year-end 2026 rate → 2027 → 2028 | Replacement: AMZN capex guidance 12% growth → 25% |
| What counts as current | Open theses on the chain; numeric theses may have one for this year and one for next year | Evidence not replaced; replacements also form a chain |
| Search scope | Entire thesis library, open and closed | Only evidence within its thesis, not the entire library |
<!-- /generated: shape -->

## One item entering the library

Process one round per item in sequence order. Candidates arrive with associations and necessary group definitions, preserved under the grouping rules. The model performs steps 4 and 7; code performs the others.

<!-- generated: intake -->
```
Evidence and candidates from extraction: one round per item
  ↓ 1 Check sources (Code): Reject sources absent from processing records and record the reason
  ↓ 2 Receive evidence (Code): Retries do not duplicate evidence. A revised input updates only its own source reference. A revised retelling does not alter the original evidence. If the revision is from the original source, compare its statements normally and replace changed statements.
  ↓ 3 Search (Code): Use a search engine such as Elasticsearch; semantic versus keyword search remains open. Search all open and closed theses for each candidate and take top N, initially 10 in Config. Search evidence only within its linked thesis, also top N. Evidence linked to candidates waits for their destinations, even if also linked to existing theses. Empty lists still proceed to matching.
  ↓ 4 Match (Model): The model does not read the original item. Show each existing thesis's subject, question, focus, ladder, due date and open/closed state. In one call: (1) decide candidate identity or a narrower part, succession with unchanged ladder orientation but new thresholds, new thesis for distinct or merely similar questions, or skip overly broad questions, numbers beyond this/next year and the same period of a closed thesis; give reasons; (2) choose dependencies and directions among searched, block-5 and same-item new theses; (3) compare evidence linked only to existing theses. Evidence linked to candidates waits for their destinations, then searches all linked existing theses together and uses one further comparison call. Evidence linked only to new theses is new evidence.
  ↓ 5 Validate (Code): Destination IDs must be in the shown lists or the relevant thesis's evidence. Merge only into open theses. New subjects must resolve within the universe using classification's identifier rules; otherwise skip. Dependencies must reference shown theses or an explicit awaited chain/year and remain acyclic. Return invalid answers for correction.
  ↓ 6 Write to the library (Code): Resolve extraction's group associations to final theses and save them in this step. Each subject has its own writing queue; write theme theses before asset theses. Save new theses with their dependency edges. A repeat adds a source reference and any new thesis link. For replacement, order by when the statement was made: later statements supersede earlier ones. A late-arriving older statement is logged, not inserted. Carry the old evidence's other thesis links to its replacement. An original-source revision that omits a statement without replacing it marks it replaced. If compared data changes before writing, repeat matching only for the affected part.
  ↓ 7 Run a rejudgement round (Model): Rejudge only open theses whose inputs changed: new/replaced/newly linked evidence, or a changed dependency conclusion, newly created awaited thesis or successor. Judge dependencies first, then theme theses before asset theses, and each thesis once per round. Extra source references alone do not trigger it. Memo-derived theses without evidence stay not yet judged. Each judgement declares whether its conclusion changed; changed conclusions propagate to dependants, and a theme's to every open asset thesis (D195). The round's queue is read from the ledger, so a resumed round recovers what an earlier commit queued.
```
<!-- /generated: intake -->

## Step 4: candidate destinations

<!-- generated: outcomes -->
| Destination | When | Writes |
|---|---|---|
| Merge into existing | The candidate concerns the same focus or a part of it, such as H20 China revenue within China revenue. Merge only into open theses; closed theses can only be succeeded. | Compare its evidence within the target thesis and preserve grouping under this section's rules. Use the existing ladder and due date. |
| Succession | The next period of the same focus: the next year for numbers, or continued tracking after an event thesis closed | Create a thesis and record succession |
| New thesis | Distinct or merely similar: Blackwell export licences and H20 export licences are different questions | Create a thesis with its ladder and due date fixed from now on |
| Skip | Too broad or mixed, bundling questions that can move oppositely, such as all US chip controls on China; numbers beyond this/next year; the same focus and period as a closed thesis; or an out-of-universe subject. Proposed themes go to human review; out-of-universe companies receive only a processing-log entry. | Do not create it. Evidence also linked to a specific valid thesis still counts; evidence linked only to the skipped candidate is not stored. |

- The D155 POC uses code for fully determined duplicate identity and model comparison when scope or legacy identity needs judgement. Reference lists guide research without vetoing candidates. Same group does not mean same thesis. See docs/poc/grouping-improvement-plan.md for the contract and measured scope.
- Search finds plausible candidates; the model handles semantic comparison. H20 and Blackwell export licences can look similar but are separate questions. Bullish and bearish accounts of one question share its identity.
- Search includes closed theses, allowing an FY2027 candidate to find closed FY2026 and be classified as succession.
<!-- /generated: outcomes -->

## Step 4: evidence destinations

<!-- generated: evidence-outcomes -->
| Destination | When | Writes |
|---|---|---|
| Repeat | The same evidence already exists under the thesis: a retelling, the same number in text and table, or the same speaker repeating the same statement | Add a source reference, not another evidence item. Existing links do not trigger rejudgement; a new thesis link changes that thesis's inputs and does. |
| Replace | A later account of the same matter: a speaker revises guidance, forecast or event progress; an official confirms/denies a rumour; or the original source revises its statement | Order by statement date. Later statements replace earlier ones, which remain in history; rejudge. A late-arriving older statement is only logged and does not trigger rejudgement. |
| New evidence | Anything else: a new event, another period's figure or another speaker's statement, including disagreement. Uncertainty also means new evidence. | Add it alongside existing evidence and rejudge |

- First resolve the evidence's thesis destination from extraction or candidate matching. Search the top N evidence items still in force within that thesis and ask the model to compare. Unlike candidate-thesis search, evidence search never spans the whole library.
- Store evidence once even when linked to several theses. Compare all those theses' evidence together. If any link is to a candidate, wait for that candidate's destination.
- Carry other thesis links from replaced evidence to the replacement and rejudge open linked theses; otherwise they would retain only an obsolete statement.
- Replacement applies to a statement or number, not the whole report. A revised sell-side revenue forecast replaces that forecast while other arguments remain in force.
- Matching reads the evidence summary, speaker, original source and statement date, not the full original item. When uncertain, treat it as new evidence; both then remain available for judgement.
<!-- /generated: evidence-outcomes -->

## Example: three items

<!-- generated: intake-example -->
```
Three items, starting with an empty library (Illustration)
├─ NVIDIA 8-K, April 15, 2025 → Empty library; two candidates arrive | Empty comparison lists; open both as new theses
│   ├─ #1 Theme thesis → China export licensing for this chip class: event (Evidence: H20 exports to China require a licence (fact))
│   └─ #2 NVDA asset thesis → FY2026 China revenue: numeric (Evidence: expected charges up to approximately $5.5 billion (party statement); depends on #1, with easing bullish)
├─ AMD 8-K, April 16, 2025 → AMD has no existing theses; two candidates arrive | Match
│   ├─ Candidate: MI308 export licensing to China → Merge into #1 (Search finds #1. The model identifies the same question: the same chip class under the same rule. AMD's MI308 statement is new evidence. #1 is rejudged but declares its conclusion unchanged: an additional affected model does not change the key facts or rung. #2 is therefore not rejudged.)
│   └─ Candidate: AMD 2025 China revenue → New thesis #3 (AMD has no open thesis; evidence is expected charges up to approximately $800 million (party statement))
└─ Reuters, April 16, 2025, retelling NVIDIA's 8-K → Existing context: #2 and its dependency #1 | Match
    └─ Evidence links to #1 and #2 → Both are repeats (The original source is the same NVIDIA 8-K and both statements already exist under #1 and #2. Add a source reference to each; neither thesis is rejudged.)
```
<!-- /generated: intake-example -->

## Example: AMZN 2026 capex evidence updates

<!-- generated: evidence-example -->
| Item | Evidence comparison | Library result | Rejudgement |
|---|---|---|---|
| February 5 call: capex guidance up 12% | New evidence; none previously under this thesis | Add g1 | Rejudge |
| February 6 Reuters report retells the guidance | Repeat of g1 | Add a source reference to g1 | No rejudgement |
| March 10 Morgan Stanley forecast: up 18% | New evidence from another speaker | Add m1 | Rejudge |
| April 30 call: guidance revised to 25% growth | Replace g1 | g2 is in force; g1 is replaced | Rejudge, reading “12% → 25%” |
| May 2 Morgan Stanley forecast revised to 27% | Replace m1 | m2 is in force; m1 is replaced | Rejudge |
| Arrives May 20: Morgan Stanley's February forecast | Late older statement; Morgan Stanley already revised it in March (m1) and May (m2) | Do not insert this forecast. Log it as superseded and unused; m2 remains in force. | No rejudgement |
| June 10 meeting reiterates “still around 25%” | Repeat of g2 | Add a source reference to g2, latest June 10 | No rejudgement |

After six months the thesis may have dozens of evidence items. Rejudgement reads those still in force: company guidance of 25% growth (12% in February), Morgan Stanley's 27% forecast (18% in March), plus other speakers and events.
<!-- /generated: evidence-example -->

## Matching labels

Initially a general-purpose model judges step 4. Retain every decision and have people label code-refused cases and periodic random samples: candidate destinations, dependencies and evidence decisions. When sufficient labels exist, train a faster smaller model to take over. Details remain deferred.

<!-- generated: judge -->
```
First version: general-purpose model matching
  ↓ 1 Large-model matching (Model): Start with a general-purpose model using Config's matching settings
  ↓ 2 Record every comparison (Code): Record what the model saw, what it returned and what was ultimately stored
  ↓ 3 Human labelling (Person): Label two sets: code-refused decisions from validation step 5 and periodic random samples. People supply the correct outcome.
  ↓ 4 Train a smaller model (Code): Use human labels to train a faster, smaller model
  ↓ 5 Smaller model takes over (Code): A smaller model eventually handles matching; the handover criterion is not yet decided
```
<!-- /generated: judge -->

### Matching-record fields

<!-- generated: trace -->
| Part | Recorded content |
|---|---|
| Which item | Upstream ID and sequence number |
| Received input | Preserve extraction's candidates, associations, new group definitions and evidence exactly. Separately record the matching-model input. |
| Shown to the model | Ranked top N thesis matches per candidate; top N evidence matches within each thesis; extraction block-5 theses and same-item new theses available for dependency selection |
| Decision maker | Large model, future smaller model or person |
| Request and response | Actual request, raw response and Config version identifying model, prompt and temperature |
| Decision | Each candidate's destination and reason; new-thesis dependencies and directions; evidence repeat/replacement/new decisions; validation results and refusal reasons |
| Stored result | What was finally written to the library |
<!-- /generated: trace -->

## Open or closed

<!-- generated: lifecycle -->
```
A thesis | Open or closed? (This is the only lifecycle switch)
├─ Open → Rejudge when its inputs change, under the rejudgement rule (When matching opens theses, only one for the same focus at a time; numeric quantities may have one each for this year and next year)
└─ Closed → No updates or rejudgement (Retain its closing state: the last rung if judged, otherwise not yet judged. Keep it searchable in the library.)
```

- Pull mode closes it when due. The current rung and reasons become its frozen final conclusion. To keep tracking, create a successor. Pull mode runs at day-end or scheduled intervals; the incoming stream does not manage time. Remaining pull-mode design is deferred.
- People may manually close or reopen a thesis, for example after a delisting. Append a record naming the person and the sequence after which it applies. The matching rule of one open thesis per focus does not restrict manual reopening. People also maintain the research universe.
<!-- /generated: lifecycle -->

## Thesis fields

<!-- generated: fields -->
| Part | Writes | Example |
|---|---|---|
| Subject | The subject in the research universe | NVDA |
| Kind | Asset thesis or theme thesis | Asset thesis |
| Focus | Numeric: which quantity and year; event: which event | FY2027 China revenue |
| Question | One sentence, immutable once written | How will NVDA FY2027 China revenue compare with FY2026? |
| Ladder | Five rungs, or two for yes/no; each is a verifiable outcome, immutable once written | Up at least 50% … down at least 80% |
| Due date | When the debate can be resolved; for numbers, their publication day | FY2027 annual earnings date |
| State | Current rung; append each judgement with reasons and whether the conclusion changed. A memo-derived thesis is not yet judged until evidence first links to it. | Strongly bearish |
| Dependency | Dependency targets and directions; for uncreated targets, the awaited chain and year | → China chip export licensing: easing is bullish |
| Research-group association | Group memberships, stored under this section's grouping rules | China licensing and business for this chip class |
| Succession | Predecessor, if any | Succeeds FY2026 |
| Origin | The item that created it | NVIDIA FY2026 annual earnings release, February 25, 2026 (illustration) |
| Open or closed | One switch: open or closed. Pull mode freezes and closes at expiry; people may close or reopen manually, such as after a delisting. Closed theses do not update. | Open |
<!-- /generated: fields -->

## Evidence fields

<!-- generated: evidence -->
| Part | Writes |
|---|---|
| Quotation | The original sentence or table cell |
| Standalone summary | A sentence understandable without the original: who, what, how much and which period. Matching and rejudgement read it. |
| Source | Upstream ID, category, publication day and location. Retellings, repeated numbers in text/tables and repeated statements add source references to the same evidence item. |
| Speaker | The person or organisation making the statement |
| Original source | For a retelling, identify who originally said it and on which day. Count independent sources and order replacements by that origin. |
| Tier | Fact, party statement, third-party view or rumour |
| Event time | When the event happened or takes effect; for a number, the period it describes |
| Replaced | The replacing evidence, where a speaker revises a statement/number, an official confirms/denies a rumour, or the original source revises/deletes it. Deletion has no replacement evidence. Replaced evidence no longer counts but remains in history. |
<!-- /generated: evidence -->

## Ordering, concurrency and traceability

<!-- generated: order -->
- Only incoming information creates evidence. Theses send notifications, not evidence, so they cannot prove themselves.
- One queue writes each thesis: the theme's queue for theme theses; the company, cryptocurrency or commodity queue for asset theses. Within an item, write themes before assets. Rejudgement order follows dependencies under the round rule. Other queues send requests, such as dependency changes or replacement links, to the owning queue with the item's sequence number.
- Order by sequence, never the computer clock. An item reads only records from earlier sequences plus its own round's writes. The result must match serial processing. If concurrent work changes anything it read, including search lists, before commit, redo the affected work.
- One item's changes form a round. Finish evidence links, thesis creation, succession and dependencies, then rejudge in dependency order. Dependants read conclusions freshly judged in that round. Judge each thesis once. A widely depended-on thesis such as the Fed rate triggers each dependant once only if it declares its conclusion changed; otherwise propagation stops.
- Append-only records: questions, ladders and due dates are immutable. Matching, rejudgement, succession, closure, reopening and labels append records with sequence numbers.
- The timeline only appends, never rewrites past knowledge. A late statement already superseded by a newer one is logged as superseded and unused, not added to the thesis. Previously unknown information counts normally with its true date. The evidence-matching model distinguishes these cases; add no separate rule.
- A revised input changes only its own source reference. Revising a retelling does not change original evidence. For an original-source revision, changed statements are replaced and deleted statements marked replaced. Rejudge each open thesis linked to affected statements once. A retelling-reference change alone does not trigger rejudgement. Keep old judgement records unchanged.
- On failure, record the item's completed step and retry from the failed step, replacing only that attempt's own result. Repeated failures go to human review.
- Trace both directions: a thesis to all information that affected it; an item to theses it created and all evidence it sourced, including repeats.

Choose storage location and database during implementation.
<!-- /generated: order -->

## Module contracts

| Module | Exchange |
|---|---|
| Extraction | Receive sourced evidence, candidates, associations and necessary group definitions. Supply open subject theses and their dependencies: question, focus, due date and links, without states/evidence, plus available groups under this contract. |
| Config | Read matching/rejudgement settings and search count; record the version with every call. |
| Pull mode | Receive day-end/scheduled updates and due-date freezing/closure; remaining design is deferred. |
| Final verdict | Whether it remains separate is deferred; due-date freezing is decided. |
| Human review pool | Send proposed out-of-universe themes and repeated failures. Resolvable out-of-universe assets receive only processing-log entries. |
| Matching labels | Supply every comparison record; receive human labels and, later, a smaller model. |

## Acceptance

- Preserve extraction's associations against final thesis IDs and trace real evidence links under the [grouping contract](#research-groups-associate-during-extraction). Default integration is pending; isolated code checks do not satisfy this acceptance.
- Every thesis has an immutable question, ladder and due date; five rungs or two for yes/no, with exhaustive, non-overlapping, verifiable outcomes.
- Numeric theses name the year and open at most one per subject/quantity for this year and next year; a previous year can remain open until due. Events have one open thesis per event. These are matching-time rules, excluding manual reopening.
- Candidate search covers all open and closed theses, taking top N before comparison. Evidence search stays within its thesis.
- Every comparison records shown input, raw response, Config version and decision maker. Reject destinations outside the shown lists or relevant evidence, and dependencies not shown or explicitly awaiting a chain/year, including cycles.
- Classify every evidence comparison as repeat, replace or new. A repeat adds a reference without rejudging existing links; a new link to an open thesis triggers its rejudgement. Replaced evidence stays in history.
- Store evidence once across multiple thesis links. Carry other links to replacement evidence.
- Rejudge only open theses with changed inputs: new, replaced or newly linked evidence, or changed dependency conclusions. Memo-derived theses without evidence remain unjudged. Cite evidence and relevant dependency IDs, and declare conclusion change. First judgement and rung changes must declare a change. Only facts can establish which rung holds.
- Choose dependencies during matching from shown theses or explicitly awaited chain/years. Numeric dependencies read the specified year; event dependencies follow succession. No cycles.
- Judge dependencies before dependants and each thesis once per item round.
- Append records without rewriting them. Trace all theses, evidence, links and matching records to their origins, and source items to created theses and sourced evidence.
- Append knowledge in arrival order. Log obsolete late statements without adding them; accept newly learned matters with their true dates. A revised retelling changes only its own source reference. Original-source revisions replace changed statements and mark deleted ones replaced.
- Retain every comparison; send code-refused and random samples for human labelling.

## Open questions

<!-- generated: open -->
- Search method and ranking remain open: semantic, keyword or both. Test on stored information during implementation. Start with top 10 and adjust during experiments.
- Labelling details remain open: who, how many, which interface, model evaluation and training, handover to a smaller model, and checks for omitted or mislinked extraction evidence.
- Design pull mode later: day-end/scheduled execution, overall review, and whether final verdict remains a separate step.
<!-- /generated: open -->

## Proposals awaiting Alex's decision

Other proposals were resolved individually. The due-date proposal became state freezing. These two remain for pull-mode design and must be decided before implementation.

<!-- generated: proposed -->
1. Proposal for later pull-mode design: besides due-date freezing, distinguish an unavailable answer (quantity no longer disclosed or event ceases to exist; dependants lack that input) and pending publication (period ended but the number is not yet released).
2. Proposal for later pull-mode design: daily pairwise duplicate checks among open theses of a subject; merge the later thesis into the earlier, move links and dependencies, check cycles and rejudge. Add separate duplicate-check settings to Config.
<!-- /generated: proposed -->

## Related decisions

- D11/D16/D26: subject ownership, human review, central library and sources. D30: count independent original sources.
- D31: sequence ordering and one writing queue per thesis; later decisions revise relationships, late inputs and universe removal.
- D33: read-only extraction; library matching/writing.
- D38–D40: question/ladder/due-date structure, state, evidence links/tiers, dependencies/succession, round-based intake, history and matching labels.
- D41/D42: align frozen modules with the rebuilt library, show dependencies during extraction, separate evidence/candidates, compare within-thesis evidence, and permit binary ladders.
- D44: initial model-owned identity and step-4 matching. D45: distinguish recorded decisions from proposals; similar questions remain separate. D155 later bounds code-owned identity in the POC.
- D46/D49: one state, concrete ladders, ordinary ingestion of decisive evidence, years based on publication day, top-N whole-library search.
- D47: consistent terms, evidence comparison after candidate resolution, dependency references in judgement reasons and Reuters example correction.
- D48: library and matching-label freeze, October 20, 2026.
- D51: rejudge on changed inputs, explicit conclusion-change declaration, dependency selection within matching, seven intake steps and no consensus calculation.
- D52/D53: plain consistent wording and full context review without new rules.
- D54: freeze the current state when due; no separate result or extra wait; pull mode owns time.
- D55–D57: manual universe maintenance and a single open/closed switch; only open theses update; manual closure/reopening allowed.
- D58: clarify dependency direction, waiting, due-date scope, matching-time uniqueness, triggers and manual-operation records; freeze all except final verdict/pull mode.
- D59/D60: subject identification and personal memos; no judgement until first evidence; clarify wording and diagram without new rules.
- D149: this module owns group handoff/storage; matching does not regroup extraction's associations.

<a id="研究主线抽取时归组"></a>

## Research groups: associate during extraction

<!-- generated: relations -->
- D149 requirement: organise theses by the continuing business process they discuss, called a research group. Vera Rubin readiness and customer deployment can share a group while shipment dates, SK factory launch and OpenAI deployment retain separate questions, ladders and due dates. A group may start with one thesis; a thesis may belong to several groups. A group has no state or ladder, creates no automatic dependency and is not an overarching investment thesis for an agent.
- Associate by business process, across companies and industries, not merely by company. A customer deployment explicitly using Rubin can join Rubin; NVIDIA PC chips cannot join just because they share a company. OpenAI deployment cannot join an SK-specific group merely because both involve Rubin. A group does not replace a research-universe theme.
- Before the full-text call, code supplies available group IDs, names and scopes. Search is not restricted by company. During that call, extraction references shown groups or declares new named and scoped groups. A candidate that tracks an ongoing matter (a product rollout and its deployments, a deal, a policy process, an investment or demand cycle) cites one or more groups, each shown or declared, without repeats; a company's own reported or guided financial lines (total or segment revenue, margins, expenses, tax rate, capex) belong to the company and cite none unless the line itself tracks such a matter (D165). Code validates the references before writing, and creates a declared group only when a written thesis that tracks a matter cites it, so a company's lines alone never found a group. Declare a new group if none fits; do not force an approximate fit.
- Matching still decides thesis/evidence identity and dependencies; it does not reread association fields to regroup. After creation, succession or merging, the writer resolves candidate IDs to final thesis IDs and local group IDs to stored group IDs, then stores membership. Candidates failing source checks or ultimately skipped do not become members. Do not create empty groups for unused declarations or reject other valid memberships because of them.
- Store each group/member pair once, with input ID and sequence number under the library's ordering and historical-read rules. Commit groups and memberships atomically with theses and evidence; roll all back on failure. Never mark a partial write complete. Redelivery must not duplicate membership; use existing dispatch and recovery.
- Groups do not copy evidence. Read sources through members' real evidence links, filtered by the requested sequence and excluding evidence already replaced at that point. No link means no evidence. A new member or an existing thesis change flag updates its groups. A repeated quote only adds a source and does not trigger an update. Evidence-only articles update existing memberships without inventing theses or groups.
- Acceptance measures source-supported membership and evidence retention, not identical names, IDs or group counts on every run. Report omissions, check refusals, missed associations and wrong associations separately. Preserve Rubin shipment/customer-deployment relationships and check wrong links to unrelated products or customer-specific groups. Multi-company and large-library behaviour is not yet validated.
- Implementation reference remains an isolated experiment: D147 supplies existing_subjects; threads declares id, name and scope; candidates[].thread_ids holds references. Local IDs are t plus a positive integer; stored IDs are g plus a positive integer. Prototype search uses title/full-text words against a global name/scope index, taking N from existing Config. These are prototype fields and search choices, not default-pipeline capabilities or evidence of large-library recall.
- See docs/poc/grouping-improvement-plan.md for gaps and steps. D148 member context and D150 reason-first output did not solve wrong grouping. D152's four name-selection responses to the third article created no candidates, so new membership was unexercised. Preserve all prior responses and results. Overarching thesis generation, MCP presentation and historical backfill are outside that implementation scope.
<!-- /generated: relations -->

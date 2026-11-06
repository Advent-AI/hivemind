# Thesis library

> **2026-11-05 decision: incomplete research is still research.** Alex: “down the road, we can always have agents do research individually to get the actual dates and information that didn't go in while this time it was going in the thesis DB … alleviate these options as conditional. Don't hardgate it based on the manual code”. A worthwhile new thesis and its evidence enter the library even when its date, check material, period or ladder is unknown. Record what the source supports and leave the rest unknown; a later research agent may fill it. Missing fields are not an admission rejection. An estimated date is an estimate, not an exact source fact; reaching it alone does not close a still-unresolved question. A ladder-based judgement can only be made when a usable ladder exists; a thesis without one stays available for evidence and later research. The older date/ladder-as-mandatory clauses below describe the previous implementation and apply only where those fields exist; they do not override this decision. The frozen extraction ruler and historical scores are unchanged.

> In the split-extraction POC, a new research subject does not have to be pre-listed to be recorded. The model judges its significance and existing-question matching judges whether it is already tracked; code supplies a stable local identity, not a list of what matters.

> **2026-11-05 split POC matching repair:** A candidate without a typed measure still receives the existing analyst review when Jev proposes merging it into an open question. Review every proposed same-question or component match against the latest question snapshot. A candidate is merged only when that existing question already covers what it asks; an existing narrow question does not by itself cover a broader candidate. Related questions may stay separate when their answers can move apart and an analyst would track them separately (D248/D258). A different period without enough typed identity to establish a successor stays a new question; missing details never block admission. The experiment uses `collision-v3`; the product replay default below has not been changed. See [matching repair and evidence](../research/2026-11-05-matching-identity-design.md).

> Status: foundation frozen, October 20, 2026. D149 adds extraction-owned grouping; D165 puts it in the default pipeline. D169: the matching step runs on Jev, with the collision judge for a candidate whose list holds a thesis of its own subject and measure (D190, D258); the replay default is `poc-v116` (D366). D168 states the Replace row's full definition and the succession answer it needs. Corrected to D63, D198, D202, D204, D169, D190, D191, D207, D251, D259, D260, D264 on 2026-11-05 (D367); the builds D368 decided are marked where they apply. English edition: October 25, 2026 (D163). Only recorded decisions apply; open questions and one proposal remain separate.
> Design page: `docs/system-design.html` → New → Thesis library → Details. This PRD also owns Matching labels. Recorded decisions take precedence. Historical discussion: `docs/views-rebuild-log.md`.

## Purpose

A thesis records an investment question and its evidence. A date, ladder and other research details are conditional on the information available; missing details can be researched later. Evidence moves its state when it can be judged. Search then compare candidates with existing theses to merge, continue, create or skip; compare evidence within its thesis to repeat, replace or add. Extra source references alone do not trigger rejudgement. Extraction determines group associations; the writer preserves them after resolving final thesis IDs under the [grouping contract](#research-groups-associate-during-extraction).

## Rationale

- Clear structures connect theses, ladders and evidence to source items.
- A thesis is a question with a state, not an assertion. Opposing views move the same state's direction rather than creating opposite duplicate theses.
- A fixed, verifiable ladder states in advance what would disprove the view, analogous to explicit analyst scenarios or predefined investment exit conditions. Do not change it after observing the outcome.
- The model judges from the evidence in view (the arrivals since its fifth most recent judgement and the basis its last ten judgements cited; the rest stays in force, D198) and dependency conclusions, at low temperature, rather than adjusting its previous score. A revision follows statement date, so a late older statement is stored as one more piece and never recorded as revising a newer one (D202).
- A theme's outcome can help one asset and harm another. Theme ladders describe outcomes; asset dependencies specify their own direction.
- A thesis contains one period and one due date, generally 6–12 months; intermediate quarterly reports are evidence. A thesis on a binding obligation a universe company takes on (a guarantee, financing, an equity stake, a purchase commitment) may set its own check day up to 18 months after the item, because the signing can be checked long before what it finances is built (D185).
- Search finds plausible matches and the model compares their meaning. A match inherits the existing ladder and due date; a merely similar question is new. D155's current POC additionally gives code ownership of fully determined duplicate identity, with its limits in the improvement plan.
- Evidence needs the same search-then-compare discipline. Otherwise February's 12% capex guidance and April's 25% revision sit side by side unrelated, forcing every judgement to rediscover which is current; the comparison records the revision, and both stay in force (D202).
- Record each repeat and revision once, as a relation between two stored pieces that both stay in force (D202, D204). The judge reads the relation, so a retelling counts as one claim and moves nothing (D260).
- Use two rungs for yes/no instead of forcing five.
- The model chooses dependencies like an analyst; code rejects cycles. Apparently mutual dependencies indicate poorly defined questions.
- Rejudge when inputs change. A changed conclusion includes a new rung or materially changed supporting facts/numbers. A repeated Fed statement should not trigger hundreds of dependants; AMZN capex moving from 12% to 25% can trigger NVDA even within the same rung.
- Match with Jev, and with the collision judge where a candidate meets a thesis of its own subject and measure (D169, D190); retain records, obtain human labels and later train a faster smaller model.

## Structure

<!-- generated: structure -->
```
Thesis library
├─ Subject → Companies, cryptocurrencies, commodities and themes in the universe
│   └─ Thesis → A question + a ladder + a due date (Immutable once written. Five rungs, or two for yes/no. When matching opens a thesis, only one may be open for the same subject and focus at a time.)
│       ├─ State → The thesis's current ladder rung (Evidence pushes towards either end; the model forecasts the rung most likely at the due date, against a reference (D260). A thesis from the user's memo is not yet judged until evidence first links to it.)
│       ├─ Link → Evidence (Store evidence once with sources and tier. Its push belongs to the link. Nothing is retired: a revised piece stays in force beside its revision, the pair recorded (D202).)
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

1. A ladder has five rungs. Asset theses run from strongly bullish to strongly bearish, describing business impact; theme theses name five ordered outcomes without good/bad labels. Use two rungs for yes/no rather than forcing five: bullish/bearish for assets; named outcomes for themes, such as signed by the deadline/not signed. Decided for the next extraction version (D186, D368): asset rungs state the business outcome against guidance (above, near, below) and each thesis names its favourable end.
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
| State | Our judgement of the thesis's current rung; evidence pushes toward either end | The model judges at low temperature: the outcome the evidence in force makes most likely at the due date, against a reference (below). It reads the evidence in view, the arrivals since its fifth most recent judgement and the basis its last ten judgements cited, the request naming how many more pieces stay in force (D198); a revision is shown beside the piece it revises and a repeat beside the piece the matcher read it as, both in force (D202, D204); plus current dependency states and reasons and, for an asset thesis, the theme block. Do not increment or decrement the previous score. Cite evidence and compare with the conclusion before this round to state whether it changed. Do not rejudge if only source references were added and dependency conclusions did not change. | After the 8-K: strongly bearish |

- Every judgement states its basis in a fixed response shape: evidence IDs such as e12 and e15, plus dependency thesis IDs such as #1 when their changes triggered rejudgement.
- Code checks cited IDs against the request that was sent: evidence must be among the pieces shown to this thesis (D198); cited theses must be its dependencies. Accept only if all checks pass. Otherwise record the reason and ask for one corrected judgement. If that also fails, use normal failure handling: retry from this step, then human review after repeated failure. This checks references, not whether the judgement is correct, like verifying a cited page exists.
- Each judgement also declares whether the conclusion changed and explains why, comparing with the state and reasons before this round, including during retries. That earlier conclusion is for comparison, not incremental scoring. A rung change or a material change in the supporting facts/numbers counts: AMZN capex guidance moving from 12% to 25% growth changes the conclusion even within one rung. Repetition does not. A changed conclusion triggers dependent theses in the same round. Code requires changed=true for a first judgement or rung change; otherwise refuse under the same correction rules.
- For historical judgement, read the records saved on that date. Do not ask the model again; a new sample can differ.
- The rung is a forecast against a reference (D260): the outcome the evidence in force makes most likely at the due date, judged against what the market expects (consensus, guidance, the stated plan or deadline). The judgement names the reference and its rung and the outcome the evidence implies (a figure or date derived from reported figures, guidance and quantified revisions), and moves when the implied outcome crosses a rung boundary. A consensus figure alone keeps the judgement at the reference's rung and is not the reason to stay once other evidence has arrived; "not established" is confidence, not a reason to stay. From judging-v6 the reference and the implied outcome are required fields of the answer, stored beside the rung; an empty one is refused.
<!-- /generated: positions -->

## Four evidence tiers

<!-- generated: tiers -->
| Tier | Example | Role |
|---|---|---|
| Fact | Official actions, published figures and completed transactions | Fixes what is known; the forecast starts from it |
| Party statement | Company guidance, management statements and official speeches | The strongest input to the forecast |
| Third-party view | Sell-side analysts, media analysis and experts | Moves the forecast in proportion to its specificity |
| Rumour | Unnamed-source claims and unattributed statements | Moves the forecast in proportion to its specificity |

- The model determines the size of the push and gives reasons, by tier and novelty: a repeat, another outlet or an opinion with no new fact or calculation moves nothing (D260). No tier has a fixed score.
- Count independent original sources. Twenty outlets retelling one exclusive are twenty pieces, each related to the one it repeats (D204), and one source, not twenty independent confirmations (D30).
- Tier follows who confirmed it. An unnamed-source report that Commerce is issuing licences is a rumour. An official or company confirmation is factual evidence recorded as a revision of it, both in force (D202). The rumour stays a rumour.
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
- Count a statement once. A statement about A is A's evidence, including when two candidates arise from one item. B learns it through A's conclusion. Daily filing gives a statement one home: the narrowest open thesis it bears on, as that thesis's own figure, step or estimate or through the demand, supply, competition or pricing behind its answer, plus the same answer's candidates (D207, D259, D264, D265); a coverage-start record is one record linked to every thesis that read it (D364). Dependencies are chosen only when B is created; a later item adding a dependency to an existing thesis is decided (D191 point 2) and to be built (D368).
- Rejudge an open thesis when its inputs change: new evidence, replacement, a new link to existing evidence, a dependency declaring a changed conclusion, or (for an asset thesis) a theme thesis declaring one. Additional source references alone do not count. Binding an awaited A or moving to its successor also changes B's inputs. Closed theses do not update. A memo-derived thesis is first judged when evidence first links to it; before that, it and its dependants see “not yet judged”.
- The matching call chooses a new thesis's dependencies, stating which conclusions it relies on and each direction (D51). Choose only among searched theses, extraction block-5 theses and candidates opened from the same item; no extra search. Jev, the default matcher, is not asked for them, so on the default configuration only seed theses carry dependencies (D253); building the choice on the Jev path is decided (D368). A seed's dependency arrow means "supports" (D368, by D208): for filing, the supporting (driver) thesis is the narrower one; for judging, the supported (root) thesis reads the supporting theses' conclusions, so drivers and themes are judged before their roots. The judging code reads the stored edge the other way today; the fix is to be built and measured (D368). Completed events are evidence, not dependencies: today's oil price influencing OPEC output is evidence for the OPEC-output thesis.
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
| Chain | Succession: Fed year-end 2026 rate → 2027 → 2028 | Revision: AMZN capex guidance 12% growth → 25%, both in force |
| What counts as current | Open theses on the chain; numeric theses may have one for this year and one for next year | Every stored piece stays in force; revisions form a chain the judge reads (D202) |
| Search scope | Entire thesis library, open and closed | Only evidence within its thesis, not the entire library |
<!-- /generated: shape -->

## One item entering the library

Process items one at a time in sequence order through steps 1–6; step 7, the rejudgement round, runs once a day after the day's last item (D63). Candidates arrive with associations and necessary group definitions, preserved under the grouping rules. Models perform steps 4 (Jev and the collision judge) and 7; code performs the others.

<!-- generated: intake -->
```
Evidence and candidates from extraction, written item by item; one judging round a day (D63)
  ↓ 1 Check sources (Code): Reject sources absent from processing records and record the reason
  ↓ 2 Receive evidence (Code): Retries do not duplicate evidence. A revised input updates only its own source reference. A revised retelling does not alter the original evidence. If the revision is from the original source, compare its statements normally: a changed statement is stored as a revision of the old one, both in force (D202).
  ↓ 3 Search (Code): Use a search engine such as Elasticsearch; semantic versus keyword search remains open. Search all open and closed theses for each candidate and take top N, initially 10 in Config. Search evidence only within its linked thesis, also top N. Evidence linked to candidates waits for their destinations, even if also linked to existing theses. Empty lists still proceed to matching.
  ↓ 4 Match (Model): The matcher does not read the original item. Jev answers, with a score, each candidate's relation to every thesis on its list (shown with its subject, question, focus, ladder, due date and open/closed state) and each piece of evidence's relation to every stored piece on its list under each linked thesis; code turns the answers into the destinations below and owns identity on typed keys (D155, D169, D197). When a candidate's list holds a thesis of its own subject and measure, the collision judge, one generative call, answers the analyst's question for those theses under D248's test, and its verdict replaces Jev's (D190, D258). Jev is not asked for dependencies. Evidence linked to candidates waits for their destinations, then searches all linked existing theses together and is compared once more. Evidence linked only to new theses is new evidence.
  ↓ 5 Validate (Code): Destination IDs must be in the shown lists or the relevant thesis's evidence. Merge only into open theses. New subjects must resolve within the universe using classification's identifier rules; otherwise skip. Dependencies must reference shown theses or an explicit awaited chain/year and remain acyclic. Return invalid answers for correction.
  ↓ 6 Write to the library (Code): Resolve extraction's group associations to final theses and save them in this step. Each subject has its own writing queue; write theme theses before asset theses. Save new theses with their dependency edges. Store every incoming piece once, as its own record with all its links (D204): a repeat also records the pair as the same claim; a replacement is linked wherever the piece it revises is linked and the pair is recorded as a revision, ordered by when each statement was made, both in force (D202); an older statement arriving later is stored and linked as one more piece, with no revision recorded. The writer retires nothing. If compared data changes before writing, repeat matching only for the affected part.
  ↓ 7 Run the day's rejudgement round (Model): Once a day, after the day's last item (D63), rejudge only open theses whose inputs changed that day: new or newly linked evidence (a repeat or a revision is a new piece), or a changed dependency conclusion, newly created awaited thesis or successor. Judge dependencies first, then theme theses before asset theses, and each thesis once per round; each judgement reads the evidence in view (D198). Extra source references alone do not trigger it. Memo-derived theses without evidence stay not yet judged. Each judgement declares whether its conclusion changed; changed conclusions propagate to dependants, and a theme's to every open asset thesis (D195). The round's queue is read from the ledger, so a resumed round recovers what an earlier commit queued.
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

- The D155 POC uses code for fully determined duplicate identity and model comparison when scope or legacy identity needs judgement. A shared quantity (an aggregate opened under its admission reason) is one thesis per theme, measure and period: its population or wording is not identity, so code merges another wording into the open one and succeeds it for the next period (D197). Reference lists guide research without vetoing candidates. Same group does not mean same thesis. See docs/poc/grouping-improvement-plan.md for the contract and measured scope.
- Search finds plausible candidates; the model handles semantic comparison. H20 and Blackwell export licences can look similar but are separate questions. Bullish and bearish accounts of one question share its identity.
- Search includes closed theses, allowing an FY2027 candidate to find closed FY2026 and be classified as succession.
<!-- /generated: outcomes -->

## Step 4: evidence destinations

<!-- generated: evidence-outcomes -->
| Destination | When | Writes |
|---|---|---|
| Repeat | The same evidence already exists under the thesis from another input: a retelling, or the same speaker repeating the same statement (within one input, the same number in text and table is one piece with several quotes) | Store it as its own piece with its own source and links, and record the pair as the same claim (D204). The judge sees the pair labelled as the matcher's opinion and counts one claim; its links queue their theses for the day's round. |
| Replace | A later account of the same matter: a speaker revises guidance, forecast or event progress; an official confirms/denies a rumour; or the original source revises its statement | Store the later statement beside the earlier one and record the pair as a revision, ordered by statement date; both stay in force (D202); rejudge. A late-arriving older statement is stored and linked as one more piece, with no revision recorded. |
| New evidence | Anything else: a new event, another period's figure or another speaker's statement, including disagreement. Uncertainty also means new evidence. | Add it alongside existing evidence and rejudge |

- First resolve the evidence's thesis destination from extraction or candidate matching. Search the top N evidence items still in force within that thesis and ask the model to compare. Unlike candidate-thesis search, evidence search never spans the whole library.
- Store evidence once even when linked to several theses. Compare all those theses' evidence together. If any link is to a candidate, wait for that candidate's destination.
- A revision is linked wherever the piece it revises is linked, and those open theses are rejudged, so each sees the change (D202).
- Replacement applies to a statement or number, not the whole report. A revised sell-side revenue forecast is recorded as a revision of that forecast; both stay in force, as do the report's other arguments.
- Matching reads the evidence summary, speaker, original source and statement date, not the full original item. When uncertain, treat it as new evidence; both then remain available for judgement.
<!-- /generated: evidence-outcomes -->

## Example: three items

<!-- generated: intake-example -->
```
Three items, starting with an empty library (Illustration)
├─ NVIDIA 8-K, April 15, 2025 → Empty library; two candidates arrive | Empty comparison lists; open both as new theses
│   ├─ #1 Theme thesis → China export licensing for this chip class: event (Evidence: H20 exports to China require a licence (fact))
│   └─ #2 NVDA asset thesis → FY2026 China revenue: numeric (Evidence: expected charges up to approximately $5.5 billion (party statement); the licence theme #1 reaches it through the theme block (an explicit dependency, easing bullish, would be chosen in matching, D51, not yet on the default Jev path))
├─ AMD 8-K, April 16, 2025 → AMD has no existing theses; two candidates arrive | Match
│   ├─ Candidate: MI308 export licensing to China → Merge into #1 (Search finds #1. The model identifies the same question: the same chip class under the same rule. AMD's MI308 statement is new evidence. #1 is rejudged in that day's round but declares its conclusion unchanged: an additional affected model does not change the key facts or rung. #1 therefore queues no rejudgement of #2.)
│   └─ Candidate: AMD 2025 China revenue → New thesis #3 (AMD has no open thesis; evidence is expected charges up to approximately $800 million (party statement))
└─ Reuters, April 16, 2025, retelling NVIDIA's 8-K → Existing context: #2 and the licence theme #1 | Match
    └─ Evidence links to #1 and #2 → Both are repeats (The original source is the same NVIDIA 8-K and both statements already exist under #1 and #2. Each retelling is stored as its own piece under its thesis, with the pair recorded as the same claim (D204). Both theses are rejudged in that day's round, #2 for this piece alone; the judge counts one claim, so neither conclusion changes.)
```
<!-- /generated: intake-example -->

## Example: AMZN 2026 capex evidence updates

<!-- generated: evidence-example -->
| Item | Evidence comparison | Library result | Rejudgement |
|---|---|---|---|
| February 5 call: capex guidance up 12% | New evidence; none previously under this thesis | Add g1 | Rejudge |
| February 6 Reuters report retells the guidance | Repeat of g1 | Add r1, recorded as the same claim as g1 | Rejudge; one claim, conclusion unchanged |
| March 10 Morgan Stanley forecast: up 18% | New evidence from another speaker | Add m1 | Rejudge |
| April 30 call: guidance revised to 25% growth | Replace g1 | Add g2 beside g1, both in force; the revision g1 → g2 is recorded | Rejudge, reading “12% → 25%” |
| May 2 Morgan Stanley forecast revised to 27% | Replace m1 | Add m2 beside m1, both in force; the revision m1 → m2 is recorded | Rejudge |
| Arrives May 20: Morgan Stanley's February forecast | Late older statement; Morgan Stanley already revised it in March (m1) and May (m2) | Add m0 as one more piece with its February date; no revision is recorded and the late-statement log keeps a row | Rejudge; m2 is still the latest forecast, so the conclusion stays |
| June 10 meeting reiterates “still around 25%” | Repeat of g2 | Add j1, recorded as the same claim as g2 | Rejudge; one claim, conclusion unchanged |

After six months the thesis may have dozens of evidence items, all in force. A rejudgement reads those in view, the arrivals since its fifth most recent judgement and the basis its last ten judgements cited (D198), each revision beside the piece it revises: company guidance of 25% growth revising February's 12%, Morgan Stanley's 27% forecast revising March's 18%, plus other speakers and events.
<!-- /generated: evidence-example -->

## Matching labels

Jev judges step 4, and the collision judge, a generative model, answers for a candidate whose list holds a thesis of its own subject and measure (D169, D190, D258). Retain every decision and have people label code-refused cases and periodic random samples: candidate destinations, dependencies and evidence decisions. When sufficient labels exist, train a faster smaller model to take over. Details remain deferred.

<!-- generated: judge -->
```
Matching: Jev with the collision judge (D169, D190)
  ↓ 1 Jev and the collision judge (Model): Jev answers under Config's matching setting (D169); for a candidate whose list holds a thesis of its own subject and measure, the collision judge, a generative model under Config's collision setting, answers for those theses and its verdict replaces Jev's (D190, D258)
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
| Decision maker | Jev or the collision judge, a future smaller model, or a person |
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

- Pull mode closes it when due. The current rung and reasons become its frozen final conclusion. To keep tracking, create a successor. Pull mode runs at the end of each day; the incoming stream does not manage time (D356).
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
| Source | Upstream ID, category, publication day and location. A number repeated in text and tables within one item adds references to the same piece; a retelling or repeated statement in another item is its own piece, with the pair recorded as the same claim (D204). |
| Speaker | The person or organisation making the statement |
| Original source | For a retelling, identify who originally said it and on which day. Count independent sources and order revisions by that origin. |
| Tier | Fact, party statement, third-party view or rumour |
| Event time | When the event happened or takes effect; for a number, the period it describes |
| Revises | The earlier piece this one revises, where a speaker revises a statement/number, an official confirms/denies a rumour, or the original source revises it. The pair is recorded and both stay in force; the writer retires nothing (D202). |
<!-- /generated: evidence -->

## Ordering, concurrency and traceability

<!-- generated: order -->
- Only incoming information creates evidence. Theses send notifications, not evidence, so they cannot prove themselves.
- One queue writes each thesis: the theme's queue for theme theses; the company, cryptocurrency or commodity queue for asset theses. Within an item, write themes before assets. Rejudgement order follows dependencies under the round rule. Other queues send requests, such as dependency changes or replacement links, to the owning queue with the item's sequence number.
- Order by sequence, never the computer clock. Before each item, extraction reads the latest committed questions from earlier sequences, including earlier same-day writes (D375 on main). The two experimental split calls share that snapshot. Processing must be equivalent to sequence order: if an earlier item changes the snapshot, including by opening a question, redo any later work that used the stale snapshot.
- A day's items form one round: each item's evidence links, thesis creation, succession and dependencies are written in sequence order, and after the day's last item the round rejudges in dependency order (D63). Dependants read conclusions freshly judged in that round. Judge each thesis once. A widely depended-on thesis such as the Fed rate triggers each dependant once only if it declares its conclusion changed; otherwise propagation stops.
- Append-only records: questions, ladders and due dates are immutable. Matching, rejudgement, succession, closure, reopening and labels append records with sequence numbers.
- The timeline only appends, never rewrites past knowledge. A statement older than one already stored on the same matter is stored and linked as one more piece with its true date, and no revision is recorded (D202); previously unknown information counts normally with its true date.
- A revised input changes only its own source reference. Revising a retelling does not change original evidence. For an original-source revision, a changed statement is stored as a revision of the old one, both in force; nothing is retired (D202). Rejudge each open thesis linked to affected statements once. A retelling-reference change alone does not trigger rejudgement. Keep old judgement records unchanged.
- On failure, record the item's completed step and retry from the failed step, replacing only that attempt's own result. Repeated failures go to human review.
- Trace both directions: a thesis to all information that affected it; an item to theses it created and all evidence it sourced, including repeats.

Choose storage location and database during implementation.
<!-- /generated: order -->

## Module contracts

| Module | Exchange |
|---|---|
| Extraction | Receive sourced evidence and candidates. Before each item, supply the item's subjects' open questions and all open theme questions with takes lines, as committed before the item; both experimental split calls share that snapshot (D375 on main). No states, evidence, dependency links or list of stored groups. |
| Config | Read matching, collision-judge and rejudgement settings and search count; record the version with every call. |
| Coverage-start reading | Receive, once at coverage start, each open question's starting figure from the company's latest earnings report as evidence linked to every question that read it (D363, D364; the one-home rule of the daily stream does not apply to these records); the records are written without matching, each linked to the questions whose reading kept it; the first day's round judges those questions. Seed questions and these records are shown from the ledger's first day. |
| Pull mode | At the end of each day, close the questions that are due at the rung they stand on, with a closing record (D54, D356). |
| Human review pool | Send proposed out-of-universe themes and repeated failures. Resolvable out-of-universe assets receive only processing-log entries. |
| Matching labels | Supply every comparison record; receive human labels and, later, a smaller model. |

## Acceptance

- Preserve extraction's associations against final thesis IDs and trace real evidence links under the [grouping contract](#research-groups-associate-during-extraction). D165 integrates the default handoff; isolated code checks do not establish semantic acceptance.
- Every thesis has an immutable question, ladder and due date; five rungs or two for yes/no, with exhaustive, non-overlapping, verifiable outcomes.
- Numeric theses name the year and open at most one per subject/quantity for this year and next year; a previous year can remain open until due. Events have one open thesis per event. These are matching-time rules, excluding manual reopening.
- Candidate search covers all open and closed theses, taking top N before comparison. Evidence search stays within its thesis.
- Every comparison records shown input, raw response, Config version and decision maker. Reject destinations outside the shown lists or relevant evidence, and dependencies not shown or explicitly awaiting a chain/year, including cycles.
- Classify every evidence comparison as repeat, replace or new. A repeat is stored as its own piece with the pair recorded as the same claim (D204); a replace is stored beside the old piece as a revision, both in force (D202); every new link to an open thesis queues it for the day's round.
- Store evidence once across multiple thesis links. Carry the revised piece's other links to its revision.
- Rejudge only open theses with changed inputs: new or newly linked evidence (repeats and revisions are new pieces), or changed dependency conclusions. Memo-derived theses without evidence remain unjudged. Cite evidence and relevant dependency IDs, and declare conclusion change. First judgement and rung changes must declare a change. The rung is a forecast of the most likely outcome at the due date, against a reference (D260).
- Choose dependencies during matching from shown theses or explicitly awaited chain/years (D51; decided, not built on the default Jev path, which asks for none). Numeric dependencies read the specified year; event dependencies follow succession. No cycles.
- Judge dependencies before dependants and each thesis once per day's round (D63).
- Append records without rewriting them. Trace all theses, evidence, links and matching records to their origins, and source items to created theses and sourced evidence.
- Append knowledge in arrival order. Store a late older statement as one more piece with its true date and no revision (D202); accept newly learned matters with their true dates. A revised retelling changes only its own source reference. An original-source revision's changed statements are stored as revisions, both in force; nothing is retired (D202).
- Retain every comparison; send code-refused and random samples for human labelling.

## Open questions

<!-- generated: open -->
- Search method and ranking remain open: semantic, keyword or both. Test on stored information during implementation. Start with top 10 and adjust during experiments.
- Labelling details remain open: who, how many, which interface, model evaluation and training, handover to a smaller model, and checks for omitted or mislinked extraction evidence.
<!-- /generated: open -->

## Proposals awaiting Alex's decision

Other proposals were resolved individually. The due-date proposal became state freezing, and D356 settled the questions whose answer is unavailable or not yet published (they close at their state like any other). This one remains and is not built until it is decided.

<!-- generated: proposed -->
1. Proposal, not decided (D356): daily pairwise duplicate checks among open theses of a subject; merge the later thesis into the earlier, move links and dependencies, check cycles and rejudge. Add separate duplicate-check settings to Config.
<!-- /generated: proposed -->

## Related decisions

- D11/D16/D26: subject ownership, human review, central library and sources. D30: count independent original sources.
- D31: sequence ordering and one writing queue per thesis; later decisions revise relationships, late inputs and universe removal.
- D33: read-only extraction; library matching/writing.
- D38–D40: question/ladder/due-date structure, state, evidence links/tiers, dependencies/succession, round-based intake, history and matching labels.
- D41/D42: align frozen modules with the rebuilt library, separate evidence/candidates, compare within-thesis evidence, and permit binary ladders; the extraction request they described (with dependencies) became open theses with their takes lines (D211, D264). D375 on main supersedes D251's day-start timing with the latest committed questions before each item.
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
- The full-text call shows no list of stored groups; an open thesis's takes line names the groups it belongs to (D264). During that call, extraction declares named and scoped groups. A candidate that tracks an ongoing matter (a product rollout and its deployments, a deal, a policy process, an investment or demand cycle) cites one or more groups it declared, without repeats; a company's own reported or guided financial lines (total or segment revenue, margins, expenses, tax rate, capex) belong to the company and cite none unless the line itself tracks such a matter (D165). Code validates the references before writing, folds a declared group into a stored one by its names (D166, D257), and creates a declared group only when a written thesis that tracks a matter cites it, so a company's lines alone never found a group.
- Matching still decides thesis/evidence identity and dependencies; it does not reread association fields to regroup. After creation, succession or merging, the writer resolves candidate IDs to final thesis IDs and local group IDs to stored group IDs, then stores membership. Candidates failing source checks or ultimately skipped do not become members. Do not create empty groups for unused declarations or reject other valid memberships because of them.
- Store each group/member pair once, with input ID and sequence number under the library's ordering and historical-read rules. Commit groups and memberships atomically with theses and evidence; roll all back on failure. Never mark a partial write complete. Redelivery must not duplicate membership; use existing dispatch and recovery.
- Groups do not copy evidence. Read sources through members' real evidence links, filtered by the requested sequence and excluding evidence a legacy replacement record had retired by then (no new one is written, D202). No link means no evidence. A new member or an existing thesis change flag updates its groups. A repeated quote is stored as its own piece with the pair recorded (D204) and updates a group only through its thesis's change flag. Evidence-only articles update existing memberships without inventing theses or groups.
- Acceptance measures source-supported membership and evidence retention, not identical names, IDs or group counts on every run. Report omissions, check refusals, missed associations and wrong associations separately. Preserve Rubin shipment/customer-deployment relationships and check wrong links to unrelated products or customer-specific groups. Multi-company and large-library behaviour is not yet validated.
- Historical implementation reference: D147's isolated grouping prototype and its field names are preserved in the research records. D165 and D169 subsequently integrated grouping into the default pipeline. See docs/poc/pipeline-plan.md for the current implementation and measured limits; the old prototype does not establish large-library recall.
- See docs/poc/grouping-improvement-plan.md for gaps and steps. D148 member context and D150 reason-first output did not solve wrong grouping. D152's four name-selection responses to the third article created no candidates, so new membership was unexercised. Preserve all prior responses and results. Overarching thesis generation, MCP presentation and historical backfill are outside that implementation scope.
<!-- /generated: relations -->

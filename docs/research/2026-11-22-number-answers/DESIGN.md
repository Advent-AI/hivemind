# judging-v13: related number questions judged together, with a checked calculation (design v10, after council round 46j and D728; for round 46k)

Opened by Alex (D726) for the bounded test of D725. Harness-only until a later decision: no product configuration names it, and
the ordinary launchers refuse it (D359, D723). The frozen judge (judging-v7, poc-v118) is unchanged.

v2 answered round 46 (`codex-r46.md`, changes marked [46.n]). v3 answers round 46b (`codex-r46b.md`, marked [46b.n]). Rounds 46 and
46b found the same weakness five times: the checks trusted what the answer declares about itself (its `uses` list, its labels, a
shortened span). **v3's structural rule:** code derives every relation it checks from the calculation itself and from the passage
text, and the answer declares nothing code relies on without checking it:
- each outcome's inputs are found by walking the figure graph;
- a future quantity shared by the family enters any forecast only through the family's one forecast node for it, checked on every
  path from an outcome, not by membership in the graph [46c.1];
- a source figure must equal a complete numeric expression that code extracts from the passage.

## 1. What changes

| Piece | judging-v7 (today) | judging-v13 |
|---|---|---|
| Unit | one question per call | one **family** per call: the number questions of one company whose quantities overlap (a total and its segment or product line, a level and its growth, and a later year declared to rest on an earlier year's base [46.2]). Each keeps its own answer |
| Who forms a family | none (0 dependencies) | **declared** for the test from the stored cases, with typed relations: `part_of(part, whole)` and `same_base(later, earlier)`. Production would need a matching version that names them |
| Evidence shown | each question's own evidence in view (D198) | the union of the members' evidence in view, each passage once with its attribution; themes once |
| Previous conclusion | rung and reasons, cut at 800 characters, unmarked | **not shown** (D728). Whether a member's conclusion changed is derived by code afterwards from its earlier rung, outcome and source figures (`calc_check.changed`) |
| Answer | prose fields plus one answer-wide citation list | a calculation (figures) plus exactly one answer per member (§2) |
| Request text | judging-v7 | a full v13 request written and audited (§5) [46.6] |
| Failure | refused twice: the question is left as it was | refused twice: the family is recorded **unresolved** and no member is updated. A member may also answer `unresolved` itself (§2) [46.5] |

## 2. The answer format (closed set; the schema enforces shape, code enforces §3)

```
figures: [ { id,
             what: { population, measure, scope, period },     # canonical: measure is the quantity ("revenue"), not its basis [46.1]
             basis: "reported" | "guidance" | "consensus" | "third_party" | "forecast" | "prior_forecast",
             scenario: "base" | "<named>",                       # default "base" [46.1]
             kind: "source" | "computed" | "estimate",
             value | {low, high} | {bound: ">" | ">=" | "<" | "<=" | "approx" | "approx_below" | "approx_above", value} | {multiplier, bound?},  unit,   # [46c.3]
             # kind source:   evidence: "<id>", expression: <index of a complete expression code extracts from that passage>,
             #                component: "midpoint" | "low" | "high" | "bound" | "multiplier" | "value"            [46b.2]
             # kind computed: inputs: [...], operation: sum|difference|product|ratio|growth|apply_growth|share|range_from_relative|roll_forward,   # [46c.2]
             #                relation (sum and roll_forward): "accounting_parts" | "time_aggregation" | "stated_in_addition" | "overlap_unknown",
             #                disputed (overlap_unknown only): "<the operand whose inclusion is in doubt>"            [46b.4, 46d]
             #                bridge (when inputs' what differ from the output's): "<figure id of an estimate>"   [46.3]
             # kind estimate: basis_text, rests_on: [figure ids, evidence ids],
             #                adjusts (optional): { figure: "<id>", type: "discount" | "uplift" | "trim" }            [46.3]
             #                a bridge estimate also names `converts: [operand ids]` and the assumption           [46b.3]
           } ]
answers: [ { view_id, shape: "forecast", outcome: "<figure id>", rung,                 # [46b.5] two shapes
             reference: { figure: "<id>" } | { unavailable: "<why>" },                # per answer [46.2]
             reasons, cites, pushes, theme_pushes, changed, why_changed }
         | { view_id, shape: "unresolved", why, cites, changed, why_changed } ]       # no outcome, no rung
```

- **An arithmetic intermediate and the analyst's final range are distinct figures** [46.2]. For example, q02's $392B × 92% is a
  `computed` figure. The final $370–400B is an `estimate` resting on it and on q01's range. Code checks the intermediate's arithmetic
  and never requires the final range to equal it.
- **`prior`** figures (basis `prior_forecast`) are for comparison only [46f.4]. They need a pointer to an earlier answer shown in the
  request and must equal a figure that answer states (C10). They may feed no figure. A declared `same_base` reads the family's own
  forecast node of the earlier member at the same snapshot (q22 reads q01's): C9.
- **`roll_forward`** [46c.2]: an opening balance as of a date, plus additions and minus drawdowns over a later period, gives the
  balance at that period's end. It is the accounting identity for a stock and its flows. An addition whose inclusion in the opening
  balance is in doubt carries `relation: overlap_unknown` and `disputed` (R2's $18B).
- **Scenarios carry ranges** [46b.1]. A forecast node is a point within a scenario. A range across members is written as paired
  scenarios (for example `low`, `high`) whose nodes stay paired. The analyst's final answer may be a range `estimate` resting on the
  scenario outcomes.
- **The family declaration** (by the harness, not by the answer) lists the shared quantities and periods the members depend on, for
  example company revenue for each FY2027 quarter, and the typed relations [46b.1].

## 3. What code checks (identity and arithmetic only)

| Check | Rule | Refuses |
|---|---|---|
| **C1 source expression** [46b.2] | code extracts every complete numeric expression from the cited passage as shown, with its qualifiers and unit. Points: "$108.0 billion". Ranges: "$105–110 billion". Relative: "$108.0 billion, plus or minus 2%" is midpoint 108 ±2%. Bounds: "more than $730 billion" (>730), "at least" (>=). Approximate bounds: "nearly $800 billion" (approx_below 800). Multipliers: "double" ×2, "more than double" (>×2). A source figure names one extracted expression and a component of it (midpoint, low, high, bound, multiplier), and must equal it exactly: value, unit, sign and qualifier. Any other wording cannot be a source figure | a figure that strips a qualifier ($730 from "more than $730 billion"); a bound used as a point; a wrong number within 0.5% (108.5); a figure naming no extracted expression |
| **C2 arithmetic** | a `computed` figure recomputes from its inputs by its operation. Rounding: to the figure's stated precision, at most 0.5% or 0.1 unit. `range_from_relative` makes 108 ± 2% into 105.84–110.16 | a wrong sum, share or endpoint |
| **C3 part within whole** [46b.1] | for each declared `part_of`, in each scenario, for each declared period: the part's value, found by walking the graph from the part member's outcome to its node for that period, is at most the whole's. Annual and quarters are compared where the declaration names them | a segment quarter above the company quarter |
| **C4 one forecast per shared quantity** [46b.1, 46c.1] | for each shared quantity and period the declaration names, each scenario has exactly one `basis: forecast` node. **Every path** in the graph from a member's outcome to any figure that measures that quantity and period passes through that node. A guide, consensus or other source of a future period may feed the forecast node; no path from an outcome may reach it while avoiding the node | the $108B guide feeding v14's $113.5B forecast and, on another path, v9's Data Center Q3 directly: the same guide node, a bypass |
| **C5 reference** [46b.3, 46c.1] | each answer's reference is `unavailable` with a reason, or a direct `source` figure of basis consensus, guidance or third_party from a passage whose speaker is not the system, or a `computed` figure whose whole graph is computed figures over such sources and `reported` sources (q02: $392B consensus × 92% reported mix). No `estimate`, `forecast` or `prior_forecast` anywhere in the reference's graph. Its provenance is shown | the system's own forecast presented as the market's, directly or wrapped in an estimate that cites outside evidence |
| **C6 rung and outcome** [46.2] | the chosen rung's band overlaps the outcome (a point: contains it). The reasons say why that band, where the range overlaps several | a rung no part of the outcome falls in |
| **C7 structure** [46.5] | exactly one answer per member; an answer's outcome `what` matches its member's question (population, measure, scope, period, from the question's typed key); figure ids are unique; references are not dangling and not circular; operations come from the closed set | a missing or doubled member, a borrowed outcome, a dangling or circular figure |
| **C8 operand compatibility** [46b.3] | by operation. **sum/difference:** same measure, population and scope, with periods either disjoint and together forming the output period (`time_aggregation`), or identical with a declared relation (`accounting_parts` needs a declared `part_of`). **roll_forward:** an opening balance as of a date, and flows over a period starting then or later, give the closing balance [46c.2]. **per unit** [gate run 1]: a total over a price per unit gives units, and units times that price give the total, for one population and scope (q19's $20B at $5,000 a Vera CPU is four million units). **share:** numerator and denominator stated, with a declared `part_of` or a reported mix. **product/ratio:** a change of measure, population, scope or period not covered above needs a bridge estimate whose `converts` names the actual operands, and an assumption | 730/800 × $1.3T with no bridge naming e1786's four-company 2026 spending and e2535's five-company capex; a bridge that converts other operands |

| **C4 scenarios** [46g.3, 46h.1, 46i.1] | each scenario has one forecast node per shared quantity. Scenario membership is derived along the whole path: no figure of a point scenario may depend, at any depth, on a forecast node of another scenario. A `range` summary is an estimate with low and high, is an answer's outcome, and feeds no figure; only it may rest on several scenarios; a bypass is a path that reaches the quantity through no forecast node of any scenario | a low path on the high total; a guide relabelled as an alternate scenario and read by the base |
| **C4 derived scenarios** [46j.1] | a figure's scenarios are those of the estimates it rests on at any depth; a point-scenario figure may rest on no estimate of another scenario; related members (`part_of`) cover the same scenarios, so C3 compares like with like | the company in `base` and Data Center in `alt`; crossed share estimates |
| **C5 one choice** [46g.2] | a reference names exactly one of a figure or `unavailable` | a prior figure hidden beside an "unavailable" reason |
| **C9 same base** [46f.3, 46j.2] | for each `same_base(later, earlier)`, the later member rests on the earlier member's forecast nodes (its outcome, or the scenario paths behind its range summary), and every path to a figure of the earlier quantity and period passes through one of them; scenarios match by C4 | FY2028 grown from the $392B consensus instead of q01's $400–435B forecast |
| **C10 earlier forecasts** [46f.3, 46f.4, 46h.2, 46i.2] | a figure is an earlier forecast when its kind is prior, its basis is prior_forecast or it carries a pointer (derived, not labelled), and it must then be kind prior with basis prior_forecast; such a figure points to an earlier answer shown in the request and equals a figure that answer states; it feeds no figure and is no answer's outcome | an invented or misdated earlier figure; an earlier forecast used as an input |
| **C2 bound direction** [46f.3] | for positive operands, a result's bound side follows its inputs: sums and products keep a lower or upper side, a ratio's or difference's second operand flips it, and mixed sides give `approx` | "more than double" times $20B declared below $40B |

**Recorded, not refused** (visible to readers and to the page) [46.3]:
- **Overlap:** a `sum` or `roll_forward` with relation `overlap_unknown`. Its alternate recomputes that same calculation without the
  named `disputed` operand, all else fixed [46b.4, 46d].
- **Adjustment:** an `estimate` that `adjusts` a figure. Its alternate is the adjusted figure (R4: the bound ">40").
- **Bridge:** every bridge; alternate undetermined.
- **Boundaries** [46f.3]: a point alternate, or a bound lying beyond the outcome on its own side, decides a crossing definitely; a bound on
  the near side only possibly. Code recomputes, from unrounded values, each outcome under each defined alternate. It records which rung boundary the
  assumption definitely or possibly decides: "crosses $40B" when the alternate is a bound, a rung change when the alternate is a
  point. Where a downstream estimate has no formula, or no alternate is defined, it records "undetermined". A reader decides whether a
  boundary-deciding assumption is supported. D721/D722: unresolved inclusion is never treated as proof of double counting.

**The model keeps:** drivers, weights, discounts, scenarios, the choice among overlapping bands, and whether to step off the
reference. Code never prefers guidance, prescribes a haircut, refuses an estimate for being one, or picks a band from a midpoint.

## 4. Tables

**Value × reader.**
- **The calculation, the recorded assumptions and band-deciding flags:** read by the checks, the readers' packets, and later the
  page.
- **`unresolved`:** read by the round (no member updated) and the bundle ("Forecast unavailable", D726).
- **The family declaration:** read by the request builder, C3, C4 and C7.
- **Nothing in poc-v118 reads any of it.**

**New path × old checks.**
- v7's id, push and theme checks apply per member answer. Rung checks apply to `forecast` answers only [46b.5]. `cites` names shown
  evidence only.
- `cites_views` is always empty.
- v7's request bytes are unchanged (the frozen pins).

**State × event (the test harness).** Inputs are fixed: the stored requests' passages and the gold packet's items, as of the stored
day.

| Event | Outcome |
|---|---|
| success | the calculation and answers are recorded with their check results |
| refusal | the errors are recorded; one retry with them |
| second refusal | the family is unresolved, recorded |
| a member's own `unresolved` [46b.5] | recorded; the family is held (no member updated) when any other member's outcome depends on a shared quantity or relation involving it; otherwise the others publish if they pass |
| crash midway | the attempt is recorded incomplete and counts as no result |

Nothing writes a product store. Production lifecycle (members closing or opening, families changing) is designed only if the test
passes.

**Prior decisions:**
- D24, D28: bounded to the figures open questions consume.
- D198: evidence in view, unioned.
- D260, D263: the standard kept.
- D359, D723: no product launcher.
- D695: number questions.
- D711, D721, D722: linking passed conclusions, and unresolved inclusion is not double counting.
- D725, D726.

## 5. The v13 request text (written and audited at $0 before the gate closes) [46.6]

- **The basis:** judging-v7's standard sentences are kept, among them the reference, run-rate, discount, sizing, identities and
  consistency.
- **Replaced where they conflict with a family:**
  - the single-question delivery ("the current conclusions of dependencies");
  - "the previous conclusion carries" pieces not shown, which becomes "our earlier forecast, not a source";
  - the one-reference, one-outcome output sentence;
  - the dependency-consistency sentence, which becomes the family's own consistency, the same clause made family-wide.
- **Added:** how to write figures (kinds, bases, expressions, relations, bridges, `adjusts`, `unresolved`).
- **The audit:** every changed sentence is shown with its source (D260, D263, D725, this design), read against a stored family
  request, and its character count before and after is reported (AGENTS §6).

## 6. The $0 gate (registered; each defect must produce its named finding) [46.5]

| Item | Content | Pass: the named finding |
|---|---|---|
| R1a | old-2 8729 (v14) and 8737 (v9) on 09-20, as stored: v9 Q4 146, v14 Q4 127 | **C3** on Q4 |
| R1b | the same, with Q3 as stored: **one** guide node (midpoint 108 from e2499, labelled `guidance`) feeds v14's company Q3 forecast (113.5, beat-adjusted) and, on a second path, v9's Data Center Q3 (108 × 92.5% = 99.9) | **C4** on Q3 company revenue (the bypass path), independent of C3 |
| R1c (control) | the same guide node (midpoint 108 ±2%, e2499's expression) feeding one shared Q3 forecast node (113.5) that both members read | passes |
| R2 | old-2 8734 as `roll_forward`: the $25B balance as of July 26 (e2620), plus the $18B committed for the rest of the fiscal year (e2889) as `overlap_unknown` and `disputed`, plus MediaTek and the talks as estimates | passes C8; recorded overlap; the alternate without the $18B (about $35B) decides the $50B boundary (conditional) |
| R3 | old-2 8595: 730 (e1786, bound ">") / 800 (e2535, bound "approx_below") × 1,300 (e2535, point) | stripped qualifiers: **C1**. Qualifiers kept: passes C1, then **C8** without a bridge naming those operands. With the bridge: recorded, undetermined |
| R4 | old-3 9166: 20 × (>2) (e3660, "more than double") gives >40, trimmed to 38–39 by `adjusts: trim` | recorded adjustment that definitely crosses the $40B boundary (rung 2 is $40–50B, rung 1 $50B+) |
| G1–G4 (controls) | q01, q02, q19, q22, from `gold-v1.json`'s reasoning (expressions from the packet items). q01's Q1 + Q2 as `time_aggregation`; q02's comparison $392B (consensus) × 92% (reported mix); q22 in one family with q01, reading q01's FY2027 node | all pass, estimates visible; q02's reference passes C5; q19's overlapping range passes C6 with its reason |
| P1–P3 (plants, on control copies) | P1, an amount absent from its expression; P2, a wrong sum; P3a, a prior forecast as the reference; P3b, the same figure wrapped in an estimate that cites outside evidence | P1 **C1**, P2 **C2**, P3a and P3b **C5**, each for its intended reason |
| T1–T7 (C1 forms, real passages) | e2499 midpoint 108 ±2% (accepted as `midpoint`); e1786 ">730"; e2535 approx_below 800 and the point 1,300; e3660 ">×2"; stripped forms "$730", "800", "double" against those passages; 108.5 against e2499 | T1–T3 parse as stated; the stripped forms and 108.5 refused |
| U1–U2 (paths) | a member answering `unresolved` while another member's outcome needs its shared quantity; a calculation refused twice | the family held, recorded; the family unresolved, recorded |

- **Stop:** any missing finding, a finding for the wrong reason, or a control the format cannot express.
- **Then:** Council B on the gate's output. The paid gate's ceiling goes to Alex.

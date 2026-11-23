# judging-v13 repair, design v2: every rule the checks enforce is held by the schema or written beside its field (D734; council rounds 49–50)

v1 answered D734. Round 49 (`codex-r49.md`) found:
- rules still unstated across C1–C10;
- two unsound check changes (a growth label the answer supplies itself; containment that flips signs and negations);
- wrong test inputs (E is a Fed question; S is CY2026);
- a blind test that could pass with no usable answer.

Round 50 (`codex-r50.md`, `claude-r49.md`) agreed on a finish line:
- at most two more review rounds, one on this exact wording and case list, one on the request the harness actually sends and the
  checks it runs;
- then the blind test once;
- a serious issue left after the second round goes back to Alex.

Claude's option B (shrink the checks) was set aside. It drops C8's guard against adding a segment into its total, and it exceeds D734.

**Out of scope:**
- the frozen ruler and `poc-v118`;
- D725's pass lines and D731's harness rules;
- the system text's judging sentences, which stay unchanged.

**The structural rule:** each refusal the checks can emit is either impossible under the schema (an enum or a marker) or has its
rule written in the request, beside the field it governs. Family-specific rules go in the user message's family header.

## 1. The wire shape

| Today | Repaired | Held by |
|---|---|---|
| `answers[].outcome` (string) | `figures[].outcome_for`: array of member ids (enum) | the enum; C7: exactly one marked figure per forecast member, none for an unresolved one, no member listed twice on one figure |
| `answers[].reference {figure, unavailable}` | `figures[].reference_for`: array of member ids (enum); `answers[].reference_unavailable`: nullable string | the enum; C5: exactly one of a marked figure or a non-empty reason for a forecast member; for an unresolved member, a marker or reason is refused (C7) |
| `figures[].evidence` | `evidence_id`: enum of the request's passage ids, or null | the enum |
| `figures[].bridge` | `bridge_estimate_id` | the description; C7, C8 |
| `figures[].disputed` | `disputed_input_id` | the description; C8 |
| `figures[].converts` | `converts_input_ids` | the description; C8 |
| `figures[].adjusts.figure` | `adjusts.figure_id` | the description; C7 |
| `figures[].unit` | enum `USD bn`, `USD`, `%`, `x`, `units` | the enum |
| `figures[].scenario` | unchanged: a free name; `base` and `range` described | the description |

**Decoding is bound to the plan's format.**
- The new plan's items carry `"format": "v13r"`. `calc_check.from_answer(data, family)` converts a v13r answer into the internal
  shape and returns the marker errors as C7 and C5, before `check`.
- `paid_gate` decodes with `from_answer` only when the item's format is v13r, at `Gate.attempt`, `summarise` and `card_lines`.
  Otherwise it decodes with today's `strip`.
- The old run's journals keep their decoder. Re-running `summarise` and `packets` on a copy of the old run must reproduce its
  `results.json` byte for byte.
- `render_v13.strict` gains the v13r direction for its fixture.
- The rehearsal takes the plan path as an argument.

## 2. The exact wording

### 2a. Schema descriptions (figures)

Examples come from other domains, never the covered company or the gate's numbers (AGENTS §6).

| Field | Description |
|---|---|
| `figures` | "The family's calculation. Each figure is one number and what it measures: a source (read from a shown passage), computed (one operation on other figures) or an estimate (your judgement). Figures name each other by id; no figure may depend on itself through other figures." |
| `id` | "A short name unique in figures, such as F1. Every link to a figure uses this id." |
| `what` | "What the number measures. Where the request lists keys (outcome keys, shared quantities), copy them exactly." |
| `what.measure` | "The quantity, such as revenue or capital expenditure; never its basis. A price per unit is 'price per unit'; a count of items is 'units'." |
| `what.period` | "Fiscal year 'FY2027', quarter 'FY2027 Q3', half 'FY2027 H1' or 'FY2027 H2', calendar year 'CY2026', a balance 'as of 2026-07-26' or 'end of FY2027'; any other period in plain words." |
| `basis` | "reported: an actual; guidance: the company's outlook; consensus: analysts' average; third_party: one outside party's figure; forecast: this family's own forecast, only on a computed or estimate figure. For each shared quantity the request lists, write one forecast figure per scenario, and let every figure that uses that quantity (a guide, a consensus, a member's calculation) reach it only through that forecast figure." |
| `scenario` | "'base' unless you carry a spread as named scenarios (for example 'low' and 'high'); source figures are 'base'. Each scenario has its own forecast figure for each shared quantity; a figure of one scenario never uses an estimate or forecast of another. A part and its whole use the same scenarios. 'range' is reserved for one estimate with low and high that summarises the scenarios, is a member's outcome, and feeds no other figure." |
| `kind` | unchanged |
| `value` | "A point, or the number a bound qualifies. Give value, or low and high, never both." |
| `low`, `high` | "A range, low at most high, with value null." |
| `bound` | "Only with value: '>' more than, '>=' at least, '<' less than, '<=' up to, 'approx' about, 'approx_below' nearly, 'approx_above' just over. On a computed figure leave it null: the code derives it from the inputs (a stated bound must match)." |
| `unit` | "USD bn: money in billions of US dollars ($1.2 trillion = 1200; $500 million = 0.5). USD: a price per unit in dollars. %: a percentage as its number (7.5% = 7.5; a fall of 12% = -12). x: a multiplier (double = 2). units: a count. An outcome is in its member's unit (USD bn)." |
| `evidence_id` | "Source only: the shown passage the number is read from." |
| `expression` | "Source only: copied word for word from that passage's Quote line, never its summary: the qualifier, the number and its scale, and nothing else, for example 'more than $2 billion', 'about 40%', '$4.5 billion, plus or minus 3%', '$3–4 billion', '$300 million or more', 'more than triple'. Qualifiers: more than, over, at least, nearly, almost, approximately, about, around, roughly, up to, less than, below, under, and 'or more' or 'or less' after the number. A negated figure ('will not exceed $5 billion') cannot be a source; state it as an estimate." |
| `component` | "Source only, which part of the expression the figure takes. value: a plain amount or a percentage ('$2 billion'; 'about 40%' is value 40 with bound approx). bound: a qualified amount ('more than $2 billion' is value 2 with bound '>'). low and high: one figure for each end of a written range, each with value. midpoint and relative: '$4.5 billion, plus or minus 3%' is two figures, 4.5 USD bn and 3 %. multiplier: 'double' or 'triple' (value 2 or 3, unit x; 'more than double' adds bound '>')." |
| `inputs` | "Computed only: the ids of the figures the operation uses, in its order; never passage ids." |
| `operation` | "Computed only. sum(a, b, …): adds; with signs, adds and subtracts. difference(a, b) = a − b. product(a, b, …): multipliers (x), or a count (units) by a price per unit; never money by a percentage (use share). ratio(a, b) = a ÷ b. growth(old, new): the % change. apply_growth(base, rate %) = base × (1 + rate ÷ 100). share(whole, percent) = whole × percent ÷ 100. range_from_relative(midpoint, relative %) = the range midpoint ± relative %. roll_forward(opening, flows …): a balance as of a date plus or minus later flows (use signs). sum takes 1 to 99 inputs, product and roll_forward 2 to 99, the others exactly 2. The figure's value must equal the result within 0.5% (at least 0.1, or 0.05 for %); a computed range states both ends." |
| `signs` | "sum and roll_forward only: one 1 or -1 per input, in order (a − b − c is sum with signs [1, -1, -1]); null adds all. Null for every other operation." |
| `relation` | "sum, difference and roll_forward: time_aggregation, one quantity over periods that combine exactly into the output's period, same fiscal year (Q1 + Q2 = H1; FY − Q1 − Q2 − Q3 = Q4); stated_in_addition, a shown passage says the amounts add; overlap_unknown, whether one input is already inside another is unknown (name it in disputed_input_id; its effect is shown to readers); accounting_parts, only for a split of a whole that the request declares (none is declared unless the request says so). Inputs measuring the same quantity and period need none." |
| `disputed_input_id` | "overlap_unknown only: the id of the input whose inclusion is in doubt; it must be one of inputs." |
| `bridge_estimate_id` | "Computed only, when an input measures another population, scope, measure or period than the output (percentages and multipliers aside) and nothing below covers it: the id of an estimate whose converts_input_ids lists exactly those inputs and whose basis_text states the assumption. Covered without a bridge: time_aggregation; share; a product by a multiplier of the same quantity; a count times a price per unit, or a total over a price per unit, for one population and scope; growth; range_from_relative; apply_growth when the family declares that a later member rests on an earlier member's base. Otherwise a rate applied to another period's base needs a bridge stating which comparison the rate is (for example 'the rate is year over year, so it applies to the same quarter last year')." |
| `converts_input_ids` | "Bridge estimates only: the ids of the inputs the assumption converts, exactly those that differ from the output." |
| `basis_text` | "Estimate only: the assumption in words." |
| `rests_on` | "Estimate only: the ids of the figures and passages it rests on." |
| `adjusts` | "Estimate only, optional: the figure (by id, never a passage) this estimate changes, and how: discount, uplift or trim; the effect of the change is shown to readers." |
| `outcome_for` | "The members whose forecast this figure is. Each member answered as a forecast has exactly one figure marked; an unresolved member has none. Its what must equal the member's outcome key." |
| `reference_for` | "The members for which this figure is the market's reference: a consensus, guidance or outside party's figure from a shown passage, or a figure computed only from such figures and reported figures, with at least one outside figure. Never a forecast or an estimate anywhere beneath it." |

### 2b. Schema descriptions (answers)

| Field | Description |
|---|---|
| `shape` | "forecast: one figure marked in outcome_for, a rung, and a reference figure or reference_unavailable. unresolved: why; no rung, no marked figure, no reference." |
| `rung` | "Forecast only: the rung number (1 to the ladder's length) whose band overlaps the outcome; a band includes its lower edge and excludes its upper edge. When a range or bound overlaps several bands, choose one and say why in reasons." |
| `reference_unavailable` | "Forecast only, when no figure is marked as its reference: why." |
| `why` | "Unresolved only: why the evidence cannot support a forecast." |

### 2c. The family header (user message; `render_v13.render`)

- `Relations:` keeps its line. A part line gains: "the part's figure for each of these periods may not exceed the whole's:
  <compare_periods>". A same-base line gains: "compute <later> from <earlier>'s forecast figure (its outcome, or the scenario figures
  behind its range), never from another figure of that quantity".
- `Shared quantities` keeps its line.
- `Outcome keys` keeps its line and adds the unit: "…, in USD bn".

## 3. Check changes (each keeps the refusal it was built for, and is proved by a mutant)

| # | Change | Why | Still refused |
|---|---|---|---|
| 3.1 | time_aggregation on sum or difference uses signed period sets: the signed count of each quarter over the inputs equals the output's quarters, within one fiscal year | FY − Q1 − Q2 − Q3 = Q4 and FY − H1 = H2 are inexpressible today (difference reads like a sum) | overlapping or missing periods; mixed fiscal years |
| 3.2 | **dropped** (the "vs" growth label) | it trusted the answer's own label (round 49) | a rate applied to another period's base without a bridge stays refused, and the bridge is now described |
| 3.3 | product refuses an operand in % multiplied with money (USD bn or USD), with the message "use share (whole, percent)" | $411 billion × 92.5% read as 38,017.5 | — (12% × 2x = 24% still passes) |
| 3.4 | **the extractor**: a leading minus sign is part of a percentage or amount; "or more" and "or less" after an amount give '>=' and '<='; an expression within three words after a negation (not, no, never, n't) is refused as a source | today "-12%" reads as 12, "$300 billion or more" as a point, and "not be over $300 billion" as '>300' | everything refused today; containment (v1's 3.4) is **dropped**, and the expression stays the exact extracted span |
| 3.5 | C2 accepts a computed figure with no bound and gives it the derived bound; a stated bound must still match | the code derives the bound anyway (`_evaluate_bounded`), so refusing an omitted one refuses an answer the code can complete | a wrong stated bound; opposing bounds (state an estimate) |
| 3.6 | C7 refuses basis `forecast` on a source figure | a source labelled forecast would count as the family's forecast node | — |
| 3.7 | C6 refuses an outcome whose unit is not its member's unit (each member declares `unit: 'USD bn'`; the bands are in billions) | $1.05 trillion written as 1.05 was compared with bands in billions | — |
| 3.8 | `from_answer` marker rules (§1) | the new shape | — |

**Unchanged:**
- C3, C4, C5's graph walk and C9.
- C10 stays unreachable through the wire format: no `prior` kind, no pointer.
- Bridges, overlaps and adjustments are recorded for readers as today.
- The same_base exception for `apply_growth` is kept as written (round 49: replacing it broke G4).

## 4. Tables

**Value × reader.**
- **The v13r schema** is read by the plan builder (a new pinned plan, `paid-plan-v13r.json` with its sha, under a new name), the
  rehearsal (given that plan), `render_v13.main` and `model.check_schema`.
- **The decoded answer** is read by `check`, `publish_decision`, `summarise`/`merge`, `card_lines`/`card_view`/`normalise` and the
  verdict, through `from_answer` for v13r and `strip` for the old format.
- **Member `unit`** is read by C6 only.
- **`compare_periods`** is read by C3 and now by the header text.

**New path × old checks.**
- The $0 gate (87), the rehearsal (63) and both mutant sets pass on the new code.
- The internal fixtures stay. The rehearsal stubs are rewritten in v13r.
- The old run reproduces on a copy.
- Each change in §3 has a mutant whose test fails without it.

**Size.**
- Today: the largest stored schema is 10,056 characters, and the largest user message is 134,199.
- The build reports the whole request (characters and estimated tokens) per item, before and after.
- Expected growth is about 6,000–10,000 characters of schema descriptions (round 50's estimate is a largest schema of 16,000–20,000).
- The written reason (AGENTS §6): these are the definitions the checks already enforce.
- The passage-id enum appears three times: `evidence_id`, `cites` and `pushes`. One `$defs` entry is used if `model.check_schema` and
  the provider's strict mode accept `$ref`. Otherwise it stays repeated, and its size is reported.

## 5. The blind conformance test (registered here; $0, no provider call)

**Inputs**, built by the repaired `paid_gate.item`. Each case's archive, call id, question, period, ladder and unit are registered
together, and the build refuses a heading whose thesis id or question differs.

| Case | Archive / call | Member key | Evidence | Role |
|---|---|---|---|---|
| P (joint) | old-1 v4 8810 + v8 8816 | NVIDIA revenue company FY2027; NVIDIA revenue Data Center FY2027 | union 296 passages, 79 quotes absent from the gate's plan | fresh evidence; the pair shape |
| P-v4, P-v8 (separate) | the same calls, one header each | as above | the same union | the separate shape |
| S | old-3 v6 9043 | four largest AI hyperscalers, data-center capex, combined, **CY2026** | 50 passages, 41 fresh | fresh evidence; a scope bridge |
| O | old-2 v29 8507 | NVIDIA equity investment commitments company end of FY2027 | 30, none fresh | control: roll_forward with overlap |
| E | old-3 v41 9071 | NVIDIA revenue Vera CPU FY2028 | 15, none fresh | control: multiplier and adjustment |

**Part A, the checks against registered forms** (code; each asserts its intended check and message, and a schema error cannot mask it).

- **A1, correct forms in v13r.** Each must pass:
  - $108.0B ± 2% as midpoint and relative, with range_from_relative;
  - Q1 + Q2 = FY2027 H1;
  - FY − Q1 − Q2 − Q3 = Q4 as a signed time_aggregation;
  - a year-over-year rate on the prior-year quarter, with a bridge;
  - a whole × mix via share;
  - "over $300 billion" (from "well over $300 billion") and "65%" as exact spans;
  - $1.05 trillion as 1050 USD bn;
  - a range outcome whose rung overlaps it;
  - one figure marked for two members;
  - a computed external reference (consensus × reported mix);
  - an unresolved member with nothing marked;
  - a roll_forward with an overlap recorded;
  - a valid scope bridge;
  - both per-unit directions;
  - a same-base family computing from the earlier forecast;
  - 12% × 2x = 24%;
  - a computed figure with its bound left null.
- **A2, planted defects on copies of A1.** Each is refused by its named check:
  - 108.5 for $108.0B (C1);
  - "$300 billion" stripped of its qualifier (C1);
  - "-12%" taken as 12 (C1);
  - "$300 million or more" taken as a point (C1);
  - "not be over $300 billion" as a source (C1);
  - value plus range (C7);
  - a missing range end (C7);
  - Q2 + Q3 labelled H1 (C8);
  - a Data Center quarter added into company revenue with no relation (C8);
  - money × % through product (C2);
  - a rate on another period's base with no bridge (C8);
  - a cycle (C7);
  - no outcome marker, two outcome markers, and a marker on an unresolved member (C7);
  - both a reference marker and a reason (C5);
  - a forecast inside a reference (C5);
  - an outcome key mismatch (C7);
  - a shared-quarter bypass (C4);
  - a cross-scenario estimate (C4);
  - a bridge converting the wrong inputs (C8);
  - an outcome in the wrong unit (C6);
  - a source labelled forecast (C7);
  - duplicate member answers (C7).
- **A3, Luna's observed mistakes** (from both journals). Each is encoded on the v13r shape and is either impossible under the
  schema (an enum) or refused with a reason the request states (the sentence is quoted):
  - prose outcome, reference, evidence and bridge;
  - unit spellings;
  - value with range;
  - signs on a difference;
  - a four-input difference;
  - money × % via product;
  - "first half";
  - "65% growth in Q4";
  - a passage id in inputs and in adjusts;
  - a trillion outcome.
- **A4, the existing harness.** The $0 gate, the rehearsal and the mutants pass, and the old run reproduces.

**Part B, blind writers.**
- **Two writers:** Claude subagents and fresh read-only Codex sessions. Each writer works in a fresh context per case (12 sessions).
  Each gets only that case's exact outgoing system text, user text and schema, and the instruction to answer as the JSON schema
  defines it.
- **The first outputs** go through `model.check_schema`, `from_answer` and `check` unedited.
- **Two readers** who wrote neither the design nor the answers (a Claude subagent and a Codex session) record two facts for each
  refusal:
  - whether the exact outgoing request states the condition, quoting the sentence;
  - whether the answer is correct against the shown passages.
- **A third reader** settles disagreements. Truncation, session failures and checker exceptions are classed apart.
- **Reported:** per case, supported forecasts, justified unresolved answers, and refusals by rule.

**Stop.** The test stops on any of these:
- an A1 form refused;
- an A2 defect escaping its intended check;
- an A3 mistake neither impossible nor stated;
- a Part B refusal whose condition the request does not state, or that refuses a correct answer;
- an INCOMPLETE run;
- a case registered as answerable (P, P-v4, P-v8, S, E, O) with zero usable first replies across both writers;
- the joint case without both supported forecasts in one reply.

**A clean result** goes to Alex as a request for the paid comparison: the same 36 requests rebuilt with v13r, under a new decision
with D725's lines. Only that run measures whether Luna can do this at medium effort in one pass.

# judging-v13 small format (v13s): code refuses only the five defects and broken structure (D737)

Alex (D737) chose to shrink the format. Code refuses an answer only for these five defects:
- a number misread;
- wrong arithmetic;
- a part above its whole, or added into it;
- two forecasts of one quarter;
- an own estimate passed off as the market's.

It also refuses broken structure. Each rule is written in one or two sentences beside its field. Every other rule of `DESIGN.md`'s
checks becomes something the readers see, not a refusal.

**Review scope (D737):** a counterexample that lets none of the five defects through, and breaks no structure, is a reader's matter,
not a finding. **Out of scope:**
- the frozen ruler and `poc-v118`;
- D725's pass lines and D731's harness rules;
- the old run and its checker `calc_check.py`, which stay as they are, so the old run stays reproducible.

## 1. What is dropped, and where it goes

| Today's rule (DESIGN.md) | v13s |
|---|---|
| bounds and their propagation (C2 bound direction, C3/C6 open ends) | a source's qualifier is checked against the quote and shown to readers; computed figures are points or ranges |
| scenarios, scenario membership, `range` summaries (C4) | one forecast per shared quantity; an outcome may be a range |
| relations `time_aggregation` / `accounting_parts` / `stated_in_addition` / `overlap_unknown`, and `disputed` | periods of one quantity must make up the output's period (S8); an uncertain overlap is written as an estimate with its assumption |
| bridges and `converts` (C8) | a conversion between quantities is computed or estimated as the analyst chooses; code records each computed figure whose inputs measure another quantity, and readers judge it |
| `roll_forward`, the per-unit identity, `range_from_relative`, `signs` | `sum`, `difference`, `product`, `ratio`, `share`, `growth`, `apply_growth` |
| `adjusts` | an estimate rests on the figure it changes |
| C9 (same base), C10 (earlier forecasts) | none of the gate's families declares a same base; the request shows no earlier forecast (D728) |
| the exact-expression grammar (C1) | the number as written (`quote_number`) plus a qualifier from a closed list |

## 2. The rules code enforces (revised after round 52, `codex-r52.md`; the revision is marked [52])

**[52] Shared definitions.**
- **Uses.** A figure *uses* another when the other is among its `inputs`, at any depth. An estimate's `rests_on` is a judgement, not
  a use. Code records it for readers, and an estimate is the value the figures above it use.
- **Recomputed values.** The published value of a computed figure is the recomputed one, a point or a range. S3, S4 and S6 compare
  recomputed values. S2's tolerance applies only between a declared value and its recomputed value.

| # | Defect | Rule [52] (as the request states it) | Where stated |
|---|---|---|---|
| S1 | a number misread | A source figure names its passage (`evidence_id`) and copies the number exactly as the quote writes it (`quote_number`). The number is in US dollars ($, US$) with its scale (trillion, billion, bn, million), or is a percentage, or is one of the words double, triple or twice. The value equals it, with money in billions. A minus written before it makes the value negative. A qualifier written just before it (or "or more" / "or less" just after) goes in `qualifier`. A written range ("$3–4 billion", "between $3 billion and $4 billion") gives low and high. "$4.5 billion, plus or minus 3%" is copied whole, and gives its range as low and high or its midpoint as value. Money in another currency cannot be a source. | `kind`, `evidence_id`, `quote_number`, `qualifier`, `unit` |
| S2 | wrong arithmetic | A computed figure equals its operation's result within 0.5% (at least 0.1, or 0.05 for %). Units are those `operation` states for each operation; a sum or difference adds one unit. A range input gives a range: both extremes are computed first, and a midpoint may be declared as value. Division by a range that contains zero is refused. | `operation` |
| S3 | a part above its whole | For each period the Relations line lists, and for the outcomes, the part's lowest recomputed value used for that period may not exceed the whole's highest. | the family header |
| S8 | a part added into its whole; periods misadded | A sum never adds a figure that uses (or is) the part's quantity to one that uses (or is) the whole's: the whole already includes the part. A difference may subtract the part from the whole only to give the rest, another scope. When a sum's or difference's inputs are periods of one quantity, each period is written FY2027, FY2027 Q3, FY2027 H1, FY2027 Q1-Q3 (or CY likewise), and together they make up the output's period exactly (Q1 + Q2 = H1; FY − Q1-Q3 = Q4). An estimate that rests on both the part and the whole is recorded for readers. | `operation`; `what.period`; the family header |
| S4 | two forecasts of one quarter | Every number the outcomes use for one quantity and period is the same figure. Compute each quantity and period once, as a point or a range, and use that figure wherever it is needed. (Guidance or consensus beneath that figure is fine; a second figure of the same quantity and period reached on another path is not.) | the family header; `figures` |
| S5 | an own estimate passed off as the market's | The figure marked in `reference_for` and every figure beneath it (inputs and rests_on) is a source, or computed with no basis forecast. None is an estimate. At least one is a quoted consensus, guidance or third_party figure, which may be the marked figure itself. A forecast member has exactly one marked reference figure or a `reference_unavailable` reason. | `reference_for`; `reference_unavailable` |
| S6 | structure: the answer's number | A forecast member has exactly one figure marked in `outcome_for`. It is a computed or estimate figure with basis forecast (the analyst's own forecast, even when it agrees with consensus). Its `what` is the member's outcome key, its unit is USD bn, and its rung is 1 to the ladder's length. The rung's band (lower edge included, upper excluded) holds the recomputed outcome, or overlaps it for a range. | `outcome_for`; `rung` |
| S7 | structure: the calculation | Ids are unique and never equal a passage id. `inputs` name figures; `rests_on` names figures or passages. No figure uses itself. A figure has value, or low and high (low ≤ high), never both. A source has `evidence_id` and `quote_number`; a computed figure has `inputs` and `operation`; an estimate has `basis_text`. Basis forecast is never on a source. There is one answer per member. An unresolved answer has `why`, rung null, `reference_unavailable` null and no marked figure. | the field descriptions |

**[52] Operation units (stated in `operation`):**
- sum and difference: one unit in, the same out.
- product: USD bn × x → USD bn; x × x → x; % × x → %; never USD bn × %.
- ratio: same unit → x; USD bn ÷ x → USD bn.
- share(whole, percent): whole's unit.
- growth(old, new): same unit → %.
- apply_growth(base, rate %): base's unit.

## 2-old. The rules as first written (superseded by the revision above)

| # | Defect | Rule (as the request states it) | Where stated |
|---|---|---|---|
| S1 | a number misread | A source figure names its passage (`evidence_id`) and copies the number as the quote writes it (`quote_number`): with currency, scale or percent sign, or the words double, triple or twice. The figure's value equals it, in billions of dollars for money. A minus written before it makes the value negative. A qualifier written just before it (or "or more" / "or less" just after) is given in `qualifier`, and none is given when none is written. A written range gives low and high. | `kind`, `evidence_id`, `quote_number`, `qualifier`, `unit` |
| S2 | wrong arithmetic | A computed figure equals its operation's result within 0.5% (at least 0.1, or 0.05 for %). A range input gives a range: low and high, or their midpoint as value. Money is never multiplied by a percentage (use share). Arity is as `operation` states. | `operation` |
| S3 | a part above its whole | For each period the Relations line lists, the part's forecast figure is at most the whole's: each end of the part's value or range is at most the same end of the whole's. The part's outcome is at most the whole's outcome. | the family header; `outcome_for` |
| S8 | a part added into its whole; periods misadded | A sum or difference never combines the part's quantity with the whole's (Relations). When a sum's or difference's inputs are periods of one quantity written as FY2027, FY2027 Q3, FY2027 H1 or FY2027 Q1-Q3, they make up the output's period exactly (Q1 + Q2 = H1; FY − Q1-Q3 = Q4). | `operation`; `what.period`; the family header |
| S4 | two forecasts of one quarter | For each shared quantity the request lists, at most one figure has basis forecast. When a member's outcome uses that quantity, exactly one does, and every figure of that quantity the outcome uses is reached only through it (the forecast itself may be computed from guidance or consensus). | the family header; `basis` |
| S5 | an own estimate passed off as the market's | A figure marked in `reference_for` has, at any depth beneath it, no estimate and no forecast, and at least one source of basis consensus, guidance or third_party. A forecast member has exactly one marked reference figure or a `reference_unavailable` reason. | `reference_for`; `reference_unavailable` |
| S6 | structure: the answer's number | A forecast member has exactly one figure marked in `outcome_for`. Its `what` is the member's outcome key, its unit is USD bn, and its rung is 1 to the ladder's length. The rung's band (lower edge included, upper excluded) holds the outcome, or overlaps it for a range. | `outcome_for`; `rung` |
| S7 | structure: the calculation | Ids are unique. `inputs` name figures and `rests_on` names figures or passages. No figure depends on itself. A figure has value, or low and high (low ≤ high), never both. A source has `evidence_id` and `quote_number`; a computed figure has `inputs` and `operation`; an estimate has `basis_text`. Basis forecast is never on a source. There is one answer per member. An unresolved answer has `why`, no rung, no marked figure and no reference. | the field descriptions |

**Recorded for readers, never refused:**
- each estimate's assumption;
- each computed figure whose money inputs measure another population, measure or scope than its output;
- each growth applied to a base of another period;
- each source qualifier.

## 3. The wire schema, word for word (examples from no covered company, AGENTS §6)

**[52] These descriptions replace the ones in the table below:**

| Field | Description [52] |
|---|---|
| `figures` (array) | "The family's calculation. Compute each quantity and period once, as a point or a range, and use that figure wherever it is needed. Figures name each other by id; no figure may use itself." |
| `id` | "Short and unique, such as F1; never a passage id." |
| `quote_number` | "Source only: the number exactly as the quote writes it, with its currency and scale or its percent sign, and nothing else: '$4.5 billion', 'US$300 million', '$2.1bn', '40%', '-3%', 'double', 'twice'. A written range in full ('$3–4 billion', 'between $3 billion and $4 billion'), given as low and high. '$4.5 billion, plus or minus 3%' in full, given as low and high or its midpoint as value. Only US dollars." |
| `qualifier` | enum adds `near`; "Source only: the qualifier the quote writes just before the number (or 'or more' / 'or less' just after); none when there is none." |
| `operation` | "Computed only. sum(a, b, …) = a + b + … (one unit); difference(a, b) = a − b (one unit); product(a, b, …) = a × b × … (USD bn × x, x × x or % × x; never USD bn × %); ratio(a, b) = a ÷ b (same units give x; USD bn ÷ x gives USD bn); share(whole, percent) = whole × percent ÷ 100; growth(old, new) = the % change; apply_growth(base, rate %) = base × (1 + rate ÷ 100). sum and product take two or more inputs; the others exactly two. A range input gives a range: compute both extremes; you may declare the midpoint as value. The figure equals the result within 0.5% (at least 0.1, or 0.05 for %). A sum never adds a figure built on the part's quantity to one built on the whole's (the whole already includes the part); a difference may take the part from the whole only to give the rest. When its inputs are periods of one quantity, write them FY2027, FY2027 Q3, FY2027 H1 or FY2027 Q1-Q3 (or CY likewise), and they make up the output's period exactly (Q1 + Q2 = H1; FY − Q1-Q3 = Q4)." |
| `outcome_for` | "The members whose forecast this figure is: your own forecast (a computed or estimate figure with basis forecast, even when it agrees with consensus), exactly one for each member answered as a forecast, none for an unresolved one. Its what is the member's outcome key, in USD bn." |
| `reference_for` | "The members for which this figure is the market's reference. It and every figure beneath it is a source or a computed figure, never an estimate or a forecast, and at least one of them is a quoted consensus, guidance or outside figure." |
| `shape` | "forecast: a figure marked in outcome_for, a rung, and a reference (a figure marked in reference_for, or reference_unavailable). unresolved: why; rung and reference_unavailable null; no figure marked for it." |

**[52] The family header is rendered from the family's data** (no member id is fixed in code):
- "Relations: <part> is part of <whole>. For each of <compare periods> and for the outcomes, the part's lowest value may not exceed the
  whole's highest. A sum never adds the part into the whole."
- "Shared quantities: …" (unchanged list).
- "Outcome keys …, in USD bn, to be used exactly: …"
- For O: "<key>: the balance at the end of FY2027, as the FY2027 annual report publishes it."

**figures[]**

| Field | Type | Description |
|---|---|---|
| (array) | | "The family's calculation: every number an answer rests on, once. Figures name each other by id; no figure may depend on itself." |
| `id` | string | "Short and unique, such as F1." |
| `what` | object | "What the number measures. Where the request lists keys (outcome keys, shared quantities), copy them exactly." |
| `what.measure` | string | "The quantity, such as revenue or capital expenditure; never its basis." |
| `what.period` | string | "For example FY2027, FY2027 Q3, FY2027 H1, FY2027 Q1-Q3, CY2026, end of FY2027." |
| `kind` | enum source, computed, estimate | "source: a number written in a shown passage's quote; computed: one operation on other figures; estimate: your judgement, with its assumption in basis_text." |
| `basis` | enum reported, guidance, consensus, third_party, forecast | "reported: an actual; guidance: the company's outlook; consensus: analysts' average; third_party: one outside party; forecast: this family's own forecast, on a computed or estimate figure only." |
| `value` | number or null | "A point. Give value, or low and high, never both." |
| `low`, `high` | number or null | "A range, low at most high." |
| `unit` | enum USD bn, %, x | "USD bn: money in billions of US dollars ($1.2 trillion = 1200; $500 million = 0.5). %: a percentage as its number (7.5% = 7.5). x: a multiple (double = 2)." |
| `evidence_id` | enum of passage ids, or null | "Source only: the passage whose quote holds the number." |
| `quote_number` | string or null | "Source only: the number exactly as the quote writes it, with its currency, scale or percent sign and nothing else, for example '$4.5 billion', '$300 million', '40%', '-3%', 'double'; a written range ('$3–4 billion') in full, given as low and high." |
| `qualifier` | enum none, more than, over, at least, about, approximately, around, roughly, nearly, almost, up to, less than, below, under, or more, or less; or null | "Source only: the qualifier the quote writes just before the number (or 'or more' / 'or less' just after); none when there is none." |
| `inputs` | array of strings or null | "Computed only: ids of figures, never passages, in the operation's order." |
| `operation` | enum sum, difference, product, ratio, share, growth, apply_growth; or null | "Computed only. sum(a, b, …) = a + b + …; difference(a, b) = a − b; product(a, b, …) = a × b × …, never money by a percentage; ratio(a, b) = a ÷ b; share(whole, percent) = whole × percent ÷ 100; growth(old, new) = the % change from old to new; apply_growth(base, rate) = base × (1 + rate ÷ 100). difference, ratio, share, growth and apply_growth take exactly two inputs. A range input gives a range (low and high, or their midpoint as value). The figure equals the result within 0.5% (at least 0.1, or 0.05 for %). A sum or difference never combines the part's quantity with the whole's; when its inputs are periods of one quantity, they make up the output's period exactly (Q1 + Q2 = H1; FY − Q1-Q3 = Q4)." |
| `basis_text` | string or null | "Estimate only: the assumption, in words." |
| `rests_on` | array of strings or null | "Estimate only: the ids of the figures and passages it rests on." |
| `outcome_for` | array of member ids (enum) | "The members whose forecast this figure is: exactly one figure for each member answered as a forecast, none for an unresolved one. Its what is the member's outcome key, in USD bn." |
| `reference_for` | array of member ids (enum) | "The members for which this figure is the market's reference: a consensus, guidance or outside figure from a shown passage, or one computed only from such figures and reported ones. No estimate or forecast anywhere beneath it." |

**answers[]**

| Field | Description |
|---|---|
| `view_id` | (enum, unchanged) |
| `shape` | "forecast: a figure marked in outcome_for, a rung, and a reference (a figure marked in reference_for, or reference_unavailable). unresolved: why, and nothing else." |
| `rung` | "Forecast only: the rung whose band holds the outcome (a band includes its lower edge, not its upper); for a range outcome, a band it overlaps, with the reason in reasons." |
| `reference_unavailable` | "Forecast only, when no figure is marked as its reference: why." |
| `reasons`, `why`, `cites`, `pushes`, `theme_pushes` | unchanged; `why`: "Unresolved only: why the evidence cannot support a forecast." |

**The family header (user message)**
- "Relations: v8 is part of v4: for each of FY2027 Q3, FY2027 Q4, FY2027, the part's forecast figure may not exceed the whole's, and
  a sum or difference never combines the two."
- "Shared quantities, one forecast figure each, through which every figure that uses the quantity takes it: …"
- "Outcome keys (population | measure | scope | period), in USD bn, to be used exactly: …"

**The system text:** one change. "a quantity the family shares has one forecast per scenario" becomes "a quantity the family shares
has one forecast". Every other sentence is unchanged.

## 4. Build

- **New files.** `calc_small.py` holds `from_answer(data, family)` (wire to internal, with S6/S7 marker errors), `check`,
  `publish_decision`, `evaluate`, `upstream_of` and `key`, and returns `{errors, recorded, published}` as `calc_check` does.
  `render_v13.v13s_schema` builds the schema; `judging-v13s.txt` holds the system text.
- **The plan.** `paid_gate.item` takes a format. A v13s plan (`paid-plan-v13s.json`, pinned) uses `calc_small`. A plan without a
  format uses `calc_check` and `strip`, so the old run's `results.json` reproduces byte for byte on a copy.
- **Rehearsal and mutants.** The rehearsal takes the plan path. Its stub answers are written in v13s. Each rule S1–S8 gets a mutant.
- **Size.** Characters and estimated tokens for the whole request, before and after, per item. The schema is expected to be smaller
  than today's (17 figure fields against 23, shorter descriptions than v2).

**Value × reader.**
- `from_answer`'s output is read by `check`, `publish_decision`, `merge`, `card_view` and `normalise`. It uses the internal names
  those readers read (`evidence`, `inputs`, `rests_on`, `outcome`, `reference`), and the dropped keys never appear.
- `merge`'s unification of a shared forecast uses `evaluate`'s values with no bound.
- The reader brief is unchanged. Its `deciding_gap` question is where readers judge the recorded conversions and estimates.

**State × event:** unchanged from D731. A refusal is retried once, diagnostic only; the first attempt is scored.

## 5. The $0 blind test (registered; REPAIR-DESIGN.md §5 with rounds 51's fixes)

**Inputs.** Each case's archive, call, question, ladder and unit are registered, and the build refuses a heading that differs.

| Case | Archive / call | Key | Ladder edges ($bn) | Role |
|---|---|---|---|---|
| P (joint), P-v4, P-v8 (separate) | old-1 v4 8810, v8 8816 | NVIDIA revenue company FY2027; NVIDIA revenue Data Center FY2027 | 431.2/392/352.8/313.6; 400/350/300/250 | the pair; 79 quotes absent from the gate |
| S | old-3 v6 9043 | four largest AI hyperscalers, data-center capex, combined, CY2026 | 500/600/700/800 | fresh: 41 of 50 quotes absent from the gate |
| O | old-2 v29 8507 | NVIDIA equity investment commitments company end of FY2027 (the fiscal year-end balance the annual report publishes) | 25/50/75/100 | control |
| E | old-3 v41 9071 | NVIDIA revenue Vera CPU FY2028 | 50/40/30/20 | control |

**Part A, code, $0.** Each case asserts its intended rule and message. The schema's validity is checked first, so a schema error
cannot mask the rule under test.
- **A1, correct forms.** Each passes:
  - a $4.5 billion ± 3% guidance as two sources with apply_growth ends;
  - Q1 + Q2 = H1;
  - FY − Q1-Q3 = Q4;
  - a year-over-year rate on last year's quarter (recorded);
  - whole × mix through share;
  - "over $300 billion" with qualifier over;
  - "-3%";
  - "$300 million or more" with qualifier "or more";
  - $1.2 trillion as 1200 USD bn;
  - a range outcome overlapping its rung;
  - one figure marked for two members (its own family);
  - a computed external reference;
  - an unresolved member;
  - a conversion between quantities (recorded);
  - "not only still expects $20 billion" as a source;
  - 12% × 2x = 24%.
- **A2, defects.** Each is refused by its named rule:
  - **S1:** 108.5 for "$108.0 billion"; a qualifier dropped; one invented; "-3%" as 3; a number not in the quote; a passage's
    summary number; trillions as 1.2 USD bn.
  - **S2:** a plain wrong result; a wrong end of a range; division by zero; money × %; a three-input difference.
  - **S3:** a part forecast above the whole for a listed quarter; an outcome above the whole's.
  - **S8:** company + Data Center in one sum; Q2 + Q3 labelled H1; FY − Q1 labelled Q4.
  - **S4:** two forecasts of one shared quarter; an outcome reaching guidance for a shared quarter beside the forecast.
  - **S5:** a forecast beneath a reference; an estimate beneath a reference; a reported-only reference; both a marked reference and
    a reason; neither.
  - **S6:** no outcome marker; two; a marker on an unresolved member; an outcome key mismatch; a rung outside the ladder; a rung
    whose band misses the outcome; at the band's upper edge.
  - **S7:** value with low; a cycle; a dangling input; a passage id in inputs; a source with basis forecast; duplicate answers.
- **A3, Luna's observed mistakes** from both journals, each encoded in v13s. Each is impossible under the schema or refused with a
  reason the request states (the sentence is quoted):
  - prose outcome, reference and evidence;
  - unit spellings;
  - value with range;
  - a four-input difference;
  - money × % through product;
  - "first half";
  - a passage id in inputs;
  - a trillion outcome.

**[52] Additions to Part A.**
- **A1 adds:**
  - the remainder company − Data Center = the rest;
  - "US$10 billion", "$96.2bn", "roughly twice", "between $105.84 billion and $110.16 billion";
  - "$108.0 billion, plus or minus 2%" as a range and as a midpoint;
  - a point Data Center forecast beside a company range (S3 holds);
  - a final range estimate resting on a computed point of the same quantity (S4 holds).
- **A2 adds:**
  - Data Center × 1x added to company (S8);
  - an estimate resting on both part and whole (recorded, not refused, and the record asserted);
  - two Data Center Q4 figures on two paths (S4);
  - Q3 guidance used directly beside a Q3 forecast (S4);
  - an estimate itself marked as the reference (S5);
  - a computed reference with basis forecast (S5);
  - a declared value within tolerance whose recomputed value crosses the rung edge (S6 on the recomputed value);
  - a part whose recomputed lowest value exceeds the whole's recomputed highest, while its declared value does not (S3);
  - sum($108B, 2%) (S2 unit);
  - division by [-1, 1] (S2);
  - [-3, -2] × [2, 4] declared other than [-12, -4] (S2);
  - a source as the outcome (S6);
  - a figure id equal to a passage id (S7);
  - "plus or minus 2%" copied as "2%" and used as +2% for the range (S1);
  - a euro amount (S1).
- **A3:** each mistake must be refused by the schema or **actually refused** by its stated rule (asserted). "first half" is refused by
  S8 when summed. "1.05 USD trillion" fails the schema, and "1050 USD bn" passes.
- **A4, the end to end rehearsal.** One v13s reply goes through the first attempt, the separate-arm reconciliation, the card render and
  recovery. For each named defect, the defective answer fails its rule while its paired correct answer reaches the reader's card. The
  old run's `results.json` reproduces from its journals with the ledger snapshot saved inside it.

**[52] Readers.**
- **What they get.** Both readers get the same complete shown passages, with the writer's identity and the checker's decision masked.
- **What they mark, on every first reply:**
  - whether each forecast is supported, naming the passage or assumption that puts it in its band;
  - any of D737's five defects;
  - broken structure.
- **The wording review is separate.** Refusals are revealed only after that marking, for the review of whether the request states
  the rule.
- **An accepted reply with a named defect** (marked by both readers, or by the third reader) is a stop.
- **INCOMPLETE** is judged against the inventory of 12 first replies and 24 readings plus the third readings due.

**Part B, blind writers ($0 at the provider).**
- **The writers.** Each of the six cases is written once by a fresh Claude subagent and once by a fresh read-only Codex session, 12
  sessions in all. Each gets only that case's exact outgoing system text, user text and schema.
- **The first outputs** go through `model.check_schema`, `from_answer` and `check` unedited.
- **The readers.** Two readers who wrote neither the design nor the answers (a Claude subagent and a Codex session) grade **every**
  answer, accepted or refused, against the shown passages. For each answer they record:
  - for each refusal, whether the exact request states the condition (the sentence quoted) and whether the answer was right;
  - for each accepted answer, whether each forecast is supported, and whether its recorded conversions or estimates decide its band.
- **A third reader** settles disagreements.
- **Usable** means accepted, publishable by `publish_decision`, and supported by the readers. For the joint case, both forecasts must
  be supported in one reply.

**Stop.** The test stops on any of these:
- an A1 form refused;
- an A2 defect not refused by its rule;
- an A3 mistake neither impossible nor stated;
- a Part B refusal whose condition the request does not state, or that refuses a right answer;
- an INCOMPLETE run;
- a case with zero usable first replies across both writers;
- the joint case without both supported forecasts in one reply.

**A clean result** goes to Alex as the request for the paid re-send: the same 36 requests rebuilt in v13s, under a new decision with
D725's lines. Only that run measures whether luna can do it.

**[D742] Registered before the third run (council rounds 56–56c).** The re-run stopped on one S4 refusal of a sound answer
(`BLIND2-RESULT.md`). The cause was the request: the system text said to carry "the guided growth forward", while the schema allowed a
guidance rate only as "a stated benchmark for an estimate" and the header required every path to go through the forecast. S4 is
unchanged (rounds 56 and 56b showed that both a blanket and a narrowed exemption let a reset to guidance publish). The request now states
one rule in the system text, the schema and the header: guidance informs the pace; the forecast pace is recorded as an estimate that
names its benchmark in `rests_on`; the quarter's dollar value is the one forecast figure. The rules for the third run:
- **The stop lines are unchanged.**
- **The refusal review** records two judgements apart for each refusal:
  - sound: is the forecast and its reasoning financially sound?
  - stated: does the exact request (system text, schema and user text) clearly state the condition?
  A sound answer refused under a clearly stated condition still stops the run.
- **The readers' brief** keeps Alex's ruling-1 sentence and adds: "Look through any rate or multiple, including inside a stated
  assumption, for a second dollar value of the quarter."
- **Adjudication:**
  - Where the two readers disagree, two adjudicators, one per family, read the packet. The packet now includes the system text.
  - A point is settled when both agree.
  - A settled defect on an accepted reply is a stop.
  - A split is disclosed, not a stop.
- **What each outcome sends where:**
  - a fresh sound refusal sends the format back to council;
  - an accepted reply confirmed to carry two values of a quarter sends the publication rule back to council;
  - only a complete run that meets every line goes to Alex for the paid re-send.
- **Part A for the change:**
  - five new cases: the stated-estimate benchmark passes; four forms of the saved refusal or a guidance reset are refused by S4;
  - one new mutant: S4's walk following `rests_on` must fail the stated-estimate case;
  - `s4_replay.py` on the saved reply.

**[D743] The blinded re-read of the third run (Alex: "补上那条，重读一遍"; council round 57), registered before any packet is built.**
- **The one change.** The readers' brief and the adjudication header add the schema's range rule to "broken structure": for a range
  outcome, "a band it overlaps, with the reason in reasons" is not broken structure; a band the range does not reach is.
- **What is re-read.** The same 12 first replies of `judging-v13s-blind3-2026-11-22`. Writers are not re-run, and the request is
  unchanged.
- **Two blinded controls** are built from a copy of E's Claude reply. Its growth estimate becomes a range, giving an outcome of $36–43B,
  which crosses the $40B edge.
  - C-overlap names rung 3 and gives its reason. It must not be marked.
  - C-disjoint names rung 4 ($20–30B), a band the range does not reach. It must be marked broken structure.
  Controls are scored on the readers' marks, not on support.
- **Blinding.** 14 packets under a fresh shuffle (ids Q01–Q14, key in `reread-key.json` beside, never in the packets). The readers are
  fresh: one Claude subagent and one Codex session per packet. They see only their packet, never earlier votes, the key or the expected
  result.
- **Scoring:**
  - The registered stop lines apply to the 12 replies exactly as before, with adjudication where the readers disagree.
  - The repair fails if either control is read wrongly by both readers, or by the adjudication when the two readers split on it.
  - Any registered stop on the 12 replies, including S losing its only usable reply, sends the result back to council.
  - A clean re-read goes to Alex for the paid re-send, beside the third run's record and its disclosures.

**[D744] The second blinded re-read (Alex: "批准再重读一次"; council round 58), registered before any packet is built.**
- **The one change: shared rule text.** Readers get the same rule material as adjudicators, from one source (`blind_rules.py`): the
  writer's system text, every schema description, and the definitions, which allow what the format rules permit. Readers judge in two
  steps:
  1. check quotes and calculations against the format rules;
  2. name the evidence for the assumption that sets the band.
- **What is re-read.** The same 12 first replies, by fresh readers (one Claude subagent and one Codex session per packet), under a fresh
  shuffle T01–T17. The key, with answer paths, is in `reread2-key.json`, never in a packet.
- **Five controls**, each checked by the code before use (`blind_reread2.py`), with these expected readings:

  | Control | Built from | Expected reading |
  |---|---|---|
  | K-midpoint | P's Claude reply, guidance given as the midpoint 108 | no "number misread" on that figure |
  | K-misread | the same reply, guidance given as 108.5 | "number misread" on that figure |
  | K-overlap | E's Claude reply with a growth range ($36–43B) and consistent text, rung 3 with its reason | no "broken structure" |
  | K-disjoint | the same reply, rung 4 | "broken structure" |
  | K-unsupported | E's Claude reply, 140% growth that its own reasons argue against | supported = no |
- **Scoring:**
  - A control fails if both readers read it wrongly, or, when the readers split on its mark, if the adjudication does.
  - The registered stop lines apply to the 12 replies as before, with adjudication where readers disagree. The adjudication packet now
    resolves control answers through the key.
  - Any failed control or any registered stop ends the re-read, and the result goes back to council.
  - Both S replies' support votes and reasons are reported beside the verdict.
  - A clean result goes to Alex for the paid re-send.

**[D745] The targeted test (Alex: "批准针对性小测"; a justified unresolved answer counts as usable, "算合格"; council rounds 59–60), registered
before anything is sent.**
- **Request changes** (`judging-v13s.txt`; the v13 request is untouched, its plan hash is unchanged):
  - "If the chosen rung depends on a share, deduction or discount, show what in the passages supports its size or gives a bound that
    justifies the rung. If the evidence cannot support a forecast, answer unresolved and explain the gap." This replaces the former
    unresolved sentence.
  - "discounted by default" becomes "discounted subject to the evidence requirement below".
  - The qualifier list adds "estimated" (cases 111 of 111, mutants 43 of 43, rehearsal 19 of 19).
- **Readers.** Shared rule text (`blind_rules.py`), including the allowed qualifier values and the unresolved ruling. First readers'
  step 2 asks:
  - for a forecast, the evidence for the band-deciding assumption;
  - for an unresolved answer, the gap left after the strongest passages.
  Adjudicators get the same definitions.
- **Scope** (`blind4.py`; run folder `poc/data/judging-v13s-blind4-2026-11-23/`):
  - cases S, E and P-v8;
  - 6 unedited first replies (a fresh Claude subagent and a fresh read-only Codex session per case);
  - 9 blinded packets (6 replies + 3 controls), each read by one Claude and one Codex reader: 18 first readings, plus adjudication
    where they disagree.
- **Controls**, each checked by the code before use:

  | Control | Built from | Expected reading |
  |---|---|---|
  | K-unsupported | the saved third-run E Codex reply, with an unsized 15% cut | not supported |
  | K-unresolved-unjustified | P-v8 Claude made unresolved with a vague reason | not supported |
  | K-unresolved-justified | S made unresolved with the specific gap | supported |
- **Pass:**
  - every S and E reply has a settled "yes" on its forecast or on its reason for leaving the answer unresolved;
  - both P-v8 replies have a settled "yes" on a forecast;
  - all three controls read as expected;
  - the refusal and defect stop lines hold as before.
- **Otherwise:**
  - a support split that adjudication does not settle leaves the run inconclusive, and it goes back to council;
  - any failure goes back to council;
  - a clean result supports asking Alex to authorize the 36-request paid re-send.

**[D747] The re-read under Alex's comparison ruling (Alex: "可以发布，要讲清楚"; council rounds 61–61b), registered before any packet is
built.**
- **The one change.** The shared definitions (`blind_rules.py`, "supported") add Alex's ruling. The band-deciding assumption must
  rest on the passages in one of three ways:
  - its size;
  - a bound that justifies the rung;
  - or, when the passages do not give the asked quantity, a related figure that the answer explains.

  An explained related figure satisfies this even though the other side of the line remains possible. It is explained when the answer
  says why the comparison applies to the companies, the period and the quantity asked, and why, under the answer's own stated
  assumptions, the chosen side of the line is more likely. An answer that does not explain this is not supported.
  - The first readers' step 2 asks, for a forecast, whether the passages support the deciding assumption's size or a bound, or whether
    the answer explains a related figure as the definitions require.
  - Adjudicators get the same definitions.
  - The requests and the answers are unchanged. Each packet carries its writer's own request.
- **What is re-read.** Nine stored answers under a fresh shuffle, W01–W09 (`blind4.py reread`). The key is in `reread-key.json`
  beside, never in a packet.

  | Answer | Expected reading |
  |---|---|
  | blind4 U01: P-v8, vague unresolved control | not supported |
  | blind4 U02: S Claude, 98% share. It calls "more than $730B" a floor for data-center spending, then forecasts $705.6B of data-center spending on $720B of total spending, so its own assumptions cannot all hold (council 62) | not supported |
  | blind4 U03: E, unsized 15% cut control | not supported |
  | blind4 U05: E Codex, unsized 10% cut | not supported |
  | blind3 T15: E Claude, a bracket between the market pace and the guidance, with Vera as all CPU revenue | supported |
  | blind4 U08 (S Codex, $25B deduction) and U04 (S justified unresolved); blind3 T10 (S Claude, read for its spending argument only: its settled quotation error stands, and its defect marks are not scored); blind4 U06 (E Claude, 1.8x with a 90% Vera share, judged with its own share) | must settle either way: both first readers agree, or both adjudicators do |
- **Changes from council round 62** (`codex-r62.md`), made before any packet was built:
  - The definition says outright that an explained related figure satisfies the support requirement, even though the other side of
    the line stays possible. Readers and adjudicators get the same words.
  - Each packet carries the request its answer was written for. U03, T10 and T15 get the third run's request. The constructed
    controls U01 and U04 are read under the request they were built for.
  - The qualifier list shown comes from each packet's own schema, so the third run's packets do not list "estimated".
  - All nine answers are shown in one layout, parsed and printed with one indent, so a control cannot be told apart by its layout.
  - The tally refuses a key that is not exactly the nine answers, or a reading without a valid vote. A settled vote is final only
    after Claude records its two reasons as compatible and applying Alex's rule (`reread-reasons.json`).
    - Matching votes whose reasons are incompatible go to adjudication.
    - An adjudicated agreement with incompatible reasons is a split.
    - A "yes" on U06 that rests on the whole range staying at $30B or more does not apply the rule, since $20B × 1.5 × 90% = $27B.
  - Checked on a scratch copy:
    - without recorded reasons, the tally gives no verdict;
    - with incompatible reasons, it asks for adjudication;
    - with compatible reasons, it passes;
    - a fixed "no" read as yes fails.
- **Readers.** Fresh readers: one Claude subagent and one read-only Codex session per packet. Where they disagree, two adjudicators
  read the packet, one per family.
- **Scoring** (`blind4.py reread-tally`):
  - It passes when the five fixed readings come out as expected and the four others settle.
  - Matching votes whose stated reasons contradict each other on the comparison are recorded as unsettled. Claude reads them by hand.
  - A settled defect on a writer's reply other than T10 is a stop.
- **What the result decides:**
  - Pass: the reading standard under D747 is settled. The next step is the E writer repair, with the council before any send, then a
    $0 writer test, then Alex for the paid re-send.
  - A split: Alex's words do not yet fix the reading. The split answers go back to the council, and to Alex as boundary cases.
  - A failed fixed reading goes back to the council.
  - A clean re-read does not turn D745 into a pass.

**[D749] The $0 writer test of the E writer repair (Alex: "批准修写手再小测"; council round 63), registered before any writer is
sent.**
- **The request change** (`judging-v13s.txt`; the D745 text is kept in `judging-v13s-d745.txt`; the registered file's sha256 is
  `ac707fa9…`, checked by `blind5.py build` against every built system text). This is the wording after council round 64
  (`codex-r64.md`).
  - The last bullet's two D745 sentences are replaced by: "Before sizing a share, deduction, discount or pace that decides the band,
    explain which band the evidence favours. Show support for the size or a justifying bound. If the passages lack the quantity asked,
    explain why a related figure fits the companies, period and quantity, and why your assumptions favour that band. If you can say
    only that the outcome might fall short or overshoot, not which band is more likely, answer unresolved and name what is unknown."
  - Bullet 3's "is an input to be discounted for time and execution (…), not an answer" becomes "is an input, not an answer: weigh
    time and execution (…) under the evidence requirement below". Council 64 found that the old imperative invited the old order
    (discount first) on E.
  - Sources:
    - D745: show the support (council 64: "give its size" was narrower than D745, so "show support for the size");
    - D747: an explained related figure counts, only when the passages lack the quantity asked (council 64: the first wording was
      wider);
    - D749: decide the band before sizing, else unresolved, naming the unknown;
    - D745's ruling: a justified unresolved answer is usable.
  - Size: 4,540 → 4,794 characters, 910 → 961 tokens (o200k_base). The writer's request now carries the same routes the readers judge
    by, and the decision order Alex approved.
  - Checks at $0: cases 111 of 111, rehearsal 19 of 19, and the pinned v13 plan unchanged (`paid-plan.sha256`). The schema and the code
    are unchanged.
- **Scope** (`blind5.py`; run folder `poc/data/judging-v13s-blind5-2026-11-23/`):
  - cases S, E and P-v8, built from the repaired request;
  - one fresh Claude subagent and one fresh read-only Codex session per case, 6 writers, each reading only `system.txt`, `user.txt` and
    `schema.json`.
- **Readers.** 8 blinded packets, shuffled X01–X08, with the key in `reader-key.json`:
  - the 6 fresh replies;
  - 2 controls carried unchanged from the targeted test, each shown with the request it was written for;
  - each packet read by one fresh Claude and one fresh Codex reader under the D747 definitions.

  Where they disagree, on support or on any defect, two adjudicators read the packet, one per family. The reasons behind every
  settled vote are recorded by Claude as compatible or not (`reasons.json`). Matching votes with incompatible reasons go to
  adjudication.

  | Control | Built from | Expected reading |
  |---|---|---|
  | K-invented-cut | blind4 U05, E Codex: 90% of $40B with no order size or shipment pace | not supported |
  | K-impossible-floor | blind4 U02, S Claude: "more than $730B" called a floor above its own $720B total | "part above or added into its whole" on F12, settled; its support is not scored |
- **Pass:**
  - every fresh S and E reply has a settled yes, on its forecast or on its unresolved reason;
  - both fresh P-v8 replies have a settled yes on a forecast;
  - every fresh reply is accepted and publishable by the code;
  - no settled defect on a fresh reply;
  - both controls read as expected.
- **Otherwise (tally rules after council 64):**
  - **Fail:**
    - a fresh reply refused or held by the code (decided before any reading; an unreadable reply builds no packet);
    - a fresh P-v8 reply that is not a forecast (decided from its shape alone);
    - a settled no on a fresh reply;
    - a settled defect on a fresh reply;
    - K-invented-cut not settled no;
    - the floor defect marked by neither reader, or rejected by both adjudicators.
  - **Inconclusive:** a support split, a defect split on a fresh reply, or a floor split left after adjudication.
  - **The floor control** is matched on its type and on naming F12, at both stages, so readers who list the other figures differently
    still agree. Adjudicator votes are validated like first votes.
  - Either outcome goes back to the council, and the paid re-send stays on hold.
  - Only a clean pass supports asking Alex to authorize the paid re-send.
- **Checked on a scratch copy before the send** (the targeted test's six replies stood in as fresh replies):
  - a clean set passes, with the floor marked by readers who listed its figures differently;
  - a fresh defect marked by one reader waits for adjudication;
  - a fresh defect still split after adjudication is inconclusive;
  - the invented-cut control read as supported fails;
  - the floor missed by both readers fails;
  - a fresh P-v8 answered unresolved fails;
  - a fresh reply that is not JSON fails before any reading.
- **Known limits, disclosed now:**
  - Readers split on boundary answers (D748). A fresh answer on a boundary can leave the run inconclusive even when the repair works.
  - All four fresh E and S replies may pass as justified "unresolved". A pass therefore shows the repair stops invented sizes. It
    does not show how often the writer withholds on boundary cases (council 64).

**[D750] The second $0 writer test (council round 65; under D439 while Alex is away), registered before any writer is sent.**
- **Why.** The D749 test was INCONCLUSIVE, with no failed line (`BLIND5-RESULT.md`).
  - X05, E Claude, took a not-yet-shipping target in full, asserting "already selling at volume". None of E's 15 passages shows
    shipments, revenue to date or orders.
  - X08, S Claude: its readers disagreed on whether "more than $730B" of AI infrastructure is a floor above its own $710.4B outcome.
- **The request change** (`judging-v13s.txt`; the D749 text is kept in `judging-v13s-d749.txt`; the registered sha256 `54f5847d…` is
  checked by `blind6.py build` against every built system text). Bullet 2's "it is taken in full only when the evidence shows the
  volume in hand" becomes "it remains a forecast when reaffirmed, and is taken in full only when you show what evidence puts the
  required volume in hand for the period".
  - This is council 65's wording. Claude's closed list was rejected: an order with a date can cover one unit, and a list would
    exclude the request's own disclosed-comparable route and D747's explained comparison.
  - Size: 4,794 → 4,867 characters, 961 → 975 tokens.
  - Checks: cases 111 of 111, rehearsal 19 of 19, and the pinned v13 plan unchanged.
- **Design.** D749's, unchanged (`blind6.py` wraps `blind5.py`), on a new run folder, `poc/data/judging-v13s-blind6-2026-11-23/`:
  - S, E and P-v8, each with one fresh Claude and one fresh read-only Codex writer;
  - the same two reader controls (K-invented-cut, K-impossible-floor);
  - fresh readers of both families, with adjudication where they disagree;
  - the same pass, fail and inconclusive lines.
- **One added reading rule** for the reasons record (council 65), applied by Claude before any vote counts as settled. On S, a reader
  citing a related figure as a floor above the answer's own outcome is not compatible with a reader treating it as a guide. Such a
  pair goes to adjudication.
- **What the result decides:**
  - a clean pass supports asking Alex to authorize the paid re-send;
  - a settled unsupported answer or defect fails;
  - a persistent split stays inconclusive and goes back to the council.
- **Changes from council round 66** (`codex-r66.md`), made before any writer was sent. The writer sentence is kept. The tally in
  `blind5.py`, shared by `blind6.py`, gains three changes:
  - **The decisive premise.** For a fresh S or E reply, a settled yes needs the reasons record to name the decisive premise and what
    in the passages supports it, in a `premise` field (`adjudicated_premise` after adjudication).
    - On E: what puts the volume in hand for the period, when the writer takes the target in full.
    - On S: how the writer's use of a related figure fits its own dollar outcome.
    - Two readers agreeing on an unsupported premise, such as both reading a floor above the outcome, go to adjudication. If both
      final approvals still rest on it, the support stays unsettled.
  - **K-invented-cut** fails on a split too, as registered: it must earn a settled no.
  - **A defect an adjudicator leaves undecided** is pending, not a split.
  - Checked on a scratch copy: no recorded premise gives no verdict; with premises it passes; a split invented-cut control fails; an
    omitted floor decision waits.
  - D749's `TALLY.json` stands as scored under its own registration. Re-running it under the new rules would ask for premise records
    it was not registered to need.

**[D751] The last $0 writer test of this wording loop (council rounds 67–68; under D439 while Alex is away), registered before any
writer is sent.**
- **Why.** D750 FAILED on one settled line (`BLIND6-RESULT.md`). E's Claude writer bracketed the pace between the market pace and a
  "more than double" it treated as a ceiling, and took the midpoint.
  - Across four runs that writer forecast $37B, $32.4B, $42B and $35B, each by a new route, none settled supported.
  - Council 67's structural reading: an unknown fact decides the side of the line. Is the FY2028 volume in hand? The writers asserted
    it one way ($42B) or the other ($35B).
  - The writer's own account named the bullet-2 and bullet-3 discount sentences and "not established … never a reason to stay".
- **The request change** (`judging-v13s.txt`; the D750 text is kept in `judging-v13s-d750.txt`; the registered sha256 `080a0012…` is
  checked by `blind7.py build`). In line 9, "Before sizing a share, deduction, discount or pace that decides the band, explain which
  band the evidence favours." becomes "When other evidence bears on the forecast, weigh the plausible alternatives for any unknown
  fact that decides the band. Explain whether the evidence as a whole favours one band before deciding whether or how much to adjust."
  - The size, bound, explained-comparison and unresolved routes are unchanged.
  - Size: 4,867 → 4,976 characters, 975 → 993 tokens.
  - Checks: cases 111 of 111, rehearsal 19 of 19, the pinned v13 plan unchanged.
- **The paper check before the change** (`PAPER-CHECK-D751.md`, verified row by row by council 68):
  - it exposes the $42B and $35B premises;
  - it preserves both specific "can't tell" answers;
  - it leaves the $37B answer a boundary case;
  - the explained near-cutoff S forecasts stand.
  - Council 68 replaced "across the plausible readings" with "weigh the plausible alternatives … whether the evidence as a whole favours
    one band". The first wording could read as requiring a forecast to survive every reading, which is stricter than D747.
- **Design and tally.** D750's, unchanged (`blind7.py` wraps `blind5.py`), on a new run folder,
  `poc/data/judging-v13s-blind7-2026-11-23/`:
  - S, E and P-v8, each with one fresh Claude and one fresh read-only Codex writer;
  - the same two controls, each with its original request;
  - fresh readers of both families, with adjudication where they disagree;
  - the decisive premise and its passage support recorded for every settled S and E vote (council 66).
- **Exit rule (council 67):**
  - a clean pass goes to Alex for the paid authorization;
  - a settled failure or a persistent split ends this wording loop, and the publication choice for E-type cases returns to Alex.

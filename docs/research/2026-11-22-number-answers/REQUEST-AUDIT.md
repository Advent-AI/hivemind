# judging-v13 request audit (DESIGN.md §5; $0)

The system text is `judging-v13-draft.txt`: 4,835 characters, against judging-v7's 4,924 (−89). The format definitions sit in the schema
descriptions beside their fields (AGENTS §3, §6), not in the system text.

## The system text, sentence by sentence against judging-v7

| v7 sentence | v13 | Source |
|---|---|---|
| L1 "judging a thesis's current rung … Use only the supplied evidence, dependency conclusions and themes" | "the current rungs of a family of related number theses …"; dependency conclusions removed | D725 (the unit is a family); the family has no dependency reads |
| L3 "the current conclusions of dependencies" | removed | the same |
| L3 "Pieces in force … are not shown; the previous conclusion carries them" | "each member's earlier forecast reflects them, but its figures are our own, never a source and never the market's expectation" | D198 kept; the self-made reference (D693 trace, `self-reference/RESULT.md`); C5 |
| L3 "Do not add to or subtract from the previous score. The previous conclusion is supplied only for comparison." | kept, per member | D260 |
| L4 reference, run-rate, shifts, product-target discount | kept word for word, per member | D260, D263 (the frozen gold's reasoning) |
| L4 "State the implied figure or date, check it against the dependencies' conclusions shown (a part cannot exceed its whole, and a figure that spans several periods or products gives this question only its share)" | "Build the family's figures once and read every member's outcome from them: a part cannot exceed its whole, a figure that spans several periods or products gives a question only its share, and a quantity the family shares has one forecast per scenario" | D260 clause (3), made family-wide; C3, C4 |
| L5 tiers, novelty, discounting, sizing, identities | kept word for word | D260, D263 |
| L6 replacement | kept | D198 |
| L7 themes | kept, per member | D191, D195 |
| L8 dependencies "not yet created" or "historical only" | removed | a family has no dependency reads (`cites_views` always empty) |
| L9 consistency with dependencies and themes; "a component cannot exceed its whole" | "consistent with each other and with the themes in force"; the component clause moved into L4's family sentence | D260; the duplicate removed (AGENTS §6) |
| L10 the output list (one rung, reference, implied_outcome …) | "Return the family's figures and one answer per member, as the JSON schema defines them. Every number an answer rests on is a figure; a number you judge … is an estimate, stated as yours. When the evidence cannot support a member's forecast, answer it unresolved …" | D725, DESIGN §2; field definitions moved to the schema |
| L11 changed | kept | PRD 06 |

**Read in both directions** (AGENTS §6):
- No v13 sentence keeps wider or narrower than v7 on the standard.
- The only new rules are the three D725 contracts: one calculation, figures labelled, and unresolved allowed. Code enforces each.
- The product-target sentence ("discounted by default") is kept. D721 and Codex's round 43 found that the gold relies on it (q19).

## The schema descriptions (the format's definitions, beside their fields)

- **`figures[].what`:** "What the number measures: population, measure (the quantity, such as revenue; never its basis), scope, period."
- **`figures[].basis`:**
  - reported: an actual;
  - guidance: the company's outlook;
  - consensus: analysts' average;
  - third_party: one outside party;
  - forecast: this family's forecast;
  - prior_forecast: our earlier forecast, with its pointer.
- **`figures[].kind`:**
  - source: stated in a shown passage;
  - computed: one operation on named figures;
  - estimate: your judgement.
- **`figures[].expression`, source only:** "the complete numeric expression exactly as the passage writes it, qualifiers included (for
  example 'more than $2 billion', '$4.5 billion, plus or minus 3%', 'more than triple')". The examples come from no gate case [46f.4].
- **`figures[].relation`, sum and roll_forward:**
  - time_aggregation: periods of one quantity;
  - accounting_parts: declared parts of a whole;
  - stated_in_addition: a source says the amounts add;
  - overlap_unknown: name the disputed figure.
- **`figures[].bridge`:** "Only when no listed identity covers the operation (periods of one quantity, declared parts, a balance and its
  flows, a stated share or multiplier, a total over a per-unit price): an estimate stating the conversion and listing the operands it
  converts." This matches C8's operation-specific rules, so q01's quarters-to-half and q02's mix applied to consensus need none [46f.4].
- **`figures[].adjusts`, estimate only:** "The stated figure this estimate changes, and how: discount, uplift or trim."
- **`answers[]`:**
  - **forecast:** the outcome figure, and the rung whose band contains it or, for a range spanning several bands, the band you choose,
    with the reason. The reference is an external figure, or a calculation from external and reported figures, or `unavailable` with
    why. It is never our earlier forecast.
  - **unresolved:** why.

## The family header (user message, before the evidence)

`[Family] members: <id> (<question>, ladder …) …`, then:
- `Relations: <part> is part of <whole>; <later> rests on <earlier>'s base.`
- `Shared quantities, one forecast each per scenario: <population, measure, scope, period> …`

The family header, the members' earlier forecasts (labelled "our earlier forecast, not a source") and the union of evidence in view
follow the order of v7's request.

## Earlier forecasts (D728, superseding the note below)

The calculation request shows no earlier forecast. The draft's first bullet now reads: judge every member from the evidence shown and
the themes in force, "as if for the first time. Earlier forecasts are not shown: whether a conclusion changed is compared afterwards."
The `changed` bullet and the answer fields `changed` and `why_changed` are removed, and code derives them. The schema offers no `prior`
kind, no `prior_forecast` basis and no pointer. The system text is 4,373 characters.

## Earlier forecasts [46f.4]

The draft says the earlier forecasts are "supplied only for comparison", and C10 makes that a check: a `prior` figure feeds no figure.
The design's earlier clause allowing a dated prior to feed a `same_base` is withdrawn. A later year reads the earlier member's forecast
node in the same call (C9).

## Rendered and checked (`render_v13.py`, `render-r1.*`)

- **The request:** the old-2 family on 09-20 (calls 8729 and 8737). System text 4,835 characters; user message 123,304 characters, with
  237 evidence items, the family header, the themes once and the earlier forecasts labelled; schema 10,066 characters.
- **The answer:** the R1c control answer, in strict shape (every optional field null). It passes `model.check_schema` with no error and
  calc_check with no error. Every passage it cites is in the rendered request.
- **Tokens:** not counted here. The two v7 calls were 36,151 input tokens together (Codex, round 45b).

## Not yet done

- The product request builder (the harness renderer above is not it).
- The sender for the paid gate.

Both are build work after the $0 gate.

# D258: each adopted thesis offers only its own two endpoints

Alex's Idea "I think Nvidia datacenter revenue will outperform next quarter; geopolitics alleviation will be a tailwind"
returned `502: SchemaError: $.composite.v10.kind: 'driver' not in ['excluded']`. The service was running; the final
assessment answer was refused after it had been archived as valid.

## Diagnosis

**Class.** Every stored `idea-summary-v7` answer (12 unique requests across the preserved Idea archives, 38 entries) was
replayed through the current binder at no cost. Two answers are refused, both for the same reason: an entry whose
`raises_outcome_position` is not one of that thesis's two supplied endpoints (v10 → `2` on 2026-10-30; v3 and v9 →
`2` on 2026-10-26). Each of those theses has endpoints 1 and 5.

**Mechanism.** D188 made the final call copy the position of one of the two supplied endpoint conditions, and v5/v6
enforced that per thesis: one keyed property per thesis, each with an enum of exactly its endpoints. D196 changed the
answer to a variable-length array. The array item cannot vary by thesis, so `positive_schema` offers `1`–`5` to
every thesis, while the binder converts the answer into the v6 keyed shape and re-checks it against `endpoint_schema`,
which keeps the per-thesis enum. The request allows a value the check refuses (AGENTS §6). The error text is
misleading because `model.check_schema` reports only the last `anyOf` option (the v6 exclusion branch, which v7 does
not have).

**The model's own account** (stored conversations continued, $0.00105 for two probes,
`position-probe-2026-10-30.json` in the session scratchpad): for v10, "I used v10's `judged.position` value of `2` …
For v10, the increasing position is `1`". For v3/v9 it "treated each thesis's bullish judgment as the position that
raises the Idea's outcome". The payload shows each thesis's current state as a position (and the judge's reasons say
"Rung 2 remains the best estimate"); the answer field asks for a position from 1–5. The model answers "where the
thesis is / which step is bullish" instead of "which of the two shown ends raises the outcome".

**Silent half.** When the current state is itself an endpoint, a copied state passes the check. All 35 in-range
entries were read beside their own reasons: every chosen end agrees with its reason; six equal the current state and
all six are the correct direction. No stored answer carries a hidden wrong sign.

**Share.** A per-thesis closed set removes all three refused entries' class: under strict structured output an
off-endpoint value cannot be generated. Removing `judged.position` from the payload would not (the reasons text still
names rung numbers), and a prompt sentence would only lower its frequency.

## Contract

- New config `poc-v33-idea`, prompt `idea-summary-v8` (text identical to v7). Candidate discovery, the final call's
  payload, model and settings are unchanged; only the response schema and its binder change.
- `adoption_schema(theses)`: `composite` is an array whose item is `anyOf` one object per candidate thesis. Each
  object pins `thesis_id` to that thesis and `raises_outcome_position` to that thesis's two endpoint positions, with
  the v7 fields otherwise unchanged. With no candidates the item keeps the v7 shape and only an empty list can bind.
- `bind_adoption` checks the answer against the same schema object that was sent, then only what a schema cannot
  express: a named outcome, no scored entries for an unclear claim, each thesis at most once, non-empty label, reason
  and weight reason, and weights totalling 100 for a nonempty list. It converts the endpoint to first/last, inverts
  once for a lower claim, and binds question and date. Output: `idea-composite/4`, identical to v7's for a valid
  answer. v3–v7 keep their binders so old configurations replay unchanged.
- `model.check_schema` reports the errors of the closest `anyOf` option (fewest errors; ties listed together).

## State × event

| State / event | Result |
|---|---|
| Final call, valid answer | Same plan as v7 would bind; archived under the exact request |
| Off-endpoint, foreign or unknown ID | Not generable under strict output; if a transport returns it, `model.call` refuses it with the closest option's error and archives it as refused |
| Duplicate thesis, bad total, empty text, unclear claim with entries | Binder refuses with its own reason (unchanged from v7) |
| No candidates | v7 item shape; only an empty list binds |
| Old v7 archive / config | v7 contract and binder unchanged; old requests replay |
| Same idea resubmitted after a v7 refusal | v8 request bytes differ (schema), so the refused v7 answer is not reused |
| Replay, range change, detail reopen | Unchanged: the plan is fixed per response |

## Value × reader

| Value | Writer | Readers |
|---|---|---|
| Request schema | `adoption_schema` | Model (strict), `model.call`'s answer check, `bind_adoption` |
| `idea-composite/4` plan | `bind_adoption` | `idea.read_idea` adoption projection, API, `prepareIdeaComposite` (unchanged shape) |
| Default config | `scripts/hivemind_api.py`, `docker-compose.yml` | Service; README and `docs/poc/idea-card.md` name it |

## New path × old checks

| Old check (v7 chain) | v8 |
|---|---|
| Schema of the sent request | Same object checked in `model.call` and the binder |
| Endpoint per thesis (`endpoint_schema`) | In the sent schema |
| Outcome named; unclear claim has no drivers (`bind_outcome`) | `bind_adoption` |
| Weight 1–100, total 100 (`bind_weighted`) | Range in schema; total in `bind_adoption` |
| Unique, known, non-empty (`bind`) | ID by schema; uniqueness and text in `bind_adoption` |
| Lower-claim inversion once | `bind_adoption` |
| English prose check | `positive_prose`, unchanged |

## Prior decisions

D188 ("representatives copy the explicit position of one supplied endpoint"; "Code validates the partition,
identities, endpoint enum"), D194 (endpoint fields unchanged), D196 ("Code checks IDs, uniqueness, endpoint validity,
positive weights and a 100 total"). None bounds a per-thesis enum; D188's v5/v6 had one. This restores that guarantee
inside D196's array.

## Second defect on the same path: two-rung display scores

`adapters/bundle.js` gives a two-rung thesis the scores `Yes`, `No` by position, ignoring its labels, and
`model/contract.js` requires that order. In the served ledger 11 of 55 two-rung theses have `No` as rung 1 (8 theme,
3 asset), so their chips show the opposite word and pill style: v14's state "Yes" renders as "No" in the white pill used for
negative states. The Idea number is
unaffected (state score and direction share the same position-based score), but the card contradicts the Idea.

Fix: when a two-rung thesis's labels are exactly Yes and No, each rung's score is its own label; other two-rung labels
keep the existing order. The contract accepts either order; `laneOf` places `Yes` on the upper lane for every two-rung
thesis. `prepareIdeaComposite` derives direction from the first rung's score sign, so the composite is unchanged.

## Verification

- $0: the ten valid stored v7 answers bind to equal plans through `bind_adoption`; the v8 schema refuses `2` for a
  1/5 thesis and accepts 1 and 5; mutant: a shared 1–5 enum fails the test. UI: a real two-rung thesis turned into
  No-first shows its own label, passes the contract and yields the same composite value; the old adapter fails it.
- Paid: the two refused requests rebuilt through `read_idea` under v33 (first two calls served from the archive),
  three draws each; every entry must be an endpoint whose direction agrees with its own reason.

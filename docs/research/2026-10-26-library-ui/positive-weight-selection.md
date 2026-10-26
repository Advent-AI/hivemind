# D196: positive-weight selection is the Idea association

The final Idea response is the model's adopted thesis list, not its input candidate list. Each adopted thesis must have a positive impact percentage, and nonempty lists total 100. The model chooses how many. There is no 0%-weight thesis in the Idea.

## Cause and proof

The three stored v6 answers all contain zero-weight exclusions, five entries in total. The schema requires every candidate to be either a driver or excluded; `reading.chosen` and `related` are built before that decision and remain unchanged. Thus the graph faithfully renders a larger candidate set than the score uses. The live example has three cards but only two weighted theses. A stored-input proof must retain v3/v1 at 60/40, remove v9 from the final associations and bundles, and preserve the +0.40 score.

## Contract

New config `poc-v32-idea` and prompt `idea-summary-v7` retain the same three-call flow and model settings. Candidate discovery is unchanged. The last call receives candidate assessments and returns a variable-length `composite` array of chosen thesis IDs, endpoint positions, positive integer weights and explanations. It has no exclusion field. Code checks IDs, uniqueness, endpoint validity, positive weights and a 100 total (or empty list with no score), then binds canonical questions and date into `idea-composite/4`.

`reading.chosen` equals the returned driver IDs. Part association lists retain only those IDs. An evaluation whose direct thesis was not adopted becomes unavailable; no dangling claim is returned. No automatic related theses are appended. Bundles contain exactly the adopted set. Retrieval candidates and prior mapping explanations remain search trace context, never additional associations. Old configurations retain their original response behavior.

## State × event

| State/event | Outcome |
|---|---|
| Candidate discovery succeeds | Candidate set only; not final associations |
| Final response returns positive subset | Bind adopted IDs, filter association lists, bundle/draw/calculate the same set at request as_of |
| Zero/negative weight, invalid total, duplicate/unknown ID or invalid endpoint | Refuse; no repaired or hidden association |
| Empty adopted set | No associated theses, related cards or score; discovery trace remains |
| A claim's direct thesis is omitted | Clear dependent claim/evaluation; no unrelated evaluation |
| Model or transport failure, cancellation, stale concurrent response | Existing failure/request-ownership handling; no partial adopted set |
| Replay/range/detail reopen | Same adopted set and weights; dated states only, no model call |
| Missing historical assessment | Existing weighted unavailable-value rule; never reallocate weight |
| Changed idea/day/config, later request or crash/replay | Existing exact-request archive semantics; no mutation of prior answers |
| Legacy response | Old version-specific adapter behavior |

## Value × writer × reader

| Value | Owner/input | Readers |
|---|---|---|
| Positive selection and weights | Final model, constrained by candidate IDs and code validation | Canonical plan, final chosen list, graph, calculation, explanation |
| Final part associations and numeric claim | Code projects prior mapping/evaluation onto adopted IDs | API caller, analysis, bundle IDs |
| Candidate lists | Existing discovery | Search trace only |
| Canonical questions, as_of and version | Code and ledger | API/UI validation and archive replay |
| Score | Existing weighted calculator over adopted IDs | Idea chart and contribution table |

## New path × existing checks

Keep source identity, schema/English checks, direction inversion, dates, cancellation, immutable archives and weighted arithmetic. Replace complete-candidate-partition validation with unique positive-subset validation. Add an end-to-end real-storage test proving an omitted candidate has no card, bundle, part association, related link or orphan claim. Frontend validation must reject a chosen/driver mismatch and zero weight. Legacy tests retain their contracts.

Before live calls run preflight and replay old Idea answers under their original contracts; old zero-weight answers do not become valid v4 answers. Compare three fresh v6 controls with three new v7 calls on the stored current context, first pair before continuing. Keep the same $0.035 allocation ceiling, including the prior $0.002993 known charge. Record every response and do not tune to a preferred count/weight. A 60/40 stored fixture proves arithmetic and projection, not desired model allocation. Final browser verification reads the real endpoint and confirms that returned weights, associations and visible cards match exactly. No source database mutation, extra model call, scoring-rule change or fixed count.

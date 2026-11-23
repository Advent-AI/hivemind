# Round 49, Claude's reflection after Codex's design review (written before round 50)

## What round 49 showed

- **The repair is not bounded.** Codex walked all 58 refusal templates in `calc_check.py` (893 lines). Rules for C1 through C10 are
  still unstated after the repair as designed: the component choice by form; C2's tolerance and bound direction; C3's
  compare_periods; C4's path-through-the-forecast-node rule; C5's reference graph; C6's overlap semantics; C7's arity limits; C8's
  operand rules per operation; C9's dependence test.
- **Two of my four check changes are unsound.**
  - The "vs" growth label lets the answer supply its own proof. A 12% sequential rate relabelled as year over year passes.
  - The containment rule lets "not be over $300 billion" pass as "> $300B", and "-12%" pass as "+12%".
- **My test inputs were wrong.** old-2 v41 is a Fed question, and S is CY2026, not CY2027. The pair and O reuse almost all of the
  gate's evidence.
- **Part B could "pass" with zero usable answers.** All-unresolved answers pass every check.

## The pattern (AGENTS §1, §7.3: "When one mechanism draws findings round after round, stop answering findings: propose one structural rule")

- The contract grew over 30 design rounds (46 to 46ad) and the 8 harness rounds. Most of its rules came from answering one gate
  fixture's finding at a time: R1 to R4, G1 to G4, the relabel and route variants. `calc_check.py` carries 29 council-tagged rules.
- Each rule is identity or arithmetic, as D725 asked. Together, though, they form a 58-way conjunction over about 20 figures per
  answer.
- **The rules were never written for the model.** The $0 gate tested them only against answers written by someone who knew them.
- **Stating every rule** would turn the schema into a manual. It would also not change the conjunction: luna (medium effort, one pass)
  must satisfy all of them at once. Round 48's reflection already warned that a long conjunction fails by chance even when each part
  is usually right.
- **What this means for D734's hypothesis.** The hypothesis was that "a bounded repair (descriptions, enums and four check fixes)
  makes the format statable". Round 49 contradicts it. By D355, the line stops and goes back to Alex.

## What still serves D725's goal

D725's diagnosis was three things:
- related questions have no shared, checked calculation;
- a prose answer cannot be checked;
- each question is judged alone, on split inputs.

The goal is that the numbers a member publishes are consistent with each other and with the passages. These checks carry that goal
directly:
1. A source number appears in the cited quote.
2. Arithmetic is right.
3. A part's outcome does not exceed its whole's.
4. A shared quarter has one forecast that both members use.
5. A rung contains its outcome.
6. A reference is not the system's own estimate.

The rest are refinements: typed relations, bridges and `converts`, roll-forward formats, per-unit identities, scenario membership
along paths, C9's perturbation test and the exact-expression grammar. Each was added to stop a case a reviewer constructed.
Arguably they are better shown to the readers as recorded assumptions than enforced as refusals: the design already records
overlaps, adjustments and bridges for readers, not refusals.

## Options for Alex (my lean, to be challenged in round 50)

- **(A) Continue the full repair.** State all 58 rules and fix the unsound changes, which means several more council rounds. The risk
  stays that luna cannot meet the conjunction even when every rule is stated.
- **(B) Shrink the format to the core six checks** (above), with a short schema that states each one. The other structure is kept as
  recorded assumptions for the readers, never as refusals. Then rebuild the $0 gate and the blind test on the smaller format.
  - This is a new design step inside judging-v13, not a wording fix.
  - It would be measured by the same 36-request gate, with D725's lines unchanged.
- **(C) Close judging-v13.** poc-v118 stays the product, and the number answers stay a known defect.

My lean is (B). It is the structural rule: enforce only what the goal needs, state every enforced rule beside its field, and show the
rest to readers. What would refute it: the six checks cannot be stated in a short schema without the refinements creeping back, or a
blind writer still needs unstated rules.

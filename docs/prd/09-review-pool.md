# Human review pool

> Status: first version frozen, October 18, 2026; intake only, output deferred. English edition: October 25, 2026 (D163).
> Design page: `docs/system-design.html` → New → Human review pool. Recorded decisions take precedence.

## Purpose

Hold items that lookup tables or rules cannot resolve for a person to review. Do not guess.

Classification already requires registering unknown table entries and identifiers, while an item with unresolved subjects can continue. Without a review destination, these gaps would accumulate unnoticed.

## Intake

| Condition | Item handling |
|---|---|
| Unknown filing code or dataset | Invalid; do not process yet |
| Unresolved author type | Invalid; do not process yet |
| Unregistered publication series | Classify by author rules and process normally |
| Unresolved company, cryptocurrency, commodity or theme identifier | Process normally; mark subject unresolved |
| Candidate proposes an out-of-universe theme, such as a new conflict | Do not open the thesis; record the reason and proposed theme |
| Repeated processing failure | Remain at the failed step for review |
| Missing upstream information | Return |

## Exclusions

A resolvable company, cryptocurrency or commodity merely outside the universe does not enter the pool. For example, Samsung in Apple news may resolve in reference data without belonging to our research universe.

## Records

Keep one entry per issue, with occurrence count and examples, rather than one entry per input item.

## Output

Deferred.

## Intake acceptance

- Each intake condition creates the corresponding pool entry.
- Resolvable out-of-universe assets do not enter.
- Repeated occurrences produce one entry with accurate count and examples.

## Open questions

- How review updates lookup tables or the research universe and takes effect.
- Notifications and review ownership.

## Related decisions

- D16: unresolved items enter human review. D19: intake only; output deferred.
- D27/D33/D41: proposed library themes enter the pool. D31: repeated processing failures enter.
- D37: first-version freeze; changes need a decision.

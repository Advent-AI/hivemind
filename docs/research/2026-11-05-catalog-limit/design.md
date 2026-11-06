# Remove the research question-catalog byte rejection

Alex, after seeing that the research reader still imposes a separate 150 KB question-catalog limit: “这个也是个傻逼的东西，移除”. Remove that limit too. The reader returns the complete historical catalog of the relevant subjects, all configured themes and the existing dependency targets, whatever its serialized size. Do not truncate, summarize, replace it with a larger arbitrary byte limit, or change selection and history. This supersedes the catalog-limit portion of D376 and of `docs/research/2026-10-27-stage12-pinned/design.md`. D376 already removed the separate evidence limit. Gold, prompts and the running seven-day worktree stay untouched.

## Census and mechanism

The only active implementation of this limit is `Reader.catalog`: it builds the full catalog then serializes it just to reject anything above 150,000 bytes. A full repository search found the diagnostic census helper passes `catalog_limit` conditionally; no production or research pipeline caller passes it, and no outside caller uses `ContextTooLarge` or `bounded`. The saved pilot and two stopped/current diagnostic snapshots were each read with the legacy enlarged limit solely for a $0 census. They contain 69, 69 and 71 questions and use 84,489, 84,593 and 87,003 bytes respectively; none hits 150,000. This is a preventive removal at Alex's direction, not a claim that the current run was stopped by this guard. The running snapshot is a point-in-time copy, not the live database.

## Contract and readers

| Value | Reader and effect |
| --- | --- |
| Catalog | `Reader.catalog` returns all in-scope open questions and their applicable dependencies, with unchanged historical boundary and full fields. The research caller and `Reader.expand` receive the same object, including `complete: true`. |
| Evidence expansion | Continues to return complete evidence under D376, with no evidence byte cap. |
| Removed constructor field | The census helper passes `catalog_limit` only when the old signature supports it; production/research callers use defaults. Remove the field and its validation, `bounded`, `ContextTooLarge` and the now-unused `json` import; the helper continues to work against both versions. |
| Data and logs | Existing snapshots, model archives, gold and results remain immutable. |

## State and events

| Event | Behavior |
| --- | --- |
| Before sequence / another writer / another scope | Preserve the single read transaction, historical sequence and subject/theme scope. |
| Empty, normal or >150 KB catalog | Return all eligible questions, complete and without truncation. |
| Expand a selected item | The catalog remains the selection authority; preserve existing invalid/duplicate ID refusals and evidence behavior. |
| Missing source, invalid scope or database failure | Propagate the existing failure; do not return a false empty success. |
| Running seven-day test | Change main worktree only; its pinned experimental worktree and process remain untouched. |

## Verification before acceptance

Use the real saved pilot to capture the canonical catalog hash before change and compare with the default reader afterward. Add a portable test that uses a temporary real SQLite ledger with a >150,000-byte catalog; check every question, scope, dependency, original text, empty/future exclusions and selected-question expansion. Exercise both `catalog()` then `expand()` and direct `expand()` on a fresh reader, and compare complete evidence. First run the new test against the old guard and confirm the expected `ContextTooLarge`, then run the unchanged test on the fix. Reinstate the old guard in a scratch copy and prove the test fails. Run the touched and frozen-ruler tests and documentation checks. Run the full suite once after the paid seven-day run no longer competes for resources; until then report the full suite as pending, not passed. A returned catalog's size is not a claim that a model can take it all in one request.

## Implementation and verification, 2026-11-05

`src/hivemind/research_context.py` now has no catalog byte rejection, constructor size setting, or unused byte-limit helper. The catalog and evidence remain complete and use the same historical snapshot and scope. Before the change the new portable test failed at 326,996 bytes against the old 150,000-byte limit; after the change it passes with all 400 added question texts intact and with both catalog-then-expand and direct-expand paths checked. A scratch copy with the old limit reinstated fails the same test at that guard. Six targeted reader and frozen-ruler tests pass. The real saved 69-question catalog matches the exact pre-change canonical hash, and the previous 69 evidence expansions and full 4,219-piece set still match their pre-change hashes. The full suite remains pending while the seven-day paid run is live; no semantic quality or downstream model capacity is inferred from these checks.

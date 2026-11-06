# Remove the evidence expansion size rejection

> **Later decision, D377:** Alex also removed the separate question-catalog byte rejection. Statements below that the catalog limit remains in force describe the earlier D376 checkpoint; the current design is `../2026-11-05-catalog-limit/design.md`.

Alex: “读取器的傻逼限制是什么？你在这个agent 跑的同时，把这个限制给移除”. The named limit is the `Reader.expand` one-million-byte rejection. Remove it: a selected question's complete evidence is returned regardless of serialized size. Keep original source references, previous statements and the historical sequence boundary. Never replace the refusal with truncation, a larger arbitrary cutoff, a model filter or a summary. The separate 150,000-byte question-catalog limit was not named by this decision; it remains as it was. This directly supersedes the evidence expansion part of `2026-10-27-stage12-pinned/design.md`'s “1,000,000 UTF-8 bytes … exceed budget fail” and “do not bypass” instruction. The prior recorded test results stay historical. No gold, prompt, model setting or live seven-day worktree changes.

## Class and mechanism

The immutable finished pilot snapshot and reproducible `census.py` read every individually selectable question before sequence 1206. Of 69 open questions, v2 (1,376,425 bytes; 1,833 evidence pieces) and v10 (1,405,331 bytes; 1,866 pieces) individually exceed the limit. The pilot's four selected questions produce 1,931,225 bytes and 2,568 unique pieces; one `bounded` check rejects the entire result, so the completed extraction, writing and daily judgement are not visible to this reader. The 69 questions together contain 4,219 unique pieces and serialize to 3,454,076 bytes. `census.json` pins the saved ledger hash and counts. These figures describe this one snapshot; combinations of smaller questions can also exceed the cap and were not exhaustively enumerated. The census used a raised caller limit solely to inspect the saved data; removing the check, not raising its constant, is the requested fix.

## Value and reader

| Value | Writer and reader | Changed behavior |
| --- | --- | --- |
| Full expansion object | `Reader.expand`; research callers `docs/research/2026-10-27-stage34-gold/run.py` and the experimental seven-day pilot continuation | Same object, source, sequence and evidence; return it when it exceeds 1 MB. No partial result. |
| `evidence_limit` argument | The reader's constructor, one retired-size test and this investigation's census helper; no production caller passes it | Remove this retired argument, stored attribute and validation. The census helper detects old versus new signatures so its saved baseline stays reproducible. |
| Catalog limit | `Reader.catalog`, same callers | Unchanged: the request only removed the evidence expansion limit. |
| Existing historical records | Read-only ledger and model archive | No writes or changes. |

## States and checks

| State/event | Behavior |
| --- | --- |
| Before selection, current or historical date | `before_seq` and one read transaction set the state, as today. |
| Empty, one or several valid question IDs | Return all corresponding evidence, even if more than 1 MB; deduplicate identical evidence IDs as today. |
| Invalid or duplicate IDs | Raise as before; never return an empty successful result. |
| Later database writes, simultaneous reader or other scope | The existing snapshot/sequence behavior is unchanged. |
| Failure during assembly | Propagate the original error; never mark partial data complete. |
| Catalog exceeds its separate limit | Existing catalog refusal stays in force. |
| The seven-day process is running | Edit and validate in the main worktree only; the running experimental worktree and its pinned runtime stay untouched. |

## Evidence before and after

First reproduce default refusal against the saved pilot snapshot and save content hashes for the old high-limit results. After the change, the default reader must return the exact same objects and all source references for the four pilot questions, both individually oversized questions and the full 69-question catalog; compare IDs, output bytes and source identities, not only `complete: true`. Add a portable temporary-ledger test containing more than 1 MB of records, with complete evidence and sources checked; it must work without the historical worktree. Check missing and duplicate IDs and preserve empty selection and the historical boundary. A scratch mutation reintroducing the old one-million-byte check must fail the decisive test; the unmutated control must pass. Measure size and runtime on the fixed snapshot. Run the touched suite and structural checks. Full-suite inability from the environment must be reported rather than called a pass. This does not claim any model can consume a 3.45 MB prompt or that the seven-day run adopted the change.

## Implementation and verification, 2026-11-05

`src/hivemind/research_context.py` no longer takes or checks `evidence_limit`; it returns the complete expansion object directly. The catalog's separate limit is unchanged. Before the edit, the portable test failed on the old guard at 2,387,048 bytes. Afterward, the reader tests and frozen-ruler tests passed (5 tests), including all 1,800 synthetic evidence IDs and their source links; restoring the old cap in a scratch copy made the new test fail with the expected `ContextTooLarge`. On the saved real ledger, each of the 69 individual outputs, the four-question 1,931,225-byte request with 2,568 evidence records, and all 69 questions with 4,219 unique evidence records had byte-for-byte identical canonical content hashes to the pre-change high-limit baseline. The complete 69-question census, including repeated individual and combined reads, took 0.2407 seconds on this machine. This is a local diagnostic, not a model-context or semantic-quality measurement. `docs/check.py` passed. The full test run was deliberately interrupted after 113 passed because the seven-day paid diagnostic was live; it is not reported as a full-suite pass.

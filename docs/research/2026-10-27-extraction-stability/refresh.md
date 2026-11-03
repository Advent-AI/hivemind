# D338 refresh and verification

2026-10-27. This slice changes the research prompt and creates an isolated development experiment. It does not modify production code, configuration, stored source data or the module contracts. The candidate fails overall stability; the result is not acceptance or authority to resume the long run.

The reasoning pass follows `docs/prd/README.md` in order. In each row: whether this slice affects the module; whether its page/PRD behaviour needs alteration; whether the example still applies; and whether acceptance/open questions change.

| Module | Reasoning |
|---|---|
| Research universe | No scope change. Page/PRD and subject examples remain applicable; no acceptance change. |
| Classification | No category or source-field change. Reporting-only text is a manually verified experimental mask, not a new upstream parser. Existing examples/acceptance remain. |
| Config | No production prompt/model version is changed. The two research prompts and their settings are independently frozen. Versioning examples and acceptance remain. |
| Dispatch | No entry-point, sequence or retry change. Independent repeated calls are research draws, not production dispatch retries. Examples and acceptance remain. |
| Extraction | The open category-prompt validation question now has a failed development comparison. The foundational page/PRD still requires complete sourced, linked output; this experiment does not weaken it. Default wording and examples remain; no acceptance claim. |
| Thesis library | Existing source, target, identity, grouping and tier contracts remain. Displaying unusable group-member IDs is recorded as an implementation defect in the studied runtime, not a new permitted link category. No page/PRD change. |
| Final verdict | No change to the deferred design or decided due-date freezing. Examples and acceptance remain. |
| Pull mode | No scheduling, date or lifecycle change. Examples and open questions remain. |
| Human review pool | No intake or output change. No new workflow is launched. |
| System overview | Read-only extraction and downstream ownership remain intact. No voting or multi-call production mechanism is introduced. The research result adds no new system contract. |

Documentation corrections: D338 now records the failed candidate; CURRENT_STATE names the admission-v12 study separately from the main default, records its defects and replaces the stale next-task paragraph with Alex's active extraction-stability task. No generated PRD block was edited.

Verification:

- Two pre-call read-only reviews found no serious blockers. Reports are preserved under `poc/reports/2026-10-27-extraction-stability/review-1.txt` and `review-2.txt`.
- Frozen request check: 60 ordered requests; sorting preserves the old canonical hash but changes actual request bytes. All 12 live input cells have five byte-identical request bodies.
- Three stored-answer mutants caught: omitted claim, changed quote number, nonexistent target ID. The genuine CoreWeave backlog claim passes.
- Preflight ran against a frozen runtime and copied item/views databases. All three study controls pass; existing historical refusals and the old judge-schema limitation are retained in the result and log.
- 60/60 live calls completed, all normal stops. 529 original evidence entries reviewed; 437 pass the unchanged source/target checks. Every sample and refusal remains in the result.
- Full Python suite: **165 passed in 21.61s**. Initial sandbox invocation failed before collection because the installed pytest rerun plugin binds a localhost socket. The same command then passed with approved host execution; the original failure log is retained.
- Final `python3 docs/check.py` output is recorded in `poc/reports/2026-10-27-extraction-stability/docs-check.txt`. A mechanical pass does not establish model stability.

No commit, push, deployment, default promotion or long-run resumption was performed.

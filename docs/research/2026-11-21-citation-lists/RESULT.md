# Citation-only judge version: build and $0 test result (D714)

**Verdict:** judging-v12 and poc-v121 are built, and every registered $0 check passes (DESIGN.md §5, registered before the runs;
D713). No paid call was made. Provider acceptance of the format, and whether the judge then picks the intended source, remain for
a paid step that is Alex's to open (D712).

## What was built (uncommitted)

| File | Change |
|---|---|
| `src/hivemind/views/judging.py` | `judging-v12` added to `SUPPORTED_VERSIONS`, plus `CLOSED_LISTS` |
| | `schema_for(version, lists)` closes the four id fields for v12: one shared `$defs` evidence enum, plain dependency and theme enums, `maxItems: 0` when a list is empty |
| | `request_parts` returns the texts and the lists from the same rows; `build_prompt` delegates to it |
| | `check_answer(..., lists)` checks membership against the lists under v12 |
| | `round_of_judgements` sends each v12 view its own format, the retry included; v7/v8 still go through `build_prompt` with the frozen format |
| `src/hivemind/model.py` | `check_schema` enforces `maxItems` |
| `src/hivemind/prompts/judging-v12.txt` | a byte copy of judging-v7 (sha `d499c4b8…`) |
| `poc/config/poc-v121.json` | poc-v118 with `rejudging.prompt_version` = judging-v12 |
| `scripts/preflight.py` | part A checks judge rows against their saved format; a judge row without one, a malformed one included (Codex r39), fails `main` with exit 1 |
| `tests/test_citation_lists.py` | 7 tests: T1c, T3, T3b, T5 (part A, and `main`'s exit) and the format-error path |
| `tests/test_frozen_questions_and_judgement.py` | 1 new test: the v12 prompt and two v12 formats pinned; the v7/v8 format sha unchanged |
| `tests/test_live_lock.py` | part A's stub returns the new pair |

**Checks of the build**
- Suite: 388 passed, rerun after the preflight fix. The frozen tests are part of it.
- `docs/check.py`: OK, rerun after the documents were updated.
- Mutants: 12 of 12 caught, each by its own assertion (`mutants.log`). The failing assertion of each of the first 11 was read; the
  12th is the malformed-row ordering.

## The registered $0 checks

| Check | Result | Record |
|---|---|---|
| **T1** old-2 replayed under poc-v121 | **PASS** | `poc/data/citation-t1-2026-11-21-run2/t1-result.json`, `t1-replay.log` |
| **T1b** the four refused originals | **PASS** | same file |
| **T1c** a real v12 retry | **PASS** | `tests/test_citation_lists.py` |
| **T2** every stored shape, offline | **PASS** | `t2-result.json`, `t2-offline.log` |
| **T3** the real validator's controls | **PASS** | `tests/test_citation_lists.py` |
| **T3b** one owner of membership | **PASS** | same |
| **T4** sizes | printed | `t2-result.json` |
| **T5** preflight on a judge row without a format | **PASS** | `tests/test_citation_lists.py`; on old-2's real archive, part A checks its 4 refused judge rows against their saved format and preflight ends `preflight done` (`preflight-old2.log`) |

### T1, old-2 replayed under poc-v121
- 1,616 judge responses went through the transport, 4 of them labelled substitutions: 591→596, 6955→6979, 7068→7073, 7774→7780.
- Every request equals old-2's outside the format.
- Every format is strict, named `judgement`, and differs from judging-v7's only in the four constraints.
- 0 list mismatches against the ids the text shows.
- The store equals old-2's on all 36 shared tables, apart from the named columns:
  - timestamps: `days_completed.at`, `processing_steps.at`, `views.created_at`;
  - the judgements' `call_id`, `request_sha256` and `config_checksum`.
- Positive control: one judgement's `why_changed` changed in a copy is reported as different.

### T1b, the four refused originals
Each goes through the real `model.call` under its v12 request and raises `SchemaError` on the id the check had refused: `e88`,
`e3955`, `v10`, `e3998`.

### T1c, a real v12 retry
The retry carries the first request's exact format and lists, plus the note.

### T2, every stored shape
- Population: 5,415 rows; 5,408 distinct pairs; 5,389 committed; 17 refused; 2 valid uncommitted.
- Every committed and every valid uncommitted answer validates.
- Every refused answer fails on its bad id:
  - e362, e3111, e393;
  - e88, e3955, e3998, e1382, e2769, e693;
  - theme ids in cites (`v6`, `v10`);
  - the dependency `v14` as evidence, twice;
  - `v5` in `cites_views`, four times.

### T3, the real validator's controls
In all four fields, an allowed id passes and an unlisted id fails. An empty list allows only `[]`, and a correctly typed item fails
on length.

### T3b, one owner of membership
- With a footnote in a quote, the v12 lists and the check accept the later real id.
- v7's text parser refuses it. That narrowing is a latent defect of the frozen versions, recorded and not fixed there.

### T4, sizes
- Over the five archives the largest request has 451 evidence ids: 464 enum values with the shared enum counted once, 915 counted per
  reference; 5,225 characters.
- In the sealed D358 run the largest has 647 ids: 676 counted once, 1,323 per reference. 10 of 949 requests exceed the documented
  1,000 if the provider counts per reference; none if it counts once.

### Format size
- Characters: judging-v7's format is 1,031; v12's median is 1,396–1,405 and its max 5,225.
- Tokens, an estimate with o200k_base on the format's JSON over all 5,415 stored requests (the provider's own count arrives with the
  paid step): v7 315; v12 median 502, p99 1,542, max 2,621.
- At $0.10 per million input tokens, the largest request costs about $0.00023 more.

## Deviations, disclosed

- **T1's first run** (`poc/data/citation-t1-2026-11-21/`) completed the replay, but the comparison crashed: a harness defect, since
  FTS tables have no rowid. The transport's log was lost with it.
  - The fixed comparison on that store found three differences. Each was named only after it was seen:
    - `views.created_at`, a wall-clock timestamp;
    - `link_selections`, a table the current uncommitted store schema adds (D694), empty;
    - `dependencies.kind`, a column the same schema adds, on a table empty in both.
  - The design's named class was "timestamps … and new empty tables". The added column on an empty table is the same kind, but not
    named in advance.
  - T1 was then rerun in full into `citation-t1-2026-11-21-run2/`. It saved passing T1 and T1b results (`t1-result.json`,
    `transport-log.json`), then exited 1: its summary print failed on a list value, a harness defect. The print is fixed, and the
    current code exits 0 on the saved results. The saved data verifies the replay without repeating it (Codex r39 checked all 1,616
    requests, the substitutions, the new hashes and the 36 tables).
- **The first harness's store** is left in place, marked harness-only.
- **Preflight** first let a refused judge row with neither a readable answer nor a saved format through with exit 0 (Codex r39,
  reproduced). The format is now checked first; T5 covers the case, and its mutant is caught.
- **Council round 39** (`codex-r39.md`): the build matches DESIGN v3; no v7 or v8 regression was found; T1's saved evidence holds;
  T2 and T4 reproduce. The items above are its findings, all taken.

## What the $0 test cannot show (DESIGN.md §6)

- Whether the provider accepts the exact format: the shared reference, `maxItems: 0`, and the largest request.
- How the provider counts a referenced enum.
- Whether the judge, constrained, cites the intended source (e3111 could become e3110 or e3112).
- Whether forecasts move.

A paid step answers these, and it is Alex's to open. Its first part would send the largest stored request and an empty-list request
to check acceptance. Then it would re-send the 17 stored refused requests and a matched set of accepted ones under v12, and read the
cited sources beside the forecasts.

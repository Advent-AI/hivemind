# Council round 74: review the slice-1 build design before any code (read-only)

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

## What to review

`docs/research/2026-11-22-number-answers/RELEASE-BUILD.md`, the build design for the first slice of the "Forecast unavailable"
release. The governing documents:
- `docs/research/2026-11-22-number-answers/FORECAST-UNAVAILABLE-DESIGN.md` (revision 4, ready per `codex-r72d.md`);
- D726, D756, D757 and D758 at the end of `docs/DECISIONS-log.md`;
- AGENTS.md §2 (design tables before code), §3 (one owner; the writer refuses), §4 (tests) and §5.

Code that the design reuses:
- `src/hivemind/service.py`: `resolve_bound`, `view_exists`, `is_open_as_of`, `state_as_of`, `evidence`, `evidence_record`,
  `ladder_bands`;
- `src/hivemind/bundle.py`: `read_snapshot`, `item_lookup`, `view_bundle`;
- `src/hivemind/views/store.py`: `view_key`, `rungs_of`;
- `src/hivemind/views/identity.py:10`;
- `src/hivemind/vocabulary.py:24`;
- `src/hivemind/idea.py`, for the idea question.

## Questions

1. **Leaks.** Does the allow-list in §1 let any number forecast reach the package? Check:
   - each allowed field's real content in stored stores, read-only (for example `poc/data/comparison-2026-11-17/run/old-1/prod/views.sqlite`):
     `question`, evidence `one_line` and `quote`, source titles;
   - whether evidence linked to a number question can itself be a system-written forecast rather than a source statement.

   Name any path with a stored example.
2. **Tables.** Are the state × event, value × reader and new path × old checks tables complete? Name any blank or wrong cell, for
   example an event the export can meet that is not listed.
3. **Tests and mutants.** Does each named test fail without the code it tests? Is a decisive case missing?
4. **The $0 release check (§7).** Is the leak sweep sound? Consider the 12-character floor and the string classes. Would it miss a
   forecast restated in different words?
5. **The four open points in §8:**
   - no idea submission in the release, with the idea acceptance moved to a later slice;
   - `object` and `kind` on every record;
   - groups left out;
   - the sweep floor.

   Decide each.
6. **Ready to build?** Give a verdict: ready, or not ready with each serious finding.

**Out of scope:** the judging, opening and extraction pieces (frozen); the closed v13s line; the POC's own behaviour; any other open
defect; wording. Report only findings that change what is built or whether it is safe.

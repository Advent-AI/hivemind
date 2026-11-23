# Council round 75e: re-review the built slice 1 after round 75's fixes (read-only)

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

Rounds 75 to 75d (`codex-r75.md` to `codex-r75d.md`) did not accept slice 1; their findings since 75c were verification gaps, answered in 75d with one structural rule (fixed expected values; exact refusal reasons). Claude fixed the code, the tests, the mutant
runner and the check script, and recorded the changes:
- `RELEASE-BUILD.md`, its revision 11 block;
- `RELEASE-CHECK-RESULT.md`, rewritten from the new run `poc/data/release-check-2026-11-23e/results.json`.

The files are `src/hivemind/release.py`, `scripts/release_build.py`, `tests/test_release.py`, and in that folder `release_mutants.py`
and `release_check.py`.

## Questions

1. Is each finding of rounds 75 to 75d closed, and does the structural rule hold in every acceptance assertion in the code and tests? Name any still open, with file:line.
2. Did the fixes introduce a new way for a value off the allow-list, or unequal to its store, to reach a package? Or a test that
   passes without the protection it names?
3. Do the claims in the rewritten `RELEASE-CHECK-RESULT.md` follow from the new `results.json`, the scripts and the code?
4. Verdict: slice 1 accepted, or not accepted with each serious finding.

**Out of scope:**
- the frozen judging, opening and extraction pieces;
- the closed v13s line;
- the POC's own behaviour, the shared `store.open_read_only` included;
- slice 2 and the idea path;
- the recorded evidence-summary disagreement;
- style.

Report only findings that change whether slice 1 is correct or safe.

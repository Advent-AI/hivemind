# Council round 75: review the built slice 1 against its design, and its $0 result (read-only)

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

## What to review

Slice 1 of the "Forecast unavailable" release was built to `docs/research/2026-11-22-number-answers/RELEASE-BUILD.md` revision 10,
which council 74j found ready:
- the code: `src/hivemind/release.py`, `scripts/release_build.py`;
- the tests: `tests/test_release.py`;
- the result: `docs/research/2026-11-22-number-answers/RELEASE-CHECK-RESULT.md`, from `release_check.py`, with output in
  `poc/data/release-check-2026-11-23/results.json`;
- the mutants: the script at `/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/release_mutants.py`.
  It ran with 21 of 22 caught; the 22nd, the canonical-day check, is equivalent on Python 3.10, as the result explains.

## Questions

1. **Divergence from the design.** Does the code do what revision 10 specifies? Check every function and command step against §1,
   §2 and §3. Name each place where the code departs from the design, with file:line, and say whether it is unsafe.
2. **Leaks.** Can any value reach the package that is not on the allow-list, or that is not equal to its stored source at the
   bound? Look at the actual code paths, not the design.
3. **The tests.** Does each test assert what its docstring claims, and fail without the code it names? Are any of the 23 tests
   vacuous? Is the mutant run sound (its edits, its environment, the control)?
4. **The result.** Do the numbers and claims in `RELEASE-CHECK-RESULT.md` follow from `results.json` and the script? Is any claim
   overstated?
5. **Verdict:** slice 1 accepted, or not accepted with each serious finding.

**Out of scope:**
- the frozen judging, opening and extraction pieces;
- the closed v13s line;
- the POC's own behaviour;
- slice 2 (the page) and the idea path;
- the recorded evidence-summary disagreement;
- style and wording.

Report only findings that change whether slice 1 is correct or safe.

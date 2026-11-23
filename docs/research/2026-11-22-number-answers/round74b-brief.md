# Council round 74b: re-review the slice-1 build design, revision 2 (read-only)

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

Round 74 (`docs/research/2026-11-22-number-answers/codex-r74.md`) found the build design not ready. Claude answered in
`claude-r74.md` and revised `RELEASE-BUILD.md` to revision 2. The governing documents are the same as in `round74-brief.md`:
`FORECAST-UNAVAILABLE-DESIGN.md` revision 4; D726, D756, D757 and D758 at the end of `docs/DECISIONS-log.md`; AGENTS.md §2–§5.

## Questions

1. **Accepted findings.** Does revision 2 resolve every finding of round 74 that Claude accepted? Check the origin check as the pass
   condition, the missing-item refusal, the build order and retry, the manifest, date validation, narrow reads, budgets, tests and
   mutants, and the decisive acceptance case. Name any finding still open, with the line of revision 2 that misses it.
2. **The disputed point** (`claude-r74.md`, "Disputed"; revision 2 §8). Claude keeps evidence summaries as extraction stored them.
   Verify Claude's evidence: does the extraction request show any rung, label or judged position (`src/hivemind/placement.py:19-61`,
   `src/hivemind/extraction.py:380-402`, `src/hivemind/research_context.py`)? Is the census framing right? Decide: is keeping the
   stored summary within D726 and the design's allow-list ("one-line, quote, …")? Or must the release use source wording where a
   summary adds a figure? If you still disagree, say so plainly. The disagreement is then recorded and the cheaper, reversible course
   taken.
3. **New problems** introduced by revision 2: the independent origin check, the staging and rename, the `check` mode.
4. **Verdict:** ready to build, or not ready with each serious finding.

**Out of scope:** the frozen judging, opening and extraction pieces; the closed v13s line; the POC's own behaviour; other open defects;
wording. Report only findings that change what is built or whether it is safe.

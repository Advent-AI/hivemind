# Council round 74h: re-review the slice-1 build design, revision 8 (read-only)

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

Round 74g (`docs/research/2026-11-22-number-answers/codex-r74g.md`) found two remaining points in revision 7, both in report writing:
- `check` could overwrite an input reached by a case-variant name;
- `build` could overwrite a file created at the report name while it ran.

Claude revised `RELEASE-BUILD.md` to revision 8 (see its "Revision 6 answers" block). The governing documents are the same as in
`round74-brief.md`.

Read the whole of revision 8 once more, end to end, as an engineer who must build it.

## Questions

1. Are the two 74g points closed? Name any still open, with its line.
2. Any serious problem left anywhere in revision 8 that would make the build unsafe, or that an engineer could not build from the
   text?
3. Verdict: ready to build, or not ready with each serious finding.

**Out of scope:** the frozen judging, opening and extraction pieces; the closed v13s line; the POC's own behaviour; other open defects;
the recorded evidence-summary disagreement (§8); wording. Report only findings that change what is built or whether it is safe.

# Council round 74e: re-review the slice-1 build design, revision 5 (read-only)

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

Round 74d (`docs/research/2026-11-22-number-answers/codex-r74d.md`) found revision 4 not ready on two points:
- publication or cleanup could remove another owner's empty folder;
- a database error could leave an empty output folder.

Claude revised `RELEASE-BUILD.md` to revision 5, with one structural rule:
- staging is private (`tempfile.mkdtemp`);
- the only public step is `renamex_np(..., RENAME_EXCL)` on macOS, or `renameat2(RENAME_NOREPLACE)` on Linux, refusing elsewhere;
- staging is removed in a `finally` covering its whole life.

Claude verified on this Mac with `ctypes`: a move onto a free path succeeds, while onto an existing empty or non-empty folder it fails
with `EEXIST` and leaves both folders intact.

## Questions

1. Does revision 5 close both 74d findings and the test-14 gap (a foreign empty folder at publication; exit status shown through the
   command)? Name any still open, with its line.
2. New problems introduced by revision 5.
3. Verdict: ready to build, or not ready with each serious finding.

**Out of scope:** the frozen judging, opening and extraction pieces; the closed v13s line; the POC's own behaviour; other open defects;
the recorded evidence-summary disagreement (§8); wording. Report only findings that change what is built or whether it is safe.

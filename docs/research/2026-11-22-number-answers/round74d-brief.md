# Council round 74d: re-review the slice-1 build design, revision 4 (read-only)

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

Round 74c (`docs/research/2026-11-22-number-answers/codex-r74c.md`) found revision 3 not ready. Claude revised `RELEASE-BUILD.md` to
revision 4 (see its "Revision 4 answers" block). The governing documents are the same as in `round74-brief.md`.

One design choice differs from 74c's suggestion. Instead of `renamex_np(RENAME_EXCL)`, the build claims its output folder with an
atomic `os.mkdir` before any export. The final `os.rename` then lands on its own empty claim. A rename replaces only an empty
destination, and fails on a non-empty one (verified on this Mac: errno 66). The build releases its claim with `os.rmdir`, which
removes only an empty folder. Judge whether this meets the requirement that no build can replace a folder it did not create, using
only the standard library.

## Questions

1. **The 74c findings.** Does revision 4 close each one?
   - one date rule;
   - `created_seq, rowid` order;
   - the move cannot replace a folder the build did not create;
   - cleanup where the staging path is known;
   - the outcome after publication;
   - test 12 through the real command;
   - tests 9, 13, 14 and 15.

   Name any still open, with the line that misses it.
2. **New problems** introduced by revision 4.
3. **Verdict:** ready to build, or not ready with each serious finding.

**Out of scope:** the frozen judging, opening and extraction pieces; the closed v13s line; the POC's own behaviour; other open defects;
the recorded evidence-summary disagreement (§8); wording. Report only findings that change what is built or whether it is safe.

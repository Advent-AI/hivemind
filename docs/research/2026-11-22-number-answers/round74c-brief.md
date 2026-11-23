# Council round 74c: re-review the slice-1 build design, revision 3 (read-only)

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

Round 74b (`docs/research/2026-11-22-number-answers/codex-r74b.md`) found revision 2 not ready, with five build blockers and one open
test. Claude revised `RELEASE-BUILD.md` to revision 3. The governing documents are the same as in `round74-brief.md`.

## Questions

1. **The 74b findings.** Does revision 3 close each one?
   - Blocker 1: the bound, class, records and counts are derived from the store.
   - Blocker 2: a missing item refuses `check`.
   - Blocker 3: regular non-symlink files, and no duplicate JSON member names.
   - Blocker 4: staging has one owner, the rename refuses an existing destination, write and rename errors are handled, and two
     builds aim at one output.
   - Blocker 5: diagnostics read only the columns a store has.
   - The builder-refusal test.

   Name any still open, with the line that misses it.
2. **The recorded disagreement on evidence summaries** (§8). Is it recorded faithfully to `codex-r74b.md` §2?
3. **New problems** introduced by revision 3. Check in particular:
   - the fault-injection test 12: is it an acceptable test of the builder's refusal under AGENTS §4?
   - the `os.rename` semantics on macOS when the destination is an existing empty folder;
   - `check`'s bound rule for a legacy ledger.
4. **Verdict:** ready to build, or not ready with each serious finding.

**Out of scope:** the frozen judging, opening and extraction pieces; the closed v13s line; the POC's own behaviour; other open defects;
wording. Report only findings that change what is built or whether it is safe.

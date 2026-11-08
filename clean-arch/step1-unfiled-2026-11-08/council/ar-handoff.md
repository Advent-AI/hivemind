Read-only review of the D387 adoption change, fresh session. Repository /Users/lchingen/hivemind.

Alex chose "采用 c8": the clean Step 1 configuration becomes c8. The record is `docs/DECISIONS-log.md` D387, the last entry.

The change, to review:
- `council/ar-diff.patch`: runner, tests and renderer;
- `clean-arch/PRD.md` §12: its introduction, "System prompt", "Closing check" and "Structured-output schema";
- `docs/DECISIONS.md`: the D387 row.

Check these, reading the files themselves:
1. Do PRD §12's three blocks equal `clean-arch/step1-unfiled-2026-11-08/arms/c8-system.txt`, `c8-closing.txt` and `c8-schema.json`
   exactly? Does a run with no candidate files send byte for byte what the accepted runs sent (system message, user message ending
   with "\n\n" + closing)? Compare with one request stored in `poc/data/clean-acceptance-2026-11-09/step1/trace.sqlite` (table trace,
   column request), with the payload set aside.
2. Do the test changes only bring fixtures to the adopted schema and parse the payload before the closing check, leaving every
   assertion's meaning unchanged? Does the new test fail without the change?
3. Is anything else changed in behaviour? Is any claim in PRD §12's new introduction unsupported by LOG §§40–44 or by D380–D387?

Out of scope: the content of c8 itself (already audited), production, and the frozen ruler.

Answer in English, under 400 words. End with APPROVE or the blocking finding.

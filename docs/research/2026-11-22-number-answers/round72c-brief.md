# Council round 72c (revision 3: one allow-listed release export), read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

Rounds 72 and 72b (`codex-r72.md`, `codex-r72b.md`) each found new leak paths in a reader-by-reader withholding design. Revision 3 of
`docs/research/2026-11-22-number-answers/FORECAST-UNAVAILABLE-DESIGN.md` replaces it with one structural rule: a single release
exporter with an explicit allow-list, and a release that reads only that export. It leaves one product choice to Alex: what Yes/No
questions show.

## Check
1. **Does the allow-list structure close every path rounds 72 and 72b found, and the class they belong to?** The paths: idea card,
   idea summary re-reading the ladder, closing text, live `/library` reload, translated export, composite trials, Yes/No prose.
   Is any path still able to bypass the export in a release build?
2. **Is §3's identity rule (now: everything not an event and not a canonical Yes/No pair is a number question, withheld) sound on the
   stored stores?** Does it withhold anything it should show, or show anything it should withhold?
3. **Is §4's open choice for Alex fair and balanced, and is option (b) decidable from stored data?** Is (a) or (b) the better
   recommendation?
4. **Is the design ready to hand to release work when Alex opens it?** This is design only; scope is agreed.
5. **Verdict:** ready, ready with listed changes, or not ready.

Return a numbered report with citations, then the verdict.

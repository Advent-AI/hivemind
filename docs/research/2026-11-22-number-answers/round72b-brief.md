# Council round 72b (revision 2 of the release-prep design), read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

Round 72 (`docs/research/2026-11-22-number-answers/codex-r72.md`) found the design not ready. Revision 2 is
`docs/research/2026-11-22-number-answers/FORECAST-UNAVAILABLE-DESIGN.md`. Scope is agreed: design only, and Alex opens release
work.

## Check
1. **Does revision 2 close every finding of round 72?** The findings were:
   - the idea leak;
   - the closing text;
   - the exports;
   - search and processing dates;
   - the identity rule's two counterexamples (sealed `v3`, Xbox `v37`);
   - showing only what Alex approved;
   - `claim_position`;
   - the fixed release setting;
   - the acceptance check.

   Verify against the code it cites.
2. **Identity.** Is §2's rule sound and buildable from the stored data? Check:
   - the view key's measure and `identity.EVENT_MEASURES`;
   - the Yes/No label test;
   - the condition parser in `service.py`;
   - the fail-closed treatment of ambiguous records.

   Does it misclassify any question in the three comparison stores or the sealed ledger the tests use?
3. **Anything still able to leak a number question's band or forecast** in a release build?
4. **Verdict:** ready for release work, ready with listed changes, or not ready.

Return a numbered report with citations, then the verdict.

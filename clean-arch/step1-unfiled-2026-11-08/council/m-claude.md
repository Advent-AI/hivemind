# Design review: `clean-arch/STEP1-CONDITIONS-DESIGN.md` (read-only)

Alex decided the shape (`LOG.md` §17; his words are quoted in the design §1). Review the draft as the skill's design gate (AGENTS §2):
find every serious problem before any code or probe.

Check:
1. **Value × reader:** every field a reader will need (Step 2, Step 3, Step 4, the evaluation);
2. **State × event for conditions:** repeat, revision, restatement, an estimate turning into an actual, the same figure from two
   parties, a condition later tested by a newly opened view;
3. **New path × old checks:** quote validation, link validation, unfiled handling, the format-failure policy;
4. **Prior decisions:** D209, D370, D371, D208, D373, the grouping decision, best match;
5. **Overreach or hard-coding:** does any rule name an importance list, a company or an industry?
6. **The three open questions** at the end.

List serious findings first, then wording-level ones. Say plainly whether the design is ready for the probe after fixes. Under 450
words.

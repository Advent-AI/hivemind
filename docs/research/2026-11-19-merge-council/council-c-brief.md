# Challenge round on the execution plan (read-only, $0). Alex has now said to execute: "write the plan, execute the plan, and don't do full blown runs, validate it works based on metrics we meassure for quality".

Read `EXECUTION-PLAN.md` and `articles.json` in this folder.

**One change from the consensus.** The 11 census articles carry almost none of old's window evidence.
- old-2 v5 drew window links from 24 other articles, old-3 v6 from 27, and the Anthropic questions from 4–5 others.
- None of the 11 was linked by old to its own target question; only control 223 was.
- So the set becomes the union of the articles either system tied to these matters: 126 articles, about $2.55 for 252 c8 sends.
- Check this against `poc/data/comparison-2026-11-17/run/old-2/prod/views.sqlite` (`evidence_links` and `evidence_sources`) yourself.

**Challenge:**
1. Is the union fair to both sides, or is a different set better?
2. The open-list conversion: old view to Step 1 thesis, as in step 1.
3. The judging-copy truncation (step 5): does it leak a later state or starve the judge?
4. Are the five lines right, and is any line one the old system itself would fail?
5. Anything that makes a pass meaningless.

Under 300 words. End `CONSENSUS: EXECUTE` or `CONSENSUS: CHANGE <smallest change>`.

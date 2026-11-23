**Do not freeze c7 yet.** The known problems include a contradictory valuation example, incomplete later linking, and measurement code that can report a pass without counting every case. For example, an older unlinked statement can remain unlinked forever if its first linking attempt fails and no later thesis opens.

This is an independent read-only review. I did not open `council/af-claude.md`, edit files, send model calls, or start runs. I cannot certify that every possible contradiction or downstream failure has been found; the complete clause-by-clause audit and stored-data census remain unfinished.

1. **Request contradictions and fixes**

- [c7 system:36](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c7-system.txt:36) presents “an analyst valued the shares at $80” as a material-statement example, while [closing:6](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c7-closing.txt:6) rejects valuation conclusions. D385 settles this: remove the valuation example; retain the underlying earnings estimate. The signed standard’s two supporting valuation entries remain a disclosed conflict, not edited gold.
- [c7 system:55](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c7-system.txt:55) says figures for “whatever period” inform a revenue or earnings thesis, while [lines 66–69](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c7-system.txt:66) require relevance and preserve period differences. Replace the automatic link with the relevance test; an unrelated period need not inform the question.
- [closing:12](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c7-closing.txt:12) orders another party’s statement split off, while the [standard:436](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:436) keeps a main claim and secondary planned or rumoured detail together unless they are different matters. Limit splitting to distinct statements; preserve necessary context in each. The report and denial remain separate.

The four opening categories at [c7 system:86](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c7-system.txt:86) omit the standard’s separate company-quantity category. D382 makes that a **by-design exclusion**, not an unreported prompt defect.

2. **Downstream checks that can mislead**

- **Keep and link:** [runner:149](/Users/lchingen/hivemind/clean-arch/step1/runner.py:149) records unverified passages and unresolved links rather than refusing them; [run_forward:52](/Users/lchingen/hivemind/clean-arch/step2/run_forward.py:52) passes the original passages and link IDs forward. Count both classes in stored traces; inspect each affected source and final dossier, including removed figures.
- **Later linking:** [library:74](/Users/lchingen/hivemind/clean-arch/step3/library.py:74) selects only groups whose *original* was unlinked, and [compare:90](/Users/lchingen/hivemind/clean-arch/step2/compare.py:90) judges only that original. A useful detail added by a later member may therefore be missed. Pending batches retry only when another thesis opens. Replay stored unlinked groups and pending batches against every relevant later thesis, reading misses as well as links.
- **Search and merge:** [compare:100](/Users/lchingen/hivemind/clean-arch/step2/compare.py:100) searches group originals, not later members. Check stored repeats and revisions missed by search, plus every wrong merge and the source text. The current score measures known mapped repeats, not all repeats or revisions ([score_final:34](/Users/lchingen/hivemind/clean-arch/step2-validation-2026-11-07/score_final.py:34)).
- **Mapping and scoring:** [map_reference:43](/Users/lchingen/hivemind/clean-arch/step2-validation-2026-11-07/map_reference.py:43) chooses passage overlap, which can map several old records to one new record. Audit collisions and unmapped pairs. [score_final:64](/Users/lchingen/hivemind/clean-arch/step2-validation-2026-11-07/score_final.py:64) divides wrong merges by *all* merges even if disputes remain unjudged. Require complete judgments before a verdict. [tally_questions:16](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/tally_questions.py:16) uses `zip`, silently omitting missing answers; require exact IDs and counts.

3. **Before freezing**

Complete the two-way request audit, fix confirmed contradictions, and replay stored answers through all checks. Census and trace the issues above; verify retry classification and exact sent requests, then run the relevant tests and full suite once. Recheck grouped-versus-ungrouped detail retention on the final path. The c7 dev run is exploratory until complete; c2–c7 test results are exposed and cannot establish acceptance ([log:1398](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1398)). Larger future-source studies can wait.

4. **Acceptance proposal—fix before choosing articles**

Use readable, NVDA-relevant articles in the supplied database that **no run has used**, excluding duplicates and checking all manifests and archives. Select chronologically with a fixed, reproducible rule, blind to outcomes; report the eligible count first. I propose **50 fresh test articles**, if available, with enough repeated reporting to exercise merging; otherwise agree the smaller population before selection. Start both thesis and evidence libraries empty and run forward in publication order.

Independent readers first list source matters, then judge coverage, false additions, thesis openings, links, attribution, dates, and grouped details; resolve disagreements against full sources. No new gold is created.

Apply the agreed lines: helpful coverage **at least 81.2%**—the 190/234 dev line, rounded up to whole matters; search **at least 90%** of independently identified incoming repeats **and revisions**; clearly wrong merges **at most 2% of all merges**, with none unjudged; grouped dossiers retain **at least as many** later details as ungrouped dossiers. Report must-open coverage and must-not openings; D384 replaced the earlier small-thesis line, but no numerical threshold for fresh-reader judgments has been agreed. Set it through council and Alex before selection.

State beforehand that company financial-level theses and valuation conclusions are excluded by design. Repeat the full dev forward run **three independent draws**, reporting each, failures and spread; do not use fresh acceptance articles to choose another configuration.

5. **Revert now**

Recommend reverting the blanket c6 splitting instruction to the standard’s distinct-matter boundary, and removing the valuation example. These are recommendations for the council to review; no files were changed.
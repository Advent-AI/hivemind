# Current state

As of October 30, 2026, the close-out of the extraction-quality phase; decisions through D246. Governing design: `docs/system-design.html` and `docs/prd/`; the extraction step's standard is [`prd/05-extraction-standard.html`](prd/05-extraction-standard.html) (D243). Every status paragraph of the phase, with its numbers, is in [the snapshot before this close-out](research/2026-10-29-ledger-standard/current-state.before-closeout-2026-10-30.md); earlier snapshots are linked there. They are records, not work orders.

## What runs, and which code is the latest

- **Latest pipeline code:** this branch, `fix/extraction-quality-2026-10-28`, stacked on `feat/thesis-admission-v12` and `feat/parallel-day`; all three pushed, none merged into `main`. `main` has the newer service, UI and Idea code (3 commits this branch lacks) and still replays `poc-v23` (extraction v10).
- **Default configuration:** `poc/config/poc-v67.json` (D246): extraction role-v51 on `gpt-6-luna`, the request showing no thesis and no group (D211); the placement call files each statement under the narrowest open question, and a statement no open question takes is dropped as `no home` (D207, D209); Jev matching with the collision judge (D190); judging with the theme block and the evidence in view (D195, D198). `scripts/replay.py`, the default-entry test and the README name it.
- **No long run is live** in any worktree; the three-month run is sealed through 2026-08-28 (D206) and the service serves that sealed ledger.
- Tests: full suite 239 passed; `docs/check.py` passes. The close-out code review (a blind reviewer, 13 findings) is answered below.

## The phase, 2026-10-28 to 2026-10-30

The three-month run was stopped on evidence bloat (D206). The extraction step was then rebuilt and measured alone, through its own harness:

1. Placement and drops (D207–D209): a separate placement call files statements; a statement no question takes is dropped with its reason and evaluation reads the drops.
2. The request no longer depends on the ledger (D211): the read is prepared early and filed at the item's turn.
3. One ruler (D229, D241, D243): the extraction standard signed by Alex, a golden set of 118 development articles and a frozen test set of 30, the scorer reading only the frozen gold (D244).
4. The prompt is a general hedge-fund brain (D237) and was iterated class by class on the direct read (D238): role-v29 (D239), role-v42 (D245, gold-rejected statements kept −26% at equal core), role-v51 (D246, must-not questions on small products 20 → 0 over 15 draws).
5. A quality read beyond the ruler (2026-10-30, [results](research/2026-10-29-ledger-standard/quality-2026-10-30/results.md)): four independent model readers read 24 random articles as analysts. The logs are [the loop log](research/2026-10-29-ledger-standard/loop-log.md) (rows 1–23) and [the direct-read log](research/2026-10-29-analyst-standard/loop-2026-10-29/log.md).

Where role-v51 stands (development set, three draws): core kept 77–81 of 86 per draw and the same in every draw (89% of core statements); supporting at least two draws 154 of 181; statements per draw 534 (role-v23: 833); numbers in the summary lines faithful (no invented figure in 2,065); about $0.0011 and 12.5 s per article.

## Open defects, to fix next

Each has its census; the extraction ones are classes for the loop of AGENTS §7.3 (one class at a time, the whole bench, read every regression).

Extraction (step 1), role-v51:

1. **Record fields when an article retells an earlier announcement** (the next class). Verified by Claude against the article text (readers' sample, 102 records of one draw, every flag read; [results](research/2026-10-29-ledger-standard/quality-2026-10-30/results.md)): the outlet is named as the original speaker of a company's or official's announcement in 13 records; the original day is the report day for an announcement made weeks or months earlier in 12 (an announcement of June dated July 6, a September reveal dated October 17) and for one covered within days in 8 more; the source tier is wrong in 9 (an official's charges as a third-party view, an announced company plan as a rumour). 30 of 102 records carry a verified field error (35 with the low date cases). The standard already rules (§5.4: an unknown day is written unknown, never the report day; §5.5 tiers); the prompt does not hold it. Downstream cost: the judge and the matcher read the original day and speaker, so old news reads as new and one announcement reads as several sources. 7 of the 12 material date errors are on one page that retells several deals (the SemiAnalysis backstop page).
2. **Summary lines** lose a condition or say more than the quote in 11 of 102 (the Groq "acquisition" in quotation marks written as an acquisition; a deal's "backstop" link left in a neighbouring record); one event is split into several records in 9 (one Reuters rumour as three records).
3. **Noise:** readers call 42 of 102 records noise and Claude agrees with all 42 (a defendant's assets on the optional Singapore case, restated year-old annual figures, a partner's own energy deal, a game list); gold-rejected sentences kept about 100 per draw on the development set.
4. **Questions**, read from the candidates themselves: DRAM contract prices (development) and the $12.9B Hugging Face acquisition (test) are opened in no draw, though the Hugging Face statement is kept in every draw; the OpenAI Ohio lease guarantee is never its own yes/no question, only covered by the wider lease-guarantee amount question; data-centre revenue for FY2028 is asked as total revenue growth (2 of 3 draws); per page the opening varies (the credit-support question on one page in 2 of 3 draws, carried by other pages in every draw). Must-not: the lidar-legislation policy question in 1 of 3 draws (role-v42: 11 of 15); one Nigeria production question in one draw.
5. **Whole statements lost:** 28 quotes refused by the quote check in three draws, every one read: 14 stitch parts of different sentences (the Palantir–Nemotron statement, the China H200 permission), 9 change a word or two at an edge ("the company" written as "Nvidia", "As a result" as "So"; among them the core "Nvidia provides a take-or-pay commitment" and "Vera CPU expected to bring $20 billion"), 2 are titles not in the body, 1 skips words with an ellipsis, 1 writes "85 percent" as "85%", 1 is a real misquote rightly refused. One whole-page empty answer on a page with 3 core entries (Micron, draw 1).
6. **The test set is small:** 9 core entries and 3 must-open questions; it shows no overfitting and little more.

Readers' doubts about the standard itself (for Alex; nothing changed): unsized named actions keep every small press release (D240); the optional Singapore case lets eleven asset records through (D231); the tier table has no row for an official's allegation, a company forecasting its own industry, or a research firm reporting a non-public action; a repeated old figure is kept at full weight each time (D243 #6) while a repeat is not new evidence (AGENTS §8). A fourth doubt, that "unknown" loses the "said by the report day" bound, is answered: every record keeps its item's publication day.

Downstream and product:

7. **Nothing downstream has run with role-v42 or role-v51** (no archive in any worktree names `poc-v39` or later). The last whole-path run is one week with role-v22 (`english-v38-nvda-1w-2026-10-28`, D211, $0.23): every story of the week had a page, 4 of 17 pages were duplicates by wording, and the placer left about 60 statements out when near-identical pages competed. Judging was halted by evidence bloat in the three-month run (D206) and has not run at scale since.
8. **Not built:** argument records (steps 5 and 6: a versioned current argument per question for the judge to read); pull mode and the final verdict (how a question is settled at its due day) are earlier drafts.
9. **Not merged:** three stacked branches; the UI serves the sealed ledger through 2026-08-28.
10. **One company:** the prompt is written as a general hedge-fund brain and measured on NVIDIA articles only.

Earlier open defects, unchanged:

- Shared by both matching engines (log row 49): the same figure stated in another document is often judged new (2–3 of 30 sampled new decisions); one matter can end up in several groups (the capex matter holds two groups in the Jev arm, three in the control); a decision naming a candidate of the same answer breaks a chain or duplicates a thesis (7 decisions over all ledgers, all generative); an empty `original_who` on both sides reads as the same party in the writer's rule; two names for the same population are sometimes kept apart (2 merge misses of 9 with Jev).
- Aggregate theses multiply under the `ai-capex` theme: the Jev arm holds nine 2026 aggregate-spending theses, each a different population under the gold's rule. Whether such variants deserve separate theses is the analyst's judgement, not an identity defect; it is recorded for a product decision.
- The classification simulation keeps the limits in [the preserved defect list](research/2026-10-25-english/classification-existing-defects.txt); a passing simulation is not classification acceptance.
- Corpus: 97 official notices with 56 body and filename collisions need the recorded re-fetch before a rebuilt corpus is relied on.
- The older intermittent search-test failure is untraced; the Docker external-connectivity restriction needs a current check before a container model run.
- Parallel day: the spend cap is checked per committed item, so in-flight early requests can pass it by at most the worker count's calls; the cap counts archived calls, not a retried attempt whose reply was lost (as for the OpenAI client). Re-prepared requests cost about 24% more per day.
- Not yet done: the service and UI switch to the English ledger (a new search index), `matching-v4` for dependencies in the generative matcher.

Pull mode and the final verdict remain earlier drafts to redesign together. The decided rule freezes the current state and reasons at the due date and closes the thesis. Upstream supply and human-review handling remain deferred.

## Adopted implementation

- D155: reference lists no longer veto candidates; full-match period handling, exact scopes, event identity, same-answer coalescing, old-key trust and atomic write and resume.
- D159: an item's accepted extraction answers the request built after every earlier item finished writing.
- D172, D181, D183: the parallel day (`hivemind.parallel_day`), the replay's default (`scripts/replay.py --workers 1` runs serially): later items' extraction requests are prepared early and prepared again right after any commit that changes them; each item accepts only a byte-identical request at its turn; matching questions within an item run concurrently and apply in order; one writer.
- D163–D166: the English runtime (`vocabulary.py`, canonical values with legacy conversion on read), the fresh English library, research groups declared during extraction with aliases and decided by names in code (`views/groups.py`).
- D167–D169: no hard-coded identity; the measure vocabulary gains `market_size` and `project_cost`; the Jev engine (`views/jev_matching.py`, client `jev.py`) with the PRD's replacement definition, the shared succession rule and an answer for "the same quantity, another period"; a repeat may name the piece shown for the same evidence under another thesis.
- Idea service: the adopted two-call contract `poc-v9` / `idea-v7`, reasoning `none` (D135/D145); limits in the [Idea specification](poc/idea-card.md). The service still reads the sealed Chinese ledger with its search index.
- UI and service: shared thesis schema and adapter, cards, history chart, evidence, drawer and graph routing; historical reads, search, numeric claim evaluation and thesis bundles over HTTP and MCP ([service specification](poc/service.md)).
- D207–D211: extraction reads, then files (`extraction.read_item`, `extraction.file_reading`); under a ledger-blind version the request depends on the item alone, so the parallel day prepares the read early and files it at the item's turn; the placement call files statements, and a statement filed nowhere is dropped as `no home` (the `unplaced_statements` table is retired). After placement the sift's candidate rule runs again (`extraction.candidates_with_evidence`): a candidate left with none of its evidence is dropped, so no thesis opens without evidence (close-out review; 0 of 222 candidates under poc-v67, 25 of 5,805 over all stored loop answers).
- D236: a quote that differs from the source only by punctuation, quotation marks, footnote markers or case, or leaves out one run of words inside one sentence, is stored as the exact source passage (`extraction.repair_quote`); anything else is refused.
- The year rule reads the universe's year forms (`universe.parse_year`, so FY29 is FY2029) and counts a fiscal year in the company's own fiscal years (`universe.fiscal_year_of`, shared with the fiscal note; NVIDIA's FY2028 in July 2026 is next year); an event question that names its quarter is not a quarterly number.
- role-v13..v15 alone name `shared_quantity`; every later prompt version gets the current four opening reasons with no code change (`extraction.SHARED_QUANTITY_VERSIONS`).
- Tests read no credential: `tests/conftest.py` makes the model and Jev key readers refuse, and the collision judge sends with the caller's transport.
- Preflight (`scripts/preflight.py`) verifies each stored extraction request against its archived configuration and source (the first `MAX_TEXT_CHARS` characters, as production sends) before replaying its answer through the current checks; a request it cannot rebuild (a Chinese version, v17's paragraph accounts) is counted and named, not fatal; the item header is one function (`extraction.item_header`).
- The placement setting is checked before the paid extraction call; the credential guard in tests raises `pytest.fail`, which the pipeline's `except Exception` cannot swallow.

The [pipeline overview](poc/pipeline-plan.md) separates the implementation from the design requirements.

## One next task

The handoff plan with every open task, the principles and the quantitative criteria is [`handoff-plan-2026-10-30.md`](research/2026-10-29-ledger-standard/handoff-plan-2026-10-30.md).

**Fix the record-field class (open defect 1) through the class loop, on the development set with the test set scored once; then, on Alex's go, run the whole pipeline once with the result over the three-month NVIDIA window and read what placement, matching and judging do with it.**

## Parallel day (D172–D183)

The replay runs the parallel day by default (D183: Alex chose it to converge faster); `scripts/replay.py --workers 1` runs the serial path, needed to resume a day a serial run left unfinished. Measured live on the complete July 27 day (53 items), three serial against three parallel trials interleaved ([result](../poc/reports/2026-10-26-e2e-parallel/results.md)): median 501.8 s → 112.5 s, **4.46× end to end**, 5.91× for item work; daily judging (~37–40 s) is the same code in both modes. Every trial's audit is clean; each parallel trial's runner accepted exactly the rebuilt exact-prefix request for all 53 items; each trial's answers replayed through the other mode give an identical ledger. Drift from the recorded sequential golden is inside the serial trials' own spread. The product entry point (`--workers 16`) ran the same day live in 135.5 s with the same checks clean. On recorded answers the parallel day equals the golden in all ten tables (D180, and again on the promoted module).

Fifteen consecutive days (August 1–15, 221 items) with every call answered by one deterministic oracle of the request bytes, at no cost (D182, [result](../poc/reports/2026-10-26-multi-day-oracle/results.md)): the parallel ledger equals the serial one in all 20 product tables, its turns accepted exactly the serial run's 221 extraction requests, and a broken runner was caught. At recorded call durations the fifteen days take an estimated 2.79× less time (2,512 s → 900 s); a busy day gains 3.6–4.5×, a day of a few items 1.5–2×.

What remains of the time is not scheduling: items that depend on the item just before them (~45–60 s), daily judging (D63), and each item's two matching phases in order (~17 s). Ten times end to end on this day would need those to shrink.

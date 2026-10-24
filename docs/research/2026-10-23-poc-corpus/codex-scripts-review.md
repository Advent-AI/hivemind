**Confirmed: the corpus can feed cut or wrong pages, misclassify documents, and finish with missing items.** For example, the stored NAVER article URL ends at `?seq`, losing the article identifier. No files changed.

**1. Original text and dropped content**

- **Confirmed — Google URLs can be cut.** The resolver extracts URLs with a regex that stops at JSON escapes instead of decoding them. An escaped `?seq\u003d123` becomes `?seq`. This occurs in the stored NAVER result, allowing a non-article page to replace the article. [resolve_gnews.py:63–67](/Users/lchingen/hivemind/poc/corpus/scripts/resolve_gnews.py:63).

- **Confirmed — “Whole page” removes potentially readable content.** `page_text()` deletes `noscript`, SVG and template contents, beyond the plan’s “scripts and styles only.” Text alternatives and chart labels disappear. [common.py:88–100](/Users/lchingen/hivemind/poc/corpus/scripts/common.py:88); [plan:26](/Users/lchingen/hivemind/docs/poc/corpus-plan.md:26).

- **Confirmed — Cut text can become pipeline text.** Extra-page harvesting selects filtered paragraphs; NVIDIA EDGAR harvesting strips headers, footers and other elements. Assembly falls back to these `.txt` files whenever `.full.txt` is absent. Regeneration repairs this only when run successfully. [harvest_extra.py:31–36](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_extra.py:31), [harvest_edgar.py:93](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_edgar.py:93), [assemble.py:106–112](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:106).

- **Confirmed — Downloads are silently truncated at 8 MB**, retaining successful HTTP status. No truncation flag reaches assembly. [common.py:40–53](/Users/lchingen/hivemind/poc/corpus/scripts/common.py:40).

- **Confirmed — Material is deliberately omitted.** Topic RSS keeps only the first `per_day` results; saturated GDELT hours lose everything beyond 250; SEC document selection excludes PDFs and other formats; TrueNorth news uses capped searches without pagination, and its downloaded filings are never assembled. [harvest_gnews_topics.py:67](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_gnews_topics.py:67), [harvest_gdelt.py:74–88](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_gdelt.py:74), [harvest_edgar_peers.py:57](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_edgar_peers.py:57), [harvest_truenorth.py:39–52](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_truenorth.py:39), [assemble.py:458–459](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:458).

**2. Publication day**

- **Confirmed — GDELT uses discovery time as publication time.** Articles discovered after their publication day receive the discovery day; boundary filtering can also exclude them. The fetched page’s date is ignored. [assemble.py:234–246](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:234).

- **Confirmed — Google and TrueNorth dates override original-page dates.** Any item whose RSS `pubDate` or provider timestamp reflects an update, indexing or aggregation receives that date. Fed harvesting likewise uses RSS dates without checking the article. [assemble.py:164–186](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:164), [assemble.py:383–400](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:383), [harvest_official.py:85–94](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_official.py:85).

- **Confirmed — New York conversion is fixed at UTC−4.** That is correct during July–October 2026, but winter timestamps between 04:00 and 04:59 UTC receive the following day incorrectly. Naive timestamps are also either accepted without conversion or interpreted using the machine’s timezone. [common.py:143–149](/Users/lchingen/hivemind/poc/corpus/scripts/common.py:143), [harvest_nvblog.py:50–53](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_nvblog.py:50), [harvest_official.py:74](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_official.py:74).

- **Confirmed — Page-date fallback can select unrelated dates.** It accepts the first `<time>` anywhere, then loosely matched date elements or prose. A navigation timestamp before the article wins. Missing/unrecognised dates are recorded as outside-window and skipped forever. Newsroom `lastmod` only orders candidates; blog `lastmod` filters candidates and can therefore omit pages before examining their actual date. [common.py:134–159](/Users/lchingen/hivemind/poc/corpus/scripts/common.py:134), [harvest_nvidianews.py:62–75](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_nvidianews.py:62), [harvest_nvblog.py:59–61](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_nvblog.py:59).

- **Confirmed — SEC avoids the acceptance-date mistake.** Both harvesters retain SEC `filingDate`, and assembly uses it. An after-17:30 acceptance is therefore dated by the supplied legal filing day, not its acceptance timestamp. No contrary conversion is present. [harvest_edgar.py:35–40](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_edgar.py:35), [assemble.py:119–141](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:119).

**3. Loss, duplication and resumability**

- **Confirmed — Deduplication can merge distinct articles.** Same-day normalised titles are matched without author identity. URL canonicalisation deletes every parameter beginning `ref` or `src`, including potentially meaningful identifiers. [assemble.py:74–85](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:74), [assemble.py:432–452](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:432).

- **Confirmed — Genuine copies remain unlinked.** Only news participates; content hashes are never compared. Company releases repeated across EDGAR, newsroom and extras remain separate. Copies do not inherit the original’s category, merge objects or consolidate publication dates. [assemble.py:432–453](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:432).

- **Confirmed — Multiple-topic identity is lost.** Resolver queues each Google link once; assembly keeps each resolved URL once. Later topic/object labels disappear. [resolve_gnews.py:94–104](/Users/lchingen/hivemind/poc/corpus/scripts/resolve_gnews.py:94), [assemble.py:372–401](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:372).

- **Confirmed — Failures become permanent completion.** EDGAR records filings despite failed document/index fetches; extras record failed URLs; topic harvesting saves incomplete days. GDELT marks parent ranges done even when children failed. Subsequent runs skip these gaps. [harvest_edgar.py:80–102](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_edgar.py:80), [harvest_extra.py:39–43](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_extra.py:39), [harvest_gnews_topics.py:60–74](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_gnews_topics.py:60), [harvest_gdelt.py:69–81](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_gdelt.py:69).

- **Confirmed — Writes are not crash-safe or process-safe.** JSON is overwritten directly; JSONL appends have no interprocess lock. Raw-file existence can suppress repair after a crash before its text companion is written. Assembly deletes the existing database before rebuilding. Concurrent runs can overwrite manifests or expose incomplete files. [common.py:163–180](/Users/lchingen/hivemind/poc/corpus/scripts/common.py:163), [harvest_edgar.py:85–97](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_edgar.py:85), [assemble.py:461–471](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:461).

- **Confirmed — Reassembly changes prior results.** New raw data can change `copy_of` selection; duplicate IDs are silently replaced; `supersedes` remains empty. No previous database/version survives. [assemble.py:89–91](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:89), [assemble.py:436–452](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:436), [assemble.py:469](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:469).

**4. Classification**

- **Confirmed — 8-K attachments use the wrong test.** Every EX-99 becomes T1 if the filing lists 2.02, whether that section references it or not. Other referenced exhibit numbers cannot receive T1. Non-earnings presentation attachments fall to T6 instead of T5. [assemble.py:125–135](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:125), [assemble.py:261–271](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:261).

- **Confirmed — Exhibit-number matching is too broad.** Prefixes `EX-2`, `EX-3`, `EX-4`, `EX-10` also match EX-21, EX-23, EX-31, EX-32 and EX-101, incorrectly assigning T3. [assemble.py:132](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:132).

- **Confirmed — 6-K earnings attachments become T6.** There is no 6-K earnings branch. Correct 10-Q/10-K handling exists; peer 20-F handling also correctly selects T2. [assemble.py:263–271](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:263).

- **Confirmed — News-channel classification ignores necessary distinctions.** Company/wire releases become T7 instead of T6/T1; media analysis becomes T7 instead of T8; analyst transcripts become T8 instead of T9; official accounts on `x.com` become T8 rather than T10. No series routing exists. The stored database contains 50 company-typed T7 rows. [assemble.py:63–71](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:63), [author-table.json:13–17](/Users/lchingen/hivemind/poc/corpus/scripts/author-table.json:13).

- **Confirmed — Blanket source tags misclassify known material.** All Fed press releases receive T11, including stored enforcement actions and application approvals that require T10. All NVIDIA newsroom releases receive T6; the stored Q2 earnings release is T6 there but T1 in extras. [harvest_official.py:20–22](/Users/lchingen/hivemind/poc/corpus/scripts/harvest_official.py:20), [assemble.py:199](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:199), [extra-urls.json:11](/Users/lchingen/hivemind/poc/corpus/scripts/extra-urls.json:11).

**5. Operational failures**

- **Confirmed — Body-fetch 429s are never retried.** `retries=0`; every result enters the index, and index membership means done. Resolver refusals sleep without retrying that item immediately; two failed runs exhaust it permanently. [fetch_bodies.py:75–84](/Users/lchingen/hivemind/poc/corpus/scripts/fetch_bodies.py:75), [fetch_bodies.py:114–136](/Users/lchingen/hivemind/poc/corpus/scripts/fetch_bodies.py:114), [resolve_gnews.py:101–127](/Users/lchingen/hivemind/poc/corpus/scripts/resolve_gnews.py:101).

- **Confirmed — Worker failures do not fail the run.** Body workers catch exceptions and continue; persistent exceptions remain pending and can loop forever. Resolver thread failures during output writing do not propagate through `join()`. [fetch_bodies.py:174–204](/Users/lchingen/hivemind/poc/corpus/scripts/fetch_bodies.py:174), [resolve_gnews.py:133–148](/Users/lchingen/hivemind/poc/corpus/scripts/resolve_gnews.py:133).

- **Confirmed — Fetcher completion is unrelated to completed days.** It requires 728 completed ranges. Quiet completed days contribute only one each; partial splitting can inflate the count without completing every day. [fetch_bodies.py:199–201](/Users/lchingen/hivemind/poc/corpus/scripts/fetch_bodies.py:199).

- **Confirmed — Overnight completion is unreliable.** `pgrep -f` can match unrelated processes and waits without deadlines. Empty body passes never log `pending 0`, so parsing reuses stale counts. Fixed round limits eventually proceed regardless; GDELT and TrueNorth are not awaited; command failures do not stop the final “done.” [overnight.sh:14–41](/Users/lchingen/hivemind/poc/corpus/scripts/overnight.sh:14).

- **Suspected — Slow responses can hold workers indefinitely.** Resolver reads have neither a size cap nor an overall deadline; socket timeout is not a total-request deadline. [resolve_gnews.py:43–46](/Users/lchingen/hivemind/poc/corpus/scripts/resolve_gnews.py:43).

**6. `feed`**

- **Confirmed — It does not mean “original document, whole.”** It means coverage is `full` **or `partial`**, with at least 200 characters. The stored database has 23 partial rows fed. HTTP-200 boilerplate, wrong pages and truncated downloads qualify; complete originals shorter than 200 characters do not. [assemble.py:97](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:97), [fetch_bodies.py:118–131](/Users/lchingen/hivemind/poc/corpus/scripts/fetch_bodies.py:118).

- **Confirmed — Explicit provider summaries and Google-title-only rows are excluded.** However, cut `.txt` fallback can still be fed under inherited coverage. Readable PDF originals are excluded from body fetching altogether. [assemble.py:179–182](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:179), [assemble.py:407–415](/Users/lchingen/hivemind/poc/corpus/scripts/assemble.py:407), [fetch_bodies.py:30–50](/Users/lchingen/hivemind/poc/corpus/scripts/fetch_bodies.py:30).
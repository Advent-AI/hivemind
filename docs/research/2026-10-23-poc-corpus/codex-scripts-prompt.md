Read-only code review. Change nothing.

Scope: `poc/corpus/scripts/*.py`, `poc/corpus/scripts/*.json`, `poc/corpus/scripts/overnight.sh`, and the plan `docs/poc/corpus-plan.md`. Context: `docs/prd/02-classification.md` (the item fields and the rule classifier these scripts imitate for a test database), `docs/poc/corpus-plan.md` (what the corpus must be: original material only, two classes plus official and noise, every item dated by its own publication day in New York time, copies kept and pointed at the original, nothing summarised or filtered by content).

Answer, concretely, with file and line:
1. Where could an item's text be something other than the original document as published (a summary, a cut, a page other than the article, boilerplate replacing content)? Where is content dropped?
2. Where could the publication day be wrong (time zones, sitemap lastmod versus page date, RSS pubDate, SEC acceptance after 17:30 ET, GDELT seendate), and which items would be mis-dated?
3. Where could an item be lost or duplicated: dedup keys (canonical URL, normalised title), resumability (progress files, index.jsonl, manifests), concurrent writers to the same file, a crash mid-write, re-running assemble after more raw data lands?
4. Classification against 02-classification: are the T tags assigned by the rules the PRD states (8-K 2.02 exhibits → T1; other exhibits by exhibit number; 10-Q/10-K/20-F → T2; 6-K? transcripts → T4; company blog/newsroom → T6; media → T7; analyst/individual authors → T8; official actions → T10; macro statistics and central bank material → T11)? Name every mis-tag you can prove from the code.
5. Operational failure modes in the harvesters: rate limits and backoff, unbounded waits, infinite loops, a 429 that is never retried, threads that swallow errors, the overnight driver's stop conditions (pgrep patterns, "pending" parsing).
6. The `feed` flag: is "original document, whole" exactly what makes an item feed=1? Name any case where a non-original (provider summary, Google title only, truncated page) would be fed, or an original would be excluded.

Under 1,800 words, bullets, each marked Confirmed or Suspected.

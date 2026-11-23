# Acceptance protocol for the clean Steps 1–2 (draft for council, 2026-11-09)

Governing decisions: D380–D386 (`docs/DECISIONS-log.md`); Alex's thesis line "50 篇里最多 2 个" (AskUserQuestion, 2026-11-08);
the agreed protocol in `LOG.md` §40. This page fixes everything before any article of the fresh set is sent.

## 1. What is accepted

The configuration c8, frozen as these files:
- `arms/c8-system.txt`, `arms/c8-closing.txt` and `arms/c8-schema.json`;
- DeepSeek Flash at high effort, a 64,000-token output cap, and one resend for a format failure or a cut answer (D380);
- Step 2 and Step 3 as in `clean-arch/step2/compare.py` and `clean-arch/step3/library.py`.

Their sha256 values are written to `SHA256SUMS` in each run folder before launch.

## 2. The fresh set

D386 asks for "NVDA articles no run has used".

- **Eligible:** an item of `poc/data/items-nvda-2026-07-01-10-27.sqlite` that passes the runner's own selection rules. That means:
  - the NVDA ticker tag is present;
  - the text is present;
  - the feed flag is 1;
  - the item is neither a copy nor superseded.
- **Order:** by publication day; then by `published_at` in UTC when its date equals the publication day, or else 23:59:59Z of that
  day; then by input id.
- **Choice:** the first 50 unused items from 2026-08-30. The procedure is `select_fresh.py`.
- **Used:** the item's full id appears in any file under `poc/data`, `clean-arch`, `docs`, `reports`, `research_notes` or
  `../tn-hivemind/docs`. The census scanned 10,871 files. It found every dev id (115 of 115) and every test id (26 of 26). The match
  takes whole ids, including ids with a second colon.
- **Not counted as uses:** these files hold the source articles themselves, and no model read an article in them. The list is in
  `selection.json`.
  - the source databases and their copies;
  - five corpus-wide page-cleaning inventories (HTML extractor output and character counts).

  **Every pipeline run counts as a use**, old or new. The old pipeline's whole-window runs processed every article up to 2026-08-29.
  The 2026-11-05 seven-day run listed every article from 2026-08-29 to 2026-09-04.
- **Two earlier drafts were withdrawn before any reader saw them.** Both were July sets.
  1. The first was ordered by (day, id).
  2. The second excluded the old whole-window runs from the use census. Council B blocked it because those runs used the articles
     (`council/am-codex.md`).

  The withdrawn July manifest is kept outside the repository.
- **Result:** 50 news articles from 2026-09-05 (18), 2026-09-06 (22) and 2026-09-07 (10). Every item has a stated time. The text has
  a median of 4,040 characters and a maximum of 17,829. Inside these three days, 8 used items were skipped; each is listed in
  `selection.json` with its files, which come from the source-cleaning checks of 2026-11-07. These days are a weekend and the US
  Labor Day holiday: they hold no NVIDIA blog or newsroom post. The topics are:
  - the Hugging Face acquisition, covered by several outlets;
  - DLSS 5;
  - RTX Spark;
  - Groq racks;
  - the Wistron share sale;
  - the Nscale funding talks;
  - China competitors;
  - many stock-commentary pieces.
- **Frozen:** `poc/data/clean-acceptance-2026-11-09/manifest.json`, sha256 `81f3f579…bd688`. The runner accepts it.
- **What a result supports:** a real three-day stream of about 50 articles, with its repeats. It says nothing about other months.
  The ordering inside a day is approximate: stored times are coarse, and ties are broken by id.

## 3. Runs

- **Fresh set.** Step 1 forward from an empty library, then Steps 2–3 forward on its trace. One draw.
- **Dev stability.** Step 1 on the 115 dev articles from an empty library, three draws, each followed by Steps 2–3.
- **Cost estimate.** About $0.0135 per article at published rates (from the c8 check sends), so about $0.7 for the fresh set and $4.7
  for dev ×3, plus embeddings and Step 2 comparisons. The limits are scaled to each run: `max_calls` is 2.2 × the number of articles,
  and `max_usd` is $20.

## 4. Readers

Fresh Codex sessions, read-only; none wrote c8.

- **Before the run, frozen with sha256:**
  - Two readers each read all 50 sources and write three lists:
    1. **Matters.** Per article, the matters an analyst would note under the standard's evidence test (§5.1 and the §5.3 rows; D385:
       target prices and valuation conclusions are not kept), each with its central claim. One matter is counted once per article
       (D250).
    2. **Repeat groups.** Articles that report the same matter, each article marked as a repeat or as a revision (a changed number,
       a denial, a later step).
    3. **Dossiers.** For each repeat group, the details each article adds.
  - A third reader settles every difference between the two readers against the source.
  - The settled lists are frozen.
- **After the run:** the readers judge the output against the frozen lists and the source. They see:
  - each kept item: helpful, noise or wrong;
  - each opened thesis, against the standard's opening tests;
  - each link;
  - each Step 2 merge;
  - each repeat or revision that search missed;
  - retention for each dossier.

  A third reader settles disputes.
- **Calibration.** Before the readers' counts are read, I hand-check two articles whose answers I traced myself.
- **Batches.** Every reader call covers at most ten articles. A single 50-article call stopped after 5 (LOG §42).

## 5. Lines, declared before the run

| Line | Pass |
|---|---|
| Helpful matters kept | ≥ 81.2% of the settled matter list. A matter counts as kept when a kept item states its central claim; a missing secondary detail is a field note, not a miss; several items for one matter count once |
| Wrongly opened theses | ≤ 2 in 50 (Alex). A thesis is wrong when it does not meet the standard's four reasons, when it is small, when it duplicates an open thesis, or when it is a fragment of one bet |
| Search | ≥ 90% of the settled repeat pairs (a later member and an earlier member of the same group; a matter may belong to two pairs) reach the earlier member's group among the search candidates |
| Wrong merges | ≤ 2% of merges, none unjudged |
| Detail retention | Grouped libraries keep no fewer settled dossier details than ungrouped records |

Every line reports its denominator.
- A line with no cases is reported as **unexercised**, not passed.
- A case still disputed after the third reader counts against the system for the verdict, and is reported both ways.
- A failed article (a format failure after one resend) counts as missing every matter it carries, and is listed.
- A pending later link counts as unlinked, and is listed.

**Reported without a line:**
- noise, wrong statements, and items kept without links (with their materiality);
- later-link precision and sampled recall;
- the fields party, date and tier;
- cost and time.

**Excluded in advance:**
- class A financial-measure theses (D382);
- valuation conclusions (D385; the conflict with the frozen gold's conditional-valuation row is disclosed).

**Limits** are set per run:
- `max_calls` is 2.2 × the number of articles;
- `max_usd` is $20;
- `max_seconds` is 21,600. The c7 dev run of 115 articles took less than half of that.

**Dev ×3** decides one thing, declared now: whether c8 clears the earlier line in every draw, rather than in one lucky draw. The line
is helpful ≥ 190 of 234 on the frozen golden-v5 dev gold. The scorer is a lead, and I read the traces myself. Each draw is reported,
never only the best, together with:
- the question measure against must_open, may_open and must_not;
- Step 2 lines 1 and 2.

## 6. Known items carried in, disclosed

- **The lidar boundary.** In one c8 check send, the model opened a lidar phase-out policy question that the gold lists as must_not.
  This is recorded and watched; no rule was added.
- **The supplier statement.** It is now kept without links (D383). Alex's earlier ruling "丢掉" came before D383, so the overlap goes
  to him as a report.
- **Later linking (c6 Step 2 run).**
  - 0 of 40 sampled rejected pairs should have been linked: both readers agreed.
  - 2 of the 3 accepted pairs were judged wrong by both readers. Both link the company's overall revenue estimates to the thesis
    "will NVIDIA's $119 billion in supply commitments be matched by enough AI demand"; the comparison scored one of them 0.55.
  - Traced: in the same run, Step 1 filed the company's reported revenue and its next-quarter guidance under that same thesis at
    extraction time (2 of its 7 direct links). Later linking therefore applies the boundary Step 1 already applies; the readers drew
    it more strictly.
  - The same class in earlier runs: the c4 run had 5 such links before the "informs" question gained its company-wide sentence, and
    its two reruns had none. c5 and the test run had none of this class.
  - The boundary (do company-wide results inform a thesis about demand against commitments?) is reported, and no rule is added. It is
    measured again in acceptance.
- **Quotes.** 2 of 288 kept items carry a passage that was not verified: one extra quotation mark, and one added word. This is the
  known one-word rewrite class; the item is kept and the passage is marked unverified.
- **The test set is exposed.** Golden-v5 test was used across configurations (D386). Its scores are not acceptance.

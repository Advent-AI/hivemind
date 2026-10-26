# The three-month NVDA run: data backfill 2026-07-01..10-27, then the pipeline

Alex, 2026-10-27: "需要你先开始把原始数据准备好，和当前nv的数据格式差不多，可以不要找noise进来，就是纯粹从7/1 to 10/27 (today) 的完整数据做补齐，
确认干净之后，开始做抽取入库跑我们的系统"; "不要设价格上限，但是清楚的帮我记录成本".

## What the stored corpus had (2026-10-27 01:00)

- The frozen window database the runs used (`items-window-tags2-2026-10-24.sqlite`) stops its news at 2026-08-21; the corpus
  itself (`poc/corpus/items.sqlite`, assembled 2026-10-25) holds NVDA news to 10-22 (fed NVDA rows: Jul 235 from 07-24, Aug 428,
  Sep 259, Oct 336). Headlines and links existed to 10-24; the page fetch had finished after the frozen database was cut.
- Nothing before 2026-07-24 except EDGAR, the February and May calls and a few bootstrap pages; nothing after 10-22.
- Two defects found by reading the data, both fixed where the data is written (tests in `poc/corpus/scripts/test_labels.py`):
  1. The Google News link resolver cut the publisher URL after the quote that closes Google's JSON string: 32,011 of 34,430
     stored links end in `",1]` or carry a second URL. Most servers served the right page anyway; some served their shell
     (an archive page, a consent wall) with status 200, which passed as a full article. `resolve_gnews.decode_url` cuts at the
     escaped quote; `common.clean_resolved_url` cleans the stored links when the corpus is assembled (the page was fetched
     under the stored link, so the lookup tries both).
  3. The same cut links explain most of the 20,858 pages recorded with no body: servers answered the garbage path with
     404 (11,228), a redirect (3,478), 400 or 403, so in September only 319 of 1,848 NVDA-topic links had a whole page.
     `fetch_bodies.listed_urls` now lists the clean form of a link unless the stored form already served the whole page
     (`HIVEMIND_TOPICS=nvda` limits a pass to the run's topic): 3,757 clean links fetched on 2026-10-27 02:11.
  2. 284 NVDA rows fed as originals were such shells (38 groups; one outlet's archive page served for 111 headlines).
     `assemble.mark_shells`: identical whole-page text at different URLs of one site is the site's shell, coverage `shell`,
     not fed.

## The backfill

- Window from the environment (`HIVEMIND_WINDOW_START/END`, `common.py`); every harvester is resumable.
- Google News headlines per day (RSS, 100 per day at most) for 07-01..07-23 and 10-23..10-27: 1,259 + 400 headlines; link
  resolution runs with 6 workers (Google refuses bursts; about 50 links a minute); page fetch with 16 workers, one request per
  domain every two seconds.
- GDELT article lists for the same ranges (direct publisher URLs; the API throttles, 45 s waits).
- NVIDIA blog and newsroom through their sitemaps (pages first recorded as outside the old window are visited again when the
  new window covers them), EDGAR (10-K/10-Q/8-K and exhibits), TrueNorth stories (90-day window, so 07-29 onward), earnings
  transcripts (the August 26 call; none in September or October).
- Not used: DeepSeek Search/Fetch. The earlier probes and a 10-headline probe today ($0.006): a bare day-bounded "nvidia" query
  returns nothing, a quoted headline finds the story on another outlet half the time, and Fetch fails on most news sites.
  It is a supplement for targeted questions, not a replacement for the listing + fetch chain.

## Clean checks before the run (`check_corpus.py`)

Per-day fed NVDA counts with empty days named; per channel and month; text length quartiles; duplicate texts among fed
originals; publication day against the source timestamp; language; rows outside the window. Then `review.py` for the manifest.

## The run

`poc/data/english-v29-nvda-3m-2026-10-27/run-all.sh`: `poc-v29` (extraction v12, Jev with the collision judge, judging with the
theme block, shared quantities by key), `--only NVDA`, 2026-07-01..2026-10-27, no spending cap, the ledger starts empty on
July 1 (a pure window, as asked: no February or May seed). Costs: `cost-ledger.md` beside the run, from `scripts/cost_report.py`.

## What the clean check found and what was fixed (2026-10-27 02:00–04:25)

Three freezes of `poc/data/items-nvda-2026-07-01-10-27.sqlite` (the first two moved aside as `…before-fetch2` and
`…before-binary-rule`, never used by a run):

| freeze | fed NVDA items | finding | fix (at the writer, test first) |
|---|---|---|---|
| 02:08 | 1,717 (Sep 138) | 1,509 September links had no fetched page: the page pass had been cut | second clean-link fetch pass (3,757 links, 02:11–04:19): 2,563 full, 640 blocked, 371 none |
| 04:20 | 4,204 | 116 fed rows (10 NVDA) were JPEG/PNG/GIF files and 7 (3 NVDA) gzip streams, decoded as text and passed the stub bar; 53 "duplicate texts" were NVIDIA-blog posts listed again by Google News, already marked copies (dispatch routes a copy as merged, never extracted) | `common.page_text`: a body starting with a file signature has no page text (`test_labels.py::test_a_binary_body_has_no_page_text`, 14 pass); `check_corpus.py` counts duplicates among non-copies |
| 04:24 | 3,852 (copies excluded) | exactly the 13 binary rows left; nothing else moved; 0 duplicate texts, 0 non-English, 1 empty day (10-27 itself), text max 174k chars (the 10-Q) | launched 04:25 |

Monthly fed NVDA items (copies excluded): Jul 725, Aug 640, Sep 1,096, Oct 1,391; per day min 3, median 30, max 91.

## What is recorded, and pausing (Alex, 2026-10-27 04:50: "务必确保数据是完整没有损坏且能够随时暂停，继续的")

Where everything lives, in the run folder `poc/data/english-v29-nvda-3m-2026-10-27/`:

- `archive.sqlite`: every model request and answer (extract, match, judge), one row per distinct request, committed as it
  lands; a repeated identical request is answered from here without a network call (`model.Archive`).
- `views.sqlite`: the ledger. Append-only (triggers refuse update and delete): one row per processing step per item
  (`processing_steps`: dispatched → extracted → matched → written → handed_over), handovers, views, evidence, judgements,
  `days_completed`. Rollback journal, every step its own commit: a stop between commits leaves a consistent file.
- `manifests/day-<day>.json`: the parallel runner's record of a day's inputs, source digest, configuration and runtime;
  a resumed half-day must match it (`parallel_day._manifest`).
- `run.out` (one line per day with counts and cost), `run-all.log` (launch, pause, resume stamps), `run.pid`.

Pausing: `pause.sh` (SIGTERM to the replay; the in-flight calls are the only loss). Resuming: `launch.sh` again; replay
continues after the last completed day, and inside a half-done day every item already handed over is routed `skipped`,
an item stopped mid-way resumes at its next step (`dispatch.route`), and judgements already committed for the round are
not re-sent. Proven live at 04:54–04:56 (ledger row above): 22 days complete before, 2026-07-23 resumed with 0
re-extractions, `integrity_check` ok on both files before and after, no item with two extracted rows, no duplicate
(view, round) judgement, no day completed twice.

## Stall at 2026-08-07 (05:30) and what was fixed

The day's judging raised `judgement refused twice: v11: push on e675 which is not under v11`. Traced on the archive ($0):

| mechanism | census | fix (test first, `tests/test_theme_block.py`) |
|---|---|---|
| A. A code-refused judgement answer was archived under its request's hash and served again to every identical later request, so a resume replayed the same two refused answers and failed again (schema-refused and malformed rows already carry a suffix that keeps them out of lookup; code-refused ones did not). | every resume after a `JudgementRefused` would loop | `model.Archive.retire(call_id)`: the row stays on record, its hash gains `:refused:`; judging retires both refused attempts. `test_a_judgement_the_code_refused_is_not_served_from_the_archive_again` (reproduces the stall, fails without the fix). Preflight part A lists these rows. |
| B. The request's closing line said "cites_views only the dependency thesis ids listed above" when the thesis had no dependency list; with the theme block in view, the theme ids were the only thesis ids shown, and the model put them in cites_views. | 4 of this run's 5 retried first answers (r4: 0 retries, r5: 1) | the closing line names the set that exists: "cites_views must be empty: this thesis depends on no other thesis" when there is none, and with themes "a theme id goes only in theme_pushes, never in cites or cites_views". Closing line 148 → 241 characters when both apply; a stray ".;" removed. |
| C. A push on an evidence id not shown (e782 toward_first, e675 none): slips when the evidence list runs to 300+ ids. | 2 of 316 judge answers | none: the check stays (closed set); with A a resume re-samples. The driver is the evidence list's growth, below. |

Recovery: after a code change the parallel runner refuses to adopt the half-done day (its manifest hashes the package), so 2026-08-07
was finished with `--workers 1` (`finish-0807-1.out`: resumed after 08-06, 7 items skipped, judged 25, $0.05) and the parallel run
relaunched from 08-08. `pause.sh`/`launch.sh` unchanged.

Finding for Alex (not changed): evidence in force per thesis grows without bound (08-07: v6 504 items, v11 333, v22 133); 40 of 316
judge requests were over 30k tokens (max 67k). Cost and slips scale with it; what stays "in force" is a design choice.

## D198 applied mid-run (06:42–06:46)

Days 2026-07-01..08-18 were judged under `poc-v29` (judging-v4, everything in force); from 2026-08-19 under `poc-v30`
(judging-v5, evidence in view: arrivals within the last five judgements + the basis cited by the last ten). The ledger records
the configuration checksum on every judgement, so the two regimes are separable in any later reading. Design, census and the
arm-beside-control run: `docs/research/2026-10-27-evidence-in-view/`.

# Architecture benchmark: the split extraction against the frozen one-call extraction (written and hashed before the paid draws)

2026-11-06. Alex, 2026-11-05: "I want you to kind of still benchmark on, you know, our new extraction architecture to see if it's the right way and
approach. Use both Codex and yourself to discuss and review after you have seen the results until you have hit a consensus." This is plan-final
C-8.1, the historical comparison on the frozen ruler. C-8.2 (an unseeded production-shaped run on a held-out window) needs a reference only Alex
opens. It is not run here, and this benchmark alone does not complete the plan's acceptance. Revision 7 answers Codex's rounds 7 to 12
(`docs/research/2026-11-05-production-plan/r7/` to `r12/`).

## The question

The split reads each item with two calls on the same snapshot of every open question:
- A proposes new questions.
- B files evidence under existing questions.
- Record preparation then completes A's questions.

How does the whole split architecture compare with the frozen one-call path on what the frozen ruler measures, and does it fix what it was built for
(duplicate and low-value new questions)? The arms differ in three ways:
- the extraction itself;
- the analyst review prompt (the split runs collision-v5 with its relation definitions, the control collision-v2);
- execution (the split runs items one after another on the latest library, D375; the control runs the parallel day on the day-start list, D251).

Matching (Jev), the writer and daily judging are the same code. An outcome is attributed to the architecture as a whole, never to the extraction
alone.

## What runs

| Part | Arm | Config | Draws | Folder (`runs/` here) |
|---|---|---|---|---|
| window (dev) | split | `poc/config/poc-split-v3.json` | 3 | `split-v3-d1..d3` |
| window (dev) | control, same day | `poc/config/poc-v108.json` | 3 | `control-v108-d1..d3` |
| test articles | split | as above | 3 | `test-split-d1..d3` |
| test articles | control | as above | 3 | `test-control-d1..d3` |

- **Window draws** (`bench_run.py`): 2026-07-01..07-14, NVDA.
  - Items: the database the r10 draws read (`57bc2544…`).
  - Starting ledger: every draw copies one fixture ledger (`fixture/views.sqlite`, sha256 `eadb16a0…`). It holds the 22 frozen seed questions
    (`poc/seeds/nvda-2026-07-01-v2.json`, `fca16f42…`) as a labelled measurement fixture. Its seeded state is identical, table by table, to that
    of the stored draw r10-control-v108/d1. `scripts/replay.py` keeps refusing seeded ledgers (D370).
  - Cap: $5 a draw.
  - The control runs the parallel day with 8 extraction workers and 8 Jev workers, as r10 did; the split runs items in sequence with 8 Jev workers.
    These are the settings each configuration's entry point uses.
- **Test draws** (`bench_test_articles.py`): golden-v5 test's 30 held-out articles (2026-09-01..10-24, outside the window).
  - Each article is read on its own against the same fixture, so both arms see the 22 seeds, each by its own production rule: the control sees
    its objects' questions open at the day's start, the split every question open before the item.
  - Each draw has its own archive, so every request is sent again in each draw.
  - What is scored is the extraction stage only: the checked handover.
- **Pinned and refused on mismatch:** each draw's manifest records, plus the names of the changed files, the sha256 of:
  - the configuration and every prompt file it names;
  - every `src/hivemind` module;
  - every script of this folder;
  - `poc/universe.json` and the seed file;
  - the fixture and the items database;
  - the scoring code it calls (`score_gold.py`, `final_scores.py`, `score_ref.py`, `score_judgement.py`);
  - both golden-v5 files, the judgement gold and the extraction standard page.

  **One rule for provenance:** a scored draw is a paid draw, made by this folder's harness, in a folder that held no ledger and no archive when it
  began. It keeps one mode and one set of pins for its whole life.
  - The harness refuses a resume whose mode (offline gate or paid draw) or pins differ from the folder's first manifest.
  - An archive may be imported only in the offline gate.
  - `bench_measure.py` refuses to score a run without this harness's manifest, a run holding any offline entry, a run whose pins name other
    scoring files or golds than those it scores with, and any two runs that pinned different versions of a file both use (code, universe, seeds,
    fixture, items, scoring, and the prompt files both configurations name). Only a file one run alone pinned may differ: its configuration and
    the prompts only it names.
  - The cross-run check compares every file across all runs that pinned it, whatever their order.
  - The scoring helpers' import chain adds another worktree's `src`; the measure and the packet load this tree's `hivemind` first and refuse to run
    if prices or sections would come from elsewhere.
  - Stored runs made before this harness are scored only with `--reference`, which says so in the output. This page, the scripts, both configurations
  and the fixture are hashed in `benchmark-design.sha256` before launch.
- **Cost estimate:** control about $0.77 a window draw (r10). Split about $1–1.5 a window draw (46 items of 2026-08-29 cost $0.25 with judging,
  against a larger library). Test draws about $0.1 each. About $7 in all.

## Before launch (done)

1. **Comparability gate.** The harness replayed r10-control-v108/d1 from its archive, with every unarchived request refused.
   - Run in a scratch copy of this tree with the one writer line restored to the stored draw's code (`runs/gate-v108-d1-offline-stored-writer`):
     every one of the 24 compared ledger tables is identical (views, rungs, keys, switches, evidence and its sources and links, judgements,
     dependencies and their resolutions, revisions, replacements, same claims, successions, handovers, groups and their members and aliases, days,
     late statements, review pool, processing steps, match records, research subjects). `compare_ledgers.py` exits 0.
   - Run in this tree (`runs/gate-v108-d1-offline-r2`): **identical except four dates**, the `revisions.said_day` of 4 of the 6 revision rows.
     That one writer line is where this tree stores the statement day, or blank, as D203 requires (2026-10-28: "the revision path stores the stated
     day too"). The stored draw's code stored the ordering day there. No judging request differs: all 219 were answered from the archive.
   - How the exception is handled: the plan's gate asks that the harness reproduce the product's path. The scratch-copy run shows it does, exactly.
     The four dates are a code difference that D203 decides. Both arms of this benchmark run the D203 writer, so it does not differ between them.
   - The stored draw had seven refused judgements and their retries. The replay answers each refused request once with its refused answer; this
     was checked for this archive only (none has an accepted answer under the same key).
2. **Preflight of the split's stored data** (`scripts/preflight_split.py` on the production-path probe of 2026-08-29/30, the same configuration).
   - Population: 73 items with a successful extraction, each with exactly one stored handover and its input.
   - Requests: 73 rebuilt from the stored snapshot, each found under its identity.
   - Record preparation: 21 rebuilt and found; the other 52 items proposed no question, so had no preparation.
   - Format: the production format check (`model.check_schema`) ran on each of the 167 archived answers replayed; 0 refused.
   - Handovers: 73 rebuilt from the archived answers, each equal to the stored one in full (every evidence and candidate field, drops, groups).
   - 0 refused.
   - Four tampered copies are each refused: a changed source text (the item's requests), a closed question (68 later items' requests), an edited
     archived answer (its record preparation), and a deleted handover (the population check).
   - What it does not prove: the archive keeps each request in sorted-key form only, so the byte order a stored request was sent in is not
     recorded and cannot be checked. The identity check proves the content. This benchmark re-sends no stored request: both arms send through the
     production `model.call`, which builds the dict and sends it in build order.
   - Archived split answers that cannot be replayed (no answer, or refused and retired): none. The split retries no refused answer.
   - `scripts/preflight.py` on the same run: the matching checks judged 793 stored matching records and refused 1. That one is from the pilot's
     starting ledger (sequence 58, not the probe's days): a succession the check reads against the final ledger, in which that same decision had
     already written the successor. Its extraction checks judged none: the split's are `preflight_split.py`'s.
3. **The chance of failing a control against itself.** Six stored draws of the control configuration exist:
   - helpful matters reached: 169, 161, 179, 161, 167, 169;
   - core matters reached: 78, 77, 78, 73, 76, 75;
   - judgement agreements: 15, 15, 16, 15, 16, 14.
   Every split of these six into three against three (20 ordered comparisons, which reuse the same draws and are not independent) gives the range a
   same-configuration difference reaches. The difference of the 3-draw means stays within:
   - helpful: −8 in 19 of 20;
   - core: −3 in 20 of 20;
   - judgement totals: −3 in 20 of 20.
   Six draws give a rough range only. A loss smaller than about 8 helpful or 3 core matters cannot be told apart from draw-to-draw variation.

## How it is judged (`bench_measure.py`, `bench_traces.py`, `blind_questions.py`, $0; three draws each; one quantity per column)

Both window arms are scored at two points of their own path:
- **The extraction stage:** each item's checked handover, which the ledger stores.
- **The product:** the ledger's evidence records.

For each helpful gold matter, the measure reports where it ended: reached, handed over but not written, or not handed over. The test arms are
scored at the extraction stage. Counting follows D372, with `score_gold.same_matter` as the counting aid for the matter test. The extraction
standard's version and page hash, the gold's hash and the D373 gold concern are printed with every score.

**What is reported.** Every number of both arms, regressions first:
- per draw: helpful and core matters reached at both points, not-kept entries written, extras, stored records, articles opened as questions, cost
  and wall clock;
- the judgement's agreements per question and per draw;
- each difference of means beside the same-configuration range of the six stored control draws.
The report states the observed differences and that range. It never claims the arms are equal, nor that one is better beyond what the numbers show.

**When the line stops.** These are not acceptance thresholds: nothing here accepts or promotes the split, which stays Alex's decision (D359). They
apply D355 (Alex, 2026-11-04: "如果有什么不符合hypothesis 的地方你需要终止然后和我说我们重新评估", "if anything does not fit the hypothesis, stop
and tell me, and we re-evaluate"). The hypothesis is that the split loses nothing the ruler measures. The work stops and goes to Alex, with its census
and mechanism, when any of these fall outside the same-configuration range, below the control:
- on the window: the split's mean helpful at the product point (below −8), its mean core (below −3), or its judgement total (below −3);
- on the test articles: the split's mean helpful or core at the extraction stage, below the control's by more than the larger of the two arms' own
  draw-to-draw ranges on those articles.
A judgement question whose agreements drop by two or more is read: its last judgement and the evidence it cites in each draw, by Claude and by a
reader who built neither arm. It is reported with its reasons.

**Read, every time (AGENTS §7.2).**
- `bench_traces.py` writes, for each arm, every helpful matter missed in at least one draw (window and test), with:
  - the gold entry and the source paragraph (marked NOT FOUND when the span is not in the stored text);
  - the item's processing steps (a merged copy or an item outside the feed shows here, the same in both arms);
  - every archived extraction-stage answer of the item in full, with its call id and request hash: the frozen extraction's, or the split's A
    and B and its record preparation. An item whose expected answers are not all present is marked UNREAD with the reason: every section of a long
    item needs an A and a B answer, A's questions need a record-preparation answer, and an archived call with no answer counts as missing;
  - the full checked handover (statements, candidates, drops, groups);
  - the written records in full, with the questions each is linked to.
  On the stored control draws it lists 109 matters missed at least once. Nine of their draw entries have no answer: two articles are merged
  copies of another item, and one is outside the feed.
- Independent readers, given the standard and the gold's own reasons, put every such miss down as the architecture's error (not written, dropped
  by a check, lost after the handover) or the measure's (the matter is there in other words; the gold entry is not in the source). The count of
  each kind is reported per arm.
- Twenty extras and twenty hits of each arm are read from a fixed-seed sample.

**What the split was built for**, read blind by a reader who built neither arm, with the arms mixed and hidden (`blind_questions.py`): every
article-opened question of every window draw of both arms (would the standard open it? is it a duplicate of a question open before it?), and
twenty stored records of each arm (helpful or unhelpful; the attribution fields right).
- Also reported: how many new questions carry a ladder and an analyst check date. The 2026-08-29/30 probe found that record preparation's ladder is
  a coin flip on some questions: the same stored request was re-sent and answered once without rungs, once with five.
- The must_open and may_open counts are a counting aid (`score_ref.same_question`, a 20% word overlap that also matches unrelated questions).
  They are reported, never a stop condition, and the blind read decides.

Codex then reviews the results read-only, round by round, until both agree on the reading. Each round is logged in
`docs/research/2026-11-05-production-plan/review-log.md`. Whether the split is promoted is Alex's decision (D359).

## What this cannot show

- The window starts from 22 seeds. It tests filing against a seeded library and opening questions beside it, not opening from an empty library
  (that is C-8.2).
- The test articles are read one at a time against the seeds, not in a running ledger.
- The judgement ruler does not measure the daily path, or whether evidence was filed under the right question; the blind reads cover part of that.

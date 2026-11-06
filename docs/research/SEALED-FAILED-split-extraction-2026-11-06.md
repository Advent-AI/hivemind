# SEALED — FAILED EXPERIMENT: the split extraction (2026-11-06)

**Status: failed and sealed. Do not run, resume or merge anything here as a candidate for production.** Decision D378 in main
(`/Users/lchingen/hivemind/docs/DECISIONS-log.md`). Alex, 2026-11-06: "我觉得你把拆分版学到的东西，有用的给cherry pick 出来，做一个PRD我们来给到生产版来实验；你现在封存拆分版并且清理赶紧并标注失败的实验吧".
What it taught is carried into main as proposed production experiments in `docs/prd/11-production-experiments-from-split.md`.

Branch `fix/no-preseed-evidence-review`, tag `split-extraction-failed-sealed-2026-11-06`. Nothing was pushed.

## What it was

Each item was read with two calls on the same snapshot of every open question:
- a new-question call (A) proposed questions with their passages;
- an evidence call (B) filed statements under existing questions;
- record preparation then completed A's questions (subject, admission reason, dates, favourable end, ladder, attribution).

It was built in production shape, in this order:
1. `src/hivemind/split.py`, with the split branch of `views/round.py`;
2. `scripts/replay.py` running split configurations item by item;
3. `research_subjects` in the ledger;
4. `scripts/preflight_split.py`;
5. `tests/test_split_extraction.py`.

## Why it failed (numbers)

**Benchmark against the frozen production configuration poc-v108**, three window draws and three test-article draws each, under the design agreed
with Codex (`2026-11-06-architecture-benchmark/benchmark-design.md`):
- Window helpful matters 156, 156, 159 against 166, 170, 162. The difference of −9 falls outside the −8 same-configuration range, so the stop line
  fired.
- Core matters 74.0 against 75.7. Judgement 44 against 47. Cost about 15% higher.
- Questions opened from articles: 44 against 12. A blind reader would open 25 against 6 and not 17 against 6, with 0 duplicates in both. Only 21 of
  the split's 44 new questions had a ladder.
- Test articles: the split was not below production.
- Independent readers put the split's misses down mostly as statements the evidence call never wrote.

Reading and review: `2026-11-06-architecture-benchmark/results/results-reading.md`, agreed with Codex.

**One revision screened, on Alex's word** ("好，按1试一次"): the evidence call moved to keep-then-file (`split-b-v2`, `poc/config/poc-split-v4.json`),
on 69 seed-drawn articles, same day, against the current call and production (`2026-11-06-architecture-benchmark/screen/`).
- It reached production's helpful level: 92.0 against 94.0, with the current call at 84.3.
- It kept more of what the standard rejects than production: 22–23 against 17.3 a send, after a blind reader checked all 212 not-kept matches.
- Not adopted (Codex agreed, r24–r25).

## Where everything is

- **Research folders of this line:**
  - `2026-11-05-seven-day-request/`: the first-100 work and its probes;
  - `2026-11-05-production-plan/`: the plan, `review-log.md` with every Codex round r0–r25, traces;
  - `2026-11-06-architecture-benchmark/`: design, harness, results, screen, probes, readers;
  - Codex's earlier parallel prototypes: `2026-11-05-parallel-refinement/` and `2026-11-05-parallel-thesis-evidence-poc/`;
  - `2026-11-05-matching-identity-design.md` (the matching changes PRD 11 E2 proposes for production).
- **Code and prompts:**
  - `src/hivemind/split.py`;
  - `src/hivemind/prompts/split-a-v3.txt`, `split-b-v1.txt`, `split-b-v2.txt`, `split-preparation-v1.txt`, `collision-v3.txt`, `collision-v4.txt`,
    `collision-v5.txt`;
  - `poc/config/poc-split-v2.json`, `poc-split-v3.json`, `poc-split-v4.json`, `poc-v117.json`, `poc-v118*.json`.
- **Data kept on disk and not in Git:** `2026-11-06-architecture-benchmark/data-on-disk.md`, and the run folders under `poc/data/` (`split-*`,
  `pilot-d369-*`, `parallel-thesis-evidence-input-2026-11-05`).

## Mistakes recorded along the way

All are logged in `review-log.md`:
- blind keys once placed in the readers' folder;
- a collision prompt sent without its field definitions;
- an edit to `split.py` during a live run;
- two probes that re-sent sorted-key archive JSON instead of production bytes;
- an overclaimed first reading of the results, corrected over Codex rounds r16–r23.

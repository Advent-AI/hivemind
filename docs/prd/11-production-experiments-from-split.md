# PRD 11 · Production experiments drawn from the failed split extraction

Status: proposed, 2026-11-06. Nothing here is built in main. Each experiment is a new production version that only Alex opens (D359), measured
against the frozen production configuration on the frozen ruler (AGENTS §7.1). Decision: D378.

Alex, 2026-11-06: "我觉得你把拆分版学到的东西，有用的给cherry pick 出来，做一个PRD我们来给到生产版来实验；你现在封存拆分版并且清理赶紧并标注失败的实验吧"
(pick out what the split taught that is useful, write a PRD so we can experiment with it on the production version; seal the split, clean it up
and mark it as a failed experiment).

## 1. What failed, in one paragraph

The split extraction read each item with two calls: one proposed new questions, the other filed evidence under existing questions, and a third
call (record preparation) completed the new questions. It was built in production shape and benchmarked against the frozen production
configuration (poc-v108). The benchmark ran three window draws and three test-article draws for each arm, under a design agreed with Codex.
- The split reached fewer helpful matters: 156, 156, 159 against 166, 170, 162. The difference of −9 falls outside the −8 same-configuration
  range, so the stop line fired (D355).
- Its judgement scores were 44 against 47, and it cost about 15% more.
- Its one strength was opening more questions worth following: 25 against 6 over three draws, but also 17 against 6 that the standard would not
  open.

One revision was screened on Alex's word. It moved the evidence call to keep-then-file. It reached production's level of helpful matters (92.0
against 94.0 on a 69-article set), and it kept more of what the standard rejects than production does (22–23 against 17.3 a send). So it is not
adopted.

The split is sealed as a failed experiment. Its record is on branch `fix/no-preseed-evidence-review`, tag `split-extraction-failed-sealed-2026-11-06`,
with the seal note `docs/research/SEALED-FAILED-split-extraction-2026-11-06.md`.

## 2. Experiments for production, in order of expected value

Each item gives the problem in production's own stored data, the evidence, the cheapest proof to run first, and the code that already exists. The
counts come from the three same-day production draws of the benchmark (`runs/control-v108-d1..d3` in the sealed worktree) unless stated.

### E1 · Helpful statements production writes and then drops as "no home"

- **Problem.** Production's extraction writes a statement, finds no open question to file it under, and drops it (D209). The three window draws
  dropped 441 statements this way, about 147 a draw. Independent readers put 60 of production's 213 missed helpful-matter draws down as "written,
  then dropped by a check", almost all of them no home. On the 30 test articles it was 36 of 68. On the window it is the second recall loss after
  "the model did not write it" (116 of 213); on the test articles it is the largest. (Corrected 2026-11-06: this line first called it the largest.)
- **What the split showed.**
  - Opening more questions and offering homeless statements to the item's new questions recovered some of these.
  - It also opened questions the standard would not open (17 of 44), and half its new questions had no ladder.
  - A keep rule tied to existing questions loses useful facts.
  So the remedy is not obvious, and the next step is a diagnosis.
- **Cheapest proof, $0.**
  - Read every helpful no-home drop of the three production draws beside its source and the questions open at the time. Put each down as either:
    - a link miss: an open question takes it under the link rule (the fallback to the company-wide revenue question, D273/D361, included);
    - an opening miss: the question that would take it does not exist.
  - The packets already exist: `docs/research/2026-11-06-architecture-benchmark/results/traces-window-control.json` and
    `traces-test-control.json`.
  - The larger class picks the experiment: a link-rule fix, or an opening fix, each with its own audit (AGENTS §6).
- **Result of the diagnosis (2026-11-06; `docs/research/2026-11-06-e1-no-home-drops/`).** 57 matters, two readers, 44 of 54 agreed: link misses
  17 (4 core), opening misses 3 (1 core), and a third class, 24 small matters the standard's §6 itself drops (none core); 10 disputed, all on the
  fallback or the indirect clause; 3 quote refusals. Opening is not the experiment. Of the link misses, 12 are the question's own quantity in
  another period or quarter, or a variant of a tracked product; the model's account says it read the question's period, population or named
  configuration as a boundary. Only 8 of their 13 dropped window draws were lost to the product (5 reached the question from another
  article), and no lost window judgement is shown to follow from them. Any fix is a new extraction version only Alex opens (D359).
- **Not to repeat.** A gate that keeps only statements connected to an existing question (§4).

### E2 · Duplicate questions: the analyst review with relation definitions

- **Problem.** In unseeded runs, matching let duplicate questions open:
  - a part-of relation at Jev probability 0.49 under the 0.5 threshold (seven-day run, seq 1253);
  - a later deadline for the same event (seq 1312).
- **What the split showed.** The matching code is production's, and two changes cut the duplicates the blind reader found in the first-100 runs
  from 3 to 1, then 0, then 0:
  - collision-v4/v5: each relation defined beside its field; a later deadline for an open one-off event is the same question; a coarser or finer
    reading of one outcome on one date is the same question, with D210's exception for an unsigned deal;
  - review of unkeyed proposals at any Jev probability, plus the closest existing question the proposer names.
  The seeded benchmark could not test this: both arms opened 0 duplicates there.
- **Cheapest proof.** Replay stored matching inputs of the seven-day and first-100 runs through production with these changes ($0 where the
  archive answers; cents for the new review calls). Then an unseeded window of production with and without them, duplicates read blind, recall
  on the frozen ruler.
- **Code to port** (sealed worktree):
  - `views/jev_matching.py`: `unkeyed_collision_peers`, `COLLISION_SCHEMA_V4`, `RELATION_DEFINITION_PROMPTS`;
  - `prompts/collision-v4.txt` and `collision-v5.txt`;
  - `tests/test_unkeyed_collision_matching.py`.

### E3 · Code checks for new questions' ladders (with D186)

- **Problem.** A new question's ladder can be inverted (the Strongly bullish rung holds the unfavourable range), carry a band whose bounds miss
  the stated reference, or carry a rung that holds no value. The split met each case:
  - a "within 5%" band whose bounds missed by $100 million (seq 1280);
  - an "exactly $279 billion" rung with equal bounds (seq 1210);
  - inverted ladders in its confirmation run.
  Production's stored numeric ladders, mostly seeds, show 0 empty rungs in 160.
- **Fit.** Alex asked for D186 (rungs against guidance) and D191.4 (shared quantity) in the next extraction version (2026-11-05: "这个你记住，我们要做").
  The split's checks belong there:
  - a favourable end that orders the rungs in code;
  - each numeric condition rendered from its bounds;
  - a stated band recomputed;
  - an empty rung refused;
  - the D197 key for a calendar-year theme quantity.
- **Cheapest proof, $0.** Run the checks over every stored production answer and count what they refuse; read each refusal before adoption.
- **Caution.** In the split, whether a new question got a ladder at all was a coin flip on the same request (21 of 44 had one). A reworded
  reference sentence lost two control ladders. Checks, not wording, are the part to port.
- **Code to port:** `split.ordered_ladder`, `band_problem`, `empty_rung`, `render` and `shared_key`, with their tests in
  `tests/test_split_extraction.py`.

### E4 · The judge's refused answers: a theme cited as a dependency

- **Problem.** In the three production draws, the frozen judge's refused answers carried 25 errors. 18 of them were "X is not a dependency of Y": a
  theme question, shown to every asset judgement under D191, written into `cites_views`, which holds dependencies only. A refused answer is retried
  once. A second refusal stops the run, as it did once in a split draw on the same frozen judge.
- **Cheapest proof, cents.** A judging version (judging is frozen, D354; only Alex opens one) where the `cites_views` field's own description says
  dependencies only and themes go to `theme_pushes` (the rule sits with its field, AGENTS §7.3). It is re-sent on the stored refused requests, and
  their refusal rate is counted against the stored answers.

### E5 · The revision's statement day (D203)

- **Problem.** D203 says the revision path stores the stated day, but production's writer stores the ordering day (`writing.py`,
  `store.revise(..., new_day, ...)`).
- **Evidence.** The benchmark's gate replayed a stored production draw: 4 of its 6 revision rows differ on this field alone. No judging request
  read it.
- **Fix.** One line, already in the sealed worktree (`store.revise(conn, target_id, stored_id, e['original_day'] or '', seq)`). It needs a test
  that fails on the old line.

### E6 · The measurement kit, as the standard way to measure a production version

Built and reviewed with Codex for the benchmark (`docs/research/2026-11-06-architecture-benchmark/` in the sealed worktree):
- `bench_run.py`:
  - a seeded fixture ledger;
  - per-draw pins of code, prompts, inputs and scoring files;
  - refusal of a resumed draw whose pins or mode differ;
  - an offline mode that replays a stored draw. It reproduced a stored production draw table by table (24 tables).
- `bench_measure.py`:
  - D372 counting at two points, the checked handover and the ledger;
  - where each helpful matter ends;
  - D373 printed;
  - refusal of runs not made by the harness.
- `bench_traces.py`: every missed matter with its source and full raw answers.
- Blind packets for questions, records, hits and extras, and screen pools.
- `compare_ledgers.py`.
- The screen rule (`results/results-reading.md` §4): the current version's self-variation over all splits of six sends, a same-day production
  reference, and "not decidable" when a self-check fails.
It is ported to main when the first experiment is opened.

## 3. Measured and not worth an experiment now

| Idea | Measurement | Verdict |
|---|---|---|
| The split architecture as a replacement for production's extraction | §1 | Failed; sealed |
| Wider quote matching (hyphen glyphs, closed-up dashes, "28.1 %") | 0 of the 17 production quote refusals in three draws recovered | No gain for production |
| One record per quoted statement keeping every summary (production's sift keeps the first) | 4 second summaries lost in 729 production answers | Too small alone; fold in if `sift` is touched |
| Reading long items in sections | 7 of 34,084 corpus items exceed 400,000 characters; none in the window | Not now |
| Reading every open question before each item (D375), research subjects outside the universe | Not tested apart from the split | Unknown; not evidence either way |

## 4. Lessons for any production prompt change

- **Keep, then file.** A keep rule tied to connection with an existing question filtered useful indirect facts and product-detail noise
  together. Removing it brought both back. Noise is handled by the standard's not-kept rules, never by a connection gate.
- **Extras are not noise.** In both arms about half of the statements the gold does not list are statements the standard keeps (blind read).
  An "extras" count is a quantity to read, not a score.
- **The not-kept count can match a neighbouring clause.** 10 of 212 matched pairs were records whose summary kept another statement. A result
  near a line is blind-checked before it decides.
- **A model call is a sampler.** The same stored request re-sent recovered 10–13 of 27 matters chosen because they had been missed. Items chosen
  by misses inflate any recovery.
- **Re-send production bytes.** The archive stores requests with sorted keys. A request is rebuilt by production code and its identity checked
  before it is sent (AGENTS §5).

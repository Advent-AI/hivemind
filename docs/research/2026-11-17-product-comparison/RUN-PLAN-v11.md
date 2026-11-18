# The product comparison that decides release (D665): run plan, version 11 (D668–D671 amendments)

v9 answers rounds 7 and 8 (`review-codex-7.md`, `review-codex-8.md`). The Claude reviewer found v7 READY. The decisions this plan takes are drafted in `D667-draft.md`.

**Alex:**
- D664: "no need for budget … run your council to determine".
- D666: "okay then you should write a run plan and monitor it carefully and don't scope drift".

**Read as:** his word to run this comparison once it passes its council review. Nothing outside it is started. The plan applies
`clean-arch/PRD.md` §1.5 (D665) and does not change it.

**How review works from here (`ROUND-LOG.md`, round 2):**
- This plan states each requirement and how it is proved.
- Prose review ends when a round finds no gap in the design.
- Everything build-level is checked on the built artifacts at the stage-0 **freeze review**: code with its tests and mutants, the frozen
  files and the dry runs. That review, by Codex and a fresh Claude reader, gates the first paid send.

## 0. Scope

**In:**
- poc-v118 against the new system (astra-frozen), from empty at 2026-07-01, three draws each;
- the blind matter census;
- the council's reading;
- D665's verdict and everything D665 prints beside it;
- the report to Alex.

**Out** (written to `FINDINGS.md`, not acted on):
- any prompt or answer-choice change (D662);
- model trials;
- live-store, planner or integration work;
- D658;
- other weeks or companies;
- any "while we are here" fix.

## 1. Stage 0 ($0): built, proved, frozen, then reviewed

### 1.1 Versions manifest

`manifest.json` holds the sha256 of:
- every file either system runs, including poc-v118's configuration and the frozen ladder request;
- the filtered items copy;
- every instrument below.

The launchers refuse a file that differs.

### 1.2 Exposure census, exclusions, one input

1. **The population.** The clean selection rule's articles from 07-20 to 09-20: 1,619 articles (by week: 185, 164, 62, 114, 109, 265, 218, 229,
   273). The warm-up from 07-01 to 07-19 has 357 articles.
2. **What counts as a read** (the closed set, frozen before any hit is read). The article's id or its text sha appears in any of:
   - a run's trace, archive or ledger (either system);
   - a probe;
   - a gold or reference;
   - a reader packet, answer or tally;
   - a design, result or log document;
   - a report;
   - a test fixture, mock or UI-check data file.

   **Not reads:**
   - **documented corpus storage, by content:**
     - `corpus-builds.json`, frozen before any hit is read, lists the documented corpus builds: the current source, `items-window.sqlite`,
       `items-window-tags2-2026-10-24.sqlite`, the page store, and any other build the decision log or `data-manifest.md` records as a corpus.
       Each comes with its record and its set of input ids.
     - A table is exempt only when it is a **verified raw copy** of a listed build: the same rows, by `input_id` and `content_sha256`. That
       covers renamed copies.
     - Any other such table (a probe's or fixture's selection) is searched like everything else.
     - The exemption covers stored rows only. Whatever a probe, run or fixture actually used, even from a whole-corpus copy, is a read
       through its trace, packet or fixture text.
     - Every other table in the same file, and every other file, is searched;
   - the search index built over the whole corpus;
   - this comparison's own files.

   Git-ignored files are searched.
3. **Where it is searched:**
   - the whole of this checkout, and of every worktree `git worktree list` shows, except `.git` (`tests/`, `poc/mock` and `poc/ui`
     included). The exempt rows are handled as above;
   - the archived runs in `docs/research/2026-10-25-english/data-manifest.md`.

   Search goes inside binary files (`rg -a`, and SQL over every SQLite table for the ids). Its controls:
   - a known hit: one of D613's 10 Step 1 reads in the week of 09-07;
   - a known miss: one id written only into a scratch control file outside the searched roots.
4. **Any read excludes the article, with one exception by actual use,** classified per folder and frozen before any hit is read:
   - **The exception:** an old-system replay run folder and its byte copies, **only when** its decision record or run note shows it ran the
     then-production configuration as the product (its library sealed or served as the product's), and no decision cites one of its articles as a
     case behind a change.
   - **Development replays are reads:** arms, probes, configuration trials and week tests.
   - **Why:** a replay of the product as it ran tunes neither system. D665's own council used the sealed run as the old system's output.
   - **Still a read:** any research artifact built from such a run (for example, the 2026-10-28 quality review).
   - **Recorded:** the per-folder classification (`replay-folders.json`, with each folder's record) and the council decision on it, both before
     the hits are read.
5. **One input.**
   - A filtered copy of the items database without the excluded articles is made once and hashed.
   - **Code change A:** `run_fresh.py --items` hands it to both children (clean `--source`; production `--testdb`).
   - **Code change B:** `fresh_week_inputs.py` takes the dates and the items path as arguments.
   - **Proof through the real entry points:** both launchers run dry with fake answers over the whole span on the copy. Each records the
     ordered ids it actually processes and their text sha. The two must be equal in order. Controls:
     - an excluded article appears in neither;
     - a kept article appears in both.

### 1.3 Blind matter census (articles only; frozen before any send)

1. **Sample (D668).** Every kept article in the scored window 2026-08-31 to 09-20, read in batches of about 40 per session. Each family merges across every batch and week before reconciling. The warm-up is 07-01 to 08-30, unfiltered: the exclusion filter applies to the scored window only. Read with week reading A1's
   brief (`../2026-11-14-use-acceptance/week/brief-A1.md`), unchanged except for the file names.
2. **Readers.** Codex (memories off, closed, D661) and Claude (closed command line), apart. Nine weeks × 2 families, in fresh sessions.
3. **Merge.** One matter is one bet. Two entries are one matter only when the same outcome settles both and their answers cannot move apart.
   Another year of a figure is another matter.
   - Each family merges its own nine lists in one session.
   - Two reconcilers, one per family, map every matter across the two families' lists (`same` or `none`). A matter is listed by both when
     both reconcilers say `same`.
   - A one-family matter goes to two third readers (one per family) with its articles. It joins the list when both say it is worth a question.
4. **The company-figure flag.** Each family marks every listed matter `company figure` or not, using D505's own list: 营收、毛利率的指引、市场预期、实际业绩.
   The flag is set when both say yes; a split is listed.
5. **N** is every listed matter (D665). The flagged subgroup is printed beside the verdict with its own a, b and N, because by D505 the new
   system does not open such questions. Alex sees how much of any gap that rule makes. (D431: the comparison is of the products as
   configured.)
6. **De-duplication and freeze (D671).** Both families group the entries that are one bet (D248); a pair only one family grouped, or one a reviewer names, goes to one blind adjudicator of each family with its articles; a merge needs both families or both adjudicators. **Frozen:** `stage0/census/matters.json`, the only scoring list: each matter with one canonical question, its source articles, its first source day and its flag; its hash is in the versions manifest.
7. **Too small at once:** if N < 20, the verdict is "too small" and goes to Alex before any paid send.

### 1.4 The verdict rule (`verdict-rule.json`, hashed; `score_comparison.py` with a test and a mutant per rule)

1. **The cutoff:** one for every matter, the end of the invocation's last day (09-20 in the full run). Libraries are read as they stand then.
   - Closed questions still count.
   - Timeliness is not scored. The days from first source to opening are printed beside.
2. **Covers (mapping, A2's form, blind):**
   - **The rule:** both families mark the question `opened`, or `narrower` with both saying it carries the matter's main outcome
     (ACCEPTANCE-DESIGN A; `tally_week.covered`). `broader` and `missed` do not cover.
   - **Blinding:** the readers see each draw's library under a random X/Y label, the key outside the repository, and are told to ignore
     style.
   - **Disagreements:** two third readers, one per family. A remaining split is resolved per counting (item 7, order: covers > does not
     cover).
3. **Same question:**
   - **A question** is an id in a system-draw's library at the cutoff, the system's own identity. Distinct questions are distinct ids.
   - **Matter to question:** the mapping rule above.
   - **Question to question:** two questions of one library are the same bet when the same outcome settles both and their answers cannot move
     apart (A1's rule; D248). Of such a pair, **the earlier-opened question is the original and the later one the duplicate** (as
     `week/brief-A2.md` named the order).
   - **During mapping:** the readers, who read each whole library, also mark its duplicates.
   - **Distinct bets** are the ids less the duplicates both families mark. The 30-question minimum counts distinct bets. A split duplicate is
     counted both ways, and the minimum must hold both ways.
   - **On cards:** a duplicate stays a question in the worth guardrail.
4. **The cards and their marks:**
   - **Worth tracking:** worth, trivia or duplicate. Each card lists its library's other questions in opening order, with their opening days.
     `duplicate` is marked only on the later question of a same-bet pair.
   - **Answer:** supported, unsupported, insufficient, or no answer (a question not judged by the cutoff).
   - **Cannot tell:** a split after the debate rounds, resolved in each counting by item 7.
5. **Served in a draw:** at least one covering question is marked `worth` and supported, in each counting after item 7's resolution. A matter **served by a system** is served in
   at least 2 of its 3 draws.
6. **The quantities:** a = served only by the new system; b = served only by the old; N = all listed matters.
7. **The two countings.** A split ("cannot tell" after the debate rounds) resolves to one of the marks its readers actually gave.
   - **Counting 1:** the new system's cards take the most favourable mark given; the old system's cards take the least favourable.
   - **Counting 2:** the reverse.
   - **The order:** for the mapping, covers > does not cover; for the answer, supported > insufficient > unsupported; for worth, worth >
     duplicate or trivia.
   - **How a resolved mark counts:** it counts as that mark. A resolved supported or unsupported mark enters the decided denominators. A
     resolved insufficient mark stays out of them, as any insufficient mark does.
   - A guardrail subgroup is **exercised** only with at least 10 cards decided **without** a split. A subgroup that is not exercised cannot
     breach. It blocks only a practical lead; a loss established otherwise still stands.
8. **The guardrails** (D428's measure, which D665 turns into these guardrails):
   - **The sample:** the random guardrail sample only, 35 questions per system-draw by seed 20261117, or all of them when a library holds
     fewer. Covering cards are not in these shares. The three draws are pooled per system.
   - **The shares:**
     - the share of **decided** figure-question answers (supported or unsupported) that are unsupported;
     - the same for yes/no questions;
     - the share of decided worth marks that are trivia or duplicate.
   - **Reported beside, not in the shares:** insufficient and no answer, with the number of splits and how each counting resolved them.
   - **The bar:** the new system's share may not be more than 10 points above the old system's.
   - **Exercised:** each subgroup needs at least 10 cards per system decided without a split (item 7), or it is "not exercised".
9. **The controls,** outside every product count:
   - 6 planted wrong answers (a rung moved, 3 per system). Each needs an explicit unsupported or insufficient mark, or the reading is invalid.
   - 4 supported controls, confirmed first by a separate reader.
   - 3 hidden repeats.
10. **No release verdict without six complete draws.** A draw that cannot finish (stopped after D449's one redo, or by its guard) gives no
    release verdict. What finished goes to Alex as a diagnostic, with the cause.
    - **D431's "same day" for a run longer than one day:** a new-system draw takes about 20 h, so one calendar day cannot hold it.
      - The six counted draws are launched within one hour of each other and run concurrently.
      - A D449 redo inside a draw counts as part of that draw.
      - Every counted send falls within 72 h of the first launch.
      - A breach makes the result a diagnostic.
      - Recorded as decision D667 before any paid send, replacing D431's one-calendar-day reading for this run only.
    - No replacement draw counts toward the verdict. The reviewers read "same day" differently (Codex: the send day; the Claude reviewer:
      the window), so the council took the cheaper, reversible course (D439): a later replacement would be a diagnostic only.
11. **The verdicts, tested in this order:**
    1. **Invalid:** a plant without an explicit rejection, fewer than 3 of 4 supported controls accepted, or fewer than 2 of 3 repeats marked
       the same.
    2. **Too small:** N < 20, or fewer than 30 distinct questions in any system-draw.
    3. **Practical lead:** a − b ≥ max(3, ⌈0.15·N⌉) and a ≥ 2b under both countings, with every guardrail exercised and passing under both.
    4. **Practical loss:** b − a ≥ max(3, ⌈0.15·N⌉) and b ≥ 2a under both countings (needing no guardrail exercised), or a breach in an
       exercised guardrail under both.
    5. **No practical winner:** everything else.
12. **Printed beside, not deciding:**
    - D428's limits next to the guardrails;
    - a sign test and an interval, labelled illustrative;
    - the company-figure subgroup;
    - the floors (§1.6).

### 1.5 The new system as run: code changes C to F, each with a test and a mutant

- **C: `run_fresh.py --limits`.** The frozen `stage2-limits.json` stays the default and stays frozen. The comparison's file sets
  max_calls 12,000 (1,976 articles × 2 format tries × 3 network attempts, the true bound) and max_seconds 172,800. It is hashed.
- **D: astra.**
  - `stage_a_astra.py` sets `SETTING` to gpt-6-astra.
  - At the transport, for **every** request (first sends and retries with the refusal note), it builds the luna request from the same system
    text, user text and schema through the same code, and refuses any difference other than the model string.
  - Reservations and the stop gate stay stage_a's own, on the shared ledger.
  - `run_fresh --ladder-variant astra-frozen` calls it and checks every pass's archive.
  - The test includes a refused-then-retried send.
  - `stage_a.py` is not edited.
- **E: `run_stage_b.py --end-day`,** threaded from `run_fresh._judge` as the invocation's last day (07-07 for the slice, 09-20 for the run).
  It is proved on a stored run with a trailing day that has no articles.
- **F: the cards.**
  - `build_cards.py` renders both systems' questions in one neutral form: the question, its latest answer, and the material that answer was
    given, as its request shows it.
  - It is tested on stored draws of both systems (`clean-e2e-full` c1 and p1).
  - `council_mark.py` takes the deck and its card count as arguments, and adds `insufficient` and `no answer`. Deck 1's recorded output must
    reproduce under the change.

### 1.6 What D665 prints beside, with its tool and input

| What | Status | Tool and input |
|---|---|---|
| D400 accounting, all three passes (`stage_a/accounting.py`) | **Hard:** figure ranges meet end to end; the favourable end is stable; the due day agrees across all three sends for ≥ 90% of eligible questions. A failure is a release blocker reported with the verdict. Lines 1–5: reported | The new system's three draws. The reader lines use Stage A's two-family reading (`clean-arch/step4-2026-11-10/stage_a/build_reader_packets.py` and its tally, D400) on every draw |
| Step 2's three lines (D427; PRD §5) | **Hard**, like D400's code-decided parts: a failed line is a release blocker reported with the verdict. Pass: earlier version found ≥ 90%; clearly wrong merges ≤ 2%; no fewer later details than no merging. Each decided on its point estimate, intervals printed. A line with fewer eligible cases than its frozen sample is **not measured** and cannot clear release | The Step 2 log §12 method on draw 1 of the new system: recall over 100 records with a labelled earlier version (stratified random); blind review of 200 random merges; the no-merge dossier comparison on 30 groups. The sample sizes are a recorded design choice |
| D431's frozen-reference reading, 07-01 to 07-14 | Printed beside | The D395 method (`clean-arch/unseeded-2026-11-10/MATCHING-v2.md`: the seven graded questions against the frozen judgement gold) on **both** systems' draws as they stood at 07-14 |
| Proposed absolute floors | Printed beside | Coverage ≥ 80%, trivia ≤ 20% and supported ≥ 90% come from this comparison's cards. Wrong citations ≤ 5% and zero answer-changing omissions need source-first readings this plan does not run: printed as **not measured** (agreed in the council before the send) |

### 1.7 Long-run risk, checked at $0

- **The old judge's request size.** poc-v118's `evidence_in_view` (`views/judging.py:41`) shows every arrival since the fifth most recent
  judgement, which is unbounded.
  - Proxy: the sealed v34 ledger (07-01 to 08-28, 8 halt files).
  - Code computes the size of every request v118's rule would build on it.
  - If any exceeds the model's input limit or v34's halting size (292 KB), the risk is reported before the send.
- **The same for the new judge,** on the carried fortnight, scaled.

### 1.8 Preflight

- Every stored answer of the latest runs of both systems goes through the current checks (AGENTS §5).
- Both launchers run dry over two days with every code change in place.

**Freeze review:** the council reads §1's artifacts, proofs and outputs. A finding is fixed and the review repeated. The paid stages start
when it finds nothing serious.

## 2. Stage 1: the slice

- **What runs:** one draw of each system, 07-01 to 07-07 (about 98 articles), each on its own ledger.
- **Passes when:**
  - both draws complete;
  - the new system's Step 1 averages ≤ 51 s and ≤ $0.0153 an article (1.5 × the measured 34 s and $0.0102);
  - every answer-choice request was checked at the transport, and every archive shows astra;
  - production's days are complete.
- **On a failure:** fix the launcher only, then rerun. Anything else goes to the council, and then to Alex.

## 3. Stage 2: the full run

- **What runs:** three draws of each system, 07-01 to 09-20, detached, each with a log and a pid.
- **One ledger per draw** (six), so a stop ends only that draw.
  - **Absolute guards** (stops, not a budget): $65 per new-system draw, about 1.6 × the upper estimate; $25 per old-system draw, about
    1.7 ×. That is $270 in all.
  - This replaces, for this run only, D449's whole-run stop across draws and D666's single $250 ledger. It is recorded as a council decision
    before the send.
- **D449 within each draw, unchanged:**
  - a redo is launched only on an eligible failure shown in the component's output, with its reason written;
  - once per component;
  - a second stop ends that draw (§1.4 item 10).
- **The measured risk:**
  - the 4 stored Step 1 failures (of 2,549 articles) were dropped connections from before the network retry;
  - 0 failures in 624 articles since;
  - 9 of 9 format retries recovered.
- **A stopped ledger** refuses later launches. A relaunch would be a diagnostic only (§1.4 item 10).

## 4. Stage 3: reading and verdict

1. The libraries at the cutoff, read by snapshot.
2. The mapping (§1.4 item 2).
3. The cards (`build_cards.py`), with labels hidden and order shuffled (the key outside the repository).
4. The council's marks.
5. `score_comparison.py`.
6. The §1.6 table.
7. **The report to Alex,** in plain words:
   - the verdict first;
   - a, b and N under both countings;
   - the company-figure subgroup;
   - every split card for his spot check;
   - the §1.6 table;
   - `FINDINGS.md`;
   - the cost and the time.

   No release engineering resumes until he answers.

## 5. Estimates (measured rates; checked at the slice)

**New system, per draw:**
- Step 1: 1,976 articles at 26 to 34 s (measured) is 14 to 19 h, at $0.0089 to $0.0102 an article: $18 to $20.
- Step 2: about $3.
- The answer-choice step: about 55 theses × 3 passes × $0.037 to $0.050, about $6 to $8.
- The judge: about $5 to $10 (the least certain).
- **About $32 to $41 and about 20 h a draw.**

**Old system, per draw:** poc-v118's own $0.53 to $0.66 for 243 articles, scaled up, is about $5. But cost per article rises as the library
grows: the sealed v34 run went from $0.0026 to $0.0077. So about $5 to $15, over 2 to 4 h.

**In all:** about $110 to $170 and about 20 h of wall clock.

**The reading:** the census takes a few hours. About 330 to 450 cards, marked by the council in about 6 to 10 h. The §1.6 readings come after
the verdict reading.

## 6. Monitoring

- **Sources** (never a live database):
  - each ledger's `ledger.json` and attempt log;
  - each draw's `run.json`;
  - production's `replay.log` day and cost lines;
  - **a snapshot of each live trace and archive** every heartbeat (SQLite online backup, as `snapshot.sh` does), counting completed articles,
    completed judge days, the largest judge request and refused judge answers.
- **Monitor:** one `Monitor` raises an event on:
  - every component state change, stop, crash, refusal or redo;
  - every 100 completed articles per new-system draw;
  - every 7 replay days per old-system draw.
- **Heartbeat:** every 20 minutes, spend per completed article (Step 1) and per completed day (judges and production), compared like with
  like:
  - each draw against its two sibling draws at the same progress;
  - the old system against the sealed v34 curve scaled by the slice.
- **Stalls:**
  - a new-system draw with no ledger attempt for 35 minutes (one call can wait 3 × 600 s plus 90 s);
  - an old-system draw with no new day line for 45 minutes.

  I read the logs and the process state within one heartbeat.
- **The stops,** each through that draw's own ledger, with the reason recorded:
  - **automatic:** its absolute guard ($65 or $25);
  - **mine:**
    - a runaway: a draw spending over 2 times the median of its running siblings at the same progress, over at least 50 articles or 5 days;
    - a hang: 0% CPU beyond the stall limit.
- **Watched and reported, never a stop:** the largest judge request and refused judge answers. A day the judge halts on is D449's to handle.
- **`RUN-LOG.md`:** a dated row per event and per check that changes anything, reported to Alex as results land.

## 7. Returns to Alex

- the verdict, whichever it is;
- N < 20 at the census;
- a stop that is not a launcher wiring fault;
- a draw's guard reached;
- a failed hard check (D400's code-decided parts, or Step 2's lines);
- a draw that cannot finish (a diagnostic, not a verdict);
- no verdict by 2026-12-01.

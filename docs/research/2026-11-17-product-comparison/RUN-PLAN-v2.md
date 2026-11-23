# The product comparison that decides release (D665): run plan, version 2

**Alex:**
- D664: "no need for budget … run your council to determine".
- D666: "okay then you should write a run plan and monitor it carefully and don't scope drift".

**Read as:** his word to run this comparison once this plan passes its council review. Nothing outside it is started. It applies
`clean-arch/PRD.md` §1.5 (D665) and does not change it.

**v2 answers review round 1:**
- `review-codex-1.md` and the Claude reviewer's report. My checks of each point are in `triage-1.md`.
- Two points are decided here and recorded as such:
  - the company's own figures count in N;
  - the exposure rule's one narrowing.

## 0. Scope

**In:**
- poc-v118 against the new system (astra-frozen), from empty at 2026-07-01, three draws each;
- the blind matter census;
- the council's reading;
- D665's verdict;
- the checks D665 keeps beside it;
- the report to Alex.

**Out (written to `FINDINGS.md`, not acted on):**
- any prompt or answer-choice change (D662);
- model trials;
- live-store, planner or integration work;
- D658;
- other weeks or companies;
- any "while we are here" fix.

## 1. Stage 0 ($0): everything that fixes the result is frozen before the first paid send

### 1.1 Exposure census and exclusion list

1. **The population.** Every article the clean selection rule takes from 07-20 to 09-20: 1,619 articles.
   - The rule is `fresh_week_inputs`'s rule, generalised to a date range.
   - Counts by week: 185, 164, 62, 114, 109, 265, 218, 229, 273.
   - The warm-up from 07-01 to 07-19 has 357 articles.
2. **Search.** Every input id is searched (`rg -F -f ids.txt`) over:
   - `poc/data` (every run, sealed or not, and its databases);
   - `poc/reports`;
   - `docs/research`;
   - `clean-arch`;
   - `research_notes`;
   - every archived run listed in `docs/research/2026-10-25-english/data-manifest.md`.

   Each hit is recorded with its path and the artifact's kind.
3. **Rule.** Any read excludes the article, with one named narrowing.
   - **The narrowing:** a read by the old system's own sealed production replays (poc-v34 through 08-28; run3 through 07-28 and 08-15) is
     listed but does not exclude the article.
   - **Why:** those runs are the old product running. Excluding them would also remove most of 07-20 to 08-28. D665's "unread" was written
     about the new system's reads (D613).
   - **Unless:** a decision cites one of those articles as the case behind a change to either system (searched in the decision log by id
     and title). Then it is excluded.
   - The narrowing is recorded as a council decision before the send.
4. **The scored span** is 07-20 to 09-20, less the excluded articles. There is no week veto: D665's "too small" is the floor (§1.3).
5. **Frozen:** `exclusions.json`, with its sha, and the census output.

### 1.2 One input for both systems

- A filtered copy of `items-nvda-2026-07-01-10-27.sqlite` without the excluded articles is made once and hashed.
- **Code change A:** `run_fresh.py --items PATH` passes that copy to both children: the clean `--source`, and the production
  `budget_replay --testdb`. The default stays unchanged.
- **Proof:** the generalised `fresh_week_inputs.py` (code change B: date range and items path as arguments, nothing else) on the copy shows
  both entries list the same items, in the same order, with the same text sha. Its controls:
  - one excluded article is in neither list;
  - one kept article is in both.

### 1.3 The blind matter census (reads articles only; frozen before any send)

1. **Sample.** In each scored week, 40 articles drawn from the kept articles by seed 20261117, read in full. This is week reading A1's brief
   (`../2026-11-14-use-acceptance/week/brief-A1.md`), unchanged except for the file names.
2. **Readers.** Codex (memories off, closed; D661) and Claude (closed command line) list each week's matters apart. That is 9 weeks × 2
   families, in fresh sessions.
3. **Cross-week merge.** Free-text keys cannot be merged by code.
   - **The rule:** one matter is one bet. Two entries are one matter only when the same outcome settles both and their answers cannot move
     apart. Another year of a figure is another matter (A1's own rule; D38, D248).
   - Each family merges its own 9 weekly lists in one session.
   - Then two reconcilers, one per family, each map every matter of one family's list to the other's (`same` or `none`). A matter is listed
     by both when both reconcilers say `same`.
4. **One-family matters** go to two third readers (one per family), each given the matter's articles. A matter joins the list when both say
   it is worth a question.
5. **N is every listed matter (D665).** The company's own figures (revenue, margin, guidance) are counted.
   - The subgroup is printed beside the verdict with its own a, b and N. By D505 the new system does not open them as questions, so Alex
     sees how much of any gap his rule makes.
   - (The Claude reviewer showed v1's carve-out had no source in D665. In the fresh week, 3 of the 5 both-listed matters were in this
     subgroup.)
6. **Frozen:** `matters.json`. Each entry holds the matter, an example question, its source articles and its first source day, with the sha.
7. **Too small at once:** if N < 20, the verdict is "too small". It goes to Alex before any paid send.

### 1.4 The credit rules (`verdict-rule.json`, hashed)

- **The cutoff:** one for every matter, the span's last day (09-20). The library and the latest answers are read as they stand at the end of
  that day.
  - Questions closed earlier count; they are still in the library.
  - Timeliness is not scored. The days from a matter's first source to each system's opening are printed beside, descriptively.
- **Same question (mapping, A2's form):** a system-draw's question **covers** a matter when both families mark it:
  - `opened`; or
  - `narrower`, with both saying it carries the matter's main outcome (ACCEPTANCE-DESIGN A, as `tally_week.covered()` already counts).

  Other cases:
  - `broader` and `missed` do not cover.
  - A disagreement goes to two third readers, one per family. A split that remains is a split.
- **Repeats:** several questions of one system-draw may cover one matter. Each is carded. The matter is served in that draw when **any** of
  them is marked worth tracking and supported by the council.
- **Served by a system:** served in at least 2 of its 3 draws.
- **The quantities:**
  - a = served only by the new system;
  - b = served only by the old system;
  - N = all listed matters.
- **Distinct questions** (for "too small"): the question ids a system-draw holds at the cutoff, each counted once.
- **The two countings:** in counting 1, every split mark or mapping is resolved for the new system; in counting 2, for the old.
- **The guardrails, per system over its three draws:**
  - the unsupported share among figure questions;
  - the unsupported share among yes/no questions;
  - the not-worth-tracking share.

  The new system's share may not be more than 10 points above the old system's. Each subgroup needs at least 10 marked cards per system
  (the frozen minimum); a subgroup under it is "not exercised".
- **The verdicts, tested in this order:**
  1. **Invalid:** a planted wrong answer accepted, fewer than 3 of 4 supported controls accepted, or fewer than 2 of 3 repeats marked the
     same (D665's counts, over the whole deck).
  2. **Too small:** N < 20, or fewer than 30 distinct questions for any system-draw.
  3. **Practical lead:** a − b ≥ max(3, ⌈0.15·N⌉) and a ≥ 2b under both countings, and every guardrail exercised and passing under both.
  4. **Practical loss:** b − a ≥ max(3, ⌈0.15·N⌉) and b ≥ 2a under both countings, or a guardrail breach under both.
  5. **No practical winner:** everything else, including a verdict a split could change and a guardrail not exercised.

### 1.5 The reading instruments (written and hashed)

- the census, merge and reconciliation briefs;
- the mapping brief (A2's);
- the card template (Deck 1's);
- the council-marking protocol (Deck 1's `PROTOCOL.md` and `council_mark.py`, unchanged);
- the control specifications;
- the seeds;
- `score_comparison.py`, with tests that each fail on a mutant of the rule they hold.

### 1.6 The new system as run: three more code changes, each with a test and a mutant

- **C: `run_fresh.py --limits PATH`** for Step 1. The frozen `stage2-limits.json` stays the default and stays in the unseeded freeze. The
  comparison's file sets max_calls 6,000 (1,976 articles × 3 attempts) and max_seconds 172,800 (48 h). It is hashed. With the shared ledger,
  Step 1's own dollar cap does not apply (`live.py` line 84).
- **D: astra.**
  - `stage_a_astra.py` sets `stage_a.SETTING` to gpt-6-astra (the pattern of `gate1_candidate.py` lines 26 and 101) and refuses, **before
    transport**, any request that differs from the frozen request except in the model string (that file's lines 65 and 66).
  - `run_fresh.py --ladder-variant astra-frozen` calls it, and checks every pass's archive against the astra configuration checksum written
    at stage 0.
  - `stage_a.py` is not edited.
  - The three passes stay. The judge reads pass 1. Passes 2 and 3 feed the stability checks in §1.7.
- **E: the judge to the cutoff.** `run_stage_b.py --end-day`, threaded from `run_fresh._judge`, set to 09-20. It is proved on a stored run
  extended by a trailing day with no articles: due questions close, and nothing is sent.

### 1.7 The checks D665 keeps beside the verdict, each with its tool

| Check | Status | Tool and input |
|---|---|---|
| Figure ranges meet end to end; the favourable end is the same in every pass; the due day is the same in ≥ 90% of passes | **Hard** (D665): a failure is reported with the verdict as a release blocker | Code over every new-system draw's three passes |
| D400's reader lines (1–5) | Reported | The October Stage A reading (`stage_a/build_reader_packets.py`, the two-family tally) on every draw's pass 1, after the verdict reading |
| Step 2's three lines (D427) | Kept, as D427 set them | The Step 2 log §12 method (`step2-validation-2026-11-07/`: retrieval, merge and dossier scripts) on the new system's three draws |
| D431's frozen-reference reading, 07-01 to 07-14 | Printed beside | Stage B's reading on each new-system draw's judgements at 07-14, against the frozen judgement gold |
| The proposed absolute floors (reflection-10) | Printed beside | Three come from this comparison's own cards: coverage (≥ 80%), trivial or duplicate (≤ 20%), supported (≥ 90%). The citation and omission floors need source-first readings this plan does not run; they are printed as **not measured** |

### 1.7a Preflight

- Every stored answer of the latest runs of both systems goes through the current checks (AGENTS §5).
- Both launchers run dry with fake answers over two days, with every code change in place.

## 2. Stage 1: the slice (wiring and rates)

- **What runs:** one draw of each system, 07-01 to 07-07 (about 98 articles), with all code changes, on its own ledger.
- **Pass checks:**
  - both draws complete;
  - Step 1 averages ≤ 51 s an article (1.5 × the measured 34 s);
  - Step 1 costs ≤ $0.0153 an article (1.5 × $0.0102);
  - every answer-choice request was checked by the wrapper before transport, and every archive shows astra;
  - production's day lines are complete.
- **On a failure:** stop, log it, and fix only the launcher. Anything else returns to the council, and then to Alex.

## 3. Stage 2: the full run

- **What runs:** three draws of each system, 07-01 to 09-20, all six at once on one shared ledger. They are launched detached, each with a log
  and a pid (AGENTS §9).
- **D449's rules unchanged:**
  - a format or transport failure stops that draw's component; one redo follows in a new folder;
  - for Step 1, the redo starts from empty, about 17 hours more;
  - a second stop, a crash, a dead launcher, a wrong configuration or a ledger refusal stops the run.
- **The risk, measured:**
  - the 4 stored Step 1 failures (of 2,549 articles) were all dropped connections from before the network retry (2026-11-15);
  - after it, 0 in 624;
  - 9 format retries, all recovered.
- **A stopped ledger refuses every later launch.** A relaunch is a new ledger and six fresh draws, decided by the council.

## 4. Stage 3 (after the run): mapping, cards, marking, verdict

1. **Read the libraries at the cutoff,** by snapshot (never a live database).
2. **Mapping** (§1.4) by both families, apart, with third readers on disagreements.
3. **Cards**, with system labels hidden and order shuffled (key outside the repository):
   - every covering question;
   - a guardrail sample of 35 questions per system-draw, drawn from its library by seed 20261117;
   - the controls: 6 planted wrong answers (a rung moved, 3 per system), 4 supported controls confirmed first by a separate reader, and 3
     hidden repeats. Controls are outside every product count.
4. **The council marks every card** by Deck 1's protocol. Only void sessions are rerun; there is no reread of a missed plant. Then
   `score_comparison.py` applies `verdict-rule.json`.
5. **The §1.7 checks.**
6. **The report to Alex** (plain words):
   - the verdict first;
   - a, b and N, under both countings;
   - the company-figures subgroup;
   - every split card for his spot check;
   - the §1.7 table;
   - `FINDINGS.md`;
   - the cost and the time.

   No release engineering resumes until he answers.

## 5. Estimates (measured rates; checked at the slice)

**New system, per draw:**
- Step 1: 1,976 articles at about 30 to 34 s (measured: 26.1 s on fresh-a2, about 31 s on e2e-full c1, 33.7 s on the carried week) is
  about 16.5 to 19 h. At $0.0089 to $0.0102 an article, that is $18 to $20.
- Step 2: about $3.
- The answer-choice step: about 55 theses × 3 passes × $0.037 to $0.050, about $6 to $8.
- The judge over 82 days: about $5 to $10 (an estimate, the least certain).
- **About $32 to $41 and about 20 h a draw.**

**Old system, per draw:** poc-v118's own $0.53 to $0.66 for 243 articles, scaled to 1,976, is about $5. About 2 to 3 h.

**The whole run:**
- about $110 to $140, and about 20 h of wall clock (the six draws at once);
- the $250 shared-ledger guard includes concurrent reservations (a Step 1 reservation is about $0.12).

**The census and reading:**
- 18 census sessions, 2 merges, 2 reconciliations and the third readers: a few hours;
- the cards, about (N + 35) × 6 + 13: roughly 330 to 450 cards. Marked by the council, about 6 to 10 h.

## 6. Monitoring (sources, thresholds, actions)

- **Sources:**
  - the shared `ledger.json` and `ledger.attempts.jsonl` (attempts and spend per pid, hence per draw and component);
  - each draw's `run.json` component states;
  - production's `replay.log` day lines;
  - the launcher logs.

  Never a live database (AGENTS §9).
- **Monitor:** one `Monitor` emits a line on:
  - every component state change, stop, crash, refusal or redo;
  - every 100 Step 1 attempts per clean draw;
  - every 7 days of each production draw.
- **Heartbeat:** every 20 minutes, spend per completed article per draw, against the slice's measured rate. Like is compared with like:
  clean draws with each other, and production draws with each other.
- **Thresholds and actions:**
  - **Clean draw stalled:** no ledger attempt for 35 minutes (a call may wait 3 × 600 s plus 90 s before failing).
  - **Production draw stalled:** no new day line for 45 minutes.
  - On a stall, I read the logs and the process state within one heartbeat.
  - **The only stops I make:**
    - a runaway: spend per article above 2 times the slice's rate over at least 50 articles;
    - a hang: the process at 0% CPU beyond the stall limit.

    Either stops the run through the ledger's own stop, with the reason.
  - Everything else (a redo, a slow draw) is logged and watched.
- **`RUN-LOG.md`:** one dated row per event, check and heartbeat that changes anything, with numbers. It is reported to Alex as results land.

## 7. Returns to Alex

- the verdict, whichever it is;
- N < 20 at the census;
- a stop of the run that is not a launcher wiring fault;
- the $250 guard reached;
- a hard check failing;
- no verdict by 2026-12-01.

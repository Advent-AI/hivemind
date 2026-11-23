# Run log: the release comparison (D665, D666)

One dated row per event and check, with numbers. Newest last.

| When (2026-11-17) | Stage | Event | Numbers / outcome |
|---|---|---|---|
| — | plan | RUN-PLAN v1 written; council review started (Codex thread 01a1ebfe…, one Claude reviewer) | — |
| 2026-11-17 | plan | Round 1: Codex NOT READY (5 points), Claude reviewer NOT READY (5 changes); every point checked against code (`triage-1.md`) | Blockers confirmed: Step 1 limits 300 calls / 8 h; ladder still luna; production ignores exclusions; judge stops at the last article; 15 s/article estimate wrong (measured 26–34 s) |
| 2026-11-17 | plan | Census of inputs: 1,976 articles (357 warm-up, 1,619 scored); Step 1 failures in stored traces: 4 of 2,549, all dropped connections before the 11-15 network retry, 0 of 624 after | — |
| 2026-11-17 | plan | RUN-PLAN v2 written (census moved to stage 0, company figures counted in N with the subgroup printed beside, exposure narrowing named, five code changes, rebased estimates); round 2 sent (Codex thread, fresh Claude reviewer) | — |
| 2026-11-17 | plan | Round 2: Codex NOT READY, Claude reviewer NOT READY (7 changes); retry, binary-search and cost-curve findings checked against code and stored runs; lessons in ROUND-LOG.md; structural rule adopted (prose review stops at design level; build-level checked at the stage-0 freeze review) | — |
| 2026-11-17 | plan | RUN-PLAN v3 written; round 3 sent (Codex thread, fresh Claude reviewer) | — |
| 2026-11-17 | plan | Rounds 3–10: v3 to v9 (design-level review only from round 3; build-level items in freeze-review-notes.md). Claude reviewer READY at v7; Codex READY at round 10 on v9 and the decision text | D667 recorded (log, index, CURRENT_STATE) |
| 2026-11-17 | stage 0 | Replay folders classified before any hit: two blind readers (Codex, Claude) both chose folder level, all 12 folders reads; frozen `stage0/replay-folders.json` (sha 0aa44d48…) | scored window by date: 08-31..09-20 (3 weeks, 720 articles before the census) |
| 2026-11-17 | stage 0 | Census sample amended (D668, Codex AGREE): every kept article in the window; warm-up 07-01..08-30 unfiltered | — |
| 2026-11-17 | stage 0 | Exposure census (`stage0/exposure_census.py`, 6 controls passed; 2 min; checkout, 5 worktrees, backups): under D667's frozen rule **720 of 720** window articles are reads | kept 0. Strict cause: superseded corpus states in the backups, two run-local corpus copies, `poc/corpus/items.sqlite`, and corpus-wide code-only censuses (source-loss, source-lineage) touch every article |
| 2026-11-17 | stage 0 | Content-use look ($0, after the hits, not adopted): the week of 08-31 was processed end to end by the old system's seven-day runs (no-preseed worktree, 2026-11-05); 09-07 and 09-14 partly by the new system's 11-09 acceptance run and Step 2 councils | a property rule by folder misclassified gold and reader folders, so it is not usable; plan trigger "N < 20 at the census" → Alex |
| 2026-11-17 | stage 0 | D669 (Alex: "只排除真被读过的，比9/7–9/20"): read rule in `stage0/classify_reads.py` keeps **414 of 502** (09-07: 172 of 229; 09-14: 242 of 273); not-read locations: 8 storage, 18 pool lists, 14 code-only (all in the source-loss and source-provenance censuses); council check sent | — |
| 2026-11-17 | stage 0 | Code D (`stage0/stage_a_astra.py`): 4 tests pass; 2 mutants caught as predicted (transport check off → a request reached the transport; build check off → 2 drifted requests sent); worst-case reserve $0.864 an astra attempt | `mutants-stage-a-astra.txt` |
| 2026-11-17 | stage 0 | Codes A, C, D (launcher side) and E in `run_fresh.py` (+ `run_stage_b.py` forwards end_day): 33 launcher tests pass (30 existing + 3 new); 5 in-memory mutants caught as predicted, control passes | `mutants-run-fresh.txt`; open: a run_stage_b test for the end-day pass-through and the trailing-day proof |
| 2026-11-17 | stage 0 | Read-rule check (Codex + Claude checker): 4 reader-shown articles added as reads (confirmed in the council sessions); 37 bulk-viewer-only articles kept excluded (split, safer course); **410 kept, frozen** (`stage0/kept-articles.json`, 172 + 238) | D670 |
| 2026-11-17 | stage 0 | Matter census launched: 410 kept articles in 11 batches (35,35,35,35,32,40,40,40,40,40,38), two families, 22 closed sessions; Codex memory probe: no memory | prompts hashed in stage0/census/prompts.sha256 |
| 2026-11-17 | stage 0 | Census reading done: 22 sessions, 0 void; Codex 164 questions (93 batch matters), Claude 205 (95); spot-read batch 07 side by side (well aligned) | — |
| 2026-11-17 | stage 0 | Census merge → reconcile → 94 third-reader sessions → 38 entries; Codex council check found same-bet duplicates and an over-merge; dedup (both families) + blind adjudication of 10 pairs (20 sessions) | **N = 32** (7 company figures), `stage0/census/matters.json` frozen (D671); 2 split pairs disclosed |
| 2026-11-17 | stage 0 | Committed 099f4a8 (Alex: "你clean up提交"); shared items DB built (92 excluded rows deleted, sha 75c28d3c…); two-entry input proof: 1,884 items 07-01..09-20, same set and order, controls pass; limits, verdict-rule.json and versions-manifest.json frozen | next: freeze review, then the slice |
| 2026-11-17 | stage 0 | Size check (§1.7): v118's 14-day draws q1-q3 max judging request 114 KB / 29K input tokens; v34 end-state proxy 630 pieces (~500 KB, overstated: v34 linked wide) — watched, never a stop. Preflight (production, frozen v108 d1): A 2/2 schema refusals as stored, B 12/726 dropped (7 quote, 5 merged), C 0/170, D 0/43 — unchanged baseline | stage0/preflight-output.txt |
| 2026-11-17 | stage 0 | Freeze review: Codex NOT READY, Claude reviewer NOT READY; fixes applied (per-pass check + test + 2 mutants, verdict rule completed sha 693911eb, card spec c930a860, launcher git-clean/ledger/redo); new judge size max 100 KB / 21.9K tokens; split on resequencing → D672 (Alex's word + Claude reviewer's conditions) | next: commit, re-freeze manifest, launch the slice |
| 20:55 | slice | Launched s-new (clean, astra-frozen, ledger $10) and s-old (poc-v118, ledger $3), 07-01..07-07, on the shared items DB at 13bc220d | — |
| 2026-11-17 21:00 | run | Alex: "开始跑，需要用council loop 讨论结果" — the full run starts as soon as the slice passes its checks (D672); results go to a council loop | — |
| 22:05 | slice | s-old complete ($0.22). s-new stopped at the ladder: the shared ledger refused a $1.33 astra reservation against the slice's $10 guard (spent $2.86; 8 concurrent worst-case reservations ≈ $10.7). Diagnosis: guard sizing, a launcher parameter (plan §2: fix the launcher only, rerun). Before the stop: Step 1 98 articles ≈ 40 s and $0.011 each; Step 2 and cases complete (9 cases); 5 astra ladder sends answered, no wrapper refusal. Full-run guard $65 leaves room (≈ $23 spent + ≈ $11 reservations at that point) | rerun as slice-2, 07-01..07-03, guards $25 / $3 |
| 2026-11-17 22:35 | slice-2 | Both draws complete (new \$0.93, old \$0.05). Checks: 1–4 PASS at once; 5 and 6 failed first by the checks' own error. Old's 3 extra items are copies merged into their originals (not extracted), and day-end judgements carry `day:<date>`. Corrected and rerun: **all six PASS** (39 articles, 42.1 s and \$0.0084 each, every ladder pass astra, same 39 items in order, a day state reads back) | stage0/slice-2-checks.txt |
| 2026-11-17 22:36 | run | **Full run launched:** new-1..3 (clean, astra-frozen, guard \$65 each) and old-1..3 (poc-v118, guard \$25 each), 07-01..09-20, on the shared items DB, all six within one minute (D667 timing), at commit 4c66408f | monitor armed (stops, crashes, component changes, progress every 100 attempts / 7 days) |
| 22:41 | reading tools | mapping.py (3 tests), mark_cards.py (4 tests), build_cards.py type field; card form check (D673): round 1 named two rung annotations (removed) and a truncation artefact of the check itself; round 2 named only the systems' own structure (rung counts, library sizes), disclosed | stage0/blinding-check-codex*.md |
| 23:03 | check | six draws running; spend new 0.43–0.45, old 0.91–1.08; my own mistake: a status check tried to count rows in a live Step 1 trace (AGENTS §9: never open a live run's databases); refused by the classifier, not repeated; status is read from run.json and the ledgers only | run/ |
| 23:24 | card form check (D673), rounds 3–4 on the new card (request context, own opening place, numbered answers) | round 3 named one form element: the answer step's third annotation form ('the amount last reported when the question opened'); the annotation filter is now the closed set of ladder_step's three suffixes (484 stored conditions, 0 left annotated). Round 4 named only content (rung counts, theme counts, library size): closed, disclosed with the result | stage0/blinding-check-codex-3.md, -4.md |
| 23:37 | reading-tools council, rounds 2–4 | round 2–3 both readers not ready (eligibility, mapping validation, publishers, debate, plants, split readings, card context); round 4: Claude ready to read, Codex 3 more (key-verified card flags, reconciled attempt log, theme rungs), fixed; 47 tests, 39 mutants + 5 controls as predicted; §1.6 design v2 sent with round 5 | D675; tools-review-codex-2..4.md; DESIGN-1.6.md |
| 00:06 | §1.6 design rounds 5–7 → v6; reading tools committed (c3704776, 802f2b08) | both readers: design faithful after v6's small fixes; built eligibility inputs, D400 code check, printed-beside quantities, diagnostic export (54 tests, 43 mutants + 6 controls); three builders started in parallel for D400 reader lines, Step 2 lines, D431 at 07-14 (new files only, fake readers) | DESIGN-1.6.md v6; D675 |
| 00:29 | three §1.6 tools built (D400 reader lines 7 tests, Step 2 lines 10, D431 6; each with mutants on scratch copies) | finding: Step 2 line 3 as v6 defines it is predetermined (group_text drops later reports' tier/stated day/period/speaker; v6 counts them; c1: 78/79 groups) while the product's judge reads each member's full record (PRD §6; 741 and 1,127 same-claim notes in c1/p1 requests); sent to the council as round 8 with the tools | tools-review-brief-8.md |
| 01:02 | §1.6 tools pass the council (round 10, Codex READY; Claude round 9 points fixed) | every instrument D672 requires is built and reviewed before any output: reading tools (round 5) and §1.6 tools (round 10); 92 stage0 tests; CURRENT_STATE next task = the reading order once the six draws end | f2cbfcfa |
| 01:20 | old-1, old-2 complete | old-1 $9.83, old-2 $8.60, no stop; old-3 near the end; the new draws still in Step 1 (about $2.8 each) | run/ |
| 01:21 | old-3 complete | $8.83, no stop; the three old draws total $27.26 against $25 guards each (not a budget); the new draws are in Step 1 | run/ |
| 13:11 | reading chain dry run end to end on the slice ($0, fake reader) | every step joins; verdict 'too small' as ordered; gap fixed: printed-beside quantities now computed for invalid and too-small verdicts too | stage0/chain_dry_run.py |

- 2026-11-18 13:59: The scorer and the chain rebuild were hardened through Codex rounds 11–22. Round 22 returned READY.
  - The verdict is computed only on a snapshot rebuilt from the primary data.
  - Any derived file that differs from the rebuild is refused.
  - Coverage: 101 stage0 tests; 75 mutants, all as predicted; the chain dry run passes (D675).
  - The run is unchanged: old-1..3 finished; new-1..3 are in Step 1, at $16.2–17.0 each at 13:39.

- 2026-11-18 18:12: new-2 finished Step 1 after 19 h 36 min. Its step1.log reads `status complete, error null, calls 1899`, and $21.14 was spent.
  Step 2 then started at 18:12:37. Two figures to keep apart: `reserved_usd` 265.30 in the log is the running sum of what each call set
  aside before it ran, while the ledger's spend is $21.14. new-1 and new-3 are still in Step 1.

- 2026-11-18 19:00: new-2 finished Step 2 (18:12–19:00) and wrote its cases.
  - Step 2: 1473 articles, 5256 records, 2327 groups. Outcomes: 2181 new, 2929 repeat, 146 revision; none refused. Later linking judged
    26647 and linked 205.
  - Cases: the trace opened 60, and all 60 were written.
  - The ladder started at 19:00:09. Spent so far: $25.94.

- 2026-11-18 19:04: **new-1 Step 1 stopped, `complete_with_failures`.**
  - 1890 calls, $22.03. One manifest item failed: gnews:24da4cc269dbf1a4b9fdf76b. On the send and again on its own retry, the answer
    left out the required `figures` field of evidence items 2 to 4 (`SchemaError`).
  - The draw is now awaiting a redo decision.
  - This is an answer that does not fit its schema after its retry, so D449 makes it eligible for a redo, and plan §3 allows one per
    component.
- 2026-11-18 19:05: **new-1 Step 1 redo launched,** with the reason recorded, through `launch_comparison.py`.
  - The launch checks passed: no uncommitted code, versions manifest unchanged, guard $65.
  - New pid 92883, folder `step1-redo`, running from empty.
  - **Projection:** the first attempt cost $22.03. The redo should cost about $21, then Step 2 about $5, the ladder about $7, and the
    judge $5 to $10. That puts new-1 at about $60 to $65, at its $65 guard. If the guard stops it, the draw gives no release verdict
    (plan §1.4 item 10).
  - **Timing:** expected to finish by about 15:00 to 17:00 on 11-19, inside D667's 72-hour window, which closes 2026-11-20 22:36.
- 2026-11-18 19:05: **The Mac is on battery,** at 12% with about 40 minutes left. Four draws are live: new-1 redo, new-2 judge, new-3
  Step 1.
  - If the machine dies, the launchers die and the draws stop.
  - Alex was notified to plug in the charger. A power monitor is armed.
- 2026-11-18 19:06: AC power back (13%, charging); no draw lost. The power monitor stays on for source changes.
- 2026-11-18 ~20:10: new-3 Step 1 ended with `status complete`, `error None`, 1892 calls. Step 2 started. new-2's judge stands at $33.28 so far: $0.91 in its first 66 minutes.
- 2026-11-18 20:56: **new-2 complete**, at $34.66 in all.
  - By component: Step 1 $21.14; Step 2 about $4.80; the ladder about $6.40; the judge about $2.30, against the plan's $5 to $10.
  - Revised projection for new-1, which pays for the Step 1 redo: about $22.0 + $21.2 + $4.8 + $6.4 + $2.3 = about $57. That is under
    its $65 guard, with about $8 to spare.
- 2026-11-18 21:03: new-3 Step 2 and cases done; ladder started ($27.76). Step 2: groups 2324; outcomes {'new': 2193, 'repeat': 2956, 'revision': 131}; refused 0; several same_statement answers 1306; later linking: judged 28281, linked 135, pending 0. Cases: new-3: 60 cases written to poc/data/comparison-2026-11-17/run/new-3/cases/cases.json (the trace opened 60)
- 2026-11-18 21:02: Mac unplugged at 100%. Alex was notified to keep it on power overnight; new-1's redo needs about 18 h.
- 2026-11-18 22:57: **new-3 complete**, at $37.64 in all.
  - Step 1 $21.3; Step 2 and the cases about $6.4; the ladder about $6.9; the judge about $3.0.
  - Five of the six draws are complete. new-1's Step 1 redo, launched at 19:05, is still running.
  - Eligibility and the reading wait for all six draws, so nothing is read before then.
- 2026-11-19 00:54: AC power back at 39% and charging, after about 4 h on battery. No draw was lost; new-1's Step 1 redo continues ($27.8).
- 2026-11-19 10:55: **Alex:** "i think you are really wasting my time and money with my reruns, just get it done and tell me the results".
  - Asked whether to wait for new-1 (about 4 h, about $17) or stop it and score the five finished draws. **He chose: "Let it finish, then score".**
  - No new reruns.
  - `reading-chain.sh` started detached (pid in `poc/data/comparison-2026-11-17/reading-chain.pid`). It waits for new-1 to complete, then
    runs the CURRENT_STATE order: eligibility, then mapping, then cards, then the verdict, then the release checks. Outputs go to
    `poc/data/comparison-2026-11-17/reading/`.

- 2026-11-19 12:27: **new-1's Step 1 redo stopped**, again `complete_with_failures`. It failed on the same single item
  (gnews:24da4cc269dbf1a4b9fdf76b), with the same `SchemaError` (`figures` missing on evidence items 2 to 4), on the send and on its retry.
  - Under D449 this second stop ends the draw: new-1 is `stopped`, and its ledger stopped at $43.36.
  - There is **no release verdict** (plan §1.4 item 10). The reading chain exited unread.
  - **My mistake:** the failure was reproducible, and I relaunched a full Step 1 (about 17 h and about $21) without first re-sending
    that one stored request, which is a cent and a few seconds (AGENTS §7.3, "a model call is a sampler, re-send before calling it a
    defect"; small first). Re-sending it would have shown that the redo could not pass.
- 2026-11-19 12:30: **diagnostic reading of the five finished draws started** (`diagnostic-chain.sh`, pid in
  `diagnostic-chain.pid`), as the plan directs: "what finished goes to Alex as a diagnostic, with the cause".
  - Same tools, with the export's `--diagnostic` mode, and a labelled diagnostic count: a matter is served when it is served in 2 of the
    system's finished draws.
  - Readers are the codex and claude command-line tools. No system is rerun.
- 2026-11-19 12:36: **Alex:** "just look at this single article what the fuck is wrong and just do it individually".
  - **What was wrong.** At step1-redo sequence 365 the model wrote 5 evidence items. For items 2 to 4, which are qualitative and carry no
    number, it left out the `figures` key, where the schema requires `figures: []`. Item 1 had no number either and did write `[]`.
    - The other new draws hit the same thing: new-2 failed the first send identically and passed on its retry; new-3 passed first time.
    - It is a sampler failure: new-1 failed 4 sends of 4.
  - **What was done** (`single_item.py`):
    - The item was sent alone through Step 1's own `run`, with the open theses it met (that row's `before_state`). The request was
      byte-identical to the stored one. It passed first time. It opened 0 theses, and its `after_state` equals row 366's
      `before_state`, so every later row stays valid.
    - The send was charged on `ledgers/new-1-item.json` ($2 ceiling).
    - It was spliced into a copy, `new-1/step1-patched/trace.sqlite`, which now has 1884 of 1884 rows complete. The originals are kept.
    - Backups were made of `run.json` and the ledger (`*.bak-20261119-before-single-item`).
    - The ledger stop was cleared, Step 1 marked completed in `step1-patched`, and new-1 relaunched normally at 12:40. Step 2 started.
    - **This departs from D449's whole-component redo, on Alex's instruction.**
  - **The release chain** (`reading-chain.sh`) was restarted and waits for new-1. Before its deck it sets the diagnostic deck key aside.
- 2026-11-19 ~13:40: **DIAGNOSTIC result on the five finished draws** (`reading-diagnostic/diagnostic-count.json`; not a release verdict).
  - **Controls:** all pass. 6/6 plants caught, 4/4 supported controls supported, 3/3 repeats the same.
  - **Served matters (N = 32, margin 5):**
    | | new | old | a (new only) | b (old only) |
    |---|---|---|---|---|
    | Counting 1 | 3 | 10 | 0 | 7 |
    | Counting 2 | 2 | 10 | 0 | 8 |
  - **Best case for the new system if new-1 served every matter served in new-2 or new-3:** new 4–5, old 10, a = 1, b = 6–7. That is
    still no lead for the new system, and b − a ≥ 5.
  - **What the old system serves and the new one misses:** M04 hyperscaler capex, M06 FY27 data-center revenue, M10 and M11 FY28 margin
    and revenue, M17 the Anthropic anchor investment, M18 the FY27 gross margin.
  - **What the new system serves:** M13, M15, M31, plus M19 and M32 in one draw only.
- 2026-11-19 12:55: **Alex chose "Stop it now"**: new-1 cannot change the conclusion.
  - new-1's launcher was stopped by SIGTERM in Step 2. Its record shows `crashed`, at $45.29.
  - The release chain was stopped too. No process is left.
  - **Final paid spend:** about $145 in all.
    - Old system: $27.26 for its three draws.
    - New system: new-2 $34.66, new-3 $37.64, new-1 $45.29, plus the $0.12 single-item send.
  - **The answer stands as the 5-draw diagnostic:** the new system loses (served: new 2–3, old 10).
- 2026-11-19 ~13:30: **Why the new system loses.** This is the D674 round's diagnosis, $0, from stored traces and libraries.
  - **The new libraries hold no question on the company's own figures.** Of their 33–41 questions, none is on revenue, data-center
    revenue, gross margin or hyperscaler capex. They are deals, investments, shipments and regulators. The old libraries open FY27
    revenue, FY28 revenue, FY27 data-center revenue, FY27 gross margin and hyperscaler capex from 07-02 to 07-08.
  - **The new system extracts the evidence but files no question for it.** new-2's Step 1 extracted 642 evidence items on
    revenue, margin or capex; 336 were linked elsewhere and 306 kept unlinked.
  - **The cause is the prompt's rule, by decision:**
    - D382 (Alex: "我觉得财务类型不应该是thesis，而更多的是条件…"): "a company's own figures are conditions, not questions".
    - D384: "opens only the big matters", with class A, the main-driver quantity, left out under D382.
    - The week acceptance (2026-09-22..28) already found the same thing: the clean path lacked FY27 and FY28 revenue and the FY28
      margin, and its stored reasoning named this do-not-open sentence.
  - **Size of the class.** 7 of the 32 matters are company figures (M06, M07, M09, M10, M11, M18, M30). The old system serves 5–6 of
    them and the new system 0. That is 4 of the old system's 7–8 old-only matters.
  - **Outside the company figures** the new system still trails: old serves 6 and new 3. It misses M04, hyperscaler capex (a shared
    quantity, which D384 allows), M17, the Anthropic anchor investment (an obligation), and M19 in 2 of its draws.
- 2026-11-19 ~14:00: **The goal's loop stops, on its limits.**
  - **A pass needs much broader opening.** At least 9 of 14 rule-allowed matters under D382, against 0–1 today, or D382 reversed. The $0
    census found three loss points, and none yields to a wording fix.
  - **Confirming any candidate needs a full comparison,** about $110. That is above D439's $40 ceiling, so it starts only on Alex's word.
  - **Probe spend this round:** about $3 by the ledgers.

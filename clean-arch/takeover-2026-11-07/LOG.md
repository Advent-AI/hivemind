# Step 1 takeover log (Claude, from 2026-11-07)

Alex, 2026-11-07: "是你停止他的工作，接收他的goal 然后你来看这些和新发现怎么锁定问题开始修改最大的几个问题并严谨的测试" (stop Codex's work, take over its goal,
lock down the problems from what it found, start fixing the largest ones, and test them rigorously).

Codex's goal, taken over as it stood: run the Step 1 loop, reflect, plan, execute and log what was tried, until Step 1 is stable and
"fully working to production grade".

**Working bar (mine; to confirm with Alex):** "production grade" means the clean Step 1 is, on the same articles, at least as good as
frozen production's extraction (poc-v108, prompt v74i) at what reaches the ledger. That is: as many helpful matters, no more noise, no
more wrong statements. It must also keep the clean contract Alex decided: thesis–evidence pairs, reuse of open theses, no duplicates.
Production is the reference because it is the measured, frozen extraction and the same model (gpt-6-luna, low reasoning). Alex also
told Codex: "read the previous code and scripts we already had this working before, DO NOT reinvent the wheel".

## 0. Handover

- **Stopped:** Codex's goal was cleared and its running turn interrupted through the Codex app-server (`thread/goal/clear` with
  `origin: user`, then `turn/interrupt`). The leftover read-only Claude reviewer it had started was stopped. No model run was live.
- **Uncommitted work preserved:** its uncommitted work (36 result documents, the `clean-arch/step1/` runner, the
  `src/hivemind/model.py` transport change, PRD/HTML and `docs/CURRENT_STATE.md` edits) is left in the working tree untouched. A tar
  backup is at `<scratchpad>/codex-handover-backup-2026-11-07.tar.gz`.
- **Codex's state:**
  - one 49-article forward run (2026-07-08..09, NVDA, empty start, the PRD prompt), which ended with 22 theses and 160 evidence items;
  - 1.5 days of diagnostics on citation completeness, source cleaning and meaning changes;
  - 11 candidate changes "not adopted", none adopted;
  - the forward run was never re-run with a fix.

## 1. Census: what is wrong, by size ($0 model, four blind Codex readers)

**Question.** On the same 49 articles, what does the clean Step 1 get wrong, and how big is each class? The comparison is with frozen
production on identical text.

**Method.**
- **Data:** production's benchmark draw `control-v108-d1` (sealed worktree), whose stored handovers cover all 49 articles; production's
  kept evidence is used, after its code drops.
- **Blinding:** each arm reduced to `{summary, quotes}`; which arm is A or B is drawn per article; the key is kept outside the repo.
  (`build_census_packets.py`, `tally_census.py`, packets and answers in `poc/data/clean-step1-takeover-2026-11-07/`.)
- **Reading:** readers listed each article's matters from the text (D250 unit) with weights from the signed standard (§6), then marked
  each arm's coverage, its extras by not-kept class and wrong statements.
- **Size:** one draw per arm.

**Spot check.** The reader's article 34 verdict (clean misses the Kyber report, the denial, the launch timing, the Q2 guidance and the
China assumption) and article 36 verdict (clean misses the $1tn visibility) match what I traced from the raw answers.

| On 49 articles, 115 helpful matters (core + supporting) | Clean Step 1 | Production v108 (d1) |
|---|---|---|
| Helpful matters covered (yes / partial / no) | 97 / 2 / 16 | 66 / 11 / 38 |
| Core matters covered (yes / partial / no) | 35 / 2 / 7 | 34 / 4 / 6 |
| Extras (items an analyst would not keep) | **70** (26 benchmark or specification, 24 generic commentary, 7 background, 7 optional, 4 other, 2 repeated) | 15 |
| Wrong statements | 4 | 6 |

**Classes, largest first:**

1. **Noise.** 70 of the clean run's 160 items (44%) are things the standard does not keep, 4.7 times production. Benchmark or
   specification and generic commentary are 50 of the 70.
2. **Core misses concentrated in dense recap articles.** 6 of the 7 clean core misses are in articles 34 and 36.
3. **Meaning changes.** 4 against production's 6: no worse than production. This is the class Codex spent most of its time on.
4. **Clean's strength.** Clean covers 33 helpful matters production misses. Many are statements production writes and then drops with
   no home (the E1 class).

Any fix must keep that strength.

## 2. Round 1: candidate K1, production's evidence reading inside the clean contract

**Mechanism read from the requests.**

The clean system prompt:
- is thesis-first ("Extract thesis–evidence pairs");
- defines evidence as anything that "supports, challenges or adds context", which is wider than the standard;
- puts a compressed not-kept list in the system text, before the article.

Production's v74i:
- is evidence-first ("Your first job is evidence … then file each one");
- carries the signed four kinds with cross-industry examples;
- ends the whole request with the full signed closing check (`review-v74i.txt`), after the article. AGENTS §6 requires that placement.

**Change (K1, `k1-system.txt` + `k1-closing.txt`).**
- The ROLE and evidence sections now use v74i's evidence-first text and four kinds.
- The clean linking rules, thesis rules (Alex's looser opening), tier, dates and schema are unchanged.
- The final check moves to the very end of the user message, as v74i's closing check plus three thesis and link lines.
- The article, open theses and schema are byte-identical to the stored requests.
- System + closing text grows from 13,427 to 18,473 characters (about 1,250 tokens). Reason: the full signed not-kept rows replace the
  compressed list that let 70 extras through.

**Probe.**
- **Articles (16):** 8 noisiest (6, 8, 16, 18, 19, 20, 33, 37), 3 with core misses (2, 34, 36) and 5 where clean beat production
  (10, 22, 30, 41, 43), each sent from its stored before-state.
- **Draws:** control = the stored request re-sent (identity checked byte for byte), 3 draws; K1, 3 draws.
- **Size and cost:** 96 calls, $0.089 at published rates, no failures.
- **Scoring:** blind readers against the census matter lists, which were written before K1 existed.

| 16 articles × 3 draws | Control (clean prompt) | K1 |
|---|---|---|
| Helpful matter-answers covered (yes / partial / no) | 112 / 7 / 28 | 95 / 8 / 44 |
| Core (yes / partial / no) | 48 / 6 / 18 | 49 / 3 / 20 |
| Extras | 77 (40 benchmark/spec, 21 commentary) | **27** (13 benchmark/spec, 7 commentary) |
| Wrong statements | 10 | 6 |

**Regressions first.** K1 lost helpful matters in these places:
- article 10: NVIDIA's reported $6.3bn CoreWeave capacity guarantee through 2032, core, 0/3 against 3/3; also observers on spare
  hyperscaler capacity, 0/3;
- article 16: Vector Core Compute as an early deployer of the SambaNova–Intel offering, 0/3;
- article 19: Perplexity using Vera, 0/3;
- one draw each on articles 2, 8, 33 and 41.

**Mechanism of the regression.** v74i's background row rejects "a deal the item mentions as already existing … even with its amount"
and dated earlier contracts. It was written for production, which has no later step that compares a statement with stored evidence.
In the clean architecture that step exists, by Alex's design [12]: "then in the nex stage I can just dedup this evidence without
having the need to read the full evidence in pre-promt". Alex's own D243 words keep background "带数字和具体的叙事" (with a number and a
specific narrative). The row is stricter than both.

**Also observed:**
- Article 36's $1tn visibility, missed in the original run, came back in 3/3 control re-sends: sampler noise, not a defect.
- Article 34's Kyber report stays missing under both arms (0/3). It is a retelling inside a recap article, and the run had already
  opened a Kyber thesis from an earlier article. Its product cost is low; it is not chased further now.

**Verdict:** K1 removes most of the noise but regresses one class. It is not adopted as is.

## 3. Round 2: candidate K2, K1 with the "already existing" ground removed for specific statements

**Change (`k2-closing.txt`; system text unchanged from K1):**
- "new" now means new to an analyst following the company, not whether it was reported before;
- a statement with its own figure, term, named counterparty or specific step keeps its place when retold, because Step 2 records the
  repeat;
- a commitment, guarantee, contract or investment stated with its amount, term or counterparty is kept even when described as
  existing;
- background without a figure or a specific step is still not kept.

**Probe:** the same 16 articles, 3 draws, 48 calls, $0.043. All 144 answers (control, K1, K2) are scored together by the same blind
readers.

**Result (all 144 answers in one blind read; 16 articles × 3 draws each):**

| | Control (clean prompt) | K1 | K2 |
|---|---|---|---|
| Helpful matter-answers covered (yes / partial / no) | 110 / 7 / 30 | 92 / 11 / 44 | 100 / 11 / 36 |
| Core (yes / partial / no) | 50 / 4 / 18 | 48 / 4 / 20 | **57 / 5 / 10** |
| Extras | 80 (44 benchmark/spec, 21 commentary) | 27 | 47 (13 benchmark/spec, 8 commentary, 16 optional) |
| Wrong statements | 7 | 5 | 8 |

**Regressions first.** K2 covers 10 fewer helpful matter-answers than control. Matter by matter:
- **Borderline under the signed rows** (the background row and the generic-commentary row):
  - article 19: Perplexity describing Vera's gains in use;
  - article 22: BofA's "700 times since 2015";
  - article 20: OpenMind founder's strategy view;
  - article 10: the circularity concern.
- **Technology-roadmap statements in article 41** (copper limits, optics later). K1, whose system text is identical to K2's, covered
  them 2/3 and 1y2p, so the K1–K2 difference there is within sampling.
- **Partial rather than missing:** article 10's capacity-guarantee item (3/3 partial).

**Gains:**
- Article 34's Kyber report, denial, Q2 guidance and China assumption: 12 of 21 matter-answers yes, against 2 for control.
- Core misses are down from 18 to 10.
- Noise is down 41%. Article 34 also gains recap Q1 actuals with figures; the reader classes them optional, and Step 2 compares
  each with stored evidence.

**Theses** (control 27 new across 48 answers, K2 35): no duplicate of an open thesis seen in a direct read of all 96. K2 opened a
valuation thesis in article 37 (2 of 3) and a vague robotics-competition thesis in article 20 (2 of 3).

**Contract:** 1 of 48 K2 answers linked two items to a new thesis it never declared (article 18 d1). The runner keeps the link visible
as unresolved; control had 0 and K1 had 0.

**Verdict.** K2 is the candidate for the whole-bench test: a forward run over all 49 articles. Its core coverage is clearly better,
noise is down by two fifths, and wrong statements are level. The supporting-item loss is mostly borderline items and is checked
again on the whole run.

## 4. Runner change for the candidate

- `runner.run(..., texts=(system, closing))` sends a candidate's system text and appends its closing check to the end of the user
  message, after the item. The schema still comes from the PRD. `run_live.py --system --closing` passes them.
- Test `test_candidate_closing_check_ends_the_user_message_after_the_item` proves the closing check is the last text sent.
  - Mutant: moving the check before the payload fails the test's first assertion (`AssertionError`, traceback read).
  - The unmutated control passes.
- The first mutant attempt passed because of a stale bytecode cache: the mutated line had the same length and the same mtime second.
  Rerun with `__pycache__` removed and `PYTHONDONTWRITEBYTECODE=1`.
- Step 1 tests: 49 pass.

## 5. Whole-bench test: K2 forward run over the 49 articles

- **Setup:** the same source database, manifest, empty starting library and settings as the original run (`forward-k2/`, pinned by
  `SHA256SUMS`).
- **Order:** sequential, so each article sees the library the previous article produced.
- **Scoring:** blind, three answers per article (original clean run, K2, production d1) against the census matter lists, with a link
  check. A separate blind read compares the two final thesis libraries for duplicates and noisy theses.

**Result, whole run on the 49 articles (one forward draw each, five blind readers):**

| 49 articles, 121 helpful matters | Original clean run | K2 | Production v108 d1 |
|---|---|---|---|
| Helpful covered (yes / partial / no) | 100 / 3 / 18 | 96 / 6 / 19 | 65 / 13 / 43 |
| Core (yes / partial / no) | 34 / 3 / 7 | **40 / 2 / 2** | 34 / 4 / 6 |
| Extras | 67 | **27** | 18 |
| Wrong statements | 2 | 3 | 5 |
| Wrong links (item filed under a question it does not inform) | **56** | 18 | 17 |
| Final library: size / duplicates / noisy / good | 22 / 1 / 8 / 13 | 26 / 0 / 9 / 17 | n/a |

- The run completed 49 of 49; the original run stopped once, at article 21.
- **A class the census missed:** the original run filed 56 items under questions they do not inform. K2 brings that to production's
  level (18 against 17).
- **Remaining gaps against production:**
  - noise, 27 against 18;
  - noisy theses: 9 of 26, mostly a single small investment, partnership or integration (Firmus, Gradium, d-Matrix with Parasail,
    LeRobot, L&T with Fortanix, FEV, GROMACS), plus a trades-training programme and a share-valuation thesis.

## 6. Frozen-ruler check on held-out articles (golden-v5 dev, code matching from `score_gold.py`)

**Setup.**
- 115 runnable gold articles (3 excluded: two are identified copies, one is not fed), in publication order from an empty library.
- Arms: the current PRD prompt (control) and K2.
- Only 9 of these articles are in the 49 used to design the candidates.
- Scorer: `score_gold_runs.py`, which uses the frozen scorer's `same` and `same_matter`. It printed the gold sha256 `6f9476bb…`,
  matching `golden-v5.sha256`.
- Scorer check: production's stored draws score 167 / 171 / 162 helpful matters of 234 on all 115 articles. The benchmark reported
  166 / 170 / 162.

**Process error (mine).**
- Both runs stopped early (control at 109 articles, K2 at 93) on "live run limit reached before send".
- I copied the 49-article limits without scaling `max_usd`, and the transport reserves at conservative rates
  ($0.50 / $1.00 per M against the published $0.10 / $0.50).
- Both were continued from their last completed state as documented segments (`*-segment-2`, with `continuation.json`).

**Result on the 93 articles both had finished (one draw each):**

| 93 articles, 197 helpful entries | Clean control | K2 | Production d1 / d2 / d3 |
|---|---|---|---|
| Helpful matters kept | 173 | **179** | 135 / 140 / 135 |
| Core kept (of 76) | 72 | 70 | 66 / 67 / 68 |
| Items matching a not-kept span | 114 | **59** | 26 / 30 / 27 |

**Reading the 59 by the gold's reject row.** The largest group is 10 items under "D250 第 1 条：只描述一个现成安排、没有新动作".
Reading them shows my K2 change caused it:
- the CoreWeave agreement "signed in September 2025 … initial value of $6.3bn" (the gold marks it not kept under that row);
- NVIDIA and Corning's plants announced earlier in the year;
- IREN's May contract;
- GPU rental deals described as in place.

The census readers had called the CoreWeave figure core. The signed gold does not; the frozen ruler governs (AGENTS §7.1, D263).
**K1's drop of that item was right, and K2's "a commitment … stated with its amount … is kept even when … already existing" goes
beyond the signed D250 boundary 1.**

## 7. Rounds 3–5: noisy theses, then the D250 boundary

**K3** (`k3-system.txt`). Source: AGENTS §8 and Alex 2026-10-30, "不要搜集一堆鸡毛蒜皮的事情，要看重要的大事".
- A single investment, partnership, integration, deployment, programme or feature opens a thesis only when its own scale can change
  revenue, profit, cash or credit risk. Otherwise it is evidence for the broader thesis it informs.
- Added a valuation counterexample.
- This replaces Codex's line "A deal, investment, product or project may merit tracking even when its business impact is not yet
  known".
- Alex's 2026-11-06 remark "no need to be very strict in opening … just don't open 'noisy' thesis" answered a question about form
  (question types, dates), not scale. The exchange was read in the Codex thread.

Probe (20 articles × 3 draws, K2 before-states, $0.106): new theses fell from 57 to 41.
- No longer opened: GROMACS, valuation, Gradium (its evidence links to open theses).
- Broadened: d-Matrix, LeRobot, L&T and FEV became broader adoption or partnership theses.
- Still opened: Firmus. A sized, not yet completed stake is a binding obligation under the signed opening reasons, so this is right.
- Regression: the HBM gross-margin thesis in article 15 was not opened (0 of 3 against 3 of 3); its evidence went to the FY2027
  profit thesis.

**K4.** Adds, as examples of big matters, the signed main-driver and opening reasons: the segment that carries the business, gross
margin, capital spending, the next generation's launch, a deciding policy process, a competitor's or customer's move, and an
obligation in the company's own name.

Probe (14 articles × 3 draws, $0.058):
- The margin thesis stays unopened (0 of 3).
- The other differences from K3 look like sampling: the Vera CPU thesis is 3 of 3 under K3 and 0 of 3 under K4.

I stopped tuning thesis opening on probes. The remaining differences are judgment calls, and their noise exceeds their signal
(AGENTS §1, §7.3). K4's system text is carried into K5 and judged on the whole run.

**K5** (`k5-closing.txt`; system text = K4).
- The closing check is production's v74i check plus one sentence: "Do not drop a reported step, figure, guidance, forecast or decision
  because the item retells it or another outlet reported it before: a later step compares each statement with the evidence already
  stored and records a repeat there."
- K2's arrangement wording is reverted to production's (D250 boundary 1).
- Probe on the 16 gold articles where K2 kept not-kept items (3 draws each, scored on golden-v5, $0.092):

| 16 gold articles × 3 draws | K2 | K5 |
|---|---|---|
| Helpful matters kept (of 147) | 129 | 132 |
| Core kept (of 54) | 51 | 51 |
| Not-kept kept | 52 (16 under D250 boundary 1) | **40** (3 under boundary 1) |

**Regressions first:**
- Article 34's retold Kyber report comes back in 1 of 3 draws under K5, against 3 of 3 under K2.
- Article 10's CoreWeave figure is no longer kept, in line with the gold.
- The Kyber setback is already filed in the same run from article 10, so the product cost of article 34's retelling is low.

**Whole-bench test of K5:** a forward run over all 115 gold articles, scored on golden-v5 against control and K2 (both continued to
115), and a forward run over the 49 articles, read blind with the library review.

## 8. Whole-bench results for K5

**On the 49 articles (one forward draw each; four answers per article read blind by four readers; three libraries ranked by a
fifth):**

| 49 articles, 122 helpful matters | Original clean run | K2 | K5 | Production d1 |
|---|---|---|---|---|
| Helpful covered (yes / partial / no) | 99 / 3 / 20 | 99 / 3 / 20 | 77 / 7 / 38 | 67 / 11 / 44 |
| Core (yes / partial / no) | 34 / 3 / 7 | 41 / 1 / 2 | 37 / 5 / 2 | 34 / 4 / 6 |
| Extras | 66 | 27 | **22** | 18 |
| Wrong statements | 3 | 1 | 3 | 7 |
| Wrong links | 46 | 13 | 14 | 5 |
| Library: size / duplicates / noisy / good | 22 / 1 / 8 / 13 | 26 / 0 / 9 / 17 | **16 / 0 / 1 / 15** | n/a |
| Library rank (blind) | 3rd | 2nd | **1st** | n/a |

**Regressions first: K5 misses 24 helpful matters that K2 covers.** Read one by one, they fall into three groups:
1. **Not kept under the signed standard:** the CoreWeave $6.3bn agreement (D250 boundary 1).
2. **Small matters that open no thesis under Alex's granularity rule:**
   - Gradium's seed round, three items;
   - L&T Vyoma–Fortanix;
   - FEV–Microsoft;
   - the trades-training programme;
   - Shield TV availability;
   - a GeForce NOW server;
   - Parasail's expansion plans;
   - Cerebras's IPO.

   With no thesis open for them, the pairing rule drops them.
3. **Competitive and demand signals, which reach the product's theses in K2's single draw:**
   - article 14: the H20 guidance from Beijing, and buyers evaluating Hygon and Cambricon;
   - article 42: Tesla's AI5;
   - article 20: Qualcomm's and Intel's robotics offerings.

   K5 opened the China substitution thesis in article 14 and filed ten custom-silicon items in article 42. The specific items it
   missed are not systematic in the probes: on the 16 gold articles from fixed before-states, K5 kept 132 helpful matters against
   K2's 129.

**On the 115 gold articles (golden-v5 dev, frozen; code matching from `score_gold.py`; gold sha256 `6f9476bb…`; one forward draw
each; control and K2 continued to 115 as segments):**

| 115 articles, 234 helpful entries (86 core) | Clean control (PRD prompt) | K2 | K5 | Production d1 / d2 / d3 |
|---|---|---|---|---|
| Helpful matters kept | 200 | **211** | 196 | 167 / 171 / 162 |
| Core kept | 79 | 79 | **80** | 76 / 76 / 75 |
| Items returned | 383 | 379 | 322 | 278 / 301 / 287 |
| Items matching a not-kept span | 136 | 77 | **50** | 30 / 34 / 34 |
| Final thesis library | 34 | 57 | **32** | n/a |
| Cost at published rates | $0.149 | $0.171 | $0.152 | n/a |

## 9. Where Step 1 stands, and the choice for Alex

**Fixed, against the clean prompt Codex left (on the frozen ruler and in the blind reads):**
- noise is down 63% (136 to 50 not-kept spans on 115 articles; 66 to 22 extras on the 49);
- wrong links are down 70% (46 to 14);
- core misses are down from 7 to 2 on the 49;
- core is level or better on the 115 (80 of 86);
- no duplicate thesis, and the library is ranked best blind (15 of 16 good bets).

Against frozen production, K5 keeps 25 to 34 more helpful matters on 115 articles (196 against 162–171) and more core matters (80
against 75–76).

**Not yet at production's level (open defects):**
- noise is 50 against 30–34;
- wrong links are 14 against production's 5 in the same blind read.

Both are the next class to work on.

**A product choice for Alex, K5 (recommended) or K2:**
- K2 opens theses for single small investments, partnerships and integrations. It keeps 15 more helpful matters on 115 articles,
  but its library grows to 57 theses in two weeks, a third of them noisy, with half again as much noise.
- K5 opens only big matters (Alex, 2026-10-30: "不要搜集一堆鸡毛蒜皮的事情，要看重要的大事"). Statements about small matters with no
  broader thesis open are dropped under the pairing rule.

**Not done:**
- The PRD prompt is unchanged. Adopting K5 means putting its system text and closing check into PRD §12 and having the runner read
  the closing check from there; this waits for Alex's choice.
- Nothing is committed.
- The source-data track (cleaner losses, contamination) is untouched. It is real but small in these runs: articles 2, 3 and 16 of
  the 49.

## 10. Alex chose K5; trace review for production readiness (2026-11-07)

Alex: "1. 没问题，这个版本你觉得整体效果质量适合生产吗？你看完trace 给我反馈".

**Read, all on the K5 115-article gold run unless stated:**
- every helpful gold entry K5 missed (38), beside its raw answer;
- every item matching a not-kept span (50);
- the final library (32 theses), with evidence counts;
- a mechanical census of both K5 runs;
- a blind field audit by four Codex readers: 40 random K5 items and 40 random production items from the same gold articles, put in
  one shape and shuffled (`build_field_audit.py`, `field-audit/`).

**Mechanical census:**
- 115 of 115 and 49 of 49 articles completed;
- 0 unresolved links, 0 lookup errors;
- 4 of 416 passages unverified.

**The 38 misses, by mechanism:**
1. A one-line statement about the company buried in another story (real defects, the core ones):
   - Rubin release in the second half of 2026 (#100);
   - Rubin Ultra four-die design cancelled (#68);
   - Huang's "$60 of every $100" (#21; K5 instead kept six emissions items and opened an emissions thesis);
   - $55k per Rubin GPU (#75);
   - China share at zero (#30, partly covered).
2. Dense articles stop early: SemiAnalysis's backstop piece, 9 items kept and 6 supporting entries missed (#54).
3. Customers' and suppliers' own figures skipped: Microsoft's $627bn RPO, Micron's revenue and margin, Corning's growth plan.
4. Small partner integrations, the K5 trade-off Alex accepted (#6, #9, #25, #32, #65, #77, #84, #111).

**The 50 not-kept items:**
- framing and background, generic commentary, product details without scale, other companies' matters, adjective-only quotes;
- none is a wrong fact;
- 46 of the 50 are filed under big theses, only 4 solely under small ones. So noise and small theses are separate classes. My guess that
  small theses give noise a home is refuted.

**Library after 115 articles (32 theses):**
- About 11 are small or against the signed opening rules:
  - an executive transition (v74i excludes "executive appointments");
  - Omniverse made free;
  - DLSS in games;
  - the RTX 50 SUPER launch (a variant of a product on sale);
  - a Beersheva R&D centre;
  - orbital data centres;
  - Chinese lidar policy;
  - Valar nuclear exploration;
  - a liquid-cooling supplier;
  - the company's own debt raise;
  - the Intel stake with Xeon selection.
- Fragmented bets: four theses on NVIDIA financing customers (credit-support model, GPU backstop exposure, lease backstops, customer
  financing); three on competing chips.
- Catch-alls: "demand → revenue growth" holds 58 items, the cloud credit-support model 52.
- The 49-article library (15 of 16 good) did not show this; the drift appears over a longer window.

**Blind field audit (40 items each):**

| Field correct | K5 | Production |
|---|---|---|
| Summary | 37 | 35 |
| Passages support the summary | 35 | 34 |
| Original party | 35 | 31 |
| Reporting speaker | 39 | 40 |
| Tier | 35 | 33 |
| Statement date | 34 | 30 |
| Period | **40** | 26 |
| Links correct | **37 of 44** | 29 of 43 |
| Worth keeping (yes / borderline / no) | 26 / 6 / 8 | 26 / 9 / 5 |

K5's recurring field errors:
- an unconfirmed claim given a tier other than rumour (2);
- a party's plans attributed to the reporter;
- a passage that misses one claim of the summary (5 of 40);
- the article's date used as the statement date (2).

**Verdict: not ready for production yet.**
- **Evidence capture** is ahead of frozen production on recall (196 against 162–171 of 234 helpful; core 80 against 75–76) and on
  per-field accuracy and links.
- **It is behind on three things:**
  - noise: 50 against 30–34 not-kept spans; 8 of 40 sampled items not worth keeping against 5;
  - library hygiene over a longer window: about a third small theses after two weeks, fragmented bets, catch-alls, and no way to
    close a thesis, so the library only grows;
  - one-line core statements buried in other stories.
- The clean pipeline also does not run end to end: Step 2 (search and Jev), Step 3 (the writer) and Step 4 are not built.

**Recommended next fix: library hygiene, because it compounds.** Every noisy thesis stays open and attracts evidence. The fix
restores the signed "do not open" list from v74i, which the clean prompt dropped (executive appointments, the company's own
borrowing, buyback authorisations, variants or features of products on sale, quarterly figures), and states one bet = one question
for financing and competition. Test: a 115-article forward run, with a pass line for Alex to confirm (at most 3 small theses, no
fragmented bets, helpful at least 190). Noise and buried one-liners follow.

## 11. Goal: fix the thesis library to the pass line (from 2026-11-07, Alex's /goal)

**Alex's goal:** "按你的过关线开始修观点库". The pass line he accepted, measured on the 115 gold articles, forward from empty, one draw:
- at most 3 small theses;
- no fragmented bets;
- helpful matters at least 190 of 234.

Other instructions:
- run the council skill (Claude and Codex) on the traces every round;
- consider prompt restructuring, pipeline changes, other models and reasoning effort;
- iterate systematically.

Council record: `clean-arch/takeover-2026-11-07/council/` (handoffs, Codex replies, JSONL streams). The Codex session
`01a1b799…` is resumed each round.

**Round 1 council (independent):**
- Codex's reading: permissive opening language; v74i's signed boundaries were dropped (executive appointments, own borrowing,
  variants of products on sale); the model saw a related open thesis and still opened a new one (fragments).
- My reading, from the model's own account of 12 small theses ($0.01, `model-account-small-theses.json`): 11 of 12 say the matter is
  not big by its own scale. The model opens a container thesis because pairing forbids evidence without a thesis, and it has already
  judged the statement material.

**Round 2 council:**
- Agreed to test S1: let `links` be empty; code drops the item as no home, visible as `unfiled_evidence` (runner change, with a test
  and a mutant).
- Codex added a K5+S1 arm to isolate S1, and articles #31/#53/#65 for noise.
- The second review call was deferred: it is the shape of the failed split (D378).

**Round-1 probe:** 27 articles (12 small-thesis openers, 5 fragmenters, 7 controls, 3 noise); fixed K5 before-states; 3 draws;
405 calls; $0.53. Gold matching from the frozen scorer, kept evidence only. New theses and unfiled items were read blind by three
Codex readers.

| 27 × 3 | K5 | K5+S1 | K6a (signed boundaries + closest-thesis fields) | K6b (K6a + S1) | K6b medium effort |
|---|---|---|---|---|---|
| Helpful (of 255) | 189 | 173 | 174 | 159 | **217** |
| Core (of 75) | 62 | 62 | 62 | 61 | **72** |
| Not-kept kept | 55 | **25** | 42 | 31 | 68 |
| New theses: bet / small / duplicate | 42 / 19 / 2 | 36 / 9 / 0 | 45 / 12 / 2 | 27 / 5 / 0 | **52 / 9 / 1** |
| Unfiled: fine / should_open / open_takes_it | n/a | 33 / 6 / 0 | n/a | 22 / **22** / 0 | 36 / 2 / 0 |

**Reading:**
- **Medium effort is the largest lever found.** Core rises from 62 to 72 of 75. Codex rechecked: 211 of medium's 217 hits also match
  on the quote, so the gain is not word-overlap scoring.
- **At low effort, K6b over-suppresses:** 22 unfiled big matters. At medium, the same request makes that call correctly.
- **Unfiled helpful entries are mostly small matters** (supplier machine centres, an executive appointment, a nuclear exploration, a
  grid pilot, a GPU-variant rumour, the company's own debt raise). A few are real link misses I read by hand, which the readers
  marked fine:
  - EPS consensus (#38) and a GPU shipment forecast (#21) that the open profit and demand theses take;
  - a conditional valuation (#38) the standard keeps.
- **Medium raises noise** (68 not-kept), at about the same rate per kept item. Codex asks for a blind read of medium's added hits and
  added noise before any prompt change.

**Running:**
- K6b medium forward over all 115 gold articles (the acceptance test; about 50 s per article);
- the decomposition at medium (K5 medium, K6a medium);
- DeepSeek Flash and V4-Pro on K6b, using JSON mode with the schema stated in the system text and checked by code; one Flash smoke
  call cost $0.017.

**Round 3 council (Codex).**
- Medium's gain is mostly real: 211 of 217 hits also match on the quote. I read the 16 added hits myself: 14 are faithful (Huang's
  $60 of $100, CPU:GPU 1:8 → 1:1, Micron's revenue and margin, memory at half of 2027 spend, 75 blocked projects); 2 on #54 are
  quote-only matches.
- Codex asked for the decomposition at medium and a DeepSeek comparison.

**Decomposition at medium (27 × 3):**

| | K5 medium | K6a medium | K6b medium |
|---|---|---|---|
| Helpful | 235 | 214 (1 empty answer failed) | 217 |
| Core | 75 of 75 | 72 | 72 |
| Not-kept | 95 | 78 | 68 |
| Theses: bet / small / duplicate | 93 opened | 61 / 12 / 2 | 53 / 9 / 0 |

- Effort alone gives the most recall but bloats the library.
- S1 still helps at medium: fewer small theses, no duplicates.
- K6b medium's remaining small theses: 6 of 9 are on article 2 (Intel stake, Xeon selection; a near-empty library), 2 on #85
  (lidar), 1 on #1 (Firmus scale).

**Models on K6b** (27 × 3; DeepSeek in JSON mode, schema in system text, checked by code, 0 of 162 failed; $5.78):

| | Luna medium | DeepSeek Flash high | DeepSeek V4-Pro high |
|---|---|---|---|
| Helpful | 217 | 218 | 211 |
| Core | 72 | 70 | 68 |
| Not-kept | 68 | **50** | 50 |
| Theses: bet / small / duplicate | 52 / 9 / 1 | **52 / 2 / 2** | 44 / 7 / 1 |
| Cost per article, time per call | about $0.003, about 50 s | about $0.017, 1–2 min | about $0.05 |

**Round 4 council (Codex).**
- Flash's advantage may come from the request form (schema in the system text, JSON mode) rather than the model. Check: Luna medium in
  the same JSON mode on 10 articles (#2, 15, 32, 85, 92, 95; controls #1, 24, 30, 49), 3 draws.
- Run Flash forward over 115 after Luna.
- Luna's partial run (70 of 115): 18 theses, 1 clear small one (#2 Intel), two risks (#31 microLED, #60 water/nuclear blend), no
  financing fragments so far.

**Runner:** a DeepSeek JSON-mode path was added to `live.py`/`runner.py`. The exact sent request is kept in `raw_response.sent_request`;
a nonconforming answer fails the item. Test `test_deepseek_is_sent_in_json_mode_with_the_schema_and_a_nonconforming_answer_fails`:
dropping the schema text fails its assertion; 51 Step 1 tests pass.

**Running:**
- Luna K6b medium forward over 115 (`gold-k6b-medium`);
- Flash K6b high forward over 115 (`gold-k6b-flash`);
- the Luna JSON-mode check (`round1d-json`).

**Luna JSON-mode check** (10 articles × 3): 8 small theses against 9 under the strict schema. 3 of 30 JSON-mode answers failed the schema
(missing `links` on unfiled items). The request form does not explain Flash's advantage; the model does.

**Luna high effort** (27 × 3): 6 of 81 calls timed out at 180 s; the answered 75 look like medium. Not worth the latency. Medium is
Luna's setting.

## 12. Pass line met: K6b on Luna medium, forward over 115 gold articles (2026-11-07)

Run: `poc/data/clean-step1-takeover-2026-11-07/gold-k6b-medium/` (pinned by `SHA256SUMS`); 115 of 115, 0 failed. Prompt files
`k6b-system.txt`, `k6b-closing.txt`, `k6b-schema.json`; `reasoning_effort: medium`.

| 115 gold articles, one draw | K5 (low) | **K6b medium** | Production d1 / d2 / d3 |
|---|---|---|---|
| Helpful kept (of 234) | 196 | **201** | 167 / 171 / 162 |
| Core kept (of 86) | 80 | **84** | 76 / 76 / 75 |
| Not-kept spans kept | 50 | 61 | 30 / 34 / 34 |
| Final library | 32 | **21** | n/a |
| Unfiled items dropped over the run | n/a | 52 | n/a |

**Library, three independent blind readers** (`library-answer-k5-medium{,-r2,-r3}.json`; same packet, K5 as the other letter):

| | Small | Fragments | Duplicates |
|---|---|---|---|
| K6b medium | 0 / 1 (the Intel stake) / 0 | 0 / 0 / 0 | 0 |
| K5 | 9 / 10 / 9 | 3 / 3 / 2 | — |

**Pass line (at most 3 small, no fragments, helpful at least 190): met.**

**Caveats (agreed with Codex, round 5):**
- **My read disagrees with the readers.** I see 4–5 small theses (Intel stake, physical AI in buildings, Taiwan and Korea power and
  water, microLED interconnects, DSX) and two possible fragments (China access / Huawei / domestic accelerators; credit-support model /
  neocloud demand channel). The library readers saw the libraries without the article text.
- **61 is a match count against not-kept spans,** not a full manual noise count. It is above K5's 50 and production's 30–34.
- **One draw, on the development articles.** A quote match does not prove that the summary or the link is right.

**Noise.**
- The 61 by reject row: framing 15, common-knowledge claims 9, product detail 7, not evidence under the keep rule 7, generic views 7,
  adjective quotes 5, arrangement in place 4, other 7. No class dominates.
- I proposed K7, a per-item `keep_test` enum that code acts on. Codex objected: it merges the type of a statement with the keep
  decision, so noise could be relabelled as "a named party's claim". Agreed: K7 is not tested in that form.
- The next noise evidence is the Flash forward run, compared article by article with the Luna run.

## 13. DeepSeek Flash forward over 115, and council rounds 5–6

**Run.** `gold-k6b-flash/`: same K6b request, `deepseek-flash`, high effort, JSON mode with the schema stated in the system text
and checked by code. 115 of 115, 0 failed, $0.99, 36.6 s per call on average.

| 115 gold articles, one draw | K5 | Luna K6b medium | **Flash K6b high** | Production d1 / d2 / d3 |
|---|---|---|---|---|
| Helpful kept (of 234) | 196 | 201 | **205** | 167 / 171 / 162 |
| Core kept (of 86) | 80 | 84 | **84** | 76 / 76 / 75 |
| Items returned | 322 | 346 | 282 | 278 / 301 / 287 |
| Not-kept spans kept | 50 | 61 | **40** | 30 / 34 / 34 |
| Items matching nothing in the gold | 58 | 52 | **28** | 72 / 84 / 73 |
| Final library | 32 | 21 | 25 | n/a |

**Blind library read: three new readers, the three libraries in one packet** (`library-answer-three-r{1,2,3}.json`):

| | Small | Fragments |
|---|---|---|
| Flash | 3 / 3 / 3 (Intel tie-up, US production expansion, orbital data centres) | 0 / 0 / 0 |
| Luna medium | 1 / 1 / 1 | 0 / 1 / 1 (Huawei threat with China domestic accelerators, the fragment I had flagged) |
| K5 | 10 / 11 / 11 | 5 / 0 / 3 |

**Councils.**
- **Round 5:** Codex agreed the pass line was met for Luna medium and opposed K7 in its merged form.
- **Round 6:**
  - Codex supports Flash high as the preferred candidate, but not yet "production". It passes the pass line on this one run, at
    exactly the limit of 3 small theses, with no margin.
  - The readers note possibly missing bets: China competition, profitability, financing-driven demand.
  - The next test that most changes confidence is a second empty-library Flash forward draw on the same 115 articles.
  - Keep the held-out test articles for the final configuration.
  - Settle the schema-failure policy before launch.

**Running:** Flash K6b forward, draw 2 (`gold-k6b-flash-d2/`, inputs byte-identical to draw 1).

## 14. Flash draw 2, council round 7, and the source-backed thesis review

**Flash draw 2** (`gold-k6b-flash-d2/`, inputs byte-identical to draw 1): 115 of 115, 0 failed.
- Gold: helpful 197, core 85, items 265, not-kept 38, unmatched 21. Draw 1 was 205 / 84 / 282 / 40 / 28.
- Codex's diff of the two draws: 17 new matched misses and 9 recovered, net −8; core +1.

**Library reads without article text varied:** Flash d1 small 3/3/3 and 2/4/5; d2 small 1/3/4; fragments 0 in every read. Luna medium
small 0–1; a fragment was flagged in 2 of 6 reads.

**Round 7 (Codex):**
- Report the small count as "at the line by median, with reader disagreement".
- Resolve the disputed theses with their source articles before changing anything.
- Then settle the schema-failure policy, run the test set with its exposure history stated, and adopt into the PRD last.

**Source-backed review.** Three readers saw each disputed thesis with the article that opened it and the theses open at that moment
(`disputed-theses-packet.json`, `disputed-answer-r{1,2,3}.json`):

| Thesis | Verdicts |
|---|---|
| AI-RAN (Flash d1, d2) | bet ×3 (both draws) |
| US production expansion (Flash d1) | bet ×3 |
| Automotive / autonomous driving (Flash d1) | bet ×3 |
| Huawei threat (Luna clean-11) and China domestic accelerators (Luna clean-19) | both bet ×3: not a fragment |
| Intel $5bn stake with Xeon selection (all three runs) | small 2 of 3 |
| Orbital data centres (Flash d1, d2) | small ×3 |
| Lidar policy (Flash d2) | small ×3 |

**Pass line, with sources:**

| Run | Small | Fragments | Helpful | Pass line |
|---|---|---|---|---|
| Flash d1 | 2 | 0 | 205 | met |
| Flash d2 | 3 | 0 | 197 | met, at the line |
| Luna medium | 1 | 0 | 201 | met |

**Noise:**
- Flash 38–40 against Luna medium's 61 and production's 30–34.
- Against Luna, Flash removes reporter framing (15 → 2), generic views (7 → 2) and adjective quotes (5 → 0).
- Product detail without scale (8–10) remains in both and is the next target.

**Recommendation:** K6b on DeepSeek Flash, high effort, as the Step 1 configuration candidate. It costs about $0.009 per article at
about 37 s per call. Luna medium is the cheaper fallback (about $0.003 per article, about 50 s), with more noise.

**Next, in Codex's order:**
1. Read draw 2's new misses and the product-detail noise.
2. Decide any configuration change without fitting a number.
3. Settle the schema-failure policy: DeepSeek has no strict schema; 0 of 507 nonconforming so far, but the runner stops on one.
4. Validate once on the 30 test articles, stating that earlier prompt iterations saw them.
5. Adopt into PRD §12.

Nothing is committed.

## 15. Council reflection: the next breakthrough angle (2026-11-07)

Alex: "好的你来council 来深度解析，看我们跑的log 学习反思我们下一步的突破angle".

**Method:**
- A fresh Codex session (`01a1b867…`) read the whole record cold, independently.
- Claude wrote its own reflection before reading Codex's (`council/reflection-1-claude.md`).
- One challenge round followed (`reflection-2-*`).

**Agreed lessons:**
- **Structural levers moved quality; sentence wording and placement did not:**
  - production's signed evidence rules, with the closing check after the item;
  - the unfiled outlet;
  - required closest-thesis fields;
  - reasoning effort;
  - the model.
- **Extra review calls and local patches failed.**
- **Weak conclusions:**
  - one draw: Flash d1 205 against d2 197 helpful; the draws share 188 hits, union 214;
  - library judgments without article text;
  - match counts are not semantic verdicts;
  - the dev articles are heavily exposed.

**New measurements on stored data:**
- the top three theses hold about half of all links in every forward run (the revenue-growth thesis holds 87 in Luna's two weeks);
- 4–7 theses are still opened after article 60.

**Agreed ranking of remaining problems by product impact:**
1. The chain past Step 1 does not exist: no dedup, no save, no judgment, while evidence piles into a few theses.
2. Meaning and source fidelity: on par with production in the 40 + 40 audit, but dangerous downstream (it can cause wrong merges).
   Tracked as a defect class.
3. Long-term library usability: catch-all theses, no closing, late openings.
4. Source input: cleaner losses and contamination.
5. Residual noise, recall variance and run stability.

**Agreed next breakthrough: validate Step 2 (retrieval, then comparison) on stored data.** This is not called "end to end"; Step 4
does not exist. Codex's corrections are folded in:
1. **Ground truth from the source articles across the selected range:**
   - real repeats (one statement in several outlets), numeric revisions and different parties' forecasts;
   - items with no prior;
   - cases where a summary's meaning drifted.

   Not only from items Step 1 found.
2. **Replay in the forward run's order.** Each new item searches only the entity's evidence saved before it, with the order within
   an article fixed. A repeat keeps its new source and adds its thesis link (Alex's decision).
3. **Measure search first** (true repeats and revisions in the top 10), **then comparison**: wrong merges, missed merges, a revision
   taken for a repeat, and different parties merged.
4. **New code.** The existing `search.py` indexes theses, not evidence, and the existing Jev prompt assumes the same thesis.
   Multi-candidate conflicts are an open design point for Alex.
5. **Count calls and cost before any send.**
6. **Read the deduplicated dossier** for three investment questions picked in advance: customer financing, competition, product
   roadmap.

**Falsifiers:**
- if search misses most true repeats, retrieval is the bottleneck;
- if search finds them and comparison errs, Jev is the bottleneck;
- if true repeats are a small share of the pile, dedup does not tame growth, and thesis structure and lifecycle come next.

**Other angles, kept for later, in order:**
1. Library stability: the same stored article against an empty, an early and a late library.
2. Source roles in the payload: body, byline, AI summary, recommended articles.
3. Entity profile and scale context for the thesis-size decision; seeding is Alex's call after D370.
4. Two-draw union for recall, only once Step 2 exists.

**Not to repeat:** sentence-level Step 1 wording edits.

## 16. Confirmation and Step 1 close-out (2026-11-08)

**Alex:** "确认 K6b + DeepSeek，把剩下的收尾做完 step 1 and 2, run council loop and we stop here first without going further". The
Step 1 configuration is K6b (`k6b-system.txt`, `k6b-closing.txt`, `k6b-schema.json`) on `deepseek-flash`, high effort, JSON mode
with the schema in the system text.

**Format-failure policy (Alex, 2026-11-08, chose the recommended option).** An answer that is not JSON, or not the schema, is sent once
more unchanged.
- If the retry also fails, the item is marked failed with both reasons, and the run continues.
- The run then ends `complete_with_failures`, with the failed items listed.
- Any other failure still stops the run.

Built in `clean-arch/step1/runner.py`, with the `trace.retry_reason` column. Tests: 3 new tests plus 1 updated, because the spec changed.
All 3 mutants were caught: no retry; the second failure stops the run; any failure retried.

**Test set, predeclared before the send.**
- `test-k6b-flash/`: the 30 golden-v5 test articles (gold `af2145cd…`), all runnable, 2026-09-01 to 2026-10-24.
- Ordered by publication day, as the dev run was, and run forward from an empty library.
- Inputs are byte-identical to `gold-k6b-flash/` (`SHA256SUMS`). Limits allow 60 calls, for retries.
- **Exposure:** earlier prompt iterations saw these articles, so this is a check of the final configuration, not a clean held-out
  estimate.
- **Proportional line**, the dev line applied proportionally, not separately confirmed:
  - helpful at least 81.2% of the gold's 46 helpful entries (190/234 on dev), that is at least 38;
  - at most 3 small theses and no fragments, from source-backed readers;
  - noise (not-kept spans kept) reported beside production's test draws where they exist.
- One draw.

**Amendment before any send (2026-11-08).** The first launch refused at selection, before any model call, on
`gnews:5ad994979828be9a769cd7d9`: the article is not tagged NVDA. Four of the 30 test articles are macro or theme feed items with no
NVDA ticker:
- Asia week ahead, no gold entries;
- OPEC quotas, 3 supporting entries;
- Hassett and Powell, no gold entries;
- Nigeria OPEC output, 1 supporting entry.

The clean flow is single-entity (PRD §3: code supplies the entity from the input), and the dev run passed the same selection check, so
these four are out of its scope and are excluded by the same rule. The runnable test set is therefore 26 articles with 42 helpful
entries. The proportional line becomes at least 81.2% of 42, that is at least 35. Limits are 52 calls.

**Test-set result** (`test-k6b-flash/`, one draw, scored by `score_gold_runs.py --test`; the scorer was re-checked on dev, 205/234 and
production's draws reproduced).
- 26 of 26 complete; 0 format failures, 0 retries; 207k input and 153k output tokens, $0.25 at the published rates.

| 26 test articles: 42 helpful, 9 core | K6b Flash | Production test draw (`test-control-d1`) |
|---|---|---|
| Helpful matters kept | **32** | 20 |
| Core | 8 | 8 |
| Items | 42 | 39 |
| Not-kept spans kept | **8** | 4 |

- Library: 10 theses, all 10 judged "bet" by three readers with source, using the dev prompt (`theses-answer-r*.json`). Small 0,
  fragments 0.
- **The proportional helpful line (at least 35) is missed by 3.** Noise is twice production's.

**The 10 misses, each read against the run's answer:**
- **7 were extracted but left unfiled** (no thesis link), so code dropped them:
  - Q2 revenue of $96.2bn with data centre up 117%, the only core miss, with 2 theses open;
  - the 50% free-cash-flow return plan, and the analysts' $441bn free-cash-flow forecast (that article filed 0 and left 6 unfiled, with
    2 theses open);
  - Dell XPS RTX Spark, twice (the article is dated Oct 9; the RTX Spark thesis opened Oct 10);
  - AI infrastructure spending above $1tn by 2029, and an author's valuation scenario.
- **3 were not extracted:** NVIDIA's denial of the RTX 5090 discontinuation; Orange testing AI-RAN; Dell, QCT and Supermicro Aerial
  configurations.

The request tells the model that a material statement no open thesis covers, and that is not itself a big matter, is returned unfiled
(`k6b-system.txt` lines 7–8 and 52–53; closing line 15). In a library that started empty over sparse articles, the model left even the
quarterly results unfiled and opened no thesis for NVIDIA's revenue and earnings trajectory. A thin library is a plausible contributor,
not a proven cause for all 7: the model's own account was not asked, because Alex said to stop at the close-out.

**Council** (`step2-validation-2026-11-07/council/group/f-*`):
- The test missed its line and the cause is not yet proven.
- Report the noise beside recall.
- Do not claim acceptance or production readiness.
- Record Alex's choice with the result and its limits.

**Status:**
- K6b on DeepSeek Flash is Alex's chosen configuration, recorded in PRD §12 with this result.
- The §12 prompt blocks are not replaced: that was the plan's last step, and it is held after the failed test line.
- Open defects:
  - evidence left unfiled under a thin library (7 of 10 test misses, 1 core);
  - noise of 8 against 4 on the test set, and 40 against 30–34 on dev.

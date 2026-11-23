# Task C report: the measuring method, audited (read-only, 2026-11-15) — Claude-family cold reader, saved verbatim

**Answer in one line:** both, but unevenly. The product has five or six real defects that hold whatever stick is used. The *stuckness* since 2026-11-10 is mostly the measuring: the gate that blocks the rebuild has never been cleared by any reference, and the end-to-end stick cannot tell two systems (or two runs of one system) apart.

**How to read this.** Every statement is first-hand from the cited file unless marked *(inference)* or *(my count)*. Paths are relative to `/Users/lchingen/hivemind`; absolute paths are at the end. Not read: `reflection-4/` (nothing), `reflection-2/` (nothing), item-level gold contents, `DECISION-PAGE-2026-11-15.md`, the design page's `.js` data (I read `docs/prd/00-system.md` and `clean-arch/PRD.md` §§1–3, 6–8 instead). Read last, as past attempts: `reflection-3/cold-codex-1.md` and `cold-codex-5.md` only.

## 1. One row per instrument

| # | Instrument | Measures, and where | Unit; size | Who judges | Cost per use | Uses; passes |
|---|---|---|---|---|---|---|
| 1 | Extraction key (`golden-v5`, standard page v5) | What the reading step keeps from one article; not where it files it (AGENTS §7.1 "does not measure… whether evidence was filed under the right question") | One matter in one article. Dev: 118 articles of 07-01..14, 237 keep-worthy, 72 optional, 801 not-kept; test: 30 articles, 46 *(my count)* | Code against a model-written key ("Model-authored", key's `about` field), then Claude reads traces (D244) | One draw: old system about $0.45; new first step about $2.5 and 2 h 20 (`e2e-comparison/SLICE-RESULT.md`) | Dozens of versions (D238–D274; c1–c22). Adopted: v74i (D274); c8 on 50 unseen articles, 132/139 kept, 1 of 10 wrongly opened (D386, D387; `CURRENT_STATE.md` l.13–21) |
| 2 | Question key + matching rule (`MATCHING-v2.md`, D430) | Whether the system opens the key's must-open questions in the key's shape | 7 graded questions × draw (28 must-open entries cover 7 of 23 questions, MATCHING-v2 §2) | Two model reader families, a third on disputes | $7–8 for three draws (MATCHING-v2 §4); full same-day run ledger $14.84 (D451) | 3 uses (D395; D443–445; D451–454). No pass line; "cannot rank them" (D483) |
| 3 | Judgement key (reader B) + `score_judgement.py` | At the window end 2026-07-14, does the chosen answer band overlap reader B's range | 23 questions, 20 with a view, 17–19 judged per draw | Code against one model reader's answers (D262) | Scoring $0; a draw about $0.8 (`acceptance-design.md`, Result) | 13 stored score files, the v116 acceptance, D392, then the three unseeded uses. Passes: D354 (15/17, 15/17, 16/17) and v116, 53 against 45 (D366); Alex then removed that mechanism and the preset questions (D370) |
| 4 | Answer-choice form (Stage A; D400's six lines) | Whether each written question and its answer choices are well formed, before any judging | One attempt (topic × 3): 132, 120, 21, 39 (`FIRST-GATE-MAP.md` §2) | Two model families, a third reader of each family, lines by `accounting.py` | Model $0.11–0.17 per 132 sends; reading about 35 min a reader (DESIGN l.1429) plus 2–6 third-reader sessions, outside every ledger (`CURRENT_STATE.md` l.262) | 7 readings (four on the 44 topics, July, two weeks). **0 passes** |
| 5 | Judge-support reading (Stage B; D428) | Is each daily answer supported by what the judge was shown | One judgement: 159 (baseline), 236 (run) | Two families, planted wrong answers, repeats | $0.42 for three draws; 0.3 h and 2.4 h of reading (`STAGE_B_RESULT.md`) | Baseline + one run. 0 passes: control line "unexercised", 4 of 8 needed |
| 6 | Filing measure (`docs/prd/10-filing-phase.md` §6) | Do facts the key uses reach the question that uses them | Fact × question; 54 + 15 articles × 3 sends × 2 arms | Code, with 4,000 random re-splits | Cents to about $1 | One registered test: failed (+7, p 0.26; §8 step 5) |
| 7 | Use readings A/B/C (D484) | Big matters covered; last answers supported; facts not delivered | 5–7 matters; 7 against 15 last answers per week | Two blind model families | Trial $0, about 25 min a family; fresh week $4.69 | Trial + one week: "not clear" (D489). Lines "proposed, not his" (`NEW-SYSTEM-FRAME.md` §1) |

## 2–3. Is each stick's own error known, and what does it really measure?

| # | Reference or a second draw put through it? | Spread with nothing changed | Can a good system fail? Can a bad one pass? | Measures the product's purpose, or one reference's choices? |
|---|---|---|---|---|
| 1 | Yes. Blind re-read: agrees with the key on 93–95% of controls, 70% of the 117 borderline entries (D250). An independent reader finds about nine in ten key items (standard page §8) | 214/211/212 of 234 (`CURRENT_STATE.md` l.23); 166/170/162 (D378) | Bad passes, recorded: one fallback sentence raised core items 64 → 68 by parking facts under one question (PRD 10 §2) | A step's form, soundly. Best-conditioned stick; its test set is spent (D386) |
| 2 | No | The same three first-step draws score 5, 3, 4 of 7 when a reader maps them to the key's wording (`unseeded/result.txt`) and 1, 2, 1 when the system's own wording must match (`e2e-comparison/RESULT.md`; D466 warns the readings differ). New 2, 1, 0 against old 1, 1, 1: "own spread… wider than the gap" (`COMPARISON-SIZING.md` §1). Third readers split by family on 17 of 17 points (`CENSUS-FULL-RESULT.md`) | Good fails: the Ohio question due 2027-07-01 against the key's 06-30, "its last judgement, Yes, would agree"; "by 2028: Yes" against the key's "by 2027: No" (same file). Bad passes: trivia and duplicates are not counted | **One reference's question shapes** |
| 3 | Partly. Two nulls printed (8/14, 5/10); reader A kept, differing on 3 of 23 answers and 12 of 20 direction labels (`ruler-v1.md` l.30) | 17/19, 17/18, 17/19; 15/17, 15/17, 16/17 | Good fails: reader A itself on q09, q12, q23. Bad passes: any system handed the 22 preset questions ("says nothing about whether the clean system opens them", D392). The key's range overlaps 1.9 of 5 bands on average; B marks 14 of 20 answers low confidence *(my counts)*; key "$9–10" agrees with the band "≥ $10" (`score-r9-frozen-v108-d1.txt`, q11) | Agreement with one model reader, on questions the judge was then **written to match**: "written to the frozen gold's own reasoning" (D263). One window, no held-out |
| 4 | **No sound control exists.** Planted faults are caught 11 of 11, but reader 1 failed 3 of 7 "sound" ladders and "my 'sound' answers are not reliably sound" (DESIGN l.1056, l.1179). The old system's 36 ladders hold every firm mark on only 19 and 25 (`stage_a/result/RESULT.md` l.59). Paid control waived (D400). No chance estimate for the zero-fault lines *(inference: none in DESIGN §8 or the four result pages)* | One family holds every firm mark on 47 of 111 ladders, the other on 84 (same file, l.55). Third readers: 22 against 6 "fails" of 42 (`result-4/RESULT.md` l.20); they differ on 41 of 48 points (`second-week/RESULT.md` §3). Line 5 reads "met: 40 and 31" or "missed: 34 and 25" on one reading | Good fails: marks on a field "the judge is never shown" (`FIRST-GATE-MAP.md` §4); a note saying "around 2027-02" against code's April 1 makes 23 open points (§5). Bad passes: unfair ranges "can still count as right" (DESIGN l.1301); the lines "passed two questions that sat on their top range all week" (LEAN-LOG §45) | **A step's internal form** |
| 5 | Yes. An unchanged judge crosses the figure line by chance 6–17% of the time, and Alex was told (`stage_b/RESULT.md` l.86–104; D428). "No control is known to be sound" | Third readers split 12 of 22, 9 with their own family | Control line can be unexercised whatever the judge does (D430's question) | Closest step-level stick to the purpose |
| 6 | Yes. The first rule "the control itself fails"; replaced by re-splits (PRD 10 §6) | Same requests drift between days, so same-day control only (§3) | — | Purpose (facts reaching answers), scored through key 3 |
| 7 | Partly. "Leads, not a calibration that holds"; readers share 7 of 12 matters; reading C "cannot be told from a reader that only says no" (`TRIAL-RESULT.md`) | One draw each; one family failed 2 of 4 confirmed-supported controls (`WEEK-RESULT.md`); detectable gap 22–38 points (D517) | A product rule (no questions on revenue and margin, D382) counted as 3 of 5 misses | **The purpose**, but too small to decide |

## 4. Conditions

| Measurements | News | Start | Draws |
|---|---|---|---|
| Keys 1–3 before D370; D392 | NVDA, 2026-07-01..14, also the tuning set ("the articles tuned c8", D392) | 22 hand-written preset questions | 3, same-day control |
| Unseeded comparisons (D395, D443, D451) | Same 14 days | Empty library | 3 |
| Stage A | 44 topics the step and the form were both tuned on (`FIRST-GATE-MAP.md` §1; the form carries D410–D420); July 40; weeks of 09-22 and 10-06 | Empty | 3 attempts a topic; one run a week |
| Use readings | July stored runs; week of 09-22 | Empty | 1 |

**The design says otherwise.** The product is a continuous stream against a standing library that each article reads (`docs/prd/00-system.md`, Purpose; D375, not built). The rebuild is to be evaluated "against a known initial library", with Alex reviewing traces "before deciding what quality is sufficient" (`clean-arch/PRD.md` §8). Since 2026-11-05 the status page has said "Alex requires a research library established from real material available before the test start… The prior empty-library diagnostic cannot represent this case" (`CURRENT_STATE.md` l.89). Preset questions were removed by Alex (D370). So **neither start state used is the product's**. All of it is one company, read at the window end only, with no due day reached (`CURRENT_STATE.md` defect 6).

## 5. The record's own warnings

| Warning | Done? |
|---|---|
| "Measure the stick before using it: control against a second control, the criterion's null estimated (a conjunction over many items fails by chance)" (AGENTS §7.1) | Sticks 5 and 6 yes; 1 partly; **4 no**; 2 no |
| "a bar the control fails against itself judges nothing" (AGENTS §7.3) | Stick 4's control was waived as "an exception" (D400). The lines were Claude's proposal ("通过线我提议"), ticked "(Recommended)" with no chance figure. Contrast D428 |
| "Nobody grades their own change with a ruler still being corrected" (AGENTS §7.1) | The Stage A form gained eight rulings between readings |
| "the upside of that step done perfectly is measured where the product is judged" (AGENTS §7.2) | Never for the answer-choice step: stopped at $0 proofs (D467, D468, D476) |
| "Model readers carry their family's threshold… his rulings are the ruler"; "Calibrate the readers before trusting a per-item count" (`council-loop/SKILL.md` l.160–164) | Rulings taken case by case; splits persist (41 of 48) |
| Test set "scored once per configuration, never tuned on" (D244) | Spent across five configurations (D386) |
| The start-state correction (`CURRENT_STATE.md` l.89) | Not carried into D466 or D469 (D559) |

## 6. Verdict, evidence both ways

**The measuring cannot tell:** tables 2–4. Reflection-3 dismissed "the pass rules are too strict" in one sentence ("agreed faults remain even on the favourable reading", `cold-codex-1.md`). It did not ask whether anything clears those lines; nothing on record does.

**Established about the product, whatever the stick:**
1. Given the facts, the judge reaches the reference answer; without them it does not: 9 of 9 against 9 of 9, same-day control (PRD 10 §2). Facts held and not delivered recur (LEAN-LOG §§26–28).
2. The same news gives different questions run to run: 18 July matters, the same judged question in every run that opened it on 3, 6 opened by one run of three (D559).
3. The answer-choice step answers or declines the same topic by chance (sound once, declined twice), and declines two-year topics 3 of 3 by Alex's own rule D397 (`second-week/RESULT.md` §5). Refusals are counted by code.
4. Ranges written with no reference figure are guesses that change between attempts ($5–10bn against $1–5bn; §7). The old system does the same: one identical request, three ladders, the favourable end flipped (DESIGN §2.2).
5. The judge names a band when nothing sizes the amount: 31 of 36 settled failures, and its own account agrees (LEAN-LOG §17). Both systems.
6. By code, one draw: 389 of 569 kept statements reach no judgement in the new system; 126 pile on one question in the old (`WEEK-RESULT.md`).

Reading the news is not the blocker (stick 1).

## 7. A sound measurement: a card deck Alex marks

*(A proposal; the reading-time and availability figures are inference.)*

- **Material, all stored:** July runs c1–c3 and p1–p3 (`poc/data/clean-e2e-full-2026-11-13`), the week of 09-22 for both systems, the week of 10-06, and `side-by-side/build_side_by_side.py`. Its current page is 15,446 words *(my count)*, too long.
- **Unit:** one card per matter per date, under about 150 words: the question as a user sees it, the answer choices, the current answer, its three strongest cited passages. A "no question" card where readers listed a matter the system lacks.
- **Marks:** about 40 cards, three ticks each: would I hold this question as worded; does the answer follow from what is shown; is something important missing or wrong.
- **Known error, built in:** six repeated cards (Alex's own consistency); pairs from two draws of the *same* system shown as "X against Y" (the noise floor); four planted wrong answers (sets exist from Stage B and the week). The two model families mark the same deck first, so their agreement with Alex becomes their measured error.
- **Accumulates:** the matter list only grows; each new version is re-rendered on it; Alex's marks are frozen as the reference, corrected by dated records.
- **Second key that grows by itself:** later stored news (items run to 10-27, LEAN-LOG §1) shows which way July's answers should have leaned. Availability per question not checked.
- **Cost:** $0 model spend; builder work; reader sessions (unpriced); one hour of Alex per round.
- **Cannot show:** whether 2027 answers come true; anything beyond NVDA and three windows; differences under roughly 20–30 points on 40 cards (D517's arithmetic applies); matters nobody listed; which step caused a bad card.

## 8. Alex's three questions

1. **The goal.** For each big matter, a question worth holding with an answer supported by the facts that can change it, kept current (PRD 00 Purpose; PRD 10 §1). The work drifted to two stand-ins: matching one key's seven question shapes, and zero form faults in answer choices. *Would change my mind:* Alex saying exact answer-choice form is itself the product, because answers freeze against their choices at the due day (PRD 00 principle 8 gives this some weight).
2. **Is it the measuring method?** For the last five days, largely yes: gate 1 has no control that clears it and no sized effect on the final answer, and the end-to-end stick cannot rank. Not only: §6's defects are real. *Would change my mind:* a human-written or old-system set that clears the four zero-fault lines under the same two-family reading.
3. **Why stuck, and the way out.** Each next step was chosen from the last failure of a stick with no known noise floor, under an empty start Alex had ruled out. Way out: his own marks on about 40 cards as the reference, with repeats and same-system pairs; start from a carried library (D559's probe is ready); treat the Stage A lines as diagnostics until a control clears them. *Would change my mind:* if cards from a carried library still fail his marks at similar rates, the problem is the product's question-forming, and the new stick only showed it faster.

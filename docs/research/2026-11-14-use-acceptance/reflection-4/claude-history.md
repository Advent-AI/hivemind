# Task B report: every past attempt, read end to end (independent, read-only) — Claude-family cold reader, saved from its hand-back

## 0. What was read

Read first-hand, whole: the brief; `docs/DECISIONS.md` index rows D229–D559 (every row) and sections 1–15; `docs/research/2026-11-01-e2e-loop/log.md` (all rows) and `review-2026-11-02.md` §§3–6; `docs/research/2026-11-04-filing-end-to-end/log.md` (all 41 rows); `docs/research/2026-11-14-use-acceptance/LEAN-LOG.md` §§0–5, 14–18, 44–51; `clean-arch/step4-2026-11-10/PROGRESS-2026-11-12.md`; `stage_b/STAGE_B_RESULT.md` (top); `clean-arch/e2e-comparison-2026-11-13/RESULT.md`.
Read first-hand, in part: `docs/DECISIONS-log.md` records D229–D249, D354, D355, D361, D362, D369–D379, D466, D483–D487, D544, D559; `docs/CURRENT_STATE.md` lines 1–200; `clean-arch/takeover-2026-11-07/LOG.md` §§0–2, 5–9, 11–16; `clean-arch/step1-unfiled-2026-11-08/LOG.md` §§0, 4–5, 8, 15–18, 25–26, 29, 35–38, 59–68, 70–80, 83–92; Step 2 log §§3–4, 7–9, 12–14; `docs/prd/10-filing-phase.md` §§0–2; `../tn-hivemind/docs/LESSONS.md` opening and "Convergence".
Not opened: anything else in `reflection-4/`; the folders `reflection-2/` and `reflection-3/`.

Short names: **E2E** = e2e-loop `log.md` (row); **FIL** = filing log (row); **TKO** = takeover log (§); **RL** = Step 1 round log (§); **S4** = Step 4 progress page; **CMP** = e2e-comparison `RESULT.md`; **LEAN** = lean log (§); **CS** = `CURRENT_STATE.md`. "Old system" = production; "new system" = the rebuild in `clean-arch/`. "Seeds" = 22 hand-written starting questions. "Judged result" = the final answers scored against the frozen judgement key (23 questions, one company, 14 days ending 2026-07-14). "(inference)" marks the reader's own conclusion.

## 1. Timeline of measured attempts since 2026-10-29 (condensed to its rows)

### 10-29 to 11-01 (old system, reading step)

| Date | Source | What changed | Result in its own numbers | Outcome |
|---|---|---|---|---|
| 10-29 | D229–D234 | Model: Haiku 5.5 against gpt-6-luna | core right every draw 43/45 vs 41/45; unrelated statements 286 vs 464; about twice the cost | Rejected (parked) |
| 10-29 | D232, D235 | Prompt: about a dozen one-sentence arms, on the pages that showed each failure | seven "work on their pages" | Not adopted as arms; three became rules (D236) |
| 10-29 | D237–D239 | Prompt: scrub, six hand-read rounds v24 → v29 | none by design | Adopted (v29) |
| 10-29..31 | D241–D244, D250 | Measuring method: one standard page, golden set v3 → v5 | all earlier numbers recomputed | Adopted; frozen 11-02 (D261) |
| 10-30 | D245 | Prompt v42 | noise kept 139.8 → 102.8 a draw; core 240.4 → 238.4 of 258 | Adopted |
| 10-30 | E2E part A | Prompt v43–v50, one fix each | "每修一处掉另一处" | Rejected |
| 10-30 | D246 | Prompt: one clause | unwanted questions 20 → 0 | Adopted (v51) |
| 10-30 | D247 | Schema: field definitions (v53) | field errors 18/96 → 11/94 | v53 adopted, others rejected |
| 10-30 | D248 | Rules (Alex): seven boundaries of "one question" | census of the sealed 3-month run: of 50 questions read, 12 duplicates, 10 should not have opened | Adopted as rules |
| 10-30/31 | D249 | A check at the end of the same request (v59–v65) | noise kept 109 → 59 on the v5 key; core flat | Method adopted |
| 10-31 | D251 | Architecture: reading step sees open questions | duplicate candidates −75% | Not adopted then |
| 10-31 | E2E row 0 | Measuring method: first whole-path funnel | filing threw away about 30 of 86 core matters | Adopted as the way to pick the layer |
| 10-31/11-01 | D253 | Start state: 10, then 22 seeds | core thrown away 30 → 21.3 → 19.3 | Kept; removed 11-05 (D370) |
| 11-01 | D254, D255 | Filing prompt versions | core reached 60.3 → 67.3, noise 23.4 → 31.4 | v4 kept |
| 11-01/02 | D257 | Code: identity rules, alias merge | article-opened questions 24.7 → 21.3 | Kept. Alex: "跑完这个不要再跑这些有的没的臂了，根本没帮助" |

### 11-02 to 11-08 (old system frozen; rebuild begins)

| Date | Source | What changed | Result | Outcome |
|---|---|---|---|---|
| 11-02 | D258–D266 | Code: part-of merge; wider "takes" line; narrower link; quote repair | $0 replays | All built |
| 11-02 | D260, D263 | Judge prompt v6, then v7 (five rules read from the key's own reasoning) | 6 of the 7 disagreeing questions enter the key's range | Built; frozen 11-03 |
| 11-02 | D261–D262 | Measuring method: the judgement key (two model readers agree on 20 of 23; reader B taken) | 13/19, 15/18, 12/17 on the old judge | Frozen |
| 11-02 | D264–D265 | Architecture: one decider (reading step files) | judged 17/19, 17/18, 17/19 → 15/18, 16/17, 17/18; noise reaching 89.2 → 56.9 | Adopted by Alex as "the version" |
| 11-02/03 | D268–D270 | Prompt audit fixes v75–v77; schema fields v78–v80 | v78 noise 21 → 154 | Rejected: "句子层面到头了" |
| 11-03 | D271–D274 | Prompt v74b → v74i | core 59 → 70, noise 89 → 81 | v74i frozen as production |
| 11-03 | D354 | Freeze check of the whole line | judged 15/17, 15/17, 16/17; two questions never fed | Frozen with five recorded defects |
| 11-04 | CS defect 7 | Judge: argument card | 12/17 against 15/17 | Rejected |
| 11-04 | D360; FIL 10–20 | Filing rules v74l (six edits; seven review rounds, one send) | "right question" 185 → 192 (p 0.26); supporting 205 → 166 | Rejected |
| 11-04 | D361; FIL 8, 21–22 | Diagnostic: facts handed straight to the frozen judge | custom chips 9/9 leave the lowest answer; with the key's passages: margin 3/3, capex 2/3, custom chips 1/3 | Showed the judge reasons once it has the facts |
| 11-05 | D363–D366; FIL 25–41 | New step: read the company's latest report once at the start | 53 against 45 of 57, three draws each, same hours | Adopted (D366), removed by Alex the same day (D370) |
| 11-05/06 | D378 | Architecture: reading split into two calls | helpful 156, 156, 159 vs 166, 170, 162; judged 44 vs 47 | Failed, sealed |
| 11-07/08 | TKO; D380 | New system prompt K1 → K6b; model DeepSeek Flash | helpful 205 and 197 of 234 (old system 162–171) | Adopted |
| 11-07/08 | D381 | New Step 2 | search 90% vs 82% | Frozen D427 |
| 11-08 | RL §§4–15 | Prompt: six "unfiled" arms | "the instrument does not discriminate" (two reader families count 15 vs 6 on the same answers) | None adopted |
| 11-08/09 | D382–D387 | Alex's rules + prompt c1 → c8; acceptance on 50 fresh articles | fresh: helpful 132/139; dev 214, 211, 212 of 234 | c8 adopted (D387) |

### 11-09 to 11-15 (new system; council decides from 11-13)

| Date | Source | What changed | Result | Outcome |
|---|---|---|---|---|
| 11-09 | D388–D391 | Prompt c9, c10a, c10b, c11; a separate focused call | "each round opened one wrong neighbouring case" | None adopted |
| 11-09 | D392 | Measurement: new Steps 1–3 with seeds supplied, old judge | judged 18, 18, 17 vs 17, 15, 16 | "Inconclusive" by its own rule |
| 11-09 | D393–D394 | Prompt c12, c13 (capex) | 0 of 3 | Rejected |
| 11-10 | D395 | Measurement: new system from empty | 5, 3, 4 against 6.33 seeded; 16 of 16 judged answers agree | Diagnostic |
| 11-10 | D396–D426 | New step writing answer choices; about ten rule changes; a "second look" | run 4 missed three lines by 1–3 answers of 131 | Not passed; frozen |
| 11-11/12 | D428–D430 | Frozen judge on the new system's own questions | unsupported 3.4% and 0.9% (lines met); control line unexercised | "Does not pass" |
| 11-12/13 | D433–D441 | Prompt c14, c15yc, c15c | 7 of 9, then 5 of 9; 17 vs 28 of 54 | Stopped |
| 11-13 | D442–D455 | Both systems from empty, same 14 days ($11.43) | agree with key: old 1/1/1, new 1/2/1; "every loss is at opening" | Diagnostic |
| 11-13 | D446–D479 | Typed-unit contract; prompt c16, c17, c18; schema c19 | c16 "moved its error"; c17 0 of 3; c18 4/6 vs 3/6; c19 1 of 21 | None adopted |
| 11-13 | D480–D481 | Old system prompt: price as a shared quantity | no candidate in 45 sends | Rejected |
| 11-14 | D483–D489 | Measuring method: "can an analyst use it"; one fresh week, both systems from empty | matters covered old 4 of 5, new 2; supported answers new 6/7, old 10/15 | "Not clear" |
| 11-14/15 | D490–D504 | Prompt c20; schema c21, c22; a figures table | c20 suppressed another question 0/3 vs 2/3; c22 missed by one figure of 185 | None adopted |
| 11-15 | D505–D543 | About thirty council rounds of $0 investigation; one six-call test | 3 confirmed undelivered facts; test inconclusive | Nothing built |
| 11-15 | D544–D558 | Council picks the new system; one more week through the answer-choice step ($3.67) | 9 declined; 6 of 12 topics right against 8 needed | "First gate not met" |
| 11-15 | D559 | Reflection on the start state | 53 of 60 topics are standing matters; 39 opened from a passing mention | Comparison prepared, not sent |

## 2. Classes of attempt (the reader's count)

| Class | Tried | Adopted | Reason the record gives for the failures |
|---|---|---|---|
| Wording inside the one reading call | about 55 old-system versions (D274 retired 54 variant files) and about 45 new-system candidates | old: 7 successive defaults; new: K5, K6b, c8. After c8 (11-09): 15 candidates, 0 adopted | one call does several jobs, so a fix moves a neighbour (D391; D493); wording moves a threshold, not discrimination; the model applies a rule when asked afterwards, not in the one pass (D249) |
| Answer shape (schema fields) | about 11 | 3 | "模型先自己定'这是证据'再填字段"; outcomes written in the same call fail the checks (D479) |
| Architecture or a new step | 9 | one decider; report-at-start (then removed); the rebuild in part | split cost more and scored lower (D378); extra calls each opened a wrong neighbour (D391) or damaged sound answers (D425) |
| Rules in code | about 11 | 8 | the three rejected ones judged meaning, not identity |
| Model or effort | 5 | 1 (Flash for the new reading step) | no gain or twice the cost; measured only on the reading step's counts |
| Judge | 4 | 2 (v6, v7) | cards lowered agreement |
| Start state | 4 | seeds and report adopted, then both removed (D370) | Alex's product decision, not a measured failure |
| Measuring method | about 20 instruments in 18 days | most used once | each built for the step in view |

## 3. What moved the result where the product is judged

1. **The judge rewritten to the key's reasoning (D260, D263).** About 13/18 → 17/18 a draw. Weak: draws on different days, and the rules were read off the same questions it is scored on.
2. **Questions present at the start.** New system: 6.33 of 7 gradable with seeds against 4.0 without; all questions 18, 18, 17 against 6, 5, 5. Different days; D466 calls it "an observed historical gap".
3. **Starting figures present (report at start).** 53 against 45 of 57, same hours, three draws; two questions from never judged to 3/3 (FIL 40). The firmest gain on record; removed the same day.
4. **Delivery in the new system (keep unlinked, link later).** 53 against 48, conditional on seeds; two questions traced to delivered facts in all six draws. Called inconclusive by its own rule.
5. **Facts handed to the judge directly (D361).** Two of three starved questions answered.
6. **Moved it down:** split reading (44 vs 47), argument card (12/17 vs 15/17).

About a hundred wording versions moved step counts; the judged result stayed at 15–17 of 17–19 from v92 to v108. (inference: every gain came from what the judge is given, none from wording.)

## 4. Circles, and requirements not followed

| Reached more than once | Dates and numbers |
|---|---|
| The start state | D208 (10-28) → seeds D253 (10-31) → report D363 (11-05) → both removed D370 (11-05) → "real library first" (CS, 11-05) → seeds as a fixture D392 (11-09) → empty D395 (11-10) → put to Alex D466 (11-13) → empty by default D469 → "return to a real library" D559 (11-15) |
| "A fact that bears on a question by one step of reasoning does not reach its judge" | E2E row 1 (11-01); `review-2026-11-02.md` §3; D355; PRD 10 §2 (11-04); E1 (11-06); capex (11-09); D456–D457; D506–D508, D529–D531 (11-15) |
| The company's main numbers | seeds are mostly figure questions → D371 "应该都是需要track 的" (11-05) → D382 figures are not questions (11-08) → D489 new system lacks them (11-14) → D490 test → D505 "should reach the judgements" (11-15) |
| One bet, one question; the year; the unsigned deal | D248, D258, D354, D388–D391, D433–D441, D463–D465, D471–D475, D555 |
| "Stop tuning sentences" | Alex 11-01/02; 11-03; 11-07; D391 (11-09); D466, D473, D477 (11-13); D493 (11-14) |
| "Measure where the product is judged" | Alex 10-31; `review-2026-11-02.md` §5; D361; D391; D483; D543 |
| "Which system carries forward" returned to Alex | D489, D512, D515, D543; reversed by D544 |

Not followed: the 11-05 start-state requirement (D559 says so itself); D375, "这个很重要" (11-05), not built by 11-15 (D521); D368's items, "这个你记住，我们要做" (11-05), not built, one probed and failed (D481); the test set "scored once per configuration" (D244) was scored for six successive new-system arms (D386); Alex's 10-31 architecture, reading with the open library, waited until he asked on 11-02 "你为什么架构上没有采纳".

## 5. What stayed constant

- **One company, one 14-day window, one scoring day** for every judged number.
- **A key written by a model reader**, 23 questions; its two readers agreed on 20 of 23. The seeded old system reached 53 of 57 (inference: the key is near its own noise in that condition). Without seeds only 7 questions are gradable, and only when the system re-creates the key's exact question and deadline.
- **The start: seeds or empty.** Never a library the system built from earlier news.
- **Readers are always models of two families.** Their third readers agreed on 21 of 70 points (S4), split 41 of 80 (RL §85); "agreement, not calibration".
- **Zero-fault lines and three-send probes.** The same stored request gave the adopted prompt 3 of 3 and then 0 of 3 (RL §90); D557 finds "no bounded way" to zero.
- **One pass decides** what to keep, what to ask, its scope and where each fact goes; the judge reads only what was linked at reading time.
- **The frozen old system.** The running default (v118) "has not completed end-to-end acceptance".
- **The loop:** a line written beforehand, missed, a new angle "from the last result's leftovers" (D466). The older project's lessons record the same in October: "You will never converge at this pace."

## 6. What the reader found no record of

1. A run that starts from a library the system itself built (prepared in D559, unsent); any window beyond 14 days on the current pipelines.
2. A human investment reader anchoring the model readers (D483 names one; none recorded).
3. Checking July's answers against what later happened; the corpus runs to 10-27.
4. Letting the judge fetch kept facts by search when it judges, instead of relying on links made at reading time (D361 shows the judge uses facts it is handed; the later-linking step judged 516, linked 2, LEAN §4).
5. A different model or effort at the judge or at filing, measured on the judged result.
6. A second company or window for the key.
7. Building D375 and D368 into the old system and measuring them.
8. Pass lines sized from a control-against-control spread for the answer-choice gate (D400 exempted it from a control).

## 7. The reader's answers to Alex's three questions

**What is the goal?** The record holds four at once: every judgement receives the facts that can change it (PRD 10 §1); the rebuild beats the old system on the key (D427); zero faults on answer choices (D400); an analyst can use it (D483). From his own words (inference): a short list of big questions kept over time, each judged on the facts that bear on it, in a library that already exists when news arrives. I would change this if he says a cold start on two weeks of news is itself the product.

**Is it a measuring problem?** Largely yes. Since 11-05 every test starts empty, so it scores whether two weeks of passing mentions re-create the key's exact questions; both systems get 1–2 of 7 while "no eligible judgement disagrees" (CMP). The lines are finer than the readers and the model's own spread. Two defects are real under every instrument: indirect facts not delivered, and unstable question forming. A warm-start run with the same losses, or a human reader confirming the zero-fault failures, would change my mind.

**Why stuck, and what breaks through?** The loop tunes sentences in the one reading call against step counts; the judged result moved only when the judge was given more (questions, starting figures, delivered facts). Measure in the real condition, anchor the readers once to a person, and move delivery out of the one-pass reading. I would drop this if the carried-library comparison shows no gain, or if supplying the missing facts on fresh weeks leaves answers unchanged (the one six-call test, D511, was inconclusive).

One inconsistency met: RL §60 gives the report-at-start run as "18, 18, 18"; FIL 40 and CS give 53 of 57.

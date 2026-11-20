# J2: the judge's next version, design for the council (2026-11-20, phase 1 steps 2–4)

## What the census and the traces show
- **The target.** 24 answers rejected by both readers (`census/CENSUS.md`). In about 16 of them the answer leaves the rung of its own
  reference on a weak step. Main classes:
  - O: overlapping amounts added (6);
  - S: a figure of another scope taken as the value (6);
  - E: an adjustment with no basis (5).
- **The order of the answer (found at $0).**
  - In all 48 stored answers of the probe set, the judge writes the fields in this order: `rung > reasons > cites > cites_views >
    pushes > changed > why_changed > theme_pushes > reference > implied_outcome`. It chooses the rung first, and states the reference and
    its own derivation last.
  - The cause is code. `judging.schema_for` inserts `reference` and `implied_outcome` after `rung` in `required`. Its comment reads
    "after rung: the reference and the implied outcome are written before the reasons". But it appends them to the end of `properties`,
    and the model writes the fields in `properties` order.
  - D260 requires both fields but names no output order (council A's correction). The order of work is the reader brief's: first the
    reference, then what the evidence implies, then the comparison.
  - It is a plausible mechanism for the arithmetic that lands just across a boundary (7 of 24), and not yet a proven one. J2a tests it
    alone.
- **The model's own account** (`poc/data/hybrid-2026-11-20/account/`, 24 continued conversations, $0.027). It names:
  - "State the implied figure … compare it with the rung boundaries, and move when it crosses one" (9);
  - "carries the guided growth forward" (6);
  - "rumour … in proportion to their specificity" (3);
  - "The rung is your forecast" (3);
  - "discounted by default" (1);
  - "Missing confirmation alone…" (1).

  Two answers concede the error: old-2 Q9 says "I inferred a Q4 figure without enough evidence"; new-2 Q31 says "moved … without new
  evidence".
- **Re-send noise.** The 48 stored requests are re-sent 3 times unchanged (arm v7, running). A target that flips on the re-send alone
  is sampler noise and is reported apart.

## Prompt audit (judging-v7 against the judgement ruler's reader brief and D260/D263)
| Failure class | Request sentence that produces it | The standard's line | Verdict |
|---|---|---|---|
| Rung chosen before the derivation (all classes) | The schema's field order: rung first, `reference` and `implied_outcome` last. Sentence 10 lists the rung first | Reader brief: "first establish what the market expected … then ask what the evidence implies, then compare the two". D260: "the answer states the reference and the implied outcome", written before the reasons | **Contradiction (code)** |
| O, overlapping amounts added | "derive the outcome … check it against the dependencies' conclusions (a part cannot exceed its whole …)", applied only to dependencies, not to the judge's own sums | Reader brief and D260 (3): "A part cannot exceed the whole it belongs to"; "the same claim … counts once" | **Missing at its owner:** the identity is stated for dependencies, not for the judge's own arithmetic |
| S, a figure of another scope as the value | "a figure that spans several periods or products gives this question only its share", which covers periods and products, not companies, measures, or balance against flow | Ruler v1 §2′, the stage 3/4 analyst standard B: "期间和定义要对上" (period and definition must match). Extraction standard: a proxy of one aggregate is evidence for the same question, never its value | **Narrower than the standard** |
| E, an adjustment with no basis | "move when it crosses one", together with "once other evidence has arrived it is never the reason to stay" | Reader brief: "a quantified revision, a customer's demand number, a supplier's constraint, a confirmed delay or cancellation shift it"; "Lean cautious, catch the increment" | **Missing:** the shift is meant to be quantified, and the prompt never says that an unquantified adjustment does not cross |
| W, talks taken as a likely completion (2) | "third_party_view and rumour move the forecast in proportion to their specificity" | Same line in the reader brief | **Misread**, 2 cases. Not targeted now |
| R, a rung's own condition misapplied (2) | — | The rung text | **Misread**, 2 cases. Not targeted now |

## The arms (revised after council A, `council-a-codex.md`; one lever each; every sentence sourced)
| Arm | Change | Source | Characters |
|---|---|---|---|
| v7 | None, re-sent as stored | Noise control | 4,924 |
| **J2a** | **Schema order only:** `properties` written as `reference, implied_outcome, reasons, rung`, then the rest unchanged. The system text is v7's, byte for byte, so the arm isolates order (council A: changing the wording too would not) | The reader brief's order of work; the code's own stated intent | 4,924 |
| **J2b** | J2a, plus a two-row check at the end of the system text, before the rung is chosen: (1) **overlap**: before adding, ask whether one amount contains all *or part* of the other, and count a shared part once (the examples are conditional on how the figures are reported); (2) **scope**: a figure of another quantity is an input to adjust or a proxy to name, never the value as it stands. Say how it was adjusted, or that it was used unadjusted as a proxy and why | (1) "a part cannot exceed its whole" (reader brief, D260); (2) analyst standard B, "期间和定义要对上", and the extraction standard's proxy line. The form follows AGENTS §6 (a check at the end) | 5,716. +792, reason: the closing-check form; nothing is cut, since each existing sentence carries a D260/D263 behaviour |

**Dropped after council A:**
- **The first draft's row (3)**, "an adjustment no item quantifies does not cross a boundary". It could block guided growth, the discount on
  untested targets and forecasts based on specific non-numeric evidence, which are D263 behaviours of the frozen gold. That is a return to
  D260's v5 stickiness.
- **The first draft's examples**, which mirrored the failing cases. The examples now come from other domains: a company's guidance and its
  reported quarter; a lender's loan book and its committed loans.

## The probe and the decision rule (written before any J2 send; revised after council A)
- **Cases.** 24 targets, plus 24 controls that both readers supported, of the same draw and type (seeded). All 48 stored requests
  rebuild byte for byte. The rebuild check compares content (sha over sorted JSON). Key order comes from production's own
  `build_request` and `schema_for`; the arms reorder only `properties`.
- **Sends.** Each arm × 48 cases × 3 repeats, at about $0.003 a call. Ledger `phase1.json`, $3.
- **Reading, complete** (council A):
  - every repeat of every case in the three arms, v7 re-send, J2a and J2b: 432 cards, none sampled out, plus 3 plants confirmed by a
    separate closed reader;
  - blind, shuffled, both families (`mark_cards`: Codex with memories off, Claude), debate rounds 1 and 2;
  - every card in the same form: the answer, then "Reference / Implied outcome / Reasons";
  - Claude reads every target that flips beside its material, and every control lost.
- **One decision rule for an arm against v7's re-send** (locked after council round 2, `council-b-codex.md`, before any J2 send). A
  case is **jointly supported** when both readers' final marks are `supported`; a split counts as not supported.
  - **(a) Targets:**
    - the arm is jointly supported in at least 2 of 3 repeats on **at least 12 of 24** targets (a floor);
    - paired by distinct question: (targets where the arm holds 2 of 3 and v7's re-send does not) minus (the reverse) is **at least 8**.
  - **(b) Controls:** a control is lost when it is not jointly supported in at least 2 of 3 repeats, a split included. The arm loses no
    more controls than v7's re-send.
  - **(c) The frozen judgement gold** (gold-v1, `636c056d…`, the scorer's own rule, 51 requests of the r9-frozen-v108 draws, 3
    repeats):
    - the arm's mean agreement over its repeats is no lower than v7's re-send;
    - every question whose agreement differs between the arms is read with its reasons.
  - **(d) Production refusals** (`judging.check_answer` on every answer, against the request it answered) are counted per arm before
    scoring. An arm refused more often than v7 is diagnosed before it passes.
- **Archive key** (council round 2). `model.request_identity` sorts keys, so J2a's request has v7's archive key. A J2 run on a populated
  archive would silently replay v7's answers.
  - The probe calls the transport with no archive.
  - The production-path check uses empty, separate archives per arm, and verifies the raw answer's field order.
  - The build must give J2 a distinct request identity, for example its schema name.
- **Falsifiers.**
  - J2a moves no more targets than v7's re-send: order is not the mechanism.
  - J2b fixes targets but fails (b) or (c): the check over-corrects. It stops there.
- **Before the end-to-end slice: a production-path check** (council A).
  - J2 and v7 run on identical inputs through `judging.round_of_judgements`, on a copy of one old store, over two consecutive days
    with updates.
  - It runs on the probe's questions and their dependants. J2 is patched into the harness; no package code changes.
  - It checks: refusals by `check_answer`; the next day's request (the previous conclusion, the evidence shown from the citations);
    dependants' consistency.
- **The slice compares v7 and J2 on the same inputs.**
  - Its arms are old reading with v7, old reading with J2, and c8 reading with J2.
  - The first plan ran J2 in both arms; that is corrected in `PLAN.md`.

## What this cannot show
- **Opening, and the 17 matters never opened.** Phase 2.
- **Effects across days.** A changed rung feeds the next day's previous conclusion. The end-to-end slice (plan step 7) shows those.
- **A release verdict.** These cases are dev: they motivated the design. Acceptance is on a fresh window.

## Out of scope for the council
Extraction, opening, Steps 2–3, the frozen ruler's files, cost work.

## Council rounds (Codex thread `01a1f7a7-e78a-7721-90a6-673bc85b6af6`, read-only, memories off)
| Round | Verdict | What it found | What it taught |
|---|---|---|---|
| A (`council-a-codex.md`) | DISAGREE | J2a changed the order and the wording together; J2b's row 3 could bring back v5's stickiness, and its examples mirrored the failures; reading was not complete; the slice ran J2 in both arms | One lever per arm, literally. A blocking rule against "unquantified" moves conflicts with D263 behaviours of the frozen gold |
| B (`council-b-codex.md`) | DISAGREE | The deck sampled same-rung answers. **J2a and v7 share an archive key** (`request_identity` sorts keys), so a populated archive replays v7. The loan-book example assumed one reporting convention. The rule was not paired | A change of key order alone is invisible to the archive's identity. Lock a paired rule by distinct question before any send |
| C (`council-c-codex.md`) | DISAGREE | The refusal check read the stored final judgement as the previous one, giving false "moved but changed is false" flags. Coverage was not enforced | A check must run on the state before the answer it checks. Positive and negative controls: stored answers 0/48 refused, a cite mutant 48/48 |
| D (`council-d-codex.md`) | DISAGREE | Invalid-rung answers fell out of the count. The replay preloaded production's whole day, which masked the theme queue | Start from production's own queue: 13 and 18 at the start, and the round adds 23 and 18, the same as old |
| E (`council-e-codex.md`) | **CONSENSUS** | — | Send J2a and J2b (probe and gold, 3 repeats), score coverage and refusals, read the complete deck, then the production-path check under v7 and the passing arm |

**Measured before the J2 sends ($0.60 spent):**
- **v7 re-send, 48 cases × 3.**
  - Targets: 21/24 reproduce the stored rung in all repeats; Q31 1→2 (3/3), old-2 Q16 1→3 (1/3), old-2 Q9 2→3 (3/3).
  - Controls: 0/24 change. Refused: 0/144.
- **v7 on the frozen gold, 51 × 3.** Agreement 45, 46 and 44 raw, 45, 46 and 42 strict (refused counted as not agreeing). Refused 3/153.
  The stored scores are 15+15+16 = 46.
- **Production-path replay, $0.** 72/72 requests are byte-identical to old's over 09-17 and 09-18, starting from production's queue,
  with the same judged set.

## Result 1: the final-request probe (2026-11-20, $1.21 spent of $3)
| Arm | Targets moved off the stored rung in at least 2 of 3 repeats | Controls moved | Refused by the production check (of 144) |
|---|---|---|---|
| v7 re-send | 2 (Q31 1→2, old-2 Q9 2→3) | 0 | 0 |
| J2a, order only | 2 (the same two) | 0 | 0 |
| J2b, order plus check | 3 (the same two, plus old-2 Q16 1→3) | 0 | 0 |

- **The registered falsifier fired at the rung level:** J2a moves no more targets than v7's re-send. J2b adds one.
- **The derivations, read by Claude for 4 cases** (old-2 Q29, old-3 Q33, old-3 Q3, old-2 Q6), are unchanged under J2b:
  - it still adds $25B and $18B;
  - it still stacks the uplift;
  - it still scales NVIDIA's $1.3T, now naming it a proxy.
- **On M08 the material is ambiguous.** The items say "$25 billion of equity investment commitments as of July 26" and "$18 billion
  committed … for the remainder of FY2027", with no stated relation. The readers' "likely overlaps" is an analyst's inference.
- **The probe was confounded, and this was found before the slice, not at the end.**
  - Every final request carries "[Previous conclusion, for comparison only] rung N; reasons: …", which is the rejected answer with its
    whole derivation.
  - The rejected rung had been held for a median of about 10 judgements: 1 to 46, and Q4 for 42.
  - So the probe measures whether the judge overturns its own carried conclusion, not whether it would have chosen it.
  - **The planned slice has the same flaw:** it starts from the 09-06 copy, with every earlier wrong rung carried in.
- **The 432-card reading is deferred** (to be agreed). With the rungs unchanged, rule (a)'s floor of 12 needs the readers to support at
  least 9 answers at a rung they rejected, on unchanged derivations. The reading cannot change the decision.

## The fork probe (written before any send)
- **Cases.** Per target, the stored judgement at which the rejected rung was first chosen and then held to the end. 6 are a question's
  first judgement, with no previous conclusion. 18 are moves from another rung, where the previous conclusion is the rung before the
  error. All 24 fork requests rebuild byte for byte.
- **Arms.** v7, J2a and J2b, 3 repeats each: 216 calls, about $0.45.
- **Metric (code).** A target "repeats the rejected rung" when its fork answer gives that rung in at least 2 of 3 repeats. Production
  refusals are counted.
- **Rule.**
  - **If v7 at the fork repeats the rejected rung on 12 or more of 24**, the errors are the judge's, not a sample carried forward. An
    arm passes the screen when it repeats on at least 8 fewer targets than v7, with no more refusals. Its fork answers and v7's are then
    read blind by both families (216 cards plus plants) to confirm that the new rungs are supported.
  - **If v7 at the fork repeats on 11 or fewer**, the errors are mostly one unlucky sample that the carried previous conclusion keeps.
    The lever is then the anchor (how the previous conclusion is shown), not a reasoning check. J2a and J2b stop, and the anchor is
    designed next.
  - **If neither arm passes the screen while v7 repeats on 12 or more**, J2's levers do not fix these errors even without the anchor.
    The J2 line stops and goes to Alex with this census.

## Council F (`council-f-codex.md`, DISAGREE) and what follows
- **The fork probe is dropped.** Its evidence differs from the final request's, and an error can predate the first use of the rejected
  rung: old-2 Q29's earlier answer already adds $25B and $18B. The fork cannot isolate the anchor.
- **The 432-card reading runs** before either arm is called passed or failed. Reasoning can be repaired at an unchanged rung (rule
  (a)), and support can be lost at an unchanged rung (rule (b)). The deck was built on 2026-11-20: 432 answers plus 3 confirmed
  plants, 0 invalid rungs.
- **The anchor test** (written before its results).
  - **Requests.** The same 48 final requests, sent without the previous conclusion (`without_previous`). Its "[Previous conclusion,
    for comparison only] …" block goes, and so does the "[Not shown: N more pieces … the previous conclusion carries them]" line.
  - **Arms.** v7-noprev and J2b-noprev, 3 repeats each (288 calls). J2a is left out: it equalled v7 on rungs.
  - **Flag.** 34 of 48 requests had hidden pieces that the previous conclusion carried; without it they lose that information. Results
    are reported apart for those 34 and for the 14 clean requests.
  - **Metric (code).** Targets moved off the rejected rung in at least 2 of 3 repeats; controls moved off their supported rung in at
    least 2 of 3. Each is compared with the same arm sent with the previous conclusion.
  - **Reading.**
    - If v7-noprev moves at least 8 more targets off the rejected rung than v7 does, and no more than 2 controls, the carried conclusion
      holds the errors in place. The lever is then the anchor.
    - If v7-noprev is within 3 targets of v7, the anchor is not what holds them: the errors are the judge's on this evidence.
    - J2b-noprev against v7-noprev is J2b's effect without the anchor.
    - Moved answers are read blind before any claim of improvement.
- **The end-to-end test is redefined** (council F agrees). It is a judge-only replay of the whole window from 07-01, with old's links,
  sources and relations fixed. Each arm builds its own conclusions, citations, theme effects and queue.
  - It runs on the prodpath machinery, extended from two days to the whole window.
  - The cost is about $2 per draw and arm, from archived tokens.
  - It replaces the slice from the 09-06 copy, which carried every earlier wrong rung.

## Result 2: the frozen judgement gold, rule (c) (51 requests × 3, scored by the frozen scorer's rule)
| Arm | Agreement per repeat (of 51) | Mean | Strict (refused counted as not agreeing) | Refused (of 153) | Rule (c): mean no lower than v7's |
|---|---|---|---|---|---|
| v7 re-send | 45, 46, 44 | 45.0 | 45, 46, 42 (44.3) | 3 | — |
| J2a | 44, 44, 45 | 44.3 | 43, 44, 45 (44.0) | 1 | **missed** |
| J2b | 44, 45, 45 | 44.7 | 44, 44, 44 (44.0) | 2 | **missed** |

- **The questions that differ, read with their reasons.**
  - Five are single-repeat flips on boundary questions: d1-q17 and d3-q17 (China share), d2-q08 (H200 authorization), d2-q22 and
    d3-q22 (FY2028 revenue).
  - **One is a consistent J2b regression: d3-q18**, Kyber NVL144 shipping by the end of 2027. The gold says No (the reported slip to
    2028). v7 says No in 2 of 3 repeats; J2b says Yes in 3 of 3. J2b's reasons treat the slip report as "one underlying source", weigh
    NVIDIA's denial, and name the NVL576 statement "a proxy". The scope row was read as a reason to discount specific third-party
    evidence. That is the direction council A warned of.
- **Both arms miss (c) as written.** The gaps are within one question of 51, inside v7's own repeat range of 44–46. The miss stands as
  scored.

## The whole-window production path (validated at $0)
- `window old-2 replay`: a copy holding nothing before 07-01. Each day is fed old's links, evidence, sources, relations, opened
  questions, closures and successions. The judge's own round runs from production's own queue.
- Result over 82 days: the same judged set on 82 of 82 days, the same evidence in 1,616 of 1,616 requests, and 1,612 of 1,616 requests
  byte-identical.
- The 4 differences are retries. In old's run, a refused first answer was re-asked with "The code returned the previous answer
  because …". The replay answers the first request with old's accepted retry answer, so no retry note is sent.
- The machinery for the end-to-end judge test is ready.
- **Cost correction.** The whole window is about 1,616 judge calls per draw, at about $0.002 each: **about $3.3 per draw and arm**, not
  $2. The $2.04 figure was the 14-day window for two draws.

## Result 3: the anchor test, v7 with and without the previous conclusion (the same 48 final requests, 3 repeats each)
| Group | Role | n | Moved in at least 2 of 3: v7 | Moved: v7-noprev |
|---|---|---|---|---|
| Clean (no hidden pieces) | targets | 8 | 1 | 3 |
| Clean | controls | 6 | 0 | 1 |
| Hidden pieces carried by the previous conclusion | targets | 16 | 1 | 11 |
| Hidden pieces | controls | 18 | 0 | 1 |
| **All** | **targets** | **24** | **2** | **14** |
| **All** | **controls** | **24** | **0** | **2** |

- **The registered reading fires:** 12 more targets moved (at least 8 needed), and 2 controls (at most 2 allowed). The carried
  conclusion holds the errors in place, so the lever is the anchor, not a reasoning check.
- **The direction of the moves (Claude's code read against both readers' named rung):**
  - 2027 capex: 4→3 on all three draws' questions (the readers named rung 3);
  - equity commitments (M08): 3→2 and 3→1 (readers: rungs 1–2);
  - FY2027 revenue: 1→2 (readers: rung 2);
  - total CPU: 1→2;
  - FY2028 gross margin: 3→2;
  - Vera FY2028: 3→2;
  - states' moratoriums: 2→1 (readers: zero states).

  These are a code reading only. The registered blind reading of the moved answers is owed before any claim.
- **The controls that moved:** C-new-3-Q33 4→5 (3/3), and C-old-2-Q15 5→{2,4,5}. To be read.
- **The confound, measured.** In the hidden-piece requests the previous conclusion carries many pieces: 13 to 82 per question, and
  2,264 for FY2027 revenue. Every item the rejected answer cited is in the shown set, so the moved answers had the evidence the
  error was built from. The previous derivation and the hidden pieces are removed together, though, so their effects are not
  separated. Only 8 clean targets exist, with +2 moves.
- **This bears on D198** (Alex, 2026-10-27: a judgement reads the evidence in view; "the previous conclusion carries" the rest). The
  carrier is also what keeps a wrong derivation alive for a median of 8.5 judgements.

## Council G (`council-g-codex.md`): J2a and J2b retired; the separating test (rule written before any send)
- **J2a and J2b are retired as candidates.**
  - Rule (c) missed for both; J2b regressed d3-q18.
  - The falsifier fired for J2a.
  - Without the previous conclusion, J2b moves 16/24 targets against v7's 14/24, with 2/24 controls each. Its check adds about 2 on
    top of removing the anchor.
  - The 432-card reading finishes for the record.
- **The separating test (council G's (a)).**
  - **Cases:** the 21 cases with 1 to 100 hidden pieces: 13 targets and 8 controls.
  - **Requests:** each request is rebuilt by the judge's own `build_prompt` on the store as of the stored judgement. Later
    judgements, links, sources, relations, switches and successions are shadowed by temporary tables. **48 of 48 stored requests
    rebuild byte for byte**, then every piece in force is shown (954 pieces restored), with no hidden line.
  - **Arms**, v7, 3 repeats each:
    - **fullprev**: full evidence with the previous conclusion;
    - **fullnoprev**: full evidence without it.
  - **Comparisons:**
    - fullnoprev against fullprev is the anchor's effect on complete evidence, the separation itself;
    - fullprev against v7 (clipped, with the previous conclusion) is the effect of restoring evidence under the anchor;
    - fullnoprev against v7-noprev (clipped) is the effect of restoring evidence without the anchor.
  - **Screen, before any claim:** fullnoprev against fullprev shows **at least 5 net target repairs** that are jointly supported by
    both blind readers in at least 2 of 3 repeats. It loses no control and adds no refusals.
  - **Reading:** a blind deck of every repeat of every moved case and control, plus a matched unmoved sample chosen before reading. It
    is shuffled with the stored answers and v7 re-sends, each card showing what its answer actually received.
  - **Budget:** about $0.4 on a new $2 ledger, `phase1b.json`. Phase 1's $3 ledger is nearly spent. The total stays inside D439's
    $40, with about $5 across the merge test and phase 1.
- **For Alex once the confound is separated (D198 is his):**
  1. keep what the previous conclusion carries and change only how it is presented;
  2. replace the carried derivation with a summary of the omitted evidence;
  3. show the full evidence.
  Option 1 stays within D198; options 2 and 3 change it.

## Result 4: the frozen judgement gold without the previous conclusion (v7-noprev, 51 × 3)
- **Agreement 43, 45, 45 (mean 44.3) against v7's 45.0.** Strict 42, 45, 44. Refused 2 of 153.
- **Questions that differ:**
  - **Regressions:** d3-q17, China share (v7 3/3 agree; noprev 0/3, rung 4→5); d1-q17 (1→0); d1-q09 and d3-q09 (3→2, one repeat
    each).
  - **Repairs:** d2-q22, FY2028 revenue (1→3); d2-q08, H200 authorization (2→3); d3-q18, Kyber (2→3).
- **Reading.** At the gold's cutoff (07-14) the previous conclusions are young. Removing them is not a pure gain there: the China-share
  question loses the consistency the previous conclusion held with the H200 theme. Any design that changes the previous conclusion
  must hold this gold question.

## Result 5: the separating test (council G's (a)), 13 targets and 8 controls with 1–100 hidden pieces, 3 repeats ($0.28)
| Condition | Targets moved off the rejected rung (at least 2 of 3) | Controls moved |
|---|---|---|
| Clipped evidence, with the previous conclusion (v7 re-send) | 0 / 13 | 0 / 8 |
| Clipped, without (v7-noprev) | 9 / 13 | 1 / 8 |
| **Full evidence, with the previous conclusion (fullprev)** | **0 / 13** | 0 / 8 |
| **Full evidence, without (fullnoprev)** | **8 / 13** | **0 / 8** |

- **Restoring the hidden evidence moves nothing while the previous conclusion is shown.** Removing the previous conclusion moves 8 of
  13 on complete evidence, with no control moving. The carried conclusion, not the missing evidence, holds the rejected rungs.
- **The hidden pieces matter little to the moves.** Clipped without the previous conclusion moves 9 targets, full moves 8. The one
  control that moved when clipped (C-old-2-Q15) is stable with full evidence: that move was evidence loss.
- **Directions (code, against the rung both readers named):**
  - equity commitments: old-1 Q28 3→1/2, old-2 Q29 3→2, old-3 Q33 3→2;
  - 2027 capex: old-1 Q7 and old-3 Q7, 4→3;
  - total CPU: old-2 Q16 1→3, old-3 Q14 1→2;
  - FY2028 gross margin: old-3 Q37 3→2.

  old-2 Q6 holds rung 4 on full evidence. The blind reading of all 126 answers is the registered screen (`fullscore`) and is running.
- Each card is built by the comparison's own card builder from the request the answer actually received. Refusals are recomputed
  against that request (the full deck's key refusals used the clipped request and are not used).

## Result 6: the 432-card blind reading of the final-request probe, scored by the locked rule (`probescore`)
| Arm | Targets jointly supported in at least 2 of 3 (of 24) | Paired net against v7 | Controls lost (of 24) | Refused | Rule (a)(b)(d) |
|---|---|---|---|---|---|
| v7 re-send | 1 | — | 3 (new-2 Q14, new-3 Q33, old-2 Q15) | 0 | — |
| J2a | 2 | +1 (new-3 Q26) | 2 | 0 | **does not pass** |
| J2b | 4 | +3 (new-2 Q4, new-3 Q26, old-2 Q16) | 1 | 0 | **does not pass** |

- **Plants:** 3 of 3 unsupported by both readers.
- **v7's own re-send loses 3 controls.** A same-rung re-answer is not always re-supported, so the readers' own noise is about 3 in 24
  controls.
- **J2a and J2b are retired by the rule as written** ((a): a floor of 12 and a net of 8). This agrees with D682.

## Result 7: the separating test's blind reading, scored by council G's screen (`fullscore`)
| | Full evidence, with the previous conclusion | Full evidence, without it |
|---|---|---|
| Targets jointly supported in at least 2 of 3 (of 13) | 0 | **4**: old-1 Q7 and old-3 Q7 (2027 capex), old-2 Q16 (total CPU), old-3 Q37 (FY2028 gross margin) |
| Controls jointly supported (of 8) | 8 | 8 |
| Refused (recomputed against the request actually sent) | 0 | 0 |

- **Screen: net repairs 4 against the 5 required, so the screen does not pass, by one.** No control lost, no refusals added. Plants 3/3
  unsupported.
- **Why the moved M08 answers are not confirmed.** old-1 Q28, old-2 Q29 and old-3 Q33 moved from rung 3 to rung 2. Both readers say
  rung 1: "$18B runs off by fiscal year-end, leaving ~$7B plus partly-funded new deals". The move is in the readers' direction, not far
  enough. old-3 Q14 is 1 of 3. old-2 Q6 stays at rung 4.
- **The mechanism is confirmed by code:**
  - with the previous conclusion, 0 of 13 move even on complete evidence;
  - without it, 8 of 13 move, toward the readers' rung, with 0 of 8 controls moving.
- **The fix, removing it, is not accepted.** The screen missed by one, and the frozen gold without it is 44.3 against v7's 45.0, with
  d3-q17 regressed.

## The fresh test (D684), written before any reading of the fresh marks
**Alex, 2026-11-20:** "那你自己持续迭代" (the reply to the request for approval of council H's test). Harness: `fresh_test.py`.

**The pool ($0, done).**
- Each question's latest judgement on or before **2026-09-06** (the day before the dev window), in the 5 draws.
- Excluded, before any reading:
  - the 73 question-and-draw pairs whose answers the design read (the 24 targets, their 24 controls, the 49 census answers);
  - a question whose last judgement is that same one (its answer was read at 09-20): 8;
  - no answer by the cut: 13; a first judgement (no previous conclusion): 2; a retry: 1.
- **116 answers, all rebuilt byte for byte** under the frozen judge. 114 of them hold the previous rung.

**The census reading.** The comparison's own card builder and readers (Codex and Claude, closed sessions, rounds 0–2), with 3
plants confirmed by a separate closed reader. Two changes, both for the date only:
- the card's library list holds the questions opened by 09-06;
- the readers' brief says "as it stood on 6 September 2026".

**The selection rule.**
- **Targets:** both readers rate the question worth tracking, and both reject the answer (unsupported or insufficient, a split between
  the two included). All of them are used; n is their number.
- **Controls:** ceil(8n/13) answers that both readers support on a worth-tracking question. Each is matched to a target by draw and
  type, then by type alone, chosen with seed 20261120, none twice.
- **If n < 8:** the pool is widened by the same rule at 2026-08-23, for questions with no target at 09-06, before any send.

**The arms** (`fresh_test.py`, `arm_parts`).
- **v7:** the frozen judge, re-sent the same day. It is the control.
- **H1 (council H):** the heading `[Previous conclusion, for comparison only]` becomes `[Previous conclusion: earlier assessment and
  carried evidence. Derive today's forecast afresh.]`. The concept's name stays, so the system text's three uses of "the previous
  conclusion" still point at the block. The rung and the reasons are unchanged, which is what D198 carries.
- **H2 (proposed to council I):** H1, plus one system sentence restated in its source's words.
  - The sentence: "Do not add to or subtract from the previous score."
  - Its source: PRD 06, line 19: "rather than adjusting its previous score".
  - The restatement: "Derive the rung from this evidence rather than adjusting the previous score."
  - Why: one of the 24 accounts the model gave of its own answers (`account/T-new-2-Q31.json`) reads that sentence as "do not move
    without new evidence". As the model reads it, the sentence is an instruction to anchor, which is the opposite of its source.
  - H2 against H1 isolates the sentence.

**The screen (each candidate arm against v7, paired, 3 repeats).**
- **Jointly supported:** both readers' final answer mark is `supported` in at least 2 of 3 repeats.
- **Net target repairs at least ceil(5n/13).**
- **No control lost.**
- **Refusals not above v7's.** They are recomputed against the request each answer actually received; an invalid rung counts as
  refused and not supported.
- **Frozen gold:** the mean per repeat at least v7's 45.0. d3-q17 must agree in 3 of 3, with its reasons read against both H200
  conclusions.
- **Readers:** every answer of every arm and repeat, plus 3 plants. Each card is built from the stored v7 text, so the heading the arms
  change is not on any card.
- **Falsifier (code, before reading):** if H1 moves fewer than 2 targets off the stored rung in at least 2 of 3 repeats, the heading
  does not loosen the anchor.

**Budget.** The `phase1b` ledger's remaining $1.72 of its $2 ceiling; no new ceiling is opened. At about $0.0022 a call (`phase1b`):
- each arm costs 3 × (n + controls) calls, about $0.17 for 25 cases;
- the gold costs 153 calls per candidate arm, about $0.35.

Three arms and two gold runs come to about $1.2. The total stays inside D439's $40.

### Council I (`council-i-codex.md`, DISAGREE) and the amendment, written before any fresh mark was opened
**Verified.** The pool held questions the design had read under another label or in another draw. Examples:
- old-1 Q8 is the same FY2027 data-center revenue question as the exposed old-2 Q9, word for word;
- the same holds for FY2027 gross margin, FY2028 gross margin, and two OpenAI chip-financing questions.

Claude's own reflection (`council-i-claude.md`) had called this mild. It is not: the census looked at these questions.

**Amended rule:**
- **Bets.** Each pooled question gets a bet, read by Claude from its text against the 73 questions the design read
  (`fresh-bets.json`). The file was written before any fresh mark was opened.
  - 52 answers sit on a bet the design read, and are excluded.
  - Questions that are the same bet across draws share one label. **Each bet gives at most one case**: from its answers in seeded
    order, the first rejected one becomes a target; otherwise the first supported one becomes a control candidate.
  - Bets the frozen matter list keeps apart stay apart: 2026 capex (M04) is not the exposed 2027 capex (M14). A bet adjacent to an
    exposed one is excluded: stand-alone CPU revenue next to total CPU revenue, and AI-buildout bond issuance next to the
    bond-issuance share.
- **Prerequisites enforced in code before any send:**
  - n ≥ 8 targets;
  - ceil(8n/13) controls;
  - all 3 census plants rejected by both readers.

  Otherwise there is no send, and the shortfall goes back to the council.
- **Scoring.**
  - A production refusal counts as not supported.
  - A plant the readers do not reject voids the reading.
  - Rung moves are reported as a description only. The falsifier on moves stays a description, not a gate.
- **H2 is not sent.** One account in 24 is too little, and "this evidence" could be read to leave out the dependencies and themes. It
  is parked with that reason. Claude agrees: the cheaper course.

## The fresh census and council J
**The fresh selection was refused by its own rule. No send was made.**
- 27 fresh bets, with 37 worth-tracking answers, gave **1 target** (F-new-3-Q3, H200). The prerequisite is 8.
- The 3 plants were rejected by both readers.
- At 09-06, 5 of 75 worth-tracking answers are rejected by both readers. 4 of the 5 are on numeric bets the design read: FY2027
  data-center revenue, FY2027 CPU revenue (twice), and the Poolside obligation. The fifth is the fresh H200 question.
- **On this corpus, the judge's errors sit in the big numeric bets, and the design has read all of them.** A fresh test of a judge
  change needs a fresh window.
- **Error of mine.** I first read 7% at 09-06 against 17% at 09-20 as "errors accumulate". Council J: the two pools are chosen
  differently (the 09-06 pool excludes what the design read at 09-20), so the comparison cannot show it. Withdrawn.

**Council J (`council-j-codex.md`, consensus): one small blinded diagnostic of H1 before anything wider.**
- **Targets:** T-old-3-Q3 (FY2027 revenue), T-old-3-Q37 (FY2028 gross margin) and T-old-1-Q7 (2027 capex). These are three bets where
  v7 kept the rejected rung in 3 of 3 re-sends and the arm without the previous conclusion moved in 3 of 3 (verified from
  `probe/v7` and `probe/v7-noprev`).
- **Controls:** two, seeded, from the controls that carry hidden evidence, were jointly supported in 3 of 3 v7 re-sends, and do not sit
  on a target's bet: C-old-1-Q29 and C-old-3-Q15.
- **Arms:** H1 against same-day v7, 3 repeats each, giving 30 answers. Every answer is blind-read with plants, against cards built from
  the v7 text.
- **Falsifier:**
  - **passes** with at least 2 net target repairs jointly supported in at least 2 of 3 repeats, no control lost, and no added refusals
    (a refusal counts as not supported);
  - **inconclusive** if same-day v7 leaves fewer than 2 targets to repair.
- **Not run:** the 48-case movement-only send, and the whole-window replay, until H1 shows a supported repair and clears the gold
  guard.
- **Dev only.** These cases motivated the design. A pass earns the end-to-end replay, not acceptance.
- **$0 checks:** all 5 requests are rebuilt byte for byte; H1 changes only the heading; the stored answers pass the production check
  under both arms.

## Closed for now (D689, council N)
Alex chose option 1: old stays production, and the hybrid's release line is paused. Council N (a fresh Codex thread, consensus with
Claude's separately written position) closed this line under D543. Every remaining lever changes D198, and every big numeric bet on
this corpus has been read by the design. Reopening conditions and a future test's proposed pass criteria are in `PLAN.md`, "Status
after D689". The phase 1 ledger reads $2.64 of $3, against the "$2.4" written in D683.

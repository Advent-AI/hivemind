# Claude × Codex review log: taking the split to production

Alex, 2026-11-05: "重跑之前你和codex subagent 需要一起我多轮的讨论和看trace，错误来达到一致下一步应该怎么改进。我需要能把这个推上线变成production，所以按照生产标准来做工作，深度的讨论直到你们彼此盲点都解决统一改动策略和计划".
Then: "你们每一轮的对谈和pk 要log起来，不要丢了context".

This log is appended after every round. Each round lists what was asked, what each side said (with the file holding the full text), what was
verified against the records, what changed, and what is still disputed. Codex runs read-only (`codex exec -s read-only`); its reports are leads
until checked (AGENTS §1). Earlier work on the first 100 items: `../2026-11-05-seven-day-request/split-v2-design.md`.

## Files

| What | Where |
|---|---|
| Per-item traces of three runs (article, A, record preparation, B, handover, matching reasons, questions written, judgements) | `traces/<run>/<seq>.json`, `_index.json`, `_ledger.json` (exporter `export_traces.py`) |
| Plans | `plan-v0.md` → `plan-v1.md` → `plan-v2.md` → `plan-v3.md` → `plan-v4.md` → `plan-v5.md`; agreed and consolidated: `plan-final.md` |
| Round prompts (exact text sent to Codex) | `r1/prompt-*.txt`, `r2/prompt-*.txt`, `r3/` to `r6/prompt-review.txt` |
| Codex reports (verbatim) | `r1/codex-*.out`, `r2/codex-*.out`, `r3/` to `r6/codex-review.out` |
| Claude's findings and responses | `r1/claude-findings.md`, `r2/claude-responses.md`, `r3/claude-diagnosis.md` |
| Census of the confirmation run (126 findings, 75 of 76 items) | `r2/codex-census-*.out`, merged in `r2/census-findings.json` |
| Probes run during the review (stored requests, cents) | `probe_a_plural.py` → `poc/data/a-plural-probe-2026-11-05/`; `probe_b_account.py` → `poc/data/b-filing-account-2026-11-05/` |

## Round 0 — Claude's draft (`plan-v0.md`)

Current state with evidence; what production requires (one code path, versioned prompts, D375 in the day runner, durable subjects, state × event,
preflight, acceptance on the frozen ruler given D370, decisions and documents); five questions for the rounds.

## Round 1 — five independent Codex reviews, Claude's own reading

**Asked:** three trace reviewers over the confirmation run's 76 items (`r1/prompt-traces-1..3.txt`); one reviewer to attack Claude's claims,
changes and measurements (`r1/prompt-attack.txt`); one production-engineering reviewer (`r1/prompt-production.txt`).

**Codex said:**
- Traces (`r1/codex-traces-*.out`): stopped early (2, 26 and 3 items fully read). Found: inverted revenue ladders (1239 ON, 1273 Broadcom:
  "Strongly bullish: below $18 billion") — blocker; the judge counting growth twice on a pace reference (1240 TSMC) — blocker; floor read as a
  point (1249, 1253); weak and broad B links; duplicate passages across A and B; wrong subject (1235); attribution (1254); a fiscal year dropped
  (1207); unverifiable question (1251).
- Attack (`r1/codex-attack.out`, 18 findings): the coarse/fine merge rule ("blocker"); the deal sentence too broad; D197 overreach (1250); the year
  rule picks a comparison year; the year limit skipped without a ladder; the em dash rule can change a sign; run-on quotes keep an unsupported
  summary; the pace reference anchors to the wrong base; unresolvable questions; B filing noise; ladders are not judgement coverage; all 22 due
  days empty; the blind reading measures precision, not recall; the 13-pair probe is narrow; tests check routing, not meaning; three tuned runs
  on the same 100 rows are not three draws; cost and latency at scale unmeasured.
- Production (`r1/codex-production.out`): not ready. Blockers: the same passage written twice (8 groups in the final run); groups dropped;
  manifest/run contract; preflight; frozen tests. Serious: research-subject identity is experiment-local; a limited production replay marks a cut
  day complete; acceptance needs the 22 seeds D370 retired. Proposed order: handover contract → snapshot and recovery → versioned path and
  identity → preflight and freeze → throughput → quality → acceptance.

**Claude found** (`r1/claude-findings.md`): the pace reference makes the frozen judge double-count growth (v79 rung 1 from "NT$4.8T × 1.36";
v84) — caused by my own change; a month-period question (v86); a B miss (1210 payment schedule); A opening the FY2028 revenue question late.

**Then a full census** (`r2/prompt-census-*.txt`, ten Codex readers, 8 items each): 126 findings over 75 items. Largest classes: one statement
stored twice (~18), B filing under a broader question (~14), weak links via the fallback (~14), A missing a question (8), the publication day used
as the statement day in matching (7), ladder errors (~9), attribution (7).

## Round 2 — Claude's responses; Codex reviews the disagreements and plan v1

**Claude** (`r2/claude-responses.md`, `plan-v1.md`): verified and agreed 14 points (A1–A14) — e.g., the duplicate passages (8 and 9 exact groups
counted), withdrawing the pace reference, favourable end for ladders (D186), rendering intervals from bounds, narrowing the em dash rule,
refusing run-on quotes, fixing the fiscal-year rule, year limits by admission reason, an analyst check date (for Alex). Disputed six (C1–C6):
C1 the coarse/fine rule is what D248 says ("the same outcome settles both"); C2 D197 for five versus four hyperscalers follows the standard §3 D
and D190's A17; C3–C6 open design points (a merged passage with an older-period link, groups, settling material, deal sentence). Measured the
all-open context: about 150 input tokens per open question per call.
**Probe** (`probe_a_plural.py`): plural wording "the important new questions" vs "an important new question" — no reliable difference in 20 sends.

**Codex said** (`r2/codex-disagreements.out`): C1 partly — D248 permits the merge, but the surviving question must carry the finer outcome and
the "bet separately" condition is untested; C2 partly — four versus five is fine, but total versus data-center spending is also a scope change,
the key's merge is unproven; C3 partly; C4 disagree — PRD 05 already gives groups to extraction; C5 partly — a named document is not proof of a
checkable answer; C6 partly. Most A-rows "partly": several actions fix the case, not the mechanism; A2's reference order is a new closed list;
A6's blanket refusal conflicts with D266; A8 flattens D210 (assumed obligations are checked at the next annual filing); A14 `narrowest_links`
cannot create a missing narrow link. Missed by Claude: the 400,000-character truncation (1280), floors read as bounded predictions, meaning
errors (an increase read as a total, a lost period), a broad total filed as a narrow amount (1210), unreconciled counts.
(`r2/codex-plan.out`): three blockers — B's no-home facts lost when A opens a new question in the same item (1240 Apple 2 nm → TSMC revenue);
groups contract undecided in the plan; truncated long items. Plus: contained quotes are not identity; the judge's floor reading; bounds
arithmetic; the date proposal needs a lifecycle table; all-open is already Alex's decision (measure, don't re-ask); the reference order is a new
rule; diagnose before any prompt change or paid resend (AGENTS §1, §6).

## Round 3 — Claude's stored-data checks and plan v2; Codex review

**Claude** (`r3/claude-diagnosis.md`, `plan-v2.md`): truncation 7 of 34,084 corpus items (1 in the first 100), and production truncates too;
B's no-home drops 6, of which 1 belonged to A's new question (1240); 15 contained pairs, all A beside B, 10 of them an A passage holding two
statements (A lacks the one-statement rule); references: guidance 6, pace 6, prior year 2, floor 1; five floor judgements, the floor placed at the
neutral rung's lower bound; B's accounts: 1211 a misread ("select the narrowest" — admits v10), 1246 the other-period rule applied
inconsistently, 1210 the total does not answer the narrow question. Plan v2: groups per PRD 05 in A; record preparation may link B's no-home
passages to A's questions; complete input; diagnose before prompt changes.

**Codex said** (`r3/codex-review.out`): not yet agreed. Seven disagreements: (1) blocker — merging identical quotes as `sift` does drops a second
statement's summary (stored example: one sentence carrying total revenue for v2 and data-center revenue for v10); (2) blocker — v2 dropped the
split-aware preflight, versioned entry points and freeze checks; (3) an open-ended floor cannot be the neutral span, and the judge's role is
unproven; (4) refusing a run-on passage conflicts with D266; (5) missing evidence, meaning, periods, identity and judgements not proven;
(6) acceptance lacks predeclared independent evidence; (7) Claude's causal claims go beyond the probes. Also corrected a number in the diagnosis
(1273's neutral rung is $20–22 billion, not $20–21 billion).

## Round 4 — plan v3; Codex review (pending)

**Claude** (`plan-v3.md` §0): (1) one record per quote keeping every distinct summary with its links; B's attribution kept when versions disagree,
the conflict counted; `sift`'s gap reported to Alex; (2) preflight (C-6) and the versioned path with durable subjects and freeze tests (C-7)
restored; (3) the floor rule withdrawn — diagnose the floor cases with two ladder variants and the judge's account first; (4) follow D266 and
report its summary gap to Alex; (5)–(6) acceptance by field and two predeclared measurements for Alex (C-8); (7) causal claims restated as leads.
**Codex said** (`r4/codex-review.out`): not yet. Resolved: (3) floors, (4) D266, (7) causal claims. Partly: (1) blocker — the test stops at
the stored record; prove each linked question's judge receives the right summary and source fields; (2) blocker — the service entry point is not
named or tested; (5) check the actual judgement reasons for the double-growth cases; (6) say what each acceptance measurement proves, its
reference and criteria, and how a seeded fixture runs when `replay.py` refuses seeded ledgers. New: keeping B's attribution on conflict is
unproven.

## Round 5 — plan v4; Codex review (pending)

**Claude checked** before answering: the judging request prints one summary line per piece (`judging.py` line 130), so a merged record's joined
summaries reach every linked question's judge; the only ledger-writing entry point is `replay.py`, the API and MCP scripts read ledgers; among the
17 duplicate groups of the two runs, 16 differ in an attribution field, almost all in convention (record preparation's own field wording versus
B's schema definitions), 3 in substance (1240, 1249 original source; 1251 original day).
**Plan v4** (`plan-v4.md`): judge-input test for merged records; replay as users call it plus API/MCP reading a split-written ledger; the frozen
judge re-sent on v79 and v84 with the corrected ladder, stop and go to Alex if it still double-counts; record preparation adopts B's attribution
field definitions, pieces merge only when attribution agrees, otherwise both kept and flagged; acceptance: both measurements needed, what each
proves and cannot, the seeded fixture through a measurement harness calling the production module (replay's refusal stays).
**Codex said** (`r5/codex-review.out`): not yet. Resolved: the entry points; the double-growth check. Partly: the judge-input test (fine when
attribution agrees, unresolved when it conflicts); acceptance wording. Verified v4's facts: the judge prints one summary and one set of source
fields per record; replay is the ingestion entry point among the three scripts; 16 of 17 duplicate groups differ in an attribution field, the three
named substantive cases are real but not proven to be the only ones. New blocker: "keep both on conflict" stores two versions of one statement and
departs from PRD 10 §5 ("one record linked to both questions"). Serious: without a reference the unseeded run cannot report recall or per-item
losses; the seeded fixture must be shown comparable.

## Round 6 — plan v5; Codex review (pending)

**Claude** (`plan-v5.md`): one record per quoted statement always; its attribution decided by record preparation (which runs after A and B, reads
the whole article and uses the evidence schema's field definitions) from the source, given both submitted versions, which stay in the handover for
audit; tests on 1240, 1249, 1251 with an independent reader and the judging requests. The unseeded run without a reference reports only what
independent readers checked; recall and per-item losses need a reference only Alex opens. The seeded harness first replays the stored v108 control
draw of the 2026-11-05 acceptance (main checkout) from the same seeded ledger and must reproduce its ledger before any send.
**Codex said** (`r6/codex-review.out`): "Yes. Apart from the choices the plan sends to Alex, I agree with v3 as amended by v4 and v5 as the plan
to execute. The proposed checks still have to pass." Both round-5 points resolved as a plan; the three attribution cases (1240, 1249, 1251) and
the archived v108 control (manifest, run log with the 22 seeds, archive and ledger) confirmed to exist; comparability "still a gate to prove"; no new
blocker or serious problem.

## Agreement (after round 6)

Codex and Claude agree on `plan-final.md` (v3 as amended by v4 and v5, consolidated). What remains is not disagreement but work and decisions: the
plan's checks must pass, and Alex takes the decisions in its §4. Disagreements resolved along the way: coarse/fine merges (allowed by D248 only where
the surviving ladder carries the finer outcome); D197 on spending of another scope (unproven, to test on labelled pairs); groups (PRD 05: A declares);
deal stages (one deal one question with D210's exception); floors (rule withdrawn, diagnose first); run-on quotes (follow D266, report its gap);
attribution on one statement (one record, one owner reading the source); acceptance (both measurements, each claiming only what it can prove).

## Running state

- **Agreed:** merge duplicate passages without losing a statement; A gets the one-statement rule; groups by A per PRD 05; B's no-home passages
  offered to A's questions through record preparation; no silent truncation; admission reason with D210's two obligation cases; favourable end,
  code-ordered and rendered intervals, bounds recomputed from a stated band; pace reference withdrawn; sequential D375 runner with a state × event
  table; split-aware preflight; versioned path, durable subjects, freeze tests; diagnose each quality class before any prompt change.
- **Disputed:** none after round 6 (Codex: "No remaining blocker or serious disagreement with the plan itself").
- **For Alex:** acceptance arrangement given D370; the fallback sentence (D273/D361); all-open capacity and cost; a check-date policy; production
  findings (`sift`'s merge, D266's run-on summary, matching's statement day, Jev's partial-overlap repeats, truncation); long items; promotion.
- **My mistakes recorded:** the answer keys sat in the first blind readers' folders (stopped within seconds, relaunched clean); the pace
  reference, the em dash rule, the run-on rule and the year rule were my changes that the reviews showed to be wrong or too broad; causal claims
  stated beyond what the probes show.

## Round 7 — the plan built; production-path probe; comparability gate; benchmark design; Codex review (pending)

**Built (2026-11-05/06, after Alex adopted the plan's recommendations):** `src/hivemind/split.py` (snapshot of every question open before the item,
research subjects in the ledger, source quotes, sections for long items, A/B/record-preparation requests, one record per quoted statement with every
summary and link, unfiled passages offered to the item's new questions, ladder order by favourable end with rendered intervals, stated-band and
empty-rung checks, admission checks by reason, analyst check dates); the split branch of `views/round.py`; `scripts/replay.py` runs a split
configuration item by item; `poc/config/poc-split-v3.json` (split-a-v3, split-b-v1, split-preparation-v1, collision-v5);
`scripts/preflight_split.py`; `state-by-event.md`; tests `tests/test_split_extraction.py` (13, each with a mutant that fails it).
**My mistakes this round:** (1) the first production-path run sent collision-v5 without the relation definitions written for it (the schema switch
named collision-v4 only); found from the code after 9 items, run stopped, fixed (`RELATION_DEFINITION_PROMPTS`) with a test and mutant, relaunched
in a new folder reusing the archive. (2) An empty rung ("exactly $279 billion", lo = hi) passed the shared bounds check; 0 of 160 stored numeric
ladders had one; the split's own check now refuses it (the shared check is the frozen path's and stays). (3) I edited `split.py` (subject order) while
that run was live, against AGENTS §9; the running process had the module loaded, and the order it uses is the insertion order the edit names, so no
request changed; recorded here.
**Preflight (C-6) on the stopped run's 9 items:** requests 9 judged, preparation 3, handovers 9; 0 refused; a copy with one stored summary edited is
refused (positive control).
**Comparability gate (C-8.1):** the harness replayed r10-control-v108/d1 from its archive with every unarchived request refused: identical totals,
0 refusals, every ledger table identical except `revisions.said_day` on 4 rows (this tree stores the statement day per D203) and completion stamps.
A stored judgement refusal is replayed once in recorded order (the first attempt had failed on it: the archive renames a refused answer's key).
**The measure** (`bench_measure.py`) reproduces the r10 acceptance's judgement totals on the stored draws (control 15, 16, 14; v116 18, 17, 18).
**Benchmark design** (`docs/research/2026-11-06-architecture-benchmark/benchmark-design.md`) sent to Codex before any paid draw (`r7/`).
**Codex said** (`r7/codex-review.out`): not ready — three blockers and six serious findings:
- (1) the agreed test set is not scored;
- (2) the thresholds have no estimate of how often they fail a control against itself (the weakest-draw allowance of 5 is smaller than the
  control's 8-point spread);
- (3) ledger-only scoring cannot tell extraction losses from later losses;
- (4) the question counting aid had been changed (50% overlap instead of the established helper's 20%);
- (5) the gate is "matched with a documented D203 difference", not exact, and the comparison omitted tables and the starting fixture;
- (6) the replay-of-refusals claim was too general;
- (7) no reading packet or hit matrix;
- (8) the D373 disclosure, the standard's hash and per-file pins were missing;
- (9) no preflight record, and the arms differ in more than the extraction.
**Claude checked each against the files and agreed with all nine.** Fixes:
- the test articles through each arm's extraction stage against the same fixture (`bench_test_articles.py`);
- thresholds re-derived from six stored control draws (helpful mean − 8: 1 of 20 false failures; core mean − 3: 0 of 20; judgement total − 3: 0 of
  20; the weakest-draw rule failed 4 of 20 and is withdrawn);
- both the checked handovers and the ledger scored, with where each matter ends;
- the established helper restored and labelled a counting aid;
- the gate's wording corrected, with processing steps, match records and subjects added (all identical), and the fixture identical to the stored
  seeded state;
- the refusal-replay claim narrowed;
- per-matter hits written;
- D373, the standard's hash and the file pins printed or recorded;
- the arms' three differences named, and an outcome attributed to the whole architecture.
Revision 2 sent to Codex (`r8/`).

## Round 8 — benchmark design revision 2; Codex review

**Codex said** (`r8/codex-review.out`): still two blockers.
- The split preflight compared selected fields, did not reconcile the population, and skipped missing inputs.
- The verdict "at least as good" could hide a real loss within the allowances, and the test set could not stop it; the thresholds and the D203 gate
  exception needed settling under the plan's authority.

Serious: resumed draws could mix versions; the reading plan skipped misses shared by both arms or missed once; the design hash file did not exist.
Resolved: the question counting aid, the refusal-replay claim.

**Claude checked and agreed.** Done before revision 3:
- Preflight rewritten: population, full handover after research-subject registration, refusals. Two-day probe: 73/73 equal, 0 refused. Four
  tampered copies each refused.
- `scripts/preflight.py` matching checks: 793 judged, 1 refused. It is the pilot's own sequence 58, a final-state artifact.
- Gate re-run with the stored writer line in a scratch copy: all 24 tables identical, so the only difference is the D203 line.
- Verdict replaced by reporting the differences beside the same-configuration range, with stop rules (window and test). No threshold claims
  equality, so no acceptance threshold needs authorising; promotion stays Alex's (D359).
- A reading packet for every missed helpful matter in every draw (`bench_traces.py`).
- Resume refusal on changed files.

**Also found on the two-day probe:**
- New questions with a ladder fell 14 → 5 against the confirmation run.
- Of the 14 empty ladders, 9 had no full-period reference in the source, 2 had growth-only guidance with no base, and 2 had a reference the model
  passed over.
- The model's account blamed the reference sentence. A cents probe re-sent the stored requests: the stored sentence produced a ladder on the
  Alphabet case that had been empty (a coin flip), and the reworded sentence lost two control ladders.
- No change was built (AGENTS §1.4). The ladder share is reported in the benchmark.

Revision 3 sent to Codex (`r9/`).

## Round 9 — benchmark design revision 3; Codex review

**Codex said** (`r9/codex-review.out`, in Chinese): one blocker and five serious findings.
- Blocker: the preflight proves request content, not the bytes sent; and it does not list refused split answers.
- Serious:
  - pins incomplete (fixture, universe, items, scoring code);
  - a new folder holding an old archive would reuse answers;
  - the reading packet lacked full answers and record preparation;
  - the current-code gate is not exact;
  - the stop lines lack Alex's decision.
- Resolved: the test set, the counting aid, the refusal-replay scope.

**Claude checked:** agreed with the pins, the stray archive, the packet and the gate wording, and fixed each.
- The pins now cover the universe, seeds, fixture, items, scoring code, golds and standard; a resume with differing pins is refused; a new folder
  must hold no ledger or archive.
- The packet now carries full answers with call ids, record preparation, the full handover and the processing steps. On the stored control draws
  it shows that 9 draw entries without answers are merged copies or an item outside the feed.
- The gate is labelled "identical except four dates", handled under D203.

**Disagreed, with reasons sent to Codex:**
- On the wire bytes: the archive never kept send order, so the limitation is stated, as Codex's own fix allows. No stored request is re-sent, and
  the preflight now lists unreplayable split answers (none).
- On the stop lines: they are D355 in Alex's words, not acceptance thresholds; promotion stays D359.

Revision 4 hashed (`benchmark-design.sha256`) and sent (`r10/`).

## Round 10 — benchmark design revision 4; Codex review

**Codex said** (`r10/codex-review.out`): it withdrew the stop-line objection ("你对停止线的区分是对的" — the design only says when to stop and re-evaluate,
and accepts or promotes nothing). The send order is no longer blocking: both arms send through the production path. It verified all 11 design
hashes. Three serious findings remained:
- the preflight did not run the production format check on archived answers (Codex ran it on the probe's 167 answers itself: all pass);
- scoring printed hashes but did not verify them against each run's pins;
- `--archive-from` could import an archive into a paid draw.
Also: the packet did not mark one missing stage, and it gave written records as quotes only.
**Claude agreed and fixed all four:**
- the preflight's format check: 167 judged, 0 refused;
- `verify_pins` in the measure;
- import allowed only offline;
- missing stages marked, and written records given in full with their links.
Revision 5 hashed and sent (`r11/`).

## Round 11 — benchmark design revision 5; Codex review

**Codex said** (`r11/codex-review.out`): the format check is resolved (167 answers, 0 refused, re-run by Codex). Still serious:
- scoring let a run without a manifest through, and it excluded the shared prompt files;
- an offline run could be resumed as a paid draw and carry its imported answers;
- the packet did not mark a null answer or a missing section of a long item as unread.

**Claude agreed.** This is the third round on one mechanism, a scored draw's provenance, so instead of answering the findings one by one, one
structural rule was written into the design and its code (AGENTS §1):
- a scored draw is a paid draw by this harness, in a fresh folder, with one mode and one set of pins for life;
- scoring refuses everything else, and requires every file two runs both use to be identical;
- the packet marks unread per section and stage.
Revision 6 hashed and sent (`r12/`), asking only for findings that could change the numbers or their reading.

## Round 12 — benchmark design revision 6; Codex review

**Codex said** (`r12/codex-review.out`): the format check and the stray archive are resolved. Two serious findings remain:
- the cross-run pin check compared only neighbouring runs, so split, control, split could hide two versions of a split-only prompt;
- the packet counted answers per stage without mapping calls to sections, and missed a null call beside a valid one.

**Claude agreed** and fixed both: every file is compared across all runs that pinned it, and each call is mapped to its section by the section's
opening text. Each fix has a positive control. While testing, Claude also found that the scoring helpers' import chain loads another worktree's
`hivemind` package (haiku_week.py hard-codes it). That would have priced costs with another tree's table, so both scripts now load this tree's
package first and refuse otherwise. The stored r10 costs are unchanged (77, 74, 79). Revision 7 hashed and sent (`r13/`).

## Round 13 — benchmark design revision 7; Codex review

**Codex said** (`r13/codex-review.out`):
- The pin comparison, the stray archive, the format check and the scoring materials are all resolved (it verified both orders).
- One serious finding remained: the packet tied a record-preparation answer to an article by its quotes. Another article that carries the same
  quote could be paired wrongly; Codex reproduced this in memory and found no mispairing on the probe.

**Claude agreed.** The answer is now tied by the item's whole article text, which the preparation request carries. More than one match is marked
unread. Checks:
- control: another article's answer with the same quote is not tied, and the item is marked unread;
- probe: all 21 preparations tied, 0 items unread.

`launch.sh` was added and hashed. Revision 7 sent (`r14/`).

## Rounds 14–15 — launcher; agreement on the benchmark design

**Codex said** (`r14/`): round 7's finding resolved; `launch.sh` checked only the six window folders, so an old test folder could be reused. **Claude
fixed it** (all twelve folders checked before any draw starts). **Codex said** (`r15/codex-review.out`): "No remaining blocker or serious finding."
**Agreement:** the benchmark design (revision 7, `benchmark-design.md`, hashes in `benchmark-design.sha256`) is agreed after nine Codex rounds (r7–r15).
Launched by `launch.sh`.

## Benchmark running (2026-11-06) — test articles scored; findings so far

Launched 16:53: three split and three control window draws, and six test-article draws. All six test draws finished: 30 of 30 articles each, 0
failures. Test, extraction stage (`bench_measure.py --test`; pins verified for 6 runs):
- helpful reached: split 24, 27, 23 against control 21, 26, 23;
- core: split 8, 8, 8 against 8, 7, 7;
- not-kept written: split 8, 7, 4 against 4, 9, 7;
- questions proposed: split 3–4 against 2.
The split is not below the control, so the test stop rule does not fire.

Independent Codex readers put down every test miss (`results/miss-test-*.out`):
- split, 64 missed draws: 58 not written by the model, 5 dropped by a check (B quotes refused, no home), 1 present in other words;
- control, 68 missed draws: 29 not written, 36 dropped by a check (the frozen filing's "no home": written but linked to no open question),
  3 gold questions (recorded, not applied).

Read by Claude:
- The largest difference is a core matter (SpaceX seeking $40 billion of financing for an NVIDIA chip order): the split missed it in 3 of 3 draws,
  the control reached it in 3 of 3.
- Mechanism: B quoted a 1,250-character passage of five paragraphs that skips one sentence. The source check refuses it in all three draws (correctly:
  it is not one passage), and the statement is lost.
- Census on the test draws: B quote refusals 1, 1, 2 per draw; the control has 0.
- Recorded as a finding with its census, not answered during the run (AGENTS §7.3).
- Correction (same day): I first wrote that B lacks the unit rule. It does not: B's prompt, like the frozen role-v74i, says "One evidence item
  records one statement … Copy its quote verbatim".
- The model's own account on two stored B requests (`probes/b-quote-account-2026-11-06.json`): it joined the deal's paragraphs under the closing
  check's "one deal … told in several sentences … is one evidence item; keep the fuller wording", and cut the share-price sentence under the reject
  list; in the second draw, "No instruction led me to join those paragraphs. That was an error."
- The frozen sift refuses the same stitched quote ("quote not in item"), so the split's check matches production. The control's model quoted the
  first sentence only, under the same rules.
- The class is a misread at the meeting of two existing rules, 1–2 items per 30 articles. It is counted on the window draws before any sentence
  ("a quote is one unbroken passage of the source") is proposed.
- Split window draw 1 stopped at 2026-07-07's judging: "judgement refused twice: v2: v1 is not among the evidence shown to v2". Traced: the frozen
  judge (judging-v7) first named the theme seed v8 (H200 import authorisation, shown to every asset judgement under D191) in `cites_views`, which
  must hold dependencies; the check refused it ("v8 is not a dependency of v2"). Its retry put the view id v1 among the evidence cites and was refused
  again. The same theme-as-dependency refusal hit v17 once in this draw and passed on retry.
- Judging is the frozen code both arms run. The stored r10 control draw had seven refused judgements, all of which passed on retry.
- Resumed through the product's own resume path, in the same folder, mode and pins. The refused answers are retired, so the judgement is sampled
  again. To keep the pins, the post-run reading script `blind_records.py` was moved into `readers/`; the design hashes verify.
- Refused judgements per draw are counted for both arms when the draws finish.

## Round 16 — benchmark results; Claude's reading; Codex review (pending)

All twelve draws finished. **The window stop line fired:**

| Quantity | Split | Control | Difference |
|---|---|---|---|
| Helpful matters reached | 156, 156, 159 | 166, 170, 162 | −9.0 (range −8) |
| Core matters reached | 71, 75, 76 | 76, 76, 75 | −1.7 (within range) |
| Judgement agreements | 44 | 47 | −3 (on the edge) |

- Noise: extras −21.3 a draw and not-kept −4.3 a draw.
- Articles opened as questions: 44 against 12; the blind reader would open 25 against 6, and found 0 duplicates in either arm.
- Test articles: the split is not below the control.

Readers, window misses:
- split: 192 not written, 21 dropped by a check, 18 present in other words;
- control: 116 not written, 60 dropped by a check, 20 present in other words.

Mechanisms:
- M1, the evidence call writes less. The one-sentence contradiction ("leave links empty" against the fallback field) was tested on 20 stored items
  and refuted. Swapping B's system prompt for the frozen role-v74i on the same 20 items, two sends each, recovered 18 and 21 of 27 lost matters,
  against 10 and 10 as stored, with helpful 73 and 77 against 57 and 58; not-kept rose to 12 and 12 from 5 and 6.
- M2, new specific questions take evidence from the broad seed question (v9 and v23). This is D207 by design; the missing dependency is D51.

Reading and one recommendation in `docs/research/2026-11-06-architecture-benchmark/results/results-reading.md`; sent to Codex (`r16/`).
**Codex said** (`r16/codex-review.out`): it agrees the stop line fired and the split as built is not promoted, but it disagreed with the
reading. Five serious findings:
- the v9 explanation combined different draws: v23 is a different question in draws 2 and 3;
- the v10 cause was not shown to be sufficient;
- "58 of 64 not written" conflicts with the readers' 51, 6 and 7;
- the probes were overstated (items selected by misses; the whole block, not a sentence; extras rose);
- the recommendation skipped the prompt audit and a balanced test.
Two minor findings: 3 and 3 unclassified misses; agreed reads missing from the report.

**Claude checked each and agreed with all seven.** Done:
- Per-draw v9 filings: v23 took the backstop records only in draw 1, where v9 agreed. M2 is withdrawn as a cause; D51 stays an open concern.
- An independent reader on v9 and v10:
  - v10: all three split draws lacked the ~66% operating-margin record the agreeing controls anchored on;
  - v9: one draw lacked a record, the other applied a larger discount to comparable evidence.
- The readers' numbers were adopted.
- The probe claims were narrowed.
- Hits and extras read blind: hits 20 of 20 in both arms; about half of all extras are worth keeping, so fewer extras is not less noise.
- Ladder counts: 21 of 44 split questions against 12 of 12.
- A prompt audit of B with a blind second reader. Both name B's first task sentence ("…help answer an existing question") as keeping narrower than
  the standard's keep-then-file rule.
- The recommendation was rewritten: B's request revised from the standard's keep rule, without growth; one test on a seed-drawn article set,
  against the unchanged request; a window run only on Alex's word.

Reading revision 2 sent (`r17/`).

## Round 17 — reading revision 2; Codex review

**Codex said** (`r17/codex-review.out`): five of seven round-16 findings resolved. It agrees with the direction: decide what an analyst would note
before filing it, as the standard says; this is a general issue, not a fitted rule. Two serious findings remained:
- the revision kept B's copy of the closing check although the audit flagged narrowing sentences in it;
- the test had no sample size, harm coverage, prediction or failure boundary.
Small items: the contradiction was still called "not the cause"; the reasons counted 16 of 17.
**Claude agreed.**
- The revision now reconciles every flagged sentence, including B's copy of the closing check; production's frozen prompt is untouched.
- The test is fixed: 40 seed-drawn dev articles plus the 30 test articles, current against revised B, three sends each, on stored requests the
  same day, with the frozen control's rates as reference and a blind reader on additions and links; the prediction and refutations are written.
  Acceptance only on the whole benchmark, on Alex's word.
- The wording was corrected, and the source-support reason count fixed to 10.
Revision 3 sent (`r18/`).

## Round 18 — reading revision 3; Codex review

**Codex said** (`r18/codex-review.out`, in Chinese): every round-1 finding is resolved except the test. Two items partly resolved, one claim to
narrow:
- "a newly reported fact about an existing arrangement is kept" is too broad; the standard still asks whether the fact bears on a question;
- the test did not fix the article list and its coverage, the blind sample's draw, or check its failure lines against same-version variation
  (AGENTS §7.1);
- the first sentence is the strongest lead, but how much of the loss it explains is not measured.
**Claude agreed** and fixed all three:
- the wording follows the standard's relevance test;
- the article set is fixed with its coverage (`next-test-set-20261107.json`: 29 with helpful matters, 6 all-reached, 23 with misses, 9 lost, 4
  gained, 11 without helpful matters);
- the blind samples are seed-drawn from all sends;
- the current request is sent six times so that current-against-current gives the self-variation before the revised sends are read;
- the claim is narrowed.
Revision 4 sent (`r19/`).

## Round 19 — reading revision 4; Codex review

**Codex said** (`r19/codex-review.out`): the wording and the claim are resolved, and it agrees with the main reading and the direction. The test's
conditions still conflicted:
- two not-kept lines that contradict each other;
- how each condition meets the six current sends, and what happens when the self-comparison fails, was not stated;
- a pool under 20 was still compared by a "2 of 20" line;
- the 11 articles were wrongly described as having nothing worth keeping.
**Claude agreed** and rewrote the test as one set of three conditions:
- gain: more than the larger of 3% and the self-difference;
- not-kept: at most the larger of the control's count and current's, plus the self-difference;
- blind quality: shares within 10 points.
A self-check runs first, with C4–C6 standing in for the revised version against C1–C3. Pools under 20 are compared as shares, and an empty pool is
unexercised, which counts as not passed. Revision 5 sent (`r20/`).

## Round 20 — reading revision 5; Codex review

**Codex said** (`r20/codex-review.out`): the not-kept contradiction, the share comparison and the 11 articles are resolved, and the self-check
arithmetic holds. Two items remain:
- one split of six sends underestimates noise. On the stored window draws, one split differs by 4 and another by about 9.3.
- the blind quality condition bounds shares, not the volume of unwanted additions.
**Claude agreed:**
- S_h and S_n are now the largest difference over all ten three-against-three splits, and above 6% the test stops as "not decidable".
- Condition 3 now bounds R's estimated unwanted additions per send by the frozen control's on the same articles, read blind the same way: the split
  must not become noisier than production.
Revision 6 sent (`r21/`).

## Round 21 — reading revision 6; Codex review

**Codex said** (`r21/codex-review.out`):
- the noise estimate over all ten splits is right, but a noise above 3% means only larger gains can be confirmed, and this was not stated;
- widening condition 3 after a failed self-check contradicts "no noisier than production";
- the stored production records are from another day; a same-day production re-send is needed.
**Claude agreed**, and since this was the fourth round on one mechanism (the screen's decision rule against noise), it wrote one structural
rule instead of answering the items one by one:
- the test is a screen that accepts nothing;
- every condition is first applied to the current request against itself on the same day;
- a failed self-check makes the condition "not decidable" and stops the screen;
- no line is widened.
Production is re-sent the same day (P1–P3). Condition 1 states what it can and cannot prove. Revision 7 sent (`r22/`).

## Rounds 22–23 — reading revisions 7 and 8; agreement on the results

**Codex said** (`r22/`): no finding that could let the screen pass noise or a noisier version, but the self-check rule made condition 1 always
undecidable. **Claude fixed it**: a self-check judges the current request against itself as a version equal to the current one should be judged
(no gain for condition 1, within bounds for 2 and 3). **Codex said** (`r23/codex-review.out`): "No remaining blocker or serious finding. I agree with
the reading and with the recommendation and its test as the next step to put to Alex."

**Agreement on the benchmark results (after eight result rounds, r16–r23):**
- The window stop line fired: helpful matters −9.0 against a −8 range. The split as built (poc-split-v3) is not promoted, and the line goes to Alex
  (D355).
- The loss is in what the evidence call writes. The strongest identified lead is B's first task sentence, which makes connection to an open
  question the test of a statement, against the standard's keep-then-file order. How much of the loss it explains is not measured.
- One recommendation, revise B's request from the standard's keep rule, with one screen fixed in
  `docs/research/2026-11-06-architecture-benchmark/results/results-reading.md` §4. The whole benchmark runs only on Alex's word.
- Disagreements resolved along the way:
  - M2 withdrawn as a cause of the v9 losses;
  - the readers' classification adopted over the code's;
  - extras are not noise;
  - the probe shows the instruction block, not a sentence;
  - the closing check is in the audit's scope;
  - the screen's noise and volume rules, ending in one structural rule.

## Alex's decision and the screen (2026-11-06)

Alex: "我不理解。所以拆分版成本更高，效果也没有更好" — answered yes, as built: about 15% more cost ($0.99 against $0.85 a window draw), fewer helpful
matters, its one strength is opening more questions worth following (and more that are not). Offered two options; Alex: "好，按1试一次" (try the
revised evidence call once, with the agreed screen).

Built for the screen:
- `src/hivemind/prompts/split-b-v2.txt`, 5,104 → 5,100 characters. Five changes, each from the audit:
  - keep first, then file, with "a question says where a kept statement goes, never whether it is kept";
  - the connection sentence cut (the links field owns it);
  - the section heading changed;
  - "leave links empty" cut;
  - the figure list names margin and backlog.
- In `split.py`, B's closing-check copy names competitors and margins among newly disclosed figures (`B_CHECK_REVISIONS`, by version), +40
  characters, from the standard's §5.1 and §6. Production's frozen check is unchanged.
- `poc/config/poc-split-v4.json`.
- `screen/screen_b_v2.py`.
Every request is rebuilt by the production code and checked against its stored identity: 69 of 70 articles prepared (39 dev, 30 test), one
excluded as a merged copy.

Note on the earlier probes: `probe_b_link_sentence.py` and `probe_b_system_prompt.py` re-sent the archive's sorted-key JSON, not production's build
order. Their arms are compared like with like, but their bytes are not production's (AGENTS §5). The screen sends through production's path.
Estimated cost about $1.02 (upper bound).
**Screen result (counting aid), 69 articles, 0 failed sends:**
- Condition 1 passes: revised mean 92.0 against current 84.3; the line is S_h = 5.67 (3.9%); production 94.0.
- Condition 2 fails by one entry: revised not-kept mean 24.0 against the bound 23.0 (production 18.33 + S_n 4.67); current 17.3.
- Additions: revised 16.3, current 15.0, production 25.0.

Claude read the 25 not-kept entries the revised version wrote more often and judged them right.

**Codex said** (`r24/codex-review.out`): the numbers reproduce, but two serious findings:
- the not-kept count matches a quote's neighbouring sentence even when the summary records another statement (the 128GB memory clause, the
  depreciation clause, "a great machine"); removing those for both versions puts the revised mean exactly at the bound;
- the set ran 69 of the 70 named articles (one merged copy, no stored request in any arm), a deviation the rule did not cover.
**Claude agreed** (AGENTS §7.3: the rejection is checked before a version is rejected). All 225 not-kept matches of the 12 sends (212 unique pairs)
go to a blind independent reader, who decides whether each record keeps the excluded matter as its statement. Condition 2 is recomputed from the
confirmed matches, consistently for every version and for S_n.

The missing article is a dispatch-level merged copy, the same in every arm; it is excluded from all versions alike and the set is reported as 69.
**Recount after the blind reader** (`screen/notkept-check-reader.out`, 212 pairs: yes 197, no 10, unsure 5; `screen/recount.txt`):

| Unsure pairs | Revised not-kept mean | Bound (production + S_n) | Condition 2 |
|---|---|---|---|
| counted as kept | 22.67 | 21.67 (17.33 + 4.33) | fails |
| not counted | 22.00 | 21.33 | fails |

The self-check holds both ways. The miscounts fell in every version, production included, so the bound fell with them.

**Codex said** (`r25/codex-review.out`): "No remaining blocker or serious finding." It recomputed all twelve sends itself and agrees. Two matches
each covered two records; Codex read the second records and the count is unchanged. The set is reported as 69 articles (39 dev, 30 test).

**Agreed outcome:** the revised evidence call (poc-split-v4) is not adopted.
- It reaches production's level of helpful matters (92.0 against 94.0; current 84.3).
- It also keeps more of what the standard rejects than production does (22–23 against 17.3 a send): product details without business scale,
  matters unrelated to the company, generic claims.
- Mechanism: the existing-question gate in split-b-v1 kept out both useful indirect facts and this noise. Removing it brought both back.
By the rule told to Alex before the screen ("if it cannot clearly catch more facts without getting noisier, drop the split and keep production"),
the recommendation is to stop the split and keep production.

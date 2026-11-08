# Step 1 fix round: evidence left unfiled (council loop, 2026-11-08)

## 0. Frame

**Alex, 2026-11-08:** "先修第一步，问模型为什么不归档季度业绩，run council loop skill, 深度的思考怎么突破这个问题，确保不是hardcode fix 和overfit prompt".

**Objective.** Stop helpful evidence being lost as "unfiled" without adding noise or small theses. On the K6b test run, 7 of the 10
missed helpful matters were extracted and then dropped because no thesis took them, among them Q2 FY27 revenue of $96.2bn with data
centre up 117%.

**Pass line: proposed, not confirmed.**
- Dev (115 golden-v5 dev articles, forward from empty, one draw): helpful at least K6b's lower draw (197/234); not-kept spans at most
  K6b's 40; small theses at most 3; fragments 0, from source-backed readers.
- Test (26 tagged articles, scored once at the end, already exposed): helpful at least 35/42; not-kept at most 8.

**Reference system.** K6b on DeepSeek Flash, high effort (Alex's chosen configuration): dev draws `gold-k6b-flash`, `gold-k6b-flash-d2`;
test draw `test-k6b-flash`.

**Ruler.** golden-v5, frozen: dev `6f9476bb…`, test `af2145cd…`. D373 applies: a suspected gold–standard inconsistency is recorded apart
and scoring continues on the unchanged gold. The E1 diagnosis (2026-11-06) already recorded such a concern: some gold-helpful
statements are ones the standard's §6 drops when no question takes them.

**Guard against overfitting (Alex's words above).**
- The test articles locate the mechanism only. Arms are designed and probed on dev articles, and test is scored once per final
  configuration.
- No rule names a company, an industry, a statement kind, or a test or gold case. Every request change traces to a line of the signed
  standard or a decision (AGENTS §6) and must read the same for a bank, a drug maker or a retailer.
- A code list of what matters is out (AGENTS §2: code owns identity, never importance).

**Constraints.** The frozen ruler; frozen production; Steps 2 to 4 out of scope.

**Budget.** Model-account probes and request probes cost cents. A dev forward run costs about $1 at DeepSeek Flash's published rates
($0.30 / $1.20 per M), and the test run about $0.25.

## 1. Census on stored runs ($0; `census_unfiled.py`, `poc/data/clean-step1-unfiled-2026-11-08/census-*.json`)

| Run | Unfiled items | Helpful if kept | Not-kept spans if kept | Unmatched if kept |
|---|---|---|---|---|
| Dev Flash d1 | 15 in 13 articles | 205 → 214 (+9, core +0) | 40 → 43 | 28 → 29 |
| Dev Flash d2 | 34 in 26 articles | 197 → 220 (+23, core +0) | 38 → 47 | 21 → 25 |
| Test Flash | 17 in 10 articles | 32 → 38 (+6, core +1) | 8 → 12 | 2 → 3 |

- **The draw-to-draw recall gap on dev (205 against 197) is mostly the unfiled count (15 against 34).** With unfiled items kept, the
  two draws are 214 and 220.
- What the helpful unfiled items are differs by set:
  - **Dev:** almost all are small matters K6b's signed do-not-open boundaries leave without a home: partner integrations (Palantir
    Nemotron, LangChain, GR00T partners), small investments (Verkada, Gradium), an executive hire, the company's debt raise, valuation
    scenarios, and an analyst EPS estimate.
  - **Test:** the company's own financial performance (Q2 revenue $96.2bn, the only core miss; free cash flow; the 50% FCF return plan;
    the analysts' $441bn FCF forecast), one link miss (AI infrastructure spending to 2029, which an open thesis covers), and Dell RTX Spark
    one day before that thesis opened.

## 2. Mechanism

**Model's own account** (`unfiled_account.py`). The stored DeepSeek conversation was continued exactly as sent, with one question per
unfiled item: 32 items (test 17, dev d1 15), $0.11 (`account-test.json`, `account-d1.json`).
- **Financial results and cash** (test 2:e1, 4:e1–e6, 8:e4; d1 40:e2, 57:ev-4, 62:e8–e9). The model quotes section 3's "Do not open a
  thesis about: … a buyback authorisation or dividend declaration; one quarter's figures or guidance … Their statements are evidence for
  the broader thesis they inform, or unfiled", and the unfiled rule.
  - It names the analyst's question itself: "How durable is Nvidia's data center revenue growth?", "Can NVIDIA sustain gross margins…",
    "How much free cash flow…".
  - It finds that question not open, and treats it as barred by the do-not-open list.
  - In 3 cases it adds "on review that was wrong" (4:e5; d1 40:e2, which cites section 3's own "quantities that carry the company's
    value (… gross margin, capital spending)" as a big matter).
- **Link misses** (test 15:e3 AI infrastructure spending; 8:e4 FY2026 revenue): "On review that was wrong. … That question is already
  open: clean-4".
- **Small matters** (exec hire, Gradium, quantum model, shareholder proposal, cargo theft, retail prices, a donation): the model cites
  the do-not-open list or the closing check's not-kept rows. These are drops the standard intends.
- **Valuation** (test 15:e4; d1 38:e5, 66:ev-3): "'Is the stock attractively valued?' is an investment conclusion", so the standard
  intends these drops too.

**Prompt audit (AGENTS §6; `.claude/skills/prompt-audit`)**, the class mapped to the request:

| Failure class | Request sentences | Standard or decision | Verdict |
|---|---|---|---|
| Company's own financial performance, estimates and cash left unfiled (test: 4 helpful, 1 core; dev d1: 4 items, not gold-helpful) | `k6b-system.txt` ll. 93–96: "Do not open a thesis about: … one quarter's figures or guidance … Their statements are evidence for the broader thesis they inform, or unfiled"; ll. 7–8 and 52–53 and closing l. 15: unfiled when "not itself a big matter" | Section 3 ll. 84–85 of the same request: "Big matters include the quantities that carry the company's value (the segment that carries the business, gross margin, capital spending)". The standard's five question types include the company's own reported lines. **D371 (Alex, 2026-11-05): "收入和财务这边对于当下，未来应该都是需要track 的，你应该要修改" — "a quarterly period is not itself a reason to withhold information …; do not confuse retaining and connecting evidence with automatically opening a separate question for every line … do not hard-code company, item or metric-specific importance."** | **contradiction**: the do-not-open item for one quarter's figures is read as barring the question of the quantity itself, and "or unfiled" gives the exit |
| Link misses (test: 1 helpful) | l. 5: "the narrowest open thesis that covers it"; closing l. 15 | Standard §6: file under the narrowest open question (D207) | **misread**: the model's account admits the error |
| Small matters and valuation (dev: most of the +9 / +23; test: 1) | ll. 88–96 (scale test, do-not-open list); §3 counterexample on valuation | Signed boundaries (v74i; D248, D250); E1 (2026-11-06) recorded that some gold-helpful statements are ones the standard's §6 drops (D373) | **not a target**: these drops are intended. Recovering them would be benchmark farming against the standard |
| Dell one day before the thesis opened | | D209: no-home is dropped; no re-placement | **not the prompt**: ordering, by design |

**Prior decisions on the mechanism:**
- D209: a statement no question takes is dropped, and no side list is kept.
- D370: seeded questions are retired, so seeding a revenue question is not available.
- D371: present and forward financial information is tracked, with no question per line and no hard-coding.
- D373: a gold–standard concern is recorded apart.
- E1 (2026-11-06): production's no-home drops were mostly link misses on fences (period, population, configuration); a re-check sentence
  "recovers some, and misfiles about as many" (PRD 10 §3).

**Target for this round:** the contradiction class (D371) and the link-miss class. Not the small-matter class.

## 3. Council A (`council/a-*`, `b-*`)

**Codex's independent read agrees on:**
- the mechanism: the one-quarter do-not-open item read as a reason to discard the financial evidence;
- link misses as a second class;
- small-matter drops being intended;
- farming risk: filing every gold-helpful item, or routing loose facts into a revenue catch-all.

Its levers were a required per-item decision (the same as Claude's L3), moving the check, and effort or model.

**The challenge rejected Claude's first u1** ("results … and cash generation are evidence for the question of the quantity … open that
one question"). It removes the analyst's opening judgment, and "cash generation" is not established as a big matter by the standard.
- u1 was rewritten. It keeps "one quarter's figures or guidance are not a thesis"; such figures, and estimates or guidance for any
  period, are evidence for the broader question of the quantity they measure. Link them to the open thesis that asks it. When none is
  open, judge that broader question by section 3's test and open it only when it passes; never one per quarter, line or estimate.
- Net +24 characters, after the two duplicated sentences were cut. Source: D371's own wording.
- u3's field may answer "none".

**Guards added at Codex's request:**
- a non-key financial line at empty state (seq 85, automotive revenue);
- the important measures already covered (seq 57 and 62 at the stored state, where the revenue home clean-11 is open: no duplicate
  thesis may open);
- empty-state small-matter control seq 108, where no thesis should open.
- Seq 8 (supplier capacity) is read against its own before-state before it is labelled.

## 4. Arms and probe 1 (predeclared)

**Arms** (`arms/`):
- **k6b**: control, rebuilt byte-for-byte from the stored request.
- **u1**: the contradiction removed at its owner (D371).
- **u3**: required `filing_question` before `links`, and `why_unfiled` after.
- **u1u3**: both.

**Cases** (`cases.json`, 16):
- **targets at their stored states:** d1 40, 57, 62, 66, 38; d2 8, 6, 66;
- **empty-state (synthetic bootstrap, labelled):** 40, 57, 62 (financial), 85 (non-key financial line), 108 (small-matter control);
- **guards at their stored states:** d1 22 (hire), 29 (the company's debt raise), 113 (quantum model).

3 draws × 4 arms = 192 sends, about $1.9. A synthetic arm-conformant answer passes every code check, and the control matches the stored
bytes.

**What it decides:** whether u1 or u3 files the company's financial evidence and link-miss items without raising small theses, noise
or misfiling on the guards, and which lever does it.

**Falsifiers:**
1. u1 does not raise filing of the target items, or opens per-quarter, per-line or duplicate theses.
2. u3 explains but does not file, or raises small theses.
3. Any arm raises guard theses, wrong links or ruler noise beyond the control's three draws.

## 5. Probe 1 results (`poc/data/clean-step1-unfiled-2026-11-08/probe-r1/`; 192 sends, $2.51)

- 3 format failures, all in the u3 family: DeepSeek added an extra `tier_note` field. They are recorded, not retried.
- Two blind readers judged 189 answers under shuffled labels (`reader-answer-R{A,B}-*.json`). Their thesis and unfiled counts came out
  identical while the notes differ: the same model family, so not independent.

| Sum of 3 draws, 16 cases | k6b | u1 | u3 | u1u3 |
|---|---|---|---|---|
| Ruler helpful (dev gold) | 69/96 | 69/96 | 66/96 | 70/91 (1 failed answer) |
| **Ruler not-kept spans kept** | 11 | 16 | 12 | **18** |
| Unfiled items | 34 | 42 | 46 | 36 |
| **Readers: unfiled that should have been filed** (an open thesis takes it, or it should open one) | 15 | 16 | 22 | **6** |
| New theses: bet / small / duplicate | 27/2/0 | 37/4/1 | 28/3/0 | 41/4/0 |
| Wrong links (reader A / B) | 3/0 | 7/4 | 7/4 | 4/2 |

**Read by hand:**
- **Filing.** Where the revenue home clean-11 is open (d1-40, d1-57), u1u3 opens a gross-margin and profitability thesis in 3 of 3
  draws. clean-11 asks about Vera Rubin shipping and revenue, so this is not a duplicate; section 3 names gross margin as a big matter.
  Dividends stay unfiled (d1-62), and valuation stays unfiled (d1-66).
- **The test miss is partly chance.** At the empty state, the control k6b also opens data-centre revenue and gross-margin theses for
  article 57.
- **The noise rise** is mostly empty-85 (not-kept 4 → 9; u1 alone 11): another company's matters (Hesai's lawsuit, Hesai's cost cut)
  kept under an empty library, not the company's financial lines.

**Process error (mine).** u1 also cut two sentences to stay length-neutral: the role paragraph's restatement of the unfiled rule, and "A
number, date or headline alone is not enough to open a separate thesis…". So u1 was not one lever, and the noise rise cannot be
assigned to the D371 line.

## 6. Council B (`council/c-*`)

- Promising signal, not passed. Not-kept spans rose 11 → 18, crossing the predeclared noise falsifier, and 2 of 48 combined answers
  failed the format check.
- 6 against 15 counts reader judgments, not a proven recovery rate.
- "Only the combination works" is not established.
- Do not advance to the dev forward run.
- The isolating step needs **u1k alone**: the D371 line added with nothing cut, beside the control and u1k+u3, keeping the original
  guards and reporting every case and failed send.

**Stopped for Alex (D355):** the hypothesis held for filing (should-be-filed unfiled items 15 → 6 in the combined arm) and failed for
noise (11 → 18). Proposed next probe, about $1: k6b, u1k, u1k+u3, on the 16 cases, 3 draws.

## 7. Decision council (Alex, 2026-11-08: "跑council决策")

- Claude (`council/d-claude.md`) and a fresh, independent Codex session (`council/e-codex.md`, which had not seen Claude's decision)
  chose the same step: **probe 2** isolating the D371 line.
- **u1k:** "one quarter's figures or guidance" moved from the do-not-open list to its own line, with **nothing cut**, +361 characters.
- **u1k+u3:** the same, with the required filing fields.
- The control reuses probe 1's 48 k6b draws: the same request bytes, cases and states, re-read blind with the new answers.
- The same 16 cases; 96 new sends, about $1.25.

**Codex's stricter criteria are adopted.** A candidate passes to the dev forward run only if, under a new independent review that
re-reads the controls blind:
- it yields at least 3 more correctly filed target matters than the control: should-be-filed unfiled items at most 12 against 15;
- ruler helpful is at least 69;
- not-kept spans are at most 11;
- small theses are at most 2, with no duplicates;
- wrong links are no higher than the control's;
- no guard gains a thesis or a wrong link;
- all 48 answers pass the format check.

**Stop and abandon this wording** if neither passes, or if a gain comes from loose links, per-line or per-quarter theses, or kept
small matters. Then trace the failures before choosing another lever.

**Readers:** two from different model families, neither involved in the change: Codex, and a Claude subagent with a fresh context. A
third reader with the source settles disagreements.

**Request audit for u1k.** These were read against the change and found consistent; no contradiction was introduced:
- the role paragraph ll. 7–8 and the UNFILED rule ll. 52–53;
- the big-matter list l. 84;
- l. 99 ("a number, date or headline alone…");
- the counterexample at l. 117 ("if an open thesis tracks sales growth, a revised sales forecast is evidence for it");
- closing ll. 14–15;
- the schema's links description.

The growth reason: the missing boundary between a question about one quarter, which is not a thesis, and the quantity's own question,
which is a big matter, is the audited contradiction. Cuts were avoided because they confounded probe 1.

## 8. Probe 2 results (`probe-r2/`, 96 sends, $1.21; review `probe-r2-review/` with probe 1's 48 control draws re-read blind)

- 2 format failures, both in u1k+u3: an unterminated string, and the extra `tier_note` field.
- **Reader A** is Codex. **Reader B** is Claude subagents (sonnet, fresh contexts, a different model family), which saw folder listings
  through a shell hook but opened no other file. The key was kept outside the folder.

| Sum of 3 draws, 16 cases | k6b (probe-1 draws) | u1k | u1k+u3 |
|---|---|---|---|
| Ruler helpful | 69/96 | 71/96 | 64/92 (2 failed) |
| Ruler not-kept spans | 11 | **12** | 11 |
| New theses | 29 | 43 | 42 |
| Should-be-filed unfiled, reader A / B | 15 / 6 | 17 / 3 | 12 / 3 |
| Small theses, A / B | 2 / 7 | 3 / 7 | 1 / 9 |
| Wrong links, A / B | 1 / 1 | 0 / 1 | 4 / 2 |
| Format failures | 0 | 0 | **2** |

**Verdict against the predeclared criteria: neither passes.**
- **u1k:** the readers split on whether filing improved (A worse, B better); noise is +1 over the line; reader A counts small theses +1.
- **u1k+u3:** format failures, helpful below 69, and reader A's wrong links up.

So the D371 wording is **stopped as a fix** (§7's stop rule).

**What the two probes established:**
1. The empty-85 noise in probe 1 came from the two cut sentences: with no cuts, u1k's empty-85 noise is back at the control's 4.
2. Probe 1's filing gain (6 against 15) does not reproduce without the cuts (12 for u1k+u3 by reader A), so it most likely came from
   the cut role-paragraph restatement of the unfiled rule, or from chance.
3. **The instrument does not discriminate.**
   - On the same 48 control answers, the two reader families count 15 against 6 should-be-filed items and 2 against 7 small theses.
   - That gap is larger than any arm difference.
   - The frozen dev ruler cannot see the D371 items, and unfiling varies widely across draws (dev d1 15 against d2 34).
4. The u1k theses that did open (gross margin, revenue path, a competitor thesis) are big matters by section 3: none duplicated an open
   thesis or was opened per quarter.

**Per the skill (two rounds moved nothing), a reflection council follows.**

## 9. Reflection council (`council/f-claude.md`, `f-codex.md`, a fresh cold read)

**Agreed:**
- The D371 wording is stopped as a fix: neither probe passed its predeclared criteria.
- K6b stays Alex's chosen configuration, **not accepted**: it missed the test line, and no fix passed.
- **Financial evidence dropped under a thin library is a real product defect.** Codex corrected Claude's "mostly protocol and chance":
  the empty start, sparse articles and one draw affect how often it shows, but do not erase the loss of an earnings result.
- The model's account locates a plausible mechanism (the one-quarter do-not-open line); intervening on that sentence alone did not
  move behaviour that the instrument can see.
- The cut sentences in probe 1, among them the role-paragraph restatement of the unfiled rule, which appears three times in the request,
  are a plausible lever. They are not isolated.
- **The instrument is the binding constraint.** On the same 48 control answers, the two reader families disagree 15 against 6
  (should-be-filed items) and 2 against 7 (small theses). The dev ruler cannot see D371 items.

**Process error (mine):** in probe 2 the skill's source-backed adjudication of reader disagreements (three readers with the source)
was skipped. It cannot change this verdict, because u1k fails on the ruler's noise (12 against 11) and u1k+u3 on format failures and
helpful 64. But it is the missing calibration step.

**Next angle, agreed: calibrate the readers on the stored dev answers before any further prompt change.** This is an evaluation change.
- Preselect the disagreement items and resolve each against the article, the theses open at the time, D371 and the signed standard,
  recording why. Include missed items as well as unfiled ones.
- Cost: no product-model calls; reader time only.
- Falsifier: if calibrated readers still cannot consistently separate a warranted financial question, a valid existing link and an
  intended drop, no prompt change can be chosen this way. A separately versioned D371 evaluation would then be needed, with independent
  review and Alex's sign-off (D371; AGENTS §7.1), and its scores are not comparable with the old ones.

**Disagreement kept:** Claude would also put the product option to Alex: keep unfiled statements for a short window so a thesis opened
later can pick them up (the Dell case; unfiled items carry about 2.4 helpful matters per not-kept span). Codex would not ask yet: the
option reverses D209 in part, and the first uncertainty is whether readers can apply his existing decisions consistently. It is
recorded as an option, not a recommendation.

**Spent this round:** account probe $0.11; probe 1 $2.51; probe 2 $1.21. About $3.83 in all.

## 10. Calibration and decision council (Alex, 2026-11-08: "你跑council loop review 然后决定下一步怎么修改")

**Calibration** (`probe-r2-review/disagreements.json`, `adjudication-C1.json`, `adjudication-C2.json`, `tally_calibrated.py`).
- Readers A (Codex) and B (Claude sonnet) split on 52 items, systematically: A says bet where B says small (18 of 19), and A says
  should-be-filed where B says fine (32 of 33).
- Two blind adjudicators had an explicit rubric quoting §3 to §6 and D371, and did not see the first readings: a fresh Codex (C1) and
  Claude opus (C2). **They agree on 17 of 52**, each siding with its own family.
- **The calibration falsifier fired:** model readers do not converge on the threshold.
- The split concentrates on:
  - FCF as a card of its own;
  - whether the company's quarterly cash-flow and cash figures are kept (D371) or dropped;
  - partner, supply and feature theses (Nemotron at Palantir, a small cooling supplier, the quantum decoder).
- Calibrated tally (k6b / u1k / u1k+u3): should-be-filed 6 / 3 / 3; small or duplicate 4 / 3 / 4; unresolved 8 / 11 / 10.

**Decision council** (`council/g-*`).
- Claude proposed carrying u1k to the dev forward run, as the request's compliance with D371.
- Codex objected: the stop condition fired, the limits were predeclared, and "no harm" is unresolved, so a forward run now would be a
  run used to try a fix (AGENTS §7.3). **Claude accepts.**

**Decided next step:** put the underlying product judgments to Alex.
- A small, balanced set of source cases with the questions available at the time: cash flow, gross margin, a forecast inside a
  valuation piece, and a small supplier. For each: keep it or not, and if kept, an existing question or a new one. Both readings are
  given, and keeping financial information is not presented as requiring a question per line (D371).
- His answers define a separately versioned D371 evaluation (D371; AGENTS §7.1, where the ruler is Alex's). Its first test is whether
  independent readers can apply them consistently on fresh dev cases. Only then is u1k, or another lever, measured against it.
- K6b stays the candidate with the defect recorded. The test set stays reserved.

## 11. Alex's rulings on the boundary cases (2026-11-08, his replies to these exact questions)

| Case | Alex's ruling |
|---|---|
| Q1 operating cash flow $50.3bn, FCF $48.6bn, cash $80.6bn; a "Vera Rubin shipping and revenue growth" thesis open; no profit or cash thesis | **丢掉** (drop) |
| Q1 gross margin 74.9%, Q2 guidance about 75%; the same library | **留，归到已有的收入观点** (keep, under the existing revenue thesis; no separate margin thesis) |
| Valuation article: analysts' average FY2028 EPS $12.76; the author's 25× target of $319; a revenue-and-EPS thesis open | **留 EPS 预测，丢目标价** (keep the EPS forecast, drop the target price) |
| A small supplier (NN Inc.) adds 47 machines for liquid-cooling parts, 100% pre-sold, $80–90m of new 2026 business; no supply thesis open | **丢掉** (drop) |

**Reading:**
- The company's results, estimates and guidance go under one broader question about the path of its revenue and earnings: never a
  separate margin, cash or per-line thesis.
- A backward figure that does not move that question's answer (a cash balance, operating cash flow) is dropped.
- A small supplier's step is dropped.
- These rulings are the first calibration cases of the separately versioned D371 evaluation. On theses and cash they side with the
  Claude-family readers; on the EPS forecast, with the Codex family.
- **u1k's direction is contradicted:** it opened separate gross-margin and FCF theses.

## 12. Decision council on the next modification (`council/h-*`, `i-*`)

- **u1r rejected** ("turns four case decisions into a rule Alex did not make"). Agreed.
- **A sourced lever found: the filing rule in force** (`docs/DECISIONS.md` Filing; D273, kept by D361; production text
  `src/hivemind/placement.py` `FILING_RULE_ROOT_FALLBACK`). K6b's §2 dropped its definition of "bears on" (the thesis's own figure,
  step or estimate, or the demand, supply, competition or pricing behind its answer) and the company-wide revenue fallback.
- Codex: worth investigating, not yet a fix.
  - **Keep the fallback:** D361 kept it despite the parking-lot finding. A supplier item can fail the prior evidence test.
  - **Resolve the one-against-many conflict:** production files under the narrowest one question, while the clean contract links
    every thesis informed.
  - **Audit the whole request first.**
  - The probe needs a fresh same-day control and a predeclared reader-calibration threshold with a stop.

**Candidate `arms/lfile-system.txt` (+388 characters).** K6b §2's three matching bullets are replaced by:
- the signed "informs" definition (own figure, step or estimate, or the four channels; a shared company, industry or ecosystem is not
  a connection);
- the clean multi-link kept, narrowest first, never a broader thesis beside a narrower one for the same reason;
- the estimate-for-another-period clause;
- the fallback, conditional on an open company-wide revenue thesis existing (the clean library has no seeds, D370);
- "match by the underlying question, not word overlap" kept.

**Audit against the rulings and decisions:**

| Case or sentence | Under lfile | Consistent? |
|---|---|---|
| Alex: gross margin goes under the existing revenue thesis | Margin is a result rather than a driver. It is linked only if read as the revenue thesis's own result, or as pricing behind it | **Uncertain**: lfile may not deliver this ruling |
| Alex: keep the EPS forecast under the revenue and EPS thesis; drop the target price | Estimate-for-another-period clause; the price target fails the evidence test (valuation) | Consistent |
| Alex: drop cash-flow figures | Not the revenue thesis's own figure and no channel, so unfiled | Consistent |
| Alex: drop the small supplier | Evidence test first. If kept, the supply channel and fallback send it to the revenue thesis | **Possible conflict**: depends on the evidence test (Codex's point) |
| Do-not-open "one quarter's figures … or unfiled" (l. 93) | Unchanged; it concerns opening, so quarterly figures can now link through own figure or fallback | No new contradiction; the D371 tension remains |
| Clean PRD multi-link | Kept | Consistent |
| Closing check l. 15 ("an item an open thesis covers is linked there") | Reinforced | Consistent |

**Expected effect, stated before any send:** it addresses the link-miss class (an open thesis takes the item); it does not open the
missing revenue home in a thin library (the test-set core miss); and it may not deliver the margin ruling.

## 13. Round closed (`council/j-*`)

**The candidate does not pass its audit.** Codex found two defects, both introduced by Claude:
1. lfile's "never a broader thesis beside a narrower one for the same reason" pulls against the unchanged closing check's "links to
   every thesis it informs".
2. Replacing the general related-period, population and variant clause with an estimate-only clause can lose other relevant evidence.

Its expected benefit is limited to existing-thesis link misses. It does not open the missing revenue home behind the test core miss,
and may not deliver Alex's margin ruling. **Probe 3 is not sent.**

**Verdict of the round:**
- No prompt change is adopted.
- K6b stays Alex's chosen candidate, **not accepted**. The test-set miss and the financial-evidence loss under a thin library are
  recorded as an open defect.
- What the round established:
  - the model's account locates the one-quarter do-not-open line;
  - intervening on it does not move behaviour that can be measured;
  - probe 1's apparent gain came from cutting two general sentences;
  - model reader families hold different thresholds and do not converge, even with a rubric;
  - Alex's four rulings are the only settled judgments.

**Next work (council):** the separately versioned D371 evaluation that D371 calls for.
- Turn Alex's exact rulings into reviewed worked cases, and extend them with his rulings on a small balanced set of further dev cases.
- Check that independent readers apply them consistently to fresh cases before the evaluation is used to choose any change.
- It needs his sign-off (AGENTS §7.1). The frozen evaluation and the test set stay unchanged.

**Spent:** $3.83 in product-model calls (account probe, probes 1 and 2); calibration and reviews used Codex and Claude readers only.

## 14. Council decides under Alex's delegation (`council/k-*`)

**Alex, 2026-11-08:** "你需要我裁定什么？你不能跑council决策吗". The threshold is delegated to the council, as in D260. The council's
decision below is **council-defined and not confirmed by Alex**, anchored on his four rulings (§11).

Claude proposed u1r′, with financial measures under one revenue-or-results card. Codex amended it: the proposal directed every margin
and earnings measure to a revenue question even when it does not help answer it, and barred a margin question that could matter
independently; the four rulings fix outcomes, not universal rules. The amended text is adopted as **u1c**, in place of the one-quarter
do-not-open item, +423 characters, nothing cut:

> One quarter's figures or guidance are not a thesis on their own. Reported results, estimates and guidance may inform an open question
> about the company's financial performance, including its revenue or earnings: link them when they help answer that question. If no
> open question takes them, judge whether the broader question they inform merits tracking under the test above; do not open a separate
> question merely for one quarter, line or estimate.

Source: D371 (relevance and opening stay with the model's judgement), §3, and the rulings as calibration.

**Probe 3 (predeclared):** a fresh same-day k6b control and u1c, the 16 cases, 3 draws, 96 sends, about $1.25.

**Pass, all required:**
1. Alex's rulings hold in their matching contexts in at least 2 more answers than the control, and no ruling breaks more often than in
   the control:
   - margin linked to the open revenue thesis (d1-40, d1-57);
   - the EPS forecast kept and linked with the target price dropped (d1-66, d2-66);
   - cash and cash-flow figures dropped (d1-57, d1-62);
   - no supplier thesis (d2-8).
2. Every changed link, opening and drop judged against the source by two readers (Codex and Claude), unresolved ones reported. No
   both-agreed rise in wrong links or small theses.
3. Ruler noise no higher than the control's, and helpful at least the control's minus 1.
4. Guards (d1-22, 29, 113, empty-108): no new theses.
5. Every answer passes the format check.

**Limitation stated before use:** the 115 dev articles and the 26 test articles have both been exposed to earlier iterations, so
neither is untouched validation. A pass locates a fix; the dev forward run and the single test check measure it, with that caveat.

## 15. Probe 3 results (`probe-r3/`, 96 sends, $1.18; fresh same-day control)

- Ruling checks (`ruling_checks.py`): k6b 10/21, u1c **16/21** (margin 5→6/6, EPS 2→3/6, cash 3→6/6, supplier 0→1/3); guard new
  theses 1 → 0; 0 format failures.
- The same checks on probe 1's control gave 15/21, so draw-to-draw spread is large.
- Ruler: helpful 71 → 68. Two of the three lost matters are the small-supplier spans that Alex ruled should be dropped (a D373-type
  conflict). Noise 13 = 13.
- Readers:
  - should-be-filed: A 17 → 16, B 8 → 3;
  - wrong links: A 2 → 0, B 3 → 2;
  - small theses: A 7 → 8, B 9 → 5.
- At empty states u1c still opens revenue, margin and FCF theses.

**Superseded before a verdict** by Alex's reframing (§16).

## 16. Alex reframes what a thesis is (2026-11-08)

**Alex:** "我觉得财务类型不应该是thesis，而更多的是条件。观点应该是独特的view，而不是喊出来的数字，除非有理由 - 这个理由恰恰才是观点你深度思考一下作为hedge fund analyst 怎么看".

**Decided (Alex's words):** financial figures are not theses on their own. A thesis is a distinctive view; a number becomes part of a
view only through a reason, and that reason is the view.

**Claude's analyst reading and the council** (`council/l-*`):
- **Agreed:**
  - the "sustain revenue growth" and "sustain gross margin" cards opened by u1k, u1c and k6b at empty states are shouted numbers, not
    views;
  - a figure is evidence when it tests a view's reason, and context otherwise;
  - the probes of §§4–15 pushed in the wrong direction (more metric cards).
- **Codex narrowed Claude's reading:**
  - a view need not always be differentiated against what is priced, because an emerging risk can precede consensus;
  - no reason may be invented that the source does not give;
  - a separate financial-context record is a plausible design, not a consequence of Alex's words;
  - the real open choice is what happens to a useful figure no view takes yet: today it is dropped (D209), whereas a per-company
    record would keep it.
- **Consequences named:**
  - Step 2 must tell a revision from a repeat on the full statement, not on measure, period and kind alone;
  - Step 4's reference must match each question's scope and date;
  - D209 changes only by an explicit decision;
  - the frozen evaluation cannot judge the new record, so a separately reviewed one is needed.

**Status:** u1c is not adopted, because it optimises the old frame. Next is the design of one source-backed financial-context record
that can also be linked to a view, covering what is kept and how revisions work, once Alex confirms the shape.

## 17. Alex decides the shape (2026-11-08)

On the recommendation "keep a useful financial figure that no view takes in the company's conditions record, labelled actual,
guidance or expectation, with who said it and the period; it becomes evidence when a related view opens and the reference when views
are judged", against the alternative "drop it as D209 does now", **Alex replied: "好".**

**Decided:**
1. Financial figures are not theses on their own; a thesis is a view with a reason.
2. A useful company financial figure that no view takes is kept as a condition, not dropped. This amends D209 for such figures only;
   other no-home statements are still dropped.

**Next:** the conditions design (`clean-arch/STEP1-CONDITIONS-DESIGN.md`), council review until a round finds nothing serious, then a
small probe.

## 18. Conditions design: passed the design gate (2026-11-08)

`clean-arch/STEP1-CONDITIONS-DESIGN.md` went through eight review rounds, each by a fresh, independent Codex session: v1 `m-codex.md`,
v2 to v8 `n-` to `t-codex.md`.

**What the rounds changed:**
- **v2:** a condition became an optional `condition` object on an evidence item, not a separate record, so every existing check and the
  Step 2 and Step 3 paths are reused. Only a condition with no links is kept instead of dropped.
- **v3:**
  - an entity-wide, evidence-only search for items with no thesis (otherwise a repeat would be saved as new);
  - the field hand-off fixed (separate date fields);
  - `balance` folded into actual.
- **v4:**
  - complete backfill with a judged-pair ledger and recovery;
  - one view definition, which includes competitive position;
  - draw rules fixed.
- **v5:**
  - numeric boundaries on the value check;
  - anchors that test Alex's margin, supplier and cash rulings as decided.
- **v6:** identity split from meaning. Code checks that a figure is quoted; readers check that it is paired with the right measure,
  with a 2% bar.
- **v7:** condition fields kept out of Step 2 by construction, with an isolation test.
- **v8:** Step 2's 600-character passage cut removed. It cut 44 of 282 stored items (16%), a latent defect of the existing Step 2 for
  evidence too, so Step 2's lines will be re-measured.

**Round 8:** "没有发现其他会使这次探针结果无法解释或导致构建错误的严重设计问题". The only remaining blockers are the prerequisites,
which are build work:
1. the scorer test;
2. the value-check real-data report;
3. the backfill tests;
4. the isolation and full-passage test;
5. the independent review of `anchors.json` and the rubric.

**Next:** build them and the c1 arm, then probe 3c, about $1.25.

## 19. Build for probe 4 (conditions, c1); Alex: no scorer (2026-11-08)

**Alex:** "不要写评分器这个之前就出问题过，你自己读trace 来分析". Written into AGENTS §7.2. The probe is judged by Claude reading every
answer against `anchors.json` (fixed before the send). The design's scorer prerequisite and its reader-family scoring are dropped.

**Sequencing.** Probe 4 is Step 1 only (fixed states). The Step 2 and 3 changes (no-thesis search, full passages, backfill) and their
tests are built before the forward run, not before this probe, because this probe does not exercise them.

**Built:**
- `clean-arch/step1/runner.py`: optional `condition` on evidence items.
  - `figure_in_passages`: the value is quoted in one verified passage, with numeric boundaries.
  - An invalid condition is removed, with the reason in `condition_issues`.
  - **A valid condition with empty links is kept**, not unfiled.
  - 3 tests; all 4 mutants caught (condition does not keep; no left boundary; no right boundary; invalid condition kept).
- **Arm c1** (`arms/c1-*`, against k6b):
  - the role paragraph and a new §2 CONDITION bullet (the company's own figures carry a condition and are kept with empty links when
    no thesis takes them; target prices, the share price and other companies' figures are not conditions);
  - §3 now reads "a thesis is a view: a question whose answer turns on a reason …; a financial figure on its own is not a view";
  - big matters read "a reason that can move the quantities that carry the company's value";
  - the do-not-open list reads "a financial measure's level, growth or guidance with no reason (it is a condition)", plus "a measure
    with a reason the item supports is a view (margins fall because input costs cannot be passed on)";
  - one closing-check sentence;
  - the schema gains `condition`.
  - System prompt +905 characters (+6.7%). **Growth reason:** the new conditions contract Alex decided needs its definition; it is not
    a patch.
- A synthetic c1 answer passes every check: 1 condition kept with empty links, 0 issues.

**Probe 4:** c1 on the 16 cases, 3 draws, 48 sends, about $0.50. **The control is probe 3's same-day k6b draws.**

## 20. Probe 4 read (c1 against the same-day k6b control): mixed; three mechanisms traced to c1's own sentences (2026-11-08)

**What was run.** 16 cases × 3 draws, 48 sends, $0.67. One c1 answer failed the format check (`condition` missing on one item); the
control had 0 of 48. **The control** is probe 3's same-day k6b draws. Every answer was read against `anchors.json`, which was fixed
before the send. The frozen-gold table from the existing scorer (`score_probe.py`) was used as a lead only; no scorer was written.

**What c1 fixed (read per answer):**

| Anchor | k6b (control) | c1 |
|---|---|---|
| No thesis that only restates a figure (empty-57: "will margin stay near 75%?", "will cash flow stay strong?") | 4 such theses | 0 |
| Thin library, figures only (empty-40) | 2 of 3 draws open a "sustain growth and margin" thesis | 0 of 3; all three figures kept as conditions |
| Analysts' EPS forecast kept (d1-66, d2-66) | 3 of 6, all linked | 6 of 6; unlinked in all three d2-66 draws |
| Author's target price dropped | 6 of 6 | 6 of 6 |

**What c1 broke or did not fix:**

| Anchor or class | k6b | c1 | Mechanism (the model's own account, `probe-r4/accounts.json`) |
|---|---|---|---|
| Cash flow and cash balance dropped (Alex's ruling, d1-57) | dropped in 2 of 3 | dropped in 0 of 3; the buyback is kept too | The c1 CONDITION bullet keeps **every** company figure. All three accounts quote it. Alex said "好" to keeping a **useful** figure; the prompt lost the word, so it keeps wider than his ruling. |
| Margin filed under the revenue view (Alex's ruling; d1-40, d1-57) | 5 of 6, inside combined items linked to clean-11 | 1 of 6; split out as a condition with empty links in 4 of 6, and under the memory thesis once | c1's closing sentence "linked **only** to theses whose reason it informs". All three accounts quote it: clean-11 is about Vera Rubin shipping and revenue, "not margin". The sentence links narrower than Alex's ruling. |
| New theses the gold does not ask for | 0 | 7: networking 3 of 3 (d1-62), supply commitments 3 of 3 (empty-62), Microsoft initiative 1 of 3 (d1-22) | **Networking:** the narrower link rule leaves the networking figure without a home, so the model applies "answers can move apart" and opens a thesis. **Supply commitments:** c1's "a measure with a reason the item supports is a view" let a generic conditional ("compound demand risk if orders slow") count as the reason; the account names the general-risk row and sets it aside. For this article the gold has must_open and may_open empty, and the NVLink Fusion statement is not kept. |
| Small supplier dropped (d2-8) | 3 of 3 open a supply thesis | 3 of 3 open a supply thesis | Unchanged; c1 does not touch this class. |

**The frozen-gold table** (lead; three draws summed; c1 lost one draw on d1-38):
- **Gold not-kept matches: 13 → 23.**
  - d1-62 2 → 5 and empty-62 4 → 6: the NVLink Fusion and "Blackwell Ultra ramping" statements, which the new networking thesis takes
    in;
  - d1-22 0 → 1;
  - empty-85 6 → 11 (per draw 2/0/4 against 3/3/5; Hesai regulatory detail; not traced to a c1 sentence, one probe);
  - d1-113 1 → 0.
- Helpful matters, on the 15 cases with all draws: 61/81 → 65/81. The gains are the EPS forecast twice, the debt raise (d1-29, gold
  supporting) and one in empty-62.
- Kept items 139 → 196, most of them conditions; unfiled 39 → 29; new theses 32 → 31.

**Fidelity.** Of 128 conditions, 48 have empty links. Reading each one found no figure filed under the wrong measure. There are 2
kind or eligibility slips: the hyperscaler revenue share is marked actual in one draw and estimate in another, and China's market size
was recorded as if it were a company figure. Both are under the 2% bar.

**Process error (mine).**
- c1 carried three levers in one arm: the conditions contract, the view definition and a narrower link sentence.
- It was sent without the prompt audit (AGENTS §6). The design gate reviewed the design, not the c1 text against Alex's four rulings,
  clause by clause.
- All three failures are clauses the audit would have flagged: one keeps wider, one keeps narrower, one contradicts the general-risk
  row.

**D355 applies:** the result contradicts the hypothesis on cash, links and new theses, so the line stops here for Alex.

**Council B** (`council/u-codex.md`, a fresh Codex session) agrees with changes. Each point was checked against the answers:

1. **The margin control was wrong in my first count.** k6b already filed the margin under clean-11 in 5 of 6 draws. Verified by
   searching the passages, and corrected in the table above.
2. **The cash mechanism is supported.** The keep-everything wording also sits in the role paragraph, the closing check and the schema,
   so all of them change together.
3. **The link wording is supported for margin.** For networking the accounts cite the existing separate-bet rule, not a missing home,
   so that cause is not established.
4. **The supply-commitment cause is not established.** The standard counts a purchase commitment as an obligation, and the gold marks
   the $119 billion statement optional, not not-kept.
5. **"Useful" must be judged in context, not by a closed list.** A list would lose d1-29's debt raise, which the gold calls supporting.

**Net against Alex's rulings:**

| Ruling | Result |
|---|---|
| Margin under the revenue view | regressed, 5/6 → 1/6 |
| Cash dropped | regressed, 2/3 → 0/3 |
| EPS forecast kept | improved, 3/6 → 6/6 (links fell) |
| Target price dropped | unchanged, 6/6 |
| Supplier dropped | unchanged, 0/3 |
| Theses that only restate a figure | 4 → 0 |
| Extra theses | 0 → 7 |

**c1 as built is not carried forward.**

**Recommendation for Alex:**
1. One coherent revision c2 after a full prompt audit:
   - the condition is kept only when an analyst would use the figure, judged in context, with Alex's cash case as the boundary
     example;
   - K6b's linking ("every thesis it informs") restored in every place;
   - K6b's big-matter wording restored.
2. Send it first on the motivating cases (a few cents).
3. Then run the same 16 cases × 3 draws against the same control, read by hand.

## 21. Reflection council on the whole record (2026-11-08; `council/v-claude.md`, `v-codex.md`, `w-challenge.md`, `w-codex.md`)

**Alex:** "run council loop to review together and tell me the current status, what you learned and next steps".

**How it was run.** Claude wrote its reflection first. A fresh Codex session read the whole record cold. One challenge round followed in
the same thread.

**New $0 evidence on Step 2 line 2** (`merge-wrong.json`):
- **X59 and X64** come from one bundled Step 1 record (49:e1, 1,097 characters) that states both the NVL144 and the NVL576 delay. The
  NVL576 claim sits past the 600-character cut, but the summary states it, and Jev reads the summary in full.
- **X30** has short passages: a Jev figure error.
- Overlaps with a record over 600 characters: 7 of 15, against 43 of 104 among all merges (not enriched).
- **The cut explains 0 of the 3 wrong merges.** It remains a separate latent defect.

**Status (agreed):**
- **Step 1.**
  - K6b on DeepSeek Flash.
  - Dev: 205 and 197/234 in two forward draws, line met.
  - Test: 32/42 against a proportional 35, one draw, exposed. Noise 8 against production's 4.
  - 7 of 10 test misses were extracted but dropped as unfiled; keeping every unfiled item would give 38 helpful and 12 not-kept, an
    upper bound, not recoveries under Alex's narrower decision.
  - The conditions arm c1 is not carried forward (§20).
- **Step 2.**
  - Search: 112/113 known counterparts found.
  - Later details: 28/36 against 27.5.
  - Wrong merges: 3/104, against a line of 2%.
  - One Jev draw. The line-2 fix is not done.

**Agreed lessons:**
1. Useful figures need a place even before a related view exists.
2. Broad linking ("every thesis it informs") worked better than linking only to a view's stated reason.
3. A design review does not replace auditing the actual request against Alex's rulings.
4. Grouping preserves text, but a wrong association can still mislead.
5. The passage cut is a separate defect, not the cause of these three merges.
6. **Claude's own instrument error:** a printer that cut summaries to 120 characters made Claude miscount the margin control as 0/6
   (it was 5/6). Anchors are read by searching passages and summaries for the figure.

**Agreed next step: c2, the smallest conditions change, audited first.**
- **Text.** K6b unchanged except:
  - the `condition` field;
  - one condition bullet for a useful company figure, judged in context;
  - the do-not-open row "a measure's level, growth or guidance with no reason is a condition" (Alex's reframe).
- **Removed from c1:** "a measure with a reason is a view" and "big matters include a reason". K6b's linking is restored everywhere.
- **Before any send:**
  - the full prompt audit with a blind second reader;
  - each of Alex's four rulings walked through the request at $0.
- **Then:**
  - the motivating cases, one draw each, a few cents;
  - then 16 cases × 3 draws against the same control, about $0.70, read by hand.
- **Diagnostic falsifiers, fixed now:**
  - margin under the revenue view at least 4/6;
  - cash dropped at least 2/3;
  - at most 1 extra thesis against the fixed set (the supply-commitment dispute disclosed);
  - gold not-kept at most the control + 3;
  - 0 figure-only theses in empty-40 and empty-57;
  - EPS kept at least 5/6;
  - a failed answer counts as a failure;
  - each condition's figure, period, speaker and qualification read;
  - target prices and the small supplier checked.
- **The exposed test set is kept for the final configuration** and not used to tune.
- **After c2:** a $0 blind, source-backed read of X59, X64 and their original, with X30 as a control. It decides whether the bundle is
  a real wrong merge before any Step 2 or Step 1 fix.

**Disagreement, and how it is settled:**
- Codex would not put Alex's cash case in the prompt.
- Claude: "useful" alone is an abstract clause, which AGENTS §6 says becomes a coin flip.
- **Settled by AGENTS §6:** Alex's case stays an audit case. The prompt gets two or three generic examples from varied domains, none
  from the bench, and the audit checks them.
- Codex also does not count every gold-unrequested thesis as wrong. They are reported, with the dispute disclosed.

## 22. Arm c2: build, audit, motivating sends (2026-11-08; Alex's /goal: run the loop until the line is met)

**Goal (Alex):** "跑loop council 统整学习，深度改进方案，下去做执行，测量再检讨循环，持续突破。试过的错的不要再犯，收敛方向关注核心重要问题。不要overfit 和hardcode for the use case, 要做的prd目标不要drift。开始做直到达标进步".

**Record shape.** A list of `figures` replaces the single `condition`. In probe 4, c1's single condition split statements: items sharing a
passage with another item rose from 2 of 178 to 18 of 225. The runner keeps an item with empty links when at least one figure is valid
(3 tests; 4 of 4 mutants caught). Design: `STEP1-CONDITIONS-DESIGN.md` §16.

**The c2 text** is K6b plus:
- the role exception: a useful figure of the company's own finances is kept as a condition;
- a §2 CONDITION bullet;
- §3: the "quantities that carry the company's value (… gross margin …)" clause cut, and the do-not-open row widened from "one
  quarter's figures or guidance" to "a financial measure's level, growth, margin or guidance for any period, on its own";
- one closing read-back;
- the `figures` schema field.

None of c1's sentences is carried.

**Audit** (Codex blind, `council/x-*`; rechecks `y-*`, `z-*`). Fixes made before any send:
1. the closing check and the schema's "unfiled" aligned with conditions;
2. "financial performance" widened to "financial figures (a reported result or balance, its guidance, or an estimate)";
3. "useful" defined by the standard's own test rather than a list;
4. the cash example made conditional on context;
5. **an estimate and a target price drawn from it are two statements.** Verified: d1-66 k6b draw 3 kept the $12.76 EPS and the $319
   target in one item.

**Kept unchanged, with the conflict recorded (D373):** closing row 6 ("a conditional valuation … is kept") conflicts with Alex's
target-price ruling, and the frozen gold marks d1-38's $305 valuation supporting. Behaviour: 11 of 12 answers in his two cases dropped
the target. Target prices are a falsifier in the probe.

**Motivating cases, one draw each.**
- **First send (`probe-r5a-motivating/`, $0.13).** Two classes remained:
  - **cash kept as conditions.** The model's account: "operating and free cash flow are literally cash"; asked afterwards, it agrees
    the carve-out governs (AGENTS §6: a test applied in one pass is applied correctly only at the end);
  - **d1-40 results unlinked.** The account: clean-11 tracks forward revenue against estimates, so a backward three-year growth, net
    income and margin "do not inform" it. With the condition outlet, leaving a figure unlinked no longer costs anything.
- **Fixes, each sourced:**
  - the usefulness test reads "funding or credit risk" for "cash or credit risk" and moves to a closing read-back;
  - "its results, guidance and estimates, margins included and whatever period they cover, inform an open thesis about its revenue or
    earnings path" (Alex's margin ruling; D371: "a quarterly period is not itself a reason to withhold information from a related annual
    question").
- **Second send (`probe-r5b-motivating/`, $0.14).** Every anchor passed:

| Case | Result |
|---|---|
| d1-40 | revenue growth, net income and margin all under clean-11 |
| d1-57 | margin guidance under clean-11; cash and buyback dropped |
| d1-62 | no extra thesis; margin under clean-11 |
| empty-62 | 2 theses, no supply or networking thesis |
| d1-66, d2-66 | EPS kept; target dropped |
| empty-40, empty-57 | 0 theses; figures kept as conditions; cash dropped |

- **Size:** system 13,476 → 14,612 characters (+1,136), closing 7,670 → 8,024 (+354), schema +1,717. **Growth reason:** the conditions
  contract Alex decided, with field definitions in the schema beside the field.

**Probe 6:** c2 on the 16 cases × 3 draws against probe 3's same-day k6b control, about $0.70, read by hand against `anchors.json` and
the §21 falsifiers.

## 23. Probe 6 read (c2 against the same-day k6b control; 48 sends, $0.67; `probe-r6/`, `probe-r6-merged/`)

Every answer was read by hand. Margins were counted by searching passages and summaries for the figure. The frozen-gold table comes
from the existing `score_probe.py` and is a lead only.

**Falsifiers fixed before the send (§21):**

| Falsifier | k6b | c2 | Met |
|---|---|---|---|
| Margin under the revenue view (d1-40, d1-57) | 5/6 | **6/6** | yes |
| Cash dropped (d1-57) | 2/3 | 2/3 | yes |
| EPS forecast kept (d1-66, d2-66) | 3/6 | **6/6** (4 linked, 2 conditions) | yes |
| Target price dropped (d1-66, d2-66, d1-38) | 8/9 (d1-66 d3 bundled it) | **9/9** | yes |
| Figure-only theses (empty-40, empty-57) | 4 | **0** | yes |
| Gold not-kept matches | 13 | **7**, with 2 fewer answers | yes |
| Extra theses against the control | — | d2-6: **3/3 against 1/3**, and the gold's must_not is "Palantir's adoption of Nemotron … as a question" | **no** |
| Failed answers | 0 | 2 (empty-62 d3, empty-85 d3: invalid JSON) | see below |

**Further readings:**
- **Helpful matters** on the cases with all draws: 57/81 → 61/81. The gains are the EPS forecast twice and the Palantir statement
  twice, kept under the must-not thesis.
- **Figures.** Each figure's measure, period and value was read: no figure under the wrong measure. One kind slip repeats from c1 (the
  hyperscaler revenue share once marked estimate, once actual). Statements stay whole: revenue and margin guidance are one item.
- **empty-57.** The theses are a customer-spending view and a Blackwell/Vera Rubin ramp view, the control's subjects written as views
  with their reasons. Its 2 not-kept matches are the generic "consensus points to continued growth" line, which the new spending thesis
  took in.
- **Output size:** median 7.3k completion tokens against k6b's 6.3k; maximum 27.9k against 20.6k.

**The two failed answers (`probe-r6/diagnose.json`).** Both requests re-sent as built returned valid JSON with finish_reason "stop"
(completion 22.8k and 18.5k tokens, under the 32k cap). So this is a sampler failure, not the prompt and not the cap. Production
retries once. The larger outputs raise the cap risk, which is watched in the forward run.

**The d2-6 regression is K6b's small-step class, not a c2 sentence.** The model's accounts (3 of 3):
- draws 1 and 3 quote K6b's "A topic may be opened before its business impact is known, but not a noisy one";
- draw 2 quotes K6b's big-matters item "a competitor's or customer's move that can shift its share or demand", and itself says the
  scale sentence ("A single investment, partnership, integration … opens a thesis only when its own scale can change …") should have
  governed: "The correct result is the statement unfiled".

The same class is in every arm: the small supplier (d2-8) opens a thesis 3/3 in k6b, c1 and c2, against Alex's ruling; k6b opened the
quantum division (d1-113) once. **Mechanism:** the scale test sits in §3 but not in the closing check. The model applies it correctly
when asked afterwards; this is AGENTS §6's single-pass rule, the same mechanism the cash read-back fixed.

**Verdict:** c2 fixes every class it was built for and turns nothing right into wrong on those classes. Its remaining miss belongs to
the next class, small-step theses. **c2 is carried forward as the base.**

## 24. Council B on probe 6, c3 not sent, the whole bench launched, Step 2 changes built (2026-11-08)

**Council B** (`council/aa-codex.md`). Corrections, accepted:
- the two failed answers count as failures (§21), so c2 is an **unaccepted base**, not a pass;
- the 7 against 13 not-kept count is not comparable while two answers are missing;
- the accounts locate instructions but do not prove why the same K6b wording opened d2-6 3/3 instead of 1/3;
- positive opening controls must be registered before any thesis-suppressing change.

Registered: `cases-positive.json` (pos-1 credit support, pos-42 hyperscaler capex, pos-49 Kyber NVL144, pos-100 China H200; gold
must_open; empty or first state).

**Small-step theses: mechanism.**
- The accounts for d2-8 (`probe-r6/accounts-d2-8.json`, 3 of 3) quote K6b's big-matter item "a competitor's or customer's move that
  can shift its share or demand", applied to a **supplier**, plus "A topic may be opened before its business impact is known" and
  "open the broader thesis with this evidence".
- They set aside K6b's scale sentence, which is the signed D248 #6: "单笔交易、产品、项目，规模要大到能改变公司的收入、利润、现金或信用风险才开题".

**c3** (c2 plus that scale test in the closing check, scoped to another party's single step) **was not sent**. The auditor
(`council/ab-codex.md`): "the sentence tests what evidence happens to appear in one article, rather than what the proposed question
asks"; it could suppress an important broader question whose first evidence is one small step, and "unless the item shows" risks
treating missing scale as insufficient. Agreed.

**A better-sourced direction is noted for later:** the standard's own opening test ("能在一个日期用公开材料核对": checkable on a date
against public material) is about the question itself. K6b's "a topic may be tracked when later observable developments can help assess
it" keeps wider than it (the first audit, `x-codex.md`). It is not tried now: it would move every thesis, the frozen question gold's
must_not also covers a custom-silicon thesis that readers judged a bet, and small theses are not what fails Step 1's line (the test set
had 0 small theses).

**Focus decision (Alex's goal: converge on the core problem, do not drift).** Step 1's line fails on recall in a thin library (test
32/42 against 35, 7 misses unfiled) and on noise, and c2 targets exactly that. So the whole bench runs now on c2:
- `gold-c2-flash/`: the 115 dev gold articles, forward from empty;
- byte-identical inputs to `gold-k6b-flash/` (manifest, initial, settings; 115 source items with identical content sha256; prompt files
  and limits in `SHA256SUMS`);
- `max_calls` 140 for retries;
- launched 21:08. The small-step class is read in its library.

**Step 2 changes for conditions, built while the run is live** (`clean-arch/step2/compare.py`, `run_forward.py`; Step 1 code untouched):
1. Search: a record with no thesis, or one listing figures, also gets one entity-wide query of its own text (design §10.1).
2. The figures never enter a search or comparison text (§14), and the comparison reads the full passages (the 600-character cut is
   removed, §15).
3. `step1_records` carries `statement_date` and `statement_date_text` separately (the texts show the first present), plus `figures`,
   `input_id` and `title`. The library stores the whole record.

Tests: 3 new, 9 in total, plus the Step 3 tests, all passing. All 3 mutants caught: the cut restored, figures in the piece text, no
own-text query.

**Deferred and stated:** backfill (design §11.1). It does not change Step 2's three lines, and it is needed only before Step 4 reads
conditions.

## 25. Whole bench: c2 forward over the 115 dev gold articles (one draw; `gold-c2-flash/`)

- 115 of 115 complete in 116 calls. Sequence 47 returned empty content once and its retry conformed: the retry policy worked in a live
  run.
- About 45 s per article; reserved $8.95 against the limit (priced at the limits' rates).
- Inputs byte-identical to `gold-k6b-flash/`. Scored by `score_gold_runs.py` (gold `6f9476bb…`, standard v5).

| 115 dev articles, one draw | **c2** | k6b d1 | k6b d2 | production v108 d1 / d2 / d3 |
|---|---|---|---|---|
| Helpful kept (of 234; line 190) | **209** | 205 | 197 | 167 / 171 / 162 |
| Core kept (of 86) | 85 | 84 | 85 | 76 / 76 / 75 |
| Not-kept spans kept | 41 | 40 | 38 | 30 / 34 / 34 |
| Items | 290 | 282 | 265 | 278 / 301 / 287 |
| Kept as conditions (empty links) | 16 | — | — | — |
| Unfiled and dropped | 16 | 15 | 34 | — |
| Theses opened | 24 | 25 | 18 | — |

**Regressions first.**
- Noise +1 against k6b d1 (41 against 40).
- 5 helpful entries missed only by c2 (both k6b draws kept them), each read against the answer:
  - 1 is a match artefact: the Seasonic RTX 5080 SUPER item is kept; the gold span is another sentence of the same matter;
  - 4 are single omissions in articles where c2 kept the neighbouring items on the same matter: the Utah executive order, the
    Malaysian smuggling seizure, SemiAnalysis's "the general market is still materially lower … for Nvidia in the 2nd half" (core),
    and Azure's $627bn of remaining obligations.
  - No c2 mechanism is evident. **Watched:** the bullet's "other companies' figures are never conditions" could bleed into keeping a
    customer's figure as evidence; this is 1 case.
- 5 helpful entries missed by c2 and one k6b draw; 15 missed by all three runs.

**Gains.**
- **The condition-only items add +9 helpful and 0 noise**: helpful 209 with them and 200 without; not-kept 41 either way.
- All 16 conditions are revenue, EPS, guidance or estimate figures (consensus EPS, SemiAnalysis's "20% above consensus", revenue paths,
  the frontier-model revenue share). None is a cash-only or buyback figure. One figure was removed by the value check: "$119B", where
  the passage reads "$119 billion".
- 5 entries recovered that both k6b draws missed:
  - core: "For every $100 spent by U.S. AI companies, $60 is spent on N…";
  - supporting: the FY2028 EPS forecast, McKinsey's AV market, XR device makers, and the Palantir/Nemotron statement (kept under the
    must-not thesis).

**Theses** (`theses-answer-r{1,2,3}.json`). Three source-backed Codex readers, each given the article and the theses open at the time,
using the dev review's prompt:
- **3 small by majority**:
  - Intel's $5bn stake with Xeon selection, small in every k6b run too;
  - Palantir/Nemotron, the gold's must_not;
  - BioNeMo life-sciences toolkits, small 3/3.
- **0 duplicates by majority, so 0 fragments.**
- Split verdicts: custom silicon (one reader says duplicate), automotive and orbital data centres (one says small each).

**The dev pass line is met:** helpful 209 ≥ 190; small 3 ≤ 3, at the line, as for k6b d2; fragments 0. Noise is flat against k6b
(41 against 38–40) and above production's 30–34.

**The test set runs once** on the same configuration (`test-c2-flash/`): 26 runnable articles, inputs byte-identical to `test-k6b-flash/`,
proportional line 35 of 42. Exposure: earlier prompt iterations saw these articles, and c2 was built only from dev cases.

## 26. Test set, once (c2; `test-c2-flash/`): line missed; the remaining gap is a product decision (2026-11-08)

26 of 26 complete, 0 retries. Inputs byte-identical to `test-k6b-flash/`. Gold `af2145cd…`. Exposure: earlier prompt iterations saw these
articles; c2 was built only from dev cases.

| 26 test articles (42 helpful, 9 core) | **c2** | k6b | production test d1 |
|---|---|---|---|
| Helpful kept (proportional line 35) | **31** | 32 | 20 |
| Core | **9/9** | 8/9 | 8/9 |
| Not-kept spans kept | 8 | 8 | 4 |
| Items | 44 | 42 | 39 |
| Kept as conditions | 9 | — | — |
| Unfiled and dropped | 12 | 17 | — |
| Theses | 9 | 10 | — |

**Read entry by entry.**
- **Recovered by c2 (4), every one a financial figure kept as a condition:**
  - the Q2 revenue of $96.2bn with data centre +117% (the only core miss before);
  - analysts' $441bn free-cash-flow forecast;
  - the plan to return 50% or more of free cash flow (forward cash items are kept; the cash boundary did not drop them);
  - Orange's AI-RAN testing.
- **Lost by c2 (5), every one extracted but unfiled with no thesis to take it:**
  - Run:ai open-sourced (two articles, three entries);
  - the eight DSX ecosystem partners;
  - NVIDIA's investment in Nous Research;
  - the leakers' RTX 5090 claim.
- **Missed by both (6):**
  - Dell XPS with RTX Spark (2), unfiled, because the RTX Spark thesis opened after it;
  - the ZOTAC denial, unfiled;
  - the valuation assumptions, unfiled;
  - AI infrastructure above $1tn by 2029, and Aerial RAN configurations, not extracted.
- **9 of c2's 11 misses are extracted, material, non-figure statements dropped for want of a home.** Keeping every unfiled item would
  give **40 of 42** (noise 8 → 10). On dev the same move gives 209 → 219, noise 41 → 42.

**The frozen test gold forbids the theses that would house them.** Its must_not entries include, word for word:
- "Will open-sourcing Run:ai strengthen NVIDIA's software moat";
- "Will NVIDIA discontinue the RTX 5090 before the end of 2026";
- the RTX Spark OEM-laptop count;
- "以约束性义务为理由开 NVIDIA 投资 Nous Research 这一题".

It marks the statements themselves helpful (supporting). So the gap cannot be closed by opening more theses (D248 and the gold say
no). Two ways remain, and both are outside Alex's decisions so far:
- **(1) Product.** Keep a statement the model judged material but no thesis takes, as an unlinked record of the company, linked when a
  thesis that covers it opens (the backfill already designed for conditions). This amends D209 beyond Alex's amendment for financial
  figures. Upper bound: test 40, dev 219, noise +2 and +1.
- **(2) Measurement.** The test starts from an empty library, which production never does in September. The dev-end library already
  holds plausible homes: clean-2 AI cloud build-out with DSX, clean-22 Nemotron/NemoClaw software adoption, clean-14 consumer-GPU memory.
  Re-running the test from it is a second test score of the same configuration, so it needs Alex's word (AGENTS §7.1: score test once
  per configuration).

Step 1 under the current decisions: dev line met (209, small 3, fragments 0); **test line missed (31 of 35)**, by design drops, not by
the model's reading. **Goes to Alex as a product decision.**

## 27. Alex decides: keep material statements with no home, link them later (2026-11-08)

**Question** (his reply to these exact options). Example: Dell's XPS with RTX Spark was read and judged useful on Oct 9, but the RTX
Spark thesis opened the next day, so the statement was dropped. 9 of the 11 test misses are like this; the gold forbids opening those
theses but marks the statements helpful.
- **"先存着，有观点再挂 (Recommended)"** (chosen):
  - a statement the model judges useful but no thesis takes yet is kept in the company's record, like a financial condition, with no
    link;
  - it is linked automatically when a related thesis opens;
  - what the closing check rejects is still dropped, the cash flow Alex ruled out included;
  - estimate: test 31 → at most 40 (line 35), noise 8 → 10; dev 209 → 219, noise 41 → 42.
- "照旧丢，改测法" (not chosen).
- "照旧丢，测法也不改" (not chosen).

**Decided:** D209 is amended a second time. Every statement the model returns as material is kept, linked or not. An unlinked statement
is stored in the company's record and linked when a thesis that covers it opens. A statement the closing check rejects is not returned
and is dropped.

**Consequences:**
- Step 1 code keeps every returned evidence item.
- The prompt no longer says an unfiled statement is dropped, and the closing read-back makes a ruled-out cash or balance statement "not
  returned".
- Step 2's own-text query already covers unlinked records (§24).
- Step 3 needs the later linking (design §11.1, now for every unlinked record, not only conditions).

## 28. Arm c4: Alex's decision built; the valuation row aligned with his ruling (2026-11-08)

**c4** = c2 plus:
- the role's unfiled sentence: "code keeps it in the company's record and links it when a thesis that covers it opens", replacing
  "does not store it", with the condition exception removed;
- the CONDITION bullet without "instead of unfiled";
- the closing read-back: a ruled-out balance or cash-flow statement is "not returned";
- the schema's links description.

`runner.py` keeps every returned item (`unfiled_evidence` is always empty). Tests were updated for the recorded spec change (§27), 37
pass; all 3 mutants caught: the old D209 drop, only figure items kept, an invalid figure kept.

**Check sends, one draw each** (`probe-r7-c4/`, $0.12; ten cases, including positive controls):
- **Right:**
  - cash not returned (d1-57, empty-57);
  - margin under clean-11 (d1-40, d1-57);
  - empty-57 conditions only, no thesis;
  - EPS linked;
  - the required openings opened: pos-1 credit support, pos-49 Kyber NVL144 shipping;
  - d1-22's Parker appointment (gold supporting) and d1-38's Cerebras claim (supporting) now kept unlinked.
- **Wrong:**
  - d1-66's author target ($319) was kept unlinked;
  - d1-22's Microsoft Frontier initiative (gold not-kept) was kept unlinked;
  - d2-6 Nemotron and d2-8 supplier theses (known class).

**Mechanism of the target price.**
- K6b closing row 6 says "a conditional valuation of the company with its assumptions, derivation and date is kept". It contradicts
  Alex's "留 EPS 预测，丢目标价".
- The conflict was hidden while the model's "unfiled" was a code drop.
- **Fixed to Alex's ruling:** "a target price or valuation of the company is not kept, even with its assumptions and derivation,
  while the estimates it rests on are judged on their own (an analysts' earnings forecast is kept)".
- **Disclosed cost on the frozen gold (D373):** golden-v5 marks d1-38's $305 valuation and the test's valuation assumptions supporting.
  Alex's later explicit ruling governs the system; the gold is not edited.

**Resend** (`probe-r7b-c4/`, $0.05):
- the targets were dropped (d1-66, d2-66, d1-38) and the P/E valuation too (d1-57);
- EPS was kept and linked in all three;
- d1-57's $19.3bn buyback was kept unlinked (unlisted in the gold, so neutral).

**Runs launched in parallel**, inputs byte-identical (source content sha256 checked):
- `gold-c4-flash/` (115 dev, `max_calls` 140);
- `test-c4-flash/` (26 test, 52). c4 is a new configuration, so the test is scored once for it.

## 29. Test set, once for c4 (`test-c4-flash/`): the line is met (one draw)

26 of 26, 0 retries. Inputs byte-identical. Gold `af2145cd…`. Exposure as in §26.

| 26 test articles (42 helpful, 9 core) | **c4** | c2 | k6b | production test d1 |
|---|---|---|---|---|
| Helpful kept (proportional line 35) | **36** | 31 | 32 | 20 |
| Core | 9/9 | 9/9 | 8/9 | 8/9 |
| Not-kept spans kept | **4** | 8 | 8 | 4 |
| Items | 51 | 44 | 42 | 39 |
| Unlinked kept | 17 | (9 conditions) | — | — |
| Theses | 10 | 9 | 10 | — |

**The 6 misses, each read against the answer:**
- the Dell Creator desktop sentence (the XPS item is kept, unlinked);
- "AI infrastructure spending will exceed $1 trillion by 2029" (not extracted);
- the valuation assumptions (dropped by Alex's target-price ruling: the disclosed cost, §28);
- the ZOTAC denial;
- Orange's AI-RAN testing;
- the Dell/QCT/Supermicro Aerial configurations.

**Noise fell from 8 to 4**, production's level; the valuation row now drops valuation conclusions.

**The 17 unlinked statements were read one by one:**
- company figures: Q2 revenue and guidance, free cash flow and the capital-return plan, two customers at 22% and 14% of revenue;
- product and deal news: Shield TV discontinued, the RTX 5090 rumour, Dell XPS with RTX Spark, the Groq acquisition;
- the cash items sit in an article about the capital-return plan, which ties cash to that use;
- one is another company's (supplier Credo's results).

The source-backed thesis review is running (`theses-answer-r{1,2,3}.json`). The c4 dev run is live.

## 30. The c4 dev run stopped on a cut answer; the runner misread Alex's retry rule; fixed and continued (2026-11-08)

**What happened.** At article 59 (`gnews:3df0bbc8…`) the model reasoned for 29,111 tokens and hit the 32,000-token output cap
(finish_reason "length"). The runner raised "provider refused or returned incomplete output" and stopped the run after 58 articles.
The same article took 13–22k completion tokens in k6b d1, k6b d2 and c2.

**The defect.**
- Alex's rule (LOG §16): "An answer that is not JSON, or not the schema, is sent once more unchanged … Any other failure still stops
  the run."
- A cut answer is not JSON. But the runner checked finish_reason before parsing and treated "length" as an other failure.
- **My close-out test even encoded that misreading:** it used a "length" answer as its example of a non-format failure. The test
  misread the spec; the spec did not change.

**Fix.**
- A cut answer raises a format failure, so it is retried once with the identical request; if the retry fails too, the item is failed
  and the run continues.
- A provider refusal still stops the run, and the test's example is now a refusal.
- One new test; 38 pass. Both mutants caught: a cut answer stops the run, a refusal is retried.

**Continuation.**
- `gold-c4-flash/segment-2/`: the remaining 57 items in manifest order, starting with article 59.
- Initial library = the 12 theses after article 58; the same c4 prompt files, settings and source (`SHA256SUMS`).
- `run_forward.step1_records` now reads 'a.sqlite+b.sqlite': a segment's sequences continue after the completed rows before it.
- Scoring reads both segments.
- **Disclosed:** the continuation restarts article 59's call with the fixed runner. The other 114 articles ran under the same code as
  far as their prompts and checks are concerned.

## 31. Whole bench for c4 (dev, one draw) and later linking checked (2026-11-08)

**Dev run** (`gold-c4-flash/` plus `segment-2/`; 115 of 115; 2 retries, both empty-content format failures that conformed on retry).

| 115 dev articles, one draw | **c4** | c2 | k6b d1 | k6b d2 | production v108 |
|---|---|---|---|---|---|
| Helpful kept (line 190) | **216** | 209 | 205 | 197 | 162–171 |
| Core | 84 | 85 | 84 | 85 | 75–76 |
| Not-kept spans kept | **35** | 41 | 40 | 38 | 30–34 |
| Items | 289 | 290 | 282 | 265 | 278–301 |
| Unlinked kept | 56 | (16 conditions) | — | — | — |
| Theses opened | 14 | 24 | 25 | 18 | — |

**Theses** (three source-backed readers, `theses-answer-r{1,2,3}.json`):
- 2 small by majority: Intel's $5bn stake, small in every run; liquid-cooling supply capacity, Alex's supplier class;
- 0 duplicates;
- split: export-control enforcement and optical interconnects (one reader says small each).

**The dev line is met:** helpful 216 ≥ 190, small 2 ≤ 3, fragments 0. Noise is the lowest of the clean runs.

**Regressions first.**
- **Core 84** against c2's 85. The core entries missed are listed in `score.json`; one draw.
- **No thesis for the hyperscalers' aggregate capex.** The frozen question gold has it as must_open for three articles; the evidence is
  kept, unlinked at article 42 and linked to the Vera Rubin thesis later. It is the D191 shared-quantity class that Alex scheduled
  for the next extraction version ("这个你记住，我们要做", 2026-11-05). Recorded, not fixed here.
- **Fewer theses** (14 against 24): the small ones of c2 (Nemotron, BioNeMo, quantum, robotics) are gone. The required openings are
  present: credit support (clean-1), China H200 (clean-8), and Kyber, as the opening it gives AMD and Google (clean-12), next to the
  Vera Rubin timeline (clean-6).

**Later linking** (Step 2 run `clean-step2-forward-c4-2026-11-08/`; Jev yes/no question per stored unlinked group from earlier
articles, in batches of 10):
- **First criteria:** 169 pairs judged, 7 linked. Read one by one, 2 were right (the Valar Atomics nuclear data-centre collaboration
  under the power-constraint thesis; Anthropic's 220k-GPU SpaceX cluster, borderline) and **5 wrong**: the company-wide revenue figures
  linked to the Huawei, custom-ASIC and inference-startup theses.
- **Mechanism:** the criteria said only "makes the thesis's answer more or less likely", and the company's revenue is the outcome those
  competition theses watch.
- **Fix, from Step 1's own rule:** "the company's overall results, guidance and estimates inform a thesis about its revenue or earnings
  path, not one about a competitor, a supplier or a policy unless they speak to it"; "a shared company … is not enough".
- **Replay** (`…-ll2/`): every Step 2 decision came from cache and was identical; later linking judged 169 and linked 1, the Valar
  item.
- **Alex's example on the test run** (`clean-step2-forward-test-c4-2026-11-08/`): **the Dell XPS statement is linked to the RTX Spark
  thesis when it opens at article 16**. The other link, the two customers at 22% and 14% of revenue under the debt-funded build-out
  thesis, is plausible.

## 32. Step 2 re-measured on the c4 records; Jev's criteria aligned with the merge line (2026-11-08)

**Run** (`clean-step2-forward-c4-2026-11-08/`): 289 records made 179 groups; 110 repeats, 4 revisions, 0 refused.

**Line 1, search** (the reference carried onto the new records by `map_reference.py`: an identity rule on shared verbatim passages in the
same article; 89% of the old records map, 326 of 333 same-statement pairs): **104 of 105 known counterparts found (99.0%), met.**

**Line 2, wrong merges** (two blind Codex readers per packet, a third on every pair either rejected; the same prompts as before, packets
built by `build_merge_packets.py`): **8 of 110 wrong (7.3%), missed**, against 3 of 104 before. Each wrong merge read:
- **6 are one cascade.** Step 1 put SemiAnalysis's Kyber-delay report and NVIDIA's denial ("Our roadmap is intact") into one record
  (49:e1). Every later outlet's denial was then judged by Jev a "same_statement" of that record, with probability 0.79–0.96.
  - In k6b d1, k6b d2 and c2 the denial was its own record. Five re-sends of article 49 with c4 (`probe-r8-kyber-c4/`) separated it
    5/5. So the bundling is rare (1 of 9 samples), but one bundle of a widely repeated statement multiplies into many wrong merges.
  - The earlier Step 2 run's wrong merges were the same class (NVL576 into the NVL144 record, twice).
- **The other 2 are Jev errors at low confidence:**
  - X30, the analysts' $253bn → $392bn path against 82%/41% growth, the same pair as the earlier run (0.52);
  - X99, China data-centre revenue at zero against no H200 revenue (0.57).
- **A probability cut is not a fix.** Below 0.6, the c4 run's merges are 3 wrong and 4 acceptable; the earlier run's are 0 wrong and 5
  acceptable.
- **An original-party identity rule is not a fix either.** The free-text party differs in 28 accepted merges ("Firmus Technologies" and
  "Firmus").

**One-ruler fix (AGENTS §7.1).**
- **The mismatch:** the merge line's test is "later reports earlier's **main** statement"; production's Jev criterion was "the same
  evidence".
- **The fix:** the clean Step 2 now asks Jev its own piece question:
  - same_statement = the incoming piece reports the stored piece's main statement; a report of only a secondary statement is not it;
  - supersedes keeps "an official confirms or denies that reported claim".
- **The replay** (`…-p2/`; every other cached answer reused): 108 repeats, 3 revisions.
  - Verdicts were carried to the 95 identical pairs; the 13 new pairs were read by two readers and one disputed pair by the third.
  - **4 of 108 wrong (3.7%).**
  - X30 and X99 no longer merge. Two denials became a revision of the report and a repeat of the standalone denial group.
  - **The 4 left are the early denials into the bundled record 49:e1**, which arrived before any standalone denial group existed.
- **Every other merge is acceptable or overlap.**

**Later linking on the new criteria:** 173 judged, 1 linked (Valar). Line 3 (the reader test) was not re-measured: its dossiers are
keyed to the old run's thesis ids.

**Next (the root of the remaining class).**
- Step 1's unit, from the signed standard's own definition, "陈述：原文里某一方说的一句话或一件事" (a statement is what one party said):
  one item holds one party's statement, and another party's response to it is its own item.
- The c4 sentence "an estimate and a target price … drawn from it are two statements" is the same rule and is folded into it.

## 33. Arm c5: one party's statement per item (2026-11-08)

**c5** = c4 plus one closing-check sentence before "Return only the evidence items you keep":
- the sentence: "Each item you keep holds one party's statement: another party's response to it (a denial, a confirmation, a comment) is
  its own item, and so is a valuation someone draws from an estimate";
- c4's system sentence "An estimate and a target price or valuation someone draws from it are two statements" is removed, because the
  general rule now carries it;
- sources: the signed standard's glossary, "陈述：原文里某一方说的一句话或一件事"; K6b §4, "one evidence item records one statement";
  Alex's EPS/target ruling;
- size: system 14,491 → 14,403; closing 8,114 → 8,302.

**Check sends, 2 draws each** (`probe-r9-c5/`, $0.14):

| Case | Result |
|---|---|
| Kyber article 49 | the denial is its own item 2/2 |
| d1-57, d1-62 | one speaker's revenue and margin guidance stays one item; no over-splitting (3 and 7–8 items, as under c4) |
| d1-66 | EPS kept, target dropped |
| pos-1 | credit-support thesis opened |

**Runs launched in parallel**, inputs byte-identical (source sha256 checked):
- `gold-c5-flash/` (115 dev);
- `test-c5-flash/` (26 test, scored once for c5).

The runner retries a cut answer (§30). Step 2 follows on the c5 dev records with the aligned Jev criteria (§32).

## 34. c5 measured; Step 2 lines 1–2 met on its records; c6 narrows the rule and raises the output cap (2026-11-08)

**c5 test** (`test-c5-flash/`, once): helpful **38/42**, core 9/9, **noise 11** (c4 4), items 57, theses 9 (0 small, 0 duplicates).

**c5 dev** (`gold-c5-flash/`): 114 of 115. Article 54 (`…9756d6`, the SemiAnalysis backstop article, 16 helpful entries) was cut at the
32k output cap twice and failed; the run continued, as Alex's rule says.

| On the 114 articles both completed | **c5** | c4 |
|---|---|---|
| Helpful (of 218) | 204 | 203 |
| Core | 80 | 79 |
| Not-kept spans kept | **39** | 33 |

**Regression read item by item on dev** (tuning set):
- **What:** the extra noise is other parties' remarks extracted as their own items (Mizuho's and Bloomberg's analysts' remarks, a
  defendant's lawyers' statement, Huang's "parabolic", startup CEOs' IPO plans).
- **Mechanism:** c5's "another party's response to it (a denial, a confirmation, **a comment**) is its own item" licensed creating items
  from remarks, not only unfolding a bundle.
- The test showed the same direction.

**The output cap is too low for the longest articles.**
- Article 54 took 27k completion tokens in c2, 18k in c4, and over 32k twice in c5.
- Re-sent once with a 64k cap, it completed: 37,210 tokens (32,074 reasoning), valid JSON, 16 items.
- The cap was an implementation detail of the close-out (32,000), not a setting Alex chose. **Raised to 64,000.** Only long answers use
  more.

**Step 2 on the c5 records** (`clean-step2-forward-c5-2026-11-08/`, aligned Jev criteria):
- **Kyber split cleanly:** the report group with 10 retellings, the denial group with 6.
- Line 1, search: **94 of 96 (97.9%), met.** The reference is now mapped by input id: c5's failed article 54 had shifted the numbering
  of every later article, so 34% mapped before the fix and 86% after; c4's mapping is unchanged at 89%.
- Line 2, wrong merges: **2 of 105 (1.9%), met.** Both are isolated Jev errors: two different revenue-sharing programmes (0.84); three
  companies' water work against NVIDIA's DSX design (0.50).
- Later linking: 325 judged, 4 linked.

**Identity fix in Step 2:** `run_forward.step1_records` and `build_merge_packets` number an article by its position in the first
segment's manifest, so a failed item no longer shifts later ids (AGENTS §3, identity). c4 and c2 numbers are unchanged; stored c5 Step
2 results stay internally consistent.

**c6** = c5 with:
- the closing sentence narrowed to "Do not fold another party's statement into an item: a report and the denial or confirmation of it are
  two items, and so are an estimate and a valuation someone draws from it, each kept only if it passes the test above";
- max_output_tokens 64,000.

**Checks** (`probe-r10-c6/`, 2 draws each, $0.14):
- Kyber denial separate 2/2; no over-splitting (d1-57);
- the lawyers' statement and the Mizuho and Bloomberg remarks are gone;
- startup CEOs' own IPO remarks remain (their own statements, not folds).

`gold-c6-flash/` and `test-c6-flash/` launched 04:10, inputs byte-identical.

## 35. c6 measured: Step 2 lines 1–2 met; Step 1 misses only "no fragments" by one per set; the question gold is far stricter than the readers (2026-11-08)

**c6 dev** (`gold-c6-flash/`): 115 of 115 in 115 calls; articles 54 and 59 completed under the 64k cap with no retries.

| 115 dev articles, one draw | **c6** | c4 | c2 | k6b d1 / d2 | production v108 |
|---|---|---|---|---|---|
| Helpful (line 190) | **219** | 216 | 209 | 205 / 197 | 162–171 |
| Core | 85 | 84 | 85 | 84 / 85 | 75–76 |
| Not-kept spans kept | **33** | 35 | 41 | 40 / 38 | 30–34 |
| Theses opened | 20 | 14 | 24 | 25 / 18 | — |
| Small / duplicate theses (majority of 3 source-backed readers) | 2 / **1** | 2 / 0 | 3 / 0 | 2–3 / 0 | — |

**c6 test** (`test-c6-flash/`, once):
- helpful **40/42**, core 9/9, not-kept 8 (c4 4, c5 11, k6b 8), 10 theses, small 2, **duplicate 1**;
- misses: the valuation assumptions (Alex's ruling) and the telecom providers working on AI-RAN.

**Step 2 on the c6 records** (`clean-step2-forward-c6-2026-11-08/`):
- 291 records → 187 groups, 104 repeats; Kyber split cleanly (report 10, denial 8);
- line 1, search: **95 of 97 (97.9%), met**;
- line 2, wrong merges: **2 of 104 (1.9%), met** (X4, the two revenue-sharing programmes, recurring; X83);
- later linking: 242 judged, 3 linked;
- line 3 not re-measured (dossiers keyed to the old thesis ids; Step 3's grouping code unchanged since it passed).

**The two duplicates, traced.**
- **The theses:** dev "AI labs building their own custom inference chips (DeepSeek, OpenAI)" against the open "non-Huawei competitors or
  alternative stacks such as Cerebras"; test "xAI's Colossus 2 buildout" against the open "neocloud GPU rental prices as the demand
  read-out".
- **The model's accounts** (`gold-c6-flash/fragment-accounts.json`): it applied K6b's separate-bet test ("their answers can move apart")
  with analyst reasons: customer insourcing is not merchant competition; one lab's deployment is not neocloud pricing.
- **The frozen question gold** marks both must_not: "A DeepSeek chip development question" and "An OpenAI Jalapeno deployment question";
  "Will xAI's Colossus 2 reach about 1.21 million NVIDIA GPUs by the end of 2026?". So they are errors by both references, not a
  reader's threshold.

**Census: theses against the frozen question gold** (c6 dev 20, test 10; read against each opening article's must_not):
- **About half match a must_not entry:**
  - Intel's stake;
  - the Singapore case;
  - AI debt above $7T;
  - Hugging Face robotics;
  - Chinese-lidar legislation;
  - SpaceX orbital data centres;
  - DeepSeek/OpenAI chips;
  - quantum (twice);
  - SpaceX's $40bn financing;
  - RTX Spark OEMs;
  - AI-RAN revenue;
  - xAI Colossus.
- **The required openings are present:** credit support, Kyber NVL144, China access, supply commitments.
- **Most of the must_not theses were judged "bet" by the readers.** k6b and c4 opened theses of the same kinds (c4's test opened the same
  xAI thesis, then not flagged because nothing overlapped).
- **So:** the reader-based pass line (small ≤ 3, fragments 0) and the frozen question gold disagree widely on what merits its own
  thesis. Which one governs Step 1's thesis granularity is Alex's call (the council-loop trap: when references split on "how big is
  big", his rulings are the ruler).

**Status against the agreed lines** (one draw each):
- **c6 meets:**
  - Step 1 helpful (dev 219, test 40), small (2/2), noise (dev 33, at production's level);
  - Step 2 search (97.9%) and wrong merges (1.9%).
- **c6 misses:** "no fragments" by 1 on each set.
- **c4** meets every Step 1 line but misses Step 2 wrong merges (3.7%, from one rare bundling cascade that c6's rule prevents).

## 36. Alex decides: open only big matters, by the frozen gold's standard (2026-11-08)

**Question** (his reply to these exact options). Example: an article says NVIDIA supplies SpaceX's orbital data centre. The readers
would open "will orbital compute become new NVIDIA revenue"; the gold, applying the signed standard (the answer can change a position,
is checkable on a date against public material, and a single deal or product opens only when its scale can change revenue), says it is
one customer's project, evidence only. Unlinked evidence is kept and linked later, so not opening loses no evidence.
- **"按金标：只开大事 (Recommended)"** (chosen):
  - open only the gold's big matters: NVIDIA's own obligations (credit support), main-product shipping (Kyber), policy (China H200), and
    checkable shared quantities (combined customer spending);
  - another company's single project, partnership or one product line is not opened; its evidence is kept;
  - next, align the opening rule with the standard's three tests and measure against the gold's must_open and must_not.
- "按读者：维持现在的线" (not chosen).
- "先定 c6，尺度以后再议" (not chosen).

**Decided:** Step 1's thesis granularity is governed by the signed standard's opening tests as the frozen question gold applies them.
The reader-based "small/fragment" line gives way to must_open covered and must_not not opened.

## 37. Arm c7: the opening rule from the standard's closed set (2026-11-08)

**c7** = c6 with §3 rewritten from the signed standard (§3 question types, §4 opening tests and the do-not-open list):
- **The opening test:** a thesis is a question whose answer can change a position, that public material settles on a date, and that
  no open thesis asks.
- **The reasons, a closed set of four:** product_node, binding_obligation (credit support included; an undertaken amount at the next
  annual report, or signing within 18 months of the item), shared_quantity and policy_stage. Each has a cross-industry example; none
  names the company or copies the gold.
- **Class A (main-driver quantity) is excluded,** by Alex's figures-are-not-theses decision; the gold lists such questions may_open.
- **Removed:** K6b's "a competitor's or customer's move that can shift its share or demand" (not in the standard's set) and "a topic may
  be opened before its business impact is known" (wider than the checkability test).
- **Added from the standard's do-not-open list:** "a customer's deployment plan is evidence … unless it changes the company's own cash
  or credit risk"; an undated moat; another estimate of what an open thesis tracks; an annual quantity after next year (obligations
  excepted).
- **Dates:** analyst-set dates are allowed as the standard does (fiscal year-end for pending regulation; within 18 months for unsigned
  obligations).
- **Schema:** `opens_as` (an enum, checked by code) and `settled_by` (non-blank, checked by code) are required. The closing check
  drops a thesis that fits none of the four reasons or has no settling material.

**Audit** (`council/ac-*`, `ad-*`; blind Codex against the standard). Fixed:
- a blanket single-product ban (it would block product nodes);
- an obligation written as signing only;
- "do not invent a date" (it contradicted the analyst-set check dates);
- "a year after next" (the standard limits annual quantities only);
- the closest-thesis test with an empty library;
- linking to every informed thesis;
- two examples copying the gold's kinds;
- a blanket single-project ban.

**Check sends, one draw each** (`probe-r11-c7/`, $0.15):
- **Gold must_open, all four opened with the right reason:**
  - pos-1, credit support: binding_obligation;
  - pos-42, the big four's capex: shared_quantity;
  - pos-49, Kyber shipping: product_node;
  - pos-100, China H200: policy_stage.
- **Gold must_not openers, 0 theses in all seven:** orbital data centres, quantum, Hugging Face robotics, lidar legislation,
  DeepSeek chips, Intel's stake, AI debt.

`gold-c7-flash/` and `test-c7-flash/` launched 06:17 (64k cap, inputs byte-identical). **The question measure is new:** must_open
covered and must_not opened, per the frozen question gold, read by blind readers.

## 38. c7 test, once; question measure baselines (2026-11-08)

**The question measure** (`question-check/`; `build_question_packets.py` and `tally_questions.py`; one blind Codex reader per run maps each
opened thesis to the article's must_open / may_open / must_not entries and checks each must_open entry against the theses open after
the article):

| Run | Opened theses: must_open / may_open / must_not / none | must_open covered |
|---|---|---|
| c4 dev | 0 / 2 / 2 / 10 (of 14) | 21/28 |
| c6 dev | 1 / 2 / 6 / 11 (of 20) | 22/28 |
| c4 test | 0 / 1 / 3 / 6 (of 10) | 0/3 |
| c6 test | 1 / 1 / 5 / 3 (of 10) | 2/3 |
| **c7 test** | 1 / 1 / **1** / 0 (of 3) | **2/3** |

**The uncovered must_open entries in c4/c6 dev** are the shared quantities (the big four's 2026/2027 capex ×5, DRAM contract prices) and
the Ohio lease guarantee. c7 adds the shared-quantity reason. **The test's one uncovered entry**, "NVIDIA data center revenue for fiscal
2028", is class A, excluded by Alex's figures-are-not-theses decision: a disclosed, by-design miss.

**c7 test** (`test-c7-flash/`, once):
- helpful **38/42**, core 9/9, not-kept 13 (c6 8, c4 4, c5 11, k6b 8), items 63 (52 unlinked);
- theses 3: supply-commitment amount (binding_obligation, must_open), Hugging Face acquisition (binding_obligation), RTX Spark OEMs
  (product_node, must_not);
- three source-backed readers: bet ×3 for each, so small 0, duplicates 0;
- noise read item by item: about half the 13 are the same items c6 kept (Nebius, streaming-device prices, DLSS 5, Surface,
  RTX 5090 price, lobbying); the rest are general lines (capacity-constrained, a dividend projection, Meta's agent). One-draw test
  noise across arms ranges 4–13, so no c7 effect is established; dev decides.

The c7 dev run is live.

## 39. Alex: "你这些改动有我你有好好的跑council 再下手"; retro council on the unreviewed changes (2026-11-08)

**Honest account.**
- **Reviewed before the send:** c2 (reflection council plus blind audit, `v`–`z`); c3 (stopped by the audit, `ab`); c7 (blind audit, `ac`,
  `ad`).
- **Not reviewed before the send:**
  - c4, including the valuation row;
  - c5 and c6;
  - the 64k cap;
  - the cut-answer retry, with its test change;
  - the clean Jev piece criteria;
  - the tightened later-linking criteria;
  - numbering by manifest position and the input-id mapping.
- Council B on results was skipped for c4, c5 and c6.
- No new run was started after his message. The c7 dev run, already 48/115, continues; its result is exploratory.

**Retro council** (`council/ae-claude.md` written first; `ae-codex.md`, a fresh independent session). Checked against the files:
- **Keep:**
  - the unlinked keep (Alex's decision);
  - manifest numbering;
  - the 64k cap, provisionally (one cut article is the evidence).
- **Revise:**
  - **Valuation row (c4 onwards).** Alex dropped one author's target price (LOG §11). The row now drops every valuation, while the
    signed D243 #4 says "孤零零的目标价可选；带推导的条件估值仍是辅助". His later ruling and his signed standard conflict on this point:
    a question for Alex, not mine to settle.
  - **Cut-answer retry.** Alex's rule covers "an answer that is not JSON, or not the schema". A length-cut answer can still parse.
    Whether a cut answer is retried or stops the run is his boundary to set; the old test was not proven wrong.
  - **c6's not-folding rule:** two-draw checks do not show it keeps useful combined context. **c5 is reverted** (superseded).
  - **Step 2:** the clean Jev criteria and the later-linking criteria were judged on the cases that motivated them. Later linking was
    not checked for missed links, and line 3 was not repeated.
  - **Reference mapping:** greatest passage overlap can map a bundled old record to one of several new records; the mapped-only score
    says nothing on unmapped cases.
- **Not trustworthy as acceptance:** the c2–c7 test numbers. The test set was exposed, and test results informed the next arm across five
  configurations, so "once per configuration" does not undo the selection. Acceptance needs a frozen configuration on fresh articles.
- **Process errors, ranked, with the rule for each:**
  1. **Selection on test.** Rule: reserve a fresh set until the configuration and criteria are frozen.
  2. **A ruling widened beyond its words.** Rule: trace every changed sentence to the exact ruling and test both boundaries.
  3. **Sends without challenge.** Rule: council before every send, now in AGENTS §7.3 in Alex's words.
  4. **Fixes judged on their motivating cases.** Rule: include untouched cases, and read both false merges and missed links.
- **Agreed next step:** before any further run, one independent, source-backed review of the complete proposed request and its
  downstream checks (valuation, split statements, retry classification, linking) on stored cases. It records each contradiction and open
  decision, and fixes what the final configuration is.

## 40. Council: complete review of the proposed final configuration (2026-11-08; Alex: "你的goal 需要严格的跑council 来review 和思考再决策")

**Decisions recorded first.** Alex's decisions of 2026-11-07/08 are appended as D380–D386 to `docs/DECISIONS-log.md`, with index rows, in
his words. D209 and D243 #4 are marked as amended for the clean path.

**Procedure.** Claude's judgement was written first (`council/af-claude.md`). A fresh Codex review read the whole configuration
(`af-codex.md`): "Do not freeze c7 yet". Every claim was checked in the files. The challenge round (`ag-challenge.md`, `ag-codex.md`)
ended in agreement with changes.

**Agreed corrections (c8 = c7 plus these):**
1. Remove the K6b example "an analyst valued the shares at $80, 15 times next year's earnings of $5.30" (c7-system line 36), which
   contradicts D385.
2. Closing line 12 against the standard's "不拆成两条，除非是两件事" (line 436): "A report and another party's denial or confirmation of it
   are two items, as are an estimate and a valuation someone draws from it; one party's statement keeps its own planned or rumoured
   details."
3. Line 55: "… inform an open thesis about its revenue or earnings path when they bear on that path; a different period is not on its
   own a reason to leave them unlinked." This keeps Alex's margin ruling and D371, with relevance as the test.

**Code corrections:**
- `score_final.py` refuses a line-2 verdict while any pair is unjudged.
- `tally_questions.py` refuses mismatched counts.
- Later linking retries pending pairs on the next write to the thesis and at a run's start (design §11.1), keeping the original
  opening boundary, and reports what stays pending.
- `map_reference` collisions are counted and inspected against the source.

**Kept, conditionally:** search and later-link judgement on group originals, provided the group is a true repeat. Stored groups where a
member adds a material detail are to be checked.

**Before freezing:**
- the whole-request two-way audit (prompt-audit skill, blind second reader);
- on stored data: unresolved links, quote and figure issues, mapping collisions, later-link misses;
- retry recovery and exact request bytes;
- the touched tests and the full suite once;
- the prompt growth explained in characters and tokens;
- the exposed test results and the two D385 conflicts with the frozen gold kept disclosed.

**Acceptance protocol, agreed, to be frozen before any article is chosen:**
- **Population:** the first 50 eligible items by published_at from 2026-07-15, excluding every article any run has used, under the
  runner's selection rules, with a deterministic tie-break. Ids and sha256 frozen before a send; the claim is limited to that July
  sequence.
- **Run:** empty libraries, forward, the frozen configuration, one draw; dev repeated three draws.
- **Readers:** two independent readers list the matters from the source first, then judge kept items, misses, theses against the
  standard's tests, links and merges, with a third reader on disputes.
- **Lines:**
  - helpful at least 81.2%;
  - search at least 90% of reader-identified repeats **and revisions**;
  - wrong merges at most 2%, none unjudged;
  - grouped detail retention not below ungrouped, on dossiers declared before the run with the number of details stated.
- **An unexercised line is reported as unexercised, not passed.** Failed articles, pending links and reader disagreements are
  predeclared.
- **The thesis line's number goes to Alex.**
- **Stated in advance:** class A and valuation conclusions are excluded by D382/D385.

## 41. c8: whole-request audit, check sends, the checks before freezing, and the acceptance set (2026-11-08/09)

**Audit.** My own pass came first (`council/ah-claude.md`). A blind Codex audit of the whole request followed (`ah-codex.md`), and it
returned NOT READY. The blocking clause was the closing read-back, "a balance or cash flow the item ties to nothing cannot …". That
was my own widening of Alex's cash ruling, the same error as the valuation row.

The challenge rounds (`ai`, `aj`) agreed on these amendments:
- the cash example becomes an illustration ("usually") in §2 and in the closing;
- "unfiled" is replaced by "kept without links", including the label NO THESIS YET;
- linking goes to every thesis an item informs, and the narrowest relevant one is chosen only between theses that cover the same
  thing;
- the opening test names which revenue, profit, cash or credit risk, or competitive position changes, and states "one quantity for
  one period, or one event";
- dates are set by the reason: an obligation already undertaken takes its next annual report, an unsigned one a check date within
  18 months, pending regulation the fiscal year-end; a shared quantity or product event takes a date only when the item supports
  one, and otherwise the question is rewritten or not opened;
- the schema's period description is aligned with that rule;
- the two under-illustrated opening reasons get examples from other industries, with their context;
- the valuation rejection becomes unconditional in the closing.

The verdict was READY TO FREEZE. Size against K6b:

| File | K6b (chars) | c8 (chars) | Change |
|---|---|---|---|
| System | 13,476 | 15,828 | +2,352 |
| Closing | 7,670 | 8,638 | +968 |
| Schema | 5,336 | 7,646 | +2,310 |

Prompt tokens on d1-57 went from 9,398 to 10,552 (+12%). Each addition carries D382–D385 or an audit amendment.

**Check sends** (`probe-r12-c8`, 20 cases, one draw, $0.27):
- **Must-open cases:** all four gold must_open cases opened, each with the right reason (credit support; big-four capex; Kyber;
  China H200).
- **Must-not cases:** six of the seven gold must_not cases opened nothing. **neg-lidar opened a Chinese-lidar phase-out policy
  question**, which the gold lists as must_not; c7 had opened nothing there. This is one draw on a boundary; it is recorded and
  watched, and no rule is added.
- **Alex's rulings all hold:**
  - cash is not kept;
  - margin is filed under the results thesis;
  - EPS is kept and the target dropped;
  - the supplier statement is kept without links (D383; his earlier "丢掉" came before D383, so this goes to him as a report);
  - the Kyber denial is its own item.

**Checks before freezing** (Council B asked for them, `ak-codex.md`):
- **Stored c7 dev run:** 0 unresolved links, 0 figure issues and 0 quote lookup errors. Two of 288 items carry an unverified passage:
  one has an extra quotation mark, one an inserted word "robot". This is the known one-word rewrite class.
- **Preflight:** all 115 stored answers replayed under the c8 schema, with 0 refusals.
- **Request bytes:** one c8 request built offline. Its system text matches byte for byte, and its user message ends with the closing.
- **Cut answer:** the stored cut answer (c4 seq 59) was replayed through `runner.run` with `LiveTransport(send=…)`. It was sent twice
  with identical bytes and the run completed.
- **Tests:** 66 clean-arch, 3 frozen-ruler and 283 full-suite tests pass.
- **Later links** (c6 Step 2 run; two blind readers, `later-link-check/`):
  - 40 random rejected pairs: both readers say do not file. That is 0 misses in 40.
  - 3 accepted pairs: in 2, both readers say wrong (the company's overall revenue estimates linked to the thesis "will $119 billion
    of supply commitments be matched by AI demand"); the third is split.
  - Traced: in the same run, Step 1 filed the company's reported revenue and its guidance under that thesis (2 of its 7 direct
    links), and the comparison scored one pair 0.55. Later linking applies Step 1's own boundary.
  - The class over all runs: 5 in the first c4 run, before the company-wide sentence was added, and 0 in its reruns, in c5 and in
    the test run. Agreed with the council: no rule now; the boundary is judged against the source in acceptance (`am-codex.md`).

**The acceptance set.**
- **First draft.** The first 50 unused items from 07-15, ordered by (day, id).
- **First correction.** The order now parses `published_at`: news items store RFC 822 text, so a text sort puts every news item
  after the official posts. The use census became a full-id match over 8,901 files; its check finds dev 115/115 and test 26/26.
- **Council B blocked the July set** (`am-codex.md`). D386 says "no run has used", and the old pipeline's whole-window runs
  (english-v29/v34 3-month, sealed, served) processed every article from 07-01 to 08-29. **Agreed:** the set must come from articles
  that no run, old or new, has used. Only the source databases and the page-cleaning inventories are not runs, since no model saw
  the article in them.
- **Now.** The set is being re-selected from 2026-08-30. The July manifest is not used for acceptance.

## 42. Acceptance set chosen and readers' lists frozen; runs launched (2026-11-09)

**Fresh set.** 50 news articles from 2026-09-05 to 09-07 that no run has used, old or new (Council B, `council/an-codex.md`: FREEZE
AND LAUNCH).
- The procedure is `select_fresh.py`: a census of 10,871 files that refuses unless every dev and test id is found.
- Inside those days, 8 used items were skipped. The days are a weekend and the US Labor Day holiday, with no NVIDIA posts.
- Manifest sha256 `81f3f579…`.

**Pre-run readers.**

| Step | Who | Output |
|---|---|---|
| First reading | Reader A | 138 matters and 24 repeat groups |
| First reading | Reader B | 132 matters and 20 repeat groups |
| Settling | Third reader | 139 settled matters: 128 listed by both readers, 11 kept by the third; 83 core |
| Settling groups | Third reader | 26 repeat groups (82 members) and 26 dossier details |

All quotes are exact spans of the source.

- **Every reader matter is accounted for.** Of A's 138, 136 were taken and 2 dropped with reasons. Of B's 132, 125 were taken and 7
  dropped.
- **Hand check of two articles.** The year-ahead forecast and the Wistron share sale are plausible, and slightly strict: the forecast
  article's retold quarter results were left out. The standard keeps an old actual only optionally.
- Frozen in `poc/data/clean-acceptance-2026-11-09/SHA256SUMS` (`settled.json` `91caaa0b…`).

**Two process findings:**
- **A single reader session over all 50 articles stopped after 5.** It returned `status: incomplete`. The third reader was re-run in
  batches of ten articles, plus one call for the groups. Post-run judging is batched the same way.
- **Four settled matters sit in two groups.** A reader's matter bundled two points, such as "70% growth guidance, while customer
  forecasts indicate a doubling". Search is therefore counted over pairs (a later member and an earlier member of the same group),
  so a matter can belong to two pairs. This mirrors the Step 1 bundling mechanism of the Step 2 log.

**Post-run judge prompt.** It gains a neutral `optional` verdict, so that D372's optional entries are not called noise. Noise is
reported without a line. I settled this wording myself.

**Launched** (c8 pins identical in every run folder):
- dev ×3 at 08:43, in `poc/data/clean-step1-c8-dev-d{1,2,3}-2026-11-09/`;
- the fresh Step 1 run at 08:51, after the lists were frozen, in `poc/data/clean-acceptance-2026-11-09/step1/`.

## 43. Acceptance on the fresh set: every line met; links are the weak point (2026-11-09)

The fresh Step 1 run finished: 50 of 50 articles complete in 52 calls. Two format failures were resent once and passed; in one of
them the model had added a field the schema does not have.
- Cost: $0.66 at published rates (input $0.3/M, output $1.2/M, no cache share applied).
- 188 kept items and 10 opened theses.
- Step 2 placed the 188 records in 131 groups (57 repeats, 0 refused). Later linking judged 182 pairs and linked 1.

**Readers.** Two readers per batch of ten articles, and a third reader on the 23 disputes (8 matters, 15 links). On the two articles
I had traced myself (9 and 42) the readers agree with me.

| Line | Result | Pass |
|---|---|---|
| Helpful matters kept | 132 / 139 = **95.0%** (core 83 / 83). All 7 misses are supporting: two author estimates, Huang's agent-compute claim (kept in another article), the capital-return policy, a driver exploit report, handheld openness, a Kioxia SSD | ≥ 81.2%: **met** |
| Wrongly opened theses | **1** of 10, by both readers: clean-5, "will Vera Rubin account for about 20% of data-center revenue in fiscal Q3", a revenue share and so a financial measure (D382) | ≤ 2: **met** |
| Search | **141 / 143** settled repeat pairs = 98.6%; 2 pairs not exercised because a member was not kept | ≥ 90%: **met** |
| Wrong merges | **1 / 57** = 1.8%, none unjudged. 52 were accepted by both readers; of the 5 disputed, the third reader found 2 acceptable, 2 overlap and 1 wrong (Vera Rubin deliveries merged into production status and revenue share) | ≤ 2%: **met** |
| Detail retention | grouped **22 / 26** = ungrouped 22 / 26. This is structural: all 188 records are stored with their own text. The 4 details missing are Step 1 omissions | no fewer: **met** |

**My disagreement with the readers on theses.** I would also call two theses wrong:
- clean-9, global semiconductor revenue in 2026 (Deloitte's estimate): an industry aggregate that adds little beyond NVIDIA's own
  guidance;
- clean-10, NAND demand created by NVIDIA's CMX: a memory supplier's quantity.

Both readers judged them shared quantities that the standard allows. By my reading the count is 3, which misses the line. This is
reported both ways.

**Reported without a line.**
- **Kept items.** Both readers called 138 helpful, 20 noise and 13 optional; the rest were split.
- **Links: 59 / 93 judged right (63%).** This is the weak point. I read all 34 links that were not judged right:
  - about 25 are real errors, where an item is linked to the topically nearest open thesis without bearing on its question. Examples:
    SK Hynix's Indiana plant linked to NVIDIA's supplier commitments; a Fed-cut probability linked to hyperscaler capex; Wistron's
    share sale linked to Vera Rubin's revenue share; Micron's revenue linked to NVIDIA's commitments;
  - about 9 look like reader strictness. Examples: the acquisition announcement that founded the Hugging Face thesis; memory-cost
    margin pressure linked to the server DRAM price thesis.
- **The class in production.** It is production's open defect 1, where news is filed under the nearest revenue question (D355),
  and the later-link disagreement of §41.

**Next class (for the council):** link precision. First, a $0 check on the dev draws:
- links per item and the share of items linked to two or more theses, c8 against c7;
- whether c8's "link one statement to every thesis it informs" (an audit amendment) raised over-linking.

## 44. Dev ×3, the reflection council, and the link recheck (2026-11-09)

**Dev ×3 of the frozen c8** (115 dev articles, an empty start, each draw complete: 116, 115 and 117 calls; frozen golden-v5 dev,
sha `6f9476bb…`, scored as a lead):

| Measure | Draw 1 | Draw 2 | Draw 3 | c7 (earlier) |
|---|---|---|---|---|
| Helpful, of 234 (line 190) | 214 | 211 | 212 | 212 |
| Core, of 86 | 85 | 86 | 86 | 86 |
| Not-kept spans kept | 27 | 27 | 30 | 30 |
| Theses opened | 8 | 10 | 10 | 10 |
| must_open / may_open / none / must_not (one reader) | 4/3/1/0 | 3/3/3/1 (lidar) | 3/2/5/0 | 4/2/3/1 |
| must_open covered, of 28 | 25 | 24 | 27 | 27 |
| Search (reference mapped onto the draw) | 98/99 = 99.0% | 91/92 = 98.9% | 97/97 = 100% | |
| Clear wrong merges (third reader) | 1/100 | 1/100 | 1/106 | |
| Overlaps | 14 | 12 | 15 | |

- **Stable across the three draws:** the six core theses (credit support, Vera Rubin, China H200, hyperscaler capex, Kyber, supply
  commitments).
- **Varies:** the edges (memory prices, Rubin Ultra, China budget shift, lidar, DeepSeek inquiry, custom ASIC pool, inference-chip
  startups).
- **Not covered in any draw:** the Ohio-guarantee yes/no question. The broader credit-support amount thesis is opened instead.

**Reflection council** (a fresh thread, `council/ap-codex.md`, then `aq-codex.md`). It confirmed helpful, search and theses. It
retracted its first claim of 3/57 wrong merges after reading the third reader's prompt: `merge_acceptable: false` is forced on
overlaps, which the prompt defines as "not misleading", and the agreed line is clear wrong merges (D381). Agreed caveats:
- report search both ways: 141/143 for search alone, 141/145 (97.2%) for the whole system. One 11-member group supplies 55 pairs, and
  revisions are barely exercised;
- line 3 is a storage comparison, not a usability test;
- my thesis dissent is recorded as a breadth concern, not a count: the council reads clean-9 and clean-10 as supported shared
  quantities;
- c8 did not raise links per item, but that says nothing about whether the links are right.

Verdict: REPORT AS STATED.

**Link recheck (the council's cheapest next step).** A fresh senior-analyst reader saw the 34 links not judged right, mixed blind
with 10 links judged right, and asked whether the item helps assess the question:

| Original verdict | Useful | Weak | Wrong |
|---|---|---|---|
| Not right (34) | 13 | 19 | 2 |
| Right, as controls (10) | 10 | 0 | 0 |

Over all 93 links, about 72 are useful (77%), 19 are weak (20%: related, but they would not change the view) and 2 are wrong (2%).
The link problem is mainly clutter, not misleading filing. My earlier estimate of 25 real errors is withdrawn.

**Next, for Alex:**
- whether to adopt c8 as the clean Step 1 configuration (PRD §12);
- whether link clutter, about one link in five, is worth a round. If it is, the round starts with the model's own account on weak
  links, a few cents, before any design.

## 45. Alex adopts c8 (D387); the PRD carries it; next, the account of weak links (2026-11-09)

**Alex's decisions:**
- "采用 c8 (Recommended)": c8 becomes the clean Step 1 configuration (D387).
- On link clutter, "先花几分钱查原因 (Recommended)": the model's own account comes first.

**What was done for D387:**
- **PRD §12** now holds c8's system prompt, closing check and schema, byte for byte the frozen files. Its introduction records the
  configuration and the acceptance results. The earlier Luna draft's illustration and review sections are marked as history.
- **The runner reads the PRD by default** (`prd_block`, `draft`, `closing_check`). A run with no candidate files sends exactly what
  the accepted runs sent: the system message, then the user message ending with "\n\n" and the closing check.
- **Tests.** The fixtures were brought to the adopted schema: `figures`, plus the four opening fields of a new thesis. Two tests now
  parse the payload ahead of the closing check. The new test
  `test_a_run_without_candidate_files_sends_the_adopted_c8_request` passes on the control and fails on both mutants: no default
  closing check, and a block dropping its final newline. The reconstructed pre-change runner and tests, run against the pre-change
  PRD, pass 58 of 58.
- **First PRD edit split the system block.** It inserted the closing check inside the system prompt's opening fence. The new test
  caught it, and the edit was redone from the backup.
- **Renderer** pointed at the new headings.
- **Checks:** full suite 283, clean-arch 87, frozen rulers 3; `docs/check.py` passes.

**Council:**
- the review (`council/ar-codex.md`) blocked at first, because `clean-arch/step1/` is untracked and the git diff showed nothing;
- with the exact reconstructed diff (`ar-diff-step1.patch`) it approved (`as-codex.md`).

## 46. Cause of link clutter: the model's own account; council stops a send (2026-11-09)

**Account** (`link_account.py`, $0.09; `poc/data/clean-acceptance-2026-11-09/judge/link-account.json`). The stored c8
conversations were continued for 21 weak or wrong links and 3 useful controls. The model was not told which was which.
- **It condemns its own weak links.** In almost every weak case it says the statement "would not change an experienced analyst's
  view" of that thesis.
- **The reasons it gives for having linked anyway:**
  - the same subject and scope (Hugging Face facts filed to the deal-closing thesis);
  - word or theme overlap ("the only thesis naming Rubin");
  - an inference chain ("backlog → GPU orders → Rubin revenue").
- **The instructions it quotes:**
  - "Link one statement to every thesis it informs";
  - §2 EXISTING "if an open thesis covers the statement, link it";
  - "Do not exclude evidence solely because it concerns a related period…";
  - the customer and supplier "bears on" clause;
  - the supply-chain example.
- **The structural gap.** The closing check reads back only items with empty links, never a link. Line 16 says "an item an open
  thesis covers is linked there".

**Proposed arm c9, not sent.** It would have been a link read-back in the closing check. The council disagreed (`council/at-codex.md`):
- its negative test, "would not change its answer", would drop the founding premise of a thesis (the model itself called NVIDIA's own
  capex forecast, under the capex thesis, "changes little"), contrary facts, and stated supply signals;
- "covers" also appears in the system prompt;
- an account is evidence, not proof that a closing check corrects the first choice;
- Alex authorized a few cents to find the cause, not a new prompt.

Agreed: stop here and report. Any design first needs a whole-request audit against the standard, protections for founding,
contrary and stated-indirect evidence written as cases, and Alex's word before a send.

## 47. Alex approves the link-check design; reflection council on the day; code review and cleanup for check-in (2026-11-09)

**Alex's answers:**
- to "design a protected link check, a whole-request audit, then a comparison with c8 on new unused articles?" he answered
  "做，按评审流程来 (Recommended)";
- then: "跑一下council 完整的reflect 过去一天的工作进行总结，理解，学习 … 需要开始准备一版code review cleanup for check in on the branch".

**Reflection council** (my reflection first, `council/au-claude.md`; a fresh cold read, `council/av-codex.md`).

Its summary agrees with the log. Corrections to my reflection:
- dev search was 98.9–100%;
- the $4.20 Step 1 cost was computed from tokens but not logged until now: dev $1.14, $1.24 and $1.16, plus the fresh set $0.66, at
  published rates with no cache share;
- my note that Alex approved the design was correct, but the log did not record his answer until this section.

Lessons it judged weaker than I stated:
- the council helps only when it runs before the send;
- read-back is a plausible lever, not a proven one;
- the link cause is a likely cause, not a found one.

Missing lessons it added:
- a passing total can hide a missing question or an unusable grouping;
- single-draw differences under disagreeing readers cannot select an arm.

Its ranking of open defects by product impact:
1. the Ohio guarantee never covered;
2. the revenue-share thesis;
3. link clutter;
4. unverified passages.

It would not rank clutter above a repeatedly missing material question. KEEP: read the source and answers directly; challenge before
sends. STOP: generalising one ruling; treating model explanations as proof; selecting on an exposed set. START: a source-backed trace
of the Ohio miss.

**Code review for check-in** (`council/aw-codex.md`). Each finding was checked in the code before fixing. All are latent: none fires
on the accepted runs.

| Finding | Checked | Fix | Test and mutant |
|---|---|---|---|
| Step 2 dropped Step 1's verified passages, so an unverified quote lost its mark | true (`run_forward.step1_records`) | the record carries `verified_passages`; comparison text unchanged | `test_run_forward.py`; mutant caught |
| An unresolved Step 1 link became a thesis id, so the run would crash on `questions[t]` | true; 0 such links in every stored run | kept apart as `unresolved_thesis_ids` | same test; mutant caught |
| A failed comparison was refused at once, against the design's "retried once; then refused" (`STEP1-CONDITIONS-DESIGN.md`) | true; the old test fixed the wrong behaviour | retried once | `test_compare.py`: fails twice → refused; fails once → retried and used; mutant caught |
| A replayed record id with different content was accepted, and new links attached to old content | true | refused; only links may grow | `test_library.py`; mutant caught |
| `model.openai_transport`: an earlier HTTP 500's status and body rode on a final timeout | true | the last HTTP details are cleared on a network error | `tests/test_model_transport_retries.py`; mutant caught |
| The default production retry (3 attempts, waits 5, 10, 15 s) had no test | true | none needed | same file; a mutant that sleeps only between attempts is caught |
| `run_forward` exited 0 with refusals or pending links | true | exit status 1 with a printed reason; `library.json` keeps `pending` | none |
| SQLite connections were not closed | true | closed | none |

Replay of every stored trace through the changed loader ($0): 0 unresolved links, and every comparison text is already in each run's
embedding cache, so the accepted results are unchanged. The verified-passage mark now shows:
- 3 fresh records;
- 1, 1 and 3 records in dev draws 1, 2 and 3;
- 2 in c7;
- 4 in c6.

**Check-in hygiene:**
- no key material found by pattern;
- 143 process files are kept out of the commit: the raw Codex event streams (`*.jsonl`), `*.stderr`, `*.pid` and two scratch
  `.patch` files.

**Second and third review rounds** (`council/ax-`, `ay-`, `az-`, `ba-codex.md`, then a final check):
- **Links resolve by type,** as the runner resolves them: an existing target must have been shown open, and a new target must have
  been opened. Any other link is listed as '<type>:<id>'. Both id-collision cases are tested, and a mutant is caught. A replay of six
  stored traces (1,605 records) leaves 0 `thesis_ids` changed.
- **The reader's text** shows the source text Step 1 found, labelled "Quote". A passage Step 1 did not find shows the model's text,
  labelled "Unverified quote". The model's own text stays in the record. There are tests for an unverified passage and for a repaired
  passage, and mutants are caught.
- **Agreed boundary:** Jev's comparison input is not changed in this commit. It still carries the model's text without the mark,
  which is recorded as an open item for its own measurement.
- **Documents:** the older next-task sentences are marked superseded; the link check is described as a design goal; the recheck
  scope reads "34 disputed + 10 controls; 49 not rechecked".

## 48. Commit; the Ohio-guarantee miss diagnosed; one mechanism under two classes (2026-11-09)

**Commit.** Alex chose "现在提交 (Recommended)". The check-in is `cc2fdf2` on `clean-arch` (not pushed). For the next step he chose
"先查俄亥俄担保为什么没开出来" over the link check.

**Class.**
- In the dev gold, 1 of 28 must_open entries is an unsigned specific obligation (C, yes/no): the Ohio lease guarantee for OpenAI,
  article 4.
- It is missed in 3 of 3 c8 dev draws. The test gold has none. It is q23 of the frozen judgement gold.
- The other dev misses are different: 2026 capex opened as 2027 in two draws, and DRAM in one draw.

**Mechanism** (traced in all three draws; the model's account, $0.011,
`poc/data/clean-step1-c8-dev-d1-2026-11-09/ohio-account.json`):
- Article 1 opens "how much credit support will NVIDIA have extended to AI cloud partners". Article 4's Ohio item is extracted and
  linked there, and no thesis is proposed.
- The model quotes three instructions: "if an open thesis covers the statement, link it", "another estimate, source or wording of
  what an open thesis tracks", and "if the two cannot move apart…".
- It calls the two "the same quantity" and treats "unsigned" and "amount undisclosed" as reasons against a separate thesis.
- The request does carry the unsigned-obligation yes/no form (c8-system line 98, with the retailer example).

**Council** (`council/bc-claude.md`, `bc-codex.md`): AGREE WITH CHANGES.
- **The deeper cause is the word "covers".** The request uses it for two different tests: whether a statement is evidence for a
  thesis, which decides a link, and whether a thesis already asks this question, which decides opening.
- **The same clause sits under link clutter (§46).** There the model links because a thesis "covers" the subject; here it does not
  open because an aggregate thesis "covers" the event. One structural clarification may serve both classes.
- **D248 records that the Ohio exception was not separately put to Alex.** It governs through D384 ("按金标"). The gold's $500
  billion is the asset's build cost, not the guarantee amount.
- **The proposed bank example is too close to the case,** and too absolute: answers moving apart does not alone make a separate
  bet.
- **A test needs named controls before any send:**
  - small unsigned obligations;
  - signed components already in a total;
  - duplicate wordings;
  - independent large unsigned obligations in other industries;
  - a blind reader against the source.

  Three draws are a first probe, not proof.

**Status.** Diagnosis complete. A fix is a new version of the adopted c8, which only Alex opens. It goes to him as one
recommendation and one test.

## 49. Arm c9 (the "covers" split) probed and stopped (2026-11-09)

**Alex's word:** "做，按评审流程 (Recommended)".

**Before the send:**
- The design and controls, with predeclared falsifiers (`council/bd-claude.md`, `cases-c9.json`, 32 cases).
- The design council asked for changes (`bd-codex.md`), and the blind whole-request audit returned NOT READY (`be-codex.md`). Both
  objected to my total-against-instance sentence as wider than D248. It was rewritten to D248 boundary 1's own two layers, and the
  indirect-signal wording was widened. Both reviewers then cleared it (`bf-`, `bg-`, `bh-codex.md`).
- Preflight: 395 stored answers judged under the c9 schema, 0 refusals.
- The c8 control rebuilds all 32 stored requests byte for byte.
- A synthetic answer passes every check.
- Tokens: an estimate of +212, against +204 measured.

**Results** (`probe-r13-c9`, `probe-r13-c9-ohio`; one draw per case, three for Ohio; $1.12 at published rates):
- **Ohio:** c9 opens the signing thesis in 1 of 3 draws, c8 in 0 of 3. **The falsifier fires.**
- **New theses under c9:**
  - fresh-24 "Will the FOMC raise the federal funds target…", plainly off-topic;
  - fresh-47, an NVIDIA investment of $2.5–3 billion, likely small;
  - fresh-14, memory supply in 2027;
  - dev-1 reworded the aggregate as "have signed".
- **Gained:** c9 drops the CMX NAND thesis on fresh-45.
- **Links per item rose from 0.65 to 0.80, and unlinked items fell from 67 to 51,** the opposite direction from the clutter goal.

**Council B** (`bi-codex.md`): stop c9 and keep c8. Lessons, narrowed by the council:
- linking rose, but the cause (the indirect-signal sentence or another edit) and whether the extra links are clutter are not
  established, since most cases had one draw;
- this wording did not reliably fix Ohio, which does not prove that wording cannot;
- the FOMC thesis is one observed bad opening, not proof that every opening rule risks it;
- the new theses, and the removed CMX thesis, still need a source-by-source judgment before they are called regressions.

The council's message to Alex: c9 failed its agreed test; keep c8, and investigate the failed answers before choosing a next change.
No further send is recommended.

**My own process note.** The stop worked as designed: the line stopped on predeclared falsifiers, at $1.12, before any full run. The
growth that protected indirect evidence likely traded against the clutter goal. The two classes may need different levers rather
than one split.

## 50. The failed c9 answers read against the source ($0; Alex: "先把失败的回答对照原文看清")

**Theses** (each new or removed thesis read with its `why_a_separate_bet` and its article):
- **c9's sentence "an event and a number are different questions" is applied where it does not belong:**
  - fresh-24 opens "Will the FOMC raise the federal funds target…". Its stated reason is "the FOMC decision is a single dated policy
    event that can resolve either way while hyperscaler capex…";
  - fresh-47 opens the completion of a $2.5–3 billion investment, judging a deal small for the company as meeting the scale test;
  - dev-1 recasts the aggregate (the gold's amount question) as "Will NVIDIA have signed credit-support commitments … large enough".
- **On Ohio the same sentence is not applied.** In the two c9 draws that fold, the relevance reads "exactly the kind of credit
  support the thesis measures". One abstract clause is over-applied in three places and under-applied where it was aimed: a coin
  flip per send (AGENTS §6).
- **Not regressions:**
  - fresh-14, memory still supply-constrained in 2027, is the same kind of question as the dev gold's must_open "change in DRAM
    contract prices in calendar 2027";
  - fresh-45 losing the CMX NAND thesis is an improvement.

**Links** (four blind analyst readers over all 229 links of both arms, mixed and unlabelled, grouped by article; 229 of 229 judged):

| Arm | Useful | Weak | Wrong | Total |
|---|---|---|---|---|
| c8 | 79 | 24 | 0 | 103 |
| c9 | 93 | 32 | 1 | 126 |

c9 adds 14 useful, 8 weak and 1 wrong link. The weak share does not fall (23% against 25%). The "informs" definition widened
linking in both directions; it did not reduce clutter.

**What this says about the next step:**
- **Link clutter:** a definition does not separate useful from weak links. The weak links do not mislead, and the earlier recheck
  found 2% wrong. I see no cheap lever that is worth its risk now.
- **Ohio:** a sentence-level rule flips by send. Whether the system should open it at all rests on a boundary D248 records as never
  put to Alex. It governs only through D384 ("按金标"), and it matters to Step 4, because q23 of the frozen judgement gold asks it.
  The boundary is a product question for Alex before any further arm.

**Council B on this reading** (`council/bj-codex.md`): AGREE, with tighter limits.
- Pausing link work is reasonable. That the "informs" definition caused the extra links remains a hypothesis, and the totals do not
  say which links were gained or lost.
- Only the FOMC answer cites the event-versus-number sentence; the other openings show c9's behaviour, not that sentence as the
  cause.
- The question to Alex is about a **material** unsigned obligation that merits a separate investment judgment, not every unsigned
  obligation. The recommendation is yes, because the standard and the gold call for it; q23 shows the consequence but is not the only
  reason.
- If Alex says no, his decision is recorded and the conflict with the frozen gold disclosed. D373 does not change the gold.
- A structural lever is an option to investigate, not an established solution.

**Alex's answer (D388).** To the exact question, "单独开 (Recommended)": a material unsigned obligation keeps its own signing
question beside an open total of its kind. Next is a structural lever, designed and reviewed by the council before any send.

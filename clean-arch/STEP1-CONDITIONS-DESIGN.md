# Step 1 conditions: design draft v8 for council review

**Status:** draft v8 for review. It is not adopted, and no code or prompt has changed.
- Reviews so far: v1 `m-codex.md`, v2 `n-codex.md`, v3 `o-codex.md`, v4 `p-codex.md`, v5 `q-codex.md`, v6 `r-codex.md`, v7 `s-codex.md` (all in `step1-unfiled-2026-11-08/council/`).
- Precedence over §§2–9: §15 (v8) first, then §14, §13, §12, §11 and §10. **The probe's c1 arm is §§2–3 as amended by §§10–15**; wherever §10.6 names its sections, read §§10–15.

## 1. What Alex decided (2026-11-08)

- "我觉得财务类型不应该是thesis，而更多的是条件。观点应该是独特的view，而不是喊出来的数字，除非有理由 - 这个理由恰恰才是观点".
- On the recommendation "keep a useful financial figure that no view takes in the company's conditions record, labelled actual,
  guidance or expectation, with who said it and the period; it becomes evidence when a related view opens and the reference when views
  are judged": **"好"**.

The decided points are:
- A thesis is a view with a reason. A financial measure's level or growth alone does not open one; a measure with a reason can.
- A **useful** company financial figure that no view takes is kept as a condition. This amends D209 for such figures only; other
  no-home statements are still dropped.
- When a related view opens, the kept figure becomes its evidence.

The four case rulings (`LOG.md` §11) are worked anchors, not universal rules.

## 2. The structural choice: a condition is an evidence item with a condition label

v1 proposed a separate `conditions` array. v2 instead adds one optional object to each evidence item:

`condition`: null, or
- `measure`: the measure as stated;
- `period`: as stated;
- `value`: as stated, with unit;
- `kind`: actual, guidance, estimate or balance (a point-in-time amount);
- `basis`: scope and qualifications as stated, such as GAAP or non-GAAP, segment or whole company, currency, conditions attached.

Everything an evidence item carries stays as it is: summary, verbatim passages, original party, reporting speaker, tier, statement
date and date text, evidence period, and links with relevance. So the existing checks, Step 2 and the grouping library apply unchanged.

The one behavioural difference:

| Item | Links | What happens |
|---|---|---|
| With a `condition` | none | **kept as a condition** of the entity: not dropped, filed under no thesis |
| Without a `condition` | none | **unfiled and dropped**, as today (D209) |

A mixed statement (a figure and a claim about a driver) is one item, with its `condition` filled and its links to the views it informs,
so nothing is recorded twice and nothing is lost.

**Which figures are useful** is the model's judgement, by the existing evidence test in the closing check (an analyst following the
company would write it in this week's notes; repeated common knowledge and retold background are noise). There is no measure list
(AGENTS §2: code owns identity, never importance). Cash flow, like any measure, is kept when it passes that test in its context.

## 3. Step 1 rules (request changes)

- **§3, what a thesis is.**
  - "Big matters include the quantities that carry the company's value (…)" becomes "the quantities that carry the company's value
    (…) are what views move".
  - A view is a question whose answer turns on a reason that can move the company's revenue, profitability, cash, credit risk or
    competitive position.
  - The analyst may supply the connection, but the reason must rest on the item's facts and may not be invented.
  - A view may precede any consensus.
- **Do-not-open list.**
  - "one quarter's figures or guidance" is replaced by "a financial measure's level, growth or guidance with no reason: record the
    figure as a condition";
  - added: "a measure with a reason the item supports is a view (for example, margins fall because input costs cannot be passed
    on)".
- **Schema.** The optional `condition` object, with its field definitions beside the fields.
- **Closing check, one readback row.** Each company financial figure kept carries its `condition`. It is linked only to views it
  informs, and it opens no thesis on its own.

## 4. Later view → kept conditions (Step 3, at thesis creation)

When Step 3 saves a new thesis, it searches the entity's stored items that carry a `condition` (embedding, the thesis question against
the item text, top 10) and asks Jev one choice question per candidate: does this stored figure inform the new view's reason? The answer
is yes or no, on the same criteria as Step 1 links.
- Each yes adds a link, marked `backfilled`, with Jev's choice as provenance.
- A failed comparison is reported and adds no link; the thesis is still saved.

## 5. Value × reader

| Value | Written by | Read by | Inputs and nulls |
|---|---|---|---|
| `condition.measure` / `period` / `value` | Step 1 | Step 2 search text; Step 4 reference; evaluation | as stated in the passage; never inferred; period null only when the item gives none |
| `condition.kind` | Step 1 | Step 2 (repeat against revision); Step 4 (actual against expected) | enum; `balance` for point-in-time amounts |
| `condition.basis` | Step 1 | Step 2 (a different basis is not a repeat); Step 4 scope match | free text as stated; empty when none is stated |
| `original_party` / `reporting_speaker` | Step 1 (existing) | Step 2 (forecast author against reporter); Step 4 | existing rules |
| `statement_date` / `statement_date_text` | Step 1 (existing) | Step 2; Step 4 | existing rules, including unknown dates |
| `links` (empty allowed with a `condition`) | Step 1; Step 3 backfill | Step 3 storage; Step 4 | empty plus `condition` = kept condition |
| `backfilled` link flag | Step 3 | Step 4; evaluation | absent on Step 1 links |

## 6. State × event (items with a `condition`)

| Event | Transition and write |
|---|---|
| New figure | stored as an evidence group (original record) |
| Another outlet reports the same figure (same party, measure, period, basis and value) | Jev says repeat: it joins the group with its own text and source (grouping decision); best match and earliest tie if several match |
| The same party changes the figure (revised forecast, guidance change, restated actual) | Jev says revision (supersedes): a new group linked as the later version; nothing overwritten |
| An estimate or guidance followed by the actual | different statements: a separate group; Step 4 compares actual against expected |
| Two parties forecast the same measure | different (another party's figure): separate groups |
| The same value and party, but a different basis or scope | different: separate groups (`basis` is part of the comparison text) |
| The same item replayed | idempotent (library replay rule) |
| Comparison failed | refused and reported; not saved (library contract) |
| Write interrupted | one unit per item; replayed safely |
| Concurrent writers | out of scope: the clean store has one writer |
| A view opens later | backfill (§4) links the figures that inform it |

## 7. New path × old checks

| Check | Applies to conditions? |
|---|---|
| Verbatim passage verification | yes, unchanged |
| Unsupported claims in the summary (fidelity review) | yes, unchanged |
| Link ID validation (existing or new) | yes, unchanged |
| Empty links | changes: kept when a `condition` is set; dropped otherwise |
| `condition` field validation | new: measure, period or value, and kind, by schema and code (shape only) |
| Format-failure retry once | unchanged |
| Within-item duplicate rule | unchanged: one measure told in several sentences is one item |

## 8. Prior decisions

- **D209:** amended for useful company financial figures only, by Alex's "好"; otherwise in force.
- **D370:** no preset questions and no report import; conditions are facts from arriving items, not seeded questions.
- **D371:** realised: present and forward financial information is tracked, and no question is opened per line.
- **D208:** not restored; the seeded hierarchy stays retired.
- **D373:** the frozen gold stays unchanged and disputes are disclosed.
- **Grouping and best match:** apply to conditions as to evidence.

## 9. Evaluation

- **The frozen ruler** (golden-v5) is unchanged. Conditions are evidence items, so the existing scorer reads them as kept items; the
  count of kept conditions is reported separately.
- **The new evaluation** needs a sourced, independently reviewed reference before any score:
  - a council-defined rubric anchored on Alex's rulings;
  - two reader families;
  - source-backed adjudication;
  - agreement reported.
- **Probe decision rules** are written with populations (which cases, which items) before the send.
- **Exposure:** both datasets have been seen before, and this is stated with every result.

## 10. v3 resolutions of the v2 review (these take precedence)

**10.1 The comparison path for an item with no thesis.**
- `step2/compare.search` today builds one query per thesis association. For an item with a `condition` and no links, there is no
  association, so search returned nothing and a repeat would be saved as new.
- v3: such an item gets one entity-wide query of its own text alone (the evidence-only query R2 from the Step 2 validation, which had
  the highest recall: 95.9% per association, 113/113 on the deduplicated history), top 10.
- An item that has links and a `condition` gets its association queries plus this one, merged.
- Comparison, best match, ties and saving are unchanged.

**10.2 Backfill completeness and failure.**
- Candidates are every stored item of the entity that carries a `condition`, when there are 60 or fewer; otherwise the top 60 by
  embedding.
- The Jev question is asked in batches of 10.
- A failed batch is retried once (Alex's retry rule). If it fails again, the thesis is saved, the batch is reported as failed with its
  reason, and no link is written. That is the same rule as every other failed call: no side list (D209) and no silent success.

**10.3 Fields and hand-off.**
- **`kind`** is actual, guidance or estimate. A balance (a point-in-time amount) is an actual whose `period` reads "as of <date>". The
  separate `balance` value is removed.
- **The record passed from Step 1 to Steps 2 and 3** carries:
  - `statement_date` and `statement_date_text` separately; `run_forward.step1_records` merges them today, which is fixed;
  - the `condition` object;
  - the source identity: article sequence, input id, publisher, publication date and title.
- **Readers:**
  - Step 2 search text: summary, passages, party, dates, and the condition's measure, period and basis;
  - Step 2 piece text: the same plus kind and value;
  - Step 3 library: everything;
  - Step 4: the condition and source identity;
  - evaluation: everything.

**10.4 Events added.**

| Event | Handling |
|---|---|
| Retry after a failed comparison | retried once; then refused and reported, not saved |
| A run that ends with items unprocessed | reported in the run's outcome as not processed |
| A date, configuration or input changes between runs | a corrected input is a new item id (identity rule); a configuration change is a new run, not a replay |
| A link half-written | the item's group, links and backfill links are applied as one unit in memory |

The probe's library is **in memory**: crash recovery and persistence are out of scope for the probe and belong to the storage design
(PRD §6: physical storage is open). This limitation is stated with every result.

**10.5 Checks, stated as the code does them today.**
- Step 1 `validate` records an unverifiable passage and an unresolved link as issues; it does not refuse the item. Conditions follow
  the same.
- **New, owned by code (identity):**
  - shape: `measure` and `value` non-empty strings; `kind` in the enum; `period` and `basis` strings or null;
  - **the figure appears in its passages:** every digit group of `value` occurs in one of the item's verbatim passages.
- If either fails, the `condition` is invalid. The item is then treated as plain evidence: kept only if it has links, and the reason is
  recorded.

**10.6 Probe: populations and decision rules, fixed now.**
- **Arms:** a fresh k6b control and c1 (§§2–3 and 10), on the same 16 dev cases (`step1-unfiled-2026-11-08/cases.json`), 3 draws, about
  $1.25.
- **The decision is made on these, all required.**
  1. **Metric-only theses:** new theses whose question is a financial measure's level, growth or guidance with no reason in the
     question. Counted by both reader families with source-backed adjudication, and by my own reading. c1 ≤ control, and c1 = 0 in at
     least 14 of 16 cases.
  2. **Anchored outcomes,** on the cases matching Alex's rulings:
     - d1-40, d1-57: margin and guidance kept, as a condition or as linked evidence;
     - d1-66, d2-66: the analyst EPS forecast kept;
     - the target price dropped in the same cases;
     - d2-8: no supplier thesis;
     - empty-40, empty-57: the reported quarter's revenue kept as a condition, with no revenue-growth thesis opened.

     c1 holds them in at least 2 more answers than the control, and holds no anchor less often.
  3. **Frozen ruler, with the D373 disclosure:** helpful at least the control's minus 1, counting conditions as kept; noise no higher
     than the control's.
  4. **Format:** every answer passes, under the retry-once rule.
  5. **Views:** small theses that both readers agree on not above the control's; wrong links not above the control's.
- **The existing scorer reads conditions** because they are evidence items in `kept`. A unit test proves it: a condition with empty
  links is in `kept`, and the scorer counts it.

**10.7 What makes a reason a view.**
- The reason must rest on the item's facts.
- It must say how something will move a quantity that carries the company's value.
- It must pass §3's existing scale test (it can change revenue, profit, cash or credit risk).
- Later evidence must be able to make it more or less likely.
- An ordinary explanation of a past number ("revenue rose on strong demand") is the figure's context, kept with the condition, not a
  view.

## 11. v4 resolutions of the v3 review (these take precedence over §10)

**11.1 Later linking: complete, with recovery.**
- **Candidates are every stored item of the entity that carries a `condition`**, with no cap, asked in batches of 10. Jev costs about
  $0.04 per million input tokens, so a few hundred items cost cents.
- **Each judged (thesis, item) pair is recorded with its answer.** That is a processing ledger, not a holding area for evidence.
- **Failure:** a batch that fails twice leaves its pairs unjudged. They are retried whenever the same thesis is next written to (new
  evidence linked to it), and at the next run's start. Until judged, they are reported as pending in the run's outcome.
- **A new stored item with a `condition`** goes through Step 2 itself (§10.1), and its own Step 1 links cover the open views. The
  backfill covers only views opened after the item was stored.

**11.2 The value check: exact identity.**
- `value` must be copied **verbatim from a single passage**: after whitespace is normalised, it is a substring of one verified passage
  of the same item. Its schema description says so.
- Otherwise the `condition` is invalid. The item is treated as plain evidence (kept only with links), and the reason is recorded.
- Unit conversion is never inferred.
- This replaces §10.5's digit-group check.

**11.3 One view definition**, consistent with §3. A view is a question whose answer turns on a reason, resting on the item's facts,
that can move the company's revenue, profitability, cash, credit risk or **competitive position**, and that later evidence can make
more or less likely. §10.7's wording "a quantity that carries the company's value" is widened to this.

**11.4 The evaluation, fixed before the probe.**

**The anchored-outcome reference** for decision rule 2: each matching case, its expected outcome, and the source of that expectation.

| Case | Expected outcome | Source |
|---|---|---|
| d1-40 | the gross-margin figure kept (a condition, or evidence linked to an open view); no margin-only thesis | Alex, LOG §11 (margin) |
| d1-57 | margin and guidance kept as above; no margin-only or cash-only thesis | Alex, LOG §11 (margin); §3 rule |
| d1-66, d2-66 | the analysts' EPS forecast kept; the author's target price not kept | Alex, LOG §11 (EPS and target) |
| d2-8 | no thesis on the small supplier's expansion | Alex, LOG §11 (supplier) |
| empty-40, empty-57 | the reported quarter's revenue kept as a condition; no revenue-growth thesis without a reason | Alex, LOG §16–17 |

**The metric-only thesis rubric** for decision rule 1, given to both reader families verbatim: a new thesis is metric-only when its
question asks whether a financial measure's level, growth or guidance holds, rises or falls, and names no reason that could move it. A
named mechanism is not metric-only. Disagreements go to two adjudicators with the source; an unresolved item counts against c1.

**Combining draws:** every threshold is on the sum over the three draws per arm, with the answer as the unit (48 answers per arm). A
failed answer counts as failing every rule it touches.

**The scorer:** the build includes a unit test, written and passing before any send. A condition with empty links is in `kept`, and
`score_gold_runs.clean_statements` and `score_probe` count it. The probe waits for that test.

## 12. v5 resolutions of the v4 review (these take precedence over §§10–11)

**12.1 The value check, with numeric boundaries.**
- After whitespace is normalised, `value` must occur in one verified passage of the same item. The occurrence must not be preceded by
  a digit, a decimal point or a digit-grouping comma, and must not be followed by a digit, or by a decimal point or comma that is
  followed by a digit. So "2.1" does not match inside "12.1" or "2.15".
- **Real-data check before the probe:** the check runs on every company financial figure in the stored K6b dev answers (`gold-k6b-flash`
  d1), with `value` taken verbatim from its passage, and on 20 hand-made wrong values (shifted digits, other figures of the same
  passage). The result is reported: valid formats rejected (target 0) and wrong values accepted (target 0).

**12.2 Anchors that test the rulings as decided** (replacing the §11.4 reference table). These are council decisions under Alex's
delegation, read in their matching contexts.

| Case | Expected outcome (per answer) | Source |
|---|---|---|
| d1-40 | the gross-margin figure is **linked to the open revenue view** (clean-11), as evidence or as a linked condition; no margin-only thesis | Alex: margin "留，归到已有的收入观点" |
| d1-57 | margin and guidance linked to clean-11; **the operating-cash-flow, free-cash-flow and cash-balance figures are not kept** (neither condition nor evidence); no margin-only or cash-only thesis | Alex: margin ruling; cash "丢掉" in this context |
| d1-66, d2-66 | the analysts' EPS forecast kept (linked to the open revenue or earnings view when one is open, else a condition); the author's target price **not kept** | Alex: "留 EPS 预测，丢目标价" |
| d2-8 | **the small supplier's expansion not kept**, neither as a condition nor as evidence; no supply thesis | Alex: supplier "丢掉" |
| empty-40, empty-57 | the reported quarter's revenue kept as a condition; no revenue-growth thesis without a reason | Alex, LOG §§16–17 |

Each row is judged per answer by code where code can (presence, links, the absence of items whose passages are the named sentences)
and by reading. The named source sentences for each case are fixed in `anchors.json` before the send.

**12.3 Draw rules.**
- **Rule 1, metric-only theses:** a case passes for an arm when **all three** of its answers have no metric-only thesis. c1 passes rule 1
  in at least 14 of 16 cases and in no fewer cases than the control.
- **Rule 2, anchors:** the count of answers meeting their anchor row, summed over the draws. c1 must reach at least the control's count
  plus 2, and must meet every row in at least as many answers as the control.
- **Rules 3–5:** sums over the three draws, as in §10.6.

**12.4 Later linking is tested deterministically, not in the probe.** The probe is fixed-state, so backfill never runs in it. Before the
probe, unit tests with a fake Jev prove:
- every stored condition is offered;
- a yes adds a link marked `backfilled`;
- a twice-failed batch leaves its pairs pending and they are retried on the thesis's next write;
- a judged pair is never asked again.

The forward run that follows a passing probe reports, per new thesis, the conditions it backfilled and the pairs left pending.

**12.5 Prerequisites before any send**, each written and passing:
1. the scorer unit test (§11.4);
2. the value-check real-data report (§12.1);
3. the backfill unit tests (§12.4);
4. an **independent review of `anchors.json` and the rubric** by one reader from each family, who did not write them, against Alex's
   words. A disagreement is settled before the send.

## 13. v6 resolution of the v5 review (this takes precedence over §§10–12)

**The blocker:** the value check cannot tell that a figure belongs to its stated measure. A passage that holds operating cash flow of
50.3 and free cash flow of 48.6 would pass 48.6 filed as operating cash flow.

**Resolution: split identity from meaning, as AGENTS §2 and §7.1 require.** Code checks only structure and counts; meaning is judged by
a reader who did not write the change.

**Code (identity), as in §12.1:**
- `value` occurs, with numeric boundaries, in one verified passage of the item;
- the shape is valid.

**This proves the figure is quoted, not that it is paired with the right measure.** The §12.1 target for "other figures of the same
passage" is withdrawn, because code cannot meet it. The real-data report keeps only the other targets: valid formats rejected, and
shifted or absent digits accepted, both 0.

**Readers (meaning)**, a new decision rule 6 for the probe:
- Every condition in every c1 answer (all of them, not a sample) is checked by both reader families against its passage.
- They check whether the measure, period, value, kind and basis are as the passage states them: the value belongs to that measure,
  for that period, as an actual, guidance or estimate, on that basis.
- Disagreements go to two adjudicators with the source. An unresolved item counts as mis-paired.
- **Pass:** mis-paired conditions are at most 2% of all c1 conditions over the three draws, and none of them is in an anchor case's
  named sentence.

The fidelity review the clean path already runs on summaries is the same kind of check, and it stays.

**Downstream guard:** Step 2 compares on the full statement and passage, not on the condition fields alone (§5, §10.3). A mis-paired
field therefore cannot by itself merge two different figures, and Step 4 reads the passage beside the fields.

## 14. v7 resolution of the v6 review (this takes precedence over §§10–13)

**The blocker:** a mis-paired condition can still be written, and the claim that Step 2 is not misled by it was unproven.

**Resolution by construction: the condition fields never enter Step 2.**
- §10.3's addition of the condition fields to Step 2's search text and piece text is **withdrawn**. Step 2 builds both from exactly what
  it uses for evidence today: summary, passages, party and dates (`compare.doc_text`, `compare.query_text`, `compare.piece_text`,
  unchanged).
- A wrong `measure`, `value`, `kind` or `basis` therefore cannot change which candidates are found or how Jev answers. The search query
  and the Jev request for an item are **byte-identical with or without its `condition` object**.
- **A unit test proves it:** an item and the same item with a deliberately mis-paired `condition` produce identical search texts and an
  identical Jev request. It is a prerequisite before any send.
- §10.1's no-thesis search uses the same evidence-only text.

**How a mis-paired record is handled:**
- It is stored as written. There is no silent repair: code cannot know the right pairing, and inventing one would be the model's
  error replaced by code's guess.
- Its passage is always stored beside it, and **Step 4's interface reads the passage with the fields** (a requirement on Step 4's
  design).
- Its rate is a measured quality bar: decision rule 6, at most 2% mis-paired, with none in an anchor case's named sentence. A higher
  rate fails the probe; it is never a reason to adjust the rule.
- The same holds for an evidence summary that misstates its passage today, which is the clean path's existing fidelity risk, measured
  the same way.

**What is now owned where:**

| Concern | Owner |
|---|---|
| The figure is quoted | code (§12.1) |
| The figure is paired with the right measure | readers (decision rule 6) |
| A condition cannot affect Step 2 | construction plus a unit test |
| Repeat or revision | Step 2 on the full statement, as for evidence |
| Reading a condition for a judgement | Step 4, passage beside fields |

## 15. v8 resolution of the v7 review (this takes precedence over §§10–14)

**The blocker:** `compare.piece_text` cuts the joined passages at 600 characters. With the condition fields kept out of Step 2 (§14), a
figure, period or qualification past the cut would be invisible to Jev, so a revision could be merged as a repeat, or a repeat missed.

**Census on the stored dev items** (`step2-validation-2026-11-07/items.json`, 282): 44 items (16%) have joined passages longer than 600
characters. The longest is 1,441 and the median 296. This is a **latent defect of the existing Step 2 for evidence as well**, not only
for conditions.

**Resolution: Step 2 sends the full passages.**
- `piece_text` drops the 600-character cut, for every item, evidence and conditions alike.
- The search text (`doc_text`, `query_text`) already uses the full passages.
- Cost: at most about 1,500 characters per candidate, ten candidates per request, at Jev's rates: cents per run.
- This changes measured Step 2 behaviour. **Step 2's three lines are re-measured** in the forward run that follows a passing probe, and
  the earlier Step 2 result (lines 1 and 3 met, line 2 missed by one merge) is read as measured with the cut.

**The isolation test, corrected.** On the same path (an item with no links, using the evidence-only query of §10.1):
- the item with a correct `condition`, and the same item with a deliberately mis-paired one (another figure of its passage filed under
  its measure);
- they produce byte-identical search texts and a byte-identical Jev request;
- **and** the Jev request contains the item's full passages (a test item longer than 600 characters).

It is a prerequisite before any send.

**The prerequisites before any send, complete list:**
1. the scorer unit test (§11.4);
2. the value-check real-data report (§§12.1, 13);
3. the backfill unit tests (§12.4);
4. the isolation and full-passage test (§15);
5. `anchors.json` with its named sentences, and the metric-only rubric, independently reviewed by one reader from each family against
   Alex's words (§12.5).

## 16. Arm c2 and its prompt audit (2026-11-08; this takes precedence over §§2–3 and §§10–15 for the prompt and the record shape)

**Why c2.** c1 failed (step1-unfiled LOG §20). The reflection council (LOG §21) agreed on the smallest change, audited first.

**The record shape changes from one `condition` to a list of `figures`.**
- In probe 4, c1's single condition forced a statement with several measures to be split into one-figure items. Items sharing a
  source passage with another item rose from 2 of 178 in k6b to 18 of 225 in c1.
- The split margin item was then left unlinked. In k6b it rode inside the revenue item, under the revenue view.
- The standard's unit is one statement per item (K6b §4, the closing check's same-fact row, D250). The gold's d1-62 item holds revenue
  guidance and margin guidance together.
- So `figures` is a list, and a statement with several figures stays one item. Code keeps an item with empty links when at least one
  figure is valid: its value must be quoted, with numeric boundaries, in a verified passage. `runner.py` has 3 tests, and all 4 mutants
  were caught.

**c2 against k6b (system +995 characters; closing unchanged).**

| # | Change | Source |
|---|---|---|
| 1 | Role: "A figure of the company's own financial performance is the exception: it is kept as a condition (section 2)." | Alex, "好" (LOG §17) |
| 2 | §2 CONDITION bullet, described below | D371; Alex's "useful" (§17); his cash ruling (§11); K6b row 8 |
| 3 | §3 big matters: the clause "the quantities that carry the company's value (the segment that carries the business, gross margin, capital spending)" is **cut** | Alex's reframe (§16) and margin ruling ("no separate margin thesis") |
| 4 | §3 do-not-open: "one quarter's figures or guidance" becomes "a financial measure's level, growth, margin or guidance for any period, on its own" | Alex's reframe; the standard's §4.3 (quarterly figures and guidance open no question) widened to any period by his words |
| 5 | Schema: `figures` (a list, may be empty) before `links`, with field descriptions | identity and shape, enforced by code |

What row 2 says:
- A performance statement lists its figures.
- It is linked like any statement, and kept with empty links when no thesis covers it.
- "Useful" is judged in context, with cross-domain examples:
  - conditions: a retailer's same-store sales, an airline's cost guidance, and consensus EPS for a bank;
  - not a condition: a cash-rich company's cash balance or operating cash flow when nothing bears on its funding or credit;
  - a condition: a heavily indebted company's cash burn.
- The share price, a target price and other companies' figures are not conditions.

**Not changed:** K6b's linking ("every thesis it informs"), the separate-bet test, the obligation rule, the closing check. c1's
sentences "a measure with a reason the item supports is a view" and "big matters include a reason" are **not** carried.

**Audit: probe 4's failure classes against the c2 request.**

| Failure class (probe 4) | c1 sentence that produced it | Standard or Alex's line | Verdict on c1 | In c2 |
|---|---|---|---|---|
| Cash kept against Alex (d1-57: 0/3 dropped; buybacks kept; FCF kept in d1-62 and empty-62) | CONDITION: "a statement of the company's own financial figure … carries a condition … kept"; the accounts quote it 3/3 | Alex keeps a **useful** figure (§17) and drops cash (§11); D371: the model judges relevance | keeps wider | "Useful" judged in context, with a not-kept cash example and the opposite case; a buyback stays unfiled under K6b's do-not-open row and the evidence test |
| Margin not under the revenue view (5/6 → 1/6) | closing "linked **only** to theses whose reason it informs" (accounts 3/3), plus the single condition forcing splits (2 → 18 shared passages) | Alex: keep it under the revenue view; K6b: link to every thesis it informs; one statement per item | keeps narrower; structural | "only" is gone; `figures` keeps the statement whole |
| Figure-only theses (k6b empty-57: margin theses 3/3, cash-flow theses 2/3) | K6b's "big matters include the quantities … gross margin …" | Alex's reframe; margin ruling | contradiction (present in K6b too) | clause cut; do-not-open row covers any period |
| Extra theses (networking 3/3, supply commitments 3/3, Microsoft 1/3) | c1 §3 "a reason that can move …" and "a measure with a reason … is a view" (empty-62 d3 cites it); networking accounts cite K6b's separate-bet test | D248 granularity; the general-risk row | widened (supply); not established (networking) | c1's sentences not carried; networking watched in the probe |
| Small supplier opens a thesis (3/3 in both arms) | K6b: "opens a thesis only when its own scale can change …" | Alex: drop | misread (both arms) | not targeted by c2; recorded |
| Format failure (1/48: `condition` missing) | the required nullable field | — | not the prompt | `figures` required, may be empty; production retries once |

**Alex's rulings walked through c2 ($0, reading as the model reads):**
1. **Cash (d1-57).** The figures are the company's own. Nothing in the item bears on funding or credit, so the cash example points
   to not a condition. K6b's evidence test then leaves them unfiled or links them. Risk: the model links cash to clean-1 (credit
   support), as k6b did once. Watched.
2. **Margin.** The revenue guidance and the margin guidance are one sentence, so they stay one item listing both figures, and K6b's
   broad linking puts it under clean-11. The d1-40 margin is its own sentence: linking depends on K6b's "every thesis it informs"
   (k6b 2 of 3 linked it inside a combined item). Watched.
3. **EPS forecast** (d1-66, d2-66). Consensus EPS is named as a condition in the bullet's examples (a bank). It is kept, linked or
   with empty links. The target price is named as not a condition.
4. **Small supplier** (d2-8). Untouched by c2: it is expected to stay as in k6b, which is wrong. Recorded, not targeted.
5. **Reframe** (empty-40, empty-57). No figure-only thesis: the clause is cut and the do-not-open row covers any period. The figures
   become conditions.

**Diagnostic falsifiers** (LOG §21, fixed before any send):
- margin under the revenue view at least 4/6;
- cash dropped at least 2/3;
- at most 1 extra thesis against the fixed set;
- gold not-kept at most the control + 3;
- 0 figure-only theses in empty-40 and empty-57;
- EPS kept at least 5/6;
- a failed answer counts as a failure;
- every figure's measure, period and value read.

## 17. Alex's second amendment of D209 (2026-11-08; precedes §§1–16 where they differ)

Alex chose "先存着，有观点再挂": every statement the model returns as material is kept. A statement no thesis takes is stored, unlinked,
in the company's record, and linked when a covering thesis opens. Only what the closing check rejects is dropped. Consequences for this
design:
- The keep rule no longer depends on `figures`. `figures` remain the record of the company's own useful financial figures, read by
  Step 4.
- §11.1's later linking covers every unlinked record, not only those with figures.
- The prompt's unfiled sentences change from "does not store it" to "keeps it in the company's record", and a ruled-out cash statement
  is "not returned".
- Source: step1-unfiled LOG §27.

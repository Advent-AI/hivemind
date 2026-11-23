# Council gj: challenge round on the next step (read-only; do not edit files or run model calls)

Claude's reflection, written before reading yours, is `clean-arch/step1-unfiled-2026-11-08/council/gh-claude.md`. Read it now.
We agree on the direction: Step 4 is next; the open contract is how a question the system opened becomes a judgeable object without
changing what it asks; nothing is built before Alex's word.

## Facts I verified that your read did not have (challenge each)

1. **Prior art the design does not quote.** `docs/prd/11-production-experiments-from-split.md`, E3: the sealed split (D378) ran a
   separate call that wrote new questions with ladders. Its record: a ladder present in 21 of 44 on the same request; inverted
   ladders; a "within 5%" band that missed its bounds; a rung holding no value; "Checks, not wording, are the part to port"
   (`split.ordered_ladder`, `band_problem`, `empty_rung`, `render`, `shared_key` exist in
   `/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/`). E4: 18 of 25 judge refusal errors are a theme written into
   `cites_views`. D186 with D368 item 1: rungs against guidance with a favourable end, "built in the next extraction version".
2. **Where the ladder call's inputs live.** A thesis's library state holds description, entity, id, outcome, period. `opens_as` and
   `settled_by` are only in `trace.result` of the opening article. Counted on the 34: binding_obligation 7, product_node 6,
   shared_quantity 13, policy_stage 8; period null 0, with an ISO date 5, prose only 29.
3. **Theme mechanics.** `judging.themes_in_force` and `queued_by_change` key on `object_kind == 'theme'`. The seeds file has seven
   theme views under theme objects (v8 is `chip-export-controls`). The clean path has no theme object. If the 21 shared-quantity and
   policy theses are stored as themes, every asset judgement carries the theme block, a changed theme queues every open asset thesis,
   and E4's refusal class applies; stored under the company, none of that happens.
4. **A known-answer control exists.** `clean-arch/unseeded-2026-11-10/mapping-runs.json`: 16 of the 34 theses were matched SAME to a
   ruler question by the frozen MATCHING-v2 reading (q07 ×3, q08 ×3, q18 ×3, q09 ×2, q13 ×2, q04, q16, q23), and their ruler-ladder
   answers agreed with the gold 16 of 16 (`result.txt`).
5. **The census packet is built ($0):** `clean-arch/step4-2026-11-10/census/packet.md` and `packet.json` (builder beside them): the 34
   theses, each with its Step 1 fields, its opening article's full text and the 79 evidence statements that article linked to it.
   Four cases I traced by hand: u1 clean-2 (Ohio: "sign … and at what amount"; no amount stated anywhere; ISO check date; one yes/no
   ladder loses nothing an analyst could settle), u1 clean-4 (worded "will it reach $1 trillion", outcome a number; references $650bn
   and $1tn in the article; due "when the four report", no date), u1 clean-7 (a number with reference $119bn; due "next annual report,
   likely early 2027"; which end is good for the business is unclear), u2 clean-10 (HBM: a capacity number with no figure in the
   article plus a price state "through late 2027"; two things, no date).

## Where I disagree with you

- **Your falsifier is not usable.** "One thesis that needs an invented date, a reference, or a changed question overturns the design."
  The count is already above zero (29 periods are prose; u2 clean-10 has no reference figure). The census cannot be pass or fail on
  zero. Its job is to size each class and to give each class one of three answers: settled by a decision in force (which), a product
  choice for Alex (with a lean), or an outcome the ladder step reports and does not hide (no ladder, with its reason).
- **"Finish the contract and the tables" is not yet a test.** Alex asked for the next implementation step. I propose the step and
  its test below.

## Proposed next step (challenge it)

**The ladder step, built first and tested alone; the frozen judge second.**

Contract, v2 outline:
1. **Call:** once per newly opened thesis, at its opening article. Input: the thesis fields Step 1 wrote (description, outcome,
   period, opens_as, settled_by), the opening article's text and date, the company and a code-built fiscal-year note
   (`universe.fiscal_note`). Nothing later.
2. **Rules:** v74i's lines 20–26 and the bounds sentence of line 35, quoted; every reference to a field the call does not have
   (ticker in `object`, measure, scope, period_start) is cut, and each cut is listed beside its line.
3. **Answer (strict schema):** either a ladder — `settles` (the one number or one event), `left_out` (parts of the thesis's wording
   the ladder does not settle, empty when none), `kind`, `question`, `rungs` (label, condition, lo, hi), `due_day`, `due_day_basis`
   (stated in the thesis | a calendar or fiscal period end | an expected publication day the article does not state), `year`,
   `reference` (the neutral comparison quoted from the article, or null) — or `no_ladder` with a reason.
4. **Code checks:** `check_ladder`, `normalise_ladder`, `check_bounds`; due day a real date after the article's day;
   `check_admission`'s 18-month limit for a binding obligation; the split's `empty_rung` and `band_problem`. One resend on a refusal,
   then the thesis stays unladdered and is counted.
5. **Compound theses:** this version writes the ladder for the one thing `outcome` and `settled_by` name and records the rest in
   `left_out`. No split: a second view would have no Step 1 thesis and no links, and D38's "two views joined by a dependency" needs
   dependencies nobody has built (D368 item 2).
6. **Themes:** the ladder call decides asset or theme by v74i line 22; a theme is stored with `object_kind` theme, so the frozen judge
   runs as production runs it (D191, D195), and refusals of E4's class are counted.
7. **Dependencies:** none, as production's default path gives an article-opened thesis none today.
8. **D186:** not in this version; put to Alex as a choice with that lean.
9. **Model:** `gpt-6-luna` with the strict schema at medium effort (the judge's setting), one configuration.

**The test, on the three stored draws, in two stages frozen together:**
- **Stage 0 ($0, before anything is asked of Alex):** two blind readers of different families fill a fixed form on the 34 packet
  cases (one thing or several; yes/no or number; due day stated, by rule, by expected publication, or none; asset or theme; a
  reference figure in the article, quoted, or none; favourable end clear or not; can one ladder ask the thesis's question without
  changing it). A third reader decides disagreements. Its counts size every class above.
- **Stage A (34 ladder calls, cents):** every thesis ends as refused (with the check), or written; two blind readers judge each
  written ladder against the thesis and the article on the same form's classes.
- **Stage B (the frozen judge through the adapter, well under $1 a draw):** every judgement of every laddered thesis is read as
  SUPPORTED, UNSUPPORTED or INSUFFICIENT EVIDENCE against all evidence linked by that day; arithmetic and the D260 fields are marked
  apart; refused judgements, unjudged theses and stopped draws are counted.
- **Control:** on the 16 matched theses, the answer on the system's own ladder is read against reader B's gold range.

## Questions

- (a) Compound theses: do D38, D248 and D388 settle "write the ladder for the settling outcome and record what is left out", or is
  that Alex's choice? Give the counterexample among the 34 where it produces a wrong question.
- (b) Themes: is storing the system's shared-quantity and policy questions as themes required by D191 and D195, or does the clean
  PRD §7 ("input selection … open") leave it to Alex? What object id does a clean theme view carry, and which reader of `object_id`
  breaks on it?
- (c) `left_out`, `due_day_basis` and `reference`: required fields that force a decision, or extra jobs in one call? Which would you
  cut?
- (d) Porting the split's two checks now, or first counting what they refuse on stored production ladders (E3's own cheapest proof)?
- (e) The control: are 16 matched theses (ten yes/no) enough to carry the "cannot pass empty" requirement? What must the lines be so
  that Stage A and Stage B can each fail?
- (f) What is the single result in Stage 0 that should stop the ladder step before Alex is asked?

Under 1,200 words. Cite a file and line for every fact.

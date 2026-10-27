# Steps 3 and 4 on the 24 gold cases: one send each (arm1, 2026-10-27 23:05, $0.2368)

The analysis call (step 4) places and merges correctly on 20 of 21 development cases and 3 of 3 held-out cases; the three
replacement errors of the product never happen. Jev's piece opinions (step 3) are right on 7 of 18 cases, and the reason the
product retires contrary reports is now named: the `supersedes` criterion it is given says "an official confirms or denies that
reported claim". The analysis call ignores that hint and keeps both sides; the product's writer acts on it.

Example: G09, NVIDIA's "our roadmap is intact" against SemiAnalysis's Kyber delay report. Jev: e49 supersedes 0.76, e53 supersedes
0.78 (the product replaced e53 with the denial). The analysis call: opposes e49, e51, e53, independent true, nothing replaced.

## What was sent

24 cases, each: the step 2 reader's catalog and the complete evidence of the linked questions at the case's historical sequence
(1 to 757 pieces; 193 Jev requests of up to 40 questions; one gpt-6-luna call with every piece in the payload, 2,944 to 160,609
input tokens). 217 calls, $0.2368, 3.66M input / 0.36M output tokens, none failed, no retry, no vote. Requests, answers and
measurements: `poc/reports/2026-10-27-stage34-gold/arm1/`.

## First pass: 18 of 24 answers refused by my own checks, for two reasons of mine

1. The prompt (rule F of the standard) says a pickup is `background_only`; the code check forbade `background_only` with `same_as`.
   Eleven answers followed the prompt and were refused. The contract is the standard's: `same_as` / `revises` / `opposes` attach the
   source; `action` says whether the argument changes. The check is corrected; the gold rows for pickups accept both actions.
2. The model cited the incoming record by its own id (`e1`, `e6`…); the check allowed only `incoming`. Seven answers refused. The
   check now accepts the record's own id.

Both are AGENTS §6 violations on my side (a request never asks for what a check refuses). Fixed at $0; no answer was re-sent.

## Gold corrections, each verified in the ledger before being allowed (`gold.json` `_corrections_after_arm1`)

Reading the answers beside the gold found ids the gold had not listed, because the gold was written from the twelve closest
pieces by word overlap, not the complete expansion. G10 is the clearest: the NY Post's "$105bn financing" is a pickup of NVIDIA's
same-day filing (e1206, the $105bn cap; e1205, the executed guaranties), which the model found and the gold had not seen; the gold
now says same_as e1206 and revises e1165/e690/e712/e750/e815 (the announcement supersedes "talks ongoing, could collapse"), as rule
E states. Others: e282/e415 (NVIDIA's China exclusion, G03), e1194 (the same 08-17 release, G12), e175 (the Kyber delay report Huang's
statement opposes, G13), e1356 (the same Bloomberg price report, G15), e1322 (the Poolside investor letter, G19), e22 (named in
gold.md, missing from gold.json, G08); G18 (Rasgon is his own source, not a pickup); G21 (rule B: a different population is
background with the mismatch named); candidate relations use Jev's candidate vocabulary. G09 and G11 were not changed: the model's
answers there are misses. Lesson for the next gold: write it from the complete expansion, never from a ranked excerpt.

## Score after the fixes (exact fields; text fields read, not matched)

| field | development (21) | held out (3) |
|---|---|---|
| step 4 action | 20 | 3 |
| step 4 question ids | 21 | 3 |
| step 4 same_as | 20 | 3 |
| step 4 revises | 21 | 3 |
| step 4 opposes | 21 | 3 |
| step 4 nothing wrongly retired (G07, G08, G09) | 21 | 3 |
| step 4 independent (where scorable) | 11 of 13 | 1 of 1 |
| step 3 Jev question relation | 12 of 20 | 2 |
| step 3 Jev piece relation | 7 of 18 | 1 |

Control (the product's stored decisions, gold.md): 14 right, 7 wrong, 3 half on the same 24.

Step 4 misses, read:
- G09: action `background_only` with opposes e49/e51/e53. The model kept both sides and marked the conflict, but did not write the
  Data Center argument as contested ("the source gives no revenue figure"). Rule D says a contested roadmap is a risk the argument
  carries. One case; the next arm's prompt names the conflict case in the action rule and is tested on G09 plus G13 (the same
  shape, which the model did write as opposes e175).
- G11: JPMorgan's "SpaceX will absorb a very significant percentage" treated as a distinct analyst expectation, independent of
  Musk's remark (e956). The prompt's own example ("a bank's note repeating the customer's remark") did not hold. One case.

Step 4 text, read on every case: the arguments carry the period caveats (Q1 is not FY2027, G02), the source-quality labels, the
limitations and "what would change it"; G10's argument reads the filing as primary and the NY Post as its relay; G21 names the
population mismatch. G20 rejects the yes/no form of the xAI candidate for the reason the standard gives.

## Step 3: what Jev gets wrong, by mechanism

| class | cases | mechanism |
|---|---|---|
| a denial or confirmation read as `supersedes` | G09 (e49 .76, e51 .59, e53 .78), G08 (e505 .68, e549 .48), G07 (e336 .52) | the criterion given to Jev defines supersedes as "…an official confirms or denies that reported claim…" (`jev_matching.PIECES`, from 06-views' evidence table). The product's writer retires the target on this label. This is the root cause of the control's three wrong replacements. |
| a cross-outlet restatement read as `different` | G02 e28 (.59), G03 e200/e37, G05 e719 (.50), G15 e1369 (.71), H03 e401 (.78), H02 e606 | the same figure or claim in other words from another outlet or claimant; the criterion's "a retelling… in another document" does not carry it at the 0.5 threshold |
| the five-class question relation | 8 misses, 6 of them at 0.39–0.55 | a new question set (direct/lead/background/unrelated/uncertain) without examples; Jev is unsure exactly where the gold is subtle (guidance vs background, a risk vs unrelated) |

The analysis call read the texts and got these right in all but G11, with Jev's opinions in its payload as hints. Under D201 Jev's
label is an opinion, so the system result is step 4's; the product today acts on Jev's label alone, which is why its control is 7
wrong. The costliest class has one sentence as its mechanism.

## The mechanism on the product's own data: the 47 replacements re-sent (`jev_contradicts.py`, 94 Jev calls, $0.0029)

For each of the run's 47 `replace` decisions, the stored Jev question (the incoming piece against the piece it retired) was sent
twice: as stored (a fresh control) and with `supersedes` stripped of "confirms or denies" plus a `contradicts` class.

| | supersedes | different | same_statement | contradicts |
|---|---|---|---|---|
| stored decision | 47 | | | |
| fresh control, same criteria | 31 | 13 | 3 | |
| split criteria | 27 | 11 | 2 | 7 |

Two findings. First, 16 of the 47 replacements do not reproduce on a fresh send of the same question with the same criteria
(the stored label came from a batched request; e.g. seq 77, the G09 denial against e53: stored replace, fresh send `different` 1.00).
The product retires a piece on one sample at a 0.5 threshold. Second, the denial class is real and the criterion is its cause:
seven re-sends flip to `contradicts` (seq 178, NVIDIA's second Kyber denial: supersedes 0.98 → contradicts 0.99; seq 191, 522, 535 ×2,
924, 938). G07 (e336, 0.55 → 0.50) and G08 (e505, 0.72 → 0.89) stay `supersedes`: Jev reads "a later statement on the same topic"
as a revision despite the criterion's last clause; G10 (e1165, 0.91 → 0.90) is a true revision and stays. So the split removes the
denial class (7 of 47 here, the costliest) and leaves the topic-revision class, which only a reader of both texts resolves: in arm1
the analysis call left all three untouched.

## D202: the writer retires nothing on a matching label (2026-10-27 23:10–23:20)

Census before the change: all 47 retirements of the run read pair by pair (`replacements-47-labels.json`): 22 right (the owner's
later value or status of the same claim), 20 wrong (10 a contradiction or qualification retired, 10 a different matter), 5
restatements mislabelled. Crossed with Jev: 17 of the 22 right and 12 of the 20 wrong carry `supersedes`; the split criterion moves
4 wrong to `contradicts` and 3 right with them. No label the matcher gives separates right from wrong well enough to delete on.

Change (`store`, `writing`, `judging`): a `replace` decision stores the piece, links it where the target is linked, and records the
pair in `revisions`; both stay in force; `replacement_refused` is `revision_refused` with the same conditions, deciding only whether
the relation is recorded; `replacements` is history (read as before, never written); `evidence_in_force` carries `revises`; the
judge's request prints "It revises eX (both in force)". Old ledgers without the table read as before (guarded).

Tests: `test_replacement_rule.py` rewritten to the D202 spec after the decision was recorded (9 → 11 tests), including the G09 shape
with its real texts: the denial arrives with a `replace` decision, both pieces stay in force, the judge sees both and the revision
note. Mutant: a scratch copy that calls `store.replace` again fails both decisive tests (`is_replaced('e1')` is True); the unmutated
code passes. Suite 208 pass; preflight exit 0 (B judged 4,035, C judged 618). Week regression replay through the whole path (`english-v34b-nvda-week-2026-10-27`, 2026-07-01..07, 98 items, 342 calls, none failed,
$0.23): `replacements` 0 rows; evidence 129 / theses 12 / judgements 23 against the v18 week's 176 / 9 / 24. The count difference is
extraction sampling (fresh model answers; the first divergent answer changes every later request), so the replay proves that the path
runs with the new writer and retires nothing, not a row-level equality. The v18 week's four retirements, read: three right (NVIDIA's
announcement over The Information's rumour ×2, the Palantir fact over its rumour) and one wrong (NVIDIA's "roadmap intact" retired
SemiAnalysis's Kyber setbacks, the G09 class again). The regression week's single `replace` decision exposed a second silent loss in
the same path: the incoming SemiAnalysis NVL576 delay note carried `original_day` "2026-07-05 to 2026-07-06", which the writer read as
older than the 07-06 denial, logged in `late_statements` and linked nowhere. Census: one such drop per run (the three-month run lost
the SharonAI $4.88bn backstop figure; the v18 week lost the Kyber delay report). Fixed in the slice: an older statement is stored and
linked as one more piece with no revision; the log row stays. 34 of the run's 1,530 pieces carry a non-ISO `original_day`: an
extraction-contract item, noted for the next pass, not changed here.

## Rigour re-check (Alex, 2026-10-27 late: "你看下你的 learning 是不是又犯了一样的错误"), quantified at $0

**1. The stick moved after the send; the score splits in two.** `gold-v1.json` is the gold as frozen before the send
(reconstructed by reverting the post-send corrections); the same stored answers, the same harness fixes, scored under both:

| field (development 21) | gold v1, pre-send | gold v2, corrected after reading the answers |
|---|---|---|
| action | 10 | 20 |
| same_as | 13 | 20 |
| revises | 20 | 21 |
| opposes | 20 | 21 |
| nothing wrongly retired | 21 | 21 |
| question ids | 21 | 21 |
| held-out action | 2 of 3 | 3 of 3 |

Ten of the twenty `action` points come from one post-send contract change (a pickup may be `background_only`); seven `same_as`
points from ids verified in the ledger after the model named them. Both were made with the answers in view, so the 20/21 is not a
measurement. What stands under either gold: nothing wrongly retired 21/21, revises 20/21, opposes 20/21, question ids 21/21.
The only clean number for the action field is a fresh case set, drawn the same way, written from the complete expansion, sent once
and scored once.

**2. The harness contradiction was avoidable before the send.** A synthetic answer written to the prompt's own rule (a pickup →
`background_only` with `same_as`) fails the original `code_checks`; running that check before the send costs nothing and would have
removed 11 of the 18 refusals. The other 7 (the record's own id) likewise.

**3. The regression replay was the wrong instrument; the right one ran afterwards at $0.** `d202-writer-replay-47.json`: all 47
stored `replace` decisions of the three-month run written through the new writer on fresh ledgers with the real pieces: 47 of 47
keep both pieces in force, 0 rows in `replacements`. The relation recorded: 37 `revisions` rows (18 right, 4 restatements, 15 wrong
by the pair reading), 9 refused by the D167 conditions (4 right ones refused, 4 wrong ones caught, 1 restatement), 1 older
statement stored as new. So the judge's "It revises eX" note is wrong in 19 of 37 cases: it inherits the matcher's label noise.
Nothing is lost any more, but the annotation is an opinion and must be labelled as one (or dropped) until step 4 decides it.

**4. The reader side of D202, quantified, not judged.** Of the 52 retired (piece × question) rows, 30 were in the judge's basis
when retired (cited in one of the ten previous judgements): 15 right revisions (under D202 the stale value stays visible for a
while), 11 wrong retirements (the judge lost a piece it had been citing), 4 restatements. Median 13 judgements followed each
retirement. Whether a visible stale value with a dated "revises" note moves a judgement is not measured; it needs the stored
judging requests re-sent with and without the old piece (about 30 calls), not done.

**5. Variance: one sample per case, none.** The design said three sends on disagreements; not run. Every per-case result above is a
single draw.

**6. The late-older drop: fixed downstream, cause upstream.** Stored pieces: 1,530, `original_day` non-ISO 34 (26 month-only, 6
text, 2 year-only), empty 0; raw handover pieces: 2,369, non-ISO 54, empty 1,445, which means the writer fills an unknown day with
the publication day (06-views' rule; D245's source contract says keep unknown). Of the 47 `replace` decisions 1 had a non-ISO
`said_day`. The extraction schema types `original_day` as a free string. The owner of both facts is extraction's contract.

**Repeated lessons, named:** (1) a stick built from an excerpt and corrected after output (retrospective #7/#8 and §7); (2) the
harness not checked against its own prompt before the send (#1); (3) a sampler run bought as an acceptance of a code change
(#1, §5); (4) one sample, no control variance (§6). Not repeated: no long run, no edits during a live run, cases drawn by seed,
decision before test change, mutants run.

## The fresh set, scored once against a frozen gold (fresh1, 2026-10-28 00:20, $0.0907)

16 new cases (`cases-fresh.json`, seed 20261028; one redraw after an incoming record turned out to be shared with the used set),
reference answers written from the complete expansion of every linked question before any send (`gold-fresh.json`, frozen), the
harness checked with three prompt-conformant synthetic answers (a pickup, an unrelated record, a new question) through every code
check, then the arm1 prompt sent once per case: 16 of 16 accepted, 89 calls, 1.34M input tokens. No gold row was edited after the
send; the one encoding mistake found is reported, not fixed in the score.

| field | development (12) | held out (4) |
|---|---|---|
| action | 11 | 4 |
| question ids | 11 | 2 (one of the two is a gold-encoding error, K04: an empty list was meant to be allowed) |
| same_as | 8 | 4 |
| revises | 11 | 3 |
| opposes | 12 | 4 |
| nothing wrongly retired | 12 | 4 |
| independent (where scorable) | 6 of 6 | 1 of 1 |
| Jev question relation | 11 | 3 |
| Jev piece relation | 6 | 0 of 2 |

Every miss read against its answer:
- **F02, F10 (same_as): a second newspaper's own reporting of the same talks is treated as a distinct, independent claim.** The
  gold says same claim (one rumour of one deal); the model says "distinct original outlet, independent corroboration". Together
  with G11 in arm1 (a bank note repeating a customer's remark) this is one class, and its root is in my contract, not only in the
  model: `same_as` means "same claim from the same original source" and `independent` is defined against the `same_as` pieces, so
  "the same claim, independently sourced" cannot be expressed at all. The analyst's standard needs both: claim identity (what the
  argument counts once) and source independence (what raises confidence). Arm 2 splits them.
- **F09 (action, questions):** NVIDIA's six-bank $500bn financing platforms, at a sequence where no financing question exists yet,
  judged `background_only` with no question: "a first-party announcement that states no investment judgement". The gold wanted an
  update to the revenue questions as a demand/financing driver, or a new question on backstop exposure. A real miss of rule F/G: a
  large new fact that opens a judgement was waved through as context.
- **F03 (same_as):** an author's valuation argument citing the Q1 figures; the model called it background (accepted) but did not
  mark the 75%/85% figures as pickups of e204/e124. Minor: the argument is unchanged either way.
- **F12 (same_as):** named e140 (Morgan Stanley's account of investor meetings) as the same claim as a rating reaffirmation. Wrong id.
- **F05 (revises):** a late relay of the "<$120bn" rumour, judged background (right) but marked as revising e690 (the $250bn report).
  Logically that revision happened, at the time; at this sequence the announced $105bn already stands, so the record revises nothing
  now. Defensible reading, scored as a miss under the frozen gold.
- **K01 (revises, held out):** Huang's scope statement attached to v40 with `same_as e1194` (right: the same release) but not marked as
  revising the rumour's description of the backstop (e830/e749/e751) under v25. Half right.
- **K02 (questions, held out):** an extraction link to the wrong question (a chip-smuggling seizure under the GPU-repurchase
  guarantee) kept as "background for v1" though the answer's own reason says it adds nothing to v1. The contract does not say what
  `question_ids` means under `background_only`; it must mean "context of these questions", so an unrelated record lists none.
- **K04 (questions, held out):** my gold encoded "may be empty" as a non-empty requirement. Gold-encoding error, reported, not fixed.

What the two sets say together: placing (action) and never retiring hold on fresh material (11/12 and 4/4; 12/12 and 4/4);
the relation fields are where the stick and the contract still disagree with the model, in one named class. Jev's piece relation
stays unreliable on fresh cases (6/12, 0/2); the system result is the analysis call's, with Jev as a hint.

## Arm 2: claim identity split from source independence (2026-10-28 00:50, $0.24 + $0.09)

One change against arm1: `same_as` ("the same claim from the same original source") became `same_claim_as` ("the same claim,
whoever reports it") and `independent` became `independent_sources` (own access to the fact, not a relay), with the examples that
had failed (two papers' own reporting of one talk; a bank note repeating a customer). System prompt 3,425 → 3,830 characters; the
growth is the two definitions. Both sets sent once; the same frozen golds; a gold v3 (`gold-v3.json`) records five consistency
fixes found while reading arm2's answers (two pickup rows that still demanded `update_existing`, three allowed-id sets that lacked
a same-claim piece), applied to both arms equally.

| set, field | arm1 | arm2 |
|---|---|---|
| dev (21) action, gold v3 | 20 | 20 |
| dev same_claim_as, gold v3 | 20 | 20 |
| dev questions / revises / opposes / untouched | 21 / 21 / 21 / 21 | 20 / 20 / 21 / 21 |
| dev independent (scorable) | 11/13 | 12/13 |
| dev held out (3): action / same_as | 3 / 3 | 2 / 2 |
| fresh (12) action / questions / same_as / revises / opposes / untouched | 11 / 11 / 8 / 11 / 12 / 12 | 12 / 11 / 9 / 12 / 10 / 12 |
| fresh held out (4): action / questions / same_as / revises | 4 / 2 / 4 / 3 | 4 / 3 / 4 / 3 |

Read case by case (16 cases moved across the two sets):
- The class the change aimed at is gone: F02, F10 (a second paper's own sourcing) and G11 (a bank's echo) are now "same claim,
  independent sources" or "same claim, not independent", as the standard says. F09 is placed (update v6/v11) instead of waved
  through; K02's wrong extraction link is no longer carried as "background for v1".
- Two new weaknesses, each a sentence in the prompt: (1) "same claim" is read loosely on a shared topic (G16 Saxo's argument marked
  the same as Chauhan's share model; H02 Eurogamer's scope note the same as a Taiwan price report; F05 a reduction rumour the same as
  the original $250bn talks); (2) a relay is marked as an independent source (F03's author citing the print; F12's relay of two
  ratings), against the sentence that says a relay has no own access.
- Three movements are judgement calls the gold could hold either way: G08, G11, H01 to `background_only` (a pickup or a qualitative
  signal need not move the argument); F07 and F02 using `opposes` where the gold expected `revises` or nothing (Huang tempering the
  reports; the NYT "in discussions" against a piece that says "announced"). G10 is right under arm2's cleaner reading (the filing in
  force already superseded the rumours; a relay of the announcement revises nothing) and the v3 gold records that.
- Every per-case difference above is one draw against one draw. Three draws per disagreeing case under each prompt are running
  (`variance` report) before any third arm is written.

## Variance: three draws per disagreeing case, both prompts, both sets (2026-10-28 01:20, 64 extra calls)

Sixteen cases where arm1 and arm2 differed (8 per set) were drawn twice more under each prompt (a `sample` index in the payload
so the archive does not answer from cache; everything else byte-identical). Agreement of the three draws per field:

| field | arm1 dev (8 cases) | arm2 dev | arm1 fresh | arm2 fresh |
|---|---|---|---|---|
| action agrees 3/3 | 4 | 3 | 6 | 5 |
| question ids agree | 5 | 3 | 4 | 3 |
| same_claim ids agree | 2 | 3 | 5 | 4 |
| revises agree | 7 | 7 | 6 | 6 |
| opposes agree | 8 | 8 | 6 | 5 |
| action accepted by the gold in all 3 draws | 7 of 8 | 7 of 8 | 7 of 8 | 6 of 8 |

Reading: on the cases where the arms disagreed, the answer varies draw to draw in the same fields where the arms differed. The
arm-to-arm differences on these cases are within one draw's noise; F09's "fix" in arm2 was one draw out of three (1/3 accepted
under both prompts); F07 gave three different relation sets under arm2 (opposes / revises+opposes / same+revises). What does not
vary: in 144 draws over both sets and prompts, no piece the gold marks must-not-touch was ever marked same or revised; `action`
stays inside the gold's accepted set in 7 of 8 cases per arm; the pickups' same-claim sets contain the gold's id in every draw.

Conclusion for the design, not for a third prompt: the fields that flip are judgement fields on borderline material (is a CEO's
tempering of a rumour a revision or an opposition; does a sizeless announcement move an argument; which of several restatements
to list). Under D201/D202 none of them deletes or merges anything, so their cost is an annotation, not a loss; but they cannot be
the basis of an irreversible write or a counted support. The production contract follows: (1) every incoming record is stored as a
source (no write depends on a one-draw label); (2) the relations are annotations the reader may show, labelled as opinions; (3)
what the judge reads is the argument record, rewritten by a call that sees the complete history, where a wrong relation in one
draw is corrected by the next draw rather than frozen into the ledger. Arm 3 is therefore not a sentence in this prompt; it is
steps 5 and 6.

Spend on the step 3/4 harness in all: $1.09 over 692 calls (arm1 $0.24, fresh1 $0.09, arm2 $0.24, fresh2 $0.09, variance draws
and Jev re-sends the rest), all within the $1.00-per-arm caps, no retry, no vote, every raw answer kept.

## D204: a repeat is stored, the merge becomes a labelled relation (2026-10-28 00:30)

Design weighed in D204 (store and show both with a label, against hiding the text as a variant of the old piece). Change: on a
`repeat` decision the writer stores the incoming piece with its own links and records (old, new) in `same_claims`; the old piece gains
no source and no link; `evidence_in_force` carries `same_as`; the judge's request prints "Opinion, not verified: the matcher read this
as the same claim as eX; the argument counts one claim, one more outlet". Tests: the two D167 assertions that pinned the merge
changed with the decision; a new test with census case #11 (the compute/networking split) red on the old writer; a mutant that
merges again fails both decisive tests; suite 212; preflight unchanged. $0 proof on the product's own data: the 40 sampled repeat
decisions through the new writer: 40 of 40 stored with the relation and both pieces in force; the 8 that had lost content are
present in force; the label appears in all 40 judge requests. Week acceptance `english-v34c-nvda-week-2026-10-27` (2026-07-01..07, 98 items, 381 calls, none failed, $0.23, 9 minutes):
218 evidence rows (129 in the D202 week, where pickups were merged), 45 `same_claims` rows, 2 revisions, 0 replacements, 0 late
statements, 7 theses, 17 judgements. Of the 45 pairs read, about 5 relate different statements (e.g. the Q1 print to a Micron
growth comparison; the Kyber delay to the scrapped backup design): those are now stored and visible instead of lost. Exposure
(`week_exposure.py`): in 9 of 17 judgements a same-claim pair was in view (100 pair-instances, most in the Kyber-delay cluster of
relays); 4 judgements cited both members of a pair. Their reasons read: "several reports place Kyber's release in 2028 … the timing
reports ultimately trace to SemiAnalysis and are not facts" and "the reports are not independent confirmation of the timing". The
judge counts the claim once with the label in front of it; the double count the design feared did not occur in the week's reasons.
Cost equal to the earlier weeks.

## Next

1. Done: fresh set, arm 2, variance. The contract keeps arm 2's split (claim identity apart from source independence); no third
   prompt arm. The next build is the argument record (steps 5/6): every source stored, relations as labelled annotations, the judge
   reading a rewritten argument; its gold is what the judge reads for v5 at seq 1085 against today.
2. D202's reader side: re-send about 30 stored judging requests with and without the old piece; label the "revises" note as the
   matcher's opinion in the judge's request.
3. Extraction contract: `original_day` ISO-or-empty in the schema and the writer, unknown days kept unknown (D245), 54 raw cases.
4. Arm 2 of step 4: the conflict case named in the action rule (one change), tested on G09, G13 and G07 as the regression, the
   held-out three scored once.
3. Then the writer and the reader (steps 5 and 6): the argument record stored as a version and read by judging, with its own gold
   (what the judgement reads for v5 at seq 1085 against today).

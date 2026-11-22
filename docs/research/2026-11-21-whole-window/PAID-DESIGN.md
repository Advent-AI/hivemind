# The paid whole-window comparison of poc-v120 against fresh controls: design, version 7 (D699, D705, D706, D707; for council review)

Version 1 was reviewed in council R round 22 (`codex-r22.md`, NOT READY: four changes), version 2 in round 23 (`codex-r23.md`, NOT
READY: the reading rule and the freshness proof), version 3 in round 24 (`codex-r24.md`, NOT READY: three outcomes per pair, product
against infrastructure failure, decisive gains traced, the worksheet), version 4 in round 25 (`codex-r25.md`, NOT READY: one rule for
credit), version 5 in round 26 (`codex-r26.md`, NOT READY: unquantifiable CPU gains marked together; coverage on the read classes); version 6
passed round 27; the build's reviews (rounds 28–29) changed H3's selection and the packets (§4, H3 and the worksheet); each finding is
answered below (§7).

## 0. What it decides, and what it can reach

It decides whether linking (poc-v120: Jev's link questions version 2; judging-v8's fuller dependency block) makes the linked number
questions' judgements agree over the release window without harm elsewhere: the evidence for Alex's choice whether the linking version
replaces poc-v118 (D699). It is paired on old-2's trajectory (DESIGN.md §1): every request byte-equal to one old-2 sent is answered with
old-2's answer; only the readers' judgements are bought.

**The attainable verdict ($0):** Data Center FY2027 above total revenue FY2027 (`contradictions.py`, calendar dates 07-01..09-20,
parser second version, before hand reading): old-1 11 days of 77, old-2 56 of 73, old-3 1 of 33 (that one a misparse,
`parser-validation.md`). The class occurs and varies widely between draws; old-2's stored path is an extreme and not a fair control.
A linked sequence that reconciles would show near zero; only fresh controls can serve as the baseline.

## 1. Arms (paired by draw n = 1, 2, 3)

- **linked-n:** poc-v120 from an empty store on its own copy of old-2's archive. Its link jobs are answered only by probe draw n's
  answers, matched by request hash (`window_test.probe_answers`; any other link job stops the sequence before a purchase), so its links
  are probe draw n's proposals, now written. Readers in all three draws: v9 (Data Center FY2027, reads v14), v14 (total revenue FY2027,
  reads v8), v16 (total CPU FY2027, reads v14), v21 (revenue growth FY2027, reads v16, and v9 in draws 2 and 3).
- **control-n:** poc-v118 from an empty store on its own copy of old-2's archive, its readers' old judgements retired as below.
- **Fresh judgements, delimited by date (round 22):** a reader's link is written by an article of day D_R (v9, v14: 07-10, seq 148;
  v16: seq 265's day; v21: seq 534's day); its first affected judgement is its first judgement on a day at or after D_R (old-2: seq 167,
  274, 542). Every judgement of a reader on a day at or after D_R must be a fresh answer in both arms: in linked-n because its request
  carries the dependency block, in control-n because the old request family is retired. The old family of a reader is identified by
  reader and judgement day: every archive judge row of that reader (accepted answers, first attempts the stored run refused, and their
  retries) whose judgement day is at or after D_R; archive rows carry no day, so a row is assigned to a day through old-2's
  `judgements` table (accepted rows) and through its request text (the refused first attempts, whose request equals the retry's before
  the correction lines). Every retired row is listed before the send and checked against old-2's judgements by reader and day.
- **old-2's stored path:** a labelled historical baseline, outside the fresh-control figures.
- All six sequences run at once, one paid call at a time within each (July's latch, round 22), one shared reservation ledger at the
  ceiling Alex names.

## 2. Harness rules (July's, `dependency-design/july_test.py`, extended to the window)

- Harness-only marker, the store lock, never resumed; a stop is final, and its verdict follows §4's precedence (a linked double refusal
  fails; an infrastructure stop or a control's double refusal makes the comparison inconclusive).
- **Allow-list before the budget transport, per sequence, under July's latch** (admission and the inner call under one lock; the first
  refusal closes the sequence): a linked sequence may buy only judge requests of its readers on days at or after their D_R; a control
  only the retired readers' judge requests on those days; a link job only from the probe draw. Admission is bound to the replay's
  judging day (the harness wraps `round.judge_day` to know the day of every judge request), not to the request's text. Any other request that misses the archive
  stops the sequence (round 22 found no legitimate non-reader change on this trajectory). The four answers old-2's own run refused are
  given back once each for non-readers, as in the `neither` pass.
- Settlement at published rates with cache writes at 1.25x; reservation from request size (D696).

## 3. The $0 proofs before the send

1. `v120-replay` (done): poc-v120 with each probe draw's own answers meets all 17 link jobs and ends equal to old-2.
2. **Linked dry run per draw** (a fake judge answering readers with markers): committed links equal probe draw n's proposals; no link
   job outside the probe; no circle correction; every non-reader judgement equal to old-2's by question and day in its request and its
   substantive fields (rung, reasons, reference, implied outcome, cites); **freshness checked on the archive side as well as the
   transport side** (round 23: a cache hit bypasses the transport): every reader judgement made on a day at or after its D_R has a call
   id above the copied archive's top, and none before; **the upstream snapshot:** when each reader prompt is built, the harness records
   the judgement id, date, reference and forecast of each question it reads (wrapping `store.current_state` as `judging.build_prompt`
   calls it) and checks the rendered dependency block against that snapshot, never against the final ledger; the cases a same-day
   upstream update, a carried-forward upstream answer (old-2's v14 has ten judgement days with no v8 judgement that day) and a refused
   upstream answer followed by its accepted retry are each exercised; the added days listed.
3. **Control dry run per draw:** the retired rows listed and checked; only the retired readers reach the transport, on the right days;
   every other judgement equal to old-2's by question and day.
4. The stop paths and the latch race, on the window.
5. Price from old-2's archived usage of the readers' days (round 22: 247 judgements, $0.872 a sequence) plus the dry runs' added days,
   prompt growth from the dependency block, retries, and the live reservations, each shown apart.

## 4. Reading rule (frozen before the send)

**Unit:** a calendar date of the fixed window 07-10..09-20 (73 dates); on each, each question's conclusion is its last accepted
judgement on or before the date, carried forward. A date's class comes from the **distinct answer pair** (v9's and v14's answers) in
force that day.

**Hand classification of every distinct pair (round 23):** `contradictions.py` orders the work (definite and ambiguous first); every
distinct pair in all six sequences is read by hand against both answers and classed **definite** (Data Center's annual low end above
total revenue's high end, as each answer finally states its FY2027 forecast), **overlap**, **clear**, or **unresolved** (an answer
states no FY2027 forecast that can be read). A parser class that the reading changes is recorded as a misparse with its corrected
class. Dates inherit their pair's class. Before reading, the pairs are listed per sequence with their date spans.

**Primary line, P, per pair n (round 24: three outcomes):** over all 73 dates, each arm's dates are definite (D), not definite
(overlap or clear, N) or unresolved (U), each date keeping its own arm's class even where the other arm is unresolved. Linked-n's
definite count lies between D_L and D_L + U_L; control-n's between D_C and D_C + U_C.
- **Improved:** D_L + U_L < D_C (the least favourable completion still has fewer definite dates in the linked arm).
- **Not improved:** D_L >= D_C + U_C (even the most favourable completion cannot give the linked arm fewer).
- **Undecided:** otherwise (the unresolved dates could change the result).
- **Testable:** D_C >= 2 (known definite dates of the control over all 73, not only dates readable in both arms).
- **Readable:** each arm has at least 60 of the 73 dates resolved **in the hand-read classes** (before any credit adjustment): a
  coverage policy that deliberately allows at most 13 unreadable dates per arm (82.2%). A readable forecast with unsupported arithmetic
  stays readable; its uncertainty reaches P through the credit-adjusted classes the bounds use.
- **Credit (rounds 24–25; one rule):** a **gain** is a date on which the linked arm is not definite and the control is definite. Only
  gains are ever adjusted; no other date's class changes for credit. When a pair is provisionally improved, **every** gain is reviewed:
  both linked answers in force on it (v9's and v14's), deduplicated by judgement id, are read for July's rule B (arithmetic following
  from stated inputs; each assumption that sizes the result disclosed and supported) and for H4. A gain whose forecasts carry a material
  rule-B failure on which its reconciliation rests earns no credit (counted definite for P). A gain resting on an unsupported CPU
  increment: when the increment can be quantified, the forecast with it removed gives the gain's credit-adjusted class; when it cannot,
  the gain counts unresolved: **every** such gain of the pair is marked unresolved, and the bounds are then recomputed once across the
  pair (round 26: two gains marked one at a time could each look harmless). Each date keeps its actual class in the report beside its
  credit-adjusted class; P is recomputed on the credit-adjusted classes. A confirmed CPU double count stays a harm (H4) whatever its
  date.
- Reported apart, per arm: definite dates that became overlap and those that became clear.

**Harm lines (each checked on all three pairs):**
- **H1, refusals (round 24):** on **matched reader-days** (a reader judged on that day in both arms of the pair), the attempted reader
  judgements and the model refusals among them (first attempts the code refused, terminal refusals included); refusals on linked-only
  propagation days reported apart. Harm at **4 or more** refusals above its control on matched reader-days (3 extra is tolerated).
  Rationale, frozen before the run: old-2's stored run refused 4 of 1,616 judgements (0.25%), about 0.6 expected per ~250 reader-days, so
  4 extra is far above that base rate while up to 3 stays inside ordinary variation. A **linked double refusal** (the corrected answer
  refused again: `judgement_refused_twice` stops the day) is a product failure: the verdict is **fail** whatever else holds; a control
  double refusal makes the comparison invalid.
- **H2, the fixed trajectory:** an unexplained difference in a non-reader request or its substantive output makes the comparison
  **invalid** (not a harm: the paired design no longer holds).
- **H3, sourcing through the link (round 23):** a figure an answer presents as the market's (consensus, guidance, an analyst estimate)
  is followed through the exact request: through the dependency block to the read judgement that stated it, and from there to its dated
  outside statement (a company figure such as Bloomberg's $393B total-revenue estimate reaching Data Center through total revenue is the
  intended use, if it is named as a company figure). A grounding error: a figure supported only by the system's own forecast, or a
  company estimate presented as a segment consensus. **Selection (round 29: the earlier trigger selected 244 of 247 reader answers on
  old-2, since the reference field always speaks of the market):** a structural rule from the exact request, the same in both arms
  (`worksheet.structural_flag`): a reference amount found among the system's own figures in the request (a read judgement's comparison
  point or forecast, or the previous conclusion) and nowhere in the evidence ("own figure as market"); or a part question (Data Center,
  CPU) whose reference names a consensus with an amount found in the evidence ("scope check"); plus every reader answer in force on the
  seven fixed dates below. Every selected row is read with its request, the read judgements it was shown and each read judgement's own
  request (the trace to the dated outside statement), and the paired arm's conclusion in force that day. On old-2's reader answers the
  rule selects 90 of 247 (80 own-figure, 10 scope), many of them cleared on reading (a guide amount written another way, a consensus
  named only to say none is supplied). Harm when a linked sequence has a grounding error whose paired control's conclusion in force on
  that date does not have the same error type.
- **H4, the CPU link:** every post-link v14 answer in the linked sequences is read against the exact CPU conclusion it received and
  its control's v14 answer that day. Double counting the CPU forecast is harm. Its effect on P goes only through the credit rule above.
- **H5, arithmetic and sourcing (July's rule B):** v9 and v14 at seven fixed dates (07-12, 07-26, 08-09, 08-23, 09-06, 09-13, 09-20) in
  all six sequences; the unit is a question-date; Claude reads first, a blind reader second; a disagreement goes to a third,
  source-backed read whose class decides. H5 is a separate paired harm count: a linked sequence with at least 2 more material failures
  than its control is harm. Its effect on P goes only through the credit rule above (a shared error moves no date).

**Verdict precedence:** (1) a **linked double refusal** → fail; (2) **invalid or incomplete** (an infrastructure stop: budget, transport
or harness; a control's double refusal; an H2 difference; an arm under 60 resolved dates) → inconclusive; (3) **confirmed harm** (H1, H3,
H4 double count, H5) → fail; (4) **untestable** (a control with D_C < 2) → inconclusive, "the class did not recur"; (5) **P**: all three
pairs improved → pass; any pair not improved → fail; otherwise (some pair undecided) → inconclusive.

**The worksheet (pinned before the launch; rounds 24, 28, 29):** built by `worksheet.py` from the six stores and archives after the run,
its format and code reviewed and run on the dry outputs before the send, in **two packets**: the P packet (blind: shuffled labels, no
arm name, P rows only) for the blind reader, and the H packet (H3, H4, H5 rows, which reveal the arm through their requests); the gain
packet follows the P reading. `verdict.py` takes the read packets themselves: it refuses unless every expected H row (regenerated from
the stores) carries a valid final finding, derives H1 from the dated judge rows of the six summaries, H3–H5 from the read rows, and each
gain's credit from the reviews of its two supplying answers; it requires all six summaries accepted by the gate, and a linked double
refusal fails before any packet is required. One P row per distinct v9/v14 answer pair per sequence, keyed by
both judgement ids and the pair's date span; it carries both answers' full `implied_outcome` and reasons, and fields for the reader:
the FY2027 low and high ends as each answer finally states them, the excerpt they come from, the class, a note. H3, H4 and H5 rows carry
the exact request text (dependency block marked), the read judgement each figure came through, and the dated source quotes. Worked
example (old-1 09-08): Data Center "$419 billion for FY2027" against total revenue "$414.3 billion ... supports roughly $414–421
billion": low end 419 is not above high end 421, so **overlap**, though the parser took $414.3B and flagged it definite. Claude reads
first; a blind reader (Codex, labels shuffled, key kept outside the repository) second; every disagreement that could change a pair's
outcome, an H3 or H4 finding, or an H5 mark goes to a third, source-backed read whose class decides. Reading load on old-2's schedule:
about 72 distinct pairs a sequence (up to 438 rows, each read twice: 876 classifications), about 213 linked v14 reviews (twice where
an H4 finding is made), 168 H5 marks (84 question-dates twice), the H3 traces, and the full gain review (both supplying answers of every
gain, deduplicated), before adjudication; the dry review counts each reader's rows apart; estimated 8–12 hours of reading across the
readers, apart from the run's three hours.

**Reported beside, not gating:** each link's relation, direction and sign (the weak CPU link disclosed); self-made references
(`reference_census.py`'s measures, the `unsourced` scan with the dependency block excluded); v14 linked against control; v21's implied
total against v9 and v14; linked-only judgement days.

## 5. Cost (estimate; the ceiling is Alex's)

Reader judgements from their links, at published rates from old-2's archived usage: $0.872 a sequence (247 judgements, round 22).
Linked sequences: about 19 added judgement days each (round 22's count on the fixed schedule; the dry runs give the exact count) and
the dependency block's prompt growth (about 10%): about $1.05. Three linked and three controls: about $5.8, plus retries and refusals
(about 5%) and the live reservations (one judge call per sequence at once). Priced exactly from the dry runs before the ceiling
question.

## 6. Time

One paid call at a time per sequence: about 270–300 calls; old-2's stored reader calls took a median 38.2 seconds (round 23), so about
3 hours with replay and retries, the six sequences at once.

## 7. Round 22 findings and where they are answered

1. Fresh judgements by date, request families, latest available upstream conclusion, the stored refusals: §1 (fresh judgements), §2,
   §3 items 2–3. 2. P on annual ranges, carry-forward, coverage, all three pairs, outcomes for every case, the parser validated on
   flagged and unflagged stored answers: §4, `parser-validation.md`. 3. H4 on every post-link v14 answer; H3 traced outside the
   dependency block; H5 with an effect on the verdict; per-link report; refusals with a denominator, stops apart: §4. 4. July's latch:
   §1, §2, §6.
Round 23: freshness on the archive side, admission bound to the judging day, the upstream snapshot at prompt construction with its three
cases: §2, §3 item 2. Every distinct pair hand-classified, misparses recorded, carried-forward dates: §4. Paired rates on jointly
readable dates of the fixed 73, unresolved dates unable to reverse, conversions to overlap reported apart: §4 P. H3 traced through the
link to the outside statement: §4 H3. H1 second refusal, H2 invalidates, H4 and H5 consequences in P, disagreement resolution,
verdict precedence: §4. Time: §6.
Round 24: three outcomes per pair from two-sided bounds over all 73 dates, the floor on known control dates, 60 stated as a policy: §4 P.
Product against infrastructure failure, matched reader-days, the H1 tolerance's rationale: §4 H1 and precedence. Credit only for gains
that pass rule B, the CPU increment shown removed or the pair undecided, H3 triggers on amount, scope or attribution against the
control's conclusion in force: §4. The worksheet, its worked example, adjudication for P, H3, H4 and H5, reading time: §4.
Round 25: every gain of a provisionally improved pair reviewed, both supplying answers, deduplicated by judgement id; only gains
adjusted, by one credit rule; H4 and H5 reach P only through it; H1's boundary stated (harm at 4); reading load counted per reader:
§4. The harness review will run two $0 verdict checks: a pair whose control has 2 definite dates and the linked arm none (both gains
reviewed, withdrawing both gives a tie: not improved); a material error shared by both arms on a clear date (no change to P); the same
pair with both gains resting on unquantifiable CPU increments (both marked unresolved together: D_L + U_L = 2, not below D_C = 2:
undecided). Round 26: every unquantifiable CPU gain marked unresolved before one recomputation; coverage on the hand-read classes, the
bounds on the credit-adjusted ones: §4.

## 8. Staged send (D708, council round 31)

Pair 1 (linked-1, control-1) is registered as pair 1 of this comparison and sent first, its two arms together, on the pinned graph and
retirement plan; its stores, archives, snapshots and summaries are kept. Its reading (`worksheet.py build-pilot`, `verdict.py --pilot`):
the blind P rows of both arms read by hand and bound to the stores' pairs; H4 on every post-link v14 answer of linked-1; H1 from the
dated summaries; the gain review when the pair is provisionally improved. The pilot's decision, by §4's precedence: a linked double
refusal fails; an invalid run, coverage short or control-1 under 2 definite dates is inconclusive; an H1 or H4 harm stops; "improved"
after the gain review continues to pairs 2 and 3 and the full reading (pair 1's remaining readings done then under the same rule);
"not improved" or "undecided" stops, each with its reason. The pilot never gives the comparison's pass, which needs three pairs. H3's
selector and H5's duplicate counting (round 30) are fixed before the full reading, not before the pilot. Pilot cost about $1.96; the
ceiling is Alex's (about $2.50 proposed).

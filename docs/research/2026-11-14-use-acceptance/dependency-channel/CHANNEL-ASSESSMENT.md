# Does D368's dependency channel convey anything in a real, correctly directed case? (D533, under D439), 2026-11-15, $0

Outside PRD 10's filing work. Script: `channel_assessment.py` (`channel-d1.json`). Run read: the first frozen seeded draw of
2026-11-03 (`poc/data/e2e-r9-frozen-v108-2026-11-03/d1`: the frozen configuration with its 22 preset questions, July window). Nothing
was sent, nothing was judged again, nothing is built.

## The answer

**Not yet established (corrected after the council's round 25).** The count below is a lead: 8 of the 14 lines hold a figure that
the receiving question's own last request did not hold. But the lines were assembled from conclusions that did not exist when
the receiving request was made: in the stored run the supporting question is judged **after** the question it supports, in the
same day-end round (total revenue at judgement 198, its data-center supporter at 202), and its conclusion had itself read the
supported question's. Feeding it back would be a circle, not the order D368 decides. What a correctly ordered run would show the
receiving judge is therefore a counterfactual these stored outputs do not give. The eight are also edges into only two
receiving questions (total revenue and data-center revenue), not eight questions.

## What was built

The preset questions carry "supports" edges. The stored code reads each edge from the supporting question's side (the supporting
question is shown the supported question's conclusion); D368 (item 4) decides the other reading: the supported question reads the
conclusions of the questions that support it. For each of the draw's 17 edges the script builds the line the supported
question's judge would receive under D368, in the production format (`views/judging.py`: the question, its current band, and the
first 600 characters of its reasons), taking the supporting question's conclusion as it stood at the supported question's last
judgement, and compares the figures in that line with the supported question's own last request.

| | Edges |
|---|---|
| in the draw | 17 |
| a line could be built (the supporting question had a conclusion by then) | 14 |
| the line holds at least one figure | 11 |
| the line holds a figure absent from the supported question's own last request | **8** |

Examples of what would arrive that the receiving request did not hold: from the data-center revenue question to total revenue, a
data-center reference of about $362 to 363 billion and a 92.2% share; from the cloud companies' spending question to total
revenue, spending levels of $765 billion and others; from the credit-support question to total revenue, the $4.88 billion
backstop, a $20.7 billion estimate and 170,000 GPUs; from the China questions to data-center revenue, shares and amounts.

One line as the judge would receive it (the credit-support question, supporting total revenue):

> - v9 (open; last_end) What total amount of financing commitments and capacity backstops to customers and partners will NVIDIA report outstanding at its FY2027 year-end?: now rung 4 Bearish; reasons: No market consensus or NVIDIA guidance for the FY2027 year-end total is supplied, so there is no market-reference forecast to map to a rung. The closest quantified baseline is $3.5 billion of guarantees added by May 2026 (rung 1), but that is a historical subtotal, not a year-end expectation. The evidence implies a materially larger outstanding total: applying Sharon AI’s disclosed $4.88 billion six-year backstop to Firmus’s targeted 170,000 GPUs versus Sharon’s up to 40,000 gives a full-capacity Firmus comparable of about $20.7 billion; adding Sharon’s $

The unsized case the council named (the trial run: the Ohio lease guarantee supporting the credit-support total): the line would
carry the band and the reasons ("The evidence makes a signed guarantee by the due date more likely than not, but does not
establish that it has been signed ...") and no figure.

## Limits

- "A figure absent from the request" is a comparison of number strings; the cut at 600 characters itself leaves fragments (a bare
  "$4"), and a new string may be a known figure in another format. Some of these figures are the supporting judge's own
  derived or assumed numbers (a reference it computed, a discount it chose), not source figures: the channel would carry a
  judge's assumptions upward as well as facts. That bears on the open choice about answers resting on the judge's own steps
  (`unsupported/DESIGN-NOTE.md`).
- The line holds 600 characters of reasons: what lies beyond is cut.
- One draw of one configuration, preset questions only; the default configuration today has no preset questions and writes no
  dependency (D370, D368), so for article-opened questions the channel has nothing to read until the matching step chooses
  dependencies.
- No judgement was re-run: whether the supported question's answer would change, or improve, is not tested.

## The stored chronology for the two receiving questions (D534, part 1; `chronology-d1.json`), $0

Ordered by each judgement's own number (inside a day-end round every judgement has the same sequence).

| Receiving question | Supported by | At its last call (2026-07-14) | And at every call from the second day on |
|---|---|---|---|
| total revenue, fiscal 2027 (`v1`) | 5 questions | 4 supporting conclusions existed already (from the round before); **all 4 had been produced with `v1`'s earlier conclusion in view**; 4 supporters were judged later in the same round | the same pattern: each supporting conclusion that existed before a call had read the receiver's earlier conclusion |
| data-center revenue, fiscal 2027 (`v2`) | 10 questions | 8 existed already; **all 8 had read `v2`'s earlier conclusion**; 8 judged later in the same round | the same |

So in the stored run no supporting conclusion exists that was produced without the receiver's conclusion in view: the stored
order is the supported question first, its supporters after, each shown the supported one's conclusion (the reading D368
replaces). A test of D368's direction cannot be assembled from stored conclusions; it has to produce the supporters'
conclusions afresh, without the receiver's, and then the receiver's with theirs.

The frozen judgement reference (corrected after the council's round 26: my first wording, "from their own figures", was wrong):
for total revenue it uses the consensus, the first quarter's actual and the second quarter's guidance and also data-center,
shipment and Vera CPU evidence; for data-center revenue it explicitly uses its total-revenue view and a segment-share inference.
That is the reference's reasoning; it does not decide the direction of stored dependencies, which D368 does. Agreement with the
reference is the outcome measure of any test, not an explanation of why an answer moved.

## The decided ordering and propagation, exercised with labelled fake outputs (D534, part 2; `ordering_proof.py`), $0

On a scratch copy of the same seeded draw, one extra judging round was run through the production round
(`judging.round_of_judgements`), the edges read in D368's direction for the judging use only (the harness answers
`store.dependencies_of` and `store.dependants_of`; the filing use, `store.direct_parents`, is left alone). One supporting question
(`v6`, which supports data-center revenue, which supports total revenue) is marked as changed; every judgement output is a labelled
fake. Seven expectations were written into the script before the run; it exits with an error if one fails.

| Expectation | Held |
|---|---|
| the chain is judged supporters first (`v6`, then `v2`, then `v1`) and nothing else is judged | yes |
| the first supporter is not shown the question it supports | yes (it is shown only its own supporter) |
| data-center revenue is shown its supporter's conclusion of this round | yes, beside its nine other supporters' stored conclusions |
| total revenue is shown data-center revenue's conclusion of this round | yes, beside its four other supporters |
| no question is shown a conclusion of a question it supports (no circle) | yes |
| the filing use of the edges is unchanged | yes |
| a changed conclusion queued exactly the questions it supports | yes |

A mutant that keeps the stored direction fails six of the seven (the supporter is shown the question it supports; the round
fans out to nineteen judgements) and the script exits with an error.

**What this shows and does not (the council's round 26: a bounded wiring result):** with the direction changed, the production round
orders and propagates as D368 describes for this chain, without touching the filing use. It does not show the information free
of circular influence: the other supporting conclusions shown to the two receivers are stored conclusions produced under the
old direction. Shown with fake outputs on one chain and one extra
round, on preset questions: nothing about what real judgements would say, and nothing for article-opened questions, which have no
edge until the matching step chooses dependencies (D368's other part, unbuilt).

## The two checks the council asked for before any measurement design (D535), both $0

**(a) A source-backed, decision-relevant case among the supporting lines** (`line-figures-d1.json`: each figure of the eight lines
looked up in the passages the supporting judgement cites).

| Supporting question → supported | Figures stated in a passage it cites | Figures in no cited passage (its own calculation or assumption) |
|---|---|---|
| data-center revenue → total revenue | none | $362 to 363 billion, $388 billion, 92.2% |
| gross margin → total revenue | 70%, 74.9%, 75% | none |
| cloud companies' spending 2026 → total revenue | $125 billion, $145 billion, $190 billion, $765 billion | none |
| credit support → total revenue | $3.5 billion, $4.88 billion, 170,000 GPUs | $20.7 billion |
| share of accelerator spending → data-center revenue | 70%, 75%, 80% | none |
| China share → data-center revenue | 46% | 1% |
| **stand-alone Vera CPU revenue → data-center revenue** | **$20 billion** | $12 billion |
| Blackwell and Rubin revenue → data-center revenue | none | $305 billion, $326 billion, 84% |

**Correction (same day, before the council read it):** the first case written here, the Vera CPU target of $20 billion reaching the
data-center question, was the wrong pick. The figure is source-backed, but the frozen reference uses it for total revenue, two
steps away (Vera CPU supports data-center revenue, which supports total revenue); its data-center answer does not use it. The
table above also only looks at figures; the reference's facts are not all figures.

**The case, read against the reference's own evidence** (`reference_facts.py`, `reference-facts-d1.json`; statements matched by id,
then every row read in the stored requests and conclusions). The reference answers data-center revenue from ten facts. Over all
14 stored requests of that question (96 distinct statements), the system showed it two of them:

| Fact the reference uses for data-center revenue | Shown to it as a statement | Elsewhere in its last stored request | Under D368's direction |
|---|---|---|---|
| first-quarter data-center revenue, $75.25 billion, 92% of sales | yes (17 statements) | | unchanged |
| SemiAnalysis: second-half data-center compute 20% above consensus | yes (2) | | unchanged |
| the Rubin shipping schedule: full production, first shipments in the third quarter, volume in the fourth | never | nowhere | would arrive if the Rubin shipping question's new conclusion states it, as its stored one does from three cited passages |
| reports of delays across the Rubin line-up | never | nowhere | the same |
| China may allow purchases of the H200 | never | yes: the H200 question's conclusion in the theme block, and the total-revenue line | already arrives; a supporter's line would repeat the theme |
| guidance assumes no China data-center compute revenue | never | in part: the total-revenue line names export restrictions and the H200 approval | the total-revenue line would go; the China-share conclusion states it |
| consensus total revenue of $392 billion | never | yes: the total-revenue line, and its own previous conclusion | the line would go; the previous conclusion carries it at first |
| second-quarter guidance of $91 billion | never | yes: the total-revenue line | the line would go; no supporter's conclusion carries the amount |
| management: growth accelerating toward $100 billion quarters | never | no (its own statements hold a related one: data-center growth guided to accelerate) | no carrier |
| a Rubin rack at about $7.8 million against $4 million | never | nowhere | no carrier (the Blackwell and Rubin conclusion mentions higher pricing, not the figure) |

**What this supports, after the council's round 27 correction** (my first reading counted statements only and said "four facts
would be brought" and "the only sized reference is removed"; both too strong). As statements the question was shown two of the
ten. Counting the whole request, the consensus, the guidance and the H200 permission arrive today through the total-revenue line
or the theme block. Two matters are nowhere in the request: the Rubin schedule with its delay report, and the rack price. D368's
direction could newly bring the first of them, and would end the line that today carries the consensus and the guidance. That is
a source-backed, decision-relevant case for the channel (the Rubin schedule) and a named cost (the reference point's path); it is
not a forecast of either: the stored supporting conclusions are leads, and what conclusions written under the corrected direction
would contain is untested. The reference itself sizes data-center revenue from its total-revenue view at a 92 to 93% share. Eight
of the ten facts were filed under another question, the filing phase's subject (`docs/prd/10-filing-phase.md` §2). For total
revenue, the reference's facts held by other questions (the 20% projection, the Rubin schedule and price, the Vera CPU target)
sit one or two steps away and would arrive only if the data-center conclusion repeats them.

A locating error caught on the way: a first lookup by wording counted two statements "with $392" shown to the data-center question;
they were the statement ids e392 and the like. The lookup now matches by statement id.

**(b) The state of 2026-07-14 before that day's judging round is rebuilt and verified** (`rebuild_seeded_state.py`). From stored
answers alone, with the network refused: the 22 preset questions written by the seeding module as the stored run did, whole days
through the production replay to 2026-07-13, then the 35 articles of 2026-07-14 through dispatch and the item's entry point
without the day's round. One kind of request is not served by the stored archive on purpose (an answer the code's own check
refused is kept under a separate key so that a replay asks again); the harness hands those stored refused replies back as they
were (one in the rebuild, one in the control round), the check refuses them again and the stored retry follows. Result: every
table identical by content to the stored run, except the three that hold the last day's round (the day's completion row, its 19
judgements, its processing record). **The control reproduces:** judging 2026-07-14 from the rebuilt state in the stored direction
returns the stored run's 19 judgements, identical in order, band, reasons, citations and request key.

The stored round of 2026-07-14 is 19 judge calls, 109,803 tokens in and 57,502 out: $0.0397 at the published
rates. Two directions, three draws each, would be of the order of $0.24 (the corrected direction's round may hold a
different number of calls: to be counted on its rebuilt requests).

## The whole round of 2026-07-14 in D368's direction, dry (`full_day_dry_run.py`, `full-day-dry-run.json`), $0

From the verified state, the production day round with the edges read in D368's direction for judging only, every output a
labelled fake that cites every supporter it was shown. Two runs bound the size: 14 calls when no fake conclusion says it changed,
18 when every one does (the stored round: 19). In both, seven registered expectations hold: no refusal; every judgement is a fake
(none answered from the stored archive); every question whose reading changed that day is judged; every supporting question is
judged before the question it supports (11 and 13 pairs); every supported question is shown this round's conclusion of each
supporter judged in the round; no question is shown a question it supports; the filing use unchanged. The judge's own check
accepts a citation of a supporter. A mutant keeping the stored direction fails four of the seven (its first run failed on an
error, not on an expectation: the stored direction's requests are answered from the stored archive; the expectations were made to
catch that and the mutant rerun).

Read in the corrected requests: a supporter not judged in the round is shown with its stored conclusion, written under the old
direction (one says "Dependency v2 implies about ..."), and every supporter's own "previous conclusion" still carries numbers
taken from the question it used to read (the Blackwell and Rubin question: "The current Data Center conclusion implies about
$388B"). A one-day switch therefore starts from old-direction numbers in two places. The frozen judge prompt's consistency rule
holds one example of each direction ("a share cannot be judged at zero while the policy that gates it is judged likely to open; a
component cannot exceed its whole").

## How much room the frozen reference leaves (the stored seeded draws scored as they are), $0

`score_judgement.py` on the three stored seeded draws: 15, 15 and 16 of 17 judged questions agree with the reference at the
window end. Total revenue and data-center revenue agree in all three, on the same band each time. The disagreements are the
custom-chip theme (3 of 3) and the China share (2 of 3); bands differ between draws on four questions, agreement on one. On this
reference a changed reading direction has fifteen agreeing answers to lose and two to gain; the two would each lose a line, not
receive one, and whether that helps them is unknown. The reference does not measure the day-by-day path, where the stored
direction's dependence shows (a total-revenue estimate moving data-center revenue across a band and back on 2026-07-11 and 12:
an observed dependence, not shown to be a wrong answer on either day).

## What was already on record, found late (2026-11-03 and 04)

`docs/research/2026-11-04-filing-end-to-end/core-problem.md` and its independent review `review-core-codex.md` had established,
on these same three draws: that the seed arrows are read backwards; that data-center revenue is sized from the total-revenue
conclusion (checked again today in the first draw: from 2026-07-06 on, all nine of its judgements take the total-revenue consensus
times the first-quarter share as their reference, and on 2026-07-11 and 12 a move of the total-revenue estimate from about $385
billion to about $399 billion took data-center revenue down a band and back while total revenue's own band did not move); that the frozen reference itself computes data-center revenue as total times share, so "total
times share" is not a failure under it; that total revenue already receives several drivers' conclusions through the theme
block (its last stored request shows eight theme conclusions, five of them questions that are also its direct or indirect
supporters); six contracts a fix must settle (filing's use of the edge, cycles across edge kinds, article-opened questions' edges, the
direction label, citations, the 600-character cut); and a bounded test (the 14 days, reading and matching replayed from the
archive, only judging re-run, three draws against a same-day control) with what would make its result misleading. PRD 10 §3
lists the matter as outside the filing phase, "settled by D368 (item 4), its fix to be built and measured"; item 4 was settled by
Claude on Alex's delegation ("好你来定"), not in his own words. This stretch (D533 to D535) re-derived part of that record and
added: the exact rebuild of the state from stored answers, the control reproduced, the two-function seam that changes the judging
use without touching the filing use, the whole-day dry run, and the table above.

## Council round 27 (D536): no measurement of the reversal is sent now

Both shapes were weighed: the one-day switch (about $0.24) keeps old-direction numbers in previous conclusions and in supporters
not judged that day; the 14-day run that re-runs only the judging (feasible: `judging_feedback_check.py` replays the 14 days with
every judgement a labelled fake, and every reading and matching request is still answered from the stored archive, with the same
589 links; about 180 to 216 judge calls a draw) would be clean of that, and would still test a seeded set that today's default
cannot hold, with the contracts for cycles, the edge's meaning, citations, the 600-character cut and closing unsettled. Neither
is sent. D368 item 4 stays a recorded decision (settled by Claude on Alex's delegation, awaiting build and measurement); these
results do not establish that a uniform reversal helps, and it is not replaced by another design here. The rebuild, the seam,
the dry run and the feedback check are kept as that slice's acceptance material.

## What came before any measurement design (council rounds 25 and 26)

Still owed, both at $0: (a) the figures of the candidate supporting lines read against their source passages and the reference,
stated figures apart from a judge's calculations and assumptions, with at least one source-backed, decision-relevant case
identified; (b) whether the state of 2026-07-14 before that day's judging round can be rebuilt and verified against the stored
run (prior judgements, evidence, edges, question states, the day's judging queue; the retired preset questions accounted for).
The old and the corrected direction would then run from copies of that one state, the corrected round producing its own
supporting answers first: a one-day switch on a history made under the old direction, not a two-week run of D368. If the state
or the control cannot be verified, it stops and the mismatch goes to the council; an extra round "as if 2026-07-15" may only be
a separately labelled exploration, never the window-end measurement. A two-sided question is legitimate, with what counts as
harm, benefit or inconclusive registered before any send; three control draws do not by themselves give a non-inferiority margin.

### The earlier list (round 25)

1. (Done, above.) The stored chronology for the two receiving questions. Not done: what the source passages say about each
   figure in the eight lines (which are source figures and which a judge's own).
2. (Done, above.) The decided ordering and propagation exercised with labelled fake judgement outputs; article-opened questions
   stated as an unexercised limit.
3. It stops if the ordering cannot be exercised without changing a frozen piece, if a cycle or an unintended filing change
   appears, or if no source-backed, decision-relevant case can be identified. A measurement, if designed afterwards, must run
   the whole correctly ordered path (the supporting requests changed too), same-day controlled, priced on its rebuilt requests.

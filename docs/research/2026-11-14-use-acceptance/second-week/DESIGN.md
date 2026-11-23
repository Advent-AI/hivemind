# One more week of news through the new system, read for its answer choices: design, third version (D549, D550; under D439), 2026-11-15

A diagnostic of the frozen step that writes answer choices, on news outside the days it was tuned on. It passes no gate:
Alex's lines (D400) are set on 44 topics and three attempts each, and he did not set this sampling. The numbers below are a
scaled, proposed rule of the council's, written before any send. The first version pooled the new week with the fresh week;
the council refused it (`reflection-2/cold-codex-9.md`): the fresh week already holds two agreed faults of a zero-fault line,
so a pooled rule could never be met. The second version judged the new week apart; the council's next round
(`cold-codex-10.md`) corrected its outcome claims, its reading capacity and its budget wording. This is the third.

## 1. What is sent

- **News:** 2026-10-06 to 10-12, 272 articles, in order (`manifest-2026-10-06-10-12.json`; the same set and order through both
  systems' own entries; text identity `659eaeda6f6c9fe1`).
- **The run:** the new system as frozen, through the runner that ran the fresh week, unchanged
  (`clean-arch/e2e-comparison-2026-11-13/run_fresh.py clean --manifest ... --passes 3`, its own root and ledger): Step 1 at c8,
  Steps 2 and 3, the topics as cases, the answer-choice step three attempts a topic, the frozen judge. The judge is kept: the
  unchanged runner is the proved path, and its share of the fresh week's charge was $0.07 of $2.52. No abbreviated harness.
- **A known limit of the unchanged runner:** the first step stops at 300 calls (a frozen limits file). The week needs 272 plus
  retries; the four stored runs used 0 or 1 retries in 235 to 243 articles. A stop there is the run's stop.

## 2. What "unseen" means here, and its bounds

No later week is wholly unseen, so the claim is bounded: **topics opened on articles not found in the exposure search, within
a week that contains previously exposed articles.** The earlier articles can still shape the library and which later topics
open. The search (`exposure_census.py`, `exposure_bounds.py`; 14,408 files, 7.0 GB, by exact article id):

| Class | Articles | How it is handled |
|---|---|---|
| Found in a stored model request, trace or library, a readers' packet, a reference file or a council transcript | 22 (`exposed-2026-10-06-10-12.json`; 7 in a first-step trace) | a topic opened by one of them is reported and left out of both counts |
| Not in any of those, but shown on a review page of the offline source-page work (the page cleaner replayed by code; an id search of that work's one model trace, the 17-article full-page diagnostic, finds none of the week's ids) | 19 (`exposure-bounds.json`) | a topic opened by one of them is in the wider count and out of the strict count |
| A recurring headline whose earlier edition an old run read in August (one a different article under the same title; one a periodic template with new figures) | 2 | as the row above |
| Everything else | 229 | counted |

Not detectable by this search: the same story rewritten under another title and another id. Two of the week's articles are the
same story at two outlets inside the week; that is the library's ordinary case, not an exposure.

**Two counts are reported, wider (250 articles) and strict (229).** If they fall on different sides of the rule below, the
result is inconclusive.

## 3. Price and bounds

- **The run, on its own ledger (estimates, not a guarantee):** from the fresh week's charges ($2.5237 for 235 articles: $2.10
  the first step, $0.34 the matching, $0.02 the answer choices, $0.07 the judge) scaled by article count, $2.91; with the first
  step scaled by text length (1.31 million characters against 1.03), $3.15; from July's dearer charge per article (run c1:
  $2.51 the first step and $0.38 the matching for 243 articles), about $3.39. The ledger also holds reservations for calls in
  flight (the judge reserves about $0.013 a call, up to about $0.2 at once). **Ledger ceiling $3.95**, decided explicitly in
  D550 in place of D549's $3.50: a guard below the plausible charge would cut a nearly finished run and waste the whole
  spend. The ledger refuses any attempt beyond it.
- **The readings, bounded in size, their dollar cost unknown:** reader sessions are not calls on the project's provider; the
  wiring design (D448) set them outside the ledger, and the project's price list holds no rate for the two review tools.
  Whether they carry a charge per token on Alex's accounts cannot be seen without reading credentials or settings, which is
  not allowed. No dollar figure is invented, and **the total spending including these sessions is not claimed to be verified
  within $5.** Their bound is in section 4.
- **Against the limits that are enforceable:** paid model calls under D439 before the run about $18.43 of $40; after it at
  most $22.38. D544's $5 checkpoint on paid calls: $0.0022 used; after this run at most $3.95. **Whatever the result, no second
  week fits in what would remain** (the two other later weeks price at about $4.1 and $5.1), so the direction returns to the
  council after this reading in every case.

## 4. What is read, and the reading's capacity

Every written ladder and every refusal of the three attempts **of every topic the week opens** (the topics left out of the
counts are read too, and reported as description), as in July: packets built by the existing builder (at most 22 items a
packet), two reader families apart with the existing form (`clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md`), one
session a packet; the marks that differ ruled by a third reader of each family; the collector's report. Claude's own marks on
every attempt are written to a file before the readers' answers are opened.

| Topics opened | Items | First-reader sessions | Third-reader sessions | Bound on input tokens (0.5 million a session) |
|---|---|---|---|---|
| up to 7 | up to 21 | 2 | 2 | 2 million |
| 8 to 14 | 24 to 42 | 4 | 2 | 3 million |
| 15 to 22 | 45 to 66 | 6 | up to 4 | 5 million |
| more than 22 | | **not read: the population exceeds the planned reading; returned to the council before any packet is opened** | | |

Comparable single-packet sessions stored in the repository used 0.07 to 0.36 million input tokens (79 to 93% cached) and at
most 3,200 output tokens. A reading is complete only when every item has a valid row from both families and every differing
mark a ruling from both third readers, or is listed as unresolved; no attempt is left unread.

## 5. The rule, fixed before the send (proposed by the council; not Alex's lines)

On the new week's eligible topics alone, `n` of them, three attempts each, in each of the two counts:

- **Too few:** `n` below 6. Nothing is concluded.
- **Clean:** no agreed fault on the four zero-fault lines in any attempt (a question other than the topic's; a part left
  unlisted; an outcome with no range or two; an unjustified refusal); the same favourable end across attempts for every
  company figure; the same due day for at least nine in ten topics; at least `ceil(35n/44)` topics right in two of three
  attempts and at least `ceil(28n/44)` of them right by written choices (at 6 topics: 5 and 4; at 7: 6 and 5; at 8: 7 and 6).
- **Not clean:** anything else, named by its kind below.

The fresh week's seven topics are shown beside the new week with their existing marks and the sensitivity reading of D547;
pooled counts are given as description only and keep that week's two agreed faults.

## 6. What each outcome is evidence of, and what is done next (none passes Stage A; none reverses the direction by itself)

A count of this size describes what was seen; it does not fix a rate or a cause. With the fresh week, a week of 6 to 8 topics
gives 13 to 15 topics from two weeks, which are not independent draws, and July's 11 declined of 40 came from three runs over
the same fourteen days.

| What is seen on the new week | What it is evidence of | What is done next |
|---|---|---|
| Clean, and no topic declined | two weeks outside the tuned days with no refusal and one fault between them. It supports designing an acceptance; it does not settle the step's refusal rate or show that July's problem is gone | the council takes up the design of a reading sized as the first gate's acceptance (its population fixed before any reading; the article database holds only two more later weeks, about 35 topics with these two, short of Alex's 44) |
| A condition or distinction of the topic left out of the choices, agreed by both families | a lead that the fresh week's fault may be a mechanism. Not yet the same mechanism | the source, the request and the model's own account are read for both cases first; a repair design opens only if they show one mechanism on two distinct questions (D545's trigger), and a new version of the frozen step is then its own council decision (D426) |
| A topic declined | a lead only: neither that July's pattern recurs nor that the first step is the cause | each refusal is read against its article and traced (whether the topic was worth a question; which rule the step applied; whether another attempt gave choices); the council reads the result before any stopped line (D473, D477) is discussed |
| Another fault, on one or two attempts (another question asked; an outcome with no range or two; direction or due day not the same) | one case | recorded with its trace and the model's own account; no design from one case |
| Too few topics, the two counts on different sides, more topics than the reading covers, or a zero-fault mark the third readers leave open | nothing about the first gate | said so; the week's library and judgements are kept as material for the later gates; no further week is sent automatically |

## 7. Stops

A failed precondition of the runner (a frozen file changed, a frozen-piece test red); a component that stops after its one
redo; the ledger's refusal; the 300-call limit. Nothing is edited while the run is live. The run is launched detached with a
log and pid file after a network check; its databases are read only after it ends.

# Reflection council "my", round 27: both checks of D535 are done at $0; what they show argues against a send. Review, and decide the next step.

D535 recorded round 26. Everything below is on `docs/research/2026-11-14-use-acceptance/dependency-channel/CHANNEL-ASSESSMENT.md`
(corrected today) with its scripts beside it. Nothing was sent; no package, configuration or frozen file changed; suite 287 green.

## 1. Done since round 26, all $0

1. **The state is rebuilt and verified** (`rebuild_seeded_state.py`). From stored answers alone, network refused: the 22 preset
   questions written by the seeding module, whole days through the production replay to 2026-07-13, the 35 articles of
   2026-07-14 without the day's round. Every table equals the stored run by content except the three that hold that day's round.
   One class of request the archive withholds on purpose (an answer its own check refused is kept under a separate key); the
   harness hands the stored refused reply back, the check refuses it again, the stored retry follows (one case in the rebuild,
   one in the control). **The control reproduces:** the stored-direction round from the rebuilt state returns the stored 19
   judgements, identical in order, band, reasons, citations and request key.
2. **The whole round in D368's direction, dry** (`full_day_dry_run.py`). Labelled fakes that cite every supporter shown; 14 calls
   if no conclusion changes, 18 if all do (stored: 19); seven registered expectations hold in both (supporters first over 11 and
   13 pairs; each supported question shown this round's conclusion of every supporter judged; no reverse line; no judgement
   served from the stored archive; filing use unchanged). The stored-direction mutant fails four. Every reader of the edges in
   judging goes through the two functions the harness answers (`judging.py` lines 109, 171, 210, 254, 269).
3. **The source-backed case, corrected.** My first pick (the Vera CPU target reaching data-center revenue) was wrong: the
   reference uses that figure for total revenue, two steps away. Read against the reference's own evidence
   (`reference_facts.py`, by statement id): the reference answers data-center revenue from ten facts; over all 14 stored requests
   (96 statements) that question was shown two. Of the eight it never saw, D368's direction would bring four through supporters'
   conclusions that state them from cited passages (the Rubin schedule, the delay report, guidance excluding China, the H200
   permission); it brings no carrier for three (the $91 billion guidance, accelerating growth, the rack price); and it
   **removes** the one that sizes the question: the $392 billion consensus is filed under total revenue only and reaches
   data-center revenue today through the total-revenue conclusion. The reference itself sizes data-center revenue from its
   total-revenue view at a 92 to 93% share.
4. **How much room the frozen reference leaves.** `score_judgement.py` on the three stored seeded draws: 15, 15, 16 of 17 agree;
   total revenue and data-center revenue agree in all three on the same band. Disagreements: the custom-chip theme (3 of 3,
   PRD 10's Broadcom case) and the China share (2 of 3, a reader disagreement PRD 10 rules out). A changed direction can show
   harm on fifteen questions and a gain on at most two, neither a question that would receive lines.
5. **The frozen prompt, read for the reversed reading.** Its consistency rule holds one example of each direction ("a share
   cannot be judged at zero while the policy that gates it is judged likely to open; a component cannot exceed its whole"). In
   the corrected requests a supporter keeps its "previous conclusion" with numbers taken from the question it used to read, and
   supporters not judged in the round are shown with old-direction conclusions: a one-day switch starts from old numbers in two
   places.

## 2. An error of process: this was largely on record since 2026-11-03

I did not search the earlier results before D533. `docs/research/2026-11-04-filing-end-to-end/core-problem.md` and its
independent review `review-core-codex.md` had already established on these three draws: the arrows are read backwards; the
reference itself computes data-center revenue as total times share ("total × share is not itself a failure under the frozen
reference"); total revenue already receives drivers' conclusions through the theme block; six contracts a fix must settle
(filing's use, cycles across edge kinds, article-opened questions' edges, the direction label, citations, the 600-character
cut); and the bounded test (the 14 days, reading and matching replayed, only judging re-run, three draws beside a same-day
control) with seven ways its result would mislead. PRD 10 §3 lists the matter as outside the filing phase, "settled by D368
(item 4), its fix to be built and measured". And D368 item 4 is not Alex's ruling on direction: he delegated it ("4. 好你来定");
the direction was settled by Claude "by D208's design", to be "measured before it enters the default". I had described it to you
as decided by Alex. (Second time this lesson: D513.) Rounds 24 to 26 added to that record: the exact rebuild, the reproduced
control, the two-function seam, the whole-day dry run, the by-id table.

## 3. What a send could and could not decide

- **Shapes now possible:** (i) the one-day switch you scoped: two directions, three draws, about 100 judge calls, about $0.24
  (a stored round is 19 calls, 109,803 tokens in, 57,502 out: $0.0397); (ii) the 2026-11-04 test, feasible with the rebuild
  harness if judging does not feed back into the reading requests (to be checked at $0): 14 days, judging only, two directions,
  three draws, about 1,300 calls, of the order of $2.70.
- **Benefit cannot show on the frozen reference** (item 4 above). The reference does not measure the day-by-day path, where the
  stored direction's known cost lies (2026-07-11 and 12: the total-revenue estimate moves from about $385 to $399 billion and
  data-center revenue drops a band and returns; verified today).
- **Harm could show**, and the table predicts where: the data-center question loses its only sized reference. On a one-day switch
  the previous conclusion would mask it; only the 14-day run would show it.
- **It bears on neither system's default.** Today's default writes no edge (`jev_matching` writes `'dependencies': []`); the
  seeded path is retired (D370; the replay refuses a seeded ledger); the clean path has no such mechanism. Whatever the send
  shows applies only after dependency selection (D368 item 2) is designed, built and measured.
- **It does not bear on the lean path's question** (which system carries forward).

## 4. My recommendation, for you to attack

**Send nothing on this line now.** The $0 work answers what round 24 asked: on a real, correctly directed case the channel would
carry four facts the reference uses and remove the reference point; neither direction alone feeds this judge; eight of ten facts
are a filing matter (PRD 10 §2), for which a 600-character conclusion is a lossy carrier. A uniform reversal is not supported by
this evidence, and neither is keeping the stored direction: the earlier review's "typed edges" (a part reads its whole for size;
a question reads its drivers for facts) fits both the reference's reasoning and the prompt's two examples, and is a design
question for the slice that builds dependency selection, not a measurement to buy now. Record: item 4's direction is **not
confirmed** by evidence (and was never Alex's own ruling); the harness (rebuild, seam, dry run) is ready as that slice's
acceptance material; the decision page says so in plain words.

Then re-rank from the goal (D466). My own reading of what is left on the lean path, to argue with: every remaining lead is
either Alex's product choice (which system; what to show when nothing sizes an amount; financial-line questions in the old
system) or a new version of a frozen piece that removes part of its class (D375: one of three duplicate pairs; the clean path's
later-linking exclusion: one of three confirmed pairs, effect on an answer not shown). I do not see a next send that changes the
choice. If you see one, name it with its falsifier; if not, say what the next task is.

Check the facts above against the files before answering (the table especially). End with: "Council position: <...>".

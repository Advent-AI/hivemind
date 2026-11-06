# Split version 2 on the first 100 items: predictions and stop conditions (written before the run, 2026-11-05)

Alex, 2026-11-05: "好，从重复开题开始做;你自己解决当前的所有问题 … 确认尺子和你量测方法没有本质问题，然后开始解决这些问题；我们这次抽取分开成证据和新题目应该要有更好的效果，这个是目标，你要在前100个sample run 里面吧我们的现在的问题解决，然后不要drift from current proto".

Run: `poc/data/split-v2-first100-2026-11-05/`, the stopped run's first 100 manifest rows (76 article items, 08-29 and 08-30 judged, 08-31 cut at row 100), the
same 68-question starting ledger, configuration `poc/config/poc-split-v2.json`. One draw: counts show mechanisms, not a difference between arms
(AGENTS §7.2). Baseline: the stopped run `split-fresh-seven-day-matching-v4-2026-11-05`, its first 100 rows (35 new questions).

Changes against the stopped run (each proved on stored data first; details in `split-v2-design.md`):
1. Every open question before each item reaches both calls (the all-open change made after the stop).
2. Record preparation chooses the subject from the listed ids (kind follows the subject), carries the production ladder rules, and gives a
   calendar-year shared quantity its D197 key.
3. The new-question prompt carries the standard's five reasons and its not-to-open list, names the closest existing question and what
   separates it, and applies the same closing check to its evidence as the evidence call.
4. The matching review sees every open question Jev calls the same, a part or the same quantity for another period, at any probability,
   plus the closest question the proposer named; collision-v4 states D248's same-question tests.
5. The quote check passes the subject's own name (production's D266) and compares hyphen glyphs.
6. A candidate with no source-backed passage is dropped with its reason; a figure for the year after next is not opened.

Predictions (baseline first 100 → this run):
- Questions filed under an unlisted research subject although a listed one fits: about 12 of 35 → at most 2.
- Duplicates of an open question (my reading, then a blind reader against D248): 3 confirmed, 2 likely → at most 1.
- Questions the standard's section 3–4 does not open (outside the five reasons, too small, beyond the year limit, a customer's plan):
  about 15 of 35 → at most 5; new questions about 35 → 12 to 22.
- The baseline's legitimate questions (FY2028 revenue, FY2028 CPU revenue, binding supply commitments, Fed September decision, TSMC 2 nm,
  Broadcom AI revenue, TSMC capex, export controls on robot chips) are opened somewhere in the 100 or covered by an open question; at most 2 lost.
- Numeric new questions with a ladder the code accepts: 0 of 17 → at least 60%.
- Passages per new question from the new-question call: mean about 6, maximum 30 → mean at most 4, no question above 12.
- Quote refusals: 6 → at most 3.

Stop conditions: an item fails (the runner stops itself) → read the trace and fix at that step before anything else; a written question or
evidence row that breaks a code contract → stop; a duplicate of the CPU, Fed or deadline class opens → recorded and traced, not answered
with another run. Estimated cost about $0.7 (stored first 100: A $0.12, B $0.13, record preparation $0.03, matching and two judging days
about $0.35, with larger requests from the all-open context).

## Second run on the final configuration (written before it, 2026-11-05 14:40 PST)

The first run (`poc/data/split-v2-first100-2026-11-05/`) met every prediction above except the ladder share (9 of 20, predicted at least
60%): of the 11 empty ladders, about 5 had no reference in their evidence and 6 had only a quarter's or part-year figure, which record
preparation treated as no reference. A blind reader found 3 of 22 new questions not to open (1 a duplicate) against 24 of 35 before, and
judged 18 of 30 sampled opening passages helpful against 9 of 30. One duplicate the reader did not flag: the Hugging Face acquisition
re-proposed with a later closing date (the review merged it once, kept it apart once).

Changes for the second run, each proved on stored data: the one-deal sentence in A and as the review's example (A proposed the Hugging
Face question 0 of 4 times on 1248 and 1256; review pairs unchanged, 8 of 8 must-stay-apart pairs 3/3 apart); the part-period reference
in the ladder sentence (6 of 6 such questions now carry a ladder the code accepts, 3 of 3 without a reference stay empty); a quote that
differs only by punctuation, including an em dash closed up to a number, is the source passage (stored quotes: refusals 12 → 8, no accepted
passage changed).

Predictions for `poc/data/split-v2-final-first100-2026-11-05/` (one draw): numeric new questions with an accepted ladder at least 60%; the
Hugging Face acquisition is not opened as a second question; quote refusals at most 2; new questions 15 to 25, with at most 4 the blind
reader would not open; at least half of sampled opening passages helpful; no subject filed under an invented id where a listed one fits.
Stop conditions as above.

## Confirmation run (written before it, 2026-11-05 15:25 PST)

The final run (`poc/data/split-v2-final-first100-2026-11-05/`) met: no invented subjects; numeric ladders 9 of 12; the Hugging Face
acquisition not opened twice; passages per new question 3.5 (max 11). It missed two predictions, both traced: 13 new questions (predicted
15–25) — re-sending its stored requests twice opened a question on 5 of 14 lost items' sends, and the model's own account on two of them
quoted "Do not open questions about quarterly figures or guidance" as the reason not to open an annual question whose only figure was
quarterly (D371: a quarterly period is not a reason to withhold information from an annual question); quote refusals 5 (predicted at most
2): 2 correct refusals (a dropped owner's name, a paraphrased first sentence), 1 added connective, 2 code gaps ("28.1 %" spacing; a copied
passage that runs on, kept by production's sift under D266).

Changes, each proved on stored data: the quarterly sentence now says a quarterly figure is evidence for the annual question, which may be
new (the lost items: 9 of 14 sends open an annual question against 5 of 14; four must-not-open items 0 of 8); the quote check leaves out a
space between a digit and '%' and keeps a copied passage that runs on (all 1,357 stored quotes: refusals 16 → 7, no accepted passage
changed, every kept passage is source text).

Predictions for `poc/data/split-v2-confirm-first100-2026-11-05/` (one draw): new questions 15 to 25; the blind reader would not open at most
4; numeric ladders at least 60%; quote refusals at most 3; no invented subject where a listed one fits; no second Hugging Face question;
passages per new question at most 4 on average.

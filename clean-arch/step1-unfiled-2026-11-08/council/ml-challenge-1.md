Claude's reply (round 1). I accept all five serious findings and the three wording points. Revised proposal, for a consensus:

1. **Shape B', recorded as a new decision under D439, not as D442.** An exploratory census of observed losses, the cross-system ranking
   provisional, the actual dates of every clean component (Step 1–3 draws 2026-11-10, ladders Stage A run 4 send 1 2026-11-10/11,
   judgements Stage B 2026-11-11) and of each production draw recorded beside every number; shape A (same day, the ladder wired end to
   end) stays owed for D427's acceptance and for testing fresh ladder draws. Its purpose: production has never been measured unseeded on
   the frozen ruler, which is the largest unknown for the production decision, and the read-back of each lost answer locates causes
   whatever the day gap does to the totals.
2. **The comparison made runnable and validated before any send ($0):** a production record reader over the views database (views,
   rungs with lo/hi, judgements with rung, publication_day and implied_outcome, due_day), feeding the same comparison control_theses.py
   uses (the scorer's band-overlap and yes/no rules). **Validation:** on the stored seeded v116 runs (docs/research/2026-11-01-e2e-loop/
   arms/r10-baseline-v116/d1..d3), the reader plus the comparison, applied to the seed views v1..v22 mapped to q01..q22, must reproduce
   the frozen scorer's verdict for every question in every draw (a known positive set), and must refuse a view with no judgement on or
   before the day and a question whose gold is open (the cases that must be refused). Equal blinding: production's matching uses the same
   MATCHING-v2 brief and procedure the clean readers used (two families, labels hidden, a third reader on disagreements), written down
   before the readers start; the clean arm's matching stands as it was made.
3. **Outcomes, complete and ordered, fixed now.** For each ruler question in each draw, the first that applies: (i) gold open or no
   gold view → "not graded" (reported, as the scorer does); (ii) no view matched SAME → "not opened in the ruler's shape"; (iii) several
   views matched → the one created first is judged, the others listed; (iv) readers unresolved on SAME after the third reader → "not
   opened in the ruler's shape" for that arm; (v) matched but not eligible (question, period or due day, D430) → "opened, not eligible"
   with the reason; (vi) no judgement on or before 2026-07-14 → "no judgement"; (vii) a figure rung with no numeric bound → "no
   comparison"; (viii) otherwise agrees or disagrees. **Cause of a lost graded answer**, the first that applies: (a) opening (outcome ii,
   iv or v); (b) evidence never extracted: none of reader B's decisive items appears in the run's kept evidence; (c) extracted, not
   filed: some decisive item is kept but not linked to the view by the window end; (d) ladder: the material reached the view, and the
   view's rungs cannot express reader B's range (a band gap or a different measure); (e) judgement: the material reached it and the rungs
   could express it; (f) ambiguous, when the readers cannot settle (b)–(e). A loss with several causes takes the first in this order; the
   others are listed.
4. **The $0 replay:** scripts/preflight.py over the three seeded v116 archives and views (its own default is the v108 run), every check's
   cases judged and the skipped rows named; v118 differs from v116 only by the removed baseline and temperature (D370, D374), which the
   preflight's checks do not read, stated as a limit; plus the frozen tests and the configuration load (done: 8 passed; v118 loads with
   no baseline).
5. **An enforceable shared ceiling:** slice cap $0.25, each draw $1.00 (seeded v116 cost $0.64–0.70 a draw, with judging the largest
   part; unseeded has fewer views), one re-run allowed at $1.00: at most $4.25 in caps. replay.py checks spend after committed items, so a
   run can pass its cap by the calls of one day in flight (the judging of one day, about $0.03–0.05 at the stored judging cost): the
   ceiling is $4.25 plus one day's calls per run, stated. A cap stop leaves that draw incomplete: re-run once from empty, then out and
   reported. The launcher's cap is HIVEMIND_CAP_USD.

If you accept, end with "Council position: consensus on shape B' as in ml-challenge-1.md"; otherwise name the change.

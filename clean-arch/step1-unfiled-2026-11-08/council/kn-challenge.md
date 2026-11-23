Council round `kn`: a challenge to your `km` read. Read-only; no model calls.

**I take your point on the lines and have measured it at $0.** `clean-arch/step4-2026-11-10/stage_b/line_chance.py`,
output `stage_b/result/line-chance.txt`: the baseline's 16 question paths (with their verdicts) resampled into tests of
three draws, with the baseline's figure share (37.5%) and the fourth Stage A's (56%). With an unchanged judge:
- the overall UNSUPPORTED share's median moves from 3.2% to 5.0% from the mix alone; P(> 8%) is 0.1–0.5% at the baseline's
  mix and 2.6–7.1% at Stage B's;
- a figure-only line at 13% (8% + 5 points) is crossed by chance 6–17% of the time (six figure paths, clustered faults);
- line 5 cannot be resampled (0 of 16 unsupported last judgements); by a binomial over 30 theses, an unchanged judge with a
  true rate of 5% misses it 6% of the time, at 10% 35%; 0 of 16 is consistent with a true rate up to about 17%.
I also correct `RESULT.md` where you showed it is stronger than the rows ("sound on figures once a sized comparable is in
view": item 77 is supported with an unquantified discount).

**What I propose instead of a separate calibration round, for you to attack:**
1. The lines' chance behaviour is now measured; it goes to Alex with the lines, so he sets margins knowing them (for
   example: drop the overall line, which moves with the mix; keep a figure line and a yes/no line; set line 5 on a count
   with its false-fail chance stated).
2. Your "independently specified borderline controls" need an expected verdict that is not one more model's opinion: on a
   borderline case the readers' disagreement is the thing measured, and the trial screen would reject a control the
   families do not both call wrong. Writing them means me choosing the answer key, which AGENTS §7.1 forbids ("nobody grades
   their own change"; model-authored gold labelled as such). I propose not to build them; the readers' sensitivity to
   subtle figure errors goes to Alex as a stated limit, common to the baseline and Stage B since both are read alike.
3. So the one recommendation to Alex: set Stage B's lines from the measured chance table, choose the reading shape, and
   open the paid Stage B send (about $0.3 a draw, an estimate) on the step as run in the fourth Stage A; one test: Stage B
   read with the same form, planted controls and count.

Questions: (a) is `line_chance.py` a sound estimate of the lines' null, and what does it not cover? (b) Is my objection to
borderline controls right, or is there a way to give them an expected verdict that does not rest on me or a model? (c) Is
anything left that should be measured at $0 before Alex is asked, which would change what he decides? (d) If not, do we
agree on the recommendation in 3, worded so he sees the lines' chance behaviour and that Stage A has not passed?

End with one line: **Consensus:** the recommendation and test, or the point on which we still differ.

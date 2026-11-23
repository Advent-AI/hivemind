# The new system's position, and the choices left (D477), 2026-11-13

**In one line:** the new system is not ready to replace the current one, and further wording fixes on this test set no longer move it; what
is left are choices about how the product is built. (Checked by the council, round 23.)

## Where it stands

- **The step that writes each question's answer options**, on 40 questions, must get at least 26 right with options it wrote (scaled from your
  line of 28 of 44). It gets 22. Of the other 18, 10 are declines that the readers count as right, and 8 are wrong.
- **Why it declines (the 11 declines its first pass made, checked by two independent readers):** six are right, and four of those six are
  questions the first step should never have opened (a stake already completed, a $500 million stake too small to matter, a background
  sentence, a figure no public report will settle). In four, the article supports a question worth asking that could be given options: the
  H100 rental price twice (the step sometimes files it under the semiconductor-cycle topic and sometimes says no topic covers it) and the
  memory price twice (once the first step wrote "the 12 months to mid-2027" instead of one calendar year; once it tied the price to a bank's
  estimate of one rack's memory cost). On paper, fixing all four and losing nothing would give 26. That is arithmetic, not an expected result:
  the readers did not check that the replacement questions would get good options, and they are narrower than the originals.
- **What today's fixes did:** four wording changes to the first step (the year split, the identity rule, the calendar-year rule, the
  unsigned-deal rule) were tested, on stored articles and, for two of them, on unseen ones. None was adopted: each moved the error to a
  neighbouring question, made the model stop asking, or found the old version already doing it half the time. The model's answers to the same
  request also swing widely (one question opened 3 of 3 times in one test and 0 of 3 in another), so three tries per case cannot show small
  gains.
- **Spend:** about $27 of the $40 ceiling I set myself for this period; nothing committed or pushed.

## The choices

1. **Define the research topics more fully.** The list of world topics (`poc/universe.json`, shared with the current system) defines
   "semiconductor cycle" only by industry revenue growth. The model files memory prices under it every time; it filed the H100 rental price
   under it in 3 of 9 tries, under a wrong topic once, and declined 5 times. Naming what each topic carries might settle this; that is untested.
   Where the H100 question did get options, 20 later judgements referred to it and one said it pushed the other way "but not enough" to change
   its answer; whether it changes any final answer is unmeasured.
2. **Make the first step write the answer options itself**, so that a question it cannot give options to is, in intention, not opened in that
   shape. Untested. It could touch at most the two memory cases and the over-opened questions, not the H100 declines unless the topic rule also
   changes; like two earlier attempts, it may make the model stop opening hard questions. Its benefit, risk and cost would be designed and
   reviewed before any send.
3. **Put the effort back into the current system.** It stays the default either way; the new system's parts (search, comparison, grouping)
   remain built and frozen for later.

The council has made no choice among these: D477 records them for you and stops paid tests on the new system until a choice is made by you,
or by the council on new evidence.

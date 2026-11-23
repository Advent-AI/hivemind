# Where we are, 2026-11-13 (written for Alex while he is away; the council decides under D439)

**The short answer: the new design ("clean") is not ready to replace the current system.** On our fixed answer key, the two get about the
same number of questions right. Among the questions that qualified for comparison, neither disagreed with the expert's final answer. Both
lose for the same main reason: they ask a question in a different shape from the key, or never ask it. The new design has also not passed
its own checks. This comparison used the current local replay setup of the existing system (v118).

## One picture

A report says NVIDIA is negotiating to guarantee the lease of a huge OpenAI data centre in Ohio. (The reported $500 billion is what the
data centre could cost to build, not the size of the guarantee.) The answer key asks: "Will NVIDIA sign that guarantee by 2027-06-30?" In
seven of twelve runs the systems never asked it. They filed the report only under the question "how much credit support will NVIDIA have
committed?" The five runs that did ask it picked a different check date (2027-07-01 or 2027-12-31). Our rulebook allows those dates, but
those five questions cannot be graded against the key's exact question.

## 1. The goal (the phase document, PRD 10 §1)

Every question's judgement should get the facts that can change its answer. We measure it at the end, against the frozen answer key
(one expert reader's answers on 2026-07-14), not by any single step's score.

## 2. What we measured today

- **A same-day run of both systems, three times each.** The full run charged $11.43 to its tracking ledger, a little above the estimate at
  published rates. We grade seven selected questions from the key. Runs agreeing with the key: clean 2, 1, 0; production 1, 1, 1. On some
  questions the two reader teams could not agree whether the question counts. Counting those in, the totals are clean 2, 2, 1 and production
  2, 2, 2. This describes the two systems; it does not pick a winner.
- **Where the losses were first found.** In this comparison, every graded loss was first classified as a question not opened in the key's
  shape or with the key's date. Some losses also had facts missing behind them. That does not prove the later steps are sound.
- **What each system kept.** For the questions it lost, the clean design had kept 51 of the 55 facts the expert relied on; production had
  kept 39. Production also failed to attach some kept facts to questions it had opened (the Kyber delay facts, the Ohio facts). We did not
  find a wrong final answer from these missing links among the questions that qualified. In the Kyber case, later reports carried the delay
  news again, and production's answer still matched the expert.

## 3. What we tried and ruled out today (reviewed by the council; some readings repeated by two independent readers)

| idea | what we found | result |
|---|---|---|
| Fix production's habit of not attaching kept facts | three causes found (it never attaches old facts to a newly opened question; it parks facts under total revenue; it picks a neighbouring question); no wrong final answer was shown among the questions that qualified | not the priority now |
| A new phase to fix how questions are opened | few clear rule breaks, spread over six small causes; the biggest differences include choices whose treatment is not yet settled (ask about one programme or the company-wide total; "by 2027" or "by 2028" after a reported delay; whether to track memory prices at all) | no new phase |
| Fix the new design's answer-choice step | the judge reads only the first attempt; it had three agreed faults of three kinds, none on a graded question: two reached the judge, one question was wrongly refused | nothing to fix as a group |
| Ask the model why it chose what it did (2 cents) | two instructions the rulebook has are missing from the new design's instructions: an unsigned deal can be its own yes/no question beside a programme total, and next year's figure is a different question from this year's. The model's answers point to them, but answers given afterwards do not prove the cause | a lead |
| A date sentence stricter than the rulebook | both readers found it the deciding reason in one case, one reader in a second; it usually appeared beside other reasons, so the effect of changing it is unmeasured | recorded, not tested alone |

## 4. Do we keep changing things?

Yes, carefully, and with no paid test yet. The next step costs nothing: compare two ways to close the "is this the same question?" gap in
the new design. One adds the rulebook's missing lines to its instructions. The other moves that decision to a separate later step, where
the rulebook puts it. Each must show three things before any test: how it handles a question the model never proposes, that it keeps
together questions that belong together, and that it does not repeat an earlier failure. Earlier today, a sentence that split the spending
years pushed the memory-price question away from the key's shape; that version was stopped and the current instructions stayed. The fix
with a chance to add graded comparisons is the year split: in five of six clean runs one of the two spending years was not asked
separately (2026 twice, 2027 three times), while production asked both years in five of six. That is up to three more comparisons, not
three proven right answers.

## 5. How far from production

- The new design still has to pass its answer-choice checks. On 40 fresh questions, each tried three times, it missed five of six checks;
  the threshold of one check was scaled by the council for this test (32 and 26 of 40, from Alex's 35 and 28 of 44).
- The judge's own reading has not passed either. The earlier full reading (2026-11-12) did not pass: too few control questions qualified,
  and one line was missed on its strictest reading. Today's reading was stopped for the same reason (too few qualifying questions).
- The whole-path acceptance (D427) is outstanding: it needs the answer-choice and judgement checks above, the whole-path comparison with
  the existing system, and the checks of the new design's second step (comparing each new fact with stored ones).
- Much of the observed gap involves question shapes whose treatment the rulebook leaves open; the size of the remaining product gap is not
  established. Some of the key's shapes are recorded as concerns (D373); the key itself does not change.
- Production has known gaps too: facts not attached to questions opened later, regulator questions dated 2026-12-31 instead of the fiscal
  year-end, and an ambiguous "launch" where the rulebook asks for first shipments. Their effect on qualifying final answers was not shown in
  this window.

## 6. Money and record

Tracked spending is about $18.42 against the council's $40 ceiling, which Claude set (D439; not confirmed by Alex). Decisions taken today by
the council: D449–D462 (`docs/DECISIONS.md`). Every result named above has a page under `clean-arch/e2e-comparison-2026-11-13/`. The work in
this report is local and uncommitted (the last commit is 053c957).

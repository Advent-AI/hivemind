# Does one missing fact change one stored judgement? Result of the six-call test (D510, under D439), 2026-11-15

Design: `EFFECT-TEST-DESIGN.md` (version 2, frozen before the send). Script: `effect_test.py`. Raw replies, answers and spend:
`poc/data/clean-effect-test-2026-11-15/v7-e379/`. Blind rankings: `codex-stance.jsonl`, `claude-stance.jsonl`. Tally:
`tally_effect.py`, `tally-effect.txt`.

## The outcome, by the rule written before the send: inconclusive

- Six calls, six HTTP attempts, all six answers valid (the judge's schema and its own check against the request sent). **$0.0093** at
  the published rates (ceiling $0.25). Spend recorded under D439: about $18.4 before, about $18.41 after.
- **The answer did not move:** all three controls and all three answers with the fact are answer 1 (yes).
- **The rankings did not separate:** in both blind readers' rankings the conditions overlap: the firmest is a control, the least
  firm is a control, and the answers with the fact lie between (one reader ties a control and an answer with the fact). The controls
  alone span the whole range, so the control's own variation is as large as anything between the conditions. The readers were not
  told the conditions, but the packet showed each answer's cited ids, e379 among them for two answers: the result is that the
  rankings did not separate, not that the conditions could not be told apart.
- By the design this is inconclusive: it does not show the gap is without effect. One request, three sends a condition.

## Every answer

| Answer | Rung | Cites e379 | Marks e379 as pushing | Codex rank | Claude rank | Its words on doubt |
|---|---|---|---|---|---|---|
| control 3 | 1 | - | - | 1 | 1 | "a possible cap or staged approval, but the thesis requires approval of a purchase" |
| with the fact 1 | 1 | no | toward the last answer | 2 | 2 | "These reports are unverified and repeated coverage ... is not independent confirmation" |
| with the fact 3 | 1 | yes | toward the last answer | 3 | 3 | "The reported shipment plan and domestic-policy constraints temper confidence" |
| control 2 | 1 | - | - | 4 | 4 | "Domestic-chip preferences, possible bundling, and the H200 precedent temper the forecast" |
| with the fact 2 | 1 | yes | toward the last answer | 4 | 5 | "Domestic substitution, possible bundling, and the H200 precedent temper confidence" |
| control 1 | 1 | - | - | 6 | 6 | "The reporting is unconfirmed ... U.S. export uncertainty, domestic-silicon preferences, possible bundling, and the H200 precedent" |

## What Claude read in the six answers and the two requests (every trace)

- **The judge registered the added statement and did not weigh it in words.** In all three answers with the fact, its list of how
  each statement pushes marks e379 "toward the last answer" (against "yes"); two of the three cite it. None of the three names the
  RTX Pro 6000D or a September 2025 stop order in its reasons.
- **The request already held a precedent of a like kind.** Under this question the judge was already shown that Chinese regulators
  mostly blocked imports of Nvidia's H200 after Washington had approved them (e566), and that H200 use was restricted. The stored
  answer and two of the three controls already temper "yes" with "the H200 precedent". This is a reason the test may not have been
  able to show an effect; it is not proof that the added stop order added nothing.
- All six answers rest "yes" on one reported signal (MIIT told firms it intends to approve) and on the question needing only one
  approved purchase by the deadline; each says no formal decision against is reported.

## A fault in the reading, found after the send

The blind readers' second mark, `uses_precedent`, was worded as "an earlier Chinese order telling firms to stop buying a related
Nvidia chip". The H200 blocking already in the request fits those words, so the readers marked "yes" for two controls and one answer
with the fact, all of which name the H200 and none the RTX Pro 6000D. The mark could not tell the added fact from what the request
already had. It decides nothing here (the rankings do not separate), but it was written without first checking what the stored
request and the stored answer already said on the point; the stored answer's "the H200 precedent" was on screen before the send.

## What this result may and may not be said to show

- Shown: for this one request, adding the missing statement did not move the answer in three sends, and two blind rankings of
  firmness did not separate the conditions; the judge's structured output marked the statement as pushing against "yes" in all
  three, an observed change in what it wrote, not in what it chose.
- Not shown: that the delivery gap of D506 and D508 is without effect on judgements (one case, three sends; this case's request
  already carried a like precedent); a rate; anything about which system carries forward.

## Council (thread mx, round 23, under D439; `clean-arch/step1-unfiled-2026-11-08/council/mx-challenge-22.md`, `mx-codex-23.md`): consensus

- The council checked all six raw replies against the recorded answers and re-ran the schema and the judge's check: all match and
  pass. The outcome is inconclusive.
- The omission is real as delivery (kept, absent from the question's requests, judged relevant by both census readers) and the
  judge's marks on it are an observed change in its structured output; no change of answer and no separated change of confidence
  was established.
- The other confirmed cases are not shown to be weaker, and a fix is not shown to be a patch: neither can be said without a
  mechanism and its share. What is supported is "do not build on this evidence now".
- **Decided under D439 (D511):** no further send and no change on this delivery line now; the confirmed omissions, the 23 open pairs
  and this inconclusive test stay open evidence; the decision D507 left for after the sizing ("then decide whether to change") is
  taken as: defer. The next step is a cold reflection council over the whole record, which ranks the remaining losses from the
  product goal and proposes one next test with its falsifier.

## Lessons

1. **Read the control for facts of the same kind before writing the measure.** The stored answer's "the H200 precedent" was on
   screen before the send, and the reader's mark was still worded so that it fits.
2. **A reader's "bears" is not a judge's changed answer.** The census counts the first; only a send shows the second.
3. **The judge's structured marks moved while its answer and reasons did not.** They are a cheaper and more sensitive observable
   than a reading of reasons, and belong in the outcomes written before a send, with what they can and cannot show.
4. **Stepping back is a decision.** After several results that separated nothing, the next step is chosen from the goal by the
   council, not from the last result.


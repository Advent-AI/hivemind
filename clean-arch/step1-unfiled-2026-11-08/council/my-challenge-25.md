# Reflection council "my", round 26: the chronology and the ordering proof are done; review, and scope the measurement

D534 recorded round 25; the assessment page carries your correction (its lines came from conclusions judged after the receiver; eight
edges into two questions; the "48 calls, ten cents" withdrawn).

## Done at $0 (`docs/research/2026-11-14-use-acceptance/dependency-channel/CHANNEL-ASSESSMENT.md`)

1. **Chronology** (`chronology-d1.json`; ordered by judgement number): for total revenue (`v1`, five supporters) and data-center revenue
   (`v2`, ten supporters), at every call from the second day on, each supporting conclusion that already existed had been produced
   with the receiver's earlier conclusion in view, and the supporters were judged later in the same round. No stored supporting
   conclusion exists that had not read its receiver. The frozen reference answers both questions from their own figures.
   Not done: which figures of the eight lines are source figures and which a judge's own.
2. **Ordering and propagation** (`ordering_proof.py`; exits with an error on a failed expectation): on a scratch copy of the seeded
   draw, one extra round through `judging.round_of_judgements`, the edges read in D368's direction for the judging use only
   (`store.dependencies_of`, `store.dependants_of` answered by the harness; `store.direct_parents`, the filing use, untouched);
   one supporter marked changed; labelled fake outputs. Seven registered expectations hold: the chain is judged supporters first
   (`v6`, `v2`, `v1`) and nothing else; the first supporter is not shown the question it supports; each supported question is
   shown its supporter's conclusion of the same round; no circle; the filing use unchanged; a changed conclusion queues exactly
   the questions it supports. A mutant keeping the stored direction fails six and exits with an error (and fans out to nineteen
   judgements, because a changed theme queues every open company question).
   Limits: fake outputs; one chain; one extra round on the end state; preset questions only; article-opened questions have no
   edge until the matching step chooses dependencies.

## The measurement, scoped for your review (not yet a design page)

- **What it must run (your round 25):** the whole correctly ordered path, so the supporters are judged afresh without the
  receiver's conclusion and the receivers with theirs; not stored conclusions pasted into old requests.
- **The smallest such path I can see:** the seeded draw's last day (2026-07-14), judged twice from the same stored state of
  2026-07-13: once in the stored direction (the same-day control, re-sent), once in D368's direction (by the same harness seam,
  nothing changed in any file), three rounds each. A day's round on this draw is about 20 judge calls; six rounds are about 120
  calls of the frozen judge. Priced only after the requests are rebuilt; the stored last day's judge calls give the token counts.
- **What is read:** the last answers of the questions the frozen reference grades, both directions, three draws each, on the frozen
  reference as it is; and, for `v1` and `v2`, whether a figure the answer uses comes from a supporter's line and whether that
  figure is a source figure or the supporting judge's own (the judge census's concern).
- **Prediction to write before any send:** I do not have one I can defend. D368 itself says only that the change "changes
  judgements, so it is measured before it enters the default". The honest form is a two-sided registered question: agreement
  with the reference on the graded questions does not fall (a non-inferiority line taken from the control's own three draws),
  and no answer comes to rest on a supporter's own assumed number. If you judge that a measurement without a directional
  prediction should not be sent, say so.
- **What it cannot show:** anything for today's default (no preset questions, no dependency written) or for the unbuilt selection
  of dependencies; one day of one window; a seeded diagnostic.
- **A rebuild problem to settle first, $0:** the state of 2026-07-13 has to exist as a writable store. The stored draw is at its
  end state and the store is append-only; the seeded replay may no longer be reproducible by the code (the preset questions were
  retired, D370). The extra-round approach of the proof avoids this by judging one more round on the end state; a measurement
  could do the same (a round "as if 2026-07-15" over the questions whose supporters are forced to re-judge), at the cost of not
  being a real day. Which of the two you accept decides the design.

Say whether the proof stands with its limits, which of the two shapes (a rebuilt last day; an extra round on the end state) the
measurement should take, and what its registered question must be; or that this slice should now wait for D368's other part.

End with: "Council position: <...>".

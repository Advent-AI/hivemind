# Does the clean ladder step lose answers when the question is right? Design, for the council and then Alex (D467), 2026-11-13

**What it can decide:** whether, on seven of the key's own questions with the same facts day by day, the clean ladder step's answer ranges
make the frozen judge agree with reader B less often than the key's own ranges, measured against a same-day control. It changes no final
answer by itself and does not pass Stage A (D400, D426); a loss located here is Step 4's to fix (frozen by D426: Alex reopens it). It needs
Alex's word: it reuses the key's questions (D392).

## The two arms (same day)

- **Control:** the seeded Stage 2 adapter unchanged (`clean-arch/e2e-2026-11-09/adapter.py`), the three seeded draws (d2 with its q23 thesis,
  as stored), judged live by the frozen judge.
- **Ladder arm:** the same adapter, the same draws and facts, with seven seed views (v4, v5, v7, v8, v9, v13, v18) taking the clean ladder
  step's ladder (question, due day, year, rungs) where the seeds are written (`swap_adapter.py`). A seed the ladder step refuses keeps the key's
  ladder (so the other views' facts and dependencies stay the same) and counts as a loss.

## Proofs done at $0

- The wiring rebuilds the stored control exactly: all 759 judge requests of the three draws served byte for byte from their archives, the
  same judgement records (`proof_control_rebuild.py`); a mutant adding one space to every quote stops on the first request.
- The swap changes nothing else: the seven (and the ten) seed views swapped to their own seed ladders rebuild the control exactly; one view
  swapped to reworded rung conditions changes exactly its first request (`proof_swap.py`). The judge reads rung labels and conditions, not the
  stored bounds (shifting the bounds alone changed no request).
- The cases (`seed-cases.json`, 21 = 7 seeds × 3 draws): each seed's article chosen by a blind reader as the earliest linked article whose
  own text states the question's subject (`article-choice*.jsonl`); opens_as and settled_by from the standard's class and settling material.
  The ladder step therefore reads an article of 2026-07-01 to 07-06 while the view opens on 2026-07-01: up to five days of look-ahead in the
  ranges' wording, disclosed; the judged answer at 2026-07-14 is unaffected by it except through that wording.

## Counting (frozen before any send; every answer read by Claude)

Per graded seed (v4, v5, v8, v9, v13, v18) and draw, the last judgement by 2026-07-14:
- control: agreement by the frozen scorer's rule on the key's ladder;
- ladder arm: agreement by `control_theses.agrees` on the clean ladder, counted only if the clean question is the same question and the due
  day the same (D430's reading); a reworded question, a moved due day or a refusal counts as not agreeing, each listed with its reason;
- for every agreement: the width of the rung that holds reader B's answer in each arm, and for yes/no the real label (the frozen comparison
  counts any label other than "Yes" as "No").

**Loss** = the control agrees and the ladder arm does not; **gain** = the reverse.

| result | rule (18 graded question-draws) |
|---|---|
| the ladder step loses answers on the right questions | losses − gains ≥ 3 |
| no loss observed on these questions in these runs | losses − gains ≤ 0, and no agreement rests only on a wider rung |
| inconclusive | anything else |

v7 is reported, not counted in the line. A result against the hypothesis that the ladder step is sound goes to Alex with the losses traced.

## Cost and stopping

Ladder step: 21 first-pass sends (the fourth Stage A: 132 answers for $0.109) → a few cents. Judging: both arms judge all views of three
draws; the stored control runs cost $0.48 a draw → about $2.9 for six judging runs. **About $3 estimated; reservation ceiling $4** (not a
guaranteed maximum); actual cost from tokens at published rates. An interrupted run is not scored.

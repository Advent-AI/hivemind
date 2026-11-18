**The new system is not ready to replace production.** Its largest demonstrated reader-facing loss is that important questions never become comparable answers; the first formal gate is also unmet and looks unreliable under the current design.

For example, in the July comparison, the new system kept **51 of 55 decisive facts** for lost questions, but often did not open the question in the required shape. Keeping facts did not ensure a reader received an answer. [July comparison](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/CENSUS-FULL-RESULT.md)

1. **Production blockers, in order**

   - **Gate 1 — answer choices:** failed in all nine readings. On Alex’s 44 topics, the fourth reading met lines 2 and 5 but had **six faults in 131 valid sends** across lines 1, 3 and 4. Later, product-condition readings also failed: **7 or 5 of 13 topics right**, versus a diagnostic target of 11. [Decision index](/Users/lchingen/hivemind/docs/DECISIONS.md:957), [fortnight result](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/carried-run/RESULT.md)
   - **Gate 2 — final answers:** not passed. Only **4 comparable controls with the required facts** were available; **8** were required. On the strictest reading, **3 of 24** last answers were unsupported, above the one-in-ten limit. Re-sending the judge cannot supply the missing comparable controls. [Stage B result](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/STAGE_B_RESULT.md), [D576](/Users/lchingen/hivemind/docs/DECISIONS.md:920)
   - **Gate 3 — end-to-end comparison:** still owed, as are the Step 2 checks; the numerical meaning of “beats” is not yet defined. In the exploratory July comparison, the new system agreed on **2, 1 and 0 of seven** graded questions across its three draws; production scored **1, 1 and 1**. This does not rank the systems. [Gate frame](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/NEW-SYSTEM-FRAME.md), [July comparison](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/CENSUS-FULL-RESULT.md)
   - **Gate 4 — unseen news:** acceptance criteria and number of runs remain proposed, not settled. One exploratory week covered **2 of 5** big matters; its exclusions and small size limit the conclusion. [Gate frame](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/NEW-SYSTEM-FRAME.md)
   - **Gate 5 — integration and release:** substantial test-store work is complete, including page serving and live-store proofs, but product-path acceptance and release remain unfinished; nothing has been deployed. [Current state](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:400)

   **Largest general loss:** forming and opening answerable questions. In July, every counted lost graded answer was classified upstream of judgment. That is a broad observed loss, **not one proven general cause**: a subsequent review found small, scattered breaches and substantial ambiguity over the remaining differences. The July runs also began from empty libraries, so they do not establish the rate in normal use. [Opening review](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/opening-review/OPENING-REVIEW.md)

2. **Is gate 1 reachable?** A lucky pass is possible; a dependable pass is not supported by the current readings. Outside the 44, the stored counts, with unresolved marks counted in the answer’s favour, are:

   | Reading | Sends | Line 1: different question | Line 3: faulty choices | Line 4: unjustified refusal |
   |---|---:|---:|---:|---:|
   | July | 120 | 2 | 2 | 1 |
   | Oct. 6 week | 39 | 3 | 0 | 2 |
   | Carried fortnight | 39 | 3 | 4 | 0 |
   | Oct. 13 week | 15 | 0 | 1 | 0 |

   Descriptively pooled, those are **8/213 = 3.8%**, **7/213 = 3.3%**, and **3/213 = 1.4%**, respectively. These are rough observed shares, **not independent estimates of a production error rate**: topics and articles repeat, the first week overlaps the fortnight, and reader disagreements affect the counts. [Four-reading map](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/second-week/FIRST-GATE-MAP.md), [fortnight result](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/carried-run/RESULT.md), [fresh reading](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/unlisted-parts/RESULT-FRESH-A2.md)

   Under a simplifying independent, constant-rate assumption, the **combined** fault probability across all zero-fault lines must be below about **0.53% per send for a 50% chance** of zero faults in 131 sends, or **0.039% for a 95% chance**. Correlated sends make those probabilities illustrative, not forecasts. The record does not prove no redesigned step can pass; it shows no current, bounded route to reliable passage.

3. **One next step: a $0 source-to-answer audit of missed important questions in the carried-library fortnight.** For the stored articles, trace each candidate missed matter against the library actually shown, the raw opening answer and any final answer. Separate genuinely missing questions from matters already covered, figures Alex chose to use as evidence, and uncertain cases. Compare the resulting mechanisms with the July opening review before proposing a change.

   **Decision-moving result:** one evidenced mechanism recurs across distinct worthwhile matters, and a stored-data counterfactual shows it can recover an answerable question without losing correctly covered matters. That would give the council a concrete, reversible new-version candidate outside the 44. **Close this route:** the losses are already covered, not worthwhile under the governing rules, unresolved, or scattered without a shared fix that survives counterexamples.

   This beats another answer-choice edge fix because it targets the larger observed loss at its source; it beats another paid comparison because the existing comparison is underpowered and the last fresh sample produced only three independent matters. It also avoids repeating the already negative period-split probe. [Opening review](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/opening-review/OPENING-REVIEW.md), [comparison feasibility](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/comparison-feasibility/RESULT.md), [split result](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/splitting/RESULT.md)

4. **What Claude’s last stretch got wrong**

   - **Scope:** it spent extensive effort proving live-store and split-writer infrastructure while the quality gates had not moved. That work may be useful for integration, but it did not establish a better answer for a reader.
   - **Sizing:** it spent **$3.45 on 383 articles** to obtain five topics, only **three independent matters** against a minimum of five; the comparison could not decide A2. The split build likewise preceded proof that its narrow target could produce sound questions.
   - **Candidate selection:** A2 and A3 chased neighbouring errors in a disputed side list; each adjustment moved the problem. The period split targeted two topics, then exposed a different underlying problem: the 2027 source supplied a GDP share while the topic asked for a total. Its small count success did not overcome the agreed wrong-question veto. The first proposed split population also included seven of Alex’s 44, caught before the send. [Lean log §§60–69](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/LEAN-LOG.md:1203), [split result](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/splitting/RESULT.md)

This review is read-only; I did not change files or start a run.


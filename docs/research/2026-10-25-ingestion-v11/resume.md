# D179: withdraw the unrelated extraction prerequisite

Alex explicitly asked to undo the mistaken change after the baseline comparison showed that the cited NAVER-to-revenue links already existed in the measured v23 library.

The withdrawn change is D178's use of those existing semantic findings as a prerequisite to repair extraction before continuing the acceleration POC. No evidence-link correction was implemented in product code. Preserve the tested NAVER milestone prompt, current matcher, writer, ordering checks, sources, golds and all recorded results.

## Effective comparison

Return to D171/D172's acceleration question: with the same sources, configuration and ordered starting state, does concurrent preparation preserve the sequential behavior, and how much time does it save?

- Exact request reconstruction, committed-prefix visibility, source preservation, valid destinations, atomic writes, failure handling and ordered daily completion remain required. A violation stops the experiment.
- Read and report semantic differences against the sequential controls and existing measured records. Distinguish an existing semantic issue, fresh model variation and a regression introduced by concurrency. An existing issue does not itself create a new extraction work order or automatically disqualify the speed comparison.
- Do not report preserved defects as correctness, ignore a new loss/false merge, or claim model equivalence from an exact cached replay. Keep the planned fresh controls, per-sample results and bounded claims.
- Both modes retain the same v24 test configuration; v23 remains the product default. No model, prompt, category, group, identity or evidence-link rule changes here.

## Reversing the stop

The sole mutable record to restore is this study's `settings.halted` flag, which the assistant set after the completed first control. Back up the journal first. Clear it only if it exactly equals the recorded semantic-stop reason, all 12 attempts are complete, the original $1.50/144-call limits remain, and no study process is running. Preserve every attempt, charged amount, request, response, old stop report and result. An unknown-usage or technical-failure stop is not cleared. Save the rollback proof.

No further paid call is part of this rollback. The next execution remains `concurrent-1` in the existing fixed sequence, under the original remaining budget. The prior plan and source review remain historical records; this document supersedes their instruction to repair unrelated extraction findings before continuing.

**hold — first fix the resend so the model can see the answer it is being asked to correct.**

For example, if the first answer quotes the wrong words, the second request says “Correct it and answer again,” but does not include that answer. The model cannot see which quote it wrote.

1. **The resend is missing the answer.** [ladder_step.py](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/ladder_step.py:284) sends the original request again with reasons appended, but no previous answer. This affects every refusal and makes the intended correction untestable as written. The note says “The code returned the previous answer because … Correct it and answer again.” Send the previous answer with the reasons and use: **“Your previous answer was refused for the reasons below. Correct those problems and return the complete answer again.”**

2. **A write failure does not stop the other workers.** The exception handler ends before `write_view` and the outcome-file write ([stage_a.py](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/stage_a.py:167)). If either fails, the shared stop flag is not set; other workers can start further paid sends while `pool.map` waits. The run ultimately raises rather than reporting a completed measurement, but it violates the one-stop rule and can spend after the error. Include view construction and outcome writing in the shared error handling.

3. **An invalid object can induce an unjustified refusal.** [ladder_step.py](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/ladder_step.py:123) says: **“return no_ladder and name it in the reason.”** An invalid label does not prove the question belongs to another company or an unlisted theme: the model may simply have mistyped a valid theme. This conflicts with the request’s six permitted reasons to decline. Use: **“The object is not the company or a listed theme. Choose the correct listed object if one applies; otherwise return no_ladder and name the other company or uncovered matter.”**

4. **A valid short quote can be refused.** [ladder_step.py](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/ladder_step.py:85) relies on `repair_quote`, which rejects normalized quotes shorter than eight characters ([extraction.py](/Users/lchingen/hivemind/src/hivemind/extraction.py:246)). Thus `YES` in the answer and `Yes` in the article fail, although §5.3 permits case differences. The exact-match path still accepts identical short quotes.

5. **The refusal message misidentifies “this article.”** The check matches both phrases, but always says **“the question says ‘this item’”** ([ladder_step.py](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/ladder_step.py:118)). Use: **“The question refers to ‘this item’ or ‘this article’. Replace that reference with the specific information needed to understand the question on its own.”** The remaining reason strings are general, not fitted to the covered company or an article.

The other checks follow the specified order, with one qualification: invalid shape or object returns early, so later problems are not reported on that refusal. A decline is accepted before ladder checks, as designed. The figure, date and reference checks otherwise enforce the stated mechanical boundaries; `write_view` orders and labels accepted ladders as specified. The separate pass archives prevent cross-pass cache reuse, and a detected cache hit stops the work. The 44 stored cases have no identical thesis-and-article payloads. The cap relies on the reservation being an upper bound on actual token cost.

**Tests overclaim:**

- [test_stage_a.py](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/test_stage_a.py:142) says sends without outcomes are counted, but checks neither the ledger nor a send without an outcome.
- [test_ladder_step.py](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/test_ladder_step.py:203) says a number is accepted and written, but calls only the number helpers, not the answer check or view writer.
- The four-range test allows its schema assertion to pass regardless of the result ([test_ladder_step.py](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/test_ladder_step.py:133)). The count tests also do not exercise the resend path promised in the design.

No files were changed, and no tests or model calls were run.
**Choose A:** once the first step has finished, run the topics and answer choices on the remaining ledger, and explicitly record matching and judging as not run. This preserves the information needed for the registered reading without raising the ceiling.

The proposed $0 proof is the right starting point: the real runner should build the same seven topics from the stored fresh-week trace, skip matching, and stop before a paid answer-choice call when the ledger refuses it. The mutant without the skips should show that matching starts.

Add one positive control before using the path: with fake external responses and a sufficient test ledger, run **all three answer-choice attempts** through the real entry point and compare the requests and outputs with the stored fresh-week run. The refusal-only proof cannot show that the answer-choice stage completes or preserves its inputs. Also verify that a stopped or incomplete first step cannot be marked complete for this path.

After the live first step ends:

- Require the guarded merge to confirm all 272 articles completed in order. Then count the opened topics and apply the reading plan’s **22-topic limit** before sending answer-choice calls.
- Check the actual remaining ledger and the answer-choice reservations, including concurrent calls. The earlier $0.02–$0.05 is an estimate; a reservation or retry can still stop the step. If the ledger cannot safely start it, return to the council without sending.
- Preserve an exact mapping from each topic to its opening article ID. The [case builder](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/build_cases.py>) supplies the article text and date but does not put its ID in the case, while the registered strict and wider counts depend on that ID.
- Label the result **continued, answer-choice diagnostic only**. The runner may mark its prepared record complete because the other components are marked skipped; that must not be presented as a completed full-system run. Matching and judging remain unmeasured and would need a separate decision and budget later.

One billing qualification: the ledger’s roughly $0.99 is the conservative charge for the lost attempts. Their actual provider bill is unknown; the earlier average of about a cent per answered call does not establish an upper bound for a cut call.

The latest permitted ledger snapshot I read had **$1.7741 spent and $0.1220 reserved** on the continuation ledger; it was still live, so the final remainder is not yet known. I opened no live database and ran nothing.

Position: Choose A after the first step completes, with a full fake-response control, opening-article mapping and a check of the final ledger before any answer-choice send.
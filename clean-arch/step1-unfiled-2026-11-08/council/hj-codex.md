NOT READY

For example, a number that should be refused can pass the supplied number check because it is rounded before its digits are counted. The design also leaves open which version of a repaired quotation gets written.

1. **The number check can accept a forbidden number and stop the run instead of refusing the answer.** [number_rule_check.py:26](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/number_rule_check.py:26) counts digits after `Decimal.normalize()`, which uses the current decimal precision. I ran `1.00000000000000000000000000001`: the function normalizes it to `1` and accepts it, although it has more than 15 significant digits. If used as a bound or numeric reference, the later float round-trip assertion in [DESIGN.md:305](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:305) would stop the run rather than classify it as a refusal and resend. Fix the digit count without rounding, and exercise long inputs that differ only beyond the decimal context’s precision, through the entry point.

2. **Two builds can write opposite meanings from a repaired quote.** [DESIGN.md:334](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:334) invokes Step 1’s quote rule, but [line 358](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:358) says to write `<words>` without saying whether these are the model’s words or the repaired source passage. Step 1’s [repair_quote](/Users/lchingen/hivemind/src/hivemind/extraction.py:240) can repair an omission: I verified that “The company does expect sales to increase this year” repairs to the source “The company does **not** expect sales to increase this year.” One engineer could write the original; another could write the repaired passage. Specify which text is checked, stored, shown to the judge and given to readers, and test a meaning-changing omission. The reader’s XR or W mark could catch this example, but the written result must still be deterministic.

3. **The fixtures do not specify all the rows they claim to specify.** [examples.json:3](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/examples.json:3) says `written` shows the rows produced. Yet the figure examples omit rung `lo` and `hi`, and all examples omit other written values specified in [DESIGN.md:408](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:408), including the checked answer and outcome record. The made-up example also omits the view ID and object ID from `written`. Thus these fixtures cannot establish that two implementations write the same complete records. Either provide the complete expected records, including nulls and bounds, or explicitly define these as projections and provide separate complete write expectations.

**Fixture walk.** All eight answers passed the actual `model.check_schema`. The remaining checks and writes do not yet exist, so the following are *design-level walks*, not executions of the proposed step:

| Fixture | Checks 1–8 | Written values shown |
|---|---|---|
| 1. Company yes/no | Pass | Shown labels, conditions, ID and date match |
| 2. Company yes/no, omitted parts | Pass; due date meets the 548-day binding limit | Shown values match |
| 3. Company five-state event | Pass | Shown order and conditions match |
| 4. Theme five-state event | Pass | Shown order and conditions match |
| 5. Company figure, lower favourable | Pass | Shown labels and interval text match |
| 6. Theme figure, reference | Pass; quoted words occur in the article and value is in the middle range | Shown labels and interval text match |
| 7. No ladder | Pass; no ladder checks apply after shape | Shown status and reason match, but the record is incomplete |
| 8. Company figure, higher favourable | Pass with its stated test universe and article | Shown labels and interval text match, but the record is incomplete |

**Checks 1–8.** The schema enforces required keys, types, enums and nonblank patterned text; production’s validator does not enforce maximum array lengths. Checks 1–6 therefore need new code for the stated shape, object, state, number, date and reference rules. The named production functions support object resolution, date limits, quote repair and parts of range validation; `check_bounds` alone does not enforce an open lower end, and the proposed check must compare exact decimals. Check 7’s ordering and rendering are new behavior derived from the named split code. Check 8’s retry and complete outcome record are also new: `model.call` raises on malformed or schema-invalid output but does not perform this step’s retry. The quotation choice and number-check defect above are the places where the specified enforcement is not yet sufficient.

I found no wrong answer that necessarily escapes **all** listed reader marks: W is expressly open to any other misleading fault. That is not proof readers will catch every fault.

Wording-level: “each fixture’s note records what readers found” and “the rows the rules produce” overstate what the fixture file contains.

Walked all eight fixture answers and their displayed writes, checks 1–8, the schema and number rule; I did not execute the unbuilt checks or verify full database writes.
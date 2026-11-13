NOT READY

For example, a model answer containing a very long integer can stop the run before the promised number check gets a chance to refuse and retry it.

1. **The retry contract does not cover every number it says it refuses.** [DESIGN.md:329](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:329) says an out-of-range number is refused and resent. But [model.call](/Users/lchingen/hivemind/src/hivemind/model.py:258) first parses the answer using ordinary `json.loads`. On this Python, an integer with 4,301 digits raises `ValueError`; `model.call` does not catch that exception, so the proposed `SchemaError` handler at [DESIGN.md:400](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:400) cannot perform the retry. I verified the parser behavior locally. Two engineers could therefore implement the stated refusal differently. The fix must specify how this answer reaches the refusal path, preserves its text and cost, and is retried; test it through the real entry point with a fake transport.

2. **The complete expected writes are still not specified for the fixtures.** The prior review’s bounds issue is addressed, and [examples.json:3](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/examples.json:3) now calls the displayed values a projection. But it also says the complete rows are in §5.4 and will be tested. [§5.4](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:448) describes the fields generically; it does not give complete expected records for each fixture. For example, fixture 8’s projection omits `view_id` and `object_id` despite saying it projects the view’s object, and fixture 7 gives only prose for its no-ladder record. The design also does not specify the checked-answer value for a twice-refused response. Provide complete expected writes, or an explicit per-field mapping including nulls and refusal outcomes, with concrete test inputs for each case.

The previous quote finding is answered: [check 6](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:362) specifies the article passage and rejects a missing “not.” The previous digit-count example is also answered in [number_rule_check.py:20](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/number_rule_check.py:20); the parser failure above is a separate path.

**Fixture walk.** All eight answers passed the actual production schema validator. The remaining checks and writes are not built, so these are design-level results:

| Fixture | Checks 1–8 | Displayed projection |
|---|---|---|
| 1. Company yes/no | Pass | Matches |
| 2. Company yes/no, omitted parts | Pass | Matches |
| 3. Company states | Pass | Matches |
| 4. Theme states | Pass | Matches |
| 5. Company figure, lower favourable | Pass | Matches labels, intervals and bounds |
| 6. Theme figure, reference | Pass | Matches labels, intervals and bounds |
| 7. No ladder | Pass | Status and reason match; prose projection |
| 8. Company figure, higher favourable | Pass | Shown values match; object and view IDs omitted |

For enforcement: the validator covers schema types and required fields, but not the five-item maximum. Checks 1–6 require the new step’s stated checks; production’s `resolve`, date helpers and quote repair provide parts of them. Production’s `check_bounds` does not enforce the open lower end or exact-decimal comparisons. Check 7’s rendering and ordering and check 8’s retry and record are new behavior. The long-integer case above is the enforcement gap I found.

I found no wrong ladder that must escape every listed reader mark: **W** can name any other misleading fault. That does not prove readers will catch every fault.

Walked §5.3–5.4, all eight fixture answers and displayed projections, the schema, number rule, and the named production code. **Not reached:** the individual source and reader-answer rows in `dryrun/`, `dryrun2/packet-a`, `dryrun3/`–`dryrun8/`, and `reference/`; therefore I have not independently verified the fixtures’ claims about those readings.
NOT READY.

For example, a valid JSON answer containing `1e999999999999999999999999` passes production’s initial parse but fails the design’s second parse before the number check can refuse and resend it.

1. **An out-of-range number can stop the run instead of being refused.** [DESIGN.md:335](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:335) requires a second parse using `Decimal`; [the number rule](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/number_rule_check.py:15) does the same. I verified locally that Python’s first JSON parse turns the example above into infinity, while the second raises `decimal.InvalidOperation`. The design promises to refuse out-of-range numbers, but [check 8](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:417) does not specify handling this second-parse failure. One engineer could stop the run; another could resend it. The fix must specify how unrepresentable decimal exponents enter the refusal path, retain the answer and cost, and retry; test positive and negative extreme exponents through the real entry point with a fake transport.

2. **Fixture 8 specifies two different thesis IDs.** Its [outer identity and expected view](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/examples.json:488) identify `clean-99` and `v99`, but its [actual input](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/examples.json:588) says `clean-1`. The [write table](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:494) derives the view ID from the thesis ID, so using that input produces `v1`, not the expected `v99`. The fix must make the input and expected complete writes agree, including the `clean_ladders` row.

The previous review’s long-integer finding is addressed for the initial production parse: version 27 explicitly catches that `ValueError` and deep-nesting `RecursionError`, preserves text and tokens, and retries. The field-by-field write table also answers the previous request for a mapping, including a null checked answer after two refusals; fixture 8’s conflicting input remains.

**Fixture walk.** All eight answers passed the actual production schema validator. The remaining checks are design-level, because the step is not built.

| Fixture | Checks 1–8 | Displayed write |
|---|---|---|
| 1. Company yes/no | Pass | Matches |
| 2. Company yes/no with omitted parts | Pass | Matches |
| 3. Company states | Pass | Matches |
| 4. Theme states | Pass | Matches |
| 5. Company figure, lower favourable | Pass | Matches |
| 6. Theme figure with reference | Pass, assuming the specified reference is in its opening article | Matches |
| 7. No ladder | Pass | Displayed fields match |
| 8. Company figure, higher favourable | Pass on the supplied answer and article | Rungs and other displayed values match; `v99` conflicts with the supplied `clean-1` input |

For enforcement, the production validator covers the declared types, required fields and patterns; it does not enforce the five-entry maximum. Checks 1–6 need the new step’s own logic, using the named production helpers where applicable. Production’s bounds check alone does not establish the open lower end or exact-decimal comparison. Check 7’s rendering and check 8’s retry and record are new behavior. Apart from the decimal parse failure above, I did not identify another rule in this angle that is promised to be enforced but has no specified owner.

I found no wrong answer that must escape all the listed reader marks: **W** permits a reader to name another misleading fault. That is not proof that readers will notice every fault.

Wording-level: fixture 8’s note says non-whole bounds use `repr`; the governing rule requires plain decimal notation, which can differ for other values.

Walked §5.3, the complete-write tables, all eight answers and projections, the schema, number rule, and the cited validator, storage, date, quote and budget code. **Not reached:** the full request sentence-by-sentence; the individual source and reader-answer rows in `dryrun/`, `dryrun2/packet-a`, `dryrun3/`–`dryrun8/`, and `reference/`; consequently I did not independently verify fixture 6’s source passage or the fixtures’ stated reader results.
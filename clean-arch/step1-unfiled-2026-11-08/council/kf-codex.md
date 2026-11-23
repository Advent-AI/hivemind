**Not ready: the reading could give a misleading baseline because the controls are visible, some do not have an unambiguous expected answer, and the count can print usable-looking shares when required readings or stop conditions are missing.**

For example, trial judgement **139** says Google “has since” given guidance, but the request’s previous conclusion already discusses that same $190 billion guidance. Judgement **64** treats “could begin shipping” as a stated plan. Those are clues in the planted answers themselves, and they complicate what a missed control would mean.

1. **Does the plan cover the design?**

The intended population and two main shares match the outline: all **159 stored judgements**, with the last judgement of each view used for the second share. The trial key has **33 packets and 168 entries**: 159 stored, six planted and three repeats. It confirms the 16 last judgements are dated July 14. The design’s lines 4 and 5 remain **proposals for Alex**, not approved acceptance margins. D426 authorizes this preparation and reading, not a paid Stage B run. [Design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:1489), [D426](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4721)

There are omissions and additions:

- The design says fewer than **30 decided judgements**, a **zero denominator**, or a reading taking more than **twice its estimate** is `NOT MEASURED`. The plan’s stop list omits all three, and the count does not enforce them. The design’s budget paragraph covers Stage B as a whole; whether its time limit applies independently to this preliminary baseline needs to be stated rather than assumed. [Design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:1504), [baseline plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/BASELINE.md:56)
- The plan adds **two third readers**, three repeats, and three treatments of unresolved verdicts. They are preparation choices, not requirements expressly fixed by the outline or D426. The unresolved ranges are useful, but they do not replace the required result or make missing readings complete. [Baseline plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/BASELINE.md:41)
- The plan promises the three unresolved treatments for **every share**. The code produces them for the unsupported share, but **only one fraction** for the supported share on last judgements. It also prints no percentage for that second share. [Count](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/baseline_count.py:82)
- The plan says 150,000 characters and at most seven judgements **per chunk**, which is what the builder attempts before controls. It is not a limit on the finished packet: a control is added afterwards, and a single request over the limit is accepted. The builder’s printed “characters” are filesystem byte sizes, not character counts. [Builder](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/build_baseline.py:52)

2. **The six planted answers**

The judgement numbers below are the numbers in the trial packets. I read their requests and answers against the form’s ordered tests. [Reader form](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-b-reader-brief.md:43)

| Plant | Trial judgement | My reading |
|---|---:|---|
| 1 | **102** | Plainly **UNSUPPORTED** under test 1: rung 3 is $800–900bn, while its own implied outcome says at least $1tn. Its `changed: false` and “rung … unchanged” contradict both the displayed rung and previous rung 5. That is a form tell as well as the intended mismatch. |
| 2 | **27** | Plainly **UNSUPPORTED** under test 1: it selects No while predicting first shipments in Q3 or fall 2026, before the deadline. Its `changed: false` and unchanged explanation conflict with previous rung 1. That is also a tell. |
| 3 | **139** | The $840bn result improperly adds Google’s **total** capex guidance to the four-company data-centre total. I would call it **UNSUPPORTED** under test 2; the request’s previous conclusion explicitly explains why the Google figure cannot be used that way. But the answer says Google “has since” guided $190bn even though that same guidance is already in the previous conclusion. `changed: true` is formally consistent with the changed rung, but the claimed new fact is a tell. The evidence does not establish precisely how much of Google’s total overlaps, so “counted twice” is stronger than what the request alone proves; the scope mismatch is the clearer fault. |
| 4 | **26** | Plainly **UNSUPPORTED** under test 2: the alleged $150bn Microsoft and Meta deferral is absent from the request. The previous conclusion is rung 5, so `changed: true` and the claimed move to rung 3 are consistent with it. The fabricated statement itself is the substantive fault; I did not find a separate `changed` inconsistency. |
| 5 | **64** | The reason given for No—shipment is “not established”—is explicitly disallowed by the form, so **UNSUPPORTED** is a reasonable application of test 2. But the request says Rubin “could begin shipping later this year,” not that NVIDIA has a stated plan to do so. A careful reader could regard the remaining evidence as too weak to choose between Yes and No and return **INSUFFICIENT**; the control is not an unequivocal test-3 case. `changed: true` fits the first-judgement instruction. “First judgement.” is unusually terse, though no field is missing. |
| 6 | **43** | Discounting solely because no hyperscaler confirmed $1tn is an impermissible step under the form, so **UNSUPPORTED** under test 2 is defensible. But the request says the projection **“could reach”** $1tn. A careful reader could consider its exact rung-5 point forecast uncertain after rejecting the arbitrary 15% discount and choose **INSUFFICIENT**. This is not a clean test-3 control. `changed: true` fits the first-judgement instruction; “First judgement.” is again terse. |

Plants 5 and 6 also show the central ambiguity in the form: test 2 asks whether the remaining material **would lead to the selected rung**, while test 5 permits `INSUFFICIENT` when no rung can be preferred. A missed plant must not automatically be treated as reader failure until its expected verdict is independently unambiguous.

All six retain the same displayed answer fields because the builder copies a stored answer and changes selected fields. The packet omits citations and pushes for **all** answers, so that omission does not single out the plants. The short invented explanations in plants 5 and 6 nevertheless differ noticeably from many fuller stored explanations. [Plants](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/build_baseline.py:22)

3. **`not_shown`**

The membership rule is a reasonable historical reconstruction of production’s rule: take links through the judgement’s sequence, remove evidence replaced by then, and subtract the IDs listed in that request. Production’s current-state function similarly takes linked evidence and removes replaced items; using the finished database without a sequence cutoff would incorrectly include later changes. [Historical reconstruction](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/stored_judgements.py:38), [production evidence in force](/Users/lchingen/hivemind/src/hivemind/views/store.py:412), [request IDs](/Users/lchingen/hivemind/src/hivemind/views/judging.py:188)

For **d2, v18, judgement 50**, sequence **243**, the database has 47 linked evidence IDs by that point and no replacements in that draw. The request lists 18 of those IDs; the packet’s `not_shown` has the other **29**. For example, **e118** was linked at sequence 54, is absent from the request and appears in `not_shown`. That checks the set for this case.

There is a presentation limitation: production attaches replacement and revision context to evidence records, while `not_shown_of` returns only selected fields and does not attach that context. The membership test may be right while a reader lacks context needed to assess E in a case with replacements or revisions. The code also calls the user-message text `request_as_sent`; it does **not** include the actual system message or schema. The form supplies the judge’s rules separately, but the label overstates what is in each packet. [Stored judgements](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/stored_judgements.py:27)

4. **The count and stop conditions**

The core counting works for completed, valid rows: matching `INSUFFICIENT` verdicts remain `INSUFFICIENT` and are excluded from both decided-share denominators. Repeats are matched back to their original stored judgement and printed for each family; they do not enter the main count twice. [Count](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/baseline_count.py:43)

The failure handling is not ready:

- A **missing third-reader row** becomes `unresolved`, and the program continues to print shares. That treats an unfinished reading like an actual disagreement between two third readers. It should distinguish missing from genuinely unresolved.
- A missing **first-reader** row stops execution, but the last-judgement `NOT MEASURED` condition is not reported as such. Conversely, a complete pair of `INSUFFICIENT` verdicts is valid and should not be confused with a missing verdict.
- When both miss a plant, a family misses two, or disagreement exceeds one third, the program prints a warning but **continues to print ordinary shares**. It does not produce an authoritative stopped or `NOT MEASURED` result.
- It does not enforce the **30 decided** or **zero-denominator** conditions. It prints “none decided” or `0/0`.
- It silently overwrites duplicate judgement rows and ignores lines not beginning with `{`. It checks only that first-reader verdicts are valid; missing or invalid other fields can be counted as though there were no defect. Third-reader verdicts are not checked for completeness before results are calculated.

The third-reader brief asks readers to consider both first readers’ reasons. That is a deliberate adjudication procedure, but it is not an independent second measurement: those reasons may influence the ruling. [Third-reader brief](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-b-third-reader-brief.md:10)

5. **What packets reveal**

The key, including the original rung, is outside the reader folder. I found no explicit control label, draw name, or `stored_rung` field in the packet items. The requests do expose production thesis and evidence IDs, which are part of the request; they are not themselves draw labels. [Builder](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/build_baseline.py:107)

But the placement makes controls conspicuous. Each affected packet contains a consecutive run of one question and **exactly one item from another question**, always at an end. For example, judgement **26** in packet 5 is the lone 2027 capex question alongside another question’s chunk. The reader need not see the key to identify the outlier. Even if repeats and plants are indistinguishable from one another, the reader can give all outliers extra scrutiny. This conflicts with the design’s requirement that planted answers cannot be told apart. [Placement](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/build_baseline.py:95)

Large packets add a separate risk: attention and context limits may affect the last items or cause skipped details. The stated 2.3-hour estimate comes from 159 judgements at 51 seconds each, but the actual workload includes nine controls and long requests; it is not a measured budget for these 33 packets.

6. **What could mislead even if the procedure is followed**

The result measures agreement with a form on **159 correlated judgements across 16 views**, not 159 independent questions. Repeated daily conclusions can dominate the overall share; the last-judgement share partly exposes that, but its denominator is only 16. A change in the mix of topics and answer types can move either share without a change in judge quality.

The plants mainly test conspicuous errors. They do not establish that readers reliably identify subtle errors or avoid falsely rejecting sound forecasts. Three repeats provide only a very small check of consistency. Both readers can share the same mistake, and the third readers receive their reasons. Finally, the result tests the frozen judge on **hand-written ladders**; it cannot establish that the new ladders are sound or isolate their effect without a comparable later reading. Stage A has **not passed**. [Design’s comparison limits](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:1512)

**Not ready — first conceal control placement and replace or independently resolve ambiguous/telltale plants; then make the count distinguish missing from disputed readings, enforce and report the applicable stop conditions, and produce both promised shares and their unresolved ranges.**


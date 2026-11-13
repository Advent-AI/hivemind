**Not ready.** The fourth review’s main gaps are substantially addressed, but the count can still accept an ordinary session that exceeded the plan’s 60-minute limit. It also does not check packet contents as completely as the plan says.

For example, if a packet returns after 61 minutes because the operator missed the stop time, the plan says it should have been stopped and retried. The count accepts a `"returned"` session of any nonnegative duration, provided the family’s total stays within five hours. It can then print shares for a reading that did not follow the plan. [Plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/BASELINE.md:55), [count](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/baseline_count.py:151)

### 1. Fourth review findings

| Finding | Status | Evidence |
|---|---|---|
| Packet shape could identify controls | **Closed for the inspected trial**, as in the fourth review. The builder keeps the same question from appearing twice in a packet. [Builder](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/build_baseline.py:146) |
| Plants 5 and 6 could be disputed | **Closed for the planned trial; the disclosed limit remains.** Both families called all six plants UNSUPPORTED and named the stored rung. For validation judgement **7**, they cited the shipment plan and evidence excluding Rubin from the reported delay; for **12**, they cited the unsupported 20% cut. Agreement is a screen, not proof that those forecasts are beyond dispute. [Plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/BASELINE.md:44) |
| Plant 3’s “has since” tell | **Closed.** Trial judgement **3** adds Google’s guidance to the four-company plan without that claim. [Plant](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/build_baseline.py:31) |
| A test left without a plant | **Closed.** The plan says not to start, and the count refuses a set without a plant for each test. [Plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/BASELINE.md:48), [count](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/baseline_count.py:106) |
| Invalid times and retries | **Partly closed.** The count now requires one or two logged attempts ending in a return and refuses two stopped attempts. It still accepts a return after the 60-minute stop limit. [Count](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/baseline_count.py:138) |
| Population identity and repeat twin | **Partly closed.** Each keyed item is compared with the stored or planted content, and the three repeats are checked. But the packet check collapses rows by judgement number, so it does not establish full packet equality. [Count](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/baseline_count.py:112) |
| Invalid E, flaw and reason fields | **Closed for the reported cases.** The specified field checks are present; a nonempty string still cannot establish that a reason is meaningful. [Count](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/baseline_count.py:57) |
| Both readers miss a plant | **Partly closed.** The plan now stops and discards the reading in either diagnosis, then restarts. It explicitly proposes replacing a faulty plant, while the design says the reading stops “until the form is mended.” That departure is disclosed but is not the design’s unconditional instruction. [Plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/BASELINE.md:99), [design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:1489) |
| Five-hour limit presented as the design’s exact rule | **Closed.** The plan labels the calculation as its interpretation. [Plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/BASELINE.md:104) |
| Future Stage B packet shape fixed prematurely | **Closed.** The plan reserves that choice for Alex and notes the comparison consequence. [Plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/BASELINE.md:22) |
| No known-sound control and chance of false stop | **Closed as a disclosed measurement limit.** The plan gives illustrative probabilities and says the trial cannot establish that readers accept sound forecasts. [Plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/BASELINE.md:110) |
| Rows not tied to packet sessions | **Closed for the reported failure.** Each answer file must contain exactly its packet’s judgement numbers, and each packet needs a successful final logged attempt. The log remains the operator’s record, as disclosed. [Count](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/baseline_count.py:175) |
| Changed packet content not detected | **Partly closed.** A changed keyed row is rejected, including the saved check’s added sentence. Full packet equality is not established because duplicate numbers can be overwritten during checking. [Count](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/baseline_count.py:112) |
| Checks did not assert the share values | **Closed for the saved sound case.** It asserts both shares, including the three treatments of unresolved verdicts: **0/156** unsupported and **15/15** supported for last judgements when unresolved are left out. The saved output reports 18 of 18 cases as expected. [Check](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/check_count.py:17), [saved output](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/check_count.output.txt:1) |

### 2. Can an incomplete reading print a result?

**Yes. The 60-minute case is serious.** A late return can be recorded truthfully; no falsified log is needed. The count checks the five-hour family total but not the per-session stop rule. A normal missed timeout can therefore pass.

**Packet equality is also a serious enforcement gap.** `record_problems` puts packet rows in a dictionary keyed by judgement number. If packet 1 accidentally contains two rows numbered **1**, an earlier altered row followed by the correct row is overwritten during checking. The reader sees both, while the answer-file check expects only the one number. The count can accept that packet although it is not the packet the builder made. [Count](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/baseline_count.py:112)

The session log could also falsely claim a stopped session returned, but that requires an untrue record; the plan explicitly discloses that the count cannot prove the log is truthful. That is a **refinement**, not a new serious finding.

### 3. Plan, code and authority

D426 authorizes the preparation and this baseline reading, says Stage A has not passed, and requires Alex’s word again before a paid Stage B send. The plan states those boundaries. [D426](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4721)

Two promises need narrowing or enforcement:

- The plan says packets on disk must **equal** those rebuilt from the stored runs and trial result. The code compares the keyed contents but does not rebuild and compare the complete packet lists, including duplicates and placement. [Plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/BASELINE.md:85)
- The plan requires the author’s own read of every judgement either first reader calls UNSUPPORTED. The count does not check that this read exists; it remains a human reporting step. [Plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/BASELINE.md:60)

The faulty-plant branch is expressly described, but it goes beyond the design’s instruction to mend the form after a plant is missed by both. It should be reconciled with that instruction before relying on the branch.

The individual-judgement packet shape, two third readers, repeats and five-hour interpretation are identified as the plan author’s choices. The lack of a known-sound control and the dependence between daily judgements are also disclosed.

### 4. What remains

The six-plant trial and the saved count checks are meaningful progress, and the principal association failure from the fourth review is addressed. The **timeout** and **complete packet comparison** gaps remain serious because an honest operator’s ordinary mistake can produce a result the plan says should not be used.

**Not ready — enforce the 60-minute session rule and compare complete packets against the builder’s expected packets; reconcile the faulty-plant branch with the design before readers start.**
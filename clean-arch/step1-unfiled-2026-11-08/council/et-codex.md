**BLOCKER — do not send yet.** The probe can declare success when the required fact was never delivered, and its stated cost is an estimate rather than a limit.

1. **Control:** The code reuses the captured `sent_request`; the seeded request changes only `open_theses`. The check compares only the stored and sent user messages, so it does not independently prove the entire captured request against what production sent. [Probe](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/stage1_probe.py:59)

2. **Fact matching:** A 30-character fragment anywhere inside a gold passage counts as the whole fact. For i163, a passage about Micron’s margin can therefore count as Nvidia’s roughly 66% margin. A correct partial quotation with different boundaries can also miss. [Matcher](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/stage1_probe.py:41)

3. **Conditions:** They are computable for successful records, but errors and refusals have no defined outcome. More seriously, each condition accepts *any* gold item in a case: q10-guidance includes revenue and EPS as well as margin, so a link to revenue can satisfy the margin test. Target IDs are counted without checking link type. The selected articles are already known to have tuned c8, as the plan acknowledges. [Frozen conditions](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/stage1-frozen.md:13)

4. **Cost and writes:** `$0.54` assumes 6,000 output tokens, while the captured request permits 64,000. Transport can retry up to three times; `--draws` is unrestricted. Python imports may also create bytecode caches outside the output folder. [Send](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/stage1_probe.py:81)

**BLOCKER**
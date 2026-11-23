**Gate 2 is not ready to show Alex.** Its controls cover several relevant neighbours, but the written pass rule can declare success when answers are missing, and some of the promised checks do not actually count lost links.

For example, if the new version keeps Goldman’s estimate but leaves it unattached to the existing question, the table says the expected result is a link, yet its stop only counts a new question or a dropped statement. That regression could pass unnoticed. [Gate 2, lines 13–23](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:13)

1. **Controls and omissions**

   **Serious:** The six controls cover repeats, another estimate of the same total, a deadline, a two-year price comparison, and Ohio. Those are sensible neighbours of the actual changes: the new wording distinguishes years and explicitly mentions combined spending. But the repeat and Goldman checks need to count evidence that is kept **without the required link**. The earlier plan also explicitly counted unlinked memory-price statements; Gate 2 dropped that check. [Prompt changes](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c15yc-system.txt:102), [earlier control lines](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/DIAGNOSIS.md:174)

   The small-obligation omission is only partly justified. Gate 1 tested that article under the customer wording alone, on one stored state and three sends per version; it did **not** test both changes together across the three available states. The year wording is scoped to shared quantities, but that does not prove the combined request cannot affect the obligation answer. The stored states make that interaction test available at the same per-control cost. [Gate 1 reading](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/gate1/G1B-READING.md:8), [stored cases](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/cases-c14.json)

   The fiscal-versus-calendar omission is honestly disclosed, but it remains an **untested risk**, not evidence of safety. The earlier plan called for choosing an article before this stage; the current design says none is stored. [Earlier plan](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/DIAGNOSIS.md:174), [Gate 2](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:30)

2. **Decision rules**

   **Serious:**

   - A refused or twice-cut answer is counted as having no bad outcome. If all nine new-version answers fail, the new version can appear to have zero bad outcomes and pass. A missing usable answer needs an explicit outcome that cannot be mistaken for success. [Gate 2](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:20)
   - A lost send makes a state unexercised, but “pass” is simply “no stop fires.” The document does not say whether an unexercised state prevents the control or the whole gate from passing. It also does not cover attempts never sent because the ceiling was reached, unfinished answers, or repeated malformed answers; the harness can produce each. [Gate 2](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:23), [harness](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/probe_c14.py:150)
   - The memory reader’s categories do not specify how to turn multiple questions in a send into “a change question lost,” or what to do when a question fits more than one category. “The source decides” does not specify who resolves a disagreement or how. Fix the comparison and disagreement procedure before seeing answers. [Gate 2](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:24)

   **Wording-level:** The tolerance of **more than two** was declared in advance; it is not a new line chosen after these answers. It deliberately permits a difference of two out of nine and is not proof of no regression. State that limitation beside the pass rule. [Earlier plan](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/DIAGNOSIS.md:174)

3. **Cost and ceiling**

   The arithmetic is right: 6 × 3 × 2 × 3 = **108 planned sends**, and $0.0135 × 108 is **$1.46**, reasonably rounded to $1.5. Gate 1 spent $0.83 across 45 initial attempts and 18 re-send attempts, including three network losses; that supports an approximate estimate, though the document should show exactly how it derived its $0.0135 mean. Retries and differences in answer length can raise the actual cost. [Gate 1 log](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:4980)

   The **$2 limit is a reservation-based stop, not an absolute bill guarantee**: a response above its reservation can exceed the limit while other attempts are already in flight. The existing preflight says so; Gate 2 should say the same when presenting the ceiling. A ceiling stop also needs the missing-result rule above. [Preflight](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/gate1/PREFLIGHT.md:18), [harness](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/probe_c14.py:122)

4. **Before the sends**

   **Serious:** Specify the completed-control requirement, all missing and failed-answer outcomes, link checks, and the memory comparison before Alex reviews the lines. Decide whether to include the available small-obligation states for the combined change. Then run the stated no-cost preflight and report its results before any paid send. Keep the year result visible as **5 of 9 against the original 8-of-9 line**, as Alex’s decision requires; carrying it forward did not turn it into a pass. [D437](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4857)

Gate 2 ready to show Alex: no
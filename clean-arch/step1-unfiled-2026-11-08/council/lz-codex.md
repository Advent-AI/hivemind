**Gate 2 is not ready to show Alex.** The revised plan closes several findings from the first review, but its decision rules can still let a real loss pass, and some failure cases have no defined result.

For example, if the new version drops a repeated capex statement entirely, the repeat check does not count that as bad: it only counts the statement when it is **kept without a link**. The plan could therefore say the control passed even though the reader lost information. [Gate 2, lines 15–16](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:15)

1. **Controls and omissions**

   The plan now has **seven controls and 126 planned sends**, rather than six and 108. They cover the main neighbours of the two changes: repeats, another estimate of the same total, a deadline, a two-year comparison, a small obligation, and Ohio. The prompt changes concern separate years and combined spending; the closing check also changes how the same aggregate is recognized. [System prompt diff](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c15yc-system.txt:102), [closing check](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c15yc-closing.txt:14)

   **Serious:** The checks for repeats and memory count a kept statement without a link, but do not say that dropping the statement is bad. The small-obligation check forbids extra questions but does not count losing the existing amount question. Those outcomes are within the stated goal of checking what c8 handles. Define them before the answers are read. [Gate 2, lines 15–20](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:15)

   The earlier review’s small-obligation omission is closed: the case is now included for both changes together across the three stored states. The fiscal-versus-calendar case remains explicitly untested. The plan says no stored article exercises it; I did not independently establish that across all stored articles. The listed cases contain no such control, so the plan cannot claim that risk is safe. [Stored cases](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/cases-c14.json), [Gate 2, lines 40–41](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:40)

2. **Decision rules**

   **Serious:**

   - The memory reader can produce **three different marks**. In that case there is no majority, so the stated tie resolution cannot decide the result. Define the resolution before reading answers. [Gate 2, lines 33–39](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:33)
   - For Ohio, an unusable answer is called a bad outcome, but the special stop compares only counts that **open the signing question**. An unusable answer cannot be classified as opening it, and the plan does not say how to combine those rules. [Gate 2, lines 23–29](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:23)
   - The memory comparison depends on whether **any** c8 send on a state asks a change question. Once one does, every c8 send without one also counts as bad. For example, one of three c8 sends asking it and none of three candidate sends asking it produces a difference of only one; the control can pass even though the candidate never asks it. The comparison needs a predeclared rule that matches the intended loss being tested. [Gate 2, line 19](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:19)
   - The harness records exceptions other than `TransportError`, but the plan does not classify them as an unusable answer or an unexercised send. It also does not state what happens if processing a received response raises an unexpected exception. Define how these prevent a pass. [Harness, lines 163–175](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/probe_c14.py:163)

   The earlier findings on **lost sends and the pass rule** are otherwise addressed: a lost or ceiling-blocked send makes its control unexercised, and every control must be exercised to pass. The tolerance of more than two was set before the earlier send, and the plan now says a difference of two can pass. [Earlier plan](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/DIAGNOSIS.md:183), [Gate 2, lines 26–32](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:26)

3. **Cost and ceiling**

   The revised arithmetic is right: **7 × 3 states × 2 versions × 3 sends = 126 sends**. The preflight estimates **$1.82**, consistent with “about $1.8.” Gate 1’s recorded $0.83 over 63 attempts is about $0.013 per attempt; network losses and different answer lengths limit how precisely it predicts this run. [Preflight](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/gate2/PREFLIGHT.md:3), [Gate 1 log](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:4980)

   The **$2.20 ceiling is a reservation-based stop, not an absolute bill guarantee**, as the revised plan correctly states. Attempts already in flight can cause an overrun. [Harness, lines 122–144](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/probe_c14.py:122)

4. **Before any sends**

   Resolve the serious gaps above, then review the revised lines before showing them to Alex. The recorded preflight reports 126 rebuilt requests and 21 stored answers passing the checks; I reviewed that record, but did not independently rerun it. [Preflight](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/gate2/PREFLIGHT.md:3)

   **Wording-level:** Keep the failed year result visible as **5 of 9 against the 8-of-9 line**. The current plan does this correctly; Alex chose to carry it forward, not to relabel it a pass. [D437](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4857)

Gate 2 ready to show Alex: no
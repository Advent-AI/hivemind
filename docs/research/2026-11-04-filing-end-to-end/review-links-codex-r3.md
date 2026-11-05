**Not ready for the test. Four serious issues remain.** The new sentence settles the rack-price example, but other choices remain unresolved, and the proposed measurement can credit improvements the judge never receives.

1. **The tie sentence does not settle all the known cases.**  
   In call **204**, it selects product revenue (`v20`) for the $7.8 million rack price. But the stored statement combining the **$55,000 Rubin GPU** and **$5,000 Vera CPU** prices still fits two specific questions about the same party: `v20` and `v19`.

   In call **370**, Broadcom’s revenue and guidance bear on custom-chip spending (`v16`) and NVIDIA’s accelerator share (`v6`). Neither question is about Broadcom itself, so “take the one about the party it describes” selects neither. D207 requires the narrowest home; it supplies no further choice here. Standard §6 concerns weight, not this choice. The [exact rule](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/links-v74l.json:4) therefore leaves part of the round-2 finding open.

2. **The amendment would count facts that never reach the relevant judge.**  
   [Amendment lines 22–23](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/prd-amendment-proposal.md:22) credit a question when evidence is filed under another question that supports it in the seed tree.

   The stored database has `v16` depending on `v6`. The share question, `v6`, depends on `v2`; it does **not** read `v16`. The judge reads [its own linked evidence](/Users/lchingen/hivemind/src/hivemind/views/judging.py:41) and the conclusions of its recorded dependencies. Filing Broadcom’s figures only under `v16` therefore does not deliver them to `v6`.

   Five frozen gold items are used by both questions, including Broadcom’s $16 billion guidance. Crediting them to both would hide a real loss against the [PRD’s goal](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md:19). The existing wiring defect need not be fixed in this task, but the measurement must not pretend it is fixed.

3. **Using averages does not resolve the control-variability problem.**  
   The stored control reaches **58 / 60 / 65** facts: mean **61**. The proposed development requirement remains “mean above 65.” The existing `definition_no_fallback` answers reach **66 / 66 / 62**, mean **64.67**, and still fail that requirement despite improving average reach.

   More decisively, the unchanged control’s noise counts are **37 / 36 / 29**, mean **34**. Of the 27 three-answer combinations resampled from those same control answers, **11 fail** the proposed “noise mean no higher than control” guard. This is a diagnostic resampling result, not a measured future failure rate. It nevertheless shows that unchanged behavior can fail the guard through observed variability alone. The [amendment](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/prd-amendment-proposal.md:20) has not yet demonstrated that its requirements distinguish harm from sampling variation.

4. **The named measurement script can mistake moving noise for removing it.**  
   The PRD explicitly counts [both revenue questions, `v1` and `v22`](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md:99). But [the script counts only `v1`](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/measure_filing.py:154), and does not calculate the required per-question noise guard.

   I tested this entirely in memory: moved only gold-labelled noise or unused facts from `v1` to `v22`, leaving their text unchanged. Its reported revenue-pile counts fell from **36 / 42 / 43** to **10 / 13 / 19**—passing the proposed halving requirement. Fact reach and total noise were unchanged. The script would reward relocating the problem.

No prior version/configuration collision was found for **v74l / poc-v115**. Their meaningful occurrences belong to this proposal and its review records.

No files were edited and no model calls were sent.
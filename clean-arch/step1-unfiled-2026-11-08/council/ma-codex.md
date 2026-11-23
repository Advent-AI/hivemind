**Gate 2 is not ready to show Alex.** Version 3 closes most of the previous review’s findings, but its memory control can still pass after losing evidence, and the harness treats some non-network failures as network losses.

For example, a new answer could keep a memory-price question but drop every memory-price statement. The design would call it good because it only requires statements that *are kept* to be linked. [Gate 2, memory control](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:22)

1. **Controls and omissions**

   **Serious:** The proposed closed-set rule does not yet close the whole class identified in the last review. It now catches dropped repeat statements and a lost credit-support amount question, but the memory control still permits all memory-price statements to be dropped. It needs to say which source statements must be retained and linked. Ohio is also governed by two special counts rather than a defined good send, so the claim that *every* control has a closed set is not literally true. [Gate 2](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:16)

   The current design has **seven controls and 126 sends**, not six and 108. The additional credit-support control addresses the previous omission: it tests both changes together on all three stored states. The other controls cover the relevant neighbours: repeated annual figures, another estimate of the aggregate, an event’s later deadline, a two-year comparison, and Ohio. These follow the actual changes to the year boundary and combined-spending example. [Prompt changes](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c15yc-system.txt:102), [closing check](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c15yc-closing.txt:14), [stored cases](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/cases-c14.json)

   The fiscal-versus-calendar-year case remains **untested**. The design says no suitable stored state was found; I confirmed it is absent from the listed cases, but did not independently establish that it is absent from all stored material. That supports disclosing the gap, not claiming the risk is safe. [Original controls](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/DIAGNOSIS.md:174), [Gate 2](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:47)

2. **Decision rules**

   **Serious:** The harness equates `TransportError` with a network failure. The transport also uses that exception for HTTP errors and malformed HTTP responses, including responses whose body arrived. Those cases can be retried and ultimately treated as unexercised, although the design says non-network errors are bad sends. The distinction needs to be decided and recorded consistently before sending. [Harness](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/probe_c14.py:163), [transport](/Users/lchingen/hivemind/src/hivemind/model.py:126)

   The other specific findings from the last review are addressed: the memory comparison now counts sends with a change question directly; the reader has categories, a disagreement procedure and a three-way fallback; Ohio separately compares unusable answers; processing exceptions are recorded; and a lost, missing or ceiling-blocked send prevents a pass. The tolerance was fixed earlier and explicitly allows a difference of two out of nine. These rules still require people to apply the definitions to the answers, but the comparison and tie-breaking procedure are stated in advance. [Gate 2 rules](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:26), [earlier tolerance](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/DIAGNOSIS.md:183)

   **Wording-level:** State explicitly that Ohio’s signing-question count applies to usable answers; unusable answers are handled by its separate comparison. That makes the intended reading easier to follow.

3. **Cost and ceiling**

   The arithmetic is right: **7 × 3 stored states × 2 versions × 3 sends = 126 sends**. Gate 1 spent **$0.83 over 63 attempts**, approximately $0.013 per attempt. The recorded preflight estimates **$1.82** for this run, so “about $1.8” is reasonable; retries and answer length make it an estimate. [Gate 1 log](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:4980), [preflight](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/gate2/PREFLIGHT.md:3)

   The **$2.20 ceiling is not an absolute bill guarantee**. The design correctly says attempts already in flight can cause an overrun. [Gate 2](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/GATE2.md:50)

4. **Anything else before the sends**

   **Serious:** An exception before the harness settles a reservation can leave that reservation outstanding. For example, a valid JSON HTTP response that is not an object would fail at `response.get(...)`; the outer handler records the error, but does not release the reservation. If enough reservations remain outstanding, later attempts can wait indefinitely. Check and handle that path before the run. [Harness](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/probe_c14.py:122)

   The preflight record reports that all 126 requests rebuilt and all 21 stored answers passed the checks. I reviewed the record; I did not rerun it. The year result remains correctly disclosed as **5 of 9 against the original 8-of-9 line**; Alex authorized carrying the changes forward, not relabeling that result as a pass. [Preflight](/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/gate2/PREFLIGHT.md:3), [D437](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4857)

Gate 2 ready to show Alex: no
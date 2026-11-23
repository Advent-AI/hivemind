NOT READY.

The replay’s restart instructions conflict: one says every stopped replay starts over, while another says to retry once and stop after a second failure. An engineer could build either behavior.

1. **The replay’s restart limit is unresolved.** [DESIGN.md:597](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:597) says a stopped replay is redone from the start in a new folder. [DESIGN.md:622](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:622) says that rule applies once and a second stop reports the draw incomplete. That leaves different behavior after a second judgement refusal. State one rule for every replay stop, including who starts a new replay and whether there is a limit.

2. **The shared stop needs an atomic boundary.** [DESIGN.md:809](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:809) requires that no send begin after the stop flag is set, but says only that each worker *reads* the flag before sending. A worker can read “continue,” pause, then begin its send after another worker sets the flag. The current [budget.py:63](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/budget.py:63) has no shared stop boundary. Define how the flag check, reservation and decision that a send has begun are synchronized; test a worker paused between its check and send, including a transport retry.

The last review’s binding-obligation exception is restored at [DESIGN.md:496](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:496). Its shared-stop finding is addressed in intent, but the interleaving above remains open.

For the spending ledger, I did not find a reserve/send/charge/process-death interleaving that exceeds $3 or understates spend **assuming the reserved worst case bounds the actual charge and the specified synced writes succeed**. An unanswered reservation is reported in full. The stop issue concerns an additional send after the stop, rather than a demonstrated cap overrun.

**Wording:** [DESIGN.md:640](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:640) describes only the “quarter” branch of the old pattern; [extraction.py:435](/Users/lchingen/hivemind/src/hivemind/extraction.py:435) also matches forms such as `Q1` and certain half-year revenue expressions.

I walked every row of §7.1 and §7.3, the Stage A stop and spending rules, and the named code paths. I found no old candidate check in `sift` without a row. No row or sentence in this assigned angle remains unread.
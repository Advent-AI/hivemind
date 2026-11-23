# Council kc: the second-look test as built, before its send (same thread; read-only)

Alex chose it (D422 in `docs/DECISIONS-log.md`): the test only; adoption is his after the result.

Read `clean-arch/step4-2026-11-10/probe-second-look-2026-11-10/REGISTERED.md`, `sample.py`, `run.py`. Checked at no cost:
66 conversations rebuild, each first turn with its stored request's identity; one instruction, the same in all, naming no
group and no fault; the check function accepts every stored first answer.

Challenge: does the build depart from `DESIGN.md` anywhere; is the sample's grouping what the page says (an agreed fault:
both first readers, or both third readers, or a named fault both uphold); can the readers of the second answers tell changed
from unchanged, or infer a group; a way the pass condition can be met by the readers' own run-to-run difference instead of
by the second look, beyond what the page already separates. One line: send / do not send.

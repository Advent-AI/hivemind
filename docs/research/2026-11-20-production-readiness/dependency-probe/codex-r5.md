**The reading rule is ready. The spending guard still has a gap.** At $0.047 per call, six worst-case calls total $0.282 before judgement retries. The script reserves for one call at a time, then records only the usage returned by the successful transport attempt. Earlier timeouts could have incurred charges that disappear from the next budget check. [Probe script](/Users/lchingen/hivemind/docs/research/2026-11-20-production-readiness/dependency-probe/probe.py:96)

Use one transport attempt per call, reserve against the full serialized request, and keep the reservation charged when usage is unknown. If the cap stops the run before both arms have three samples, report it as inconclusive.

**DISAGREE**
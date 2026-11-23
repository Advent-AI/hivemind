# Council round 47e: after 47d (read-only, same thread)

47b–47d kept finding the same two mechanisms (process information inside the scoring packets; a packet-to-unit mapping that can move after reading), so 47d is answered by three structural rules (PAID-GATE.md §3e), not finding by finding:
1. Scoring text = only what the four questions need: per card the final answer's passages, figures, recomputed outcome, assumptions and card (`packet_body`, `card_lines`). No attempt history, no code decision, no check code; the verdict applies the run's decision. Earlier attempts go to attempts.md under separately shuffled D-labels with no packet link, unscored (`render_attempts`). A card with no final answer states why (`NO_ANSWER`: not sent / started, no answer recorded / no answer arrived / retry not sent / format).
2. The readers' text commits to the mapping: key = {salt, run_digest, order, attempts}; its sha256 is packets.md's first line (`key_commitment`, `render_packets`); `verdict` refuses a key that differs from that line, re-renders and compares with packets.md and the readings' sha. Rehearsed: swapping two packets with identical text → INCOMPLETE; a key with forged decisions → INCOMPLETE.
3. Reconciliation one to one (`merge`): a declared shared forecast is unified only when each call holds exactly one candidate for that quantity and scenario with the same value. Rehearsed: two candidates in the first call, and two in the second call (your R1 shape), each → C4 refusal.
Also: started-but-unfinished attempts are kept as interrupted in results.json, and their card says so.

Rehearsal 51 of 51 (three runs). Mutants 20 of 20, control passes. Plan unchanged (6f81dae5…).

Out of scope: the frozen ruler, production code, D725's verdict lines, the $0 gate's checks.

Output: READY TO SEND (once Alex names the ceiling) or NOT READY; only findings that would let the run spend outside the ceiling, lose a record, bias the comparison, or make the result unreadable or open to fitting. Cite file:line.

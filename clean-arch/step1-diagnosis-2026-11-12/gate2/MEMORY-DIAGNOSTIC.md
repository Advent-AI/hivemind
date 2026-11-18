# Gate 2's memory diagnostic (D440), fixed by council consensus before any send, 2026-11-13

Gate 2 failed under its declared rules (`READING.md`): two stop lines on the memory article, of which the link line measured the wrong
thing (c8 lines 7–9: an uncovered statement is returned with empty links) and the thesis line (c8 3 of 9 sends with a memory-price
thesis, c15yc 0 of 9) has no established cause. That failure stays on record. This diagnostic, agreed in council round mj
(`clean-arch/step1-unfiled-2026-11-08/council/mj-codex.md` to `mj-codex-4.md`; Claude's replies `mj-challenge-1..3.md`), decides
whether c15yc may go on.

- **Sample:** 18 fresh sends per stored draw per arm (c8, c15yc) on the memory article (step 56): 54 a side, 108 sends, ceiling $2.0.
  The first run's 9 a side and its 3-to-0 are reported beside it, not pooled. Each draw reported apart and combined.
- **Outcomes:** (1) a send with a memory-price thesis (decisive); (2) a send that retains every listed memory claim (M1, M2, M3 in d1
  and d2; M1 in d3), an empty link allowed (decisive); (3) a v5-like thesis, a 2027 price or the 2026-to-2027 change (reported).
- **Reading:** memory theses marked as GATE2.md says (my marks, a blind reader's, a third reader and the majority on a disagreement);
  retention by the claim rule (my reading and a blind reader's; a disagreement counts against c15yc and for c8).
- **Unusable answers** count against the arm that produced them (for c15yc: no thesis, not retained; for c8: a thesis, retained) and
  are reported apart; an unusable c8 answer is never described as having opened or retained anything.
- **Decision:** `gate2/memory_rule.py` (sha256 `4fd07cb685f78a2070841709078c92622a2de70a24d90b60475495eeffbb5ec3`): Newcombe's hybrid score interval (Wilson), two-sided 90%, for c15yc minus
  c8 on counts pooled over the three equal-size states; margin -22.2 points (the original 2-of-9 tolerance). Proceed if the lower bound
  is above the margin, stop if the upper bound is below it, otherwise inconclusive; inconclusive if no usable c8 answer opens a
  memory-price thesis (or the claims cannot be judged). c15yc goes on only if both decisive outcomes say proceed; inconclusive keeps c8
  and returns the question to the council.
- **Validated before the send** (`gate2/validate_memory_rule.output.txt`, reproduced by the council): erroneous proceed at the margin
  0.047 to 0.055; coverage 0.90 to 0.92; with no effect, proceed 0.81. Limits stated with any result: the 5% is approximate, sends are
  assumed independent, and "proceed" means the loss is within the chosen 22.2-point tolerance, not that the change has no effect.

**Completion, recorded before any answer was read (council round mj-5, `council/mj-codex-5.md`: "consensus on (a)"):** the first
run sent 97 of 108 jobs; 11 were never sent because the $2.0 ceiling's reservations held them back (10 c15yc in d3, sends 9–18, and
c8 d3 send 18), my pricing error (output averaged about 12,500 tokens a call, not 9,500). Those 11 jobs, and only those, are sent with
the same saved requests and settings into `poc/data/clean-step1-gate2-memory-completion-2026-11-13/`, under a new completion ceiling of
$1.2, a council-approved departure from D440's $2.0 step ceiling (the $40 total and provider caps unchanged). Before any answer is
read, the combined job identities must hold exactly 18 per arm per draw with no duplicates; if a completion job stays unsent, the
diagnostic is inconclusive. Both folders and every original outcome are kept. Reported with the result: ten of the eleven later calls
are c15yc in d3, so a change in the provider's behaviour over time could touch the comparison.


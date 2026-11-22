# Blind reading of six answers (read-only; no edits, no model calls)

Read `docs/research/2026-11-20-production-readiness/dependency-probe/run/reader-packet.md`: six answers, under shuffled labels, to
one judging question (NVIDIA FY2027 Data Center revenue, as of 2026-09-20), and the total-revenue question's conclusion of that day.
The evidence the requests listed is in `docs/research/2026-11-20-production-readiness/dependency-probe/run/control-request-user.txt`
(some requests also showed the total-revenue conclusion; you are not told which, and should not try to guess beyond what an answer
itself says).

Apply this rule to each answer, exactly as written, from the section "The reading rule" of
`docs/research/2026-11-20-production-readiness/dependency-probe/reading-rule.md` (A to E; read only that section and the
"Reconciles" line). For C, credit only a figure, guidance or growth rate present in the evidence file or in the quoted total-revenue
conclusion; for any range, report the midpoint and the lower bound.

Output, under 400 words: one table row per answer label (A's three figures, B, C with the unsupported step named, D with the room
in dollars, E, Reconciles yes / no / not tested), then two lines on anything the rule misses.

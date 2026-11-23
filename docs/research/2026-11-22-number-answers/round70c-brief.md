# Council round 70c (confirmation of round 70b's two fixes before the one-time paid send): read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

Round 70b (`docs/research/2026-11-22-number-answers/codex-r70b.md`) blocked the send for two reasons:
- the renderer skipped `pushes[].evidence_id`, so an unresolved E card hid 6 of the 15 passages it weighed;
- the range expansion had a width limit of 50.

Both were changed in `paid_gate.py` (`named_in_text` and the return of `card_view`). Nothing else changed since round 70b.
`PAID-GATE.md`'s last section records it.

## Check
1. **Render the cards again.** Render the six D751 answers (`poc/data/judging-v13s-blind7-2026-11-23/{S,E,P-v8}/answers/*.json`,
   each case's `item.json` as the plan item) and the D749/D750 answers through `card_lines` in memory. Does every passage named at card
   level (cites, pushes, prose including ranges) now appear? Does every prose figure reference resolve? Is every shown value the
   writer's?
2. **Does anything in the two changes reach beyond what round 70b asked?**
3. **Is the launch otherwise unchanged and ready?** The plan pin is `0dc7c310…`, the cap $0.50, the authorization absent, and the run
   folder absent.
4. **Verdict:** send, or do not send (with the blocking reason).

Return a short numbered report with citations, then the verdict.

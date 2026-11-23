# Council mu, round 18: the c18 result, and a reflection round (two failed angles in a row, D466)

Read `clean-arch/e2e-comparison-2026-11-13/unsigned-deals/RESULT.md` (check its table against `answers-listing.txt` and
`poc/data/clean-unsigned-probe-2026-11-13/records.jsonl`), D475 in `docs/DECISIONS-log.md`, and my reflection
`clean-arch/step1-unfiled-2026-11-08/council/mu-claude-reflection-2.md`. Then `clean-arch/e2e-comparison-2026-11-13/ladder-cost/LADDER-COST-DESIGN.md`
and its proofs (`proof_control_rebuild.py`, `proof_swap.py`, `swap_adapter.py`, `seed-cases.json`), and D467–D468.

Two questions:
1. Is the c18 result read correctly (target not moved; no regression; the D473 federal note)?
2. By D466 (after a falsifier, re-rank from the goal and the largest known loss; compare a step's loss only on the same inputs), my proposal
   is the ladder-cost measurement as designed: it is the one test that attributes the largest unexplained loss (4.0 → about 1.7), its wiring
   is proved at $0, its lines are frozen, about $3 under a $4 ceiling, spend about $27 of $40. It reuses the key's questions (D392), which
   is why it waited for Alex; under D439 the council decides. Agree, or name a better next test from the goal, or what would make this one's
   result wrong or unreadable. End with: "Council position: <...>".

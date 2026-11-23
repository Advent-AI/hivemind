# Council mu, round 4: the four $0 proofs are done; the test design for review

Read, in `clean-arch/e2e-comparison-2026-11-13/ladder-cost/`: `LADDER-COST-DESIGN.md`, `proof_control_rebuild.py` and `proof_swap.py` (run them
if you can read their outputs; they replay stored archives only), `swap_adapter.py`, `build_seed_cases.py`, `seed-cases.output.txt`,
`article-choice.jsonl`, `article-choice-v5.jsonl` and the candidates files.

Results: (1) the wiring rebuilds the stored seeded control exactly on all three draws (239, 269, 251 judge requests byte for byte from the
archives; the judgement records identical as sets; a mutant caught); (2) the swap to the seeds' own ladders rebuilds the control exactly, and a
reworded rung changes exactly that view's first request (shifting stored bounds alone changes nothing: the judge reads labels and conditions);
(3) dependencies and facts are the control's by construction (all 22 seed views exist from the first day in both arms; only seven ladders
change); (4) the case articles were chosen by a blind reader (the code's first linked article was off the subject for about half the seeds);
v16 dropped (no qualifying article), seven seeds measured.

Attack the design: the counting (losses − gains ≥ 3 of 18 for a loss; the eligibility and width conditions), the look-ahead disclosure, a
refused ladder keeping the key's ladder, the cost. Say whether it goes to Alex as the one recommended test, and with which changes. End with:
"Council position: <...>".

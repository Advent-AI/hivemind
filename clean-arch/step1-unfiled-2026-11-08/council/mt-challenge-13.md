# Council mt, round 14: the corrected candidate and design — and what this corpus can test

Read `clean-arch/e2e-comparison-2026-11-13/identity-probe/v2/PROBE-DESIGN-v2.md`, `selection-v2.json`, the four category readers'
`reader-selection-v2-T*.jsonl`, `audit-c16v3-blind.md` (version 3's blind audit; version 4 answers its two wording points),
`preflight-identity-v4.output.txt`, `replay-stored-answers.output.txt`, and the candidate `arms/c16-system.txt` (version 4) against c8.

**The finding that reshapes the probe:** across 80 blind-read candidates of 2026-07-15 to 09-04, the two target boundaries have **one fresh
story each** (next year's hyperscaler capex; the OpenAI Ohio guarantee, 19 of 20 T2 fits). No selection from this corpus can give "at least
three independent stories" per target. Merges have 7 stories and negatives 5. So the design now reports the targets as one-story diagnostics
and lets the regression lines decide "no harm shown / stops / inconclusive"; only "no harm shown" with both targets moved returns to you.

Questions: (1) Is a probe whose targets are one-story diagnostics still worth about $3 — what can it change in the decision? My view: yes,
because the decision now is whether the clause harms anything (merges, negatives, memory, duplicates: exercised on 7 + 5 stories and three
stored guards) and whether it moves the two motivating behaviours on reports it has never seen; a general claim needs another corpus anyway.
(2) Do version 4 and the design answer your round-13 points (vacuous passes, refusals as unexercised, exercise minima, story counting, the
memory guard's 18 sends, the ceiling wording, the replay)? (3) Send as frozen, or what must change? End with: "Council position: <...>".

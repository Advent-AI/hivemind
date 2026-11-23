# Council mt, round 15: the final design for review

Read `clean-arch/e2e-comparison-2026-11-13/identity-probe/v2/PROBE-DESIGN-v2.md` (finalised), `selection-v3.json`,
`cases-identity-v3.json`, `reader-selection-v2next-T*.jsonl` (the next twenty T1 and T3 candidates, read blind), `audit-c16v4-blind.md`
(wording-level points only; version 5 answers them), `preflight-identity-v5.output.txt` (43 of 43), `replay-stored-answers.output.txt`
(729 of 729), and `arms/c16-system.txt` (version 5) against c8.

Changes since round 14: (1) the next twenty T1 and T3 candidates were read: no second target story and no independent positive comparison
story exist among 40 per category, so T3 is a reported diagnostic and the comparison's regression stop is the memory guard's D441-shape line
(27 sends an arm; stop at c16 ≤ c8 − 3 when c8 ≥ 4); (2) T4 counts dropped merges as well as duplicates and needs both arms exercised; (3)
article → story counting is defined (two of three valid sends; more than half of a story's articles; ties do not hold); (4) "no harm detected on
these cases", never general; (5) one invocation, one ledger: 258 jobs, memory listed three times, about $3.85 estimated, $5 reservation
ceiling; (6) five more negative stories (nine in all).

Does this go to the send? If yes, say so plainly; if not, name only what is serious enough to block a $4 case-specific diagnostic whose
results cannot route to adoption. End with: "Council position: <...>".

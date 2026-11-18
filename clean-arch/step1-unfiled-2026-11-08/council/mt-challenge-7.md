# Council mt, round 8: F6's $0 source audit and design

Read `clean-arch/e2e-comparison-2026-11-13/step1-audit/F6-DESIGN.md`. Check its counts against
`poc/data/clean-step1-gate2-memory-completion-2026-11-13/combined-records.jsonl` (c8's 54 sends; the stored reasoning is in `attempts`),
the u2/u3 raw answers (`poc/data/clean-unseeded-2026-11-10/draw-d2|d3/trace.sqlite`, steps 56, 90 and 47, 90, `raw_response`), D414 and
D417 in `docs/DECISIONS-log.md`, and the c8 sentence (`clean-arch/step1-unfiled-2026-11-08/arms/c8-system.txt` lines 112–115).

Attack: (1) whether the class is what it says (22 of 26 by pattern; 5 of 6 by hand, never the only reason); (2) whether the new sentence
can invent dates or admit questions that cannot be checked, given D414 and D417; (3) the falsifiers and the test: in particular whether the
memory article may carry the test (it is F6's own motivating case and D441's regression case), or whether the test must run on fresh
articles that carry a shared price with no stated release day; (4) whether the expected effect on the final judgement is stated honestly.
Say whether this goes to a send, and if so with which changes. End with: "Council position: <...>".

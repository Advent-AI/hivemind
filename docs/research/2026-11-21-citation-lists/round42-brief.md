# Council round 42 (Council B): the probe's result, before it goes to Alex (read-only)

The paid probe ran ($0.274 of $0.50; 122 sends, all answered; A2 skipped by its headroom rule). Read:
`poc/data/citation-probe-2026-11-22/` — `run-summary.json`, `answers.jsonl`, `packet-B.json`, `packet-C.json`, `readings-claude.json`
(first reader), `readings-codex.json` (blind reader), `adjudication-case.json` with `docs/research/2026-11-21-citation-lists/
adjudication-preregistration.md`, `adjudication-codex.md` (fresh Codex adjudicator; the fresh Claude adjudicator gave the same
decisions: confirmed (b) for linked-1:8776, omitted for the four Part B items), `readings-final.json`.

The registered verdict (`probe_read.py verdict`): NOT READY — confirmed material harm in Part C, linked-1:8776 (b): v12 #2 and #3 name
Bloomberg for the $393 billion reference while citing only e669 (Wall Street average via Yahoo Finance), every v7 answer cites e195
(Bloomberg). Claude's first reading had called it "not a harm"; the blind reader and both adjudicators applied the rule as written.

Beside the verdict (not changing it):
- What v12 was built to fix: 48 of 48 Part B answers format-valid and passing the request-time check (the 16 requests had produced 17
  refusals under v7); 0 misattributions; every material target with valid support in all three draws; all 24 placement readings correct;
  0 refusals in 72 Part C answers; the 72 Part C rungs identical across arms; v12 cites one source per claim where v7 often cites every
  duplicate or every listed entry.
- Rejection check (AGENTS §7.3): a $0 census of "an outlet named in the answer's text that no cited entry names", hand-checked. A first
  census mis-flagged linked-1:8768 (the Bloomberg figure is carried by the cited dependency v14, which the census skipped). Corrected:
  matched Part C, v12 2 of 36 (8776 #2, #3) vs v7 1 of 36 (8776 v7 #3 names Zacks' 80% citing neither Zacks entry); Part B, v12 1 of 48
  (8807 #1, "Bloomberg/Yahoo Finance", cites e669). The slip exists in both formats; the counts cannot tell whether v12 raises it.

Questions:
1. Is the verdict computed exactly by the registered rule, and is the adjudication sound? Anything misread?
2. Is the rejection check stated correctly and without overreach?
3. The next step for Alex (one recommendation; the choice is his). Candidates: (A) stop — v12 not adopted, poc-v118 stays; (B) a small
   registered follow-up that measures the outlet-label slip rate, v12 against v7, on the requests where two outlets carry the same figure,
   with a pass rule written first; (C) adopt v12 overriding the registered verdict because the class is pre-existing (Claude does not
   recommend overriding a registered verdict). Which, and what would the follow-up need to decide anything?
Answer with your position and blocking corrections only.

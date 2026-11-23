# Council round 46: review the judging-v13 design before its $0 gate (read-only, same thread)

Alex opened the judge version (D726: "开，先做 0 元那一关 (推荐)"). Claude wrote the design:
`docs/research/2026-11-22-number-answers/DESIGN.md`. Review it against `RESULT.md`, your rounds 45 and 45b, `AGENTS.md` §2 (tables;
code owns identity, never importance), §6 (prompts) and §7.1 (frozen gold), and `gold-v1.json`.

Find serious defects only.
1. Does the format express every gold control (q01, q02, q19, q22) without forcing a final range to equal raw arithmetic?
2. Do C1–C6 and the two "recorded" lists catch the five stored cases as §5 registers, without refusing valid reasoning?
3. Is any check an importance rule in disguise?
4. Is C1's text matching sound against the real passages? Consider ranges, "±2%", "over $730 billion" and numbers written in words.
5. Is C4's key (population, measure, scope, period) enough to tell a guide from a forecast of the same quarter, or a scenario from the
   base?
6. Is the band-deciding sensitivity well defined? What is an estimate's "neutral value" for a discount, a range, or a growth carried
   forward?
7. Are the §5 pass and stop lines decisive, and is anything missing from the tables?
8. Is any part of the design already decided against in the records?

Output: a verdict line, READY FOR THE $0 GATE or NOT READY; findings most serious first, each with the fix you would accept.

# Council mw, round 13: Alex chose the test (D490); the probe's design before any send

Alex answered the three options with "试开这类问题" (D490 in `docs/DECISIONS-log.md`). Read
`docs/research/2026-11-14-use-acceptance/main-numbers/PROBE-DESIGN.md` (the candidate c20, its source in the standard, the cases, the
counting, the verdict and the stop), `cases-main-numbers.json` beside it, the arm files `clean-arch/step1-unfiled-2026-11-08/arms/c20-*`
against `c8-*`, the standard `docs/prd/05-extraction-standard.html` §3 row A, and `clean-arch/step1-unfiled-2026-11-08/LOG.md` §20 (arm c1).
A separate blind audit of the wording runs beside this round; do not repeat it line by line.

Challenge the design, not the decision to test:
1. Is c20 one lever, and does it carry the standard's row A rather than a rule of Claude's? Is dropping capital expenditure (D490's scope)
   handled honestly?
2. The cases: do they test what Alex asked ("能否开出这 3 个问题，同时不乱开、不重复")? Which class the change can move is left unguarded (AGENTS
   §7.3: a small sample guards every class the change can move)? "不重复" across articles is left to a second step because the stored states
   hold no revenue question: is that acceptable, and what must that second step be?
3. The counting: is any line too loose to fail or too strict to pass against c8's own spread (three sends a case)? Is "a growth rate counts
   as that year's revenue" right? Is g1 (a question opened from a bare reported figure) rightly reported and not a line?
4. What must be written before the send that is not: a no-room outcome, a line for the links of the figure statements, anything else?

Name only what would make the probe's result unreadable or wrong. End with: "Council position: <...>".

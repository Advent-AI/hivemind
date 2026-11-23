# Council mx, round 18: Alex chose "the kept figures should reach the judgements of related questions" (D505); the $0 check's design before any reader

Alex answered D504's question with one option only: "进入相关问题的判断" (D505 in `docs/DECISIONS-log.md`); he did not choose the table or
tracked financial questions. The first step he approved is the $0 check you proposed in round 17.

Read `docs/research/2026-11-14-use-acceptance/delivery/DELIVERY-CHECK-DESIGN.md`, `census_delivery.py` with its output
`delivery-census.json` (step 1, done: in this run a judgement request shows exactly the statements the reading step linked to its
question, so a figure reaches a judgement only through a link), `questions.json` (the seven questions with their possible answers),
`brief-needed.md` (the blind readers' brief) and the table `../record-3/financial-table-week.md`. The standard for "should have
received" is quoted from the current phase's PRD (`docs/prd/10-filing-phase.md` §1 and §2), not written anew.

Name only what would make the result wrong or unreadable:
1. **The standard:** is PRD 10's "facts that can change its answer", with onward reasoning, the right test here, and does the brief
   state it without widening or narrowing it? (PRD 10 was written for production's filing; the new system's reading request has its
   own linking rules. Is using PRD 10 here a second ruler in disguise?)
2. **The readers' task:** seven questions against 146 lines in one session, blind to deliveries; "which way it moves the answer" as
   the admission test. Too loose (model readers over-flag), too strict, or unreadable at this size?
3. **Delivered or absent:** by link, else by the same figure in a shown statement, then read by hand. The census found that same-claim
   joins are large (groups of up to 21 statements) and a statement can carry several figures: is "the same figure in a shown
   statement" the right unit, or does it hide a figure that was shown inside a different claim?
4. **The rule:** a finding needs both families and a hand read; none stops the line. Does that let a real gap pass, or manufacture one?
5. What the report must not say.

Then say whether the readers may run. End with: "Council position: <...>".

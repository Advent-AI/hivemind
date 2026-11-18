# Round 10: reading A is done (Alex's six lines on the fortnight's answer choices) and C is built and proved. Verify; then the next iteration.

**A, gate 1 in the product condition** (`poc/data/clean-carried-run-2026-11-16/stage-a/report.txt`; the October tooling unchanged:
two families apart, 39 valid rows each, 24 sends disputed, a third reader of each family on 34 points). Under both countings:
line 1 missed (3 or 5 sends), line 2 missed (7 sends), line 3 missed (4 or 7 sends), line 4 **met** (the only refusals, clean-8
×3, justified), line 5 **missed: right 7 or 5 of 13, by written choices 6 or 4** (scaled lines 11 and 9), line 6 not measured.
Faults by kind: a stated plan left out of the reference (XR fails on 4 topics: the $125bn residual-value proposal, the Hugging Face
agreement ×2 attempts, Huang's 10-20 GW pace); a due day before the material that settles it (W upheld: Rubin revenue "as the
FY2027 10-K shows" due 2027-01-31; CPO volumes for calendar 2027 due 2027-12-31); "and" in the question against "or" in the Yes
rung (MIIT, three attempts); parts left unlisted (L, several); a question leaning on an unnamed lab (Q, credit support).
So "written for 12 of 13" did not mean right: your round-9 caution held. Compare: October from empty, wider count 9 of 12 right,
6 by written choices; July 32 of 40 and 22. Gate 1 is unmet in every one of eight readings, now in the product condition too.

**C, the page** (`carried-run/INTEGRATION-CHECK.md`): the first diagnosis (completed days only) was incomplete; the page also needs
the processing record (`service.seq_day_map`). Fixed at the writer in `ladder_adapter.py` (`record_article`, `complete_day`; the
base adapter is frozen with the unseeded measurement and stays unchanged: my first attempt there was refused by the runner's
freeze check and reverted to its frozen bytes); a test, two mutants on a scratch mirror; the extension proof re-run 19 of 19
(every judge request and judgement unchanged); the page lists every judged question; full suite 287 passed.

**What I take from it** (attack): in the product condition, the step that writes answer choices stops refusing but still writes
choices with faults of the same kinds as from an empty start; the condition was not the reason gate 1 fails. Two of the fault
kinds look general and product-relevant: (a) a due day before the report that settles the event (the judge would close "still
open" where the event happened), and (b) a stated plan or expectation left out of the reference. Both live in the frozen
answer-choice step (D426) and in rules Alex set (D403: an event's due day is a date given or the period's last day; D411).

**Candidate next steps:**
1. Record C as a decision (a writer fix, proved; it changes no judgement) and keep it.
2. Put to Alex, as one page, the decisions only he can take, with this run as evidence: whether the six lines stay the gate (D560
   asked after the deck); and, if they stay, whether the answer-choice step may be opened as a new version for the two general
   faults (a), (b), each against its rule (D403, D411), with Alex's D426 stop in view.
3. Meanwhile at $0: size (a) on every stored reading (how many event questions name a settling report published after their due
   day; how many would close wrongly), since it touches the final answer directly.
Name a better course with its reason. End with `CONSENSUS: yes` or `CONSENSUS: no, because …`.

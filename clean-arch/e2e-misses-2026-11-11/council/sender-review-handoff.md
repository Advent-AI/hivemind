You are an independent, read-only reviewer, new to this work. Do not edit any file and do not send any network request.

Scope: a small paid probe about to be sent in /Users/lchingen/hivemind (branch clean-arch): 18 requests to the frozen production
judge, about 4 cents, re-sending saved requests of three saved runs.
- Protocol: clean-arch/e2e-misses-2026-11-11/PROBE.md
- Sender and reader: clean-arch/e2e-misses-2026-11-11/resend.py (new; it imports clean-arch/step2-edge-effect-2026-11-10/edge_replay.py,
  which rebuilds a saved run offline and was reviewed and used yesterday, and clean-arch/e2e-2026-11-09/budget.py, the shared
  spending limit). A sender of the same shape, clean-arch/step2-edge-effect-2026-11-10/judge_probe.py, went through four review
  rounds yesterday; its findings (answers lost when the accounting fails, an unreadable outcome crashing the reader, a reader not bound
  to its case, cost without retries) are the ones to look for here.
- Inputs: poc/data/clean-e2e-misses-2026-11-11/control-d{1,2,3}/ (the offline replays) and the ledgers it rebuilds there.
- Code it calls: src/hivemind/model.py (build_request, openai_transport, check_schema), src/hivemind/views/judging.py (check_answer,
  round_of_judgements for how a refused answer is re-asked).
- Rules: AGENTS.md sections 5 ("a re-sent request is the bytes production sends"), 7.3 and 9.

You may run, it sends nothing:
  python3 clean-arch/e2e-misses-2026-11-11/resend.py check --case 3 v17 2026-07-08 first --case 3 v17 2026-07-08 accepted --case 1 v17 2026-07-08 accepted --case 3 v17 2026-07-14 accepted --case 2 v22 2026-07-14 accepted --case 3 v22 2026-07-14 accepted

Out of scope: the judge's quality, any redesign, wording preferences.

Mark every finding "serious" (it could make a send differ from what production sent, send the wrong request, lose an answer, spend
past the cap, damage saved data, or let the reading rule be applied to the wrong answers) or "not serious", with file and line:
A. Is each case's request exactly the saved one (the `first` case in particular: is it the request whose answer was refused, and is
   the rebuilt ledger the one production checked it against)?
B. Can `send` lose a returned answer, re-send beyond the spending limit's own retries, write outside the data folder, or pass the cap?
C. Can `read` crash on an outcome, read another folder's answers, or count an answer under the wrong case?
D. Any sentence of PROBE.md that claims more than the files show (the numbers in "Found at no cost" are in
   poc/data/clean-e2e-misses-2026-11-11/refusal-census.json, built by clean-arch/e2e-misses-2026-11-11/refusal_census.py)?
End with one line: READY TO SEND, or NOT READY with the serious findings numbered.

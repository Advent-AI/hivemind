# Round 8: the proofs and the slice. Proceed to the rest of week 2?

Alex has since set a standing goal (2026-11-16): "go in the council loop everytime you get result, and need to proceed, review
deeply and progress towards the production goal, don't scope drift … don't stop until you do, but with each iteration you
should learn from previous runs and improve your approach".

Done, all in `docs/research/2026-11-14-use-acceptance/carried-run/` (read-only check, please):
- `extension.py`; `proof-output.txt` 19 of 19 (the real launcher re-reading a stored week's second half from its first half's
  library sends the stored requests byte for byte; the join equals the stored trace in every column; five mutants refused; the
  later steps on the joined trace equal the stored draw's; no judge request holds material first read after its day);
  `inputs-proof-output.txt` 11 of 11 (order, text identities, starting library, first request, the date check's control).
- `PLAN.md` frozen before any send (sha256 in `PLAN.sha256`), with the ledger fixed at $6 and the slice's four conditions.
- **The slice** (2026-09-29, 33 articles, from week 1's 7 topics): `check_slice.py` 4 of 4 (33 of 33 complete; no refusal;
  $0.0098 an article against a limit of $0.0134; the first request holds week 1's library). Ledger: about $0.32 of $6. What it
  did (my read of the trace, `poc/data/clean-carried-run-2026-11-16/slice/trace.sqlite`): one topic opened in 33 articles ("How
  much venture funding will physical AI (robotics) companies raise globally in calendar 2026?", from "Nvidia Alumni Are
  Fueling a New Wave of Robotics and AI Startups"; I doubt it is worth holding: a lead for the reading, not a stop); no held
  matter re-opened; 91 statements kept, 71 with no link; links: Rubin 11, credit support 4, Hugging Face 2, supply 2.

Proposal: by the plan as frozen, launch the rest (2026-09-30..10-05, 208 articles) from the slice's last library, join the
three parts, and run the later steps over the fortnight, all on the same ledger; read as frozen. Anything that should stop
or change this? End with `CONSENSUS: yes` or `CONSENSUS: no, because …`.

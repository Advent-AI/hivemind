# Council mr: c2's Step 1 stopped; a redo under D449?

**What the output shows** (read by me): `poc/data/clean-e2e-full-2026-11-13/c2/step1/step1.log` ends with
`{"status": "failed", "input_id": "gnews:f66e1689ec2e27e7eab2a2dd", "error": "TransportError: IncompleteRead(32718 bytes read)", "calls": 57}`;
the trace holds 55 complete rows and one failed row (sequence 56, no response stored). The same article completed in c1 (response 102,717
bytes) and in c3 (106,331 bytes). Step 1 sends each call once (`max_attempts=1`), so a dropped response ends the draw. This is a transport
failure, the class D449 names as eligible (a stop a second send can change); not a check's refusal, not a crash, not the ledger
(spent $3.64, nothing stopped). c1 and c3 continue (63 and 60 of 243).

**Proposal:** `run_fresh.py clean --root poc/data/clean-e2e-full-2026-11-13 --label c2 --ledger <ledger> --until-day 2026-07-14
--passes 3 --redo step1 --redo-reason "TransportError IncompleteRead(32718 bytes read) at item 56 (gnews:f66e1689ec2e27e7eab2a2dd);
55 items complete; the same item completed in c1 and c3"`: Step 1 from empty in `step1-redo` (D449: a new folder; one redo; its stop
stops the run), then the rest of the draw as usual. Cost about $2.5 more and about 2 h 20 min (estimate); the run's projected ledger total
becomes about $11.5 of $14.84. The alternative, continuing c2 from item 56 as a segment, would save about $0.6 but is not the agreed rule
(D449 redoes in a new folder) and `run_fresh.py` has no such path; I do not propose it.

Same-day: the redo's sends fall on 2026-11-13 like the others'.

End with: "Council position: <redo c2's Step 1 as proposed | change ... first>".

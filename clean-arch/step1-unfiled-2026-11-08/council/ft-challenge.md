Your blocker was answered. Re-read `clean-arch/q12-capex-2026-11-09/DESIGN.md` (§5 rewritten, with the blind audit),
`probe-frozen.md`, `q12_probe.py` and the c8→c12 diff. Read-only, under 250 words.

1. **Case B** now requires that c12 links neither the cash-flow nor the cash-balance sentence to any thesis, 3 of 3, and keeps either
   one unlinked in no more draws than c8. c8's stored dev answer already kept the cash flow unlinked, which is reported as c8's own
   defect.
2. **Added links are a line.** Every c12-only link goes, as a (statement, thesis) pair, before a blind reader, mixed with c8's links on
   the same cases as controls. c12's "does not inform" share must not exceed c8's.
3. **The transport check** now compares `json.dumps` bytes, key order included. The dry run passes on all 14 cases.
4. **The synthetic answer:** the cash-flow sentence kept and linked to v12, run through `runner.validate` on case A's c12 request.
   It passes.
5. **The whole-request audit** used a blind second reader on c12's system text, closing check and schema. Its main finding: the first
   draft's "its revenue or earnings path included" could invite linking cash figures to a revenue thesis. c12 now keeps c8's revenue
   clause word for word and adds only ", and any other open thesis whose figure follows from them by a standard definition (two
   reported balances give the change between them; a reported total less one of its parts gives the other part)". Pre-existing c8
   tensions are recorded, not changed.
6. **Prompt tokens** are reported from usage per arm. The size is +197 characters, with the reason written.
7. **The numbers are fixed:** 84 calls, $0.88 estimated.

SEND or BLOCKER?

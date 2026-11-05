# The one test: predictions written and frozen before the send (2026-11-04)

Conclusion under test (core-conclusion in log.md row 8): the system uses a fact for a question only when the fact states that question's own
figure; an analyst also uses it by inference (the other side of the same sale, a price for a product's revenue, a variant for its launch).
The filing step's literal linking is established by the traces (Broadcom's figures never reached the custom-silicon question in any draw;
the model's own words "not a figure for cloud-provider spending"). What is not yet established: whether the judging step uses such facts once
they reach the question, or reads them literally too (it set custom silicon to "below $40bn" because "no aggregate figure can be derived").

The test: in each frozen v108 draw (d1, d2, d3), the custom-silicon question's (v16) last stored judging request (2026-07-14), sent as stored
three times (control) and three times with the evidence lines of that draw's own ledger statements that state the facts the frozen gold rests
q16 on (Broadcom's Q2 AI semiconductor revenue and Q3 guide, its custom-chip ramp for named AI customers, Amazon's Trainium scale, the custom
ASIC growth forecast) inserted in the evidence block, as the request would show them had filing placed them there; the block's count updated;
nothing else changed. 18 sends, the production judging prompt (judging-v7), about $0.06.

Prediction if the conclusion holds: the control stays at rung 1 ("less than $40 billion") in most sends; with the facts, the judge derives a
figure from Broadcom's revenue and leaves rung 1 (rung 2, $40–60bn, or rung 3, $60–80bn) in at least 2 of 3 sends in every draw.
Refuted (the judging step reads literally too, and the fix must cover judging as well as filing): with the facts, rung 1 in at least 2 of 3
sends in any draw. Reported beside it: agreement with reader B ($60–85bn: rung 3 or 4) and reader A ($35–65bn: rungs 1–3), the two readers
of the frozen ruler, since rung 2 sits between them.

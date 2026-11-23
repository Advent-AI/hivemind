# The July test: reading rule, frozen 2026-11-21 before any send (D694 (c))

Copied from `TEST-PLAN.md` without change; scored line by line as written.

## Reading rule (frozen before the send; council R round 2, `codex-r2.md` §7(b), with round 3)
- **A. Comparable answers:** both 07-12 answers give a FY2027 forecast in USD for their own quantity (a range by its stated ends);
  quarters recorded where both give comparable figures; a missing annual figure leaves reconciliation untested.
- **B. Arithmetic and sources:** reported figures keep their amount and scope; the arithmetic follows from the stated inputs within
  rounding; each assumption that materially sizes the result is disclosed and supported by the material available that day; a linked
  forecast is treated as a forecast with assumptions.
- **C. Room for the rest:** the high end of the Data Center forecast is at least $6B below the low end of the company forecast (the Q1
  floor: $81.6B total minus $75.25B Data Center); each comparable quarter keeps the segment within the total.
- **D. The link did the work (linked arm):** matching chose "v9 reads v14", the writer committed it at seq 148, and v9 used v14's
  forecast in its calculation or as a stated bound; delivery and use of the Bloomberg-compiled $393B (e195) recorded separately; a
  mention or citation alone earns no credit.
- **Pass:** at least two of three linked sequences meet A–D; at most one control meets A–C; no first-attempt refusal added and no new
  material grounding error on either question across 07-10..07-12 (relabelling a system forecast as a market estimate, or treating
  $393B as a Data Center consensus, is one). **Inconclusive:** two or more controls reconcile, fewer than two comparable sequences in
  either arm, or a ceiling stop. **Fail:** a new material error, an added refusal, fewer than two correct link selections, or any other
  miss. Failures take precedence.
- **Readers:** Claude's marks written first, then a fresh blind Codex reader on the six sequences under shuffled labels, the key outside
  the repository; every sequence reported.

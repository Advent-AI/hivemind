# c13 probe: frozen before any send (2026-11-09; D393; Alex chose "加在最后复查里再试一次")

**Arm c13** (`arms/c13-*`, schema unchanged):
- c8 plus the scope fix in both places ("when it informs no open thesis" / "that informs no open thesis usually cannot"), which passed
  line 2 in the c12 probe.
- One closing-check step after the read-back: "Then go back over the item for statements of the company's own figures that you have
  not returned, or returned without links: for each, check whether an open thesis asks about a figure that follows from it, alone or
  with another figure the item states, by a standard definition (a reported total less one of its parts gives the other part), and
  whether that figure makes the thesis's answer more or less likely; when both hold and no row above rejects the statement, return it
  linked to that thesis, with the passages both figures come from, and say in the link that the figure is derived."
  - It was revised after a blind audit (`council/fw-audit-c13.md`) to:
    - keep the reject rows;
    - use the standard's test words;
    - cover unlinked kept statements;
    - make the derived record stand alone.
- c12's CONDITION derivation clause is not carried.
- Size: system 15,828 to 15,826 characters; closing check 8,638 to 9,226 (+588). Why: the one-pass pattern (AGENTS §6). The model
  derives capex from operating less free cash flow when asked afterwards (3 of 3, `capability-c12.json`), and the existing read-back
  never sees a statement that was not returned.

**Cases and control:**
- `cases-probe.json`, the same 14 cases. Three c13 draws each, 42 calls, about $0.44–0.45 estimated (input tokens estimated; transport
  retries possible).
- The control is the c8 arm of the c12 probe (`poc/data/clean-q12-2026-11-09/probe-c12/records.json`). It was sent today, with the same
  byte-checked stored requests.

**Lines** (as in `probe-frozen.md`, with c13 in place of c12; any failing one stops the line and goes to Alex):
1. **A:** c13 writes i131 and links it to v12 in at least 2 of 3.
2. **B:** c13 links neither the cash-flow nor the cash-balance sentence to any thesis, 3 of 3, and keeps either one unlinked in no more
   draws than c8.
3. **C:** no gold item c8 writes in at least 2 of 3 is written by c13 in at most 1 of 3.
   - Whether a kept item states the gold sentence's fact is judged by a reader who wrote neither c13 nor this probe, blind to the arm,
     on every C case's kept items against its gold sentences.
   - The matcher's count is printed beside it. The c12 probe showed that the matcher misses rewordings of i304.
4. **Added links:** every c13-only link is blind-read beside c8's links on the same cases. c13's "does not inform" share must not
   exceed c8's.

**Before the send:**
- A synthetic answer that follows c13 (the cash-flow sentence kept and linked to v12) passes `runner.validate` on case A's c13 request.
- A blind whole-request audit of c13 is in the council folder.

**Labels:** the motivating article and the Stage 1 articles, on which c8 was tuned. A probe locates; it does not accept.

# Council A, one probe arm (read-only, $0). Reply in under 250 words, ending `SEND`, or `DO NOT SEND: <smallest change>`.

**The finding.** On the release comparison (D665; diagnostic of 5 draws), the new clean system loses.
- Of the 32 frozen key matters, it serves 2–3; the old system serves 10.
- The old system serves 7–8 that the new one does not. 5 of those are the company's own figures: FY27 data-center revenue, FY28 total
  revenue, and FY27 and FY28 gross margin. The new libraries hold no such question.
- The cause is the Step 1 prompt's do-not-open item, "a financial measure's level, growth, margin or guidance for any period, on its
  own" (D382, D384: "Class A, the main-driver quantity, stays out under D382").
- See `docs/research/2026-11-17-product-comparison/RUN-LOG.md`, the last entries.

**The arm.** `arm-system.txt`, `arm-closing.txt` and `arm-schema.json` are in this folder; the base is `clean-arch/PRD.md`'s c8 prompt. It
makes one change:
- a fifth opening reason, `main_driver`: the company's total revenue, the revenue of its value-carrying segment, or its gross margin, for
  the current or next fiscal year;
- the do-not-open item narrowed to match;
- the enum extended.
It grows by 473 characters.

**The probe.**
- Twelve July items, each re-sent twice with new-2's stored open theses at that point.
- Six are motivating items: those on which the old draws opened FY27 and FY28 revenue, data-center revenue, gross margin and
  hyperscaler capex.
- Six are random July guard items on which new-2 opened nothing.
- The cost is about $0.30. Nothing in production changes.

**Check:**
1. Does every sentence of the arm trace to the signed extraction standard (`docs/prd/05-extraction-standard.html`, class A) and read as a
   general analyst rule, not fitted to NVIDIA?
2. Is it a closed set with examples?
3. Does it contradict another sentence of the request?
4. Is the probe enough to show opening on the motivating items without new noise on the guards?

Out of scope: the frozen ruler, Step 2, the ladder and the judge.

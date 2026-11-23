# Decision council: Alex has delegated the threshold, so the council decides the next modification (read-only)

**Alex, 2026-11-08,** after I offered him about 10 more boundary cases to rule on: **"你需要我裁定什么？你不能跑council决策吗"**. The
threshold is delegated to the council, as in D260 (`docs/DECISIONS-log.md` D260: "门槛没有标准，按照你作为 hedge fund analyst 的认识来定";
there the decision was recorded as Claude's analyst judgement, not Alex's words). We may not hand it back to him. We decide, record
the decision as council-defined and not confirmed by Alex, and test it.

**The anchors:** Alex's four rulings (`LOG.md` §11):
- cash-flow and cash figures: dropped;
- gross margin: kept under the existing revenue thesis;
- an analyst EPS forecast in a valuation piece: kept, with the target price dropped;
- a small supplier's expansion: dropped.

**The analyst threshold proposed for the council.** The company's own results, estimates and guidance belong to one card: the path
of its revenue and earnings.
- A measure (margin, EPS, a segment's growth) is evidence on that card, not a card of its own, unless an open thesis already tracks
  that measure separately.
- A backward balance or cash figure that does not move the card's answer is dropped.
- When no revenue or results card is open, the item's results are what opens that one card, by section 3's test (the segment that
  carries the business is a big matter).
- This reads the same for a bank (net interest income and earnings), a drug maker (product revenue and earnings) or a retailer (sales
  and margin).

**Modification u1r', replacing the one-quarter item; nothing else changed.**
"- One quarter's figures or guidance are not a thesis. The company's reported results, estimates and guidance (its revenue, the
segment that carries the business, margins, earnings) are evidence for the open thesis on its revenue or results: link them there
rather than opening a thesis for one of those measures, unless an open thesis already tracks that measure. When none is open, judge
by the test above whether the path of its revenue and earnings merits a thesis, and open that one question with them when it does;
never one thesis per quarter, line or estimate."
- Sources: D371, §3's value quantities, the four rulings.
- The model keeps the relevance and opening judgement.

**Probe 3:**
- A fresh same-day k6b control and u1r', 16 cases × 3 draws = 96 sends, about $1.25.
- **Decisive checks, anchored to the rulings and checked by code plus my reading, not by model-reader thresholds:**
  - margin (d1-40, d1-57) and the EPS forecast (d1-66, d2-66) linked to the open revenue thesis;
  - cash and cash-flow figures not kept (d1-57, d1-62);
  - no supplier thesis (d2-8);
  - at the empty states 40, 57 and 62, exactly one revenue or results thesis and no separate margin or FCF thesis;
  - guards: no new theses on d1-22, 29, 113 and empty-108;
  - ruler noise at most the control's;
  - all answers pass the format check.
- **Pass:** u1r' beats the control on the ruling-anchored checks in at least 2 more answers, and breaks none of the rest.
- Then the dev forward run (115 articles, Alex's Step 1 line), then the test set once.
- **Overfitting guard:** the probe cases include the rulings' own articles, so the probe locates; only the forward run and the
  untouched test set accept.

Decide with me: send, amend (give the exact amendment), or stop.

Under 250 words.

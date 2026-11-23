I ran your read-only audit: `clean-arch/e2e-2026-11-09/stage2-delivery-audit.txt`.

**q10 (the "66% operating margin" fact):**
- Clean: stored, linked to v10 and shown in 9 of 9 judge requests, in every clean draw.
- Control: never stored in any draw.

**q16 (Broadcom's $10.8bn and $16bn):**
- Clean: linked to v16 in every draw and shown in the last request.
- Control d1 and d3: stored but linked to v16 zero times, and they disagreed.
- Control d4: linked once and shown, and it agreed. So delivery and outcome match one for one.

**q12:**
- Neither arm links the cash-flow facts.
- Operating cash flow is never stored. Clean stores free cash flow once, unlinked. v12 is never judged in either arm, so the gap is at
  Step 1.

**The parking lot (PRD 10 §2):**
- Links to v1: clean 13–15% of seed links; control 21–26%.
- v1's last judgement cites non-NVIDIA speakers 2–6 of 10–11 times in clean, and 7–16 of 11–21 times in control. This is a lead: the
  speaker field is a coarse label.

**My draft for Alex (one conclusion, one recommendation, one test):**
- **Conclusion.** With the questions supplied, the clean system feeds the judge the facts that change answers better than production:
  +5 over three draws, traced to delivery. It solves two of the PRD's three starving questions (custom chips, operating margin) and piles
  less into total revenue. It is inconclusive under the frozen rule because capital spending (q12) is still starved at Step 1.
- **Recommendation.** The largest unknown before the clean path can replace production is whether it opens these questions itself.
  The product starts empty (D370), and this diagnostic was seeded.
- **Test.** An unseeded clean run on the same 243 items, three draws, about $7. An independent reader maps each opened question to the
  23 ruler questions with the same identity check used for q23. Mapped questions are judged by the frozen judge and scored; unmapped
  ruler questions count as not in run.

**Challenge it.** Is this the right next step versus fixing q12 or anything else? Does it need a decision or a ruler addition first?
(The scorer refuses a run whose v1–v22 are not the seed texts, and a matter-to-question mapping is "D2, not yet built".) Is anything in
the audit overstated? Under 300 words.

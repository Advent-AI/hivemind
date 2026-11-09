# Stage 1 of D392: predictions and stop condition, frozen before any send (2026-11-09)

**The probe.** `stage1_probe.py` with `stage1_cases.json`: 13 dev articles carrying gold-cited facts for q10, q12, q16, q17 and q23, and
for the production-agreed figure questions v1, v3, v11 and v22.
- **Control:** the stored dev-d1 sent request, re-sent once the same day.
- **Seeded arm:** that sent request with only the open-theses list replaced by the 22 seeds, three draws.
- **Seed rule:** description = question, outcome = looks_at, period = "<year>, due <due_day>".
- **About $0.54** at published rates (estimate, 6k output tokens each). About $4.16 if every answer used the 64k cap, and up to about three times that if every request were billed on each of the transport's
  three attempts. These are estimates, since input tokens are estimated. Draws are capped at 3.
- **$0 checks passed:** each sent request equals the live transport's form of the stored request (`deepseek_json_mode`); the payload re-serialises byte for byte; open_theses equals the
  stored before-state; every gold item's article is its case's article. On the stored unseeded answers, the matcher finds every gold
  fact written (13 of 13 articles); most are unlinked or linked to clean theses.

**Definition.** D(q, case) is the number of seeded draws in which a gold item that the frozen gold cites for q (`gold_questions()`) is
quoted by a kept evidence item linked to existing thesis q.
- **Quoted** means that, after normalising, a kept passage contains the whole gold passage, or lies inside it and covers at least 60% of
  its length.
- A draw with a transport error or a contract refusal counts as a draw that delivered nothing and wrote nothing.
- **Matches are adjudicated before the conditions are applied.** Every matched (gold item, passage) pair goes to a blind reader with
  the gold item's `meaning`. Only pairs the reader confirms as stating that fact count; for i163, that means Nvidia's roughly 66%
  operating margin. Unconfirmed matches count as not quoted.

**Stage 1 holds only if all four hold:**
1. **q10:** for some q10 case (q10-margin, q10-guidance), D(v10) is at least 2.
2. **q12:** for some q12 case (q12-cashflow, q12-capex), D(v12) is at least 2.
3. **Production's figure questions are not lost:** for each of v1, v3, v11 and v22, some case targeting it has D at least 2.
4. **Nothing written is lost:** every gold item is written in at least 2 of the 3 seeded draws. The stored dev-d1 answers wrote every
   gold item (13 of 13 articles), so the stored answer is the reference, and the same-day control send is recorded beside it. A failed
   control send cannot make this condition pass.

**Recorded, not gating:**
- delivery to v16, v17 and the Ohio statement (to v12 or a new signing thesis);
- new theses a reader judges to duplicate a seed;
- links per item against the control;
- contract refusals.

**On the result (D392):**
- If it holds, Stage 2 proceeds.
- If it fails, the line stops and goes to Alex with every answer read.

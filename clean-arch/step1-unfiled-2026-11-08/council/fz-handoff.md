Council before a recommendation to Alex. Read-only, fresh reader, under 400 words. Repository /Users/lchingen/hivemind.

**Context:** Alex chose (D394) to start the unseeded measurement with a $0 question-matching stage. Done so far
(`clean-arch/unseeded-2026-11-10/`): two blind readers (Codex `reader-codex.jsonl`, Claude `reader-claude.jsonl`) mapped the 28
questions three stored unseeded c8 dev runs opened by themselves to the 23 judgement-ruler questions (`ruler-questions.json`) under the
D248 identity rule.
- They agree on 24 of 28. The 4 disagreements are same-versus-broader or narrower on q09, q08 and q18.
- Each run opens a SAME match for only 4–6 of the 23: q07, q08, q13 and q18 always; q05 and q09 sometimes. q23 was opened in one
  Stage 2 draw.

**What I then found** (verify each):
- **The frozen question gold** (`docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json`, each article's
  `questions.must_open`) asks for credit support and backstops, the Ohio guarantee, the hyperscalers' 2026 and 2027 capex, Kyber NVL144,
  DRAM prices and China H200 permission. It does not ask for NVIDIA revenue, margin or EPS questions; class A appears as may_open.
- **Alex, 2026-11-08** (round log §16): "我觉得财务类型不应该是thesis，而更多的是条件。观点应该是独特的view，而不是喊出来的数字，除非有理由".
  Round log §§38 and 44 treat class A as excluded by this decision, a by-design miss.
- **The existing question measure** (round log §44, c8 dev ×3) covers must_open 25, 24 and 27 of 28.
- **The judgement ruler** (D3, frozen 2026-11-02) seeds 22 questions. About 9 are company-figure questions (revenue FY2027 and FY2028,
  data-center revenue, margins, EPS, capex, and so on) that the product, by the 11-08 decision, will not open.

**My reading:**
- An unseeded judgement run would mostly measure the absence of figure questions that Alex's later decision rules out. That is a
  mismatch between the frozen judgement ruler and a later decision; D373 says to record the concern separately and not edit the ruler.
- Opening is already measured on the frozen question gold, at 24–27 of 28.
- A paid unseeded run would add judgement only on the 5–7 overlapping questions, which all agreed in the seeded Stage 2, apart from q23
  at 1 of 3.

**My draft recommendation:**
- Do not spend on the unseeded paid run now.
- Record the ruler-versus-decision concern for Alex.
- Close the filing phase's measurement with the clean system's Stage 2 result (two of the three starving questions delivered, q12 a known
  gap), and move to the next product step.

**Check:**
1. Is the reading right? Search the decisions for anything that makes company-figure questions openable (for example a single
   "revenue and earnings path" question per company, from the 11-08 rulings in round log §11). If one exists, the unseeded run is not
   moot for v1, v11 and v22.
2. What is the next product step, per `docs/prd/10-filing-phase.md` and the decisions? Is "close the phase" justified?
3. Give the one recommendation you would put to Alex.

**Out of scope:** editing any frozen ruler.

# Diagnosis: the Ohio-guarantee question is never opened (Claude, before the council; 2026-11-09)

Alex chose: "先查俄亥俄担保为什么没开出来" (investigate first). Nothing has been sent except the account ($0.011).

1. **Class.**
   - In the dev gold, 1 of 28 must_open entries is an unsigned specific obligation (type C, yes/no): "Will NVIDIA sign a guarantee of
     OpenAI's Ohio data center lease by 2027-06-30?" (article 4, `gnews:4d1677af37befd53ca3e7b45`).
   - It is missed in 3 of 3 c8 dev draws. The test gold has 0 such entries. It is q23 of the frozen judgement gold, so Step 4 will be
     judged on it.
   - The other dev misses are a different mechanism: calendar-2026 big-four capex opened as 2027 in two draws, and DRAM 2027 in one
     draw.
2. **Mechanism** (traced in all 3 draws). Article 1 opens clean-1, "how much credit support will NVIDIA have extended to AI cloud
   partners…". On article 4, all three draws extract the Ohio negotiation item and link it to clean-1, proposing no thesis.
   - The model's own account (`poc/data/clean-step1-c8-dev-d1-2026-11-09/ohio-account.json`) quotes:
     - §2 "if an open thesis covers the statement, link it";
     - §3 "Do not open a thesis about … another estimate, source or wording of what an open thesis tracks";
     - "If the two cannot move apart, link the evidence…".
   - It judges the two "the same quantity" that "cannot move apart", and it treats "a reported negotiation, not a signed obligation"
     and "amount undisclosed" as reasons against a separate thesis.
3. **Step back.** The request already carries the standard's rule (c8-system line 98: "one not yet signed by whether it is signed by
   a check date within 18 months", with the retailer-guarantee example). The standard §3 C row lists a guarantee of another party's
   lease, and the gold's rule reads "还没签 → 是非两档; §4.2 test 1: huge credit risk". D384 says theses open as the gold applies the
   standard, so the gold governs. The model misapplies D248's "answers can move apart": whether one named unsigned obligation is
   signed can move apart from the total of a kind of obligation. The total can grow without it, and it can be signed while the total
   shrinks. This is a misread of an abstract clause, not a missing rule.
4. **Proposed fix (not built; a new version only Alex opens).** Teach the "move apart" test with one closed-set example in §3,
   cross-industry, beside the existing separate-bet text. For example:

   > An open thesis on the total of a kind of obligation does not cover whether one named obligation not yet signed will be signed:
   > their answers move apart. A bank's question on its total guarantees does not cover whether it will sign a guarantee for one
   > developer's large lease; that is its own yes/no question when its scale alone could change credit risk.

   Remove as much elsewhere (AGENTS §6). Sources: the standard §3 C, D248, D384.
5. **The test I would recommend** (cents, on Alex's word):
   - re-send article 4's stored request with the change, 3 draws: the Ohio question opens;
   - re-send the controls where folding is right: article 1 and the other credit-support articles in dev (the gold lists the
     aggregate as one must_open across several articles), plus fresh-set articles with an open thesis of the same family: no new
     fragment theses;
   - falsifier: fewer than 2 of 3 open Ohio, or any control fragments.

   Only then a dev ×3 and a fresh-set comparison with c8.
6. **Share.** The fix targets the whole counted class (1 case in dev). The risk is fragments, the line c6 missed.

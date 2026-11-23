# Council round 56c (choose how the S4 refusal is resolved): independent read, read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite what you read.

**Read first:**
- `docs/research/2026-11-22-number-answers/codex-r56.md`: the blanket % / x stop is rejected.
- `docs/research/2026-11-22-number-answers/codex-r56b.md`: the narrowed `apply_growth` exemption is rejected.
- D741 in `docs/DECISIONS-log.md` (Alex's exact question and ruling 1).
- D738.
- The refused reply: `poc/data/judging-v13s-blind2-2026-11-22/P-v4/answers/claude.json`.

**What two rounds showed.** Whether a guidance rate on an outcome's path supplies a second dollar value of the quarter is not decided by the
calculation's structure. Arithmetic can cancel (56b), and equivalent forms land on opposite sides of any structural line.

**What I now see.** Alex's ruling 1 reads "a growth rate computed from guidance and used only as a stated benchmark **for an estimate**,
when one figure supplies the quarter in the revenue calculation". The refused reply did not use an estimate: it computed the guidance
rate straight into Q4 with `apply_growth`. The current S4 is consistent with the ruling's text. What misled the writer is the request,
which pulls three ways:
- the system text, `judging-v13s.txt` line 4: "reported figures and guidance give a run-rate that carries the guided growth forward";
- the schema, `render_v13.py`, `v13s_schema`, figures description: "may serve as a stated benchmark for an estimate";
- the header, `render_v13.py`, `v13s_header`: "Shared quantities … through which every figure an outcome uses for that quantity goes".

**The two candidates.**
- **A' (my recommendation): no code change.** Make the request state the ruling's closed set in all three places. Proposed wording:
  - system text: "… reported figures and guidance give a run-rate that your own estimate carries forward at the guided pace, never the
    last quarter annualised flat; …"
  - schema: "A growth rate computed from guidance for a shared quantity may serve as a stated benchmark for an estimate (named in
    rests_on), never as an input of a computed figure; wherever the calculation uses that quantity, it uses your one forecast figure."
  - header: unchanged.
  - reader brief and adjudication header: keep Alex's ruling sentence as written; add "Look through any rate or multiple for a second
    dollar value of the quarter."
  - Tests: keep your 56/56b counterexamples as A2 regression cases (all refused by the current code), and add:
    - an A2 case: the refused reply's form, a guidance rate computed straight into Q4, refused by S4 with the rule stated;
    - an A1 case: the same rate as the stated benchmark of a Q4 estimate passes.
  - Consequence: the refused reply's form stays refused. In a fresh run, a writer who still computes the rate directly is refused under a
    stated rule. The reviewers may still call its amount "right", so the registered stop line could fire again. That would be an honest
    result: the request failed to get the form followed.
- **B: the blanket % / x stop (rejected in 56), defended under D738.** A guidance figure reached only through a rate or multiple is an
  indirect form. It is recorded for readers, not refused. Such a reply already gets the existing record "one quantity, several figures"
  (`calc_small.py` `_recorded`), and readers are told to look through rates. Consequence: no right answer of this kind is refused, but a
  reset through a ratio (your 56 counterexample) publishes, and only the readers and the card's record stand between it and an analyst.

## Questions
1. Which candidate, A' or B, is right under D737, D738 and D741 ruling 1? Or is there a third? Weigh the product risk (Alex: "don't
   hallucinate with the numbers") against refusing right answers.
2. For A': does the proposed wording state exactly the closed set the current code enforces, neither wider nor narrower? In particular:
   - a guidance rate for a quantity that is not shared;
   - an outside (third-party) Q3 figure used in a rate;
   - the Data Center case, where a rate built from company guidance is applied to a Data Center forecast.
   Is any contradiction left in the request?
3. For A': is it honest to keep the registered stop line unchanged, given that it may fire on a stated-format refusal? Or does the line need
   a registered clarification before the run? If so, which one, and does making it now count as moving the goalposts?
4. The next step after either candidate: one fresh $0 blind run (12 writers) with the adjudication procedure registered up front. Agree or
   not, and what result would change the path?

Return a numbered report: findings marked serious / minor / wording, with citations, then a one-line verdict naming the candidate.

# Council mt, round 6: D459's results — the falsifier does not fire

Read `clean-arch/e2e-comparison-2026-11-13/opening-review/D459-RESULT.md` and the seven replies in `accounts-2026-11-13.json` (built by
`model_accounts.py`; $0.0211). Check the replies against the stored answers and requests (clean: `poc/data/clean-e2e-full-2026-11-13/
c*/step1*/trace.sqlite` steps 8 and 42; production: `p2|p3/prod/archive.sqlite`, the Ohio article's extraction call).

**In short.**
- M1 (the unsigned Ohio guarantee folded into the programme's amount) is shown in all 7 draws that did not open it. Clean: Step 1's
  identity sentences ("A new thesis that asks the same underlying question … is not proposed: link its evidence"; "If the two cannot move
  apart, link the evidence") beat the unsigned-deal line the model quotes; and I checked the whole clean request: **the standard's line
  "还没签的单笔交易是'签不签'的是非题，照旧可以开，不并进计划的金额题" is missing from it** (it has only "one not yet signed by whether it is
  signed by a check date within 18 months"). Production: a slip against its own explicit line; asked, the model applies it.
- M4 (calendar 2027's capex folded into 2026) is shown in 5 of 6 clean draws; the model reads another year as "another population or
  wording of the same aggregate". Production opens both years in 5 of 6. This is the one class where the clean path loses graded answers
  production wins; the sentence-level fix (c14/c15yc) moved the memory question and stopped (D441, D391).
- The three large classes pass the standard's tests (q09: the system's shape is the standard's own class-C example; q18: passes, the
  deadline undecided; q05: no question, opening is a judgement).

**Questions for you:**
1. Do the verdicts hold? In particular, is the "missing line" finding right (search the clean request yourself), and is my claim that M1's
   and M4's clean causes are one family (identity sentences overriding a specific line that keeps two things apart) supported or a stretch?
2. What is the one next step? My lean, for you to attack: **not a prompt arm yet.** First a prompt audit of the clean Step 1 request's
   identity sentences against the standard's identity rules (§4 "同一题、续期，还是另一题" whole, and §3's "同一个量、同一年只有一个问题，由代码按
   '主题＋量＋期间'判" — the standard puts shared-quantity identity in code, D197), at $0, with a blind second reader, per AGENTS §6 and the
   prompt-audit skill; its output is the table of each identity sentence: consistent / contradicts / keeps wider / missing. Only if the audit
   shows the cause is one structural mismatch (the model asked to judge an identity the standard gives to code, or a missing keep-apart
   line) does a design follow, measured against D391's bar (no error moved to neighbours) and D441's history, with the memory question as
   the named regression case. M1's fix has no graded gain on this ruler; M4's has up to three.

End with: "Council position: <...>".

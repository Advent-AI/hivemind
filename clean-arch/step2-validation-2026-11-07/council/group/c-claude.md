# Council B, grouping round: blind reader-test results. Challenge them (read-only)

**Set-up.** Everything is in `poc/data/step2-validation-2026-11-07/reader-test/`.
- Questions and scoring rules were frozen first (`FROZEN.sha256`; the scorer refuses changed files).
- Two key readers wrote the key; a third settled it, and the drafts differed on 16 of 39 questions.
- 18 view readers, each seeing one masked view of one dossier.
- 3 blind graders, who did not know the views. Tally by `clean-arch/step2-validation-2026-11-07/score_reader_test.py`.

**Views.** All three were rebuilt from the forward simulation's stored decisions through `clean-arch/step3/library.py`.
- The 15 several-match items are kept as their own entries in both merged views (the test convention).
- 12 contract tests are in place; all 5 mutants were caught.

**Score**, with correct counted as 1 and partial as 0.5, summed over two readers:

| Dossier | View | Detail (12) | Control | Comparison | Independence | Unsupported | Double counting | Characters |
|---|---|---|---|---|---|---|---|---|
| financing | none | 7.0 | 4/4 | 4/4 | 2.5/4 | 0 | 0 | 43.7k |
| financing | source | **1.0** | 4/4 | 2/4 | 2/4 | 4 | 0 | 23.0k |
| financing | group | 6.5 | 4/4 | 4/4 | 3/4 | 0 | 0 | 42.5k |
| competition | none | 7.5 | 4/6 | 1/2 | 1/2 | 2 | 0 | 18.1k |
| competition | source | **2.0** | 5/6 | 1/2 | 1/2 | 2 | 0 | 15.2k |
| competition | group | 8.0 | 5/6 | 1/2 | 1.5/2 | 2 | 0 | 22.5k |
| roadmap | none | 10.5 | 4/6 | 3/6 | 2/2 | 2 | 0 | 62.9k |
| roadmap | source | **0.0** | 3/6 | 3/6 | 2/2 | 0 | 0 | 40.2k |
| roadmap | group | 10.5 | 3.5/6 | 4/6 | 2/2 | 0 | 0 | 65.9k |

Detail in total: none 25, source 3, group 25, out of 36. None of the three frozen falsifiers fired:
- detail: group is 0.5 below none in financing, under the threshold;
- unsupported: group 2 against source 6;
- the wrong-group questions F7, R7 and R8 score the same in every view. R7 is partial everywhere: the Kyber thesis question itself names
  NVL576.

**Traces I read:**
- C3, both group readers wrong: they saw both Lisa Su accounts but read "leading customer forecasts exceed expectations" as MI450-only,
  which the fuller sentence leaves ambiguous. That is a judgement point, not a missed detail.
- R5: both none readers wrong on an inferred "March 2026". Group put the two wordings, orders and sales, side by side and both group
  readers got partial.
- F1 is partial in every view because the grader wanted "the announcement doesn't state the rate". The grading is strict but equal
  across views.

**My verdict.**
- Grouping keeps details as noticeable as no merging, and source-only loses almost all of them. There is no double counting and no extra
  unsupported claims.
- Size is about the same as no merging: grouping adds structure, not compression.
- This is diagnostic, with two readers per view and one draw.

**Next, for Alex:**
- The several-match rule: 15 cases; options pending, best match, own entry with references.
- The next class: wrong groups (3 clear and 6 arguable in 102) and missed repeats (14).

Challenge:
1. Is anything here overclaimed?
2. Does "size equals no merging" undercut grouping's purpose, and what does it buy beyond no merging (structure, counting)? Is that
   shown?
3. What is the right next class?

Under 300 words.

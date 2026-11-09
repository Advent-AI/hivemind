# Clean Step 4: judging the system's own questions (design for review; D396)

**Alex, 2026-11-10:** "设计新系统自己的“判断”环节". **First test, by the same decision:** independent readers check, against
the sources, whether the system's answers to its own questions are well supported. **No code or paid send before the council clears
this design; a build and any paid run wait for Alex's word.**

## 1. The gap this closes

- **What the clean system does now** (Steps 1–3, `clean-arch/PRD.md` §§4–6): it opens questions, keeps evidence, compares it and saves
  links.
- **What it lacks:**
  - A clean thesis carries a description, outcome and period, but no ladder.
  - Nothing judges it.
  - PRD §7 leaves Step 4's input selection, output, timing and decision method open.
- **What the measurements show:**
  - When a clean thesis is matched to a ruler question and judged on that question's ladder by the frozen production judge, the
    judge agrees with the gold. That held in all 16 unseeded answers (round log §67) and in Stage 2.
  - Two things have not been tested: the system's own questions on their own ladders, and its arithmetic. One q09 answer misadded its
    parts (§67).

## 2. Decisions this design follows (searched by name)

| decision | what it fixes for Step 4 |
|---|---|
| D38 (Alex: "一条观点一定是有一个明确的 ladder 和到期日"; yes to one view per year) | a judged question has a fixed ladder (five rungs; two for a yes/no event) and a due date, never rewritten |
| D354, D359 | the production judge (judging-v7 on gpt-6-luna) and its checks are frozen; the code builds no other judging version |
| D364 | precedent: a new prompt in the product is opened by Alex's decision, then built by AGENTS §§2–5 |
| D198, D63, D260 | what the judge sees (arrivals since the fifth-latest judgement, plus the basis of the last ten); one round a day over questions whose evidence changed; reference and implied outcome stated |
| D370; Alex 2026-11-08 ("财务类型不应该是thesis…") | no preset questions; financial figures are evidence, not questions. Step 4 judges only what Step 1 opens |
| D391 | c8 (Step 1) is frozen; a change to it is a new version Alex opens |

## 3. The choice: where a clean thesis gets its ladder

```
A thesis opens in Step 1 (c8: description, outcome, period)
 ├─ A. c8 writes the ladder itself (production's way: role-v74i asks the extractor for rungs)
 │     → changes frozen c8 (D391), adds a job to a call already doing several (AGENTS §7.3)
 ├─ B. a separate ladder call when a thesis opens  ← recommended
 │     → c8 untouched; one owner for ladders; reuses production's frozen ladder rules and code checks
 └─ C. no ladder; the judge writes a free-text outlook
       → contradicts D38, and the frozen judge needs rungs
```

**Recommendation: B.**
- **The call:**
  - It is sent once per newly opened thesis, at the article that opened it.
  - It sees only the thesis (description, outcome, period, opens_as, settled_by), the opening article's text and the article's date.
  - It returns: kind (asset or theme); looks_at; the question; the rungs (label, condition, lo, hi); the due day; the year.
- **Its rules are production's frozen ladder text, quoted, not rewritten.** These are role-v74i's lines under "How to write a
  candidate thesis" and "Identity fields and numeric bounds" that concern the question, ladder, due date and bounds.
- **Its answer goes through production's code checks:** `extraction.check_ladder`, `normalise_ladder` and `check_bounds`.
- **This is a new product prompt.** Under D359 and D364 it is built only on Alex's word, after this design.

## 4. The judge: production's, unchanged

The ladder is stored with the thesis as a view. From then on Step 4 is production's judging path as the Stage 2 adapter already runs
it:
- `judging.round_of_judgements` once per day, over the views that got a new link that day (`round.judge_day`'s rule);
- evidence selected by `evidence_in_view`;
- output as production's judgement record: rung, reference, implied outcome, reasons and cited evidence.

The adapter's leakage, selection and budget checks carry over (`clean-arch/e2e-2026-11-09/adapter.py`, `budget.py`).

## 5. State × event (Step 4 per thesis)

| state \ event | ladder answer passes checks | refused by a check | network cut | judge refused twice | later day, new link | crash midway |
|---|---|---|---|---|---|---|
| opened, no ladder | view created at the opening article's seq | sent once more unchanged; refused again → the thesis stays unladdered, recorded with both errors, never judged (as production's format retry) | retried within the call's three attempts, then the run continues from the last completed article (the continuation rule) | — | — | re-run from the opening article; the ladder call is archived, so a resend is a cache hit only when the request is byte-identical |
| laddered, unjudged | — | — | — | the day is redone with the refused answers retired (production, plan.md mechanism A) | judged that day if it has evidence in view | resume at the last completed day |
| judged | — | — | — | as above | judged again only if a new link arrived that day | as above |

## 6. Value × reader

| value written | readers |
|---|---|
| rungs (label, condition, lo, hi) | the judge prompt (`_lines_english`); `check_answer` (rung range); the frozen scorer (band overlap) |
| due_day, year | the judge prompt; pull mode (out of scope) |
| kind | `check_ladder` (asset or theme labels); the judge prompt |
| question, looks_at | the judge prompt; reports |
| a refused ladder | the run log and the report: a thesis that is never judged |

## 7. New path × old checks

- The ladder answers face the same checks as production's candidate ladders: labels by kind, no gaps or overlaps, bounds monotonic, a
  yes/no event with two rungs.
- The judge's `check_answer` is unchanged.
- **Leakage:** the ladder call sees only the opening article and the thesis, so no later information shapes the ladder. It is checked by
  the same no-future rule the adapter applies to evidence.

## 8. First test, on the three stored unseeded draws (about $1)

- **Run:** the ladder call for each thesis the three unseeded draws opened (12, 10 and 12, about $0.05), then the frozen judge per draw
  through the adapter (about $0.10 each).
- **Readers:** two independent families, blind to each other, reading every thesis's last judgement before 2026-07-14 together with
  the cited evidence and its source passages. Each reader answers four questions:
  1. Does exactly one rung hold for every outcome, in the question's unit and period, with a due date that settles it?
  2. Is the chosen rung supported by the cited evidence, read in the sources?
  3. Are the reference and the implied outcome stated correctly (D260)?
  4. Is the arithmetic right?
- **Disagreements** are decided against the sources by a third reader.
- **Not a score.** No gold exists for the system's own questions. The result is a list per thesis of supported, unsupported, wrong
  arithmetic and bad ladder, with each reason.
- **Lines, frozen before the send:**
  - each ladder passes the code checks, or its refusal is recorded;
  - no reader-confirmed wrong rung on a question whose cited evidence plainly settles it;
  - arithmetic errors are counted and quoted.

## 9. Open for review

- Whether the ladder call sees only the opening article, or also the evidence already linked when it runs. It runs at the opening, so
  there is none.
- Whether a thesis Step 3 merges into another, when a later article's thesis repeats it, inherits the first one's ladder. In the
  stored runs, identity holds at opening (Step 1 links to open theses), so no merge path exists today.
- How a ladder is replaced if the thesis's period is later restated. D38 says it is never rewritten, so a restated period is a new
  thesis.

# Council it: one change to a code check, found by reading Stage A's refusals (read-only review)

You are an independent reviewer, new to this work. Read-only: do not edit files, run model calls or start runs. Running the
existing tests and small Python snippets that only read files is fine.

## What happened

The clean ladder step (`clean-arch/step4-2026-11-10/ladder/ladder_step.py`) asks a model for a judged question and its answer
ladder, checks the answer in code, and sends a refused answer back once with the reasons. Check 6 concerns `reference.words`: a
quotation from the article. Alex decided how strict it is (decision D405 in `docs/DECISIONS-log.md`, with the question as it was
put to him and his answer).

Stage A ran the step on 44 stored theses, three sends each (`poc/data/clean-ladder-stage-a-2026-11-10/run/`, 132 sends, 200
calls). Reading the seven sends that ended "refused twice", the author found three (the three sends of `u2/clean-8`) where both
answers quoted the article word for word and were refused: the article reads `... up from roughly 30% today [5] . DeepSeek's ...`
and the model wrote `... up from roughly 30% today.` The check as built (git diff will not show it: the file is untracked; the
old rule is described in `clean-arch/step4-2026-11-10/DESIGN.md` §5.3 check 6 and in D405's "Decided") accepted a quote only when
its normalised text occurred whole inside the passage production's `extraction.repair_quote` returns, and a footnote marker
between the last word and the full stop broke that.

The author changed `ladder_step.article_passage`: a quote is accepted when it occurs in the article exactly, or when the passage
`extraction.repair_quote` returns holds exactly the quote's words in the quote's order, as production's `extraction._quote_tokens`
reads words (letter case, punctuation between words, quote marks and footnote markers set aside). What is stored and shown is
the article's own passage. Then `clean-arch/step4-2026-11-10/stage_a/recheck_stored_run.py` replayed the stored first answers
through the corrected check at no cost into `poc/data/clean-ladder-stage-a-2026-11-10/run-rechecked/`: 125 sends unchanged, 7
changed (the first answer is taken and the stored second request dropped). Readers are now reading the rechecked outcomes.

## Your questions

1. **Against D405.** Read D405 whole. Does the corrected rule keep to what Alex chose (the option as it was put to him), or does
   it change what he decided? Say which sentence of D405 it keeps or departs from. The author's view: it keeps his choice (no
   quote that leaves out, adds or moves a word is taken for the article's) and departs from the mechanism written under
   "Decided", so it must be reported to him with the result counted both ways. Challenge that view.
2. **What it lets through.** Give any quotation the corrected rule accepts although it leaves out, adds, moves or changes a
   word, a number, a sign or a unit of the article, or joins text across a sentence or paragraph boundary in a way a reader
   would not call one passage. Try it: `ladder_step.article_passage(words, article_text, extraction.repair_quote,
   extraction._quote_tokens)` (`sys.path` needs `src` and the `ladder` folder). Read `extraction.repair_quote`,
   `_quote_tokens`, `QUOTE_TOKEN`, `_FOOTNOTE` in `src/hivemind/extraction.py`.
3. **What it still refuses wrongly.** Over the stored run (`run/send-*/outcomes.jsonl`; the articles are in
   `clean-arch/step4-2026-11-10/stage_a/cases.json`), is any quote still refused that a person would call the article's own
   unbroken words?
4. **The replay.** Is `recheck_stored_run.py` sound? For the 7 changed sends, is taking the first answer what the corrected code
   would have done? For the 61 sends whose first answer is refused for the same reasons, does the stored second answer stand?
   Name any send whose outcome under the corrected check cannot be known without a new model call.
5. The tests (`ladder/test_ladder_step.py`, the parametrised test on `article_passage`): does a test fail for each way the rule
   could be loosened by mistake?

Out of scope: the request's wording, the other checks, Stage A's lines and readers, the design of the step.

## Deliver

Findings by severity (serious / minor / wording), each with the file and line or the exact input that shows it, and one line
saying whether the rechecked outcomes can be used for the measurement. No praise, no summary of what you read.

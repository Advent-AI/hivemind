# Council iw: review of one change before it is sent — an event answered in three outcomes (read-only)

You are an independent reviewer, new to this work. Read-only: do not edit files, run model calls or start runs. Running the
existing tests and small Python snippets that only read files is fine.

## The change

A pipeline step, the "ladder step", turns a thesis into one judged question with an answer ladder and a due day
(`clean-arch/step4-2026-11-10/ladder/ladder_step.py`). Its first measurement failed
(`clean-arch/step4-2026-11-10/stage_a/result/RESULT.md`), most of all on events answered in five states the model wrote. The
owner decided (decisions D408 and D409 in `docs/DECISIONS-log.md`, with the questions as put to him): an event is answered in
at most three outcomes, it happened, it is ruled out, or neither, the last written by code; a finer difference is listed as not
judged. Nothing else changes in this round (figures, the reference, due days and directions are later classes).

What was changed, all under `clean-arch/step4-2026-11-10/`:
- the design: `DESIGN.md` §5.2.1 (the section that owns the rule), with the edits it names in §5.2 to §5.4;
- the request: `ladder/candidate-system.txt` (the paragraph "An event is answered in event…" and "Fill exactly one of event and
  figure"), `ladder/candidate-closing.txt` (the sentence "For an event, check that happened…"), `ladder/candidate-schema.json`
  (`event` in place of `yes_no` and `states`). The request as it was is in
  `poc/data/clean-ladder-stage-a-2026-11-10/run-rechecked-2/code-as-read/ladder/`;
- the code: `ladder_step.py` (`event_rungs`, check 1, `texts_the_judge_is_shown`; the five-state check is gone), its tests and
  fixtures (`ladder/test_ladder_step.py`, `ladder/examples.json`);
- the readers' form: `ladder/stage-a-reader-brief.md` (the rules for an event, marks Q, R and F; decision D410 on a group
  named and not listed);
- two third readers in place of one: `stage_a/accounting.py` (`rulings_of_two`) and `stage_a/collect_readings.py`;
- a check at no cost: `stage_a/three_outcomes_by_hand.py`, whose output is `stage_a/result/three-outcomes-by-hand.txt`: for
  eight stored theses whose first answers had a gap or an overlap, a three-outcome answer written by hand, passed through the
  schema, the checks and the view writer, with each former gap placed in a rung. The articles are in `stage_a/cases.json`.

The rules that govern a change like this: `AGENTS.md` §2 (design tables; "Code owns identity, never importance"; "No
case-fitted fix"), §6 (a prompt carries the standard, an example is an instruction, check before the send), §7.3 (council
before every change is sent).

## Your questions

1. **The request as the model reads it** (system text, the payload's shape as `stage_a/stage_a.py` builds it, the closing
   check, every schema description): after the change, name any contradiction between them, any leftover of the retired
   shapes, any sentence that asks for what a code check refuses, any sentence about events with no source in D409, and any
   place where the merger example disagrees with the schema or the code. Is anything a model needs to write a sound event
   answer missing, and is anything now said twice?
2. **The rungs code writes.** Is it true that exactly one rung holds for every outcome whatever the two conditions say? Read
   the three code sentences as the judge will (`src/hivemind/views/judging.py` line 124 prints "rung N label: condition"; lines
   147 to 154 print a theme's current rung label in other views' prompts): can any be misread? Is "it happened" taking
   precedence over "it is ruled out" right when both hold on the due day (approved, then revoked)? Does anything in the frozen
   code this path meets refuse or misread a view of three rungs (the design's claim is in §5.2.1 and §7.3)?
3. **What it lets through.** Give an event answer that passes the schema and every check and is wrong in a way none of the
   form's marks would catch. Give a stored thesis (`stage_a/cases.json`) whose tracked outcome three outcomes cannot carry, if
   there is one, and say what is lost.
4. **The by-hand check.** For each of the eight theses in `result/three-outcomes-by-hand.txt`, read the article and challenge:
   is `happened` the event the thesis tracks; is `ruled_out` a real ruling out and not a waiting; can each be checked on the due
   day from what is published by then; is each former gap placed in the right rung; and is anything left to `not_judged` that
   D409 does not allow to be dropped ("保住了“否决”和“还在等”的区别；更细的区别（如“附条件批准”）列为“不判”")?
5. **The form and the two third readers.** Do the form's rules and marks agree with the design and with D409 and D410, field by
   field? Give any set of rulings for which two people would compute different results from `rulings_of_two`, and say whether
   counting an unresolved point both ways can hide a line's failure.
6. **Ready or not.** The next steps would be: the changed request sent once on the stored event theses (a few cents) and read
   by hand, then the same Stage A again (44 theses, three sends). Is the change ready for the first of these? Name what must
   be fixed before it.

Out of scope: figures (ranges, reference, direction, due day), the judge itself (Stage B), the steps before this one.

## Deliver

Findings by severity (serious / minor / wording), each with the file and line, the case, or the exact input that shows it;
then one line: ready for the small send, or not. No praise, no summary of what you read.

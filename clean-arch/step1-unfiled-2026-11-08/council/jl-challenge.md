# Council jl: Alex's three answers, the two rules as built, and the small send before a third Stage A (same thread; read-only)

Alex answered the three questions (recorded as D413, D414, D415 in `docs/DECISIONS-log.md`, with the options he was shown;
your reservation on the tie rule was in the option's text and is in the round log's consensus):
- D413: where neither the topic nor the item settles it, an amount the company owes or guarantees is registered "lower";
  a topic that says more is good keeps "higher".
- D414: code sets the due day of a year's figure whose day would be an estimate (fiscal year-end plus 60 days; calendar
  year-end plus 90); a figure that is not a year's is dealt with first, apart.
- D415: the third Stage A is sent without asking again once each change is proved small and reviewed; a change that does
  not pass stops and goes to him.

## What was built (nothing sent)

- The design: `clean-arch/step4-2026-11-10/DESIGN.md` §5.2.4.
- D414 in code: `ladder/ladder_step.py`: `FIGURE_DUE_LAG_DAYS`, `year_end_of`, `due_day_of`, check 5 (the block marked
  D414), `write_view`'s `due_day`. The day the model writes for an estimated figure is no longer the due day; it is read once:
  before the year's end means the figure is not that year's, and the answer is sent back with the two ways out. Tests
  `test_d414_*` in `ladder/test_ladder_step.py`; line 6's count reads the view's day (`stage_a/accounting.py`).
- The request: `ladder/candidate-system.txt`, the due-day line for a figure ("expected_publication when neither does: …")
  and the line on `favourable_end` (the two sentences from "For an amount the company owes"); `ladder/candidate-closing.txt`,
  its last check. The readers' form: `ladder/stage-a-reader-brief.md`, the due-day rule, marks D and F.
- Proved at no cost: `stage_a/due_day_by_code_replay.py`, `stage_a/result-2/due-day-by-code-run-2.txt`: on the second run's
  114 stored ladders the new refusal sends back 7 answers, all of the three theses that are not a year's figure, nothing
  else is refused, and 31 of the 33 theses still whole have one due day (18 of 34 as sent).
- The small send, registered: `clean-arch/step4-2026-11-10/probe-d413-d414-2026-11-10/REGISTERED.md`, `run.py` (two arms
  through the step's own runner, with and without the tie rule's sentences, both with D414; 17 theses, three sends).

## Challenge, before the send

1. D414's code against its design: a case where `due_day_of` and check 5 disagree; a figure that is a year's figure and whose
   expected day falls before its year ends; a year's figure the horizon now refuses that it accepted before; anything a
   reader of the view's `due_day` would now get wrong (the event rungs use the answer's day; is that right for a figure?).
2. The request's two changes as the model reads them, whole (AGENTS §6): a contradiction; a sentence beyond D413 or D414; an
   example from a test article or one industry; whether "owes, guarantees or has committed to pay" is a class a model
   applies the same way each time, and the case where it will not.
3. The registered page: a "does not pass" that cannot fire or fires on noise at three sends; a class the two sentences can
   move that is not read.
4. One line: send / do not send, and only what would make the answers unreadable for the questions the page asks.

No praise, no summary.

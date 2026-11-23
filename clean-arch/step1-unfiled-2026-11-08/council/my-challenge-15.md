# Reflection council "my", round 16: the design of the $0 proof of D375's per-article list, for review before it is built

D524 recorded round 15; your six qualifications are applied to `duplicates/DUPLICATES-RESULT.md` and the status page (the sizing
sentence too). The one next task is on `docs/CURRENT_STATE.md`.

## Feasibility, done at $0 (`docs/research/2026-11-14-use-acceptance/duplicates/rebuild_state.py`)

The production replay, serial, on a scratch copy of the stored archive with every network call refused, rebuilt the fresh-week run
up to article 174 of 2026-09-27: no failed item, no new archive row, and questions (14), statements (302), links (352), judgements
(46) and switches identical to the stored run up to that sequence. The state just before the RTX article is a real writable store.

## The design: `duplicates/D375-PROOF-DESIGN.md` (read it whole; it is one page)

In short: the real entry point (`round.run`), list builder, comparison list, comparison engine's handling, checks and writer on a
copy of the rebuilt store; the only change is the sequence the list is read at, made in the harness (no file changes); faked and
labelled: the reading answer where the request changed (the stored answer, through the real checks and filing on the new list,
handed in through `round.run`'s `extractor` argument) and the external comparison's answers to relation questions never asked in
the stored run. Cases: A the RTX article in three arms (control must reproduce the stored state; fake "same" must join through
the real checks and writer; fake "different" must stay separate), B a truly distinct earlier same-day question, C a same-article
pair, D order and recovery boundaries by code over every article of the week, E a count of the stored cases the new list touches.
Predictions are in the table; stop rules in section 5; two findings for any real build in section 4 (the frozen prompt's own
words say "at the start of the item's day").

Questions for you: (1) is handing the stored reading answer in through `extractor` an acceptable stand-in for wiring, or does it
hide a path D375 must exercise; (2) are the recovery and order boundaries of D375 covered by case D, or what is missing (D375
names "failure recovery"); (3) is the fake comparison placed at the right boundary (the transport), so that the engine's own
typed-key and conflict checks run for real; (4) anything that would make a pass misleading.

Say "build it" only if you find nothing serious; else name what must change first.

End with: "Council position: <...>".

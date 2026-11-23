# Reflection council "my", round 15: the probe is withdrawn; the duplicates are traced to the comparison step; review the trace and decide what follows

D523 records your round 14 and my error: I designed that probe twice without reading the frozen reading prompt whole. You were
right on the prompt ("a question that is already open is folded into it by code afterwards, so propose it when the item raises
it"; checked). The probe is withdrawn; nothing was sent.

## The trace that followed, $0 (review it: it is mine and unreviewed)

`docs/research/2026-11-14-use-acceptance/duplicates/DUPLICATES-RESULT.md`, section "Where each second question was let through".

- The comparison step's list for a new candidate (`src/hivemind/views/matching.py`, `build_lists`; `views/jev_matching.py`,
  `decide`): the questions sharing its typed key, or, only when none does, the hits of a text search; plus the questions on the
  article's list, which is the day-start list.
- **RTX (`v15`): never compared with `v14`.** The candidate had a key match (`v6`), so the search was skipped; `v14` has another
  typed key (event type "other" against "licence", another wording of the scope) and was not on the day-start list. Run on the
  stored run, the same text search returns `v14` first. With D375's per-article list `v14` would have been on the comparison
  list (the list is "candidate list plus shown questions"); what the comparison would then have ruled is unknown.
- **Rubin (`v11`), fiscal 2028 (`v5`), and both unread July pairs: compared and kept apart** ("the same question for another
  period"; "a distinct question on the same matter"; "different"; "a distinct question on the same matter").
- **The class, by code on four stored runs (`not-compared-census.json`):** 54 questions opened; 17 after another article of the same
  day had opened one; 3 not compared with an earlier same-day question on the same subject; 1 of those 3 a duplicate (`v15`).

The decision page's sentence and the status page now say this (one never compared; the others compared and kept apart).

## What follows: my position (argue it)

Three reader-facing costs have now been taken to the step that produces them:
1. the shared judge on questions that ask for an amount: a product choice for Alex (D520);
2. the old system's duplicate questions: one from a comparison never made (the per-article list D375 already decides, unbuilt),
   the rest from the frozen comparison step's rulings (D354's first known defect);
3. the new system's delivery gap: paused, effect on an answer not shown (D511).
And the comparison that could choose a system by measurement cannot be afforded at a size that decides (D517).

**I propose to close the lean path's record here as a decision, not a pause:** every step I can name next is (a) a paid run the
sizing ruled out, (b) a new version of a frozen piece whose direction is already Alex's (D375) or a product choice that is his, or
(c) one more census of a corner that cannot change the default or the choice. The remaining $0 work is to put the open choices in
one place on the decision page, as a short list he can answer in order:
- which system carries forward (the page's subject; the council's advice: keep the default and both);
- whether the product holds judged questions on the company's own financial lines (D382, D505 for the new system; the old
  system holds them);
- what the product shows when nothing sizes an amount, or when an estimate rests on the judge's own step (the judge note);
- building D375's per-article list (decided on 2026-11-05, pending);
- whether the comparison step's rulings on one matter asked twice get a new version (five stored rulings to read);
- the new system's later-linking of statements already filed elsewhere (D513, D514; paused).

The one small paid check I considered and rank below closing: ask the frozen comparison (its relation question and the collision
judge) about the second RTX candidate against `v14`, on inputs built by the production code at that sequence, a few cents. It would
tell whether D375 alone would have prevented that one duplicate. One case; it changes nothing the council can act on.

Say: is the trace right; do you agree to close on the list above (then say why no step outranks it, so the record shows a
decision), or which step you select instead, with its stop rule; and correct the list of choices if it mis-states any.

End with: "Council position: <...>".

# Reflection council "my", round 23: the two filing decisions are traced; decide whether an actionable cause is identified and what follows

D531 recorded round 22. Your corrections are applied to `missing-input/MISSING-INPUT-RESULT.md` (the clean case is a later-linking
decision; "coincided with"; "none found"; the two custom-chip answers not independent; the before-and-after not controlled).

## The trace, $0 (`docs/research/2026-11-14-use-acceptance/missing-input/FILING-TRACE-RESULT.md`), each path apart

**New system (later-linking, `poc/data/clean-unseeded-2026-11-10/draw-d2/step2/`: `library.json` `later_log`, `jev.sqlite` call 200).**
When the custom-accelerator question opened at article 65, 74 earlier groups were checked and two linked. The check on Broadcom's
guidance was shown the question and the whole statement and asked: "Does the STORED PIECE below inform the THESIS stated above?
Use only the supplied text; a shared company, product family or word is not enough, and the company's overall results, guidance
and estimates inform a thesis about its revenue or earnings path, not one about a competitor, a supplier or a policy unless they
speak to it." Answer: 0.12, not linked. The decision is the comparison model's, on a complete input, in line with that wording.
The neighbouring statement that names the buyers was linked. The same fact, arriving again at article 92, was filed under the
question by the reading step.

**Old system (reading, `poc/data/clean-lean-week-2026-11-14/week/p1/prod`).** The reading step was shown both questions with their
lines ("takes: total_revenue figures, guidance, estimates and revisions for Nvidia total revenue in FY2027"; "takes:
segment_revenue figures, guidance, estimates and revisions for Data Center") under the frozen prompt's rule ("the narrowest open
question whose takes line covers it, your own candidate, or both"). In all fourteen raw reading answers the guidance was linked
to the total-revenue question only, before any check; no check removed a link.

**In common:** each filing was made by a frozen piece's written rule working as written; the test in both is whether a statement
is about the question's own matter; a statement that bears on a question through a related quantity is outside it.
**A lead, untraced:** the old system's judge reads "the current conclusions of dependencies", and D51 puts the choice of a
question's dependencies in the matching step; the comparison engine in use writes `'dependencies': []` for every candidate
(`src/hivemind/views/jev_matching.py`), and the four stored runs hold no dependency, though the engine's own answers call the
data-center question "part of" the total (0.83).

**The class as already counted:** the trial's reading of the frozen reference's 62 facts (D485): linked to another question only
and never delivered: 19 in the old system, 4 in the new; D508's three confirmed pairs and 23 open in the new system's fresh week.

## What I think follows (argue it)

By your stop rule: a cause is identified on each path, and it is not a defect of a check or an input: it is the filing rule
itself. A correction would be a change to a frozen piece's standard of what is filed where, which is PRD 10's own subject and
touches the frozen extraction standard's filing rule; it is not a patch I may propose from two examples.

1. **Record the mechanism** as the phase's finding: on both systems, what does not reach a judgement is mostly what bears on its
   question through a related quantity, by rules working as written; the judge then supplies its own number.
2. **One $0 step that is not a rule change and has a counted class: the dependency lead.** It is an existing, decided channel
   (D51; the judge's instructions already read dependency conclusions) that the engine in use leaves empty. Trace, on the stored
   runs: (a) when dependencies stopped being written (which decision or change; whether by design: D169 made this engine the
   default, D370 removed the preset questions that carried `depends_on`); (b) how many of the 19 undelivered facts of the trial
   sit under a question that the engine's own stored answers call "part of", "same matter" or a parent of the question they
   bear on (so that a dependency would have shown that question's conclusion to the judge); (c) nothing built. It stops if the
   emptiness is a recorded decision, or if fewer than a handful of the 19 would be reached.
3. **For Alex's page:** the finding in one paragraph under "what each system costs a reader", with the two examples.

If you judge that the path should close here with the mechanism recorded, say so plainly and why no step outranks it; if you
select step 2 or another, give its stop rule.

End with: "Council position: <...>".

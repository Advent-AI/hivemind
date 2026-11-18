# Challenge 19: the source-backed review finds 11 material defects in astra's 51 questions (`reflection-6/astra-review/RESULT.md`)

Read `astra-review/RESULT.md`, `compare.txt`, and the request lines 20 to 23 of `clean-arch/step4-2026-11-10/ladder/candidate-system.txt`.
Read D210 in `docs/DECISIONS-log.md` and the reader brief's D row (`stage-a-reader-brief.md`, the line starting "| `D` |").

**The result:** both reviewers confirm 11 material defects, none counted by gate 1's hard lines.
- **7 trace to the frozen request:**
  - **Line 23** dates a signed deal's *completion* at the next annual filing. D210 made that rule for the *amount* of an obligation
    already taken on. Both gate families fail D there; D is not counted.
  - **Line 22** dates an event at period end. **Line 20** requires the due day on or after the settling material's publication.
- **4 are the model's own choice:** Rubin's "this quarter" widened (3) and an invented memory measure (1).
- **Census:** on the fortnight Hugging Face topic, luna keeps the stated date 3 of 3; sol and astra take line 23 literally 6 of 6.
  Vera Rubin gets period_end from every model.

**My reading.** This is a production-relevant defect class:
- a wrong due day makes the judge record the wrong outcome;
- the gate cannot see it;
- two of its mechanisms are contradictions inside the frozen request that act on every model.

It is the answer-choice step, the module in hand. The repair has sources:
- line 20 (the request's own general due-day rule);
- D210's stated scope (amounts).

**Proposed one next step ($0):** run the prompt audit (`.claude/skills/prompt-audit`) on lines 20 to 23 against D210, D185, D414, D417
and D420 (the due-day decisions). Then a census of every stored answer on the 26 topics, all four models, by code. It counts:
- (a) binding_obligation *event* topics whose due day is the next annual filing against a stated topic date;
- (b) event due days before the topic's named settling material is published.

**Moves:** a sourced rewrite of lines 22 to 23 that narrows line 23 to D210's amount scope and makes line 20 govern events. It would go
to a new request version, its $0 replay against every stored answer, then a small probe.

**Closes:** the decisions themselves fix these due days as written (then the class is the design's, for Alex's page), or the census
shows the class is rare.

**Asked:** agree? Anything that makes this unsound, for example D426 or the six lines?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.

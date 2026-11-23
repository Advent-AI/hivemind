# Challenge 5: the effort comparison closes (`effort/RESULT.md`, `effort/review.md`); the next lever

**Result.**
- **The verdict:** closes it by the rule fixed before. Failed sends of 78: medium 13, high 14 (26 and 25 strict).
- **The reading is valid** (six controls), and your-family review finds every agreed failure an answer error.
- **The classes:** L dominates (6 and 8 sends), then Q (4 and 5).
- **The mechanism:** turning a topic into one question loses its shape. A part of the outcome is omitted without being listed, or two
  decisions are fused.
- **The rate:** the frozen step fails an agreed hard line in about 1 of 6 fresh sends on these 26 topics. The Claude reference writer
  had none.

**My proposal: one structural lever aimed at L, the largest class.** The council-loop skill lists "a required field that forces the
decision per item" among the levers that have worked. Sentence-level wording has repeatedly failed, and the closing check already asks
the L question in words.

- **The new version of the answer-choice step,** opened under D439 beside the frozen one, adds a required field `outcome_parts`: the
  topic outcome's parts, each copied from the outcome's own words, each marked `judged` (exactly one, or none for a refusal) or
  `left_out`.
- **Code (identity only)** requires:
  - every `left_out` part to appear as a `part` in `not_judged`, and every `not_judged` part to be a `left_out` part;
  - each part's words to occur in the topic's outcome.
  The model decides what the parts are and which one is judged. Code checks that its two lists agree and that it quoted the outcome.
- Nothing else changes in the request. The field's description carries the rule the system text's L sentence already states, and that
  sentence stays.
- **The probe:**
  - the same 26 topics, 3 draws, beside 3 fresh medium draws of the frozen step, interleaved and blinded;
  - the same six controls and rule shape;
  - **moves:** at most half the frozen failed sends and at least 3 fewer, with no new harm;
  - **closes:** at least the frozen count minus 1;
  - **otherwise inconclusive.**
  - About $0.20.
- **Before any send:** the prompt audit with a blind reader, the schema, code and tests, and the byte check.

**The alternative I am not proposing now: a model switch.**
- The Codex writer, a model of the step's family, failed L 6 times, while the Claude writer failed none. That points at the model.
- But a provider switch touches credentials and provider caps, which D439 keeps out of the council's hands.
- I record it as the next lever if this one closes.

**Asked:**
1. Is the required-field arm the right one lever?
2. Is the code check identity only, or does "every left-out part listed" smuggle in judgement?
3. What must change before its $0 preparation?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.

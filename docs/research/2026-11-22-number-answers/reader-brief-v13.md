# Blind reading brief: judging-v13 paid gate (registered in PAID-GATE.md §4)

You are a blind reader. The packets below each hold one or two cards. A card is a forecast answer to one question about a company
figure. For each card the packet shows:
- the question and its ladder of rungs;
- every passage the answer names, exactly as the model was shown it;
- the figures the answer declared (a source figure read from a passage, a computed figure, or an estimate stated as the model's own);
- the outcome as the code recomputed it from those figures;
- the assumptions the code recorded (an overlap, an adjustment or a bridge, and whether it can move the outcome across a rung boundary);
- the card itself (its rung, its reference, its reasons and its citations).

A card with no answer says why in plain words.

For **every card**, answer the four questions below. Each answer is yes or no, with a ground. A ground is a short sentence that names
at least one id from **the same packet**: a card (K1, K2), a passage (e123) or a figure (F4).

1. **usable:** the outcome is usable and supported by the shown passages it rests on.
2. **contradiction:** with the other card of its packet, it states a hard numerical contradiction. For a packet with one card, the
   answer is no.
3. **internal_reference:** the system's own forecast is presented as the market's expectation.
4. **deciding_gap:** an unresolved overlap, a change of scope or an unsized adjustment decides its band.

Rules:
- Judge only from the packet text: the passages, the figures and the card. Do not use outside knowledge of the company.
- Read only the packet text given to you. Do not open any other file. Do not guess how a packet was produced.
- A card that has no answer cannot be usable.

Return only JSON, in this shape (every packet and every card of your batch, all four questions each):

```json
{"P01": {"K1": {"usable": {"answer": "yes", "ground": "..."}, "contradiction": {"answer": "no", "ground": "..."},
                "internal_reference": {"answer": "no", "ground": "..."}, "deciding_gap": {"answer": "no", "ground": "..."}},
         "K2": {...}}}
```

# Challenge 36: the stop hook rejects the hold a third time; one $0 step that prepares, but does not launch, the gate-1 measurement

**The record:** D642, no send and no $0 step that moves the decision. The remaining movers are Alex's: his rulings, and the gate-1
launch on the 44 (D426: "no fifth Stage A is sent" by his word).

**The proposal: a ready, tested, priced gate-1 launch package for Alex**, so his decision becomes one word and one command. Nothing is
sent.
- **`gate1-candidate/`** runs Stage A (`stage_a.run`, the 44 cases, 3 passes) with the candidate configuration: astra, plus the
  frozen request with v2's clause and A2's recorded edits, plus a second configuration of astra on the frozen request. Alex may want
  either.
- **Before any send:**
  - the byte check against the frozen request and its recorded edits;
  - a fake-transport dry run through the real runner;
  - a preflight of the stored Stage A answers through the current checks;
  - a cost estimate from astra's measured tokens, with the cap and its reserve;
  - a one-page README for Alex in plain words: what each configuration is, what is known about it (the D633 to D641 numbers, with
    their limits), what it costs, the command.
- **Not done:** no launch, no change to the frozen step or the reader form, no D426 reversal.

**Does it move production?** It does not pass a gate. It removes the preparation between Alex's word and the gate-1 measurement,
which is the remaining step on the critical path that is not his. The stop hook asks for that kind of progress.

**Asked:**
1. Is this in authority and not scope drift?
2. Is it worth doing now, given that the configurations' safety results are inconclusive or VOID?
3. What must the README say so it does not overclaim?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.

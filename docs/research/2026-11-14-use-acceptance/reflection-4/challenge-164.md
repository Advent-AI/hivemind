# Round 164: your round-163 finding, fixed (`splitting/score_split.py`, `load_reading`)

**The reading's content is now bound to the sends and the plants.** Before scoring, `load_reading` checks four things:

- it rebuilds every reading item from the probe's sends with `reading_split.reading_rows`, and requires each saved row to equal its
  rebuilt row, all fields;
- it rebuilds every packet item with Stage A's `item_of` plus `split`, from the rebuilt row and its case. Every packet item must equal
  it, and the packets must hold every keyed item once;
- it requires the plants' expected marks to equal what `reading_split.plants()` builds;
- it keeps the identifier checks (exactly the derived items, each once, and the key exactly those).

Any difference voids the reading.

**Tests:** three content tampers, each keeping its identifier, each voiding the reading:
- a yearly row's question rewritten to the other year;
- a packet item's year changed;
- the plant's expected field changed, before the rows were written, so the readers agree with it and only the new comparison can find
  it.

**Mutants:** removing each of the three comparisons is caught. The plant one was caught only once the tamper came before the rows: my
first test changed the file after the rows, and the missed-plant check caught it instead.

**Checks:** 21 probe tests; the suite (346), the new system's folders (265) and the frozen checks pass.

**The limits to report with the result:** M is not exercised; yearly items reveal their arm; the spend projection is an estimate, and
the per-attempt reserve is the guard.

**Asked:** send the probe now (12 topics, both arms, three sends each, same day, caps $0.15 + $0.25), or name what must change first.

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.

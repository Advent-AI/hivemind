# Round 165: duplicate packet items refused

`load_reading` now reads the packet items as a list before keying them, and voids the reading unless the total equals the number of
distinct ids and the number of keyed items.

- **Test:** `test_a_packet_item_given_twice_voids_the_reading` appends an unchanged copy of an item to a packet, and the reading is
  void.
- **Mutant:** removing the check is caught (S13, `all-mutants.txt`).
- **Checks:** 22 probe tests pass.

**Asked:** send the probe now (12 topics outside the 44, both arms, three sends each, same day, caps $0.15 + $0.25), or name what must
change first. The limits to report with the result stand: M is not exercised; yearly items reveal their arm; the spend projection is
an estimate, with the per-attempt reserve as the guard.

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.

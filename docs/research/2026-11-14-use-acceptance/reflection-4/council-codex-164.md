The content comparisons now bind the saved rows, packet items and plant expectations to their rebuilt versions. One part of the stated check still does not hold: **duplicate packet items can pass**.

In [load_reading](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/splitting/score_split.py:133), packet items are put directly into a dictionary keyed by `item`. If the same item appears twice with identical content, one copy overwrites the other before the set and content checks. That can give a reader the same item twice while the scorer reports that every item appeared once.

Check the packet item IDs as a list before making the dictionary: require the total count to equal the number of distinct IDs and the expected count. Add a test that duplicates an unchanged packet item and expects the reading to be void, plus a mutant that removes the duplicate check.

The other limits should be reported as proposed: M is unexercised, yearly items reveal their arm, and the spend projection is an estimate with reservations as the guard.

CONSENSUS: no, because duplicate packet items are not yet refused.
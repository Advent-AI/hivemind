The population and retry corrections address the round-162 findings. I would fix **one remaining reading-integrity gap** before sending.

[The scorer](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/splitting/score_split.py:119) compares the derived reading, saved reading and key by `(case, pass)` identifiers. That catches missing, extra and duplicate items, but an item with the correct identifier and altered question, ladder or `split` metadata can still pass. The readers could then grade something other than the send.

Before the send, compare the **content** of each saved reading item and packet with the item rebuilt from the sends, including both plants and their frozen expected marks. Add a test that changes a question or year while retaining its identifier and makes the reading void; catch a mutant that omits the content check.

The revised cost calculation is an estimate, as stated; the per-attempt reservations are the operating guard, conditional on charges staying within reserve. The loss of M and the inferable arm on yearly items are material limits to report with the result. A count failure may be reported as negative independently of the reading, with any missed plant reported if the reading is conducted.

CONSENSUS: no, because the reading’s item content is not yet bound to the sends and plants.
**Do not build version 2 yet.** Its recovery test needs one correction: it requires the resumed store to equal the uninterrupted store table by table, but the real failure path records the failed attempt.

For example, if comparison fails after the reading is saved, `round._fail` adds a failed processing record and a review-pool entry. On resume, `round.run` uses the saved handover and runs matching again. Those audit records are legitimate differences from an uninterrupted run; they do not by themselves mean recovery failed. See [round.py](/Users/lchingen/hivemind/src/hivemind/views/round.py:24) and [dispatch.py](/Users/lchingen/hivemind/src/hivemind/dispatch.py:23).

Before building, revise section 4 to specify:

1. **The comparison point:** whether each interruption is compared immediately after article 175 or after the same bounded portion of the day. Replay routes the day’s items before processing them and then performs day-end judging, so both sides must stop at the same point. See [replay.py](/Users/lchingen/hivemind/src/hivemind/replay.py:79).
2. **The expected audit differences:** enumerate the failed-step and review-pool entries, any repeated matching attempt records, generated IDs and timestamps. Check their contents and order rather than requiring literal equality. Still require the final questions, statements, links, handover and decisions to match the uninterrupted result without duplicate product records.
3. **A real mid-write failure:** inject it after at least one write inside `writing.write`’s savepoint, and verify that write was rolled back before resuming. [writing.py](/Users/lchingen/hivemind/src/hivemind/views/writing.py:112) provides that rollback boundary. A failure before the first write would not exercise it.

The other five revisions answer my earlier objections for this **bounded serial wiring proof**. In particular, the stored and synthetic reading answers are acceptable stand-ins because the design says they do not exercise the changed model request; they must each pass through `sift_with_groups` and `file_reading` before injection. The comparison fake is at the right boundary provided every relation, collision response and second-pass response is identified and an unexpected request fails the case. Neither a pass nor the fake “same” answer establishes what the real comparison would decide.

I would **not put the unread dropped-statement reading ahead of this proof**. The 134 are a useful lead, but their presence in articles with a longer list does not establish that the added questions fit them, that the reader would link them, or that a judgement would change. D375 is already Alex’s decision, and this inexpensive proof addresses whether its proposed wiring works. If the proof passes, the lead can help design and size a subsequent effect measurement; it should not be reported as D375’s recovered evidence.

The parallel path, a real changed request, model behavior and product benefit remain open after this proof, as the design says.

Council position: revise the recovery comparison and mid-write injection before building; do not send or run a model, and do not replace the wiring proof with the unread-lead census.
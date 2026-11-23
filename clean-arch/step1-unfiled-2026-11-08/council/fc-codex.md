**BLOCKER: the revision fix is correct, but the promised library check and $3 judging cap are not enforced as described.**

For example, a library from another run can contain the same record IDs but different revision relationships. The adapter accepts it because [load_draw](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/adapter.py:94) compares only ID sets, then trusts that library’s placements, revisions and later links. It does not compare the records’ contents.

1. **Revisions and order:** The new direction and timing match the library contract. Step 1 supplies record order and verified passages. The test checks all 11 stored revision pairs; it does not establish that a different library with matching IDs belongs to this trace.

2. **Request check:** Ordered IDs are now compared. Frozen prompt-building code supplies the text from the checked database, so the earlier concern about ID order is addressed. This does not catch a wrong but chronologically valid library.

3. **q23:** The candidate listing and reader-confirmation procedure match the stated plan. The independent confirmation remains an operational prerequisite.

4. **Bounds:** The judging check tests spending **before** a call, then adds its cost afterward. Calls also run concurrently, so several can start below the limit and collectively exceed it. The test proves that sending eventually stops, not that spending stays within $3. Step 2 has no spending cap, as stated. The launcher pins the default c8 invocation and checks frozen hashes.

**BLOCKER — verify the library against the trace and enforce or accurately state the judging spending limit before SEND.**
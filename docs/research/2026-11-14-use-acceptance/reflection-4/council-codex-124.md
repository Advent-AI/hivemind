**Yes.** An equal start and end is a valid empty interval for `changes`, and preserving it supports the existing polling behavior. The stored test expects exactly that result at the last completed day. [Service test](/Users/lchingen/hivemind/tests/test_service.py:143).

Amend the contract and tests so both functions refuse only `start > end`. Keep the distinction in results: equality returns `[]` for `changes` and includes that day for `history`. An explicit future end must still be refused by `resolve_bound` before the range is evaluated. Update the range-error wording and the existing equality assertions to match. [Current resolver](/Users/lchingen/hivemind/src/hivemind/service.py:73).

CONSENSUS: yes
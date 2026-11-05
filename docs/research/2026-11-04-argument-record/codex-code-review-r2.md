Found **three issues**. Five first-round fixes hold; the provenance fix remains incomplete.

1. **[P2] A theme used in the judgement can still lose its version.** [judging.py:553](/Users/lchingen/hivemind/src/hivemind/views/judging.py:553) saves versions only for IDs appearing in card references, although design §3 requires every supplied dependency and theme. Reproduced: the request shows `v2` judgement 1; the answer weighs `v2` in `theme_pushes`, but its card cites only `e1`. The saved `read` is `{}`. **This partially reopens r1 #2.**

2. **[P2] Invalid and unbounded relay lists are accepted.** [judging.py:507](/Users/lchingen/hivemind/src/hivemind/views/judging.py:507) checks membership only. A claim with `refs=["e1"]` and `relays=["e1"]` passes, despite the schema defining a relay as repeating *another* reference. Repeating `"e1"` **1,000 times** also passes and is stored. This permits contradictory source information and defeats the card’s size bound.

3. **[P2] Preflight F misclassifies retired-version answers as failures.** [preflight.py:314](/Users/lchingen/hivemind/scripts/preflight.py:314) treats every non-card answer as v7. On the sealed v34 archive, it rejects **925/925 committed judgements** because `reference` and `implied_outcome` are missing—fields their original schema never requested. Unsupported versions need explicit accounting rather than v7 validation.

The nine card tests passed using in-memory databases. Write rollback, cached recovery and same-sequence resume also passed. Against `HEAD`, 77 v7 requests were byte-identical and 649 answer checks matched on the same stored states; this was not a full historical replay.

The requested full suite could not start because the sandbox has no writable temporary directory. No files were edited and no paid calls were made.


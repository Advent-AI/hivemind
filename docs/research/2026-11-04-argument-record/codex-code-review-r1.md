Found six issues; the first can stop a valid v8 round.

1. **[P1] A request can have no valid answer.** [judging.py:466](/Users/lchingen/hivemind/src/hivemind/views/judging.py:466) requires a nonempty card, and every claim requires a shown reference. After three v7 judgements with empty citations, old evidence can remain in force while v8 shows **zero references**. An empty card passes the schema but is refused twice; inventing a reference also fails. Reproduced in memory.

2. **[P2] Cards do not record which dependency or theme judgement they used.** [judging.py:522](/Users/lchingen/hivemind/src/hivemind/views/judging.py:522) stores bare IDs such as `v2`, without the referenced judgement ID. If `v2` changes later—or later in the same round—the card lacks the exact version required by design §§3 and 6. The request text also omits that ID. This is missing stored provenance, independently of the deferred UI work.

3. **[P2] Preflight can reject a correct historical answer.** [preflight.py:322](/Users/lchingen/hivemind/scripts/preflight.py:322) calls v7’s checker, which reads **current** dependencies. Reproduced: an accepted answer cites dependency `v3`; a later resolution changes the dependency to `v2`; F reports “v3 is not a dependency,” despite `v3` appearing in the stored request.

4. **[P2] Source counting rejects an answer the schema permits.** [judging.py:480](/Users/lchingen/hivemind/src/hivemind/views/judging.py:480) limits `independent_sources` to the number of references. A supplied theme conclusion can explicitly summarize two independent reports: `refs=["v2"], independent_sources=2` accurately describes that claim, but is refused. The schema counts original reports, not reference IDs; the design leaves source independence to the model.

5. **[P2] Removed claims have no enforced count or uniqueness limit.** [judging.py:487](/Users/lchingen/hivemind/src/hivemind/views/judging.py:487) validates entries individually. Repeating the same removed `k1` eleven times passes both checks and is stored successfully. Arbitrarily longer lists also pass, violating §4’s maximum of ten removals.

6. **[P2] Preflight silently omits unverifiable answers.** [preflight.py:305](/Users/lchingen/hivemind/scripts/preflight.py:305) only visits committed judgements. Refused or rolled-back answers receive no “unverifiable” count, contrary to §5. Reproduced with an archived answer lacking a committed judgement: F prints zero judged and zero refused, without accounting for it.

I found no v7 behavior change in the reviewed diff and targeted comparisons. Transaction rollback, cached resume and repeated execution at the same sequence worked in memory. All seven existing card tests passed using in-memory databases. The full suite could not start because the sandbox has no writable temporary directory. No files were edited and no paid calls were made.


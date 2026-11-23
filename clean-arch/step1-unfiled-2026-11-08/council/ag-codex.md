**I agree with the prompt changes and most of the protocol, with changes to recovery and acceptance.** The key distinction is that 50 consecutive July articles can test one forward sequence, but cannot establish performance across four months.

**Your items 1–6:** Accept 1–3 and 6. Your wording for 6 preserves Alex’s margin decision while making relevance, rather than period alone, the test. Accept 5, but also inspect collisions against source passages: reporting both scores does not establish which mapping is right.

Amend 4. An end-of-run retry is useful, but it does not implement the recorded retry on the next write or at run start. Preserve the original opening boundary when retrying, so later-arriving evidence is not accidentally treated as earlier evidence. Report pairs still pending. The recovery design is in [§11.1](/Users/lchingen/hivemind/clean-arch/STEP1-CONDITIONS-DESIGN.md:221); the present forward loop calls later linking only when a thesis opens ([compare.py:148](/Users/lchingen/hivemind/clean-arch/step2/compare.py:148)).

I accept retaining original-only search and later-link judgment for now. Their correctness is **conditional on the group actually being a repeat**. Check stored groups where a member adds a material detail the original lacks, and read false later-link decisions against the source; do not assume the comparator was always right.

**Acceptance population:** I accept the first 50 eligible consecutive articles as a practical, predeclared test of that July sequence, subject to verifying the pool and excluding **all articles used by any run**, not only dev and test. Fix a deterministic tie-break for equal timestamps. Do not claim it represents later months. A separate month-stratified study can wait; do not select articles for this acceptance by looking for likely repeats.

The proposed readers and empty-library start are sound. Add revisions to the search check, as the product must find earlier versions for revisions too. Two dossiers can test detail retention, but declare how they are chosen before seeing results and report the number of details judged; an empty or unexercised comparison cannot pass. If too few repeats, merges, or relevant dossiers occur, report that line as **unexercised**, not passed.

The proposed thesis threshold is **not yet agreed**. Ask Alex to set it before selection. Also predeclare treatment of failed articles, pending links, and reader disagreements; do not silently exclude them.

**Before freezing:** finish the whole-request audit; apply the agreed corrections; check unresolved links, quote/figure issues, mapping collisions and later-link misses on stored data; verify retry recovery and exact request bytes; then run the touched checks and required suite. Explain prompt growth in characters and tokens. Keep the exposed test results and the two D385 conflicts with frozen gold disclosed.

**AGREE WITH CHANGES:** recovery at the specified triggers; acceptance claims limited to the July sequence; revisions and unexercised lines reported; thesis threshold agreed before selection.
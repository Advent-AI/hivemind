**I would not close the lean path yet. D375 already states the next behavior Alex wants, and a $0 proof can establish what implementing it would actually change before anyone sends or adopts a new version.**

The RTX trace is substantially right. I checked the stored candidate and matching record: `v15` was compared with `v6` and the day-start questions, not `v14`. The candidate’s typed event kind matched `v6` and differed from `v14`, so the keyed path did not use the text-search fallback. If `v14` were in the shown-question list, the matcher would include it in the relation questions. What it would decide is still unknown. [Matcher](/Users/lchingen/hivemind/src/hivemind/views/jev_matching.py:221)

There is an additional useful fact: I checked the stored `v14` key against the `v15` candidate through `identity.conflicts`. Both merge checks return **false** for a conflict: the code treats policy-event type differences as potentially one process. That makes a stored-data proof meaningful. It does **not** prove the model or collision judge would merge the questions.

The trace needs these qualifications:

- The text search was run on the **stored end-state database**. Its ranking there does not prove what the search would have returned at article 175.
- The four-run figures are counts of recorded openings under the census’s filters. The JSON shows the totals, but I did not find the generating census script to verify its completeness. “Three not compared” is not a general duplicate rate.
- The two July pairs remain unreviewed; do not call them confirmed duplicates or assume their rulings share D354’s mechanism.
- Replace “the missing comparison **explains** one duplicate” with “one pair both reviewers called duplicate was opened without that comparison.” Comparison is necessary to the proposed route, but the unmade comparison’s result is unknown.
- The final “what this result shows” paragraph is stale: it says all pairs have the same band and calls one answer “less-informed.” The corrected earlier wording—two yes/yes pairs, two different revenue scales, and an observed association—is the accurate one.
- D517 did **not** show that every affordable comparison cannot decide. It stopped the proposed design because its reliability could not be defended from the available readings.

My selected next step is **one reviewed $0 design and deterministic proof of D375’s per-article visibility**, using the actual historical state and the production entry point. It should show:

1. The stored day-start control reproduces its request and matching list; the D375 version includes every eligible question committed before the article, including `v14`, without including later information.
2. On the stored RTX candidate, a **fake external comparison** returning “same question” reaches the real checks and writer, and a “different” control remains separate. This tests wiring and identity handling, not what Jev or the collision judge would actually decide.
3. The proof also covers an earlier same-day question that is genuinely distinct, a same-article pair, and recovery/order boundaries required by D375. Count which stored cases the new list touches; do not fit the change to RTX.

**Stop** if the historical state cannot be reconstructed, the existing checks do not behave as predicted, the changed list loses or adds ineligible questions, or the proof cannot exercise the real path without changing frozen files. A passing proof establishes only that the intended visibility and handling are wired; it does not establish reader benefit, justify adoption, or make the RTX duplicate disappear in a real model call. A new version and any paid measurement return to the council separately.

This outranks the proposed package-and-stop because D375 is **already Alex’s decision**, not an open product choice. Its implementation and acceptance are pending. The package should say that, rather than ask him whether to build it again. The other items remain open, but should not all be framed as choices needing a fresh answer: D505 remains his decision for the new system; the later-linking gap remains paused and is specifically about groups whose **original** statement arrived linked; and the two compared July pairs are not yet confirmed duplicates. [D375](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4034)

Council position: Correct the trace’s scope and stale wording; do not declare the comparison impossible or close the path. Prepare and review a bounded $0 D375 visibility proof with real entry points and fake external comparisons, then return its result to the council before any frozen-piece change or paid send.
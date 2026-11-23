**Build a reader test first.** Keep every repeat’s text and source, then check whether people actually notice details such as “guidance assumes no China revenue” when reading a group.

### 1. Group contract

A group keeps the original record’s ID and unchanged original fields. Each incoming item keeps its own stable ID, text, fields and source inside that group. Thesis links attach to the group, with the contributing member recorded so their basis remains visible. Revisions are links between groups; they do not replace either group.

| Event | Write |
|---|---|
| New | Create a group with the incoming item as its original; save its source and thesis links. |
| Repeat of one group | Add the item as a member, its source, and missing thesis links. |
| Repeat of several groups | **Do not choose or combine groups automatically.** Record the conflicting comparison and leave the item pending for resolution. |
| Revision | Create a group for the item and link it as a revision of each identified earlier group. |
| Repeat of one group and revision of another | Add the item to the repeat group; link that group to the other as a revision, retaining which member established the link. |
| Failed comparison | Record the failure and leave the item pending; do not call it new or partially save it as a repeat. |
| Two items from one article match one group | Keep both distinct members and their passages; count the article once as a source. |
| Same item replayed | Use its stable item ID to find the existing member; add any missing link once, without adding another member or source. |
| Missing thesis link | Add the link once, with the member that supports it. |
| Crash midway | Save the item, membership, sources and links in one transaction. A retry either sees the completed write or safely performs it once. |

Several matches may mean that earlier groups should be combined, or that one comparison is wrong. Putting the item into all of them duplicates it and may spread a false link. The pending rule is my **proposal**, not Alex’s confirmed decision; how conflicts get resolved remains open.

### 2. Search and comparison

For the first test, reconstruct the existing forward decisions against their original anchor texts. This makes the three dossier versions comparable without inventing new Jev decisions.

For a future live path, **propose searching members as well as anchors**, returning groups rather than letting 14 members occupy 14 search slots. Show Jev the anchor and matched member, with their source and date. A match to a member does not itself prove the incoming item matches the anchor: additions and wrong earlier grouping can make the chain drift. This search and comparison design needs its own evaluation; it is not established by the existing simulation.

### 3. What the reader sees

Show one group as a unit, with the original first and every member’s own text, fields and source visible below it in arrival order. Mark revisions and retain their earlier text. Show the number of **distinct articles**, not the number of members, and identify known speakers or original sources. Do not describe articles as independent confirmations unless their independence is established. A wrong group must remain readable as its separate statements, not as a rewritten combined claim.

### 4. Cheapest reader test

Use the fixed dossiers: clean-1; clean-18 and clean-24; clean-11 and clean-17, including Kyber’s 14-member group. Create three views from the same stored history: source-only, grouped, and unmerged full information. Preserve the actual wrong groups in the simulation.

Before exposing readers to the views, two independent readers inspect the underlying articles and records and agree on a source-cited answer key. Fix questions on: material conditions and figures; who said what and when; whether reports establish independent sources; revisions; and whether apparently grouped statements actually differ. Include the known guidance, financial-results and Taiwan-raid details wherever they occur in these dossiers. Record disagreements in the key.

Use independent readers who did not build the views. Mask view labels and balance dossier/view assignments and order across readers; a reader sees only one version of a dossier. Ask for answers with citations and confidence, plus reading time. Score each predeclared fact, attribution, revision and independence judgment against the same key; separately count unsupported claims and double-counting. Report every question and disagreement, not just an aggregate.

**Proposed budget:** cap the grouped view at twice the unmerged view’s text size and record actual characters and reading time, including Kyber. This is a trial budget, not an accepted product limit.

Grouping fails this test if readers miss material details source-only readers miss, introduce more unsupported or double-counted claims, or cannot identify a known wrong grouping; compare all three views and disclose small-sample uncertainty. The unmerged control shows what the same readers can recover with full information, not what an undefined Step 4 would do.

### 5. Build now

In an isolated test path, have **one writer** reconstruct the three views from stored records and decisions. Test it with real stored items: original unchanged, all member fields retained, distinct article counts, thesis links and replay without duplication. Then run the blind reader test. Do not build a live group writer, new search behavior or a judgement interface before those results and the unresolved multi-match rule are settled.

This is an independent, read-only design; no files or production configuration were changed.


# Claude's independent design, grouping round (written before reading Codex's)

## Census, forward simulation, $0

- 282 items made 180 records. Group sizes:
  - 138 records stand alone;
  - 20 have 2 members, 6 have 3, 7 have 4;
  - one each has 5, 6, 9, 11, 12 or 14, and 3 have 7.
- 15 items matched more than one record. 16 merged items also had a revision answer from another candidate.
- 4 records hold more than one member from the same article.
- Size per dossier, as characters of summary and passages:

| Dossier | No merging | Source only | Grouped (member summaries; an item matching several records copied into each) |
|---|---|---|---|
| clean-1 | 35.9k | 13.9k | 26.2k |
| clean-11 | 25.9k | 18.6k | **30.8k** |
| clean-17 | 22.0k | 4.6k | 14.3k |

- clean-11 grouped is larger than no merging, because a member placed in several groups is copied into each. "Join every match"
  therefore double-counts by construction.

## 1. Group contract

A group is one stored statement.
- **Anchor:** the first record. It is never rewritten. Its id is the group's id, and the group is what the library and search address.
- **Members:** the later records judged repeats. Each keeps its own id (the item key), summary, passages, party, speaker, dates, tier and
  source article.
- **Thesis links:** the union over anchor and members, each link remembering which member brought it.
- **Revision links:** to other groups.

Identity: the anchor's id never changes. Membership only grows, and a member is never moved by the writer (D202 spirit: the writer never
deletes or merges).

| Event | What is written |
|---|---|
| New | A group with an anchor only. |
| Repeat of one group | A member is added. Missing thesis links are added with their provenance. |
| Repeat of several groups | **Best match only**: the member joins the group with the highest Jev same_statement probability; ties go to the earliest group. The other groups get an `also_matches` reference (visible, not counted). |
| Revision of a group | A new group, with a `revises` link to the matched group. |
| Repeat of one group and revision of another | Repeat takes precedence: join the repeat group and record the `revises` link to the other group. |
| Comparison failed (Jev error or invalid answer) | Nothing is written. The item is reported as failed with its reason, never silently saved as new. |
| Two items of one article match the same group | Both are added as members. The source count counts distinct articles, so the group shows one more article, not two. |
| The same item replayed | Nothing is written: member ids are unique and the replay is detected. |
| Missing thesis link | Added to the group with its provenance (the member that brought it). |
| Crash midway | Each item's writes are applied as one unit. On restart the item is replayed; the replay rule makes this safe. |

## 2. What search and Jev compare against

Keep the anchor only (measured: 112/113 found). A cheap arm, $0 because the embeddings are cached: search over member texts too,
mapping a hit to its group. Jev keeps comparing against the anchor. The first group statement is the identity, and drift through
members (A≈B, B≈C, A≉C) is the chain risk Codex named.

## 3. Dossier view of a group

- Anchor block: summary, passages, party, speaker, date and tier.
- Then "Later reports of the same statement (N articles from M outlets; reports are not independent confirmation unless a different
  original party says so)", with each member's date, outlet, party if different, and summary, oldest first.
- `revises` and `also_matches` shown as links.

## 4. Test, $0 in models plus Codex readers

- **Arms:** three forms of each predeclared dossier, built by code from `forward-sim.json` with the best-match rule:
  - NONE: every item an entry;
  - SOURCE: anchor plus a source list;
  - GROUP.
- **Questions, fixed before any reader sees a dossier,** from the stored items only:
  - detail questions, one per fact held only by a later retelling on these theses. Taken from the loss readers' "lost, not held
    elsewhere" lists, confirmed by me against the passages, and filtered to material or moderate;
  - control questions on facts in the anchors;
  - counting questions: "how many distinct statements bear on X", "is X confirmed by its original party";
  - one wrong-group question per known wrong merge in these dossiers (NVL576 inside the NVL144 group).
- **Readers:** two blind readers per form per dossier. Each reader sees one form only, so the forms do not contaminate each other, and
  answers from the dossier only.
- **Answer key:** written from the items before any reader runs.
- **Score:** detail recall, control accuracy, counting accuracy, wrong-group misled yes or no, and characters.
- **Falsifiers:**
  - GROUP's detail recall clearly below NONE, meaning a preserved detail is not noticed;
  - GROUP counts worse than SOURCE;
  - the Kyber group unreadable: detail recall in clean-17 below NONE.

## 5. Build now

A clean Step 3 library module (`clean-arch/step3/library.py`) owning the contract in §1: groups, members, links, the multi-match rule,
replay safety and failure refusal. It has tests per table row, against real records from `items.json`. The forward simulation and the
dossier renderer use it, and the renderer is part of the module. This is a logical store; the PRD leaves physical storage open. Nothing
here depends on the test's outcome except the presentation.

**Uncertain:** whether the best-match probability is calibrated; whether member-text search helps; whether a reader proxy says
anything about the eventual Step 4.

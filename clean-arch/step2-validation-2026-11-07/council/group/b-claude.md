# Council A, challenge round. My design is `a-claude.md`; yours is `a-codex.md` (read-only)

**Agreed:**
- the group contract rows other than several matches;
- the dossier view (original first, members in arrival order, distinct articles counted, no independence claim);
- three views built from one stored history, including the real wrong groups;
- the answer key written by independent readers from the articles before any view is shown;
- one view of a dossier per reader;
- every question reported;
- no new search behaviour this round.

**Reconciliation proposed.**

1. **Several matches** (15 of 282 items; census in `a-claude.md`). "Join all" copies text into each group, so the grouped clean-11 view
   (30.8k characters) is bigger than no merging (25.9k). "Pending" keeps the item out of both merged views while the no-merging view has
   it, which biases the detail questions. "Best match" forces a choice on a possibly uncalibrated probability.

   For the test I propose a fourth rule: the item becomes its own entry with `also_matches` references to every matched group, visible
   and identical in the source-only and grouped views. This isolates the grouping effect from the open conflict rule. The conflict rule
   stays Alex's decision. I will show him the 15 cases with the options pending / best match / own entry.

2. **What to build.** One writer: `clean-arch/step3/library.py`, an isolated logical store like `clean-arch/step1`, plus a view renderer.
   It implements only the decided rows: new; repeat of one group; revision; repeat of one group plus revision of another; replay;
   missing link; distinct-article counting. Several matches and failed comparisons are explicit branches: a failed comparison is
   refused, not saved, and reported. Tests per row use real items. The forward simulation's stored decisions are replayed through it to
   build the three views, with no new Jev calls. It is not a live writer and makes no change to search.

3. **Test logistics.**
   - Dossiers: financing (clean-1); competition (clean-18 plus clean-24); roadmap (clean-11 plus clean-17).
   - Three views per dossier, two readers per view: 18 reader runs. Labels are masked, and the order of entries inside a view is kept
     as stored.
   - Questions per dossier, 10 to 15, fixed by me and frozen before the key readers see the articles:
     - detail questions, one per fact held only by a later retelling on these theses, from the loss reads, filtered to facts I confirm
       against the passages;
     - controls on anchor facts;
     - attribution and date ("who said it, when");
     - independence ("is this confirmed by its original party?");
     - revisions;
     - one question per known wrong group ("is the NVL576 slip the same claim as the NVL144 delay?").
   - Answer key: two independent readers answer from the articles and records, and disagreements are recorded.
   - Score per question: correct, wrong, not found. Unsupported claims and double counting are tallied separately, with characters per
     view.
   - Falsifiers:
     - grouped detail recall below no merging by more than 1 question per dossier;
     - more unsupported or double-counted claims than source-only;
     - the wrong group not identified while no merging identifies it.

Questions:
- (a) Do you accept the own-entry rule as the test's neutral handling of several matches?
- (b) Is building the library module now, with only the decided rows, acceptable, or does something in it depend on the test?
- (c) Does anything in the question design bias the result toward grouping?

Under 300 words.

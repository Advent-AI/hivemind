# Stage 0, step 1: classify the old-system replay folders BEFORE any article hit is read (read-only, $0)

D667 (in `/Users/lchingen/hivemind/docs/DECISIONS-log.md`, search "## D667 ") and plan §1.2 item 4 (`../RUN-PLAN-v9.md`) exempt an
old-system replay folder and its byte copies "only when its decision record or run note shows it ran the then-production configuration as
the product (its library sealed or served as the product's), and no decision cites one of its articles as a case behind a change.
Development replays (arms, probes, configuration trials, week tests) are reads, and so is any research artifact built from an exempt run."
Classification is frozen per folder before any hit is read.

**Do not search any file for article ids.** That is the census, which comes after this classification. Read decision records and run notes
only.

## The folders whose replayed days reach the scored span (2026-07-20 to 09-20)

Each folder is listed with its replayed day span (from its `replay.log` day lines) and its configuration. The span 02-25 to 08-15 is the
earlier `items-window` corpus.

**Configuration trials, arms and week or day tests.** These look like development by name and configuration. Confirm or dispute.
- `poc/data/english-2026-10-25`: poc-v17, to 08-05.
- `english-groups*`, `english-jev*`, `english-v23-jev`, `english-v23-llm`, `english-v25-admission*`, `english-v26-collision-r4` and
  `english-v29-theme-r5`: v20 to v29, to between 07-23 and 08-15.
- `pinned-shared-2026-10-27/arm-v29-shared`: to 08-15.
- `old-2026-10-23-run1`, `run2` and `run3b`: poc-v1 and poc-v2, to 07-24, 07-30 and 07-23.
- In the worktree `/Users/lchingen/hivemind-no-preseed-evidence-review`: `poc/data/split-v3-prod-0829-0830*` (08-29 to 08-30) and
  `v117-one-day-smoke-2026-11-05` (08-29).

**run3 family** (poc-v2, the `items-window` corpus, 02-25 to 08-15):
- the root `poc/data/replay.log`;
- `old-2026-10-23-run3c` (to 07-24);
- `sealed-2026-10-24-run3-through-0728` and `-through-0815`.

Record: D63 (re-judging once a day, from the run's cost; results through 07-28 sealed).

**The two three-month runs on the current corpus** (these decide the scored span):
- **`english-v29-nvda-3m-2026-10-27`** (poc-v29, replayed 07-01 to 08-24).
  - Record D199: "the poc-v29/v30 run stays paused and untouched". Its 493 empty extraction answers in 1,553 calls (32%; 65% of the first
    week's items) led to extraction v16.
  - Check whether a served library was built from it: see `service-3m-2026-10-27` and the README or CURRENT_STATE history.
- **`english-v34-nvda-3m-2026-10-28`**, with its sealed and served byte copies (poc-v34, replayed 07-01 to 08-28).
  - Record D205: the judging output cap doubled after one judgement of thesis v10 hit the cap.
  - Record D206 (as carried in D358): sealed and served to the front end as the product's library. It diagnosed evidence bloat, removed
    v68's rows from the served copy, and changed the writer to store each cited id once (from judgement 736).
  - Also built from it: the research in `docs/research/2026-10-28-quality-review/`.
- `english-v32-nvda-3m-2026-10-27` replayed only within the warm-up; it is not in scope.

## What to decide

1. For each folder or family: **exempt** or **read**, with the record line you rely on.
2. **The reading of the condition.** "No decision cites one of its articles as a case behind a change" can be read two ways:
   - **(a) Folder level:** if any decision used the run's traces or articles to justify any change, the whole folder is a read.
   - **(b) Article level:** the folder's own replay is exempt, and an article is a read only when a decision or a research artifact uses
     that article.

   Which is faithful to D665's "unread weeks … as far as the full exposure census supports" and to D667's purpose (a replay of the product
   as it ran tunes neither system)? Argue it on the records above, and on the risk that an article informs tuning without being named.
3. Say what each reading means for the scored span, by date only (no hits):
   - v29-3m and v34-3m as reads exclude whatever they read up to 08-24 and 08-28;
   - as exempt, those days stay, less the other reads.

End with one JSON object per folder or family: `{"folder": "...", "class": "exempt|read", "reason": "<= 40 words", "record": "..."}`, then
your choice of reading (a) or (b) with a reason under 80 words. Under about 700 words in all.

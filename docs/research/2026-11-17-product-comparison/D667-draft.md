## D667 · 2026-11-17 · Under D666 and D439 (council, run-plan rounds 1–10): the release comparison's run plan and the rules it takes for this run

- **Council:** `docs/research/2026-11-17-product-comparison/`: `RUN-PLAN-v1.md` … `RUN-PLAN-v9.md`, `review-codex-1..10.md` (thread
  01a1ebfe-4f67-7c72-af87-7830055e0f09, memories off), a fresh Claude reviewer each round (READY at v7), and `ROUND-LOG.md` (what each round
  taught).
- **Decided**, for this comparison only; D665's rule is unchanged:
  1. **The plan** is `RUN-PLAN.md` v9, frozen as `RUN-PLAN-v9.md`. Build-level checks run at the stage-0 freeze review
     (`freeze-review-notes.md`), which gates the first paid send.
  2. **Exposure.**
     - Plan §1.2 governs the whole census: the closed set of read kinds, the search roots and every exclusion. Any read excludes an article.
     - **Not reads,** and only these:
       - the search index built over the whole corpus;
       - this comparison's own files (its census, reader packets and outputs are not prior exposure);
       - **An old-system replay folder and its byte copies.** Only when its decision record or run note shows it ran the then-production
         configuration as the product (its library sealed or served as the product's), and no decision cites one of its articles as a case
         behind a change. Development replays (arms, probes, configuration trials, week tests) are reads, and so is any research artifact
         built from an exempt run. Classified per folder in `replay-folders.json` before any hit is read.
       - **Stored rows that are verified raw copies of a corpus build** listed in `corpus-builds.json` (the same rows by `input_id` and
         `content_sha256`). Whatever a probe, run or fixture actually used is still a read through its trace, packet or fixture text.
     - D613's "unread" was a Step 1 census; this is the full census D665 asks for.
  3. **The company's own figures** (D505's list) count in N, as D665 says. Their subgroup is flagged blind at the census and printed beside
     the verdict. The new system does not open such questions by D505, and Alex sees how much of any gap that makes (D431 compares the
     products as configured).
  4. **One ledger per draw.**
     - Absolute guards: $65 per new-system draw and $25 per old-system draw, $270 in all. They are stops, not a budget (D664).
     - For this run, this replaces D449's whole-run stop across draws and D666's single $250 ledger. D449's one redo within a draw is
       unchanged.
  5. **D431's "same day," for a run longer than one day.** A new-system draw takes about 20 h, so one calendar day cannot hold it.
     - The six counted draws are launched within one hour of each other and run concurrently.
     - A redo within a draw counts as part of that draw.
     - Every counted send falls within 72 h of the first launch.
     - A breach makes the result a diagnostic.
     - This replaces, for this run only, the one-calendar-day reading in `WIRING-DESIGN.md`.
  6. **No replacement draw counts.** A draw that cannot finish gives no release verdict; what finished goes to Alex as a diagnostic. The
     reviewers read "same day" differently, so the council took the cheaper, reversible course (D439).
  7. **The credit and scoring rules** are plan §1.4:
     - one cutoff, the span's last day;
     - "covers" in A2's form, blind;
     - the earlier-opened question of a same-bet pair is the original;
     - distinct bets for the 30-question minimum;
     - D428's decided-only guardrail shares;
     - splits resolved per counting to a mark the readers gave;
     - an unexercised subgroup blocks only a lead;
     - the verdicts tested in order: invalid, too small, lead, loss, no winner.
  8. **Step 2's three lines** (D427) are hard checks, each decided on its point estimate over frozen samples: 100 records, 200 merges, 30
     groups. A line with too few cases is not measured and cannot clear release.
  9. **Two proposed floors** (wrong citations, answer-changing omissions) are printed as not measured. Measuring them needs source-first
     readings outside this comparison.
- **Out of scope during the run** (to `FINDINGS.md`): D662's holds, D658, and any fix, except a launcher-only repair after a failed slice,
  followed by a slice rerun (plan §2).
- **Back to Alex:**
  - the verdict, or a diagnostic;
  - N < 20 at the census;
  - a stop that is not a wiring fault;
  - a guard reached;
  - a failed hard check;
  - no verdict by 2026-12-01.

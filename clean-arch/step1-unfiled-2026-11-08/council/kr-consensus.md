# Council kr: where the clean path stands; the consensus (2026-11-12)

Alex: "你能先准备搞一个段落让整个council看一下你的过去跑的整体进度和反馈结果吗？我们到底做到哪里了". The summary
(`clean-arch/step4-2026-11-10/PROGRESS-2026-11-12.md`) was read cold by two independent members (Codex `kr-codex.md`; a Claude
Opus reader, its report kept below in substance), each checking it against the record. Every claim below that changes the
summary was checked by me against its source before it was written here.

## Corrections to the summary, checked
- **The Stage A table was simplified to the strict reading.** On "both first readers fail": run 1 missed lines 3, 4 and 6; run
  2 met line 4 (0 of 16) and missed 3 and 6; run 3 went back on lines 1 and 2 (0 to 1 each) and met 6; run 4 missed 3 and 4.
  Line 3 fell from 7 failures to 1 (result pages' line tables).
- **The seeded end-to-end result is INCONCLUSIVE under its frozen rule** (q12 0 of 3), conditional on the supplied questions,
  on articles c8 was tuned on (115 of 243), with an exploratory threshold (round log §63). Not "ahead of production".
- **Unseeded over all questions: 6, 5, 5 against seeded 18, 18, 17**, most of it company-figure questions the product does not
  open (D370; round log, unseeded result). The 4.0 against 6.33 is a different-day, exploratory comparison.
- **The remaining ladder faults are not scattered:** five of the six answers behind lines 1, 3 and 4 sit on theses whose
  outcome names two things or two periods (result-4).
- **Baseline:** 16 question paths of 8 distinct questions; three paths carry every fault; 7 INSUFFICIENT and 1 unresolved
  beside the 151 decided. (The Claude reader said 7 distinct; the paths name 8.)
- **Line 6 of Stage A is met by construction** once code sets the due day (D414): agreement, not correctness of the day.
- **Housekeeping found stale:** the status page's headline, its line saying the adapter mode is not built, PRD §7's Step 4
  paragraph; all Step 4 work since D396 is uncommitted (272 untracked paths; last commit f1d9ab2).

## Weaker than it looks (agreed)
The baseline's 159 judgements are 16 correlated paths; 0 of 16 unsupported last judgements is consistent with up to about
17%. Reader agreement is not calibration; no control is known to be sound. Stage B's lines 4 and 5 test whether the judge
follows its own rules, not whether it is right; line 3 is the only gold check, and a rewritten question makes a control
ineligible rather than wrong; line 2 counts only theses that got a ladder, so the eight declines cannot fail it.

## Lessons at the level of mechanism (agreed)
- **What worked:** moving a decision out of the model into code or a typed field (due day by code: 18 of 34 to 33 of 33; the
  tie rule; three outcomes and a typed ruling out: event faults 7 to 1); small sends with pass and fail written first (the
  second look settled for $0.12); $0 replays that predicted runs.
- **What failed:** extra sentences, and asking the model to check itself.
- **What slowed it:** reviewing imagined behaviour before observing the model (about 30 design versions and 60 reviewer
  sessions before a six-thesis probe found three classes the reviews had missed); reviews with no budget (findings per round
  stayed near 10 to 15); a design page of 164 KB too large to review whole; tuning the same 44 theses class by class.

## The next step and the largest gap (agreed, with one difference)
- **Next:** finish Stage B (approved, cheap, prepared). It answers one question: when a question exists, does the real judge
  answer it defensibly? Its pass would not close the opening gap or the failed Stage A lines.
- **The largest demonstrated product gap is upstream: how Step 1 cuts a matter into theses** (one quantity, one period, one
  question a year, D38). It explains all nine misses of the unseeded graded questions (a second year never opened; memory in
  the wrong shape; a check date; Ohio folded into a broader thesis), five of six remaining Stage A faults, three of the 16
  Stage B controls already ineligible, and part of the eight declines (both memory theses). Diagnose source by source, then
  one change as a new Step 1 version, measured on fresh articles.
- **Difference:** the Claude reader would send Stage B with no further review; the Codex reader holds D429's condition (a
  review that finds nothing serious). D429 is Alex's words and stands: one more review, then the send.

## For Alex to decide (agreed)
1. **The end-to-end yardstick for D427.** Against the seeded configuration the clean path loses about 11 questions a draw by
   construction (company figures it does not open). D370 made production unseeded too, so "current production" is the same-
   condition comparator; whether D427 means that, and which questions count, is his.
2. **Whether a Stage B pass counts as "Step 4 meets its lines"** (D427), with Stage A unmet: after Stage B's result.
3. **After Stage B, the thesis-cutting work** (above) as the next phase.

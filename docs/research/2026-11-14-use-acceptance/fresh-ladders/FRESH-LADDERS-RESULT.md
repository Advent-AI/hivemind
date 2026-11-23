# The new system's answer choices in the fresh week, read against the six lines and traced to the judge (D544), 2026-11-15, $0

What was read: the 21 stored attempts of the step that writes a question's answer choices (seven questions the first step
opened in the fresh week of 2026-09-22 to 09-28, three attempts each; `poc/data/clean-lean-week-2026-11-14/week-r2/c1/ladder/`),
through the existing packet builder and reading form of Stage A (`clean-arch/step4-2026-11-10/stage_a/build_reader_packets.py`,
`ladder/stage-a-reader-brief.md`). Two readings made apart: Claude's own, written first (`own-marks-before-the-reader.json`), and a
fresh Codex session given only the form, the packet and the list of themes (`codex-reader.jsonl`; `key.json` maps items to
attempts). Then each question traced into the judge's stored judgements. No model was asked anything new; nothing changed. The
judge used the first attempt of each question. Seven questions are a diagnostic sample: this passes or fails no gate.

## The answer

**By the lines, the fresh week's answer choices are mostly sound, with one fault both readers found apart on three questions.
The larger fault is one the lines cannot see: two of the seven questions sat on their top range from the first or second day.**

## 1. Against the six lines

| Line (D400) | Both readers, apart | One reader only |
|---|---|---|
| 1. no question other than the thesis's | none fails (21 of 21) | |
| 2. no part left unlisted | **6 attempts on 3 questions fail, the same six in both readings**: a clause of the thesis's wording that the question leaves out is listed in one attempt and not in another (Blackwell to China: "so that China data-center revenue can resume", attempts 1 and 3; the cloud companies' spending: "compared with the nearly $800 billion", attempts 1 and 2; the Chinese permission: "versus blocking, delaying or capping quantities", attempts 1 and 3) | the Hugging Face closing, attempt 3: "repriced" not named (Codex fails it; Claude took the listed price to cover it) |
| 3. every outcome has exactly one range | none fails in both | Codex fails two single attempts (a "will not be reached" announcement read as a forecast, not a decision; "rejects all plans submitted so far" not ruling out a later plan) |
| 4. no unjustified refusal | no refusal in 21 attempts | |
| 5. right in two of three attempts | by Claude's marks 4 of 7 questions (the three with the fault of line 2 are right in one attempt of three) | by Codex's marks 1 of 7, because of the due-day reading below |
| 6. the same favourable end and due day in all three | holds for all seven (the cloud-spending question's ranges differ between attempts: 700/775/825/900 against 600/750/850/1,000 billion) | |

A disagreement on a rule, not on the step: Codex fails the due day of the two commitment questions (April 1, 2027, the day code
sets 60 days after the fiscal year-end, against "the next annual report, expected around February 2027") and of the Hugging Face
question (March 24, 2028, the check date the first step wrote, against "an obligation already taken on is due at its next annual
filing"). Claude holds both by the form's words (code's day where no day is stated; the thesis gives the check date). The second
is the first step's choice of period, not this step's.

## 2. Traced to the judge: two amount questions that opened with no figure

Both readers marked the ranges of the two commitment questions "not assessable": their opening articles state no amount, so the
step wrote ranges of its own ("no reference figure when the question opened").

| Question | Ranges the step wrote | What the judge was shown | The judge's answer, day by day |
|---|---|---|---|
| total of credit support and revenue guarantees (new system) | below 10 / 10 to 25 / 25 to 50 / 50 to 100 / **100 billion or more** | a disclosed maximum guarantee exposure of $105 billion on the first day, $108.5 billion later | the top range on all seven days |
| purchase and supply commitments (new system) | below 50 / 50 to 100 / 100 to 150 / 150 to 200 / **200 billion or more** | "current supply commitments of $279bn" from the second day | the middle range on the first day, the top range on the other six |
| financing commitments (old system, the same week, for comparison) | below 1 / 1 to 5 / 5 to 10 / 10 to 25 / **25 billion or more** | the same $105 billion | the top range on all seven days |

The top range is what the filed amounts point to, and it cannot tell amounts above its boundary apart: whether the total turns
out to be $105 billion or five times that, the answer is the same range. (Corrected after the council's check: "the answers are
supported" was too strong. In the week's reading one reader family called the new system's credit-support answer unsupported
and the old system's financing answer too little to prefer a range, partly because a maximum exposure is not the amount that
will be reported. And the records show ranges set without a reference and later exceeded; they do not prove that the missing
opening figure is the only cause of ranges this low.) The six lines pass these ladders (every outcome has one range), and the
reading form marks their ranges "not assessable". The mechanism is shared by both systems: ranges are written once, when the
question opens, from the opening article alone; an article that names the matter without its size leaves the ranges to a guess
that the first disclosed amount then overruns.

## 3. The census the council asked for (D545): every amount question of the stored runs, both systems, $0

`range_census.py` (`range-census-sheet.json`: ranges, answers day by day, the amount statements the judge cited on end-range days,
the amounts in the opening article) and Claude's reading of each question (`range-census-reading.json`). The fresh week and the
three July runs of each system: **49 amount questions** (one two-stage question on an approval process set aside), 366 judged days.

| Opening article | Questions | With at least one day on an end range | Days on an end range |
|---|---|---|---|
| gives a comparable amount (the ranges are placed on it) | 37 (new 10, old 27) | 4 (new 0, old 4) | 20 of 255 |
| gives none (the ranges are the step's own) | 12 (new 8, old 4), on 5 matters | 9 (new 5, old 4) | 56 of 111 |

The twelve by matter: the total of credit support and guarantees (one question in each of the eight runs: seven of the eight sat
on the top range, for 5 to 8 days each); purchase and supply commitments in the fresh week (6 of 7 days; in July the same
matter opened from an article that gave the amount last reported, $119 billion, and never left its middle ranges); DRAM contract
prices for 2026 (2 of 8 days); DRAM and HBM prices for 2027 and a GPU-hour spot price (no end-range day).

What carried each answer past the last boundary, read from the judge's reasons and the statements it cited:

| What it was | Questions |
|---|---|
| a filed amount comparable with the question (the same quantity) | 2: purchase commitments ($279 billion at the end of the second quarter); one July credit-support question whose top boundary was $5 billion (two disclosed amounts, $4.88 and $3.5 billion) |
| a maximum exposure, not the amount that will be reported | 2: the fresh week's credit-support questions of both systems |
| the judge's own scaling of one disclosed backstop to another project (the defect of the judge already on record, D519) | 5: the July credit-support questions, one of them opened from an article with two partial amounts |
| figures of another measure (quarterly rises against a year's change) | 1: DRAM prices |
| not this mechanism (the ranges were placed on a figure; the judge's own projection crossed a boundary for a few days, or it took the bottom range for want of sized evidence) | 3 of the old system's July questions |

Two things the table does not show. The same matter was given very different ranges from run to run when no figure placed
them: the top boundary of the credit-support question was 5, 10, 10, 20, 25, 25, 50 and 100 billion in the eight runs
(corrected by the council's check of the sheet). And in every
candidate the end range hides what the question was opened to track (how large the support, the commitments or the price move
becomes).

The classification of what each figure means is one reader's (Claude's), checked by the council against the sheet for
identities and counts only; the sheet lists selected statements and shortened reasons, a starting point for checking a case, not
everything the judge received. The counts repeat the same matters across runs: they describe these runs and are not a rate.

**By the trigger agreed before the census: no general design is opened on this evidence (D546).** Beyond the two matters of the
examples, one further matter shows the pattern (DRAM prices), and its figures are not comparable; the rule asked for three. The
association is strong (9 of 12 against 4 of 37) and narrow: twelve questions on five matters, one matter in every run. The
three observed examples stay recorded as defects, and most of the July cases are the judge's own scaling, a defect already on
record.

## 4. What this may and may not be said to show

- Shown, on seven questions of one week: the fault of line 2 recurs in the same form on three questions and was found by two
  readings made apart; two of the seven questions (and one of the old system's) were answered at an end range from the start
  because their ranges were written without a figure.
- Not shown: a rate; that either fault changes what a reader would decide; that a change would mend either (the "second look"
  that re-read answers mended 6 of 18 faults and damaged 3 of 30 sound answers, D422, D425); anything about Stage A or Stage B,
  which this sample neither passes nor fails.

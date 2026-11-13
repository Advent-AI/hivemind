# Council gk: the $0 results since gj, and a revised contract (read-only; do not edit files or run model calls)

## New evidence ($0; every number has a script or a file)

**1. E3's cheapest proof, run** (`clean-arch/step4-2026-11-10/census/production_ladders.py`, output `production_ladders.txt`): every
candidate ladder the frozen v74i wrote in the three same-day control draws of 2026-11-09 (729 stored extraction answers).

| | count |
|---|---|
| candidate ladders | 36 (14 yes/no, 22 five-rung) |
| refused by `check_ladder` | 0 |
| refused by `check_bounds` | 1 |
| refused by the split's `empty_rung` | 0 |
| refused by the split's `band_problem` | 0 |

The checks pass almost everything. The ladders are not stable. One question ("What total amount of financing commitments and
capacity backstops … will NVIDIA report outstanding at its FY2027 year-end?") was laddered 12 times:
- Strongly bullish holds the lowest band in 10 writes and the highest band in 2 (control d1 call 460, d4 call 12);
- the Neutral band is $1–5bn, $2–3bn, $2–6bn, $3–6bn, $5–10bn (five times) or $10–20bn.
The purchase-commitments ladder has Neutral at $50–75bn in d1 (call 878) and $100–119bn in d4 (call 949); the article states $119bn.
In production these candidates mostly folded into a seeded question with a reviewed ladder. On the clean path the first write is the
ladder for the life of the thesis (D38).

**2. First blind census reader (Codex family; the Claude reader is still reading; a third reader decides disagreements):**
`census/reader-codex.jsonl`, tallied by `census/tally.py`. Of 34 theses:
- several things 16, of which one ladder "drops a part" 13 and "no single ladder keeps the question" 3 (u1 clean-5, u2 clean-10, u3
  clean-10: memory and HBM);
- ladder type: number 18, yes/no 11, several states of one thing 5;
- due day: stated 4, a period end 4, an expected publication 17, none 9 (mostly "late January 2027", which production's
  `universe.fiscal_period` turns into 2027-01-31);
- asset 19, theme 15;
- of the 18 number questions, 9 have no reference figure in the opening article; all 6 asset number questions have an unclear
  favourable end.
c8's own rule is "A thesis asks one quantity for one period, or one event" (`arms/c8-system.txt`); the bundling is in `description`,
while `outcome` usually names one thing.

**3. Two facts for the writer mapping.**
- `judging.themes_shown_in` reads theme ids with `^- (v\d+) \(` and `evidence_shown_in` with `^- (e\d+) \[`
  (`src/hivemind/views/judging.py` lines 182–191). A theme view stored as `clean-4` would never be found, so every `theme_pushes`
  entry naming it would be refused. View ids on the judging side must be `v<N>`.
- Production already answers "which object": the request's [Subjects] block says "about a theme, choose an id from this list, or
  state what the matter is when none fits" with `universe.theme_list()` (twelve themes in `poc/universe.json`), and code resolves it
  (`universe.resolve`, `universe.kind`); `universe.fiscal_note` gives the fiscal-year line.

## My reading (challenge it)

1. The original design's premise, "reuse production's frozen ladder rules and code checks", does not hold a ladder still. The frozen
   sentences give a different yardstick on each send, and no check sees it. Falsifier: show that the 12 writes differ because the
   articles differed in the reference they stated.
2. The levers that have worked in this project are a required field that forces the decision and a code check where code can hold it,
   not a sentence (round log §§53–58; skill §4). So the ladder step should carry D186 now, as the split built it: the model states
   `favourable_end`; code orders and labels the rungs and renders each numeric condition from its bounds (`split.ordered_ladder`,
   `render`, `empty_rung`). That is also Alex's standing decision for the next version that writes ladders (D368 item 1).
3. Your objection to "pick one and keep the rest aside" is answered if the judged question is its own text. The thesis stays the topic
   Step 1 opened (PRD §1: "the thesis, its evidence and its judgement are different things"). The ladder step writes one view whose
   `question` states exactly the one thing its ladder settles, and lists every other part of the thesis's wording as not judged, with
   the reason. The reader is shown the view's question, never the thesis's wording, beside the answer. A thesis where nothing is
   primary (the three memory cases) gets no ladder and says why. Splitting one thesis into several views is the alternative; it makes
   the ladder call decide how many bets a topic holds, which is the decision that went in circles at Step 1 (§§48–58).

## Revised contract (v3 outline)

- **Input:** the thesis fields from the opening article's Step 1 answer; the article's date and text; the company, its fiscal-year
  note and the research list's themes, as production's [Subjects] block gives them.
- **Answer, strict schema:** `settles`; `not_judged` (each other part, with why); `object` (the ticker or a listed theme id);
  `question`; `ladder_type` (yes_no | states | number); `unit`; `rungs` (condition, lo, hi; a label only where code does not assign
  it); `favourable_end` (higher | lower, for a number about the company, with one sentence why); `reference` (the article's words
  and, for a number, its value; or null); `due_day` and `due_day_basis`; `year`; or `no_ladder` with a reason.
- **Code:** resolves `object` and takes the kind from the research list; orders and labels a numeric company ladder from
  `favourable_end`; renders intervals; runs `check_ladder`, `check_bounds`, `empty_rung`; requires a stated numeric reference to lie
  inside the middle rung of a company ladder (v74i line 25, "State the neutral comparison in its condition"; D186, "above, near or
  below guidance"); requires `reference` words to be found in the article; a real due day after the article's day; 18 months for an
  unsigned obligation. One resend, then no ladder, counted.
- **Store:** view id `v<N>` from `clean-<N>`; no dependencies; themes as theme objects, so the frozen judge runs as production runs
  it.

## The test (challenge the lines)

- **Stage A, a probe with a control arm.** Arms: control = v74i's ladder sentences quoted as they are (the original design);
  candidate = the contract above. Same 34 theses, same model and effort, 3 draws each (204 calls, under $2).
  - By code, all draws: refusals by check; for each thesis, whether its three draws agree on the favourable end and whether their
    middle bands overlap.
  - By two blind readers and a third on disputes, one draw per arm, arms mixed and unlabelled, with the thesis and article: does the
    ladder settle the thesis's `settling_outcome`; does exactly one rung hold for every outcome; is the due day supported; is the
    direction defensible; is the reference quoted and placed right.
  - Lines (proposed, for Alex to confirm): the candidate writes a ladder two readers call sound for at least 26 of the 31 theses that
    are not the three "nothing primary" cases; it is worse than the control in no class; three-draw agreement on direction is 3 of 3
    for every company number thesis. Any line missed stops before Stage B.
- **Stage B.** The frozen judge over the candidate's ladders, one fixed draw of ladders per stored run. Readers judge every judgement
  at which the rung changed, plus each thesis's first and last. The control is the matched theses whose question, period and due day
  a reader first confirms equal to the ruler's.

## Questions

- (a) Is my reading 1 right that instability across sends, not check refusals, is the ladder's main risk? What else explains the 12
  writes?
- (b) Does "the view's own question, the rest listed as not judged" meet D38 and your objection, or must a thesis with two things
  that can move apart become two views in this version? Name the case among the 34 where the single-view rule misleads a reader.
- (c) Which fields of the answer would you cut, and which code checks are unsourced?
- (d) The control arm: is quoting v74i as it stands the right control, and are the three lines falsifiable and fair?
- (e) What in this contract still needs Alex's word beyond "build it": D186 in this step, the single-view rule, the theme list as
  the only theme objects?
Under 1,000 words. Cite a file and line for every fact.

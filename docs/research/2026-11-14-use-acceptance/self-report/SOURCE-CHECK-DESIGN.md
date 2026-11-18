# Can readers apply "nothing stated sizes it" consistently, and does it track the answers readers reject? A $0 source check (council round 17), draft for the council

**Why.** D520 left Alex a product choice for amount answers (A leave the band, B label it, C show no band) and allowed the two cases
to be treated apart: (1) nothing shown sizes the amount; (2) an estimate built on stated amounts with a step of the judge's own.
The self-report diagnostic (D565) failed by its frozen rule; the judge's sentences suggest the split, but they are its own
after-the-fact words and were read by the design's author. This check asks independent readers, on stored answers outside those
45, whether the split can be applied to the sources consistently and whether it tracks the answers the earlier readers rejected.
It changes nothing in either system. The judge is shared by both systems, including the running default, so a usable case (1)
rule would bear on the product now running, not only on the new system.

**Cases** (outside the 45; fixed before any reading): the baseline reading (D426: the frozen judge on hand-written questions,
July window, three draws, every day's answer read by two families), its key rebuilt at $0 from the stored runs and checked against
the packet files the readers read (`baseline_count.record_problems`). Figure answers only. Rejected: every one settled INSUFFICIENT
or UNSUPPORTED. Accepted: an equal number, both first readers SUPPORTED, drawn by a fixed seed from the same question paths where
they exist, else from the other figure paths. If the rejected set is smaller than 8, the fortnight's and the fresh week's figure
last answers with their recorded verdicts are added and named. **Built** (`build_source_check.py`, seed 20261118; the rebuilt key
reproduces the reading's packet files exactly): rejected 11 (INSUFFICIENT 7, UNSUPPORTED 4) on three paths (credit support in
draws d1 and d3, custom-chip spending in d2), accepted 11 drawn from the 20 passed on those paths; with the three controls, four packets of 6 or 7 cases.
**Limit:** these are the same two matters as most of the 45 (credit support, custom silicon), other draws and questions; the
split is tested on new answers, not on new matters.

**Controls** (councils rounds 18 and 19; read by Claude before any reading, expected marks recorded in `build_source_check.py`,
every recorded mark checked): the fortnight's 2027 capital-spending answer (judgement 89; e674: NVIDIA's stated $1.3 trillion for
calendar 2027, inside the chosen band; expected `bears: direct`, `supports_band: yes`, `step_decides: no`); Stage B `u3` judgement
39 (HBM wafer capacity: no capacity figure is shown; expected `bears: none_shown`); Stage B `u3` judgement 15 (credit support:
Sharon AI's stated $4.88bn scaled by GPU count to Firmus, which decides the top band; expected `bears: comparable`,
`step_decides: yes`). The 22 study answers are outside the earlier 45; the two Stage B controls were among the 45. Shuffled in.

**What the readers receive** (described as it is): for each case, the user message of the stored judging request (the question,
its answer choices, and every statement shown to the judge with its source line and quote, as the judge saw them; not the
judge's instructions and not the articles) and four fields of the stored answer (band, reference, reasons, implied outcome).
Readers judge against what the judge was shown, not against the articles.

**The reading.** Two families apart, blind to the earlier verdicts and to the set each case comes from. Per case:
- `start_amount`: the evidence id(s) and the amount the answer's estimate starts from, or `none`.
- `bears`: how that amount bears on the quantity and period asked: `direct` (a stated figure or stated forecast of the same measure
  and period), `comparable` (another
  party, measure or period that you accept as a basis for this one), `weak` (the answer treats it as comparable but you do not
  accept it as a basis), `none_shown` (no amount is the start), `cannot_tell`.
- `supports_band`: do that starting point and any calculation from shown figures support this band? `yes` | `no` | `cannot_tell`.
- `step_decides`: does a step the evidence does not state (a scaling, a discount, a growth rate, a share) decide which band is
  chosen? `yes` | `no` | `cannot_tell`; if yes, `step` names it and its effect.
- `accept`: would you accept the chosen band as supported by what is shown? `yes` | `no` | `too_little`.
- `why`: at most 30 words, naming the evidence ids.
Case (1), "nothing shown sizes it", is `bears` `none_shown` or `weak`; case (2) is `bears` `direct` or `comparable` with
`step_decides: yes`.

**Decision rule, written before any reading (exploratory: 11 against 11 on three paths of two matters, related days; it is
not proof of a general rule and does not by itself open a live test):**
- **Unclear** if either family misses any recorded expected mark of any control; control results are reported apart.
- **Not applicable consistently:** the families differ on case (1) membership in more than a quarter of the 22 (6 or more), a
  `cannot_tell` from either counting as a difference.
- **Does not track rejection:** the share of case (1) by both families among the rejected is not at least 30 points (4 cases)
  above the same share among the accepted.
- **Lead:** none of the above. Every path, both families' marks, every `cannot_tell` and the earlier verdicts are reported
  separately; a live test of a case-(1) mark would be a separate design for the council.

# The second-look test: what is sent, read and decided, written before the send (D422)

Written 2026-11-10 before any second answer exists. The design Alex approved is `DESIGN.md`; this page fixes what the build
adds to it.

- **Sample** (`sample.py`, `sample.json`; the groups in a key outside this folder): sends of the fourth Stage A in four
  groups: every one with a fault the readers agree on (18); every one with a fault on which the two third readers part;
  every one with a mark one first reader failed that both third readers held; and 30 of those on which neither first
  reader failed a mark or named a fault (seed 20261110; ten events, ten figures, ten declines). The council's read
  (`council/kc-codex.md`) corrected the grouping: the third kind had been counted among "no reader faults". The counts
  are printed by `sample.py`.
- **What is sent** (`run.py`; `run.py check` rebuilds every conversation and each first turn has its stored request's
  identity): the first turn as the fourth Stage A sent it, the model's accepted answer as its own turn, and one instruction,
  the same in all 76 and naming nothing: "Check your answer once more against each rule above, one rule at a time. If it
  breaks none, return it unchanged. If it breaks one, return the corrected answer." The request's schema; the same model,
  effort and output cap. One send each: 76 calls, about eight cents; cap $0.20. (`DESIGN.md`, written before the grouping was corrected, says 66 and seven cents.)
- **What code does with the second answer:** the step's checks. A second answer equal to the first is "unchanged". One that
  code refuses is "refused", and the first stays: that fallback is part of the candidate. Otherwise the second is kept.
- **Reading.** I read every pair that differs, first against second, before any reader. Then the two reader families mark,
  with the unchanged form and in one reading round, a shuffled packet that holds the first answer of every sampled send
  and, for every send whose second answer differs and is kept, that second answer as an item of its own; no item says
  which it is, which send it belongs to, or which group. Where the two families differ, two third readers. A fault is
  "mended" only when, in this one round, the first answer carries it and the second does not; "new" when the second
  carries a fault its first does not. The fourth Stage A's own marks choose the sample and decide nothing else, so that the
  readers' difference from one round to the next is not counted as a correction (the council's condition,
  `council/kc-codex.md`).
- **What counts** (as in `DESIGN.md`):

  | | passes | fails | in between |
  |---|---|---|---|
  | the 18 with an agreed fault | at least 9 are mended in the one round (of those whose first answer the round again faults as agreed) and carry no new agreed fault | 5 or fewer | reported as it is |
  | the 30 no reader faulted | at most 1 now carries an agreed fault, or turned from a ladder into a decline or the reverse, or was refused by code | 3 or more | reported as it is |
  | the disputed and the held | reported only | | |

  If the one round does not fault again, as agreed, at least 12 of the 18 first answers, the readers' own difference is
  too large for the first row to be read, and the test is reported as not decided.
- **What it cannot show:** that the six lines are met; only a fresh run of the 44 theses with the second look in the step
  can. Whether the step takes a second look is Alex's decision after this result (D422).

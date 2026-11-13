# A second look by the model at its own answer: a candidate test, written for Alex's decision (2026-11-10; nothing built, nothing sent)

> **As run (2026-11-10, D422):** built and sent as `REGISTERED.md` fixes it, on 76 answers in four groups (this page, written
> before the council corrected the grouping, says 66 in three). The result is `RESULT.md`: it did not pass.

**What it is.** After the model's answer is accepted by code, the same conversation is continued once: the request, the
answer, and one plain instruction to check the answer against each rule of the request and return it corrected or
unchanged. The returned answer goes through code's checks as any answer does. It is one more call for every new thesis.

**Why it is a candidate and no more.** Four Stage A runs have left a small residue on lines 1 to 4 each time (what both
readers fail: 4, 5, 5 and 3 answers), each run mending the class it aimed at and showing a new small one. In five rounds of
asking the model about 23 of its own faulted answers, it called each fault its own slip and quoted the rule against it
(`stage_a/result-2/direction-accounts.json`; `probe-d413-d414-2026-11-10/result/event-accounts.json`;
`stage_a/result-3/wait-accounts.json`; `probe-d416-d418-2026-11-10/result/accounts.json`;
`stage_a/result-4/decline-accounts.json`). Those questions named the fault. Whether a question that names nothing finds
it, and what it does to answers that were sound, is not known: that is what the test is for.

**It departs from a rule in force.** AGENTS §6, Alex, 2026-10-30: the test the model must apply is a check at the very end
of the same prompt. That check is in place (1,325 characters, eight checks) and leaves this residue. A separate call is
his to decide.

## The test, if he approves it

- **Answers:** from the fourth Stage A's stored final answers, read by two reader families and two third readers:
  all 18 sends that carry a fault the readers agree on (a mark both first readers fail, or both third readers rule failed,
  or a fault outside the form both third readers uphold; three of them declines); all 18 that carry only a fault the
  readers dispute; and 30 of the 95 that no reader faults, drawn with a fixed seed, ten events, ten figures, ten declines.
  66 answers.
- **What the model is told:** the same instruction for every one of the 66, with no word of whether or where a fault is:
  "Check your answer once more against each rule above, one rule at a time. If it breaks none, return it unchanged. If it
  breaks one, return the corrected answer." The request's own schema; the request's own closing check is not repeated.
- **Who reads the result:** every returned answer that differs from the stored one is put before the two reader families
  with the unchanged form, in a packet that does not say which answers are second looks or which group they come from,
  mixed with the unchanged answers of the sample; where they differ, two third readers. I read every pair myself first.
- **What counts, written before any send:**

  | | passes | fails | in between |
  |---|---|---|---|
  | the 18 agreed faults | at least 9 no longer carry the agreed fault and carry no new one | 5 or fewer | reported as it is |
  | the 30 that no reader faults | at most 1 now carries a fault the readers agree on, a ladder turned into a decline, a decline into a ladder, or an answer code refuses | 3 or more | reported as it is |
  | the 18 disputed | reported only: how many change, and how the readers then mark them | | |

  The candidate goes forward only if both rows pass. A pass means "worth one Stage A with the second look in the step"; it
  is not a pass of the six lines, which only a fresh run of the 44 theses can show.
- **Price:** 66 calls, about seven cents from tokens; cap $0.20. If adopted: about one tenth of a cent and ten to twenty
  seconds more for every new thesis (the fourth Stage A: 148 calls for 132 sends, $0.109; with a second look about 280
  calls and $0.24).
- **What it changes in the design if adopted:** one more state between "answer accepted by code" and "ladder written"; the
  outcome record keeps both answers; a second answer that code refuses falls back to the first. Not designed further
  before the test says whether it is worth designing.

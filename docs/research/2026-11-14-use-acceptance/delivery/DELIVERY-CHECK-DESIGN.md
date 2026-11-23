# Do the kept financial figures reach the judgements of related questions? A $0 check, version 2 (D505), 2026-11-15

**What it can decide.** Whether, in the new system's stored fresh-week run (2026-09-22..28, the draw of D489), a kept revenue or
gross-margin figure that could change the answer of one of its seven questions was absent from that question's judgement requests.
Alex's word (D505): "进入相关问题的判断", on the option "第一步不花钱（$0）：检查现有问题做判断时，有没有系统存了、本该用到、却没送进去的财务数字。有就报给你，没有就停。"
Nothing is sent to a model; nothing changes in the system.

**The standard for "should have received" is not written here: it is the current phase's goal** (`docs/prd/10-filing-phase.md` §1:
"Each question's judgement must receive the facts that can change its answer"; §2: an analyst also reasons onward from a fact, e.g.
the other party's figure in a deal, price and volume for a product's revenue). Background that would leave the judgement where it is
does not count; PRD 10 also says facts that bear on no question must not be piled into one.

**Version 2, after council round 18 (`mx-codex-18.md`), before any reader ran.** Four changes: (1) the census no longer counts a
figure as delivered because a statement of the same claim group was shown (its example: the $92.37 billion consensus, line T-115,
was counted as delivered to the export question through a statement that states other figures); a group is a lead and the request's
own words decide; (2) a figure that changes how likely an answer is counts, not only one that changes the answer; (3) one question a
packet, with an explicit completion line, so an omission is not read as a considered "none"; (4) a third outcome, undecided, so that
readers' disagreement or an unsettled hand check is never reported as "none".

## Scope (fixed now)

- The seven questions of the stored draw (`delivery/questions.json`, from the run's `views.sqlite`).
- The 146 lines of the week's financial table (`record-3/financial-table-week.md`: the revenue and gross-margin figures the reading step
  kept, 111 statements). This is the scope Alex chose (the company's main financial numbers). The other statements no question
  received are not examined here (389 of 569 kept statements have no question, D489): that is the wider filing matter of PRD 10.

## Step 1: the census by code (`census_delivery.py`, read-only on the finished run; done)

- A judgement request shows exactly the statements the reading step linked to its question: over all 37 requests, no statement was
  shown that is not linked (0), and every linked statement was shown (196 links over the seven questions, checked for each). Each
  shown statement carries a note naming the statements the matcher read as the same claim; a repeat is shown itself only if it is
  linked too. So a figure reaches a judgement only through a link made when its article was read.
- Of the 146 table lines, 24 have a statement linked to some question. Lines whose own statement was shown, by question: credit
  support and guarantees (v1) 1; supply commitments (v2) 7; Blackwell exports to China (v3) 6; Vera Rubin shipments (v4) 10; the
  hyperscalers' 2026 capital spending (v5), the Hugging Face purchase (v6) and the RTX Pro 5500 approvals (v7) none. A statement of
  the same claim group shown to a question is recorded as a lead only.

## Step 2: what each question needs, read blind (frozen before any reader)

Readers of each family (Codex, Claude subagents), blind to what was delivered and to each other, take one question at a time
(`question-v1.json` .. `question-v7.json`, `brief-needed-v1.md` ..) with its possible answers and the whole table, and list every line
whose figure can change the question's answer or how likely an answer is, saying which answer it moves and why. Background is not
listed; a question may have none. Each question ends with a completion line (done, and how many listed): a question without one is
not read, and is run again.

## Step 3: delivered or absent

For every (question, line) either family lists:
- **delivered** when a statement of the line itself was shown to the question, or when the stored request of that question states
  this figure: its value with the measure, period, source and qualification that make it bear on the question (found by a code
  search of the request for the value, then read in the request; a same-claim group only says where to look);
- **absent** otherwise; and then **when**: was the question already open when the figure's article was read (the reading step did
  not link it), or was the question opened later (nothing files an earlier statement under a later question);
- its **article and stored passage are read** before its source and bearing are reported: the table's stored labels can be wrong.
A line only one family lists and that is absent is read by a fresh reader of each family against the question, the article and the
passage (can this figure change the answer or its likelihood?): both yes, it counts as listed by both; both no, it is dropped;
split, it stays an open lead.

## The instrument's own check

The lines the system did deliver (step 1) are a positive control read both ways: the share of them the readers also list (a reader
who lists none of what the system linked has a different bar from the system), and the share of the readers' agreed lines the system
delivered.

## The rule (Alex's words: "有就报给你，没有就停")

- **A finding:** a line both families list for a question (or one lists and the fresh pair confirm), absent from the requests of
  that question, confirmed by reading the stored request and the article. Each is reported with the question, the figure, its
  article and which answer it bears on.
- **None:** every question has its completion line from both families, and no listed line is absent. Only then does the line of work
  stop on Alex's "none".
- **Undecided:** an absent line stays an open lead after the fresh pair, a packet is incomplete, or a hand check cannot settle
  whether the request states the figure. Reported with the leads; not "none".

**What it cannot show:** whether a judgement would have changed with the figure (that takes re-sending a stored request with the
fact added: a few cents, only on Alex's word); whether all useful evidence reached the seven questions, or whether statements
outside the financial table should have; anything about production or about which system carries forward. A finding is a relevant
kept figure absent from the named requests, in this one run and this table's scope.

## Correction (2026-11-15, found by the reflection council "my", round 3, and checked in the stored run)

This page said that nothing in the new system files an earlier statement under a question opened later, and that a judge is shown
the statements linked "when their articles were read". Both are wrong as written. **The new system has a later-linking step**
(`clean-arch/step3/library.py`, `link_later`): when a question opens, the system checks the earlier groups of statements (a
statement with its repeats) **whose original statement arrived without a question** (a batch that fails twice stays pending and is
tried again; none stayed pending in this run). In this week: seven calls, 516 group-and-question checks, 2 linked (both to the Vera
Rubin question); of the 196 links, 194 were made when the statement's article was read and 2 by this step. **A group whose original
arrived under another question is excluded, even if the new question also needs it:** e379 (the group `163:e3` in the stored
library) arrived linked to the export question at article 163, so it was not among the 166 checked when the RTX Pro 5500 question
opened at article 169. The counts and findings of this page do not change; the description of the cause does: the
case is "linked elsewhere and so never reconsidered", not "nothing looks back". Production does not link an earlier record to a
question opened later (D456: none of 3,225 links in six draws points back; a later article that repeats the fact can still deliver
it; `clean-arch/e2e-comparison-2026-11-13/unlinked-trace/UNLINKED-TRACE-RESULT.md`, which found that in those draws, on the graded
questions of the July window, such unlinked facts cost no final answer).

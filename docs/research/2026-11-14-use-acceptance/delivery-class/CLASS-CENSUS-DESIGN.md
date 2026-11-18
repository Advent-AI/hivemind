# How large is the gap? A $0 census over everything the new system kept in the fresh week, version 2 (D507), 2026-11-15

**What it can decide.** In the new system's stored fresh-week run (2026-09-22..28, the draw of D489: 567 kept statements, seven
questions, 37 judgements), how many kept facts that bear on a question never reached its judgement: whether the one instance of D506
is an isolated case or common. Alex's word (D507): "先查清这类缺口有多大", on the option "不限财务数字，把系统存下的全部说法（包括已归到别的问题下的）对着 7 个问题查
一遍，看有多少“该进某个问题的判断却没进”。查清是个别还是普遍，再决定要不要改。" Nothing is sent to a model; nothing changes in the system.

**The standard for "bears on" is the current phase's goal, not a new one** (`docs/prd/10-filing-phase.md` §1: "Each question's
judgement must receive the facts that can change its answer"; §2: an analyst also reasons onward from a fact). A change in how
likely an answer is counts (council round 18). Background that would leave the judgement where it is does not; PRD 10 also says
facts that bear on no question must not be piled into one.

**Version 2, after council round 20 (`mx-codex-20.md`), before any reader ran.** The council confirmed the population (each of the 567
stored records once) and asked for three changes, all made: (1) facts are counted within statements: a statement can hold several
(e488 holds three per-gigawatt figures), so the fresh readers name the one fact they judge, and Step 2's same-claim groups are
leads for grouping, never automatic merges (each hand merge is recorded with its members and reason); (2) the fresh readers get the
whole article of every candidate and mark whether it supports the stored fact; the same claim repeated by another outlet is
"already shown", a different source's own figure is not; (3) disagreement stays visible: the two marks are recorded apart and a
candidate is dropped only when both fresh readers agree on the same ground; the first readers write all seven question keys for every
statement, and a part is refused unless each expected statement has exactly one such line. The brief no longer says that most
statements bear on nothing. The council also checked that every statement shown in any request of a question is in its last request.

## What is already known by code (D506's census)

A judge is shown exactly the statements linked to its question when their articles were read: 196 links, 185 statements linked to
at least one question (11 to two), 382 to none. The questions opened at articles 4, 14, 33, 35, 42, 116 and 169 of 235: a statement
read before a question existed could not be linked to it when read (17, 43, 79, 82, 101, 274 and 399 statements), and nothing in
this system files an earlier statement under a later question.

## Steps (frozen before any reader)

1. **First readers, blind to the links.** All 567 statements, as a judge would see them (summary, quote, who said it, the days), in
   the order read, in six parts of at most 95 (`statements-part1.json` ..). A reader of each family takes each part with the seven
   questions and writes, for every statement, one line holding all seven question keys: empty, or which fact bears, on which answer
   and why (`brief-class-part1.md` ..). A part is read only when each of its statements has exactly one such line; else it is run
   again.
2. **Candidates, by code:** every (statement, question) a reader lists where the statement is not linked to that question.
3. **A fresh reader of each family, shown everything the judge had.** For each question, its candidates (those both families listed
   and those one listed), each with its summary, quote and whole article, beside the whole text of the question's last judgement
   request, in packets of at most fifteen. For each candidate: the one `fact` judged; `in_article` (the article supports it as
   stored); `already_shown` (the request already states this same fact, in any wording, the same claim repeated by another outlet
   included); and `bears` (added to what the judge had, it can change the answer or its likelihood; which answer and why).
4. **Counting, by this rule:**
   - a **confirmed missing fact** for a question: listed for it by a first reader, not linked to it, and marked in the article, not
     already shown and bearing by **both** fresh readers. Candidates that state the same fact count once for a question: a merge is
     made by reading the two readers' `fact` words and the summaries (Step 2's groups only say where to look), and each merge is
     listed with its members and reason;
   - **dropped**: both fresh readers say it does not bear, or both say it is already shown;
   - an **open lead**: anything else (they differ on a mark, or one says the article does not support it); both pairs of marks are
     shown.
   Each confirmed fact is read in the stored request by hand before it is counted, and is sorted by when and where: the question
   was open when its article was read and the statement was linked to another question, or to none; or the question opened later.

## What is reported (no pass line: Alex asked for the size)

- Per question: the confirmed missing facts (count and list, with the answer each bears on), the open leads, and beside them the
  number of distinct facts that did reach it.
- Over the seven questions: the confirmed missing facts by kind (linked to another question; linked to none; the question opened
  later).
- **The instrument's own check:** of the 196 links the system made, the share each first-reader family also lists (a family that
  lists few of them has a higher bar than the system); how many candidates each family alone listed and what became of them.
- The D506 finding as a known case: do the first readers list the two per-gigawatt statements for the credit-support question.
- Stated limits: one stored week, one draw, seven questions; **the confirmed count is a minimum found by this reading, not a complete
  census** (a fact neither family lists is not found; a low count is not proof the gap is isolated); model readers over-list (D506:
  29 one-family candidates became five open leads); "never reached" is read at the question's last request and does not measure a
  fact that arrived late for an earlier judgement; the effect of a missing fact on a judgement is not measured.

**What it cannot show:** that a judgement would have changed; a rate for the system in general; anything about production or about
which system carries forward. Whether to change anything is Alex's after the size is known.

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

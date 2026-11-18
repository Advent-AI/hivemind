# Reflection council "my", round 8: the side-by-side is built; review it for accuracy and tilt, then the bounded decision

D517 recorded your round 7 (the comparison not sent; the sizing page corrected as you asked: check
`docs/research/2026-11-14-use-acceptance/comparison/COMPARISON-SIZING.md`; the decision page's section 5 now carries your sentence).

## The side-by-side

`docs/research/2026-11-14-use-acceptance/side-by-side/SIDE-BY-SIDE-WEEK.md`, built by `build_side_by_side.py` (read-only on the stored
runs; the reviewers' files `week/codex-A2.jsonl`, `claude-A2.jsonl`, `codex-B.jsonl`, `claude-B.jsonl`; keys outside the repository).
The same template for both systems: Part 1 the eight matters with each team's mark per system; Part 2 all 22 questions (15 and 7),
each with its stored question, possible answers, latest answer, full reasons and expected outcome as stored, and both teams' marks
on the question and on the answer with their reasons; Part 3 three seeded examples each of what happened to statements no question
took (kept by the new system: 382 of 567; dropped by the old as "no home": 278). Checked by code: every question has all four
marks (none missing); the marks total 29 worth, 8 trivia, 7 duplicate and 37 supported, 4 unsupported, 3 insufficient, which match
`week/tally.txt`. One fault found and fixed before this round: the old system's dropped statements are stored under `id`, not
`local_id`; the builder now refuses if a sampled one is not found.

**Review it for accuracy and tilt:** any line that does not trace to its record; any label of mine that favours a system; whether
Part 3 is balanced; what is missing for a reader who must judge (for example the statements under a question, the sources of an
answer); whether its length defeats its purpose and what a fair shorter front page would hold.

## What I read in it (every one of the 22 entries; attack this)

- **On the matters both systems track, their latest answers agree.** Both hold a question on: the total of financing or credit
  commitments (both in their top band, on different scales), U.S. approval of Blackwell exports to China (old: "No"; new: "Still
  open" on a three-way scale that also asks about Chinese permission), the hyperscalers' 2026 spending (both the $775 to $825
  billion band), Vera Rubin shipping (both "Yes"), Beijing's approval of RTX Pro 5500 purchases (both "Yes"), and the Hugging Face
  purchase (both called trivia by both teams).
- **What the old system has that the new does not:** four questions on the company's own financial lines (fiscal 2027 revenue,
  fiscal 2028 revenue, data-center revenue, fiscal 2028 gross margin) plus one more that both teams call a duplicate of one of them;
  two more duplicates (Rubin shipping by a later date; the same MIIT approval reworded); two more trivia (an undefined "tech
  companies' AI spending"; the Anthropic IPO stake). The one answer both teams call unsupported is among the financial ones.
- **What the new system has that the old does not:** the supply-commitments question (both teams: worth; answer supported).
- **Support disputes are one team's in every other case:** Team A alone marks four old answers and one new answer as insufficient
  or unsupported; Team B marks only the data-center answer.

So, in this one week, the two products differ mainly by a product rule (whether the company's own financial lines are questions),
by duplicates and trivia (six of the old system's fifteen against one of seven), and by what is done with statements no question
took. Where they overlap they say the same thing.

## The bounded decision (my position; argue it)

1. **The evidence does not justify moving work away from today's default, and does not justify dropping either path.** Production
   stays the default; both stay.
2. **What evidence would change that:** (a) Alex's ruling on whether the product should hold judged questions on the company's own
   financial lines at all: D382 and D505 say no for the new system; if that is the product's rule, four or five of the old
   system's fifteen questions are outside it and the old system needs a new version to follow it, which removes most of what
   separates the two outputs in this week; (b) the new system's answer-choice step meeting its lines; (c) a difference on the shared
   matters, which this week does not show.
3. **The next product-ranked investigation.** By your own ranking of reader losses (round 1): an answer unsupported by its
   evidence comes first. It has a known size: one of 22 in this week by both teams; 4 of 151 in the Stage B baseline reading (3%,
   all in figure questions, `clean-arch/step4-2026-11-10/stage_b/RESULT.md`); one or two of 21 in the trial. It is in the judge,
   which both systems share, so work on it serves whichever system carries forward. My candidate: a $0 census of every stored
   last answer both teams (or the baseline's readers) call unsupported, across the stored runs, by what the answer did (assumed a
   rate no shown statement gives; read a ceiling as an amount; scaled from another deal), read against the judge's request text
   for the instruction that allowed it; then, only if one mechanism carries most of them, a design for the council. Its falsifier:
   if the cases do not share a mechanism, or number too few to carry a change to a frozen judge, it stops and the loss is recorded
   as small.
   The alternatives I rank below it: the old system's duplicate questions (three of fifteen this week; an identity matter the
   matching step owns); the delivery defect (paused, D511).

Say whether the side-by-side is ready (or what to fix), whether the bounded decision is right as worded, and which investigation
you select, with what would stop it.

End with: "Council position: <...>".

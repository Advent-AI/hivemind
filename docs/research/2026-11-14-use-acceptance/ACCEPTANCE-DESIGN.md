# The use-oriented acceptance: design for Alex's decision (D484), version 3, 2026-11-14

**What it decides.** Whether a system gives an analyst a usable research record on news it has never seen: the big questions opened, the
judgements supported by what they were shown, the statements accurate against their articles, and no fact that would change a judgement left
out, within the articles read. Both systems, the same days. It is added beside the frozen ruler, which stays and is reported unchanged on its
own window (D261); it changes no existing gate by itself (D483). Version 2 answers council round 6 (`council/mw-codex-6.md`); version 3 round 7 (`mw-codex-7.md`).

## Run

- **News:** 2026-09-22 to 10-05: 479 eligible articles, of which 6 were sent by earlier Step 1 runs (takeover and unfiled rounds, 2026-11-07/08)
  and are removed; 473 never sent by any stored run or probe (checked over every run database and probe record, the source copies excluded;
  the list is frozen, `fresh-articles-2026-09-22-10-05.json` with its sha256, which also names what sent each removed article: the
  Step 1 test traces of the takeover and unfiled rounds). The 2026-09-08..21 window is not used: the unsigned-deal probe sent four of its articles.
- **Draws:** three per system, launched together, from an empty library, in publication order (AGENTS §7.3: totals from three draws). Reported
  per draw and in total; no draw is added after the result.
- **Systems:** production as it now runs (poc-v118) and the clean path as frozen (Step 1 c8, Step 2, the ladder step, the frozen judge). No
  production change, no new prompt.
- **Cost:** priced from the full run's charged cost per article: production about $1.20 a draw, clean about $6.00 a draw; about $22 for the six
  draws, a reservation ceiling of $35. This is above the $40 ceiling I set myself while Alex was away ($29 spent); it needs his word.

## Readings (two reader families, blind to the system and to each other; disagreements listed; key disputes to Alex or a reader he names)

- **Scopes, each stated with its result:** A's missed questions and C cover a sample of 80 of the 473 articles, stratified by day (seed fixed
  before the run), and are stated for those 80, not for the window; A's quality marks, B and B2 cover every question each draw opened in the
  window, every last judgement by 10-05, and every statement those judgements cite (window-level).
- **A, big questions:** each family lists from the 80 articles the questions worth tracking on their own; then each system's questions are
  marked opened / narrower / broader / missed per matter. Counted: matters both families list, and separately matters only one lists (reported
  with the disagreement, not dropped). **Covered** = opened, or narrower when the narrower question carries the matter's main outcome (each such
  call written with its reason); broader and missed are not covered. Each system's opened questions are also marked worth tracking / trivia /
  duplicate.
- **B, judgements:** every question's last judgement by 10-05, read against the request as sent. Planted wrong judgements are built on requests
  not otherwise in the packet; supported controls are confirmed by a separate reader first and any disputed control is replaced.
- **B2, statements:** every statement a last judgement cites, against its own article (the passage located in the article text): date,
  speaker and summary.
- **C, delivery:** first, a separate fact listing: each family reads each of the 80 articles and lists every statement that bears on a covered
  matter (with its passage), not only the sentences that raise a question; then code classes each listed fact per system (not extracted / no
  link / linked elsewhere / delivered in the request of a judgement after it arrived), checked by hand; the undelivered ones are read against
  the full judgement request ("would it change the rung?"). Controls of both kinds: known "would not" (facts already in the request, or
  unrelated) and a known "would change" **group** (PRD 10's custom-chip case: a group of facts moved 9 of 9 sends off the lowest rung), read
  as a group because no single-fact positive case is established.
- **Denominators and empty cases:** a system that opens no question on a matter is "missed", never excluded; a system with no judgement on a
  covered matter fails B for it; an empty denominator is reported as not measured, never as met.

## Lines (for Alex to set; a starting proposal, not decided)

| reading | proposed line, per system, in at least two of three draws | basis in the trial (leads only) |
|---|---|---|
| A | covers at least 4 in 5 of the matters both families list | 6–7 of 7 in the trial |
| A | at most 1 in 5 of its opened questions marked trivia or duplicate by both families | clean acceptance D386: 1 of 10 |
| B | at least 9 in 10 last judgements supported by both families | 7 of 9 and 10 of 12 in the trial |
| B2 | at most 1 in 20 cited statements wrong in date, speaker or summary against the article | 4 of 201 flagged by both, unconfirmed |
| C | no undelivered fact both families say would change a judgement | the product's purpose (PRD 10 §1) |

A system that meets every line is usable on this news; which system goes forward, and whether either is called production-ready, is Alex's
decision after the result.

# The use-oriented acceptance: the $0 trial run on stored runs (D483, D484), design version 3, 2026-11-14

**What it decides.** Whether the three readings the acceptance needs can be done reliably and at what workload, before the acceptance's design
and lines go to Alex: (A) the big questions an analyst would hold, listed from the articles, and which each system missed; (B) whether each
judgement is supported by what the judge was shown that day; (C) whether a fact a system missed, left unlinked or sent to the wrong question
would have changed a judgement. It declares no winner (D483) and measures no completeness of the window. No model is paid: readers are Codex
(read-only) and Claude subagents. Version 2 answers council round 3 (`council/mw-codex-3.md`), version 3 round 4 (`mw-codex-4.md`).

**Stop rule for design rounds.** After version 3, a finding that the trial itself would reveal (a reading the readers cannot do, a class with
no case, a disagreement) is recorded as a question the trial answers, not as a blocker; only a finding that would make the trial's own result
wrong or unreadable stops it (AGENTS §1: when one mechanism draws findings round after round, a structural rule, not another answer).

**Material.** The full run of 2026-11-13 (window 2026-07-01..07-14): clean draw c1 and production draw p1 (`poc/data/clean-e2e-full-2026-11-13/`),
one draw each. The frozen golden-v5 is used only as a known reference to calibrate readers, never edited or rescored (D261).

## A. Big questions these articles raise, and what each system opened

- *Articles:* 40 of the gold's 115 dev articles that both draws processed: the 24 with a must_open question, 8 with only may_open and 8 with
  neither (seed 20261114), plus the articles of D456's known cases (p1's Ohio guarantee and Kyber cancellation) when not already drawn, in
  publication order. **Scope:** only the questions these 40 articles can raise; no window-wide miss rate.
- *Reading 1 (blind):* each reader sees only the 40 articles (text, day, publisher) and the standard's §3–§4; per article it lists the questions
  worth tracking on their own (a big matter; an outcome public material can settle on a date), with the quoted sentence; then merges them into
  matters across the 40 (one matter, several articles).
- *Calibration, defined:* the unit is a gold matter: the 28 must_open entries merged into matters by the gold's own text before reading (written
  down with the merge, `calibration-matters.json`). A matter is **recalled** when the reader lists a question that the same outcome would settle
  and whose answer cannot move apart from the gold's (D248's test); another year of a figure is another matter where D38 tracks years apart.
  Each judgement is written with its reason; the two readers' disagreements are kept. Line: recall of the must_open matters at least three in four.
  The must_not side: the denominator is the articles the reader lists anything for; the must_not entries of these 40 articles are listed with their articles
  before reading (`calibration-matters.json`); a reader **fails** when more than one in five of the articles it lists anything for carries a listed question the gold marks
  must_not. may_open matters and new reasonable questions are never errors; they are reported.
- *Reading 2:* each listed matter against each system's library at 2026-07-14, with each system question's opening step, article and day
  recorded: opened (same matter, any reasonable shape), opened narrower or broader, opened from an article outside the 40, or missed. A shape
  the key's D430 reading would count as a loss is recorded, not counted as a miss.

## B. Judgement support, on what the judge was shown

- *Items:* every view's last judgement by 2026-07-14 in c1 and p1; for each, the judge request as sent (rebuilt from the archive and
  `judge-requests.json`: the evidence shown, with each item's original passages, speaker and date). Material dated after the judgement day is
  refused.
- *Controls (mixed in, unlabelled):* four planted wrong judgements (a rung moved against what the cited facts say), and four real judgements
  that a separate reader (a third family-blind Claude subagent, before the trial readers) confirms supported against that day's request;
  a disputed one is replaced, so a reader that calls everything wrong or everything right fails.
- *Reading:* supported / unsupported / insufficient, against what was shown that day (the request as sent; the original article
  is shown apart and marked as not seen by the judge); per cited item, whether the summary matches its quote,
  the speaker and the date; the later outcome, where known, recorded apart.
- *Calibration:* both families catch all four planted and pass at least three of four known-supported; else the reading is not reliable as
  briefed.

## C. Facts that did not reach a judgement in time

- *Questions:* every view either draw opened on a matter of A's list or the gold's 40 articles; where only one system opened it (p1's Ohio
  question), the other is recorded as not opened, not as a delivery comparison.
- *Candidates, from the source, within A's 40 articles only:* for each such view, the facts of those articles that either reader of A, or the
  gold's items, tie to its matter (a disagreement is kept as pending, not dropped); each is classed by code and read: not extracted; extracted,
  no link; linked to another question; delivered. **Timing:** a fact counts as delivered for a judgement only when it is in that judgement's
  request as sent (its shown evidence); a link that did not reach the request, and a later delivery, are recorded apart. No claim covers
  articles outside the 40.
- *Known cases first:* D456's traced cases (p1's Ohio guarantee linked to the credit-support total, not to the Ohio view; p1's Kyber
  cancellation arriving one article before the view opened) must be found by this procedure in each of their classes; a class with no known
  case is reported as not measured.
- *Reading:* would the missing fact change the judgement a user should get that day (yes / no / cannot tell), with controls (delivered facts,
  unrelated facts) mixed in.

## What is reported

Per reading: items, the two families' agreement per class (not one overall rate), the calibration result, unresolved points, and the workload
(articles and items read, reader tokens and time). A reading that fails its calibration, or whose families agree on fewer than three items in
four in any class, is reported as not reliable as briefed. Then the acceptance's design goes to Alex: fresh articles (from 2026-09-08 on, unused
by any run), both systems the same days from an empty library, the readings as calibrated, runs and budget priced from tokens, his lines.

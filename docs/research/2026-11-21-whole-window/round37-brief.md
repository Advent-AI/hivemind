# Council round 37: the pilot's control stopped on a double refusal (read-only)

Scope: `docs/research/2026-11-21-whole-window/` (PAID-DESIGN.md §2, §4, §8; paid_run.py), the pilot data in
`poc/data/link-pilot-2026-11-21/`, and the product's judging retry (`src/hivemind/views/judging.py` `round_of_judgements`,
`check_answer`, `retry_note`; `src/hivemind/views/round.py` `judge_day`). Out of scope: every other module; no change to frozen files;
no paid call. Your report is a lead; cite the lines you read.

Files: control-1 is finished; read its copy at
`/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/control-1-copy/` (views.sqlite,
archive.sqlite, summary.json), open read-only (`file:...?mode=ro`). Do NOT open anything under `poc/data/link-pilot-2026-11-21/linked-1/`:
that run is live. My scripts: `.../scratchpad/h2_until_stop.py`, `.../scratchpad/id_typo_census.py` (same scratchpad folder). Stored
v118 runs: `poc/data/comparison-2026-11-17/run/old-{1,2,3}/prod/`.

## What happened (verify each line)

1. control-1 (poc-v118) stopped on 2026-09-08: `judgement refused twice: v21: e3111 is not among the evidence shown to v21`. Calls 8938
   (first answer) and 8941 (the retry with the code's note) in `control-1/archive.sqlite`. v21 = "How much will NVIDIA's total revenue
   grow in FY2027?". Its request listed 29 evidence ids; the answer cites all 29.
   - 8938 cited `e362` where the list has `e3620` (the only shown id it left out).
   - 8941, after the note "e362 is not among the evidence shown … citing only the listed ids", cited `e3111` where the list has `e3110`
     and `e3112`.
   Both are one-character copy errors of a listed id; the reasoning is not at issue.
2. Through the last completed day (09-07), control-1's trajectory equals old-2's on every table H2 checks (984 non-reader judgements,
   4,196 evidence rows, 5,223 links, views, keys, rungs, switches, successions); the summary's H2 `false` comes only from the missing
   days after the stop (script: `scratchpad/h2_until_stop.py`, reproduced in my notes). Only readers were bought (201 attempts:
   v14 60, v9 58, v16 44, v21 39); spend for both sequences so far about $1.47 of the $2.50 ceiling.
3. Census of refused judge answers on stored v118 runs: old-1 1,610 judge calls, 1 refusal (theme ids, not evidence); old-2 1,620
   calls, 4 refusals (3 evidence ids one edit from a listed id: e88, e3955, e3998; 1 theme ids); old-3 1,709 calls, 2 refusals (both
   one-edit evidence ids). No retry was refused in the three runs. control-1's fresh calls: 3 refusals in 201 (8807 v14 `e393`, not
   one edit from any of its 124 listed ids, its retry 8809 accepted; 8938 `e362`; 8941 `e3111`), one of them a retry. Readers cite
   long lists (v21 cites 29, v14 sees 124), which plausibly raises their rate. Census script: `scratchpad/id_typo_census.py`.
4. In control (poc-v118), no dependencies exist and none of the 118 fresh v9/v14 requests mentions v21: v21's conclusion feeds neither
   question of the primary line P (v9 Data Center, v14 total revenue).
5. The ordering tool (`contradictions.py`, a lead, not a reading) on 07-10..09-07: control-1 28 definite of 60 dates, old-2 50 of 60.
   The class recurs in the fresh control.
6. linked-1 (poc-v120) is still running at the time of writing; its outcome will be added below before you answer.

## The registered rule

PAID-DESIGN.md §2: "a stop is final, and its verdict follows §4's precedence (a linked double refusal fails; an infrastructure stop or
a control's double refusal makes the comparison inconclusive)". §4 precedence (2): "a control's double refusal … → inconclusive". §8:
"an invalid run … is inconclusive". The product itself on a double refusal: `judge_day` records `judgement_refused_twice` and the day
"remains resumable"; a resume re-samples (the refused rows are retired).

## Questions

1. Is the registered pilot verdict "inconclusive (invalid: control double refusal)" — or "fail" if linked-1 double-refuses — exactly
   what the rules give? Anything I have misread?
2. Is the mechanism right (one-character id copy errors, a product defect of the frozen judge, unrelated to the links)? Is the census
   right and complete on the stored runs?
3. The design treats a double refusal as terminal, while the product treats it as a resumable day. With about 200 reader attempts per
   sequence, a double refusal in some sequence of six is not rare. Should the rule for the remaining comparison change, and to what?
   Candidate (mine): on a double refusal in either arm, the day is resumed once, as the product does (the refused rows retired, the
   refusals counted in H1); a second double refusal on the same day is terminal under the old precedence. Recorded before any further
   send. Counter-arguments: selection, a rule changed after a result, the symmetry between arms.
4. The next step for Alex (he is active; any spend beyond the $2.50 ceiling is his). Options I see:
   A. Stop the line with the inconclusive verdict.
   B. Re-draw control-1 from scratch under the current rules (about $0.85, a new ceiling; the same risk again).
   C. Resume control-1 from 09-08 under the candidate rule (about $0.15 inside the current ceiling), then read pair 1 as registered.
   Which one, and what result of it would move the decision? If C, is it legitimate for pair 1 given that I have seen control-1's
   lead count (item 5) but not linked-1's P rows?
5. Should the id copy error itself go to Alex as a product finding (one structural rule), and what would that rule be (for example,
   evidence cited by a short list position the code maps back, or the retry note naming the nearest listed ids)? It is a change to the
   frozen judge, a new version only Alex opens.

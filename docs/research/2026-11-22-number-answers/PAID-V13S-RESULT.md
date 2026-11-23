# The one-time v13s paid re-send (D753, D754): result

**Verdict: STOP (complete).** The verdict is sealed in `poc/data/judging-v13s-paid-2026-11-23/verdict.json`, with the readings in
`readings.json` and the key in `~/.hivemind-keys/v13s-paid-gate/`.

- **Joint:** usable in 3 of 9 pairs against the registered 8 of 9; per snapshot old-1 2, old-2 1, old-3 0.
- **Separate:** usable in 0 of 9 pairs.
- **Published defects:** 5, all singleton "deciding gaps".
- Nothing is tuned on these 36 answers (`PAID-GATE.md` §5).

## 1. The run

- **Model and plan.** gpt-6-luna (poc-v118's judging setting). The plan is `paid-plan-v13s.json` (`0dc7c310…`): 12 requests × 3
  draws, the D751 request.
- **Spend.** $0.3339 of the $0.50 cap (ledger), with no stop. All 36 scored first attempts finished, and the 22 diagnostic retries
  were sent after them.
- **Code decisions on the scored first attempts:**

  | Arm | Published | Refused |
  |---|---:|---:|
  | Joint (9) | 3 | 6 |
  | Separate (18) | 5 | 13 |
  | Singletons (9) | 6 | 3 |

  - The separate arm's pairs: 8 not reconciled, 1 refused.
  - After the diagnostic retries (not scored): joint 3 published, separate 11, singletons 8.

## 2. Why the code refused 22 first attempts (each read against its source)

Every one of the 22 refused answers contains at least one error of luna's against a rule the request states. None was refused by a
check alone.

| Class (answers can carry several) | Count |
|---|---:|
| A piece of a longer expression copied (e.g. "$108.0 billion" from "$108.0 billion, plus or minus 2%", the schema's own example) | 8 |
| Reference marking missing or doubled (S5) | 6 |
| More than one figure marked as the outcome (S6) | 4 |
| A qualifier or extra words inside the number ("around $113 billion to $114 billion") | 4 |
| Not as written (a range rewritten with a dash; "$1 billion") | 2 |
| A table number split by a line break ("$" and "177,837" on separate lines). The check is strict here; it appeared twice, both times beside a model error | 2 |
| A qualifier mismatch ("over" recorded as "more than") | 1 |
| Value and range both given (S7) | 1 |

- **The check-strictness case** (a number split by a line break in a table) is real and worth fixing, but it decided no outcome here.

## 3. What the readers found (two blind families, a third Codex reader on 12 disagreements)

- **Usable pairs.** Joint 3 of 9 against separate 0 of 9, a gain of 3. The registered pass needs at least 8 joint pairs.
- **The five published defects** are all singleton deciding gaps: an unsized adjustment decides the band.

  | Packet | Case | Draw | The adjustment |
  |---|---|---|---|
  | P15 | O | 2 | half of a possible investment counted, with no evidence for the fraction; the full amount moves the answer to the next band |
  | P16 | E | 1 | growth cut to 90%, taking FY2028 below $40B, with no passage sizing the loss |
  | P19 | S (CY2027) | 2 | a data-center share of at least five-sixths needed for the band; no passage establishes it |
  | P26 | S (CY2027) | 1 | an Oracle deduction the passages do not bound decides between bands |
  | P27 | S (CY2027) | 3 | a 75% share gives one band and a 95% share another; the passages do not say which is likelier |
- **Luna on E.** It answered three times with no "can't tell yet":
  - d1: $38B, rung 3, an unsized cut, a defect;
  - d2: $43B, rung 2;
  - d3: $37.5B, an unsized cut, refused for format.

  Its behaviour on E matches the free tests' Claude writer, not the Codex writer.

## 4. What it shows, and what it does not

- **The design point (D725), directional.** Computing the pair together gave 3 usable pairs, and computing them apart gave none,
  because separate answers did not reconcile. That supports the design idea, but far below the registered line, on one run.
- **The production model on this format.**
  - Luna fails mechanical format rules on 61% of first attempts. The diagnostic retries show many are fixable once named.
  - On boundary questions it publishes numbers decided by unsized adjustments: 5 of its 6 published scored singletons.
  - The free tests' proxy writers (Claude, Codex) did not predict either rate.
- **Not shown.** Whether a stronger model, a higher reasoning effort, or code-side format repair would pass. Each is a separate
  decision and a separate test.

## 5. Corrections from council round 71 (`codex-r71.md`), each checked against the run files

- **One refusal was not luna's error.** On O's first answer (`answers.jsonl` line 20), the request showed the period as
  `end of FY2027` followed by an explanatory parenthesis and asked for keys to be copied exactly. Luna copied both, and the checker
  expected only `end of FY2027`. Removing the parenthesis in a replay turns the refusal into a publish.
  - The headline is therefore: the checker refused 22 of 36 first attempts (61.1%) on these 12 requests. 21 carry an identifiable
    luna violation, and one is this request/checker mismatch.
  - The readers had found that this same $45B forecast rested on an unresolved overlap, so admitting it would have added a defect.
- **Several outcomes marked:** 3 answers, not 4.
- **A checker misread.** On lines 14 and 38 the checker read a change over time (from $253B trailing to $392B this fiscal year) as a
  range. Luna's $392B for the current year was right. Both answers also carry another genuine error.
  - Joining "$" and "177,837" across the line break still fails, because the quoted table omits its scale.
- **Retries:** 8 of 22 cleared the checks (6 separate, 2 singleton, 0 joint). They are diagnostic only.
- **The design point (D725), stated precisely.** Readers saw every packet, the withheld ones included. Their settled readings found
  conflicting numbers in 8 of 9 separate pairs and 0 of 9 joint pairs; in the ninth separate pair, both readers attributed the
  difference to rounding. Of the 9 separate pairs, 8 never reached the code's reconciliation because an answer had been refused. The
  one that did used $113.5B against $108B for the same Q3.
  - This supports D725's consistency claim on these snapshots. It does not establish forecast accuracy or readiness to publish.
- **Open checker defects,** recorded and not fixed (the STOP bars tuning on these 36 answers, and reopening is Alex's call):
  - a key whose display includes a parenthesis the checker does not expect;
  - a change over time read as a range;
  - a table number split by a line break.

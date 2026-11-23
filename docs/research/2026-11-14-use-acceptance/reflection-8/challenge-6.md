# Deep council, round 6: Alex's ruling D654, passage v5.5, and the paired test, rewritten per your round 5. Consent to send?

## Alex's ruling (D654, 2026-11-17)
- **The question put to him** (your round-5 wording): should a topic that names a total with one kind's share, a volume with whether supply stays
  short, or demand with whether capacity keeps pace, without saying which is main, always be asked as the total, volume or demand, with the other side
  as context? Or should the model decide from the topic and decline when that stays unclear?
- **The options:**
  - the general rule (recommended);
  - only the cases he ruled on;
  - no rule.
- **The cost given:** a topic that really tracks the share could be asked as the total. The mitigation given: "题目追的就是份额本身时，就问份额".
- **Alex: "立通用规则 (Recommended)".** Recorded as D654 in `docs/DECISIONS-log.md`.

## The passage, v5.5 (`narrow-d436/edit.json`; inputs frozen read-only in `narrow-d436/audit-v55-inputs/`, sha256 beside them)
- **The system text:** D654's three shapes in its own words, each with two examples from industries outside the 44, plus the share counter-case with
  two examples. It adds 1,280 characters (9,545 to 10,825; o200k tokens 2,031 to 2,294).
- **Two pointers to the same exception,** where the request restates the decline case:
  - the closing check: "(the figure the outcome tracks, when it also names one of that figure's second sides; the share, when the outcome tracks
    the share itself)";
  - the `no_ladder` description: "a figure the outcome tracks, named with one of its second sides as the system text lists them, is one thing".
- **`cut_review`:** every part of the request was read for a cut or merge (system lines, closing, schema, payload, retry note). Nothing is cut, because a
  cut is its own lever.
- **`scope_rule`:** the passage carries D654's words only; a case those words do not plainly name is reported, not decided.

## Audit rounds after D654 (both families, fresh auditors each round)
| Version | Codex auditor | Claude auditor | Changed next |
|---|---|---|---|
| v5.1 | NOT SOUND: one example a shape; u3/clean-10's easing side | SOUND | two examples a shape; easing wording |
| v5.2 | NOT SOUND: the vaccine example mirrors u3/clean-10; cut review not shown | void (I replaced its files mid-read) | fertilizer; merged examples; cut review |
| v5.3 | NOT SOUND: easing wider than D654; no_ladder and closing restate the decline case without the exception; cut review partial | void (same error) | pointers; full cut review; inputs now frozen per audit |
| v5.4 | NOT SOUND: easing wider; capacity added not plainly supply; port volume may be throughput; pointers say "names" and drop the share exception | NOT SOUND: the closing pointer drops the share exception (u3/clean-11 could be corrected to the total) | v5.5 |
| v5.5 | **SOUND** (`narrow-d436/audit-v55-codex.md`) | **SOUND** (`narrow-d436/audit-v55-claude.md`) | record hygiene only (below) |

**The easing form and u3/clean-10:**
- The families split three times on whether D654's words reach u3/clean-10 (capacity added, "easing the shortage").
- I took the narrower, reversible course:
  - shape (b) is D654's literal "whether supply stays short of demand";
  - u3/clean-10 is sent in all three draws and reported, not deciding.

## The paired test, rewritten per your round-5 points (`narrow-d436/paired_probe.py`)
- **Targets (deciding), 3 passes each:** acc/clean-8, acc/clean-9 and pool-17.
- **Reported, not deciding:**
  - u3/clean-10 (3 passes), per the scope rule;
  - u2/clean-10 (2 passes): its decline is defensible but ambiguous, your round 5.
- **Decline controls, 2 passes each:** week c1/clean-4, week c1/clean-12, fortnight c1/clean-8, pool-19 and u1/clean-9.
- **Share control, 2 passes:** u3/clean-11. It must not ask the total. Either of its two splits is allowed: you said D654 does not choose between them.
- **Exercise:** frozen-arm "no ladder" only, at least 5 of the 9 target sends, falling on at least 2 of the 3 targets. Otherwise the result is
  INCONCLUSIVE.
- **PASS needs all of these:**
  - every edited target send is a question with no hard-line fault from either family;
  - no material defect of kind (i) wrong side, (ii) invented measure or (iii) second side dropped, from either source reviewer (`review-brief.md`; the
    frozen arm's written answers are mixed in blind);
  - every edited decline control is a decline that neither family marks unjustified;
  - both edited share sends are questions, with no kind (i) and no hard-line fault;
  - no edited send is lost.
- **Not deciding:** due-day defects (iv) are reported, and a pass is not a claim of sound production questions.
- **Not measured:** a stopped draw, a missed planted control, or a review row without a valid defect list.
- **Code checks at $0:**
  - `check` passes (the edited request is the frozen astra request plus exactly the passage and its two pointers, on all 11 topics);
  - `test_paired_probe.py` has 11 verdict-path tests;
  - `test_paired_probe_send.py` dry-runs all 6 draws through the real runner and spend limit with stored astra answers, then builds the reading (58
    items in 3 packets) and the source-review packet.
- **Cost, priced from stored astra tokens on these topics** (38 requests: input mean 5,187, output mean 196; $10/$50 per million):
  - about $0.041 a send with the system text cached, about $2.15 for the 52 sends;
  - the D652 diagnostic measured $0.034 a send;
  - $0.062 a send if nothing is cached, about $3.2.
  - The cap is $3.60, shared by both arms. The runner's first-request projection plus room stops a run before a draw that would not fit.
  - Alex's remaining testing authorization is about $4.34.

## After the v5.5 audits (record only, the passage unchanged)
- The Claude auditor found two record problems:
  - `audit-topics.json` still listed u2/clean-10 as a deciding control, while D654's Next line and `paired_probe.py` make it reported. The topic file now
    agrees.
  - A stale source line on the removed easing wording is now dropped from `edit.json`.
- `check` passes again, and all 13 tests in `narrow-d436/` pass.
- **Not taken:**
  - the optional fertilizer wording ("whether its fertilizer stays short of demand"), since it moves no listed topic and would need a new audit round;
  - a pointer on system line 6, since both auditors read line 6 as qualified by the passage directly above it.
- **pool-17's text** was not in the Claude auditor's permitted files. The Codex auditor read it.

## Questions
1. Is v5.5 ready to send, with both v5.5 auditors SOUND?
2. Is the rewritten rule right, including u3/clean-10 reported and the exercise rescaled to 3 targets?
3. Is the budget right, with the uncached worst case?

Answer CONSENSUS (send) or DISAGREE with the smallest change.

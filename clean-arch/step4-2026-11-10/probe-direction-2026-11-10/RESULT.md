# The three-arm probe: result (2026-11-10)

96 of 96 first answers stored, none incomplete; $0.0737. An exploration at three draws a cell: it shows mechanisms and
signals, no rate, and nothing here passes or fails a line of Stage A. What it would report and decide was written before the
send (`REGISTERED.md`); the two readers' judgement of the texts was written and sealed before the send
(`direction-key/SHA256SUMS`). Files: `result/cells.txt`, `result/checks.txt`, `result/events-blind.txt`,
`result/events-my-read.md`, `result/direction-key-by-thesis.json`; answers in
`poc/data/clean-ladder-stage-a-2026-11-10/probe-direction/answers.jsonl`.

## S1. Did the reference change move a direction? No signal

| thesis | old request | reference (D411) |
|---|---|---|
| u3/clean-8 | higher, lower, lower | lower, lower, lower |
| u1/clean-7 | lower ×3 | lower ×3 |
| u2/clean-6 | lower ×3 | lower ×3 |
| u1/clean-1 | lower ×3 | lower ×3 |
| acc/clean-3 | lower ×3 | lower ×3 |
| acc/clean-1 | higher, lower, higher | lower, lower, higher |
| acc/clean-7 | higher, lower, lower | higher, lower, lower |
| acc/clean-5 (a quarter) | declined, declined, higher | higher, declined, higher |

No thesis gives one end in all three answers of the old arm and the other in two or three of the reference arm: the
registered signal did not fire. The small send's "higher" for u3/clean-8 is also found in the old request sent in the same
run, so it is not the new request's alone. Three draws cannot exclude that the change shifts how often it happens.

## S2. Did the reference change move the events? No signal

Read without the arm's name (`result/events-my-read.md`): faults in 2 of the old arm's 12 answers (a wait written as a
ruling out, in u1/clean-3 and u1/clean-12) and in 1 of the reference arm's 12 (no ruling out, u1/clean-12). Both faults the
small send showed occur in the old request sent in the same run. One reader, the author, read these blind; that a ruling out
written without "after" is governed by code's sentence rests on the earlier with-and-without reading by two readers, not on
the judge. The object also wobbles in both arms: the H200 sales
permit (u2/clean-3) is under the company in 1 of 6 answers here and was under it in 3 of 3 in the second run; so the second
run's count of one mixed thesis in 16 understates the class.

## What the working checks say of the two arms' first answers

| | old request | reference (D411) |
|---|---|---|
| first answers | 36 | 36 |
| of them ladders | 34 | 35 |
| a first answer a check would send back | 15, all for the quotation | 6: 5 for the quotation, 1 for a last-reported 25 billion below a middle range of 30 to 40 billion |

The quotations of u1/clean-7, u1/clean-11 and u1/clean-12, refused in every answer of the old arm, are exact in the
reference arm (one exception); the reference arm's own refusals are on the two theses that had no reference before
(acc/clean-1, acc/clean-7). A difference worth watching, seen twice now (the small send: 0 of 18); first answers only, so it is no measure of what
the working path with its resend costs.

## S3. Does `unclear` do what the option claims? Not by the registered test

The key, from the texts alone, before any answer:

| thesis | Codex reader | Claude reader | arm `unclear` | arm reference |
|---|---|---|---|---|
| acc/clean-7 | both argued | both argued | unclear ×3 | higher, lower, lower |
| acc/clean-3 | both argued | both argued | lower, unclear, unclear | lower ×3 |
| u2/clean-6 | both argued | both argued | lower, unclear, lower | lower ×3 |
| acc/clean-1 | higher | nothing said | unclear ×3 | lower, lower, higher |
| u1/clean-1 | higher | both argued | unclear ×3 | lower ×3 |
| u1/clean-7 | higher | both argued | unclear ×3 | lower ×3 |
| u3/clean-8 | higher | both argued | unclear ×3 | lower ×3 |
| acc/clean-5 (a quarter; both readers) | higher | higher | higher ×3, never declined | higher, declined, higher |

- The registered test asked for `unclear` in 3 of 3 on every thesis the key calls not settled. It fails on two of the three
  theses both readers call not settled (acc/clean-3, u2/clean-6: "lower" in one and in two answers).
- The two theses that gave both ends in both full runs (acc/clean-1, acc/clean-7) give `unclear` in 3 of 3. Theses with one
  value in all three answers: 6 of 8 in the arm, 5 of 8 in the reference arm, 4 of 8 in the old arm. The wobble moved to two
  other theses; it did not go.
- With `unclear` allowed, five of the seven obligation theses lose their direction in every answer and the other two in some.
- The arm wrote a ladder for the quarter (acc/clean-5) in all three answers, where the reference arm declined once and the
  old arm twice. Three draws; shown, not explained.
- The arm tested only whether the model returns the field the same way. A company ladder with no direction was never put
  before the judge.
- **What the key itself shows, apart from the arm.** For the seven obligation theses neither reader finds the texts settling
  "lower" in any; one finds "higher" in four (the article praises locking in supply, or says the credit model speeds
  adoption) and the other finds both ends argued or nothing said. The working request answers "lower" in 19 of its 21
  first answers on them. The readers were asked what the texts say; the request asks the model what is good for the business,
  which an analyst may infer from an obligation's weight without the article saying so. So the key does not show "lower" to
  be wrong, nor "higher" to be right: it shows that the direction of an obligation's amount has no stable footing in the
  texts, and that readers of the same texts part on it.

## Who reads a company ladder's order and labels in production (searched at no cost)

"Position 1 is Strongly bullish" is not the ladder step's own convention. A company figure shown without it would meet:

| reader | what it does | file |
|---|---|---|
| the thesis writer's check | refuses a five-rung company ladder whose labels are not Strongly bullish to Strongly bearish, in that order or reversed | `src/hivemind/extraction.py`, `check_ladder`, `normalise_ladder` |
| the successor rule | stores a later year's ladder in its predecessor's direction, read from the order of the numeric bounds | `src/hivemind/views/writing.py`, `oriented_like`; `views/matching.py`, `ladder_direction` |
| the judge's page of a thesis | shows each rung as "rung <position> <label>: <condition>"; judging-v7 itself has no bullish or bearish word | `src/hivemind/views/judging.py`, `_lines_english` |
| dependencies | a dependent states "first_is_bullish" or "last_is_bullish" of the thesis it depends on | `src/hivemind/vocabulary.py`, `DIRECTIONS`; the matching prompts |
| the idea prompts | "Five-rung asset ladders run from bullish to bearish" | `src/hivemind/prompts/idea-v11.txt` and later |
| the page | a company thesis is drawn by position, a theme thesis by the size of its numbers | `poc/ui/src/adapters/bundle.js`, `legacyScores` |

So any option that shows a company figure without a direction changes the thesis library's contract (D38, D186) in these
places, all of them in the frozen configuration. It is not a change of the ladder step.

## What follows

- The reference change (D411) is carried, with the risk named: the registered signals did not fire at three draws on twelve
  theses.
- The favourable end of an obligation's amount is not a defect of wording. Asking the model for it gives an answer the
  texts do not hold; letting the model say `unclear` moves the wobble. This is a choice about what the product registers
  (D186), so it is Alex's, with this page as its evidence.

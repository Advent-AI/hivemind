# Architecture benchmark: results and reading (2026-11-06, revision 8 after Codex rounds r16–r22)

Design: `../benchmark-design.md` (revision 7, agreed with Codex after rounds r7–r15; hashes verified at launch). Scores: `window-measure.txt` and
`bench_measure.py --test`. Readers: `miss-window-*.out`, `miss-test-*.out`, `blind/questions-reader.out`, `blind/records-reader.out` (keys kept
apart from the readers). Probes: `../probes/`. All twelve draws finished; one split window draw was resumed once after a frozen-judge refusal
(review-log, "Benchmark running").

## 1. Numbers (regressions first; three draws each)

Window, golden-v5 dev, the product point (ledger records):

| Quantity | Split | Control | Difference of means | Same-configuration range (6 stored control draws) |
|---|---|---|---|---|
| Helpful matters reached (of 237) | 156, 156, 159 | 166, 170, 162 | **−9.0** | −8 (19 of 20 splits) |
| Core reached (of 86) | 71, 75, 76 | 76, 76, 75 | −1.7 | −3 |
| Judgement agreements, 22 seeds | 16, 13, 15 (44) | 16, 15, 16 (47) | −3 | −3 |
| Not-kept gold entries written | 23, 32, 29 | 29, 34, 34 | −4.3 | — |
| Extras (matching no gold entry) | 30, 41, 35 | 53, 63, 54 | −21.3 | — |
| Statements from gold articles | 238, 253, 245 | 277, 300, 287 | −42.7 | — |
| Questions opened from articles | 19, 14, 11 | 2, 6, 4 | +10.7 | — |
| Cost (USD, upper bound) | 1.07, 0.98, 0.92 | 0.78, 0.84, 0.92 | +0.14 | — |

- The extraction stage (checked handovers) gives the same picture: helpful 156, 156, 159 against 167, 171, 162. The split's lost matters are all
  lost at the extraction stage ("not handed over" 81, 81, 78 against 70, 66, 75); the control also loses one handed-over matter after the handover
  in each of its first two draws.
- Every split draw is below every control draw on helpful matters (the lowest control draw is 162; nine control draws exist: 161–179).
- **The window stop line fires on helpful matters (−9.0 against a −8 range).** Core and judgement are within range; judgement sits on its edge.

Test articles, golden-v5 test, extraction stage:
- helpful: split 24, 27, 23 against 21, 26, 23;
- core: 8, 8, 8 against 8, 7, 7;
- not-kept written: 8, 7, 4 against 4, 9, 7.
The split is not below the control here.

Judgement questions that drop by two or more: v9 (split 1/3, control 3/3) and v10 (split 0/3, control 2/3). v22 rises by two (split 2/3,
control 0/3).

## 2. What the readers found

Every missed helpful matter, per draw, read by independent Codex readers (window):

| Where the miss happened | Split (240 missed draws) | Control (213) |
|---|---|---|
| The model did not write it | 192 | 116 |
| Written, then dropped by a code check | 21 | 60 (the frozen filing's "no home") |
| Present in other words (the counting aid missed it) | 18 | 20 |
| Not processed (merged copy, outside the feed) | 6 | 6 |
| Lost after the handover | 0 | 2 |
| Gold question (recorded, not applied) | 0 | 6 |
| Unclassified (one article with no archived answer, handover or step, marked unread) | 3 | 3 |

The counting aid errs about equally for both arms (18 against 20), so the gap is in what the arms write.

Test articles, the same readers: split 64 missed draws (58 not written, 5 dropped by a check, 1 present in other words); control 68 (29 not
written, 36 dropped by the frozen filing's "no home", 3 gold questions).

Samples read blind (twenty of each kind and arm, fixed seed):
- Hits: 20 of 20 in both arms are the gold matter, so the counting aid's hits hold.
- Extras (records matching no gold entry):
  - control: the standard would keep 11, not keep 3, unsure 6;
  - split: keep 10, not keep 2, unsure 8.
  About half the extras are statements worth keeping that the gold does not list. Fewer extras is fewer unmatched statements, not that much less
  noise.

New questions opened from articles:
- with a ladder: split 9 of 19, 8 of 14 and 4 of 11 (numeric 1, 3, 0); control 2 of 2, 6 of 6 and 4 of 4;
- with a due day: all of them in both arms. The split's are all analyst check dates; the control's come from the source.
A question without a ladder cannot be placed on a rung by the daily judging.

Blind reads (arm hidden):
- Article-opened questions: split 44, of which 25 the standard would open, 17 not, 2 unsure; control 12, of which 6 would open, 6 not. Duplicates
  of an open question: 0 in both. The reader's reasons for the split's 17:
  - a period, basis or figure the source does not give (10);
  - the same US$500 million investment, too small to move revenue, profit, cash or credit risk, once a draw (3);
  - a company share on a calendar year instead of the fiscal year (2);
  - a product question asking for the launch, not the first shipment (1);
  - no stated effect on the business (1).
  Two more the reader marked unsure.
- Twenty stored records each:
  - helpful: 17 in both arms;
  - summary wrong: split 7, control 10;
  - links wrong: 6 in both;
  - attribution errors are similar (original speaker 5 against 6, statement day 3 against 1, tier 8 against 7).
- Disclosed limit: the question packet hides the focus line, due day and research ids, but a split ledger lists more open questions before each
  question.

## 3. Mechanisms (traced, then proved on stored requests)

**M1 — the split's evidence call writes fewer statements.**
- Of the 27 helpful matters the split missed in at least two draws while the control reached them in at least two, the readers put the split's 64
  missed draws down as 51 not written, 6 dropped by a check, and 7 present in other words. In one case, the revenue-sharing and credit-support
  partnership was present in all three split draws although the counting aid missed it.
- The control filed these matters under specific seed questions (v17 China share, v18 Rubin Ultra and others) and, for 38% of the filings, under
  the company-wide revenue question v1.
- B's own account on four stored requests:
  - it applied the closing check's exclusions too broadly (a competitor's stockpile treated as background);
  - it read the link rules narrowly ("shared names or an ecosystem alone do not establish it"; "Do not infer that two named programmes are
    identical"; "When no supplied question is connected, leave links empty").
- First hypothesis, refuted: B's system prompt says "When no supplied question is connected, leave links empty", which contradicts its own links
  field (the adopted fallback, D273/D361, plan decision 2); the frozen request carries only the fallback. Replacing that one sentence with a
  deferral to the field, on the 20 items behind the 27 matters, two sends each, showed no improvement on these selected sends (stored 13, 11 of 27;
  changed 12, 10) and wrote more not-kept entries (8, 6 against 11, 10). The contradiction is real and is recorded. These sends do not show it
  driving the loss, and they do not rule out an effect elsewhere.
- Second hypothesis, flipped: B's system prompt (split-b-v1, copied from the older structure-v2 text) was replaced by the frozen production role
  role-v74i, with the user text and schema unchanged. On the same 20 items, two sends each, the results moved:

  | Quantity (two sends) | Stored B prompt | Frozen role |
  |---|---|---|
  | Lost matters recovered (of 27) | 10, 10 | 18, 21 |
  | Helpful | 57, 58 | 73, 77 |
  | Statements filed | 70, 68 | 102, 106 |
  | Not-kept written | 5, 6 | 12, 12 |
  | Extras | 3, 1 | 8, 4 |

  Read as what it shows: B's instruction block moves these answers.
  - The 20 items were chosen because the split missed matters on them, so some recovery on any re-send is expected; the stored prompt recovered
    10 in both sends.
  - Two sends on a selected set do not give a full-window effect.
  - The probe checks source quotes and non-empty links, not whether the links are right.
  - The whole frozen role also asks for questions B's schema cannot return, so the text tested is not a text proposed.
  - Not-kept entries rose (5–6 to 12), and unjudged extras rose (1–3 to 4–8).
- The prompt audit (`prompt-audit.md`, class 1) and its blind second reader (`prompt-audit-b-reader.out`) independently name the same sentence:
  B's first task, "find article statements that help answer an existing question". It keeps narrower than the standard's keep rule, which keeps
  what an analyst would note and files it after (D207, D209); the frozen role states that order. The second reader adds two more:
  - B's background exclusion ("a partnership, contract, plant or investment" dated earlier, "even with its amount") can pull against newly
    reported figures;
  - the figure exceptions ("revenue, capacity, orders or contracted amount") read like a closed list.

**The two judgement drops**, read by an independent reader (`judgement-drops-reader.out`):
- v9 (financing commitments and backstops; gold $25–60 billion):
  - split draw 2 lacked the record of Firmus's target of up to 170,000 GPUs, which the agreeing control draws used to size a Firmus estimate;
  - split draw 3 had comparable records and discounted that estimate by 50%, where control draw 3 used 25%;
  - split draw 1 agreed.
  Records under v9: split 9, 20, 19; control 34, 31, 31. In split draw 1, the new question v23 (credit-support arrangements) took 10 of its 12
  backstop records; in draws 2 and 3, v23 is the Ohio guarantee question and most backstop records sit under v9. **The new questions are not shown
  to cause the two losses.** The missing dependency between a new driver and its root (D51) remains an open concern, not a proven cause here.
- v10 (non-GAAP operating margin; gold 65–69%):
  - all three split draws lacked the record that puts NVIDIA's operating margin at about 66% (a comparison with Micron);
  - both agreeing control draws anchored on it, and the disagreeing control draw also lacked it.
  The loss follows a record B did not write (M1). Whether that one record alone would have changed the split's answer is unknown.

Other findings with their census:
- B joined separated paragraphs into one quote (test: 1, 1, 2 per draw; the SpaceX financing core matter in 3 of 3 test draws). The frozen sift
  refuses the same quote. It is a misread where two existing rules meet; the class is small.
- Frozen-judge refusals per draw: split 3 (d1, one stop), 5, 6; control 7, 10, 7. The same frozen code in both arms.

## 4. Reading (revision 2)

1. The stop line fired: the split as built (poc-split-v3) is not to be promoted, and the line goes to Alex (D355).
2. On what the split was meant to change:
   - 0 duplicate questions, as in the control;
   - more questions the standard would open (25 against 6 over three draws), and also more it would not (17 against 6), with reasons that point
     at the new-question call's prompt (class 4 of the audit, not yet audited sentence by sentence);
   - half its new questions carry no ladder;
   - fewer unmatched statements, about half of which, in both arms, are worth keeping.
3. The helpful-matter loss is in what the evidence call writes (M1). The strongest lead the audit and its blind second reader identified is B's
   first task sentence, which makes connection to an open question the first test of a statement, against the standard's keep-then-file order.
   How much of the loss it explains is not measured. The probe shows that B's whole instruction block moves these answers; it does not prove a
   particular sentence or an edited text.
4. One recommendation: **B's request is revised from the standard's keep rule**, not from the failing articles. This is a new version of the split's
   evidence call; the frozen production prompt is not touched.
   - Keep first, file second, as the standard states it: a statement an analyst would note is kept, then filed under the narrowest open question
     (D207). With no home it is dropped and read at evaluation (D209), and the relevant question need not exist yet.
   - The "existing question" task sentence and the "leave links empty" contradiction are cut.
   - Every sentence the audit and its second reader flagged is reconciled with its exact standard boundary, including the sentences of B's copy of
     the closing check (the background exclusion "even with its amount", the figure exceptions read as a closed list). The rule that keeps old,
     known background out stays. A newly disclosed fact is not excluded only because the arrangement already exists; it is still judged by the standard
     (would an analyst note it, does it move a question's answer) and its other boundaries. The complete schema is read with the request.
   - The prompt does not grow (characters and tokens reported before and after).

   **One test, fixed before any send.** It is a screen that decides whether the whole benchmark is worth running. It accepts nothing.

   One rule governs every condition: each is first applied to the current request against itself, on the same day, and must judge it as it
   should judge a version equal to the current one:
   - condition 1 must find no gain;
   - conditions 2 and 3 must find it within bounds.
   If a self-check judges otherwise, the test reports "not decidable" for that condition and stops; no line is widened after the fact.

   - Set, fixed now (`next-test-set-20261107.json`): 40 golden-v5 dev articles drawn with seed 20261107 from the 118, without regard to this
     benchmark's misses, plus all 30 golden-v5 test articles. Coverage of the 40:
     - 29 hold helpful matters: on 6 the split reached all of them in every draw, on 23 it missed some;
     - 9 hold a matter the split lost against the control, and 4 one it gained;
     - 11 hold no helpful matter in the gold; what a version adds there is still judged by the standard.
   - Sends, all on the same day, on stored requests of the same articles:
     - the current B request six times (C1–C6);
     - the revised B request three times (R1–R3);
     - the frozen production extraction three times (P1–P3), on its stored requests from control window draw 1 and test draw 1.
   - Counted per send: helpful matters reached (D372), not-kept entries written, unmatched additions, links per statement.
   - Blind reads, mixed and arm-hidden, 20 unmatched additions and 20 links per pool, drawn with seed 20261107. The pools are R1–R3, C1–C3, C4–C6
     and P1–P3. A pool with fewer than 20 is read whole and compared as a share. A pool with nothing to read makes its condition not decidable.
   - Noise on this set: S_h is the largest difference of mean helpful reached over all ten three-against-three splits of C1–C6; S_n is the same for
     not-kept entries. Six sends give a rough estimate only.
   - Three conditions. The revised version passes the screen only if all three hold:
     1. Gain: the mean helpful reached of R1–R3, minus that of C1–C3, is more than the larger of 3% of the set's helpful total and S_h.
        - Self-check: C4–C6 against C1–C3 must show no gain. It cannot, because no split difference exceeds S_h, so this self-check always holds.
        - What this proves: a gain larger than any difference the current request shows against itself on this set. If S_h is above 3%, the
          screen can only confirm gains above S_h.
        - If S_h is above 6%, the screen cannot separate the gap measured on the window (3.8%) from noise, and reports "not decidable".
     2. Not-kept: the mean not-kept entries of R1–R3 is at most that of P1–P3, the same-day production, plus S_n.
        - Self-check: C4–C6 against C1–C3 by the same rule. The arithmetic makes it pass whenever the current request is at or below production.
        - If the current request is already above production by more than S_n, the condition is not decidable.
     3. Blind quality and volume:
        - (a) R's share of right links is no lower than that of C1–C3 by more than 10 percentage points.
        - (b) R's estimated additions the standard would not keep per send is no more than P's. The estimate is mean unmatched additions times the
          pool's share the reader does not keep: the split must not be noisier than same-day production on what the gold does not list.
        - Self-check: (a) and (b) are applied with C4–C6 in place of R. If either fails, condition 3 is not decidable.
   - Result:
     - all three conditions hold: the revision is put to Alex for the whole benchmark;
     - any condition fails: the revision is not adopted, and the census of the failure is reported;
     - any condition is not decidable: the screen says so and stops.
   - A send that returns no answer for an article makes the screen not decidable until it is re-sent.
   - This check proves the change on a subset; a prompt change is accepted only on the whole benchmark (AGENTS §7.3): three split window draws and
     three same-day control draws under this design, started only on Alex's word.
   - The new-question call (audit class 4) is audited next, on its own.

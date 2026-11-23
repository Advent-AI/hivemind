# Council v, challenge round (read-only; do not edit files or run model calls)

My own reflection, written before I read yours, is `clean-arch/step1-unfiled-2026-11-08/council/v-claude.md`. Read it.

**New $0 evidence on Step 2 line 2** (`poc/data/clean-step2-forward-2026-11-08/merge-wrong.json`, records rebuilt by `run_forward.step1_records`):

| Wrong merge | Earlier record | Later record |
|---|---|---|
| X59 | 49:e1, joined passages 1,097 characters | 71:e3, 170 |
| X64 | 49:e1, 1,097 | 72:e2, 153 |
| X30 | 24:e3, 214 | 42:e3, 162 |

- In 49:e1 the NVL576 claim sits at character 951, past the 600-character cut. **But the summary states it**, and Jev reads the
  summary in full (`compare.piece_text`). So the cut did not hide it.
- X59 and X64 come from a bundled record: one Step 1 item states both the NVL144 and the NVL576 delay.
- X30 has short passages: a Jev figure error ($253bn → $392bn path against 82%/41% growth).
- Overlaps: 7 of 15 involve a record over 600 characters, against 43 of 104 among all merges. That is not enriched.
- **Conclusion:** the cut explains 0 of the 3 wrong merges. Fixing it is a latent-defect fix, not the line-2 fix.

**Where we agree:**
1. Status as you wrote it.
2. Mechanisms 1–3 and 5.
3. The next angle: conditions in their smallest form, after a full prompt audit against Alex's rulings.

**My points to challenge:**
1. **The concrete minimal form (c2).**
   - K6b unchanged except: the `condition` field; one CONDITION bullet (a useful company figure judged in context, with Alex's cash case
     as the boundary example; forward plans and estimates kept per D371); and the do-not-open row "a measure's level, growth or
     guidance with no reason is a condition" (Alex's reframe).
   - **No** c1 sentence "a measure with a reason the item supports is a view", **no** "big matters include a reason", and K6b's linking
     restored everywhere.
   - You wrote "require a supported reason for a new view". Is that already K6b's rule ("its own scale can change …", the separate-bet
     test), or does it need a new sentence? A new sentence is a lever; name its source.
2. **The falsifiers**, fixed before the send, over 16 cases × 3 draws against the same control:
   - margin under the revenue view at least 4/6;
   - cash dropped at least 2/3;
   - at most 1 extra thesis;
   - gold not-kept at most the control + 3;
   - 0 figure-only theses in empty-40 and empty-57;
   - EPS kept at least 5/6.
   Are these right, and is the case set enough to guard every class the change can move? Should a test-set miss be added? The test set
   is exposed, and I lean no.
3. **Step 2 line 2.** Two of the 3 wrong merges come from one bundled Step 1 record.
   - Is the fix at Step 1 (one claim per item where the claims can move apart, D248), at Step 2 (Jev told to judge against the group's
     whole record), or nowhere, because the third reader's "wrong" on a record that states both claims is debatable?
   - What is the cheapest decisive check, and does it belong before or after c2? Alex's scope is Steps 1–2, so it is in scope.
4. **The order of work, one recommendation for Alex.** I propose c2 first: Step 1's test miss is the largest product loss, and 6 of
   the 7 unfiled misses would be recovered if kept. Step 2 line 2 comes after. Do you agree?

Answer in English, under 600 words. End with the agreed lessons (at most five lines), the agreed next step with its falsifier, and any
remaining disagreement.

# A new reference for the final-answer test's control line (D658): design, version 2, for council review ($0; nothing run)

**In one line:** answer the 15 control questions, plus Ohio listed apart, as the new system asks them. The answers come from the frozen
ruler's own 14-day material and brief, written by two blind readers of two families. Code assembles everything, and every disagreement goes to
Alex with the third readers' reasons. Alex signs, the reference is frozen, and only then are the judge's stored answers scored, by a scorer fixed
before any reader runs.

Version 2 answers the two independent reviews of version 1 (`council-codex-1.md`, thread 01a1ebb0-9724-7e51-a979-bae88cb9cba9; the Claude-family
review, condensed in `council-claude-1.md`). Both read version 1 NOT READY. The changes are listed in §9.

## 1. What Alex decided, and the material

- **D658** (Alex: "第一条ok, 仔细的跑run council review"). The option he chose read: "按新系统实际出的这 15 道题，重写一份标准答案（推荐）：请两组没参与造这个系统的审查者，用同样的材料各自独立作答…你看过签字后冻结，再拿判答案那一步的结果去批一次".
- **"同样的材料" is the frozen ruler's material,** the material the old reference was written from: `packet-v1.json` (golden-v5's 309 items, sha
  `53d1e8b4…`).
- **D658's record line "written from the complete material the judge is shown" is my paraphrase of AGENTS §7.1, not his option,** and it contradicts
  the option. His option governs ("check it against his raw messages, not against a log you wrote", AGENTS, Authority and scope). The correction is
  recorded in D659.
- **Why the packet, not the evidence the judge was shown:**
  - **The packet measures** whether the judge's last answer lands where an analyst would land after reading everything collected for the window.
    It is the same for all three draws (ruler-v1: "账本随每臂变，尺子不能随臂变").
  - **The material-shown filter** (§4) keeps only controls whose decisive items reached the judge. That separates the judge's reasoning from
    delivery.
  - **The judge's own evidence** would measure whether the answer follows from what it saw. Stage B's per-judgement readers already measure that
    (`STAGE_B_READING.md`).
  - **The packet cannot see** statements the judge saw that the packet lacks, delivery (a control whose items were not shown drops out), or
    questions read as no_view.

## 2. What this piece is

A new piece beside the frozen ruler (AGENTS §7.1), never an edit of it.
- **Its own unit:** 16 questions. They are the 15 controls (c01 to c15) and Ohio (c16, listed apart as today), each a question as the system wrote it
  in one draw, judged at the window end 2026-07-14.
- **Kept from the frozen ruler:** the material, the brief, the fields and the agreement rule. Old scores are never compared with it.
- **Its own name and version:** `control-reference-v1`.

| Piece of the line | Today (D428 line 3) | Under this design |
|---|---|---|
| The reference answer | Reader B's frozen answer to the seed question | The new reference's answer to the system's own question |
| Same question, same due day | Two readers and third readers | Holds by construction |
| Material | `packet-v1.json` | the same file, copied and sha-checked |
| The analysts' brief | `reader-brief.md` | the same file, copied byte for byte. The question file is named `questions-v1.json` inside the readers' folder, so the brief's file names hold (its content: the 16 questions). Its example id "q01" is a shape example; the ids are c01 to c16 |
| Agreement (a figure) | The chosen rung's band overlaps the reference range | Unchanged |
| Agreement (an event) | Yes against yes; "Ruled out" or "Still open" against no | Unchanged; the limit in §6 is stated |
| Material shown | Every decisive item shown by 2026-07-14 | Unchanged rule, by an items-only brief (§4); an empty or one-item list never counts as shown |
| Threshold | At least 8 controls with material shown; all but one agree; Ohio apart | Unchanged |

## 3. The procedure, fixed before any reader runs

**The access boundary:**
- **Claude has already seen the stored judgements.** It read the 17 a reader called UNSUPPORTED, and `control-census.txt` lists each control's
  agreement with reader B. So the protection cannot rest on Claude not having seen them.
- **Claude writes no reference content.** Code builds every file a reader, a third reader or Alex sees. Claude only runs code and passes on the
  handoffs code generates.
- **No file shown to any participant carries a judge's answer, a chosen rung, a judgement reason or a stored agreement.** Code checks every packet
  it writes against the stored judgement rows, and refuses any packet that names a chosen rung or a judgement's text.
- **The steps:**
1. **Build** (code, `build_control_reference.py`).
   - From the stored ladders it copies only question, unit, year, due day, rungs and kind. It never copies the ladder's reason, reference_status or
     checked answer.
   - It refuses a figure ladder with a gap, an overlap or an unbounded middle rung. There are none today: all six figure ladders are contiguous.
   - It writes the readers' folder `poc/data/clean-control-reference-2026-11-17/readers-input/` holding exactly three files: `reader-brief.md` and
     `packet-v1.json`, each a byte copy with its sha checked against the frozen file, and `questions-v1.json` with the 16 questions.
   - The draw and thesis behind each question are kept in `keys/` outside the readers' folder.
2. **Readers.**
   - **A** (Codex, `codex exec -s read-only -C <readers-input>`) and **B** (a Claude-family subagent) each answer all 16, independently, in fresh
     sessions.
   - Each is told to open only the three files. A's command log is checked for any other path. B's handoff names only the folder.
   - **Validity** is defined now by a code schema: the brief's fields; a figure's low ≤ high in the question's unit; an event's yes_no set; and,
     unless no_view, at least 2 decisive items that exist in the packet (the brief asks "2–6").
   - An invalid row is asked again once, in the established wording. Both rows are kept. A row still invalid makes that question unresolved, and it
     goes to Alex.
3. **Reconcile** (code, then readers).
   - Code compares the two readers per question: figures overlap or not, yes/no equal or not, no_view on either side.
   - **The proposed reference is reader B's answer as written.** This is the D262 precedent, and a stronger reason applies here: the judge is
     gpt-6-luna (OpenAI), the same family as reader A, so B is the only reader outside the judge's family.
   - Every disagreement goes to two third readers, one of each family. They see the packet, the brief, the question and both answers, on sides
     drawn by a fixed seed. Each rules **A**, **B** or **neither** (giving its own range or yes/no with items), citing item ids. Code writes their
     prompts.
   - **Nothing is replaced automatically.** All disagreements, with both rulings, go to Alex.
   - **A prediction, written now:** on 9 of Stage B's 12 splits, each third reader sided with its own family's first reader. So most A–B disputes
     here will split and reach Alex.
4. **Alex signs.**
   - The signing page `control-reference-v1-for-signing.md` is generated by code, in plain English. It shows the 16 questions, each reference
     answer with its cited items, every disagreement with both third readers' reasons, and every no_view or unresolved row. It shows no judge
     answer.
   - For each disputed question, Alex picks one of a closed set: A's answer, B's answer, a third reader's answer, or a range or yes/no in his own
     words with items cited.
   - Nothing is scored before his signature.
5. **Freeze.**
   - `control-reference-v1.json` records `reference_version: 1`, both readers' sha256, each question's source (A and B agree, or Alex's pick and
     why), and the label model-authored.
   - Its sha goes into `control-reference-v1.sha256` and the decision. It is never edited: a later defect is a dated correction record printed with
     every score.
6. **Material shown** (after the freeze).
   - A new items-only brief, `control-items-brief.md`. It is the "items" part of `control-reader-brief.md`, with the same-question and same-due
     parts removed because they hold by construction. It is reviewed before use.
   - Two readers, one of each family, mark each of the reference's decisive items shown or not_shown in the evidence the judge's requests listed on
     or before 2026-07-14. Third readers rule the disputes.
   - The readers see the evidence and the items, never the chosen rung.
7. **Score** (code, `control_reference_count.py`, with its tests, written and sha-recorded before step 2).
   - It reads `control_theses.py`'s stored-judgement and evidence functions and edits no frozen file.
   - It refuses a reference whose sha or version differs.

## 4. The count, fixed now

For each control c01 to c15:
- **Excluded, listed as not exercised, with the reason:** no judgement on or before 2026-07-14; no_view in the frozen reference; a reference
  citing fewer than 2 items; material not shown (any item not_shown or unresolved); a figure rung with no bounds.
- **Otherwise counted:** it agrees when the last judgement's rung overlaps the reference range (a figure), or Yes matches yes and "Ruled out" or
  "Still open" matches no (an event).
- **The line passes** when at least 8 controls are counted and all but one of them agree. It is unexercised when fewer than 8 are counted.
- **Ohio** (c16) is scored and printed apart. It never counts towards the 8.
- **Printed beside the verdict:**
  - **The noise.** The line scored against reader A's answers instead of the reference, and the A–B disagreement rate.
  - **Null baselines.** For figures, the lookup baseline (the rung that contains the reference's stated value) and always-neutral. For events,
    always "Still open" and always Yes.
  - **Per matter.** The 15 controls are 7 matters (q07, q08 and q18 three times each; q09 and q13 twice each; q04 and q16 once each), so 8
    controls are not 8 independent tests.

## 5. Predictions, written before any reader runs

- **Under the old reference's decisive items, exactly 8 of 15 controls had every item shown:** u1/clean-3, u1/clean-6, u2/clean-2, u2/clean-5,
  u2/clean-7, u3/clean-1, u3/clean-3 and u3/clean-7 (`control-census.txt`). The new reference may cite other items. One more not_shown leaves the
  line unexercised, and the shortfall is then delivery (D511, D592), not the questions.
- **Most A–B disputes will split by family and reach Alex** (§3, step 3).

## 6. What it does not measure, and its weak points

- **What it does not measure:** whether the system opened the right questions (D1), whether evidence reached them (D2, beyond the shown filter),
  the judge's daily path, or which "no" an event lands on. The yes/no reference cannot tell "Ruled out" from "Still open", so Stage B's pattern 1
  ("Still open" kept because nothing is settled; u2 v5 is control u2/clean-5) is invisible to this line. Lines 1 and 2 of Stage B see it. Keeping
  the brief word for word is chosen over adding a field.
- **Model-authored.** Two model readers, with Alex's signature as the human vote. The noise is printed (§4).
- **One stored run, the luna configuration's questions.**
  - A pass shows the line exercised and met on these 15. It does not pass Stage B, which also missed the strictest last-answer reading.
  - A miss is a finding about the judge, or about the reference, that carries over to any ladder configuration. It stops the line before any further
    spend (D355).
  - An unexercised result points to delivery.
- **Tuning exposure.** If a miss leads to a judge change (D263), these 15 become tuning data, and the next application must be on unseen
  questions.
- **The next application.** A reference for another run's questions, such as astra's, is a new gold and needs its own decision (AGENTS §7.1). This
  design does not pre-authorise it.

## 7. State × event

| Step | Invalid row | A–B disagree | Third readers rule neither, or split | Alex amends at signing | Defect after freezing | Missing or malformed ladder data | Shown check fails or is unresolved |
|---|---|---|---|---|---|---|---|
| 1 Build | — | — | — | — | — | refused; that control is listed not built, with the reason | — |
| 2 Readers | asked again once; still invalid: unresolved, to Alex | — | — | — | — | — | — |
| 3 Reconcile | — | two third readers | both rulings to Alex | — | — | — | — |
| 4 Sign | — | — | Alex picks from the closed set | recorded in his words; the page is regenerated and re-signed | — | — | — |
| 5 Freeze | — | — | — | — | a dated correction record, printed with every score | — | — |
| 6 Shown | — | — | — | — | — | — | not shown; the control is excluded (§4) |
| 7 Score | — | — | — | — | printed beside | — | — |

## 8. Prior decisions read

- **D261, D262** (the frozen ruler; reader B as gold); ruler-v1 §2 (the "desk ruler", D3 in its own numbering); AGENTS §7.1.
- **D428** (line 3), **D430** (a figure's due day).
- **D575, D592** (the shortfall; a new reference is Alex's), **D658** (his choice), **D659** (the material correction).
- **D263** (a gap between system and gold is the system's to close).
- **D355** (a result against the hypothesis stops the line).

## 9. Changes from version 1

- **The material** follows Alex's option text; D658's paraphrase is corrected (D659).
- **The unit** is called a new piece with its own unit (16 questions), not "unchanged".
- **No automatic replacement of B by A.** All disagreements go to Alex, the third readers can rule "neither", and Alex picks from a closed set.
- **The access boundary covers every participant,** and the false claim that Claude had not seen the judgements is removed.
- **Ohio** is c16, listed apart.
- **The count's exclusions are fixed:** no_view, fewer than 2 items, an unbounded rung.
- **Added:** null baselines, the line against reader A, and the per-matter report.
- **The items-only shown brief** is new and reviewed; the old brief is not used unchanged.
- **The scorer** is written and its sha recorded before the readers run.
- **The astra application** needs its own decision.
- **Predictions** are written down.

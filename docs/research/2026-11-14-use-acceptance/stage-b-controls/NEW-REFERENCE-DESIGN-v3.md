# A new reference for the final-answer test's control line (D658): design, version 3, for council review ($0; nothing run)

**In one line:**
- The 15 control questions are answered as the new system asks them.
- The answers come from the frozen ruler's own 14-day material and brief, written by two readers of two families who work with no file and no tool
  access.
- Every disagreement goes to Alex with the third readers' reasons. Alex signs, the reference is frozen, and only then are the judge's stored answers
  scored.
- The scorer and every text any participant will see are fixed by sha before the first reader runs.

Version 3 answers the round-2 reviews: Codex (`council-codex-2.md`, thread 01a1ebb0-9724-7e51-a979-bae88cb9cba9) and the Claude family
(`council-claude-2.md`). Both read version 2 NOT READY. The changes are listed in §14.

## 0. The structural rule that closes the fitting class

The orchestrator (Claude) has already seen the stored judgements, so no step may rest on its not having seen them.
- **Every file, prompt and page shown to any participant** is produced by code. The participants are the readers, the third readers, the
  material-shown readers and Alex at signing.
- **The code and its templates are fixed by sha before step 2,** together with the scorer and its tests (`manifest-v1.json`).
- **Nothing a participant sees is written after that point.** A step whose code or template sha differs from the manifest refuses to run.
- **Every participant works inline,** with no file or tool access, and its log is checked for any tool call.

## 1. What Alex decided, and the material

- **His option, as shown to him** (D658), word for word: "按新系统实际出的这 15 道题，重写一份标准答案（推荐）。请两组没参与造这个系统的审查者，用同样的材料各自独立作答。两组意见不一致的地方，逐条对照原文裁定。你看过、签字后冻结，再拿判答案那一步的结果去批一次。旧标准答案一字不动，几乎不花钱。"
- **The material is the frozen ruler's packet, `packet-v1.json`** (golden-v5's 309 items, sha `53d1e8b4…`).
  - **Sources:**
    - ruler-v1 §1 ("材料：…golden-v5…309 条事项…不用系统的账本（账本随每臂变，尺子不能随臂变）");
    - D658's Next line ("the readers' brief taken from the frozen ruler's definition");
    - D659's correction of D658's paraphrase. The phrase "同样的材料" in the option alone could also mean "the same as each other"; the two
      sources above settle it.
  - **What it measures:** whether the judge's last answer lands where an analyst would land after reading the window's material, on controls whose
    decisive items reached the judge.
  - **What it cannot measure:** statements the judge saw that the packet lacks; delivery (a control drops out when its items were not shown);
    questions read as no_view.

## 2. The piece

A new piece beside the frozen ruler (AGENTS §7.1), never an edit of it.
- **Name:** `control-reference-v1`.
- **Unit:** 15 questions (c01 to c15), each the question the system wrote for one control thesis in one draw of the Stage B baseline (D428), judged
  at 2026-07-14.
- **Ohio is not included,** because Alex's option names 15 questions. The line already excludes it.
- **Kept from the frozen ruler:** the material, the brief file, the fields, and the comparison for figures and for yes/no.
- **Added:** the event outcome field (§4). Old scores are never compared with this piece.

## 3. Inputs built by code (`build_control_reference.py`)

- **The population.** The 15 controls of `control_theses.py` (Ohio excluded), from `mapping-runs.json` and the three draws' `views.sqlite`.
- **A closed key set per question:**
  - `id` (c01 to c15);
  - `kind`: `figure` when the rungs carry bounds; `event` when the rungs are exactly Yes, Ruled out and Still open with no bounds; anything else is
    refused;
  - `question` (views.question);
  - `due_day` (views.due_day);
  - `year` (views.year);
  - `unit`: for a figure, the `figure.unit` key of the stored `checked_answer` JSON, read as that one key and no other; for an event, `yes/no`;
  - `rungs`: position, label, condition, lo, hi.
- **The stripping rule.** Every rung condition loses the parenthetical that carries the ladder step's own reference ("(the reference when the
  question opened: …)" or "(no reference figure when the question opened)"). Code then refuses any condition that still contains "reference" or
  "question opened". These are system output, and the frozen readers never saw system output (ruler-v1 §1). There are 3 such rungs in draw u1
  today; all are counted at build.
- **Refused:** a figure ladder with a gap, an overlap or a middle rung with no bounds (all six figure ladders are contiguous today); a missing
  view or rung; a unit missing for a figure.
  - A refusal stops the whole build. The fixed population cannot shrink silently, and the refusal returns to the council.
- **Judgement text.** Code collects every stored judgement's text and rung for these views, and refuses any participant-facing file that contains
  a judgement's reason text or a field naming a chosen rung. All rungs are shown; which one was chosen is never shown.
- **Input manifest.** The sha256 of `mapping-runs.json`, the three `views.sqlite` files, `packet-v1.json`, `reader-brief.md`, every template and
  script, and the built `questions-v1.json`. Every later step refuses when one differs.

## 4. Readers (step 2)

- **Two readers:** A (Codex) and B (Claude family). Each gets one inline prompt built by the frozen reader-A runner's own shape
  (`run_reader_codex.py`, `prompt_for`):
  - `reader-brief.md` byte for byte;
  - the packet as text;
  - the 15 questions (the closed key set);
  - the output instruction;
  - "Do not read any file or run any command: everything you may use is in this message."
- **How each runs:**
  - **A:** `codex exec -s read-only --ephemeral --json`. The event log is checked for any command or file event.
  - **B:** `claude -p --output-format stream-json --verbose --no-session-persistence`, with every tool disallowed. The stream is checked for any
    tool_use event.
  - A session with a tool event, a failure, or output that cannot be parsed is void. It is run once more fresh; a second void makes every one of
    its questions unresolved (to Alex). Both raw outputs are kept.
- **Two additions to the output, stated in the prompt and not in the brief file:**
  - `decisive_items` holds 2 to 6 distinct item ids. Source: ruler-v1 §1.5, "撑起这个看法的 2–6 条事项编号".
  - For an event, one more key, `outcome_on_due_day`: "Yes", "Ruled out", "Still open" or "cannot tell", meaning which of the question's own
    rungs the material supports on the due day, with items. It must agree with `yes_no` ("Yes" exactly when yes_no is true). Source: D409, the event
    in three outcomes, and council round 2 ("a yes/no reference cannot decide which one holds").
- **Validity schema** (code, fixed now):
  - the brief's keys, with the types the brief gives;
  - `question_id` is c01 to c15, each exactly once;
  - when `no_view` is true, every other field may be null;
  - otherwise:
    - a figure has `low` ≤ `high`, numbers in the question's unit, and `yes_no` null;
    - an event has `yes_no` boolean, `low` and `high` null, and `outcome_on_due_day` from the closed set;
    - `direction` is from the brief's set and `confidence` from its set;
    - `decisive_items` holds 2 to 6 distinct ids;
    - every id cited anywhere exists in the packet.
  - An invalid row is asked again once by a fixed template naming only the invalid fields and the rule they break. Still invalid: unresolved, to
    Alex.

## 5. Reconcile (step 3)

- **Agreement**, by code:
  - a figure: the ranges overlap;
  - an event: `outcome_on_due_day` is equal, and "cannot tell" on either side is a disagreement;
  - no_view on one side only is a disagreement.
- **The proposed reference is reader B's answer.** Source: D262, Alex choosing reader B's answers as the frozen gold, with A kept as the noise
  record. The family point (the judge is gpt-6-luna, OpenAI, as is reader A) is a supporting observation from the archive (80 of 80 rows), not a
  rule.
- **Every disagreement** goes to two third readers, one of each family, inline and logged as in §4.
  - They see the brief, the packet, the question and both answers with their reasons, on sides drawn by a fixed seed.
    Source: the Stage A third readers' practice (`collect_readings.py disputes`, which shows both marks and reasons).
  - Each rules **A**, **B** or **neither**. "Neither" carries its own answer in the schema of §4.
  - A missing or invalid ruling is asked again once; still missing, unresolved.
- **Nothing is replaced automatically.** Every disagreement, with both rulings, goes to Alex.

## 6. Alex signs (step 4)

- **Who signs.** Only Alex. Signing cannot be delegated: the council has seen the stored judgements, and a reference for the ruler is his (AGENTS
  §7.1; D592). While he is inactive, the line waits.
- **The signing page** `control-reference-v1-for-signing.md`:
  - generated by code, in plain English;
  - shows the 15 questions, the proposed answers with their cited items, every disagreement with both readers' answers and both third readers'
    rulings and reasons, and every unresolved or no_view row;
  - shows no judge answer and no chosen rung;
  - Claude's message presenting it makes no recommendation on a disputed question.
- **His choices per question**, a closed set:
  - A's answer;
  - B's answer;
  - a third reader's answer;
  - his own answer in the §4 schema, which code validates;
  - **leave out** (no_view);
  - **reject**: the question is excluded, with his reason.
- **If Alex declines to sign,** nothing is scored and the line stays as it is.

## 7. Freeze (step 5)

- `control-reference-v1.json` holds `reference_version: 1`, both readers' sha256, each question's source (A and B agree, or Alex's choice in his
  words), and the label model-authored.
- Its sha is written to `control-reference-v1.sha256` and to the decision. It is never edited: a later defect becomes a dated correction record,
  printed with every score.

## 8. Material shown (step 6, after the freeze)

- **The brief.** `control-items-brief.md`, fixed in the manifest. It is the items part of `control-reader-brief.md` word for word, including
  "Search the entries for the figure or the fact; do not mark an item shown because a related item is", with the same-question and same-due parts
  removed.
- **The readers.** Two readers, one of each family, inline and logged as in §4, see each control's reference decisive items and the evidence entries
  the judge's requests listed on or before 2026-07-14. This is the existing rule, unchanged. It cannot show that the last judgement saw an entry
  that a later request listed; that limit is disclosed.
- **No chosen rung** appears.
- **Disputes** go to third readers of each family, who rule without the two answers (`control-reader-brief.md`, third-reader section). A split is
  `unresolved`, reported apart from `not_shown`.
- **Failures.** A failed or invalid packet is asked again once; still failing, the control is unresolved.

## 9. The count (step 7, `control_reference_count.py` and tests, fixed in the manifest)

**Exclusions** (each listed with its reason, never counted):
- not built;
- no judgement on or before 2026-07-14;
- the reference is no_view, left out or rejected;
- fewer than 2 decisive items;
- an item not_shown;
- an item unresolved (reported apart);
- a figure rung with no bounds;
- an event whose reference outcome is "cannot tell".

**Agreement:**
- a figure: the last judgement's rung band overlaps the reference range;
- an event: the last judgement's rung equals the reference's `outcome_on_due_day`.

**The line** is met when at least 8 controls are counted and all but one of them agree. It is unexercised when fewer than 8 are counted.

**Null baselines** (ruler-v1 §1: "判断要在这两条线之上才算有判断力"). They are scored on the same counted controls, each with its own denominator and
an unavailable count:
- **Figures, lookup:** the rung containing the reference's `reference.value`. Unavailable when the value is null or no rung contains it.
- **Figures, middle:** rung 3 of 5. The ladder step puts the reference's value in the middle range (the ladder request, line 16), so this is its
  neutral rung.
- **Events, always Yes,** and **events, always Still open**, the status quo. These are this design's analogue of ruler-v1's always-neutral, for
  three-outcome events that ruler-v1 did not have; Alex signs them with the design.
- **A baseline is formed per control,** from its figure or event rule, and given its own line verdict under the same rule.

**The verdict:**
- **PASS** when the judge's line is met **and** the judge agrees on more counted controls than every available baseline.
- **MET, NOT ABOVE BASELINE \<name\>** when the line is met but a baseline ties or beats the judge.
- **MISSED** when the line is not met with at least 8 counted.
- **UNEXERCISED** when fewer than 8 are counted.

**Printed beside the verdict:**
- **The line against reader A:** the same counted controls, with A's answer in place of the reference. A's no_view or invalid answers are not
  counted there, and the denominator is printed. It is a sensitivity reading only.
- **The A–B disagreement rate.**
- **Per matter:** each seed question id (q04, q07, q08, q09, q13, q16, q18) with its counted controls and agreements. Eight controls are not eight
  independent tests.

## 10. Predictions, written before any reader runs

- **The old reference's 8 of 15 is a historical count, not a bound.** Under the old reference's decisive items, 8 of 15 controls had every item shown.
  The new reference may cite more or fewer items.
- **An unexercised result** may come from no_view, invalid or unresolved references, missing judgements, unresolved shown checks, "cannot tell"
  events, or delivery. The report names which.
- **A missed result** is specific to this reference, these questions and these stored judgements.
- **Most A–B disagreements will reach Alex split by family.** On 9 of Stage B's 12 splits, each third reader sided with its own family's first
  reader. That was on judgement verdicts, not reference answers.

## 11. State × event

| Event | What happens |
|---|---|
| Build refusal (a gap or overlap, missing data, leftover reference text) | the whole build stops; to the council |
| A stored input or template changes between steps | the step refuses on the manifest; to the council |
| A reader's session has a tool event, fails or cannot be parsed | void; one fresh rerun; a second void makes its questions unresolved |
| Invalid reader row | asked again once with the fixed template; still invalid: unresolved |
| A–B disagreement | two third readers |
| Third reader missing, invalid, or ruling "neither" | missing or invalid: asked again once, else unresolved; "neither" goes to Alex with its answer |
| Alex inactive | the line waits; the council cannot sign |
| Alex amends | from the closed set, recorded in his words; the page is regenerated and re-signed |
| Alex declines to sign | nothing scored; recorded |
| Shown-check session failure, invalid packet, or split | asked again once; else unresolved, reported apart |
| Defect found after the freeze | a dated correction record, printed with every score |
| A later run with other questions (astra) | a new gold, with its own decision (AGENTS §7.1); not pre-authorised here |

## 12. Sources of every rule (AGENTS §11)

| Rule | Source |
|---|---|
| The packet as material | ruler-v1 §1; D658's Next line; D659 |
| Brief byte for byte; inline prompt; no file or command | ruler-v1 §2.1; `run_reader_codex.py` |
| 2 to 6 decisive items; refuse fewer than 2 | ruler-v1 §1.5; AGENTS §4 (a check over an empty population is unexercised) |
| `outcome_on_due_day` | D409; council round 2 |
| Reader B as the proposed reference, A as noise | D262 |
| Third readers see both answers | Stage A third readers (`collect_readings.py disputes`) |
| Shown-check third readers without the answers | `control-reader-brief.md` |
| All disputes to Alex; signing his alone | D658; AGENTS §7.1; D592 |
| Figure comparison, line threshold, window end | D428; `control_theses.py`; `score_judgement.py` |
| Null baselines, and the judge above them | ruler-v1 §1; the event analogues are this design's, signed by Alex |
| Strip the ladder's reference from the rungs | ruler-v1 §1 (readers see no system output) |
| Freeze and correction records | ruler-v1 §2; D261 |

## 13. What it does not measure, and its weak points

- **Not measured:** whether the right questions were opened (D1); delivery beyond the shown filter (D2); the judge's daily path.
- **Model-authored.** Alex's signature is the human vote, and the noise is printed.
- **One stored run, on the luna configuration's questions:**
  - PASS shows the line exercised and met on these 15. It does not pass Stage B, which also missed the strictest last-answer reading.
  - MISSED is a finding about the judge or the reference on these questions, and stops the line before further spend (D355).
  - UNEXERCISED names its causes.
- **Tuning exposure.** If a miss leads to a judge change (D263), these 15 become tuning data, and the next application must be on unseen
  questions.

## 14. Changes from version 2

- **Ohio dropped:** 15 questions, as Alex's option says.
- **Option text recorded word for word.** The material now has stronger sources.
- **Readers work inline** with no tool access, both families' logs are checked, and A follows the frozen runner's precedent.
- **The ladder's reference is stripped from the rungs** by a stated rule.
- **Kind and unit derivation stated.** A build refusal stops the whole build.
- **Every participant-facing text and the scorer** are fixed by sha before step 2 (§0).
- **Events** are compared by the reference's `outcome_on_due_day`, with "cannot tell" excluded.
- **Baselines defined,** each with its own verdict; PASS requires the judge to beat them.
- **The line against A** has its population and denominator stated.
- **Signing:** Alex's alone; the closed set gains "leave out" and "reject"; no recommendation on disputed questions; the line waits while he is
  inactive.
- **The items-only brief** is fixed in the manifest. Its third readers rule without the answers; "unresolved" is reported apart from "not_shown".
- **Validity schema closed.** Failure states are complete (§11). Sources are listed (§12).

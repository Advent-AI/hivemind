# Blind audit (version 5.4, after Alex's ruling D654) of one inserted passage in the ladder step's request (read-only, $0)

**What changes:**
- **The step:** it writes one judged question, its answer choices and its due day for each opened topic, or declines with a reason.
- **The edit:** one passage, inserted into the system text after the sentence ending "in not_judged, each with one sentence on why it is not the one
  tracked."
- **The texts:** `frozen-system.txt` and `edited-system.txt` (with the passage); `frozen-closing.txt` and `edited-closing.txt`, and
  `frozen-no-ladder-description.txt` and `edited-no-ladder-description.txt` (each with one short pointer to the same exception, listed in
  `edit.json` under `more`). Diff each pair yourself.
- **The passage and its stated sources:** `edit.json`.
- **The rest of the request, unchanged:** `/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-closing.txt` (the closing check) and
  `candidate-schema.json` (field descriptions, including `no_ladder`).

**The decisions it must agree with** (search `/Users/lchingen/hivemind/docs/DECISIONS-log.md` for "## D436 ", "## D397 ", "## D403 ", "## D414 ",
"## D417 ", "## D631 ", "## D635 "):
- **D436 (Alex):** one bet seen from two sides is one question; "the shortage beside the shipments, the AI-chip share beside the chip total, the capacity
  keeping pace beside the demand"; the second side stays as context, shown as not judged.
- **D397:** judge the one the topic's outcome names as tracked; list every other part.
- **D631 and D635:** no rule decides which part is the question when an outcome names several things; a description-priority rule was refused. Six
  boundary cases are Alex's, and the edit must not decide them.

**Also open:** `/Users/lchingen/hivemind/AGENTS.md` §6 (the prompt principles: carry the standard and decisions, add no new rule, examples from other
industries and never from a test article, a classification as a closed set with examples). The topics to test the passage on are in `audit-topics.json`.

**Alex's ruling since (D654, search "## D654 " in the decision log):** a general rule for the three shapes. When the outcome tracks a figure and also
names one kind's share of it, whether supply stays short of demand, or whether capacity keeps pace with demand, the figure is the question and the
second side is not judged. When the outcome tracks the share itself, the share is the question. Judge the passage against D654 first. Whether a
shape-based choice is licensed is settled by D654 and is not a finding. Whether the passage says exactly D654 and nothing wider is a finding.

## Answer, citing the sentence

1. **Clause by clause, in both directions:** for each clause of the passage and of the two pointers, consistent, contradicts, keeps wider, keeps narrower, or no source, against
   D436, D397, the decline cases (system line 6), the closing check and the `no_ladder` description. Name any other sentence of the request it collides
   with.
2. **The targets:** for each of the 4 targets, what a careful model following the edited request would write: the question about which figure, and what is
   listed. Is that what D436 rules?
3. **The controls:** for each of the 6 decline controls (the two topics listed as entangled are not controls), does the edited request still lead to a decline? If not, is the decline still justified under the
   decisions, so the control is wrong to keep?
4. **The boundary cases:** for each of D631's 6, does the edited request now decide which part is the question where the frozen request did not? Any case
   it decides is a finding.
5. **The examples:**
   - Do any of the examples come from, or mirror, the 44 test topics (`/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/cases.json`)?
   - Does each read the same for a bank, a drug maker, a retailer or a chip maker?
   - Does each example's orientation agree with D436? D436's third example puts demand as the figure and "capacity keeping pace" as the side.
6. **Growth:** the passage adds characters and removes none; `edit.json` gives the reason. Is the reason, with the line-by-line `cut_review` in `edit.json`, sufficient under AGENTS §6, read with the council-loop trap it cites (`/Users/lchingen/hivemind/.claude/skills/council-loop/SKILL.md`, "Cuts made to keep a prompt length-neutral are levers too")?

7. **The share-centred counterexample** in `audit-topics.json`: would the edited request still ask the share it tracks, and not switch to the total?
8. **The trigger's same-bet clause:** under D654 the closed list of second sides decides; does each shape stay tied to the figure the outcome tracks, so that two things merely mentioned together do not trigger it? Are the
   counter-case sentence and the main sentence consistent with each other?

Check the controls against the listed themes (`audit-topics.json`, "themes listed in every request").

**End with one line:** `SOUND`, or `NOT SOUND: <the smallest change that would make it sound>`. You are read-only: edit nothing, and make no model call.

# Deep council, round 4: the audited passage is ready for your decision on the paired test

## The audit history
Two blind auditors per round, fresh each round, one Codex and one Claude-family. Files: `narrow-d436/audit-v1..v3-*.md` and `edit-v1..v3.json`.

| Version | Codex auditor | Claude-family auditor |
|---|---|---|
| v1 | Not sound: an automatic whole-over-part rule; the airline example inverts D436 | Not sound: "a condition" is too wide (it collides with the drug example and with H20); narrow to D436's shapes |
| v2 | Not sound: shape-based selection | Not sound but close: bind the trigger to the tracked figure and the same quantity; no boundary case decided; all targets and controls behave |
| v3 | Not sound: "tracks" is ambiguous, so require the outcome to identify the figure as main first; the growth-rate wording; the examples mirror test structures; growth not offset | Not sound only on the retailer's holiday (part-year) example and the attribution; everything else consistent |

## v4 (`narrow-d436/edit.json`, `edited-system.txt`)
- **Fixes:** the examples name full years; shape (b) reads "beside a figure that measures that supply or its growth"; the examples are joined into one
  sentence; the attribution is corrected.
- **Size:** +741 characters; tokens (o200k) 2,031 to 2,182.
- **The passage:**
  > "When the outcome tracks a figure and also names the share of that same figure that one kind makes up, whether supply stays short of demand beside a
  > figure that measures that supply or its growth, or whether capacity keeps pace with the demand that figure measures, the two are one bet seen from two
  > sides, not several things with none the main one: ask the figure, and list that second side in not_judged. So a bank's total lending for the year
  > named with the share that is commercial lending is asked as the total lending, a retailer's sales for the year named with whether its shelves run short
  > are asked as the sales, and a utility's power demand for the year named with whether its generating capacity keeps pace is asked as the demand."

## A fact the audit surfaced: attribution
- **Alex's own words:** "算一个题，第三处不改". He gave them in reply to an option shown with the HBM shipments-and-shortage example only. Its rationale was
  "都是同一个押注的不同侧面".
- **The other two pairs and their orientation** (the AI-chip share beside the chip total, capacity keeping pace beside demand) come from D436's Decided
  line. That line is in force, but it is the recorder's statement of the ruling's scope, not his verbatim words.
- **So:**
  - shape (b) rests on his words;
  - shapes (a) and (c) rest on the decision as recorded.
- I will tell Alex this plainly.

## The disputed point
- **The Codex auditor's position (v3):** apply the shapes only when the outcome already identifies the figure as the main tracked part.
- **My position:**
  - The targets' outcomes name both sides with no stated priority. That is exactly why astra declines; its own account says "the outcome does not
    establish" a priority.
  - D436 settles which side is the second side for these shapes. Requiring an explicit priority would leave D436 unapplied on the very cases it was
    decided on.
  - The binding ("tracks a figure and also names … that same figure") already prevents inversion when the share itself is the tracked thing.
- **The Claude-family auditors (v2 and v3):** the binding is sourced, a generalisation of D436's own examples, and it decides none of D631's six cases.

## Questions
1. Is v4 fit to send in the paired test? The test is a measurement; nothing is adopted. Sending it does not settle the disputed point, but it will show
   whether the targets flip and the controls hold.
2. If the dispute is unsettled, AGENTS says: record both positions and take the cheaper, reversible course. The paired test is that course: $2.1, not
   adopted, and any later adoption goes to Alex with the attribution fact.
3. Anything in the paired rule (`paired_probe.py`'s docstring) to change before the send?

CONSENSUS or DISAGREE.

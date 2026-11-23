# Gate 1's reading measured with a blinded reference control outside the 44 (D623), fixed before any reference is written

**Question.** Gate 1's zero-fault lines are judged by two model-reader families. This control asks two narrower things (council,
`../codex-challenge-1.md`):

1. Do the readers mark faults on sound answers (reader error)?
2. Is there a clear, repeated difference between careful independent answers and the frozen step's answers on the same topics?

It cannot prove gate 1 reachable or unreachable.

## The population (fixed now)

Every topic of the two stored sources outside the 44 that have the frozen step's stored sends: 26 topics.

| Source | Topics | Kinds in the stored first send |
|---|---|---|
| The fortnight (`clean-carried-run-2026-11-16`, c1/clean-1 to c1/clean-13) | 13 | 6 figures, 6 events, 1 refusal |
| The week of 10-06 (`clean-second-week-2026-11-15/week-continued`, c1/clean-1 to c1/clean-13) | 13 | 6 figures, 5 events, 2 refusals |

None is among the 44 (checked by description).

## The arms

- **Frozen:** each topic's stored pass-1 answer from the frozen step, as stored.
- **Reference A:** one fresh read-only Codex session per source, writing all 13 topics of that source.
- **Reference B:** one fresh Claude subagent per source, writing all 13 topics of that source.

**What the writers get.** Each writer gets, per topic:
- the exact request the step sends: the system text, the user message (payload and closing check) and the schema;
- `stage-a-reader-brief.md`, the gate form's rules, as the quality bar.

**What the writers never get:** a stored answer, a reader's mark, another writer's work, or this design's rule.

**The writer's answer.** One answer per topic, fitting the schema: a ladder, or a refusal with its reason.

## Checks

- Each reference passes production's schema check (`model.check_schema`) and the step's code checks (`ladder_step.check_answer`).
- A reference those checks refuse goes back once to the same writer, with the reasons as the step's resend gives them. Refused twice
  means it is recorded as the writer's failure and not read.
- Accepted references are rendered by the step's own `write_view`.

## The reading

- **What is read:**
  - all frozen and accepted reference items, blind, shuffled, with arm names in the key outside the repository;
  - four controls: two planted wrong (a ladder with a gap between rungs, R; a question asking another thing than the topic's
    outcome, Q), and two sound (frozen ladders both families marked clean on every mark in an earlier reading).
- **Who reads:** both families with `stage-a-reader-brief.md` alone: the full gate form, every line.
- **Disputes:** disputed marks are counted both ways (unresolved for the answer, then against it). No third readers unless a disputed
  point decides one of the results below.
- **A missed planted-wrong control voids the reading. A sound control marked faulty by both families is itself a confirmed reader
  error, if the review below confirms it.**

## Review of every settled reference fault

Every mark both families settle as a fault on a reference (lines Q, L, R and N, and any other) is reviewed against its source and the
brief's rule. Claude reviews first, writing down each verdict; an independent read-only Codex session then reviews it. Each is put down
as one of:
- an answer error;
- a reader error (the answer meets the rule and the reader misapplied it);
- unresolved.

## What moves a decision

1. **A confirmed reader error on a sound answer** (a sound control or a reference) that would fail one of gate 1's zero-fault lines.
   This shows part of gate 1's misses can come from the reading. The council takes that to the reading's validity, not to the step.
2. **A clear, repeated difference favouring the references:** on at least 4 of the 26 topics, both references are free of settled
   faults on lines 1 to 4 where the frozen answer has one, with the reverse on at most 1. This shows the step has headroom on the same
   inputs. The council takes that to a new version of the step developed outside the 44.

**Closes the control:** no independently confirmed reader error and no difference meeting result 2. The uncertainty is reported, not a
verdict on the gate.

**Limits:**
- the writers belong to the readers' families;
- 26 topics;
- one frozen send a topic.

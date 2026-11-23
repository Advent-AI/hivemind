# Candidate for challenge only, not a changed prompt

Current `supersedes` criterion (275 characters):

> a later version of the stored piece's main statement, changed: the same speaker revises that guidance, forecast or event-progress statement, an official confirms or denies that reported claim, or the original source revises it; another statement on the same topic is not this

One potential replacement (unmeasured; exactly how much prompt must be cut remains subject to full request audit):

> Identify the statement the incoming piece changes, confirms or denies; it must be the stored main statement. A later change may be the same speaker revising guidance, forecast or event progress; an official confirming or denying it; or the original source revising it.

Difference in procedure: ask the model first to identify the statement actually addressed, then compare it to the stored main statement. This does not request chain-of-thought, require literal identical text, or add an uncertainty product outcome. Risks: it might be semantically equivalent and fail to change Jev; it might cause missed correct updates or change scope; omitting "another statement on the same topic" may regress related-but-distinct comparisons. It cannot be sent until the complete request is audited against the existing signed standard and reviewed, controls are checked, and any required preflight and scope rules are met. This is a hypothesis, not an actual code change or a proven solution.

## Revised candidate for council challenge

The independent reviewer correctly found that the first draft failed to make later timing a mandatory part of its first instruction, and removed the explicit related-statement boundary. A corrected *hypothesis*, still not a prompt change or an approved design:

> Identify the claim the incoming piece changes, confirms or denies. It must be the stored main statement, not a related claim, and the account must be later: e.g. the same speaker revises guidance, a forecast or event progress, an official confirms or denies the claim, or the original source revises it.

This draft is 303 characters, 28 more than the original 275. The explicit proposed addition is an instruction to identify and compare the actual target. The growth and any omitted or subtly narrowed behavior require a whole-request audit, and at least equivalent cuts elsewhere or a documented reason consistent with AGENTS §6. How it handles missing or conflicting times needs review: it must not silently invent a time or change the existing contract. No model has been sent this candidate.

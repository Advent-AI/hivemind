# Reader brief B, third form: does each judgement follow the judge's own rules on the evidence it was shown? (read-only)

You are an independent reader. Do not edit files, run model calls or start runs. Do not read any other reader's answers.

`clean-arch/step4-2026-11-10/dryrun2/packet-b.json` holds 20 judgements of two research questions, in day order within each question.
Each has:
- `request_as_sent`: what the judge was shown that day: the question, its ladder of rungs (exactly one rung is meant to hold on the
  due day), the evidence in view (each item with its source, a one-line summary and a quote), sometimes the conclusions of other
  questions and themes, and the previous conclusion;
- `answer`: the judge's answer that day: the `rung` it chose with its label, the `reference`, the `implied_outcome`, its `reasons`,
  and whether it says its conclusion `changed`.

Some of the answers are sound and some are not. Judge each on its own from its `request_as_sent`.

## The standard: the judge's own rules

The judge was given the rules below. They are the standard you read each answer against. A judgement is a forecast, not a proof:
an answer that sizes an undisclosed amount from a disclosed comparable, or that states that no market expectation is given, follows
these rules and is not wrong for that.

```
You are a senior hedge-fund analyst judging a thesis's current rung. Use only the supplied evidence, dependency conclusions and themes in force. The rung is your forecast: the outcome the evidence in force makes most likely at the due date, not the one it has proved.

- Rejudge from the evidence shown (what recent judgements relied on and what arrived recently), the current conclusions of dependencies and the themes in force. Pieces in force that no recent judgement relied on are not shown; the previous conclusion carries them. Do not add to or subtract from the previous score. The previous conclusion is supplied only for comparison.
- Judge against a reference: what the market expects for this question (consensus, the company's guidance, the stated plan or deadline). Say where the reference sits on the ladder. A consensus or guidance figure by itself keeps the judgement at the reference's rung; once other evidence has arrived it is never the reason to stay. Then derive the outcome the evidence implies: reported figures and guidance give a run-rate that carries the guided growth forward, never the last quarter annualised flat; a quantified revision, a customer's demand number, a supplier's constraint, a confirmed delay or cancellation shift it. A target for a product with no shipments yet is discounted by default; it is taken in full only when the evidence shows the volume in hand. State the implied figure or date, check it against the dependencies' conclusions shown (a part cannot exceed its whole, and a figure that spans several periods or products gives this question only its share), compare it with the rung boundaries, and move when it crosses one.
- Weigh by tier and by novelty. Only fact can establish that a rung's outcome already holds; "not established" is a statement of confidence, never a reason to stay. Guidance for the current or next quarter is the strongest forecast input. A management target for a product not yet shipping, or an ambition spanning years, is an input to be discounted for time and execution (how many selling quarters remain, what volume and price the figure implies, what the company's own choices say), not an answer; consensus is where the market stands, not the answer either. third_party_view and rumour move the forecast in proportion to their specificity (a number, a date, a named party): a research firm's shipment or revenue tracking with a number counts. A commitment or deal that is announced but not sized is sized from its disclosed comparable (the same programme's other deal, scaled by capacity or units); a figure no one states is derived from the accounting identities in the evidence when they allow it. A repeat, another outlet for the same claim, or an opinion that adds no new fact or calculation moves nothing. Missing confirmation alone is not grounds for the lowest or highest rung: an event not being confirmed is not confirmation that it did not happen.
- An evidence item that replaces another includes its predecessor for context, such as guidance revised from 12% to 25% growth. The predecessor is no longer evidence in force.
- “Themes in force” lists the library's open theme theses (policy stages, shared quantities) with their current conclusions. They are our own judgements, never evidence: do not cite them in cites. Weigh each one that bears on this thesis and report it in theme_pushes with the direction it pushes this thesis (toward_first, toward_last or none); leave out a theme that does not bear on it. A theme marked “updated since this thesis was last judged” may change the conclusion; one that is not marked already stood at the previous judgement. When no themes are listed, theme_pushes is empty.
- A dependency marked “not yet created” supplies no input. A dependency marked “historical only” is closed without a successor; its closing conclusion is background only.
- Your conclusion must be consistent with the conclusions of the theses it depends on and the themes in force as shown: a share cannot be judged at zero while the policy that gates it is judged likely to open; a component cannot exceed its whole.
- Return the rung's one-based position; reference (what the market expects and which rung that is); implied_outcome (the figure or date the evidence implies and how you derived it, in one or two sentences); reasons (the gap between the two and why it does or does not cross a rung boundary); citations to supplied evidence and dependency IDs; each evidence item's push (toward_first, toward_last or none); theme_pushes; changed; and why_changed. Write explanations in English; preserve IDs and any quoted source text.
- changed is true for a different rung or a change to the key facts or figures supporting the same rung, including a changed implied outcome. Repetition or another source for the same statement does not alone change the conclusion. The first judgement always has changed true.
```

## What to return

One JSON object per judgement, one per line, in packet order, as your final message: no prose before or after, no code fence. 20
lines. Fields:

| field | values | meaning |
|---|---|---|
| `judgement` | the number in the packet | |
| `verdict` | `SUPPORTED`, `UNSUPPORTED`, `INSUFFICIENT` | about the **rung** only. SUPPORTED: applying the rules above to the evidence shown, the chosen rung is the most likely one. UNSUPPORTED: applying the rules, another rung is the most likely one; or the rung chosen is not the one the answer's own implied outcome falls in; or the answer **moves** to a rung different from its previous conclusion's on a step the rules or the evidence do not allow, when without that step the evidence would not lead there (name the step). INSUFFICIENT: the evidence shown gives no way, even by the rules' comparables and identities, to prefer one rung, and the answer does not move rung on a disallowed step |
| `rung_the_evidence_points_to` | a rung number, or `null` | for UNSUPPORTED: the rung the rules and the evidence lead to |
| `reasoning_flaw` | `none`, `does_not_change_the_rung`, `changes_the_rung` | a step in the reasons that the rules or the evidence do not allow (a comparable from another programme, a figure counted twice, an amount already paid counted as outstanding, a statement not in the evidence); `changes_the_rung` always goes with UNSUPPORTED |
| `arithmetic` | `right`, `wrong`, `none` | whether any calculation in the answer is right; `none` when it makes none |
| `reference` | `holds`, `fails` | the answer states what the market expects and where it sits on the ladder, or states plainly that the evidence gives none |
| `implied_outcome` | `holds`, `fails` | the answer states the figure or date the evidence implies and how it was derived |
| `why` | one sentence | the reason for an UNSUPPORTED or INSUFFICIENT verdict, a flaw, a `wrong` or a `fails`, naming the evidence id or the figure |

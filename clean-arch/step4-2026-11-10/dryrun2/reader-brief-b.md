# Reader brief B: is each judgement supported by the evidence it was shown? (Stage B reading form; read-only)

You are an independent reader. Do not edit files, run model calls or start runs. Do not read any other reader's answers.

`clean-arch/step4-2026-11-10/dryrun2/packet-b.json` holds 20 judgements of two research questions, in day order within each question.
Each has:
- `request_as_sent`: what the judge was shown that day: the question, its ladder of rungs (exactly one rung is meant to hold on the
  due day), the evidence in view (each item with its source, a one-line summary and a quote), sometimes the conclusions of other
  questions and themes, and the previous conclusion;
- `answer`: the judge's answer that day: the `rung` it chose with its label, the `reference` (what the market expects and which rung
  that is), the `implied_outcome` (the figure or date the evidence implies, and how it was derived), its `reasons`, and whether it
  says its conclusion `changed`.

A judgement is a forecast: the rung the evidence shown that day makes most likely on the due day, not the one it has proved. Some of
the answers are sound and some are not. Judge each on its own from its `request_as_sent`.

## What to return

One JSON object per judgement, one per line, in packet order, as your final message: no prose before or after, no code fence. 20
lines. Fields:

| field | values | meaning |
|---|---|---|
| `judgement` | the number in the packet | |
| `verdict` | `SUPPORTED`, `UNSUPPORTED`, `INSUFFICIENT` | SUPPORTED: the evidence shown makes the chosen rung the most likely. UNSUPPORTED: the evidence points to another rung, or the reasons rest on something not in the evidence shown, or the rung chosen is not the one the answer's own reasons and implied outcome lead to. INSUFFICIENT: the evidence shown does not separate the rungs |
| `rung_the_evidence_points_to` | a rung number, or `null` | for UNSUPPORTED: the rung you would choose from the evidence shown |
| `arithmetic` | `right`, `wrong`, `none` | whether any calculation in the answer is right; `none` when it makes none |
| `reference` | `holds`, `fails` | the answer states what the market expects and where that sits on the ladder |
| `implied_outcome` | `holds`, `fails` | the answer states the figure or date the evidence implies, and it follows from the evidence shown |
| `why` | one sentence | the reason for an UNSUPPORTED or INSUFFICIENT verdict, a `wrong` or a `fails`, naming the evidence id or the figure |

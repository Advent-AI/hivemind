# Reading Step 1 theses: one tracked thing, or more (read-only)

You are an independent reader. Read only this brief and `packet.json` beside it. Do not open other files, run commands or model
calls.

Each item is a thesis a research step opened: its question, its outcome (what it tracks) and its period. The rule the step was
given: "A thesis asks one quantity for one period, or one event."

For each thesis, classify what its **outcome** (with its question and period) tracks:
- `one`: one quantity for one period, or one event. A reference figure it is compared with ("measured against the $119 billion
  cited"), the event's own negation ("permitting or continuing to bar"), or details of the same event (the fine or remedies of a
  decision) still count as one.
- `two_periods`: the same quantity or event for two periods, or a date and an alternative date ("in 2027 or delayed to 2028").
- `two_outcomes`: two different quantities or events (a capacity and a price; whether a deal is signed and its amount).
- `main_and_second`: one main quantity with a second quantity attached (in brackets, "and the portion of it", "and the resulting").
- `alternative`: one outcome with an alternative outcome written beside it as part of what is tracked ("closes (or restructures)").

Return one JSON object per thesis, one per line, in packet order, and nothing else:
`{"thesis": "u1/clean-1", "shape": "one|two_periods|two_outcomes|main_and_second|alternative", "why": "one short phrase quoting the words that decide it"}`.

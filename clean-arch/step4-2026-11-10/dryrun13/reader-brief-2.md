# A reading of rungs (read-only)

You are an independent reader. Do not edit files, run model calls or start runs. Open only this brief and `packet-2.json` in this
folder; open and list nothing else, in the repository or anywhere else.

`packet-2.json` holds four questions about events. Each has a `due_day` and its `rungs`, exactly as a later judge is shown them:
"rung N label: condition". For each question there is a list `facts_on_the_due_day`: each entry states, as known and complete,
what is true on the due day.

For every scenario, say which rung holds, reading only the rung texts and the facts given. Add nothing you know from elsewhere.
Exactly one rung is meant to hold; if you find that none does, or that two do, say so instead of choosing.

Return one JSON object per scenario, one per line, in scenario order, and nothing else:
`{"scenario": 7, "rung": 3, "why": "one sentence naming the words of the rung that decide it"}`; use `"rung": "none"` or
`"rung": "two"` when that is what you find.

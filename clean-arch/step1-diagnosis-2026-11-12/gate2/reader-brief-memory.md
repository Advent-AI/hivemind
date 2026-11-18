# Gate 2 memory-thesis marks (read-only)

You are an independent reader. Read only this brief and `packet-memory.json`. Do not open other files or run commands or model calls.

Each entry is one research question (question, outcome, period). Give each exactly one mark:
- `one-year price`: a price level for one period;
- `change`: the move from one year to another (a question that tracks a level and the change is marked change);
- `span`: a price over several years without a change;
- `not a price`: anything else.

Return one JSON object per entry, one per line, in packet order, and nothing else: `{"n": 1, "mark": "...", "why": "one sentence"}`

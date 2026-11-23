Whole-request audit, read-only, fresh reader. Repository /Users/lchingen/hivemind, branch clean-arch.

A new focused call is built by `clean-arch/step1-unfiled-2026-11-08/focused/focused_probe.py`:
- the system text `system.txt`, with the schema `schema.json` appended after "Return only one JSON object that conforms to this JSON
  Schema:";
- then a user message: the JSON payload (source_item, theses, statements), a blank line, then `closing.txt`.

To see a real request, build it with
`PYTHONPATH=src python3 -c "import sys; sys.path.insert(0,'clean-arch/step1-unfiled-2026-11-08/focused'); import focused_probe as f; p,a,k=f.stored_case('poc/data/clean-step1-c8-dev-d1-2026-11-09/trace.sqlite',4); r=f.route(a,k); print(f.build(p,a,r)[0][-6000:])"`.

Read the whole request as the model reads it. Clause by clause, in both directions, check it against the signed standard as quoted
from c8 §3 (`clean-arch/step1-unfiled-2026-11-08/arms/c8-system.txt`) and D388 (`docs/DECISIONS-log.md`, "## D388"). For each clause
say whether it is consistent, contradicting, wider, narrower or unsourced, and whether any instruction forces a wrong answer for a case
the standard keeps or rejects.

Under 300 words: READY or NOT READY, with each blocking finding.

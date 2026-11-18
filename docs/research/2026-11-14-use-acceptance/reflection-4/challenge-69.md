# Round 70: the $0 Idea-planner check (D580). Result and next.

`idea-planner/RESULT.md`, `trace_planner.py`, `trace-output.txt` (the fortnight's page store; `poc-v118-idea.json` = idea-summary-v8,
endpoints only; three drivers: event v3, theme range v5 with no favourable end, company figure v2; hand-written realistic answers; no
model call). The falsifier does not hold in full:
- an event is shown to the planner as "Yes" and "Still open" (positions 1 and 3; Ruled out omitted), and a plan can record "Still
  open" as the end that raises the outcome; that JSON reaches API and MCP clients as written;
- no misleading number: only the page's composite reads supporting_end, it scores on the ±2 investment scale, and since D570 it refuses
  undirected drivers with a note;
- coverage: theme ranges with no favourable end (4 of 11 questions here, beside 6 events) make any Idea using them show no composite,
  although the planner gives each range a direction relative to the Idea's outcome.
Two choices a narrow design would make: how an event can be a driver (all three outcomes shown, Yes or Ruled out as the raising end;
or context only), and whether a range's own positions with the planner's direction may form the composite scale. Both change what the
product shows (the second changes the page's composite contract, D570/D571's neutral treatment of undirected questions).
My lean: design the first (the event) at $0 and bring it here; it fixes a misdescription and changes no number. Leave the second for
Alex's page beside choice 5 (directions the product invents), since it would let the composite score theme ranges. End with
`CONSENSUS: yes` (state the course) or `CONSENSUS: no, because …`.

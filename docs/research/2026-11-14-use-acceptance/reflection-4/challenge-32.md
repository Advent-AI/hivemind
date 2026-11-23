# Round 33: D569's next step designed. Attack before any code.

`not-judged-display/DESIGN.md`: the bundle writer adds `not_judged` (rows: list; empty row: []; no table or row: None), the closed
UI schema gains an optional `notJudged`, the adapter copies it, the drawer shows a "Not judged" section beside the current assessment
only when non-empty, the UI spec records it; value × reader (HTTP, MCP and the page share the bundle writer; no judging path reads
it), new path × old checks (closed schema extended, older datasets valid, budget), prior decisions, and a $0 proof (bundle test with
a real row, empty and absent, plus a mutant; UI schema/adapter/drawer checks; the real page in a browser; the extension proof and the
full suite). Census on the fortnight: 12 questions, each with one row; 10 rows list 12 parts; 2 list none.

Attack: the None/[] distinction; time visibility; schema versioning (optional field in `thesis-ui/2` versus a new version); where
"beside the answer" sits; any reader I missed. End with `CONSENSUS: yes` (build and prove) or `CONSENSUS: no, because …`.

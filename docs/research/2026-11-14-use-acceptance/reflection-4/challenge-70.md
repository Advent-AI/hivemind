# Round 71: the planner result corrected (12 questions; API by code path only; no MCP tool), and the event design (`idea-planner/DESIGN.md` v1).

Two options compared: context only (the event cannot be a scored driver; it sits in `excluded`) and an honest driver (all three
outcomes shown; Yes or Ruled out named as the raising outcome; `supporting_position` recorded instead of `supporting_end`; Still open
refused). A table covers every shape against both claim directions (three-choice and two-choice events, figures with and without a
favourable end, unrecorded shapes); the page's refusal of event drivers (D570) is unchanged and needs a test that a plan with
`supporting_position` gives the note rather than a TypeError; consumers listed; tests and two mutants named. My lean: option 2.
Attack it, including whether it is worth building at all before the new system is adopted (it only matters on a new-system store).
End with `CONSENSUS: yes` (build option 2, or name the other course) or `CONSENSUS: no, because …`.

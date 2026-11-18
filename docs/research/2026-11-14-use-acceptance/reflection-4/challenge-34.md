# Round 35: the before-creation rule. Go or no-go.

`not-judged-display/DESIGN.md` version 3: before a view's creation the field is suppressed on every path: `view_bundle` returns
`None` for `not_judged` when its `as_of` does not yet see the view's creation sequence (whatever the caller, `idea.py` included; the
view's other fields keep their present behaviour), and the UI's one date filter, `snapshotThesis`, gives `notJudged: null` on a day
before `created_day`; the drawer opened by `openThesis` reads the snapshot. Tests named for both direct paths (bundle directly before
and on creation; snapshot and drawer before creation, on a later day with and without an assessment). End with `CONSENSUS: yes`
(build and prove) or `CONSENSUS: no, because …`.

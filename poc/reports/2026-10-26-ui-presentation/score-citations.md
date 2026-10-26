# Card scores and citations — October 26, 2026

D189 removes the Idea chart footer and names its title “AI score (composite)”. D190 renders citations as plain blue `[1]` links. D191 moves score pills beside chart titles, retaining their shape and matching 11px text.

## Verification

- All 90 library cards render a score pill beside the title, with matching font size, no title overlap and no score in the top header. The current Idea and its three connected Thesis cards pass the same check.
- Real cached Idea replay changes the composite from 0.00 to +0.50 and the connected thesis scores with it. Full and Last 30 days retain the pills and chart. No driver/history footer remains.
- Citation census: 1,358 references across 137 assessments in 33 theses. Of their reference-only groups, 580 have parentheses or brackets, including 20 with hyphen/en-dash ranges. Every rendered reference remains present; all outer duplicate wrappers are removed. A scratch mutant retaining the wrappers fails the decisive assertion.
- In the real drawer, citations have blue text, transparent background, zero border and padding. Current and historical references both open the corresponding stored evidence. User source text and IDs are unchanged.
- 40 UI tests, lint and formatting pass; 160 Python tests pass. Final JavaScript is 155,465 bytes, and the final local validation sample is 25.1ms for 90 theses.
- All three source database hashes match the D181 baseline. The Idea model archive stays at seven rows: browser submissions reused cached calls.

Screenshots: [score pills](score-pills.png), [blue citations](blue-citations.png).

## Reasoning refresh

Research universe → classification → Config → dispatch → extraction → thesis library → final verdict → pull mode → human review pool → system overview: these presentation changes alter no inputs, stored fields, dates, ordering, identity, model calls or module outcomes. The existing examples and acceptance criteria remain applicable. The Idea specification's old chart-caption sentence was corrected; the UI specification now owns citation appearance and score placement. D181 remains the owner of source identity and historical reads; D188 owns composite calculation. No probability scale has been implemented.

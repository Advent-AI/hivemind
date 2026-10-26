# Score pill below the title — October 26, 2026

D192 supersedes D191's horizontal placement. The shared title renderer puts the existing pill in a left-aligned row below the title. Charts with a pill reserve 24px; their plot coordinates remain local and unchanged. Canvas card height includes that row. Charts without a pill retain their layout.

Browser verification covers all 90 library cards: each pill is below and aligned with its title, and each chart remains inside its card. The cached Idea and its three connected Thesis cards pass the same checks. Home/End replay updates the pills from the selected date; Full/Last 30 days also work. See [the final screenshot](score-below-title.png).

40 UI tests, lint and formatting pass. 160 Python tests pass. The final build is 155,581 JavaScript bytes and validates 90 theses in 24.5ms in this sample. The three source database hashes remain unchanged and the model archive retains seven rows; no new model request was sent.

Reasoning refresh in PRD order: research universe, classification, Config, dispatch, extraction, thesis library, final verdict, pull mode, human review pool and system overview retain their inputs, outputs, examples and acceptance criteria. This change only relocates rendered values and makes room for them. The UI presentation rule and current-state paragraph were updated; D192 records the changed placement. Probability design remains a discussion, with no model/schema/calculation change.

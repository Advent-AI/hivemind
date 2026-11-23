# Council round 6: design version 6 and the participant-facing texts

Version 6 is in `review-v6/` in this folder, read-only:
- `NEW-REFERENCE-DESIGN-v6.md`;
- `control-items-brief.md`;
- `templates/`, which holds the texts every participant will see, word for word.

It answers your round-5 review and the Claude family's, condensed in `council-claude-5.md`. The change list is §15.

Check your round-5 findings first:
1. the stage-specific permitted source of the leak check, and its test on generated files;
2. retry attempts as their own slots;
3. the items brief's control ids.

Then read every template as a participant would. Does any wording steer a reader or third reader towards an answer? In particular:
- the `outcome_on_due_day` instruction;
- the third reader's "1", "2" or "neither";
- the ask-again reasons.

Is any template inconsistent with the frozen brief or with D660?

Also check the population resolution: the `questions` map, then `clean_ladders`.

Report only findings that would change what is built or measured. Out of scope: the ladder step's prompt, gate 1 and cost. The frozen ruler's
files must not change. End with `READY` or `NOT READY: <the smallest change>`.

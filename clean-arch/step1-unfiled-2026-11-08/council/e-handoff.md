# Decision council: the next step of the Step 1 unfiled fix round (read-only, independent)

Alex asked the council to decide the next step. You are a fresh, independent reviewer.

Read:
- `AGENTS.md` (§1, §2, §6, §7);
- `clean-arch/step1-unfiled-2026-11-08/LOG.md` (all sections);
- the arms in `clean-arch/step1-unfiled-2026-11-08/arms/`;
- the probe-1 data in `poc/data/clean-step1-unfiled-2026-11-08/probe-r1/` (`records.json`; reader answers);
- the council files in `clean-arch/step1-unfiled-2026-11-08/council/` **except** `d-claude.md`.

Out of scope: the frozen gold, frozen production, Steps 2 to 4. Alex's constraints: no hard-coding, no prompt overfitted to test
cases, and every rule sourced in the standard or a decision.

Decide one next step and justify it. Options include, but are not limited to:
- probe 2 isolating the D371 line (no cuts) alone and with the required field;
- the dev forward run;
- a different lever;
- stopping the fix and accepting the current configuration with the defect recorded.

For the chosen step give:
- the exact arms, cases, draws and readers;
- the predeclared pass and stop criteria;
- the cost at DeepSeek Flash's published rates ($0.30 / $1.20 per M; about $0.013 per send measured);
- what result would make you abandon the line.

Also say whether probe 1's control draws can be reused as the control, and how to make the readers more independent.

Under 450 words.

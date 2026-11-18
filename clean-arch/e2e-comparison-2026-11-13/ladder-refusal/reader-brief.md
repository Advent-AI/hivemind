# Blind reader: does each research question's tracked outcome name one main figure or event? (read-only)

Repository `/Users/lchingen/hivemind`. Read:
- the step's rules, `clean-arch/step4-2026-11-10/ladder/candidate-system.txt` lines 5 and 6 (judge the one the outcome names as tracked and list
  the other parts; refuse when the topic names "several with none of them the main one");
- the owner's ruling D436 in `docs/DECISIONS-log.md` (search "## D436"): a second side of the same bet is one question, kept as context and shown
  as not judged;
- the cases: `clean-arch/e2e-comparison-2026-11-13/ladder-refusal/main-refusal-cases.json` (12 questions with their outcome text and how often the
  step refused or laddered them).

For each case decide, from the outcome text alone and the two rules: (a) does the outcome name one main figure or event to track, with the
rest a second side, a comparison or context of the same bet? Name it. (b) Or does it name two or more things an analyst would track and bet
on separately, with none the main one? Return one JSON object per line:
{"case": "...", "verdict": "one main" | "none main", "main": "<the main figure or event, or null>", "others": "<what goes to not_judged, or why
they are separate bets>", "why": "<= 40 words"}

Then, in at most 150 words, state the boundary between your two groups as a rule an analyst could apply to any industry's question (not
"whatever comes first"), and name the cases that would test it hardest. Out of scope: changing any file; judging ladders.

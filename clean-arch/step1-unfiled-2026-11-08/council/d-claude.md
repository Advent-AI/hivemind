# Claude's decision (written before reading Codex's)

**Decision: run probe 2, narrowly, then decide on evidence.**
- **Arms:** u1k (the D371 line added to section 3; "one quarter's figures or guidance" moved out of the do-not-open list; nothing else
  cut) and u1k+u3. The control reuses probe 1's three k6b draws: the same requests, fresh samples already taken. That saves about
  $0.60.
- **Cases:** the same 16 (targets, empty-state, guards). 96 sends, about $1.25.
- **Readers:** reader A is Codex. Reader B is a **Claude subagent from a different model family**, which answers the
  "not independent" critique. Disagreements go to a third reader with the source.

**Predeclared, against the control's probe-1 numbers:**
- **Pass to the dev forward run** if the best arm has:
  - should-be-filed unfiled items at most 9 (control 15);
  - not-kept spans at most 13 (control 11, plus 2);
  - small theses at most 3 (control 2);
  - no new thesis on the guards (d1-22, 29, 113, empty-108);
  - format failures at most 1.
- **Stop and re-diagnose** if u1k removes the noise but not the filing gap and u1k+u3 does not keep it either. Then the filing gain in
  probe 1 came from the cut sentences or chance, and the next angle is the model's own account on the u1u3 answers.

**Why not the alternatives:**
- **The dev forward run now:** probe 1 crossed its noise falsifier, so that would be a run used to try a fix (AGENTS §7.3).
- **Keeping unfiled items stored:** that reverses D209, Alex's words. It is his call, not a council's.
- **Two calls (extract, then file):** that changes the Step 1 architecture (one call, Alex's design).
- **u3 alone:** it made unfiling worse (46 against 34). The why_unfiled field seems to invite rationalised drops, so it is not
  pursued alone.

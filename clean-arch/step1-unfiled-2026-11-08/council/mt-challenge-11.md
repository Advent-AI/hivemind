# Council mt, round 12: the identity comparison (D462)

Read `clean-arch/e2e-comparison-2026-11-13/step1-audit/IDENTITY-COMPARISON.md`. Check the table against the requests (clean:
`step1-audit/request-system.txt`, `request-user.txt`; production: `src/hivemind/prompts/role-v74i.txt` lines 13–16, 26), the census
results (both capex years, Ohio, memory per draw: CENSUS-FULL-RESULT.md, RESULT.md, opening-review/VERDICTS.md), and the stopped versions'
sentences (`clean-arch/step1-unfiled-2026-11-08/arms/c14-*.txt`, `c15yc-*.txt`; D441).

Attack: (1) whether production's clause is really the difference (both see open questions; production also has a later matcher and other
sentences); (2) whether the proposed clause can repeat D441's memory regression despite the written comparison case, and whether that case
is a standard line or a fit to the bench; (3) the examples (AGENTS §6: two or three per class, general); (4) the test (fresh articles from
after 2026-07-14 with a full-run draw's library as the before-state; guards; falsifiers). Say whether P goes to a written candidate and a
reviewed probe design, and with which changes. End with: "Council position: <...>".

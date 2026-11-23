# Council mw, round 11: the fresh week's result (lean step 2) and the next small step

Read, in this order:
- `docs/research/2026-11-14-use-acceptance/LEAN-LOG.md` §2 (the plan and the decision rule, frozen before any send, and the run's log);
- `docs/research/2026-11-14-use-acceptance/week/WEEK-RESULT.md` (the result) and `week/tally.txt` (every reader verdict joined to the keys);
  the reader files are `week/codex-A2.jsonl`, `claude-A2.jsonl`, `codex-B.jsonl`, `claude-B.jsonl`, `control-confirmation.jsonl`,
  `controls-B.json`; the builders `week/build_week_A2.py`, `build_week_B.py`, `tally_week.py`;
- `clean-arch/step1-unfiled-2026-11-08/council/mw-claude-week-reflection.md` (Claude's reading, written before this round, with the history
  it found afterwards);
- for the history: `clean-arch/step1-unfiled-2026-11-08/LOG.md` §§16–17, 19–20, 36–37; `docs/DECISIONS-log.md` D382, D384, D389;
  `clean-arch/step1-unfiled-2026-11-08/arms/c8-system.txt` lines 50–61 and 115–121.
- The stored runs, read-only, if you want to check a claim: `poc/data/clean-lean-week-2026-11-14/week-r2/c1` (clean) and `…/week/p1`
  (production).

Out of scope: the frozen ruler (it is not used to choose here), the judging prompt, Step 2, the network fix (round 10).

Challenge, with the file and line you rest on:
1. **The verdict.** Is "not clear" the rule applied as written? Is any count in the result wrong, or any reader verdict joined wrongly?
2. **Reading B.** Claude reads it as not separating the systems (7 judgements against 15; the gap comes from the Codex reader, which failed 2
   of its 4 confirmed supported controls, both production items). Is that fair, or does it explain away a real difference?
3. **Reading A.** Is the three-matter gap rightly traced to the request's do-not-open sentence, and is "by Alex's design (D382, §17, D384),
   optional under the question gold" the right status for it, or is Claude under- or over-stating it?
4. **The next small step.** The rule says it targets the largest difference observed. Claude's candidate: put to Alex whether the clean path
   keeps no question on the company's revenue and margin; if he reopens it, test one more opening reason gated on a quoted pair (the
   company's guide and a stated market expectation for the same measure and period), first on this week's stored states for a few cents,
   then one forward draw on the second fresh week (2026-09-29..10-05, never sent). Is this the largest difference? Does arm c1's failure
   (LOG §20) already answer it? Is there a smaller or better-aimed step, including on production's side (duplicates, trivia, 278 statements
   thrown away, the misfiled supply commitments)? What must the report to Alex not claim?

Name only what would make the result's reading wrong or the next step badly aimed. End with: "Council position: <one or two sentences>".

# Council gp: review of the Step 4 design, version 7 (fresh reviewer; read-only: do not edit files, run model calls or start runs)

You have not seen this work before. Review `clean-arch/step4-2026-11-10/DESIGN.md` (version 7) with its request
`clean-arch/step4-2026-11-10/ladder/candidate-system.txt` and schema `candidate-schema.json`, as a design that must be READY before
any code is written. Read `AGENTS.md` first (§1, §2, §6 and §7 govern a design, a prompt and a test). Open the code and the data behind
every claim you rely on.

## What is settled, do not reopen

Alex decided the two product choices on 2026-11-10: D397 (one judged question per thesis; other parts shown as not judged) and D398
(the ladder step carries D186 in full), `docs/DECISIONS-log.md`. The items under "Behaviour this design takes from production"
in §4 are marked there as reported to him or still to report. Five earlier reviews are in `clean-arch/step1-unfiled-2026-11-08/council/` (`gg-codex.md`, `gl-codex.md`, `gm-codex.md`,
`gn-codex.md`, `go-codex.md`); version 7 claims to answer every finding of the last (`go-codex.md`).

## Angles (answer each)

1. **go's findings.** Is each answered in version 7? Quote what is still missing.
2. **The contract (§5.1–§5.4, the schema).** Walk these five answers through the schema, checks 1–8 and the label rule, and say what
   is written for each: a yes/no event about the company; five states of a company event; five states of a theme event; a company
   figure with a stated reference; a theme figure with no reference. Then give any answer that passes every check and is a wrong
   ladder in a way §5.3's list of "what these checks do not establish" does not name.
3. **The request against its sources (AGENTS §6).** Read `candidate-system.txt` sentence by sentence against the source the table in
   §5.2 gives (v74i's lines in `src/hivemind/prompts/role-v74i.txt`, D38, D185, D186, D260, D397, D398). For each sentence: consistent,
   wider, narrower, contradicts, or no source. Does any sentence or example fit the covered company or a test article? Does the
   request ask for anything a check refuses, or does a check refuse what the request allows? Does the closing check repeat only rules
   stated above it?
4. **State × event (§7.1).** Name each reachable state-event pair with no row, a wrong row, or no stated date or sequence number.
   Check the rows against `src/hivemind/views/judging.py`, `store.py` and `clean-arch/e2e-2026-11-09/adapter.py`.
5. **Value × reader (§5.4) and new path × old checks (§7.3).** Name a reader or an old check (`src/hivemind/extraction.py` `sift`)
   still missing or misdescribed.
6. **The test (§8).** Can Stage A and Stage B each fail? Is any line impossible, unfalsifiable, or unfair to an arm? Are the
   denominators complete? Is the workload feasible (count the ladders and judgements the readers must read)?
7. **Could two engineers build different things from §5 and §6?** Name each place.

Out of scope: the frozen ruler, the frozen production prompts and judge (a defect in them is a finding, never an edit), c8, Step 2
and Step 3, `clean-arch/step2-validation-2026-11-07/LOG.md`, `reports/step2-*`, the frontend.

## Deliver

First line: READY, READY WITH CHANGES (name them; none may be a design decision), or NOT READY. Then the findings, most serious
first, each with its file and line and what a complete fix must contain; wording-level points in a short list at the end. Under
1,300 words.

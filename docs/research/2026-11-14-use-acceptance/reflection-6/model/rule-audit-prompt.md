You are an independent auditor. Read-only: do not edit files or start runs. No conclusion is preferred.

**The question.** The answer-choice step must turn a research topic into one judged question, or decline. A stronger model
(gpt-6.1-sol) declines more often than the current one, with the reason "the outcome names several parts, none of them the main one",
on topics where readers disagree whether a main part exists. Decide, from the sources, how the main part should be identified when
a topic's outcome names several parts. Then decide whether any general wording the sources support would reduce wrong declines
without making the step decline true no-main topics less, or pick one of two genuinely separate bets.

**Read:**
- the request: `clean-arch/step4-2026-11-10/ladder/candidate-system.txt`, `candidate-closing.txt` and `candidate-schema.json`;
- the reader form: `clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md` (the Q, L and N lines);
- the decisions: D397, D436 and D417 in `docs/DECISIONS-log.md` (search "## D397 ", "## D436 ", "## D417 ");
- the earlier rule review: `docs/research/2026-11-14-use-acceptance/unlisted-parts/rule-review.md`;
- the cases:
  - `docs/research/2026-11-14-use-acceptance/reflection-6/model/refusal-trace.txt`, sol's 24 declines with the readers' N marks and
    luna's matched answers;
  - the topics' text in `poc/data/clean-carried-run-2026-11-16/c1/cases/cases.json` and
    `poc/data/clean-second-week-2026-11-15/week-continued/c1/cases/cases.json`.

**Answer:**
1. What do D397, D436 and D417 say about the main part, quoted? Where are they silent?
2. For each topic in the trace, which part is main by the sources, or is there none? Mark each sol decline as justified,
   unjustified or the standard is silent.
3. Is there a wording, quoting only what the sources say, that would tell the model how to find the main part? Test it against
   every topic in the trace, including the justified declines, and say what it would change. If the sources do not settle it, say so,
   and list the boundary cases a ruling by the owner (Alex) would need, each with the two readings.

Be concise. End with one line: SOURCED WORDING EXISTS, or SOURCES SILENT: OWNER RULING NEEDED.

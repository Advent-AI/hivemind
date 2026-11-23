# Council hi: third blind whole-request audit of the ladder step's request (read-only: do not edit files, run model calls or start runs)

You are the blind second reader of a prompt audit (AGENTS.md §6, "The prompt audit"). You have not seen this work. Do not read
`clean-arch/step4-2026-11-10/DESIGN.md` §5.2's source table before you have written your own verdicts: it is the author's mapping,
and you are checking it blind. You may read the rest of the design for what the step does.

## The request under audit (everything the model would be given or held to)

- the system text: `clean-arch/step4-2026-11-10/ladder/candidate-system.txt`;
- the answer schema with every description: `clean-arch/step4-2026-11-10/ladder/candidate-schema.json`;
- the user payload's keys: `{"company", "fiscal_year_note", "themes": [{"id", "name"}], "thesis": {"id", "description", "outcome",
  "period", "opens_as", "settled_by"}, "item": {"publication_date", "publisher", "title", "text"}}`;
- the three examples inside the system text (an example is an instruction: AGENTS §6). `ladder/examples.json` is NOT part of the request and is never sent to the model: leave it out.

## The standard it must carry, and nothing else

- Alex's decisions, in `docs/DECISIONS-log.md`: D38 (a view: one question, a fixed ladder, a due date), D185 (18 months for a
  binding obligation), D186 with D368 item 1 (rungs against guidance; the favourable end), D248 (one bet, one question), D260 (the
  reference), D356 (the due day and publication), D397 and D398 (the two rulings of 2026-11-10 for this step), and D399 (the request teaches how to build an
  event's five states: the construction and its merger example are decided, so judge whether the text carries them rightly, not
  whether they should be there).
- Production's frozen ladder sentences: `src/hivemind/prompts/role-v74i.txt` lines 13, 16–17, 20–26 and 32–35, and production's
  request sentences on the object and the year in `src/hivemind/extraction.py` (`build_prompt`, `CLOSING`).
- The prompt principles of AGENTS §6: a general hedge-fund brain (no sentence or example fitted to the covered company NVIDIA or
  to a test article); a classification as a closed set with examples; a closing check at the very end that repeats only rules
  stated above it; an example must agree with the standard, the schema and the code that reads the answer; the request never asks
  for what a check refuses (the checks are DESIGN.md §5.3, checks 1 to 8; read them as they now stand, the number rule of check
  4 and the count of five of check 1 included).

## Deliver

1. **Request to standard.** A table with one row per sentence of the system text (number them), per schema description, and per
   in-text example: the clause in a few words; its source in the standard (decision or v74i line), or "none"; a verdict: consistent,
   wider, narrower, contradicts, or no source; one line of reason for every verdict that is not "consistent".
2. **Standard to request.** For each rule of the standard above that bears on writing a ladder: is it carried, carried wider or
   narrower, or missing? Name what is missing.
3. **Principles.** Any sentence or example fitted to NVIDIA or to a test article; any abstract clause where a closed set with
   examples is needed; any closing-check clause not stated above it; any place the request asks for what a check refuses or a
   check refuses what the request allows; any example that would fail a check or a reader mark (walk every outcome of each event
   ladder for overlap and gaps, including boundaries).
4. Then, and only then, open DESIGN.md §5.2's table and list each row where your verdict differs from the author's.

Under 1,500 words. Cite the line for every verdict that is not "consistent".


Two earlier audits (`gw-audit-codex.md`, `gy-audit-codex.md`) read earlier wordings of this request; the text has changed since
(a sixth `no_ladder` case, the five-state construction, the number wording, the reference's value). Do not open them before your
own verdicts are written; afterwards, say which of their findings the current text still carries.

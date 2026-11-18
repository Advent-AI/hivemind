# A source-backed product review of 51 written questions (read-only)

Each item in `packet.json` holds:
- a research **topic**, written by an analyst system: its `description` (the question asked), `outcome` (what is tracked), `period`
  and `settled_by`;
- the **article** the topic came from (date, publisher, title, full text);
- the **answer** a model wrote: one judged question with answer choices (`figure.ranges` for a quantity, or the event's rungs),
  `not_judged` (the topic's parts the question leaves out), `reference` (a quoted expectation, if any), `due_day` and its basis;
- the **passage** it quoted.

A later judge uses the question and its answer choices to record what happened, and an analyst reads the result. Earlier reviewers
already checked the system's formal lines. Your job is the product check they may have missed.

**For each item, check against the topic and the article:**
1. **Period:** does the question keep the topic's period or check date, or does it change the window (for example "this quarter"
   becoming "by year-end")?
2. **Quantity or event:** is the thing measured the one the topic tracks? If the question constructs a measure (an average, a basket,
   a formula, a specific data source), does the topic or the article support it, or is it invented?
3. **Conditions:** are the topic's conditions kept in the question or listed in `not_judged`, and is nothing added that the topic
   does not have?
4. **Answer choices:** can a judge apply them on the due day? Check that they do not overlap, leave no gap, and are in the right unit
   and scale. For an event, check that the rungs are distinct, dated outcomes.
5. **Usefulness:** would an analyst reading the question learn the answer to the topic's question?

**Return one JSON line per item, in order:**
- `item`;
- `verdict`: `"sound"` or `"defect"`;
- `class`: `null`, or one of `period_changed`, `measure_invented`, `measure_changed`, `condition_lost`, `condition_added`,
  `choices_unusable`, `other`;
- `material`: true only if the defect would change what the judge records or what an analyst concludes;
- `evidence`: the exact words from the question or answer, and from the topic or article, that show it, quoted;
- `why`: one sentence.

Judge each item on its own text; similar items may differ. Return exactly 51 lines, nothing else.

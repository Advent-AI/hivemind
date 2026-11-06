You are an independent, read-only reader. Classify 54 cases. Do not edit any file.

Material: /private/tmp/claude-501/-Users-lchingen-hivemind/c9c431b7-c05a-4b90-8212-66f99e875264/scratchpad/e1/reader-packet.json
- `links_rule_as_the_model_reads_it`: the exact filing rule the extraction model was given for its `links` field.
- `question_blocks`: the open questions the model was shown, with each question's "takes" line, keyed by id.
- `cases`: each case is a statement from a news article that a reference gold lists as useful evidence. A production extraction wrote it (see
  `dropped_statements`, as the model wrote it) with empty links, so code dropped it as "no home". Each case gives the source paragraph, the
  gold's span and meaning, the gold's question entries for the article (must_open / may_open / must_not), and per draw the question block shown
  (`questions_shown`) and any new questions the same answer proposed.
- The governing standard: /Users/lchingen/hivemind/docs/prd/05-extraction-standard.html (sections 3 and 4 say when a new question is opened;
  section 6 says a statement no open question takes is dropped as "no home").

For each case put the statement into exactly one class:
- LINK: at least one question in the shown block takes this statement under the links rule exactly as written (read the rule in full: the
  narrowest question; its own figure, step or estimate; the demand, supply, competition or pricing behind its answer; an estimate for another
  period or population of a question's quantity when no open question covers that period; and the fallback to the company-wide revenue
  question for a statement that moves the demand, supply, competition or pricing behind the company's results). Name the question id(s) and the
  clause of the rule that admits it.
- OPEN: no shown question takes it, and a question that would take it should have been opened (the gold's must_open or may_open for the
  article, or the standard's opening tests). Name the question.
- NONE: no shown question takes it under the rule, and no question should be opened for it (the gold's must_not, or it fails the standard's
  opening tests, for example a small matter for the company); the standard drops it as no home.
- UNSURE: only when the rule or the standard genuinely leaves it open; say which two readings compete.

Read the rule as written; do not widen or narrow it. "A shared company, industry, event or ecosystem is not a connection" is part of the rule.
When the draws show different question blocks, classify against the blocks shown (say if the answer differs between draws).

Out of scope: proposing fixes, reviewing prompts, judging whether the gold is right to call the statement useful, any other module.

Answer with one JSON array and nothing else, one object per case, in case order:
{"case": "K00", "class": "LINK|OPEN|NONE|UNSURE", "questions": ["v.."], "clause": "the rule clause or standard line", "reason": "one sentence"}

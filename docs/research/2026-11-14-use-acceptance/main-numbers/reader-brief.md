# Blind reader: what does each new question ask, and were the named facts kept and filed? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/main-numbers/reader-packet.json` and, for what
counts as one question or two, the signed standard `docs/prd/05-extraction-standard.html` §4 ("同一题、续期，还是另一题"). Open no other file in
that folder or anywhere else: keys, designs and other readers' answers exist and you must not see them.

The packet holds `articles` (each with its text, the questions that were already open when it was read, and, for some, `named_facts`) and
`answers` (several independent answers per article, from two versions of one system, in shuffled order; you are not told which is which and
must not guess). Each answer lists the `new_questions` it proposed for the company the articles cover (NVIDIA; its fiscal year ends in late
January, so fiscal 2027 is the year to January 2027 and fiscal 2028 the year after) and, for articles with named facts, its
`kept_statements` with the questions each is linked to.

For every answer:

1. **Each new question, by what it asks** (ignore any label; read the question, its outcome and its period):
   - `asks`: `revenue` (the company's own revenue) / `gross_margin` (the company's own gross margin) / `other_line` (another line of its
     statements: EPS, net income, cash flow, cash, capital expenditure, a small segment) / `quarter` (a quarter's figure or guide) /
     `other_company` (another company's figure) / `not_a_figure` (an event, a decision, an obligation, a shared quantity outside the company);
   - for `revenue` and `gross_margin`: `scope` (`total`, or `segment: <name>`), `fiscal_year` (`FY2027`, `FY2028`, `later`, `unclear`),
     `shape` (`level` or `growth`), and `named` = true when the question itself names the measure, its scope and the fiscal year (and, for a
     growth rate, the year it grows over) so that the year's reported figure settles it.
2. **Pairs in one answer:** every pair of its new questions that the same reported result would settle (§4: "同一个结果能判掉两题，就是同一题"), for
   example a level and its growth for the same measure, scope and year. A total and one of its segments is a pair only if their answers
   cannot move apart on what the article shows; say why.
3. **Each named fact of the article** (only where the article has `named_facts`):
   - `kept`: true when one of the answer's kept statements states this fact as the article does (the same figure, measure and period);
     give that statement's id; false when none does;
   - `linked`: the ids of the new questions that statement is linked to (empty when none);
   - `link_match`, for each such link: `same` (the question asks this fact's own measure, scope and fiscal year), `scope_differs` (for
     example a total-revenue figure under a segment question, or the reverse), `year_differs`, or `other` (say what).

Judge only from the article and the answer as shown. Write one JSON object per line, one line per answer:
{"answer": "A01", "questions": [{"id": "...", "asks": "...", "scope": "...", "fiscal_year": "...", "shape": "...", "named": true}],
 "pairs": [{"ids": ["...", "..."], "why": "<= 20 words"}],
 "facts": [{"fact": 1, "kept": true, "statement": "...", "linked": ["..."], "link_match": ["same"]}]}
Use empty lists where there is nothing; leave `scope`, `fiscal_year`, `shape` and `named` out for questions that are not `revenue` or
`gross_margin`.

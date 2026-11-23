# Blind audit of a one-sentence change to production's extraction role (read-only)

Repository `/Users/lchingen/hivemind`. The stored request as the model read it: `docs/research/2026-11-13-shared-quantity-price/request-p2-136-system.txt`
(the role) and `request-p2-136-user.txt` (the user text; the schema is `extraction.schema_for('v74i')` in `src/hivemind/extraction.py`). The
change replaces exactly this sentence of the role:
OLD: "industry_aggregate: one aggregate quantity for one calendar year, such as the combined capital spending of named companies."
NEW: "industry_aggregate: one quantity or price outside any one company that several companies move on, for one calendar year, such as the
combined capital spending of named companies or a raw material's contract price."
Sources: the signed standard `docs/prd/05-extraction-standard.html` §3 (the table of reasons; "问题怎么写") and §6 item 2 ("共同量"); D191 point
4 in `docs/DECISIONS-log.md` (Alex: "好").

Report: is the new sentence consistent / contradicts / keeps wider / keeps narrower / no source against the standard and D191? Does it
contradict any other sentence of the role or user text (for example "A number, a financial line, a target or a named customer project does not
by itself open a thesis", "A yearly metric … keeps the current/next-year limit", the theme list, the rungs and due-day rules for a theme)? Do its
examples read the same for any industry and name no covered company, product or number? Could it make the model open price questions an
analyst would not track (a single product's retail price, another company's own price, a price no public release settles), or stop opening
an aggregate it opens today? Name the words. Out of scope: other prompts; changing the standard.

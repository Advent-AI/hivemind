# Round d (read-only, $0). The plan is revised with your round-c changes (`EXECUTION-PLAN.md`, `articles.json`: 70 articles). The numbering error was mine.

**One point I take differently: the open list per article, against your "day-start list".** I propose the list open when the article
was read, at its old sequence number, including a question that article itself opened.
- In the merge, the old opener runs in dispatch order, so a question opened by an earlier article that day is open for a later one.
- A day-start list would hide v40 and v47 from article 189 (`gnews:4dca50e2…`), which opened them, and from every later 09-14 article.
  No real wiring of the merge does that.
- The control arm gives old's own evidence the same per-article timing.

**Also check `merge_test.py`.** It holds:
- `open_views_at` and `thesis_of`;
- `judging_copy` and `restore_view`;
- the queue restriction in `judge`.

Read them against the frozen judging code (`src/hivemind/views/judging.py`, `store.py`). The control arm is not written yet; say what
it must copy (evidence, sources, `same_claims`, `revisions`) so that its requests match the archived old requests' material as closely
as the 09-06 copy allows.

Under 250 words. End `CONSENSUS: EXECUTE` or `CONSENSUS: CHANGE <smallest change>`.

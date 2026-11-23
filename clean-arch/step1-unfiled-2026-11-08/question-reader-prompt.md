You are an independent reader for a hedge-fund research system. Read-only task: do not edit files or run model calls.

Read PACKET_PATH. Do not open any other file. Each entry is one news article about NVIDIA: the research questions (theses) the system opened while reading it ("opened"), every question open after it ("open_after"), and a reference list for that article: "must_open" (questions that should be open after this article), "may_open" (acceptable) and "must_not" (questions that should not be opened).

For each entry:
- for each opened question, in order: which reference entry it matches, if any. It matches when it asks the same underlying question; a different wording, deadline written differently, or one programme's or quantity's other phrasing still matches. Answer "must_open", "may_open", "must_not" or "none", and quote the matched reference entry;
- for each must_open entry: is it covered by any question in "open_after" (the same underlying question, or the broader programme or quantity it folds into)? Answer true or false and name the covering question.

Return only a JSON array: [{"id": "A1", "opened": [{"verdict": "must_open|may_open|must_not|none", "ref": "<quoted entry or null>"}], "must_open": [{"covered": true|false, "by": "<question or null>"}]}].

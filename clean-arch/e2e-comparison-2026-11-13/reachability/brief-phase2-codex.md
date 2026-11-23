# Blind reader, phase 2: compare your questions with the thesis a system opened (read-only)

Repository `/Users/lchingen/hivemind`. You wrote phase 1 (`clean-arch/e2e-comparison-2026-11-13/reachability/codex-phase1.jsonl`, where READER is
your file name as given below). Now read `reachability/packet-phase2.json`: for each case, the thesis a system opened from that article (its
judging step later declined to write answer options for it). Read nothing else in the folder.

For each case, answer:
- **same matter**: which of your phase-1 questions (quote it) is about the same underlying matter as the thesis, or "none";
- **thesis shape**: can the thesis as written be laddered (one main figure for one period, or one event with a check date)? If not, why
  (two figures with none leading, a rolling window, an unsupported period, other);
- **reachable**: does the article support a question on the same matter that can be laddered and is worth asking (yours or another)? yes / no;
  if yes, would it lose anything the thesis tracks that matters to an analyst?
- **declining right**: if not reachable, is declining (no question in any ladderable shape) the right outcome by the standard and D417? yes / no.

Return one JSON object per line:
{"case": n, "same_matter": "<your question or none>", "thesis_ladderable": "yes|no", "thesis_problem": "<<= 25 words>", "reachable": "yes|no",
"reachable_question": "<the ladderable question, or null>", "loses": "<what it loses, <= 25 words, or 'nothing'>", "declining_right": "yes|no|n/a",
"note": "<= 30 words"}

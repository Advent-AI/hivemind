Revised for your blocker:
- the whole sent request is checked to equal live.deepseek_json_mode(stored request), not only the user message;
- the matcher now needs a kept passage that contains the whole gold passage, or lies inside it covering at least 60% of its length;
- D(q, case) counts only gold items the frozen gold cites for q (gold_questions()), and only links to existing theses;
- errors and refusals count as draws that delivered and wrote nothing;
- draws are capped at 3, and the worst case is printed ($4.16 at the 64k cap; $0.54 expected);
- the run uses PYTHONDONTWRITEBYTECODE.

On stored answers the stricter matcher still finds all gold facts written. Files: stage1_probe.py, stage1-frozen.md (re-frozen sha256 in stage1-frozen.sha256). Under 150 words: SEND or the blocker.

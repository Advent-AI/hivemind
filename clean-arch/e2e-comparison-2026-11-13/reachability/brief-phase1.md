# Blind reader, phase 1: which questions does each article support? (read-only)

Repository `/Users/lchingen/hivemind`. You are independent. Read ONLY these files: `clean-arch/e2e-comparison-2026-11-13/reachability/packet-phase1.json`
(eleven cases: an article and the research questions already open when it arrived), the signed standard `docs/prd/05-extraction-standard.html`
§3 (opening reasons, "问题怎么写") and §4 (opening tests; "同一题、续期，还是另一题"), and in `docs/DECISIONS-log.md` the records D417 (a rolling
window with no publication day is not given a question; Alex: "确认：这类题不出题") and D436 (a second side of the same bet is one question). Do not
open any other file in the `reachability` folder or elsewhere in `clean-arch/`: a system's answers exist and you must not see them.

For each case, as a senior hedge-fund analyst covering NVIDIA, list every question this article supports that is worth tracking on its own
(standard §3 reasons and §4 tests: a big matter, an outcome later material can settle) and that no open question already asks. Several cases
share an article but have different open questions: judge each against its own list. For each question you list, judge two things apart:
- **worth asking**: yes, with the §3 reason and the §4 test it passes;
- **can be laddered**: yes when it asks about one main figure for one period (a calendar or fiscal year, or a stated date) or one event with
  a check date; no when the source supports only a shape that cannot be (a rolling twelve months with no publication day, two figures neither
  of which leads, a period the source does not support), saying which.
Also list a matter the article raises that an analyst would track but the source supports only in a shape that cannot be laddered, as
"decline", with the reason. Small matters open nothing; say "nothing" when nothing qualifies.

Return one JSON object per line:
{"case": n, "question": "<the question as you would write it, or null>", "matter": "<a short key for the underlying matter>",
"quote": "<= 40 words from the article>", "worth_asking": "yes|no|decline", "reason": "<§3 reason and §4 test, <= 30 words>",
"can_be_laddered": "yes|no", "ladder_note": "<main figure and period, or event and check date; or why not, <= 30 words>"}

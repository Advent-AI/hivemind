# Review packet: one change to filing, one test (round 1, written by Claude, 2026-11-04)

Alex: "就测试一种，一次 … 能不能自己有个超级自信的定论和证据再给我提建议". So: one change, tested once (three sends per article, the
sampler minimum, AGENTS §7.3), decided by rules written before the send. This packet is for reviewers who did not write it. Read-only:
do not edit any file, do not send any model call.

## Goal (end to end)

Each question's judgement must receive the facts that move its answer, and the total-revenue question must not keep receiving what no
judgement uses (its reading grows with the news flow; a three-month run halted on it, D358). Frozen: the rulers (AGENTS §7.1). The change
is to the frozen extraction request (D274), a new version only Alex opens; he opened this one ("好你试试看").

## Evidence (all in docs/research/2026-11-04-filing-end-to-end/; numbers re-derivable by the scripts named)

E1 Total-revenue pile, frozen v108 draws of 2026-11-03 (`sink_by_standard.py`): of its statements whose article the extraction gold read,
   32–39% the standard does not keep, 31–44% kept but used by no question in the judgement gold, 11–18% used only for other questions,
   7–10% used for q01. Reader B's q01 rests on 12 items, none another company's revenue, backlog or partnership.
E2 The total-revenue judgements cite those pieces: 24–44% of their citations are about another company or the market (Intel Arc retail
   price, Greenpeace on Taiwan gas plants, Broadcom revenue), three frozen draws.
E3 The narrow custom-chip question (q16) never received Broadcom's figures in any draw (`trace_lost.py q16`) and was judged below $40bn three
   times with "no reference"; readers A and B both rest q16 on Broadcom's revenue.
E4 Today's resend of byte-identical requests (54 articles of draw 1, rebuilt by the production code; key order checked against the
   pre-cleanup code) files about half as many statements under total revenue as the archive did on 2026-11-03 (36–43 against 75 on the
   41 pile articles) and writes 17% fewer statements; cause not confirmed. Every comparison below is against today's resend.
E5 Four rules sent 3 times each (`answers.json`, `measure_filing.py`; the stop condition of `predictions-filing.md` fired on the paired
   metric, which double-counts facts the gold uses for two questions):
   - total-revenue intake on the pile articles: stored 36/42/43, definition 41/43/36, no_fallback 13/15/18, definition_no_fallback 15/14/16;
   - core present (of 59): 51/52/51, 51/52/50, 51/49/47, 52/53/50; supporting (of 103): 67/72/74, 74/82/76, 56/59/59, 62/62/70;
   - not-kept spans present (of 427): 67/73/64, 65/74/62, 50/51/51, 52/54/55; dropped for no home (3 sends): 81, 80, 146, 154.
E6 Removing the fallback also drops facts the stored rule filed to specific questions: of the important matters homeless under
   no_fallback, their counterparts in the stored sends went to a specific question 63 times, to total revenue 51, homeless 14, unwritten 10.
E7 The definition sentence moved facts between questions: Broadcom items from the share question to the custom-chip question (custom-chip
   gains 2/3 per item), and Morgan Stanley's Rubin rack and GPU prices from the Blackwell/Rubin revenue question (stored 3/3) to capex,
   memory and shipping questions.
E8 Neutral re-file in a second turn, rule text visible (`probe_refile.py`, `refile-no_fallback-with-rule.json`): of 42 homeless statements
   the judgement gold uses, 20 re-filed to the gold's question, 13 to another (mostly defensible: net income to EPS, a GPU price to Rubin
   revenue), 9 still none; but 7 of 24 not-kept and 21 of 47 kept-but-unused statements were also linked, about half to total revenue.
   Without the rule text visible: 11 / 8 / 23. Earlier "asked afterwards it files correctly" (4/4, 6/6) came from probes that named the
   question, a leading form.
E9 The model's own account of the stored filings (`probe-filing-account-d1.md`): it filed competitor and customer facts under revenue by
   the fallback sentence; it rejected the narrow questions as "not the question's own figure".

## The one change Claude proposes to test

"no_fallback + re-check": the links rule without the fallback sentence (`links-rules.json` key `no_fallback`), and at the very end of the
user message, after the closing check's "Return only the evidence items you keep.", one filing check:

> Then read back the links of each item you keep. An item with no link: compare it once more with every question in [Open questions] and
> its takes line, including the variants, stopgaps and other names a takes line lists, and give it the narrowest question whose answer it
> makes more or less likely; leave it empty only when none is connected. An item linked only to a company-wide revenue or margin question:
> when a specific question's answer is the one it makes more or less likely, link that question instead.

Why this one: E1–E3 say the fallback's home is wrong and harmful; E5–E6 say removing it alone loses facts; E8 says the model, made to look
again with the rule in view, finds homes for most of them; AGENTS §6 says a test the model must apply to each statement is a check at the
end of the same prompt (Alex, 2026-10-30). The definition sentence is not tested (E7).

## Decision rule (to be frozen before the send; control = today's stored sends)

Adopt as the candidate for a 14-day run (Alex's word) only if all hold over the three sends: total-revenue intake at most 0.7 × the stored
mean; gold-used items reaching at least one question the gold uses them for, per item (not per pair), at least the stored mean; core
present at least the stored minimum − 2; not-kept present at most the stored mean. Otherwise: the in-call re-check does not fix filing;
prompt-level filing work stops and the filing stays as frozen.

## What reviewers are asked

1. Is this the single change the evidence supports best? If another single change is better supported (including no change), say which and
   why, citing the evidence.
2. What in the evidence is weaker than stated, or misread? Check against the files, not this summary.
3. The re-check text: does every clause trace to the standard (§6, §5.1, §5.3) and the decisions (D207, D259, D265, D273)? Can it pull
   back the noise E8 saw? Is it general (a bank, a drug maker, a retailer)?
4. The decision rule and the metric: can they pass a change that hurts, or fail one that helps? Would the per-item metric be gamed by a
   statement linked to many questions?
5. What do you predict the test will show, with reasons?
Out of scope: the rulers' files, the judging step, every other part of the extraction request.

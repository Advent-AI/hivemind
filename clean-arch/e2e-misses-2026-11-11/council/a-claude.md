# Council A: Claude's own reading, written before reading Codex's (2026-11-11)

All on saved data, no model call. Files: `trace_question.py`, `poc/data/clean-e2e-misses-2026-11-11/trace-q17.json`, `trace-q22.json`,
the three replayed draws `control-d{1,2,3}/` (each reproduces its saved run, 239, 269 and 251 judge requests).

**The clean misses, by owner.**
- Capital spending (q12), 3 of 3 draws, production too: traced (D394): Step 1 does not write the cash-flow identity.
- Ohio guarantee (q23), 2 of 3 draws: traced (round log §48): Step 1 folds the unsigned guarantee into the open aggregate thesis.
- China share (q17), draw 3; FY2028 revenue (q22), draw 2: untraced until now.

**China share, draw 3.** Gold 1 to 8% (rung 4, 1 to 5%). On 2026-07-08 the report that China will let Alibaba, ByteDance and
DeepSeek buy fewer than 200,000 H200s arrived in all three draws, with the figure, in the request (checked: "200,000" in the
request of every draw that day). Draws 1 and 2 moved 5 to 4 that day; draw 3 stayed at 5 after one refused answer and its re-send.
The reasons share one frame, "1% of a roughly $50 billion market is about $500 million", and split on whether a limited tranche
clears it: no H200 price is in the evidence, so nothing lets the judge size 200,000 chips. After that day no draw changes its rung
again (d1, d2 hold 4 to the end; d3 holds 5), and production's control does the same: 4 in one draw, 5 in two. Lead: the judge's
own split at the 1% boundary on the arrival day, then held. Not an input difference.

**FY2028 revenue, draw 2.** Gold $560 to $640 billion (rung 2, $550 to $650 billion). Every draw anchors on the consensus of about
$554 billion and on $392 billion times 41% = $553 billion, $3 billion above the boundary. On 2026-07-10 a Trefis line ("about 32% a
year for the next few years") arrives; it takes the question to rung 3 in clean draws 1 and 2 and production draw 4 (production draw
3 to rung 5). Draw 1 returns to 2 on 07-13 and draw 3 on 07-14; draw 2 stays at 3 through 07-14. Two input differences in draw 2:
Step 1 filed the second "41% in 2027" statement (`60:e2`) under FY2027 revenue only, so draw 2's question shows one 41% item where
draws 1 and 3 show two; and its final reasons misread its own figure, "the separate 41% growth view implies about $553 billion,
close to but still below the rung-2 boundary" ($553 billion is above the $550 billion floor).

**Why both questions sit on a boundary at all.** The gold's upside items for FY2028 (hyperscaler spending stepping to over $1
trillion, Huang's $1 trillion of Blackwell and Rubin sales, a higher FY2027 base) are filed under other questions in every draw,
so the clean system stays at consensus, $3 billion from the line. For China, no price for an H200 is in the evidence.

**The class.** The window-end rung differs between clean draws on 6 of 22 questions (v3, v9, v11, v16, v17, v22); 4 of them still
agree because the gold range spans both rungs. 11% of later judgements change the rung (8% in production): a question tends to keep
the rung it reached on the day its decisive news arrived.

**What would decide it, cheaply.** Re-send the saved request three times: draw 3's China request of 07-08 (if any answer is rung 4,
the arrival-day decision is the judge's own split) and of 07-14 (if all stay 5, the held rung carries it); draw 2's FY2028 request
of 07-14 beside draw 3's of 07-14 (if draw 2 stays at 3 and draw 3 at 2, the input differs; if both are mixed, the judge's split).
About 12 to 15 sends, a few cents. A hand-built request with `60:e2` added would be a sizing, not a replay, and is not proposed.

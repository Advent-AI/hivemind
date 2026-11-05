**The reframing is right: test whether supplying the missing evidence fixes the answers before designing another extraction change. But Claude’s proposed q16 test is incomplete, and the revenue pile must remain an explicit product problem.**

The concrete distinction: delivering NVIDIA’s “roughly 66 percent” statement repairs missing input. It does not establish that the judge can forecast **full-year non-GAAP** operating margin from a reported quarterly comparison.

**a. Narrow the experiment, not the product goal.**

Working backward from q10, q12 and q16 is a better diagnostic than maximizing 122 delivered facts. It identifies whether the next intervention belongs in finding, quotation, delivery or interpretation.

Those three questions are not a replacement acceptance standard. The [PRD’s goal](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md:20) includes both supplying useful evidence and keeping unrelated material out. Revenue agreeing does not excuse its irrelevant citations: the PRD records **24–44%** of its citations as other-company or market news. Noise can damage explanations and increase request size without changing the selected answer.

Keep the fallback-removal trade-off visible: **83 fewer parked records, 34 fewer noise records, 12 fewer useful deliveries, 25 more homeless facts**. Alex must choose whether that loss is acceptable; unchanged revenue accuracy cannot choose for him.

**b. One buildable experiment—with a correction to q16.**

**i234 and i139 are only q16’s reference evidence.** Its [frozen answer](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json:709) also cites i155, i228, i300 and i138. The previous script selected five items, omitting i228. Testing the two Broadcom items alone cannot refute “complete delivery fixes q16.”

Use the following complete cited sets, including IDs appearing only in the explanation:

| Question | Items and source context supplied |
|---|---|
| **q10: operating margin** | **i163, i084, i153, i281, i302, i295, i217, i142.** Preserve the full Micron/NVIDIA comparison; the actual 74.9% sentence following i084’s net-income quotation; Q2’s 75% guidance and China exclusion; revenue/net-income growth; management’s accelerating-growth statement; the memory-cost paragraph containing **435%**, which precedes i217’s quoted passage; and Micron’s 86% guidance. |
| **q12: NVIDIA capex** | **i131, i007, i006, i001, i285, i120, i301, i052, i145, i295.** Preserve both cash-flow operands together and the article’s FY2027 identification. Include the investments, guarantees, backstop, buyback, proposed borrowing and growth statement. For i145 include the explicit absence of a construction schedule, investment amount or permit. Preserve that Gradium’s $100m is the whole funding round. |
| **q16: custom silicon** | **i234, i139, i155, i228, i300, i138.** Preserve Broadcom’s reported quarter versus guidance, AI-semiconductor category, named custom-chip customers, Trainium’s unspecified period, Jalapeno’s June introduction, late-2026/2027 production timing, and Bloomberg’s through-2033 growth forecast. |

These come from [packet-v1.json](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/packet-v1.json) and their stored articles. Do not relabel AI-semiconductor revenue as pure ASIC spending, infer a non-GAAP basis for i163, or supply the gold’s calculations, forecasts or reasoning.

**Construction:**

- Fix **frozen v108 draw 1**, endpoint **2026-07-14**, before sending.
- For q16, reconstruct its last archived request through `model.build_request` and `judging.schema_for("judging-v7")`; require its original request hash, as [one_test.py](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/one_test.py:50) does. Add only the prepared evidence block.
- For q10/q12, call [`judging.build_prompt`](/Users/lchingen/hivemind/src/hivemind/views/judging.py:166) against the read-only endpoint ledger. It obtains `store.view`, `store.rungs_of`, `evidence_in_view`, `store.dependencies_of`, `store.current_state` and `themes_in_force`. Format additional pieces with `_lines_english`; build the request with the same frozen schema and configuration.
- Label these **constructed endpoint requests with constructed evidence records**, not historical replays or successful extraction. Maintain a manifest from each synthetic `e…` ID to packet ID, article ID and exact source span. Preserve attribution and uncertainty. The formatter truncates quotations at **400 characters**: split necessary context into separately identified spans before formatting.
- Preserve existing evidence, previous conclusions, dependencies and themes. In particular, q10 has **no dependency on q03**, although reader B used q03’s conclusion. Do not secretly inject that conclusion. Failure therefore identifies a remaining downstream obstacle under current wiring, not necessarily arithmetic alone.

**Controls and sends:** q10/q12’s production controls remain “no judgement”: the scheduler skips empty evidence. Do not force artificial empty-input calls. Send q16’s unchanged control three times and each supplemented question three times: **12 fresh calls**, without cached answers.

Run the required preflight and validate every answer with `model.check_schema` and `judging.check_answer(..., request_text=...)`. Retain refusals and raw responses.

**Reading and decision:** Claude and an independent reader who did not assemble the evidence should read every response against the actual request. Report mechanical agreement separately from unsupported reasoning.

The [frozen scoring rule](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py) tests overlap with the selected interval—not similarity to the written forecast:

- q10: positions **1 or 2** agree with 65–69%.
- q12: positions **3 or 4** agree with $7–11bn.
- q16: positions **3 or 4** agree with $60–85bn.

If any supplemented question produces **source-supported agreement in at most one of three sends**, reject “complete delivery reliably fixes all three.” Two or three successes are diagnostic encouragement, not production acceptance.

**Cost:** repository [`model.PRICES`](/Users/lchingen/hivemind/src/hivemind/model.py:29) gives $0.10/M input and $0.50/M output. With a checked 10,000-input-token ceiling and the configured 16,000-output-token cap, twelve calls budget **$0.108 before retries**, ignoring cache discounts.

**c. Sentence pointers solve a real, small problem.**

They prevent invented quotation wording **when the selected span is correct**. They do not prevent selecting Micron’s margin instead of NVIDIA’s, omitting a fact, choosing the wrong destination or making the wrong inference.

The verified approximately 1% affected gold fact-sends makes this a bounded source-integrity improvement, not the demonstrated breakthrough. It also changes the frozen extraction interface.

No finding/derivation redesign currently has stronger evidence. [D273](/Users/lchingen/hivemind/docs/DECISIONS.md:3140) records that a section-walk instruction failed; more reasoning recovered facts while increasing noise. The judge already requests accounting derivations. Adding another instruction or stage before this experiment would repeat the premature-design mistake.

**d. One recommendation, one test.**

**Recommendation:** authorize the complete-evidence experiment above before choosing another mechanism.

It decides whether better evidence delivery offers enough downstream benefit to pursue. It does not accept a filing design, resolve the revenue pile, prove general reliability or authorize changing frozen components.

Alex must authorize this diagnostic after the failed-test stop and amend PRD 10’s prescribed next work. Later extraction changes require reopening D274; judging changes require D354; architecture changes require the relevant D207/D209/D264 decisions. No frozen ruler changes are needed.

No files edited; no model calls sent.
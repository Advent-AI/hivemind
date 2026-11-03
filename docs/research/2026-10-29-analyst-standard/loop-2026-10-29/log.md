# Direct-read loop, 2026-10-29 night

Alex: "你根本不要再给我跑什么三轮了。每一篇的问题明显地出错的你不要再用工具尺子了，你直接下去看；改动分提示词准则你有了按照他下去改，并快速实验"
and "你也不用全部读完，看到问题差不多就下去自己改了，持续这个loop".

Method: one send per article on the 118 bench articles (gpt-6-luna, production bytes via `extraction.request_for`), the
answers read beside the article text by hand, every change written as a general rule with examples from other industries
(AGENTS §6), the model's own account asked where a rule's effect was unclear (`loop.py probe`). No score: the counts below
are counts, not a ruler. Script: `../loop.py`; answers: `<tag>/answers.sqlite`; probes: `<tag>/probes.sqlite` and `probe-*.txt`.

| Run | Request | Evidence kept / empty answers | Questions (obligation / driver / aggregate / policy) | Read by hand |
|---|---|---|---|---|
| v23 draw 1 | role-v23, poc-v39 (D237 scrub) | 833 / 5 | 9 / 17 / 8 / 2 | 45 articles with text: other companies' own results and valuations kept (Intel, Microsoft P/E, Palantir, IREN, Strategy, Google–Klarna, Trump's trades); game lists, retail deals, driver news kept; one hire or deal split into five items; the credit-support question of page 82 missing |
| v24 | role-v24, poc-v40 | 687 / 8 | 9 / 19 / 9 / 2 | the junk above gone on most pages; new error: an obligation question on NVIDIA's unsized, completed Verkada stake (model's account: the new "whether or not the item gives an amount" covered stakes); a customer's campus opened as a main-driver date (pages 3, 39); media relays of announcements written as rumour |
| v25 | role-v25, poc-v41 | 622 / 11 | 11 / 16 / 9 / 2 | page 82 opens its obligation question; Verkada and Firmus questions gone; all 11 empty answers are pages with nothing to keep (Burry shorts, game list, retail deal, trading cards, an unrelated page, a 415 W rumour); new error: memory-supply statements dropped (35 → 14 items; page 260 lost "memory is half of 2027 data-center spend", the model citing the v24 other-company clause); technical throughput figures still kept as named-party claims (page 355, model's account) |
| v26 | role-v26, poc-v42 | 672 / 7 | 12 / 17 / 8 / 3 | memory items back (14 → 21; page 260 keeps "memory is half of 2027 data-center spend" and "NVIDIA locked in its memory supply"); obligation questions on 3, 15, 39, 82, 111, 143, 210, 260, 267; no Verkada or Firmus question; page 355's eight throughput figures down to a customer trial and a partnership; still wrong: one reported measure split into four items (page 211: a segment's revenue, share, yearly and quarterly growth), partner pages pull in the partner's own details (Hesai lidar costs, Valar's reactor permits), Micron's "tight conditions until 2028" missed on page 379, Microsoft's $627 billion backlog missed on page 41 |
| v27 | role-v27, poc-v43 | 615 / 9 | 13 / 16 / 8 / 3 | one reported measure is one item (page 211: the segment's revenue, share and growth in one); page 260 keeps the memory items and the reported Vera Rubin delays; page 379 keeps "Micron said tight conditions could last until 2028"; new error: an obligation question on an officer's standard indemnity agreement (page 38; model's account: it read the indemnity as a guarantee); a partner's integration date opened as a main driver (page 381, Hesai sensors) |
| v28 | role-v28, poc-v44 | 639 / 10 | 13 / 20 / 8 / 2 | the indemnity question is gone (page 38); the Hesai integration date is gone (page 381); new error from the new word "lease": an obligation question on the company's own office lease (page 396); the empty answers are again pages with nothing to keep (a game driver post, a technical blog, a game list, a retail deal) |
| v29 | role-v29, poc-v45 | 627 / 8 | 10 / 17 / 6 / 3 | no lease, indemnity, stake or customer-campus question; the credit-support question opens on pages 3, 15, 37, 39, 82, 111, 143 and 262, supply commitments on 260 and 267; keyword counts against v23: other companies' valuation and finance lines 19 → 1, investor trades and share moves 9 → 0, retail, game and driver lines 15 → 3; the 8 empty answers are pages with nothing to keep; still open: a partner's own details on partner pages, an 8-K's compensation lines, NVIDIA's $3.4 billion cloud purchase from IREN never opened, the OpenAI Ohio question in about half the sends, Rubin-by-Q3 from an anonymous commenter opened once (page 380) |

Prompt size: role-v23 9,841 characters, role-v29 10,643 (+8%); input tokens per call 4,336 → 4,518, output 1,614 → 1,356. The growth is the
standard's reject and obligation rules that role-v23 did not state; four sentences that restated the schema or named a list the request does
not show were cut in v25.

Code found on the way: an event question that names its quarter ("first shipments by the end of Q3 2026") was refused as a
quarterly figure (3 of 169 stored event questions, all from page 199); the quarter rule now skips event measures
(`extraction.sift`, test `test_admission.py::test_an_event_question_naming_a_quarter_is_not_a_quarterly_number`).

Stopped after v29 (D239): Alex chose role-v29 as the extraction request ("A，这是最新版"); `poc-v45` is the replay default. Config
files v39–v45 carried `version: poc-v38` during this loop (my copy error); the loop stored the config path, and the request bytes do
not contain the version, so no answer here changes; each file now names itself.

Same ruler as the morning, code half only (`same_ruler.py`, $0: reference v2 matched by quote with `score_week.matches`, every
answer re-sifted with the current code; meaning not read by hand; v29 is one send, role-v22 three):

| | role-v22 luna-1 / 2 / 3 | role-v29 |
|---|---|---|
| records kept (118 articles) | 937 / 956 / 954 | 627 |
| core kept / lost | 48/2, 48/2, 47/3 | 47/3 |
| supporting kept / lost | 77/8, 81/4, 77/8 | 78/7 |
| kept records matching no reference statement | 706 / 724 / 718 | 407 |
| records kept on the 37 articles whose reference keeps nothing | 206 / 175 / 171 | 91 |
| obligation questions on an unsized stake, the Intel stake or a debt issue | 3 / 3 / 3 | 0 |
| questions naming the product generation (Kyber) | 4 / 4 / 4 | 8 |

The morning's hand labels found about two thirds of role-v22's unmatched records unrelated (464 of ~716).

Correction to the D238/D239 open-class list ("each seen on one or two pages"), from reading v29's records against the reference
(`v29_rest.py`, `lost_vs_v22.py`): on the 37 articles whose reference keeps nothing, v29 still keeps 91 records on 30 of them.
About 55 are releases, integrations, partnerships, research papers or customers' use of the company's products with no business
scale, mostly on the company's own blog pages (ICML papers 10, a robotics-library integration 9, an agent-framework post 9, a
humanoid-model post 4, a countries programme 4, efficiency post 5, Palantir's use of the models 5); about 7 are famous investors'
or commentators' general views (Burry's index overvaluation, Cramer on customers' complaints); 3 are the company's market valuation
multiple; 8 are one research-centre opening told in eight lines; 2 are 2025 tariff background; 5 are game and driver lines.
Of the 10 core or supporting statements the code flags as lost, 5 are kept in other words (the quote match misses them), 3 were
missed by role-v22 as well, and 2 are real losses role-v22 kept in 2 or 3 of 3 draws: a memory supplier's results and margin, and
the memory supplier's view that tightness lasts to 2028 (on a second page; page 379's was restored in v27).

## Class by class after D239 (Alex: "你一类一类改，快速迭代然后测regression")

Regression check per round: `regress.py <old> <new>` (reference v2 by quote match, an alarm only; every flagged article read by hand).
Noise floor of one send, from v28 against v29 (a one-clause change about leases): 4 reference statements lost and 3 gained, article
record counts moving from 4 to 17. A loss is a regression only when the reading traces it to the new sentence.

| Run | Change | regress.py (old → new) | Read by hand |
|---|---|---|---|
| v30 | reject list: an adoption, integration, partnership or research result without business scale, even with well-known names | records 627 → 558; on nothing-to-keep articles 91 → 63; core 47 → 48; supporting 78 → 75 (lost 5, gained 3); empty answers 8 → 12 | fixed: partner's own details (Valar pages 17 → 3 and 7 → 1, Hesai's own costs and subsidies gone), conference papers 10 → 2, robotics-library integration 9 → 2; regressions caused by the sentence: a bank choosing a rival's inference chips (SambaNova page), a cloud's launch on the company's systems with its capacity contracted (Bleeding Edge), the company choosing a supplier's CPU (Intel page); the example "a hospital chain now runs the vendor's scheduling software" teaches a customer's deployment as junk. Not the sentence: the DeepSeek chip report refused by the quote check |
| v31 | v30's sentence narrowed: an integration of the company's software, models or tools into others' products or research, or a research or award result, without business scale; a customer's purchase, order or deployment and a choice of supplier or rival are actions | records 627 → 588; on nothing-to-keep articles 91 → 62; core 47 → 48; supporting 78 → 78; empty answers 8 → 19 | the three v30 regressions are back (SambaNova's bank customer, Bleeding Edge's launch, the supplier CPU choice); the 19 empty answers are all articles whose reference keeps nothing (game lists, retail deals, trading cards, the Palantir partnership pages, technical blogs, one hire); the H200 China permission was written but refused by the quote check (as in v28: a quote-check class, not the prompt). Surprise losses (`surprise.py`: kept by every other run, lost here) are 0–4 per run (role-v22 draws 2, 1, 0; v27 4); v31 has 3, and the model's own account ties one to the new sentence: the competitor's own inference chip read as "a research result". Vera Rubin's production status was dropped under the older product-detail clause (its own account), kept by all ten earlier runs |
| v32 | "a research or award result" narrowed to "a published paper or an award" | records 627 → 534; on nothing-to-keep articles 91 → 53; core 47 → 47; supporting 78 → 77; empty answers 19 (all on articles whose reference keeps nothing); surprise losses 0 | v31's three losses are back (the competitor's chip, Vera Rubin's production status, the competitor's like programme); SambaNova's bank customer is written (the quote match misses it); the custom-silicon competitor's customers were left out once, and the model's own account names no instruction for it (a sampled miss). Class 1 accepted at v32 |

Quote refusals per run (`quote_refusals.py`): role-v22 4–6 of ~960 written, v24–v31 3–11 of ~600; quotes joining three or more separate sentences 0–2 per run. The H200 China report was refused in v28 and v31 because its quote joins three paragraphs; the D236 repair rightly refuses that. Not a class to change now.

Prompt size: role-v29 10,659 characters, v32 11,196 (+537, nothing cut). AGENTS §6 asks for a cut of at least as much or a written reason; a cut round (merging overlapping reject items) follows the class rounds, measured like them.
| v33 | kind (2) adds a counterparty's reported figure, with two examples (a customer's backlog, a supplier's margin) | records 534 → 578; supporting 77 → 81; core 47 → 47 | the memory supplier's results and margin and its tightness-to-2028 view both kept; the hyperscaler customer's growth and backlog kept |
| v34 | the v30–v32 rejection removed (D240): a named party's action is kept without an amount, its weight judged apart | (sending) | role-v34 = role-v29 with v33's kind (2); 10,812 characters |

Mistake recorded (D240): v30–v32 rejected a partner's integration of the company's software, papers and awards without business
scale. The standard's kind 2 keeps a partner's action with a name, and its §2 says incomplete or unofficial information is still
evidence. The rule was written toward my own reference's "keeps nothing" labels on those pages, a ruler of my own (AGENTS §7).

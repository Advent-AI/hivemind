| | r4 control (poc-v26) | r5 arm (poc-v29) |
|---|---|---|
| theses | 45 | 44 |
| theme_theses | 6 | 8 |
| judgements | 186 | 305 |
| asset_judgements | 175 | 287 |
| requests_with_block | 0 | 245 |
| with_theme_push | 0 | 194 |
| propagation_only | 0 | 123 |
| propagation_only_changed | 0 | 13 |
| rung_moves | 9 | 13 |
| judge_calls | 186 | 307 |
| judge_input_tokens | 1144991 | 1924965 |
| cost | {'extract': 0.819, 'judge': 0.319, 'match': 0.193} | {'extract': 0.844, 'judge': 0.521, 'match': 0.22} |
| cost_total | 1.331 | 1.585 |

asset theses with the same question in both ledgers: 5; first 10 with their last reasons:

### NVDA: How much total revenue will NVIDIA report for FY2027?
- r4 rung 1 (2026-08-15): Rung 1 remains the best-supported forecast judgement, but the FY2027 outcome is not established: no supplied fact reports NVIDIA’s FY2027 total revenue. FY2026 revenue was $215.938 billion, so rung 1 requires at least $259.1256 billion (e6). NVIDIA reported Q1 FY2027 total revenue of $81.6 billion (e27) and guided to Q2 revenue of $91.0 billion, plus or minus 2%, with no Data Center compute revenue from China assumed (e25). Combining Q1 actual revenue, Q2 guidance, and the roughly $103.1 billion
- r5 rung 1 (2026-08-15): Rung 1 remains the best-supported forecast, but FY2027 revenue of at least $320 billion is not established by fact. Reported FY2026 revenue was $215.9 billion, and reported Q1 FY2027 revenue was $81.6 billion, up 85% year over year and 20% sequentially. NVIDIA's stated Q2 outlook is $91 billion, while third-party estimates cited here put Q2 near $91.8–$91.9 billion and Q3 near $103.1 billion. On those figures, the first three quarters would total about $276 billion, leaving roughly $44 billion i
- r5 theme pushes: [{"view_id": "v19", "push": "toward_last"}, {"view_id": "v20", "push": "toward_first"}, {"view_id": "v22", "push": "toward_first"}, {"view_id": "v25", "push": "toward_first"}, {"view_id": "v26", "push": "toward_last"}, {"view_id": "v30", "push": "toward_first"}, {"view_id": "v36", "push": "toward_last"}]

### NVDA: How much Compute & Networking segment revenue will NVIDIA report for FY2027?
- r4 rung 1 (2026-08-15): Rung 1 remains the best judgment, but the FY2027 outcome is not established: the in-force facts report FY2026 Compute & Networking revenue of $193.479 billion (e14) and Q1 FY2027 revenue of $74.550 billion (e26), not the full-year result. Reaching $270 billion would require $195.450 billion over the remaining three quarters, or $65.150 billion per quarter—below Q1's reported revenue. Blackwell and networking growth statements (e15, e28, e21), infrastructure plans and customer activity (e458, e45
- r5 rung 1 (2026-08-15): Rung 1 remains the best-supported forecast, but FY2027 Compute & Networking revenue of at least $250 billion is not established by a reported full-year result. FY2026 revenue was $193.479 billion (e10). In Q1 FY2027, NVIDIA reported $60 billion in data-center computing revenue and $15 billion in data-center networking revenue (e17); those components indicate strong segment momentum, though they are not themselves a reported Q1 Compute & Networking segment total. Reaching $250 billion would requi
- r5 theme pushes: [{"view_id": "v22", "push": "toward_first"}, {"view_id": "v25", "push": "toward_first"}, {"view_id": "v30", "push": "toward_first"}]

### INTC: What gross margin will Intel report for FY2026?
- r4 rung 3 (2026-07-24): The evidence reports Intel's gross profit for the first six months of FY2026, but gives neither revenue nor a gross-margin percentage, and it does not establish the full-year FY2026 margin. It therefore cannot place the outcome in any margin band; the middle rung is retained as the judgement under uncertainty, not as a fact-established result.
- r5 rung 2 (2026-08-13): Rung 2 remains the best judgment, not an established FY2026 outcome. First-half gross margin was about 39.9% ($11.856 billion divided by $29.705 billion), within rung 2 and below rung 1's 41% threshold; the comparable prior-year first-half margin was about 32.2%. This supports a higher-margin direction, but first-half results do not establish the full-year margin or second-half performance. Intel's statement about where most gross profit came from describes its source, not the direction of conso
- r5 theme pushes: [{"view_id": "v22", "push": "toward_first"}, {"view_id": "v25", "push": "toward_first"}]

### AMZN: How much AWS segment revenue will Amazon report for FY2026?
- r4 rung 3 (2026-07-31): Rung 3 remains the best-supported judgement, with a bullish lean. Amazon reported $79.819 billion of AWS sales in the first half of 2026, versus $60.140 billion in the first half of 2025, and Q2 sales were $42.2 billion, up 37% year over year. Amazon's $169 billion annualized run rate is close to, but below, rung 2's $170 billion threshold. Reaching $170 billion for the full year would require $90.181 billion in the second half; the evidence does not establish that result. The reported first-hal
- r5 rung 1 (2026-08-13): Rung 1 remains the best-supported judgment, but FY2026 AWS revenue of at least $160 billion is not established. Amazon reported $79.819 billion in the first half, so AWS needs $80.181 billion in the second half to reach the threshold. Q2 sales of $42.2 billion and Amazon's stated $169 billion annualized run rate support the view that the threshold is achievable; neither establishes the full-year result.
- r5 theme pushes: [{"view_id": "v22", "push": "toward_first"}, {"view_id": "v25", "push": "toward_first"}]

### AMD: How much Data Center segment revenue will AMD report for FY2026?
- r4 rung 2 (2026-08-05): Bullish remains the best-supported estimate, but the FY2026 amount is not established: the available facts cover only the first half. AMD reported $12.5 billion of Data Center revenue for the six months ended June 27, up 81% year over year, including $6.718 billion in Q2, up 107%. The CFO's expectation that Data Center sales would accelerate in the second half supports a result above a simple first-half run rate and makes the $29–$31 billion range plausible. It does not establish that annual rev
- r5 rung 2 (2026-08-13): Rung 2 remains the best-supported judgment, not an established FY2026 outcome. AMD reported $12.493 billion of Data Center revenue in the first half, leaving $16.507 billion for the second half to reach $29 billion—about $8.25 billion per quarter, roughly 23% above Q2's $6.718 billion. Management's expectation that second-half sales will accelerate, together with the stated multi-year customer deployment intentions, supports that path. Rung 1 would require $18.507 billion in the second half, or 
- r5 theme pushes: [{"view_id": "v22", "push": "toward_first"}, {"view_id": "v25", "push": "toward_first"}]


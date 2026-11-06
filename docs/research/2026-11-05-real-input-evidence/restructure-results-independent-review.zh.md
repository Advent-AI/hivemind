# Independent reading (initial report and correction)

**Correction:** the initial claim that 07-candidate e2 was lost was wrong; the correction below supersedes it.

## Correction

My report was wrong about the acquisition: **07-candidate `e2` is present in the handover.** It did not disappear.

- The [07-candidate result](/Users/lchingen/hivemind-no-preseed-evidence-review/poc/data/restructure-prompt-pilot-2026-11-05/07-candidate/result.json) lists handover evidence IDs **`e1`, `e2`, and `e3`**. Acquisition `e2` retains its link to `v64`. The dropped list contains only `e4` and `e5`, both marked `no home`. I retract both statements that `e2` was lost and that its disappearance was unaccounted for. The article’s acquisition claim still has the date limitation described in the report.

- The **09-candidate date finding is supported by the stored article, with a narrower conclusion**. In the [candidate result](/Users/lchingen/hivemind-no-preseed-evidence-review/poc/data/restructure-prompt-pilot-2026-11-05/09-candidate/result.json), `e1–e10` each store `original_day: "2026-08-29"`; `e11` leaves it blank. The article describes the fiscal periods and management’s outlook, but does not give August 29 as the day NVIDIA originally reported those figures or made those statements. The corresponding records in the [control result](/Users/lchingen/hivemind-no-preseed-evidence-review/poc/data/restructure-prompt-pilot-2026-11-05/08-control/result.json) leave the original day blank. This establishes that the date is **unsupported by this article**, not that the actual original date was necessarily different.

- **There is no verified tier regression for the corresponding 09-candidate records.** `e1–e6` are stored as `fact`, matching the control’s reported financial results. `e7–e10` are `party_statement`, matching the control’s management guidance and assumptions; `e11` is also `party_statement`, matching the control’s Kress statement. The report’s omission of separate author interpretations is a difference in content, not evidence that their tier was changed.

No files were edited.

## Initial review

The clearest regression in this one comparison is that the candidate **loses a warning about NVIDIA’s demand being supported by customer financing** before handover. The candidate wrote the warning as `e6`, but joined two separate quotations into one quotation that does not exist in the source. The handover dropped it for that reason. The control’s equivalent `e6` survived.

There are also source-date problems that limit what these answers can establish. In particular, the NVIDIA shareholder article’s stored listing date is August 29, but the complete page body displays **August 30**. Its statements should not be treated as verified information available on August 29.

This is one answer per version for each of five sources. The differences below are observations, not proof that the prompt change caused them, and not an acceptance judgment. I checked the direct handovers; I did not assess later filing or judgment. No files were edited.

The question lists shown to each pair were identical. The Microsoft pair saw 23 questions, including 2026 and 2027 hyperscaler spending, but no Microsoft revenue question. Each of the four NVIDIA pairs saw the same 68 questions. Thus, a missing link to a question that was not shown is **no opportunity**, not evidence that the answer chose the wrong existing question.

## Meaningful regressions and shared risks

- **Financing-risk warning lost — podcast candidate `e6`.** The source quotes Wissner-Gross saying he would not like to discover in two or three years that some or much infrastructure demand had been artificially propped up. Candidate `e6` combines that with a preceding quotation across the intervening words “he said.” The handover records `quote not in item` and drops it. Control `e6` quotes the actual second sentence and survives. Candidate `e4` still carries his separate concern about whether markets priced customer financing, but it does not fully replace the warning about artificially supported demand. Both versions correctly treat this as a concern, not an established fact.

- **A stated acquisition is lost at handover — shareholder article candidate `e2`.** The source says a **$12.9 billion Hugging Face acquisition was announced**. Control `e4` links and hands it over to the existing acquisition question `v64`. Candidate `e2` has the same link in the raw answer but is absent from its handover; the recorded dropped list only names `e4` and `e5`, both as `no home`. The direct handover therefore does not account for the disappearance of `e2` in its dropped list. The source itself does not establish the announcement date, a signed agreement, or completion. Moreover, the page-body date conflicts with the stored day, so this is a source claim with a timing limitation, not proof of a real transaction.

- **The candidate supplies unsupported original dates — earnings/memory article candidate `e1–e10`.** Each assigns August 29 as the original day for NVIDIA’s reported results or management statements. The article supports the fiscal periods but does not establish that NVIDIA originally reported each item on August 29. Control leaves those original dates blank. Candidate `e11`, the CFO’s component-commitment statement, also leaves the original date blank. An article’s date is not automatically the date of the underlying statement.

- **The China assumption is over-linked in the candidate — earnings/memory article `e8`.** Both answers preserve the Q3 revenue guidance’s assumption of no compute sales to China. Control `e9` links it to total revenue `v2`; candidate `e8` adds `v3`, `v11`, and `v14`, which ask whether China permits or authorizes **H200** purchases or imports. The source does not identify H200, a formal Chinese decision, or the named buyers. It is useful context for revenue, but those three additional links risk making a general sales assumption look like evidence of those specific decisions.

- **The candidate loses manufacturing concentration and a qualified product threat — podcast.** Control `e9` preserves the source’s assertion that NVIDIA represents about one-third of TSMC output and lacks real manufacturing diversification. Candidate has no equivalent. Control `e12` preserves the article’s claim of a 90% inference share and that Jalapeno moved from idea to production in months; candidate omits both. The source frames the competing-cloud incentive as conditional on performance claims holding. The 90% share and production claim are the article’s assertions, not independently verified facts.

- **The candidate loses a compatibility expectation — DLSS article.** Control `e3` carries the author’s expectation that “true DLSS 5” will probably be limited to 50-series GPUs, linked to the DLSS launch question `v22`. Candidate has no equivalent. It is an author expectation, not an NVIDIA confirmation; its relevance to whether launch occurs is plausible but less direct than the release timing itself.

## Pair-by-pair audit

### 1. Microsoft cloud and spending

**Source:** `gnews:d144b91986c520ea36e718cf` — [control result](poc/data/restructure-prompt-pilot-2026-11-05/00-control/result.json), [candidate result](poc/data/restructure-prompt-pilot-2026-11-05/01-candidate/result.json).

- Control `e1 → v4` and candidate `e2 → v4, v5` both preserve the article’s claim that Microsoft did not materially raise its annual data-center spending guidance. Neither the spending amount nor the year covered is specified. The `v4` link to 2026 spending is plausible, but not established by the source’s wording; candidate’s additional `v5` link to 2027 is likewise **semantically uncertain**. Control attributes the statement to Microsoft management, although the quoted passage is the article’s account. Candidate attributes it to the article, which is safer; its August 29 original day is the article’s day, not a confirmed day of management guidance.
- Candidate `e1 → v4, v5` adds Azure growth of **43%**, annual Azure revenue above **$100 billion**, and **$678 billion** commercial backlog. The figures are accurately represented as a recent analysis, with Q4 ending June 30, but the passage does not give a data-center spending amount or assign spending to either calendar year. Both spending links are indirect and uncertain.
- Both omit the source’s Microsoft Q4 revenue of **$90.01 billion**, Q1 revenue guidance of **$89.85–90.95 billion**, Azure growth guidance of approximately **45% in constant currency**, and FY2027 analyst revenue estimate of **$391.1 billion**. These would matter to a Microsoft revenue question, but **none was shown to either answer**. The source does not supply a concrete data-center spending amount to substitute for them.
- Neither answer creates a question. The absence of a Microsoft revenue question in the shown list is an opportunity to consider creation, but the article alone and the observed output do not establish whether creation was required under the applicable opening criteria.

### 2. NVIDIA podcast: financing, supply and competition

**Source:** `gnews:8f8a2d115ab834c7026aefd1` — [control result](poc/data/restructure-prompt-pilot-2026-11-05/02-control/result.json), [candidate result](poc/data/restructure-prompt-pilot-2026-11-05/03-candidate/result.json).

- **Results and guidance:** control `e1–e3 → v2` and candidate `e1 → v2`, `e2 → v13`, `e3 → v2` preserve $96.2 billion revenue, $59.7 billion net income and $108 billion forward guidance. The source does not identify the quarter or guidance period. Candidate’s `v13` link is more direct for net income than control’s total-revenue link; both should retain the period limitation.
- **Customer financing:** control `e4–e6 → v2` and candidate `e4–e6 → v2` cover related but distinct points. The article says $5–20 billion checks partly help customers buy NVIDIA products; control `e4` attributes that claim directly to Wissner-Gross, while candidate `e5` attributes it to the article, which better matches the passage. Candidate `e6` is the exact-quote drop described above. Control `e7 → v2`, the conditional “mini winter” view, has no candidate equivalent; it is a broad market outlook, so its direct relevance to FY2027 NVIDIA revenue is uncertain.
- **New FY2028 growth question:** both create `c1`, linked from control `e8` and candidate `e7`, for FY2028 sales growth. Both preserve the source’s roughly **70%** outlook, **44%** consensus and **over 100% only without supply constraints**. The candidate’s bands use 70%, 44% and 100% as boundaries; the control uses different bands. The article supports the three reference figures, but not either set of bands as independently validated market expectations. The source gives no date for the original guidance.
- **Supply and competition:** control `e9 → v2` is the omitted TSMC concentration claim. Control `e10–e11 → v2` and candidate `e8–e9 → v2` preserve the reported Jalapeno comparisons: **1.5–1.9 times work per watt**, up to **3.6 times lower latency**, half the power, and a claimed **54-fold throughput** against less-specified architectures. They are reported claims, not proven comparative results. Control `e12 → v2` carries the production and market-share claims the candidate omits. Total revenue is a broad and indirect home for these competitive risks.
- **Candidate additions:** `e10 → v64` accurately says Salim Ismail speculated that an acquisition of Hugging Face *could* be part of NVIDIA’s strategy; it is not an announcement or agreement. `e11–e13 → v2` capture Blundin’s opposing views about CUDA’s weakening inference advantage, NVIDIA-only cluster scale of **100,000 to several million GPUs**, and its interconnect advantage. These are attributed views. Their total-revenue links are indirect, and `e12–e13` could be read together as one argument rather than independent confirmations.

### 3. DLSS 5

**Source:** `gnews:6dcaad557a1b21d7b867fe34` — [control result](poc/data/restructure-prompt-pilot-2026-11-05/04-control/result.json), [candidate result](poc/data/restructure-prompt-pilot-2026-11-05/05-candidate/result.json).

- Control `e1` and candidate `e1 → v22` preserve the central distinction: an **unfinished version leaked with NBA 2K27**, while the official release was expected later in 2026. Neither turns the leak into an official launch.
- Control `e2` and candidate `e2 → v22` preserve NVIDIA’s reported plans for intensity, color-grading and masking controls. These describe the product, not a confirmed release date.
- Control `e3 → v22`, omitted by candidate, is the author’s probable 50-series restriction, discussed above.
- Both omit the author’s test result: Cyberpunk performance fell from approximately **170 to 115 FPS** with the unfinished version, alongside flickering, shifting faces and art-style limitations. Those are first-hand observations of an unfinished build. They describe readiness and adoption trade-offs, but whether each belongs under the binary launch question is a semantic judgment, not an automatic omission error.
- The page says **August 29 at 2:30 p.m. EDT**, while the stored published timestamp is **07:00 GMT** that day. The timestamp in the listing cannot establish that the page was available at 07:00 GMT.

### 4. NVIDIA shareholder article

**Source:** `gnews:71114e6d410b3ece8ed7f321` — [control result](poc/data/restructure-prompt-pilot-2026-11-05/06-control/result.json), [candidate result](poc/data/restructure-prompt-pilot-2026-11-05/07-candidate/result.json).

- Control `e1 → v2` and `e2 → v10` split total revenue of **$96 billion, up 106%**, from data-center revenue of **$89 billion, up 117%**. Candidate `e1 → v2, v10` combines them into one record. The two numbers remain present, but the combined record sends both quantities to both questions. The article says “second quarter” and does not name the fiscal year.
- Control `e3 → v2` and candidate `e3 → v2` carry Huang’s claim that demand was accelerating. Candidate also retains his description of multiple labs scaling. It remains management’s view, with no original statement date supplied.
- Control `e4 → v64` survives; candidate `e2 → v64` disappears without an entry in the dropped list, as described above. Both reflect the article’s acquisition assertion; neither source text nor these answers proves a binding agreement.
- **Every explicit drop:** control `e5`, the **$26 billion** buyback, and `e6`, the **25-fold** dividend increase, are dropped as `no home`. Candidate `e4`, valuation ratios, and `e5`, dividend increase and **0.49% yield as of August 27**, are dropped as `no home`. None of the shown questions directly asks about buybacks, dividends or valuation, so these are understandable no-home decisions. Candidate omits the buyback altogether rather than recording a drop.
- Both omit the source’s statement that NVIDIA helps smaller companies afford infrastructure through a new financing platform. That is potentially relevant context to the shown AI Compute Partnership question `v1`, but the article supplies no binding guarantee, capacity purchase, counterparty or amount. It is not proof that `v1` is satisfied.
- **Date limitation:** the listing assigns August 29, while the complete page body displays **August 30, 2026**. The input’s cleaned text omits that byline date. The source-date conflict remains unresolved.

### 5. NVIDIA earnings and memory costs

**Source:** `gnews:69d682468e018e0065df5180` — [control result](poc/data/restructure-prompt-pilot-2026-11-05/08-control/result.json), [candidate result](poc/data/restructure-prompt-pilot-2026-11-05/09-candidate/result.json).

- **Results:** control `e1 → v2`, `e2 → v10`, `e4 → v6`, `e5–e6 → v13`, `e7 → v10` correspond to candidate `e1 → v2`, `e2 → v10`, `e3 → v6`, `e4–e5 → v13`, `e6 → v10, v2`. The figures and FY2027 Q2 period agree with the article: $96.2 billion revenue, $89 billion data-center revenue, 75% gross margin, $63.7 billion operating income, $59.7 billion net income and $2.46 EPS, and $48.7 billion hyperscaler revenue up 102%. Candidate’s extra `v2` link on `e6` is broader than its direct data-center `v10` link.
- **Guidance:** control `e8–e11` and candidate `e7–e10` preserve $108 billion ±2% Q3 revenue, the no-China-compute-sales assumption, Q3 gross margin of **74% ±50 basis points**, and a **71–72%** Q4 trough before FY2028 recovery. The extra China-policy links on candidate `e8` are not supported as specific H200 decisions.
- **Memory:** control `e13 → v6` and candidate `e11 → v6` preserve Kress’s **$119 billion to $279 billion** critical-component commitments, primarily related to memory procurement. Neither says the whole increase was memory or identifies SK Hynix, so it does not establish the shown SK Hynix commitment question `v29`.
- Control `e3`, `e12`, and `e14–e16 → v6` carry the article’s explanation and author’s interpretation that memory costs pressure margins and benefit Micron. Candidate omits these separate interpretations but retains the numerical commitments and margin outlook. Control `e15` presents the author’s assertion that higher commitments imply higher realized memory prices as an attributed argument; the source does not prove that implication. The candidate therefore delivers less of the explanation, though it preserves the principal figures.
- Both leave the current-period **operating-margin** question `v25` without a link, despite supplying operating income and total revenue from which a quarterly margin could be calculated. Whether that indirect link should be made is a semantic question; the article does not itself state the FY2027 full-year operating margin.

The five stored inputs and ten answers are a useful set of concrete examples, but the date conflicts, unsupported original dates and exact-quotation rejection must be kept separate from the question of whether the facts matter.

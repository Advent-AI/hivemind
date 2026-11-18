# Production's opening rule holds a price too (D191 point 4, D368 item 1): probe design (choice 3 of D477; council round 27, D439), 2026-11-13

**What it can decide.** Whether production, its role's industry_aggregate sentence widened to "a quantity or price" as Alex decided, opens the
memory-price question it never opens today (0 of 6 production draws: q05, a graded ruler question, "no memory question; memory facts under
total-revenue questions", `clean-arch/e2e-comparison-2026-11-13/opening-review/VERDICTS.md`), without opening price questions an analyst would
not track and without disturbing the aggregates it opens today. A pass leads to a council decision on a production end-to-end measurement with
this one change (a new version, measured against frozen v74i as D368 requires); a failure stops this change on this evidence.

**Mechanism, traced ($0).** Production's role (v74i, frozen by D274) defines the reason as "industry_aggregate: one aggregate quantity for one
calendar year, such as the combined capital spending of named companies." The signed standard (§6 item 2, D191): "任何一家公司之外、好几家都会受它影响的
量或价格（合计支出、合约价、利率）都可以开题", and §3 gives "2027 年 DRAM 合约价相对 2026 年的变化" as its example. Alex: D191 point 4, "a quantity or price outside
any one company that several move on" ("好"); D368 item 1, "这个你记住，我们要做", in the next extraction version. On the rack-memory article (p2 call
136) production proposed no candidate and filed every memory statement under the Rubin shipment question. Production's code accepts a price
candidate: a synthetic DRAM contract-price change for calendar 2027 against 2026, under the semiconductor-cycle theme with its own group, passes
`extraction.sift_with_groups` on that stored answer.

**The change** (arm `price`; `resend_shared.py`): one exact edit of the role, the rest byte for byte: "industry_aggregate: one quantity or price
outside any one company that several companies move on, for one calendar year, such as the combined capital spending of named companies or a
raw material's contract price." The enum keeps its name (the rename touches code and keys, a separate step of the next version). The arm
`stored` sends the stored request unchanged, the same hour.

**Cases** (`selection.json`, 30; three sends an arm; 180 sends; gpt-6-luna at $0.10 / $0.50 per million tokens: about $0.7, a $1.5 reservation
ceiling): the five articles reader B relied on for q05 (memory capacity, the rack's memory cost, memory pricing power, a tight memory market,
memory prices up tenfold), in each of p1–p3 (15); the article where each draw opened its spending aggregate (3); twelve random p1 articles
(seed 20261113) as a noise guard.

**Counting** (frozen; every answer read by Claude; a *kept candidate* is a candidate production's code keeps (`sift_with_groups`); matching and
the writer are not run, so this probe measures candidates, not opened questions or q05's judgement, which only an end-to-end run measures):
- *Valid:* all three sends valid per case and arm; a target case short of that is inconclusive, and more than two inconclusive targets, or
  any guard case short of it, make the probe inconclusive.
- *Target:* a kept candidate on a memory price (DRAM, HBM, NAND or memory contract or spot price) for one calendar year, this or next, or its
  change against the year before. A target article-draw **holds** when it is kept in at least two of three `price` sends and at most one
  `stored` send. **Met:** at least 5 of the 15 article-draws hold, in at least two of the three draws. The 15 are five articles in three
  stored states, not fifteen independent articles.
- *Noise:* on the twelve random articles, every kept candidate `price` adds over `stored` is read: one an analyst would not track (a single
  product's retail price, a supplier's own price, a price no public release settles) is noise. **Regression:** noise candidates kept in at
  least two of three sends on two or more articles.
- *Aggregates:* on each draw's aggregate article, the spending aggregate kept in fewer `price` sends than `stored` sends by two or more fails;
  when `stored` keeps it in fewer than two sends, that draw's guard is not measured (listed).
- *Bytes:* the answers' top-level key order must equal production's stored answers' (`evidence`, `candidates`, `new_groups`), or the run is void
  (AGENTS §5).
- *Reported:* kept evidence and no-home counts per arm; every new price candidate's question, period, rungs and settled_by.

**Before the send:** the rebuild refused nothing (30 of 30 carry the stored archive key); `scripts/preflight.py` on p1's archive and views
(`preflight-p1.output.txt`, exit 0: 243 answers replayed, 742 statements judged, 2% refused as in the stored run; 133 matching records; enum
values all named); a blind audit of the change (`audit-blind.md`: consistent with the standard and D191; reading risks only, each covered by the
noise and aggregate guards); every attempt reserved and settled on its own in the ledger.

**Verdict:** pass = target met, no noise regression, aggregates kept; fail otherwise; inconclusive as above.

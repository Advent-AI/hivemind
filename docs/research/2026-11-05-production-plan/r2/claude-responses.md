# Round 2: Claude's responses to the round-1 findings (each checked against the records before answering)

Sources: `r1/codex-traces-1..3.out`, `r1/codex-attack.out`, `r1/codex-production.out`, `r1/claude-findings.md`. "Verified" means I read the
trace, code or decision cited, not only the finding.

## A. Agreed and verified — to fix (several are defects I introduced)

| # | Finding (who) | Verified evidence | Agreed action |
|---|---|---|---|
| A1 | The same passage is written twice, once by A for its new question and once by B for an existing one (production review, blocker) | Exact duplicate quotes inside one item's handover: 8 groups in the final run, 9 in the confirmation run, plus 8–15 contained-quote pairs (`traces/*/<seq>.json`, `handover.evidence`). Production `extraction.sift` merges identical quotes into one piece with both links (`src/hivemind/extraction.py`, "the same sentence read out twice is one piece with both links") | Merge in the handover exactly as `sift` does (same normalised quote → one piece, union of links, candidate references re-pointed); decide with Codex what happens to a contained quote and to B's link to a broader question when A's candidate is the same period's home (§C3) |
| A2 | The part-period ladder reference makes the frozen judge count growth twice (Claude J1; production review; attack) | v79 TSMC revenue rung 1 from "NT$4.8T × 1.36"; v84 ACIE rung 1 from compounding 25% sequential growth; 7 pace-referenced ladders in the confirmation run, 2 judged at the extreme rung on this reasoning; PRD 06 lists the reference as consensus, guidance, the stated plan or deadline, and its own example compares with the prior year | Withdraw the pace sentence. The reference is guidance, consensus or a stated target when the source gives one, else the prior year's reported figure for the same quantity (growth bands, as PRD 06's example); a part-period figure is evidence, not a reference; none of these → no ladder |
| A3 | Inverted revenue ladders: "Strongly bullish: below $18 billion" (traces-2 1239, traces-3 1273; blocker) | 1273 Broadcom AI revenue and 1239 ON revenue: lowest range labelled Strongly bullish; `check_ladder` checks label order, `check_bounds` the partition, neither the direction | D186 (decided for the next extraction version, D368): each thesis names its favourable end. Record preparation returns `favourable_end` (higher / lower; the model's judgement), code orders the numeric rungs so Strongly bullish holds that end and refuses non-monotonic bounds (code owns the ordering, not the direction) |
| A4 | Condition text and numeric bounds disagree ("at most $215.25 billion" with an exclusive hi of $215.25 billion; a 5% band whose bounds are $100 million off) (traces-1 1227, traces-3 1280) | Read both rungs in the traces | Code renders each numeric rung's interval from its bounds into the stored condition (the bounds are the contract; the model's words stay as description), so the judge reads one boundary |
| A5 | The em dash compared as a space can turn "—$10 million" into "$10 million" (attack) | `compare_form` maps every U+2014 to a space | Compare an em dash as a space only when it is closed up between two word characters ("report—$96.2" after a letter); elsewhere it keeps the production mapping to "-" |
| A6 | A run-on quote keeps the copied sentence but the summary still describes the discarded continuation (attack 1243; traces-1 1210) | 1243 and 1210 summaries name facts not in the kept passage | Refuse a run-on quote in the split (back to the stricter rule): 3 of 1,357 stored quotes. Record that production's D266 run-on rule has the same summary gap (production is frozen; a finding for Alex, not a change) |
| A7 | `question_year` takes the first fiscal year anywhere in the question, even a comparison year (attack) | A question "calendar 2028 … versus FY2025" returns FY2025 | Reinterpret record preparation's bare year as fiscal only when the question names that same year as a fiscal year; otherwise use the prepared year |
| A8 | The year limit is skipped when there is no ladder (attack) | `figure` is true only with numeric rungs | Record preparation returns the admission reason (the standard's five, D184's closed set: main_driver, product_node, binding_obligation, shared_quantity, policy_stage); code applies each reason's limit as production's `check_admission` does (annual quantities this or next year; obligations within 18 months; events by their dates), with or without a ladder |
| A9 | Every written question has an empty due day, so pull mode never closes it (attack; traces-1) | All 22 confirmation-run questions have `due_day` empty; `pull.end_of_day` closes by due day | Proposal for Alex's confirmation: when no exact day is supported, code sets an analyst check date from the settling material's expected period (for a fiscal-year figure, the end of the month the fiscal-year note gives for its annual report; for a pending policy step, the fiscal year-end, as the standard's §3 E already allows), stored with `date_basis = analyst_check` and never presented as a source fact. The unnumbered "incomplete details" record allows a labelled estimate ("A date estimate is not an exact source fact") |
| A10 | Groups: the split writes no new research groups (production review) | Candidates carry `group_refs: []`, no `new_groups`; Jev still proposes membership of visible groups (`jev_group_refs`) | Discuss in round 2 (§C4) |
| A11 | Measurement limits: three tuned runs on the same 100 rows, a model reader, precision-only samples, no recall, no cost and latency at a growing library (attack) | Agreed as stated | Acceptance moves to held-out inputs and the frozen ruler (§B, §D) |
| A12 | Unsupported or unverifiable new questions: a derived share no public material reports (1251, every run); TSMC gross margin from an unconfirmed supplier report (1277); market share without source support (1252) | Read in the traces | The admission reason (A8) carries the settling material; discuss whether the standard's "能核对" test can be checked by preparation (§C5) |
| A13 | Subject and attribution errors in record preparation: Hormuz oil under a new subject; company figures attributed to the article author with the article day (1254) | Read | Fold into the record-preparation prompt audit (AGENTS §6) before the next version |
| A14 | B files specific statements under broad revenue questions (1211 hyperscale revenue → v2; 1246 CPU forecast → v72) and parks weak links (1207 futures, 1240 TSMC → ON revenue, 1263, 1270) | Read | The parking is the fallback sentence (D273, kept by D361); the narrowing step of production (`file_reading` → `narrowest_links`) is not applied in the split (production review): apply it, and put the fallback choice to Alex (§B2) |

## B. Decisions only Alex can take (to put to him with options and a recommendation once the plan is agreed)

1. **Acceptance on the frozen ruler** (production review §6): the judgement scorer requires the 22 frozen seed questions; D370 retired them as
   the starting library. Options: the seeds as a measurement fixture only, labelled; an unseeded production-shaped run with a newly designed,
   reviewed scoring of what can be measured; or both.
2. **The fallback sentence** in the evidence call (D273, kept by D361): every new company-wide revenue question becomes a new place to park
   weak links (confirmation run: existing-question passages helpful 16 of 30).
3. **All-open context at production scale**: measured on the confirmation run's 76 A and B requests, input grows about 150 tokens per open
   question per call (68 shown: about 13,800 tokens; 87 shown: about 16,200; mean 16,450; the 104,272-token maximum is a long filing, not the
   question list). At 500 open questions that is about 75,000 tokens a call; across 15 companies' libraries it exceeds what one request can
   carry. Alex chose all-open for the experiment ("改 work on it"); production with a growing library and 15 companies needs
   the measured curve and a choice (all-open with a budget, or a retrieved shortlist plus subject-tagged questions plus all themes).
4. **The analyst check date** (A9) and the production promotion itself (D359: a new version only Alex opens).

## C. Disagreements and open points for Codex in round 2

- **C1. "Coarse and fine merged" as a blocker (attack).** D248's general rule: "two questions are one when the same outcome settles both; they
  are kept apart only when their answers can move apart and an analyst would bet on each separately"; item 1: "wordings of one plan whose final
  check is the same number are one question". The September decision's range settles "will it raise"; the two answers cannot move apart.
  The risk Codex names (a threshold question losing the full range) is real only when the merged question's ladder cannot carry the finer
  answer; the evidence still reaches it. I propose: keep the rule, limited to one outcome on the same date (the probe's Fed year-end merge was
  fixed that way), and test it on independently labelled threshold-versus-range pairs. Codex: does D248 permit keeping them apart?
- **C2. D197 for five versus four hyperscalers (attack; traces-2 1250).** Standard §3 D: "同一总量的另一种人群、另一种说法是这个量的证据"; D190's
  measured case A17 is "the four-company figure as evidence to the five-company aggregate". Total versus data-center capital spending of the same
  companies is the same aggregate under another wording in the standard's sense. I propose keeping the D197 key and asking: which pair in the
  stored runs would the key merge that the standard keeps apart?
- **C3. A merged passage linked to A's new question and B's broader one** (1207: FY2028 guidance → c1 FY2028 revenue and v2 FY2027 revenue). B
  could not see the candidate. The link rule files "an estimate for another period … under it when no open question covers that period"; once
  A's candidate exists, it covers that period. Code cannot read periods from unkeyed questions. Options: keep both links; or let the record
  preparation type the candidate's period so code drops the other-period link.
- **C4. Groups**: declare new groups in A (the v74i way), or leave group creation to a matching-time step? PRD 05 says extraction determines
  group associations.
- **C5. Settling material**: can the standard's "能核对" test (a public material on a date that puts the answer into a rung) be held by the
  admission reason plus a named settling material, without a list of what companies report?
- **C6. The deal sentence (attack).** Agreed in substance: "One deal or one programme is one question" can swallow D210's exception (a
  not-yet-signed single deal's signing question stays apart from a programme's amount question). Proposed wording: "One deal is one question:
  its agreement, approval and closing are steps of it; a deal not yet signed under a programme already asked by amount keeps its own signing
  question." Same exception in collision-v4's instance clause.

## D. Probe after the census: A's singular opening is not the cause of the misses (hypothesis refuted)

`probe_a_plural.py`, results in `poc/data/a-plural-probe-2026-11-05/results.json`: the confirmation run's stored A requests on the five items
where the census found a missed question (1209, 1210, 1228, 1234, 1266), sent twice as stored and twice with the opening "find the important new
questions this item raises" (v74i's wording). Stored: 1209 opened the FY2028 revenue question in both sends (the census "miss" was one draw);
1228 opened Azure revenue both times. Plural: one send of 1234 opened two questions, the other none; 1228 opened total revenue once and capital
spending once; 1266 opened nothing in any arm. Whether A opens a question on a given item is a sampler draw in both arms; the wording does not
move it. Not changed.

Consequence for the measurement: a matter that several articles carry (FY2028 revenue appears at 1207, 1209, 1210, 1213) reaches the library at
some item even when one item's draw misses it. What the product needs is the question in the library before its evidence arrives, so A's recall
is measured at the library level by day (which important questions exist by the end of each day, and which evidence arrived while none did), not
item by item.

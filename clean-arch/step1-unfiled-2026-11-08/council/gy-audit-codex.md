**The request has three material gaps:** it does not carry the rule against disguising a distant annual forecast as an event; it allows some answers that the planned checks will reject; and it gives no worked event ladder to teach or test complete, non-overlapping outcomes.

For example, a question with three possible outcomes—approved, rejected, or still pending—must be given five distinct states by the request, but no example shows how to do that without overlap or artificial splits. The request and checks are drafts; I did not edit files or run calls.

### 1. Request to standard

In the tables, **S** means [system text](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt), **J** means [schema](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json), **P** means [production prompt](/Users/lchingen/hivemind/src/hivemind/prompts/role-v74i.txt:13), and **D** means a decision in the [decision log](/Users/lchingen/hivemind/docs/DECISIONS-log.md:753). Sentence numbers below follow their order within each system-text line. “Consistent” includes format instructions that implement the sourced rule.

| Sentence | Clause | Source | Verdict |
|---|---|---|---|
| S1.1 | Analyst role | P1 | Consistent |
| S1.2 | Opening context | D398 | Consistent |
| S1.3 | One question, ladder, due day | D38, D397 | Consistent |
| S1.4 | Written once, opening item only | D38, D398 | Consistent |
| S4.1 | One figure or event | P20 | Consistent |
| S4.2 | Question, not assertion | P21 | Consistent |
| S4.3 | Resolvable outcome | P21 | Consistent |
| S4.4 | Period and settling material | D38 | Consistent |
| S5.1 | Topic may contain several things | D397 | Consistent |
| S5.2 | Judge `outcome` | D397 | Consistent |
| S5.3 | List all omitted wording and why | D397 | Consistent |
| S5.4 | Do not combine; two examples | D397, P20 | Consistent |
| S6.1 | Five refusal cases | D38, D185, D397; P16–17 | Consistent |
| S9.1 | Company and obligations use ticker | P13, P22 | Consistent |
| S9.2 | Other company’s figure uses its ticker | D38; [production request](/Users/lchingen/hivemind/src/hivemind/extraction.py:390) | Consistent |
| S9.3 | Theme ID or matter name | P22; production request | Consistent |
| S12.1 | Concrete conditions | P24 | Consistent |
| S12.2 | No unspecified future target | P24 | Consistent |
| S12.3 | No gaps or overlap | P25 | Consistent |
| S13.1 | Yes/no event | P25 | Consistent |
| S13.2 | Other event: five distinct states | P25 | **Narrower:** three or four natural outcomes are not addressed; five distinct states can require arbitrary splits. |
| S13.3 | Company labels; theme names | P25, D38 | Consistent |
| S14.1 | Unit, year, five ranges | P25–26, P34–35; production closing | Consistent |
| S14.2 | Inclusive lower, exclusive upper | P35 | Consistent |
| S14.3 | Full money amounts; percent scale | P35 | Consistent |
| S14.4 | Open endpoints | P35 | Consistent |
| S15.1 | Exactly one answer shape | P25 | Consistent |
| S16.1 | Opening reference and value | D260, D398 | Consistent |
| S16.2 | Middle range holds reference | D186, D398 | Consistent |
| S16.3 | No reference: estimated ranges | D398 | Consistent |
| S17.1 | Favourable end and reason | D186, D398 | Consistent |
| S17.2 | Result and direction differ | D186 | Consistent |
| S17.3 | Theme direction n/a | D38, D398 | Consistent |
| S20.1 | Due when resolvable | P26 | Consistent |
| S20.2 | After item, on/after publication | D356; P13 | Consistent |
| S21.1 | Figure publication date and basis | P26 | Consistent |
| S21.2 | Fiscal/calendar conversion | P26, P33 | Consistent |
| S21.3 | Other figures: calendar | P26 | Consistent |
| S22.1 | Event date and basis | P16, P26 | **Narrower:** permits only the stated date or named period end, apart from the regulatory exception; P26 does not impose that closed set. |
| S23.1 | Obligation and 18 months | D185; P13 | Consistent |
| S25.1–2 | Check one thing and omissions | D397 | Consistent |
| S25.3 | Sample outcomes or event states | P25; AGENTS §6 | **Narrower:** three sampled numbers do not establish coverage at every boundary. |
| S25.4 | Check reference, bounds, date | D186, D356, D398; P24 | Consistent |
| S25.5 | Correct failures | AGENTS §6 | Consistent |

| Schema description | Clause | Source | Verdict |
|---|---|---|---|
| J19 | Refusal and null shape | D38, D185, D397; P16–17 | Consistent |
| J44 | Question, period, source | D38; P20 | Consistent |
| J49 | Object choices | P22; production request | Consistent |
| J53 | Omitted wording | D397 | Consistent |
| J74 | Yes/no shape | P25 | Consistent |
| J90 | Yes condition | P25 | Consistent |
| J95 | No condition | P25 | Consistent |
| J102 | Five event states | P25 | **Narrower:** same three/four-outcome issue as S13.2. |
| J122 | State labels | D38; P25 | Consistent |
| J134 | Figure shape | P25, D398 | Consistent |
| J162 | Other unit named in question | P34 | Consistent |
| J167 | Fiscal/calendar year form | P26; production closing | Consistent |
| J190 | Inclusive lower bound | P35 | Consistent |
| J201 | Exclusive upper bound | P35 | Consistent |
| J213 | Favourable end | D186, D398 | Consistent |
| J217 | Reason; empty for theme | D398, D38 | Consistent |
| J239 | Reference words | D260, D398 | Consistent |
| J250 | Reference value | D398 | Consistent |
| J267 | Date basis | P16, P26 | **Narrower:** same restriction as S22.1. |

| In-text example | Source | Verdict |
|---|---|---|
| Drug approval versus patient count, S5 | D397 | Consistent |
| Carrier fuel bill versus strike, S5 | D397 | Consistent |
| Capital spending and direction, S17 | D186 | Consistent |

### 2. Standard to request

- **Carried:** one fixed question and due date; one tracked outcome and disclosure of omitted parts; binding-obligation horizon and filing/signing distinction; reference and favourable end; due day on or after publication; fiscal versus calendar years; numeric bounds and open ends. See S4–6, S14–17 and S20–23.
- **Missing:** a numeric completion target may define an event without becoming an annual metric, but a beyond-horizon annual forecast must not be repackaged as an event ([P16](/Users/lchingen/hivemind/src/hivemind/prompts/role-v74i.txt:16)).
- **Missing:** the neutral comparison must be stated in its condition for five-rung ladders ([P25](/Users/lchingen/hivemind/src/hivemind/prompts/role-v74i.txt:25)). Figure rendering adds the reference in code, but the request does not instruct this for event states.
- **Carried narrower:** event due-day choices and the treatment of events with three or four natural states, as above. The opening rules for matters such as appointments and routine litigation are upstream opening decisions, rather than independent ladder-writing instructions here.

### 3. Principles and checks

- **Fitting:** none of the three examples names NVIDIA, its products, or an identifiable test article. They span drugs, airlines and capital spending.
- **Examples and boundaries:** none is a completed event ladder. The two event-containing examples choose which question to judge; the spending example explains direction. Therefore there are **no example event-rung outcomes or boundaries to walk**, and none can demonstrate the no-gap rule. S13.2’s classification needs worked, exhaustive examples.
- **Closing check:** its checks are stated above, but sampling three numeric outcomes cannot prove the full partition ([S25](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:25)). The planned bounds check is stronger ([check 4](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:266)).
- **Allowed but refused or dropped:** S9/J49 allow another company’s ticker or an unlisted matter; [check 2](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:250) ends those without a view. S14 allows numeric bounds without a size limit; [check 7](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:294) refuses non-finite bounds and whole-number bounds of at least 2^53 in magnitude. The former is an intentional downstream outcome in the design, but remains a mismatch with the request/check principle.
- **Reader mark:** [mark D](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:585) requires a figure’s due day after its period ends; S20–21 require publication and resolution but do not explicitly state that boundary.

### 4. Differences from the author’s table

I opened [§5.2](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:197) after forming the verdicts above.

- **“Yes/no event … anything else five,” line 209:** the author records the missing three/four-state shape but treats it as sourced; I judge the request narrower and inadequately illustrated.
- **“Event’s due day,” line 216:** I judge the closed choices narrower than P26.
- **“The closing check,” line 218:** I agree its clauses repeat earlier rules, but three numeric samples do not establish the earlier requirement for every outcome.
- **Omissions from the table:** P16’s warning against repackaging a distant annual forecast, P25’s neutral comparison for event states, the check-2 and numeric-limit mismatches, and the reader’s period-end boundary are not mapped as request gaps.
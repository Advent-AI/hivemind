## Converged design

- **Use one judging call and one checked calculation for related number questions.** Each question keeps its own answer, and each answer reads from the same calculation.
- Show the judge the combined evidence already in view. Keep each source passage once, with its original attribution.
- Let the judge identify and label the figures it actually uses, including their scope and period. Distinguish source figures, calculations, and assumptions.
- Give each shared quantity one value or range per scenario. Show a forecast as unresolved when the figures cannot be reconciled.
- Keep extraction v74i as it is. Use declared relationships for the first test, then put automatic selection in matching if the design earns a production version.
- For a first release, show number questions and their sources with **“Forecast unavailable”**. Keep forecasts out of the published results until they pass the checks.

## 1. The unit of the shared calculation

**I’d take Claude’s joint call over my original proposal for separate judges.** Sharing the evidence gives both judges the $108B Q3 guide. It still lets one forecast from that midpoint while the other forecasts from a beat-adjusted $113.5B. A check at publication can catch the difference, but it cannot choose which assumption the analyst should use. A joint call can choose once and use that choice throughout. It can also show both scenarios, provided each card uses the same figures within each scenario.

I joined the stored total-revenue and Data Center answers by draw and day and read their chosen bases and outcomes. Under a strict rule that withholds a pair if it disagrees on a shared base or has a segment above the total, **17 of 18** pairs on September 15–20 would have been held for the Q3 base alone. Across the post-earnings window, **at least 50 of 77** would have been held for one of those reasons: **18/26** in old-1, **26/26** in old-2, and **6/25** in old-3. Those are lower bounds on the saved answers under that rule, not predictions for a new version. Old-2 calls **8729/8737** are the positive control. Old-1 calls **5652/5660** use the same $108B guide and have Q4 Data Center below the company total. Under the separate-judge proposal, a held pair would show **“Forecast unresolved”** for that update rather than publish two current answers. [Stored runs](/Users/lchingen/hivemind/poc/data/comparison-2026-11-17/run)

The September 20 requests were **71,653 characters and 18,361 input tokens** for v9, and **68,978 characters and 17,790 input tokens** for v14. An in-memory merge that kept both question descriptions and previous answers, used the common instructions and theme block once, and deduplicated **five identical evidence entries** came to **127,740 message characters** and **237 evidence entries**. That is **9% less** than the two messages combined and **78% more** than the larger single request. The two original calls used **36,151 input tokens** in total. The joint character count is measured; the joint token count and new answer format remain unmeasured. [Old-2 request archive](/Users/lchingen/hivemind/poc/data/comparison-2026-11-17/run/old-2/prod/archive.sqlite)

## 2. Where to label a figure’s identity

**Start at judging.** The calculation needs to record what each source figure measures. Labelling it at extraction is unnecessary for the first fix and would still leave overlap, assumptions, and publication unchecked. Judge-side labelling is cheaper to try because it touches only the figures a forecast uses and works with the saved v74i requests. There is no measured running-cost advantage yet. [Extraction freeze, D274](/Users/lchingen/hivemind/docs/DECISIONS-log.md:3151)

Checking that a figure appears in the quote is necessary for a direct source claim. It is insufficient for class S. In call **8595**, all three amounts appear in the evidence. The defect becomes checkable when the calculation identifies **four companies’ 2026 AI infrastructure spending**, **five companies’ 2026 capex**, and **five companies’ 2027 capex** as different inputs. Code can see that the calculation needs a bridge between spending definitions, populations, and years. The judge can still mislabel a quote, so a blind reader must check whether the labels actually match the passages in the first test. Typing the figures earlier would move that interpretation upstream. It would not make it independently true. [Old-2 request archive](/Users/lchingen/hivemind/poc/data/comparison-2026-11-17/run/old-2/prod/archive.sqlite)

## 3. What code checks and what the model decides

Code would check these five things:

1. A direct figure points to a shown source passage containing that value or range and unit. A derived figure points to its inputs and operation.
2. The arithmetic recomputes, with explicit unit conversion and rounding. An addition declared to represent disjoint amounts requires a declared accounting relationship. Unknown overlap stays an assumption.
3. A declared part fits within its whole for the same period, basis, and scenario where the accounting relationship requires a nonnegative remainder.
4. Each use of the same shared quantity **in the same role and scenario** resolves to one value or range. The $108B company guide and a $113.5B analyst forecast can both exist. Two cards cannot silently choose different values for the same Q3 forecast in the same scenario.
5. A market comparison points to shown external source material, directly or through a disclosed calculation. The answer can say there is no external comparison. A prior system forecast cannot fill that role.

The model decides which drivers matter, how much weight to give them, what discount is defensible, and whether an overlap assumption supports a conditional forecast. Code would be making an importance judgement if it prescribed a haircut, always preferred guidance, or rejected a forecast simply because it used an assumption. A blind reader decides whether the evidence supports an assumption that carries the forecast across a boundary. [Current judgement checks](/Users/lchingen/hivemind/src/hivemind/views/judging.py:259), [D721 on the CPU increment](/Users/lchingen/hivemind/docs/DECISIONS-log.md:10859)

## 4. D24 and D28

The warehouse risk comes from collecting figures before a question needs them. Bound this design to the figures consumed by open questions and the few intermediate values needed to explain their forecasts. A quarterly path is appropriate when it supports the annual answer. It should be possible to leave a quarter unsized when the evidence only supports a half-year or annual range. Store the calculation with the dated judgement and refer back to its existing evidence. That follows D28’s rule that filings enter as research material and D24’s rule that the question determines which numbers matter. [D24](/Users/lchingen/hivemind/docs/DECISIONS-log.md:433), [D28](/Users/lchingen/hivemind/docs/DECISIONS-log.md:567)

## 5. Who declares related questions

**Matching should propose the relationship. Typed keys should find candidates and confirm identities they can establish.** Use a narrower question than the pilot’s “would this conclusion inform the other?” Ask whether the questions share a specific quantity or a defined accounting relationship, and have the decision name that relationship. Grouping is undirected. The arithmetic still needs to know which quantity is the part or which year is the growth base.

The judge decides how to use the relationship inside the calculation. Stand-alone CPU’s `other` key illustrates why keys alone cannot find all the right pairs. A shared company or a useful driver also does not make two questions share a calculation. For the first test, declare the relationships from the stored cases so a matching error cannot decide the result. [Question identity code](/Users/lchingen/hivemind/src/hivemind/views/identity.py:13), [Pilot link wording](/Users/lchingen/hivemind/docs/research/2026-11-21-whole-window/WORDING-V2.md), [D368](/Users/lchingen/hivemind/docs/DECISIONS-log.md:3960)

## 6. Which frozen pieces need a new version

**Alex would open a new judge version for the test.** It changes the judging unit, request, answer format, and publication check. The test can use declared families and existing filings. The production design above would also need a new **matching** version for automatic family selection. Extraction stays on v74i.

The frozen gold gives four controls. **q01** builds a total-revenue range and considers Vera upside without declaring a fixed increment. **q02** derives a segment range from q01’s shared total and a sourced mix. **q19** makes a reasoned execution discount using selling time and implied unit volume. **q22** reuses q01’s FY2027 base, then widens the calculated FY2028 range using analyst judgement. The calculation must be able to show both a recomputable intermediate and a reasoned forecast range. Requiring the final range to equal the raw multiplication would reject q02 and q22’s reasoning. [Frozen judgement gold](/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json)

## 7. Minimum safe first release

Claude’s **evidence and events, with numeric forecasts withheld** is the honest interim. The cheapest implementation would be at the published bundle, where the product already exposes answer shape, judgement history, and reasons. Show the question, sources, and **“Forecast unavailable.”** Withhold the forecast band and forecast text together, including history and other views that reuse the bundle. A warning beside an otherwise normal-looking forecast would still invite readers to act on it. [Published view bundle](/Users/lchingen/hivemind/src/hivemind/bundle.py:100)

## 8. The one test

**Use one registered test with a $0 gate and a paid gate.**

- **$0 gate.** Hand-reconstruct old-2 **8729/8737**, **8734** and **8595**, and old-3 **9166**, using the proposed answer format. The format must expose the conflicting pair, the unresolved overlap, the incompatible scope, and the unsized discount. It must also represent **all four** frozen-gold controls. Add three deliberate errors to those same reconstructions: a source amount absent from the quote, a wrong sum, and an internal forecast labelled as market consensus. All three must fail. Stop on any miss or any valid control the format cannot express.
- **First paid comparison, if Alex opens it.** Freeze the September 20 total/Data Center pair in each of the three old draws. Use identical dated evidence and the same structured answer rules in both arms. One arm judges the pair together. The other judges each card separately and then runs the same reconciliation check. Take **three fresh samples** per snapshot, for **9 joint calls and 18 separate calls**. Add **9 singleton calls**, three each on the stored O, S, and E requests above, to check that the new answer format helps where grouping alone cannot. That is **36 planned calls**. Read every output against its source with the arm hidden.
- **Pass.** The joint arm publishes **both usable, source-supported answers in at least 8/9 pairs**, including **at least 2/3 on each snapshot**, and produces **at least 3 more usable pairs** than the separate arm. Across the joint and singleton answers, **zero** published answers may contain a hard numerical contradiction, an internal forecast presented as a market reference, or an unresolved scope change, overlap, or unsized adjustment that determines the answer band. A singleton may state that the evidence is insufficient and show why.
- **Stop.** One such published defect stops the line. Missing either coverage threshold stops it. A gain of fewer than three usable pairs means this test has not shown that the joint call earns its complexity. An incomplete comparison earns no pass. This is a small design test, not release acceptance.

**For Alex:** Open one judge version for this bounded test. The decisive question is whether sharing the calculation gives readers more usable answers than giving two separate judges the same evidence.

**Remaining disagreement with Claude:** The September 20 numbers show that $146B is the residual of $410B minus $164B minus $100B. The saved answer does not establish which number the judge chose first. Likewise, a source citation can establish that an amount was stated without establishing that it fits the question. Those distinctions are why the first test must read the calculations and their sources, as well as check the arithmetic. This round was read-only and made no model calls.
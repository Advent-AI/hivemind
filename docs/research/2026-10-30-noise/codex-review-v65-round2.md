**Nothing serious remains in the revised review prompt within this audit’s scope.** For example, a customer’s adoption mentioned alongside a product comparison now goes through the analyst’s judgment; it is neither automatically kept nor discarded just because the sentence contains a comparison.

The corrections match the standard:

1. **Required keeps and row boundaries.** The [prompt](src/hivemind/prompts/review-v65.txt) says, “What a line says it does not cover goes to the check, unless the line says it is kept.” It separately says retold guidance and forecasts or plans still in force “keep their place,” and a qualifying conditional valuation “is kept.” The [standard](docs/prd/05-extraction-standard.html:400) says “重提的季度指引和仍然有效的预测、计划按本来分量” and “有假设、有推导、有时点的条件估值要留.” The prompt preserves those outcomes while sending other row-specific exceptions to the check.

2. **Adoption correction.** [D250](docs/DECISIONS.md:2981) records the accepted lean as “其余的都算产品细节，不收.” It did not say that adoption in the same sentence must always be kept. The [page](docs/prd/05-extraction-standard.html:394) now says “同一句里伙伴、客户采用或集成的动作不因这一条删，照旧按 5.1 判”; D250 says it “is not dropped by this rule and is judged by 5.1 as before.” Both match the recorded lean without adding an unconditional keep. The prompt likewise says the product-detail row “does not cover” adoption or integration, “also when a comparison shares its sentence,” which sends it to the check.

3. **Analyst interpretation.** The prompt now rejects “a **named analyst’s** reading of an event already recorded that adds no new fact or calculation,” and says the row “does not cover a reading that adds a new fact or calculation.” The [standard](docs/prd/05-extraction-standard.html:396) says “具名分析师对一件已记下的事的解读……没有新事实或推算的，不收，有新事实或推算的按 5.1 判.” These match.

4. **Existing arrangements.** The prompt separately rejects “an arrangement the item only describes as in place, with no new step, even when no date is given.” The [standard](docs/prd/05-extraction-standard.html:397) says “只描述一个现成安排……没有新动作的，是背景，不收，文中没写日期也一样.” The arrangement no longer depends on proving the analyst already knew it.

5. **Competitor comparison.** The prompt says the product-detail row “does not cover a competitor’s comparison against the company’s product.” The [standard](docs/prd/05-extraction-standard.html:394) says “对手拿它和本公司产品比的说法不能用这一行删掉，按 5.1 判.” The row-specific exception supplies the needed precedence over the general rejection of published comparisons.

6. **Example.** The prompt now uses “the vacuum runs 60 minutes on a charge” for a product detail without business scale. The [standard](docs/prd/05-extraction-standard.html:394) rejects “没有业务规模的产品、游戏、驱动、跑分细节.” The replacement fits that rule and is general across companies.

The round-one concern about the **earlier role’s kind-and-list procedure remains open**. As requested, I treated the role as context only; this conclusion does not claim that the final check fixes that earlier conflict. This was a read-only wording audit, not a measurement of model behavior.
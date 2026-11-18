**Version 2 resolves the first audit’s main wording problems, but it still risks narrowing some valid event questions.** The phrase “whether it has happened by then” can turn a question about several meaningful outcomes into a yes/no question. For example, a regulatory process may be approved, rejected, or still pending at the check date; those are not necessarily the same as simply “happened” or “did not happen.”

The requested diffs confirm that c19’s system text and closing check are identical to c8’s. The schema adds the two required fields and their definitions; the only other difference is the final newline.

### Sentence-by-sentence review

| New description | Verdict | Signed standard and assessment |
|---|---|---|
| **`settles_on`, sentence 1:** “one quantity for one period, which may be its change against a stated earlier period … or one event checked by a date (whether it has happened by then).” | **Keeps narrower**, for events | §3 says “一个问题只问一个量的一个期间，或一件事” and gives “2027 年 DRAM 合约价相对 2026 年的变化” as an example. The new text now preserves that comparison. But the same table allows an event “五档，或是非两档”; “whether it has happened” suggests a yes/no test even where the analyst tracks several states. |
| **`settles_on`, sentence 2:** “If no date and public material can place the answer in fixed outcomes, rewrite the thesis; if it cannot be rewritten, do not propose it (whether its statements are kept is judged as evidence, section 4).” | **Consistent**, with a scope caution | §4 asks “有一个日期和一份公开材料能把答案放进事先固定的档吗？没有就重写问题” and says “重写不了就不开，材料作证据.” The new parenthesis correctly makes keeping a statement a separate evidence judgment; §4 says “它的陈述留不留照第 5 节判.” The rewrite must still preserve what the source supports, rather than invent a date or change the matter being tracked. |
| **`outcomes`, sentence 1:** “five ranges of that quantity or of its change, or the event’s states, five or two … checkable, not overlapping and leaving no gap …” | **Consistent** | §3 specifies quantities as “量，五档,” unsigned obligations as “还没签：是非两档,” and events as five or two. It also says “结果档可核对、不重叠、不留缝，到期恰好一档成立；中间一档写明和什么比.” The unsigned-deal example correctly asks whether signing occurred **by** the check date. |
| **`outcomes`, sentence 2:** “A company thesis’s outcomes describe the business result, even when a policy drives it; a theme’s … describe only the result, not whether it is good.” | **Consistent** | §3 says “标的问题的档描述业务结果；主题问题的档只写结局，不写好坏.” Its policy row says a question about “一家公司的收入、利润、份额或产品进度，算标的，即使由政策驱动.” The revised sentence preserves that distinction. |

One schema detail remains: the array permits **2, 3, 4, or 5** items, while the description and standard specify **five or two**. The description tells the model the right rule, but the schema alone would also accept three or four outcomes.

### First audit: what changed

The year-on-year issue is resolved in the wording: both fields explicitly allow ranges of the **change** against an earlier period. The prior “one figure” language no longer directs the model to replace the comparison with a raw annual value.

The evidence issue is resolved: rejected questions’ statements are judged as evidence, rather than automatically kept. The unsupported “several figures none of which leads” rejection is gone. The policy classification issue is resolved: a policy-driven company outcome is no longer automatically treated as a theme.

The earlier date concern is substantially improved: the unsigned-deal example says **“by the check date,”** and the event wording says **“by then,”** rather than implying the event must occur on the exact day. The remaining event-state concern above is new to this wording.

### Conflicts with the rest of the request

I found **no direct contradiction** with the system or closing check on the four named points:

- **Opening:** the new fields add the standard’s checkability requirement; they do not say a checkable question opens without also being important and a separate bet.
- **Dates:** they do not override the system’s different date rules for obligations, regulatory decisions, shared quantities and products. They also do not repeat those rules, so the model must still apply the system text.
- **Evidence without a thesis:** the new wording sends statements to the evidence judgment. The system and closing check then link passing evidence to relevant existing questions or leave it unlinked.
- **Separate bets:** neither description explicitly removes that requirement. There is still a risk that “rewrite the thesis” leads to a smaller question that no longer represents the original separate bet; the descriptions do not explicitly tell the model to preserve the tracked matter when rewriting.

[D417](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4606) declines a non-annual rolling-period figure when neither the topic nor the item gives a publication day. Its recorded scope is the clean path’s ladder step. It does **not** support a general refusal of annual comparisons, undated unsigned obligations, or product events with a supported check date.

### Industry neutrality and concrete risks

The new descriptions are industry-neutral and name no covered company, product, or specific business number. “Unsigned deal” and the calendar-year comparison are general examples.

- **Next year versus this year:** explicitly supported by “its change against a stated earlier period” and “ranges … of its change.” I do not see the former raw-number narrowing in version 2.
- **Unsigned deal:** explicitly supported as a yes/no question by the check date. The system still supplies the separate rule that the check date is within 18 months.
- **Shipment by a date:** “whether it has happened by then” fits a shipment yes/no question and does not require shipment on the exact date. The system still requires a supported date.
- **A multi-state event:** “whether it has happened by then” can pull a broader question toward yes/no despite the next field allowing five event states. That can lose the difference between outcomes an analyst tracks.
- **Any rewritten question:** “rewrite the thesis” could produce a narrower, easier-to-check question that drops the original subject, scope, or economically meaningful comparison. This is a risk in interpretation, not proof that the model will do so.

These are wording findings from a read-only comparison; they do not establish how often the model would make these mistakes. Sources: [candidate schema](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c19-schema.json:51), [signed standard §§3–4](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:272), and [first blind audit](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/outcomes-at-opening/audit-c19-blind.md).
- **Verdict: useful, but the wow is deferred—and the proposal overstates both its uniqueness and what it can prove.**
- Picture the first difficult moment: the stock has already fallen, the agent shows a filing, and asks permission to sell. The user’s question is “Did you help me make a better decision?” A citation alone does not answer that.
- This review covers the proposal, including its added self-critique. The background documents inform the review; the frozen design is not being reviewed or redesigned. No files were changed.

- **1. Is this a wow? Three separate reactions.**

- **Product leader — first touch:** “That understood my situation” could land. “Here are four standard questions about NVDA” could feel generic. The difference is whether the mapped question preserves what I actually meant. Your example quietly changes “demand through year-end” into “next quarter’s revenue meets guidance.” That is a different promise. [Proposal](./docs/agentic-experience.md:13)
- **Product leader — after one month:** I see a retention problem, not an established wow. The proposal assumes users interpret silence as successful work before the product has earned that interpretation.
- **Product leader — after the first action:** This is the decisive product moment. Did it catch something I missed, connect it to my earlier rule, and save me work? Or did it send an elaborate earnings alert?
- **Product leader — after settlement:** A receipt can establish accountability. One correct result cannot establish a dependable service. “Seven actions accepted” also does not justify moving from $200 to $5,000; acceptance measures agreement, not judgment quality. **Where it falls flat:** the story treats agreement, trust, autonomy and larger allocations as one inevitable progression.

- **Five-stock retail investor — first touch:** “Someone remembers why I own this” is appealing. But I may own NVDA because I broadly expect AI growth, not because I hold a precise revenue forecast. I will probably accept your polished plan without understanding how much you narrowed my belief.
- **Retail investor — after one month:** If prices are calm, I forget the product. If prices are falling, I keep checking prices and wonder whether the agent missed something. “No change” does not resolve that anxiety automatically.
- **Retail investor — after the first action:** If it catches a buried development, I feel looked after. If it asks me to sell after a conspicuous earnings disappointment, I feel late. If I disagree, “ask me” leaves the hardest decision with me.
- **Retail investor — after settlement:** “My stated test passed, but I lost money” might teach me something. It might also feel like the app is congratulating itself while I am poorer. **Where it falls flat:** the receipt must answer my experience, not merely announce its own scoring result.

- **Hedge-fund PM — first touch:** I inspect the question, horizon and evidence. I am not impressed by converting prose into a plan. I am interested in whether the maintained record contains something my existing process missed.
- **PM — after one month:** Silence is acceptable if I can inspect coverage and freshness. Silence without that evidence is indistinguishable from neglect.
- **PM — after the first action:** I ask why this development invalidates the position at the current price. A broken assumption can justify reassessment; it does not mechanically establish that selling everything now is the best trade.
- **PM — after settlement:** Separating the business outcome from investment returns is useful. Calling the difference “luck” is unjustified: one tracked question does not explain the entire return. **Where it falls flat:** this is potentially an analyst’s monitoring aid, not yet a substitute for portfolio judgment.

- **2. “Exit on a fact”: differentiator or liability?**

- **Strongest case for it:** It makes the investor’s commitment specific before emotions intervene. Price falls; the agent checks the agreed reason. Evidence undermines that reason; the agent brings back the original commitment. The benefit is consistency and saved attention. It need not beat the market’s reaction time to provide those.
- **Strongest case against it:** Suppose a filing breaks the thesis and the stock immediately falls 15%. Selling afterward cannot recover that loss. Nor does the old thesis breaking establish that the newly discounted stock is unattractive. A separate price stop addresses a different risk; it does not repair this decision problem.
- **There is also a meaning problem.** The frozen design explicitly makes the current state a model judgment. Management statements, third-party opinions and rumors can move it; confirmed events can establish an outcome. Therefore, **“the state crossed my line” and “a fact invalidated my belief” are not interchangeable.** This is a problem with the proposal’s promise, not a criticism of the state layer. [State and evidence rules](./docs/prd/06-views.md:80)
- **The source sentence helps, but does not finish the argument.** A supplier’s reported growth may be factual. What it implies for NVDA’s future revenue remains an inference. The user must see that distinction.
- **Verdict:** A credible differentiator in decision discipline; an unproven differentiator in investment results. I would promise **“review my position when evidence crosses my agreed threshold.”** I would not sell “fact-based exit” as inherently superior execution.

- **3. Could existing products reproduce 80%?**

- **For a motivated five-stock investor: plausibly yes. That is an estimate, not a measured result.** The proposal’s statement that competitors’ conditions can only involve price and time is unsupported.

- **Robinhood already supplies much of the machinery.** Its official documentation lists portfolio access, financial statements, news, SEC filings, structured filing facts, order proposals and trading tools. Built-in agents have trade approval enabled by default. Those are not merely price-and-time inputs. [Robinhood tool documentation](https://robinhood.com/us/en/support/articles/trading-with-your-agent/)
- **Important availability distinction:** Robinhood’s public page still labels Loops “coming soon.” Its announced purpose is continuous or scheduled research and trading. I would treat that as a credible competing direction, not claim that every user can run it today. [Robinhood Agents](https://robinhood.com/us/en/agents/)
- **Memory and scheduled work are also real capabilities.** Official OpenAI documentation describes persistent notes and memory, plus scheduled work that can return to an existing conversation. That does not establish an automatic shared memory connection with Robinhood, but it defeats the proposal’s picture of GPT necessarily starting from zero every time. [Memory](https://learn.chatgpt.com/docs/dots/tasks-and-memory), [scheduled tasks](https://learn.chatgpt.com/docs/automations)

- **Concrete competing workflow:** Save a dated instruction: “I own NVDA because of X. Recheck X against new filings and relevant supplier reports. Keep my original condition unchanged. Ask me before selling. Show the source and what changed. At the deadline compare the reported result with my original condition.” A configured agent with research access, scheduling and durable storage could approximate this. Its reliability would need testing, just as yours does.
- **What memory alone cannot supply:** A trustworthy historical ledger, a consistently maintained shared question, evidence replacement rules, or verified outcome grading. Those require deliberate storage and processing. A competitor can build them; they do not emerge merely from remembering the user’s preferences.
- **Existing thesis tools already overlap substantially.** Investi advertises saved company theses, scheduled rechecks against new evidence, and read-only brokerage connections. Its changelog records scheduled monitors as shipped. Its public materials do not establish Hivemind’s exact fixed-question, append-only, settlement contract. [Investi](https://tryinvesti.com/), [shipped monitors](https://tryinvesti.com/changelog)
- **Would users notice the remaining difference?** Usually not during onboarding. They might notice when a source is corrected, the agent contradicts their preferred story, or an earlier judgment turns out wrong and remains visible. Your advantage must show up in those difficult cases. “Everyone reads the same state” is mostly invisible to someone managing five stocks.

- **4. Cold start: there is no honest way to manufacture lived history.**

- **Product day one:** Launch with a narrow covered set. Historical material can provide useful context immediately. Genuine monitoring history begins when you actually start monitoring.
- **Uncovered name:** Say “We have no maintained history for this company.” Offer a fresh assessment or a newly tracked question where supported. That experience will be weaker. Admit it.
- **Historical reconstruction is legitimate context, not a live track record.** Distinguish when the source was published, when your system processed it, and when the question and rule were chosen.
- **The added rule-replay idea does not fully solve this.** Even if every input predates the simulated decision, a rule chosen today benefits from knowing what happened afterward. “This rule would have triggered here” is an illustration. “We would have saved you” is not established.
- **Honest fix:** Use a clearly labeled historical walkthrough for explanation, and begin a real forward record. You can accelerate understanding; you cannot accelerate the passage of time.

- **5. The silent month: initially forgettable, eventually reassuring.**

- **Silence becomes valuable after demonstrated competence.** Before that, it leaves three possibilities unresolved: nothing relevant changed, the product missed something, or monitoring stopped.
- **One non-notification retention mechanism:** A permanent **“Why I still own this” card** beside the holding, where the user already checks it. Show their original reason, the exact tracked question and horizon, current assessment, last successful check, and the condition requiring their attention.
- **That card earns return visits by answering an existing question.** It should not invent daily activity. “Checked today; no qualifying change” can be useful even when the state has been unchanged for weeks.
- **Cut the compulsory Sunday message.** It is a notification, and “38 stories read” demonstrates volume rather than useful judgment. Put inspectable monitoring evidence behind the card instead.
- **Avoid “the drop had nothing to do with your thesis.”** The defensible statement is narrower: “We found no qualifying change in the evidence we monitor.” The proposal’s stronger explanation is not supplied by an unchanged state. [Example wording](./docs/agentic-experience.md:21)

- **6. The sharpest demonstrable wow**

- **One sentence:** “It catches a document that crosses the rule I set before the news, shows exactly why, and brings back the action I already chose.”
- **Seconds 0–3:** Show the saved belief, precise tracked question, and dated user-approved exit condition.
- **Seconds 3–6:** Show the new source sentence and the earlier versus current assessment. Label the inference where one is involved.
- **Seconds 6–10:** Show “This meets your condition; review your planned sale,” with the source and original instruction one tap away.
- **Why this is stronger:** It demonstrates continuity through a decision. It does not require promising superior returns or pretending a citation is unique. Use an actual forward-recorded case; label a reconstruction as a reconstruction.

- **7. What I would cut, and the one thing I would add**

- **Cut the automatic escalation story.** More accepted actions do not establish that the user should grant broader authority or allocate 25 times more money.
- **Cut broad victory language.** Say “this question resolved within your chosen range,” not “your investment judgment was right.” A frozen judgment is also not automatically a verified outcome; the proposed verification work remains necessary before claiming checked settlement. [Proposal’s outstanding work](./docs/agentic-experience.md:46)
- **Cut the quarterly example as written.** It both narrows the user’s year-end belief and relies on a quarterly numeric question where the frozen contract describes annual numeric questions and intermediate quarters as evidence. Choose an example the existing design actually supports. [Numeric-question contract](./docs/prd/06-views.md:53)
- **Cut the implied completeness of one selected belief.** “You did not choose the China question” means that rule is outside the mandate. It does not mean China cannot matter to the holding.
- **Cut the competitive absolutes:** “Nobody maintains this,” “GPT cannot do this,” and “rules can only use price.” They weaken an otherwise testable proposition.
- **Add one thing:** The permanent holding card described above. Its first job is to expose mismatches between the user’s belief and the question actually being monitored. That is more valuable than another polished plan.
- **Change the validation emphasis:** Draft acceptance measures onboarding ease. Test whether users understand the mapped condition, whether important developments are missed, and whether the workflow adds value against a competently configured existing agent. Include late alerts, rejected actions and unsuccessful outcomes—not just the attractive replay.

- **8. Final verdict**
- **Wow:** Deferred; demonstrable at the first useful, previously agreed intervention.
- **Utility:** Yes, for investors who want help maintaining explicit reasons for holdings.
- **Build it:** With a narrower promise: evidence-triggered review, honest history, and a visible record of what it caught and missed.
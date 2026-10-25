# Experience proposal: from incoming information to a tracked investment decision

October 23, 2026, ninth draft. English edition: October 25 (D163). **Discussion proposal, not approved by Alex.** The [system PRDs](prd/README.md), recorded decisions and [current state](CURRENT_STATE.md) govern the product. This document preserves the proposed experience; it does not authorise trading or change the frozen design. Its examples, competitor observations and research figures are historical draft material, not newly verified measurements. The [original draft](research/2026-10-25-english/experience-prd.original.zh.md) retains the complete earlier wording; [the short version](agentic-experience.md) describes the central journey.

Earlier drafts moved from “monitor your investment reason” to a broader entry point: a user may bring news, somebody else's post or a vague belief. The proposed scope is agent-assisted trading and investment, not only an agent managing money. This edition uses the system glossary for Hivemind concepts and distinguishes proposed user actions from existing library behavior.

## 1. Purpose

Turn incoming information into a clear, verifiable, time-bounded investment judgement that an agent can keep following. The surrounding stack can then turn the user's chosen outcome into a plan and act within explicit permissions.

Consider three people in the draft's July 10, 2026 scenario. Alex's father reads a report suggesting Chinese buyers may receive H200 chips and buys NVDA. Joyce's mother follows an influential investor's three reasons on Xueqiu, but the author never updates them. Alex holds NVDA for “AI demand” and worries after a price drop. They have different inputs, but none has made explicit which business outcome the position depends on, what would disprove it or when an answer should be available. After buying, price becomes their only feedback.

A conversational assistant can explain the news, supply background and list opportunities and risks. The proposal argues that an isolated answer does not by itself maintain a dated question, a history of evidence-based changes, a previously chosen exit condition and a later outcome record. Memory and scheduled tasks can help, so this is a workflow distinction to demonstrate, not a claim that competing products can never provide it. Earlier broad claims about sycophancy and absent follow-up remain in the source draft, not established findings of this POC.

The proposed product maps “I think AI demand will hold” to a maintained question such as annual NVDA data-center revenue growth, explains the mismatch between that question and the user's words, and shows the evidence behind its current state. The user chooses an expected rung and an exit condition. The agent follows new evidence, keeps a card beside the position and asks before acting if the judgement crosses the condition. At the due date, the proposal also wants an outcome record verified against published data; that extension remains subject to the system's final-verdict/pull-mode decisions.

The desired changes to user behavior are concrete: know the business outcome before buying, learn when its supporting reason breaks, and distinguish an unchanged evidence-based judgement from a price move. No profit or market-timing advantage follows from these alone.

The long-term stack has three owners: Hivemind maintains shared research; a trade-plan component translates the user's chosen outcome into a plan; an agent runtime monitors positions and executes authorised actions. Hivemind knows no individual user and holds no money. All agents read the same research record.

## 2. Terms in this proposal

Hivemind terms take their meaning from the [system glossary](prd/00-system.md#glossary). The user-facing planning terms below belong to the surrounding experience, not the thesis schema.

| Term | Meaning here | Example |
|---|---|---|
| Thesis | A question, fixed ladder and due date maintained by Hivemind | How will FY2027 data-center revenue compare with FY2026? |
| Ladder / rung | The defined possible outcomes; five, or two for yes/no under the system rules | Annual growth ranges; the draft's ranges are illustrative, not approved settlement boundaries |
| State / current judgement | Current rung judged from the evidence, with recorded reasons | Growth above 50% |
| Evidence tier | Fact, party statement, third-party view or rumour | Company guidance is a party statement; an unconfirmed unnamed-source claim is a rumour |
| Exit condition | The user's prior instruction linking a judgement change to a proposed position action | Sell all if judged growth falls below 10% |
| Trigger | A new judgement crosses the chosen exit condition | Show the supporting source and tier, not just the new score |
| Position card | A persistent display of belief, thesis, judgement, last check and exit condition | Available beside the holding, without routine push notifications |
| Checkpoint | A relevant event before the due date that may provide new evidence | Quarterly earnings |
| Outcome verification | The proposed check of published actuals against the ladder | Distinct from the currently decided freeze/close behavior; requires further design |
| Commitment record | The user's expected rung, exit condition, amount, date and permission | Stored by the surrounding runtime, not Hivemind |
| Permission level | Notify me / ask me first / act for me | First proposed version offers ask me first only |

The earlier draft described two to four questions per company and five bullish-to-bearish outcomes. Those are journey examples, not a hard quota or a replacement for binary/theme ladders. Likewise, evidence tiers do not impose an automatic “rumours never move a state” rule.

## 3. Ten steps from information to a decision

Using the draft's H200-report scenario:

| Step | Work | Example |
|---|---|---|
| 1. Identify the source | Who is involved, who said it and whether it is new | An unnamed-source retelling lacks official confirmation |
| 2. Identify the questions | Separate business outcomes with dates | Data-center growth, China revenue, margin and customers' own chips |
| 3. Match the information | Find the question it directly affects | China revenue or export licensing |
| 4. Weigh the evidence | Read it alongside evidence already in force | Twelve outlets retelling one report are not twelve independent sources |
| 5. Consider market expectations | Ask what is already reflected in price | Deferred from the proposed first version |
| 6. Draft the plan | Expected outcome, position size, entry, exit and horizon | A plan the user reviews |
| 7. Execute | Submit the authorised order | Runtime/broker responsibility |
| 8. Monitor | Repeat steps 1–4 when information arrives | Quarterly results or a new company filing |
| 9. Follow the plan | Respond to the prior exit condition | Ask before taking the agreed action |
| 10. Review the outcome | Compare the published result and retain the record | Annual result; keep research outcome separate from investment return |

The draft describes users often skipping from a headline to an order; this is a product hypothesis, not a measured population result.

| Steps | Owner | Status of the proposed capability |
|---|---|---|
| 1–4 | Hivemind | Categories, evidence, questions and rejudgement exist in the design. Granularity and matching vague input need validation |
| 5 | Undecided | Deferred |
| 6 | Trade-plan component | Separate component in the proposed stack |
| 7 | Agent runtime with broker/on-chain access | Outside Hivemind |
| 8 | Hivemind judges; runtime monitors | Change events carrying evidence and measured latency are proposed additions |
| 9 | Runtime | Permission-controlled action |
| 10 | Hivemind freezes research; runtime stores user commitments | Actual-number verification and outcome records remain proposed additions |

The user chooses whether to believe the judged outcome, what to commit and the exit condition. Hivemind does not choose a user position, move money or rank investors. Other components do not silently rewrite its thesis or manufacture its outcome.

## 4. Four users

| User | Input and difficulty | Desired experience |
|---|---|---|
| Alex | Own research compressed into “AI demand”; cannot separate a broken reason from anxiety about price | Separate the questions, choose the expected outcome and exit condition, inspect the reasoning |
| Alex's father | News reader who cannot analyse financial statements; buys on the headline | Plain explanation of the affected question, evidence strength and date; a small commitment if he chooses |
| Joyce | Professionally trained and fast to form a view; may trade impulsively and lacks time to monitor/review | Put the relevant research in front of her before the order, then track the plan and record outcomes |
| Joyce's mother | Trusts one commentator whose posts supply entry reasons but no updates | Map the commentator's reasons to questions without rating the person; alert when evidence undermines a chosen reason |

These correspond to four of the needs discussed in Joyce's earlier eight-needs framework. The proposal does not choose whom users should trust. It makes the business question and later evidence inspectable.

## 5. Alex's journey

The annual question remains open through interim earnings. August 26 is a checkpoint, not settlement. The examples below retain the original draft's illustrative dates and amounts.

| Time | User action | Product response |
|---|---|---|
| July 24 | “I hold NVDA. I think data-center demand will last to year-end. Yesterday's drop worried me.” | Match the question tracked since February 25, explain the mismatch, show its history and other relevant questions, draft a plan |
| July 25–August 25 | Check the holding as usual | Quietly update the position card's five lines: belief, thesis, current judgement, last check, exit condition |
| August 26 checkpoint | Read the short update | Quarterly data-center revenue is evidence for the annual question; say whether the judgement or exit condition changed and give the next checkpoint |
| A day in September | Read the source and confirm an action | A company filing crosses a separately chosen China-revenue condition; show its quote, tier and the previously chosen action |
| February 2027 | Inspect the annual outcome | Proposed verification of actual revenue and growth against the ladder; record price performance separately |
| Following year | Decide whether to change permissions or budget | Show requests, approvals, refusals, justified/unjustified triggers and omissions. Approval frequency is not accuracy |

The July 24 response could be:

```text
Closest maintained question:
How will NVDA FY2027 annual data-center revenue compare with FY2026?
Current judgement: growth above 50%.
Due: publication of the annual results in February 2027.

Illustrative history: May 20 Q2 guidance of $91 billion moved the judgement up
one rung. July 8 Foxconn AI-server revenue growth of 39.8% did not move it further.

You said “demand lasts to year-end”; the thesis asks about annual revenue growth.
Demand can hold while prices fall. Does this question represent your belief?
We found no relevant evidence change explaining yesterday's move in this thesis.
That is not a finding that the price move was unrelated.

Draft plan:
Expected outcome: growth above 50%.
Position: retain the current holding, without adding.
Exit condition: sell half if judged growth falls below 10%.
Checkpoints: August 26 Q2 results; November 17 Q3 results.
Due: February 2027 annual results.
Permission: ask me first.
Set any loss-based stop separately with your broker.
```

Alex changes “sell half” to “sell all” and confirms. The product records his instruction and the difference between his belief and the maintained question.

Other journeys retain the same structure. Alex's father gets a plain-language explanation of what the report affects and that it is not official confirmation. Joyce's mother sees the commentator's original words beside the mapped questions, then receives updates even if the post never changes. Joyce sees the relevant margin question before shorting after a memory-price report, along with its evidence tier and the honest absence of a market-expectations reading. The original draft's “seven of twelve” and “40% versus 65%” outcome examples are illustrative future records, not measured user results.

## 6. The central experience

Remember the exit condition before the news arrives. When a filing moves the judgement across it, bring the exact source and the user's previously chosen action together for review.

A ten-second demonstration shows the saved commitment, the new quotation and movement, then the requested action. Label inference and historical replay. The visible history gives the first experience credibility; a subject without maintained history must be described honestly.

Do not rely on “three seconds for ten steps,” “GPT cannot do this,” or “rules can only monitor prices.” A polished interface or a single convincing answer does not establish a maintained research process. Its value must survive corrections, disagreement with the user's preferred story and visible historical errors. More approvals do not establish sufficient accuracy to expand a budget.

The strongest value may emerge late. An evidence-based exit can follow a price decline. A replay using a condition chosen today is explanatory; it cannot prove the system would have protected the user in the past.

## 7. Two limits

1. A trigger reflects a **judgement**, not necessarily an established fact. Show the evidence and its tier; distinguish source statements from inference.
2. Evidence-based action can lag price. It addresses a broken investment reason, not a loss limit. The first proposed screen directs the user to a broker for loss-based stops.

## 8. Proposed first version

Include mapping from arbitrary user input with an explicit mismatch, a draft plan, ask-first permission, original quotes and tiers at a trigger, the persistent position card, short checkpoint/outcome updates and a record of requests, approvals, refusals, errors and omissions.

Defer market expectations, per-rung probabilities, recommendations, rankings, automatic execution, proprietary stop-losses, automatic budget growth and Sunday notifications. Do not infer an entire investment was correct from one question's outcome.

## 9. Historical comparison hypotheses

These observations belong to the October 23 draft. They require fresh verification before a competitive claim; translation does not validate them.

| Comparison | Draft observation | Proposed use or question |
|---|---|---|
| Distilla | Drivers, causal explanations, facts, summary snapshots, dated documents and consensus; the inspected topic rows appeared to lack fixed outcomes, due dates and retained changes | Potential upstream input and control. Is a question/history system materially different, or readily added? See the original inspection |
| Thesis workbenches | Investi, Jera Value, AlphaVue, InvestLab and Simply Wall St Narratives were cited as maintaining user theses and reviews | Test shared judgements, verified outcomes and agent interfaces rather than claiming nobody tracks theses. The draft cited seven million registered Narratives users; this is an unverified historical citation |
| Robinhood agent / Loops | Document/news reading, order proposals, approval and scheduled workflows were described | Potential execution environment and comparison arm; determine what maintained research they actually provide |
| ChatGPT with memory/scheduled tasks | Remembering user context and returning later | Compare maintained identity, evidence replacement and outcome history, not memory alone |

The source draft also cites roughly six minutes of research per retail trade, noisy earnings-related trading and about one percentage point lower six-month returns associated with price alerts. These are historical research claims to verify before use. Their product implication was fewer unsolicited interruptions. The draft is not fully consistent on whether checkpoint updates are pushed or merely available: section 8 includes checkpoint updates while the original section 9 allowed only trigger/outcome pushes. That notification decision remains open; translation does not decide it.

## 10. Joyce's fourteen challenges

Full historical discussion: [Joyce's challenge](joyce-challenge.md).

| # | Challenge | Proposed response, not proof |
|---|---|---|
| 1 | You only provide data | The intended product maintains questions and judgements; data is its input |
| 2 | The gap is in the planning/execution layers; this is a data vendor | The stack supplies those components; shared research is intended as an agent-readable record |
| 3 | Position sizing belongs in layer two | Agreed; Hivemind does not size positions |
| 4 | There may be no incremental investment judgement in layer one | Do not promise market-pricing advantage; measure consistency, timeliness and honest outcome records |
| 5 | GPT can do much of it | A single answer is not the comparison; test repeated maintenance and history |
| 6 | Derive layer one's needs from trade planning | Use the component-responsibility table and interface requirements |
| 7 | Wealthfront sells discipline; users have different needs | Prior exit conditions and explicit permissions address discipline; the four journeys differ |
| 8 | Asset-based and volume-based fees create opposing incentives | Platform incentives and whom the product serves require Alex's decision |
| 9 | Thesis monitoring reacts late, while Alex wants anticipation | Evidence-based exits may lag price; do not pretend otherwise |
| 10 | Hivemind should generate and push ideas | This proposal begins with user-supplied information |
| 11 | Pushed ideas become a screener | No screener or leaderboard in the proposed scope |
| 12 | The journey is already short; what happens after losses? | A reviewed plan should make the failed assumption identifiable, without promising protection |
| 13 | Where is the agent? | Monitoring and permission-controlled response to a judgement change |
| 14 | Use a bounded opportunity mandate with real money | The memo proposed a small amount, one week and one opportunity type as a validation unit; no live test is authorised here |

## 11. Proposed validation

| Check | Method | Measurement |
|---|---|---|
| Mapping and explanation | 20 real inputs: own beliefs, news, commentator posts and a pre-trade judgement | Correct mappings; user can explain the mismatch |
| Omissions | NVDA replay July 24–October 22, using only information available by each date | Correct/missed triggers and false “unchanged” days |
| Existing alternative | A configured comparison agent on the same period | Omissions, delay and differing answers |
| Willingness to use/pay | Proposed 50-person study covering the four profiles; the source draft suggests a 200-unit commitment over an earnings cycle | Actual participation, renewal and a second commitment; requires separate approval and currency definition |
| Honest reporting | Include refusals, late arrivals and wrong outcomes | No success-only presentation |

These are proposed acceptance studies, not completed measurements or permission to spend/trade. The first POC priority in this draft is mapping and omissions.

## 12. Risks

| Risk | Consequence | Proposed response |
|---|---|---|
| False reassurance from missed evidence | User continues holding after a material reason changed | Measure latency and omissions; show evidence tiers and the last completed check |
| No market-expectations reading | Correct business outcome can still accompany a losing investment | State the missing input |
| Wrong thesis granularity | Mapping and downstream plan follow the wrong question | Validate the questions first |
| Vague commentator input | User feels the view was misrepresented | Preserve original words beside the mapped question |
| Weak evidence moves judgement little | User may act independently on the headline anyway | Explain the evidence without claiming control over the user |
| Evidence arrives after price moves | Exit feels late | Target patient monitoring, not a promise of price protection |
| No maintained history | First experience resembles a fresh answer | State the lack of history |

## 13. Proposed Hivemind additions

The original proposal identified these gaps. Their current status must be read from CURRENT_STATE and the service PRD; this dated table is not a second implementation tracker.

| Addition | Purpose |
|---|---|
| Push changed judgements with supporting evidence | Let an agent respond without repeatedly polling |
| Expose processing records | Show the last completed check and what it processed |
| Measure source-to-judgement latency | Detect false reassurance caused by delay |
| Verify published outcomes in code | Do not let the model alone declare the realised answer |
| Retain question-level outcome records | Inform later permission decisions without confusing agreement with accuracy |

Mapping vague, undated long-form opinions and choosing a valid horizon also need testing. Market expectations and probabilities remain deferred. Outcome verification must be considered with pull-mode/final-verdict design, not inserted into the existing freeze rule through this proposal.

## 14. Decisions requested in the original draft

Alex was asked to decide the central experience, whether to serve all four users through an arbitrary-input entry point, the ask-first/card scope, component boundaries, whether to put section 13 on the design agenda and whether to begin with section 11's first two studies. This English edition does not treat those questions as approved.

## Source material

[Short experience proposal](agentic-experience.md), [Joyce's challenge](joyce-challenge.md), [granularity research](granularity-research.md), [earlier product direction](killer-experience.md), [user journey](user-journey.md), [Distilla inspection](distilla-reference.md), and original reports in `docs/research/2026-10-22-granularity/`. Earlier discussion documents remain historical sources, not competing current definitions.

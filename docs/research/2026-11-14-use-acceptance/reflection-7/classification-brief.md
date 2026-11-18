# Classification brief: does each topic have one main figure or event to ask? (blind, before any answer is written)

You read `/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-7/classification-packet.json`, 11 items. Each has a topic (description, outcome, period) and the article it came from. The company is NVIDIA (NVDA). The listed
themes are: chip-export-controls, ai-capex (AI capital spending), custom-silicon (custom silicon at cloud providers), semiconductor-cycle,
fed-policy-rate, us-inflation, us-recession-risk, us-china-tariffs, taiwan-strait, middle-east-conflict, russia-ukraine-war, supply-chain-shift.

The step that writes a question from a topic follows these rules, quoted verbatim:

> Return no_ladder with the reason, and ladder null, in seven cases: the topic has no main figure or event, naming none, or naming several with none of them the main one; nothing in the topic can be checked on a date, which for an event means that neither the topic nor the item gives a date and the topic names no period, unless it is a pending regulatory decision, for which use the company's current fiscal year-end; the figure is a company's figure for a quarter or a half-year, which is evidence to a yearly question; the figure covers a period that is not one fiscal or calendar year, such as a survey's rolling twelve months, and neither the topic nor the item gives the day it is published; the figure is for a year that has already ended on the item's day; the figure is for a year beyond next year, unless the topic's opens_as is binding_obligation; or the question belongs to another company or to a matter that no theme in the request's themes covers, in which case name that company or matter in the reason. Do not rewrite a figure for a year beyond next year as an event to keep it; a numeric completion target may define the state of an event that is itself the topic.

> A question about the company's revenue, profit, share, product progress or its own obligations is about the company: object is its ticker, even when policy or macroeconomics drives it. A question about what happens in the world, such as licensing, interest rates or aggregate spending, rather than the resulting effect on one company, belongs to a theme: object is a theme id from the request's themes. A question whose tracked outcome is a government's or regulator's decision to permit, restrict or ban a class of products or trade belongs to the theme that covers it, also when the product is the company's own: whether a health ministry lifts its import ban on one drug maker's vaccine belongs to the theme that covers that country's drug approvals. When the tracked outcome is the company's own sales, shipments or revenue under such a decision, the question is about the company, as is a proceeding against the company itself, such as an investigation of its conduct or a fine. A question about another company's own figure, or about a matter no listed theme covers, has no object here: return no_ladder.

A topic may name a main figure or event together with a second side of the same bet (a part of it, a condition, a comparison). The step's rules
(D436) say such a second side stays as context and is listed as not judged; it is not by itself a reason to decline.

For each item, answer:
- "write": the topic has one main figure or event that can be asked, and none of the seven cases applies to it; or
- "decline": one of the seven cases applies (name which, in a few words).

Judge from the topic and the article only. Return exactly 11 lines, one JSON object per line, in item order:
{"item": <n>, "call": "write" | "decline", "case": "<the decline case, or the main figure or event if write>", "why": "<one sentence, quoting the topic or article>"}
No prose before or after, no code fence. You are read-only: open only this brief and the packet.

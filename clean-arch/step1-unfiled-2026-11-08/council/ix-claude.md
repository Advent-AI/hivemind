# ix — independent read of the eight hand-written three-outcome answers (Claude)

Date: 2026-11-10. Read-only. No model call, no run, no file edited.

**What I read, and nothing else:** `clean-arch/step4-2026-11-10/stage_a/result/three-outcomes-by-hand.txt` (whole file) and, from
`clean-arch/step4-2026-11-10/stage_a/cases.json`, the eight entries acc/clean-2, u1/clean-12, u2/clean-3, u3/clean-12, u3/clean-5,
u1/clean-3, u1/clean-11, u3/clean-9 (thesis fields and the full article text of each). u2/clean-3 and u3/clean-5 share one article
byte for byte; so do u1/clean-12 and u3/clean-9.

**How to read the sources below.** Words in quotation marks are copied from one of the two files. A fact marked *(my knowledge)* is
not in either file: it is a real-world precedent or a rule of procedure I bring, and it is a lead to check, not a measurement.
"The judge" is the later reader who sees the question and the rungs, and not the "->" lines.

## Verdict in one table

| thesis | a. happened = thesis's event | b. ruled out is a real ruling out | c. checkable on the due day | d. "->" lines | e. not judged |
|---|---|---|---|---|---|
| acc/clean-2 | yes; question and rung name different proofs | "a regulator has blocked it" is not always final | yes | all 3 right; a restructure that replaces the purchase has no clean rung | allowed kind |
| u1/clean-12 | yes | rung 2's words also fit "investigation ended, Nvidia charged" | closure need not be published | 1 of 3 right only if the conclusion ends the case | fine size and remedy kind dropped, not listed |
| u2/clean-3 | yes | real, but a rejection is only counted when officially announced | proof may never exist | both right | allowed kind |
| u3/clean-12 | partly: asks "in force on the day", not "has moved" | real, rarely made | yes for a published rule | both right; "any other" lets small actions in | "how far" (the thesis's first words) dropped, listed |
| u3/clean-5 | no: asks whether a disclosure exists in two document types | can hold with nothing decided (standing lock-out) | rung 1 yes, rung 2 not reliably | 1 of 2 unsafe | permission-without-sale and the US side dropped |
| u1/clean-3 | mostly; "start of revenue" cut | no rule-out rung (fine for a deadline) | **no** | 1 of 2 cannot be reached by any judge | empty; a definition is missing |
| u1/clean-11 | partly: the thesis's second proof removed | a general ban is not how a "no" arrives here | **not reliably** | **1 of 2 sits in the wrong rung by the owner's words** | the open half of the thesis dropped |
| u3/clean-9 | partly: thesis names the finding; rungs copied from u1/clean-12 | same as u1/clean-12 | same | both right | the finding, which this thesis names, dropped |

---

## 1. acc/clean-2 — Nvidia completes the Hugging Face purchase, due 2028-03-05

Article (2026-09-05): "On Thursday, NVIDIA ... announced a $12.9 billion deal to purchase Hugging Face". It gives no closing date, no
condition and no word on any review.

**a. Happened = the thesis's event? Yes.** Thesis outcome: "Whether Nvidia closes (or abandons/restructures) the announced $12.9
billion purchase of Hugging Face". Rung 1: "Nvidia has completed the acquisition of Hugging Face on or before 2028-03-05."
One mismatch inside the answer itself: the question ends "as reported in Nvidia's Form 8-K, Form 10-Q or Form 10-K", and rung 1 names
no proof at all. A completion announced by press release, with no filing yet, is rung 1 by the rung and "not shown" by the question.
The judge is handed two tests.

**b. Ruled out a real ruling out? Two of its three triggers are; the third is not always.**
Rung 2: "Nvidia or Hugging Face has announced that the acquisition is terminated or abandoned, or a regulator has blocked it."
- "terminated or abandoned" by announcement: a real ruling out.
- "a regulator has blocked it": (i) it is worded as something that happened at any time "On or before 2028-03-05", so a block that is
  under appeal, or was later cured, still counts. *(my knowledge)* Microsoft–Activision: the UK regulator prohibited the deal on
  26 April 2023; the deal was reshaped, cleared and closed on 13 October 2023. Any due day in those months reads "Ruled out" for a
  deal that closed. (ii) "blocked" is not defined. A regulator that goes to court to stop a deal has not blocked it; the case is
  pending, which is "still waiting". And in the United States the stop comes from a court, which is not "a regulator": a deal halted by
  a court order, before anyone announces termination, is literally rung 3.
- Both holding with rung 1 wrongly on top: Nvidia completes, then a regulator orders the purchase undone. *(my knowledge)* Meta–Giphy:
  completed May 2020, ordered sold in November 2021. Rung 1 wins and the answer is "Happened" while the asset must be sold. Unlikely for
  a deal this size, which normally waits for clearance; named because the question asks.

**c. Checkable? Yes**, for completion and for an announced termination. "the deal lapses with no announcement" is by its own wording a
fact nobody outside could know; the file sends it to rung 3, which is where a judge would put it anyway.

**d. The "->" lines.** All three are placed correctly given the rung words: "completed at a revised price ... rung 1", "the deal lapses
with no announcement and has not closed: rung 3", "abandoned by announcement: rung 2".
Attempts to break it:
1. *A restructure that replaces the purchase.* The thesis outcome names "restructures". Suppose the two companies announce a "revised
   agreement": Nvidia licenses the technology and hires the team, or takes a minority stake. *(my knowledge: Microsoft–Inflection 2024;
   Meta's 49% of Scale AI 2025.)* Rung 1: no, the acquisition is not "completed". Rung 2: only if someone says "terminated or
   abandoned". Otherwise rung 3, which reads as "still pending" although the purchase is off. The "not judged" entry covers only a
   restructure that still closes ("whether the deal closes on restructured terms or at another price").
2. A regulator sues to stop the deal, case pending on the due day: rung 2 or rung 3 depending on how the judge reads "blocked". An
   analyst says rung 3.
3. A block under appeal on the due day: rung 2 by the words. An analyst says contested, not dead.
4. A partial purchase (a majority but not all of the company, or one business of it): "completed the acquisition of Hugging Face" is
   undecidable from the words.

**e. Not judged.** "whether the deal closes on restructured terms or at another price" is the kind the owner allowed. "Rejected versus
still waiting" is kept in form (rung 2 against rung 3) and leaks at "blocked", as in b. Not listed although the thesis's `settled_by`
names "regulatory clearance announcements": "cleared and about to close" and "under review" both sit in rung 3 with no line in the list.

---

## 2. u1/clean-12 — French competition authority fines or orders a remedy, due 2027-01-31

Article (2026-07-09), the only sentences on the matter: "the French competition authority announcing Thursday that its antitrust
investigation into the company is nearing a conclusion. This probe focuses on allegations of anti-competitive practices within the
cloud-AI and GPU markets."

**a. Happened = the thesis's event? Yes.** Thesis outcome: "The French competition authority's conclusion of its antitrust
investigation ..., and any remedies or fines imposed." That is two things, a conclusion and a sanction. Rung 1 takes the sanction
("published a decision imposing a fine, a remedy or both on Nvidia"), rung 2 the conclusion without one, rung 3 no conclusion. Both
parts are carried, provided rung 2 means what it is meant to mean. It does not always: see b.

**b. Ruled out a real ruling out? Not as worded. This is the serious defect of the two French answers.**
Rung 2: "the authority has closed the investigation, or published its conclusion, with neither a fine nor a remedy."
Nothing in these words says the case is over. *(my knowledge)* In French procedure the investigation is run by the authority's case
team. It ends in one of two ways: the case is dropped, or written charges are sent to the company. A fine or a remedy is decided later
by the authority's board, usually many months after the charges. The article's "nearing a conclusion" of the "investigation" is that
earlier step. So the likeliest state on 2027-01-31, under seven months after the article, is: investigation ended, Nvidia charged,
decision still to come.
Read that state against rung 2: the investigation is closed, its conclusion is out, and there is "neither a fine nor a remedy". The
words fit. The answer would be "Ruled out" on the day a fine has become more likely, not less. An analyst puts this state in rung 3.
Rung 1 and rung 2 both holding in a harmful way: I found none (a fine on one part of the case and a closure of another is rung 1, which
is right).

**c. Checkable?** Rung 1, yes: "published a decision". Rung 2's first half says "has closed the investigation" with no "published": a
case dropped quietly by the case team is a fact nobody outside may know, and it then sits in rung 3 beside "still open". The file's own
third "->" line ("the investigation still open, its status not stated by the authority") lands in the same place, so the two cannot be
told apart. *(my knowledge)* Charges are not normally published by the authority; they become known when the company or the press says so.

**d. The "->" lines.**
- "a conclusion that neither finds nor clears the conduct and imposes nothing ... rung 2 Ruled out": right only when that conclusion
  ends the case. The same words describe the end of the investigation stage (b), and a general market report that imposes nothing on
  anyone *(my knowledge: the authority also issues such reports)*. In both, "Ruled out" is wrong and the rung text cannot tell.
- "a remedy accepted with no finding of an infringement ... rung 1 Happened": right in intent. But rung 1 says "imposing" and the line
  says "accepted". Promises a company offers and the authority makes binding are not plainly "imposed"; a literal judge can read such a
  decision as rung 2, a closure with "neither a fine nor a remedy". The judge does not see the "->" line.
- "the investigation still open, its status not stated by the authority ... rung 3": right.

Attempts to break it:
1. Charged, decision pending: rung 2 by the words, rung 3 in truth (b).
2. The European Commission opens its own case and the French authority closes its file *(my knowledge: a national authority loses a case
   when Brussels takes it)*: rung 2, literally true for France, and the reader is told "Ruled out" when the antitrust risk has grown.
3. A fine for obstructing the investigation, not for the practices *(my knowledge: the authority has fined companies for this)*: rung 1
   by the words "a decision imposing a fine ... on Nvidia".
4. An interim order while the case continues: rung 1; an analyst would probably accept it.

**e. Not judged.** Listed: "whether the conclusion finds anti-competitive conduct". Dropped and **not listed**: how large the fine is
and what the remedy touches. Rung 1 puts a token fine and an order that changes how Nvidia sells GPUs in one outcome. That is the kind
of finer difference the owner allowed, but his rule is that it is listed, and it is not. "Rejected versus still waiting" is kept only
if rung 2 is read as "case dropped"; the charged case breaks it.

---

## 3. u2/clean-3 — Chinese authorities permit H200 sales in mainland China (theme), due 2027-01-31

Article (2026-07-02): "The Chinese government has to date locked Nvidia out of the China market, despite the Trump administration
having cleared its path for H200 exports." Most of the article is about Washington: "Nvidia is losing sympathy in Washington"; "I hope
that would give members of Congress and staffers and the White House pause".

**a. Happened = the thesis's event? Yes.** Thesis outcome: "An official Chinese government/regulator decision permitting (or continuing
to bar) H200 sales in China, confirmed by an official Chinese announcement or by NVIDIA disclosing H200 China revenue/shipments."
Rung 1 keeps both proofs: "an official Chinese announcement has permitted H200 sales in mainland China, or NVIDIA has disclosed H200
sales or shipments into mainland China."

**b. Ruled out a real ruling out? Yes when it occurs; three weaknesses.**
Rung 2: "Chinese authorities have officially announced that H200 sales in mainland China are prohibited."
- It is an event at any time "On or before 2027-01-31". A prohibition announced in the autumn and eased later without an official word
  (the way the sibling article shows easing arrives, see c) leaves rung 2 holding: "Ruled out" on a day sales are allowed.
- The reverse order: permission announced, or sales disclosed, then a new ban before the due day. Rung 1 wins: "Happened" on a day the
  ban stands. The thesis asks "will Beijing lift the block that currently keeps NVIDIA's China share at zero"; for that reader rung 1
  taking precedence gives the wrong picture.
- No start date: an official prohibition announced before the article would satisfy it.

**c. Checkable?** When the proof exists, yes. The doubt is whether it will exist. The other article in this set on the same matter
(u1/clean-11, six days later) shows how a Chinese permission arrives: "Chinese officials have informed companies such as Alibaba Group,
ByteDance and DeepSeek that they will have permission", "according to the Information", "citing two unidentified people familiar with
the matter". The one official quoted says only that "the country's position on US chip exports has been consistent". No official
announcement. If a refusal arrives the same way, rung 2 can never hold, and rung 1 can only be reached through NVIDIA's own disclosure.
On that second route: the thesis period is "NVIDIA's fiscal year-end (FY2027, late January 2027)", the due day itself. The report that
covers November to January cannot be out on 2027-01-31, so sales that start in those months are invisible on the due day unless NVIDIA
says so elsewhere.

**d. The "->" lines.** Both right: "no announcement of any kind; whether a review is pending cannot be known ... rung 3", and "a
permission with conditions and a disclosure of sales ... rung 1" (conditions are listed as not judged).
Attempts to break it:
1. Permission reported by the press, chips arriving, no official word, NVIDIA's next report after the due day: rung 3. An analyst says
   it happened.
2. Regulators reported to have told firms not to buy, no official word: rung 3. An analyst says rejected.
3. **Washington withdraws its clearance.** The sale is then formally ruled out, by the other government. Rung 2 covers a Chinese act
   only, so the answer is rung 3, "neither". This is the risk the article is about.
4. NVIDIA stops offering the chip for China (writes off the stock, moves to another product). In the owner's words that is "formally
   abandoned or withdrawn". Rung 3 again.
5. An official notice that firms "may apply" case by case, nobody approved yet: rung 1 or rung 3 depending on the judge's reading of
   "has permitted H200 sales".

**e. Not judged.** "conditions or quantity limits attached to a permission" is the allowed kind; "NVIDIA's China share remaining at
zero" is harmless. "Rejected versus still waiting" is kept on paper and lost whenever the rejection is not an official Chinese
announcement (breaks 2, 3, 4).

---

## 4. u3/clean-12 — a binding US restriction on AI-chip shipments to third countries (theme), due 2027-01-31

Article (2026-07-14): "The US Commerce Department issued guidance in May aimed at curbing advanced AI chips from reaching overseas
subsidiaries of Chinese companies"; and the news itself: "NVIDIA has more than halved the number of Asian customers authorised to buy
its AI chips".

**a. Happened = the thesis's event? Partly.** Thesis outcome: "Whether the US Commerce Department / Bureau of Industry and Security
moves beyond its May 2026 guidance to a binding export-licensing rule or other escalated restriction ..., and the resulting constraint
on Nvidia's sales to those markets." The thesis tracks a move. Rung 1 asks for a state on one day: "A binding US restriction, a
licensing rule or any other, ... is in force on 2027-01-31." This is the only one of the eight worded that way; the other seven say "on
or before". Effect: a rule issued in December 2026 that starts in March 2027 is not "in force", so rung 3, although Commerce has moved.
*(my knowledge: the January 2025 US chip rule was published with a start date four months later and was withdrawn before it began.)*
Two widenings as well: "US" (any body) where the thesis says Commerce; "any other" where the thesis says "other escalated restriction".
The second half of the outcome, "the resulting constraint on Nvidia's sales", goes to "not judged".

**b. Ruled out a real ruling out? Yes in form.** Rung 2: "the Commerce Department has formally announced that it will impose no such
restriction, and none is in force." It cannot hold together with rung 1 ("and none is in force"), so precedence is never wrong here.
Such an announcement is rare *(my knowledge: one precedent, the May 2025 announcement withdrawing the earlier rule)*. An easing that
does not use those words (the May guidance itself withdrawn, or replaced by agreements with the countries) is rung 3.

**c. Checkable?** A published rule and its start date: yes. A restriction sent by letter to one company is binding and "in force" but
known outside only if the company discloses it *(my knowledge: the April 2025 licence requirement on one Nvidia chip arrived by letter
and became public through Nvidia's own filing)*.

**d. The "->" lines.** Both right: "a licensing rule and another restriction both adopted ... rung 1" (if in force on the day) and "one
proposal pending while another has been rejected ... rung 3" (a rejected proposal rules nothing out while another is pending).
Attempts to break it:
1. Rule issued, start date after the due day: rung 3 by "in force"; an analyst says happened.
2. "any other": the US adds a few named Malaysian or Singaporean firms to its blacklist, a routine act. It is binding, in force, about
   shipments to third countries and later than the guidance, so rung 1 by the words. An analyst says that is not the escalation tracked.
3. No start date: binding US restrictions on such shipments existed before May 2026; the article says chips "may have been exported to
   Chinese-linked entities in countries such as Malaysia despite US restrictions". "beyond the May 2026 guidance" has to be read as
   "newer and stricter than", which is not written. A literal judge can find rung 1 true on the day the thesis opens.
4. A rule for other countries only: rung 1; the thesis names "Malaysia, Singapore and Japan". Listed as not judged ("which countries
   it covers").
5. A rule in force and then suspended by a court on the due day: "in force" is undecidable.

**e. Not judged.** Listed: "the resulting constraint on Nvidia's sales to those markets" and "how far the restriction goes: a licensing
rule or another, and which countries it covers". Both are listed, so within what the owner allowed. Note what they are: the thesis
description's first words are "How far will the US crackdown ... escalate", and the article's own news is that Nvidia's sales are
already constrained with no binding rule. A rule that only writes Nvidia's present practice into law and a cap on whole countries are
the same "Happened". "Rejected versus still waiting" is kept (the second "->" line shows it).

---

## 5. u3/clean-5 — Nvidia discloses revenue from H200 sales to customers in China, due 2027-01-31

Same article as u2/clean-3.

**a. Happened = the thesis's event? No.** Thesis outcome: "Whether H200 sales to Chinese customers take place (China data-center
revenue returning above zero) versus Beijing keeping Nvidia locked out despite the U.S. approval." Rung 1 asks instead whether a paper
exists: "Nvidia has disclosed, in a Form 10-Q or an earnings release, revenue from H200 sales to customers in China." Three narrowings:
- *Time.* The thesis period is "by Nvidia's FY2027 year-end" and `settled_by` names the "FY2027 Form 10-K". A 10-K for a year ending
  late January 2027 cannot be out on 2027-01-31, and the rung leaves the 10-K out. Sales in the last fiscal quarter cannot count.
- *Document.* A statement by the finance chief does not count unless it is repeated in the release or the 10-Q. The u1/clean-11
  article quotes exactly that kind of statement: "Colette Kress said the H200 chips had yet to generate any revenue for the company in
  China."
- *Product.* The thesis accepts "China data-center revenue returning above zero"; the rung needs revenue named as H200.
Each narrowing makes the rung checkable on the day. Together they turn "did sales take place by the year-end" into "was it written, by
chip name, in two kinds of document about the quarters before the last one".

**b. Ruled out a real ruling out? It can hold with nothing decided.** Rung 2: "On 2027-01-31 a formal Chinese prohibition on purchases
of H200 chips by Chinese customers is in force." It is a state on the day; it does not ask that anything was decided during the period.
The article: "The Chinese government has to date locked Nvidia out of the China market". If that lock-out is "a formal Chinese
prohibition", rung 2 is true the day the thesis opens and stays true if nothing happens at all: "Ruled out" would mean "Beijing has not
lifted it yet", which is waiting. If the lock-out is informal, the same nothing-happened world is rung 3. The line between "rejected"
and "still waiting" therefore hangs on the word "formal", which the article does not settle.
Both holding: revenue disclosed in November, a ban in force in January, gives rung 1. Right for "sales took place"; the reader of
"Happened" is not told the door is shut again.

**c. Checkable?** Rung 1: yes, by construction. Rung 2: it needs to be known that a prohibition is in force on one given day. Where the
prohibition is not published, that is a fact nobody outside could know.

**d. The "->" lines.**
- "a prohibition in force while a review of it is pending ... rung 2 Ruled out": it fits the rung's words, and I think it is unsafe.
  In this outcome "rejected" and "still waiting" are both true, and the answer picks "rejected". If the ban is new, a decision against
  was taken and rung 2 is right. If it is the standing lock-out, the pending review is the very thing this thesis waits for (the
  description: "will Beijing permit Chinese commercial users to buy the chips"), and the right reading is "still waiting". The rung
  cannot tell a new ban from the old one.
- "a permission announced and no sale disclosed ... rung 3 Neither": right by the words, and listed as not judged. The same world is
  "Happened" in u2/clean-3. That is defensible because the two theses differ, but see e.

Attempts to break it:
1. The finance chief says on the results call that H200 revenue from China has begun; the release and the 10-Q give revenue for China
   without naming the chip: rung 3 by the words.
2. Sales in November to January, reported in late February: rung 3 on the due day, contradicted weeks later by the 10-K the thesis names.
3. Washington withdraws its clearance: rung 3. And "the US clearance of H200 exports in December 2025" is expressly "not judged".
4. Nvidia withdraws the product from China: rung 3.
5. Chips sold to Chinese companies' sites outside China: "customers in China" is undecidable.

**e. Not judged.** "Beijing permitting purchases where no sale has yet been disclosed" is not a finer difference inside one outcome. It
is the step the thesis description itself puts after "i.e.", and it sits in "Neither" beside "nothing happened". An analyst holding
only this card needs it; it is carried only if u2/clean-3 or u1/clean-11 is also held. "the US clearance of H200 exports in December
2025": leaving this out removes one way the event is ruled out (break 3). Not listed: the size of the revenue. "Rejected versus still
waiting": depends on "formal", see b.

---

## 6. u1/clean-3 — Vera Rubin first shipments by 2026-12-31 (two rungs)

Article (2026-07-02): "Vera Rubin, Nvidia's next-generation AI chip platform, is in full production and could begin shipping later
this year."

**a. Happened = the thesis's event? Mostly; one cut.** Thesis outcome: "Whether Vera Rubin reaches first shipments (start of revenue)
by the end of 2026"; the description: "begin first shipments — the step that brings revenue". Rung 1: "First shipments of Vera Rubin
took place on or before 2026-12-31." "start of revenue" is gone and there is no start date. Trial units sent to customers are "first
shipments" by these words; the article does not say whether any have gone out.

**b. Ruled out.** There is no rule-out rung. That is right for a deadline: on the day itself, "ruled out" and "has not happened" are
the same thing. But rung 2, "Rung 1 does not hold on 2026-12-31", is also where a judge ends up when it cannot tell.

**c. Checkable? No. This is the one answer of the eight that cannot be judged on its due day.**
It is the only one with no proof named in the question or in a rung. The thesis's `settled_by` is "NVIDIA quarterly earnings releases
and 10-Q/10-K disclosures confirming Vera Rubin first shipments/revenue, and shipping confirmations." The period fields of the other
theses put Nvidia's fiscal year-end in "late January 2027". So the quarter that contains December 2026 ends in late January 2027, and
its earnings release and the 10-K are published after 2026-12-31. A first shipment in the last weeks of the year needs a document
published after the due day.
It is worse than late: that quarter runs across 31 December. A later statement that the platform "began shipping in the fourth quarter"
does not say on which side of 31 December. The fact may never be knowable from outside.

**d. The "->" lines.**
- "shipments began and no confirmation has been published ... rung 1 Happened": true as a fact, and no judge can reach it. On the due
  day this world and the next line's world ("no shipment by the day: rung 2 Not happened") look identical from outside. The file sends
  two worlds that cannot be told apart to opposite rungs. A judge who sees no confirmation will answer rung 2, the opposite of the
  file's placement. The first run's problem ("neither Yes nor No in the first run") has been assigned a rung, not solved.
- "no shipment by the day: rung 2": right.

Seven of the eight write their conditions as a published act, so "nothing published" falls safely into the last rung. This one writes
its condition as an unpublished fact, so "nothing published" has no correct rung.
Attempts to break it:
1. Trial units already sent: rung 1 on day one.
2. One part of the platform ships (the processor, or the networking part) and the rest does not; or chips reach the assemblers and no
   finished system reaches a buyer: "First shipments of Vera Rubin" is undecidable.
3. First shipment in January 2027, inside the same fiscal quarter: published confirmations cannot separate it from December.

**e. Not judged.** The list is empty. What is missing is not a finer difference but the definition of the event: do trial units count,
and which part of the platform. The volume of the first shipments could have been listed. There is no "rejected versus still waiting"
line to keep.

---

## 7. u1/clean-11 — Chinese authorities approve imports of H200 by Chinese firms (theme), due 2027-01-31

Article (2026-07-08): "Chinese officials have informed companies such as Alibaba Group, ByteDance and DeepSeek that they will have
permission to purchase some of the processors"; "The companies need to say how many chips they need – and why – to get approval"; "The
Chinese government, meanwhile, is still figuring out how many H200 chips to allow the companies to buy, but the total may end up being
fewer than 200,000".

**a. Happened = the thesis's event? Partly; the thesis's second proof is removed.** Thesis outcome: "Whether Chinese authorities grant
approval for Alibaba, ByteDance, DeepSeek and other firms to import Nvidia H200 chips (potentially a total below 200,000), as reflected
in official Chinese government decisions and in Nvidia's disclosed China H200 revenue." Rung 1: "Chinese authorities have officially
approved imports of H200 chips by at least one Chinese firm"; the question: "as shown by official Chinese government decisions or
announcements". "Nvidia's disclosed China H200 revenue" is cut from the question and moved to "not judged" ("Nvidia's resulting H200
revenue in China"). u2/clean-3, on the same matter, kept it.

**b. Ruled out a real ruling out? Yes if it occurs; it is not the form a refusal takes here.** Rung 2: "Chinese authorities have
officially prohibited imports of H200 chips, and no approval has been given." The article describes a request-by-request process
("need to say how many chips they need – and why – to get approval"). In such a process a "no" is a refused request, not a general
prohibition, and least of all after officials have told the firms "they will have permission".
No start date: the article's summary calls the move "easing previous restrictions". If those restrictions were official and no firm is
approved yet, rung 2 is literally true on the day the thesis opens.
Both holding: an approval in the autumn and a ban in winter gives rung 1 (and rung 2's own guard, "no approval has been given", fails):
"Happened" on a day imports are banned.

**c. Checkable? Not reliably.** An approval for one firm is given to that firm. In the article, knowledge of the policy came from "the
Information", "citing two unidentified people familiar with the matter"; the official on record stated no fact. Whether "at least one
Chinese firm" has been approved is, without a leak, a fact nobody outside could know, and a leak is not what the question accepts. The
proof that would exist, Nvidia reporting H200 revenue, was removed. The thesis period says "checked at its next annual report/10-K",
which is after the due day.

**d. The "->" lines.**
- **"some requests refused and the others withdrawn or lapsed ... rung 3 Neither".** By the rung words this is correct: there is no
  general prohibition. By the owner's own words for outcome 2, "decided against, or formally abandoned or withdrawn", it is not: every
  request in this world has been decided against or withdrawn, and nothing is pending. An analyst calls it "China said no". The answer
  puts it in the rung that reads "still waiting". Of all the "->" lines in the file this is the one I judge to be in the wrong rung,
  and the cause is rung 2 being written as a general ban only. (The counter-argument: firms can apply again, so the event is not ruled
  out for good. No rejection is for good; the same is true of an announced ban.)
- "a limited approval for some firms: rung 1 Happened": right; quantity is listed as not judged.

Attempts to break it:
1. Nvidia reports H200 revenue from China and there is no Chinese announcement: a judge holding to "as shown by official Chinese
   government decisions or announcements" answers rung 3. The same world is "Happened" under u2/clean-3.
2. Washington withdraws its clearance: rung 3.
3. Is the article's own state already rung 1? "will have permission to purchase some" against "need ... to get approval": two judges
   can differ on day one.
4. State-owned buyers barred, private firms allowed, none approved yet: rung 2 by the words "officially prohibited imports of H200
   chips, and no approval has been given".

**e. Not judged.** "how many chips are approved, such as a total below 200,000" and "Nvidia's resulting H200 revenue in China". The
thesis description asks "— and roughly how many —". After this article, that some purchase will be allowed is already reported; how
many, and whether revenue follows, is what is still open, and the article says why it matters: "that is not a large number. A single
data centre can use more than 400,000 Blackwell processors." Both open parts are in "not judged". They are listed, so the form of the
owner's rule is met; the part an analyst would hold the card for is not judged. "Rejected versus still waiting" is **not** kept for the
way a rejection would really arrive (first "->" line).

---

## 8. u3/clean-9 — French competition authority, second thesis on the same article, due 2027-01-31

**a. Happened = the thesis's event? Partly.** Thesis description: "conclude ... with an adverse decision, fine or remedy, and by when?";
outcome: "including the decision date, finding and any fine or remedy imposed." The rungs are word for word those of u1/clean-12, whose
thesis does not name the finding. Here the finding is named, and it is put in "not judged" ("whether the conclusion finds
anti-competitive conduct"). A decision that finds a breach and sets neither a fine nor a remedy goes to rung 2, "Ruled out", beside a
clean closure, although the description counts an "adverse decision" on the yes side. It is rare in practice *(my knowledge: a finding
normally comes with a fine or an order)*, but the label is the opposite of the thesis's.
"and by when?" becomes "the date of the decision" under "not judged"; the due day carries only before or after.

**b. and c.** As for u1/clean-12: the same rung 2 words, so the same defect (investigation ended, Nvidia charged, reads as "Ruled
out") and the same unpublished-closure gap. One small mismatch: the question says "published decision or conclusion statement", rung 1
says "published a decision" only.

**d. The "->" lines.** "a remedy with no finding of an infringement ... rung 1" is right, with the "imposing" against "accepted"
caveat of u1/clean-12. "the investigation still open and the authority silent on its status ... rung 3" is right. The breaks are those
of u1/clean-12, plus the finding without a sanction (a).

**e. Not judged.** The finding is dropped although this thesis names it; fine size and remedy kind are dropped and not listed.
"Rejected versus still waiting": as u1/clean-12.

---

## Across all eight

**C1. "Ruled out" is written as one formal act in every answer, narrower than the owner's own words, so real rejections fall into the
last rung.** The owner's outcome 2 is "decided against, or formally abandoned or withdrawn". The rungs accept: an announced termination
or a regulator's block (acc/clean-2), a closure without sanction (the French pair), an official Chinese announcement or a formal Chinese
prohibition (the three H200 answers), a Commerce announcement of no restriction (u3/clean-12). Not accepted, and landing in "neither":
every request refused or withdrawn (u1/clean-11's own "->" line), a refusal that reaches firms without an announcement, Washington
withdrawing its clearance, Nvidia withdrawing the product, a purchase replaced by a different kind of deal. The last rung is a
catch-all, so nothing can "fit no rung" any more; the cost has moved to what the last rung means. It now holds "still waiting", "said
no in a way the rung did not foresee" and "cannot be known" together.

**C2. One matter, three answers, three different rule-outs.** H200 into China is asked three times. u2/clean-3: "have officially
announced that ... are prohibited" (an event). u3/clean-5: "a formal Chinese prohibition ... is in force" on the day (a state).
u1/clean-11: "have officially prohibited ..., and no approval has been given" (an event with a guard). The same world gets different
answers:

| world on 2027-01-31 | u2/clean-3 | u3/clean-5 | u1/clean-11 |
|---|---|---|---|
| Nvidia's November release names H200 revenue from China; no Chinese announcement | Happened | Happened | Neither on a strict reading |
| Official permission announced; no sale disclosed yet | Happened | Neither | Happened only if a firm is named |
| Ban announced in autumn, eased quietly in December, no sale disclosed yet | Ruled out | depends on "in force" | Neither (guard fails) |
| Washington withdraws its clearance | Neither | Neither | Neither |
| Every firm's request refused or withdrawn, no general ban | Neither | Neither | Neither |

The last two rows are rejections in an analyst's reading and "neither" in all three.

**C3. No condition has a start date.** Every rung says "on or before" the due day or "on" it; none says "after the article". Where the
state already existed when the thesis opened, the question can be answered on day one by the old state: u3/clean-12 (binding
restrictions older than the guidance: "despite US restrictions"), u3/clean-5 ("has to date locked Nvidia out"), u1/clean-11 ("easing
previous restrictions"), u1/clean-3 (trial units), u2/clean-3 (an older announcement).

**C4. Event or state is not ruled.** Seven rung 1s are events ("on or before"); once true they stay true, so "allowed, then banned
again" reads "Happened". One (u3/clean-12) is a state ("is in force on"), so "issued, starts next month" reads "Neither". Of the seven
rung 2s, four are plain events (acc/clean-2, u1/clean-12, u2/clean-3, u3/clean-9), two are events with a guard about the day
(u3/clean-12 "and none is in force", u1/clean-11 "and no approval has been given") and one is a state (u3/clean-5). Nothing in the
answers says which form is used when, and the choice changes the answer.

**C5. The proof is handled five different ways.** In the question but not in the rung (acc/clean-2, u3/clean-12); in both (the French
pair, and u2/clean-3, which keeps both of the thesis's proofs); in the rung, narrowed to two document types (u3/clean-5); one of the
thesis's two proofs removed (u1/clean-11); none at all (u1/clean-3).

**C6. The "not judged" lists are incomplete against the owner's rule that a dropped finer difference is listed.** Not listed: fine size
and remedy kind (both French answers); size of the revenue (u3/clean-5); trial against revenue shipments and volume (u1/clean-3, empty
list); stage of regulatory review (acc/clean-2). In two answers the list holds something that is not a finer difference inside an
outcome: u3/clean-5 ("Beijing permitting purchases where no sale has yet been disclosed", a whole step) and u3/clean-9 (the finding,
which that thesis names).

**C7. The due day falls before the document the thesis names.** Six due days are 2027-01-31, given by the theses as the fiscal
year-end. Three of those theses name Nvidia's results or annual report as proof (u2/clean-3, u3/clean-5, u1/clean-11: "checked at its
next annual report/10-K"). The report that covers the last quarter of that year cannot exist on the due day. u1/clean-3's due day,
2026-12-31, falls inside a fiscal quarter.

### The weakest of the eight: u1/clean-11

It fails on every one of the five points. Its only accepted proof is an official Chinese decision or announcement, and its own article
shows the decision reaching firms privately and the public through a news site's unnamed sources (c). It removed the one proof that
would exist, Nvidia's reported revenue, which the thesis names twice (a). Its rule-out is a general ban, while its article describes
request-by-request approval, so a real "no" lands in "Neither", as the file's own line shows (b, d). And what is still open after the
article, how many chips and whether revenue follows, is under "not judged" (e).

Second: u1/clean-3, for one reason only, and a decisive one. Its condition is a fact that cannot be known on the due day, and its own
"->" line places an outcome by a fact the judge cannot have (c, d).

Third: the two French answers, because the likeliest real outcome by the due day (investigation ended, Nvidia charged) fits the words
of "Ruled out". This rests on my knowledge of French procedure, not on the files; it should be checked before it is acted on.

### Is three outcomes the wrong shape for any of them?

None of the eight is impossible to write in three outcomes. Three lose what the analyst holds the card for:

- **u1/clean-11.** The description asks "and roughly how many". A count cannot be an outcome unless the "happened" condition carries a
  threshold, and the thesis gives none beyond "potentially a total below 200,000". What the three outcomes do carry, whether any
  purchase is approved, is the part the article already reports. This is the clearest case of a wrong shape.
- **u3/clean-12.** The description's first words are "How far will the US crackdown ... escalate". Three outcomes carry "any binding
  restriction or none". The yes/no that follows the dash in the description does fit; the "how far" does not.
- **u3/clean-9.** "and by when?" is carried only as before or after the due day.

A fourth point is about the shape itself, not one thesis. Three outcomes assume a decider that says yes or no in public. For the three
H200 answers the decider is one that, on the evidence of the u1/clean-11 article, tells firms privately. There the "ruled out" rung is
close to unreachable, and the question behaves as two outcomes, "Nvidia disclosed sales" and "everything else".

The shape fits best where the decider publishes: acc/clean-2 and, once rung 2 is limited to a case that is over, the French pair.

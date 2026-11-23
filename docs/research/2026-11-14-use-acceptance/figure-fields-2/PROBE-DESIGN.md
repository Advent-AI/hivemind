# The figure fields, second version: empty unless the article says it. Probe design, version 2 (D497), 2026-11-15

**What it can decide.** Whether c22, which differs from the first arm (c21) only in the wording of the two field definitions, (1) leaves a
figure's source empty where the article states the figure in its own voice, (2) writes a fixed period only where the article writes that
year, (3) keeps the first arm's gain (the market's figure and the company's figure under their own names), (4) does not now empty a
source the article does state, and (5) leaves what the request decides today as it was. Read on ten stored states the first probe did
not use. A pass leads to the record test on unread articles, asked of Alex first; anything else stops the line and goes to him.

**Alex's word (D497):** "做第二版再测", on the option "把两个字段的定义改成“文章没明说就留空”，换另一批已存文章按同样的方法再测".

## Diagnosis first (the first arm's own stored reasoning, $0)

- *The unattributed outlook.* On "Gross margins are expected to bottom in the 71% to 72% range in Q4 …" the reasoning of all three sends
  calls it "gross margin guidance" at once and never asks whose expectation it is. Nothing in the first definitions named that case.
- *The year never written.* On an article that writes only "fiscal 2028", one send worked the quarter's year out from the publication
  date (which the definition forbade), two from "the next year (fiscal 2028)" ("so current fiscal year is 2027"). The first definition
  said "establishes", which a deduction satisfies.

## The candidate (`clean-arch/step1-unfiled-2026-11-08/arms/c22-*`)

System text and closing check: c8's, byte for byte. Schema: c21's two fields reworded, and the existing `kind` description clarified at
its owner (three descriptions in all; 7,254 → 7,911 characters as sent):
- `party`: the company is the source of its own reported result; of a forecast **only where the item says the company, its management or
  a named executive gave it**; the named person, firm or "consensus" for analysts' or the market's expectation; the author or outlet for
  its own calculation. "The item may state the source in another sentence than the figure's. null when the item does not state the
  figure's source anywhere ("margins are expected to fall", "earnings are projected at", with no one named in the item)."
  Source: the signed standard's rule that an unknown speaker stays unknown and an inference is not written as a source's statement
  (council mx round 8).
- `kind` (c8's wording was "guidance: the company's own outlook; estimate: a named party's or consensus forecast"): "guidance: the
  company's own outlook, where the item says the company, its management or an executive gave it; estimate: any other forecast: a named
  party's, the consensus, or one the item states without saying whose it is." The blind audit (`audit-c22-blind.md`) found that telling
  the model from inside `party` to call an unattributed forecast an estimate contradicted this field's own words; the clarification is
  made here, at the field, and it is the third description touched: disclosed, since Alex's option named two.
- `fiscal_period`: a fixed form "only when the item itself **writes the year** of this figure's period", in another sentence if need be
  ("for a quarter the item must say which quarter it is and tie it to that year"); the stated basis kept, fiscal or calendar; null when
  the item never writes that year, for a range or a deadline; never from the publication date or outside knowledge.
  A choice of wording within Alex's shape (a period in a fixed form): the strict form is the one code can check for presence, and an
  empty period costs a grouping while a wrong one corrupts it. It will leave empty some periods a reader could deduce; the first arm
  made 15 such deductions on other articles, a historical observation, not a measured loss of this arm.

## Cases (`cases-figure-fields-2.json`; stored c8 requests and states of the week, steps 13, 16, 33, 50, 55, 73, 98, 116, 231, 232)

| case | step | what the article holds | what must come out |
|---|---|---|---|
| u1-target | 231 | "The company's upcoming EPS is projected at $2.47"; "our latest consensus estimate expects the revenue to be $109.02 billion"; the full-year Zacks consensus; no fiscal year written anywhere | the EPS: empty, or the outlet's consensus, not the company, and not guidance; the two consensus figures: the market's; every fixed period empty |
| u2-target | 50 | "Nvidia is expected to have earnings per share of $15.68" for fiscal 2028 | empty or analysts, not the company; not guidance; FY2028 |
| m1-target | 232 | "Management guided revenue for that quarter to $108 billion"; "The consensus forecast for that quarter is $111.3 billion" | the guide the company's (not empty); the consensus the market's |
| m2-target | 16 | "the company projected 70% … in fiscal 2028 — well above the 45% analysts had expected"; margin "sliding under 72% by the fourth quarter" in analyst estimates compiled by Bloomberg | 70% the company's; 45% and the margin estimate the analysts'; "the fourth quarter" and "last quarter" empty |
| m3-target | 73 | "Revenue in the second quarter of fiscal 2027 … was $96.2 billion"; "the consensus revenue estimate of $109.0 billion" for the next report | the revenue the company's, FY2027-Q2; the estimate the market's |
| a1-control | 98 | "For fiscal 2028, management has guided about 70% revenue growth"; "the guide has that margin settling in the 72% to 73% range" | both the company's, **not empty** (the guard against emptying what is stated) |
| p1-target | 55 | the fiscal second quarter's results, "roughly 70% revenue growth in the next fiscal year", "the current quarter"; no fiscal year written anywhere | every fixed period empty; the parties the company's |
| p2-target | 13 | "latest quarter generated $89 billion of data-center revenue"; no fiscal year written | every fixed period empty |
| k1-keep | 116 | c8 opened the Hugging Face question here (stored draw) | |
| k2-keep | 33 | c8 opened the Blackwell China question here (stored draw) | |

Both arms (c8, c22) on all ten, three sends each: 60 sends; about $0.90 (dry run $0.86; the first probe cost $0.85); ceiling $2.00.
c21 is not sent again: its numbers on the first ten cases are the reference for what the rewording changes, on different articles.

## Who reads (as the first probe, with its lessons)

Two blind reader families on two packets, the article shown with its title and publisher. Packet one (both arms, one shape, no fixed
period): per figure the party (right / wrong / missing / unknown_ok), measure, value and kind; per statement its own party and date; the
named figures' places; the links of the statements with figures on the eight target and control cases. Packet two (c22 only): per
figure, whether the article writes the year of its period, and the fixed period right / wrong / empty. **Packets go to the Codex readers
in parts of ten answers.** Marks the families give differently are read again by a fresh reader of each family **for both arms**; a
line those could still change is undecided. **Beside the readers, a code check** on the period rule, which is mechanical: for every
fixed period c22 writes, the year in it must be written in the article with its fiscal or calendar marker; each failure is listed.

## Counting (frozen before any send; rates over an arm's valid sends of a case; "most" is two thirds)

- *Valid sends:* at least two of three per case and arm, or the case is left out for that arm and listed.
- **Named figures** (each case's list, with its accepted and rejected sources). A figure is *exercised* when either arm keeps it in at
  least two valid sends. *Retained:* c22 keeps it in no fewer sends than c8 less one (a figure c8 keeps in most sends and c22 in fewer
  than two fails). *Right:* over c22's sends that keep it, the readers mark its party right (or unknown_ok where the case accepts empty)
  in most; where the case says "not guidance", its kind is not guidance in most; where it says "guidance", its kind is guidance in
  most. A case passes when every exercised named figure is retained and right. **Line:** at least six of the eight target and control
  cases have an exercised figure and all of those pass but at most one; **a1-control must have both its figures exercised and pass**
  (a stated source is not emptied and its outlook is not relabelled).
- **Party, all figures:** c22's parties wrong in no more than one in twenty after settling; missing (empty though the article states the
  source) in no more than one in ten, counted apart.
- **Fixed period.**
  - *Readers (packet two), figure by figure:* does the article write the year of this figure's period and, for a quarter, say which
    quarter and tie it to that year. Where it does (needs ten such figures): c22's fixed period right in at least two thirds, wrong in
    no more than one in twenty. Where it does not: a fixed period written there is wrong.
  - *The year-unknown cases (u1, p1, p2: no fiscal year in the article):* each needs at least two figures kept in at least two sends, or
    it is not exercised; over the three pooled, fixed periods written in no more than one in twenty of their figures, and not in most
    sends of any one of them. This tolerance is the proposed line, stated as such.
  - *Code, beside the readers:* for each fixed period, whether its year is written in the article with its fiscal or calendar marker.
    Presence only: it cannot show the year belongs to the figure. Every fixed period that fails the code check, and every one the
    readers and the code check judge differently, is printed.
  - *Reported:* fixed periods left empty where the readers say the article writes the year (missing), and where a reader could deduce it.
- **Guards** (each fails the probe): openings on the keep cases (lower than c8's by two thirds in a case or by a half pooled; control
  absent when c8 opens in fewer than most; reported per case, never as "preserved"); kept statements, statements linked to an open
  question and figures per send, pooled, each not lower than c8's by more than a third; each statement-to-question link on the target and
  control cases not "most against none" between arms unless both families call the difference right; the statement's own party and
  date on the statements holding the named figures not wrong in more sends than c8's by two or more; measure and value wrong in no more
  than one in twenty; kind wrong after settling, read for both arms, in no more than one in twenty and not more than c8's rate plus
  one in twenty; invalid
  sends no more than c8's plus one.
- **The tally prints every line above with its verdict**; a line it cannot compute is reported as not computed, not as met.

**Verdict:** inconclusive = a required condition not exercised; undecided = a difference the fresh pair leaves that could change a line;
pass = every line met; fail = anything else. **Stop:** anything but a pass stops the line and goes to Alex with the listing.

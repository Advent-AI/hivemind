# Does a kept figure come out with the right source and period when it carries its own? Probe design, version 2 (D495), 2026-11-14

**What it can decide.** Whether c21, the adopted clean Step 1 request (c8) with two more fields on each figure of a kept statement (whose
figure it is; its period in a fixed form), gives each figure the right party in the statements where c8's one party per statement is
wrong for some figure, writes a fixed period only where the article establishes one, and leaves everything the request decides today as
it was (what is kept, what opens, what is linked, the figures' measure, value and kind). A pass leads to the record test on unread
articles (its design goes to the council then, its cost to Alex first); a failure stops the line and goes to Alex. It cannot show that
the record then passes its six-question test, nor any effect on a judgement.

**Alex's word (D495):** "开新版：每个数字自带来源", on the option "让每个数字自己带上来源和固定格式的期间（只加字段，不改开题和挂靠规则）。先在已存文章上测并守住现有行为，再用没看过的文章重做
记录测试". The shape is the one he approved on 2026-11-08 (`clean-arch/step1-unfiled-2026-11-08/LOG.md` §17: a kept figure "labelled actual,
guidance or expectation, with who said it and the period").

## The candidate (`clean-arch/step1-unfiled-2026-11-08/arms/c21-*`)

- System text and closing check: c8's, byte for byte. No sentence about keeping, opening or linking changes.
- Schema: each item of `figures` gains two required fields, defined beside the field (AGENTS §6):
  - `party`: "The source of this figure, which may differ from the statement's original_party. For the company's own reported result or
    its own guidance: the company (add an executive's name only where the item gives that figure as the executive's statement). For an
    estimate: the named person or firm, or "consensus" where the item gives it as analysts' or the market's expectation. For the item's
    own calculation or estimate: its author or outlet. Figures of one statement may share a source or have different ones; the statement
    stays one item. null when the item does not say whose figure it is."
  - `fiscal_period`: `FY2027`, `FY2027-Q3`, `CY2027`, `CY2027-Q2` or null (a pattern code checks): "The same period in fixed form, only when
    the item itself establishes it … A relative period ("last quarter", "next fiscal year") takes a fixed form only when the item itself
    names that quarter or year. null when no period is given, when the item does not establish the year or quarter, or when the period is
    not one year or one quarter (a range, or a deadline such as "by" a year). Never work one out from the publication date or from
    knowledge outside the item, and do not convert a calendar period into a fiscal one."
  The statement's own `original_party`, dates and every other field are unchanged. Schema 5,744 → 7,254 characters as sent (+1,510).
  Growth reason: two field definitions the record lacks (D494); nothing else can be cut for them without touching a rule.
- **Blind audit of the first wording** (`audit-c21-blind.md`): "whose figure" could be read as the figure's subject; its relation to the
  statement's party, the string for the company, an executive voicing the company's guidance, and the periods the form cannot hold (a
  range, a deadline, none) were not said. Each is now said in the field's own description; no rule about keeping, opening or linking is
  added. The format examples keep their digits (they show a form, not a company's number).
- **Why this is not the eleventh sentence:** it changes no rule the call applies; it asks for two more values per figure. It is still a
  change inside the one call, so every decision of that call is guarded below, with a same-day control on every case.
- A synthetic answer with the two fields passes the arm's schema and the runner's checks; the stored c8 answer fails the arm's schema (the
  fields are required) and a period outside the fixed form fails it.

## Cases (`cases-figure-fields.json`; the stored week's own c8 requests and states)

The reviewed probe (`clean-arch/e2e-comparison-2026-11-13/identity-probe/probe_identity.py`) unchanged; both arms on all ten cases, three
sends each: 60 sends; about $1.00 (the last probe of this size cost $1.02; the script's estimate is $0.86); ceiling $2.00.

| case | step | why | figures whose party must come out right (fixed now, from the article) |
|---|---|---|---|
| t1-target | 22 | the CFO's guide and the market's earlier expectation in one statement | the 45% is the market's (analysts, Wall Street, consensus), not the company's or the CFO's; the 70% is the company's or its CFO's |
| t2-target | 32 | the company's dividend and the author's arithmetic | the $25 billion a year and the 2,400% are the author's or the outlet's, not the company's; the $0.25 dividend is the company's |
| t3-target | 46 | the CEO's remark and a growth figure the article gives to no one | "can supply only 70% of demand" is the CEO's; the 70% fiscal-2028 growth is the company's or empty, not the CEO's |
| t4-target | 121 | the CFO's outlook and the reported margin (the record test's error) | the 75% is the company's or empty, not the CFO's; the 72%–73% is the CFO's or the company's |
| t5-target | 201 | the reported quarter and the consensus it beat | the $92.37 billion is Wall Street's (analysts, consensus), not the company's; the $96.22 billion is the company's |
| c1-control | 37 | thirteen figures of the company's quarter, one party | every party the company |
| c2-control | 115 | the company's margin guide and reported margin | every party the company |
| k1-keep | 35 | c8 opens the Vera Rubin question here (2 of 3 in the last probe) | |
| k2-keep | 42 | c8 opened the hyperscaler-spending question here (stored draw) | |
| k3-keep | 169 | c8 opened the RTX Pro 5500 approval question here (stored draw) | |

## Who reads

Claude reads every answer and keeps the listing. Two blind reader families (Codex, a Claude subagent) read two packets, each answer
beside its article **with the item's title and publisher as the model saw them**:
- **Packet one, both arms under shuffled labels, one shape:** every kept statement that holds figures, with its statement-level party
  and date, and every figure with its measure, stored period, value, kind, basis and one `party` (for c21 the figure's own; for c8 the
  statement's party, repeated on each of its figures: what a record built from c8 shows). No fixed period appears in this packet, so
  nothing in its form tells the arms apart; where an answer gives the figures of one statement different parties, that is the thing
  under test and the readers are not told what the two versions are. The readers mark, per figure: `party` right / wrong / missing (empty
  though the article says whose it is) / unknown_ok (empty and the article does not say); `measure`, `value`, `kind` right or wrong;
  per statement: the statement's own party and date, with the same four marks; and, for a target case, where each named figure is among
  the kept figures, or that it is not kept. For the seven target and control cases the packet also gives the questions open when the
  article was read and, for each kept statement with figures, every link it has (the question, and the answer's reason for the link), or
  says that it has none; the readers mark each such link supported or unsupported by the article and the question.
- **Packet two, c21's answers only** (no comparison of arms is read from it): every figure with its stored period and its fixed period.
  The readers mark, per figure: `established`, yes only when the article itself supports a period the fixed form can hold in full (a
  fiscal or calendar year; a quarter together with its year), and no for a quarter with no year, a relative period the article does not
  pin down, a range, a deadline or no period (for those the right fixed period is empty); and the fixed period right / wrong / empty.
Counts are taken on marks the two families agree on; a mark they give differently is listed, and when it could change a line it is
settled against the article by a fresh reader of each family; if those differ too, the line is undecided.

## Counting (frozen before any send; rates are over an arm's valid sends of a case; "most" is two thirds)

- *Valid sends:* at least two of three per case and arm, or the case is left out for that arm, of pooled counts too, and listed.
- **Party (the target).** For each named figure:
  - *kept:* c21 keeps it in at least two valid sends, and in no fewer sends than c8 less one; a figure c8 keeps in most sends and c21
    in fewer than two fails; a figure c8 itself keeps in fewer than two is not exercised;
  - *right:* over the sends where c21 keeps it, its party is right (or unknown_ok where the case allows empty) in most.
  A target case passes when every exercised named figure is kept and right; a case with no exercised figure is not exercised. **Line:**
  at least four target cases exercised and at least four pass; and over all figures of all ten cases, c21's parties wrong in no more
  than one in twenty (missing counted apart and reported). *Room:* by the same marks, c8 must fail at least three of the five target
  cases, or the probe has no room and cannot pass.
- **Fixed period** (packet two; marks both families agree on). *Established figures* (as defined for the readers above: a period the fixed form can hold in full): c21's fixed
  period right in at least two thirds of them and wrong in no more than one in twenty. *Not established:* empty in at least two thirds
  of them; a fixed period written there is wrong. The line needs at least ten established figures and at least five not established;
  with fewer of either, that half is not exercised and the line cannot pass. Reported: the share of the same figures whose stored period
  in c8 is relative or empty.
- **Guards on what the request decides today (each fails the probe):**
  - *Openings:* on a keep case, c21's rate of opening the stored question lower than c8's by two thirds or more, or by a half or more over
    the exercised keep cases pooled. A keep case where c8 itself opens it in fewer than most sends is control absent; with all three
    absent the guard is not exercised and the probe cannot pass. On any case, a question one arm opens in most sends and the other in
    none counts, in either direction. Per-case counts are reported; a guard that does not fire is reported as "no difference seen at
    three sends", never as openings preserved.
  - *Kept and filed:* over the cases pooled, c21's kept statements per send, its statements linked to an open question per send and its
    figures per send each not lower than c8's by more than a third. And, statement by statement on the seven target and control cases:
    a link from the case's stored statement to an open question that one arm gives in most sends and the other in none is listed with
    both answers and read by the two families against the article; c21 losing a link both call supported, or adding one both call
    unsupported, fails.
  - *The statement's own fields:* on the seven target and control statements, c21's statement-level party or date wrong in more sends
    than c8's by two or more over the seven pooled fails (the new fields must not disturb the old ones).
  - *Figures' old fields:* c21's measure, value or kind wrong in no more than one in twenty figures, and not more than c8's rate plus
    one in twenty; an arm with no figures in the cases is not exercised.
  - *Format:* c21's sends that end invalid no more than c8's plus one.
- *Reported:* tokens and cost per send by arm; every party c21 leaves empty; how c21 writes one source across sends ("consensus", "Wall
  Street", "analysts"), since a record that groups by party will meet those spellings.

**Verdict:** inconclusive = a target, period or guard condition not exercised, or no room; undecided = a reader difference that could
change a line and that the fresh pair does not settle; pass = party, fixed period and every guard met; fail = anything else. A pass
says what was seen on ten stored states at three sends; it is not a proof that nothing else moved.
**Stop:** a fail, an inconclusive or an undecided result stops the line and goes to Alex with the listing; nothing is tuned on these cases.

## After a pass (designed then, not now)

The record test of `../record/RECORD-TEST-DESIGN.md` on articles no arm has read (the second fresh week, 2026-09-29..10-05), with the
comparison's gaps closed (the questions' wording shown to the comparers; "each pair" scoped to revenue and margin) and the publisher in
every reader's packet. Sending c21 on those articles costs about $0.02 an article; the number and the budget go to Alex first.

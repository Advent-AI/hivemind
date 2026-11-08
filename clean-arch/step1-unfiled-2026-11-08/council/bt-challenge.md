Follow-up on c10, read-only. I took your asks: the model's own account, the request read in full, and the separate mechanisms.

**Model's own account.** Six questions in the stored conversations: `poc/data/clean-step1-unfiled-2026-11-08/probe-r14-c10/thesis-account.json`
(script `thesis_account.py`, asks `council/bs-asks.json`, $0.025). The assistant turn is re-serialised from the parsed answer, since
the probe keeps no raw text.
- **The small stakes:**
  - fresh-47 c10a, fresh-50 c10a and fresh-50 c10b all quote the read-back. Each sizes the deal against clean-7's $25bn total
    ("roughly a tenth", "roughly 8% added") and against the $12.9bn Hugging Face deal in the open list. None compares it with
    revenue, profit, cash or credit, though fresh-47's article gives $96.2bn of quarterly revenue.
  - The control, fresh-47 c10b, which opened nothing, also judged the stake "large enough" against the $25bn. It held back only
    because the report is single-sourced and hedged. So the scale test failed in 4 of 4 answers, and the one pass came for another
    reason.
- **fresh-9 c10b:** "agreed to provide guarantees … reports no definitive signed guarantee documents, so I treated it as unsigned".
  The signed standard's split is 已经承担 (undertaken: amount) against 还没签 (not yet signed: yes/no). c10b's field and the
  read-back say "has not yet signed", which invites the documentary reading. c10a's fresh-9 answer opened the amount question,
  which is right.
- **fresh-12 c10a:** it cites §3 policy_stage directly and calls itself "the weakest part of my answer". It does not cite the
  read-back. I read it as c8's own boundary, one draw, not this lever.

**The request against the standard.** The signed standard, D248 boundary 6: "单笔交易、产品、项目，规模要大到能改变公司的收入、利润、现金或信用风险才开题；够不上的不开题".
c8 §3 carries it ("large enough to change its revenue, profit, cash or credit risk"). The read-back says only "when its scale meets
section 3", and frames the case as "beside an open total of its kind", so the total becomes the yardstick.

**Census on c8's own stored runs** (fresh plus dev ×3, 395 answers):
- the obligation theses opened are totals, plus one single deal, Hugging Face at $12.9bn, which readers judged open;
- no small single stake was opened.

So under c8 the duplicate check masks the scale test whenever a total is open. The read-back's override removes the mask and exposes
it.

**Empty answer:** 1 of 135 probe sends (dev-4, c10b). c8's 86 empty answers of 395 are all articles with nothing kept.

**The one recommendation I would take to Alex:**
- keep c10a;
- in the read-back, replace "when its scale meets section 3" with D248 boundary 6's yardstick: "when it is large enough to change the
  company's own revenue, profit, cash or credit risk (section 3), judged against those and not against the total of its kind or
  another deal";
- in the subject, write "not yet undertaken" to match §3's own word.

That is one definitional change, sourced verbatim. The test: the same 32 cases plus Ohio ×3. Falsifiers:
- Ohio below 2/3;
- fresh-47 or fresh-50 opens;
- any new thesis a blind reader judges wrong, with arms in separate packets this time;
- fresh-8 loses its thesis;
- links per item move more than 10%.

Challenge under 250 words:
1. Is the yardstick mechanism now supported?
2. Is this a sentence-level rule of the kind c9 showed flips by send, or a definition the model lacked?
3. Is there a counterexample in the 32 cases it could break, such as Ohio's unknown guarantee amount?

End with AGREE, AGREE WITH CHANGES, or DISAGREE.

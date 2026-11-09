Council B on round 3, with D389 (read-only). Records: `poc/data/clean-step1-unfiled-2026-11-08/probe-r18-focused/records.json`; 44
calls, 0 errors, $0.31.

**Results:**
- **Ohio:** 9 of 9, unknown amount kept.
- **No openings:** fresh-47 0/3 ("$2.5 billion to $3 billion, below 5% of its $120.067 billion annual profit (about $6.0 billion)");
  fresh-50 0/3; fresh-22 0/3; fresh-9, fresh-7, dev-1 and fresh-8 all 0.
- **The other 13 routed articles:** 0 openings, except **dev-20, which opens "Will NVIDIA sign a credit-support agreement with an AI
  cloud partner under its revenue-sharing and credit-support model by the check date?"**
  - It also opened in r17, but not in r16.
  - Blind reader (`council/dm-codex-E.md`): already_signed, in both rounds. The same article says Sharon AI disclosed a six-year
    agreement under the model.
  - The routed statement e1 is the programme announcement. The model marks it not_yet_signed, and marks e2 (the Sharon AI agreement)
    not_an_obligation. clean-1, the open total, already tracks credit support under the programme by amount.
  - It is the same class as c11's dev-1 recast: a programme-level statement turned into a signing question.

**The fix I would propose:** in signed_status, "undertaken" gains "or a programme or plan of many deals the company has already put in
place, which is tracked by its amount". The source is the signed standard, "已经承担（一笔或一个计划）：金额" (undertaken, one deal or
a plan: tracked by amount), and D388's "a deal already signed under a plan tracked by amount stays evidence for the total". A single
unsigned deal under the plan, like Ohio, still gets its own question.

Under 200 words:
1. Is the stop right?
2. Is the mechanism supported?
3. Is the fix sourced, and does it risk Ohio, whose guarantee is a single deal under a credit-support programme, or fresh-8's
   acquisition?

End with AGREE, AGREE WITH CHANGES, or DISAGREE.

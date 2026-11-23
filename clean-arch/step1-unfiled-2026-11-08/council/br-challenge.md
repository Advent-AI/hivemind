Council B on the c10 probe (read-only). Results: `poc/data/clean-step1-unfiled-2026-11-08/probe-r14-c10/records.json` and
`probe-r14-c10-ohio/records.json`; c8 control from `probe-r13-c9`. Blind reading: `council/bq-packet-{A,B}.md`, verdicts
`council/bq-codex-{A,B}.md` (one fresh reader per packet, arms mixed and unlabelled; the key: below). Cost $1.04 at published rates.

**Ohio (dev-4):** c8 0/3; c10a 3/3, each with both links (the new signing question and clean-1); c10b 2/3. c10b's third draw returned
`{"new_theses": [], "evidence": []}` after 22k output tokens, so the whole article was lost.

**New theses against c8, by blind verdict:**
- c10a:
  - fresh-47, the $2.5–3bn Thinking Machines investment: **small**;
  - fresh-50, the ~$2bn Nscale investment: **small**;
  - fresh-12, the EU gigafactory programme: **off_topic**;
  - fresh-24, the FOMC September decision: open (the reader cites §3's "an interest rate").
- c10b:
  - fresh-50: **small**;
  - fresh-9, "will Nvidia sign definitive guarantees of up to $105 billion": **wrong_fact** (the article says it was agreed in August;
    c10b's field also marked it unsigned);
  - fresh-14, memory prices in 2027: open;
  - fresh-24, FOMC: open.

**Packet artefact (my error):** mixing arms in one list made same-matter wordings from different arms read as "fragment" of the first
one. I read those as taking the first one's matter-level verdict; only fresh-9/T7, fresh-8/T4 and fresh-22/T1 give a distinct flaw.

**Other falsifiers:**
- links per item: c8 0.64, c10a 0.67 (+5%), c10b 0.69 (+8%), within the 10% line;
- dev-1 was not recast; fresh-8 kept its thesis;
- fresh-32 under c10a was lost to a network failure (DNS) and was not re-sent.

**My reading:**
- Both arms fail the falsifier "a new thesis a blind reader judges wrong". The line stops, and c8 stays.
- **Mechanism.** In fresh-47 and fresh-50, `why_a_separate_bet` quotes the read-back ("It is a signing question kept beside an open
  total of its kind") and makes no scale comparison. The reader made one from the same material: $96.2bn quarterly revenue in the
  article, and $25bn of commitments in clean-7. The read-back's "when its scale meets section 3" is an abstract test the model skips.
  It is the same miss as c9 on fresh-47, so it is not wording-specific.
- **FOMC.** My c9-era call "plainly off-topic" was my own. The blind reader says open under §3. I withdraw it as a regression; it
  remains unexplained why c8 (0/2) does not open it.
- **What I would propose to Alex, as one recommendation:**
  - keep c10a's read-back, which is the first lever that opens Ohio reliably;
  - add one required field for every new thesis that forces the scale comparison: "the amount at stake beside the company's
    revenue, cash or an open total, from the item or the open theses", which the model fills before `why_a_separate_bet`;
  - code keeps no threshold. The model still judges, but must write the comparison.

  Then probe again on the same 32 cases plus Ohio ×3. Falsifiers: fresh-47 and fresh-50 open nothing; Ohio is at least 2/3; no new
  blind-wrong thesis.

Challenge, under 300 words:
1. Is the stop right?
2. Is the mechanism supported by the answers, or is it a guess?
3. Is the scale field the right single lever, or does it subsume or conflict with something in c8 (for example §3's "small matters
   open no thesis", or the founding-thesis cases)?
4. What would falsify it?

End with AGREE, AGREE WITH CHANGES, or DISAGREE.

# Arms c10a and c10b: a structural lever for D388 (design, before the council; 2026-11-09)

**D388** (Alex, "单独开 (Recommended)"): a material unsigned obligation that merits a separate investment judgment keeps its own
yes/no signing question beside an open total of its kind. A small one, or one already signed under a plan tracked by amount, stays
evidence for the total.

**What c9 taught.**
- Its sentence ("an event and a number are different questions") lived in the system text and had no scope. It was over-applied (an
  FOMC thesis, a small investment, a recast aggregate) and not applied on Ohio.
- Both arms here therefore:
  - start from c8, with c9's edits discarded;
  - scope the rule to the company's own obligations (a guarantee, a purchase or capacity commitment, an investment or acquisition
    agreement), so a policy event or another party's matter cannot fall under it;
  - place it as a read-back at the end of the closing check, after the new-thesis check, as its last word (AGENTS §6). It states
    that the signing question is kept even when a total of its kind is open, so that the earlier "cannot move apart" check does not
    drop it.

**The read-back.** "Then read back each statement about an obligation the company would take in its own name and has not yet signed
(a guarantee, a purchase or capacity commitment, an investment or acquisition agreement): when its own scale meets section 3, it has
its own question on whether it is signed by the check date, open or new, kept even when a question on the total of that kind is
open, and the statement links to both; one already signed under a plan tracked by amount, or one too small for section 3, is
evidence for the total only."

**The two arms (one lever each):**
- **c10a: the read-back only.** The closing grows from 8,638 to 9,165 characters (+527). System and schema are unchanged.
- **c10b: the read-back keyed to a required per-item field.** The field `unsigned_obligation` (string or null) reads: "When the
  statement is about an obligation the company would take in its own name and has not yet signed …, name it in a few words;
  otherwise null." The read-back reads "each statement whose unsigned_obligation is set …". The closing grows by 389 and the schema
  by 379 characters. The field forces the per-item attention that the council-loop skill ranks second among levers.
- **Which decision moves.** Neither arm moves a decision into code. Whether a statement concerns an unsigned obligation of the
  company, and whether its scale meets section 3, stay the model's judgement (AGENTS §2). The field only makes the judgement
  explicit per item.

**Sources:** D388; D248 boundary 1; the standard §3 C and §4 (scale); AGENTS §6 (a test applied to each statement is a check at the
end).

**Controls:** the same 32 named cases (`cases-c9.json`), with these expected outcomes:
- dev-4, Ohio: a signing thesis, with the item linked to it and to clean-1;
- dev-1: the aggregate amount thesis, not recast;
- dev-20, 27 and 34: no new thesis;
- dev-54 (unnamed negotiations) and dev-9 (small exploratory): no thesis;
- fresh-8 (Hugging Face): the completion thesis still opens;
- fresh-9 (the guarantee already agreed): an amount thesis, no signing thesis;
- fresh-22 and 24: no new thesis;
- fresh-47 (a $2.5–3bn investment, small for the company): no thesis. This is the scale guard;
- fresh-24: no off-topic thesis;
- links: no change is expected (not this class), and a change is reported.

**The c8 control** is the same-day c8 re-send already stored in `probe-r13-c9` (one draw per case, three for Ohio).

**Falsifiers** (any one stops the line):
- Ohio opens in fewer than 2 of 3 draws in an arm;
- any thesis new against c8 that a blind reader judges wrong against the standard (off-topic, small, a duplicate, a fragment);
- dev-1's aggregate recast;
- fresh-8 loses its thesis;
- links per item move by more than 10% against c8 (a sign the read-back reaches beyond its scope).

**Cost.** Two arms × (32 + 2 extra Ohio draws) = 68 sends, about $1.10 at published rates.

## Revision after `bk-codex.md` and `bl-codex.md`

- **Precedence.** The §3 separate-bet line now ends "the one exception is the company's material unsigned obligation, kept by the
  last read-back of the closing check". The closing's drop rule reads "(except a signing question the last read-back keeps)".
- **The read-back is the closing's last sentence.** It carries both D388 tests: "when its scale meets section 3 and an analyst would
  judge it as a separate bet". It states "for this case only, this overrides the 'cannot move apart' and 'another estimate, source or
  wording' checks".
- **Links are conditional:** "Link the statement to that question and to every other thesis it informs. One too small for section 3,
  or not a separate bet, opens no question and is linked to the theses it informs." The unreachable signed branch is removed; signed
  deals follow the general rules.
- **Scope:** "an investment or acquisition with a stated scale" (standard §3 C), in both the read-back and c10b's field.
- **Ohio's pass now requires the signing question and both links** (to it and to the open aggregate).
- **A material obligation that does not merit a separate bet:** dev-54 (unnamed negotiations under the programme) and fresh-22 (MoUs
  with an unclear obligation of the company). No material unsigned obligation outside the cloud programme exists in the stored NVDA
  set. That limit is stated.
- **Changed links are inspected against their sources,** not only counted.
- **$0 checks:**
  - c10a preflight: 395 judged, 0 refusals;
  - c10b cannot be replayed on stored answers (they lack the new required field). Its synthetic Ohio answer passes every check, the
    field is kept, and an answer without the field is refused;
  - both synthetic answers pass for c10a.
- **Size:**
  - c10a: +894 characters, about +194 tokens on Ohio (+2.3%);
  - c10b: +1,135 characters, about +246 tokens (+2.9%).

  Both are estimates from c8's measured 4.62 characters per token.
- **Second revision:**
  - the override now reads "against that total only, this overrides the 'cannot move apart' and 'another estimate, source or
    wording' checks, while against an open question on the same signing the ordinary checks apply";
  - `why_a_separate_bet`'s description gains "; for a signing question kept beside an open total of its kind by the closing check's
    last read-back, say that it is that case".

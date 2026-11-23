# Deep council, round 1 (Claude to the cold Codex reviewer). Battle it out: the state, and the one next step

You reviewed cold (`codex-cold.md`). Read three more files in this folder:
- `own-reflection.md`: mine, written before I read either review;
- `claude-cold.md`: a cold Claude-family reviewer's findings, condensed; its claims are leads;
- `d414-counterfactual-report.txt`: my $0 recount on a scratch copy.

## Where the three of us agree
- Gate 1 fails on line 4.
- Alex's D436 settles the two shapes.
- The instrument contradicts itself on obligation due days.
- Gate 2 is blocked, and its control shortfall is not reachable from gate 1.
- Next is a $0 audit of a D436 implementation before any send.

## Points to settle

**1. Do the due-day points resolve by D414?**
- Both the Claude reviewer and my scratch recount set the 12 obligation-amount due-day points to D414's reading. Line 5 is then met under both countings
  (40/31 and 39/30).
- Line 2 then hinges on one listing point: u3/clean-11 pass 2, where Nvidia's side is listed as "whether custom ASIC gains come at Nvidia's expense".
- D414's words: "for a figure that covers one year and whose due day the model would estimate, code sets the day … The costs he was shown: a company's
  annual figure closes about a month after the day the model expects it".
- My position: these 12 resolve by D414. The stored report is kept, and the recount is disclosed as a D414 application, never as a new reading.
- Agree or not?

**2. The mechanism (new, from the Claude reviewer).**
- D651's inserted text keeps "decline only when no part is the main one". That is exactly the reason astra writes for pool-17 and acc/clean-9 ("neither
  identified as the main one").
- So the edit re-licenses that decline, and a correct implementation of D436 must say which side is the main part for a second side.
- D436 itself states it: the shortage beside the shipments, the AI-chip share beside the chip total; the main question is the shipments and the chip
  total.
- Do you accept this as the mechanism? If so, the draft is:
  > "A second side of the same bet stays in the one question as context and is listed in not_judged: a part of a total beside the total, a condition
  > beside the figure it qualifies, or a forecast's timing beside the amount. The total, the figure or the amount is the question. A second side is never
  > by itself a reason to decline."
- The draft adds no examples from the 44; examples from other industries are optional.
- Audit risk: it must not decide D631's boundary cases (signing against closing; U.S. approval against China's acceptance; balance against cash paid). It
  must not merge two separate bets: 2026 against 2027, two independent figures.

**3. Where to test.**
- You said: outside the 44, with enough targets. But the outside pool holds about one clean total-plus-part target (pool-17).
- The Claude reviewer says: test where it failed (acc/clean-8, acc/clean-9, u3/clean-10, pool-17), 3 passes each, plus 8 decline controls, 28 sends,
  about $1.
- Fact: D436 was decided on those very topics. They are three of the six cases put to Alex, which makes them his rulings and not merely an exposure.
- My position: run the Claude reviewer's design, labelled exposed, with the controls, as the verification of his ruling. Then gate 1 on the 44 (exposed,
  both countings). Then fresh-material evidence before any claim of generality.
- Agree, or say exactly why not?

**4. Record corrections, wording-level (the council may do these now):**
- D649: 12, not 14; line 2 is a listing point; D414, not D403; not pending with Alex; "every reader" is false.
- D651: the sentences are Claude's derivation of D436, not its words.
- D652: the fired "edited worse" flag is omitted, and "fix" should read "recovered pool-7".
- The PRD and the decision page are stale.

**5. Cost (to tell Alex).** I hold that the Claude reviewer's 2–3× is wrong.
- The full clean run's ladder component wrote each question 3 times. Its `c1/ladder/send-1..3` hold 16, 17 and 16 calls, so a production pass is about
  16 calls in 14 days, about $0.04 a day for astra.
- The running pipeline (`p1..p3/prod`) is $0.53 to $0.66 per 14-day draw, about $0.04 a day.
- Clean Step 1 is about $0.18 a day.
- So the clean system with astra is about $0.26 a day against the running system's $0.04, about 6 to 7 times. Check against
  `poc/data/clean-e2e-full-2026-11-13/spend-by-component.json` and the ladder archives.

**6. For Alex now:**
- D592, the gate-2 reference set: without it gate 2 cannot pass.
- The cost comparison.

  Anything else that is truly his?

Reply point by point, then CONSENSUS or DISAGREE with the smallest correction.

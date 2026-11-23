# Does one unsupported revision relation change a judgement? Protocol

2026-11-10. Written before any send. This carries out the one bounded test the council of 2026-11-09 recommended
(`reports/step2-after-failed-probe-council-2026-11-09/CONCLUSIONS.md`); Alex handed the Step 2 work over with that conclusion on
2026-11-10. Nothing here changes Jev, a prompt, a rule, the frozen judge or any saved run.

## The case

Saved D392 clean draw 1 (`poc/data/clean-e2e-2026-11-09/stage2-clean-d1`, judged by the frozen judge through the experimental adapter
`clean-arch/e2e-2026-11-09/adapter.py`).

- Record `70:e4` (evidence `e185`): an NVIDIA spokesperson answers a report that the Kyber rack is delayed: "Our roadmap is intact."
  Step 1 filed it under the Kyber shipping question (v18) only.
- Jev read it as a later version of `69:e5` (evidence `e181`), a different statement: NVIDIA plans to sell more racks of the existing
  form. Two source readers called the two statements different (case C036 and the census of 2026-11-09).
- The adapter gives a record every question link of the record it revises, so `e185` also entered v20, "How much revenue will NVIDIA
  report from Blackwell and Rubin products in FY2027?".

## Stage 1, no cost: done

`edge_replay.py`, every judge request answered from the saved archive, none sent.

1. **Untouched control: passed.** 239 of 239 requests equal a saved request in the archive's form (sorted keys) and took its saved
   answer; every saved row was used. Equal to the saved run's: the 23 ledger tables the adapter and the judge write (less
   `judgements.call_id`, an archive row number given in the order answers return), the recorded judge requests (day, sequence
   number, question, evidence ids shown) and the adapter counts. Not compared: the two search-index tables and `sqlite_sequence`;
   the saved responses' metadata beyond the answer.
2. **One relation removed** (`70:e4` → group `69:e5`, in a stamped copy of the library): the rounds of 2026-07-01 to 07-05 are
   identical. In the round of 2026-07-06, v20's request differs: the `e185` block (4 lines) is gone and the item count reads 28 for
   29; the 14 other requests of that level are identical. The replay stops at that request, so the rest of the round (v16, v19 and
   the re-send of v17, which the control sent afterwards) is not built and nothing is known of it.
3. **The relation removed, its link kept:** all 14 rounds identical to the control. For this relation, the judge's input changes
   only through the link it carried, not through the "later version" line (which names another piece, `e131`, the relation written
   last). This is shown for this one relation, not as a general rule.
4. **The class, counted on the saved ledger** (`inheritance_census.py`): 5 of 700 links exist only because a revision relation carried
   them (3 records, 4 questions). By the readers' label of the carrying relation: 2 different statements (`e185` into v20, `e324`
   into v7), 1 uncertain (`e185` into v7), 2 repeats (`e173` into v2 and v4).
5. Step 1 itself never filed the "roadmap is intact" statement under v20: 0 of 28 copies in the three saved draws (v18 26, v7 12).

## Stage 2, paid: one judgement, two inputs

- **Requests:** v20 on 2026-07-06 as the saved run asked it (control), and as the same code builds it with the relation removed
  (counterfactual). `judge_probe.py check` proves, with no send: the control equals the saved request in the archive's form and is,
  byte for byte as serialized for sending, what `model.build_request` builds today; the two differ only by the `e185` block and the
  item count; the frozen check accepts the saved answer on the control and refuses it on the counterfactual (it cites `e185`).
- **Limit on "the same bytes".** The archive keeps a request only with sorted keys, so the bytes sent on 2026-11-09 cannot be read
  back. What stands in for them: the files that build and serialize the request (`src/hivemind/model.py`, `views/judging.py`,
  `views/store.py`, `config.py`, `poc/config/poc-v108.json`) were last written before that run (2026-11-08 13:43 at the latest; the
  run's calls are 2026-11-09 04:05 to 04:52) and have no uncommitted change, so the key order is consistent with the one that code
  produced then; a file changed and restored in between would not show.
  Headers and the credential are not saved and not compared. After the send, each answer's key order is compared with the saved
  answer's.
- **Sends:** 3 per arm, the arms interleaved and sent at once, through the production transport, no archive, no automatic re-send by
  the script beyond production's own retry of a failed connection. Model and settings: the frozen judge's (`poc-v108`).
- **Cost:** $0.0665 if every send answers at its first attempt, priced at its reserve (every character an input token, the whole
  output cap); $0.1994 if every send is tried three times, the most the spending limit's retry rule allows; cap $0.25 for the one
  invocation. Expected about $0.03.
- **Preflight** (`preflight.log`, no cost): over the saved judging archive and ledger, the schema's 43 enum values are all named in
  the prompt, and the 10 stored rows marked refused are the 10 answers the judge's check refused in the saved run. Its extraction
  and matching checks have no case here (the archive holds judgements only, and this probe sends neither), so it exits "unexercised"
  for those two. The judge's own check ran over all 239 stored answers in the control replay: 229 accepted and 10 refused, as saved.
- **Why the control arm:** the saved answer is one draw. It moved v20 from rung 3 to rung 2 on this very day, with an implied figure
  of about $330 billion against the $320 billion boundary, so the judge's own spread at this boundary must be seen beside the
  counterfactual.

## Reviews before the send

Four read-only Codex reviews, each by a new session (`council/sender-review-*.md`), and one blind reading of the article
(`council/relevance-codex.md`). None ended "ready"; each serious finding and what was done:

| Round | Serious finding | Done |
|---|---|---|
| 1 | The archive cannot prove the bytes sent on 2026-11-09 | Stated as a limit, with what stands in for it (above) |
| 1 | "The round differs in one request" although the replay stops there | Reworded: v20's request differs, the rest of the round is not built |
| 1 | No minimum of accepted answers; a mixed result called the judge's spread; one sentence widened to the class | Rule rewritten and computed by `verdict()` |
| 2 | The reader could stop on an answer the schema refuses | Closed with the rule of round 3 |
| 2 | The worst cost left out the retries | Stated: $0.1994 with three attempts a send |
| 2 | No preflight record | Run, with its limits (above) |
| 3 | The reader could stop on an unexpected shape of the token counts | One rule: an outcome the reader cannot read is "unreadable" and not counted |
| 4 | An answer could be lost if the accounting failed after it returned | The sender writes every returned body to disk before the accounting reads it; shown in a dry run with a fake transport |
| 4 | The cap holds only while reported tokens stay within the reserve | Not changed: the reserve prices every request byte as an input token and the whole output cap, which a real answer cannot exceed; it is the shared limiter of the D392 runs (`e2e-2026-11-09/budget.py`), outside this probe |

The send goes out on my reading that these are closed, not on a reviewer's clearance. The blind reader, shown the article and the
revenue question and not the relation, placed the statement as (b): context that should not move the FY2027 estimate.

## Reading rule, fixed now

Each answer goes through the frozen judge's own check; a refused or failed answer is reported and not counted, and not re-sent.
`judge_probe.py read` prints the verdict by this rule.

- **Not decided** unless all three answers of each arm are accepted.
- **The conclusion differs in these samples** only if the three counterfactual answers are on one rung and the three control
  answers on another.
- **No difference in the conclusion in these samples** only if the six answers are on one rung.
- **Anything else: not decided by this probe.** Three answers an arm cannot say whether a mixed result is the judge's own spread or
  the removed record.
- Read and reported, not scored: the implied figure, the stated reasons and why_changed, and in the control arm whether `e185` is
  cited, how it is pushed and whether the reasons use it.

## What each outcome means for the next step

The size of the class comes from the count, not from this probe: links that exist only through a revision relation are 5 of 700
in draw 1, and 11 of 725 and 8 of 730 in draws 2 and 3 (relations of every kind, right or wrong; the readers labelled draw 1 only).

- No difference: removing this one record did not move this conclusion on this day in these samples. It says nothing of the other
  relations. With the count, the recommendation to Alex is to keep Jev's revision relation as a recorded defect and not spend the
  next round on it.
- The conclusion differs: this judgement is sensitive to this one record in these samples; it does not prove the relation caused
  the saved draw's conclusion. The lever would be the rule that a revision carries question links, which is a product rule and
  Alex's to decide; it is not a reason to resume wording changes to Jev.
- Either way it is one case and one day of one draw: it shows sensitivity or its absence here, not how often it happens.

## Not claimed

That removing the relation is more accurate (the record could bear on v20 on its own; an independent reader is asked, blind to the
relation); anything about the days after 2026-07-06 (later rounds would rest on answers the archive does not hold); anything about
the clean Step 4, which is not built; overall Step 2 precision or recall.

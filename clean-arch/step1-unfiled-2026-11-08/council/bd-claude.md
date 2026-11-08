# Arm c9: one clarification of "covers" (design, before the council; 2026-11-09)

Alex approved designing it through the council process: "做，按评审流程 (Recommended)". The diagnosis is in round log §48 and
`bc-codex.md`.

## The change (files `arms/c9-*`)

**Census.** c8 uses "cover" 13 times:
- 10 in the link sense (is this statement evidence for that thesis);
- 3 in the open sense (does an open thesis already ask this question);
- the rest are unrelated (a row's "it does not cover", a period "covers").

**Edits.** c9 replaces:
- the link sense with "informs", defined once at the top of §2, from standard §5.1: "A statement informs a thesis when it makes that
  thesis's answer more or less likely, or bears on a condition that decides it: a contrary fact, the forecast, plan or announcement
  the thesis tracks or was opened on, and a signal the item ties to the thesis's outcome all inform it. Sharing the thesis's company,
  product or topic alone does not."
- the open sense with "already asks". It illustrates D248's move-apart test with a domain unlike the case: "A question on the total
  of a kind does not already ask whether one named instance of that kind happens: the total can change without it, and it can
  happen while the total falls (a carmaker's total recall costs this year do not ask whether its regulator orders a recall of its
  best-selling model by year-end). The named instance is its own thesis only when its own scale meets section 3 and an analyst would
  bet on it separately; otherwise it is evidence for the total."

Both D248 tests are kept: the answers move apart, and an analyst bets separately. The scale test (§3) is kept.

**Size.** System 15,828 → 16,663 (+835), closing +6, schema +2. The reason is the two definitions the measured failures lacked; no
redundant text was found to cut (the "match by underlying question" line is the matching rule both senses use).

**Sources.** The standard §5.1 (evidence makes an answer more or less likely), §3 C, §4; D248 boundary 1 (one bet, move apart, bet
separately); D383; AGENTS §8 (indirect, incomplete and forecast information is evidence).

## Controls, named before any send (expected outcomes)

Arms c8 (a same-day control) and c9, re-sent on the stored requests with the stored before-states. Dev cases use draw 1's stored
state; fresh cases use the acceptance run's.

| Case | Situation | Expected under c9 |
|---|---|---|
| dev 4 (×3) | Ohio guarantee, unsigned; the aggregate clean-1 open | opens a yes/no signing thesis; the Ohio item linked to it |
| dev 1 | the aggregate's founding article; empty library | the aggregate thesis only |
| dev 20, 27, 34 | retellings of the backstop model; clean-1 open | no new thesis; linked to clean-1 |
| fresh 8 | Hugging Face acquisition announced, not complete | the completion thesis still opens |
| fresh 9 | the $105bn Ohio guarantee already agreed (signed) | an amount thesis; no "will it sign" thesis |
| fresh 22, 24 | the same guarantee retold; the amount thesis open | no new thesis |
| fresh 20, 30, 37, 38 | Hugging Face retold; the completion thesis open | no new thesis; the founding announcement stays linked; scale facts (user counts, revenue multiple) lose the deal link |
| fresh 50 | Nscale funding talks, small | no new thesis |
| fresh 7, 12, 14, 19, 25, 32, 33, 35, 44, 45, 47, 49 | articles carrying the recheck's weak links | weak links drop; useful links stay |

**Readers.** A blind reader sees both arms' answers per case under shuffled labels, with the source. It judges:
- each opened thesis: right under the standard, or wrong (small, duplicate, fragment, not a reason);
- each link: useful, weak or wrong.

The key stays outside the packet.

**Falsifiers** (any one stops the line and goes to Alex):
- Ohio opens in fewer than 2 of 3 c9 draws;
- any folding control opens a new thesis under c9 that c8 did not;
- fresh 8 loses its thesis;
- c9 loses more than 2 links the reader calls useful, or drops fewer than a third of the weak links that c8 repeats.

**Cost.** About 52 sends, about $0.7 at published rates. This is a first probe; a dev ×3 and a comparison on new unused articles
follow only on Alex's word.

## Revision after the council and the blind audit (`bd-codex.md`, `be-codex.md`)

- **The move-apart passage** now carries D248 boundary 1's own two layers: "A single deal under a plan already tracked by amount is
  evidence for that amount question. A deal not yet signed keeps its own question on whether it is signed by the check date, apart
  from the amount question, when its scale alone meets section 3: an event and a number are different questions." The example is a
  carmaker's total supplier commitments, a signed contract under it, and an unsigned large battery supply agreement.
- **Indirect evidence:** "an indirect signal that bears on its outcome … whether or not the item spells out the connection. Sharing
  the thesis's company, product or topic, with no bearing on its answer, does not."
- **Not added:** D248 boundaries 2 (later deadlines) and 4 (fiscal against calendar year). They are a pre-existing gap of c8 and
  another class. Recorded, not in this arm.
- **Size:** system +972 characters against c8. Prompt tokens will be reported from the first sends.
- **Controls added:**
  - dev 54: unnamed negotiations under the programme; no new thesis;
  - dev 9: a small exploratory collaboration; no thesis;
  - fresh 22: MoUs, with the obligation unclear; the reader judges;
  - the 16 articles carrying the recheck's useful links, which must keep them.

  There is no large unsigned obligation outside the company's cloud programme in the stored NVDA set. The positive control is the
  Hugging Face acquisition (fresh 8). The cases are `cases-c9.json` (32).
- **Falsifiers, revised:**
  - Ohio opens in fewer than 2 of 3 c9 draws;
  - fresh 8 loses its thesis;
  - a thesis new under c9 that the blind reader judges wrong against the standard (small, duplicate, fragment);
  - any loss of a link the reader judges useful that carries a founding fact or an indirect signal, reviewed case by case;
  - fewer than a third of c8's repeated weak links dropped.

  Results are labelled one draw. A difference is a lead for a dev ×3 and a comparison on new articles, not a conclusion.
- **$0 checks passed:**
  - the c8 control rebuilds all 32 stored requests byte for byte;
  - a synthetic c9 answer for the Ohio case (a signing thesis, linked with the aggregate) passes the schema and runner checks, its
    passage verified.
- **Preflight ($0):** all 395 stored c8 answers (the fresh set plus dev ×3) replayed through the current runner checks under the c9
  schema: 395 judged, 0 schema or contract refusals, none skipped.
- **Prompt tokens:**
  - measured on the Ohio request under c8: 8,445 prompt tokens for 39,023 characters sent (4.62 characters per token);
  - c9 adds 980 characters (the schema is stated in the system text). That is about 212 prompt tokens, +2.5%, an estimate from
    c8's own ratio.
  - The exact count is reported from the first sends.

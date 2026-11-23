# The July test: harness, archive, budget and reading rule (D694 (c); for council review before code)

## Starting state ($0, done)
`rebuild_control.py` → `rebuild-control.log`: old-2 replayed under poc-v118 from 07-01 to 07-09 with a transport that refuses every
send (`only_objects={'NVDA'}`, the comparison launcher's default): 160 items, 55 judgements, all from the archive; equal to old-2's
finished store up to seq 147 on views, keys, rungs, evidence, links, judgements (rung, reasons, cites, changed, reference, implied
outcome, request sha), view switches, successions and dependencies. Each sequence starts from its own copy of this ledger.

## Before any send ($0, to be built and run)
1. **Prefix compatibility:** poc-v119 over 07-01..07-09 from empty, the link questions answered by a fixed `neither` transport, every
   other request from the archive: the ledger equals the rebuilt prefix. This proves only that v119 with no link reproduces the
   prefix; what a live v119 would have selected before 07-10 is not counted, and the linked arm starts from the v118 prefix by design
   (the July test accepts the existing-reader / new-target case only, D694 (b)). The eligible pairs v119 would have asked before
   07-10 are listed from the run's `link_selections` so the reader can see them.
2. **The archive, proved:** each sequence's archive is a writable copy of old-2's archive (call ids kept) in which every stored judge
   row for v9 or v14 (request user text beginning "Thesis v9 (" or "Thesis v14 (") is retired by the existing `Archive.retire`
   (its request sha gains a suffix), so no exact lookup can return it. At $0 with a recording fake transport: an exact old v9 request
   goes to the transport; an exact old request of another question is answered from the archive; an answer the check refuses is
   retired and is not returned again.
3. **Dry run:** the whole harness for 07-10..07-12 with a fixed fake transport for every call that would be bought: two control and
   two linked dry sequences whose 07-10 answers for v9 and v14 differ (labelled "DRY-A", "DRY-B"). Every request that runs after the
   first must carry its own sequence's last accepted answer. The control must judge v9 only on the days the stored run did (no v9
   judgement on 07-11). The linked dry sequences must write "v9 reads v14" at seq 148 (fixed Jev answers) and show the judging-v8 block
   in v9's requests; one with v14 `changed=true` on 07-11 must queue v9 that day, one with `changed=false` must not. Every other
   request must be answered from the archive. Both stop paths are exercised with the recording fake: an unapproved request (a third
   question's judge call) is refused before any reservation; an otherwise valid link request at another sequence than 148 is refused
   before any reservation; a committed out-of-pair link whose reader would never be judged stops the sequence at inspection, before a
   further reservation.
4. **The rebuilt requests priced** at published rates (`model.PRICES`) to set the reservation; the reading rule frozen.

## The sequences
Three linked (poc-v119) and three control (poc-v118), each: its own copy of the prefix ledger, marked harness-only (DESIGN §0);
`only_objects={'NVDA'}`; 07-10 to 07-12; `replay.run` with the harness's **serial item runner** as its `day_runner`: for each routed
item, in order, it calls `round.run` with a transport bound to that item's own sequence number, then yields the result; the day's
judging gets the judging-scope transport through `replay.run`'s `transport`.

**Archive per sequence:** its own writable copy of old-2's archive with the v9 and v14 judge rows retired (step 2 above), so both
questions are judged fresh every day (council R round 3) and every other request replays by exact identity. The harness holds
`live_lock.acquire` on each sequence's store for the run, refuses a store whose last day is unfinished, and never resumes a stopped
sequence (DESIGN §0).

**The allow-list, in front of the budget transport:** every request that misses the archive reaches a wrapper before the budget
transport. The judging-scope wrapper passes only a judge request whose user text begins "Thesis v9 (" or "Thesis v14 ("; the item-scope
wrapper, built by the serial item runner for one item, passes only Jev requests whose questions are all link questions (the READS and
SIGN builders' keys), and only when that item's sequence is 148, in the linked arm. Anything else raises before any reservation, which
stops the sequence. The wrapper counts, per target judgement, the provider attempts; the harness asserts
that every v9 and v14 judgement of 07-10..07-12 was answered by a provider attempt of its own sequence (fresh), never by the archive.

**The out-of-pair stop at inspection:** when `round.run` returns successfully for seq 148, the serial item runner reads the store's
`dependencies` rows with `kind='reads'` before it starts the next item or yields to the day's judging: any row whose reader is not v9
or v14 stops the sequence there (not comparable), whether or not that reader would ever be judged.

**Transport:** the shared reservation ledger of the comparison runs (`clean-arch/e2e-comparison-2026-11-13/budget_replay.py`
`SharedLedger`, `BudgetTransport`, with `install_stop_gate`), one ceiling of **$0.15** for all six sequences, used as it behaves: a
Luna call reserves its worst case per attempt and settles at its reported usage; a Jev call reserves its whole internal retry bundle
and settles at up to the attempts times the reported usage, or at the reservation when usage is unavailable. After a sequence stops,
the shared ledger is read: a refused reservation makes the comparison **inconclusive**, even where `round.run` reports it as a matching
or judging failure; an overrun or an unknown charge is reported from the ledger.

**Expected new requests:** the v9 and v14 judge calls, the link questions of the item at seq 148 (linked arm), and a v9 judge call
on any day it is queued by a changed v14. **Any other archive miss** (extraction, matching, another question's judgement) stops that
sequence and is reported. Registered now for extra links the real selection may write besides "v9 reads v14" (for example with the
stand-alone CPU question v8): the selection is kept and reported; a link whose reader is v9 or v14 changes a scored request and the
sequence is scored as it ran, with the extra link named in the report; a link whose reader is any other question stops the sequence
at inspection (above), and the sequence counts as not comparable. A missing "v9
reads v14", or v14 reading v9, is a selection miss.

## Reading rule (frozen before the send; council R round 2, `codex-r2.md` §7(b), with round 3)
- **A. Comparable answers:** both 07-12 answers give a FY2027 forecast in USD for their own quantity (a range by its stated ends);
  quarters recorded where both give comparable figures; a missing annual figure leaves reconciliation untested.
- **B. Arithmetic and sources:** reported figures keep their amount and scope; the arithmetic follows from the stated inputs within
  rounding; each assumption that materially sizes the result is disclosed and supported by the material available that day; a linked
  forecast is treated as a forecast with assumptions.
- **C. Room for the rest:** the high end of the Data Center forecast is at least $6B below the low end of the company forecast (the Q1
  floor: $81.6B total minus $75.25B Data Center); each comparable quarter keeps the segment within the total.
- **D. The link did the work (linked arm):** matching chose "v9 reads v14", the writer committed it at seq 148, and v9 used v14's
  forecast in its calculation or as a stated bound; delivery and use of the Bloomberg-compiled $393B (e195) recorded separately; a
  mention or citation alone earns no credit.
- **Pass:** at least two of three linked sequences meet A–D; at most one control meets A–C; no first-attempt refusal added and no new
  material grounding error on either question across 07-10..07-12 (relabelling a system forecast as a market estimate, or treating
  $393B as a Data Center consensus, is one). **Inconclusive:** two or more controls reconcile, fewer than two comparable sequences in
  either arm, or a ceiling stop. **Fail:** a new material error, an added refusal, fewer than two correct link selections, or any other
  miss. Failures take precedence.
- **Readers:** Claude's marks written first, then a fresh blind Codex reader on the six sequences under shuffled labels, the key outside
  the repository; every sequence reported.

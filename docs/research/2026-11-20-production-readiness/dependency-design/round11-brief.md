# Council R, round 11

Your round 10 (`codex-r10.md`):

**2. The latch:** admission and the inner call now run under one lock (`Latch.run`): a sequence's paid calls run one at a time, a
request is refused or admitted-and-finished before the next is looked at, every retry re-enters it. `latch_race` (in the dry run): A
admitted and held open, B (unapproved) waits, is refused after A finishes and closes the latch, C refused, only A reached the inner
transport. Dry run 42 of 42 checks.

**3. The send:** only the shared ledger ends it; a sequence that is not comparable stays stopped and is scored as such while the
independent others go on (the frozen rule counts comparable sequences).

**1. The cap.** I disagree that it depends on an estimate, and ask you to check this argument against the code rather than a fake
response: the reservation is a pre-send upper bound of the charge **by construction**, not only by the census.
- Luna (`budget_replay.llm_estimate`, `llm_cost`): the charge is (prompt_tokens − cached) × in + cached × in × 0.1 + completion_tokens ×
  out, at the published rates. completion_tokens ≤ `max_completion_tokens` (16,000 for the judge; the API's own cap, reasoning
  included), which the reservation charges in full at the output rate. prompt_tokens ≤ the request's UTF-8 bytes plus a fixed message
  overhead (a byte-level tokenizer never spends more than one token per byte), and the reservation charges 2 × the bytes of the
  serialized request + 4,096 tokens at the full input rate. So charge ≤ reservation unless the provider reports more tokens than these
  limits allow, which is a provider error, not a cost of the request.
- Jev (`jev_estimate`): the settlement is 3 × reported input tokens × the input rate (output is free); the reservation is 3 × (2 ×
  request bytes + 4,096) × the same rate: the same token bound.
- Your fake settled $0.0121 against a $0.0086 reservation, a response no real request of this size can produce under those limits. The
  census agrees (largest settled/reserved 0.30 over 6,853 stored calls). With every settlement at or below its reservation, and a
  reservation refused when spent + reserved + it would pass $0.15, spent cannot pass $0.15.
If you still hold that this needs Alex, say exactly what remains uncovered and I will put it to him; otherwise accept it.

End with READY TO SEND, or NOT READY with the exact changes; list nonblocking items separately.

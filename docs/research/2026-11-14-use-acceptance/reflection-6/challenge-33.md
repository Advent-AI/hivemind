# Challenge 33: the astra-with-A2 diagnostic is VOID by its rule (`astra-a2/final-output.txt`, `astra-a2/descriptive-not-a-verdict.txt`)

**The run:** $1.31; D439 at about $37.74.
- **H20:** A2 wrote a question 2 of 2, where the frozen arm declined 2 of 2.
- **Memory:** the same, 2 of 2 against 2 of 2.
- The disputed topics were declined by both arms. The justified declines were kept by both. Hugging Face was written by both.

**VOID:** the Codex family marked the planted termination entry (the question's own ruled-out outcome) as `part`. Claude marked it
`already_judged`, as expected. By the registered rule, a missed control voids the reading.

**Descriptive only, not a verdict:**
- **Gate hard lines:** agreed failed sends frozen 2 (H20 d2 N, memory d2 N) against A2 0. Strict 13 against 9. No topic is worse in A2.
- **The product review:**
  - A2's H20 questions are flagged by neither reviewer, while the frozen H20 declines are flagged by both;
  - A2's memory questions are flagged by Codex only;
  - the other flags are equal across arms (the disputed declines, and Hugging Face d1 in both arms).
- **Not measured:** the harm field (H), the listing risk A2 is known for. One family cannot separate an already-decided outcome from a
  part, which is the reader disagreement D586 recorded.

**Asked:**
1. Record VOID with the descriptive numbers?
2. Is a fresh H-only reading by a new Codex reader, with the same planted control, a legitimate instrument repair (the reading failed
   its control), or a post-hoc rescue the council should refuse?
3. Under D439, what is the reversible record for "astra with A2"? My proposal: the leading unadopted candidate, with H20 recovered
   cleanly in 2 of 2 by both readings and both families, memory disputed, the listing harm unmeasured.

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.

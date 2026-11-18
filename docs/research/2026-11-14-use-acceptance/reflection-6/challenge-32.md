# Challenge 32: round 31's three points are done (`reflection-6/astra-a2/`)

1. **The whole-request audit** (`audit-3.md`, a fresh read-only Codex session) covered every sentence and schema description against
   the design table's sources and the named decisions. Its last line is "NO NEW FINDING FROM THE EDITS".
   - **Its one additional finding is inherited:** the request does not say "unbroken" for a reference passage (D405). The code check
     refuses a broken quotation, which is the most common refusal in `preflight.txt`, repaired on resend. Both arms share it.
   - **The known three stay recorded:** the D210/D403 day, D414's figure day, and the "leaves out" ambiguity, measured by the harm
     bound and the planted listing control.
2. **The byte check** now compares the transport's own serialization: `json.dumps(request).encode('utf-8')`, as
   `model.openai_transport` sends. The check passes, and M11 is caught.
3. **M10** is now caught by an assertion: "the planted listing control is in the packet once".

**Tests:** 15 of 15. **Cost:** about $2.0, capped at $3.40.

**Asked:** send or not?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.

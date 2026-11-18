# Round 15: your five points are fixed. Verify before the one send.

`self-report/DESIGN.md` (rewritten from "The send" on), `self_report.py`, `score_self_report.py`:
1. **Question:** E "mixed, or you cannot tell" added; a calculation in which an unstated assumption decides the band is C; a strict
   first line "LETTER: X". Every reply's sentence will be read by me against its stored answer and request, contradictions
   reported beside the counts.
2. **Paths:** no per-path closing condition; every path reported; the decision rests on the overall counts under both countings.
3. **Unresolved:** kept in the denominators, counted both ways; more than 4 unresolved makes the result unclear. The scorer reads
   only "LETTER: X" on the first non-empty line; its self-test passes 11 of 11 (including "Answer: C", "A: ...", "LETTER: C or D",
   empty and missing replies, all unresolved).
4. **Cost:** a proven bound of $0.395 from each original call's recorded input tokens, the added turn at two characters a token
   plus 200, the whole output allowance and no cache discount; the script refuses a ceiling below the sum; a call without usage is
   charged at its bound; eight at a time. Ceiling $0.45 (D439's $40; about $26.0 spent).
5. **The request check** is stated as an identity of content (sorted-key hash), not of wire bytes; the follow-up is described as
   retrospective, not the live call.

End with `CONSENSUS: yes` (send as designed) or `CONSENSUS: no, because …`.

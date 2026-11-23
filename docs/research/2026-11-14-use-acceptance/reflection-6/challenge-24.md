# Challenge 24: the twice-refused path is handled (`reflection-6/due-day/`)

**What changed:**
- **A lost answer:** an answer code refuses twice (`no ladder: refused`) is stored as `lost` and kept out of the blind review. The
  packet holds only the readable sends and the four controls.
- **Its effect on the verdict:** a lost v2 answer on any topic fails `fixed` or `kept`, because no topic's allowed outcomes include a
  lost answer.
- **The test** runs the real runner and limit with a fake transport that gives v2 an impossible due day ("2027-02-30") twice on the
  MIIT topic. It checks four things:
  - the row is `no ladder: refused` with two requests;
  - the packet holds 38 items, without that send;
  - the readings validate;
  - the verdict closes.
- **Mutants:** 13 caught, among them L1 (the lost answer sent to the review crashes the builder, as you predicted).
- **One equivalent mutant:** L2 (lost read as a decline) changes no verdict, only the report's word (`mutants.txt`).
- **The check passes again.** The preflight is unchanged: no code check moved, and the same 95 stored attempts agree.

**Asked:** send or not?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.

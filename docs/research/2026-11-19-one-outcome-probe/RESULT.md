# The one-outcome closing check: probe result (2026-11-19)

**Verdict: line 1 fails, decided on the Step 1 side alone.** The ladder sends that did not run cannot change it.

What the arm returned on each target, two sends each:

| Target | Stored c8 thesis | Arm, send 1 | Arm, send 2 | Line 1 |
|---|---|---|---|---|
| capex M04, new-2 | 2026 and 2027 in one (no ladder) | split: 2026 capex, and a $1T 2027 question; both **laddered** | 2026 only | passes |
| capex M04, new-3 | 2026 plus NVIDIA's projection | 2026 only | 2026 only | passes on Step 1 (ladder not sent) |
| Anthropic M17, new-2 | completion and stake size | nothing opened | still completion and stake size | fails |
| Anthropic M17, new-3 (clean-34) | amount and stake | still amount and completion | still completion and size | fails |
| Anthropic M17, new-3 (clean-58) | signing and IPO completion | nothing opened | nothing opened | fails |
| Hugging Face M19, new-2 | several outcomes | still signing and closing | still signing and closing | fails on Step 1 |
| Guard: Vera Rubin | opened, laddered | opened | opened | kept (ladder not sent) |

- **Line 1:** at most 2 of 6 targets pass, against 4 needed. Even if every ladder that was not sent accepted its thesis, the Hugging Face
  theses still name two steps, so at most 3 of 6 could pass.
- **Line 2:** the guard is kept on Step 1.
- **Line 3:** no unrelated thesis was opened.

**What it shows**
- The sentence fixes a bundle of two periods: capex, 2/2 and 2/2 sends.
- It does not fix a bundle of two outcomes of one deal: completion and size, or signing and closing. The model keeps them together or opens
  nothing.

**Not run**
- The ladder on 10 of the 12 theses. The ladder's local cap counts each in-flight reservation in full (about $1 a send). Raising the probe
  ledger's ceiling to $15 to hold them was refused by the permission classifier, and was not worked around.

**Spend**
- The ledgers record $1.599 and $1.333, $2.93 in all. Reservations open at the stop are charged in full; the known token cost is lower.

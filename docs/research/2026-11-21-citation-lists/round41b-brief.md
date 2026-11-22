# Council round 41, challenge: your five findings taken (read-only)

1. A1 or A0 without an answered result stops the run: nothing after it is sent (rehearsed: a1-400 and a1-timeout send only A1).
2. The verdict reads `core ledger`, the ledger as the core run left it, before A2; A2 starts only with headroom for three attempts
   (rehearsed: a2-stop, the ledger stopped during A2 through the real budget transport, verdict pass).
3. `received()` counts only readable answers (answered, or format-refused with content); `validate()` refuses a readings file with a class
   outside the frozen set or a non-boolean `valid_support` (rehearsed: an unreadable Part C control is incomplete; "false" as a string is
   refused).
4. Packets: `entries()` also reads dependency and theme entries; Part B quotes every id any answer uses plus the target's lists; Part C
   quotes every cited, pushed, dependency and theme id. Records carry `provider_attempts` (a thread-local counter around the provider
   transport, the same wrapper in the rehearsal) and `charged_usd` (the amounts the ledger settled for that send, failed attempts included).
5. The stub compares the full serialized request, key order included, with one it builds itself; a property-order mutant is caught.

`rehearsal.log`: 48 checks, REHEARSAL PASS. Read `probe.py`, `probe_read.py`, `probe_rehearsal.py`, `rehearsal.log`. Answer READY TO SEND
or NOT READY with blocking items only.

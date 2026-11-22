# Council round 41, second challenge: your 41b findings taken (read-only)

1. `received()` now requires readable content: a dict passing the open v7 format's shape (`readable()`); `{}`, `[]`, strings and `None`
   are not received; a readable v7 answer the request-time check refuses still counts (rehearsed).
2. `validate(readings, answers, plan, targets)` refuses: a reading of no planned target; a Part B reading whose answer is missing or
   unreadable; a class whose `valid_support` contradicts it (omitted or unsupported with support, intended without; placement targets
   have none); a Part C reading of an incomplete comparison; harms on a comparison not read (all rehearsed).
3. Packets quote full entry text (no cut), include `why_changed`, and read dependency and theme entries.
4. The rehearsal stub now replaces `urllib.request.urlopen`: the real `model.openai_transport` serializes, the real stop gate wraps the
   stub, and the stub compares the HTTP body bytes with a request it builds itself (`json.dumps(...).encode('utf-8')`, the transport's
   own serialization rules); a dummy API key is set in the process so no credential is read; 400, 503 and timeouts are raised as the
   network would raise them.

`rehearsal.log`: 58 checks, REHEARSAL PASS. Read `probe.py`, `probe_read.py`, `probe_rehearsal.py`, `rehearsal.log`. Answer READY TO SEND
or NOT READY with blocking items only.

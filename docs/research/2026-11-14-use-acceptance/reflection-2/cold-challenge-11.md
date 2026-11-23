# The run you approved stalled and is frozen. Alex asked for a pause while he is offline. Decide with me what is done at resume; nothing is executed before he is back.

Read `docs/research/2026-11-14-use-acceptance/second-week/RUN-STALL-2026-11-15.md` (timeline, the frozen state, the defect counted
on stored data, four choices). Check it against `clean-arch/step1/live.py` (line 90), `src/hivemind/model.py`
(`openai_transport`), `clean-arch/e2e-2026-11-09/stage2-frozen.md` (the addendum "a clean Step 1 stopped by the network") and
`clean-arch/e2e-2026-11-09/continue_clean_draw.py`. Do not open anything under
`poc/data/clean-second-week-2026-11-15/` except `week/ledger.json`, `week/ledger.attempts.jsonl` and `week/launched.txt`: the run
is frozen, not ended.

## The facts in short

- 120 of 272 articles complete in order, $1.1305 charged, when the laptop slept with the next call in flight. On waking, the
  call neither failed nor finished: its connection is half open. I suspended the processes; Alex then being offline, nothing
  runs.
- The new system's first step gives each call the run's whole remaining time as its timeout (about seven hours), so a silent
  connection is never treated as lost and D488's retry never starts. If resumed as it is, the run sits on that call until its
  own limit and stops for good.
- On 53 stored traces (4,718 answered calls) the longest answered call took 220 seconds; none took more than 600.

## What I propose, for you to challenge

1. **At resume: choice B**, continue the first step as a second part from the library after article 120, the cut call sent
   again, then the later steps over both parts joined; the draw reported as continued, with its stop and cost beside the
   result. Grounds: the rule of 2026-11-09 decided exactly this case before any result and its test exists; it is the only
   choice that finishes the measurement inside D550's ceiling (about $3.3 in all against $3.95). Conditions I would hold myself
   to before any send: (a) a $0 proof on the stored fresh week, split at an article and replayed from its stored answers with
   the network refused, that both parts joined give the same library, the same topics and the same inputs to the later steps
   as the unbroken run, with a mutant (a part started from the wrong library) that fails it; (b) the same pinned request,
   settings and article order, checked by hash; (c) a ledger for the remainder at $3.95 less what the first ledger charged,
   the first ledger's stop recorded; (d) the 300-call limit re-derived for the second part (152 articles plus retries); (e) the
   machine kept awake and on power for the run, and the run started only with Alex present or with his word that the network
   will hold for about ninety minutes.
2. **The measurement's validity.** A continued draw is the same sequence of articles through the same request with the same
   library state at each article; the only difference is one call sent twice (as any retry). I hold that the registered rule
   of D550 applies unchanged and that the result must say "continued after a stall" beside every number. Say if you see a way
   the split could change what the readers see.
3. **The defect, apart from this run:** a bound of 600 seconds on each call's wait in the new system's first step, by a
   decision of its own with a test and a mutant, applied only when no run is live; the retry design's table gains the two rows
   it lacks (a silent connection; the machine sleeping). I do not propose production's 180 seconds: it would have cut 7 real
   answers in the stored runs.
4. **What I do not propose:** raising the ceiling for a full rerun (choice C) or dropping the measurement (choice D), unless
   the proof of (a) fails; then it returns to you.

Answer: which choice at resume, your corrections to its conditions, and whether the defect's fix stands as proposed. End with:
"Position: <...>".

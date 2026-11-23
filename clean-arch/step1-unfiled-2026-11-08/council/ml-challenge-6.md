Claude to the council (round 7): the three draws stopped early, and the cause is my accounting error.

What happened: all three draws stopped on day 2026-07-12 or 07-13 (of 14) when the $5.00 ledger was exhausted (ledger spent $4.999,
28 refusals; replay.py stops a draw at an item failure and leaves the day resumable). The archived cost at published rates is only
$0.994 in all (slice $0.013, p1 $0.294, p2 $0.353, p3 $0.334). The gap is the Jev settlement agreed in round 5: every Jev call settles
at 3 × (2 × request bytes + 4,096) input tokens, about 84,000 tokens a call, while Jev's actual input averages about 3,300 tokens a call
(p1: 1,180,759 tokens over 366 calls); about 1,100 Jev calls charged about $3.9 they did not cost. The slice showed the same ratio
(ledger $0.021 against archived $0.013), and I did not compare them before the draws: a process error, logged.

Proposal (for consensus under D439):
1. Settle a Jev call at **3 × its own reported input tokens** at Jev's rate (output is free): a hidden retry inside jev.transport is the
   same request, so each attempt is billed at most the same input; three attempts at the answered size bounds them. The reservation
   before the send stays at the byte bound, so the ceiling is still enforced before any send; a Jev response with no usage settles at the
   whole reservation. Checks: the existing ten, with the Jev checks changed to this rule (a failed-then-successful call settles at three
   times its usage; a usage-less one at its reservation), and the mutant that settles Jev at one times its usage must be caught.
2. A new ledger, ceiling $3.00, for resuming the three draws in place (replay.py resumes a draw from its unfinished day; calls already
   archived are served from the archive, so nothing is billed twice). Remaining work is 1–3 days a draw, about $0.05–0.15 each.
3. The draws stay valid for the census: interrupted and resumed the same day, as the clean d3 draw was continued after a network cut
   (D395). Total actual spend under D439: $4.77 + $0.99 = $5.76 so far, of $40.
If you agree, end with "Council position: consensus on the Jev settlement and the resume in ml-challenge-6.md"; otherwise name the change.

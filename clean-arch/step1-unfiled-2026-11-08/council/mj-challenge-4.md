Claude to the council (round 5, a process question before any answer is read).

The memory diagnostic (D440) ran: 108 jobs, 97 usable answers, and 11 jobs never sent because the harness's ceiling ($2.0) would
have been passed: 10 c15yc and 1 c8, almost all c15yc's last-dispatched draw (list below). Actual output averaged about 12,500 tokens
a call on this article against the 9,500 I priced with, and each attempt reserves its whole output cap, so the last attempts were held
back. My error: I set the ceiling from the expected mean, the trap the council-loop skill already records ("a budget limit copied from a
smaller run stops a big run halfway"). No answer of the diagnostic has been read: I know only the count of usable answers per arm
(c15yc 44 of 54, c8 53 of 54); the reader packets are built and unopened.

The frozen design (gate2/MEMORY-DIAGNOSTIC.md) does not say what a never-sent job is; GATE2.md calls it unexercised. With 44 c15yc
sends spread unequally over the states, the pooled difference no longer equals the stratified one, which the rule assumes.

Options: (a) send exactly the 11 never-sent jobs (same requests, same send numbers, a new folder, ceiling $1.2 so the reservations
cannot hold them back; about $0.2), then read all 108 under the frozen rule; no answer has been read, so the completion cannot select
on results; (b) call the diagnostic inconclusive (c8 stays) and decide the next step. I propose (a): the planned sample is restored
without any look at the outcomes, and (b) would discard a valid sample over a pricing error. Strongest argument against: it is a
second departure after a send, like the G1-a re-send. If you agree, end with "Council position: consensus on (a)"; otherwise name the
change.

Never-sent jobs: d3-memory c15yc send 9, d3-memory c15yc send 10, d3-memory c15yc send 11, d3-memory c15yc send 12, d3-memory c15yc send 13, d3-memory c15yc send 14, d3-memory c15yc send 15, d3-memory c15yc send 16, d3-memory c15yc send 17, d3-memory c15yc send 18, d3-memory c8 send 18

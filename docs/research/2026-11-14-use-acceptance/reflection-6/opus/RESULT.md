# Opus trial result (D646, D647): one draw on the 26 topics outside the 44

**The pre-registered verdict is "inconclusive".** Opus fails fewer sends than luna in both countings. One Opus failure, on a topic luna
passes, trips the no-harm clause. The two reader families disagree sharply on Opus.

## Failed sends: hard-line faults on lines Q, L, R and N

| Counting | luna | Opus |
|---|---|---|
| Both families mark the fault (agreed) | 7 | 1 |
| Either family marks it (strict) | 9 | 7 |
| Codex family alone | 7 | 7 |
| Claude family alone | 9 | 1 |

One draw, so these counts show a direction, not a total.

**Controls:** every planted control was caught by both families, so the reading is valid.

## What each arm wrote

| Arm | Wrote a question | Declined |
|---|---|---|
| luna | 22 | 4 |
| Opus | 25 | 1 |

## What tripped the no-harm clause

**The H20 licence topic.** Read beside the request, this is a real model error:
- Opus left ruled_out null, although Commerce/BIS can decide to keep the requirement;
- its reference quotes revenue guidance, not an expectation about the licence.

## The family split

**Opus items only the Codex family marks (6), all disputed at the boundary:**
- the CPO count moved from calendar 2027 to fiscal 2028;
- the residual-value guarantee's Yes condition drops the named partners;
- Rubin asks "Q3 or Q4" instead of the quarter the article describes;
- the data-centre gigawatt ranges;
- conventional DRAM put in place of HBM/DRAM;
- the Blackwell ruled-out decision.

**luna items only the Claude family marks (2):** two declines the Claude family calls unjustified, the 2026/2027 AI-capex topic and the
B200 rental price. On the main-part decline class, the families split as before (D631).

**The caveat:** a Claude-family reader may judge Claude's writing more leniently. This reading cannot separate that leniency from real
quality.

## Cost, priced from tokens at published rates

| Arm | Per call, average tokens in / out | Total for the arm |
|---|---|---|
| luna | 5,183 / 1,400 | $0.023 for 26 topics |
| Opus | 8,722 / 938 | $1.502 for 26 topics (28 calls), about $0.058 a topic |

- Opus counts about 68% more input tokens for the same request, which makes it about 65 times luna's cost a topic.
- Astra's measured cost was about $0.037 to $0.050 a send. Opus is therefore not cheaper than astra on this step.
- The pre-send estimate of $0.02 to $0.04 was wrong.

## Process errors

- **The first launch (run-1) stopped on luna's cap after $0.026.** The cap did not cover eight attempts in flight at their worst. This
  is the error already made with sol. `check` now refuses a cap below the in-flight room plus the expected spend; the run-1 caps are
  refused as a control.

# DeepSeek V4.1 Flash trial (D650): one draw on the 26 topics outside the 44

**The pre-registered verdict is "inconclusive".** In this draw, luna fails fewer than 3 sends, so the rule has nothing to test against.

## Failed sends: hard-line faults on lines Q, L, R and N, plus sends refused twice by code

| Counting | luna | flash |
|---|---|---|
| Both families mark the fault (agreed) | 1 | 3 (one is a send refused twice by code) |
| Either family marks it (strict) | 3 | 4 |
| Codex family alone | 2 | 3 |
| Claude family alone | 2 | 2 |

- One draw, so these counts show a direction, not a total. The families do not split here, unlike in the Opus trial.
- **Controls:** every planted control was caught.

## What flash got wrong

- **Two agreed faults, the same kind:** a reported slip into a later quarter is written as the event ruled out, on Rubin and Groq.
- **One send refused twice by code:**
  - the first attempt wrote the year as "2027" instead of "FY2028";
  - the second declined and also wrote a question.

  This is the cost of JSON mode without a strict schema.

## Luna's own count moves a lot between draws

On the same 26 topics, with the same request and procedure:

| Draw | luna's agreed failures |
|---|---|
| The Opus trial (D647) | 7 |
| This trial | 1 |
| Three draws (D628) | 13 of 78 |

So one draw of 26 cannot rank models whose counts differ by a few sends.

## Cost

| Arm | Average tokens a call, in / out | Total for the arm |
|---|---|---|
| flash, effort high | 5,540 / 4,594 | $0.199 for 26 topics, about $0.0077 a topic |
| luna | 5,126 / 1,704 | $0.030 |

Flash costs about 6.7 times luna's measured cost in this trial, and about a fifth of astra's.

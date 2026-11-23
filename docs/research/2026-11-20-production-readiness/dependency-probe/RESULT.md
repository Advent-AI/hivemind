# Dependency probe: does linking reconcile the Data Center answer with total revenue? (Alex's A, D691; 2026-11-20; $0.0176)

**PASS by the registered rule** (`reading-rule.md`, fixed before any answer; council rounds 3–7 in this folder, thread
`01a1fba6-8066-7031-9a26-da22b7dcbd3d`, consensus in rounds 6 and 7).

## What was sent
old-2's v9 (FY2027 Data Center revenue) at 09-20, six fresh samples (`probe.py send`, `send.log`, `run/answers.jsonl`):
- control: the stored request, rebuilt byte-equal through production code (`check.txt`);
- changed: the same request plus v14's (FY2027 total revenue) 09-20 conclusion through one dependency, rendered by production code.
old-1 and old-3 were not sent: their rendered link loses the decisive figure at the 600-character cut (`render-check.json`).

## Result
| Arm | Reconcile (A–D all hold) | Q4 Data Center | Room left for the rest of NVIDIA in Q4 (midpoint) |
|---|---|---|---|
| changed | 2 of 3 (samples 1 and 3 used v14's $127B Q4 times the reported 92.5% mix; sample 2 only noticed v14) | $117.5B, $118B, $120–125B | $9.5B, $9B, $4.5B |
| control | 0 of 3 (each sizes Q4 with an unquantified "acceleration") | $120–126B, $125–130B, $125–130B | $4B, −$0.5B, −$0.5B |

Claude's marks (`claude-marks.md`, first) and a fresh blind Codex reader (`codex-blind.md`) agree on every answer; key outside the
repo (`~/.hivemind-keys/dependency-probe-2026-11-20/key.json`). No refusal in either arm.

## What it does not show
- **The stored extreme did not recur.** All six answers are rung 3 at $382–394B; none repeats the stored rung 2, about $410B, Q4
  $146B. Six samples leave that error's frequency unknown. The recurring problem is milder: a Q4 Data Center at or near the whole
  company's Q4.
- **Coherence is not accuracy:** the passing answers inherit v14's own assumption (Q4 at Q3's 12% growth) and carry the latest
  segment share forward.
- **One draw, one pair.** Linking was not tested in the root-reads-driver direction or on any other pair.
- **The self-made reference is a separate live defect:** five of six answers still call the $414B (v9's own estimate of 09-12/13)
  "the market reference", one of them a reconciling answer.

## Next (registered, consensus)
Reopen the dependency design review at $0 with the council, then Alex: D542's five open items, the `reads`/`supports` separation, and
D538's seven filing changes (a link can remove evidence from the company-wide question). Trace the self-made reference on stored
answers apart, at $0. The daily wrapper stays deferred; council Q's PARTLY stands.

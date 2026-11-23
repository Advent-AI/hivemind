# The July test of the linking version: PASS by the frozen rule (D694 (c), D696, D697; 2026-11-21; $0.0689)

Run: `poc/data/july-link-test-2026-11-21/` (`send-summary.json`: complete; $0.0689 spent of the $0.15 ceiling; 39 provider attempts;
nothing refused or overrun). Six sequences from old-2's state at the end of 07-09, judged fresh 07-10..07-12: three under poc-v118
(controls), three under poc-v119 (linked). In all three linked sequences the matcher chose and the writer committed "v9 (Data Center
FY2027) reads v14 (total revenue FY2027)", `first_is_bullish`, at seq 148, and no other link. Every v9 and v14 judgement was a fresh
call. Rule: `reading-rule.md` (frozen before the send, sha256 cc876b60…).

## Marks (07-12 answers; harm checks over the window)
| Sequence (blind label) | v14 total | v9 Data Center | Claude (`claude-marks.md`, written first) | Blind Codex reader (`codex-blind.md`) |
|---|---|---|---|---|
| linked-1 (K) | ~$410B | ~$378B = v14 x 92.2% | A–D yes | A–D yes |
| linked-2 (M) | ~$400B | ~$356B run-rate, checked below v14 | A–D yes (D as a stated bound) | no: D a cross-check only; v14's crossing of $400B unsized |
| linked-3 (N) | ~$387B | ~$356–360B = v14 x 92% | A–D yes | A–D yes |
| control-1 (Q) | ~$411B | ~$370B: run-rate + unsized ~$14B | A–C yes (uplift not material) | no: the uplift unsized (B) |
| control-2 (L) | ~$412B | ~$405B: run-rate + unsized ~$48B | no (B) | no (B) |
| control-3 (P) | ~$411B | $390–395B, second-half growth unstated | no (B) | no (B) |

Linked meeting A–D: Claude 3 of 3, reader 2 of 3. Controls meeting A–C: Claude 1 of 3, reader 0 of 3. First-attempt refusals: none.
Grounding errors as the rule defines them: none (both readers). The reader identified all six arms correctly from the answers. The
two disagreements are judgement calls that do not move the verdict. **PASS** by both readers.

## What it shows and what it does not
- **What the link changed:** every linked v9 answer, every day, took Bloomberg's $393B total-revenue projection (e195, in v14's
  conclusion) as its reference and translated it at the reported 92% mix, saying it is not a Data Center consensus; two of three sized
  their forecast from v14's forecast. The controls had no market figure for the segment and built a run-rate from the Q2 total guide,
  then added uplifts they did not size ($14B, $48B, an unstated second-half growth).
- **The stored annual contradiction did not recur.** On 07-12 the stored run had Data Center $400–410B against a total of $387B. In all
  three fresh controls the total rose to ~$411B on 07-12, so the annual Data Center figure stayed below it. What remains in the controls
  is in the second half, which C as written cannot see (v14 states no second-half quarters): control-2 implies a Data Center second half
  above the company's ($245.75B against $239.4B); control-3 leaves the rest of NVIDIA about $2.6B for the half against $6.35B in Q1.
- **The verdict rests on B for the controls.** Read leniently (a disclosed but unsized uplift counts as supported), all three controls
  reconcile and the result is inconclusive. Both readers failed control-2 and control-3 on B as written.
- **Coherence is not accuracy:** the linked forecasts inherit v14's growth assumption and carry the Q1 mix forward.
- **Scope:** one draw-window of three days, one pair, the market figure in hand for the total from the start. It says nothing yet about
  other pairs, a whole run, or what links the matcher chooses elsewhere.

## Added after the result (2026-11-21, while designing D699): the link's margins
The three linked sequences each asked Jev the 07-10 opening of v14 against v9 afresh (the same request, sha 6dcb7664…; answers in
each sequence's archive, call 8738). "v9 reads v14" won with 0.52, 0.54 and 0.51; "v14 reads v9" had 0.47, 0.45 and 0.48. The rule
accepts Jev's choice at 0.5 or more, so a shift of about 0.02 gives no link or the opposite link. The same opening's v14–v8 pair
(stand-alone CPU) had "v14 reads v8" at 0.47, 0.46 and 0.44 (below the line, no link). "Chosen in 3 of 3" above is true, but the
direction was close to a coin flip; the whole-window design measures this class before buying any judgement
(`docs/research/2026-11-21-whole-window/DESIGN.md` §3).

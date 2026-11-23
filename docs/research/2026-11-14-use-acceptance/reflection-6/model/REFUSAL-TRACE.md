# Sol's 24 refusals traced at $0 (D630), 2026-11-16

Source: `refusal-trace.txt`, each sol refusal with its reason, the two families' N marks and luna's matched answers.

| Topic | Sol refusals | N (Codex / Claude) | Luna's answers | Sol's reason |
|---|---:|---|---|---|
| fortnight c1/clean-8 (robotics venture funding) | 2 | holds / holds ×2 | 3 refusals | no listed theme covers it: **justified** |
| week c1/clean-12 (global AI capex 2026 and 2027) | 3 | holds / holds ×3 | 3 refusals | two annual figures, neither main: **justified by both** |
| week c1/clean-4 (hyperscalers' capex 2026 and 2027) | 3 | holds / holds ×3 | 3 refusals | the same: **justified by both** |
| fortnight c1/clean-13 (CPO shipments) | 3 | 1 split, 2 fails / fails | 3 ladders, all faulted (L) | "Q4 2026 through 2027 … several checkpoints rather than one main annual figure" |
| week c1/clean-5 (Hugging Face) | 1 | fails / fails | 3 clean ladders | "closing, consideration and regulatory conditions, none the main one" |
| week c1/clean-3 (AI-server memory prices 2027) | 3 | 1 both fail, 2 split | 3 clean ladders | "HBM and DRAM are distinct series … selling prices and margins, none the main one" |
| fortnight c1/clean-3 (Blackwell into China) | 3 | holds / fails ×3 | 3 ladders, all faulted (L) | "U.S. approval and Chinese acceptance, neither the main one" |
| week c1/clean-11 (Reflection AI) | 3 | holds / fails ×3 | 3 clean ladders | "signing, completing, consideration, conditions, none the main one" |
| week c1/clean-13 (equity commitments) | 3 | holds / fails ×3 | 1 ladder, 2 refusals | "remaining balance, cash paid, changes, none the main one" |

**One mechanism behind every unjustified or disputed refusal:**
- Sol applies the decline case "naming several with none of them the main one" whenever the topic's outcome lists several parts.
- It does so even when the topic's description asks one of them, and the others are comparisons, details or second sides.
- **All 4 agreed-unjustified refusals are this mechanism** (CPO ×2, Hugging Face, memory prices), and so are the 12 disputed ones (count corrected in council round 11). Their stated reasons differ, though (a span of checkpoints, two price series, two authorities), so one shared instruction is a lead, not a proven cause.
- The 8 refusals both families call justified are a different case: another matter, or two annual figures.

**Where the request leaves the gap.** The frozen system text says "Judge the one the topic's outcome names as what is tracked". It
assumes the outcome names one thing, and says nothing on how to find the main one when it names several. The readers find it in
the topic's description ("The description asks …").

**The source for a repair.** D436, in Alex's words: "a second side of the same bet … is one question, with the second side shown as
not judged". The repair names where the main part is found, and does not add a rule. Luna, which picks the leading part, faults L on
those topics in 6 of 9 sends: it picks the part but leaves others unlisted.

# Merging the two systems: the council's design and its small test (2026-11-19)

**Sources:**
- Claude's proposal (`claude-proposal.md`), written first;
- Codex's independent design (`council-a-codex.md`, thread 01a1f606…);
- one challenge round (`council-b-codex.md`), which ended in consensus.

## The merge
| Piece | From | Measured reason |
|---|---|---|
| Opening questions, and their answer choices | Old (v118 proposals, matcher, duplicate check) | It serves 10 of 32 frozen matters, against 2–3. Its choices are kept when they pass the clean range, reference and direction checks |
| A refused proposal | — | Stays out of the open list. This is the refusal-cascade lesson |
| Reading and extraction | Clean Step 1 (c8), given the old system's accepted questions as its open list | It keeps more of what matters (211–214 against 162–171 of 234) |
| Earlier versions, repeats and unlinked facts | Clean Steps 2–3 and D383 | 141 of 143 earlier versions found; repeats grouped with each source kept; useful facts kept |
| Judging and closing | The frozen judge (the same in both) | Differences come only from what reaches it |

- **The figures.** Under D382/D505, NVIDIA's own figures inform the related questions. Standalone revenue and margin questions need Alex's
  exception.
- **Ceilings** on the stored results: 6 of 32 under D382/D505; 10 with the exception.
- **The main risk is meaning drift.** A question about four-company 2026 data-center capex could take five-company, 2027 or total-spending
  figures as its answer.

## The small test (consensus; awaiting Alex's approval)
- **Articles:** the 11 frozen articles of 09-07..09-20 behind M04 (four-hyperscaler 2026 capex) and M17 (the Anthropic anchor
  investment), plus article 223 as a control for five companies and 2027.
- **What runs:**
  - the 12 articles are re-sent through c8 against old-2's and old-3's question lists as they stood at the start of each day, with the old
    answer choices and the history to 09-06 kept;
  - one frozen-judge request per question per run is built from the evidence c8 filed, giving 4 answers;
  - both card readers judge the 4 answers blind, beside the archived old answers.
- **Pass lines, written now:**
  1. All 4 judge requests carry the decisive, source-verified passages that c8 filed.
  2. No five-company, 2027 or total-spending figure is offered as a direct answer to four-company 2026 data-center capex.
  3. The Anthropic talks stay unconfirmed: talks are not a signed commitment.
  4. No standalone NVIDIA financial question is proposed, including on article 181, which carries NVIDIA's revenue.
  5. Both readers support all 4 answers.
- **Attainable:** 4 of 4 deliveries and up to 4 of 4 supported answers. The passages exist in both clean runs.
- **Cost:** $0.33–0.42 before retries, from archived token use: 24 c8 calls and 4 judge calls.
- **It cannot decide:** automatic opening, repeat grouping, performance over the full window, or release readiness.

# Paid acceptance probe of judging-v12: result (D718)

**Registered verdict: NOT READY** (`probe_read.py verdict`, PROBE-DESIGN.md v5 §3):

> confirmed material harm in Part C: linked-1:8776 (b)

- **Spend:** $0.274 of Alex's $0.50 (D715).
- **The run:** 122 sends, all answered. No ledger stop, no comparison left unstarted or interrupted. A2 (the sealed 647-id request) was
  skipped by its headroom rule: $0.226 left against $0.247 for three attempts. That request size stays unverified.
- **Folder:** `poc/data/citation-probe-2026-11-22/`.

## The harm that decides it

On linked-1:8776 (total revenue, linked run), v12 answers #2 and #3 name Bloomberg for the $393 billion reference. Each cites only
e669, which is Wall Street's average via Yahoo Finance, also $393 billion; neither cites e195, which is Bloomberg. All three v7
answers cite e195. The figure and the rung held, but the citation does not support the source the answer names. That is repeated in 2
of 3 v12 answers against 0 of 3 v7.

**How it was read:**
- Claude's first reading called it an uncited provenance label, not a harm. That reading is superseded.
- The blind reader (Codex) called it harm (b).
- The disagreement went to a panel registered before it answered: one fresh Codex and one fresh Claude adjudicator, a class standing
  only if both gave it. Both decided harm (b) confirmed.
- e577, cited by those answers, gives FY2026 revenue and does not carry the Bloomberg figure.

## Beside the verdict (it does not change it)

**What v12 was built to fix** (Part B, the 16 requests that produced 17 refusals under v7, 3 draws each):
- 48 of 48 answers were format-valid and passed the request-time check;
- there were 0 misattributions;
- every material target had valid support in all three draws: the Kyber delay (e41, e42), the signed agreement (e3768), the $393
  billion reference (e669) and Zacks' 85.4% (e3620);
- all 24 placement readings were correct: themes only in theme pushes, the dependency only in `cites_views`;
- the four non-material readings of e2769 and e693 are "omitted" after adjudication.

**Part C** (12 matched comparisons, 3 v12 and 3 v7 answers each):
- 0 refusals, including the v7 controls;
- the 72 rungs are identical across arms;
- references and outcomes match;
- v12 cited fewer entries on average: 12.7 against 14.0 per answer (cited or pushed, 14.2 against 23.1). Some v7 answers list every
  entry shown (122 of 122, 45 of 45).

**A screen for unsupported source names** (an outlet named in the text that no cited entry or cited dependency names; $0;
hand-checked):
- Part C: v12 2 of 36 (8776 #2 and #3) against v7 1 of 36 (8776 v7 #3 names Zacks' 80% citing neither Zacks entry).
- Part B: v12 1 of 48 (8807 #1, "Bloomberg/Yahoo Finance", cites e669).
- All three Part C flags come from one request. The slip exists in both formats; these counts cannot tell whether v12 raises it.
- The screen also misses a wrong attribution when another cited entry names the same outlet for a different claim.
- A first version of the screen mis-flagged linked-1:8768: the Bloomberg figure there is carried by the cited dependency v14, which
  that version skipped. Corrected before this report.

## Council B (round 42, `codex-r42.md`)

- The verdict is reproduced and the adjudication agreed.
- Recommendation: keep poc-v118; judging-v12 is not adopted.
- Corrections taken: the screen's name and limits; "fewer entries on average" in place of "one source per claim"; Claude's first
  reading marked superseded.
- A follow-up would need:
  - fresh requests where one figure is attributed to different sources;
  - paired production-text sends under both formats;
  - blind checks of which source supports each named claim;
  - an acceptable increase agreed in advance;
  - a size set by distinct requests;
  - dropped claims counted.
  Repeating the disputed request cannot settle adoption.

## Process record

- **Council rounds:** 38 to 38d (design), 39 to 39c (build), 40 to 40f (probe design), 41 to 41e (harness), 42 (result).
- **Frozen inputs, fixed before the first send:** `probe-targets.json` (amended twice before any send) and `stored-v7-support.json`.
- **Readings:** `readings-claude.json`, `readings-codex.json`, `readings-final.json`.
- **Adjudication:** `adjudication-case.json`, `adjudication-preregistration.md`, `adjudication-codex.md`, and the Claude adjudicator's
  report, given in D718.

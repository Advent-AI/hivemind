# From the split prototype to production: plan v4 (after round 4)

Plan v3 stands except where this version changes it. Round 4 (`r4/codex-review.out`): disagreements 3, 4 and 7 resolved; 1, 2, 5 and 6 partly;
two new points. Changes below, each with the stored-data check behind it.

## 0. Answers to round 4

| Round-4 point | v4 |
|---|---|
| **Blocker 1**: merged meanings must reach each affected daily judge, not only the stored record | The merged record's summary carries each distinct summary; the judging request prints one summary line per piece (`src/hivemind/views/judging.py` line 130), so each linked question's judge reads both. Accepting test (C-1): the control-3 sentence through the real writer, then the judging request built at $0 for v2 and for v10 contains the total-revenue and the data-center statement with their source fields; a mutant keeping one summary fails |
| **Blocker 2**: every real entry point | Only `scripts/replay.py` writes a ledger; `scripts/hivemind_api.py` and `scripts/hivemind_mcp.py` read one (no ingestion route; round-1 production review §1). C-7 tests: replay as a user calls it with the split configuration and its defaults, on a temporary ledger with fake transports, writes through the split path; the API and MCP readers serve a split-written ledger (research subjects, groups, keys, merged records) without error and with the stored values; any future ingestion entry point must call the same coordinator |
| Serious: actual judgement reasons for the double-growth cases | C-4 adds: rebuild the frozen judging requests of v79 and v84 with the ladder the corrected record preparation writes, send them (a few cents) and read the reasons; the line stops if the judge still applies growth to a figure that already contains it, and that goes to Alex (judging frozen, D354) |
| Serious: attribution conflicts must not default to B | Counted on stored runs: 16 of the 17 duplicate groups differ in an attribution field, almost all in convention (A's record preparation writes "NVIDIA management, as reported by the article", B writes "fool.com (analyst)" for the same speaker); 3 differ in substance (1240 and 1249 original source; 1251 original day). Mechanism: the record-preparation call describes speaker, original speaker, original day and tier in its own words, not with the evidence schema's field definitions B uses (role-v74i schema). Change: record preparation uses those same field definitions (one owner for attribution). Merge rule: pieces merge only when the attribution fields agree after that; a remaining disagreement keeps both pieces and is recorded for review, with no precedence for either side. Test: the three substantive cases stay separate and flagged; convention-only cases merge once the definitions are shared (a changed request: small send after the audit) |
| Serious: what each acceptance measurement proves; how the seeded fixture runs | C-8 states it (below) |

## C-8 Acceptance (replaces v3's C-8)

Both measurements are needed; neither replaces the other.

1. **Historical comparison on the frozen ruler** (AGENTS §5, §7.1). What it proves: the split against the frozen production configuration on
   the ruler both were measured on: extraction on golden-v5 dev and test (D372 counting: core and supporting helpful, not-kept unhelpful,
   optional neutral; D373 disclosure of the disputed entries), questions against must_open / may_open, the judgement at 2026-07-14 against reader
   B. What it cannot prove: behaviour from an empty or real starting library. How it runs: a measurement harness calls the production split module
   and the real round code with the frozen seeds as its starting ledger, labelled as a measurement fixture; `scripts/replay.py`'s refusal of seeded
   ledgers stays for production runs (D370). Criteria: written and hashed before the run, from the frozen production configuration's same-day
   control (three draws each), regressions first.
2. **Production-shaped run, unseeded, on a held-out window.** What it proves: the product path from a real starting library: library-level question
   recall by day and per-item losses, evidence delivered to the right question and received by its judge, judgements eligible, produced and correct,
   attribution and meaning by field, cost and wall-clock per item and per day. What it cannot prove without a reference: completeness. A reference
   built from the complete sources before outputs are seen is a new ruler piece: Alex opens it or the run reports only what independent readers
   checked. Criteria written and hashed before the run; three draws; every draw and regression reported.

Alex decides: authorising the seeded fixture for measurement; whether to open a held-out reference; the criteria's thresholds.

## Unchanged from v3

§1 C-1 to C-7 (with the additions above), §2 diagnosis classes, §3 items for Alex (the attribution-convention finding added to §3.5 is not a
production change).

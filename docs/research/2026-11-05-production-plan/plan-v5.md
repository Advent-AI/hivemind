# From the split prototype to production: plan v5 (after round 5)

Plan v3 as amended by v4 stands except where this version changes it. Round 5 (`r5/codex-review.out`): the entry points and the double-growth
check resolved; one blocker (conflicting attribution) and one serious point (what the unseeded run can claim; comparability of the seeded
fixture) remain.

## 0. Answers to round 5

**Blocker: conflicting attribution on one quoted statement.** v4's "keep both pieces" is withdrawn: it stores two versions of one statement and
departs from PRD 10 §5 item 2 ("one record linked to both questions").
- One record per quoted statement, always. Its attribution (speaker, original speaker, original day, tier) has one owner that reads the source:
  record preparation, which already runs after A and B in the same item, reads the whole article and uses the evidence schema's field definitions
  (v4). For a B passage whose quote equals one of A's passages, record preparation receives B's version beside A's and returns one attribution
  for the statement from the source; the record stores that attribution, the links of both, and each distinct summary; both submitted versions are
  kept in the handover for audit. No precedence rule for either side; no extra call (record preparation runs whenever A has passages, and a
  duplicate needs A to have one).
- Must prove: 1240 (author versus the reported data set), 1249 (author versus an unspecified market estimate) and 1251 (empty versus the
  publication day for the author's own estimate) each produce one record whose attribution an independent reader confirms against the source;
  the judging requests built at $0 for each linked question show that attribution and both summaries; a mutant that keeps two records, or one
  side's fields unread, fails. A changed request: a small send after the record-preparation audit.

**Serious: what the measurements can claim.**
- The unseeded production-shaped run without a reference reports what independent readers checked: errors found in the written records, their
  links and the judgements they read, and the inputs they read in full; it does not report question recall or per-item losses for the window.
  Those need a reference built from the complete sources before outputs are seen, a new ruler piece only Alex opens; with it, recall by day and
  per-item losses are counted against it.
- The seeded comparison's comparability is shown before any send: its harness replays the stored answers of one existing frozen-configuration
  acceptance draw (`docs/research/2026-11-01-e2e-loop/arms/r10-control-v108/d1` in the main checkout, which holds its `archive.sqlite` and `views.sqlite`; a v108 control of the 2026-11-05 acceptance; this worktree has only its manifest) through the real
  round code from the same seeded starting ledger and must reproduce that draw's stored ledger (questions, evidence, links, judgements); the split arm
  then starts from the byte-identical starting ledger (hash recorded). Only then are the same-day control and the split arm sent, three draws each.

## Unchanged

v3 §1 (C-1 to C-7, with v4's additions), §2, §3; v4's C-8 with the wording above replacing its unseeded-run claims.

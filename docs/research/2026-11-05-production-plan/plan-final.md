# The split extraction: agreed plan for production (Claude and Codex, after six rounds)

Agreed on 2026-11-05 after six read-only Codex review rounds and Claude's checks on stored data; the whole exchange is in `review-log.md`.
This file consolidates `plan-v3.md` as amended by `plan-v4.md` and `plan-v5.md`; Codex's round-6 verdict: "Apart from the choices the plan sends
to Alex, I agree … as the plan to execute. The proposed checks still have to pass." Nothing below is built or proven yet; nothing is re-run
before Alex has taken the decisions in §4.

## 1. What we are taking to production, and what is wrong with it today

The split reads every item with two calls on the same snapshot of the questions open before it (D375, all-open): A proposes new questions with
their passages, B files passages under existing questions; record preparation fills subject, dates, attribution and ladders for A's questions; Jev
matching with the analyst review, the real writer and the daily judging follow. On the first 100 items it opened far fewer wrong questions than the
stopped run (a blind reader: 24 of 35 → 3 of 22), filed none under an invented subject, and gave most numeric questions a ladder. The census of
the confirmation run (`r2/census-findings.json`, 126 findings over 75 items, to be reconciled by source matter) and the reviews show what blocks
production: one statement stored twice; groups never declared; long items silently truncated; inverted or miscomputed ladders and a reference that
made the judge count growth twice; B filing under broad questions and parking weak links; attribution and meaning errors; questions that never close;
and a prototype that lives in a research script with no recovery contract, no preflight and no frozen version.

## 2. Contracts, in order (each: what it must prove; its $0 proof; its accepting test)

**C-1 Handover: one statement, one record, every home that takes it.**
- One record per quoted statement (PRD 10 §5 item 2). Its summary keeps every distinct summary merged into it with the links each came with.
  Its attribution (speaker, original speaker, original day, tier) has one owner reading the source: record preparation, which runs after A and B,
  reads the whole article and uses the evidence schema's field definitions; for a B passage equal to an A passage it receives both versions and
  returns one attribution; both submitted versions stay in the handover for audit.
- A carries B's and role-v74i's unit rule ("One evidence item records one statement …"); whether that removes the contained-quote pairs is measured.
- B's no-home passages go to record preparation, which may link each to an A question of the same item; code keeps a passage only when linked.
- Must prove: no statement loses its meaning, its attribution or a home that takes it; candidate survival, merge and rejection each leave the right
  final links. $0: every stored handover of the three v2 runs through the real writer on temporary ledgers (1207, 1211, 1275, 1240, the control-3
  sentence `poc/data/parallel-b-link-2026-11-05-v2/gnews_3df0bbc8aff2c1d008bc0a32-control-3/result.json`; 1207's candidate surviving, merged and
  dropped). Tests: the control-3 sentence gives one record with both summaries and links, and the judging requests built at $0 for v2 and v10 each
  show both statements and their source fields; 1240, 1249 and 1251 each give one record whose attribution an independent reader confirms against the
  source; 1240's Apple passage reaches the TSMC question; mutants keeping one summary, two records or one side's fields unread fail.

**C-2 Groups, as PRD 05 already assigns them.** A declares new groups and group references where the grouping contract calls for them; matching
and the writer resolve them. Must prove: a deal creates or joins its group; a company's own financial line carries none; an existing group is joined
and found again after a restart.

**C-3 Complete input.** No silent truncation (400,000 characters today, in both paths; 7 of 34,084 corpus items exceed it; 1280 in the first 100).
Alex chooses sections or refusal; must prove either 1280's later note reaching A and B, or an explicit refusal with the item not marked complete.

**C-4 Record preparation.**
- Subject from the listed ids or `new` (built). Attribution fields with the evidence schema's definitions (C-1).
- Admission reason from the standard's five (D184), each reason's checks in code with or without a ladder: an annual quantity this or next year; an
  obligation not yet signed checked within 18 months, one already assumed at the next annual filing (D210); events by their dates. Missing
  material or dates never reject (the unnumbered 2026-11-05 record); a claimed settling material is stored and a known mismatch flagged.
- Target period: a bare prepared year is read as fiscal only when the question names that same year as fiscal; tested with target and comparison
  years in both orders and a wrong or missing prepared year.
- Ladders: `favourable_end` (D186, D368); code-ordered rungs, monotonic bounds, intervals rendered from the bounds, bounds recomputed from a stated
  base and percentage (1280's 5% band must fail). The reference is an open list ("such as guidance, a consensus or analyst estimate, the last reported
  figure for the same quantity, a stated target"); the part-period pace sentence is withdrawn. Floors are diagnosed before any rule: 1249, 1253 and
  1273 re-judged on the same evidence with two ladder variants (the floor as the boundary between the neutral and favourable rungs; the prior
  period's figure as the reference with the floor stated in its rung) and the judge's own account; a needed change to the frozen judge goes to Alex.
- The double-growth cases: the frozen judging requests of v79 and v84 rebuilt with the corrected ladder and sent (cents); the line stops and goes
  to Alex if the judge still applies growth to a figure that already contains it.
- Must prove on stored answers: 1239 and 1273 refused or reordered, 1280 refused.

**C-5 Day runner under D375 and the state × event contract.** Sequential items, A and B in parallel, as the reference implementation; the table
(drafted in `r1/codex-production.out` §3) names each transaction (archive record, savepoint, round commit, subject registry), the saved request and
snapshot, the day resumed judging uses, and the outcome for a refused retry, a crash between each stage, a configuration change, a corrected input,
a competing writer and a limit-cut day. Tests: item 2's A and B both see item 1's committed question; each event behaves as the table says; a cut day
is never marked complete. Speculative preparation only after a replay shows identical accepted requests and ledgers and counts the discarded calls.

**C-6 Preflight.** Reconstructs every A, B and record-preparation request from the stored source and snapshot, compares wire bytes, replays the
checks and the handover, reports skipped and unexercised checks, fails on an empty population. Test: an altered source, snapshot or answer is refused.

**C-7 The versioned production path.** A module in `src/hivemind`; prompt files for A, B and record preparation; a configuration version naming them
(D359); `scripts/replay.py` selects it by configuration (the only ledger-writing entry point; `hivemind_api.py` and `hivemind_mcp.py` read ledgers).
Durable research subjects in the ledger (id, name, kind, aliases; created in the item's transaction; competing creation resolved by identity, not text
hash alone). Freeze tests for the version's prompt bytes, schemas and checksum. Tests: stored answers replayed through the moved code give
byte-identical requests and identical handovers; replay as a user calls it (split configuration, defaults, fake transports, temporary ledger) writes
through the split path; the API and MCP serve a split-written ledger; after a restart a research subject keeps its id and reaches the next item's A,
B and matching. The research runner retires.

**C-8 Acceptance (defined, written and hashed before any run; both measurements needed).**
1. Historical comparison on the frozen ruler: extraction on golden-v5 dev and test (D372 counting, D373 disclosure), questions against must_open /
   may_open, the judgement at 2026-07-14 against reader B. A measurement harness calls the production split module and the real round code with the
   22 frozen seeds as a labelled starting fixture (`replay.py`'s refusal of seeded ledgers stays). Comparability first: the harness replays the stored
   answers of the v108 control draw `docs/research/2026-11-01-e2e-loop/arms/r10-control-v108/d1` (main checkout) from the same seeded ledger and must
   reproduce its stored ledger; the split arm starts from the byte-identical ledger. Then three draws each of the split and a same-day control.
2. An unseeded production-shaped run on a held-out window, three draws: without a reference it reports what independent readers checked (errors in
   written records, links, judgements and the inputs they read in full), cost and wall-clock; question recall by day and per-item losses need a
   reference built from the complete sources before outputs are seen, a new ruler piece only Alex opens.

## 3. Quality classes to diagnose before any prompt change (AGENTS §1, §6)

Reconcile the census into one row per source matter and mechanism. Then, per class, the request sentence, the standard's line, a verdict and the
model's account, before a single change and its proof: B's broad-only and wrong-period filings (accounts: 1211 a misread, 1246 the other-period rule
applied inconsistently); the 1210 total filed as a narrower amount, separately from A's narrow question wording; attribution, amount meaning, period
and uncertainty by field; unverifiable questions (an independent reader on the claimed materials: unknown, known not reported, supported); A's and B's
source-supported omissions (1209, 1210, 1228, 1234, 1252, 1266, 1280; 1242, 1246, 1255, 1259, 1267), measured per item and in the library by day;
coarse and fine readings (merge only where the surviving ladder carries the finer outcome; true alternate wordings as controls); D197 on spending of
another scope (labelled same-theme pairs, D190's A17 as the merge control); deal stages (one deal one question, with D210's exception, in A and the
review; a signing-versus-programme pair and a same-deal control through the writer).

## 4. Decisions for Alex

1. **Acceptance arrangement (C-8).** Authorise the seeds as a measurement fixture for the historical comparison; decide whether to open a held-out
   reference for the unseeded run; the criteria's thresholds.
2. **The evidence call's fallback sentence** (D273, kept by D361): every new company-wide revenue question becomes another place weak links are
   parked (confirmation run: existing-question passages helpful 16 of 30).
3. **All-open context at scale** (decided; numbers for him): about 150 input tokens per open question per call (87 open questions ≈ 16,200 tokens);
   500 open questions ≈ 75,000 tokens a call; the failure mode beyond one request.
4. **A check-date policy** for questions without an exact source date (all 22 in the confirmation run), after the lifecycle table (estimated date,
   material arrived or not, no ladder, end-of-day closure, later research).
5. **Production findings outside the split:** `sift`'s identical-quote merge keeps only the first summary; D266's run-on rule keeps a summary its
   passage does not support; matching uses the publication day as the statement day when the original day is unknown; Jev marks a passage a repeat on
   a partial overlap; the 400,000-character truncation.
6. **Long items:** sections or refusal (C-3).
7. **Promotion** of the accepted split version to the default (D359).

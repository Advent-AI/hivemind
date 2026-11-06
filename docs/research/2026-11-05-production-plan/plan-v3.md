# From the split prototype to production: plan v3 (after round 3)

Replaces v2. Round 3 (`r3/codex-review.out`) found seven remaining disagreements; this version answers each (§0), restores the production-path
gates v2 dropped, and states every accepting test as what it must prove about meaning, not counts. Causal claims from my probes are leads only.

## 0. Answers to the round-3 disagreements

| # | Round-3 point | v3 |
|---|---|---|
| 1 | Merging identical quotes as `sift` does drops a second statement's summary (`poc/data/parallel-b-link-2026-11-05-v2/…control-3/result.json`: one sentence, a total-revenue summary for v2 and a data-center summary for v10; `sift` keeps the first) | One stored record per quote (PRD 10 §5 item 2: "code stores two items that quote the same sentence as one record linked to both questions"), whose summary keeps every distinct summary merged into it, each beside the links it came with; when the merged versions disagree on speaker, original speaker, original day or tier, the record keeps B's fields (the evidence call carries the tier rules) and the conflict is recorded and counted, never silently resolved. Accepting test: the control-3 sentence yields one record carrying both summaries and both links; a mutant that keeps only the first summary fails. The same gap in production's `sift` is reported to Alex (§3.5) |
| 2 | Split-aware preflight, versioned entry points and freeze checks missing from v2 | Restored as C-6 and C-7 (§1) |
| 3 | An open-ended floor cannot be the neutral rung's span; the judge's role is unproven | Withdrawn as a rule. Diagnose first: the floor cases (1249, 1253, 1273) re-judged with the frozen judging request rebuilt on the same evidence and two ladder variants (the floor as the boundary between the neutral and the favourable rungs; the prior period's reported figure as the reference with the floor stated in its rung), and the judge's own account. The judge is frozen (D354): if its behaviour must change, that goes to Alex with the evidence |
| 4 | Refusing a supported run-on passage conflicts with D266 | Follow D266 as decided: keep the copied passage. Its summary and attribution may describe the dropped continuation (1243, 1210): counted on the three stored cases and reported to Alex as a gap in D266 itself (§3.5), not changed by me |
| 5 | Missing evidence, meaning, target periods, subject identity and final judgements not proven | Acceptance by field (C-8): an independent reader compares the source with each written record (speaker, original speaker, day, period, amount and its meaning, uncertainty, subject) and with what the daily judge received; durable subject identity has its own restart test (C-7) |
| 6 | Acceptance lacks independent, predeclared evidence of recall, filing and judgement | C-8 defines the two measurements Alex chooses between before any run: inputs, the complete-source reading made before outputs are seen, three draws, a same-day control, prewritten criteria and stop conditions, and the counts (per-item losses and library state by day, evidence delivered to the right question, judgements eligible, produced and correct). A reference built from complete sources for the unseeded run is a new ruler piece (AGENTS §7.1): only Alex opens it |
| 7 | Causal claims beyond the probes | Restated: the plural probe (2 sends × 5 items × 2 arms) shows variation and no reliable effect, too small to rule one out; B's accounts and A's missing unit rule are leads to the mechanism, to be confirmed by the prompt audit and small sends, not causes |

## 1. Contracts, in order (each: what it must prove, its $0 proof, its accepting test)

**C-1 Handover.** Identical quotes as §0.1. A gets the unit rule of B and role-v74i ("One evidence item records one statement …"); whether that
removes the contained-quote pairs is measured, not assumed. B's no-home passages are given to record preparation, which may link each to an A
question of the same item; code keeps a passage only when linked. Must prove: no stored statement loses its meaning or a home that takes it;
candidate survival, merge and rejection each leave the right final links. $0: replay all stored handovers of the three runs through the real
writer on temporary ledgers (1207, 1211, 1275, 1240, the control-3 sentence; the 1207 candidate surviving, merged and dropped). Test: as §0.1,
plus 1240's Apple passage reaching the TSMC question when preparation links it (a changed request: a small send after the audit).

**C-2 Groups (PRD 05's contract, decided).** A declares new groups and group references where the grouping contract calls for them; matching
and the writer resolve them. Must prove: a deal creates or joins its group; a company's own financial line carries none; an existing group is
joined and still found after a restart.

**C-3 Complete input.** No silent truncation. Alex chooses sections or refusal (7 of 34,084 corpus items exceed 400,000 characters; 1 in the
first 100). Must prove either 1280's later note reaching A and B, or an explicit refusal with the item not marked complete.

**C-4 Record preparation.** Subject from listed ids or `new` (built). Admission reason (D184's five) with each reason's checks in code with or
without a ladder: annual quantities this or next year; an unsigned obligation within 18 months, an assumed one at the next annual filing (D210);
missing material or dates never reject (the unnumbered 2026-11-05 record); a claimed settling material stored and a known mismatch flagged.
The target period: the prepared year is reinterpreted as fiscal only when the question names the same year as fiscal; tested with target and
comparison years in both orders, a wrong and a missing prepared year. `favourable_end` (D186, D368), code-ordered rungs, monotonic bounds,
intervals rendered from the bounds, and the bounds recomputed from a stated base and percentage when the condition states one (1280's 5% band
must fail). The reference: pace withdrawn; an open list ("such as guidance, a consensus or analyst estimate, the last reported figure for the
same quantity, a stated target"); floors per §0.3. Must prove on stored answers: 1239 and 1273 refused or reordered; 1280 refused.

**C-5 Day runner (D375) and the state × event contract.** Sequential items with A and B in parallel as the reference. The table names each
transaction (archive record, savepoint, round commit, subject registry), the saved request and snapshot, the day resumed judging uses, and the
expected outcome for a refused retry, a crash between each stage, a configuration change, a corrected input, a competing writer and a limit-cut
day. Tests: item 2's A and B see item 1's committed question; each event as the table says; a cut day is never complete.

**C-6 Preflight.** Reconstructs every split request (A, B, preparation) from the stored source and snapshot, compares the wire bytes, replays the
checks and the handover, reports skipped and unexercised checks and fails on an empty population. Test: an altered source, snapshot or answer is
refused.

**C-7 Versioned production path.** `src/hivemind` module for the split, prompt files for A, B and preparation, a configuration version that names
them (D359), replay selecting it by configuration; the research runner retires. Durable research subjects in the ledger (id, name, kind,
aliases; created in the item's transaction; a competing creation resolved by identity, not by text hash alone). Freeze tests for the version's
prompt bytes, schemas and checksum beside the existing ones. Tests: byte-identical requests and identical handovers when the stored answers are
replayed through the moved code; after a restart a research subject keeps its id and reaches the next item's A, B and matching.

**C-8 Acceptance (defined before any run; Alex chooses).** (a) Historical comparison on the frozen ruler with the 22 seeds as a labelled
measurement fixture (golden-v5 dev and test, D372 counting, D373 disclosure, reader B's judgement gold); (b) an unseeded production-shaped run on
a held-out window. For each: inputs frozen, predictions and stop conditions written and hashed, three draws and a same-day control, every draw and
regression reported; counts: per-item losses and the library's questions by day, evidence delivered to the right question (and what the daily
judge received), judgements eligible, produced and correct, attribution and meaning by field. A complete-source reference for (b) is a new ruler
piece only Alex opens.

## 2. Quality classes still to diagnose before any prompt change (AGENTS §1, §6)

Reconcile the census first: one row per source matter and mechanism, overlapping entries merged, with the list behind each count. Then, per
class, the request sentence, the standard's line, a verdict and the model's account: B's broad-only and wrong-period filings; the 1210 total filed
as a narrower amount (B) and A's narrow question wording, as separate mechanisms; the fallback parking (Alex); attribution, amount meaning,
period and uncertainty; unverifiable questions (independent reader on claimed materials); A's and B's source-supported omissions (1209, 1210,
1228, 1234, 1252, 1266, 1280; 1242, 1246, 1255, 1259, 1267); coarse/fine pairs (the surviving ladder must carry the finer outcome, or the merge
is not right for that pair); D197 on spending of another scope (labelled pairs, D190 A17 as the merge control); deal stages (the amended wording
in A and the review, a signing-versus-programme pair and a same-deal control through the writer).

## 3. For Alex (options and a recommendation each, once agreed)

1. Acceptance arrangement (C-8). 2. The fallback sentence (D273, D361). 3. All-open capacity and cost (about 150 input tokens per open question
per call) and the failure mode beyond one request; the decision stands until he changes it. 4. A check-date policy, after the lifecycle table.
5. Production findings: `sift`'s identical-quote merge drops a second summary; D266's run-on keeps a summary its passage does not support;
matching's publication day as statement day; Jev's partial-overlap repeats; the 400,000-character truncation. 6. Long items: sections or refusal.
7. Promotion of the accepted version (D359).

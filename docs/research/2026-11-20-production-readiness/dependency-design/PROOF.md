# The $0 proof of the linking version (D694, D695), for the council before the July send

Built (working tree, not committed): `src/hivemind/views/links.py` (new); `views/round.py` (the link step between matching and the
`matched` marker, `link_selections` records); `views/writing.py` (`proposed_links`, `_write_links`); `views/store.py` (`dependencies.kind`,
`link_selections`, `direct_parents` skips `reads`, `current_state` returns the stance fields); `views/judging.py` (`judging-v8`, the full
dependency block); `config.py` (`jev-links`); `parallel_day.py`; `research_context.py` (explicit columns); `scripts/replay.py` and
`clean-arch/e2e-comparison-2026-11-13/budget_replay.py` (refuse `jev-links` and a harness-only ledger); `prompts/judging-v8.txt` (byte
copy of v7); `poc/config/poc-v119.json`.

| Check | Result | Record |
|---|---|---|
| the whole suite | 378 passed (the rollback test now checks the state before the test's own rollback) (346 before; `tests/test_links.py` 31; one new pin test) | `python3 -m pytest -q` |
| mutants | 7 of 7 caught, each control passing; the harness-ledger mutant's failure read: the refusal message is missing | `mutants.py`, `mutants.log` |
| frozen pins | v7 pins unchanged; v8 file sha = v7's; v8 schema = v7's; the link questions pinned | `tests/test_frozen_questions_and_judgement.py` |
| the July starting state | old-2 rebuilt to the end of 07-09 under poc-v118, every request from the archive; equal on views, keys, rungs, evidence, links, judgements (with cites, changed, reference, implied outcome, request sha), switches, successions, dependencies. Each sequence's copy is checked again against old-2 (the same comparison) and for its last completed day 07-09 before any transport is built | `rebuild_control.py`, `rebuild-control.log`, `july_test.prepare` |
| poc-v119 with no link reproduces the prefix | equal on the same tables; 3 link requests asked before 07-10 (answered neither), eligible pairs listed | `july_test.py prefix`, `prefix-v119.log` |
| the archive (an archive test) | 145 v9/v14 judge rows retired; exact old v9 and v14 requests go to the transport; an exact old v8 request is answered from the archive with its call id; a retired answer is not returned again | `july_test.py archive` |
| the dry run (fake answers with a marker unique to sequence, question and attempt) | all checks true: in all four sequences each v9 and v14 request carries exactly its previous accepted answer (v9's first: old-2's 07-09 answer; v14's first: none); in the linked ones each v9 request shows exactly that day's accepted v14 comparison point and forecast; the link "v9 reads v14" (`first_is_bullish`, seq 148); a changed v14 on 07-11 queues v9, an unchanged one does not; controls judge v9 only on 07-10 and 07-12 and write no link; every target judgement a fresh call ("comparable") | `july_test.py dry`, `dry-run.log` |
| the latch (two workers, deterministic) | a request admitted and held open; an unapproved request arriving meanwhile waits for it, is then refused and closes the latch; a later request is refused; only the first reached the inner transport (admission and the inner call run under one lock: a sequence's paid calls run one at a time) | `july_test.latch_race`, `dry-run.log` |
| the stop paths, through replay | an unapproved judge request (v8's rows retired too): refused, v8 never forwarded, the latch stops the sequence, nothing judged after 07-10; a link request at another sequence: refused at seq 148, nothing forwarded; an out-of-pair link: stopped at inspection, no judge attempt, no item handed over after seq 148 | `dry-run.log` |
| the request at the transport boundary | read by Claude: the linked v9 request of 07-10 (37,196 characters; 72 evidence lines; the dependency block, three themes, the previous conclusion, the closing sentence) | `linked-v9-0710-request.txt` |
| the selection record on a failure | a Jev failure after an answered job: the jobs marked answered (with its call id), failed (its sha named), not asked; a write conflict: proposed then failed; a circle closed by a later insertion rolls back the whole write | `tests/test_links.py` |
| historical settlements stayed within reservations | settled at the published rates including cache writes (1.25x; the stored 07-10 Data Center call $0.002895); over all of old-2's stored calls (1,620 judge, 70 collision judge, 5,163 Jev) the charge is at most 0.31 of the reservation; a reply without usage keeps its reservation; Jev reserved at the published 64K limit x 3 attempts ($0.0081). The Luna input bound is the request's size, kept by Alex's choice (D696) | `july_test.py bounds`, `settled_llm_cost` |
| price | control sequence $0.0098 (the stored calls, uncached); linked sequence at most about $0.0185 (an extra v9 call, two link jobs); six sequences about $0.085; ceiling $0.15 | `july_test.py price` |
| preflight | extraction 1,884 rows replayed, 69 statements dropped by the current checks (48 quote not in item, 21 merged; as in the stored run); matching 61 records judged, 0 refused, 1 skipped (request not in this archive); 4 judge answers the stored run itself refused and retried; enum names 46, none missing; 13 keyed views, no duplicate key. It does not replay the new link questions or judging-v8 (not in any archive): the dry run and the tests exercise them | `preflight.log` |
| filing exposure | 105 reading answers after seq 148 link a statement to both v9 and v14 (total revenue's own Q1 figure and Q2 guidance among them); with `kind='reads'` none moves (re-filed by Codex in round 9: 105 of 105 keep both links) | `filing-exposure.md`, test 5 |
| the reading rule | frozen: `reading-rule.md` (sha256 below) | |

Written, not run: `july_test.py send <scratch> <prefix ledger> <out>`: six sequences alternated (control-1, linked-1, ... under
poc-v118 and poc-v119) through `run_sequence` with `BudgetTransport` over a new `SharedLedger` (ceiling $0.15) and `install_stop_gate`.
Each sequence's start and finish are logged; after each, the shared ledger is read (stopped, refused or overrun: inconclusive) and the
sequence's own result (a stop or a target judgement that was not fresh: not comparable). Only the shared ledger ends the send (the
sequences not started are listed); a sequence that is not comparable stays stopped, is scored as not comparable, and the other
independent sequences go on. The summary is written on any normal exit or Python exception; an abrupt kill leaves the start log and the
ledger. It runs only after the council passes this proof. Not done: the PRD 06 text for the
new matcher outcome (it changes with the decision that makes a version the product).
reading-rule.md sha256: cc876b60b8eef25b7675f6d078147d2e569ec97d1b1bfa969f9ec8060d596680

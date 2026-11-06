# Preserve an unknown original statement day in matching and writing

## Diagnosis on the stored day

The user asked that an author's relevant view be kept as a view. D203 says an original statement day is the day the original party made it, or unknown; it must not be filled from the article publication day. The current Jev matcher does the opposite: `jev_matching.decide` substitutes `item.publication_day` when `e.original_day` is empty, puts it in the model's state as the day the statement was made, and returns it as `said_day`. The writer trusts this `said_day` or again falls back to publication day when making a revision.

Census: among the stored 2026-08-29 real run's 98 match decisions that map to extracted evidence, 77 decisions for 66 distinct evidence items in 20 articles had an empty original day and carried a fabricated `2026-08-29` said_day. Of the 77, 38 were new, 38 repeat and 1 replace. This is 77 decisions exposed to the wrong date, **not proof all 77 outcomes were wrong**. The real A-pass/B example has 2 more undated B records; do not send them through this defect and call it a correct simulation.

A decisive stored case: item `gnews:71114e6d410b3ece8ed7f321`, seq 1208, evidence e3 says the $12.9bn Hugging Face acquisition was announced recently; its `original_day` is empty. Jev returned `replace` against e3858 and `said_day=2026-08-29`; writer stored e4211 with unknown `original_day` but inserted revision 122 saying it was stated on 2026-08-29. The day is not established. Under D202/D203, keep the source evidence, but do not create a date-dependent revision when the statement day is unknown. The writing code already expresses `revision_refused(..., 'no stated day')`; the fallback prevents it from firing on the empty value.

## Prior decisions and scope

- D203, `docs/DECISIONS.md` Statement fields: an original statement day is an ISO day or unknown, never filled from publication day.
- D202 / PRD 06: a revision is a later account; the two records remain in force. A date not established is not a later account.
- D204: a repeat is one claim with a relation, and both source records remain; this change does not reclassify Jev's repeat decisions.
- This is a defect fix to the current matching/writer path needed for the explicitly requested A/B integration, not an alteration of the gold, the importance rule, prompt or production configuration. No prior statement dates or revisions in historic databases are rewritten.

## State x event

| Incoming evidence / matcher outcome | Matcher sees | Writer behavior |
|---|---|---|
| Original day known, new | original day; separately article publication day | Store evidence with original day; no revision. |
| Original day unknown, new or repeat | original day unknown; separately publication day | Store original day empty; a repeat relation follows actual matching decision. No date is invented. |
| Original day known, replace; same date supplied by matcher | original day | Existing D202 checks decide older/newer and tier/source; valid revision gets this original day. |
| Original day unknown, replace | unknown | Keep source evidence and links, decline date-dependent revision with `no stated day`; no late record and no guessed date. |
| Original day known, matcher supplies conflicting day | original extracted day remains authoritative | Use original day; keep discrepancy observable in saved raw matcher decision. Never treat model-supplied alternative as a verified original date. |
| Model transport/refusal or crash | request archived and current actual failure behavior | No fake success; existing retry/transaction rules remain. |
| Same article in another scope, another day, another writer | same evidence contract | Runtime gets publication day from that item; original source date stays the evidence's own; no global mutable time. |

## Value x reader and old checks

`original_day` is written by extraction and read by Jev's piece-state text, match decisions, writer `revision_refused`, `revisions.said_day`, late-statement ordering and downstream `research_context.Reader`. Article publication day remains available as a distinct label in the Jev request, never as the original statement day. `matching.check` accepts an empty `said_day`; no schema change. The writer owns revision identity and reads `e.original_day` instead of a potentially invented matching date; original code paths for known dates, source/tier and existing repeat relations remain. The generic non-Jev matcher can still emit `said_day`, but writer no longer substitutes it for an unknown original source date. `piece_state` keeps compatibility with archived diagnostic callers by accepting optional publication day.

## Proof before edit

1. Replay the stored seq-1208 decision into a **temporary copy of the clean 08-28 real ledger** with its original e3 and real `writing.write`: control must write e4211 and a revision with the invented date; changed code must preserve the source and link but produce no revision, with `no stated day`. The old data stays unchanged. This addresses the one observed fabricated-date revision, 1/1 of this class in the counted day. The 77 model decisions exposed to the wrong date require updated model requests before any claim about their resulting semantic outcomes.
2. Test actual Jev request construction: with unknown original day, state says unknown, lists publication day separately and returns blank `said_day`; with known original day, preserve that day. Fake external Jev only; no credential. A mutant reinstating the fallback must fail the unknown-day control. Test writer with unknown and a forged matcher's date, known same day, conflicting date, and earlier genuine date; known source dates, tier logic and repeat semantics must not regress.
3. Replay preflight archived answers on a clean scratch copy, separately record any changed refusal; touch `tests/test_jev_matching.py`, `tests/test_replacement_rule.py`, the isolated A-pass writer harness and frozen-ruler hash tests. Only after the structural proof may the affected one-case real matcher call run. No seven-day result is claimed by this fix alone.

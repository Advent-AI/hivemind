# The small comparison D559 puts to Alex: the week of 10-06's opening articles read from a kept library and from empty (not started), 2026-11-15

**Status: prepared and proved at $0; nothing is sent without Alex's word.** Decision D559; council
`../reflection-3/cold-codex-4.md` (the test and its five proofs) and `cold-codex-5.md` (consensus).

## What it asks

Every clean measurement examined so far starts from an empty library. In the week of 10-06 that produced 13 topics, 12 of
them (by both reader families) on matters that already existed, some of which the same system had opened two weeks earlier
in its own run of the week of 09-22. The record of 2026-11-05 asks for a test that starts from a library built from real
material available before the test. This comparison is the smallest form of it: does the unchanged first step, shown the
library it built itself in the week of 09-22, stop re-creating the questions that library holds, without losing the
article's facts or the questions that are really new?

## What is sent

- The unchanged first step (`clean-arch/step1/run_live.py`; DeepSeek flash, high effort, the frozen request).
- The 11 distinct articles from which the stored October run opened its 13 topics (`inputs/articles.json`; selected because
  they opened topics: this is not a sample of the week's news).
- Each article is read twice, each read its own one-article run from a fixed starting library: `empty`
  (`inputs/initial-empty.json`) and `carried` (`inputs/initial-carried.json`: the seven topics of the September run's completed
  state). 22 reads, one draw, two at a time, on one new ledger with a ceiling of $1.00. Driver: `run_probe.py`.
- Size: the $0 dry run charged $0.46 for the 22 reads at the stored answers' sizes (the ledger's prices); the stored run needed
  14 calls for these 11 articles (three resends), so about $0.5 is expected. An estimate, not a measurement.

Frozen inputs:
- `inputs/articles.json`: sha256 `6ead553882e3c430…`
- `inputs/initial-carried.json`: sha256 `6e0669faac176a63…`
- `inputs/initial-empty.json`: sha256 `37517e5f3dc66819…`
- `inputs/manifest-base.json`: sha256 `3038c186e9a05d59…`
- `inputs/settings.json`: sha256 `7716a85da8750830…`

## Proved at $0 (`proofs/`)

| Proof | What it shows | Judged | Mutant that must fail |
|---|---|---|---|
| `carried_library_proof.py` E1 | the carried library is the September run's completed state: started from empty, every article complete, the state after the last one, equal to that run's seven topics, window ending 2026-09-28 | 235 articles, 7 topics | a dropped topic: fails |
| E2 | the articles are the opening articles of the October week's 13 topics, in reading order, each equal to its stored case | 13 topics, 11 articles | a swapped article: fails |
| E3 | the real run loop, given an article's stored library, rebuilds the stored request byte for byte and the same library after | 11 of 11 | |
| E4 | an empty-start request equals a stored one as built | 1 | |
| E5 | the carried request differs from the empty one only in the open questions shown, which are the September state's | 11 of 11 pairs | |
| E6 | the same settings and system text in both stored runs and today | 2 runs | |
| `probe_dry_run_proof.py` D1 to D3 | the real driver and launcher under the trap (canned answers, placeholder keys): 22 reads, 22 sends each under a live reservation; requests stored with the intended open questions; the bytes sent from empty for the article production itself read from empty equal the bytes production sent; ledger 22 attempts, none refused, nothing left reserved | 22 reads | |
| D4 | with a ceiling below one reservation the first read is refused, the ledger stops, the probe stops, no send | 1 run | a driver that ignores the stop: fails |

Not proved by these: anything about what the model will answer. The dry run's answers were written for another library and
are not results.

## The cases, labelled before any answer (against the carried library alone)

From the two reader families' coverage answers (`../reflection-3/codex-coverage.jsonl`, `claude-coverage.jsonl`: the September
topics they named for each October topic) and my own read stored before theirs.

| October topic (stored run) | Article (sequence) | Against the carried library |
|---|---|---|
| clean-2 supply commitments | 9 | same question (September clean-2), both families |
| clean-5 the Hugging Face acquisition | 30 | same question (September clean-6), both |
| clean-7 Rubin's ramp | 76 | same question (September clean-4), both; the deadline is worded differently |
| clean-4 capital spending 2026 and 2027 | 15 | 2026 is September clean-5 (both); 2027 is not in the carried library |
| clean-1 the lease guarantee | 9 | related: September clean-1 asks the total of credit support, both |
| clean-8 the loss-share exposure | 76 | related: September clean-1, both |
| clean-6 the U.S. licence requirement | 35 | unresolved: one family names September clean-3 |
| clean-12 global AI spending | 206 | unresolved: one family names September clean-5 |
| clean-3 memory prices, clean-9 Groq's rack, clean-10 the B200 rental price, clean-11 Reflection AI, clean-13 the equity commitments | 12, 119, 173, 200, 235 | absent |

## The reading (fixed now)

Alex's rule of 2026-11-05, applied to the library actually shown: a matter the library already holds, not opened again, is
correct; a matter it lacks and that is worth a question, opened, is correct; whether the existing question received the
article's facts is checked apart.

1. Claude reads every one of the 22 answers beside its article and stores its marks first. Then two reader families apart,
   with the article, the open questions shown and the answer.
2. Per new topic in an answer: `redundant` (the library shown holds the same question), `related` (it holds the same matter
   in another shape), `new`; and whether it is worth a question by the standard's test for a big matter.
3. Per labelled case: the article's statements on that matter in each read: kept and filed under the existing question,
   kept and filed elsewhere or nowhere, or not kept. The empty read of the same article is the reference for what was there
   to keep.
4. The five absent cases are the guard against suppression: opened or not in each read.

**It supports going on** when, on the same-question cases, the carried read opens no second question on the matter and files
under the existing one at least what the empty read kept, and the absent cases open as often as in the empty read.
**It fails** when the carried read re-opens the same question in two or more of the four same-question cases; or drops the
matter's statements where the empty read kept them, in two or more; or opens two or fewer of the absent cases that the empty
read opens. Anything between is reported as it is. Ambiguous coverage stays unresolved. One draw: a reason to go on or to
stop, not an estimate of anything.

**Stopping rule of the run:** the first read the ledger refuses, that fails in transport after its retries, or whose launcher
prints no result stops the probe; an answer the step's own checks reject is that read's outcome.

## To start it (only on Alex's word)

```
python3 clean-arch/e2e-comparison-2026-11-13/budget_replay.py --init-ledger <root>/ledger.json --ceiling 1.00
caffeinate -i python3 docs/research/2026-11-14-use-acceptance/carried-library/run_probe.py --root <root>/reads --ledger <root>/ledger.json
```
with `<root>` a new folder `poc/data/clean-carried-library-<date>/`; machine and network checked first; nothing heavy beside it.

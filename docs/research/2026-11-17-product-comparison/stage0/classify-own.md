# My own classification, written before reading either reader's answer

**Leaning: reading (b), article level.** My confidence is moderate, and the council decides.

## Why (b)

- **The purpose.** D667 states it: "a replay of the product as it ran tunes neither system". Exposure is a property of an article: was its
  content used to shape either system or the readers?
- **v29-3m.** D199 rewrote the extraction rule from an aggregate count over the run: 493 empty answers in 1,553 calls, 65% of the first
  week's items. That is a census of a behaviour, not the content of the scored-week articles.
- **v34-3m.**
  - D205 doubled an output cap after one judgement hit it. That is generic.
  - D206's writer change came from a judgement's duplicate id.
  - The served-copy edit removed v68's rows from data, not from either system.
- **Later freezes.** The old extraction prompt was later rebuilt and frozen (v74i) on golden-v5, which covers 07-01 to 07-14. The new system
  never read these runs as input.

## The risk Codex named

An article can inform tuning without being named. Under (b), that risk is held by three things:
- every research artifact built from these runs is a read, including the 2026-10-28 quality review and any trace census document that
  quotes articles;
- every decision's quoted passages count;
- the full census reads documents, not only run folders.

## What each reading leaves, by date only

| | (a) Folder level | (b) Article level |
|---|---|---|
| v29-3m and v34-3m | reads | exempt |
| First possible scored day | about 08-29 (v34 ran to 08-28) | 07-20 |
| Scored weeks | about 3: 08-31, 09-07 and 09-14 (the split-v3 trial also read 08-29 and 08-30) | 07-20 to 09-20 |
| Articles left | about 700 | about 1,619, less the dev arms' `items-window` reads (about 527 by the earlier reviewer's count, if all are reads), the research reads, and D613's 14 |
| N | at 40 articles a week, about 120 articles are read, and N may fall below 20 | — |

## Classification

- **Every configuration trial, arm, week test and day smoke** listed in the brief: read.
- **The run3 family:** production use at the time (D63: sealed, window to 08-15). Its in-span reads are all in `items-window`, which the dev
  arms also read, so the class does not change the outcome. Exempt.
- **v29-3m:** exempt under (b), read under (a).
- **v34-3m, sealed and served:** exempt under (b), read under (a).

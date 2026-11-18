# The small comparison of D559: the same 11 articles read from a kept library and from empty (D561), 2026-11-16

**Answer: on these 11 selected articles, the read with last week's library re-opened none of the four questions it already
held and filed the identified facts under them; it opened 4 questions where the read from empty opened 16, none of them on a
matter the library held (both reader families). It opened three of the four missing matters the empty read opened (not the
equity-investment commitments), so by the rule written before the run the result sits between "supports going on" and
"fails", and is reported as it is. One draw; nothing about final answers.**

Run: `poc/data/clean-carried-library-2026-11-16/` (22 of 22 reads complete, one call each, no resend; ledger $0.427 of $1.00).
Design and proofs: `DESIGN.md`, `proofs/`. My own read stored before the readers': `OWN-READ.md`. Readers (two families,
blind to which read had the library in so far as the packet allows: the library shown is part of a read): `brief-readers.md`,
`codex-readers.jsonl`, `claude-readers.jsonl`; tally `tally_readers.py` → `tally-readers.txt`.

## The rule written before the run

| Line | Result |
|---|---|
| Re-opens a held question in two or more of the four same-question cases | **0 of 4** (supply commitments, Hugging Face, Rubin's ramp, 2026 spending) |
| Drops the matter's statements where the empty read kept them, in two or more | **0 of 4** by my own reading before the readers (`OWN-READ.md`): 1, 1, 2, 1 statements filed under the held question against 1, 1, 2, 1 kept by the empty read; the readers judged the homes, not a fact-by-fact comparison. Article 15's sentence holds both $800bn for 2026 and $1.3tn for 2027; it went under the 2026 question, and 2027 is tracked by neither read |
| Opens two or fewer of the absent cases the empty read opens | opens **3 of the empty read's 4** (Groq's rack, the B200 price, Reflection AI; not the equity commitments), plus memory prices, which the empty read did not open |
| Supports going on only if, besides the two lines above, the absent cases open as in the empty read | **not met** (3 of 4); not failed either: between the two, reported as it is |

## What the readers say (both families unless split)

| | Empty | Carried |
|---|---|---|
| Questions opened | 16 | 4 |
| Of them, on a matter the library shown already held | 0 (no library) | **0** |
| Worth holding | 12 yes; 3 yes/unsure; 1 yes/no (global AI spending as a share of U.S. GDP) | 1 yes; 3 yes/unsure (memory prices, Groq's rack, the B200 price) |
| Statements filed under a held question | n/a | 27: right 17, wrong 2, unsure 2, split 6 |
| Reader-listed entries of a matter deserving a question that the read neither opened nor held (both families' lists added per article and read; names not merged, so not distinct matters) | 25 | 18 |

**The two homes both families call wrong:** customers' share of NVIDIA's receivables filed under the credit-support total
(article 173); the CFO's 70% growth outlook filed under supply commitments (article 206; D508's readers had counted the same
kind of statement as bearing on that question, so the line is disputed across readings).

**What the carried read lost:** a question on a DOJ or FTC action against the Groq deal (opened from empty; the stored October
run did not open it either; one family names it missing for the carried read, the other did not mark its worth above
"unsure"). The equity-investment commitments were not opened; their facts went under the held credit-support question, whose
own outcome reads "versus the equity investments it has made", and both families call those four homes right: the held
question's scope carries into the filing, and the separate equity-commitments question the empty read opened was not opened.

**A gap the readers name in both conditions:** questions on the company's own numbers. The Claude-family reader names the
$108bn quarterly outlook, the 70% growth outlook for fiscal 2028 and the gross-margin outlook cut to 72-73% on several
articles; the Codex-family reader names gross margins and memory costs, 2028 growth, customer concentration and the funding
of investments and payouts. These are missing questions, not missing facts: the figures were mostly kept, and in the carried
read the $108bn outlook was filed under the China question. It is the standing product rule (D382, D384) and the item Alex
ruled on (D505: such figures should reach the judgements of related questions), not something this test changes.

## Limits

Everything above is one read of these articles from a fixed library, not behaviour over a changing library. One draw; 11 articles chosen because they opened topics (not a sample of the week); a seven-topic library one week old,
itself opened from empty; the step's read of each article from a fixed library (no carry-over between articles); no
matching, answer choices or judging run. The empty reads differ from the stored October run of the same articles (12 and 35
opened nothing; 15 opened a 2026-only question): run-to-run variation, one draw each.

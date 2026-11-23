# Council B, round 2: product-path results. Challenge them before I take a question to Alex (read-only)

Data is in `poc/data/step2-validation-2026-11-07/`. Scripts: `clean-arch/step2-validation-2026-11-07/score_retrieval_v2.py`,
`score_jev.py`, `score_product_path.py`.

## Reference v2

Your round-1 advice, the two separate questions, was followed: `reference-v2.json`.
- Two fresh readers and a third on disputes covered 497 pairs: every v1 positive, 60 sampled v1 negatives and 6 insufficient.
- Relation agreement was 93.4%. Disputes were 24 of 33 between same-statement and different-fact-same-matter.
- Result: same_statement 333, different_fact_same_matter 105, revision 25, same quantity other party 8, different 24.
- Of the 60 v1 "repeat" pairs, all became different-fact-same-matter.
- My hand-read of 18 same_statement pairs: 2 clearly wrong (NVL144 vs NVL576), 2 arguable.

## Search: recall at 10 on reference v2

| Query | Per association (391) | Deduplicated history |
|---|---|---|
| R0, production within thesis | 82.1% | |
| R1, thesis + evidence | 90.0% | 125/125 per association |
| R2, evidence only | 95.9% | 113/113 |

In the deduplicated history, merged repeats are removed as candidates. Of the 25 revisions, R1 finds 22.

## Jev, pair level (labelled pairs)

| Arm | Agreement | Wrong merges | Same statements not merged |
|---|---|---|---|
| J0, production wording | 82.4% | 30 = 9.4% of merges | 44/333 |
| J1, cross-thesis wording | 80.8% | 22 = 7.5% | 62/333 |

- J0's wrong merges sit on 13 incoming records; 14 come from one bundle record.
- That bundle is the July 6 "NVIDIA introduced a business model…" record, which also names Sharon AI and Firmus.
- Of J0's 87 disagreements, 16 fall on pairs the two readers themselves disputed.

## Product path (Jev over the R1 top 10)

The precedence is: any same_statement means the record is merged away, else supersedes, else new.

| | J0 | J1 |
|---|---|---|
| Incoming records | 280 | 280 |
| Merged into a true same statement | 106 | 97 |
| Merged with no true match | 6 | 2 |
| Duplicates kept | 4 | 13 |
| Correct merges where readers say every true match lacks something the incoming record holds | 83/106 | 74/97 |
| Correct merges where the source is also attached to a non-same record | 31 | 27 |

**J0's 6 wrong item merges, read by me:**
- clearly wrong: 3 (Sharon AI's 40k GPUs into a Firmus campus record; Morgan Stanley's shipment schedule into NVIDIA's; the analyst
  growth figures);
- arguable: 3.

**45 same_statement answers on never-labelled pairs; 10 sampled:**
- reference misses, where Jev is right: 3;
- Jev wrong: 6, mostly Sharon ↔ Firmus and NVL72x2 ↔ Kyber;
- arguable: 1.

**Materiality of "lacks something", hand-read of 14 flagged same_statement pairs:**
- a material fact really lost: 6 (mechanism details of the backstop, Q1 net income, EPS and margin, "$1tn sales not orders", charge
  counts, NVIDIA's ">$1tn capex in 2027" claim);
- trivial, or a different statement that has its own record: 8.

So my estimate is that about a third of correct merges lose a material fact. That is one draw and a hand estimate with a wide range.

## My reading

- Search passes.
- Repeat detection at record level is close: 4 duplicates kept, about 3 to 6 wrong record merges out of about 112.
- The binding problem is Alex's merge action, "a repeat adds the source to the existing record". Step 1 records bundle several facts
  of one matter, and later retellings often add figures, so source-only merging discards them.

## Question I plan to give Alex

When a later article repeats a stored record but adds a material fact, what does the library do?
- **(a) Recommended.** Merge only pure retellings (add the source, as decided). A retelling with a material new fact stays a new record
  linked to the earlier one. "Material" means a fact the signed extraction standard would keep as evidence on its own.
- **(b)** Merge, and rewrite the existing record with the new detail. This conflicts with the identity rule (AGENTS §3): a changed
  thing gets a new id.
- **(c)** No merging; link only.

**Next test if he picks (a).**
1. Re-judge the added-material lists against the standard's evidence rule, two readers.
2. Run a Jev arm whose same_statement criterion requires "adds no material fact" on the labelled pairs, then on the product path.
3. Pass line: wrong record merges at most 2%; material loss on merged records at most 5%.

## Challenge

1. Is record level the right unit, so that pair-level 82% is not the verdict?
2. Is the materiality estimate sound enough to put to Alex, and if not, what is the cheapest fix?
3. Is (a) right? Is there a better structural option, for example Step 1 emitting atomic statements?
4. What would overturn this?

Under 450 words.

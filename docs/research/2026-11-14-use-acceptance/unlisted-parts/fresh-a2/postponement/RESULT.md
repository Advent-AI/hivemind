# Ruled-out rungs that catch a postponement: the census (D590; $0)

**In one line:** the fresh week's line-3 failure (Taiwan, control p3) is the only answer of its kind in 296 event answers of the
frozen step. The step named a timing statement as the ruling out of an authority's proceeding, which D420 calls the wait. A second,
much larger kind (37 answers) is a company's announced delay on a deadline question. Readers mostly pass it (29 of 37 by both
families), but not consistently, and no decision of Alex's covers it.

## Method

- **`postponement_census.py`** lists every event answer of the 14 stored gate-1 readings with its Ruled-out rung's first sentence:
  424 answers over 43 topics.
  - Its screen picked 135 answers. It catches the known positive (fresh clean-17 p3).
  - It is too wide: both families passed R on 104 of the 135.
  - It misses forms such as "no … shipments during calendar 2028", seen in the unpicked sample.
  - The screen was therefore not used for counts (`census-output.txt` keeps its validation samples).
- **The counts come from two readings of the stored marks:**
  1. **Every event answer at least one first reader failed on R** (92 answers over 23 topics), read reason by reason. 18, over 12
     topics, give a reason about waiting, delay or timing. I read each against the brief's R row, D409, D416 and D420.
  2. **The frozen step's outputs only** (run 4 and every reading after it: 296 event answers;
     `frozen-step-tally.txt`). Each rung whose first sentence is a timing statement is classed by its decider
     (`ruled_out_by`): an authority or the company.

## What the frozen step writes

| Kind | Answers | First readers on R (both hold / both fail / split) | Third readers | Rule |
|---|---|---|---|---|
| An authority's proceeding: "will not adopt … by <due day>" | 1 (Taiwan p3; p1 and p2 name abandonment or withdrawal) | 0 / 0 / 1 | both fail | D420: the proceeding still going on is the wait; only formal abandonment or withdrawal rules it out |
| The company announces the event will come later than a deadline question's day ("deferred until 2027", "will not close by …") | 37 | 29 / 3 / 5 | mixed (2 both hold, 3 split) | No decision covers it. D416 replaced the day *passing* with a typed decision (who decides, what), and a company's announced delay names both. The brief's R row excludes "the event's merely being still awaited" |

The earlier runs (Stage A runs 2 and 3, before D416) carry the day-passing kind ("The end of December 31, 2026 has passed …"). It
does not appear in the frozen step's outputs.

## What it means for line 3

- **The authority kind is one answer of 296.** The rule (D420) is already in the request, and the step's other two sends on the
  topic follow it. It is a misapplication in one send of three. By AGENTS §1 and the prompt audit, such a miss needs the model's own
  account before any change.
- **The company kind is a question of meaning, not a model error.** For "will X happen by <day>", should a company's formal
  announcement that it will happen later show as "Ruled out" (a decision against the event as asked) or "Still open" (the event
  still awaited)?
  - The readers mostly say "Ruled out".
  - A minority says "Still open", including both families on two stored answers. The two answers are the Hugging Face deal's "will
    not close by March 24, 2028" and Vera Rubin's "will not reach volume shipments during FY2027".
  - The answer changes what the card tells an analyst: a product delayed versus a product dropped.

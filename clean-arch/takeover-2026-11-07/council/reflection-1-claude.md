# Claude's independent reflection (written before reading Codex's)

## Lessons at the level of mechanism

What moved quality was structural: the output contract, effort, the model, and fields that force an explicit decision. Wording did
not.

| Lever | Effect | Evidence |
|---|---|---|
| Production's signed evidence rules, with the closing check placed after the article | Noise roughly halved on held-out articles (136 → 50 not-kept on 115) | LOG §§2, 8 |
| The model's own account → an "unfiled" outlet | Removed container theses: the model was opening a thesis only to give a material statement a home | LOG §11 |
| Required closest-open-thesis fields | Fragments gone in every forward read | LOG §§12–14 |
| Reasoning effort, low → medium | The biggest recall lever (probe core 62 → 72 of 75; forward core 80 → 84 of 86). Low effort also mis-applies judgment rules: K6b low unfiled 22 big matters | LOG §11 |
| The model (DeepSeek Flash) | Less framing, generic-view and adjective noise (15 → 2, 7 → 2, 5 → 0 against Luna); fewer small theses; confirmed not to come from the request form (Luna in JSON mode is no better) | LOG §§13–14 |

What failed repeatedly:
- Sentence-level wording and placement edits (Codex's 11 "not adopted"; my K3/K4 thesis tweaks were within sampling noise).
- Extra review calls: the split (D378), and same-article citation review.
- Relaxing a signed rule on my readers' judgment: K2's "arrangement with amount" let in 10 D250-boundary-1 items; the frozen gold was
  right.

Conclusions weaker than they look:
- **One draw.** Flash d1 205 against d2 197 helpful. The two draws share 188 hits; 17 are d1-only and 9 d2-only, union 214. A single
  run misses about a tenth of what another run catches, at random.
- **Library judgments without article text** ranged from 1 to 5 small theses for the same library; the source-backed review
  settled it.
- **Not-kept is a match count.**
- **Probes from fixed before-states** miss how one article's choices cascade.
- **The dev articles have been seen many times.**

## Remaining problems, ranked by product impact

1. **The product does not run end to end, and evidence piles up.**
   - The top three theses hold about half of all links: Flash d1 137 of 282 items, d2 147 of 265, Luna 182 of 346, with "revenue
     growth" at 87 in two weeks.
   - This is Alex's original worry on 2026-11-06: thesis counts stay fine, but the evidence attached keeps growing.
   - Nothing yet dedups repeats (Step 2) or reads the pile (Step 4). Over months, these catch-all theses will hold hundreds of
     items.
2. **Thesis lifecycle.** No thesis ever closes or rolls forward. Forward runs still open 4–7 theses after article 60.
3. **Random recall loss of about 10% per run.** Core is stable (84–85 of 86); supporting items vary.
4. **Residual noise.** About 40 not-kept against production's 30–34; product detail without scale is the shared class.
5. **Evaluation reliability.** Without a fixed, source-backed library rubric and two draws by default, iteration chases noise.

## Breakthrough angles not yet tried

**A. Build Step 2 on the stored Step 1 output and measure the dossier, not Step 1.**
- Embed every evidence item from the Flash run (282) and search the entity's evidence for the top 10 (Alex's own number).
- Have Jev compare each pair: repeat, revision or different. Apply Alex's decision: a repeat adds a source to the existing record.
- Measure how much of each thesis's pile is repeats, what the dossier per thesis looks like after dedup, and what the noise costs
  once deduped.
- **Why a step change:** it is the first time the product runs past Step 1. It attacks evidence growth directly, and it tells us
  whether Step 1's remaining noise matters downstream.
- **Cost:** cents (embeddings; Jev at $0.042 per M tokens), all on stored data.

**B. Company profile and scale context in the Step 1 payload (cold start).**
- Add a short entity profile: annual revenue, segment sizes, the value-carrying drivers. "Its own scale can change revenue, profit,
  cash or credit risk" then becomes a judgment against numbers. Today the model reasons "the article does not establish scale" and
  opens anyway.
- It could also seed driver-level theses so evidence spreads across real drivers instead of one catch-all.
- **Risk:** the profile goes stale; seeds would reopen a decision Alex made (D370 removed seeds), so seeding is his call.
- **Test:** the 27-article probe with a profile block, then one forward run.

**C. Recall by union, with Step 2 doing the merge.**
- Two Step 1 draws per article already recover 214 of 234, against 197–205 for one. Step 2's repeat detection is the natural merge.
- The theses must not diverge: the second draw would see the first draw's theses.
- **Cost:** twice Step 1, plus more noise. Only worth it once A exists.

**D. Evaluation harness as a product.**
- A frozen library rubric, a source-backed thesis review, and two draws by default, so iteration stops chasing reader variance.

## Recommendation

**A.** Build Step 2's search and Jev comparison over the stored Flash Step 1 output, and measure the dossier per thesis after
dedup. It runs on stored data for cents.

Falsified if:
- repeats are a small share of the pile, so dedup does not tame growth; then the fix is thesis structure or lifecycle (B / Step 4);
- or the top-10 search misses most of the repeats a reader finds.

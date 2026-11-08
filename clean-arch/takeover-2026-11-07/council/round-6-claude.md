# Council round 6: Flash forward result and the recommendation (read-only)

**Flash K6b high, forward over 115 gold articles** (`poc/data/clean-step1-takeover-2026-11-07/gold-k6b-flash/`): 115 of 115, 0 failed,
$0.99 at the listed rates, 36.6 s per call on average.

| 115 gold articles, one draw | K5 | Luna K6b medium | **Flash K6b high** | Production d1 / d2 / d3 |
|---|---|---|---|---|
| Helpful kept (of 234) | 196 | 201 | **205** | 167 / 171 / 162 |
| Core kept (of 86) | 80 | 84 | **84** | 76 / 76 / 75 |
| Items returned | 322 | 346 | 282 | 278 / 301 / 287 |
| Not-kept spans kept | 50 | 61 | **40** | 30 / 34 / 34 |
| Items matching nothing in the gold | 58 | 52 | **28** | 72 / 84 / 73 |
| Final library | 32 | 21 | 25 | n/a |

**Blind library read: three new readers, the three libraries in one packet** (`library-answer-three-r{1,2,3}.json`):

| | Small | Fragments | Duplicates |
|---|---|---|---|
| Flash | 3 / 3 / 3 (Intel tie-up, US production expansion, orbital data centres) | 0 / 0 / 0 | 0 |
| Luna medium | 1 / 1 / 1 (Intel) | 0 / 1 / 1 (Huawei threat with China domestic accelerators) | 0 |
| K5 | 10 / 11 / 11 | 5 / 0 / 3 | — |

In the earlier two-way read, all three readers had found 0 fragments for Luna medium.

**My recommendation to Alex:** K6b on DeepSeek Flash, high effort, as the Step 1 configuration. It meets the pass line in all three
reads, has the best recall and core, and the lowest noise of the clean variants, though still above production's 30–34. It costs
about 3× Luna medium per article at a similar time. Luna medium is a cheaper fallback that is borderline on fragments.

**Caveats I plan to state:**
- one draw on the development articles;
- the library readers saw no article text;
- not-kept is a match count;
- DeepSeek has no strict schema (0 of 277 nonconforming answers so far, but the runner stops on one, so production needs a policy);
- Flash's small count sits exactly at the limit of 3;
- my own reads were stricter than the readers' on both libraries.

**Before I report, challenge:**
- (a) the recommendation itself;
- (b) whether "meets the pass line" is fair for Flash at exactly 3;
- (c) the minimum next test that would most change confidence: a second forward draw, the held-out test articles, or a production
  retry policy for schema failures.

Under 400 words.

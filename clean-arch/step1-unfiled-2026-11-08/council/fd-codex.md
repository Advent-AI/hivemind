**BLOCKER: the spending cap still has a concurrency gap.** A call releases its reservation under one lock, then records its cost under a second lock. Another call can reserve that gap before the first cost is added, allowing the total to exceed $3. See [adapter.py](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/adapter.py:229).

The code also records `min(actual cost, reserve)`, which can understate spending if the estimate is exceeded. And the default transport retries internally, so those attempts do not each acquire a new reservation.

The library check now compares the ten stated fields for every copy and rejects the tested changed summary. It checks that revision and later-link references exist, but it does not prove that their relationships or the placement mapping came from this draw.

**BLOCKER**
**Keep the launcher block, revert the broad exception catch, and keep all three clean-ups.**

### 1. The two bugs

- **Bug 1 — REAL, low exposure.** Before the fix, an operator who explicitly passed `--config poc/config/poc-v121.json` could run the shelved judge, spend money, and save its judgements through either ordinary launcher. The default is v118, so routine runs were unaffected. I read D719’s “enabled by no product launcher” as covering explicit selection too. The fix enforces that boundary and leaves the experiment harness available. [D719](/Users/lchingen/hivemind/docs/DECISIONS-log.md:10825) · [Replay](/Users/lchingen/hivemind/scripts/replay.py:90) · [Budgeted replay](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/budget_replay.py:349)
- **Bug 2 — NOT A PROBLEM for the product or its named runs.** The review test manufactures an empty link-question setting in Python. Loading either supported linking configuration supplies or validates that setting. The catch adds a failure record for that artificial case, but the harness already stops on an unexpected exception. [Review test](/Users/lchingen/hivemind/tests/test_links.py:499) · [Config loader](/Users/lchingen/hivemind/src/hivemind/config.py:89) · [July harness](/Users/lchingen/hivemind/docs/research/2026-11-20-production-readiness/dependency-design/july_test.py:175)

I reproduced a budget refusal in memory with and without the catch. Both recorded the same article failure and stopped the budget ledger. `links._ask` already converts the transport error to `links.Refused`, and replay stops on the failed article. Claude’s continuation claim is incorrect. [Budget transport](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/budget_replay.py:293) · [Link call](/Users/lchingen/hivemind/src/hivemind/views/links.py:213) · [Replay stop](/Users/lchingen/hivemind/src/hivemind/replay.py:108)

### 2. The eight recorded findings

**None warrants a product fix.** The repeated `PRAGMA` in `current_state` does run on v118, contrary to D723’s blanket statement. It adds a database query per lookup. Its speed impact is unmeasured. [D723](/Users/lchingen/hivemind/docs/DECISIONS-log.md:10918) · [State lookup](/Users/lchingen/hivemind/src/hivemind/views/store.py:234)

### 3. What `3ba40d8f` changes for v118

- **Judging and filing.** The v7 prompt matched byte for byte on 43 stored views, and its answer format matched too. `maxItems` only applies when the format declares it. v118 still uses ordinary Jev matching and supplies no proposed links to the writer. [Judging](/Users/lchingen/hivemind/src/hivemind/views/judging.py:58) · [Validator](/Users/lchingen/hivemind/src/hivemind/model.py:220) · [Round](/Users/lchingen/hivemind/src/hivemind/views/round.py:153) · [Writer](/Users/lchingen/hivemind/src/hivemind/views/writing.py:113)
- **Storage and preflight.** Opening a writable database adds the link table and dependency column. Preflight now checks refused judge answers against their saved formats and exits if one is missing. All six refusals in the two archives I checked had the original v7 format. [Store](/Users/lchingen/hivemind/src/hivemind/views/store.py:25) · [Preflight](/Users/lchingen/hivemind/scripts/preflight.py:68) · [Preflight exit](/Users/lchingen/hivemind/scripts/preflight.py:362)
- **Upgrade and resume.** An unfinished parallel replay started before the upgrade will reject its saved progress after the upgrade. I confirmed that the same v118 file produces a different saved settings key. The runner also checks the code version. Finish any such replay on the version that started it. [Setting](/Users/lchingen/hivemind/src/hivemind/config.py:43) · [Resume check](/Users/lchingen/hivemind/src/hivemind/parallel_day.py:68)

### 4. Action

- **Keep** the v12 refusal in both launchers and its test. **Revert** the broad link exception handler and its test. [Review diff](/Users/lchingen/hivemind/docs/research/2026-11-22-code-review/review-fixes.diff:99)
- **Keep** the preflight cleanup, the descriptive variable names in `judging.py`, and the `research_context.py` comment. Add no code. [Clean-ups](/Users/lchingen/hivemind/docs/DECISIONS-log.md:10914)

The review was read-only. Claude’s follow-up was blocked by login, so this is my recommendation after checking its written position.
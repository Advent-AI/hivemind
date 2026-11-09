**BLOCKER.** The revised probe still has three issues that can change the result or cost:

- The 60% rule can still count the wrong fact. Most of i163 describes Micron and Nvidia’s gross margins; a long enough excerpt can omit Nvidia’s **66% operating margin** yet count it as written. Matched passages need human adjudication before applying the frozen conditions. [Matcher](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/stage1_probe.py:41)
- The transport still retries up to three times after a timeout or connection failure. A completed but lost response may be billed, so **$4.16 is not a maximum**; input tokens are also estimated. [Transport](/Users/lchingen/hivemind/src/hivemind/model.py:126)
- A malformed response without `choices[0].message.content` raises outside the error handler. It can abort the run without writing the records, rather than count as an empty draw. [Probe](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/stage1_probe.py:103)

The frozen hashes pass, and the question-to-fact mapping resolves for the listed targets.

**BLOCKER**
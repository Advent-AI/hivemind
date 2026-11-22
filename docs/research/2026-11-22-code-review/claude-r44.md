# Claude's position before council round 44 (written before Codex)

Alex asked: are the two "bugs" from the code review real problems, or is this nitpicking? Step back and converge.

**Bug 1. The ordinary launcher runs poc-v121 (judging-v12) when it is named.**
- Running it takes someone typing `--config poc/config/poc-v121.json`. The default is poc-v118. No product, schedule or service names
  poc-v121.
- D719's "enabled by no product launcher" means no launcher uses it by default. Alex's option text was "the new format's code is kept
  but not enabled".
- The linking versions are refused because D694 §0 decided that explicitly. No decision asks the same for v12.
- AGENTS: "Add no mechanism, safeguard or substitute rule for a case no one has named." The refusal is such a safeguard. It would also
  block a later measurement Alex might open.
- One argument the other way: D359 says the code builds only frozen versions and refuses others. But Alex opened v12 (D712) and chose
  to keep its code (D719).
- **My verdict: not a problem. Revert the refusal and its test.**

**Bug 2. A link-step error other than a refusal escapes the round with no record.**
- The trigger shown is a setting built in code with an empty question version. `config.load` never produces that.
- The linking version is paused and harness-only; the ordinary launchers refuse it.
- The "fix" turns an exception into a recorded article failure, and the run goes on. That includes a budget-ceiling `TransportError`
  inside the link step. AGENTS §3 says a rule refuses, and "a warning that lets the run continue is a silent failure".
- For a paid harness, a loud crash is the safer behaviour. Matching swallows errors the same way, but that is not a reason to widen the
  pattern.
- **My verdict: not a problem, and the fix is arguably worse. Revert it and its test.**

**The three clean-ups** (preflight's dead entry and docstring, renamed one-letter variables in `judging.py`, one history comment):
- They follow written rules: Alex's "Always use descriptive variable names", and AGENTS §3 on comments.
- They change no rendered text; the frozen pins pass. Keep them.

**The step back:** the question that matters for the product is whether 3ba40d8f changed poc-v118's behaviour. The frozen pins pass,
v7's schema has no `maxItems`, and the linking and v12 paths are harness-only. Anything beyond that is review of paused lines,
which is low value.

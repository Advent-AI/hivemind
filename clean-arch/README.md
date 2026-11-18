# Clean architecture

This directory is the starting point for the new Hivemind architecture on the `clean-arch` branch.

Read [PRD.md](PRD.md) for the source, or open [architecture.html](architecture.html) for the reading page. The PRD is the single source of truth for the architecture being developed here. The [reference diagram](reference-diagram.png) is Alex's starting picture; where a label on the picture conflicts with the clarified flow in the PRD, the PRD states the clarification. The diagram is a reference image, not an implementation or an acceptance result.

The PRD is a working design. Section 1 states the vision (a market world model built the way a hedge-fund analyst works), the problems it answers and what it does differently; section 8 states where each step stands. Its open questions and untested choices must not be mistaken for approved implementation contracts. Decided: Step 1 runs the adopted request c8 (D387, closed by D391); Step 2 with Step 3's grouping library is frozen (D427; `tests/test_frozen_clean_step2.py`); Step 4's ladder step is built and frozen as it ran (D426), followed by production's frozen judge. The new system replaces the running pipeline only after it passes the five gates of PRD section 1.5 (D548); until then the running pipeline stays the default (D544). The work of 2026-11-06 to 11-08 that the PRD used to carry is kept word for word in [PRD-HISTORY.md](PRD-HISTORY.md).

Section 12 of the PRD is read by `step1/runner.py` at run time: its system prompt, closing check and schema must stay byte for byte the frozen c8 files (`step1/test_runner.py` fails otherwise).

After editing `PRD.md`, run `node clean-arch/render.mjs` from the repository root. Run `node clean-arch/render.mjs --check` to verify that the HTML matches the source. The repository's `python3 docs/check.py` also runs this check. The HTML is generated; do not edit it by hand. The renderer uses the repository's existing Markdown renderer and Node.js.

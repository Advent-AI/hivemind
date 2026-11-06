# Clean architecture

This directory is the starting point for the new Hivemind architecture on the `clean-arch` branch.

Read [PRD.md](PRD.md) for the source, or open [architecture.html](architecture.html) for the reading page. The PRD is the single source of truth for the architecture being developed here. The [reference diagram](reference-diagram.png) is Alex's starting picture; where a label on the picture conflicts with the clarified flow in the PRD, the PRD states the clarification. The diagram is a reference image, not an implementation or an acceptance result.

The PRD is a first draft. Its open questions and untested choices must not be mistaken for approved implementation contracts. The existing product and historical research are separate from this draft and remain available for reference.

After editing `PRD.md`, run `node clean-arch/render.mjs` from the repository root. Run `node clean-arch/render.mjs --check` to verify that the HTML matches the source. The repository's `python3 docs/check.py` also runs this check. The HTML is generated; do not edit it by hand. The renderer uses the repository's existing Markdown renderer and Node.js.

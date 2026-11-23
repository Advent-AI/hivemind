# Hivemind clean architecture: review handoff

Please review the proposed architecture and implementation plan. This is a **read-only review**: do not change code, prompts, configuration, frozen references or documents, and do not run model calls or start a pipeline.

## Start here

- Architecture and implementation plan: [PRD.md](PRD.md). Read the whole document, especially sections 4–8, 12–13 and 16–18.
- Original architecture diagram: [reference-diagram.png](reference-diagram.png).
- Human-readable rendering of the PRD: [architecture.html](architecture.html).
- Repository working rules: [AGENTS.md](../AGENTS.md). Alex's explicit directions for this clean architecture take precedence.

## What Alex is building

Hivemind is a hedge-fund research brain. For the current single-entity scope:

1. Luna reads an incoming source item and the open theses. It proposes thesis–evidence pairs: evidence for an existing thesis or a new thesis with evidence.
2. Search retrieves related prior evidence; Jev compares it with incoming evidence as a repeat, revision or different evidence.
3. The system saves evidence, sources and links.
4. A separate step judges the thesis. Its detailed contract remains open.

The local source database stands in for Hummingbird. The intended direction is to reuse the existing thesis/evidence database and records where compatible. Cross-entity relationship maintenance is future work, not part of the first single-entity slice.

For Step 1, Alex prefers a forward run followed by review of the source articles, model traces and changing thesis state; he does not want a newly constructed golden database as a prerequisite.

## Review questions

1. Does the PRD accurately express the original diagram and Alex's direction? Identify contradictions, missing context and old behavior carried over without a clear reason.
2. Is the proposed Luna prompt clear enough to identify useful theses, reuse an open thesis, and return source-backed thesis–evidence pairs? Review the system prompt, sample input and output schema together.
3. Does the implementation plan define a practical first Step 1 forward run without requiring the whole system to be built first?
4. Are the claimed relationships between the draft and existing production code accurate? Trace material claims to the code and identify what cannot safely be reused or mapped yet.
5. What decisions or missing contracts would prevent the proposed system from working? Separate confirmed code facts from risks and recommendations.

## Existing implementation to inspect

- [Extraction and production output schema](../src/hivemind/extraction.py)
- [Model request builder and schema checker](../src/hivemind/model.py)
- [Round orchestration](../src/hivemind/views/round.py)
- [Evidence ranking](../src/hivemind/views/matching.py)
- [Jev comparison](../src/hivemind/views/jev_matching.py) and [Jev transport](../src/hivemind/jev.py)
- [Ledger writer](../src/hivemind/views/writing.py) and [store](../src/hivemind/views/store.py)
- [Dossier reader](../src/hivemind/bundle.py)
- [Current extraction prompt](../src/hivemind/prompts/role-v74i.txt), as reference; it is frozen and is not the clean draft.

The clean draft's `pairs` response does **not** pass the existing production schema, which expects `evidence`, `candidates` and `new_groups`. Section 18 records the local compatibility check and the open field-mapping questions. Do not assume that missing fields can be invented, or that the database must be replaced.

## Feedback format

Lead with the most consequential findings. For each, give the specific PRD or code location, a concrete example of what could go wrong, and a recommendation. Explicitly identify open product decisions. State which files you read and the limits of the review. Do not claim a finding is proven without checking the source it relies on.

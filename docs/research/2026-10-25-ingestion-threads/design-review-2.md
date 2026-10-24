No serious finding remains in the amended state, value, and check tables for this isolated experiment.

For example, local thread A can point to local B, which resolves to an existing thread. Both retain their separate viewpoints under that one thread identity. Self-references, cycles, unknown IDs, and missing or duplicate matches are rejected before final writes.

The two earlier gaps are addressed:

- **Same-batch identity:** local-to-local resolution reaches one canonical root; roots without retained members are not created.
- **Evidence provenance:** thread readers follow stored `evidence_links`, filter by the requested sequence, and return empty evidence when links are absent. Candidate evidence IDs no longer stand in for stored links.

The tables also cover filtered candidates, existing-view membership, duplicate inputs, rollback, restart restrictions, and updates through existing members. The planned checks follow actual stored relationships and preserve the original viewpoint and evidence checks.

This conclusion concerns the written design; implementation and experiment results remain unverified.
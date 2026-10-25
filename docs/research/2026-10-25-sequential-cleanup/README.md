# Sequential request construction cleanup

The sequential pipeline now has one owner for each request construction operation:

- `extraction.request_for` builds the existing extraction setting, messages and schema.
- `jev.request_for` builds the existing typed request body.
- `model.request_identity` serializes the request and computes its archive key for both clients.

The call sites use those helpers without changing payloads, prompts, schemas, models, cache keys or exception handling. Existing public call signatures are unchanged. This commit contains no concurrent runner, speculative extraction, parallel matching or eligibility change.

Validation on the preserved v23 archives: [3,595 request bodies and hashes match](request-identities.json), including 2,814 OpenAI requests and 781 Jev requests. Reproduce without a provider using `python3 docs/research/2026-10-25-sequential-cleanup/verify.py` with the preserved archives in `poc/data/`. All 123 existing product and corpus tests passed; [read-only review](review.txt) found no regression.

The change is a refactor, not a fix for the separately observed project-eligibility issue. No product behavior or design decision changes. The PRDs were reviewed in module order; scope, classification, Config, dispatch, extraction semantics, library writes, verdict, pull, review pool and overview remain unchanged. No page/PRD mismatch was introduced. The final documentation check is recorded in `docs-check.txt`.

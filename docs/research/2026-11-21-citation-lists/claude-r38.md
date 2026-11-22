# Claude's own reading of the design, round 38 (written before Codex's)

- **T1's mechanics.** Under v9 every judge request has a new archive key. The product's `model.call` misses the scratch archive and
  calls the harness transport. The transport finds old-2's answer by the system and user bytes, retry notes included.
  - For old-2's 4 refused first answers it must return the stored refused answer anyway, so that `check_answer` refuses it, the
    stored retry follows and the trajectory stays old-2's.
  - It records that the answer fails the closed-list schema. A real provider could not have produced that answer under v9. The
    replay keeps the old path so the stores stay comparable.
- **The empty list.** `maxItems: 0` with `items: {"type": "string"}` avoids an empty enum, which the guide does not cover. A
  schema-only check is still needed that the provider accepts `maxItems` under strict mode for this model. The guide says
  `minItems`/`maxItems` are supported; it excludes them for fine-tuned models only.
- **The provider's acceptance of the schema** cannot be shown at $0. The first send of a v9 request is the first proof. A schema
  refusal is an HTTP 400 before generation, which the transport surfaces as an error (a resumable day), not a silent fallback. That
  belongs in the later paid test's first step.
- **Dependencies in v7's shape:** poc-v118 has no dependency rows, so `cites_views` is always `maxItems: 0` under poc-v121. In v8's
  shape the block lists `- vN (` lines; the set must equal `check_answer`'s resolved dependencies (to verify on linked-1).
- **Is the scope right?** Rung-range refusals were never observed; leaving the rung open follows "no mechanism for an unnamed case".
- **Representation:** a plain enum per field fits every stored request (max 915 of 1,000). The margin is thin for a request showing
  more than about 495 evidence ids; the refusal before the send makes that a visible failure, not a silent one.

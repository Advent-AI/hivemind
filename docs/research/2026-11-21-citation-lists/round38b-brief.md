# Council round 38, challenge: design v2 (read-only)

Same scope and limits as round 38. I took every finding of your round-38 answer; `DESIGN.md` is rewritten as v2 (its header lists
what changed). Read v2 against the code and data again.

Questions:
1. Does v2 answer each round-38 finding correctly (the format-error path, batch and resume cells, duplicate theme pushes, preflight,
   the D358 sizes, lists from the rendered rows, the version name, T1's mechanics and the substitution for the four refused first
   calls, the real-validator controls, the T2 population)?
2. Representation: one shared `$defs` evidence enum plus plain enums for dependencies and themes, `maxItems: 0` for empty lists, no
   pre-send counting rule, the provider's HTTP 400 as the visible stop. Is the absence of a pre-send rule right, or is a counted
   refusal needed? Is anything in the format unsupported by `model.check_schema` or likely refused by the provider?
3. Preflight part A reading each row's saved format for every purpose: is that within scope and safe for extraction and matching rows?
4. T1: can the existing replay runner do it as written (the transport keyed by system and user bytes; the rest of the request
   compared; the substitution), and is the store comparison complete (every table, substantive judgement fields including both push
   lists and why_changed)? What would still let T1 pass while the product is wrong?
5. Anything serious left before the build? Answer READY TO BUILD or NOT READY with the blocking items.

# Adjudication of the blind-reading disagreements (registered before either adjudicator answers)

PROBE-DESIGN.md v5 §3: a disagreement between the first reader (Claude) and the blind reader (Codex) goes to a third, source-backed read whose class decides.
Five disagreements: Part B old-3:6458 draws 1-3 (e2769) and linked-1:8777 draw 3 (e693), both non-material targets; Part C linked-1:8776 (harm b).

Because the two readers are of two model families, the third read is a panel of two fresh, independent adjudicators, one of each family (a fresh Codex session and a fresh Claude subagent), each given the same case file (`poc/data/citation-probe-2026-11-22/adjudication-case.json`) with the two positions unnamed. A class stands when both adjudicators give it; when they split, the item is unresolved (for Part C, an unresolved difference that would be material if confirmed: the verdict becomes inconclusive). This is stricter than one third reader, chosen so that neither family decides alone.

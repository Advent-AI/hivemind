# Frozen-member trace: investigative leads, not a score

Alex asked how to strengthen Jev. Previous council recommended checking the frozen source-reference repeat members before choosing a fix. The reference `poc/data/clean-acceptance-2026-11-09/settled.json` has 26 groups and 55 later members marked repeat (plus one revision). These are article-level research matters, not Step 2 records. The reference and all historical outputs remain unchanged.

`repeat_trace.py` reads the two saved independent article-to-item reader outputs A and B by exact matter ID. It retains a provisional mapping only if both say kept and name the same single item; a matter appearing in more than one frozen group or an item assigned to multiple matters is explicitly excluded as a bundled/multiple mapping. It does not use textual substring matching to identify the case. It then traces the actual recorded candidate groups and final placement. This is a mechanical lead generator, not a semantic scorer or a replacement for source-backed review. H01 known positive control confirms that reference `20:ev-1` searched earlier `8:E1`, Jev chose different and the saved outcome was new.

| Preliminary mapping state for 55 later members | Count |
|---|---:|
| Both reader maps agree on one item, no marked multiple-matter/group mapping | 37 |
| A reader's matter judgment missing | 4 |
| Matter/item occurs across multiple matters or reference groups | 11 |
| Readers disagree or another status | 2 |
| Both readers call the matter missed | 1 |

For the 37 agreement mappings, 25 have an earlier reference group's ID among candidates and are placed in one of those groups; 8 have a candidate but are not placed in any prior mapped group; 1 has no corresponding prior group in its candidates; and 3 have no earlier eligible mapped record. This is **not missed-repeat recall, precision or a Jev error count**. Two readers assigning matter IDs to the same record does not prove the two full records have the same main statement, especially when one quotes several facts. Earlier source group originals, not later members, are what Jev actually compares. The 8 are high-priority trace leads; some clearly feature a different main claim, attribution or period, so cannot all be counted as a defect. All original prior/current record IDs, historical candidate group IDs, outcome and reader mapping states are preserved in `repeat-trace-leads.json`. The 55-reference population is conditional on the reference and 11-member story concentration; no global sample inference is warranted.

**Examples of why the underlying definition matters:** H01 (`20:ev-1 → 8:E1`) is the independently source-read missed repeat of a $12.9bn / rounded $13bn acquisition announcement. `14:e2 → 9:e1` is the independently source-read 70% company guidance, while the reports name different executives. In `13:e9 → 9:e13`, the newer record leads with $108.5bn total guarantees, including a $105bn Ohio guarantee, while the earlier record centers on the $105bn Ohio guarantee itself; the source-level matter cluster alone does not settle whether these full records are the same statement. In `24:e8 → 9:e7`, the 2m AWS GPUs have different reported period wording (through fiscal Q2 2029 vs calendar 2027–28), and that difference must be resolved against sources before calling a miss. These show why raw counts cannot be turned into a threshold or case-specific rule.

Next: manually read every lead against both complete articles and the actual Jev input; keep source-reference ambiguity and source/period attribution explicit. Review a sample of the 25 seemingly joined cases to ensure matching was meaningful. The approach and all claims must be independently checked before any model prompt or code changes. No paid call was sent.

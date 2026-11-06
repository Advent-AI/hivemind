# D203 correction: statement day versus ordering day

Independent review of `unknown-statement-day-design.md` found that its proposed refusal of undated revisions conflicts with D203. That proposal is withdrawn. D203 permits the publication day for ordering; D202 records the matcher's revision opinion and links the new record to the old record's destinations. Both remain unchanged.

The stored Aug 29 example shows two separate violations: the Jev input describes the fallback ordering day as the original statement day, and the revision row stores that fallback as `said_day`. The extraction's actual `original_day` is blank. In the completed Aug 29 ledger, 77 matching decisions on 66 unknown-day evidence items use the fallback; 38 new, 38 repeat, one replace. This counts exposure, not proven incorrect decisions. The one replacement writes the fallback into `revisions.said_day`.

Fix at both owners: Jev receives the original statement day (or unknown) and the ordering day labelled separately. Matching keeps returning the same ordering fallback. The writer uses that value unchanged for ordering, but writes the evidence's actual `original_day` into the revision. No relation, destination, tier or late-arrival rule changes.

| State / event | Effect |
| --- | --- |
| Unknown day, new/repeat | Matcher sees unknown and ordering day; writer stores unknown, existing outcome unchanged. |
| Unknown day, replace | Ordering uses fallback; revision and original evidence day are blank; normal revision links and judgement remain. |
| Known day, replace | Ordering rule remains; revision stores the actual statement day. |
| Refused match/write/crash | Existing transaction and retry behavior remains. |
| Later day or changed input | Each input supplies its own statement and ordering days; existing sequence and replay rules remain. |
| Existing historical rows | Read as stored; no retroactive mutation. |

Readers: Jev sees two explicitly labelled fields. `matching.check` and `writing` continue to receive the existing ordering `said_day`. `revisions.said_day` stores the evidence day; `store.evidence_in_force` and judging continue to see the same relation and both pieces. Historical replacements and service/bundle's separate replacements table are unaffected. Old diagnostic callers of `piece_state` keep the two-argument API and receive the same labels. No new gate is introduced.

Tests reproduce both failures before the fix, retain an actual revision and both records, check known and unknown days and check the request passed to the Jev transport. Stored-case replay and the full affected suite follow. The changed Jev request needs a fresh model call for any claim about its decisions. The A formatter's literal ISO-date check, independently found overly strict, remains a separate unvalidated POC defect and is not applied to this B-only path.

## Independent review and final scope

The proposed Jev request change is withdrawn: D354 freezes the shared matching default, and the user requested a faithful simulation. Its original wording continues to present the publication-day ordering fallback as a stated day; `scripts/trace_items.py` also prints the matching fallback as “said on”. These are documented open limitations and can influence matching. The only code change is the writer's D203 storage correction; no historical rows or production deployment are modified. The positive and negative writer tests cover unknown and actual known day, and preserve the revision and both pieces. The old Jev request remains unchanged. Earlier paragraphs describing a Jev change are superseded by this section.

Preflight on the matched August archive/items/ledger: 40 extraction answers, 163 pieces, 162 retained; the one refused quote is absent from the source. 757 matching records examined; one refused because the final-state ledger already contains the successor, and 31 records skipped because their requests are not in this archive. Two archive schema-refusal records are historical provider refusals, not successful answers. A copied read-only ledger initially caused 12 preflight write errors; using a writable scratch copy removes them. This check does not validate the split prompts or the preparation step, which were checked separately. Full pytest could not collect the unrelated UI suite because the local `mcp` dependency is missing; the 33 affected and frozen-ruler tests pass.

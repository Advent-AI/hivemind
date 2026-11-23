You are the third, independent reader for a hedge-fund research system. This is a read-only task: do not edit any file and do not
run any model call. You did not write the system under test, and you will not see its output.

Read `{groups_packet}` and `{packet}` (the 50 source articles), and no other file. The groups packet holds:
- `matters`: the settled matters of all 50 articles, with their ids and central claims;
- `groups_A` and `groups_B`: the repeat groups readers A and B proposed independently, rewritten onto the settled matter ids. A
  member a reader listed that no settled matter took is shown as `unsettled`.
- `dossiers_A` and `dossiers_B`: the details each reader said a later member adds.

A repeat group is a set of matters, in different articles, that report the same research point. Each later member is either a
`repeat` (the same facts again) or a `revision` (a changed number, a denial, a confirmation, or a later step of the same matter).

Settle the groups against the sources:
1. A group both readers propose with the same members is kept.
2. Where they differ (a member, a kind, or two groups against one), decide against the sources. A shared company, product family or
   topic is not enough; the articles must report the same point.
3. A settled matter that belongs in a group neither reader made may be added. Give its reason.
4. For each final group, list the details each later member states that the earlier members did not (a number, a date, a party, a
   condition). Each detail carries an exact quote from its article.

Return only JSON:

```
{"repeat_groups": [{"members": [{"matter": "<settled id>", "kind": "first|repeat|revision"}], "settled_by": "both|third",
                    "reason": "..."}],
 "dossiers": [{"group": 0, "details": [{"matter": "<settled id>", "detail": "...", "quote": "<exact span>"}]}]}
```

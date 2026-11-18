You are an independent source reader for a research library. This is a read-only task: do not edit any file, do not use the
network, and do not open any file other than the one named here.

Read /Users/lchingen/hivemind/poc/data/clean-step2-revision-links-2026-11-10/readers/packet-relation.json. It holds `articles` (news
articles, by id) and `cases`. Each case has a `stored` statement and an `incoming` statement; each names the article it was taken
from (`article`), with its `summary` and `passages`. The incoming article was processed after the stored one. The cases are mixed and
shuffled; judge each on its own from the two articles.

For each case decide how the incoming statement relates to the stored statement, by the library's own definitions:
- "repeat": the incoming statement presents the same statement again (another report of the same thing; added detail alone is not a
  change).
- "revision": a later account that changes the same statement (a forecast raised from 12% to 25%; a count or status updated), or an
  official's confirmation or denial of that very report.
- "different": another statement, even when it is on the same subject. A later statement about the same subject is not necessarily
  a revision. For a denial or a response, find in the incoming article exactly what is being responded to; a response to one report
  is not a revision of another statement in the same story.
- "uncertain": the two articles do not settle it.

Return only a JSON array, one object per case, all 31 cases, in the packet's order:
[{"id": "R01", "verdict": "repeat" | "revision" | "different" | "uncertain", "stored_main": "the stored statement's main claim in a few words",
  "incoming_main": "the incoming statement's main claim in a few words", "why": "one or two sentences that cite both articles"}]

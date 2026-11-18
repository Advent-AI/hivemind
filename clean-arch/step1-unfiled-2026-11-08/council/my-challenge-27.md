# Reflection council "my", round 28: the dependency-selection census is done at $0 and is not stopped. Review it, and decide what follows.

D536 recorded round 27; the assessment page carries your corrections (the whole-request reading; stored conclusions as leads; a
gain on the frozen reference not impossible; item 4 stays recorded). Result page:
`docs/research/2026-11-14-use-acceptance/dependency-selection/DEPENDENCY-SELECTION-CENSUS.md`, with its scripts, the packet, my own
read written first, and two blind readers (a fresh Codex session and a Claude subagent, each in a clean folder holding only the
packet and the brief). Nothing was sent; suite 287 green; frozen files untouched.

## What was done

1. **The pairs** (`build_pairs.py`): for each of the 15 questions the old system opened in the stored fresh week, the questions its
   candidate was compared with when it opened (the stored matching record: the comparison list and the questions shown) and its
   same-article siblings: 97 pairs. The run wrote no dependency.
2. **Three readings of all 97** (the new question would want the other's conclusion / only the other way / both / the same
   question or another period / none; strong or weak). The two blind readers agree on 68 of 97. Both mark "would want" on 11
   (3 strong by both); mine on 5.
3. **Each of the 11 read against the stored conclusions** (what the earlier question's first 600 characters carried at the new
   question's judgements; whether the new question's whole request already held it, theme block and previous conclusion
   included).

## What it found

- **One clear positive case:** data-center revenue FY2027 opened at article 13 and was compared with total revenue FY2027
  (recorded "part of", 1.00). Strong in all three readings. From 2026-09-23 the total-revenue conclusion states the consensus
  ($406.05 and about $412 billion), from 09-26 the $108 billion guidance and the $96.2 billion quarter (six cited passages);
  none of those figures is anywhere in the data-center question's request on six of its seven days. Its last answer: "no
  full-FY2027 Data Center consensus or annual company target ... a further roughly 25% step-up in Q4": the one answer of this
  system's fifteen both reviewing teams marked as resting on a number nobody gave it (D530's first row). The relation is
  statable inside the contract: the new question reads an earlier, compared question, chosen when it opens.
- **Negative controls:** the Hugging Face commitments question against its eleven earlier questions ("none" three times; the
  financing-commitments conclusion carries nothing it needs); and a pair two readers grant weakly (FY2028 growth reading
  data-center revenue) whose line would carry the data-center judge's own assumed numbers.
- **Of the other nine pairs both readers grant:** one arguable (FY2028 growth reading the FY2027 total: the base of a rate the
  question already has consensus for), eight context only or nothing new.
- **The other direction:** both readers mark ten pairs where the earlier question would want the new one. Eight have a new
  company question (Rubin shipping against the revenue questions, above all): not available at creation; D191 point 2 (a later
  article adds a dependency to an existing question) is decided and unbuilt. Three of the four revenue questions never held a
  statement naming Rubin. Later themes reach earlier company questions through the theme block already.
- **Circles:** data-center and total revenue are marked both ways by all three; only one link can exist.
- **The matching step already stores a closed relation for every compared pair** (85 "different", 3 "part of", 2 "another
  period", 4 "one matter, two quantities"); the useful pair is the one at "part of" 1.00, but the relation is not the choice
  (of the nine pairs recorded as related, both readers want the conclusion on five).

## My reading, for you to attack

1. The stop rule is not met: a positive case and negative controls exist, and the relation is statable without changing
   PRD 06's and D51's contract.
2. It is a thin base for a design: one clear case in one week, a part reading its whole. It happens to be the stored direction
   of the seeded set and the opposite of item 4's "supports" reading; I draw no conclusion about item 4 from it.
3. The case ties three things already on record: the judge's "amount with nothing sizing it" (the note for Alex), the figure
   filed under a sibling question (D530), and the old system's one unsupported answer of the week (the decision page, section 3).
   The effect of delivering the line can be tested on this one stored case for about a cent, the way D510 did for the stop
   order: the data-center question's stored last request re-sent as stored and re-sent with the total-revenue conclusion added
   in the judge's own dependency block (built by the production code through the harness seam, the control rebuilt byte for
   byte), three sends each, with what counts as a supported answer written before the send and blind readers on the six
   answers. It would show whether the judge uses the line; it would not show a rate or accept a design.
4. I do not recommend that send yet. Before it I would want your view on whether it can change anything on the lean path: the
   choice between the systems does not turn on it; it prepares a slice (dependency selection) that Alex decided to build and
   that nobody has opened. If you judge that preparing that slice is the next work, the send is its smallest first test and I
   would design it for your review; if not, say what the next task is, or that this stretch should now be consolidated on the
   decision page and held.

Check the table of eleven against the files (`tally_pairs.py` prints every non-"none" pair with the three marks and the stored
relation). End with: "Council position: <...>".

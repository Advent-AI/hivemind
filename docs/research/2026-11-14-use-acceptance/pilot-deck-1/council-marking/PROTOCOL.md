# Deck 1 marked by the council (Alex, 2026-11-17), protocol written before any mark ($0 of API calls)

**Alex** (2026-11-17): "Instead of asking me, why don't you run a council with claw code? And basically, you guys argue, battle until you agree what
you need to score for the 19 questions ... run it through so that you can basically get the results that you need to proceed with next steps."

## What it answers now

D662 asked whether Alex's own reading can serve as the instrument. With the council marking, it asks the same question of the council: do two model
families, argued to agreement, reject both planted wrong answers, accept the confirmed supported control, and mark the hidden repeats the same?
- If they do, the council is the candidate reader for the next comparison, and Alex spot-checks its disputed cards.
- It still does not decide which system is better (DESIGN.md: "It cannot show … which system is better").

## Readers and blinding

- **Readers.** A is Codex, with memories off (D661). B is Claude, through the command line with no settings, tools, MCP or slash commands. Each
  card is its own fresh session, run from an empty directory, with everything inline. Logs are checked: any command, tool or file event voids the
  session.
- **What a session sees.** Only the card as the page shows it to Alex: the question, the answer choices with the present answer, its reasons, the
  cited statements with their passages, the complete request, the completeness sheet, and the linked articles' text, plus the fixed brief below.
- **What no session sees:** the key (`~/.hivemind-keys/pilot-deck-1/`), the stored model-family marks, DESIGN.md, or which cards are planted or
  repeated.
- **Claude, the orchestrator,** writes no mark. Code builds every prompt from the page.

## Steps (fixed)

1. **Independent marks.** For each card, A and B each mark the page's own fields:
   - `worth`: yes, no or cannot tell;
   - `supported`: yes, no or cannot tell, answer cards only;
   - per sheet fact, `bears` (yes, no or cannot tell) and `effect` (the answer, only the confidence, neither, or cannot tell);
   - a short `why`.
2. **Debate.** For each card where any field differs, both readers get a fresh session with the card, their own mark and reason, and the other
   reader's mark and reason. Each keeps or changes each disputed field, with a reason. There are at most two rounds.
3. **The council's mark.**
   - **Agreed:** that value.
   - **Still split after two rounds:** "cannot tell", listed as a split for Alex's spot check.
4. **The tally.** The council's marks are written in the page's own format (`c<n>-worth`, `c<n>-supported`, `c<n>-why`, `c<n>-fact<i>-bears`,
   `c<n>-fact<i>-effect`) and tallied by the unchanged `tally_deck.py` against the sealed key.
5. **Read against D662's lines, with the time line not applicable:**
   - **"Enough to design the next comparison":** both plants marked `supported = no`; the separately confirmed supported control `yes`; at least 2
     of 3 repeats the same on both fields.
   - **Anything unmet** is inspected for its cause.
   - **Reported:** every split; agreement with each stored model family, with D661's caveat; and the sheets.

## The brief every session gets (fixed text, in `brief.md`)

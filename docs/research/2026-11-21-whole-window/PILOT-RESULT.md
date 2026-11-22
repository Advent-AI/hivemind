# Pilot pair 1 result (D711)

**Registered verdict: inconclusive.** control-1 (poc-v118) stopped on 2026-09-08 on a double refusal (PAID-DESIGN.md §4 precedence
(2), §8). linked-1 (poc-v120) completed and passed every acceptance check, so precedence (1) does not apply. The comparison is closed:
no redraw, no resume (council round 37, consensus). Spend: $1.70 of the $2.50 ceiling (`poc/data/link-pilot-2026-11-21/ledger.json`).

## What stopped the control

- v21 ("How much will NVIDIA's total revenue grow in FY2027?") on 09-08. Its request listed 29 evidence ids.
  - Call 8938 cited `e362` for `e3620`.
  - The retry, call 8941, cited `e3111`, one character from `e3110` and `e3112`.
  - Both are copy errors of a listed id. The forecast is the same in both (about $407.1B, 88.5% growth).
- control-1 equals old-2 on every table H2 checks through 09-07, the last completed day: 984 non-reader judgements, 4,196 evidence
  rows and 5,223 links. The summary's H2 `false` comes only from the days missing after the stop.
- Only readers were bought: 201 attempts.

## Exploratory findings

These come from one pair and one draw. They are not the registered blind reading.

| Line | linked-1 | control-1 | How it was read |
|---|---|---|---|
| P: Data Center above total revenue, 07-10..09-07 | parser 3 of 60; **0 real** | parser 28 of 60; the 5 sampled are real | Codex read all 12 linked dates the parser flagged across the window; Claude read 4 of them and 5 random control dates |
| H4: CPU double count in total revenue | **4 answers** (07-15, 07-16, 07-17, 07-18; in force 07-15..07-19) | no CPU link | Claude read all 71 post-link v14 answers; Codex did a shuffled second read with dates hidden (exploratory, because the list was in the brief); both lists agree |
| H1: reader refusals on the 200 matched reader-days | 5 | 1 | an excess of 4, at the harm line |

### P
- In linked-1, Data Center is computed as a share of v14's total. Example from 07-22: "About $352 billion: v14's approximately $387.3
  billion … multiplied by 91%".
- Linked-1's parser hits are artefacts: the parser took the total's amount as the Data Center figure.
- The safe claim is that the link kept the two forecasts consistent in the readings checked. Removal of the class is not shown.

### H4
- Each double-counting answer adds $19–19.5B to a total of about $387B built from company guidance. That addition lifts the total
  above $400B.
- On 07-20 the judge reversed it itself ("included within, not added to").
- The link behind it, v14 reads v8 ("stand-alone CPU sales"), had been flagged in D705 as running against the tie-break's direction.
- **Correction (2026-11-22, D721):** these are four unsupported increments with the overlap unresolved, not proved double counts.
  The frozen gold (q01) lists the Vera CPU target among the drivers above consensus. The paired control reached about $417B
  without any CPU addition on 07-16..07-18, so only 07-15 differs in rung.

### H1
- A resumed control would make (v21, 09-08) a matched day and add the control's two refusals. That lowers the excess to 2 or 3.

### Refused answers
- Every refused judge answer is an id-membership error: an id outside the list its field allows. Count: 17 in 5,408 distinct
  archived attempts (old-1, old-2, old-3, and the fresh calls of both pilot arms).
- All 5,389 committed answers fit those lists.
- 6 of linked-1's 7 fresh reader refusals mix up which list an id belongs to:
  - the dependency `v14` in evidence citations, twice;
  - theme ids in `cites_views` beside a valid dependency, four times.
- The closing instruction of every request already forbids theme ids in `cites_views` (`judging.py` lines 180–182). The answer format
  accepts any string in these fields.

## Council round 37 (`round37-brief.md`, `codex-r37.md`, `claude-r37.md`, `round37b-brief.md`, `codex-r37b.md`)

- **Consensus: A.**
  - C (resume control-1 from 09-08) is exploratory at most. The stop and the control's lead were seen before the rule change was
    proposed, and a resume would move H1 across its line through the very refusals that invalidated the control.
  - B (a redraw) selects a replacement after seeing the stop and repeats the risk.
  - Claude first proposed C; it withdrew C once linked-1's H1 numbers showed the effect.
- **A resume-once rule** for a double refusal may be used only in a future comparison registered before its send. It applies to both
  arms, keeps the original refusals in the matched-day count, and is proven on stored data first (the runner overwrites a resumed
  day's call range today).

## Recommendation to Alex (consensus)

Open a judge version that changes the citation format only:
- **The change:** every id field of the answer (cites, push ids, `cites_views`, theme pushes) gets a closed list built from the exact
  request. The judge still chooses which evidence matters; the code fixes which ids each field can hold.
- **The test, at $0, from request generation through answer checking:**
  - every stored accepted answer fits its lists;
  - every observed bad id is excluded;
  - a field with no allowed id accepts only an empty list.
- **Limits:**
  - Whether the judge picks the intended source is a separate measurement.
  - Changing the format changes the archive key of every request, so any paired run needs a new replay proof first.
  - Used in both arms, it tests what links add to that judge; whether the linked product should replace frozen v118 stays open.

The link direction (a whole reading its own part) is a separate design, not part of this version:
- The typed keys label the stand-alone CPU question `other`, so a key-based part-and-whole rule would miss it.
- Whether a part's forecast may inform a whole is a judgement. A total built from non-overlapping parts is legitimate.
- D704 allowed both directions on purpose.

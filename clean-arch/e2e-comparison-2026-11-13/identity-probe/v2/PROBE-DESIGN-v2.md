# The identity probe, design version 2: c16 (version 5) against c8 (D463; council round 13's corrections)

**What it can decide:** whether one identity bullet changes clean Step 1's behaviour on the two boundaries the audit found missing (next
year's figure of a shared quantity; signing an unsigned deal beside a programme's amount) on articles it has never seen, by story, without
splitting comparisons, without duplicating open questions, and without D441's memory regression. A class-specific result; a "goes on" leads
only to a council decision on a larger fresh-article test, never to adoption.

## The candidate (version 5)

`arms/c16-system.txt` (17,742 characters, +1,914 over c8), `c16-closing.txt` (identity sentence pointing to the bullet), schema = c8's. Four
classes: the same thesis (when the same result settles both; another wording, source, estimate, direction, or another population or wording
of the same aggregate; another form of one plan); evidence, not another thesis (a later deadline while the earlier-deadline thesis is open);
another thesis (next year's figure of a shared quantity beside this year's; signing an unsigned single deal beside a programme's amount when
that deal alone could change revenue, profit, cash or credit risk; each only when it passes the opening tests); one thesis although two years
appear (a shared quantity's change from this year to next). Two examples per boundary, from other industries.

Blind audits: version 1 (`../audit-c16-blind.md`), version 3 (`audit-c16v3-blind.md`); version 4 answers version 3's two wording points
("another calendar year" → "next year's figure … beside this year's"; the size test now lists revenue, profit, cash or credit risk); version 4
(`audit-c16v4-blind.md`) left wording-level points only, answered in version 5 ("next year's figure of a shared quantity tracked as its own
outcome, beside this year's thesis"; "a franchisee's lease big enough to change its credit risk"). Kept and
disclosed: the bullet judges identity against the open theses, which the standard gives to matching (§4); c8 already does this by the clean
architecture's design (AUDIT.md), and c16 does not change who decides. **Growth (+1,914):** the audit found the lines missing (AGENTS §6); the
existing near-duplicates (§2's "A different wording, source, forecast or direction alone does not make a new thesis"; §3's "Another population
or wording of the same aggregate is evidence for it"; the do-not-open list's "another estimate, source or wording") stay because each also
carries its own section's rule, and cutting them would be a second lever in the same arm.

## The cases

- **Fresh** (`selection-v2.json`, sha256 `fa76958bea8d688570191d1ac9874e9699da94177d7613b84a39c15c253543ee`): Step 1-eligible items of
  2026-07-15 to 09-04 never sent in a Step 1 measurement; twenty candidates per category by broadened patterns in a new seeded order
  (`select_candidates_v2.py`); four blind Codex readers, one per category, marked all eighty (fit, story, expected behaviour;
  `reader-selection-v2-T*.jsonl`). **What the window holds:** the two target boundaries have **one fresh story each**: next year's
  hyperscaler capex (1 fitting T1 article of 20, and 1 T3 article on the same matter) and the OpenAI Ohio guarantee (19 of 20 T2 fits, all one
  story). Merges have 7 stories and negatives 5. **Rule applied:** every article of the capex-2027 story (2); the first three "open"
  articles of the Ohio story; the first article of each "nothing to open" story (5: the Ohio story's in-passing report, NVIDIA's FY2028
  revenue growth, gross margin and earnings growth, SpaceX's compute capacity); the first article of each merge story (7: clean-1, -2, -4, -5,
  -6, -8, -14). The next twenty T1 and T3 candidates in the same order were then read (`reader-selection-v2next-T*.jsonl`): no further target
  story and no independent positive comparison story; the first article of each new "nothing to open" story was added (Alphabet's 2027 capex,
  NVIDIA's FY2028 revenue, its 2027 buybacks, used RTX 40 prices, Marvell's FY2028 revenue; NVIDIA's FY2028 revenue and revenue growth are
  counted as one story). **Selection v3** (`selection-v3.json`, sha256 `3e1dcffae8a9e740a79e005a24c4087fb95d3720cf0953c7d2d0a5fae34f30bf`):
  22 articles; cases file `cases-identity-v3.json`, sha256 `bdb3ae66f3375b035ac89ab8271737bf898d05263eb962809166d96213b1e6b4`.
- **Before-state:** c3's library after 2026-07-14 (`../snapshot-c3-2026-07-14.json`), a controlled snapshot, not an evolving replay.
- **Guards** (stored, not tuning material): memory d1–d3 (six sends each per arm), Ohio, capex-open, capex-repeat-a (must merge), population
  (must merge), d1–d3, three sends each.
- Requests built by `../build_fresh_trace.py` (byte-for-byte reference check, a mutant refused) and sent by `../probe_identity.py`, the
  reviewed `probe_c14.py` with two changes only: the ledger is a module-level class, and usage that is missing, malformed or prices at zero
  settles at its reservation (council round 15; `../test_probe_identity.py`: 5 tests pass; a mutant settling zero usage at zero fails one); preflight: every case builds both arms with only the two texts differing (`../preflight-identity-v2.output.txt`, to be re-run on
  version 4 and the new selection); every stored Step 1 answer of the full run (729) passes the current checks
  (`replay-stored-answers.output.txt`); `scripts/preflight.py` replays production archives and does not cover clean Step 1's checks.

## Counting (Claude reads every answer; a disputed mark goes to a blind second reader)

A send is **valid** when its answer passed the schema and the runner's checks; refusals, format failures after the resend, run-check
refusals and sends not made are listed and are not valid. An **article** is exercised for a line when each arm has at least two valid sends
on it; for each article and arm, a behaviour **holds** when at least two of its three valid sends show it. A **story** holds for an arm when
the behaviour holds on more than half of its exercised articles (a tie does not hold); articles of one story are never counted as separate
stories.

- **T1 target** (stories expected "open"): a new thesis on the article's shared quantity for next year.
- **T2 target** (stories expected "open"): a new yes/no thesis on whether NVIDIA signs the article's unsigned deal by a check date.
- **T3 positive** (expected "open"): one new thesis on the change to the later year; a **split** is two new theses for the two years.
- **Negative controls** (expected "nothing to open" or "link", any category): a new thesis on that matter is an **unwanted opening**.
- **T4** (expected "link to clean-N"): a new thesis on what clean-N tracks is a **duplicate**; a **dropped merge** is an article where the
  statement is linked to clean-N in at least two of c8's valid sends and in at most one of c16's. A T4 article is exercised when both arms
  have at least two valid sends and at least one arm links the statement to clean-N in at least two of them.
- **Guards:** memory: valid sends with a memory-price thesis (any shape), and those in the 2027 or 2026-to-2027 shape (D441's shape), of 27
  per arm (three states × nine sends);
  capex-repeat-a and population: valid sends opening a duplicate capex thesis, of 9; Ohio and capex-open: the target, reported.

A story is a **win** for c16 when the target holds for c16 and not for c8, a **loss** in the reverse case.

## The lines (frozen before any send)

| line | met | inconclusive | not met / regression |
|---|---|---|---|
| T1 target, T2 target (each; one story, so a diagnostic, never "met" in general) | the target holds for c16 on most of the story's articles and for c8 on fewer | — | the target holds for c8 on as many articles as for c16, or more |
| T3 (one fresh positive story, the capex-2027 change: a diagnostic; the comparison's regression stop is the memory guard's D441 shape line) | reported: split, dropped or one question, per arm | — | — |
| negative controls | no story where an unwanted opening holds for c16 and not for c8 | fewer than 2 exercised negative stories | one or more: regression |
| T4 duplicates and dropped merges | no exercised story where a duplicate holds for c16 and not for c8, and at most one dropped merge | fewer than 4 exercised stories | a duplicate holding for c16 and not c8 on any story, or two or more dropped merges: regression |
| memory guard, any shape | c16 ≥ c8 − 4 of 27 | c8 below 5, or either arm with fewer than 7 valid sends in any state (fewer than 21 of 27) | c16 ≤ c8 − 5: regression |
| memory guard, D441's shape (2027 or 2026-to-2027) | c16 ≥ c8 − 2 of 27 | c8 below 4, or the validity minimum above not met | c16 ≤ c8 − 3: regression (D441: 13 against 3 of 54) |
| capex-repeat-a, population | c16 − c8 ≤ +1 duplicate sends of 9, each | — | ≥ +2: regression |

**Validity, every line:** the valid sends of each arm are reported per line; a line whose population has three or more fewer valid c16 sends
than c8 sends is **inconclusive**, with the refusals listed, never met.

**Verdict, class by class:** the two targets are reported as diagnostics on one story each (moved / not moved); they cannot show the
clause works in general, because this corpus holds one story per boundary. The regression lines decide: **no harm detected** when every
regression line is met and exercised (said as "no harm detected on these cases", never as safe in general); **stops** when any regression
fires; **inconclusive** when a regression line is unexercised. Only "no harm detected" with both targets moved goes back to the council, which then decides whether a general test needs another corpus (other
companies) or whether c16 is measured end to end as a Step 1 version. A result against the hypothesis stops the line and goes to the council
(AGENTS §7.3). Each article and story stays visible in the result.

## Cost and stopping

Sends, in **one invocation of `probe_identity.py` sharing one ledger**: fresh articles × 2 arms × 3, four guards × 3 states × 3 × 2 = 72,
memory 3 states × 9 × 2 = 54 (each memory state listed three times in the cases file under the names memory, memoryb, memoryc, pointing to the
same stored request, so `--sends 3` gives nine): with 22 fresh articles (132 jobs), 258 jobs in all; dry run: about $3.85 at published rates;
**planned ceiling $5** for this probe, a ceiling on reservations and not a guaranteed maximum (a request admitted before an overrun can finish
after it); actual cost recorded from tokens at published rates. An interrupted probe (any line's population incomplete because of the
ceiling, an overrun stop or network loss) is not scored as a pass.

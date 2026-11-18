# The identity probe: c16 against c8 (D463) — design and frozen lines, for the council before any send

**What it can decide:** whether one general identity bullet makes clean Step 1 open the questions the standard keeps apart (another year of
a shared quantity; signing an unsigned deal beside a programme's amount) on articles it has never seen, without splitting comparisons or
duplicating open questions. It cannot show a right final answer; a pass leads only to a council decision on a larger fresh-article test.

## The candidate

`clean-arch/step1-unfiled-2026-11-08/arms/c16-system.txt`, `c16-closing.txt` (schema = c8's): one bullet after section 3's closest-thesis
bullet ("Same thesis or another …", three classes, two or three general examples each) and the closing check's identity sentence pointing
to it. System text 15,828 → 17,522 characters (+1,694), closing 8,638 → 8,615; the growth's reason: the audit found the standard's identity
boundaries missing (AGENTS §6, "add an instruction only when the audit shows one is missing"); nothing is cut, because cuts are levers too.
F6 is not included.

**Blind audit of the first wording** (`audit-c16-blind.md`) and what changed in this wording (version 2): "another population" narrowed to
"another population or wording of the same aggregate" with "when the same result settles both"; "another year of a yearly quantity" narrowed
to "another calendar year of a shared quantity" (the company's own fiscal-year lines keep §4 boundary 4); "another quantity with its own
driver" and its battery example removed (no permitted opening reason fitted it); "another decision" narrowed to the unsigned single deal with
its size test, two examples; the comparison narrowed to "a shared quantity's change from this year to next is one thesis about next year",
two shared-price examples (the hotel revenue-per-room example removed: a company financial measure is not opened under this request). Kept and
disclosed: the bullet judges identity against the open theses, which contradicts the standard's allocation to matching (§4 "抽取不判库里的");
c8 already does this by the clean architecture's design (AUDIT.md), and c16 does not change who decides.

## The cases (frozen)

- **Fresh** (`selection.json`, sha256 `dbb6666b4f291b0985ae455f5d6bb7bb4b2d13e7973e067f1d0764fc568bf183`): items Step 1 could receive,
  2026-07-15 to 09-04, never sent in a Step 1 measurement; candidates found by one pattern per category (`select_candidates.py`), in a
  seeded order; a blind Codex reader read each beside the snapshot and the standard and marked fit and the expected behaviour
  (`reader-selection.jsonl`); the first four fits per category were taken by rule. T1 (2027 capex while the 2026 question is open; expected
  "open a new question") 4; T2 (NVIDIA negotiating the reported ~$250bn OpenAI financing or backstop beside the programme-amount question;
  expected "open") 4; T3 (a comparison across two years; expected "link" or "nothing to open") 3 (the reader stopped after four reads; three
  fit); T4 (a statement an open question tracks: another 2026 capex estimate, the programme, the Intel stake, Vera Rubin shipments; expected
  "link to clean-N") 4.
- **Before-state:** clean draw c3's library after its last item of 2026-07-14 (`snapshot-c3-2026-07-14.json`, 15 open theses), the same
  for every fresh article: a controlled snapshot, not a replay of an evolving library.
- **Requests:** `build_fresh_trace.py` builds each c8 request exactly as the runner does; it first rebuilt c3's stored request of sequence
  243 and its sent form byte for byte (a mutant renaming one payload key is refused). The c16 arm replaces only the system text and the
  closing check (the reviewed `probe_c14.py`, unchanged, which also checks every stored request carries c8 exactly).
- **Guards** (stored states of `cases-c14.json`, not tuning material): memory, Ohio, capex-open, capex-repeat-a (a repeated capex report:
  must merge), population (another population of the aggregate: must merge), in d1–d3.
- 30 states × 2 arms × 3 sends = 180 requests; dry run: about $2.65 at published rates; **ceiling $4**; spend under D439 then at most about
  $22.4 of $40. A synthetic c16-conformant answer (a 2027 capex thesis on fresh-T11) passed the schema and the runner's checks.

## Counting (by Claude, every answer read; a disputed mark goes to a blind second reader)

Per send, on its retained new theses and links:
- **T1 target:** a new thesis on the article's shared quantity for 2027 (the year the reader named).
- **T2 target:** a new yes/no thesis on whether NVIDIA signs the reported OpenAI deal (financing, guarantee or backstop) by a check date.
- **T3 failure:** two new theses for the two years of the compared quantity, or a new thesis the reader expected to be a link.
- **T4 failure:** a new thesis on what the reader's open question clean-N tracks. A T4 article is exercised only when some send of either arm
  links the statement to clean-N or opens a duplicate; otherwise reported unexercised.
- **Guards:** memory: sends with a memory-price thesis in the 2027 or 2026-to-2027 shape, over all sends; capex-repeat-a and population:
  sends opening a duplicate of an open capex thesis; Ohio and capex-open: the target behaviour, reported.

## The lines (frozen before any send; 12 sends an arm on T1, T2 and T4, 9 on T3 and on each guard)

| line | met | inconclusive | not met / regression |
|---|---|---|---|
| T1 target | c16 − c8 ≥ +4 | +2 or +3 | ≤ +1 |
| T2 target | c16 − c8 ≥ +4 | +2 or +3 | ≤ +1 |
| T3 failures | c16 − c8 ≤ +1 | — | ≥ +2: regression |
| T4 failures (exercised articles) | c16 − c8 ≤ +1 | — | ≥ +2: regression |
| memory guard | c16 ≥ c8 − 1 | — | ≤ c8 − 2: regression (D441's) |
| capex-repeat-a, population duplicates | c16 − c8 ≤ +1 each | — | ≥ +2: regression |

**Verdict:** *passes* when at least one target is met, neither target is "not met" by a negative difference, and no regression fires;
*fails* when any regression fires, or both targets are not met; *inconclusive* otherwise. A refusal, a format failure after its resend or a
run-check refusal counts as a send without the target and without a failure, and is listed. A result against the hypothesis stops the line
and goes to the council (AGENTS §7.3).

## Before the send

The whole-request audit of the change by a blind reader (`audit-c16-blind.md`, running); `scripts/preflight.py` on the stored c3 trace;
the council's review of this page, the candidate and the audit.

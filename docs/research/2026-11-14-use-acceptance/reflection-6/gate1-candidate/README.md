# Gate 1 on your 44 topics: a prepared draft, launched only on your word

**What this is:** the same Stage A measurement you ran four times (44 topics, 3 passes each, 132 answers), prepared for a stronger
model. Nothing has been sent. Under D426, a fifth Stage A is your call.

**Two configurations. You pick one:**

| | `astra-frozen` | `astra-a2-v2` |
|---|---|---|
| **Model** | astra (published price 100 times the current model's) | astra |
| **Instructions** | today's frozen instructions, unchanged | today's, with arm A2's changes and the due-day fix |
| **What we know, on topics outside your 44** | broke one of your lines 1 to 4 in 4 of 78 attempts, every one a decline on a topic that names several things. Its second screen closed by its own rule (D634) | never measured as this pair. A2's two readings were void and the due-day fix's check was inconclusive (D637, D640, D641) |

**What `astra-a2-v2` changes:**
- **Arm A2:**
  - the topic's wording is read as its description and its outcome;
  - your D436 sentence: another side of the same bet stays as context, and is not by itself a reason to decline;
  - the closing check reads "every other part … that the question leaves out", matching its own instructions.
- **The due-day fix:** the "next annual report" day applies to amounts, not to whether a deal closes.

**How it is read:** unchanged from the fourth Stage A.
- the same reader brief (`clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md`), both reader families;
- the same scoring (`clean-arch/step4-2026-11-10/stage_a/collect_readings.py`), with its rules for missing or invalid readings;
- your six lines as written.

**What a pass would and would not mean:**
- It would pass Stage A only. The other gates remain: the judging stage, the end-to-end comparison and live use.
- A run that stops early, or is incomplete, ends with "NOT MEASURED" and is not a pass.

**Cost** (estimates from astra's measured cost on outside topics, not a guarantee):
- **Expected:** about $4.90 to $6.60 for the 132 answers, before retries.
- **The cap:** at least about $9. That leaves room for up to two attempts in flight, each reserving up to about $1.20. A higher price
  can still stop the run.
- **Budget:** this is beyond what remains of today's $40 (about $2.26), so it needs your new ceiling.

**To launch:**
1. Write `authorization.json` in this folder, for example `{"config": "astra-frozen", "cap_usd": 9.5, "by": "Alex"}`. The launcher
   checks what the file says, not who wrote it. It is a procedural guard: the step stays yours.
2. Run `python3 gate1_candidate.py launch astra-frozen <new run folder>`.
3. Read the result with the usual six-line form.

**Checked at no cost:**
- every one of the 132 requests is today's request with only the model (and, for `astra-a2-v2`, the recorded changes) altered
  (`check-output.txt`);
- the fourth Stage A's 148 stored answers pass the current checks exactly as they did when stored (`preflight.txt`);
- the launcher refuses without your authorization, and a run that stops reads NOT MEASURED;
- a dry run through the real runner, on topics outside your 44, works for both configurations;
- the preflight refuses when it finds no stored attempt or a verdict that differs;
- tests pass, 9 of 9.

**Before any paid launch:** run `python3 scripts/preflight.py` as AGENTS §5 requires, and read what it exercises and skips.

**Not checked:** whether each guard is the one that fails its test. The mutation runs were refused by Claude Code's permission check
and were not worked around (`mutants.txt`).

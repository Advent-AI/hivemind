---
name: council-loop
description: Drive a measured improvement of one pipeline step to a pass line Alex sets, in rounds, with a Codex–Claude council at every decision. Use it when a step's quality must be raised or a new step validated. It takes the work from census to mechanism, independent council, cheap probe, blind scoring, council on the results, whole-bench run, a source-backed pass-line verdict, a written log, and a reflection council for the next angle. Alex, 2026-11-07 - "我觉得这几次的循环很有效的逼近问题我觉得应该把他写成一个skill".
---

# Council loop: census → mechanism → council → probe → blind score → council → whole bench → verdict → reflect

This loop took the clean Step 1 from 70 noise items in 160 to a library that passed Alex's line in two forward draws, in one day
(`clean-arch/takeover-2026-11-07/LOG.md` §§1–15). It works because each round:
- measures before it changes anything;
- has an independent reader grade every claim;
- names in advance the result that would stop it.

AGENTS.md governs every step. This file only orders the steps and records the traps already paid for.

## 0. Frame (write it at the top of the round log before anything runs)

- **Objective and pass line, in numbers.** Use Alex's words when he set them. Otherwise propose numbers, label them "proposed, not
  confirmed", and ask him in the report. Example from Step 1: at most 3 small theses, no fragmented bets, helpful at least 190 of 234
  on the 115 gold articles, forward from empty, one draw.
- **The reference system.** Name it: frozen production, or the previous candidate. The pass line is relative to it unless Alex says
  otherwise.
- **The ruler.** Name it and its sha256 (AGENTS §7.1). It is frozen. A disagreement with the gold is a gap in the system, and a
  reader's judgment never relaxes a signed rule (see the trap list).
- **Constraints and out of scope.** Alex's decided contract for the step, frozen files, and modules not taken up.
- **Budget.** The cost ceiling per probe and per whole-bench run, from published rates (`hivemind.model.PRICES`).

## 1. Census on stored data ($0 model; blind readers)

Before any idea, count what is wrong, by class, on stored runs.
- **Method:** compare the current system with the reference on identical inputs. Readers see both outputs reduced to one shape,
  under shuffled labels (key kept outside the repo). They list each input's matters from the source first, then mark coverage, extras
  by reject class, wrong statements and wrong links.
- **Toolkit:** `build_census_packets.py`, `tally_census.py`.
- **Ranking:** rank the classes by size and by product impact. The largest class is the round's target.
- **Check the instrument:** spot-check the readers on two inputs whose answer you traced yourself.

## 2. Mechanism

For the target class:
- Read raw answers beside their inputs, with the whole request as the model reads it.
- Get the model's own account (`model_account.py`: continue the stored conversation, ask which instruction led there, and what it
  would have done). It locates a reason; it does not prove a fix. It found the "container thesis" mechanism in Step 1.
- Search the decisions and earlier experiment logs for the mechanism by name (AGENTS §2.4); quote what they rejected.

## 3. Council A: independent, then challenge

- **Independent investigation.** A fresh Codex session reads the primary material cold, with no preferred conclusion
  (`templates/council-independent.md`):
  `codex exec -s read-only -C <repo> --skip-git-repo-check --json -o <out.md> - < handoff.md`. Keep the `thread_id` from the first
  JSON line.
- **Your own reflection.** Write it to a file before reading Codex's.
- **Challenge rounds.** Resume the same thread with `codex exec resume <thread_id> -c 'sandbox_mode="read-only"' ...`
  (`templates/council-challenge.md`): send your findings, your disagreements and the proposed arms. Ask for counterexamples,
  missing isolation arms and falsifiers.
- **Stop condition.** Every arm, article set and falsifier is agreed, or the remaining disagreement is written down. Codex's report is
  a lead: read the file it cites before acting (AGENTS §1).

## 4. Design arms

- **Prefer structural levers over sentence wording.** In order of what has worked:
  - the output contract (an outlet such as "unfiled");
  - a required field that forces the decision per item (closest open thesis, why a separate bet);
  - reasoning effort;
  - the model;
  - the placement of a check after the input.

  Sentence-level wording and order edits failed repeatedly.
- **One lever per arm,** plus an isolation arm for each combined change, so the effect can be attributed.
- **Each arm states its source:** a line of the standard, a decision, or Alex's words. It states its falsifier before it is sent.

## 5. Cheap probe

- **Inputs.**
  - Fixed before-states from a stored run, so arms differ only in the request.
  - Articles: the cases that motivated the change, controls that must not regress, and inputs carrying the next class (for example,
    noise).
  - 3 draws per arm.
- **Before any send:**
  - the control request rebuilt byte for byte from the stored one (`probe.py` checks it);
  - a synthetic answer through every code check;
  - the call count and cost estimated;
  - one line on what the probe will decide.
- **Toolkit.** `probe.py` takes arms as files `<arm>-system.txt`, `<arm>-closing.txt`, optional `<arm>-schema.json` and
  `<arm>@<variant>-settings.json` (model, effort, provider, `json_mode`). Each (arm, draw) gets its own archive, so repeats are fresh
  samples.

## 6. Blind scoring

- **The frozen ruler by code** (`score_round.py` for probes, `score_gold_runs.py` for forward runs). Print the gold sha256.
- **Blind readers on everything the ruler cannot see.** Theses: bet, small or duplicate. Unfiled items: fine, should open, or an
  open thesis takes it. Fields: summary, passages, party, tier, dates, links, worth keeping. Readers see all arms mixed under shuffled
  labels (`templates/reader-blind-compare.md`).
- **Source-backed review.** Any item the readers disagree on goes to three readers with its source text
  (`templates/reader-source-backed.md`). Readers who saw only the library ranged from 1 to 5 small theses; with the articles, they
  agreed.
- **Read by hand** the added hits and the lost items of the winning arm. Classify each as real, match artefact, or small-by-design.
  Report regressions first.

## 7. Council B on the results

Send the table, regressions first, to the council thread. Ask it to challenge:
- whether the gain is real (for example, does a hit match on the quote or only on word overlap?);
- the decomposition (which lever did it);
- what the next class is.

Decide: carry the candidate to a whole-bench run, run one more isolating probe, or stop. If a result contradicts the hypothesis, stop
the line and re-diagnose; never add an arm to cover it (AGENTS §7.3).

## 8. Whole-bench run and verdict

- **The run.** Forward from the agreed starting state, in source order, inputs pinned (`SHA256SUMS`), limits scaled to the run.
- **Repeat at the line.** Run a second draw when the first lands at the line, and report both.
- **Verdict.** Score on the ruler, then have three independent readers judge the outcome against the pass line, source-backed where
  they disagree. Report the verdict with every caveat: one draw, match counts, exposure of the evaluation set, your own disagreements
  with the readers.

## 9. Write it down, every round

- **The round log**, one section per round (`templates/round-log.md`): hypothesis, change, numbers against the reference
  (regressions first), the council's position, verdict.
- **`docs/CURRENT_STATE.md`**: the status and the one next task (English only; `python3 docs/check.py`).
- **The memory resume point.**
- **Code changes ship with a test and a mutant.** The mutant runs in a mirrored scratch tree with `PYTHONDONTWRITEBYTECODE=1` and no
  `__pycache__`.

## 10. Reflection council (at the pass line, or when two rounds move nothing)

- A fresh Codex session reads the whole record cold; you write your own reflection first.
- One or two challenge rounds agree on: the lessons at mechanism level, the conclusions weaker than they look, the remaining
  problems by product impact, and the next breakthrough angle with its falsifier.
- That angle starts the next run of this loop.

## Report to Alex

- Plain Chinese, answer first, then one concrete example, then the table with regressions first.
- What the council agreed, what it disputed, and what Alex must decide.
- No new rule enters a prompt without its source. A product trade-off goes to him with options and a recommendation.

## Traps already paid for

- **Relaxing a signed rule on reader judgment.** Readers called an existing $6.3bn arrangement "core"; the frozen gold marks it not
  kept (D250 boundary 1). The relaxed rule let 10 noise items in. Check the gold before relaxing.
- **Tuning on probe differences inside sampling noise** (K3 against K4). Stop and run the whole bench instead.
- **One draw read as stable.** Two draws of the same configuration shared 188 of 214 helpful hits.
- **Library judged without article text.** Always attach the source for verdicts that decide the pass line.
- **A fixed-state probe cannot show cascade effects;** only a forward run shows how one article's choices shape the next.
- **A budget limit copied from a smaller run stops a big run halfway.** Scale `max_usd`, `max_seconds` and `max_calls`.
- **zsh does not split an unquoted variable into arguments.** Write the arguments out.
- **A stale bytecode cache makes a mutant pass** when the mutated line has the same length and the same mtime second.
- **Low reasoning effort mis-applies judgment rules** (it over-suppressed big matters). Test an effort arm before blaming a rule.
- **Pair-level accuracy is the wrong unit when records bundle facts.** Step 2's pair agreement was 82%, yet per incoming record, on
  a forward simulation, detection was close. Score the decision the product takes per record on the library it would really see; a
  fixed-history replay assumes every earlier merge was right.
- **Model readers over-flag materiality.** Two readers flagged 66 of 102 merges as losing a material fact, but a hand-read of a random
  12 found only 3 clearly material. A materiality gate shown to the model (Jev's stricter repeat) behaves the same way. Hand-read a
  random sample before quoting the readers' count.
- **Cuts made to keep a prompt length-neutral are levers too.** In the unfiled round, u1 cut two sentences beside its one change; the
  cuts, not the change, moved filing and noise. Make each cut its own arm, or let the prompt grow with a written reason.
- **Calibrate the readers before trusting a per-item count.** Two reader families judged the same 48 control answers as 15 against 6
  should-be-filed items. Run the source-backed adjudication of disagreements (step 6) before reading arm differences smaller than the
  readers' own gap.
- **Model readers carry their family's threshold.** Two adjudicators given the same rubric sided with their own families (17 of 52
  agreed). When the families split on "how big is big", take a balanced set of boundary cases to Alex; his rulings are the ruler.
- **Signed text copied piecemeal into another contract can contradict it.** Audit the whole request, closing check included, before
  proposing a sourced restoration.
- **Keep reviewing a design with a fresh reviewer each round until one finds nothing serious.** The conditions design took eight
  rounds, and round 7 found a latent defect in existing code: Step 2 cut passages at 600 characters for 16% of items. "Ready" means the
  design rounds are clean; the prerequisites (tests, reports, an independently reviewed reference) are build work done before the send.
- **A truncated printout miscounts anchors.** A printer that cut summaries at 120 characters hid a margin figure inside combined
  items; the control was called 0/6 when it was 5/6. Count an anchor by searching passages and summaries for the figure.
- **A design gate is not a prompt audit.** Eight design rounds passed, and the arm's text still kept wider than Alex's ruling, linked
  narrower than his ruling and widened "big matter". Walk each of Alex's rulings through the changed request at $0 before any send.
- **One rare bundle of a widely repeated statement cascades.** One Step 1 record holding both a report and the company's denial (1 in 9
  samples) turned six later denials into wrong merges. Read wrong merges for one shared original before blaming the comparator, and
  fix the unit at Step 1 ("one party's statement per item"), not with a probability cut.
- **The judge's criterion and the line's test must be one ruler.** Jev's "same evidence" against the readers' "main statement" made
  4 of 8 wrong merges. Aligning Jev's wording to the line's test removed them.
- **An output cap binds on the longest articles.** At high effort, reasoning alone can exceed 32k tokens. A cut answer is not JSON: retry
  it as a format failure, and size the cap from the longest completions seen.
- **Number records by a stable identity, never by a count of completed rows.** One failed item shifted every later id and broke the
  reference mapping (34% mapped instead of 86%).
- **Check theses against the frozen question gold, not only the readers.** Readers called most theses "bets" that the gold lists
  must_not. When the two references split widely, that is Alex's decision.
- **A fix found by reading a probe is a new arm.** Tonight four arms (c4, c5, c6 and the Step 2 criteria) went out after trace reading and
  the model's account, with no council round. The retro council found one ruling widened beyond its words (valuation), one rule too
  broad (c5 "a comment") and selection on the test set. Council before every send, Council B after every result.
- **Never choose among configurations with the test set.** Five configurations each scored "once" on the same exposed test are a
  selection, not an acceptance. Freeze, then measure on fresh articles.
- **A provider without strict JSON schema** (DeepSeek) needs the schema stated in the system text, a code check on every answer, the
  exact sent request recorded, and a failure policy.

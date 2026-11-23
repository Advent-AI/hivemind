# Stage A's agreed failures on the full run, traced to the judge (D458), 2026-11-13, $0

**Answer: the falsifier fires. The judge used only the first pass (`<draw>/judge-inputs.json` names `ladder/send-1`), and of the agreed
faults only three are in the first pass: three different rules, one case each, none on a graded ruler question.** There is no substantial
class to repair in the ladders the judge received.

## What the judge received

| first-pass fault (both third readers agree) | the Step 1 thesis | the ladder the judge got | reaches the judge? | graded? |
|---|---|---|---|---|
| c3/clean-1, Q: the question names no model | "…under its new revenue-sharing and credit-support business model?" | "…committed to AI cloud partners **under this model** by the FY2027 annual report…": the descriptor dropped in the rewrite | yes | no (matched to q09 as narrower) |
| c3/clean-7, L: a part of the outcome left out unlisted | "commodity DRAM (and by extension graphics memory) contract prices … through calendar 2026" | commodity DRAM only; the shortage listed as not judged, graphics memory not listed | yes | no |
| c2/clean-10, N: refused for "two figures, none main" though the outcome leads with one | custom-ASIC purchases by the top US hyperscalers in 2026, compared with NVIDIA GPU purchases | none: refused, never judged | no (wrongly refused) | no |

The other agreed faults are in passes 2 and 3 (c3/clean-3's Yes covering every outcome, c2/clean-8's threshold already crossed, c1/clean-5's
left-out part), which the judge never reads.

## The one recurring mechanism

The wrong "two figures" refusal recurs across Stage A populations: u3/clean-11 (sends 1 and 3) and acc/clean-9 (send 2) in the fourth
Stage A, where the model said its decline "was incorrect" and "I over-applied the instruction" (`clean-arch/step1-diagnosis-2026-11-12/
DIAGNOSIS.md`), and c2/clean-10 here: four sends over two populations. The ladder step is frozen (D426); D432 offered mending its
remaining faults and Alex chose Step 1's diagnosis instead.

## The refusals the judge's path made (not faults, recorded for the PRD goal)

11 of the 40 theses were refused in the first pass and never judged. Ten refusals count as right under the favourable treatment (several
are family splits ruled one way, e.g. Firmus's stake and the H100 rental price; council round 5): five theses that track
two figures or two outcomes (Firmus amount and stake, federal AI spending and awards, the Intel stake's size and carrying amount, 2026 memory
prices and rack memory cost, US approval status and China sales scale), three rolling twelve-month figures with no publication day (the
China domestic-share survey twice, memory prices to mid-2027: D417, Alex: "确认：这类题不出题"), and two H100 rental-price theses no listed
theme covers (the readers split; ruled right). These are Step 1 shapes the ladder step must refuse: D432's "theses with no ladder", whose
Step 1 change (c14, c15yc) failed and stopped (D441, D391); D436 settled a second side of the same bet as one question (Alex: "算一个题，
第三处不改"), not every question that holds two figures. Two of them are the memory question (c1, c2), the opening review's M5.

## Limits

One draw of each clean path; the first pass is what the judge reads, so the passes-2-and-3 faults show the step's variability, not what was
judged; the effect of the "this model" wording on the c3 credit-support judgements was not measured (the question is not graded).

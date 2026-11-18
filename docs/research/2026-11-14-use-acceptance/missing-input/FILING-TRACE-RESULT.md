# Why the two figures were not filed under the question they bear on: the trace of two decisions (D531, under D439), 2026-11-15, $0

Read in the stored records only: the requests as sent, the answers as returned, the checks' records. Nothing was sent. The two paths
are in two systems and are reported apart; they need not share a cause.

## 1. The new system: Broadcom's guidance and the custom-accelerator question (a later-linking decision)

- The statement (group `63:E-5`): "Broadcom guided third-quarter AI semiconductor revenue to $16.0 billion, more than 200% year over
  year, as a custom-ASIC alternative to NVIDIA accelerators", read at article 63, kept with no question.
- The question (`clean-7`) opened at article 65: "How much will Amazon, Google, Microsoft and Meta spend in calendar 2026 on custom
  AI accelerators (such as Trainium, TPU, Maia and MTIA), a measure of how much AI compute demand bypasses NVIDIA's GPUs?"
- When it opened, the later-linking step checked 74 earlier groups and linked two (`library.json`, `later_log`). The check on this
  statement is stored (`step2/jev.sqlite`, call 200). It was shown the question and the whole statement and asked: "Does the STORED
  PIECE below inform the THESIS stated above? Use only the supplied text; a shared company, product family or word is not enough,
  and the company's overall results, guidance and estimates inform a thesis about its revenue or earnings path, not one about a
  competitor, a supplier or a policy unless they speak to it." **The answer was 0.12 on a scale from 0 to 1: not linked.**
- So the negative decision is the comparison model's, on a complete input, and it is consistent with the question's written
  criteria (a supplier's overall guidance does not "inform" a question about its customers' spending "unless it speaks to it").
  This does not prove the wording caused the answer, or that a figure not broken out by buyer should have been linked to this
  four-company question (council round 23). The statement does not name the four buyers; its neighbour from the same article,
  which names two ("Broadcom's custom chips for Alphabet and Meta"), was linked.
- The same fact arrived again at article 92 and was filed under the question by the reading step, which had the question on its
  list. Two deciders, two outcomes for one fact.
- The frozen judgement reference uses this figure as its basis for the matter (D354, known defect 4).

## 2. The old system: the next quarter's guidance and the data-center revenue question (the reading step's own filing)

- As shown to the reading step (article 35 and after), the two questions and the lines that say what belongs in each file:
  - total revenue: "takes: total_revenue figures, guidance, estimates and revisions for Nvidia total revenue in FY2027";
  - data-center revenue: "takes: segment_revenue figures, guidance, estimates and revisions for Data Center".
- The frozen reading prompt: "file each one through its links ...: the narrowest open question whose takes line covers it, your
  own candidate, or both." The answer form's own instruction for the links says more (`src/hivemind/placement.py`, D259): the
  narrowest open question "whose answer this statement makes more or less likely, as that question's own figure, step or
  estimate or through the demand, supply, competition or pricing behind its answer; compare the specific questions before a
  company-wide revenue or margin question and take that one only, never a broader question beside it".
- **In all fourteen raw reading answers that wrote the guidance down, the model linked it to the total-revenue question only**,
  before any check. No check removed a link.
- So the filing is the reading step's own: the guidance is the total-revenue question's own figure, and one home is the rule.
  Whether total-revenue guidance belongs under the segment question instead, under that one-home rule and its "compare the
  specific questions first", is a judgement these records do not resolve (council round 23).

## 3. What the two have in common, and what they do not

- **In common, as observed and no further:** in both cases the deciding step had the whole statement and the question before it and
  filed the statement elsewhere or nowhere; neither is a broken check or a truncated input. That both systems categorically
  leave out statements that bear through a related quantity is **not** established by two cases (council round 23): the old
  system's link instruction names indirect evidence, and the new system's check linked a neighbouring statement.
- **Not in common:** the decider (the reading model on takes lines; the comparison model on a yes-or-no question), the system,
  and the moment (at reading; when a question opens).
- **A lead on the old system, and a decision that already covers it (D368, Alex, 2026-11-05, which I had not found):** "the matching
  step chooses a new thesis's dependencies (D51), which the default Jev path does not ask today" is one of three decided rules
  to be built and measured, each as its own slice; and by the same decision the supported (root) question reads its supporting
  (driver) questions' conclusions. So the empty dependencies of the stored runs are known and decided. Two things follow for
  any use of the lead: the direction must be D368's (it is not given that the data-center question would read the total's
  conclusion), and a judge receives a dependency's conclusion and shortened reasons, not its statements. PRD 10 lists the
  dependency arrows apart from its filing work.

## 4. Counts already on record that may hold the same kind of case (not counts of this cause)

- The trial's reading of the frozen reference's 62 facts on the July window (D485): facts linked to another question only and
  never delivered to their own: 19 in the old system, 4 in the new. Why each was not delivered was not established, and that
  reading had no known case of a changed answer.
- The new system's fresh week (D508): three confirmed fact-and-question pairs, 23 open.
- The fresh week's old system: this guidance and consensus; the six pairs kept under other questions.

## 5. What this trace may and may not be said to show

- Shown: for these two decisions, which step decided, on what input, under which written rule.
- Not shown: that a change to either rule would deliver these facts without filing noise under every related question (the
  rule's purpose); that a dependency would carry them; that any answer would change; a rate.

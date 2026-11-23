**A common lead remains, but the proposed assumptions field is not yet a demonstrated correction.** I support a $0 design and evidence note, followed by council review before any send. The note should present the product choice without deciding what Alex should see.

The four raw replies match the saved accounts. All four identify an assumption that the shown evidence does not quantify. In the two unsized cases, the follow-up also acknowledges that the chosen lowest band was not justified. That is a useful lead for separating **what the evidence says** from **what the forecast assumes**. It does not prove the original model knew this at the time, nor that a closing check or new field would change its answer. [Accounts](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/unsupported/ACCOUNT-RESULT.md)

**The previous-conclusion finding is partly right, but one example needs correction.**

- **Data-center revenue:** the prior conclusion shown in the request already contains the approximately 25% Q4 assumption and the $75 billion Q1 figure. The later answer repeats them. That establishes carry-forward; it does not establish that the $75 billion figure was invented, or that seeing the prior conclusion caused the later choice. Its origin needs tracing.
- **Credit support:** the prior conclusion in the stored request contains the **undiscounted $25.6 billion estimate**, not the one-fifth factor. The stored answer introduces the one-fifth factor when moving to roughly $9 billion. So it is not evidence that the one-fifth returned through the previous conclusion. [Stored requests](/Users/lchingen/hivemind/poc/data/clean-judge-account-2026-11-15/requests.json)

Please correct the result page’s statements that both assumptions were in previous conclusions. The genuine risk remains: a prior answer is shown again, and the instructions say earlier material not shown is carried by it. Whether an unsupported assumption *causes* later answers to inherit it requires a trace or comparison, not this one request. [Judge request construction](/Users/lchingen/hivemind/src/hivemind/views/judging.py)

I would prepare **one design**, with a short reader-facing note as its introduction:

- State the observed cases, the concentration of the 31 counted observations in a few repeated question paths, and the different possible product responses. Do not present the middle band as evidence-supported merely because the amount is unknown.
- Trace the origin and later use of the **25% and $75 billion** through the stored answers and evidence; also trace the $25.6 billion-to-$9 billion change. Include supported forecasts where a calculation legitimately uses a comparable or assumption.
- Specify every reader of a proposed assumptions field, including storage, display and the next judgement. Decide what it means if a number comes from a previous conclusion whose original evidence is no longer shown.
- Compare the full changed request and its schema with the frozen instructions and reference. A new field and its description are themselves an instruction; adding it to the form does **not** guarantee the model writes or reasons through it before choosing a band.
- Predefine what the test must change for a reader: identifying an assumption is useful only if the label is accurate and visible, and it must not wrongly flag supported calculations or suppress legitimate forecasts. Test the multi-day path as well as individual answers.

The **stop** is a design or stored-data check showing that the field cannot distinguish unsupported steps from legitimate forecasts, that its consumer cannot preserve their provenance across days, or that the proposed behavior requires an unresolved product choice. If those checks hold, the council can review a concrete proposal for a small paired proof. A populated field alone would not prove the judgement is improved, and nothing is adopted by that proof.

The short note for Alex can explain the choice between showing an answer with its assumptions and withholding or otherwise qualifying an answer when evidence does not size it. It should not claim D59 already decides that case. Under your stated boundary, adoption of a product behavior remains for Alex.

Council position: Correct the previous-conclusion account, prepare a $0 design and concise evidence note around separating sourced figures from assumptions, trace the multi-day cases and controls, and return the design to the council before any send or product change.
**SEND WITH CHANGES.** The field asks the model to explain company impact, which addresses the observed comparison with other deals. It may still give an unsupported explanation, so the probe must inspect the reasoning.

The main conflict is that `company_impact` exists only on **new** questions, while the final check also applies when the signing question is already open. It asks the model to write the field for that open question and may then tell it to “drop that question.” Make the check work for an existing question without changing or dropping it. [Schema](</Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c11-schema.json:60>), [closing](</Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c11-closing.txt:17>).

The field otherwise preserves the D248 company-impact test and permits other deals as context. “Company’s known scale” could invite an unsupported figure; require the explanation to distinguish what the provided material states from an inference.

The falsifiers cover the main failures, but add these checks:

- Ohio must retain **both relevant links**, and no part of its answer may present the project cost as the guarantee amount.
- Inspect every obligation’s impact explanation for unsupported figures or a mere assertion of importance, including when the field is `null`.
- Inspect changed links against the source; a count within 10% can still hide a consequential error.

**SEND WITH CHANGES**
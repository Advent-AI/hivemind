READY TO SEND
plan-sha256: 0f3563b26b48649ea52e0b7c132fc0366286800635aaf148d113a7608916fb79
candidate-sha256: 62deda0b0ebc148de2369087398e3e28dde115401ebb3572a7196ccb1b58c305

This is readiness for the bounded exploratory experiment only, not production adoption or a finding that the candidate is equivalent or effective. I independently checked the bytes of `prepared-1/plan.json` and `candidate.txt` against the hashes above. The plan was hashed, not reviewed for execution safety or experimental design. This is a blind standards review: I did not inspect model answers, experiment results, previous reviews, case labels, private files, or paid keys, and made no model calls.

## Current full comparison question

The current `clean-arch/step2/compare.py` criteria are:

- `same_statement`: “the INCOMING PIECE reports the STORED PIECE's main statement: a retelling, another outlet carrying it, the same number in text or a table, or the same speaker repeating it; wording, precision and extra detail may differ. If the stored piece carries several statements and the incoming piece reports only a secondary one, this is not it”
- `supersedes`: “a later version of the stored piece's main statement, changed: the same speaker revises that guidance, forecast or event-progress statement, an official confirms or denies that reported claim, or the original source revises it; another statement on the same topic is not this”
- `different`: “a different fact, figure or matter, a figure for another period or quantity, or only a secondary statement of the stored piece, even if on the same topic”

The question instruction is: “How does the INCOMING PIECE relate to the STORED PIECE below? Use only the supplied text. STORED PIECE:\n” followed by the stored piece. The incoming piece is supplied as state.

## Candidate and standards assessment

Candidate: “Identify the statement addressed; a later change to the stored main statement: the same speaker revises that guidance, forecast or event progress, an official confirms or denies that claim, or the original source revises it; another statement on the same topic is not this”

PRD §5 defines a repeat as the same statement again, a revision as a later account changing the same statement, and new evidence as neither identified relationship. It says words, amount, speaker, source and time can matter; a later statement on the same subject need not be a revision, and the same amount alone does not prove sameness. D168 describes a later changed version of the same statement or number: the same speaker revises it, an official confirms or denies the claim, or the original source revises it. It specifically mentions guidance revisions and an original source revising its own figure. PRD §5 also identifies an official denial of a report as a revision.

- “Identify the statement addressed” introduces a procedure but does not specify that the statement must be stored or allow explicitly for none. A new statement may address no stored statement; the phrase could also identify a secondary statement or a topic. The later criterion still requires the stored main statement, and `different` expressly covers a secondary statement. This ambiguity is a concrete risk, not a demonstrated behavioral change.
- “A later change to the stored main statement” retains the main-statement and later-account boundaries. It does not by itself determine chronology where the supplied text does not establish it. The current wording says a later changed version; the candidate's shift to “change” does not establish equivalence.
- “The same speaker revises that guidance, forecast or event progress” retains those cases and points back to the stored statement. An ordinary later event-progress update can qualify without explicitly responding to or citing the earlier account, provided the supplied text supports that it revises that statement. The same topic or subsequent development alone does not establish that relationship.
- “An official confirms or denies that claim” retains confirmation and denial explicitly. Confirmation may leave the claim's content unchanged, which sits awkwardly under “change”; the existing criterion also places confirmation under a changed version. The text does not resolve that tension.
- “The original source revises it” retains that case. Neither the candidate nor the existing criterion fully disambiguates original source or establishes source identity where the supplied text leaves it unknown.
- “Another statement on the same topic is not this” retains the topical boundary. Implicit references remain possible; nothing explicitly demands a direct reference. The supplied text must support the relationship, rather than identity or chronology being assumed from a topic alone.
- D168 explicitly includes a statement or number and a source revising its own figure. The current and candidate criteria speak of the stored main statement without separately naming changed numbers; a number expressed as that statement is not excluded, but the candidate does not make number treatment explicit. The sibling `same_statement` mentions the same number, while `different` distinguishes another figure, period or quantity. These boundaries do not settle all cases in which material repeats a statement and adds detail.

I find no definite blocking contradiction in the candidate's actual wording with PRD §5 or D168. The uncertainties above are not evidence that the wording will behave equivalently; the bounded experiment must test its effect. Source identity and chronology must not be invented when unavailable.

Final check (read-only). `library.labelled_passages` now shows the found source text (verified value) as "Quote", and the model's
text as "Unverified quote" only when the verified value is None; the record keeps the model's `passages`. A new test covers a
repaired quote; a mutant that shows the model's text is caught. The Jev-input mark is recorded as an open item in
`docs/CURRENT_STATE.md` (open defect 4) and LOG §47. Suites: full 285, clean-arch 92, frozen rulers 3; docs/check passes.
Under 150 words. End with READY TO COMMIT or the blocker.

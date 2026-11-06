# Two-article gold drafts: disagreements to resolve

Both readers are AI; neither is a human reviewer. Both read the same original article and the earlier SEC release before seeing any experiment answer. Neither draft is gold, signed, frozen or safe to score. No report-context model calls have been sent.

| Article | Comparison | Status |
|---|---|---|
| Wardogs | Both identified no keepable research matter in the game-release update. | Agreement, still needs standard and source review. |
| Skild | Both identified the use of NVIDIA infrastructure, Skild's $100m run rate / >60 partners, and the deployment for Blackwell assembly as supporting. | Agreement on tentative matter and weight, not automatic proof. The Skild figures belong to Skild and are a run rate, not NVIDIA revenue or already earned annual revenue. |
| Skild | Independent reader also proposed a distinct matter: Skild and NVIDIA are developing simulation solvers and plan to make them available in Newton. First reader omitted it. | Unresolved: source text is explicit; check whether this is an incremental partner action or technical detail under standard §5.1/§5.3/D250 before adding or excluding. |
| Skild | First reader assigned party-statement tier to the three items; second reader assigned fact. | Unresolved: review each exact claim, whether a public announcement establishes an action vs an assertion/plan, and who actually confirmed it. Do not infer a universal tier from the publisher alone. |
| Both | No reader claims original captured pages are proven unchanged since publication. | Check historical version or clearly limit interpretation. |

Source spans in both drafts were checked as literal substrings of the supplied article body (6 author spans and 10 independent-reader spans). This check does not decide whether the matter should be kept or its tier/weight. An independent standard review and resolution must precede Alex's review and any scoring.

## Provisional source-based resolution

A further independent AI read maps the three agreed items to `fact` under §5.5 for reported actions and published actual figures; this corrects the first draft. It flags that the article does not explicitly say Skild confirmed the figures. It recommends preserving the specific future public release of the solver separately, while keeping that release as a plan. The planned release is provisionally `party_statement`; the mixed-record tier remains a reasonable uncertainty, and no new standard rule is made. Full reasoning: [independent-adjudication.md](independent-adjudication.md). The consolidated draft is `draft-gold-resolved-two.json`, still unreviewed by Alex and not frozen. The Wardogs copy was later found to omit the source page availability caveat, so that source is excluded pending historical verification.

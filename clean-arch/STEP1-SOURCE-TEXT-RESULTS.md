# Step 1: source-text comparison

## Result

On these selected articles, the recorded prepared source removed some concrete contamination, but it did **not** reliably solve extraction or source interpretation. The clean production path is not changed. [Open the article replay](../poc/data/clean-step1-source-text-comparison-2026-11-07/review.html) to inspect both texts, every answer, the cited passages and thesis links.

All 60 requests completed: ten previously examined articles, three fresh answers from the original cleaned text and three from recorded source-role-selected text. Each pair used the same saved pre-item thesis state, prompt, schema, metadata, model and reasoning setting. The selected text can add and remove several lines at once; output differences cannot be attributed to any particular line. The source selector itself was not rerun, and the selected role records were chosen after earlier inspection. The prepared arm's existing validator also checks a citation against the captured original page, whereas the control uses its original check; do not treat the validation counts as a same-check comparison.

Independent readers examined the captured page, open theses and all 60 anonymized answers before the condition key was opened. Actual sent text was then inspected to distinguish source preparation from extraction. Answer content itself can reveal which text was used, so this is condition-hidden, not fully blind. Original reviews and the later independently checked observation about article 28 remain separate. These are three draws on known articles, not a population error rate, an acceptance test, or proof of a causal mechanism.

## Source-backed observations

Counts are answers out of three in each condition for the named article. Findings overlap; a sample's difference does not establish a general improvement or regression.

| Article | Original cleaned text | Prepared text | What the trace shows |
|---|---:|---:|---|
| 3: unrelated DayOne listing teaser treated as Firmus listing risk | 2/3 | 0/3 | The old input contained the unrelated teaser; selected text excluded it. Both conditions still retained the main reported investment in all three answers. |
| 3: $15.5bn valuation given an explicit US-dollar currency | 2/3 | 3/3 | The captured article does not explicitly label that figure's currency. Source selection did not resolve this qualification issue. |
| 8: page-generated summary cited as source text | 2/3 | 0/3 | The original cleaned text included the generated-summary sentences without their label. The selected text excluded those sentences. The authored technical article also contains corresponding details, so source identity and context matter. |
| 16: $1bn funding paragraph appears in the model input | 0/3 | 3/3 | The captured article reports it, and selection restores it. None of the six answers mentions the financing; whether it merits its own topic or link requires analyst judgment. |
| 28: an example model described as the proposed system's selected model | 3/3 | 3/3 | The release says small models “such as” Phi-4-mini-instruct. All six answers give the specific model a more definite role; source selection did not preserve this qualification. |
| 34: Kyber delay report and NVIDIA denial returned | 2/3 | 0/3 | Both source inputs contain the relevant paragraph. The unchanged input had omitted the matter in 16 earlier saved answers, yet returned it twice in this fresh control, illustrating variation. These observations do not prove why it was missed. |
| 34: Q2 results guidance returned | 3/3 | 1/3 | The guidance is in both inputs. This is a selected-case difference, not proof that the prepared text caused it. |
| 35: no pair returned | 3/3 | 3/3 | The trading-card article is a legitimate empty-output control. |

Other findings matter too. In article 6 one prepared answer explicitly attributes d-Matrix's performance figures to its CEO, while the article attributes those figures to the company and separately quotes the CEO on chip design; another prepared answer's speaker field creates a related attribution concern. Article 16's future deployment/customer announcement is described as uptake or initial use in some answers. Article 29 has a control answer that changes money flowing into AI-infrastructure stocks into infrastructure investment; another prepared answer's link blurs that distinction. Article 42 includes one prepared answer with a nonliteral quotation. Several company-reported figures, indirect links and dates require judgment; see the source-backed per-answer reviews rather than reading these observations as a single error score.

## Retrospective model accounts

Two follow-ups continued saved prepared-text conversations. Asked which statements it considered but did not return, the article 16 model said it could not know its earlier deliberation and identified a cooling comparison rather than the financing paragraph. Asked to justify its article 28 model-selection wording, the model quoted “such as” and acknowledged that the source does not establish a definitive selection. These are leading retrospective accounts, not a record of the original internal decision or evidence that future answers will be correct. [Questions and raw accounts](../poc/data/clean-step1-source-text-comparison-2026-11-07/account-predictions.md) are retained in the same experiment folder.

## What the comparison can and cannot establish

The captured page for article 3 is itself incomplete. Prepared text cannot restore content that was never captured. For article 8, removing generated-summary text changes where the model can cite, but it does not decide whether the vendor benchmark details merit keeping. Article 16 shows restored text alone does not guarantee the model will use it. Article 28 shows an exact quotation can accompany a summary that drops a qualification. Article 34 shows why the new same-day control is necessary even after repeated historical misses.

The comparison supports treating source selection as a useful **candidate** to investigate for contamination and source preservation; it does not validate the selector for unseen pages, prove that its labels are correct, establish a safe live source service, or justify promoting the prepared path. A clean writer and actual downstream readers must still preserve multiple passages, source/time context and link explanations. The next decision should consider all findings, relevant former attempts and useful counterexamples; the council is reviewing them.

## Inspection and records

- [Full replay of 60 answers](../poc/data/clean-step1-source-text-comparison-2026-11-07/review.html), with both actual input texts and pre-item theses.
- Condition-hidden reviews: [articles 3, 6, 8, 16](../poc/data/clean-step1-source-text-comparison-2026-11-07/review-03-06-08-16.md), [25, 28, 29](../poc/data/clean-step1-source-text-comparison-2026-11-07/review-25-28-29.md), and [34, 35, 42](../poc/data/clean-step1-source-text-comparison-2026-11-07/review-34-35-42.md). [Codex's frozen first-pass notes](../poc/data/clean-step1-source-text-comparison-2026-11-07/CODEX-BLIND-NOTES.md) and [separate adjudications](../poc/data/clean-step1-source-text-comparison-2026-11-07/adjudications.json) preserve the later independent article-28 recheck.
- [Pre-send design and controls](../poc/data/clean-step1-source-text-comparison-2026-11-07/design.md), [request and selection manifest](../poc/data/clean-step1-source-text-comparison-2026-11-07/manifest.json), [recorded judgments](../poc/data/clean-step1-source-text-comparison-2026-11-07/blind-judgments.json) and [condition mapping](../poc/data/clean-step1-source-text-comparison-2026-11-07/blind-key.json). Exact requests, raw responses and validator outcomes are saved per call.

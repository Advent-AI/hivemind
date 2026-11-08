# Step 1 isolated runner

This is a local implementation of the Step 1 contract in `../PRD.md`. It reads the prompt and response schema from that PRD, freezes an explicitly ordered source selection, and writes requests, raw responses, validation results and before/after thesis state to a new SQLite file. It does not write the production ledger or implement evidence deduplication, judgement or Hummingbird integration.

The offline entry point consumes recorded provider responses. The live entry point reuses the repository’s `model.call`, `model.Archive`, `model.openai_transport`, request builder and cost accounting; it adds a bounded, single-attempt adapter and keeps the clean test state and full trace isolated. Its limits guard starting requests, not the final provider bill or an absolute wall-clock deadline. Failed, refused or incomplete attempts may not appear in archive cost totals; inspect the full trace and its reserved amount, and treat the provider bill as authoritative. One selected three-article Luna run used the earlier single-passage schema; one repaired citation was incomplete. The revised multiple-passage schema was sent to Luna in the 49-article exploratory run. The results do not establish general extraction quality or production compatibility.

From the repository root:

```sh
PYTHONPATH=src python3 -m unittest discover -s clean-arch/step1 -p 'test_*.py' -v
python3 clean-arch/step1/run_offline.py --help
```

For an offline replay, pass `--source` (the source SQLite), `--output` (a new path), `--manifest`, `--initial`, `--settings` and `--responses` (JSON files). Selection currently requires `feed = 1`, excludes identified copies and corrections, and requires a tag matching the chosen entity. This is a bounded selection rule, not a claim that the full production dispatch was reproduced. Quote repair currently does not supply company aliases, so it can reject some name-for-pronoun repairs accepted by the production path. Manifest fields: `entity`, `from_day`, `until_day`, `item_ids` in intended order, and `item_limit`. Initial theses are a JSON array of `{id, entity, description, outcome, period}`. Settings contain `provider`, `model`, `reasoning_effort`, `max_output_tokens`. Responses are an ordered JSON array in the provider's `choices[0].message.content` format. The response's content is a JSON string conforming to the PRD schema. These are caller-supplied fixtures, not golden answers.

The SQLite `run` row holds the frozen source records and starting state. The `trace` rows contain each before state, request, full available response, interpreted result, after state and outcome. The file is not overwritten. Each original passage and its located source span, when available, are retained in order with a repair flag. In the exploratory path an unmatched passage is marked unverified and an unresolved thesis reference is preserved for review rather than stopping the stream; a new thesis without resolved supporting evidence does not enter the state. Later state is provisional. Other failures can stop a segment; a documented new segment may continue from the last completed state. Source-location checks do not prove that the summary is supported.

When the existing quote repair cannot preserve the complete quotation, the isolated runner also looks for a complete normalized match and retains the exact original source slice. Identical repeated slices are treated as the same text without claiming a source position; differing matches stay unverified. A lookup error is recorded with the evidence and passage number and displayed in the replay without stopping the exploratory stream. “Located in input” means the text sent to extraction; the prepared-source page check described below is separate. [Investigation and checks](../STEP1-QUOTE-INTEGRITY-CENSUS.md).

The bounded live entry point accepts the same arguments except `--responses`, plus `--limits`. See `../STEP1-DESIGN.md` for the limits, failure and trace contract. Each item uses the existing model archive in the isolated output database.

The optional prepared-source replay starts with **already recorded** source-role requests and responses; it does not run a source-selection model or change the production source. To reproduce the local example on a machine with its archived data, create a new output path:

```sh
python3 clean-arch/step1/materialize_source.py \
  --source poc/data/items-nvda-2026-07-01-10-27.sqlite \
  --selection poc/data/clean-step1-review-consensus/prepared-example/selection.json \
  --output poc/data/clean-step1-review-consensus/prepared-example/new-items.sqlite
```

The selection names each original input ID, archived source packet, source-role record, article number, arm and draw. The materializer verifies the archived identity and full page, then atomically publishes a small, separate SQLite file. It retains the original page, previous cleaned text, selected line IDs, role output and full source-role request/response. The roles are model proposals and may misclassify an author, source, date or page text. The original `authors` field is not populated by guessing. The prepared file can be passed as `--source` to the existing offline or bounded live runner. The caller explicitly supplies the ordered manifest, initial thesis library, settings and, for live calls, limits. A source quotation in this path is verified only when it is contiguous in both the text sent to Luna and the original captured page; an unverified quotation remains visible and does not stop the exploratory run. The replay shows the selected source alongside the earlier cleaned source, original page and role decisions.

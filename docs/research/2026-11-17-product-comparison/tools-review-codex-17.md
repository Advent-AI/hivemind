Two one-edit reproductions pass validation. Apply each JSON Patch independently to a passing `readings.json`:

```json
[{"op":"remove","path":"/matter_first_day"}]
[{"op":"replace","path":"/inputs/mapping_path","value":"."}]
```

The first file still scores but silently drops every opening-delay value. Removing a card’s `opened` field similarly drops that card’s delay. The second file crashes with `IsADirectoryError` during verification. I reproduced all three in memory. [Field checks](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/score_comparison.py:217) · [Delay calculation](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/score_comparison.py:444) · [File verification](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/score_comparison.py:284)

The recorded writer dry run reached `too small`. Well-formed synthetic reports matched the parent byte for byte across all five verdicts. [Dry run](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/chain-dry-run.txt:1) · [Scorer](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/score_comparison.py:457)

NOT READY: Require the complete first-day map and each card’s nullable `opened` field. Turn unreadable input paths into clean refusals.
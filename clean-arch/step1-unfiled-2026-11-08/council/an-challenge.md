Follow-up on your blocking item (read-only). I accepted it: every pipeline run counts as a use, old or new.

- Census redone with a reproducible script, `clean-arch/step1-unfiled-2026-11-08/select_fresh.py` (census + choose). 10,871 files under poc/data, clean-arch, docs, reports, research_notes, ../tn-hivemind/docs; whole-id token match (second-colon ids included); self-check dev 115/115, test 26/26 or it refuses.
- Not counted as uses: only the source databases and their copies, plus five corpus-wide page-cleaning inventories (HTML extractor output / character counts; no model read an article in them). Listed in `poc/data/clean-acceptance-2026-11-09/selection.json`. Everything else counts, including the old whole-window runs (processed every article to 2026-08-29) and the 2026-11-05 seven-day run (listed every article 2026-08-29..09-04).
- Choice from 2026-08-30 with the fixed order rule: 50 news articles, 2026-09-05..09-07 (18/22/10), all with stated times. All of 08-30..09-04 is used; inside 09-05..09-07 only 8 used items were skipped (source-cleaning checks of 11-07), each listed with its files. Weekend + US Labor Day: no NVIDIA blog/newsroom post; repeats include the Hugging Face acquisition across several outlets. Manifest sha256 81f3f579…; runner accepts it. Protocol §2 rewritten (`ACCEPTANCE-PROTOCOL.md`), with the two withdrawn July drafts recorded; no reader has seen any set.
- Later links: as you accepted, no rule; the boundary is judged against the source in acceptance.

Sequence I propose: launch dev x3 now (independent of the set); build the source packet and run the two pre-run readers, settle with a third, freeze their lists with sha256; only then launch the fresh Step 1 run, then Steps 2–3.

Under 200 words: anything still blocking? End FREEZE AND LAUNCH or the blocking item.

NOT READY

The previous review’s serious finding is answered: version 29 says to register each new question and its mapping before writing links, and specifies a test through to the judge’s request. A refused question gets neither entry. [Design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:568); [adapter](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/adapter.py:193).

I found **no new serious defect in the readers I checked**. I cannot give READY for this angle because I did not finish checking every outside reader.

The main replay compatibility checks I did complete:

- The proposed `v<N>` IDs fit the judge’s theme-ID reader. The company/theme values drive the judge’s selection and queueing; `kind`, `year`, question and focus are printed in the request. [Judge](/Users/lchingen/hivemind/src/hivemind/views/judging.py:76)
- For events, omitted `lo` and `hi` become null in storage. The judge reads rung position, label and condition; it does not require numeric bounds. [Store](/Users/lchingen/hivemind/src/hivemind/views/store.py:81); [judge](/Users/lchingen/hivemind/src/hivemind/views/judging.py:121)
- The created open switch is read by the judge’s eligibility check. The proposed event year is accepted as text and printed by the judge. [Store](/Users/lchingen/hivemind/src/hivemind/views/store.py:192); [judge](/Users/lchingen/hivemind/src/hivemind/views/judging.py:300)
- The previously requested corrections about `created_at`, `created_from_input`, `views_for_prompt`, `due_day` and the figure-reference qualification are present. [Design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:408)

Wording-level corrections:

- The outside-reader column omits product-page readers for several values: for example, the bundle reads rung bounds and switches, and the service reads the question, year, creation sequence and switch history. These readers are outside this replay, but the table should name them. [Bundle](/Users/lchingen/hivemind/src/hivemind/bundle.py:45); [service](/Users/lchingen/hivemind/src/hivemind/service.py:150)
- The Stage A form’s packet description lists `favourable_end` but omits `favourable_why`, although its F mark requires the reason. The design says the packet builder supplies both, and the stored practice packet included the reason; make the form’s list agree. [Form](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md:18); [design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:527); [practice packet](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/dryrun11/packet.json:273)

Fields searched: `view_id`, `object_id`, `object_kind`, `kind`, `looks_at`, `question`, `due_day`, `year`, `rungs`, `seq`, `input_id`, `created_seq`, `created_from_input`, `created_at`, `position`, `label`, `condition`, `lo`, `hi`, `open`, `reason`, `by_whom`, `after_seq`, `views_fts`, `thesis_id`, `status`, `reference_status`, `checked_answer`, `outcome_record`, `config_checksum`, `article_seq`, `article_day`, `not_judged`, `favourable_end`, `favourable_why`, `reference`, and `due_day_basis`.

I walked the field-by-field writes and principal replay readers; **not reached in full:** every outside-reader search hit for the rows at [design lines 513–524](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:513), including the complete page and research-context reader paths.
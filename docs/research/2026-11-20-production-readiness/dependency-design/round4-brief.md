# Council R, round 4: review of the build design before any code (AGENTS §2)

Alex chose A (D694 in `docs/DECISIONS-log.md`: links leave filing alone; new matching and judging versions for linking; the July test
after the council passes the $0 proof). The build design is `DESIGN.md` in this folder. Review it against the code it names
(`src/hivemind/views/jev_matching.py`, `matching.py` `check`, `writing.py` `_write`, `judging.py`, `store.py`, `extraction.py`
`shown_views`/`narrowest_links`, `round.py`, `config.py`), AGENTS §2–§4 and §6, PRD 06, and our rounds 1–3.

Done since round 3, at $0: `rebuild_control.py` → `rebuild-control.log`: old-2 replayed from 07-01 through 07-09 under poc-v118 with a
transport that refuses every send: 160 items, 55 judgements, every request answered from the archive; views, keys, evidence, links,
judgements (with request sha) and dependencies equal to old-2's finished store up to seq 147. That is the July test's starting state.

Please answer:
1. Is anything in the four tables wrong or missing for a cell this build can reach? Name the cell and the code line.
2. The two Jev question texts (`READS`, `SIGN`): read them as the matcher reads them, with `candidate_state` and `thesis_text`. Do they
   decide the old-2 07-10 pair the agreed way, serve any company (AGENTS §6), and avoid deciding importance in code? Any sentence
   with no source?
3. The label mapping (section 2): correct on the worked case and its mirrors? Is "the end labelled Strongly bullish is R's favourable
   end" sound for every asset ladder the writer stores (`extraction.check_ladder`, `vocabulary.ASSET_LABELS`)?
4. The circle rule (section 4): a cycling link is refused and recorded and the article proceeds, because Jev cannot correct and a
   failure would recur on every replay. Accept as a recorded departure from PRD 06's wording, or require something else?
5. The block (section 3) and `current_state`'s new fields: any reader of `current_state` that would change under judging-v7?
6. Versioning (section 0): `judging-v8.txt` as a byte copy of v7 and the engine name `jev-links`. Acceptable under D354/D359, and does
   the frozen-piece test need new pins as proposed?
7. Anything the July test's harness must handle that the design omits (only both questions fresh; other questions replayed by exact
   identity; the new Jev questions are the only other new requests).

Reply with findings ranked by severity, each with its file and line, and end with READY TO BUILD or NOT READY with the exact changes.

# Council mx, round 16: Alex chose the reading on the fresh week (D503); its design before any reader runs

Alex answered D502's question with "看样表，并在最初那一周再验一次" (D503 in `docs/DECISIONS-log.md`). Your bounds of round 15 are the
design's rules: a separate question from D489's; D489's 2 against 4 unchanged; the articles, the required outcomes and the line fixed
before the blind read; what the week's articles support checked first.

Read, under `docs/research/2026-11-14-use-acceptance/record-3/`: `TABLE-WEEK-DESIGN.md`, the built table `financial-table-week.md` (trace
`table-rows-week.json`; `build_table.py --trace` on the new system's stored week draw: 186 rows in 146 lines, 18 joined lines; the
D501 table is byte-identical after the builder gained this input), `week-matters.md` (the question, without figures),
`week-articles.json` (the seven articles D489's families tied to M01, M02, M03), the briefs `brief-week-reference.md` and
`brief-week-table-reader.md`. D489's matters are in `../week/matters-A2.json` and its result in `../week/WEEK-RESULT.md`.

Name only what would make the result wrong or unreadable:
1. **The key:** built from two reference readers on the seven articles as "every (a) company outlook or (b) market estimate both list
   with the same value, period and source"; group (c) context only; an empty key leaves a matter not exercised. Is the intersection
   rule fair, and is the three-group question the right reading of "the matter's main outcome"? Should the key come from the seven
   tied articles or from more of the week?
2. **The table** is built from all 235 articles' stored answers while the key comes from seven: figures from other articles can be
   checked against their lines only. Does that let anything pass that should not, or fail a matter unfairly?
3. **The line** ("findable": every key item found by at least one table reader of each family, none misstated by both comparers; a
   key figure not in the table at all makes the matter not findable). Too easy, too hard, or measuring the readers?
4. **The joins on this week** (18 lines): the D501 check read ten lines of another week. Must these 18 be read by both families
   before the table readers, or is the per-key-item check against the articles enough for this question?
5. Anything in the wording that would let the result be read as "covered" in D489's sense.

Then say whether the readers may run. End with: "Council position: <...>".

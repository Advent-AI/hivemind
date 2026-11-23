# "Forecast unavailable" for number questions: the design, ready for when release work opens

**Status: design only. Nothing is built.** Alex decided the behaviour twice:
- D726, "同意": until the number answers pass, a first release shows number questions with their sources and "Forecast unavailable",
  with the band, the forecast text and its history withheld together; "it is built with the release work, which is not started";
- D756, "结束这条线，预测暂缺上线".

Opening release work is Alex's call (council 72). This page makes the build a known, reviewed slice for that moment.

**Revision 4 (council 72c) of revision 3: one structural rule instead of a list of leaks.** Rounds 72 and 72b each found new paths by which a withheld forecast
could reach a reader:
- the idea card;
- the closing text;
- an idea summary that re-reads the ladder;
- a release page that reloads from the live POC service;
- a translated export;
- a Yes/No explanation that quotes a number question's band.

A rule that withholds fields reader by reader will keep missing one (AGENTS §1: "when one mechanism draws findings round after round,
stop answering findings: propose one structural rule"). Revision 3 replaces that rule with an allow-list at one boundary.

## 1. The gap, measured at $0 (2026-11-23)

The stored poc-v118 store `poc/data/comparison-2026-11-17/run/old-1/prod/views.sqlite`, read-only, gives:
- **The number question v8 (FY2027 Data Center revenue)** exposes its band, label, condition, reasons, 75 judgements and 69 change rows.
- **Its idea input** reads "Bullish … $350 billion to under $400 billion".
- **Yes/No explanations quote number forecasts:**
  - `old-3` `v36`, judgement 799: "around $1 trillion" for 2027 spending;
  - `old-1` `v10`, judgement 865: the selected bands of both spending questions.

  The judge is shown related questions' selected bands (`views/judging.py:208`), and its prose can repeat them.

## 2. The structural rule: one release export, allow-listed

- **One exporter writes the release data:** `release_export`, a single function beside `service.py`. It emits only the fields on an
  explicit allow-list. A field not on the list cannot appear, so a new or overlooked path fails closed.
- **The release builder calls `release_export` directly** and accepts no external input; a marker or version names a format, not
  who wrote the text (council 72c). The finished package is checked as well as the page: it holds only the export's output, with no
  market data, composite trials or translated file beside it.
- **The release reads only that export.** Its page, its static build and its API, if any, read nothing else:
  - no live POC service;
  - no `/library` reload (`poc/ui/src/bootstrap.js` must not fetch in a release build);
  - no prepared or translated JSON (`scripts/mock_translate.py`'s `data.en.json`);
  - no `--composite-trials` input.

  The static builder refuses any input not produced by `release_export`, which carries a marker and the allow-list version.
- **For a number question, the allow-list is:**
  - the question and its id;
  - the evidence in force: one-line, quote, speaker, original day, tier and sources, amounts as quoted. Council 78b (D761): "amounts
    as quoted" applies to the text labelled Source quote; the labelled Hivemind summary may state an amount that follows directly from
    it and keeps its qualifiers;
  - the marker "Forecast unavailable".

  Nothing else is listed:
  - no ladder;
  - no band, label or condition;
  - no reasons or why_changed;
  - no history, counts or assessment dates;
  - no closing band ("closed" only);
  - no theme pushes, no composite, no idea derived from its forecast.
- **Ideas.** The release's idea composition (`idea.py`, `idea_composite.py`) runs on export data only. A number question enters it
  as question and evidence with the marker. Its ladder is not read from storage in either the answer-format build or the summary
  input (`idea_composite.py:255`, `:281`; `poc-v118-idea.json:94`). The test inspects the composed request itself, not only the
  delivered card.
- **The POC is unchanged.** Its API, MCP and page keep today's behaviour. Whether colleagues' POC page also changes is a separate
  later choice for Alex.

## 3. Identity: what a number question is (verified on four stores by council 72b)

A view is a number question unless one of the following excludes it:
1. **An event.** The view key's measure is in `identity.EVENT_MEASURES` (`event`, `policy_event`). That covers 85 of 85 event
   questions in the three comparison stores.
2. **A Yes/No question.** The ladder has exactly two labels which, canonicalised with the existing vocabulary
   (`vocabulary.canonical`), are Yes and No in either order. The sealed ledger's 30 such questions use `是` and `否`. The Xbox `v37`
   (`growth_rate`, bounds around zero) is Yes/No.

Every other view is a number question. Its forecast is withheld whether its bands come from `lo`/`hi`, parse from the conditions
(the sealed `v3`), or cannot be resolved. An unresolved record is withheld and listed in the release check, with a key or without
(council 72b: an `old-1/v8` copy without bounds does not parse, and its key still exists).

Counts (council 72b), number / event or Yes/No:
- `old-1` 19 / 28, `old-2` 17 / 26, `old-3` 18 / 31;
- the sealed ledger: 43 parse as money, 21 are withheld as unresolved, 30 are Yes/No.

No wrong show-or-withhold result was found.

**Events are binary too.** All 85 comparison-store events are also two-answer questions, including both known prose leaks, and a
binary event such as "Restriction adopted" / "No restriction adopted" exists in the served ledger (council 72c). §4's rule applies to
every question that is not a number question, events and Yes/No alike, and each keeps its answer label.

## 4. Questions that are not number questions: an open choice for Alex (not decided here)

D726 covers number questions. A Yes/No question's band is not a number forecast, but its stored explanation can quote one (§1). The
allow-list must say which Yes/No fields the release shows:
- **(a)** the question, its evidence and its answer (Yes/No and label), with no explanation text. Safe, and it removes the reasoning
  readers would see.
- **(b)** as (a), plus the explanation only for judgements whose request showed the judge no number question's state. Code can
  decide this from the stored request (`views/judging.py`, which builds the related questions shown).
- **Measured (council 72c),** matching each judgement to its archived request:
  - (b) would keep explanations on 31 of 769, 44 of 776 and 43 of 958 judgements in the three comparison runs;
  - for a reader at the latest answer, it would keep them on 21 of 85 questions;
  - it would keep 73 of 73 in the sealed ledger.
- **The limit of (b).** It cannot promise the prose quotes no number forecast. A request also carries the question's own previous
  reasoning, and can carry another question's, either of which may repeat a forecast seen earlier. Both known leaks are in
  `why_changed`.
- **Recommendation: (a) for the first release** (council 72c; Claude agrees, withdrawing its lean for (b)). It is the only option
  that guarantees no number forecast reaches a reader through prose. (b) remains a measured later step.

## 5. Tests and the $0 release check (each names its row above)

- **Fixtures (real store on a temporary path):**
  - a number question with `lo`/`hi`;
  - one with bounds only in its conditions;
  - an unresolved one with a key;
  - a Yes/No question with numeric bounds;
  - an event question;
  - a Yes/No judgement whose prose quotes a number band;
  - a real closing switch;
  - an idea.
- **What the tests assert.** `release_export`'s output holds only allow-listed keys (a schema check that fails on any extra key). For
  number questions it holds no band, ladder, reasons, history, date or closing band; Yes/No follows §4's choice. The static build
  refuses foreign input, and a release page makes no network fetch.
- **Mutants:**
  - an extra field;
  - a fetch left on;
  - a ladder read in idea composition;
  - the identity mis-sorting each fixture.

  Each must fail.
- **End-to-end acceptance (council 72c):**
  - an idea whose only question is `old-1/v8`: the card keeps its sources and "Forecast unavailable", with no scored driver and no
    substitute band (the current composite expects an endpoint for every scoring candidate, `idea_composite.py:214`, `:231`);
  - in the same release package, the two known event answers keep their labels and carry no spending forecast under the chosen
    prose rule.
- **The $0 release check.**
  - On `old-1/v8`, confirm the marker and the same sources in the page and in the export data.
  - Exercise closure on a temporary copy with a real closing switch, after first confirming that the unrestricted response exposes the
    final band there.
  - Check ideas with a recorded or test transport, inspecting the composed request.
  - Use `old-3/v36` and `old-1/v10` as the Yes/No prose cases.
  - Use one unchanged event question as the control.

## 6. Not in scope

- The judging, opening and extraction pieces (frozen).
- The closed v13s line.
- Other open defects.
- No prompt or pipeline change.
- The POC's own behaviour.

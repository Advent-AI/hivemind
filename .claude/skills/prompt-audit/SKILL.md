---
name: prompt-audit
description: After every measurement of an extraction configuration, and before any prompt change, map each failure class in the stored draws to the sentence of the request that produced it, check that sentence against the frozen standard and the prompt principles, and write the audit table. Alex, 2026-11-02 - "你应该看着prompt，然后对比失败的trace，然后仔细的根据尺子做对比，并且我们prompt的principle也要带入，是尝试教他general hedge fund analyst skill，不是要hardcode或是benchmark farming；你把这个写成一个skill以后固定跑".
---

# Prompt audit: failures → the request's sentences → the standard → the principle

Run this after every measured configuration (three draws scored on the frozen ruler) and before any edit to a prompt file, a schema
description or a takes line. A measurement without this audit is a score without a diagnosis (AGENTS §7.2, §6). The audit is read,
not scripted: the scripts below only produce the lists to read.

## 0. Inputs

- The arm's run folders (`docs/research/2026-11-01-e2e-loop/arms/<arm>/d1..3`) and the baseline's.
- The frozen ruler (AGENTS §7.1): the extraction standard `docs/prd/05-extraction-standard.html` (version 3, D243, with D250's
  boundaries), golden-v5, the questions standard, the judgement gold. Never edited; every disagreement is a gap in the system.
- The prompt principles (AGENTS §6 and §8): the prompt carries the standard and no new rule; it teaches a general hedge-fund
  analyst, so every sentence and example reads the same for a bank, a drug maker, a retailer or a chip maker, names no covered
  company, product or number, and takes no example from a test article; a classification is a closed set with examples; never grow a
  prompt to fix quality without cutting as much elsewhere; a field's definition sits in the schema beside the field; code owns
  identity, never importance.

## 1. Dump the request as the model reads it

One stored request of the configuration (any article), printed whole: the system text (the role), every user block before the item
(category block, subjects, research reference, open questions with their takes lines, research groups), the closing sentence, the
end-of-request check, and every schema field description (evidence and candidates). Read it top to bottom once. List every
instruction that decides keep, reject, link, open, or a field value, with its location (role paragraph, check row, schema field,
takes line, category block). This list is the thing the failures are mapped onto.

```sh
python3 - <<'PY'
import sqlite3, json
a = sqlite3.connect('file:<run folder>/archive.sqlite?mode=ro', uri=True)
req = json.loads(a.execute("select request_json from model_calls where purpose='extract' and request_json like '%<title fragment>%' order by call_id desc limit 1").fetchone()[0])
print(req['messages'][0]['content']); print(req['messages'][1]['content'].split('[Item]')[0]); print(req['messages'][1]['content'].rsplit('\n\n', 2)[-2:])
print(json.dumps({k: v.get('description') for k, v in req['response_format']['json_schema']['schema']['properties']['evidence']['items']['properties'].items() if v.get('description')}, ensure_ascii=False, indent=1))
PY
```

## 2. Produce the failure lists (all $0, on the stored draws)

| List | Script | What it gives |
|---|---|---|
| Matter states across draws | `harness/matter_states.py arm=d1,d2,d3 base=d1,d2,d3` | every gold core/supporting matter: extracted or reaching in 3/2/1/0 draws; the systematic misses (0 of 3) and the coin flips (1 of 3) |
| Written noise by the standard's row | the `rows_all` count in `design-v72.md` §10 (the gold's `not_kept[].row`) | which row of the standard the written noise falls under, with examples |
| No-home drops | `harness/dropped_census.py d1 d2 d3` | gold matters written but dropped, with the questions open at the time |
| Where links go | `harness/links_by_question.py d1 d2 d3 --sample 20` | the pile per question, the revenue-sink share, statements under several questions, noise under revenue |
| Quote refusals | the `dropped` reasons of the handovers (`quote not in item`), each diffed against its closest source window | paraphrase against a word or two off |
| Question recall | `harness/question_recall.py d1 d2 d3` | must_open / may_open covered by seeds and by article-opened questions |
| Fields | 15 random stored statements with speaker, original_who, original_day, tier | read against the quote and the item's day and publisher |

For every list, read the items, not the counts: the raw answer beside the article for every systematic miss (a miss the scorer reports
may be the matter written in other words: check before counting it), a sample of twenty for every pile.

## 3. Map each failure class to the request

For each class with more than a handful of cases, fill one row:

| Failure class (count, share) | The sentence(s) of the request that produced it, quoted | The standard's line on the same case (section, decision) | Verdict | The model's own account (when the sentence is not obvious) |
|---|---|---|---|---|

Verdicts, one of: **contradiction** (two sentences of the request pull opposite ways, or a request sentence removes what the standard
keeps, D240), **missing** (no sentence decides the case; the model guesses, a coin flip per send), **abstract** (a clause without an
example, read differently each send), **misread** (the sentence is right, the model does not apply it; needs the model's own account
before any change), **not the prompt** (code, scorer or sampler).

The model's own account: continue the stored conversation with one question about one case (`harness/probe_v72_link.py`,
`probe_v72_missing.py`), a cent a case, for every "misread" and for any class whose sentence is not obvious from reading.

## 4. Check every proposed fix against the principles before writing it

- It is written from the standard's line, not from the failing article: the example comes from another domain, names no covered
  company, product or number, and reads the same for every industry. A fix that only recovers the bench's misses is benchmark
  farming and is not written.
- It removes a contradiction, supplies a missing definition at its owner (schema field, takes line, check row, category block), or
  replaces an abstract clause with a closed set and examples. It never adds a rule the standard does not hold.
- It cuts at least as much as it adds, or the growth has a written reason; report characters before and after.
- One class per change; the change is proved on the stored requests of that class, three sends as stored against three changed,
  with the noise guards of the same articles; the whole bench accepts it (three draws) only when Alex asks for a run.

## 5. Output

Write the table and the verdicts into the arm's design document (a numbered section), one row per class, in the order of the loss;
the report to Alex states each class in a reader's words (what the system does wrong, which sentence makes it do that, what the
standard says), never in the loop's own words (AGENTS, "Authority and scope": explain as to a sixteen-year-old).

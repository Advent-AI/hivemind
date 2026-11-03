"""Structural check of the golden-v3 drafts, and the changes against reference v2 that need reading.

    python3 check.py [batch numbers]      # default: every draft-batch-*.json present

Checks (each reports how many it judged): every article of the batch present; every item and not_kept span an exact substring
of the article text; required fields present with allowed values; depends_on only 1-9. Then lists, per article, the items that
are new against reference v2, reference v2 statements that no item covers, and weight changes, which are read by hand.
"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / '2026-10-29-analyst-standard'))
import score_week as sw  # the quote matcher used by the earlier rulers

KINDS = {1, 2, 3, 4, None}
WEIGHTS = {'core', 'supporting', 'optional'}
TIERS = {'fact', 'party_statement', 'third_party_view', 'rumour'}
TYPES = {'A', 'B', 'C', 'D', 'E'}
batches = [int(a) for a in sys.argv[1:]] or sorted(int(p.stem.split('-')[-1]) for p in HERE.glob('draft-batch-*.json'))
totals = {'articles': 0, 'items': 0, 'spans checked': 0, 'span not in text': 0, 'field problems': 0, 'not_kept': 0,
          'must_open': 0, 'new vs v2': 0, 'v2 uncovered': 0, 'weight changed': 0}
report = []
for b in batches:
    src = {a['input_id']: a for a in json.loads((HERE / 'batches' / f'batch-{b}.json').read_text())}
    draft = json.loads((HERE / f'draft-batch-{b}.json').read_text())
    got = {a['input_id'] for a in draft}
    missing = [i for i in src if i not in got]
    if missing:
        report.append(f'batch {b}: articles missing {missing}')
    for a in draft:
        art = src.get(a['input_id'])
        if art is None:
            report.append(f'batch {b}: unknown article {a["input_id"]}'); continue
        text = art['text']; totals['articles'] += 1
        for it in a.get('items', []):
            totals['items'] += 1; totals['spans checked'] += 1
            if it.get('span', '') not in text:
                totals['span not in text'] += 1; report.append(f'SPAN  {a["input_id"]} | {it.get("span", "")[:90]}')
            probs = [f for f, ok in (('kind', it.get('kind') in KINDS), ('weight_current', it.get('weight_current') in WEIGHTS | {'excluded'}),
                                     ('weight_proposed', it.get('weight_proposed') in WEIGHTS), ('tier', it.get('tier') in TIERS or it.get('tier') is None),
                                     ('depends_on', all(d in range(1, 10) for d in it.get('depends_on', []))), ('rule', bool(it.get('rule')))) if not ok]
            if probs:
                totals['field problems'] += 1; report.append(f'FIELD {a["input_id"]} | {probs} | {it.get("span", "")[:60]}')
        for nk in a.get('not_kept', []):
            totals['not_kept'] += 1; totals['spans checked'] += 1
            if nk.get('span', '') not in text:
                totals['span not in text'] += 1; report.append(f'SPAN  (not_kept) {a["input_id"]} | {nk.get("span", "")[:90]}')
        for q in a.get('questions', {}).get('must_open', []):
            totals['must_open'] += 1
            if q.get('type') not in TYPES:
                totals['field problems'] += 1; report.append(f'FIELD question type {a["input_id"]} | {q}')
        ref = art['reference_v2']
        items = a.get('items', [])
        for st in ref.get('statements', []):
            hit = [it for it in items if sw.matches(it.get('span', ''), st)]
            if not hit:
                totals['v2 uncovered'] += 1; report.append(f'V2-UNCOVERED {a["input_id"]} | {st["weight"]} | {st["note"][:110]}')
            elif all(h.get('weight_current') != st['weight'] for h in hit):
                totals['weight changed'] += 1; report.append(f'WEIGHT {a["input_id"]} | v2 {st["weight"]} -> {[h.get("weight_current") for h in hit]} | {st["note"][:90]}')
        for it in items:
            if not any(sw.matches(it.get('span', ''), st) for st in ref.get('statements', [])):
                totals['new vs v2'] += 1; report.append(f'NEW   {a["input_id"]} | {it.get("weight_current")}/{it.get("weight_proposed")} dep {it.get("depends_on")} | {it.get("span", "")[:100]}')
print(totals)
print('\n'.join(report))

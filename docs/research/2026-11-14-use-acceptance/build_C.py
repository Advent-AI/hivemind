"""D485 trial, reading C ($0): for the facts reader B relied on (the judgement gold's cited items) whose article is one of A's 40, and for each
system's view on the same matter, the fact's class by code: not extracted (no kept statement of that article whose quote shares at least half
of the item passage's words); extracted, not linked; linked to another view only; or linked to the matter's view; and, per judgement of that
view made after the fact was kept, whether the fact was in that judgement's request as sent ("- e<N>" lines of the archived request).
Code classes; Claude reads every row against the article before anything is counted.

  python3 build_C.py <views per system as JSON: {"c1": {"M01": ["v1"]}, "p1": {...}}>
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
GOLD = ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold'
FULL = ROOT / 'poc/data/clean-e2e-full-2026-11-13'
STORES = {'c1': (FULL / 'c1/judge/draw-c1/views.sqlite', FULL / 'c1/judge/draw-c1/archive.sqlite'),
          'p1': (FULL / 'p1/prod/views.sqlite', FULL / 'p1/prod/archive.sqlite')}
MATTER_OF = {'q09': 'M01', 'q23': 'M02', 'q04': 'M03', 'q13': 'M04', 'q18': 'M05', 'q08': 'M06', 'q07': 'M07', 'q19': 'M08', 'q02': 'M10',
             'q05': 'M12'}
WORD = re.compile(r'[a-z0-9]+(?:\.[0-9]+)?')


def words(text):
    return set(WORD.findall((text or '').lower()))


def facts(sample_ids):
    items = {i['id']: i for i in json.loads((GOLD / 'packet-v1.json').read_text())['items']}
    out = []
    for entry in json.loads((GOLD / 'gold-v1.json').read_text())['entries']:
        matter = MATTER_OF.get(entry['question_id'])
        if not matter:
            continue
        cited = set((entry.get('decisive_items') or []) + ((entry.get('reference') or {}).get('items') or [])
                    + ((entry.get('implied_outcome') or {}).get('items') or []) + ((entry.get('against') or {}).get('items') or []))
        for item_id in sorted(cited):
            item = items[item_id]
            if item['input_id'] in sample_ids:
                out.append({'matter': matter, 'question': entry['question_id'], 'item': item_id, 'input_id': item['input_id'],
                            'day': item['day'], 'passage': item['passage']})
    return out


def classify(system, fact, matter_views):
    store, archive = (sqlite3.connect(f'file:{p}?mode=ro', uri=True) for p in STORES[system])
    passage = words(fact['passage'])
    kept = []
    for evidence_id, quote, created_seq in store.execute(
            'select e.evidence_id, e.quote, e.created_seq from evidence e join evidence_sources s using(evidence_id) where s.input_id=?',
            (fact['input_id'],)):
        shared = len(passage & words(quote)) / max(1, min(len(passage), len(words(quote))))
        if shared >= 0.5:
            kept.append((evidence_id, created_seq, round(shared, 2)))
    if not kept:
        return {'class': 'not extracted'}
    evidence_ids = [k[0] for k in kept]
    links = {e: [v for (v,) in store.execute('select view_id from evidence_links where evidence_id=?', (e,))] for e in evidence_ids}
    linked_to_matter = any(v in matter_views for vs in links.values() for v in vs)
    linked_anywhere = any(links.values())
    judgements = []
    for view in matter_views:
        for seq, call_id, rung in store.execute('select seq, call_id, rung from judgements where view_id=? order by seq', (view,)):
            if seq < min(k[1] for k in kept):
                continue
            row = archive.execute('select request_json from model_calls where call_id=?', (call_id,)).fetchone()
            shown = set(re.findall(r'^- (e\d+) ', json.loads(row[0])['messages'][-1]['content'], re.M)) if row else set()
            judgements.append({'view': view, 'seq': seq, 'rung': rung, 'in_request': bool(shown & set(evidence_ids))})
    if linked_to_matter:
        klass = 'linked to the matter\'s view'
    elif linked_anywhere:
        klass = 'linked to another view only'
    else:
        klass = 'extracted, not linked'
    return {'class': klass, 'kept': kept, 'links': links, 'judgements': judgements}


def main():
    views = json.loads(sys.argv[1])
    sample_ids = {s['input_id'] for s in json.loads((HERE / 'sample.json').read_text())}
    rows = []
    for fact in facts(sample_ids):
        for system in ('c1', 'p1'):
            matter_views = views[system].get(fact['matter'], [])
            result = classify(system, fact, matter_views) if True else None
            result.update({'system': system, 'matter_views': matter_views, **fact})
            if not matter_views:
                result['note'] = 'the system opened no question on this matter'
            rows.append(result)
    (HERE / 'facts-C.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    from collections import Counter
    print(f"{len(rows) // 2} facts in the 40 articles, by system and class:")
    for system in ('c1', 'p1'):
        print(' ', system, dict(Counter(r['class'] for r in rows if r['system'] == system)))
    for system in ('c1', 'p1'):
        missing = sum(1 for r in rows if r['system'] == system for j in r.get('judgements', []) if not j['in_request'])
        print(f"  {system}: judgements after the fact was kept that did not carry it: {missing}")


if __name__ == '__main__':
    main()

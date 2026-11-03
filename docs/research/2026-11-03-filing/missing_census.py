"""Gold-cited statements (judgement gold, reader B's cited packet items per question) that are not in a draw's ledger: never written by
the extraction, or written and dropped (with the drop reason from the handover). $0, read-only; same matching as gold_home_census.py.

    python3 missing_census.py
"""
import sqlite3, json, re, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
G = ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold'
gold_q = json.loads((G / 'gold-v1.json').read_text())['entries']; packet = {i['id']: i for i in json.loads((G / 'packet-v1.json').read_text())['items']}
words = lambda s: set(re.findall(r'[a-z0-9$.%]+', (s or '').lower()))
ov = lambda a, b: len(words(a) & words(b)) / max(1, min(len(words(a)), len(words(b))))
RUNS = {'v94': ROOT.parent / 'hivemind-extraction-quality-2026-10-28/docs/research/2026-11-01-e2e-loop/arms/r7-combined-v94', 'v108': ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03'}
for name, base in RUNS.items():
    tot = collections.Counter(); examples = []
    for d in (1, 2, 3):
        c = sqlite3.connect(f'file:{base}/d{d}/views.sqlite?mode=ro', uri=True); a = sqlite3.connect(f'file:{base}/d{d}/archive.sqlite?mode=ro', uri=True)
        ledger = collections.defaultdict(list)
        for inp, q in c.execute('select created_from_input, quote from evidence'): ledger[inp].append(q)
        dropped = collections.defaultdict(dict)
        for inp, hj in c.execute('select input_id, handover_json from handovers'):
            for eid, why in json.loads(hj).get('dropped', []): dropped[inp][eid] = why
        answers = {}
        def answer(inp):
            if inp not in answers:
                r = a.execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {inp},%',)).fetchone()
                answers[inp] = json.loads(r[0]).get('evidence', []) if r and r[0] else []
            return answers[inp]
        for e in gold_q:
            if not e.get('seed_view_id') or e.get('no_view'): continue
            for it in dict.fromkeys((e.get('reference') or {}).get('items', []) + (e.get('implied_outcome') or {}).get('items', [])):
                item = packet.get(it)
                if not item or any(ov(q, item['passage']) >= 0.6 for q in ledger.get(item['input_id'], [])): continue
                written = [x for x in answer(item['input_id']) if ov(x.get('quote', ''), item['passage']) >= 0.6]
                if not written: tot['never written'] += 1; continue
                why = next((dropped[item['input_id']].get(x['id']) for x in written if x['id'] in dropped[item['input_id']]), 'written, not in ledger, no drop reason')
                tot['written, dropped: ' + why[:40]] += 1
                if 'home' in why: examples.append((d, e['question_id'], item['passage'][:120]))
    print(name, dict(tot.most_common()))
    for d, q, p in examples: print(f'    d{d} no home, the gold uses it for {q} | {p}')

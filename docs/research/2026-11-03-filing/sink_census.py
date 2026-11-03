"""What sits under the sink questions (total revenue v1, data-center revenue v2) of finished end-to-end draws, read against both frozen
golds ($0, read-only). For each linked statement from a gold article: its extraction-gold class (golden-v5: core, supporting, optional,
not_kept, unlisted), and for core/supporting statements whether the judgement gold (reader B) cites the matching packet item for the
sink's own question, for another question, or for none.

    python3 sink_census.py
"""
import collections, json, re, sqlite3, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'docs/research/2026-10-31-reference-context'), str(ROOT / 'src')]
import score_ref as sr  # noqa: E402
G = ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold'
gold_q = json.loads((G / 'gold-v1.json').read_text())['entries']
packet = json.loads((G / 'packet-v1.json').read_text())['items']
seed_of = {e['question_id']: e.get('seed_view_id') for e in gold_q}
cites = collections.defaultdict(set)          # packet item id -> gold questions citing it
for e in gold_q:
    for it in (e.get('reference') or {}).get('items', []) + (e.get('implied_outcome') or {}).get('items', []):
        cites[it].add(e['question_id'])
by_input = collections.defaultdict(list)
for it in packet: by_input[it['input_id']].append(it)
articles = {a['input_id']: a for a in sr.articles}
words = lambda s: set(re.findall(r'[a-z0-9$.%]+', (s or '').lower()))
def overlap(a, b):
    A, B = words(a), words(b); return len(A & B) / max(1, min(len(A), len(B)))
def gold_class(a, e):
    for i in a['items']:
        if i['weight'] in ('core', 'supporting') and sr.sg.same_matter(i, e): return i['weight']
    if any(sr.sg.same_matter(i, e) for i in a['items'] if i['weight'] == 'optional') or any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'optional'):
        return 'optional'
    if any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'not_kept'): return 'not_kept'
    return 'unlisted'
RUNS = {'v94': ROOT.parent / 'hivemind-extraction-quality-2026-10-28/docs/research/2026-11-01-e2e-loop/arms/r7-combined-v94',
        'v108': ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03'}
for sink, qid in (('v1', 'q01'), ('v2', 'q02')):
    print(f'== sink {sink} (gold {qid}): per draw')
    for name, base in RUNS.items():
        for d in (1, 2, 3):
            c = sqlite3.connect(f'file:{base}/d{d}/views.sqlite?mode=ro', uri=True)
            rows = c.execute('select e.evidence_id, e.created_from_input, e.quote, e.one_line from evidence e join evidence_links l on l.evidence_id=e.evidence_id where l.view_id=?', (sink,)).fetchall()
            cnt = collections.Counter(); use = collections.Counter(); other_q = collections.Counter()
            for eid, inp, quote, ol in rows:
                a = articles.get(inp)
                if not a: cnt['not a gold article'] += 1; continue
                k = gold_class(a, {'quote': quote, 'one_line': ol}); cnt[k] += 1
                if k in ('core', 'supporting'):
                    its = [it for it in by_input.get(inp, []) if overlap(quote, it['passage']) >= 0.6]
                    qs = set().union(*[cites[it['id']] for it in its]) if its else set()
                    if qid in qs: use['cited for this question'] += 1
                    elif qs: use['cited for another question'] += 1; other_q.update(qs)
                    else: use['cited for no question'] += 1
            print(f'  {name} d{d}: links {len(rows)} | ' + ', '.join(f'{k} {v}' for k, v in sorted(cnt.items())) + ' || core+supp: ' + ', '.join(f'{k} {v}' for k, v in sorted(use.items())) + (f' | other questions {dict(other_q.most_common(4))}' if other_q else ''))

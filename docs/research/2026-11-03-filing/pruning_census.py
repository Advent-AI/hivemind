"""How many statements lost a link to a broader question in code (extraction.narrowest_links, D207): the extraction answer linked the
statement to a question and to a question it depends on, and the ledger keeps only the narrower one. Per draw: statements pruned, which
broad questions lost them, and samples. $0, read-only.

    python3 pruning_census.py
"""
import sqlite3, json, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
RUNS = {'v94': ROOT.parent / 'hivemind-extraction-quality-2026-10-28/docs/research/2026-11-01-e2e-loop/arms/r7-combined-v94', 'v108': ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03'}
for name, base in RUNS.items():
    for d in (1, 2, 3):
        c = sqlite3.connect(f'file:{base}/d{d}/views.sqlite?mode=ro', uri=True); a = sqlite3.connect(f'file:{base}/d{d}/archive.sqlite?mode=ro', uri=True)
        parents = collections.defaultdict(set)
        for v, dep in c.execute('select view_id, depends_on from dependencies'): parents[v].add(dep)
        def ancestors(v, seen=None):
            seen = set() if seen is None else seen
            for p in parents.get(v, ()):
                if p not in seen: seen.add(p); ancestors(p, seen)
            return seen
        lost = collections.Counter(); samples = []; n = 0
        for (aj,) in a.execute("select answer_json from model_calls where purpose='extract' and answer_json is not null"):
            for e in json.loads(aj).get('evidence', []):
                links = [l for l in (e.get('links') or []) if l.startswith('v')]
                broader = set().union(*[ancestors(l) for l in links]) if links else set()
                pruned = [l for l in links if l in broader]
                if pruned:
                    n += 1; lost.update(pruned)
                    if len(samples) < 3: samples.append((links, pruned, e.get('one_line', '')[:110]))
        print(f'{name} d{d}: statements that lost a broader link {n}; lost from {dict(lost.most_common(5))}')
        for links, pruned, ol in samples: print(f'     answer {links} -> dropped {pruned}: {ol}')

"""Link precision, blind, for an end-to-end comparison (design-placement-v2.md P4 and P5): per arm, the number of evidence links, the share
under the seeded company-wide figure questions (v1 total revenue, v2 Data Center revenue, v3 gross margin), and a blind packet of 40 links per
arm (statement, article, the question it was filed under) shuffled together for a reader to judge right / wrong / new in blind-seq/links.md's
format; the key (arm per entry) is written apart.
    python3 e2e_links_packet.py <out folder> <seed> name=run1,run2,run3 name2=run4,run5,run6"""
import json
import random
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import score_ref as sr  # noqa: E402

out_dir, seed = Path(sys.argv[1]), int(sys.argv[2])
arms = {}
for arg in sys.argv[3:]:
    name, paths = arg.split('=', 1)
    arms[name] = [str(ROOT / p) if not p.startswith('/') else p for p in paths.split(',')]
articles_by_id = {a['input_id']: a for a in sr.articles}
rng = random.Random(seed)
sample = []
for name, runs in arms.items():
    links, total, figure = [], 0, 0
    for draw, run in enumerate(runs, 1):
        views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); views.row_factory = sqlite3.Row
        questions = {r['view_id']: r['question'] for r in views.execute('select view_id, question from views')}
        for r in views.execute('select l.view_id, e.quote, e.one_line, e.created_from_input from evidence_links l join evidence e on e.evidence_id=l.evidence_id'):
            total += 1
            figure += r['view_id'] in ('v1', 'v2', 'v3')
            article = articles_by_id.get(r['created_from_input'])
            if article:
                links.append({'article': article['title'], 'day': article['publication_day'], 'quote': r['quote'], 'one_line': r['one_line'],
                              'question': questions[r['view_id']], 'arm': name, 'draw': draw, 'question_id': r['view_id'], 'input_id': r['created_from_input']})
    print(f'{name}: links {total}; under the figure seeds v1-v3: {figure} ({figure / max(total, 1):.0%}); links from gold articles {len(links)}')
    sample.extend(rng.sample(links, min(40, len(links))))
rng.shuffle(sample)
packet, key = [], {}
for n, s in enumerate(sample, 1):
    entry_id = f'L{n:02d}'
    key[entry_id] = {k: s[k] for k in ('arm', 'draw', 'question_id', 'input_id')}
    packet.append({'id': entry_id, **{k: s[k] for k in ('article', 'day', 'quote', 'one_line', 'question')}})
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / 'links.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
(out_dir / 'key.json').write_text(json.dumps(key, ensure_ascii=False, indent=1))
print(len(packet), 'links in the packet')

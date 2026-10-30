"""D244: the test set. Articles the pipeline would extract (feed items, not copies or corrections, a research-list object in
a watched category: dispatch.route) from 2026-09-01..2026-10-27, a window no run or arm has read (the three-month run
stopped at 2026-08-28; the bench is 2026-07-01..14). Thirty articles in the development set's category mix (T7 73, T8 25,
T6 20 of 118 -> 19, 6, 5), drawn with a fixed seed. Writes test-pick.json and the drafting batches with full text."""
import json, random, sqlite3, sys
from pathlib import Path
ROOT = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import universe  # noqa: E402

HERE = Path(__file__).resolve().parent
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
QUOTA = {'T7': 19, 'T8': 6, 'T6': 5}
SEED = 20261029

uni = universe.load(ROOT / 'poc/universe.json')
db = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
db.row_factory = sqlite3.Row
eligible = {k: [] for k in QUOTA}
for row in db.execute("select * from items where publication_day >= '2026-09-01' and publication_day <= '2026-10-27' and feed = 1 "
                      "and copy_of is null and supersedes is null order by input_id"):
    item = dict(row)
    if item['category'] not in QUOTA or not (item['text'] or '').strip():
        continue
    objects = [o['value'] for o in json.loads(item['object_identifiers'] or '[]') if uni.has(o['value'])]
    if objects and any(uni.watches(o, item['category']) for o in objects):
        eligible[item['category']].append(item)
rng = random.Random(SEED)
picked = []
for cat, n in QUOTA.items():
    picked += rng.sample(eligible[cat], n)
picked.sort(key=lambda i: (i['publication_day'], i['input_id']))
print({k: len(v) for k, v in eligible.items()}, 'eligible;', len(picked), 'picked')
meta = [{'input_id': i['input_id'], 'category': i['category'], 'day': i['publication_day'], 'publisher': i['publisher'],
         'title': i['title'], 'chars': len(i['text'])} for i in picked]
(HERE / 'test-pick.json').write_text(json.dumps({'seed': SEED, 'quota': QUOTA, 'window': ['2026-09-01', '2026-10-27'],
                                                 'eligible': {k: len(v) for k, v in eligible.items()}, 'articles': meta}, ensure_ascii=False, indent=1) + '\n')
(HERE / 'batches').mkdir(exist_ok=True)
for b in range(3):
    part = picked[b * 10:(b + 1) * 10]
    (HERE / 'batches' / f'batch-{b + 1}.json').write_text(json.dumps(
        [{'input_id': i['input_id'], 'set': 'test', 'category': i['category'], 'publication_day': i['publication_day'], 'publisher': i['publisher'],
          'title': i['title'], 'text': i['text']} for i in part], ensure_ascii=False, indent=1) + '\n')
for m in meta:
    print(m['day'], m['category'], m['chars'], m['publisher'][:22], '|', m['title'][:80])

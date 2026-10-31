"""Pick the noise small sample from stored role-v53 answers (run U, dev gold only): articles where a gold not-kept sentence was kept in at
least two of three draws, and gold-empty pages (no core or supporting) where v53 kept statements in at least two draws; plus 12 random
dev articles outside both as guards (seed 20261101). Writes the frozen key: decisive not-kept sentences, guard core/supporting items."""
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard')
OUT = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-30-noise')
sys.path[:0] = [str(ROOT), str(ROOT / 'final-2026-10-30')]
import score_gold as sg  # noqa: E402
import final_scores as fs  # noqa: E402

articles = json.loads(Path(fs.GOLDS['dev']).read_text())['articles']
runs = [sg.answers(f'U-v53-d{d}') for d in (1, 2, 3)]
PROBED = ['gnews:ad47330f25c9d5ff84ced7e2', 'gnews:beb97ecf3fbd192e0636c2db', 'gnews:4a892d75e355bee00aa3c572', 'gnews:56085a9d3e88c464bcaed67b',
          'edgar:NVDA:0001045810-26-000060:nvda-20260628.htm', 'gnews:085b1e1a1543437edb9756d6', 'gnews:c0432377817a1c00a1bbadf0',
          'gnews:2f953a56cd06571ab0afc348', 'gnews:9e0d5b0d6b3e603c60340128']   # the nine articles whose noise the model explained
NOISE_ARTICLES, EMPTY_PAGES, GUARDS = 20, 8, 12
stable_by, empty_by = {}, {}
for a in articles:
    iid = a['input_id']
    sifted = [sg.kept(r.get(iid), iid) for r in runs]
    nks = [n for n in a['not_kept'] if n['weight'] == 'not_kept']
    stable = [n for n in nks if sum(bool(s) and any(sg.same(n['span'], e['quote']) for e in s['evidence']) for s in sifted) >= 2]
    keeps = [i for i in a['items'] if i['weight'] in ('core', 'supporting')]
    nonempty = sum(bool(s and s['evidence']) for s in sifted)
    stable_by[iid] = stable
    if not keeps and nonempty >= 2:
        empty_by[iid] = sum(len(s['evidence']) for s in sifted if s)
dev_ids = {a['input_id'] for a in articles}
chosen = [i for i in PROBED if i in dev_ids]
for iid in sorted(stable_by, key=lambda i: (-len(stable_by[i]), i)):
    if len(chosen) >= NOISE_ARTICLES:
        break
    if stable_by[iid] and iid not in chosen:
        chosen.append(iid)
empty_pages = [i for i in sorted(empty_by, key=lambda i: (-empty_by[i], i)) if i not in chosen][:EMPTY_PAGES]
chosen += empty_pages
decisive = [{'input_id': iid, 'span': n['span'], 'row': n.get('row')} for iid in chosen for n in stable_by.get(iid, [])]
rest = [a['input_id'] for a in articles if a['input_id'] not in chosen]
guards_random = random.Random(20261101).sample(rest, GUARDS)
sample = chosen + guards_random
guard_items = [{'input_id': a['input_id'], 'weight': i['weight'], 'span': i['span']}
               for a in articles if a['input_id'] in sample for i in a['items'] if i['weight'] in ('core', 'supporting')]
key = {'about': 'Noise small sample, frozen before any send (2026-10-30). Decisive: gold v3 not-kept sentences role-v53 kept in >=2 of 3 '
                'draws of run U (the arm should keep them less often). Empty pages: dev articles with no core or supporting gold entry where '
                'role-v53 kept statements in >=2 draws (statements kept there are counted; gold-optional ones are not noise). Guards: every '
                'core and supporting gold entry of the sampled articles (the arm must keep them as often as role-v53, three draws each). '
                'Gold: golden-v3-signed.json with gold-v4-evidence-check.md (no evidence entry changed).',
       'articles': sample, 'noise_articles': chosen, 'random_guard_articles': guards_random, 'empty_pages': empty_pages, 'probed_articles': [i for i in PROBED if i in dev_ids],
       'decisive_not_kept': decisive, 'guard_items': guard_items}
body = json.dumps(key, ensure_ascii=False, indent=1)
(OUT / 'key-small.json').write_text(body)
(OUT / 'key-small.sha256').write_text(hashlib.sha256(body.encode()).hexdigest() + '  key-small.json\n')
print('articles', len(sample), '| noise articles', len(chosen), '| empty pages', len(empty_pages), '| random guards', len(guards_random))
print('decisive not-kept sentences', len(decisive), '| guard items', len(guard_items), {w: sum(g['weight'] == w for g in guard_items) for w in ('core', 'supporting')})
print('sha256', hashlib.sha256(body.encode()).hexdigest())

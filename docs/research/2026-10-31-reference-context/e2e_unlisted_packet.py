"""Blind packet to re-estimate the noise share of the pieces that reach judgement and that the gold lists nowhere (e2e_compare.py's
UNLISTED_NOISE_SHARE was read on the extraction's kept statements, another population): 60 distinct gold-unlisted statements stored and not
replaced in the given runs, from gold articles, each with its article's title, day, opening and passage (blind-v68a-ruler/unlisted.json's
shape); the readers weigh them under standard version 5.   python3 e2e_unlisted_packet.py <out folder> <seed> run1 run2 run3"""
import json
import random
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import score_ref as sr  # noqa: E402

ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
OPENING, WINDOW = 600, 500
out_dir, seed, runs = Path(sys.argv[1]), int(sys.argv[2]), [str(ROOT / p) if not p.startswith('/') else p for p in sys.argv[3:]]
articles = {a['input_id']: a for a in sr.articles}


def unlisted(a, e):
    if any(sr.sg.same_matter(i, e) for i in a['items']):
        return False
    return not any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'])


pool = {}
for run in runs:
    v = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); v.row_factory = sqlite3.Row
    replaced = {r[0] for r in v.execute('select old_evidence_id from replacements')}
    for r in v.execute('select evidence_id, quote, one_line, created_from_input from evidence'):
        a = articles.get(r['created_from_input'])
        if a and r['evidence_id'] not in replaced and unlisted(a, dict(r)):
            pool.setdefault((a['input_id'], r['quote']), r['one_line'])
print(len(pool), 'distinct gold-unlisted statements reaching judgement over', len(runs), 'runs')
chosen = random.Random(seed).sample(sorted(pool), min(60, len(pool)))
db = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
texts = {iid: db.execute('select text from items where input_id=?', (iid,)).fetchone()[0] for iid in {c[0] for c in chosen}}


def passage(text, span):
    at = text.find(span)
    if at < 0:
        at = text.find(span[:60])
    if at < 0:
        span_words = sr.sg.words(span)
        at = max(range(0, max(1, len(text) - len(span)), 50), key=lambda i: len(span_words & sr.sg.words(text[i:i + len(span) + 100])))
    start, end = max(0, at - WINDOW), min(len(text), at + len(span) + WINDOW)
    return ('…' if start else '') + text[start:end] + ('…' if end < len(text) else '')


entries, key = [], {}
for n, (iid, quote) in enumerate(chosen, 1):
    sid, a = f'U{n:02d}', articles[iid]
    key[sid] = {'input_id': iid, 'quote': quote, 'one_line': pool[(iid, quote)]}
    entries.append({'id': sid, 'article_id': iid, 'title': a['title'], 'publication_day': a['publication_day'],
                    'article_opening': texts[iid][:OPENING], 'passage': passage(texts[iid], quote), 'statement': quote})
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / 'unlisted.json').write_text(json.dumps(entries, ensure_ascii=False, indent=1))
(out_dir / 'unlisted.key.json').write_text(json.dumps(key, ensure_ascii=False, indent=1))
(out_dir / 'articles.json').write_text(json.dumps({iid: {'title': articles[iid]['title'], 'publication_day': articles[iid]['publication_day'], 'text': t} for iid, t in texts.items()}, ensure_ascii=False, indent=1))
print(len(entries), 'in the packet from', len(texts), 'articles')

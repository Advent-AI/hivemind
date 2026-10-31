"""Build a blind packet that tests the ruler, not a version: every not-kept gold entry a version keeps in at least one draw of a full
run (kept-rejected-<PREFIX>-<VERSION>.json from kept_rejected.py), mixed with two controls the reader cannot tell apart from them:
core or supporting gold entries the version keeps in at least two draws, and not-kept gold entries it keeps in no draw. Each statement
carries its article's title, day, opening and the passage around it. A reader who did not write the gold or the prompt gives each a
weight under the signed standard and says whether the standard settles it. Labels and the key are written apart; seed fixed.

    python3 blind_ruler.py Y3 v63 [packets] [seed] [folder] [kept_controls] [dropped_controls]
    (folder defaults to blind4; a later folder reads kept-rejected-<PREFIX>-<VERSION>.json as written for it, e.g. only unread entries)
"""
import json
import random
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / '2026-10-29-ledger-standard'
sys.path[:0] = [str(LEDGER), str(LEDGER / 'final-2026-10-30')]
import final_scores as fs  # noqa: E402
import score_gold as sg  # noqa: E402

ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
KEPT_CONTROLS, DROPPED_CONTROLS, WINDOW, OPENING = 40, 30, 700, 500

prefix, version = sys.argv[1], sys.argv[2]
packets = int(sys.argv[3]) if len(sys.argv) > 3 else 3
rng = random.Random(int(sys.argv[4]) if len(sys.argv) > 4 else 20261031)
FOLDER = HERE / (sys.argv[5] if len(sys.argv) > 5 else 'blind4')
FOLDER.mkdir(exist_ok=True)
if len(sys.argv) > 7:
    KEPT_CONTROLS, DROPPED_CONTROLS = int(sys.argv[6]), int(sys.argv[7])
articles = {a['input_id']: a for a in json.loads(Path(fs.GOLDS['dev']).read_text())['articles']}
kept_rejected = json.loads((HERE / f'kept-rejected-{prefix}-{version}.json').read_text())
rows = json.loads((LEDGER / 'final-2026-10-30' / f'per-article-{prefix}-dev.json').read_text())[version]
sifted = [{iid: sg.kept(run.get(iid), iid) for iid in articles} for run in (sg.answers(f'{prefix}-{version}-d{d}') for d in (1, 2, 3))]

kept_pool = [(iid, item) for iid, a in articles.items() for weight, key in (('core', 'core'), ('supporting', 'supp'))
             for idx, item in enumerate([i for i in a['items'] if i['weight'] == weight]) if sum(rows[iid][key][idx]) >= 2]
listed = {(e['input_id'], e['span']) for e in kept_rejected}
dropped_pool = [(iid, n) for iid, a in articles.items() for n in a['not_kept'] if n['weight'] == 'not_kept' and (iid, n['span']) not in listed
                and not any(sg.same(n['span'], e['quote']) for s in sifted if s.get(iid) for e in s[iid]['evidence'])]
chosen = ([('kept_rejected', e['input_id'], e['span'], 'not_kept', e['row']) for e in kept_rejected]
          + [('control_kept', iid, it['span'], it['weight'], it.get('rule', '')) for iid, it in rng.sample(kept_pool, KEPT_CONTROLS)]
          + [('control_dropped', iid, n['span'], 'not_kept', n.get('row', '')) for iid, n in rng.sample(dropped_pool, DROPPED_CONTROLS)])
rng.shuffle(chosen)

db = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
texts = {iid: db.execute('select text from items where input_id=?', (iid,)).fetchone()[0] for iid in {c[1] for c in chosen}}


def passage(text, span):
    """The text around the span: an exact find, else the first 60 characters of the span, else the best word overlap window."""
    at = text.find(span)
    if at < 0:
        at = text.find(span[:60])
    if at < 0:
        span_words = sg.words(span)
        at = max(range(0, max(1, len(text) - len(span)), 50), key=lambda i: len(span_words & sg.words(text[i:i + len(span) + 100])))
    start, end = max(0, at - WINDOW), min(len(text), at + len(span) + WINDOW)
    return ('…' if start else '') + text[start:end] + ('…' if end < len(text) else '')


entries, key = [], {}
for n, (group, iid, span, weight, reason) in enumerate(chosen, 1):
    sid = f'S{n:03d}'
    a = articles[iid]
    key[sid] = {'group': group, 'input_id': iid, 'gold_weight': weight, 'gold_reason': reason, 'span': span}
    entries.append({'id': sid, 'article_id': iid, 'title': a['title'], 'publication_day': a['publication_day'],
                    'article_opening': texts[iid][:OPENING], 'passage': passage(texts[iid], span), 'statement': span})
size = -(-len(entries) // packets)
for p in range(packets):
    (FOLDER / f'packet-{p + 1}.json').write_text(json.dumps(entries[p * size:(p + 1) * size], ensure_ascii=False, indent=1))
(FOLDER / 'key.json').write_text(json.dumps(key, ensure_ascii=False, indent=1))
(FOLDER / 'articles.json').write_text(json.dumps({iid: {'title': articles[iid]['title'], 'publication_day': articles[iid]['publication_day'],
                                                                  'text': t} for iid, t in texts.items()}, ensure_ascii=False, indent=1))
print(len(entries), 'statements in', packets, 'packets:', {g: sum(c[0] == g for c in chosen) for g in ('kept_rejected', 'control_kept', 'control_dropped')})

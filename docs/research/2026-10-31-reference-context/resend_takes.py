"""Cheapest proof for the takes-line clause (AGENTS §1 step 4; design-placement-v2.md measured section): re-send one draw's stored placement
requests for the gold articles with every figure question's takes line stripped of ", and the direct drivers of that figure stated with a
size", one send each, and count per gold class the statements that lose every home, gain one or move. One draw, one send: a mechanism's
size, not a difference between arms.
    python3 resend_takes.py <run folder> <config json> <reader-A unlisted verdicts.jsonl> <unlisted.key.json>"""
import collections
import concurrent.futures
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'src')); sys.path.insert(0, str(HERE))
from hivemind import config, model  # noqa: E402
import score_ref as sr  # noqa: E402

CLAUSE = ', and the direct drivers of that figure stated with a size'
run, cfg = sys.argv[1], config.load(sys.argv[2])
rows = [json.loads(l) for l in open(sys.argv[3]) if l.strip().startswith('{')]
ukey = json.load(open(sys.argv[4]))
noisy_unlisted = {(ukey[r['id']]['input_id'], ukey[r['id']]['quote']) for r in rows if r['weight'] == 'not_kept'}
weighed_unlisted = {(ukey[r['id']]['input_id'], ukey[r['id']]['quote']): r['weight'] for r in rows}


def gold_class(a, e):
    if any(sr.sg.same_matter(i, e) for i in a['items'] if i['weight'] in ('core', 'supporting')):
        return 'core/supp'
    if any(sr.sg.same_matter(i, e) for i in a['items'] if i['weight'] == 'optional') or any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'optional'):
        return 'optional'
    if any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'not_kept'):
        return 'not_kept'
    w = weighed_unlisted.get((a['input_id'], e['quote']))
    return f'unlisted, reader A {w}' if w else 'unlisted, unread'


def one(a):
    archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)   # one connection per call: a shared one segfaults under threads
    needle = json.dumps(a['title'], ensure_ascii=False)[1:-1]
    row = archive.execute("select request_json, answer_json from model_calls where purpose='place' and request_json like ? order by call_id desc limit 1", (f'%{needle}%',)).fetchone()
    ext = archive.execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {a["input_id"]},%',)).fetchone()
    if not row or not ext:
        return None
    body = json.loads(row[0]); stored = {p['id']: p['links'] for p in json.loads(row[1])['placements']}
    user = body['messages'][-1]['content']
    stripped = user.count(CLAUSE)
    body['messages'][-1]['content'] = user.replace(CLAUSE, '')
    answer = json.loads(model.openai_transport(cfg.provider, body)['choices'][0]['message']['content'])
    new = {p['id']: p['links'] for p in answer['placements']}
    by_id = {e['id']: e for e in json.loads(ext[0]).get('evidence', [])}
    out = []
    for sid, old in stored.items():
        if sid not in by_id:
            continue
        cls = gold_class(a, by_id[sid]); now = new.get(sid, [])
        change = 'unchanged' if set(old) == set(now) else ('loses every home' if old and not now else ('gains a home' if not old and now else 'moves'))
        out.append((cls, change))
    return stripped, out


counts = collections.Counter(); stripped_total = 0; calls = 0
with concurrent.futures.ThreadPoolExecutor(8) as pool:
    for result in pool.map(one, sr.articles):
        if result is None:
            continue
        calls += 1; stripped_total += result[0]
        for cls, change in result[1]:
            counts[(cls, change)] += 1
print(f'{calls} placement requests re-sent once each; {stripped_total} takes lines stripped of the clause')
classes = sorted({c for c, _ in counts})
print(f'{"class":<28}{"unchanged":>11}{"loses home":>12}{"gains home":>12}{"moves":>8}')
for c in classes:
    print(f'{c:<28}{counts[(c, "unchanged")]:>11}{counts[(c, "loses every home")]:>12}{counts[(c, "gains a home")]:>12}{counts[(c, "moves")]:>8}')

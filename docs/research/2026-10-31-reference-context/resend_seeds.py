"""Cheapest proof for a seed list (review-2026-10-31-method.md R1; AGENTS §1 step 4): re-send one draw's stored placement requests for the
gold articles with the NEW seed questions (those absent from the stored request) appended to the [Open questions] block, lines written by
placement.takes as the product writes them, one send each; count per gold class the statements that gain a home, and which seeds take them.
One draw, one send: a mechanism's size, not a difference between arms.
    python3 resend_seeds.py <run folder> <config json> <seed json> <reader verdicts A.jsonl> <reader verdicts B.jsonl> <unlisted.key.json>"""
import collections
import concurrent.futures
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'src')); sys.path.insert(0, str(HERE))
from hivemind import config, model, placement  # noqa: E402
import score_ref as sr  # noqa: E402

run, cfg, seed = sys.argv[1], config.load(sys.argv[2]), json.load(open(sys.argv[3]))
ukey = json.load(open(sys.argv[6]))
readers = [{r['id']: r['weight'] for r in (json.loads(l) for l in open(p) if l.strip().startswith('{'))} for p in sys.argv[4:6]]
noisy_unlisted = {(ukey[i]['input_id'], ukey[i]['quote']) for i in ukey if all(w.get(i) == 'not_kept' for w in readers)}
noisy_either = {(ukey[i]['input_id'], ukey[i]['quote']) for i in ukey if any(w.get(i) == 'not_kept' for w in readers)}


def seed_line(q):
    view = dict(q, key=q['key'], groups=[])
    return f"  - {q['view_id']} ({q['object_id']}, due {q['due_day']}): {q['question']}\n      {placement.takes(view)}"


def gold_class(a, e):
    if any(sr.sg.same_matter(i, e) for i in a['items'] if i['weight'] in ('core', 'supporting')):
        return 'core/supp'
    if any(sr.sg.same_matter(i, e) for i in a['items'] if i['weight'] == 'optional') or any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'optional'):
        return 'optional'
    if any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'not_kept'):
        return 'noise (gold not kept)'
    if (a['input_id'], e['quote']) in noisy_unlisted:
        return 'noise (unlisted, both readers)'
    if (a['input_id'], e['quote']) in noisy_either:
        return 'unlisted, one reader not kept'
    return 'unlisted, other'


def one(a):
    archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    needle = json.dumps(a['title'], ensure_ascii=False)[1:-1]
    row = archive.execute("select request_json, answer_json from model_calls where purpose='place' and request_json like ? order by call_id desc limit 1", (f'%{needle}%',)).fetchone()
    ext = archive.execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {a["input_id"]},%',)).fetchone()
    if not row or not ext:
        return None
    body = json.loads(row[0]); stored = {p['id']: p['links'] for p in json.loads(row[1])['placements']}
    user = body['messages'][-1]['content']
    new = [q for q in seed['questions'] if f"  - {q['view_id']} (" not in user and q['question'] not in user]
    head, tail = user.split('\n\n[Statements]', 1)
    body['messages'][-1]['content'] = head + '\n' + '\n'.join(seed_line(q) for q in new) + '\n\n[Statements]' + tail
    answer = json.loads(model.openai_transport(cfg.provider, body)['choices'][0]['message']['content'])
    links = {p['id']: p['links'] for p in answer['placements']}
    by_id = {e['id']: e for e in json.loads(ext[0]).get('evidence', [])}
    new_ids = {q['view_id'] for q in new}
    out = []
    for sid, old in stored.items():
        if sid not in by_id:
            continue
        cls, now = gold_class(a, by_id[sid]), links.get(sid, [])
        to_seed = [v for v in now if v in new_ids]
        change = ('gains a home' if not old and now else 'loses every home' if old and not now else 'moves' if set(old) != set(now) else 'unchanged')
        out.append((cls, change, to_seed[0] if to_seed else ''))
    return len(new), out


counts, by_seed = collections.Counter(), collections.Counter()
calls = 0
with concurrent.futures.ThreadPoolExecutor(8) as pool:
    for result in pool.map(one, sr.articles):
        if result is None:
            continue
        calls += 1
        for cls, change, to_seed in result[1]:
            counts[(cls, change)] += 1
            if to_seed:
                by_seed[(to_seed, cls)] += 1
print(f'{calls} placement requests re-sent once each with the new seeds appended')
print(f'{"class":<32}{"unchanged":>10}{"gains home":>11}{"loses home":>11}{"moves":>7}')
for cls in sorted({c for c, _ in counts}):
    print(f'{cls:<32}{counts[(cls, "unchanged")]:>10}{counts[(cls, "gains a home")]:>11}{counts[(cls, "loses every home")]:>11}{counts[(cls, "moves")]:>7}')
print('\nstatements filed under a new seed (gains and moves), by seed and class:')
for vid in sorted({v for v, _ in by_seed}, key=lambda s: int(s[1:])):
    print(f'  {vid:>4}: ' + ', '.join(f'{c} {by_seed[(vid, c)]}' for c in sorted({c for v, c in by_seed if v == vid})))

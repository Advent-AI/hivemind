"""The simplest test of the filing hypothesis: re-send stored extraction requests exactly as production sent them, except for the sentences
a variant replaces, and print every statement's links per send beside the stored answer. Arms: 'stored' (no change, the control: how much
the model sways on its own), and the variants in variants.py. No ledger is written; the answer's own links are what the hypothesis is
about. About $0.0013 a send.

    python3 test_filing.py --calls d1:818 d1:214 ... --arms stored v1 v2 --sends 3 [--save out.json] [--replay out.json]
"""
import argparse
import json
import sqlite3
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / 'src')]
from hivemind import config, model  # noqa: E402
import variants  # noqa: E402

RUN = ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03'
CFG = config.load(str(ROOT / 'poc/config/poc-v108.json'))


def stored(draw, call_id):
    a = sqlite3.connect(f'file:{RUN}/{draw}/archive.sqlite?mode=ro', uri=True)
    req, ans = a.execute('select request_json, answer_json from model_calls where call_id=?', (call_id,)).fetchone()
    return json.loads(req), json.loads(ans)


def send(body):
    reply = model.openai_transport(CFG.provider, body, timeout=300)
    return json.loads(reply['choices'][0]['message']['content'])


def show(tag, answer):
    ev = answer.get('evidence', [])
    empty = sum(1 for e in ev if not e.get('links'))
    print(f'  {tag}: {len(ev)} statements, {empty} with no link')
    for e in ev:
        print(f"      {e['id']:>4} {','.join(e.get('links') or []) or '-':<14} {e.get('one_line', '')[:120]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--calls', nargs='+', required=True)
    ap.add_argument('--arms', nargs='+', default=['stored'])
    ap.add_argument('--sends', type=int, default=3)
    ap.add_argument('--save'); ap.add_argument('--replay')
    args = ap.parse_args()
    saved = json.load(open(args.replay)) if args.replay else {}
    jobs = {}
    with ThreadPoolExecutor(8) as pool:
        for call in args.calls:
            draw, cid = call.split(':')
            req, _ = stored(draw, int(cid))
            for arm in args.arms:
                body = variants.apply(arm, req)
                for n in range(args.sends):
                    key = f'{call}|{arm}|{n}'
                    if key not in saved:
                        jobs[key] = pool.submit(send, body)
        for key, fut in jobs.items():
            try:
                saved[key] = fut.result()
            except Exception as exc:          # a failed send is reported, never silently dropped
                saved[key] = {'error': str(exc)[:300]}
    if args.save:
        json.dump(saved, open(args.save, 'w'), ensure_ascii=False, indent=1)
    for call in args.calls:
        draw, cid = call.split(':')
        req, ans = stored(draw, int(cid))
        title = req['messages'][1]['content'].split('title: ', 1)[-1].split('\n', 1)[0][:90]
        print(f'\n## {call} | {title}')
        show('as stored in the run', ans)
        for arm in args.arms:
            for n in range(args.sends):
                a = saved.get(f'{call}|{arm}|{n}', {})
                if 'error' in a: print(f'  {arm} send {n + 1}: ERROR {a["error"]}'); continue
                show(f'{arm} send {n + 1}', a)


if __name__ == '__main__':
    main()

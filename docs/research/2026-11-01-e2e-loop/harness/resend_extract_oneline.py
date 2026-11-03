"""Cheapest proof of an extraction-prompt sentence change on stored requests (AGENTS §1 step 4): re-send the stored extraction
request of named articles n times as stored and n times with one system-prompt sentence replaced, and print every statement's
one-line summary side by side, marking the statements whose quote carries a named fragment (the class under test). Sends the bytes
production sent, with only the one sentence changed; about $0.001 a send.

    python3 resend_extract_oneline.py <run folder> <config json> <old sentence file> <new sentence file> <n> --match TITLE... [--span FRAGMENT...]
"""
import argparse
import json
import sqlite3
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / 'docs/research/2026-10-31-reference-context'), str(ROOT / 'src')]
import score_ref as sr  # noqa: E402
from hivemind import config, model  # noqa: E402

SENDERS = 8


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('run'); ap.add_argument('config'); ap.add_argument('old_file'); ap.add_argument('new_file'); ap.add_argument('n', type=int)
    ap.add_argument('--match', nargs='+', required=True, help='article title fragments (case-insensitive)')
    ap.add_argument('--span', nargs='*', default=[], help='quote fragments that mark the statements under test')
    args = ap.parse_args()
    cfg = config.load(args.config)
    archive = sqlite3.connect(f'file:{args.run}/archive.sqlite?mode=ro', uri=True)
    old, new = Path(args.old_file).read_text(encoding='utf-8').strip(), Path(args.new_file).read_text(encoding='utf-8').strip()
    wanted = [m.lower() for m in args.match]
    marks = [s.lower() for s in args.span]
    articles = [a for a in sr.articles if any(w in a['title'].lower() for w in wanted)]
    print(f'articles {len(articles)}; sentence replaced: {old[:60]!r} -> {new[:60]!r}; n {args.n} as stored + {args.n} edited', flush=True)

    def send(body):
        content = model.openai_transport(cfg.provider, body)['choices'][0]['message']['content']
        return json.loads(content).get('evidence', [])

    jobs = []
    with ThreadPoolExecutor(SENDERS) as pool:
        for a in articles:
            row = archive.execute("select request_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1",
                                  (f'%[Item] id {a["input_id"]},%',)).fetchone()
            if not row:
                print(f'- no stored extraction request for {a["title"][:60]!r}', flush=True); continue
            body = json.loads(row[0])
            system = body['messages'][0]['content']
            if system.count(old) != 1:
                print(f'- {a["title"][:60]!r}: the old sentence occurs {system.count(old)} times in the stored system prompt; skipped', flush=True); continue
            edited = json.loads(json.dumps(body)); edited['messages'][0]['content'] = system.replace(old, new)
            jobs.append((a, [pool.submit(send, json.loads(json.dumps(body))) for _ in range(args.n)],
                            [pool.submit(send, json.loads(json.dumps(edited))) for _ in range(args.n)]))
        for a, control_f, edited_f in jobs:
            control = [f.result() for f in control_f]; edited = [f.result() for f in edited_f]
            print(f'\n## {a["publication_day"]} | {a["title"][:90]}', flush=True)
            for label, sends in (('control', control), ('edited', edited)):
                for i, evidence in enumerate(sends, 1):
                    lengths = [len(e.get('one_line') or '') for e in evidence]
                    print(f'### {label} send {i}: {len(evidence)} statements, one_line mean {sum(lengths) / max(1, len(lengths)):.0f} chars', flush=True)
                    for e in evidence:
                        mark = ' <<' if any(m in (e.get('quote') or '').lower() for m in marks) else ''
                        print(f'  - {e.get("id")}{mark} | {e.get("one_line")}\n      quote: {(e.get("quote") or "")[:110]!r}', flush=True)
            if marks:
                print('### marked statements, control -> edited one_line', flush=True)
                for m in marks:
                    c = [e.get('one_line') for s in control for e in s if m in (e.get('quote') or '').lower()]
                    d = [e.get('one_line') for s in edited for e in s if m in (e.get('quote') or '').lower()]
                    print(f'  [{m}] control {len(c)}/{args.n} sends: {c}\n  [{m}] edited  {len(d)}/{args.n} sends: {d}', flush=True)


if __name__ == '__main__':
    main()

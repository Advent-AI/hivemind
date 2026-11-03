"""Cheapest proof of a schema field definition on stored extraction requests (AGENTS §1 step 4, §2 "a field's definition sits in
the schema beside the field"): re-send the stored extraction request of named articles n times as stored and n times with a
description added to one evidence field, and print, per statement, the links it gets in each send, marking the statements whose
quote carries a named fragment (the class under test) and counting every statement that gains a link (the guard: a definition
must not link everything). Sends the bytes production sent, with only the one description added; about $0.001 a send.

    python3 resend_extract_links.py <run folder> <config json> <field> <note file> <n> --match TITLE... [--span FRAGMENT...]
"""
import argparse
import collections
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
    ap.add_argument('run'); ap.add_argument('config'); ap.add_argument('field'); ap.add_argument('note_file'); ap.add_argument('n', type=int)
    ap.add_argument('--match', nargs='+', required=True); ap.add_argument('--span', nargs='*', default=[])
    args = ap.parse_args()
    cfg = config.load(args.config)
    archive = sqlite3.connect(f'file:{args.run}/archive.sqlite?mode=ro', uri=True)
    note = Path(args.note_file).read_text(encoding='utf-8').strip()
    wanted = [m.lower() for m in args.match]; marks = [s.lower() for s in args.span]
    articles = [a for a in sr.articles if any(w in a['title'].lower() for w in wanted)]
    print(f'articles {len(articles)}; field {args.field!r} gets a description of {len(note)} characters; n {args.n} as stored + {args.n} edited', flush=True)

    def send(body):
        content = model.openai_transport(cfg.provider, body)['choices'][0]['message']['content']
        return json.loads(content)

    jobs = []
    with ThreadPoolExecutor(SENDERS) as pool:
        for a in articles:
            row = archive.execute("select request_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1",
                                  (f'%[Item] id {a["input_id"]},%',)).fetchone()
            if not row:
                print(f'- no stored extraction request for {a["title"][:60]!r}', flush=True); continue
            body = json.loads(row[0])
            edited = json.loads(json.dumps(body))
            field = edited['response_format']['json_schema']['schema']['properties']['evidence']['items']['properties'][args.field]
            assert 'description' not in field, f'{args.field} already carries a description in the stored request'
            field['description'] = note
            jobs.append((a, [pool.submit(send, json.loads(json.dumps(body))) for _ in range(args.n)],
                            [pool.submit(send, json.loads(json.dumps(edited))) for _ in range(args.n)]))
        totals = collections.Counter()
        for a, control_f, edited_f in jobs:
            control = [f.result() for f in control_f]; edited = [f.result() for f in edited_f]
            print(f'\n## {a["publication_day"]} | {a["title"][:90]}', flush=True)
            for label, sends in (('control', control), ('edited', edited)):
                for i, ans in enumerate(sends, 1):
                    ev, cands = ans.get('evidence', []), ans.get('candidates', [])
                    linked = sum(1 for e in ev if e.get('links'))
                    totals[(label, 'statements')] += len(ev); totals[(label, 'linked')] += linked
                    print(f'### {label} send {i}: {len(ev)} statements, {linked} linked; candidates: '
                          + '; '.join(f'{c.get("id")} {(c.get("question") or c.get("title") or "")[:70]}' for c in cands), flush=True)
                    for e in ev:
                        mark = ' <<' if any(m in (e.get('quote') or '').lower() for m in marks) else ''
                        print(f'  - {e.get("id")}{mark} links {e.get("links")} | {(e.get("one_line") or "")[:120]}', flush=True)
            if marks:
                print('### marked statements, links per send (control -> edited)', flush=True)
                for m in marks:
                    c = [[e.get('links') for e in s.get('evidence', []) if m in (e.get('quote') or '').lower()] for s in control]
                    d = [[e.get('links') for e in s.get('evidence', []) if m in (e.get('quote') or '').lower()] for s in edited]
                    print(f'  [{m}] control {c} -> edited {d}', flush=True)
    print('\ntotals: ' + ', '.join(f'{k[0]} {k[1]} {v}' for k, v in sorted(totals.items())), flush=True)


if __name__ == '__main__':
    main()

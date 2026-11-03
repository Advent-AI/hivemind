"""Arm beside control on stored articles (AGENTS §6): the stored extraction request re-sent with role-v15 as the system message
(arm) against the stored answer (control, role-v12) and, for two items, a fresh re-send of the unchanged request (sampling).
For every control piece we know whether any judgement ever cited it; the arm is scored by which of them it kept.
Run: python3 pinned_arm.py <run folder> <items.sqlite> <scratch archive> <input_id...>"""
import json
import os
import re
import sqlite3
import sys
import time
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import model  # noqa: E402

ROLE_V15 = open(os.path.join(ROOT, 'src', 'hivemind', 'prompts', 'role-v15.txt'), encoding='utf-8').read()
REVENUE = ('v6', 'v11')


def norm(text):
    return re.sub(r'\W+', ' ', text or '').strip().lower()


def same_piece(a, b):
    qa, qb = norm(a['quote']), norm(b['quote'])
    if not qa or not qb:
        return False
    short, long_ = (qa, qb) if len(qa) <= len(qb) else (qb, qa)
    return short in long_ or len(set(short.split()) & set(long_.split())) >= 0.7 * len(set(short.split()))


def send(archive, request, system_text, purpose_tag):
    request = json.loads(json.dumps(request))
    if system_text is not None:
        request['messages'][0]['content'] = system_text
    started = time.time()
    response = model.openai_transport('openai', request)
    data = json.loads(response['choices'][0]['message']['content'])
    usage = response.get('usage') or {}
    tin, tout = int(usage.get('prompt_tokens') or 0), int(usage.get('completion_tokens') or 0)
    cached = min(tin, int((usage.get('prompt_tokens_details') or {}).get('cached_tokens') or 0))
    pin, pout = model.PRICES[request['model']]
    cost = round((tin - cached) / 1e6 * pin + cached / 1e6 * pin * model.CACHED_INPUT_SHARE + tout / 1e6 * pout, 6)
    archive.record(purpose=f'extract:{purpose_tag}', config_version='poc-v31', config_checksum='pinned', model=request['model'],
                   request_sha256=model.request_identity(request)[1] + ':' + uuid.uuid4().hex[:6], request_json=json.dumps(request),
                   response_json=json.dumps(response)[:200000], answer_json=json.dumps(data, ensure_ascii=False), prompt_chars=sum(len(m['content']) for m in request['messages']),
                   input_tokens=tin, output_tokens=tout, cost_usd=cost, seconds=round(time.time() - started, 1), created_at=time.strftime('%Y-%m-%dT%H:%M:%S'))
    return data, cost


def main(run, items_path, scratch, input_ids, fresh_controls=99):
    views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
    views.row_factory = sqlite3.Row
    stored = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    items = sqlite3.connect(f'file:{items_path}?mode=ro', uri=True)
    scratch_archive = model.Archive(scratch)
    cited = set()
    for j in views.execute('select cited_evidence_json from judgements'):
        cited |= set(json.loads(j[0] or '[]'))
    total_cost, rows = 0.0, []
    for n, input_id in enumerate(input_ids):
        text = items.execute('select text from items where input_id=?', (input_id,)).fetchone()[0]
        probe = text[:160]
        found = [r for r in stored.execute("select request_json, answer_json from model_calls where purpose='extract' and request_json like ? order by call_id", (f'%{input_id}%',))
                 if probe.replace('\n', ' ')[:80] in json.loads(r[0])['messages'][1]['content'].replace('\n', ' ')]
        request, control = json.loads(found[0][0]), json.loads(found[0][1])
        ledger = [dict(r) for r in views.execute('select evidence_id, quote from evidence where created_from_input=?', (input_id,))]
        links = {e['evidence_id']: [r[0] for r in views.execute('select view_id from evidence_links where evidence_id=?', (e['evidence_id'],))] for e in ledger}

        def stored_id(piece):
            return next((e['evidence_id'] for e in ledger if same_piece(e, piece)), None)
        control_pieces = [dict(p, stored=stored_id(p)) for p in control.get('evidence', [])]
        for p in control_pieces:
            p['cited'] = p['stored'] in cited
            p['revenue'] = any(v in REVENUE for v in links.get(p['stored'], []))
        arm, cost = send(scratch_archive, request, ROLE_V15, 'arm')
        total_cost += cost
        arm_pieces = arm.get('evidence', [])
        kept = [p for p in control_pieces if any(same_piece(p, a) for a in arm_pieces)]
        new = [a for a in arm_pieces if not any(same_piece(a, p) for p in control_pieces)]
        fresh_n = fresh_kept_cited = 0
        if n < fresh_controls:
            fresh, cost2 = send(scratch_archive, request, None, 'fresh-control')
            total_cost += cost2
            fresh_pieces = fresh.get('evidence', [])
            fresh_n = len(fresh_pieces)
            fresh_kept_cited = sum(1 for p in control_pieces if p['cited'] and any(same_piece(p, a) for a in fresh_pieces))
        c_cited = [p for p in control_pieces if p['cited']]
        c_never = [p for p in control_pieces if not p['cited']]
        rows.append((input_id, len(control_pieces), len(c_cited), len(c_never), fresh_n, fresh_kept_cited, len(arm_pieces),
                     sum(1 for p in kept if p['cited']), sum(1 for p in kept if not p['cited']), len(new),
                     sum(1 for p in control_pieces if p['revenue']), sum(1 for a in arm_pieces if any(v in REVENUE for v in a.get('links', [])))))
        print(f'\n== {input_id}')
        for p in control_pieces:
            mark = 'KEPT' if p in kept else 'dropped'
            print(f'  control {"cited " if p["cited"] else "never "} {mark:7s} links {links.get(p["stored"], [])} | {p["one_line"][:110]}')
        for a in new:
            print(f'  arm new                 links {a.get("links")} | {a.get("one_line", "")[:110]}')
    print('\n| item | control pieces | cited | never cited | fresh control pieces | fresh kept of cited | arm pieces | arm kept of cited | arm kept of never | arm new | control on v6/v11 | arm on v6/v11 |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for r in rows:
        print('| ' + ' | '.join(str(x) for x in r) + ' |')
    t = [sum(r[i] for r in rows) for i in range(1, 12)]
    print('| **all** | ' + ' | '.join(str(x) for x in t) + ' |')
    print(f'\ntotal USD {total_cost:.4f}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])

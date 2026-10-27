"""One arm of the single-call experiment: the paused run's stored request with the cleaned text (production key order),
the system prompt replaced by a file, the closing sentence about empty arrays replaced, sent N times at low.
Run: python3 arm.py <arm name> <system file or v12> <run folder> <cleaned items db> <scratch archive> <N> <input_id...>"""
import concurrent.futures
import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(os.path.dirname(HERE), '2026-10-27-evidence-gate')
sys.path.insert(0, GATE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), 'src'))
from benchmark import send  # noqa: E402
from benchmark_clean import with_clean_text  # noqa: E402
from pinned_arm import norm  # noqa: E402
from wire_order import restore  # noqa: E402

EFFORT = os.environ.get('ARM_EFFORT', 'low')
WORKERS = int(os.environ.get('ARM_WORKERS', '8'))
T8_READ_OLD = "[What to read out] The author's opinions, arguments, forecasts, ratings and price targets, and changes to them; facts and figures the author cites, retaining their attribution."
T8_READ_NEW = "[What to read out] The author's forecasts, ratings and price targets with their figures; the facts and figures the author cites, with their original attribution. Not the author's general arguments or risk lists."

OLD_CLOSING = ' Return empty arrays when there is nothing to extract.'
NEW_CLOSING = ' Return empty arrays only for a page with no business content.'
import re as _re
MONTH = _re.compile(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b')
SKIPS = ['boilerplate', 'navigation', 'repeat', 'no_claim']


def mandatory(paragraph):
    return bool(_re.search(r'\d', paragraph) or MONTH.search(paragraph) or len(paragraph) >= 120)


def accounted(request, input_id, clean_text):
    """A3: the same single call, but the answer accounts for every mandatory paragraph (statements or a skip reason),
    with the page numbered pNNNN; evidence keeps its nine fields. Pieces are flattened back for scoring."""
    schema = request['response_format']['json_schema']['schema']
    piece = schema['properties']['evidence']['items']
    lines = [l for l in clean_text.split('\n') if l.strip()]
    ids = [f'p{i:04}' for i in range(1, len(lines) + 1)]
    numbered = '\n'.join(f'{pid} {line}' for pid, line in zip(ids, lines))
    must = [pid for pid, line in zip(ids, lines) if mandatory(line)]
    entry = {'anyOf': [
        {'type': 'object', 'properties': {'statements': {'type': 'array', 'minItems': 1, 'items': {'$ref': '#/$defs/piece'}}}, 'required': ['statements'], 'additionalProperties': False},
        {'type': 'object', 'properties': {'skip': {'type': 'string', 'enum': SKIPS}}, 'required': ['skip'], 'additionalProperties': False}]}
    paragraphs = {'type': 'object', 'properties': {pid: entry for pid in must}, 'required': must, 'additionalProperties': False}
    new_schema = {'type': 'object', '$defs': {'piece': piece}, 'properties': {'paragraphs': paragraphs, 'extra': {'type': 'array', 'items': {'$ref': '#/$defs/piece'}},
                                                   'candidates': schema['properties']['candidates'], 'new_groups': schema['properties']['new_groups']},
                  'required': ['paragraphs', 'extra', 'candidates', 'new_groups'], 'additionalProperties': False}
    request['response_format']['json_schema']['schema'] = new_schema
    user = request['messages'][1]['content']
    head = user.index('\n\n[Item] id ' + input_id + ','); header_end = user.index('\n\n', head + 12); closing = user.rindex('\n\nReturn evidence')
    account = ('\n\n[Paragraphs to account for] Every paragraph listed here gets an entry: its evidence statements, or a skip reason '
               '(boilerplate, navigation, repeat, no_claim). Statements from other paragraphs go in extra. ' + ', '.join(must))
    request['messages'][1]['content'] = user[:header_end + 2] + numbered + account + user[closing:]
    return request, len(must)


def flatten(data):
    pieces = [p for entry in (data.get('paragraphs') or {}).values() for p in entry.get('statements', [])]
    return pieces + list(data.get('extra') or [])


def main(arm, system_file, run, items_db, scratch, n, input_ids):
    from hivemind import model
    stored = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    items = sqlite3.connect(f'file:{items_db}?mode=ro', uri=True)
    archive = model.Archive(scratch)
    system = open(system_file, encoding='utf-8').read() if system_file != 'v12' else None
    total = 0.0
    print(f'arm {arm}: system {"v12 unchanged" if system is None else f"{system_file} ({len(system)} chars)"}; closing sentence {"unchanged" if system is None else "replaced"}')
    print('| article | pieces per sample | empty | reasoning tokens | distinct | in every sample | links used | seconds |')
    print('|---|---|---|---|---|---|---|---|')
    prepared = {}
    for input_id in input_ids:
        req, = stored.execute("select request_json from model_calls where purpose='extract' and request_json like ? order by call_id limit 1", (f'%[Item] id {input_id},%',)).fetchone()
        request = restore(json.loads(req))
        clean, = items.execute('select text from items where input_id=?', (input_id,)).fetchone()
        request = with_clean_text(request, input_id, clean)
        if system is not None:
            request['messages'][0]['content'] = system
            user = request['messages'][1]['content']
            assert OLD_CLOSING in user
            request['messages'][1]['content'] = user.replace(OLD_CLOSING, NEW_CLOSING)
        if 'B3' in arm or 'B4' in arm or 'B5' in arm or 'B6' in arm or 'B7' in arm:
            request['messages'][1]['content'] = request['messages'][1]['content'].replace(T8_READ_OLD, T8_READ_NEW)
        if 'A2' in arm or 'A3' in arm:
            user = request['messages'][1]['content']
            request['messages'][1]['content'] = _re.sub(r' — members: [^\n]*', '', user)   # groups shown by name, scope and aliases only
        if 'A3' in arm:
            request, must = accounted(request, input_id, clean)
            print(f'  {input_id}: {must} mandatory paragraphs')
        prepared[input_id] = request
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {(input_id, i): pool.submit(send, archive, prepared[input_id], EFFORT, purpose=f'arm:{arm}') for input_id in input_ids for i in range(n)}
        results = {key: future.result() for key, future in futures.items()}
    for input_id in input_ids:
        counts, reasons, secs, sets, links = [], [], [], [], set()
        for i in range(n):
            pieces, reasoning, cost, seconds = results[(input_id, i)]
            if 'A3' in arm:
                pieces = flatten(pieces)
            total += cost
            counts.append(len(pieces)); reasons.append(reasoning); secs.append(seconds)
            sets.append({norm(p['quote'])[:80] for p in pieces}); links |= {l for p in pieces for l in p['links']}
        union = set().union(*sets); common = set.intersection(*sets) if sets else set()
        print(f'| {input_id} | {counts} | {sum(1 for c in counts if c == 0)} | {reasons} | {len(union)} | {len(common)} | {sorted(links)} | {secs} |')
    print(f'\ntotal USD {total:.4f}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], int(sys.argv[6]), sys.argv[7:])

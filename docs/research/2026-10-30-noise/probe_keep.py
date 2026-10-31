"""The model's own account of a kept statement (AGENTS §1, before any design): continue the stored extraction conversation of one draw
in which the statement was kept on its own (not inside the quote of a matter the gold keeps) with one question: which sentence of the
request made it keep the item through the closing check, and which line of the check it weighed for dropping it. The request is rebuilt
on the product's path (bench_v23.build) and must hash to the stored request before anything is sent. Replies go to probes/.

    python3 probe_keep.py Y3 v63 poc/config/poc-v79.json S003 S013 ...     (ids from agreed-noise-Y3-v63.json)
"""
import concurrent.futures
import copy
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LEDGER = HERE.parent / '2026-10-29-ledger-standard'
LOOP = HERE.parent / '2026-10-29-analyst-standard'
sys.path[:0] = [str(ROOT / 'src'), str(LOOP), str(LEDGER), str(LEDGER / 'final-2026-10-30')]
import bench_v23 as bench  # noqa: E402
import final_scores as fs  # noqa: E402
import score_gold as sg  # noqa: E402
from hivemind import model  # noqa: E402

QUESTION = ('Your answer kept this evidence item ({eid}): "{quote}". Quote the exact sentence of the request that made you keep it '
            'through the check at the end of the request. Then quote the line of that check you weighed for dropping it, if any, and say '
            'in one sentence why you kept it anyway.')


def stored(prefix, version, draw, input_id):
    db = sqlite3.connect(f'file:{LOOP / "loop-2026-10-29" / f"{prefix}-{version}-d{draw}" / "answers.sqlite"}?mode=ro', uri=True)
    return db.execute('select config, request_sha256, content from answers where input_id=?', (input_id,)).fetchone()


def probe(prefix, version, config_path, entry, articles):
    a = articles[entry['input_id']]
    kept_gold = [i for i in a['items'] if i['weight'] in ('core', 'supporting', 'optional')]
    for draw in entry['draws']:
        config, request_sha, content = stored(prefix, version, draw, entry['input_id'])
        s = sg.kept((content, 1, config), entry['input_id'])
        own = [e for e in s['evidence'] if sg.same(entry['span'], e['quote']) and not any(sg.same_matter(k, e) for k in kept_gold)]
        if own:
            break
    else:
        return entry['sid'], 'carried in every draw: not probed'
    *_, request, cfg = bench.build(entry['input_id'], config_path)
    if model.request_identity(request)[1] != request_sha:
        return entry['sid'], 'REQUEST MISMATCH: not sent'
    body = copy.deepcopy(request)
    body.pop('response_format', None)
    body['messages'] = body['messages'] + [{'role': 'assistant', 'content': content},
                                           {'role': 'user', 'content': QUESTION.format(eid=own[0].get('id', ''), quote=own[0]['quote'])}]
    response = model.openai_transport(cfg.provider, body)
    reply = response['choices'][0]['message'].get('content') or ''
    usage = response.get('usage', {})
    (HERE / 'probes' / f'{version}-keep-{entry["sid"]}.txt').write_text(
        f'{entry["input_id"]} draw {draw}\nspan: {entry["span"]}\nkept quote: {own[0]["quote"]}\n\n{reply}\n')
    return entry['sid'], f'ok in {usage.get("prompt_tokens")} out {usage.get("completion_tokens")}'


if __name__ == '__main__':
    prefix, version, config_path, rest = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    source = HERE / rest.pop(0) if rest and rest[0].endswith('.json') else HERE / f'agreed-noise-{prefix}-{version}.json'   # another entries file
    ids = set(rest)
    articles = {a['input_id']: a for name in ('dev', 'test') for a in json.loads(Path(fs.GOLDS[name]).read_text())['articles']}
    entries = [e for e in json.loads(source.read_text()) if e['sid'] in ids]
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for sid, status in pool.map(lambda e: probe(prefix, version, str(ROOT / config_path), e, articles), entries):
            print(sid, status, flush=True)

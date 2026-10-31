"""The model's own account of a dropped gold entry: continue the stored extraction conversation of one draw in which no kept statement
matches a core or supporting gold entry (score_gold.same_matter) with one question: which line of the closing check, or which other
sentence of the request, made it leave the statement out. The request is rebuilt on the product's path and must hash to the stored one.

    python3 probe_drop.py Y4 v64 poc/config/poc-v80.json "<input_id>|<first 40 characters of the gold span>" ...
"""
import concurrent.futures
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import probe_keep as pk  # noqa: E402  (stored(), bench, model, final_scores, score_gold)

QUESTION = ('Your answer did not include this statement from the item: "{span}". Quote the exact line of the check at the end of the '
            'request, or the other sentence of the request, that made you leave it out, and say in one sentence why. If you left it '
            'out by oversight, say so.')


def probe(prefix, version, config_path, iid, span_start, articles):
    item = next((i for i in articles[iid]['items'] if span_start in i['span']), None)
    if item is None:
        return iid, f'no kept gold entry contains {span_start!r}'
    for draw in (1, 2, 3):
        config, request_sha, content = pk.stored(prefix, version, draw, iid)
        s = pk.sg.kept((content, 1, config), iid)
        if s is not None and not any(pk.sg.same_matter(item, e) for e in s['evidence']):
            break
    else:
        return iid, 'kept in every draw: not probed'
    *_, request, cfg = pk.bench.build(iid, config_path)
    if pk.model.request_identity(request)[1] != request_sha:
        return iid, 'REQUEST MISMATCH: not sent'
    body = copy.deepcopy(request)
    body.pop('response_format', None)
    body['messages'] = body['messages'] + [{'role': 'assistant', 'content': content}, {'role': 'user', 'content': QUESTION.format(span=item['span'])}]
    reply = pk.model.openai_transport(cfg.provider, body)['choices'][0]['message'].get('content') or ''
    name = f'{version}-drop-{iid.split(":")[-1][:12]}-{abs(hash(span_start)) % 1000:03d}.txt'
    (HERE / 'probes' / name).write_text(f'{iid} draw {draw} ({len(s["evidence"])} items kept)\ngold ({item["weight"]}): {item["span"]}\n\n{reply}\n')
    return iid, f'ok -> probes/{name}'


if __name__ == '__main__':
    prefix, version, config_path, pairs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    articles = {a['input_id']: a for a in json.loads(Path(pk.fs.GOLDS['dev']).read_text())['articles']}
    jobs = [p.split('|', 1) for p in pairs]
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for iid, status in pool.map(lambda j: probe(prefix, version, str(pk.ROOT / config_path), j[0], j[1], articles), jobs):
            print(iid, status, flush=True)

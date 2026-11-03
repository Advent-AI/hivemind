"""Is extraction a loud sampler? The identical stored request (byte for byte) sent N times at reasoning_effort low (the run's
setting) and N times at medium, per article; per sample the piece count and reasoning tokens; across samples the overlap of the
pieces (a piece is the same when its quote is the same text). Run: python3 benchmark.py <run folder> <scratch archive> <N> <input_id...>"""
import json
import os
import sqlite3
import sys
import time
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pinned_arm import norm  # noqa: E402
from wire_order import restore  # noqa: E402  (the archive is alphabetised; send the production order)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import model  # noqa: E402


def send(archive, request, effort, purpose=None):
    request = json.loads(json.dumps(request))
    request['reasoning_effort'] = effort
    started = time.time()
    response = model.openai_transport('openai', request)
    data = json.loads(response['choices'][0]['message']['content'])
    usage = response.get('usage') or {}
    tin, tout = int(usage.get('prompt_tokens') or 0), int(usage.get('completion_tokens') or 0)
    reasoning = int((usage.get('completion_tokens_details') or {}).get('reasoning_tokens') or 0)
    cached = min(tin, int((usage.get('prompt_tokens_details') or {}).get('cached_tokens') or 0))
    pin, pout = model.PRICES[request['model']]
    cost = round((tin - cached) / 1e6 * pin + cached / 1e6 * pin * model.CACHED_INPUT_SHARE + tout / 1e6 * pout, 6)
    archive.record(purpose=purpose or f'benchmark:{effort}', config_version='poc-v29', config_checksum='benchmark', model=request['model'],
                   request_sha256=model.request_identity(request)[1] + ':' + uuid.uuid4().hex[:6], request_json=json.dumps(request),
                   response_json=json.dumps(response)[:200000], answer_json=json.dumps(data, ensure_ascii=False), prompt_chars=sum(len(m['content']) for m in request['messages']),
                   input_tokens=tin, output_tokens=tout, cost_usd=cost, seconds=round(time.time() - started, 1), created_at=time.strftime('%Y-%m-%dT%H:%M:%S'))
    return (data.get('evidence') if 'evidence' in data else data), reasoning, cost, round(time.time() - started, 1)


def main(run, scratch, n, input_ids):
    stored = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    archive = model.Archive(scratch)
    total = 0.0
    print('| article | effort | pieces per sample | reasoning tokens per sample | distinct pieces over samples | pieces in every sample | seconds |')
    print('|---|---|---|---|---|---|---|')
    for input_id in input_ids:
        req, = stored.execute("select request_json from model_calls where purpose='extract' and request_json like ? order by call_id limit 1", (f'%[Item] id {input_id},%',)).fetchone()
        request = restore(json.loads(req))
        for effort in ('low', 'medium'):
            counts, reasons, secs, sets = [], [], [], []
            for _ in range(n):
                pieces, reasoning, cost, seconds = send(archive, request, effort)
                total += cost
                counts.append(len(pieces)); reasons.append(reasoning); secs.append(seconds)
                sets.append({norm(p['quote'])[:120] for p in pieces})
            union = set().union(*sets); common = set.intersection(*sets) if sets else set()
            print(f'| {input_id} | {effort} | {counts} | {reasons} | {len(union)} | {len(common)} | {secs} |')
    print(f'\ntotal USD {total:.4f}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4:])

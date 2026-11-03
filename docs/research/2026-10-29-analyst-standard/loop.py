"""The direct-read loop (Alex 2026-10-29: read each article and its answer directly, change the prompt by principle, test fast):
one send per article on a named configuration, then a reading packet of the article's answer beside another run's answer.
No score: the packet is for reading.

    python3 loop.py send <tag> <config> [input_id ...]        # every bench article when no id is named
    python3 loop.py packet <tag> <other-tag|v23> <out.md> [--text] [input_id ...]
    python3 loop.py probe <tag> <input_id> <question>          # the model's own account: the stored conversation continued
"""
import concurrent.futures
import copy
import json
from pathlib import Path
import sqlite3
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bench_v23 as bench  # noqa: E402
import haiku_week as hw  # noqa: E402
from hivemind import model  # noqa: E402

RUNS = HERE / 'loop-2026-10-29'


def store(tag):
    (RUNS / tag).mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(RUNS / tag / 'answers.sqlite')
    conn.execute('create table if not exists answers (input_id text primary key, config text, request_sha256 text, response_json text, content text,'
                 ' completed integer, input_tokens integer, output_tokens integer, seconds real, error text)')
    return conn


def manifest():
    return {e['input_id']: e for e in json.loads((hw.RUN / 'manifest.json').read_text())['items']}


def send(tag, config_path, ids):
    ids = ids or list(manifest())
    conn = store(tag)
    done = {r[0] for r in conn.execute('select input_id from answers where completed=1')}
    conn.close()
    jobs = [i for i in ids if i not in done]
    print('sending', len(jobs), 'on', config_path, flush=True)

    def one(input_id):
        item, uni, setting, schema, req, cfg = bench.build(input_id, config_path)
        start = time.monotonic()
        response, content, completed, error, tin, tout = None, None, 0, None, None, None
        try:
            response = model.openai_transport(cfg.provider, req)      # the bytes production sends under this configuration
            choice = response['choices'][0]
            completed = int(choice['finish_reason'] == 'stop')
            content = choice['message'].get('content') or ''
            tin, tout = response.get('usage', {}).get('prompt_tokens'), response.get('usage', {}).get('completion_tokens')
        except Exception as exc:  # noqa: BLE001
            error = type(exc).__name__
        with hw.LOCK:
            c = store(tag)
            c.execute('insert or replace into answers values (?,?,?,?,?,?,?,?,?,?)', (input_id, config_path, model.request_identity(req)[1], json.dumps(response),
                                                                                     content, completed, tin, tout, round(time.monotonic() - start, 2), error))
            c.commit()
            c.close()
        print(input_id[:30], 'ok' if completed else f'INCOMPLETE {error}', flush=True)

    with concurrent.futures.ThreadPoolExecutor(hw.WORKERS) as pool:
        list(pool.map(one, jobs))
    print(store(tag).execute('select count(*), sum(completed), sum(input_tokens), sum(output_tokens) from answers').fetchone())


def answers(tag):
    """input_id -> (content, completed, config) for a loop run, or draw 1 of the v23 bench."""
    if tag == 'v23':
        db = sqlite3.connect(f'file:{bench.RUN / "answers.sqlite"}?mode=ro', uri=True)
        return {i: (c, d, bench.CONFIG) for i, c, d in db.execute('select input_id, content, completed from answers where draw=1')}
    db = sqlite3.connect(f'file:{RUNS / tag / "answers.sqlite"}?mode=ro', uri=True)
    return {i: (c, d, cfg) for i, c, d, cfg in db.execute('select input_id, content, completed, config from answers')}


def render(input_id, row):
    if row is None:
        return ['(not sent)']
    content, completed, config_path = row
    answer = json.loads(content) if content else None
    rec = bench.sift_answer(answer, completed, input_id, config_path)
    if not rec['completed'] or rec['schema_errors']:
        return [f"(incomplete or schema error: {rec['schema_errors']})"]
    dropped = dict(rec['sift']['dropped'])
    lines = []
    for e in answer['evidence']:
        mark = f' DROPPED:{dropped[e["id"]]}' if e['id'] in dropped else ''
        lines.append(f"{e['id']} [{e['tier']}] who={e['original_who'] or e['speaker']}{mark} | {e['one_line']}")
    for c in answer['candidates']:
        mark = f' DROPPED:{dropped[c["id"]]}' if c['id'] in dropped else ''
        lines.append(f"Q {c['id']} {c.get('opens_as')}/{c.get('measure')} due {c.get('due_day')}{mark} | {c['question']}")
    return lines or ['(empty answer)']


def packet(tag, other, out, with_text, ids):
    m = manifest()
    ids = ids or list(m)
    mine, theirs = answers(tag), answers(other)
    db = sqlite3.connect(f'file:{hw.ITEMS}?mode=ro', uri=True)
    parts = []
    for input_id in ids:
        title, text = db.execute('select title, text from items where input_id=?', (input_id,)).fetchone()
        e = m[input_id]
        parts.append(f"######## call {e['call_id']} · {input_id} · {e['category']} · {e['day']} · {title}")
        if with_text:
            parts += ['--- TEXT ---', text]
        parts += [f'--- {other} ---'] + render(input_id, theirs.get(input_id)) + [f'--- {tag} ---'] + render(input_id, mine.get(input_id)) + ['']
    Path(out).write_text('\n'.join(parts) + '\n')
    print('wrote', out, len(ids), 'articles')


def probe(tag, input_id, question):
    """Continue the stored conversation of one loop answer with one question (AGENTS section 1); prose reply, 3000 tokens."""
    content, completed, config_path = answers(tag)[input_id]
    item, uni, setting, schema, req, cfg = bench.build(input_id, config_path)
    db = sqlite3.connect(f'file:{RUNS / tag / "answers.sqlite"}?mode=ro', uri=True)
    assert db.execute('select request_sha256 from answers where input_id=?', (input_id,)).fetchone()[0] == model.request_identity(req)[1]
    body = copy.deepcopy(req)
    del body['response_format']
    body['max_completion_tokens'] = 3000
    body['messages'] = req['messages'] + [{'role': 'assistant', 'content': content}, {'role': 'user', 'content': question}]
    response = model.openai_transport(cfg.provider, body)
    reply = response['choices'][0]['message'].get('content')
    conn = sqlite3.connect(RUNS / tag / 'probes.sqlite')
    conn.execute('create table if not exists probes (input_id text, question text, reply text, response_json text, at real)')
    conn.execute('insert into probes values (?,?,?,?,?)', (input_id, question, reply, json.dumps(response), time.time()))
    conn.commit()
    print(reply)


if __name__ == '__main__':
    if sys.argv[1] == 'probe':
        probe(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'send':
        send(sys.argv[2], sys.argv[3], sys.argv[4:])
    else:
        rest = sys.argv[5:]
        with_text = '--text' in rest
        packet(sys.argv[2], sys.argv[3], sys.argv[4], with_text, [a for a in rest if a != '--text'])

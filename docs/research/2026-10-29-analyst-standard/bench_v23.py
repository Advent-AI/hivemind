"""The test bench on the scrubbed extraction request (D237): poc-v39 (role-v23, categories-v23) built on the product's own path
(extraction.request_for), gpt-6-luna, the week's 98 articles and the 20-article holdout, three draws; the production sift of the
current code (D236 quote rule). The baseline is the stored role-v22 (poc-v38) gpt-6-luna answers of haiku_week.py re-sifted
with the same code.

    python3 bench_v23.py plan | send | sift
"""
import concurrent.futures
import json
from pathlib import Path
import sqlite3
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import haiku_week as hw  # noqa: E402
from hivemind import config, extraction, model, universe  # noqa: E402

RUN = HERE / 'bench-v23-2026-10-29'
CONFIG = str(hw.ROOT / 'poc/config/poc-v39.json')
DRAWS = 3


def build(input_id, config_path=CONFIG):
    db = sqlite3.connect(f'file:{hw.ITEMS}?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    item = dict(db.execute('select * from items where input_id=?', (input_id,)).fetchone())
    item['object_identifiers'] = json.loads(item['object_identifiers'])
    cfg = config.load(config_path)
    uni = universe.load(str(hw.ROOT / 'poc/universe.json'))
    setting, system, user, schema = extraction.request_for(cfg, item, item['text'], [], uni, [])
    return item, uni, setting, schema, model.build_request(setting, system, user, schema, 'extraction', cfg.provider), cfg


def items():
    return [e['input_id'] for e in json.loads((hw.RUN / 'manifest.json').read_text())['items']]


def plan():
    sizes = []
    for input_id in items():
        _, _, setting, schema, new, _ = build(input_id)
        old = hw.build(input_id)[4]
        assert setting.prompt_version.endswith('-v23') and new['model'] == old['model']
        assert {k: v for k, v in new.items() if k != 'messages'} == {k: v for k, v in old.items() if k != 'messages'}   # same model, settings, schema
        sizes.append((len(old['messages'][0]['content']), len(new['messages'][0]['content'])))
    print('items', len(sizes), '| system characters v22 -> v23', sizes[0], '| calls', DRAWS * len(sizes))


def store():
    RUN.mkdir(exist_ok=True)
    conn = sqlite3.connect(RUN / 'answers.sqlite')
    conn.execute('create table if not exists answers (draw integer, input_id text, request_sha256 text, response_json text, content text,'
                 ' completed integer, input_tokens integer, output_tokens integer, seconds real, error text, primary key (draw, input_id))')
    return conn


def one(job):
    draw, input_id = job
    item, uni, setting, schema, req, cfg = build(input_id)
    start = time.monotonic()
    response, content, completed, error, tin, tout = None, None, 0, None, None, None
    try:
        response = model.openai_transport(cfg.provider, req)      # the bytes production sends under poc-v39
        choice = response['choices'][0]
        completed = int(choice['finish_reason'] == 'stop')
        content = choice['message'].get('content') or ''
        tin, tout = response.get('usage', {}).get('prompt_tokens'), response.get('usage', {}).get('completion_tokens')
    except Exception as exc:  # noqa: BLE001
        error = type(exc).__name__
    with hw.LOCK:
        conn = store()
        conn.execute('insert or replace into answers values (?,?,?,?,?,?,?,?,?,?)', (draw, input_id, model.request_identity(req)[1], json.dumps(response),
                                                                                  content, completed, tin, tout, round(time.monotonic() - start, 2), error))
        conn.commit()
        conn.close()
    print(draw, input_id[:30], 'ok' if completed else f'INCOMPLETE {error}', flush=True)


def send():
    conn = store()
    done = {tuple(r) for r in conn.execute('select draw, input_id from answers where completed=1')}
    conn.close()
    jobs = [(d, i) for i in items() for d in range(1, DRAWS + 1) if (d, i) not in done]
    print('sending', len(jobs), flush=True)
    with concurrent.futures.ThreadPoolExecutor(hw.WORKERS) as pool:
        list(pool.map(one, jobs))
    conn = store()
    print(conn.execute('select count(*), sum(completed), sum(input_tokens), sum(output_tokens) from answers').fetchone())


def sift_answer(answer, completed, input_id, config_path):
    item, uni, setting, schema, req, cfg = build(input_id, config_path)
    rec = {'completed': bool(completed), 'error': None, 'answer': answer, 'schema_errors': None, 'sift': None}
    if answer is not None:
        rec['schema_errors'] = model.check_schema(answer, schema)
        if completed and not rec['schema_errors']:
            version = setting.prompt_version.rpartition('-')[2]
            e, c, d, g = extraction.sift_with_groups(answer, item, item['text'], set(), uni, english=True, shown_group_ids=(),
                                                     version=version, keep_unlinked=extraction.places(version))
            rec['sift'] = {'evidence': e, 'candidates': c, 'dropped': d, 'new_groups': g}
    return rec


def sift():
    """bench sifted.json: luna-1..3 = the stored role-v22 answers re-sifted with the current code; v23-1..3 = this bench."""
    out = {}
    base = sqlite3.connect(f'file:{hw.RUN / "answers.sqlite"}?mode=ro', uri=True)
    for draw, input_id, content, completed in base.execute("select draw, input_id, content, completed from answers where provider='luna'"):
        answer = json.loads(content) if content else None
        out.setdefault(f'luna-{draw}', {})[input_id] = sift_answer(answer, completed, input_id, str(hw.ROOT / 'poc/config/poc-v38.json'))
    for draw, input_id, content, completed in store().execute('select draw, input_id, content, completed from answers'):
        answer = json.loads(content) if content else None
        out.setdefault(f'v23-{draw}', {})[input_id] = sift_answer(answer, completed, input_id, CONFIG)
    (RUN / 'sifted.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print('sifted', {k: len(v) for k, v in out.items()})


if __name__ == '__main__':
    {'plan': plan, 'send': send, 'sift': sift}[sys.argv[1]]()

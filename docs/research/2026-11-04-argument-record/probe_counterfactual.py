"""The cheapest proof of a mechanism (AGENTS §1.4): re-send a stored judging-v8 request as stored and with one edit per arm, each
`sends` times, and compare the rungs. The request is rebuilt as production sends it: the stored system and user texts, the schema from
the code (`judging.schema_for`, its key order as built) and `model.build_request`; the probe refuses to send unless the rebuilt request's
archive key equals the stored one. Sends run eight at a time.

The spec (JSON): {"run": <run folder>, "case": "<view_id>:<day>", "sends": 3, "config": <config path, default poc-v109>,
                  "version": <judging prompt version, default judging-v8>,
                  "arms": {"<name>": [["<old text>", "<new text>"], ...], ...},
                  "insert_after": {"<name>": ["<header line start>", ["<line>", ...]]},   (optional: lines added after a block header)
                  "swap": {"<name>": {"system_from": [<run>, "<view_id>:<day>"], "version": "<judging version>"}}}   (optional: another
                  stored system text and that version's schema on this request's material)
Every old text must occur exactly once in the stored request.

usage: python3 probe_counterfactual.py <spec.json> <out.json>
"""
import concurrent.futures
import json
import sqlite3
import sys

sys.path.insert(0, '/Users/lchingen/hivemind/src')
from hivemind import config, model  # noqa: E402
from hivemind.views import judging  # noqa: E402


def edited(user, replacements, insertion):
    for old, new in replacements:
        if user.count(old) != 1:
            raise SystemExit(f'the text to replace occurs {user.count(old)} times: {old[:80]!r}')
        user = user.replace(old, new)
    if insertion:
        header, lines = insertion
        rows = user.split('\n')
        at = [i for i, row in enumerate(rows) if row.startswith(header)]
        if len(at) != 1:
            raise SystemExit(f'the header occurs {len(at)} times: {header!r}')
        user = '\n'.join(rows[:at[0] + 1] + lines + rows[at[0] + 1:])
    return user


def main():
    spec = json.load(open(sys.argv[1], encoding='utf-8'))
    out = sys.argv[2]
    cfg = config.load(spec.get('config', '/Users/lchingen/hivemind/poc/config/poc-v109.json'))
    view_id, day = spec['case'].split(':')
    views = sqlite3.connect(f'file:{spec["run"]}/views.sqlite?mode=ro', uri=True)
    archive = sqlite3.connect(f'file:{spec["run"]}/archive.sqlite?mode=ro', uri=True)
    sha, stored_rung = views.execute('select request_sha256, rung from judgements where view_id=? and publication_day=?', (view_id, day)).fetchone()
    stored = json.loads(archive.execute('select request_json from model_calls where request_sha256=?', (sha,)).fetchone()[0])
    system = next(m['content'] for m in stored['messages'] if m['role'] == 'system')
    user = next(m['content'] for m in stored['messages'] if m['role'] == 'user')
    schema = judging.schema_for(spec.get('version', 'judging-v8'))
    if model.request_identity(model.build_request(cfg.rejudging, system, user, schema, 'judgement', cfg.provider))[1] != sha:
        raise SystemExit('the rebuilt request does not match the stored one; refusing to send')
    arms = {'as_stored': user}
    for name, replacements in spec['arms'].items():
        arms[name] = edited(user, replacements, spec.get('insert_after', {}).get(name))
    for name in spec.get('insert_after', {}):
        if name not in arms:
            arms[name] = edited(user, [], spec['insert_after'][name])

    systems, schemas = {name: system for name in arms}, {name: schema for name in arms}
    for name, swap in spec.get('swap', {}).items():   # {arm: {"system_from": [run, "<view_id>:<day>"], "version": v}}: another prompt on this material
        other_run, other_case = swap['system_from']
        other_view, other_day = other_case.split(':')
        other_views = sqlite3.connect(f'file:{other_run}/views.sqlite?mode=ro', uri=True)
        other_archive = sqlite3.connect(f'file:{other_run}/archive.sqlite?mode=ro', uri=True)
        other_sha = other_views.execute('select request_sha256 from judgements where view_id=? and publication_day=?', (other_view, other_day)).fetchone()[0]
        other = json.loads(other_archive.execute('select request_json from model_calls where request_sha256=?', (other_sha,)).fetchone()[0])
        arms.setdefault(name, user)
        systems[name] = next(m['content'] for m in other['messages'] if m['role'] == 'system')
        schemas[name] = judging.schema_for(swap['version'])

    def send(name):
        request = model.build_request(cfg.rejudging, systems[name], arms[name], schemas[name], 'judgement', cfg.provider)
        answer = json.loads(model.openai_transport(cfg.provider, request)['choices'][0]['message']['content'])
        return name, answer['rung'], answer['implied_outcome']

    if spec.get('skip_as_stored'):
        arms.pop('as_stored')
    jobs = [name for name in arms for _ in range(spec.get('sends', 3))]
    results = {'case': spec['case'], 'stored_rung': stored_rung, 'characters': {n: len(t) for n, t in arms.items()}, 'answers': {n: [] for n in arms}}
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for name, rung, implied in pool.map(send, jobs):
            results['answers'][name].append({'rung': rung, 'implied_outcome': implied})
    for name, answers in results['answers'].items():
        print(f'{spec["case"]} {name:12} rungs {[a["rung"] for a in answers]} | {answers[0]["implied_outcome"][:150]}')
    json.dump(results, open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()

"""T1 and T1b of the citation-only judge's $0 test (DESIGN.md §5, registered before it runs; D713).

T1: old-2's whole window replayed under poc-v121 (judging-v12) through `replay.run`. The scratch archive holds old-2's non-judge calls
only, so every judge request reaches this transport and the real `model.call` / `model.check_schema`. The transport finds old-2's call by
the request's system and user bytes, asserts that the request equals the stored one in every key but the answer format, that the format
is strict, named `judgement`, and differs from judging-v7's only in the four citation constraints, and that each closed list equals the
ids the request text shows. The four first answers old-2's check refused get old-2's accepted retry answer, labelled. Then the store is
compared with old-2's on every table, the expected differences named.

T1b: each of those four refused originals through the real `model.call` under its v12 request must raise SchemaError on its bad id.

  python3 t1_replay.py <new output folder>
"""
import copy
import json
import re
import sqlite3
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / 'src'))
from hivemind import config, live_lock, model, replay, universe        # noqa: E402
from hivemind.views import judging                                     # noqa: E402

OLD2 = REPO / 'poc/data/comparison-2026-11-17/run/old-2/prod'
ITEMS = REPO / 'poc/data/comparison-2026-11-17/items-comparison.sqlite'
UNIVERSE = REPO / 'poc/universe.json'
V121 = REPO / 'poc/config/poc-v121.json'
WINDOW = ('2026-07-01', '2026-09-20')
RETRY_MARK = '\n\nThe code returned the previous answer because: '
EXPECTED_JUDGE_RESPONSES, EXPECTED_SUBSTITUTIONS = 1616, 4
# columns that differ by construction: timestamps, the new judge calls' archive ids and request hashes, the configuration's checksum
EXPECTED_DIFFERENT = {'days_completed': {'at'}, 'processing_steps': {'at'}, 'views': {'created_at'},
                      'judgements': {'call_id', 'request_sha256', 'config_checksum'}}
# the current store schema's additions since old-2 ran (D694's linking build, uncommitted): a table and a column, both empty here
NEW_TABLES = {'harness_only', 'link_selections'}
NEW_COLUMNS = {'dependencies': {'kind'}}


class Stop(Exception):
    pass


def opened(schema):
    """The format with its four citation constraints removed: judging-v7's format if nothing else differs."""
    schema = copy.deepcopy(schema)
    schema.pop('$defs', None)
    properties = schema['properties']
    for field in ('cites', 'cites_views', 'pushes', 'theme_pushes'):
        properties[field].pop('maxItems', None)
    properties['cites']['items'] = {'type': 'string'}
    properties['cites_views']['items'] = {'type': 'string'}
    properties['pushes']['items']['properties']['evidence_id'] = {'type': 'string'}
    properties['theme_pushes']['items']['properties']['view_id'] = {'type': 'string'}
    return schema


def closed_lists(schema):
    """The ids each field allows (an array with maxItems 0 allows none)."""
    properties, defs = schema['properties'], schema.get('$defs', {})

    def ids(array, item_path):
        if array.get('maxItems') == 0:
            return []
        node = array['items']
        for key in item_path:
            node = node['properties'][key]
        node = defs[node['$ref'].rsplit('/', 1)[1]] if '$ref' in node else node
        return sorted(node['enum'])
    evidence = ids(properties['cites'], ())
    if evidence != ids(properties['pushes'], ('evidence_id',)):
        raise Stop('cites and push ids allow different evidence ids')
    return {'evidence': evidence, 'dependencies': ids(properties['cites_views'], ()), 'themes': ids(properties['theme_pushes'], ('view_id',))}


def dependencies_shown_in(user):
    block = user.split('\n[Current conclusions of the theses it depends on]', 1)
    return set(re.findall(r'^- (v\d+) \(', block[1].split('\n\n[', 1)[0], re.M)) if len(block) == 2 else set()


def stored_judge_calls():
    """old-2's judge calls by (system, user): each a list of rows, the refused first answers included."""
    archive = sqlite3.connect(f'file:{OLD2 / "archive.sqlite"}?mode=ro', uri=True)
    calls = {}
    for call_id, sha, request_json, answer_json, tokens_in, tokens_out in archive.execute(
            "select call_id, request_sha256, request_json, answer_json, input_tokens, output_tokens from model_calls where purpose='judge' order by call_id"):
        request = json.loads(request_json)
        key = (request['messages'][0]['content'], request['messages'][1]['content'])
        calls.setdefault(key, []).append({'call_id': call_id, 'refused': ':refused:' in sha, 'request': request, 'answer': answer_json,
                                          'usage': {'prompt_tokens': tokens_in or 0, 'completion_tokens': tokens_out or 0}})
    return calls


def compare_stores(built_path):
    built = sqlite3.connect(f'file:{built_path}?mode=ro', uri=True)
    stored = sqlite3.connect(f'file:{OLD2 / "views.sqlite"}?mode=ro', uri=True)
    tables = lambda conn: {r[0] for r in conn.execute("select name from sqlite_master where type='table'")}
    report, ok = {}, True
    extra = tables(built) - tables(stored)
    if extra - NEW_TABLES or tables(stored) - tables(built):
        ok = False
    report['tables only in the replay'] = sorted(extra)
    report['tables only in old-2'] = sorted(tables(stored) - tables(built))
    for name in sorted(extra & NEW_TABLES - {'harness_only'}):
        rows = built.execute(f'select count(*) from "{name}"').fetchone()[0]
        report[f'{name} (new table) rows'] = rows
        ok = ok and rows == 0
    for name in sorted(tables(stored) & tables(built)):
        columns = [r[1] for r in stored.execute(f'pragma table_info("{name}")')]
        built_columns = [r[1] for r in built.execute(f'pragma table_info("{name}")')]
        if columns != built_columns:
            added = [c for c in built_columns if c not in columns]
            expected = built_columns[:len(columns)] == columns and set(added) == NEW_COLUMNS.get(name, set())
            empty = built.execute(f'select count(*) from "{name}"').fetchone()[0] == 0
            if not (expected and empty):
                report[name] = f'columns differ: {added}'
                ok = False
                continue
        kept = [c for c in columns if c not in EXPECTED_DIFFERENT.get(name, set())]
        select = f'select {", ".join(chr(34) + c + chr(34) for c in kept)} from "{name}"'      # some FTS tables have no rowid: compare as sorted rows
        rows_built, rows_stored = sorted(built.execute(select), key=repr), sorted(stored.execute(select), key=repr)
        equal = rows_built == rows_stored
        report[name] = {'rows': len(rows_stored), 'equal': equal, 'columns not compared': sorted(EXPECTED_DIFFERENT.get(name, set()))}
        if not equal:
            ok = False
            report[name]['first difference'] = next((str((b, s))[:400] for b, s in zip(rows_built, rows_stored) if b != s), f'{len(rows_built)} rows against {len(rows_stored)}')
    return ok, report


def t1(folder):
    if folder.exists():
        raise SystemExit(f'{folder} exists: T1 starts from an empty folder')
    folder.mkdir(parents=True)
    archive_path, views = folder / 'archive.sqlite', folder / 'views.sqlite'
    seed = sqlite3.connect(f'file:{OLD2 / "archive.sqlite"}?mode=ro', uri=True)
    target = sqlite3.connect(str(archive_path))
    seed.backup(target)
    seed.close()
    removed = target.execute("delete from model_calls where purpose='judge'").rowcount
    target.commit()
    target.close()
    marker = sqlite3.connect(views)
    marker.execute('create table harness_only (name text, day text)')
    marker.execute("insert into harness_only values ('t1_replay.py', '2026-11-21')")
    marker.commit()
    marker.close()
    v7_format = judging.schema_for('judging-v7')
    stored = stored_judge_calls()
    lock = threading.Lock()
    log = {'responses': 0, 'substitutions': [], 'problems': [], 'list mismatches': [], 'sizes': [], 'outgoing for refused originals': {}}

    def transport(*args):
        if len(args) == 1:
            raise Stop('a Jev request missed the seeded archive')
        provider, request = args
        if (request.get('response_format') or {}).get('json_schema', {}).get('name') != 'judgement':
            (folder / 'missed-request.json').write_text(json.dumps(request, ensure_ascii=False, indent=1))
            raise Stop('a non-judge request missed the seeded archive')
        system, user = request['messages'][0]['content'], request['messages'][1]['content']
        rows = stored.get((system, user))
        if not rows:
            raise Stop(f'no stored old-2 judge call for this text ({user[:80]!r})')
        problems = []
        first = rows[0]
        outgoing_rest = {k: v for k, v in request.items() if k != 'response_format'}
        stored_rest = {k: v for k, v in first['request'].items() if k != 'response_format'}
        if outgoing_rest != stored_rest:
            problems.append('the request differs from old-2 outside the format')
        json_schema = request['response_format']['json_schema']
        if request['response_format'].get('type') != 'json_schema' or json_schema.get('strict') is not True or json_schema.get('name') != 'judgement':
            problems.append('the format is not strict json_schema named judgement')
        schema = json_schema['schema']
        if opened(schema) != v7_format:
            problems.append('the format differs from judging-v7 outside the four citation constraints')
        lists = closed_lists(schema)
        shown = {'evidence': sorted(judging.evidence_shown_in(user)), 'dependencies': sorted(dependencies_shown_in(user)), 'themes': sorted(judging.themes_shown_in(user))}
        mismatch = {k: {'only in format': sorted(set(lists[k]) - set(shown[k])), 'only in text': sorted(set(shown[k]) - set(lists[k]))}
                    for k in lists if lists[k] != shown[k]}
        accepted = [r for r in rows if not r['refused']]
        with lock:
            log['responses'] += 1
            log['sizes'].append({'evidence': len(lists['evidence']), 'themes': len(lists['themes']), 'dependencies': len(lists['dependencies']),
                                 'format chars': len(json.dumps(schema)), 'v7 format chars': len(json.dumps(v7_format))})
            if mismatch:
                log['list mismatches'].append({'call': first['call_id'], 'mismatch': mismatch})
            if problems:
                log['problems'].append({'call': first['call_id'], 'problems': problems})
            if not accepted:                       # old-2's check refused this first answer: its accepted retry answer, labelled
                retries = [r for (s, u), group in stored.items() if s == system and u.startswith(user + RETRY_MARK) for r in group if not r['refused']]
                if len(retries) != 1:
                    raise Stop(f'call {first["call_id"]}: {len(retries)} accepted retries found')
                log['substitutions'].append({'refused call': first['call_id'], 'retry call': retries[0]['call_id']})
                log['outgoing for refused originals'][first['call_id']] = {'request': request, 'answer': first['answer']}
                chosen = retries[0]
            else:
                chosen = accepted[0]
        return {'choices': [{'message': {'content': chosen['answer']}}], 'usage': chosen['usage']}

    held = live_lock.acquire(str(views))
    started = time.time()
    stopped = ''
    try:
        replay.run(testdb_path=str(ITEMS), views_path=str(views), archive=model.Archive(str(archive_path)), cfg=config.load(str(V121)),
                   universe=universe.load(str(UNIVERSE)), from_day=WINDOW[0], until_day=WINDOW[1], transport=transport, log=lambda *a: None,
                   only_objects={'NVDA'})
    except Exception as error:
        stopped = f'{type(error).__name__}: {error}'[:500]
    finally:
        live_lock.release(held)
    (folder / 'transport-log.json').write_text(json.dumps({k: v for k, v in log.items() if k != 'outgoing for refused originals'}, ensure_ascii=False))
    (folder / 'outgoing-refused-originals.json').write_text(json.dumps(log['outgoing for refused originals'], ensure_ascii=False))
    equal, comparison = compare_stores(views) if not stopped else (False, {})
    sizes = log['sizes']
    result = {
        'stopped': stopped, 'seconds': round(time.time() - started), 'judge rows removed from the seed': removed,
        'judge responses through the transport': log['responses'], 'substitutions': log['substitutions'],
        'problems': log['problems'], 'list mismatches': log['list mismatches'], 'store equal to old-2 (named columns apart)': equal,
        'store comparison': comparison,
        'sizes': {'requests': len(sizes), 'max evidence': max((s['evidence'] for s in sizes), default=0),
                  'format chars median': sorted(s['format chars'] for s in sizes)[len(sizes) // 2] if sizes else 0,
                  'format chars max': max((s['format chars'] for s in sizes), default=0), 'v7 format chars': sizes[0]['v7 format chars'] if sizes else 0},
    }
    result['T1 pass'] = (not stopped and log['responses'] == EXPECTED_JUDGE_RESPONSES and len(log['substitutions']) == EXPECTED_SUBSTITUTIONS
                         and not log['problems'] and not log['list mismatches'] and equal)
    return result, log['outgoing for refused originals']


def t1b(originals):
    """Each refused original answer through the real model.call under its v12 request: SchemaError on the bad id."""
    cfg = config.load(str(V121))
    out = {}
    with tempfile.TemporaryDirectory() as scratch:
        archive = model.Archive(str(Path(scratch) / 'archive.sqlite'))
        for call_id, item in originals.items():
            request = item['request']
            system, user = request['messages'][0]['content'], request['messages'][1]['content']
            schema = request['response_format']['json_schema']['schema']
            try:
                model.call(archive, cfg, cfg.rejudging, system, user, schema, 'judgement', 'judge',
                           transport=lambda provider, sent, answer=item['answer']: {'choices': [{'message': {'content': answer}}], 'usage': {}})
                out[call_id] = 'NOT REFUSED'
            except model.SchemaError as error:
                out[call_id] = f'SchemaError: {str(error)[:200]}'
    return out, all(v.startswith('SchemaError') for v in out.values()) and len(out) == EXPECTED_SUBSTITUTIONS


def main():
    if len(sys.argv) != 2 or sys.argv[1].startswith('-'):
        raise SystemExit(__doc__)                  # the one argument is a new output folder, never an option
    folder = Path(sys.argv[1])
    result, originals = t1(folder)
    result['T1b'], result['T1b pass'] = t1b(originals) if originals else ({}, False)
    (folder / 't1-result.json').write_text(json.dumps(result, indent=1, ensure_ascii=False))
    summary = {k: v for k, v in result.items() if k not in ('store comparison',)}
    print(json.dumps(summary, indent=1, ensure_ascii=False)[:6000])
    print(json.dumps({k: ({kk: vv for kk, vv in v.items() if kk != 'columns not compared'} if isinstance(v, dict) else v)
                      for k, v in result['store comparison'].items()}, indent=0)[:4000])
    sys.exit(0 if result['T1 pass'] and result['T1b pass'] else 1)


if __name__ == '__main__':
    main()

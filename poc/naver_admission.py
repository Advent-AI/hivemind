"""One frozen source/context: three fresh controls and three instruction-only treatments."""
import argparse
import copy
import dataclasses
import json
from pathlib import Path
import shutil
import signal
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'poc'))
from hivemind import config, dispatch, extraction, model, universe
from hivemind.views import round as rounds, store
from concurrency_study.budget import GuardedTransport, single_attempt_http
from concurrency_study.ingestion import StudyTransport, protected_changes, readonly
from concurrency_study.runner import digest

ORDER = ('control-1', 'treatment-1', 'treatment-2', 'control-2', 'control-3', 'treatment-3')


def inputs(directory):
    item = json.loads((directory / 'item.json').read_text())
    cfgs = {'control': config.load(ROOT / 'poc/config/poc-v23.json'),
            'treatment': config.load(ROOT / 'poc/config/poc-v24-admission-test.json')}
    uni = universe.load(ROOT / 'poc/universe.json')
    requests = {}
    with readonly(directory / 'baseline.sqlite') as db:
        objects = [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
        shown = store.views_for_prompt(db, objects)
        groups = store.groups_for_prompt(db, objects, item['title'])
        assert store.next_sequence(db) == 22
        assert not db.execute('select 1 from handovers where input_id=?', (item['input_id'],)).fetchone()
        for name, cfg in cfgs.items():
            setting, system, user, schema = extraction.request_for(cfg, item, item['text'], shown, uni, groups)
            requests[name] = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
    expected = copy.deepcopy(requests['control'])
    expected['messages'][0]['content'] = requests['treatment']['messages'][0]['content']
    if expected != requests['treatment']:
        raise ValueError('treatment changes more than the system message')
    prior = json.loads((directory / 'request-audit.json').read_text())
    if model.request_identity(requests['control'])[1] != prior['old_request_sha256']:
        raise ValueError('control is not the failed request')
    return item, cfgs, uni, requests


def metadata(directory):
    item, cfgs, _, requests = inputs(directory)
    paths = [directory / 'item.json', directory / 'baseline.sqlite', ROOT / 'poc/universe.json', Path(__file__),
             ROOT / 'poc/config/poc-v23.json', ROOT / 'poc/config/poc-v24-admission-test.json']
    paths += sorted((ROOT / 'src/hivemind').rglob('*.py')) + sorted((ROOT / 'src/hivemind/prompts').glob('*'))
    paths += sorted((ROOT / 'poc/concurrency_study').glob('*.py'))
    paths += [ROOT / 'docs/research/2026-10-25-day-batch-review/snapshot_proof.py',
              ROOT / 'docs/research/2026-10-25-day-batch-review/audit.py']
    return {'order': list(ORDER), 'input_id': item['input_id'], 'seq': 22,
            'max_calls': 36, 'cap_microdollars': 600000,
            'configs': {k: dataclasses.asdict(v) for k, v in cfgs.items()},
            'requests': {k: model.request_identity(v)[1] for k, v in requests.items()},
            'hashes': {str(p.resolve()): digest(p) for p in paths if p.is_file()}}


def prepare(directory):
    if protected_changes(directory):
        raise ValueError('protected database changed')
    with (directory / 'study.json').open('x') as handle:
        json.dump(metadata(directory), handle, indent=2)


def run(directory):
    frozen = json.loads((directory / 'study.json').read_text())
    if metadata(directory) != frozen or protected_changes(directory):
        raise ValueError('experiment inputs changed')
    if (directory / 'budget.sqlite').exists():
        raise ValueError('study already attempted; no automatic retry')
    item, cfgs, uni, requests = inputs(directory)
    transport = StudyTransport(GuardedTransport(directory / 'budget.sqlite', single_attempt_http(),
                                              cap_microdollars=600000, max_calls=36), workers=1)
    def cancel(signum, frame):
        transport.stop('cancelled')
        raise KeyboardInterrupt
    handlers = {sig: signal.signal(sig, cancel) for sig in (signal.SIGINT, signal.SIGTERM)}
    reports = []
    failure = None
    try:
        for name in ORDER:
            if metadata(directory) != frozen:
                raise ValueError('experiment changed during the run')
            arm = name.split('-')[0]
            folder = directory / name
            folder.mkdir()
            shutil.copyfile(directory / 'baseline.sqlite', folder / 'views.sqlite')
            archive = model.Archive(folder / 'archive.sqlite')
            conn = store.open_db(folder / 'views.sqlite')
            started = time.perf_counter()
            try:
                route = dispatch.route(conn, item, uni)
                if route.kind != 'extract' or route.sequence_no != 22:
                    raise ValueError('unexpected routing or source order')
                result = rounds.run(conn, archive, cfgs[arm], uni, item, route.sequence_no, transport=transport)
                if result.failed:
                    raise RuntimeError(result.failed)
                conn.commit()
                extracted = archive.conn.execute("select request_sha256,input_tokens,output_tokens,answer_json from model_calls where purpose='extract'").fetchall()
                if len(extracted) != 1 or extracted[0][0] != frozen['requests'][arm]:
                    raise ValueError('accepted extraction request mismatch or missing fresh response')
                row = conn.execute('select handover_json from handovers where input_id=?', (item['input_id'],)).fetchone()
                handover = json.loads(row[0])
                raw_answer = json.loads(extracted[0][3])
                with readonly(directory / 'baseline.sqlite') as before:
                    shown = store.views_for_prompt(before, ['NVDA'])
                    groups = store.groups_for_prompt(before, ['NVDA'], item['title'])
                checked = extraction.sift_with_groups(copy.deepcopy(raw_answer), item, item['text'],
                                                       {v['view_id'] for v in shown}, uni, english=True,
                                                       shown_group_ids=[g['group_id'] for g in groups])
                expected_hand = dict(zip(('evidence', 'candidates', 'dropped', 'new_groups'), checked))
                if handover != json.loads(json.dumps(expected_hand)):
                    raise ValueError('handover differs from the bound raw answer')
                summary = {'name': name, 'seconds': time.perf_counter() - started, 'result': dataclasses.asdict(result),
                           'request_sha256': extracted[0][0], 'input_tokens': extracted[0][1], 'output_tokens': extracted[0][2],
                           'raw_answer': raw_answer, 'handover': handover,
                           'new_views': [dict(r) for r in conn.execute('select * from views where created_seq=22')],
                           'new_groups': [dict(r) for r in conn.execute('select * from thesis_groups where created_seq=22')],
                           'new_members': [dict(r) for r in conn.execute('select * from thesis_group_members where seq=22')],
                           'new_sources': [dict(r) for r in conn.execute('select * from evidence_sources where seq=22')],
                           'matching': [dict(r) for r in conn.execute('select * from match_records where seq=22')],
                           'archive_totals': archive.totals()}
                (folder / 'result.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False))
                reports.append(summary)
                print(json.dumps({k: summary[k] for k in ('name', 'seconds', 'input_tokens', 'output_tokens', 'result')}, ensure_ascii=False), flush=True)
            finally:
                conn.close(); archive.conn.close()
    except BaseException as exc:
        transport.stop('study failed')
        failure = {'type': type(exc).__name__, 'message': str(exc)[:500]}
        raise
    finally:
        for sig, previous in handlers.items():
            signal.signal(sig, previous)
        changed = protected_changes(directory)
        report = {'failure': failure, 'changed_protected': changed, 'samples': reports,
                  'budget': transport.guard.summary(), 'scope': 'one item through writing, no daily judging'}
        (directory / 'result.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
        print(json.dumps({'failure': failure, 'changed_protected': changed, 'samples': len(reports),
                          'budget_microdollars': report['budget']['held_microdollars']}), flush=True)
        if changed and not failure:
            raise ValueError('protected database changed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    if args.prepare:
        prepare(args.directory.resolve())
    elif args.live:
        run(args.directory.resolve())
    else:
        parser.error('choose --prepare or --live')

"""D147: equivalent single-pattern wire schema for extracted subject references."""
import argparse
import copy
import dataclasses
import fcntl
import json
import re
from pathlib import Path

import extraction_membership as membership
from extraction_membership import process
import ingestion_threads as legacy
import study
from hivemind import dispatch, universe
from hivemind.views import store


def wire_schema(schema, offered):
    result = copy.deepcopy(schema)
    old_ids = [row['thread_id'] for row in offered]
    pattern = r'^(?:t[1-9][0-9]*' + ''.join('|' + re.escape(ident) for ident in old_ids) + ')$'
    result['properties']['candidates']['items']['properties']['thread_ids']['items'] = {
        'type': 'string', 'pattern': pattern}
    return result


class Calls(membership.Calls):
    def __init__(self, out, label):
        super().__init__(out, label)
        self.cfg = dataclasses.replace(self.cfg, version='membership-flat-reference-v1')

    def stage(self, name, prompt, payload, schema, setting):
        if name.endswith('-extract'):
            schema = wire_schema(schema, payload['existing_subjects'])
            if name == 'item2-extract':
                sample = self.sample.split('-')[0]
                baseline = json.loads((self.out / f'sample-{sample}-membership' / 'item2-extract.json').read_text())['request']
                expected = copy.deepcopy(baseline)
                expected['response_format']['json_schema']['schema'] = schema
                actual = study.model.build_request(setting, prompt, json.dumps(payload, ensure_ascii=False), schema,
                                                   'hierarchy_result', self.cfg.provider)
                if actual != expected:
                    raise ValueError('Paired input changed outside the reference schema')
        return super().stage(name, prompt, payload, schema, setting)


def fingerprints():
    return membership.fingerprints() | {str(Path(__file__).relative_to(study.ROOT)): study.digest(__file__)}


def prepare(out):
    membership.verify(out)
    path = out / 'flat-manifest.json'
    if path.exists() or list(out.glob('sample-*-flat')):
        raise ValueError('Use a fresh flat-reference experiment')
    sources = {}
    for sample in [1, 2, 3]:
        source = out / f'sample-{sample}-membership'
        target = out / f'sample-{sample}-flat'
        target.mkdir()
        before = study.digest(source / 'views.sqlite')
        src = study.read_only(source / 'views.sqlite')
        dst = legacy.open_db(target / 'views.sqlite')
        src.backup(dst)
        src.close()
        dst.close()
        assert study.digest(source / 'views.sqlite') == before
        sources[str(source / 'views.sqlite')] = before
        for name in ['item1-extract.json', 'item1-match.json', 'item1-result.json']:
            record = json.loads((source / name).read_text())
            record['reused_from'] = str(source / name)
            study.write_json(target / name, record)
            sources[str(source / name)] = study.digest(source / name)
    budget = json.loads((out / 'budget.json').read_text())
    study.write_json(path, {'version': 'membership-flat-reference-v1', 'dependencies': fingerprints(),
        'copied_sources': sources, 'shared_attempts_before': len(budget['attempts']),
        'shared_budget_before': budget['estimated_spent']})


def verify(out):
    membership.verify(out)
    manifest = json.loads((out / 'flat-manifest.json').read_text())
    if manifest['dependencies'] != fingerprints() or any(study.digest(path) != sha for path, sha in manifest['copied_sources'].items()):
        raise ValueError('Frozen flat-reference experiment changed')


def run(out, extra=False):
    verify(out)
    if extra:
        review = json.loads((out / 'flat-core-review.json').read_text())
        if review.get('reviewed_by') != 'assistant' or review.get('core_semantics_passed') is not True:
            raise ValueError('Extra article requires the predefined successful core review')
        events = [(4, json.loads((out / 'extra-item.json').read_text()))]
    else:
        events = list(enumerate(json.loads((out / 'items.json').read_text()), 1))
    uni = universe.load(str(study.ROOT / 'poc/universe.json'))
    with (out / 'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        streams = []
        for sample in [1, 2, 3]:
            label = f'{sample}-flat'
            calls = Calls(out, label)
            conn = legacy.open_db(out / f'sample-{label}' / 'views.sqlite')
            streams.append((label, calls, conn))
        stop = False
        for index, item in events:
            for label, calls, conn in streams:
                failed = out / f'sample-{label}' / ('extra-failed.json' if extra else 'failed.json')
                if failed.exists() or store.is_processed(conn, item['input_id']):
                    continue
                try:
                    result = process(conn, calls, uni, item, index)
                    study.write_json(out / f'sample-{label}' / f'item{index}-result.json', result)
                    print(f'WRITTEN {label} item={index} new_views={len(result.get("new_views", {}))}', flush=True)
                except Exception as error:
                    conn.rollback()
                    study.write_json(failed, {'item_index': index, 'error': type(error).__name__ + ': ' + str(error)[:1000]})
                    print(f'FAILED {label} item={index}: {error}', flush=True)
                    if 'budget' in str(error).lower():
                        stop = True
                        break
            if stop:
                break
        last_item = events[-1][1]
        for label, calls, conn in streams:
            if store.is_processed(conn, last_item['input_id']):
                route = dispatch.route(conn, last_item, uni)
                study.write_json(out / f'sample-{label}' / ('extra-resend.json' if extra else 'resend.json'),
                                 {'route': route.kind, 'reason': route.reason})
            conn.close()
            calls.archive.conn.close()
    budget = json.loads((out / 'budget.json').read_text())
    print(f'FINISHED shared_attempts={len(budget["attempts"])} estimated_usd={budget["estimated_spent"]:.6f}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'core', 'extra'])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    if args.command == 'prepare':
        prepare(out)
    else:
        run(out, args.command == 'extra')

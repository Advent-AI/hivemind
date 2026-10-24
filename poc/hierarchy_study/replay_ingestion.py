"""Replay recorded ingestion answers without network access; audit affected groups and retained hints."""
import argparse
import json
from pathlib import Path

import ingestion_groups as ingest
import study
from hivemind import dispatch, universe
from hivemind.views import matching, writing


class RecordedCalls:
    def __init__(self, source):
        self.source = source
        self.cfg = study.config.load(str(study.ROOT / 'poc/config/poc-v7.json'))
        self.read_count = 0

    def stage(self, name, prompt, payload, schema, setting):
        record = json.loads((self.source / f'{name}.json').read_text())
        expected = study.model.build_request(setting, prompt, json.dumps(payload, ensure_ascii=False), schema,
                                              'hierarchy_result', self.cfg.provider)
        if record['status'] != 'complete' or expected != record['request']:
            raise ValueError(f'Recorded input differs: {self.source.name}/{name}')
        self.read_count += 1
        return record['answer']


def run(source, out):
    if out.exists():
        raise ValueError('Use a new dated replay directory')
    out.mkdir(parents=True)
    items = json.loads((source / 'items.json').read_text())
    uni = universe.load(str(study.ROOT / 'poc/universe.json'))
    changes, relations, streams = [], [], []
    for label in ['1-control', '1-grouped', '2-grouped', '2-control', '3-control', '3-grouped']:
        target = out / f'sample-{label}'
        target.mkdir()
        conn = ingest.open_experiment_db(target / 'views.sqlite')
        calls = RecordedCalls(source / f'sample-{label}')
        grouped = label.endswith('grouped')
        for index, item in enumerate(items, 1):
            event = ingest.process(conn, calls, uni, item, index, grouped)
            old = json.loads((calls.source / f'item{index}-result.json').read_text())
            assert event['new_views'] == old['new_views'] and event['members'] == old['members']
            if event['affected_groups'] != old['affected_groups']:
                changes.append({'stream': label, 'item': index, 'before': old['affected_groups'], 'after': event['affected_groups']})
            if grouped:
                extract = json.loads((calls.source / f'item{index}-extract.json').read_text())
                decision = json.loads((calls.source / f'item{index}-match.json').read_text())['answer']
                outcomes = {c['id']: (dict(zip(ingest.OUTCOMES, matching.OUTCOMES))[c['outcome']], c['target_view_id'], []) for c in decision['candidates']}
                checked = matching.Checked(outcomes, {}, [], {})
                written = writing.Written(set(event['changed_views']), event['new_views'], {}, [])
                visible = {v['view_id'] for v in json.loads(extract['request']['messages'][1]['content'])['existing_theses']}
                projected = ingest.resolve_hints(extract['answer'].get('relationship_hints', []), checked, written, visible)
                event['retained_extraction_relations'] = projected
                relations.extend({'stream': label, 'item': index, **r} for r in projected)
            study.write_json(target / f'item{index}-result.json', event)
        before = calls.read_count
        assert ingest.process(conn, calls, uni, items[-1], 3, grouped)['route'] == 'skipped'
        assert before == calls.read_count
        streams.append({'stream': label, 'recorded_calls_read': before, 'resend_new_calls': calls.read_count-before})
        conn.close()
    summary = {'source_run': str(source), 'network_calls': 0, 'corrected_affected_events': changes,
               'retained_extraction_relations': relations, 'streams': streams}
    study.write_json(out / 'summary.json', summary)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    run(args.source.resolve(), args.out.resolve())

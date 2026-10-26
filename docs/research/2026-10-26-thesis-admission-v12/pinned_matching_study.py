#!/usr/bin/env python3
"""Does the collision judge (D190) work? Measured with extraction pinned: both arms replay the same window with every extraction
request answered by the r3 run's recorded answer for that item (group references and fold targets stripped, since ids differ
between ledgers), Jev live, the collision judge live in the arm, judging synthetic. Only the matcher differs between the arms,
so a difference in theses, duplicates and gold is the judge's.

  python3 .../pinned_matching_study.py --source /abs/r3 --out /abs/out-dir   (runs control = poc-v25, then arm = poc-v26)
"""
import argparse
import json
import os
import pathlib
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, jev, model, replay, universe  # noqa: E402

ITEMS = '/Users/lchingen/hivemind/poc/data/items-window-tags2-2026-10-24.sqlite'
STAGES = [('2026-02-25', '2026-07-23', {'NVDA'}), ('2026-07-24', '2026-07-31', None), ('2026-08-01', '2026-08-15', None)]


class Pinned:
    """Extraction: the recorded answer of the same item. Collision: the real model. Judgement: synthetic. Jev: real."""

    def __init__(self, source_archive, source_views=None, own_views=None):
        self.source_views, self.own_views = source_views, own_views        # recorded view ids are translated to this arm's ids by (item, question)
        self.identity = {}
        if source_views:
            with sqlite3.connect(f'file:{source_views}?mode=ro', uri=True) as db:
                self.identity = {vid: (inp, q) for vid, inp, q in db.execute('select view_id, created_from_input, question from views')}
        self.recorded = {}
        with sqlite3.connect(f'file:{source_archive}?mode=ro', uri=True) as db:
            for request_json, answer_json in db.execute("select request_json, answer_json from model_calls where purpose='extract' order by call_id"):
                user = json.loads(request_json)['messages'][1]['content']
                marker = '[Item] id '
                if marker in user:
                    input_id = user.split(marker, 1)[1].split(',', 1)[0]
                    self.recorded[input_id] = json.loads(answer_json)         # the last recorded answer for the item
        self.counts = {'extraction': 0, 'extraction_unrecorded': 0, 'collision': 0, 'judgement': 0, 'jev': 0}

    def __call__(self, *args):
        if len(args) == 1:                                   # Jev's typed endpoint
            self.counts['jev'] += 1
            return jev.transport(args[0])
        provider, request = args
        name = request['response_format']['json_schema']['name']
        if name == 'collision':
            self.counts['collision'] += 1
            return model.openai_transport(provider, request)
        if name == 'extraction':
            user = request['messages'][1]['content']
            input_id = user.split('[Item] id ', 1)[1].split(',', 1)[0]
            answer = self.recorded.get(input_id)
            if answer is None:
                self.counts['extraction_unrecorded'] += 1
                answer = {'evidence': [], 'candidates': [], 'new_groups': []}
            else:
                self.counts['extraction'] += 1
                answer = json.loads(json.dumps(answer))
                for c in answer.get('candidates', []):
                    c['group_refs'] = []
                    if 'folds_into' in c:
                        c['folds_into'] = ''
                answer['new_groups'] = []
                if self.own_views and os.path.exists(self.own_views):
                    with sqlite3.connect(f'file:{self.own_views}?mode=ro', uri=True) as db:
                        own = {(inp, q): vid for vid, inp, q in db.execute('select view_id, created_from_input, question from views')}
                    for e in answer.get('evidence', []):
                        e['links'] = [own.get(self.identity.get(l), l) if l.startswith('v') else l for l in e['links']]
            return {'choices': [{'message': {'content': json.dumps(answer)}}]}
        self.counts['judgement'] += 1
        data = {'rung': 1, 'reasons': 'pinned study: synthetic judgement', 'cites': [], 'cites_views': [], 'pushes': [], 'changed': True, 'why_changed': 'synthetic'}
        return {'choices': [{'message': {'content': json.dumps(data)}}]}


def run_arm(name, cfg_path, source, out):
    folder = out / name
    folder.mkdir(parents=True, exist_ok=True)
    cfg = config.load(cfg_path)
    uni = universe.load(ROOT / 'poc' / 'universe.json')
    archive = model.Archive(str(folder / 'archive.sqlite'))
    transport = Pinned(source / 'archive.sqlite', source / 'views.sqlite', str(folder / 'views.sqlite'))
    log_path = folder / 'replay.log'

    def log(*parts):
        with open(log_path, 'a', encoding='utf-8') as handle:
            handle.write(' '.join(str(p) for p in parts) + '\n')

    totals = []
    for from_day, until_day, only in STAGES:
        totals.append(replay.run(testdb_path=ITEMS, views_path=str(folder / 'views.sqlite'), archive=archive, cfg=cfg, universe=uni,
                                 from_day=from_day, until_day=until_day, spend_cap_usd=3.0, log=log, only_objects=only, transport=transport))
    (folder / 'summary.json').write_text(json.dumps({'config': cfg.version, 'totals': totals, 'transport_calls': transport.counts}, indent=1, default=str))
    print(name, cfg.version, transport.counts, totals[-1] if totals else None, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    source, out = pathlib.Path(args.source), pathlib.Path(args.out)
    run_arm('control-v25', ROOT / 'poc' / 'config' / 'poc-v25.json', source, out)
    run_arm('arm-v26', ROOT / 'poc' / 'config' / 'poc-v26.json', source, out)
    print('DONE', flush=True)


if __name__ == '__main__':
    main()

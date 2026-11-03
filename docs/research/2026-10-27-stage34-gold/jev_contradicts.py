"""The mechanism's share on the product's own data: for each of the run's 47 `replace` decisions, re-send the stored Jev question
(the incoming piece against the piece it replaced) twice, once with the criteria as stored (fresh control) and once with the
`supersedes` criterion without "confirms or denies" and a `contradicts` class added. Counts the flips. No ledger is written.
Run: python3 jev_contradicts.py"""
import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, jev, model  # noqa: E402

RUN = '/Users/lchingen/hivemind/poc/data/english-v29-nvda-3m-2026-10-27'
OUT = '/Users/lchingen/hivemind/poc/reports/2026-10-27-stage34-gold/jev-contradicts'
SPLIT = {
    'same_statement': 'the same evidence: a retelling, the same number stated in text and in a table or in another document, or the same speaker repeating the same statement; wording, precision and document may differ',
    'supersedes': 'a later version of the same statement or number, changed by its owner: the same speaker revises that guidance, forecast or event-progress statement, an official confirms that reported claim, or the original source revises that statement; another statement on the same topic is not this',
    'contradicts': 'a claim that denies or disagrees with the stored piece: a company denies a reported delay or cancellation, an independent test disputes a vendor benchmark, a second party gives an opposite account; both statements stand',
    'different': 'a different fact, figure or matter, or a figure for another period or quantity, even if on the same topic'}


def main():
    os.makedirs(OUT, exist_ok=True)
    views = sqlite3.connect(f'file:{RUN}/views.sqlite?mode=ro', uri=True)
    archive_old = sqlite3.connect(f'file:{RUN}/archive.sqlite?mode=ro', uri=True)
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v34.json'))
    archive = model.Archive(os.path.join(OUT, 'archive.sqlite'))
    jobs = []
    for seq, iid, shown, dec in views.execute('select seq,input_id,shown_json,decisions_json from match_records order by seq'):
        d, s = json.loads(dec), json.loads(shown)
        for e in d.get('evidence', []):
            if e['outcome'] != 'replace':
                continue
            key = f"piece__{e['view_id']}__{e['target_evidence_id']}"
            for r in s.get('requests', []):
                row = archive_old.execute('select request_json from model_calls where call_id=?', (r['call_id'],)).fetchone()
                if not row:
                    continue
                req = json.loads(row[0])
                if key in req['questions'] and req['state'].startswith('INCOMING PIECE') and e['id'] in e.get('reason', '') or key in req['questions']:
                    jobs.append((seq, iid, e, key, req['state'], req['questions'][key]))
                    break
    print('replace decisions with a stored question found:', len(jobs))
    rows = []
    for seq, iid, e, key, state, question in jobs:
        control = jev.ask(archive, cfg, cfg.matching, state, {key: question}, 'jev-contradicts:control')
        arm_q = dict(question, criteria=SPLIT)
        arm = jev.ask(archive, cfg, cfg.matching, state, {key: arm_q}, 'jev-contradicts:split')
        c, a = control.data[key], arm.data[key]
        rows.append({'seq': seq, 'input_id': iid, 'piece': e['id'], 'view': e['view_id'], 'target': e['target_evidence_id'],
                     'stored_reason': e.get('reason', '')[:120], 'control': [c['choice'], c['probabilities'].get(c['choice'])],
                     'split': [a['choice'], a['probabilities'].get(a['choice'])], 'split_probabilities': a['probabilities'], 'state': state[:300]})
        print(f"seq {seq} {e['id']}->{e['target_evidence_id']} ({e['view_id']}): control {c['choice']} {c['probabilities'].get(c['choice']):.2f} | split {a['choice']} {a['probabilities'].get(a['choice']):.2f}")
    json.dump(rows, open(os.path.join(OUT, 'results.json'), 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print('control labels:', Counter(r['control'][0] for r in rows))
    print('split labels  :', Counter(r['split'][0] for r in rows))
    print('archive:', archive.totals())


if __name__ == '__main__':
    main()

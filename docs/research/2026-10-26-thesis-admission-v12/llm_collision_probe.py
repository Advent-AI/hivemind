#!/usr/bin/env python3
"""Cheapest proof for a hybrid matcher: when a candidate's list holds a thesis of the same object and measure (a collision), ask the
generative model the analyst's question instead of Jev's. Re-uses the stored Jev states and thesis texts; three samples; scored
against the probe labels. Scratch archive only.

  python3 .../llm_collision_probe.py --ledger <run dir> --labels <labels.json> --out <dir> --archive <scratch sqlite> [--samples 3]
"""
import argparse, collections, json, pathlib, sqlite3, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hivemind import config, model  # noqa: E402
import jev_relation_probe as P  # noqa: E402

SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['relations'],
          'properties': {'relations': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['thesis_id', 'relation', 'why'],
                         'properties': {'thesis_id': {'type': 'string'},
                                        'relation': {'type': 'string', 'enum': ['same_question', 'same_question_other_period', 'distinct_question_same_matter', 'different']},
                                        'why': {'type': 'string'}}}}}}
SYSTEM = ("You are a senior hedge-fund analyst keeping a short list of live questions per company and theme. A question is one decision: "
          "two texts are the same question when the same outcome settles both and you would not keep two cards for them; another estimate, "
          "source, wording, or another population or proxy of one aggregate (the top five, five named companies, the largest four) is the same "
          "question, and so is the same deal or proceeding described twice. They are distinct questions in one matter when their answers can "
          "move apart and you would want each: a component with its own drivers, a different quantity in the same deal (a guarantee beside a "
          "financing), a different event. The same quantity for a later period is a succession. Judge from the texts only; equal numbers and "
          "similar words do not decide.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ledger', required=True); ap.add_argument('--labels', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--archive', required=True); ap.add_argument('--samples', type=int, default=3)
    args = ap.parse_args()
    ledger = pathlib.Path(args.ledger)
    conn, archive_ro = P.ro(ledger / 'views.sqlite'), P.ro(ledger / 'archive.sqlite')
    keys, views, work = P.collect(conn, archive_ro)
    labels = json.loads(pathlib.Path(args.labels).read_text())
    cfg = config.load(ROOT / 'poc' / 'config' / 'poc-v25.json')
    setting = cfg.extraction['T7']                       # gpt-6-luna, low reasoning
    archive = model.Archive(args.archive)
    records, spent = [], 0.0
    for w in work:
        if w['key'] not in labels:
            continue
        c, request = w['candidate'], w['request']
        theses = {q[5:]: body['instructions'].split('THESIS:\n', 1)[1] for q, body in request['questions'].items() if q.startswith('rel__') and q[5:] in w['peers']}
        user = request['state'] + '\n\nTHESES:\n' + '\n'.join(f'--- {v}\n{t}' for v, t in theses.items()) + '\n\nFor each thesis id, state the relation.'
        rec = {'key': w['key'], 'label': labels[w['key']], 'samples': []}
        for s in range(args.samples):
            answer = model.call(archive, cfg, setting, SYSTEM, user + f'\n[sample {s + 1}]', SCHEMA, 'collision', 'match')
            spent += answer.cost_usd
            rels = {r['thesis_id']: r for r in answer.data['relations']}
            open_at = lambda v, seq=w['seq']: keys.get(v, {}).get('seq', 10 ** 9) < seq
            outcome, target = 'new', ''
            for v in w['peers']:
                r = rels.get(v)
                if not r:
                    continue
                if r['relation'] == 'same_question' and open_at(v):
                    outcome, target = 'merge', v; break
                if r['relation'] == 'same_question_other_period':
                    outcome, target = 'succession', v
            rec['samples'].append({'outcome': outcome, 'target': target, 'relations': {v: (rels[v]['relation'], rels[v]['why'][:120]) for v in rels}})
        records.append(rec)
        maj = collections.Counter((s['outcome'], s['target']) for s in rec['samples']).most_common(1)[0][0]
        print(f"{w['key'][-40:]}: expect {rec['label']['expect']} {rec['label'].get('target','')} -> {[s['outcome'] + ' ' + s['target'] for s in rec['samples']]}")
    out = pathlib.Path(args.out); out.mkdir(parents=True, exist_ok=True)
    (out / 'llm-records.json').write_text(json.dumps(records, ensure_ascii=False, indent=1))
    right = 0
    for rec in records:
        maj = collections.Counter((s['outcome'], s['target']) for s in rec['samples']).most_common(1)[0][0]
        want = rec['label'].get('target', '')
        right += maj[0] == rec['label']['expect'] and (not want or maj[1] == want)
    print(f'labelled {len(records)}: generative matcher right {right}; ${spent:.4f}')


if __name__ == '__main__':
    main()

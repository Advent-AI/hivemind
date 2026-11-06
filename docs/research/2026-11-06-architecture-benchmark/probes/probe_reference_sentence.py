"""Cents probe (AGENTS §7.3): the record-preparation reference sentence, as stored (split-preparation-v1) against one rewording, re-sent on the
stored preparation requests of the 2026-08-29/30 production-path probe. Motivating cases: 1227 (a management forecast "toward as much as $205
billion" rejected as not guidance), 1241 (the July 12-month inflation reading rejected because its month differs). Controls that must stay empty
(no full-period reference in the source): 1240, 1228, 1234, 1248, 1209, 1246. Controls that must keep a ladder: 1230, 1251, 1273, 1275.
Each answer's ladder goes through the split's own ladder checks.

    PYTHONPATH=src python3 probe_reference_sentence.py <out.json>"""
import concurrent.futures
import json
import sqlite3
import sys

sys.path.insert(0, '/Users/lchingen/hivemind-no-preseed-evidence-review/src')
from hivemind import config, model, split  # noqa: E402

RUN = '/Users/lchingen/hivemind-no-preseed-evidence-review/poc/data/split-v3-prod-0829-0830-r2-2026-11-06'
OLD = ('State the neutral comparison in its condition: the reference the source or evidence gives, such as guidance, a consensus or analyst estimate, '
       'the last reported figure for the same quantity or a stated target; a figure for part of the period is evidence, not the reference.')
NEW = ('State the neutral comparison in its condition: the reference the source or evidence gives, such as the guidance or forecast of whoever '
       'sets or reports the figure (a range or a ceiling counts), a consensus or analyst estimate, a stated target, or the latest reading of the same '
       'measure over a period of the same length (last year\'s figure for an annual question; the latest 12-month rate for a 12-month rate); a figure '
       'for part of the question\'s period is evidence, not the reference.')
CASES = {'motivating': [1227, 1241], 'stay empty': [1240, 1228, 1234, 1248, 1209, 1246], 'keep a ladder': [1230, 1251, 1273, 1275]}


def main():
    cfg = config.load('/Users/lchingen/hivemind-no-preseed-evidence-review/poc/config/poc-split-v3.json')
    views = sqlite3.connect(f'file:{RUN}/views.sqlite?mode=ro', uri=True)
    archive = sqlite3.connect(f'file:{RUN}/archive.sqlite?mode=ro', uri=True)
    rows = [(json.loads(r), json.loads(a)) for r, a in archive.execute("select request_json, answer_json from model_calls where purpose='split_preparation'")]
    jobs = []
    for group, seqs in CASES.items():
        for seq in seqs:
            question = json.loads(views.execute('select handover_json from handovers where seq=?', (seq,)).fetchone()[0])['candidates'][0]['question']
            request, stored = next((r, a) for r, a in rows if question[:80] in r['messages'][-1]['content'])
            cid = next(q['id'] for q in json.loads(request['messages'][-1]['content'].split('[Questions]\n')[1].split('\n\n[Evidence]')[0]) if q['question'][:80] == question[:80])
            assert request['messages'][0]['content'].count(OLD) == 1
            for arm, sentence in (('stored', OLD), ('reworded', NEW)):
                changed = json.loads(json.dumps(request))
                changed['messages'][0]['content'] = changed['messages'][0]['content'].replace(OLD, sentence)
                jobs.append((group, seq, cid, question, arm, changed, stored['candidates'][cid]))

    def send(job):
        group, seq, cid, question, arm, request, stored = job
        response = model.openai_transport(cfg.provider, request)
        answer = json.loads(response['choices'][0]['message']['content'])['candidates'][cid]
        rungs, problem = split.ordered_ladder(answer['rungs'], 'theme' if answer.get('favourable_end') == 'none' and answer['opens_as'] == 'shared_quantity' else 'asset',
                                              answer.get('favourable_end'), answer.get('unit'))
        return {'group': group, 'seq': seq, 'arm': arm, 'question': question, 'rungs_returned': len(answer['rungs']), 'ladder_problem': problem,
                'conditions': [r['condition'] for r in answer['rungs']], 'favourable_end': answer.get('favourable_end'), 'usage': response.get('usage')}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(send, jobs))
    json.dump(results, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
    for r in sorted(results, key=lambda r: (r['group'], r['seq'], r['arm'])):
        print(f"{r['group']:13} {r['seq']} {r['arm']:9} rungs {r['rungs_returned']} {('PROBLEM ' + r['ladder_problem']) if r['ladder_problem'] else ''} | {r['question'][:70]}")
        for c in r['conditions'][:5]:
            print('        ', c[:160])


if __name__ == '__main__':
    main()

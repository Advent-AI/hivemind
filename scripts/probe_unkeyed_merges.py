"""Exercise the existing collision judge on historical unkeyed merge requests."""
import concurrent.futures
import dataclasses
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, model  # noqa: E402
from hivemind.views import jev_matching  # noqa: E402

SNAP = Path('/Users/lchingen/hivemind-no-preseed-evidence-review/poc/data/split-fresh-seven-day-2026-11-05-v2/snapshot')
OUT = ROOT / 'poc/data/matching-identity-merges-direction-2026-11-05'


def cases():
    views = sqlite3.connect(f'file:{SNAP / "views.sqlite"}?mode=ro', uri=True)
    archive = sqlite3.connect(f'file:{SNAP / "match-judge-archive.sqlite"}?mode=ro', uri=True)
    cases = []
    rows = views.execute('select m.seq,h.handover_json,m.decisions_json from match_records m join handovers h on h.seq=m.seq where m.seq>=1205 order by m.seq')
    for seq, handover_text, decisions_text in rows:
        handover = json.loads(handover_text)
        candidates = {c['id']: c for c in handover['candidates']}
        for decision in json.loads(decisions_text)['candidates']:
            c = candidates.get(decision['id'])
            target = decision['target_view_id']
            if not c or c.get('measure') or decision['outcome'] != 'merge' or f'{target}: part_of' not in decision['reason']:
                continue
            found = []
            for call_id, request_text, answer_text in archive.execute("select call_id,request_json,answer_json from model_calls where purpose='match' and model='jev-1.14.0' and request_json like ?", ('%' + c['question'][:65] + '%',)):
                request, answer = json.loads(request_text), json.loads(answer_text)
                if c['looks_at'] in request.get('state', '') and 'rel__' + target in request.get('questions', {}):
                    found.append((call_id, request, answer))
            if len(found) != 1:
                raise ValueError(f'{seq}: expected one exact request, got {len(found)}')
            call_id, request, answer = found[0]
            peers = []
            for relation in ('same_quantity_or_event', 'part_of'):
                peers.extend(v for _, v in sorted(((a['probabilities'][relation], qid[5:]) for qid, a in answer.items()
                    if qid.startswith('rel__') and a['choice'] == relation and a['probabilities'][relation] >= jev_matching.THRESHOLD), reverse=True))
            if target not in peers:
                raise ValueError(f'{seq}: stored target absent from proposed matches')
            texts = {v: request['questions']['rel__' + v]['instructions'].split('THESIS:\n', 1)[1] for v in peers}
            cases.append({'seq': seq, 'target': target, 'source_call': call_id, 'state': request['state'], 'peers': peers, 'texts': texts})
    if len(cases) != 17:
        raise ValueError(f'expected 17 stored unkeyed merges, got {len(cases)}')
    return cases


def main():
    saved = cases()
    cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
    cfg = dataclasses.replace(cfg, collision=dataclasses.replace(cfg.collision, prompt_version='collision-v3'))
    system = Path(config.prompt_path(cfg.collision.prompt_version + '.txt')).read_text()
    OUT.mkdir(parents=True, exist_ok=False)
    archive = model.Archive(str(OUT / 'archive.sqlite'))

    def send(case):
        user = case['state'] + '\n\nTHESES:\n' + '\n'.join(f'--- {v}\n{case["texts"][v]}' for v in case['peers']) + '\n\nFor each thesis id, state the relation.'
        answer = model.call(archive, cfg, cfg.collision, system, user, jev_matching.COLLISION_SCHEMA, 'collision', 'match')
        ids = [r['thesis_id'] for r in answer.data['relations']]
        if len(ids) != len(case['peers']) or set(ids) != set(case['peers']):
            raise ValueError(f'{case["seq"]}: incomplete collision answer')
        verdict = {r['thesis_id']: r for r in answer.data['relations']}
        target = next((v for v in case['peers'] if verdict[v]['relation'] == 'same_question'), '')
        return {**{k: case[k] for k in ('seq', 'target', 'source_call', 'peers')}, 'new_outcome': 'merge' if target else 'new',
                'new_target': target, 'answer': answer.data, 'tokens': [answer.input_tokens, answer.output_tokens]}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(send, saved))
    (OUT / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    for r in results:
        print(r['seq'], r['target'], '->', r['new_outcome'], r['new_target'], 'peers', len(r['peers']))


if __name__ == '__main__':
    main()

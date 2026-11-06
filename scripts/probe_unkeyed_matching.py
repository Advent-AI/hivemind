"""Probe the existing collision judge on exact candidate/target texts saved by Jev."""
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
OUT = ROOT / 'poc/data/matching-identity-direction-probe-2026-11-05'
CASES = [(1251, 'v32'), (1209, 'v10'), (1227, 'v4'), (1250, 'v5'), (1243, 'v64')]


def stored_cases():
    views = sqlite3.connect(f'file:{SNAP / "views.sqlite"}?mode=ro', uri=True)
    archive = sqlite3.connect(f'file:{SNAP / "match-judge-archive.sqlite"}?mode=ro', uri=True)
    cases = []
    for seq, target in CASES:
        handover = json.loads(views.execute('select handover_json from handovers where seq=?', (seq,)).fetchone()[0])
        candidate_data = handover['candidates'][0]
        candidate = candidate_data['question']
        matches = []
        for call_id, request_text in archive.execute("select call_id,request_json from model_calls where purpose='match' and model='jev-1.14.0' and request_json like ?", ('%' + candidate[:65] + '%',)):
            request = json.loads(request_text)
            question = request.get('questions', {}).get('rel__' + target)
            if question and candidate in request.get('state', '') and candidate_data['looks_at'] in request['state']:
                text = question['instructions'].split('THESIS:\n', 1)[1]
                matches.append((call_id, request['state'], text))
        if len(matches) != 1:
            raise ValueError(f'{seq}: expected one exact stored request, got {len(matches)}')
        call_id, state, text = matches[0]
        cases.append((seq, target, call_id, state, text))
    return cases


def main():
    cases = stored_cases()
    cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
    cfg = dataclasses.replace(cfg, collision=dataclasses.replace(cfg.collision, prompt_version='collision-v3'))
    system = Path(config.prompt_path(cfg.collision.prompt_version + '.txt')).read_text()
    OUT.mkdir(parents=True, exist_ok=False)
    archive = model.Archive(str(OUT / 'archive.sqlite'))

    def send(case):
        seq, target, call_id, state, thesis = case
        user = state + '\n\nTHESES:\n--- ' + target + '\n' + thesis + '\n\nFor each thesis id, state the relation.'
        answer = model.call(archive, cfg, cfg.collision, system, user, jev_matching.COLLISION_SCHEMA, 'collision', 'match')
        return {'seq': seq, 'target': target, 'source_call': call_id, 'answer': answer.data, 'tokens': [answer.input_tokens, answer.output_tokens]}

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(send, cases))
    (OUT / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

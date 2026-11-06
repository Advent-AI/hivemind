"""Ask the existing analyst judge about the stored low-confidence same-transaction pair."""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, model  # noqa: E402
from hivemind.views import jev_matching  # noqa: E402

SOURCE = ROOT / 'poc/data/split-fresh-seven-day-matching-v3-2026-11-05'
OUT = ROOT / 'poc/data/collision-low-confidence-probe-2026-11-05'


def main():
    db = sqlite3.connect((SOURCE / 'snapshot/match-judge-archive.sqlite').resolve().as_uri() + '?mode=ro', uri=True)
    candidates = []
    for call_id, request_text, answer_text in db.execute("select call_id,request_json,answer_json from model_calls where purpose='match' and model='jev-1.14.0'"):
        request, answer = json.loads(request_text), json.loads(answer_text)
        if 'Will NVIDIA complete its reported acquisition of Hugging Face by February 29, 2028?' in request.get('state', '') and 'rel__v64' in request.get('questions', {}):
            candidates.append((call_id, request, answer))
    if len(candidates) != 1:
        raise ValueError('expected exactly one stored candidate comparison')
    call_id, request, answer = candidates[0]
    verdict = answer['rel__v64']
    if verdict['choice'] != 'part_of' or verdict['probabilities']['part_of'] >= .5:
        raise ValueError('stored comparison is not the diagnosed case')
    thesis = request['questions']['rel__v64']['instructions'].split('THESIS:\n', 1)[1]
    user = request['state'] + '\n\nTHESES:\n--- v64\n' + thesis + '\n\nFor each thesis id, state the relation.'
    cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
    system = Path(config.prompt_path(cfg.collision.prompt_version + '.txt')).read_text()
    OUT.mkdir(parents=True, exist_ok=False)
    archive = model.Archive(str(OUT / 'archive.sqlite'))
    result = model.call(archive, cfg, cfg.collision, system, user, jev_matching.COLLISION_SCHEMA, 'collision', 'match')
    if len(result.data['relations']) != 1 or result.data['relations'][0]['thesis_id'] != 'v64':
        raise ValueError('analyst reply did not cover v64 exactly once')
    (OUT / 'result.json').write_text(json.dumps({'source_call': call_id, 'answer': result.data}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result.data, ensure_ascii=False))


if __name__ == '__main__':
    main()

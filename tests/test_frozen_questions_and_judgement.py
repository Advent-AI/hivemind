"""Steps 3 and 4 are frozen (D354, Alex 2026-11-03: "那你跑了吧，我们赶紧确认step 3,4 可以freeze"): opening and matching questions, and
judging them, as `poc/config/poc-v108.json` runs them (its sha256 is pinned in test_frozen_extraction_prompt.py). Every piece that shapes
those requests is pinned here: the collision judge's and the judge's prompt files, the matching prompt the configuration names, the
judge's answer schema, and the three questions the Jev matcher is asked. A change is a new version opened only by Alex's decision."""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind.views import jev_matching, judging  # noqa: E402

FROZEN_FILES = {
    'src/hivemind/prompts/collision-v2.txt': 'a5f0f58d53c4f4215b14e534935b1f95a79b35ba097d68c0ab598af7b88a3bd0',
    'src/hivemind/prompts/judging-v7.txt': 'd499c4b89ad038ade9bd41e037d766d5e54defecef273541f46dc01509db5a2c',
    'src/hivemind/prompts/matching-v3.txt': '04e23ee314e71cb094273b23e75f816c467176969b8c17dfec5a6e5d17a45a49',
}
JUDGING_SCHEMA_SHA = '4d1469ae9c14256c24e2c39e1b6cc772cb25e160c937f32091fc4f35bf539ca9'
MATCHER_QUESTIONS_SHA = '86cb70600ce456be3cd5197ef173c38023513157fa3c92e341036651f95a5218'


def sha_of(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()


def test_the_frozen_question_and_judgement_prompt_files_are_unchanged():
    for path, expected in FROZEN_FILES.items():
        with open(os.path.join(ROOT, path), 'rb') as handle:
            assert hashlib.sha256(handle.read()).hexdigest() == expected, f'{path} changed; steps 3 and 4 are frozen (D354)'


def test_the_code_written_parts_of_the_question_and_judgement_requests_are_unchanged():
    assert sha_of(judging.schema_for('judging-v7')) == JUDGING_SCHEMA_SHA
    questions = [jev_matching.relation_question('X'), jev_matching.member_question('X'), jev_matching.piece_question('X')]
    assert sha_of(questions) == MATCHER_QUESTIONS_SHA

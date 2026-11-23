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
from hivemind.views import jev_matching, judging, links  # noqa: E402

FROZEN_FILES = {
    'src/hivemind/prompts/collision-v2.txt': 'a5f0f58d53c4f4215b14e534935b1f95a79b35ba097d68c0ab598af7b88a3bd0',
    'src/hivemind/prompts/judging-v7.txt': 'd499c4b89ad038ade9bd41e037d766d5e54defecef273541f46dc01509db5a2c',
    'src/hivemind/prompts/matching-v3.txt': '04e23ee314e71cb094273b23e75f816c467176969b8c17dfec5a6e5d17a45a49',
    # D694: poc-v119's judge prompt is judging-v7's text byte for byte; only the code-built dependency block differs (tests/test_links.py)
    'src/hivemind/prompts/judging-v8.txt': 'd499c4b89ad038ade9bd41e037d766d5e54defecef273541f46dc01509db5a2c',
    # D713: judging-v12's prompt is judging-v7's text byte for byte; only its answer format closes the id fields
    'src/hivemind/prompts/judging-v12.txt': 'd499c4b89ad038ade9bd41e037d766d5e54defecef273541f46dc01509db5a2c',
}
JUDGING_SCHEMA_SHA = '4d1469ae9c14256c24e2c39e1b6cc772cb25e160c937f32091fc4f35bf539ca9'
CLOSED_FORMAT_SHA = '661782f2f9519f9bd8ab438bd636cade9e74a4102f6bfcf3ae1263fd31c57187'         # D713: judging-v12 on evidence e2, e10; dependency v3; theme v5
CLOSED_FORMAT_EMPTY_SHA = 'ea69bac9427b086bcd25becb7a3f72f2720c60b205effc208ced9b4c1979a585'   # D713: judging-v12 with no id listed in any field
MATCHER_QUESTIONS_SHA = '86cb70600ce456be3cd5197ef173c38023513157fa3c92e341036651f95a5218'
LINK_QUESTIONS_SHA = '4144f359701e0677159afb058701b721698ba3ae7bded61988de2f98f3c340b5'      # D694, D695: poc-v119's READS and SIGN questions
LINK_QUESTIONS_V2_SHA = '3fc3ffff5dc8437db05fcd8f6b0ef1043bf53c43f66734f4782c1517b666d47e'   # D705: poc-v120's links-v2 questions (WORDING-V2.md)


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


def test_the_linking_version_pins_its_questions_and_keeps_the_judge_schema():
    assert sha_of(judging.schema_for('judging-v8')) == JUDGING_SCHEMA_SHA
    questions = [links.reads_question('X'), links.sign_question('X', links.CANDIDATE_READS), links.sign_question('X', links.THESIS_READS)]
    assert sha_of(questions) == LINK_QUESTIONS_SHA
    version_two = [links.reads_question('X', version='links-v2'), links.sign_question('X', links.CANDIDATE_READS, version='links-v2'),
                   links.sign_question('X', links.THESIS_READS, version='links-v2')]
    assert sha_of(version_two) == LINK_QUESTIONS_V2_SHA


def test_the_citation_version_pins_its_closed_format_and_leaves_the_frozen_formats_alone():
    """D713: judging-v12's format on a fixed list and on empty lists is pinned; judging-v7's and judging-v8's formats are not moved."""
    assert judging.SUPPORTED_VERSIONS == ('judging-v7', 'judging-v8', 'judging-v12')
    assert sha_of(judging.schema_for('judging-v12', {'evidence': ['e2', 'e10'], 'dependencies': ['v3'], 'themes': ['v5']})) == CLOSED_FORMAT_SHA
    assert sha_of(judging.schema_for('judging-v12', {'evidence': [], 'dependencies': [], 'themes': []})) == CLOSED_FORMAT_EMPTY_SHA
    assert sha_of(judging.schema_for('judging-v7', {'evidence': ['e2'], 'dependencies': [], 'themes': []})) == JUDGING_SCHEMA_SHA

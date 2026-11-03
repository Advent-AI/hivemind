"""The extraction production prompt is frozen (D274, Alex 2026-11-03: "上一个版本是不是freeze作为我们的抽取生产提示词吧"): poc-v108, extraction v74i at
low reasoning. Every piece that shapes its request is pinned here: the role, the closing check, the category blocks, the configuration, the links rule
and the code-written takes lines, and the evidence schema. A change is a new version opened only by Alex's decision, never an edit of these."""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import extraction, placement  # noqa: E402

FROZEN_FILES = {
    'src/hivemind/prompts/role-v74i.txt': '12fb59cb8fccff9c176ea938549d47143bc1260322647afa38b81d44dbeef594',
    'src/hivemind/prompts/review-v74i.txt': '25f2d9b2166b9d603570338c5e9abc537cc083373566d87dc098929ea988dc66',
    'src/hivemind/prompts/categories-v74i.json': '2a694031b8feb8e1c1fb576e765528f32c3855f77ad9305741ee99dc36231057',
    'poc/config/poc-v108.json': 'e83e826351990cc1c98e2f14abc609e50858966ee1c3cfd748a1c0ec2151b38a',
}
FILING_RULE_SHA = 'ed22acea4f152ec8bf20e59fcf21cb8fa3620ce8fa6e0db94d4dd183437b8658'
TAKES_SHA = '0a4020e48b3c107302530762c433b8543e8859319924507fd6742aa30620c77e'
SCHEMA_SHA = '983d022b55fa003f1f0b462a9c983b63b77b2e8796f0525d1b9b65c7be84c4f5'
VIEWS = [{'view_id': 'v1', 'object_id': 'ABC', 'due_day': '2027-02-28', 'question': 'q', 'key': {'measure': 'segment_revenue', 'scope': 'Cloud', 'period_start': '2026-02-01', 'period_end': '2027-01-31'}},
         {'view_id': 'v2', 'object_id': 'ABC', 'due_day': '2027-02-28', 'question': 'q', 'key': {'measure': 'event', 'event_type': 'launch', 'scope': 'Model X'}},
         {'view_id': 'v3', 'object_id': 'ABC', 'due_day': '2027-02-28', 'question': 'q', 'key': {'measure': 'policy_event', 'scope': 'Export licence'}}]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def test_the_frozen_prompt_files_and_configuration_are_unchanged():
    moved = {path: sha(open(os.path.join(ROOT, path), 'rb').read()) for path in FROZEN_FILES}
    assert moved == FROZEN_FILES, 'a frozen file of the production extraction prompt changed (D274): open a new version instead'


def test_the_code_written_parts_of_the_frozen_request_are_unchanged():
    assert sha(placement.FILING_RULE_ROOT_FALLBACK.encode()) == FILING_RULE_SHA
    assert sha(json.dumps([placement.takes(v, True) for v in VIEWS]).encode()) == TAKES_SHA
    assert sha(json.dumps(extraction.schema_for('v74i', shown_view_ids=('v1',))).encode()) == SCHEMA_SHA
    assert extraction.PATHS_ONCE_VARIANTS == ('v74i',)


def test_the_replay_default_is_the_frozen_configuration():
    source = open(os.path.join(ROOT, 'scripts', 'replay.py'), encoding='utf-8').read()
    assert "default=os.path.join(ROOT, 'poc', 'config', 'poc-v108.json')" in source
    settings = json.load(open(os.path.join(ROOT, 'poc', 'config', 'poc-v108.json')))['extraction']
    assert {s['prompt_version'].split('-')[1] for s in settings.values()} == {'v74i'} and {s['reasoning_effort'] for s in settings.values()} == {'low'}

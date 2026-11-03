"""AGENTS §5 preflight: every archived extraction answer is replayed through the current checks with the configuration it was
sent under and the questions its stored request showed, after the request is checked against the source (a changed source is
refused); a long source is checked against the part production sends, and a row of a retired version or configuration is counted
and named, not fatal (2026-10-30 review; D354's defect that the preflight could not read the one-decider requests)."""
import importlib.util
import json
import sqlite3
from pathlib import Path

import pytest

from hivemind import config, extraction, model, universe

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('preflight', ROOT / 'scripts' / 'preflight.py')
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


SHOWN = [{'view_id': 'v1', 'object_id': 'NVDA', 'due_day': '2027-01-31', 'question': 'What will NVIDIA report as FY2027 revenue?',
          'key': {'measure': 'total_revenue', 'scope': 'total', 'period_start': '2026-02-01', 'period_end': '2027-01-31'}, 'groups': []}]


def archive_one(tmp_path, text='The company announced a financing arrangement on July 2, 2026.', config_name='poc-v108', shown=()):
    cfg = config.load(str(ROOT / f'poc/config/{config_name}.json'))
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    item = {'input_id': 'gnews:test-preflight', 'category': 'T7', 'publisher': 'example.com',
            'publisher_type': 'media', 'publication_day': '2026-07-02', 'title': 'Cloud financing', 'text': text,
            'object_identifiers': [{'kind': 'ticker', 'value': 'NVDA'}]}
    setting, system, user, schema = extraction.request_for(cfg, item, item['text'], list(shown), uni)
    request = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
    encoded, sha = model.request_identity(request)
    answer = {'candidates': [], 'new_groups': [], 'evidence': [{'id': 'e1', 'quote': item['text'][:60],
              'one_line': 'A financing arrangement was announced.', 'speaker': 'The company',
              'original_who': 'The company', 'original_day': '2026-07-02', 'tier': 'party_statement',
              'event_time': '2026-07-02', 'links': []}]}
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    archive.record(purpose='extract', config_version=cfg.version, config_checksum=cfg.checksum,
                   request_sha256=sha, request_json=encoded, answer_json=json.dumps(answer))
    items = sqlite3.connect(tmp_path / 'items.sqlite')
    items.row_factory = sqlite3.Row
    items.execute('create table items (input_id text, category text, publisher text, publisher_type text, publication_day text, title text, text text)')
    items.execute('insert into items values (?, ?, ?, ?, ?, ?, ?)', tuple(item[k] for k in
                  ('input_id', 'category', 'publisher', 'publisher_type', 'publication_day', 'title', 'text')))
    items.commit()
    return archive.conn, items, uni


@pytest.fixture
def archived_answer(tmp_path):
    return archive_one(tmp_path)


def test_the_replay_keeps_an_unlinked_statement_for_the_handover(archived_answer, capsys):
    archive, items, uni = archived_answer
    assert preflight.part_b(archive, items, uni) == 1
    assert 'evidence produced 1 kept 1' in capsys.readouterr().out


def test_the_replay_reads_the_questions_the_stored_request_showed(tmp_path):
    archive, items, uni = archive_one(tmp_path, shown=SHOWN)
    request_json = archive.execute("select request_json from model_calls").fetchone()[0]
    item = dict(items.execute('select * from items').fetchone(), object_identifiers=[])
    cfg = config.load(str(ROOT / 'poc/config/poc-v108.json'))
    assert preflight._preflight_extract_inputs(json.loads(request_json), item, cfg) == ('v74i', ['v1'])


def test_replay_refuses_changed_original_text(archived_answer):
    archive, items, uni = archived_answer
    items.execute("update items set text = text || ' Changed.'")
    items.commit()
    with pytest.raises(ValueError, match='source'):
        preflight.part_b(archive, items, uni)


def test_a_source_longer_than_the_request_limit_is_checked_against_the_part_production_sends(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(extraction, 'MAX_TEXT_CHARS', 80)
    archive, items, uni = archive_one(tmp_path, text='The company announced a financing arrangement on July 2, 2026. ' * 3)
    assert preflight.part_b(archive, items, uni) == 1
    assert 'unidentifiable 0' in capsys.readouterr().out


def test_a_row_of_a_retired_configuration_is_counted_not_fatal(tmp_path, capsys):
    archive, items, uni = archive_one(tmp_path)
    archive.execute("update model_calls set config_version='poc-v16-retired'")
    archive.commit()
    assert preflight.part_b(archive, items, uni) == 0
    assert 'not replayed: poc-v16-retired (configuration retired): 1' in capsys.readouterr().out


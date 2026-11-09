"""Checks of the D392 v108 control harness (control_v108.py, its docstring is the requirement):
(a) prepare seeds the 22 seed questions into a new ledger at the given time and refuses an existing folder;
(b) the reference-archive transport answers a byte-identical request with the stored response and refuses a request one byte off, in
    both call forms the pipeline uses (model: (provider, request); Jev: (request,));
(c) the dispatch guard refuses a day whose inputs arrive in another order than the reference manifest, before the day runner runs;
(d) live refuses to start without a passing proof of the same code and inputs in a sibling folder.
Real storage on temporary paths; fake transports only. tests/conftest.py does not reach this folder, so the credential readers are
replaced by a refusal here: a call that escapes its fake transport fails the test."""
import dataclasses
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT / 'src')]
import control_v108  # noqa: E402
from hivemind import config, dispatch, jev, model, parallel_day  # noqa: E402
from hivemind.views import store  # noqa: E402

SEED = ROOT / 'poc/seeds/nvda-2026-07-01-v2.json'
CONFIG = ROOT / 'poc/config/poc-v108.json'
SYSTEM = 'You judge whether the evidence moves the question. Answer in the schema.'
USER = 'Question v1: NVIDIA fiscal 2027 total revenue. Evidence e1 (2026-07-01, Reuters): data center bookings rose 12% quarter on quarter.'
SCHEMA = {'type': 'object', 'properties': {'verdict': {'type': 'string', 'enum': ['supports', 'weakens', 'neither']}},
          'required': ['verdict'], 'additionalProperties': False}
JEV_STATE = 'Statement A (2026-07-01): NVIDIA guided Q2 revenue to $45B. Statement B (2026-07-02): NVIDIA expects about $45B in Q2.'
JEV_QUESTIONS = {'same_statement': {'type': 'noul', 'question': 'Do A and B report the same guidance?'}}


@pytest.fixture(autouse=True)
def no_credentials(monkeypatch):
    def refuse(*arguments):          # pytest.fail raises a BaseException, which the pipeline's `except Exception` cannot record
        pytest.fail('a test read a credential: a model or Jev call escaped its fake transport')
    monkeypatch.setattr(model, '_key', refuse)
    monkeypatch.setattr(jev, '_key', refuse)


def test_prepare_seeds_the_22_questions_into_a_new_ledger_and_refuses_an_existing_folder(tmp_path):
    """Requirement 1 (prepare)."""
    paths = control_v108.prepare(tmp_path / 'control', created_at='2026-07-01T00:00:00Z', seed_path=SEED)
    conn = store.open_db(str(paths.views))
    rows = conn.execute('select view_id, created_from_input, created_seq, created_at from views').fetchall()
    assert sorted(row['view_id'] for row in rows) == sorted(q['view_id'] for q in json.loads(SEED.read_text())['questions'])
    assert len(rows) == 22 and sorted(store.open_views(conn)) == sorted(row['view_id'] for row in rows)
    assert {(row['created_from_input'], row['created_seq'], row['created_at']) for row in rows} == {('seed:nvda-2026-07-01-v2.json', 0, '2026-07-01T00:00:00Z')}
    assert not paths.archive.exists()
    with pytest.raises(FileExistsError):
        control_v108.prepare(tmp_path / 'control', created_at='2026-07-01T00:00:00Z', seed_path=SEED)


def stored_reference_archive(tmp_path):
    """A reference archive written by the production call paths: one judgement call and one Jev call, each through a fake provider."""
    cfg = config.load(str(CONFIG))
    reference = model.Archive(str(tmp_path / 'reference.sqlite'))

    def provider(provider_name, request):
        return {'id': 'chatcmpl-ref-1', 'object': 'chat.completion', 'model': 'gpt-6-luna',
                'choices': [{'message': {'role': 'assistant', 'content': json.dumps({'verdict': 'supports'})}}],
                'usage': {'prompt_tokens': 1240, 'completion_tokens': 85}}

    def jev_provider(request):
        return {'model': request['model'], 'answers': {'same_statement': {'type': 'noul', 'noul': 0.93}}, 'usage': {'input_tokens': 310, 'output_tokens': 0}}
    model.call(reference, cfg, cfg.rejudging, SYSTEM, USER, SCHEMA, 'judgement', 'judge', transport=provider)
    jev.ask(reference, cfg, cfg.matching, JEV_STATE, JEV_QUESTIONS, 'match', transport=jev_provider)
    reference.conn.close()
    return cfg


def test_the_archive_transport_answers_the_identical_request_and_refuses_one_byte_off(tmp_path):
    """Requirement 2, requests: a byte-identical request is answered from the reference archive; one changed byte is a refusal naming it."""
    cfg = stored_reference_archive(tmp_path)
    transport = control_v108.ReferenceArchiveTransport(tmp_path / 'reference.sqlite')
    replay_archive = model.Archive(str(tmp_path / 'replay.sqlite'))

    answer = model.call(replay_archive, cfg, cfg.rejudging, SYSTEM, USER, SCHEMA, 'judgement', 'judge', transport=transport)
    jev_answer = jev.ask(replay_archive, cfg, cfg.matching, JEV_STATE, JEV_QUESTIONS, 'match', transport=transport)
    assert (answer.data, answer.cached) == ({'verdict': 'supports'}, False)
    assert jev_answer.data['same_statement']['noul'] == 0.93 and sum(transport.matched.values()) == 2

    one_byte_off = USER[:-1] + '!'
    off_sha = model.request_identity(model.build_request(cfg.rejudging, SYSTEM, one_byte_off, SCHEMA, 'judgement', cfg.provider))[1]
    with pytest.raises(control_v108.ReferenceMissError, match=off_sha):
        model.call(replay_archive, cfg, cfg.rejudging, SYSTEM, one_byte_off, SCHEMA, 'judgement', 'judge', transport=transport)
    jev_off_state = JEV_STATE[:-1] + '!'
    with pytest.raises(control_v108.ReferenceMissError, match='jev'):
        jev.ask(replay_archive, cfg, cfg.matching, jev_off_state, JEV_QUESTIONS, 'match', transport=transport)
    assert [miss[0] for miss in transport.misses][0] == off_sha and len(transport.misses) == 2


def realistic_item(input_id, published_at, publisher, title):
    return {'input_id': input_id, 'publisher': publisher, 'published_at': published_at, 'publication_day': published_at[:10],
            'category': 'news', 'klass': '媒体报道', 'source_uri': f'https://news.example.com/{input_id.split(":")[1]}', 'title': title,
            'text': f'{title}. NVIDIA shares moved after the report.', 'object_identifiers': [{'kind': 'ticker', 'value': 'NVDA'}]}


def test_the_dispatch_guard_refuses_a_reordered_day_before_the_day_runner_runs(tmp_path):
    """Requirement 2, dispatch: a day's routed inputs must equal the reference manifest in order; the reference hash is parallel_day.item_key."""
    items = [realistic_item('gnews:87607a311ad24b410c6ef85a', '2026-07-01T08:15:00Z', 'Reuters', 'NVIDIA unveils capital partners for AI buildout'),
             realistic_item('gnews:1fe368a4d9fafb59b11e7aba', '2026-07-01T11:40:00Z', 'Bloomberg', 'Data center orders climb into the third quarter'),
             realistic_item('gnews:5c0d2e91b7a44f03a8e1c6d2', '2026-07-01T16:05:00Z', 'CNBC', 'Analysts lift fiscal 2027 revenue estimates')]
    manifest_dir = tmp_path / 'manifests'
    manifest_dir.mkdir()
    (manifest_dir / 'day-2026-07-01.json').write_text(json.dumps({'day': '2026-07-01', 'inputs': [
        {'input_id': item['input_id'], 'seq': position, 'hash': parallel_day.item_key(item)} for position, item in enumerate(items, start=1)]}))
    days_run = []

    def production_day_runner(conn, archive, cfg, universe, day_items, *, day, transport=None, log=print):
        days_run.append([item['input_id'] for item, _ in day_items])
        return iter(())
    guard = control_v108.ReferenceInputsGuard(production_day_runner, manifest_dir)

    in_reference_order = [(item, dispatch.Route('extract', sequence_no=position)) for position, item in enumerate(items, start=1)]
    guard(None, None, None, None, in_reference_order, day='2026-07-01')
    assert days_run == [[item['input_id'] for item in items]]

    arrived_reordered = [(item, dispatch.Route('extract', sequence_no=position)) for position, item in enumerate([items[0], items[2], items[1]], start=1)]
    with pytest.raises(control_v108.InputsMismatchError, match='input 1'):
        guard(None, None, None, None, arrived_reordered, day='2026-07-01')
    assert len(days_run) == 1


def test_live_refuses_to_start_without_a_passing_proof_beside_it(tmp_path):
    """Requirement 3: no sibling proof of this code and these inputs, no live run (and no folder, no credential read)."""
    reference_run = tmp_path / 'reference-run'
    reference_run.mkdir()
    (reference_run / 'archive.sqlite').write_bytes(b'reference archive bytes')
    items_database = tmp_path / 'items.sqlite'
    items_database.write_bytes(b'items database bytes')
    inputs = dataclasses.replace(control_v108.ControlInputs(), reference_run=reference_run, items_database=items_database)
    runs = tmp_path / 'runs'
    runs.mkdir()
    stale_proof = runs / 'prove-earlier'
    stale_proof.mkdir()
    (stale_proof / control_v108.PROOF_MARKER).write_text(json.dumps({'passed': True, 'code_digest': '0' * 64,
                                                                      'inputs': control_v108.input_digests(inputs)}))

    with pytest.raises(control_v108.ProofMissingError):
        control_v108.run_live(runs / 'live-1', 2.0, inputs=inputs)
    assert not (runs / 'live-1').exists()

    current_proof = runs / 'prove-today'
    current_proof.mkdir()
    (current_proof / control_v108.PROOF_MARKER).write_text(json.dumps({'passed': True, 'code_digest': control_v108.code_digest(ROOT),
                                                                        'inputs': control_v108.input_digests(inputs)}))
    assert control_v108.find_sibling_proof(runs / 'live-1', inputs) == current_proof / control_v108.PROOF_MARKER


def test_the_live_transport_passes_every_first_day_request_unchanged_within_its_cap(tmp_path):
    """Requirement 3 (live) with its hard cap (budget.py): the live run's transport is the spending limit around the production
    transports. Here the limit wraps the reference archive in both call forms over the first reference day, so every request it lets
    through must be byte-identical to production's and the counted spend must stay within the cap."""
    import budget
    inputs = dataclasses.replace(control_v108.ControlInputs(), until_day='2026-07-01')
    reference = control_v108.ReferenceArchiveTransport(inputs.reference_run / 'archive.sqlite')
    limit = budget.Budget(3.0, attempt=reference, jev_transport=reference)
    paths = control_v108.prepare(tmp_path / 'control', created_at=inputs.seed_created_at, seed_path=inputs.seed_path)
    guard = control_v108.guarded_day_runner(paths, inputs)
    control_v108.run_control(paths, inputs, guard, transport=limit, spend_cap_usd=3.0, log=lambda *parts: None)
    assert not reference.misses and sum(reference.matched.values()) > 0
    assert 0 < limit.spent_usd <= 3.0 and limit.reserved_usd == pytest.approx(0, abs=1e-12)

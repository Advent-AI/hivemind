"""D162 state and value tables, using real stored articles and temporary SQLite databases."""
import copy
import json
import sys
from pathlib import Path

import pytest

import ohio_sequence as ohio
import source_first as split

sys.path.insert(0, str(ohio.ROOT / 'src'))
from hivemind.model import PRICES  # noqa: E402

# the fake transport answers with 200 prompt and 100 completion tokens a call; the expected cost follows the price table
# (published gpt-6-luna rates since 2026-10-25, build-log row 28), never a literal
COST_PER_CALL = 200 / 1e6 * PRICES['gpt-6-luna'][0] + 100 / 1e6 * PRICES['gpt-6-luna'][1]

OLD = ohio.ROOT / 'poc/reports/2026-10-25-extraction-evidence-01'
NEW = ohio.ROOT / 'poc/reports/2026-10-25-source-first-01'


def parts(raw):
    source = {'observations': [{k: copy.deepcopy(v) for k, v in e.items() if k != 'links'} for e in raw['evidence']]}
    organised = {'candidates': [{k: copy.deepcopy(v) for k, v in c.items() if k != 'evidence_ids'} for c in raw['candidates']],
                 'threads': copy.deepcopy(raw['threads']),
                 'dispositions': {e['id']: {'links': copy.deepcopy(e['links']), 'omit_reason': ''} for e in raw['evidence']}}
    return source, organised


def responses(values, requests):
    answers = iter(values)
    def send(provider, request):
        requests.append(copy.deepcopy(request))
        return {'choices': [{'message': {'content': json.dumps(next(answers), ensure_ascii=False)}}],
                'usage': {'prompt_tokens': 200, 'completion_tokens': 100}}
    return send


def test_d162_every_stored_answer_roundtrips_without_changing_evidence():
    """Value table: source fields and both evidence-relation readers stay identical across all 18 answers."""
    files = sorted(OLD.glob('*/item*/extraction.json'))
    assert len(files) == 18
    for path in files:
        raw = ohio.read(path)
        source, organised = parts(raw)
        assert split.assemble(source, organised, ohio.read(path.parent / 'context.json')['offered']) == raw


@pytest.mark.parametrize('breach', ['missing', 'extra', 'both', 'neither', 'duplicate_relation'])
def test_d162_incomplete_or_contradictory_disposition_refuses(breach):
    """Closed disposition contract: one explicit decision per source item, one relationship owner."""
    source, organised = parts(ohio.read(OLD / 'control-1/item1/extraction.json'))
    if breach == 'missing':
        del organised['dispositions']['e1']
    elif breach == 'extra':
        organised['dispositions']['e999'] = {'links': [], 'omit_reason': 'not relevant'}
    elif breach == 'both':
        organised['dispositions']['e1']['omit_reason'] = 'not relevant'
    elif breach == 'neither':
        organised['dispositions']['e1']['links'] = []
    else:
        organised['candidates'][0]['evidence_ids'] = ['e2']
    with pytest.raises(ohio.Refused):
        split.assemble(source, organised, [])


def test_d162_omission_and_reassignment_have_one_source_of_truth():
    """Value table: candidate evidence is derived from links even when a source item is omitted or reassigned."""
    source, organised = parts(ohio.read(OLD / 'control-1/item1/extraction.json'))
    organised['dispositions']['e1'] = {'links': [], 'omit_reason': 'same fact already covered by e2'}
    organised['dispositions']['e2']['links'] = ['c2']
    result = split.assemble(source, organised, [])
    assert [(c['id'], c['evidence_ids']) for c in result['candidates']] == [('c1', []), ('c2', ['e2'])]
    assert result['evidence'] == [dict(source['observations'][1], links=['c2'])]


def test_d162_prepared_entry_point_keeps_control_and_runs_two_steps(monkeypatch, tmp_path):
    """State table: all three articles run, control stays single-step, two-step source/cost/history are real."""
    out = tmp_path / 'run'
    out.mkdir()
    (out / 'preflight.txt').write_text('Controlled external service; no credentials or network.')
    split.prepare(out, source_role_path=NEW / 'read-source.txt', organiser_role_path=NEW / 'organise-source.txt',
                  control_role_path=OLD / 'role-evidence.txt', design_path=ohio.ROOT / 'docs/research/2026-10-25-source-first.md')
    sent = {}
    def factory(folder, label, deadline):
        values = []
        for n in (1, 2, 3):
            raw = ohio.read(OLD / f'control-1/item{n}/extraction.json')
            values.extend(parts(raw) if label.startswith('grouped') else [raw])
            values.append(ohio.read(OLD / f'control-1/item{n}/matching.json')['answer'])
        sent[label] = []
        return responses(values, sent[label])
    monkeypatch.setattr(ohio, 'BoundedTransport', factory)
    with pytest.raises(ValueError, match='dedicated reader'):
        ohio.run(out)
    assert sent == {}
    split.run(out)
    assert set(ohio.read(out / 'status.json').values()) == {'complete'}
    for label, requests in sent.items():
        assert len(requests) == (9 if label.startswith('grouped') else 6)
        if label.startswith('grouped'):
            first = json.loads(requests[0]['messages'][1]['content'])
            second = json.loads(requests[1]['messages'][1]['content'])
            assert first['text'] == ohio.read(out / 'items.json')[0]['text']
            assert 'text' not in second and second['observations'] == parts(ohio.read(OLD / 'control-1/item1/extraction.json'))[0]['observations']
            assert requests[0]['messages'][0]['content'] == (NEW / 'read-source.txt').read_text()
            assert requests[1]['messages'][0]['content'] == (NEW / 'organise-source.txt').read_text() + '\n\n' + ohio.GROUP_PROMPT
            assert ohio.read(out / label / 'item1/reader-calls.json')['organisation']['call_id'] == 2
            handover = ohio.read(out / label / 'item1/handover.json')
            assert handover['call_id'] == 2 and handover['cost_usd'] == pytest.approx(2 * COST_PER_CALL)
        else:
            assert requests[0]['messages'][0]['content'] == (OLD / 'role-evidence.txt').read_text() + '\n\n' + ohio.GROUP_PROMPT
        assert len(ohio.read(out / label / 'item3/result.json')['snapshot']['thread_members']) == 2


@pytest.mark.parametrize('event', ['empty', 'failure'])
def test_d162_source_only_terminal_outcomes(tmp_path, event):
    """State table: empty selection binds its real source call; organisation failure writes no product state."""
    conn = ohio.groups.open_db(tmp_path / 'views.sqlite')
    archive = model_archive = ohio.model.Archive(str(tmp_path / 'calls.sqlite'))
    item = ohio.read(OLD / 'items.json')[0]
    requests = []
    source = {'observations': []} if event == 'empty' else parts(ohio.read(OLD / 'control-1/item1/extraction.json'))[0]
    first = responses([source], requests)
    def send(provider, request):
        if requests:
            raise TimeoutError('controlled organisation failure')
        return first(provider, request)
    kwargs = dict(conn=conn, archive=archive, cfg=ohio.config.load(OLD / 'config.json'), uni=ohio.universe.load(OLD / 'universe.json'),
                  item=item, grouped=True, directory=tmp_path / 'item1', transport=send,
                  role_text=(NEW / 'organise-source.txt').read_text(), reader=split.SourceFirstReader((NEW / 'read-source.txt').read_text()))
    try:
        if event == 'failure':
            with pytest.raises(TimeoutError, match='controlled organisation failure'):
                ohio.process(**kwargs)
            assert conn.execute('select count(*) from handovers').fetchone()[0] == 0
        else:
            ohio.process(**kwargs)
            handover = ohio.read(tmp_path / 'item1/handover.json')
            assert handover['call_id'] == 1 and handover['cost_usd'] == pytest.approx(COST_PER_CALL)
            assert ohio.read(tmp_path / 'item1/reader-calls.json')['organisation'] is None
        assert conn.execute('select count(*) from views').fetchone()[0] == 0
        assert model_archive.conn.execute('select count(*) from model_calls').fetchone()[0] == 1
        assert len(requests) == 1
    finally:
        conn.close()
        archive.conn.close()

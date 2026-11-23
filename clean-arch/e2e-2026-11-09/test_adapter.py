"""Stage 0 checks of the D392 adapter (plan v4, 'Adapter') on a constructed seeded case: the stored c8 dev draw with three clean theses
relabelled as seeds (clean-1 -> v9, clean-2 -> v1, clean-3 -> v8). A fake judge answers; no model is called."""
import hashlib, json, sqlite3, subprocess, sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT / 'src')]
import adapter  # noqa: E402

DRAW = ROOT / 'poc/data/clean-step1-c8-dev-d1-2026-11-09'
RELABEL = {'clean-1': 'v9', 'clean-2': 'v1', 'clean-3': 'v8'}


@pytest.fixture
def constructed(tmp_path, monkeypatch):
    step1_records = adapter._step1_records()
    def relabelled(trace):
        articles, questions, opened = step1_records(trace)
        for article in articles:
            for record in article:
                record['thesis_ids'] = [RELABEL.get(t, t) for t in record['thesis_ids']]
        return articles, questions, opened
    monkeypatch.setattr(adapter, '_step1_records', lambda: relabelled)
    library = json.loads((DRAW / 'step2/library.json').read_text())
    for group in library['groups'].values():
        for copy in [group['original'], *group['members']]:
            copy['thesis_ids'] = [RELABEL.get(t, t) for t in copy['thesis_ids']]
    for entry in library['later_log']:
        entry['thesis'] = RELABEL.get(entry['thesis'], entry['thesis'])
    folder = tmp_path / 'step2'
    folder.mkdir()
    (folder / 'library.json').write_text(json.dumps(library))
    stamp(folder)
    return folder, library


def stamp(folder):
    digests = [hashlib.sha256(path.read_bytes()).hexdigest() for path in (DRAW / 'trace.sqlite', folder / 'library.json')]
    (folder / 'inputs.sha256').write_text(f'{digests[0]}  trace.sqlite\n{digests[1]}  step2/library.json\n')


def fake_judge(provider, request):
    shown = adapter.SHOWN_EVIDENCE.findall(request['messages'][-1]['content'])
    answer = {'rung': 1, 'reference': 'consensus as stated', 'implied_outcome': 'the figure the evidence implies', 'reasons': 'test',
              'cites': shown[:1], 'cites_views': [], 'pushes': [], 'changed': True, 'why_changed': 'test', 'theme_pushes': []}
    return {'choices': [{'message': {'content': json.dumps(answer)}}], 'usage': {'prompt_tokens': 1000, 'completion_tokens': 100}}


def test_replay_judges_linked_seeds_day_by_day_and_the_frozen_scorer_reads_it(tmp_path, constructed):
    # plan v4 'Adapter' 1-3: chronological insertion, judging once per day for views with a new link, the scorer's input
    result = adapter.replay(DRAW / 'trace.sqlite', constructed[0], tmp_path / 'out', transport=fake_judge)
    conn = sqlite3.connect(tmp_path / 'out/views.sqlite')
    assert result.counts['judgements'] > 0 and result.counts['links written'] > 0
    assert {v for (v,) in conn.execute('select distinct view_id from judgements')} <= {'v1', 'v8', 'v9'}
    days = [d for (d,) in conn.execute('select publication_day from judgements order by judgement_id')]
    assert days == sorted(days)
    for request in result.sent:
        assert all(conn.execute('select created_seq from evidence where evidence_id=?', (e,)).fetchone()[0] <= request['seq'] for e in request['shown'])
    scored = subprocess.run([sys.executable, str(ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py'), str(tmp_path / 'out')],
                            capture_output=True, text=True)
    assert scored.returncode == 0, scored.stderr
    assert 'q01' in scored.stdout


def test_a_revision_runs_from_the_revised_groups_original_to_the_record_that_brought_it(tmp_path, constructed):
    # plan v4 qualification: how several revisions map into the judge's fields; library.py:72-74 stores {'group': revised, 'by': record}
    folder, library = constructed
    result = adapter.replay(DRAW / 'trace.sqlite', folder, tmp_path / 'out', transport=fake_judge)
    conn = sqlite3.connect(tmp_path / 'out/views.sqlite')
    expected = {(result.evidence_of[library['groups'][r['group']]['original']['id']], result.evidence_of[r['by']])
                for g in library['groups'].values() for r in g['revises']}
    assert len(expected) == 11
    assert set(conn.execute('select old_evidence_id, new_evidence_id from revisions')) == expected
    for old, new in expected:   # the new piece inherits the old piece's seed links (writing.py:256-261)
        old_views = {v for (v,) in conn.execute('select view_id from evidence_links where evidence_id=?', (old,))}
        new_views = {v for (v,) in conn.execute('select view_id from evidence_links where evidence_id=?', (new,))}
        assert old_views <= new_views


def test_a_future_record_before_judging_is_refused(tmp_path, constructed, monkeypatch):
    original = adapter.Adapter.judge
    def plant_then_judge(self, day, seq, changed):
        adapter.store.add_evidence(self.conn, evidence_id='e999999', quote='x', one_line='x', speaker='', original_who='', original_day='',
                                   tier='fact', event_time=None, seq=seq + 1, input_id='future')
        return original(self, day, seq, changed)
    monkeypatch.setattr(adapter.Adapter, 'judge', plant_then_judge)
    with pytest.raises(adapter.Leak):
        adapter.replay(DRAW / 'trace.sqlite', constructed[0], tmp_path / 'out', transport=fake_judge)


def test_judging_stops_at_its_cap(tmp_path, constructed):
    with pytest.raises(adapter.budget.OverBudget):
        adapter.replay(DRAW / 'trace.sqlite', constructed[0], tmp_path / 'out', transport=fake_judge, cap_usd=0.0001)


def test_a_library_from_another_draw_is_refused(tmp_path, constructed):
    folder, library = constructed
    group = next(g for g in library['groups'].values() if g['members'])
    group['members'][0]['summary'] += ' (another draw)'
    (folder / 'library.json').write_text(json.dumps(library))
    stamp(folder)
    with pytest.raises(SystemExit, match='not this draw'):
        adapter.replay(DRAW / 'trace.sqlite', folder, tmp_path / 'out', transport=fake_judge)


def test_concurrent_judging_never_spends_past_its_cap(tmp_path, constructed, monkeypatch):
    # every call reserves its worst case before it is sent, so what was spent and what was in flight stay within the cap
    cap = 0.05
    seen = []
    original = adapter.Adapter.judge
    def tracking(self, day, seq, changed):
        seen.append(self)
        return original(self, day, seq, changed)
    monkeypatch.setattr(adapter.Adapter, 'judge', tracking)
    with pytest.raises(adapter.budget.OverBudget):
        adapter.replay(DRAW / 'trace.sqlite', constructed[0], tmp_path / 'out', transport=expensive_judge, cap_usd=cap)
    assert len(seen[-1].sent) >= 3 and seen[-1].budget.spent_usd <= cap and seen[-1].budget.reserved_usd == pytest.approx(0, abs=1e-12)


def expensive_judge(provider, request):
    response = fake_judge(provider, request)
    response['usage'] = {'prompt_tokens': 20000, 'completion_tokens': 10000}   # about $0.007 a call at gpt-6-luna's rates
    return response


def test_a_library_changed_after_the_launcher_stamped_it_is_refused(tmp_path, constructed):
    folder, library = constructed
    library['later_log'] = []
    (folder / 'library.json').write_text(json.dumps(library))
    with pytest.raises(SystemExit, match='does not name this trace'):
        adapter.replay(DRAW / 'trace.sqlite', constructed[0], tmp_path / 'out', transport=fake_judge)


def test_every_attempt_is_charged_and_production_retry_rule_holds():
    # a lost answer may be billed: each failed attempt is charged its full reserve; HTTP 400 is not retried (model.openai_transport)
    attempts = []
    def flaky(provider, request):
        attempts.append(1)
        if len(attempts) < 3:
            raise adapter.model.TransportError('timed out')
        return fake_judge(provider, request)
    limit = adapter.budget.Budget(1.0, attempt=flaky, sleep=lambda seconds: None)
    request = {'model': 'gpt-6-luna', 'max_completion_tokens': 16000, 'messages': [{'role': 'user', 'content': 'x' * 1000}]}
    reserve = adapter.budget.worst_cost(request)
    limit.send('openai', request)
    assert len(attempts) == 3 and limit.spent_usd == pytest.approx(2 * reserve + adapter.budget.cost(request, fake_judge('openai', request)))
    def refused(provider, request):
        attempts.append(1)
        failure = adapter.model.TransportError('HTTP 400: bad request')
        failure.http_status = 400
        raise failure
    limit.attempt, attempts[:] = refused, []
    with pytest.raises(adapter.model.TransportError):
        limit.send('openai', request)
    assert len(attempts) == 1 and limit.reserved_usd == pytest.approx(0, abs=1e-12)


def test_an_answer_without_usable_usage_is_charged_its_full_reserve():
    limit = adapter.budget.Budget(1.0, attempt=lambda provider, request: {'choices': fake_judge(provider, request)['choices']})
    request = {'model': 'gpt-6-luna', 'max_completion_tokens': 16000, 'messages': [{'role': 'user', 'content': 'x' * 1000}]}
    limit.send('openai', request)
    assert limit.spent_usd == pytest.approx(adapter.budget.worst_cost(request))


def test_a_continued_trace_reads_as_one_draw(tmp_path, constructed):
    # a run stopped after article 40 and continued as a segment from that state reads exactly as the unbroken run
    # (run_forward.step1_records' '+' convention): the same days and opened theses, and no article left failed
    import sqlite3 as sq
    first, segment = tmp_path / 'first.sqlite', tmp_path / 'segment.sqlite'
    for target, keep in ((first, 'sequence <= 41'), (segment, 'sequence > 40')):
        source = sq.connect(DRAW / 'trace.sqlite')
        source.execute(f"vacuum into '{target}'")
        source.close()
        copy = sq.connect(target)
        copy.execute(f'delete from trace where not ({keep})')
        copy.execute("update trace set status='failed' where sequence=41 and ? like '%first.sqlite'", (str(target),))
        copy.commit()
        copy.close()
    whole = adapter.trace_articles(DRAW / 'trace.sqlite')
    joined = adapter.trace_articles(f'{first}+{segment}')
    assert joined == whole and joined[2] == []
    only_first = adapter.trace_articles(first)
    assert len(only_first[0]) == 40 and only_first[2] == [41]



@pytest.fixture
def unseeded(tmp_path):
    """The stored dev-d1 draw as it is: an unseeded c8 run whose theses are clean-1..clean-8, with its library stamped."""
    folder = tmp_path / 'step2'
    folder.mkdir()
    (folder / 'library.json').write_text((DRAW / 'step2/library.json').read_text())
    stamp(folder)
    return folder


DEV_D1_MAPPING = {'clean-2': 'v7', 'clean-3': 'v8', 'clean-4': 'v13', 'clean-5': 'v18'}   # MATCHING-v2.md, the dev-d1 row


def test_an_unseeded_run_feeds_only_its_matched_theses_to_the_ruler_views(tmp_path, unseeded):
    # D395: matched clean theses feed the ruler question's view; every other clean thesis's links are dropped; the scorer reads it
    result = adapter.replay(DRAW / 'trace.sqlite', unseeded, tmp_path / 'out', transport=fake_judge, mapping=DEV_D1_MAPPING)
    conn = sqlite3.connect(tmp_path / 'out/views.sqlite')
    linked_views = {v for (v,) in conn.execute('select distinct view_id from evidence_links')}
    assert linked_views and linked_views <= set(DEV_D1_MAPPING.values())
    assert {v for (v,) in conn.execute('select distinct view_id from judgements')} <= set(DEV_D1_MAPPING.values())
    assert result.counts['links through a matched clean thesis'] > 0 and result.counts['links to other clean-opened theses dropped'] > 0
    scored = subprocess.run([sys.executable, str(ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py'), str(tmp_path / 'out')],
                            capture_output=True, text=True)
    assert scored.returncode == 0, scored.stderr
    assert conn.execute("select count(*) from views where view_id='v23'").fetchone()[0] == 1   # all 23 ruler views exist (MATCHING-v2 §4)


def test_a_thesis_matched_to_two_ruler_questions_feeds_both(tmp_path, unseeded):
    adapter.replay(DRAW / 'trace.sqlite', unseeded, tmp_path / 'out', transport=fake_judge, mapping={'clean-4': ['v4', 'v13']})
    conn = sqlite3.connect(tmp_path / 'out/views.sqlite')
    v4 = {e for (e,) in conn.execute("select evidence_id from evidence_links where view_id='v4'")}
    v13 = {e for (e,) in conn.execute("select evidence_id from evidence_links where view_id='v13'")}
    assert v4 and v4 == v13


def test_a_mapping_to_q23_creates_the_ruler_question_the_scorer_finds(tmp_path, unseeded):
    adapter.replay(DRAW / 'trace.sqlite', unseeded, tmp_path / 'out', transport=fake_judge, mapping={'clean-1': 'v23'})
    conn = sqlite3.connect(tmp_path / 'out/views.sqlite')
    question, = conn.execute("select question from views where view_id='v23'").fetchone()
    assert question == "Will NVIDIA sign a guarantee of OpenAI's Ohio data-center lease by 2027-06-30?"
    assert [r for (r,) in conn.execute("select label from rungs where view_id='v23' order by position")] == ['Yes', 'No']
    assert conn.execute("select count(*) from evidence_links where view_id='v23'").fetchone()[0] > 0


def test_a_mapping_naming_an_unopened_thesis_or_a_non_ruler_view_is_refused(tmp_path, unseeded):
    with pytest.raises(SystemExit, match='not a thesis this run opened'):
        adapter.replay(DRAW / 'trace.sqlite', unseeded, tmp_path / 'a', transport=fake_judge, mapping={'clean-99': 'v7'})
    with pytest.raises(SystemExit, match='not a ruler question view'):
        adapter.replay(DRAW / 'trace.sqlite', unseeded, tmp_path / 'b', transport=fake_judge, mapping={'clean-2': 'clean-2'})


def test_an_unseeded_draw_with_no_match_is_still_judged_in_mapping_mode(tmp_path, unseeded):
    # MATCHING-v2: an empty set of matches is a valid outcome; every clean link is dropped and all 23 ruler views exist
    result = adapter.replay(DRAW / 'trace.sqlite', unseeded, tmp_path / 'out', transport=fake_judge, mapping={})
    conn = sqlite3.connect(tmp_path / 'out/views.sqlite')
    assert conn.execute('select count(*) from evidence_links').fetchone()[0] == 0 and result.counts['judgements'] == 0
    assert conn.execute("select count(*) from views where view_id='v23'").fetchone()[0] == 1

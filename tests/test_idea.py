import re
"""The idea card in two model calls with the service in between (docs/poc/idea-card.md, D112, D135), on the sealed
ledger with the model scripted: the bundle is the shape the mock reads; call 1's parts drive one real search each;
call 2 may map only candidates; the dependency graph adds upstream and downstream views; the claim is evaluated by
code and needs an amount in the idea; no model call when no view is recorded; the HTTP route answers as a user
starts the server.

Run: python3 -m pytest tests/test_idea.py -q
"""
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import bundle, config, idea, idea_composite, model, search, service  # noqa: E402
from hivemind.views import store  # noqa: E402

LEDGER = os.path.join(ROOT, 'poc', 'data', 'sealed-2026-10-24-run3-through-0815', 'views.sqlite')
ITEMS = os.path.join(ROOT, 'poc', 'data', 'items-window.sqlite')
UNIVERSE = os.path.join(ROOT, 'poc', 'universe.json')
CONFIG = os.path.join(ROOT, 'poc', 'config', 'poc-v7.json')
MOCK_DATA = os.path.join(ROOT, 'poc', 'mock', 'data.json')
IDEA = "Can NVIDIA's data center revenue top $300B this year?"


@pytest.fixture(scope='module')
def ledger():
    return service.open_ledger(LEDGER)


@pytest.fixture(scope='module')
def items():
    return store.open_read_only(ITEMS)


@pytest.fixture
def index(ledger, tmp_path):
    conn = search.open_index(str(tmp_path / 'index.sqlite'))
    search.build_index(ledger, conn, embed=search.fake_embed, embedding_model='fake')
    return conn


def scripted(decompose, mapping):
    """A transport answering call 1 with `decompose` and call 2 with `mapping(request)` (a function of the request,
    so a test can map ids the service actually offered); keeps every request."""
    requests = []

    def transport(provider, request):
        requests.append(json.loads(json.dumps(request)))
        answer = decompose if len(requests) == 1 else mapping(request)
        return {'choices': [{'message': {'content': json.dumps(answer, ensure_ascii=False)}}], 'usage': {'prompt_tokens': 1000, 'completion_tokens': 100}}
    return transport, requests


DECOMPOSED = {'parts': [{'object': 'NVDA', 'looks_for': 'FY2027 data center revenue', 'period': 'FY2027', 'query': 'NVIDIA FY2027 data center revenue'},
                        {'object': 'ai-capex', 'looks_for': 'hyperscaler capex', 'period': '2026', 'query': '云厂商 2026 资本开支'},
                        {'object': 'MU', 'looks_for': 'HBM share; the library has no Micron view', 'period': '2026', 'query': 'Micron HBM'}],
              'claim': {'part': 0, 'comparator': '>=', 'value_usd': 300e9}}


def offered(request):
    """The candidates call 2 was given, per part, read back from the request (briefs under the idea-v7 contract,
    ids under idea-v8)."""
    body = request['messages'][1]['content']
    end = body.index('\n\nThe candidates, each once:') if 'The candidates, each once:' in body else body.index("\n\nThe idea's own search results")
    parts = json.loads(body[body.index('[', body.index('Parts and the')):end])
    return {p['index']: [c['view_id'] if isinstance(c, dict) else c for c in p['candidates']] for p in parts}


def test_bundle_is_the_shape_the_mock_reads(ledger, items):
    with open(MOCK_DATA, encoding='utf-8') as handle:
        mock = {v['view_id']: v for v in json.load(handle)['views']}
    item_of = bundle.item_lookup(items)

    def projected(ours, theirs):
        if isinstance(theirs, dict):
            assert set(theirs) <= set(ours), set(theirs) - set(ours)
            return {k: projected(ours[k], theirs[k]) for k in theirs}
        if isinstance(theirs, list):
            assert len(ours) == len(theirs)
            return [projected(a, b) for a, b in zip(ours, theirs)]
        return ours
    for view_id in ('v3', 'v1', 'v7'):
        ours, theirs = bundle.view_bundle(ledger, item_of, view_id), mock[view_id]
        ours['dependants'], theirs['dependants'] = sorted(ours['dependants']), sorted(theirs['dependants'])
        assert projected(ours, theirs) == theirs
    early = bundle.view_bundle(ledger, item_of, 'v3', '2026-05-19')
    assert all(j['day'] <= '2026-05-19' for j in early['judgements']) and all(e['day'] <= '2026-05-19' for e in early['evidence'] if e['day'])
    assert len(early['judgements']) < len(mock['v3']['judgements'])
    assert bundle.days(ledger, '2026-05-19')[-1] == '2026-05-19'


def test_the_graph_adds_the_mapped_views_neighbours(ledger):
    # v3 (data center revenue) depends on v1 (capex) and v7 (Rubin); v2, v9, v48 depend on v3 (the sealed ledger)
    related = idea.related_views(ledger, ['v3'], '2026-08-15')
    assert {(r['view_id'], r['relation']) for r in related} == {('v1', 'upstream'), ('v7', 'upstream'), ('v2', 'downstream'), ('v9', 'downstream'), ('v48', 'downstream')}
    assert all(r['via'] == 'v3' and r['judged'] and r['judged']['position'] for r in related)
    assert next(r for r in related if r['view_id'] == 'v1')['direction'] == '同向'
    # as of the first day only the bootstrap views exist: v48 (opened later) is not a neighbour yet
    assert 'v48' not in {r['view_id'] for r in idea.related_views(ledger, ['v3'], '2026-02-25')}
    assert idea.related_views(ledger, ['v36'], '2026-08-15') == []          # an event view with no edges
    text = idea.object_list(ledger, '2026-08-15', search.object_aliases(UNIVERSE))
    assert text.startswith('Objects with open views as of 2026-08-15') and 'NVDA (company) 2' in text and 'no view yet: ' in text and 'MU' in text and len(text) < 600


def test_two_calls_with_the_service_between_them(ledger, items, index, tmp_path):
    cfg = config.load(CONFIG)
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))

    def mapping(request):
        got = offered(request)
        return {'parts': [{'index': 0, 'views': [{'view_id': got[0][0], 'fit': 'direct'}] + ([{'view_id': got[0][1], 'fit': 'context'}] if len(got[0]) > 1 else []), 'why': 'direct'},
                          {'index': 1, 'views': [{'view_id': v, 'fit': 'driver'} for v in got[1][:5]] + [{'view_id': 'v999', 'fit': 'driver'}], 'why': 'driver'},
                          {'index': 2, 'views': [], 'why': 'no Micron view'}], 'summary': 'S'}
    transport, requests = scripted(DECOMPOSED, mapping)
    card = idea.read_idea(ledger, index, items, archive, cfg, IDEA, aliases=search.object_aliases(UNIVERSE), transport=transport)
    # call 1 saw the object list, not a catalog; call 2 saw one candidate list per part and the idea's own search
    assert len(requests) == 2 and 'Objects with open views' in requests[0]['messages'][1]['content'] and 'Library catalog' not in requests[0]['messages'][1]['content']
    got = offered(requests[1])
    assert set(got) == {0, 1, 2} and 1 <= len(got[0]) <= idea.PER_PART and got[2] == [] or len(got[2]) <= idea.PER_PART
    # the service searched each part with the model's query and with its own canonical one (object name, looks_for, period)
    assert [t['query'] for t in card['reading']['trace']] == ['NVIDIA FY2027 data center revenue', '云厂商 2026 资本开支', 'Micron HBM']
    assert card['reading']['trace'][0]['canonical'] == 'NVDA FY2027 data center revenue FY2027' and card['reading']['trace'][1]['canonical'] == 'ai-capex hyperscaler capex 2026'
    assert idea.merged([{'view_id': 'a'}, {'view_id': 'b'}], [{'view_id': 'b'}, {'view_id': 'c'}], 8) == [{'view_id': 'a'}, {'view_id': 'b'}, {'view_id': 'c'}]
    # mapping: only candidates survive; the parts carry their type, query and candidates
    first_part = card['reading']['parts'][0]
    assert first_part['view_ids'][:1] == got[0][:1] or first_part['service_direct'] == got[0][0]     # the model's pick or the service's, the same id
    assert first_part['context'] == (got[0][1:2] if len(got[0]) > 1 else []) and got[0][1:2] and first_part['context'][0] not in first_part['view_ids']   # context stays off the canvas
    second_part = card['reading']['parts'][1]
    assert second_part['view_ids'] == got[1][:3] and second_part['context'] == got[1][3:5] and card['reading']['parts'][2]['view_ids'] == []   # at most three drivers on the canvas
    assert card['reading']['dropped'][0]['view_id'] == 'v999' and 'not among the candidates of part 1' in card['reading']['dropped'][0]['why']
    assert card['reading']['parts'][0]['object'] == 'NVDA' and card['reading']['parts'][0]['period'] == 'FY2027' and card['reading']['parts'][0]['candidates'] == got[0]
    assert [c['view_id'] for c in card['reading']['chosen']] == [got[0][0], *got[1][:3]] and card['reading']['chosen'][0]['fit'] == 'direct' and card['reading']['chosen'][1]['fit'] == 'driver'
    assert card['reading']['language_slips'] == 0
    # the claim: evaluated by the service against the claimed part's first view
    assert card['reading']['claim']['view_id'] == got[0][0] and card['evaluation'] is not None
    # the graph's neighbours are on the card and in the bundles; nothing is drawn twice
    chosen_ids = [c['view_id'] for c in card['reading']['chosen']]
    assert all(r['view_id'] not in chosen_ids for r in card['related'])
    assert [v['view_id'] for v in card['views']] == chosen_ids + [r['view_id'] for r in card['related']]
    assert card['cost']['turns'] == 2 and card['cost']['cached'] is False and card['cost']['usd'] > 0
    # the same idea again replays both calls from the archive
    transport2, requests2 = scripted(DECOMPOSED, mapping)
    again = idea.read_idea(ledger, index, items, archive, cfg, IDEA, aliases=search.object_aliases(UNIVERSE), transport=transport2)
    assert requests2 == [] and again['cost']['cached'] is True and again['reading'] == card['reading']


def test_a_claim_needs_an_amount_in_the_idea_and_a_mapped_part(ledger, items, index, tmp_path):
    decomposed = dict(DECOMPOSED, claim={'part': 2, 'comparator': '>=', 'value_usd': 1e9})       # the Micron part maps to nothing
    transport, _ = scripted(decomposed, lambda request: {'parts': [{'index': 0, 'views': [{'view_id': offered(request)[0][0], 'fit': 'direct'}], 'why': 'w'}], 'summary': 's'})
    card = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'a.sqlite')), config.load(CONFIG), IDEA, aliases=search.object_aliases(UNIVERSE), transport=transport)
    assert card['evaluation'] is None and any(d['why'] == 'the claimed part has no direct view; a driver is not the quantity the idea names' for d in card['reading']['dropped'])
    transport, _ = scripted(DECOMPOSED, lambda request: {'parts': [{'index': 0, 'views': [{'view_id': offered(request)[0][0], 'fit': 'direct'}], 'why': 'w'}], 'summary': 's'})
    card = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'b.sqlite')), config.load(CONFIG), 'Blackwell demand is softening', aliases=search.object_aliases(UNIVERSE), transport=transport)
    assert card['evaluation'] is None and card['reading']['claim'] is None and any(d['why'] == 'the claim states an amount the idea does not' for d in card['reading']['dropped'])
    assert not idea.MONEY_IN_IDEA.search('Hyperscaler capex peaks in 2026 and falls in 2027')
    assert all(idea.MONEY_IN_IDEA.search(s) for s in ('top $300B this year', '能到 3500 亿美元吗', 'hold a 75% gross margin', 'over 500 billion of capital'))


def test_the_service_decides_the_first_parts_direct_view():
    part = {'object': 'NVDA', 'looks_for': 'data center revenue', 'period': 'FY2027'}
    looks = {'v3': 'NVIDIA FY2027 数据中心收入', 'v2': 'FY2027 NVIDIA 全年总收入', 'v94': 'TSMC 2026年资本开支（美元）', 'v16': 'FY2026 NVIDIA 数据中心收入'}
    assert idea.service_direct(part, ['v3', 'v2'], looks) == 'v3'                                   # the first of the model's direct views in the search's order
    assert idea.service_direct(part, ['v16', 'v3'], looks) == 'v3'                                  # FY2026 does not carry FY2027
    assert idea.service_direct(dict(part, period='calendar year 2026'), ['v3'], looks) == 'v3'      # FY2027 covers calendar 2026
    assert idea.service_direct(dict(part, period='2025'), ['v3'], looks) is None                   # FY2026 would; FY2027 does not
    assert idea.service_direct(dict(part, object='TSM', period='2026'), ['v94'], looks) == 'v94'    # no object test: a theme's view is a company part's direct view
    assert idea.service_direct(dict(part, period='', looks_for='data center revenue'), ['v16'], looks) == 'v16'   # a part naming no year takes the first
    assert idea.service_direct(part, [], looks) is None


def test_d186_analyst_briefs_include_only_the_requested_days_state():
    current = service.open_ledger(os.path.join(ROOT, 'poc/data/english-v23-jev-2026-10-25/views.sqlite'))
    try:
        rows = [r for r in service.summaries(current, '2026-08-09') if r['view_id'] == 'v2']
        past = idea.brief(current, rows, '2026-08-09', detailed=True)[0]
        latest = idea.brief(current, rows, '2026-08-15', detailed=True)[0]
        assert past['judged']['label'] == 'Neutral' and latest['judged']['label'] == 'Bearish'
        saved = current.execute("select * from judgements where view_id='v2' and publication_day<='2026-08-09' order by judgement_id desc limit 1").fetchone()
        assert past['judged']['reasons'] == saved['reasons']
        assert past['judged']['day'] == saved['publication_day']
        assert '400 billion' in past['judged']['condition']
        assert past['question'] == rows[0]['question']
        legacy = idea.brief(current, rows, '2026-08-09')[0]
        assert set(legacy) == {'view_id', 'object', 'looks_at', 'judged'}
        assert set(legacy['judged']) == {'position', 'label'}
    finally:
        current.close()


def test_d186_summary_cannot_change_mapping_and_reads_only_chosen_states(ledger, items, index, tmp_path):
    cfg = config.load(os.path.join(ROOT, 'poc/config/poc-v26-idea.json'))
    text = 'Demand supports growth, but the next-quarter beat case remains unproven without a comparable earnings estimate.'
    requests = []

    def transport(provider, request):
        requests.append(request)
        schema = request['response_format']['json_schema']['schema']
        if schema == idea.SUMMARY:
            answer = {'summary': text}
        elif schema == idea.DECOMPOSE:
            answer = DECOMPOSED
        else:
            answer = {'parts': [{'index': 0, 'views': [{'view_id': offered(request)[0][0], 'fit': 'direct'}], 'why': 'Revenue supports earnings.'}], 'summary': 'Original summary'}
        return {'choices': [{'message': {'content': json.dumps(answer)}}], 'usage': {'prompt_tokens': 1000, 'completion_tokens': 100}}

    original = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'original.sqlite')),
                              config.load(os.path.join(ROOT, 'poc/config/poc-v9.json')), IDEA,
                              aliases=search.object_aliases(UNIVERSE), transport=transport, bundles=False)
    before = requests[:]
    requests.clear()
    progress = []
    result = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'analyst.sqlite')), cfg, IDEA,
                            aliases=search.object_aliases(UNIVERSE), transport=transport, bundles=False,
                            on_progress=lambda stage: progress.append((stage, len(requests))))
    assert progress == [('search', 0), ('decompose', 0), ('retrieve', 1), ('map', 1), ('summarize', 2)]
    assert requests[:2] == before and len(requests) == 3
    assert result['reading']['summary'] == text and original['reading']['summary'] == 'Original summary'
    for field in ('parts', 'chosen', 'claim', 'dropped', 'trace'):
        assert result['reading'][field] == original['reading'][field]
    assert result['evaluation'] == original['evaluation'] and result['related'] == original['related']
    payload = json.loads(requests[2]['messages'][1]['content'])
    rows = payload['theses']
    assert [row['view_id'] for row in rows] == [row['view_id'] for row in result['reading']['chosen']]
    assert all('question' in row and {'condition', 'day', 'reasons'} <= set(row['judged']) for row in rows if row['judged'])
    assert requests[2]['response_format']['json_schema']['schema'] == idea.SUMMARY
    assert result['cost']['turns'] == 3 and result['cost']['input_tokens'] == 3000


def test_d186_summary_configuration_requires_a_mapping_step(tmp_path):
    raw = json.load(open(os.path.join(ROOT, 'poc/config/poc-v26-idea.json')))
    raw.pop('idea')
    path = tmp_path / 'config.json'
    path.write_text(json.dumps(raw))
    with pytest.raises(config.ConfigError, match='idea_summary requires an idea setting'):
        config.load(path)


def test_d188_composite_is_bound_to_the_unchanged_selection(ledger, items, index, tmp_path):
    requests = []

    def transport(provider, request):
        requests.append(request)
        schema = request['response_format']['json_schema']['schema']
        if schema == idea.DECOMPOSE:
            answer = DECOMPOSED
        elif schema == idea.MAP:
            answer = {'parts': [{'index': 0, 'views': [{'view_id': offered(request)[0][0], 'fit': 'direct'}], 'why': 'Relevant revenue.'}], 'summary': 'Mapped summary'}
        else:
            context = json.loads(request['messages'][1]['content'])
            assert schema == idea_composite.endpoint_schema(context['theses'])
            assert all('ladder' in t and len(t['ladder']) == 2 for t in context['theses'])
            assert all('why' not in part for part in context['parts'])
            answer = {'summary': 'Revenue is the direct driver.', 'outcome': 'Revenue', 'claim_direction': 'higher', 'composite': {
                context['theses'][0]['view_id']: {'kind': 'driver', 'label': 'Revenue', 'raises_outcome_position': '1', 'reason': 'Higher revenue supports the claim.'}
            }}
        return {'choices': [{'message': {'content': json.dumps(answer)}}], 'usage': {'prompt_tokens': 1, 'completion_tokens': 1}}

    old = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'old.sqlite')),
                         config.load(os.path.join(ROOT, 'poc/config/poc-v9.json')), IDEA,
                         aliases=search.object_aliases(UNIVERSE), transport=transport, bundles=False)
    old_requests = requests[:]
    requests.clear()
    card = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'new.sqlite')),
                          config.load(os.path.join(ROOT, 'poc/config/poc-v30-idea.json')), IDEA,
                          aliases=search.object_aliases(UNIVERSE), transport=transport, bundles=False)
    assert len(requests) == 3 and requests[:2] == old_requests
    for key in ('parts', 'chosen', 'claim', 'dropped', 'trace'):
        assert card['reading'][key] == old['reading'][key]
    composite = card['reading']['composite']
    assert composite['version'] == 'idea-composite/2' and composite['method'] == 'equal_weight'
    assert composite['as_of'] == card['idea']['as_of']
    selected = card['reading']['chosen'][0]['view_id']
    assert composite['drivers'][0]['thesis_id'] == selected
    assert composite['drivers'][0]['question'] == store.view(ledger, selected)['question']
    assert composite['target'] == {'outcome': 'Revenue', 'direction': 'higher'}


def test_d196_final_associations_are_exactly_the_positive_model_selection(ledger, items, index, tmp_path):
    """D196: omitted candidates have no association, bundle, related edge or orphan claim."""
    requests = []
    picked = []
    def transport(provider, request):
        requests.append(request)
        schema = request['response_format']['json_schema']['schema']
        if schema == idea.DECOMPOSE:
            answer = DECOMPOSED
        elif schema == idea.MAP:
            ids = offered(request)[0][:3]
            answer = {'summary': 'Mapped candidates.', 'parts': [{'index': 0, 'why': 'Candidate relevance.',
                'views': [{'view_id': ident, 'fit': 'direct' if n == 0 else 'driver'} for n, ident in enumerate(ids)]}]}
        else:
            context = json.loads(request['messages'][1]['content'])
            assert 'theses' not in context
            assert schema == idea_composite.positive_schema(context['candidate_theses'])
            thesis = context['candidate_theses'][-1]
            picked.append(thesis['view_id'])
            answer = {'summary': 'The selected driver provides directional support.', 'outcome': 'Revenue', 'claim_direction': 'higher',
                'composite': [{'thesis_id': thesis['view_id'], 'label': 'Revenue driver', 'raises_outcome_position': str(thesis['ladder'][0]['position']),
                               'reason': 'Raises revenue.', 'weight_percent': 100, 'weight_reason': 'The selected driver.'}]}
        return {'choices': [{'message': {'content': json.dumps(answer)}}], 'usage': {'prompt_tokens': 1, 'completion_tokens': 1}}
    aliases = search.object_aliases(UNIVERSE)
    idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'old.sqlite')),
                  config.load(os.path.join(ROOT, 'poc/config/poc-v9.json')), IDEA, aliases=aliases, transport=transport)
    old_requests = requests[:]
    requests.clear()
    archive = model.Archive(str(tmp_path / 'positive.sqlite'))
    cfg = config.load(os.path.join(ROOT, 'poc/config/poc-v32-idea.json'))
    card = idea.read_idea(ledger, index, items, archive, cfg, IDEA, aliases=aliases, transport=transport)
    assert requests[:2] == old_requests and len(requests) == 3
    assert [c['view_id'] for c in card['reading']['chosen']] == picked
    assert [v['view_id'] for v in card['views']] == picked and card['related'] == []
    plan = card['reading']['composite']
    assert plan['version'] == 'idea-composite/4' and 'excluded' not in plan
    assert [d['thesis_id'] for d in plan['drivers']] == picked
    assert card['reading']['claim'] is None and card['evaluation'] is None
    for part in card['reading']['parts']:
        for key in ('view_ids', 'direct', 'driver', 'context'):
            assert set(part[key]) <= set(picked)
        assert part['service_direct'] is None or part['service_direct'] in picked
    requests.clear()
    again = idea.read_idea(ledger, index, items, archive, cfg, IDEA, aliases=aliases, transport=transport)
    assert requests == [] and again['reading'] == card['reading']


def test_d196_positive_selection_refuses_zero_duplicates_and_unknown_candidates(ledger):
    """D196: the model returns a positive subset, not a partition containing zero-weight exclusions."""
    import copy
    selected = [{'view_id': ident} for ident in ('v3', 'v1', 'v9')]
    theses = idea_composite.add_ladders(ledger, selected, endpoints_only=True)
    records = {r['view_id']: r for r in service.summaries(ledger, '2026-08-15')}
    answer = {'summary': 'Revenue supports the idea.', 'outcome': 'Revenue', 'claim_direction': 'higher',
              'composite': [{'thesis_id': 'v3', 'label': 'Revenue', 'raises_outcome_position': '1',
                             'reason': 'Raises revenue.', 'weight_percent': 100, 'weight_reason': 'Direct impact.'}]}
    bind = lambda value: idea_composite.bind_positive(value, selected, records, '2026-08-15', theses)
    assert len(bind(answer)['drivers']) == 1 and 'excluded' not in bind(answer)
    for mutate in (
        lambda a: a['composite'][0].update(weight_percent=0),
        lambda a: a['composite'][0].update(weight_percent=99),
        lambda a: a['composite'][0].update(thesis_id='v999'),
        lambda a: a['composite'][0].update(raises_outcome_position='3'),
        lambda a: a['composite'].append(a['composite'][0]),
    ):
        bad = copy.deepcopy(answer); mutate(bad)
        with pytest.raises(model.SchemaError): bind(bad)
    empty = copy.deepcopy(answer); empty['composite'] = []
    assert bind(empty)['drivers'] == []


def test_d194_weighted_call_preserves_mapping_and_caches_percentages(ledger, items, index, tmp_path):
    """D194: three calls, the same first two requests, explicit saved weights and unchanged chosen IDs."""
    requests = []

    def transport(provider, request):
        requests.append(request)
        schema = request['response_format']['json_schema']['schema']
        if schema == idea.DECOMPOSE:
            answer = DECOMPOSED
        elif schema == idea.MAP:
            ids = offered(request)[0][:2]
            answer = {'parts': [{'index': 0, 'views': [{'view_id': ident, 'fit': 'driver'} for ident in ids],
                                 'why': 'Relevant drivers.'}], 'summary': 'Mapped summary'}
        else:
            context = json.loads(request['messages'][1]['content'])
            assert schema == idea_composite.weighted_schema(context['theses'])
            assert len(context['theses']) == 2
            answer = {'summary': 'Revenue is the principal driver.', 'outcome': 'Revenue', 'claim_direction': 'higher',
                      'composite': {t['view_id']: {'kind': 'driver', 'label': 'Revenue driver',
                          'raises_outcome_position': str(t['ladder'][0]['position']), 'reason': 'Higher revenue supports the claim.',
                          'weight_percent': weight, 'weight_reason': 'Its relative importance to revenue.'}
                          for t, weight in zip(context['theses'], (70, 30))}}
        return {'choices': [{'message': {'content': json.dumps(answer)}}], 'usage': {'prompt_tokens': 1, 'completion_tokens': 1}}

    aliases = search.object_aliases(UNIVERSE)
    old = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'old.sqlite')),
                        config.load(os.path.join(ROOT, 'poc/config/poc-v9.json')), IDEA, aliases=aliases,
                        transport=transport, bundles=False)
    mapping_requests = requests[:]
    requests.clear()
    archive = model.Archive(str(tmp_path / 'weighted.sqlite'))
    cfg = config.load(os.path.join(ROOT, 'poc/config/poc-v31-idea.json'))
    result = idea.read_idea(ledger, index, items, archive, cfg, IDEA, aliases=aliases, transport=transport, bundles=False)
    assert len(requests) == 3 and requests[:2] == mapping_requests
    for field in ('parts', 'chosen', 'claim', 'dropped', 'trace'):
        assert result['reading'][field] == old['reading'][field]
    plan = result['reading']['composite']
    assert (plan['version'], plan['method']) == ('idea-composite/3', 'weighted')
    assert [d['weight_percent'] for d in plan['drivers']] == [70, 30]
    requests.clear()
    replay = idea.read_idea(ledger, index, items, archive, cfg, IDEA, aliases=aliases, transport=transport, bundles=False)
    assert requests == [] and replay['reading']['composite'] == plan


def test_d195_weighted_mapping_keeps_the_model_selected_thesis_count(ledger, items, index, tmp_path):
    """D195: a model-selected fourth or fifth driver is not demoted by a display quota."""
    def transport(provider, request):
        schema = request['response_format']['json_schema']['schema']
        if schema == idea.DECOMPOSE:
            answer = DECOMPOSED
        elif schema == idea.MAP:
            ids = offered(request)[0][:5]
            assert len(ids) == 5
            answer = {'parts': [{'index': 0, 'views': [{'view_id': ident, 'fit': 'driver'} for ident in ids],
                                 'why': 'Relevant drivers.'}], 'summary': 'Mapped summary'}
        else:
            context = json.loads(request['messages'][1]['content'])
            assert len(context['theses']) == 5
            answer = {'summary': 'Several factors drive revenue.', 'outcome': 'Revenue', 'claim_direction': 'higher',
                      'composite': {t['view_id']: {'kind': 'driver', 'label': 'Revenue driver',
                        'raises_outcome_position': str(t['ladder'][0]['position']), 'reason': 'Supports the outcome.',
                        'weight_percent': 20, 'weight_reason': 'Material to the outcome.'} for t in context['theses']}}
        return {'choices': [{'message': {'content': json.dumps(answer)}}], 'usage': {'prompt_tokens': 1, 'completion_tokens': 1}}
    card = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'weighted.sqlite')),
                         config.load(os.path.join(ROOT, 'poc/config/poc-v31-idea.json')), IDEA,
                         aliases=search.object_aliases(UNIVERSE), transport=transport, bundles=False)
    assert len(card['reading']['chosen']) == 5
    assert sum(d['weight_percent'] for d in card['reading']['composite']['drivers']) == 100


def test_d194_weight_contract_rejects_bad_totals_types_and_exclusion_weights(ledger):
    """D194: a complete 100% plan or empty zero plan is accepted; invalid allocations are refused."""
    import copy
    selected = [{'view_id': ident} for ident in ('v3', 'v1', 'v9')]
    records = {row['view_id']: row for row in service.summaries(ledger, '2026-08-15')}
    theses = idea_composite.add_ladders(ledger, selected, endpoints_only=True)
    answer = {'summary': 'Revenue has the most direct impact.', 'outcome': 'Revenue', 'claim_direction': 'higher',
              'composite': {t['view_id']: {'kind': 'driver', 'label': 'Revenue driver',
                  'raises_outcome_position': str(t['ladder'][0]['position']), 'reason': 'Raises revenue.',
                  'weight_percent': weight, 'weight_reason': 'Relative importance to the revenue outcome.'}
                  for t, weight in zip(theses[:2], (70, 30))}}
    answer['composite']['v9'] = {'kind': 'excluded', 'weight_percent': 0, 'reason': 'Overlaps revenue.'}
    bind = lambda value: idea_composite.bind_weighted(value, selected, records, '2026-08-15', theses)
    plan = bind(answer)
    assert sum(d['weight_percent'] for d in plan['drivers']) == 100
    negative = copy.deepcopy(answer)
    negative['claim_direction'] = 'lower'
    assert bind(negative)['drivers'][0]['supporting_end'] != plan['drivers'][0]['supporting_end']
    for weight in (-1, 0, 69, 101, True, 70.5):
        invalid = copy.deepcopy(answer)
        invalid['composite']['v3']['weight_percent'] = weight
        with pytest.raises(model.SchemaError):
            bind(invalid)
    for change in (
        lambda a: a['composite']['v9'].update(weight_percent=1),
        lambda a: a['composite']['v3'].update(weight_reason=''),
        lambda a: a['composite'].pop('v9'),
        lambda a: a['composite'].update(v999=a['composite']['v9']),
    ):
        invalid = copy.deepcopy(answer)
        change(invalid)
        with pytest.raises(model.SchemaError):
            bind(invalid)
    empty = copy.deepcopy(answer)
    empty['composite'] = {s['view_id']: {'kind': 'excluded', 'weight_percent': 0, 'reason': 'No directional link.'} for s in selected}
    assert bind(empty)['drivers'] == []


def test_d188_composite_requires_a_complete_unique_partition_of_chosen_theses():
    import copy
    selected = [{'view_id': 'v3'}, {'view_id': 'v1'}]
    records = {'v3': {'question': 'Data-center revenue'}, 'v1': {'question': 'Capital expenditure'}}
    plan = {'drivers': [{'thesis_id': 'v3', 'label': 'Demand', 'supporting_end': 'first', 'reason': 'Revenue supports growth.'}],
            'excluded': [{'thesis_id': 'v1', 'reason': 'The period is outside the claim.'}]}
    assert idea_composite.bind(plan, selected, records, '2026-08-15')['excluded'][0]['question'] == records['v1']['question']
    empty = {'drivers': [], 'excluded': [{'thesis_id': row['view_id'], 'reason': 'No clear directional link.'} for row in selected]}
    assert idea_composite.bind(empty, selected, records, '2026-08-15')['drivers'] == []
    for change in (
        lambda p: p['excluded'].clear(),
        lambda p: p['excluded'].append(p['excluded'][0]),
        lambda p: p['drivers'][0].update(thesis_id='v999'),
        lambda p: p['drivers'][0].update(supporting_end='higher'),
        lambda p: p['drivers'][0].update(weight=10),
        lambda p: p['drivers'][0].update(reason=''),
    ):
        invalid = copy.deepcopy(plan)
        change(invalid)
        with pytest.raises(model.SchemaError):
            idea_composite.bind(invalid, selected, records, '2026-08-15')


def test_d188_keyed_schema_prevents_duplicate_missing_and_foreign_dispositions():
    import copy
    selected = [{'view_id': 'v3'}, {'view_id': 'v1'}]
    records = {'v3': {'question': 'Data-center revenue'}, 'v1': {'question': 'Capital expenditure'}}
    answer = {'summary': 'Demand remains uncertain.', 'composite': {
        'v3': {'kind': 'driver', 'label': 'Demand', 'supporting_end': 'first', 'reason': 'Higher revenue supports the claim.'},
        'v1': {'kind': 'excluded', 'reason': 'Its period is outside the claim.'}}}
    bound = idea_composite.bind_dispositions(answer, selected, records, '2026-08-15')
    assert [r['thesis_id'] for r in bound['drivers'] + bound['excluded']] == ['v3', 'v1']
    for change in (
        lambda a: a['composite'].pop('v1'),
        lambda a: a['composite'].update(v999=a['composite']['v1']),
        lambda a: a['composite']['v3'].update(kind='excluded'),
        lambda a: a['composite'].update(drivers=[a['composite']['v3']]),
    ):
        invalid = copy.deepcopy(answer)
        change(invalid)
        with pytest.raises(model.SchemaError):
            idea_composite.bind_dispositions(invalid, selected, records, '2026-08-15')
    assert idea_composite.bind_dispositions({'summary': 'No coverage.', 'composite': {}}, [], {}, '2026-08-15')['drivers'] == []


def test_d188_lower_claim_reverses_every_driver_once_in_code():
    import copy
    selected = [{'view_id': 'v3'}, {'view_id': 'v1'}]
    records = {'v3': {'question': 'Data-center revenue'}, 'v1': {'question': 'Capital expenditure'}}
    higher = {'summary': 'Demand supports revenue.', 'outcome': 'Data-center revenue', 'claim_direction': 'higher', 'composite': {
        'v3': {'kind': 'driver', 'label': 'Revenue', 'raises_outcome_end': 'first', 'reason': 'The high-revenue end raises the outcome.'},
        'v1': {'kind': 'driver', 'label': 'Capex', 'raises_outcome_end': 'last', 'reason': 'Higher customer spending supports revenue.'}}}
    lower = copy.deepcopy(higher)
    lower['claim_direction'] = 'lower'
    up = idea_composite.bind_outcome(higher, selected, records, '2026-08-15')
    down = idea_composite.bind_outcome(lower, selected, records, '2026-08-15')
    assert [d['supporting_end'] for d in up['drivers']] == ['first', 'last']
    assert [d['supporting_end'] for d in down['drivers']] == ['last', 'first']
    lower['claim_direction'] = 'unclear'
    with pytest.raises(model.SchemaError, match='unclear claim'):
        idea_composite.bind_outcome(lower, selected, records, '2026-08-15')


def test_d188_endpoint_ids_are_checked_before_claim_inversion():
    import copy
    selected = [{'view_id': 'v3'}, {'view_id': 'v1'}]
    records = {'v3': {'question': 'Revenue'}, 'v1': {'question': 'Capex'}}
    theses = [{'view_id': 'v3', 'ladder': [{'position': 1}, {'position': 5}]},
              {'view_id': 'v1', 'ladder': [{'position': 1}, {'position': 5}]}]
    answer = {'summary': 'Demand supports revenue.', 'outcome': 'Revenue', 'claim_direction': 'higher', 'composite': {
        'v3': {'kind': 'driver', 'label': 'Revenue', 'raises_outcome_position': '1', 'reason': 'Higher revenue raises the outcome.'},
        'v1': {'kind': 'driver', 'label': 'Capex', 'raises_outcome_position': '5', 'reason': 'More spending raises demand.'}}}
    up = idea_composite.bind_endpoints(answer, selected, records, '2026-08-15', theses)
    assert [d['supporting_end'] for d in up['drivers']] == ['first', 'last']
    lower = copy.deepcopy(answer)
    lower['claim_direction'] = 'lower'
    down = idea_composite.bind_endpoints(lower, selected, records, '2026-08-15', theses)
    assert [d['supporting_end'] for d in down['drivers']] == ['last', 'first']
    answer['composite']['v1']['raises_outcome_position'] = '3'
    with pytest.raises(model.SchemaError):
        idea_composite.bind_endpoints(answer, selected, records, '2026-08-15', theses)


def test_the_parts_queries_are_embedded_in_one_round_trip(ledger, items, tmp_path):
    # with real vectors (here fake ones under the real model name) an idea with three parts embeds its own query once and
    # the parts' six queries once more, not once per search; a second read finds everything cached
    conn = search.open_index(str(tmp_path / 'real-name.sqlite'))
    search.build_index(ledger, conn, embed=search.fake_embed, embedding_model=search.EMBEDDING_MODEL)
    calls = []

    def counting(texts, embedding_model=search.EMBEDDING_MODEL):
        calls.append(list(texts))
        return search.fake_embed(texts, embedding_model)

    transport, _ = scripted(DECOMPOSED, lambda request: {'parts': [{'index': 0, 'views': [], 'why': 'x'}], 'summary': 's'})
    card = idea.read_idea(ledger, conn, items, model.Archive(str(tmp_path / 'a.sqlite')), config.load(CONFIG), IDEA, aliases=search.object_aliases(UNIVERSE), transport=transport, embed=counting)
    assert card['search']['mode'] == 'semantic' and [len(c) for c in calls] == [1, 6]
    idea.read_idea(ledger, conn, items, model.Archive(str(tmp_path / 'a.sqlite')), config.load(CONFIG), IDEA, aliases=search.object_aliases(UNIVERSE), transport=transport, embed=counting)
    assert [len(c) for c in calls] == [1, 6]


def test_the_lean_contract_writes_each_candidate_once_and_asks_no_reason(ledger, items, index, tmp_path):
    # idea-v8 (poc-v11): call 2's message carries every candidate brief once, parts refer to ids, and the answer has no
    # per-part reason; under the idea-v7 contract the same answer fails the schema
    lean = config.load(os.path.join(os.path.dirname(CONFIG), 'poc-v11.json'))
    transport, requests = scripted(DECOMPOSED, lambda request: {'parts': [{'index': 0, 'views': [{'view_id': offered(request)[0][0], 'fit': 'direct'}]}], 'summary': 's'})
    card = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'a.sqlite')), lean, IDEA, aliases=search.object_aliases(UNIVERSE), transport=transport)
    message = requests[1]['messages'][1]['content']
    briefs = message.count('"looks_at"')
    ids = set(re.findall(r'"view_id": ?"(v\d+)"', message))
    assert briefs == len(ids) > 1 and 'why' not in json.dumps(requests[1]['response_format'])
    assert card['reading']['parts'][0]['direct'] == [offered(requests[1])[0][0]] and card['reading']['parts'][0]['why'] == '' and card['reading']['summary'] == 's'
    legacy_transport, _ = scripted(DECOMPOSED, lambda request: {'parts': [{'index': 0, 'views': [{'view_id': offered(request)[0][0], 'fit': 'direct'}]}], 'summary': 's'})
    with pytest.raises(model.SchemaError):
        idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'b.sqlite')), config.load(CONFIG), IDEA, aliases=search.object_aliases(UNIVERSE), transport=legacy_transport)


def test_the_clause_contract_keeps_each_drivers_clause(ledger, items, index, tmp_path):
    # idea-v10 (poc-v13): every listed view carries a clause (how a driver moves the part); the card keeps the clauses per part
    clause = config.load(os.path.join(os.path.dirname(CONFIG), 'poc-v13.json'))
    transport, requests = scripted(DECOMPOSED, lambda request: {'parts': [{'index': 0, 'views': [{'view_id': offered(request)[0][0], 'fit': 'direct', 'clause': ''}, {'view_id': offered(request)[0][1], 'fit': 'driver', 'clause': 'the segment it sells into'}], 'why': 'w'}], 'summary': 's'})
    card = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'a.sqlite')), clause, IDEA, aliases=search.object_aliases(UNIVERSE), transport=transport)
    first, got = card['reading']['parts'][0], offered(requests[1])[0]
    assert 'clause' in json.dumps(requests[1]['response_format']) and first['clauses'] == {got[1]: 'the segment it sells into'} and first['driver'] == [got[1]]
    strict, _ = scripted(DECOMPOSED, lambda request: {'parts': [{'index': 0, 'views': [{'view_id': offered(request)[0][0], 'fit': 'direct'}], 'why': 'w'}], 'summary': 's'})
    with pytest.raises(model.SchemaError):
        idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'b.sqlite')), clause, IDEA, aliases=search.object_aliases(UNIVERSE), transport=strict)


def test_the_service_pick_follows_the_models_direct_label(ledger, items, index, tmp_path):
    # the model lists nothing: no pick. The model calls the top hit "context" and a lower view "direct": the pick is the
    # direct one and the claim is judged against it (until 2026-10-24 the top hit on object and year overrode the label)
    transport, requests = scripted(DECOMPOSED, lambda request: {'parts': [{'index': 0, 'views': [], 'why': 'nothing fits'}], 'summary': 's'})
    card = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'a.sqlite')), config.load(CONFIG), IDEA, aliases=search.object_aliases(UNIVERSE), transport=transport)
    assert card['reading']['parts'][0]['direct'] == [] and card['reading']['parts'][0]['service_direct'] is None and card['reading']['chosen'] == []
    texts = {r['view_id']: r['looks_at'] for r in service.summaries(ledger, card['idea']['as_of'])}

    def mapping(request):
        top, *rest = offered(request)[0]
        lower = next(v for v in rest if 'FY2027' in texts[v])
        return {'parts': [{'index': 0, 'views': [{'view_id': top, 'fit': 'context'}, {'view_id': lower, 'fit': 'direct'}], 'why': 'x'}], 'summary': 's'}
    transport, requests = scripted(DECOMPOSED, mapping)
    card = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'b.sqlite')), config.load(CONFIG), IDEA, aliases=search.object_aliases(UNIVERSE), transport=transport)
    first, top = card['reading']['parts'][0], offered(requests[1])[0][0]
    assert first['service_direct'] == first['direct'][0] != top and first['context'] == [top]
    assert card['reading']['claim']['view_id'] == first['direct'][0] and card['evaluation'] is not None


def test_a_market_price_part_maps_to_nothing_and_carries_no_claim(ledger, items, index, tmp_path):
    decomposed = {'parts': [{'object': 'NVDA', 'looks_for': 'NVIDIA share price reaching $300', 'period': '2026', 'query': 'NVIDIA stock price $300'},
                            {'object': 'NVDA', 'looks_for': 'FY2027 total revenue', 'period': 'FY2027', 'query': 'NVIDIA FY2027 total revenue'}],
                  'claim': {'part': 0, 'comparator': '>=', 'value_usd': 300}}
    transport, _ = scripted(decomposed, lambda request: {'parts': [{'index': 0, 'views': [{'view_id': v, 'fit': 'driver'} for v in offered(request)[0][:2]], 'why': 'w'},
                                                                   {'index': 1, 'views': [{'view_id': offered(request)[1][0], 'fit': 'direct'}], 'why': 'w'}], 'summary': 's'})
    card = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'a.sqlite')), config.load(CONFIG), 'NVIDIA stock will hit $300 by year end', aliases=search.object_aliases(UNIVERSE), transport=transport)
    first = card['reading']['parts'][0]
    assert first['market_reading'] is True and first['view_ids'] == [] and first['service_direct'] is None
    assert sum('market reading' in d['why'] for d in card['reading']['dropped']) == 2
    assert card['evaluation'] is None and any('market price' in d['why'] for d in card['reading']['dropped'])
    assert [c['view_id'] for c in card['reading']['chosen']] == [card['reading']['parts'][1]['view_ids'][0]]


def test_a_chinese_field_is_asked_again_in_english(ledger, items, index, tmp_path):
    answers = iter([
        {'parts': [{'object': 'NVDA', 'looks_for': '数据中心收入', 'period': 'FY2027', 'query': 'NVIDIA FY2027 data center revenue'}], 'claim': None},   # call 1, slips
        {'parts': [{'object': 'NVDA', 'looks_for': 'data center revenue', 'period': 'FY2027', 'query': 'NVIDIA FY2027 data center revenue'}], 'claim': None},   # call 1 again
    ])
    requests = []

    def transport(provider, request):
        requests.append(json.loads(json.dumps(request)))
        if 'Parts and the candidates' in request['messages'][1]['content']:
            got = offered(request)
            answer = {'parts': [{'index': 0, 'views': [{'view_id': got[0][0], 'fit': 'direct'}], 'why': 'w'}], 'summary': 's'}
        else:
            answer = next(answers)
        return {'choices': [{'message': {'content': json.dumps(answer, ensure_ascii=False)}}], 'usage': {'prompt_tokens': 10, 'completion_tokens': 10}}
    card = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'a.sqlite')), config.load(CONFIG), IDEA, aliases=search.object_aliases(UNIVERSE), transport=transport)
    assert len(requests) == 3 and requests[1]['messages'][1]['content'].endswith('Write every field in English.')
    assert card['reading']['language_slips'] == 1 and card['reading']['parts'][0]['looks_for'] == 'data center revenue' and card['cost']['turns'] == 3


def test_the_card_alone_leaves_the_bundles_to_the_bundles_route(ledger, items, index, tmp_path):
    transport, _ = scripted(DECOMPOSED, lambda request: {'parts': [{'index': 0, 'views': [{'view_id': offered(request)[0][0], 'fit': 'direct'}], 'why': 'w'}], 'summary': 's'})
    card = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'a.sqlite')), config.load(CONFIG), IDEA, aliases=search.object_aliases(UNIVERSE), transport=transport, bundles=False)
    assert card['views'] == [] and card['reading']['chosen'] and len(json.dumps(card)) < 60_000
    ids = [c['view_id'] for c in card['reading']['chosen']] + [r['view_id'] for r in card['related']]
    full = bundle.thesis_bundles(ledger, items, ids, card['idea']['as_of'])
    assert [v['view_id'] for v in full['views']] == ids and full['as_of'] == card['idea']['as_of']


def test_search_ranks_light_summaries_not_full_records(ledger):
    light = service.summaries(ledger, '2026-08-15')
    full = service.views(ledger, None, '2026-08-15')
    assert [r['view_id'] for r in light] == [r['view_id'] for r in full] and all(r['open'] for r in light)
    v3 = next(r for r in light if r['view_id'] == 'v3')
    assert v3['dependencies'] == ['v1', 'v7'] and set(v3['dependants']) == {'v2', 'v9', 'v48'} and 'evidence' not in v3 and 'counts' not in v3
    assert 'v16' not in {r['view_id'] for r in service.summaries(ledger, '2026-07-23')}      # not opened yet
    assert 'v24' in {r['view_id'] for r in service.summaries(ledger, '2026-08-15', include_closed=True)} and 'v24' not in {r['view_id'] for r in light}


def test_read_idea_calls_no_model_when_no_view_is_recorded(ledger, items, index, tmp_path):
    transport, requests = scripted(DECOMPOSED, lambda request: {'parts': [], 'summary': ''})
    card = idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'archive.sqlite')), config.load(CONFIG), 'Should I buy a house in Austin',
                          aliases=search.object_aliases(UNIVERSE), transport=transport)
    assert requests == [] and card['no_recorded_view'] is True and card['reading'] is None and card['views'] == [] and card['cost']['usd'] == 0


def test_config_without_an_idea_setting_is_refused_by_read_idea(ledger, items, index, tmp_path):
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v2.json'))
    assert cfg.idea is None
    transport, _ = scripted(DECOMPOSED, lambda request: {})
    with pytest.raises(config.ConfigError):
        idea.read_idea(ledger, index, items, model.Archive(str(tmp_path / 'archive.sqlite')), cfg, 'AI capex 2027', aliases=search.object_aliases(UNIVERSE), transport=transport)


def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def test_http_ideas_route_as_a_user_starts_the_server(tmp_path):
    port = free_port()
    proc = subprocess.Popen([sys.executable, os.path.join(ROOT, 'scripts', 'hivemind_api.py'), '--views', LEDGER, '--items', os.path.join(ROOT, 'poc', 'data', 'items-window.sqlite'), '--port', str(port), '--lexical',
                             '--index', str(tmp_path / 'index.sqlite'), '--archive', str(tmp_path / 'archive.sqlite')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        def http(method, path, body=None):
            data = json.dumps(body).encode('utf-8') if body is not None else None
            req = urllib.request.Request(f'http://127.0.0.1:{port}{path}', data=data, method=method, headers={'Content-Type': 'application/json'} if data else {})
            for _ in range(40):
                try:
                    with urllib.request.urlopen(req, timeout=10) as r:
                        return r.status, (json.loads(r.read()) if r.status != 204 else None)
                except urllib.error.HTTPError as e:
                    return e.code, json.loads(e.read())
                except (urllib.error.URLError, ConnectionError):
                    time.sleep(0.25)
            raise AssertionError('the server did not answer')
        assert http('GET', '/days')[0] == 200
        status, card = http('POST', '/ideas', {'text': 'Should I buy a house in Austin', 'bundles': False})
        assert status == 200 and card['no_recorded_view'] is True and card['reading'] is None and card['cost']['usd'] == 0
        assert http('POST', '/ideas', {})[0] == 400 and http('POST', '/nothing', {'text': 'x'})[0] == 404
        assert http('OPTIONS', '/ideas')[0] == 204
        assert http('GET', '/views/v3?as_of=2026-05-19')[1]['state']['position'] == 3 and http('GET', '/search?q=Rubin&k=2')[1]['results']
    finally:
        proc.terminate()
        proc.wait(timeout=10)


def test_d187_http_progress_arrives_before_the_model_finishes(tmp_path, monkeypatch):
    """D187: actual stage boundaries flush immediately; the terminal payload keeps the existing shape."""
    import importlib.util
    import threading
    spec = importlib.util.spec_from_file_location('idea_progress_api', os.path.join(ROOT, 'scripts/hivemind_api.py'))
    api = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(api)
    api.PATHS.update(views=LEDGER, items=ITEMS, index=str(tmp_path / 'index.sqlite'), archive=str(tmp_path / 'archive.sqlite'))
    api.CFG = config.load(os.path.join(ROOT, 'poc/config/poc-v26-idea.json'))
    api.ALIASES = search.object_aliases(UNIVERSE)
    api.SEMANTIC = False
    entered, release = threading.Event(), threading.Event()

    def transport(provider, request):
        schema = request['response_format']['json_schema']['schema']
        if schema == idea.DECOMPOSE:
            entered.set()
            assert release.wait(5), 'The client must receive progress before releasing the model'
            answer = DECOMPOSED
        elif schema == idea.SUMMARY:
            answer = {'summary': 'The evidence leaves the outcome open.'}
        else:
            answer = {'parts': [{'index': 0, 'views': [{'view_id': offered(request)[0][0], 'fit': 'driver'}], 'why': 'Relevant revenue evidence.'}], 'summary': 'Mapping summary'}
        return {'choices': [{'message': {'content': json.dumps(answer)}}], 'usage': {'prompt_tokens': 1, 'completion_tokens': 1}}

    monkeypatch.setattr(model, 'openai_transport', transport)
    server = api.http.server.ThreadingHTTPServer(('127.0.0.1', 0), api.Handler)
    server.daemon_threads = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f'http://127.0.0.1:{server.server_port}/ideas'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/x-ndjson'}
    try:
        request = urllib.request.Request(url, data=json.dumps({'text': IDEA, 'as_of': '2026-08-15', 'bundles': False}).encode(), headers=headers)
        with urllib.request.urlopen(request, timeout=5) as response:
            assert response.headers.get_content_type() == 'application/x-ndjson'
            assert entered.wait(2)
            events = [json.loads(response.readline()), json.loads(response.readline())]
            assert events == [{'type': 'progress', 'stage': 'search'}, {'type': 'progress', 'stage': 'decompose'}]
            assert not release.is_set()
            release.set()
            events.extend(json.loads(line) for line in response)
        assert [e['stage'] for e in events if e['type'] == 'progress'] == ['search', 'decompose', 'retrieve', 'map', 'summarize']
        assert events[-1]['type'] == 'result'
        assert events[-1]['data']['reading']['summary'] == 'The evidence leaves the outcome open.'
        assert events[-1]['data']['cost']['turns'] == 3
        bad = urllib.request.Request(url, data=b'{}', headers=headers)
        with urllib.request.urlopen(bad, timeout=5) as response:
            assert json.loads(response.readline()) == {'type': 'error', 'status': 400, 'message': 'POST /ideas needs a JSON body with text'}
    finally:
        release.set()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

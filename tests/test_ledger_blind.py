"""Ledger-blind extraction, v22 / poc-v38 (D211): the extraction request shows no thesis and no group, so its bytes depend on the item
alone; links name only the answer's own candidates; the placement call files the statements under the theses open at the item's
turn; the parallel day never finds such a request stale. Real ledger and archive on temporary paths; a scripted model."""
import json
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from test_concurrency import english_jev_send, setup_run, CASES  # noqa: E402
from test_theme_block import ledger  # noqa: E402
from test_placement import ITEM, TEXT, PLATFORM, KRESS  # noqa: E402
from hivemind import config, extraction, model, replay, universe  # noqa: E402
from hivemind.parallel_day import ParallelDay, extraction_key  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
UNI = universe.load(ROOT / 'poc' / 'universe.json')
V38 = config.load(ROOT / 'poc' / 'config' / 'poc-v38.json')
V37 = config.load(ROOT / 'poc' / 'config' / 'poc-v37.json')


def test_the_v22_request_is_the_same_bytes_whatever_the_ledger_shows_and_v21_is_not(tmp_path):
    conn = ledger(tmp_path)
    shown = extraction.shown_views(conn, V38, ITEM, ['NVDA'])
    groups = [{'group_id': 'g1', 'name': 'Rubin rollout', 'scope': 'Rubin production', 'aliases': ['Rubin'], 'members': []}]
    empty = extraction_key(V38, ITEM, TEXT, [], UNI, [])
    assert extraction_key(V38, ITEM, TEXT, shown, UNI, groups) == empty                     # decisive: two ledgers, one request
    assert extraction_key(V37, ITEM, TEXT, shown, UNI, groups) != extraction_key(V37, ITEM, TEXT, [], UNI, [])   # control: v21 depends on the ledger
    _, _, user, schema = extraction.request_for(V38, ITEM, TEXT, shown, UNI, groups)
    assert '[Existing theses' not in user and 'v1' not in user and '[Research groups] None yet' in user
    fields = schema['properties']['candidates']['items']['properties']
    assert 'folds_into' not in fields and 'lost_if_folded' not in fields and 'opens_as' in fields and 'settled_by' in fields


def test_v22_links_only_to_the_answers_candidates_and_the_placer_files_under_the_open_theses(tmp_path):
    conn = ledger(tmp_path)
    shown = extraction.shown_views(conn, V38, ITEM, ['NVDA'])
    calls = []

    def transport(provider, request):
        name = request['response_format']['json_schema']['name']
        calls.append(name)
        if name == 'extraction':
            assert '  - v1 (' not in request['messages'][1]['content']
            candidate = {'id': 'c1', 'object': 'NVDA', 'kind': 'asset', 'looks_at': 'FY2027 stand-alone CPU revenue', 'question': 'How much stand-alone CPU revenue will NVIDIA report for FY2027?',
                         'rungs': [{'label': l, 'condition': l, 'lo': None, 'hi': None} for l in ('Strongly bullish', 'Bullish', 'Neutral', 'Bearish', 'Strongly bearish')],
                         'due_day': '2027-02-28', 'year': 'FY2027', 'evidence_ids': ['e1'], 'measure': 'product_revenue', 'scope': 'stand-alone CPU', 'period_start': '2026-02-01',
                         'period_end': '2027-01-31', 'basis': 'GAAP', 'unit': 'USD', 'event_type': 'n/a', 'opens_as': 'main_driver', 'settled_by': 'the FY2027 annual report', 'group_refs': []}
            data = {'candidates': [candidate], 'evidence': [dict(PLATFORM, links=['c1']), dict(KRESS, links=['v1'])], 'new_groups': []}
        else:
            data = {'placements': [{'id': 'e1', 'links': []}, {'id': 'e2', 'links': ['v2']}]}
        return {'choices': [{'message': {'content': json.dumps(data)}}]}

    handover = extraction.extract(model.Archive(str(tmp_path / 'archive.sqlite')), V38, ITEM, TEXT, shown, UNI, transport=transport)
    assert calls == ['extraction', 'placement']
    assert [(e['id'], e['links']) for e in handover.evidence] == [('e1', ['c1']), ('e2', ['v2'])]   # an in-call link to v1 does not survive filing; the placer's v2 does
    assert [c['id'] for c in handover.candidates] == ['c1'] and 'folds_into' not in handover.candidates[0]


def test_the_parallel_day_never_resends_a_v22_request_and_files_at_the_turn(tmp_path):
    """Two items, two workers: the second is prepared while the first opens v1; its request is not stale, and its placement
    request lists v1, the thesis opened in between."""
    args = setup_run(tmp_path)
    args['cfg'] = V38
    inner = english_jev_send(require_overlap=True)
    placements = []

    def send(*parameters):
        request = parameters[-1]
        if len(parameters) > 1 and request['response_format']['json_schema']['name'] == 'placement':
            text = request['messages'][1]['content']
            placements.append(text)
            listed = re.findall(r'^\s*- (v\d+) \(', text, re.M)
            ids = re.findall(r'^  - (e\d+) \[', text, re.M)
            return {'choices': [{'message': {'content': json.dumps({'placements': [{'id': i, 'links': listed[:1]} for i in ids]})}}]}
        answer = inner(*parameters)
        if len(parameters) > 1 and request['response_format']['json_schema']['name'] == 'extraction':      # the shared fake writes v12's two fold fields; v22 has none
            data = json.loads(answer['choices'][0]['message']['content'])
            for candidate in data.get('candidates', []):
                candidate.pop('folds_into', None); candidate.pop('lost_if_folded', None)
            answer = {'choices': [{'message': {'content': json.dumps(data)}}]}
        return answer

    day = ParallelDay(Path(args['testdb_path']), tmp_path / 'manifests', extraction_workers=2, jev_workers=2)
    replay.run(**args, transport=send, day_runner=day)
    assert [e['event'] for e in day.events if e['event'] == 'stale'] == []
    assert [e['event'] for e in day.events if e['event'] in ('reused', 'reextracted')] == ['reused', 'reused']
    second = [t for t in placements if CASES[1]['item']['input_id'] in t or CASES[1]['evidence']['quote'][:30] in t]
    assert second and '  - v1 (' in second[-1]                                            # filed at the turn, under the thesis the first item opened
    with sqlite3.connect(args['views_path']) as db:
        sends = db.execute("select count(*) from handovers").fetchone()[0]
    assert sends == 2 and args['archive'].conn.execute("select count(*) from model_calls where purpose='extract'").fetchone()[0] == 2    # one sample per item


# D209 (2026-10-30 review): a statement no open question takes is dropped like every other drop, so a candidate left with none
# of its evidence is dropped as in the sift, and never reaches matching to open a thesis with no evidence.
def test_a_candidate_whose_only_evidence_placement_drops_does_not_survive(tmp_path):
    conn = ledger(tmp_path)
    shown = extraction.shown_views(conn, V38, ITEM, ['NVDA'])
    candidate = {'id': 'c1', 'object': 'NVDA', 'kind': 'asset', 'looks_at': 'FY2027 stand-alone CPU revenue', 'question': 'How much stand-alone CPU revenue will NVIDIA report for FY2027?',
                 'rungs': [{'label': l, 'condition': l, 'lo': None, 'hi': None} for l in ('Strongly bullish', 'Bullish', 'Neutral', 'Bearish', 'Strongly bearish')],
                 'due_day': '2027-02-28', 'year': 'FY2027', 'evidence_ids': ['e1'], 'measure': 'product_revenue', 'scope': 'stand-alone CPU', 'period_start': '2026-02-01',
                 'period_end': '2027-01-31', 'basis': 'GAAP', 'unit': 'USD', 'event_type': 'n/a', 'opens_as': 'main_driver', 'settled_by': 'the FY2027 annual report', 'group_refs': []}

    def transport(provider, request):
        if request['response_format']['json_schema']['name'] == 'extraction':
            data = {'candidates': [candidate], 'evidence': [dict(PLATFORM, links=[]), dict(KRESS, links=['c1'])], 'new_groups': []}
        else:
            data = {'placements': [{'id': 'e1', 'links': []}, {'id': 'e2', 'links': []}]}
        return {'choices': [{'message': {'content': json.dumps(data)}}]}

    handover = extraction.extract(model.Archive(str(tmp_path / 'archive.sqlite')), V38, ITEM, TEXT, shown, UNI, transport=transport)
    assert handover.candidates == [] and handover.evidence == []
    assert handover.dropped == [('e1', 'no home'), ('c1', 'candidate without surviving evidence'), ('e2', 'no home')]


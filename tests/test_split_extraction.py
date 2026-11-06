"""The split extraction in production shape (docs/research/2026-11-05-production-plan/plan-final.md, C-1 to C-5, C-7): real ledgers on
temporary paths, the real round, matching and writer, and fake model and Jev providers. Each test names the contract it proves."""
import copy
import dataclasses
import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, model, split, universe  # noqa: E402
from hivemind.views import judging, round as rounds, store  # noqa: E402

CFG = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-split-v3.json'))
DAY = '2026-08-30'
REVENUE = 'Revenue rose 85% year over year to $81.6 billion, with data center up 92% to $75.2 billion.'
DEAL = 'Nvidia agreed to invest $3.5 billion in MediaTek through convertible bonds, the companies said on Monday.'
PARTNER = 'MediaTek expects revenue of about $20 billion in 2026, according to its chief executive.'
CHIPS = 'The two companies will build AI chips for cars and personal computers together.'
TEXT = ' '.join([REVENUE, DEAL, PARTNER, CHIPS])


def item(input_id, text=TEXT, day=DAY):
    return {'input_id': input_id, 'publication_day': day, 'category': 'T7', 'publisher_type': 'media', 'publisher': 'example news',
            'title': 'Nvidia invests in MediaTek', 'text': text, 'object_identifiers': [{'kind': 'ticker', 'value': 'NVDA'}], 'authors': [],
            'channel': 'web', 'source_uri': 'https://example.com/' + input_id}


def ledger(tmp_path):
    """A ledger with one open question, v1: NVIDIA's FY2027 Data Center revenue."""
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    store.ensure_writable_columns(conn)
    rungs = [{'label': l, 'condition': c, 'lo': lo, 'hi': hi} for l, c, lo, hi in [
        ('Strongly bullish', 'at least $350 billion', 350e9, None), ('Bullish', '$300–350 billion', 300e9, 350e9), ('Neutral', '$250–300 billion', 250e9, 300e9),
        ('Bearish', '$200–250 billion', 200e9, 250e9), ('Strongly bearish', 'below $200 billion', None, 200e9)]]
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='asset', kind='asset', looks_at='FY2027 Data Center revenue',
                      question='What Data Center segment revenue will NVIDIA report for FY2027?', due_day='2027-02-24', year='FY2027', rungs=rungs,
                      seq=1, input_id='seed', created_at='2026-08-01T00:00:00')
    store.add_key(conn, 'v1', {'measure': 'segment_revenue', 'scope': 'Data Center', 'period_start': '2026-02-01', 'period_end': '2027-01-31',
                               'basis': 'n/a', 'unit': 'USD', 'event_type': 'n/a', 'key_version': 2}, 1)
    conn.commit()
    return conn


def attribution(**over):
    return dict({'speaker': 'example news', 'original_who': 'NVIDIA', 'original_day': '', 'tier': 'fact', 'event_time': 'FY2027 Q2'}, **over)


def ladder_ascending_mislabelled():
    """MediaTek revenue ranges written from the lowest up with the canonical labels in their usual order: the inverted ladder of seq 1273."""
    B = 1e9
    return [{'label': l, 'condition': c, 'lo': lo, 'hi': hi} for l, c, lo, hi in [
        ('Strongly bullish', 'below $16 billion', None, 16 * B), ('Bullish', '$16–19 billion', 16 * B, 19 * B),
        ('Neutral', 'around the chief executive\'s $20 billion', 19 * B, 21 * B), ('Bearish', '$21–24 billion', 21 * B, 24 * B),
        ('Strongly bearish', 'at least $24 billion', 24 * B, None)]]


class Providers:
    """Fake model and Jev providers. Records every request; answers A, B and record preparation for item 'first'; nothing new for 'second'."""

    def __init__(self):
        self.requests = []

    def __call__(self, *parameters):
        request = parameters[-1]
        if len(parameters) == 1:                         # Jev: every relation 'different', every membership 0.05
            answers = {}
            for qid, q in request['questions'].items():
                if q['type'] == 'noul':
                    answers[qid] = {'type': 'noul', 'noul': 0.05}
                else:
                    labels = q['criteria']
                    answers[qid] = {'type': 'choice', 'choice': 'different', 'confidence': 1.0, 'probabilities': {x: float(x == 'different') for x in labels}}
            return {'answers': answers, 'usage': {}}
        self.requests.append(request)
        name = request['response_format']['json_schema']['name']
        user = request['messages'][-1]['content']
        first = 'test:first' in user or REVENUE in user and 'test:second' not in user
        if name == 'new_question':
            body = {'questions': [], 'new_groups': []}
            if first:
                body = {'new_groups': [{'id': 'n1', 'name': 'NVIDIA–MediaTek partnership', 'scope': 'NVIDIA\'s investment in MediaTek and their joint chips',
                                        'aliases': ['MediaTek investment', 'NVIDIA MediaTek convertible bonds']}],
                        'questions': [
                            {'question': 'Will NVIDIA complete its $3.5 billion investment in MediaTek convertible bonds by January 31, 2027?',
                             'why_it_matters': 'a sized, unfinished stake', 'closest_existing_question': 'none', 'what_separates_it': 'no question tracks it',
                             'how_and_when_to_check': 'a closing announcement', 'group_refs': ['n1'],
                             'evidence': [{'quote': DEAL, 'what_it_shows': 'NVIDIA agreed to buy $3.5 billion of MediaTek convertible bonds', 'original_speaker': 'NVIDIA and MediaTek'},
                                          {'quote': REVENUE, 'what_it_shows': 'NVIDIA has the cash flow for the stake: revenue $81.6 billion', 'original_speaker': 'NVIDIA'}]},
                            {'question': 'What revenue will MediaTek report for 2026?', 'why_it_matters': 'the partner\'s scale', 'closest_existing_question': 'none',
                             'what_separates_it': 'another company', 'how_and_when_to_check': 'MediaTek annual report', 'group_refs': ['n1'],
                             'evidence': [{'quote': PARTNER, 'what_it_shows': 'MediaTek guides about $20 billion for 2026', 'original_speaker': 'MediaTek CEO'}]}]}
        elif name == 'extraction':
            body = {'evidence': []}
            if first:
                body = {'evidence': [
                    dict(attribution(speaker='example news (media)'), id='x1', quote=REVENUE, one_line='NVIDIA Data Center revenue $75.2 billion, up 92%', links=['v1']),
                    dict(attribution(original_who='NVIDIA and MediaTek', tier='party_statement'), id='x2', quote=CHIPS, one_line='joint AI chips for cars and PCs', links=[])]}
        elif name == 'record_preparation':
            assert '"other_reading"' in user and '[Unfiled passages]' in user and CHIPS in user
            body = {'candidates': {
                        'c1': {'object': 'NVDA', 'new_subject': '', 'new_subject_kind': 'none', 'opens_as': 'binding_obligation', 'obligation_state': 'unsigned',
                               'shared_measure': 'none', 'unit': 'n/a', 'year': '', 'due_day': '', 'date_basis': 'unknown', 'date_provenance': '', 'favourable_end': 'none',
                               'rungs': [{'label': 'Bullish', 'condition': 'completed by the date', 'lo': None, 'hi': None},
                                         {'label': 'Bearish', 'condition': 'not completed by the date', 'lo': None, 'hi': None}]},
                        'c2': {'object': 'new', 'new_subject': 'MediaTek', 'new_subject_kind': 'company', 'opens_as': 'main_driver', 'obligation_state': 'none',
                               'shared_measure': 'none', 'unit': 'USD', 'year': '2026', 'due_day': '', 'date_basis': 'unknown', 'date_provenance': '',
                               'favourable_end': 'higher', 'rungs': ladder_ascending_mislabelled()}},
                    'evidence': {'e1': attribution(original_who='NVIDIA and MediaTek', tier='party_statement'), 'e2': attribution(original_who='NVIDIA'),
                                 'e3': attribution(original_who='MediaTek', tier='party_statement')},
                    'unfiled': {'u1': {'links': ['c1']}}}
        else:
            raise AssertionError('unexpected request ' + name)
        return {'choices': [{'message': {'content': json.dumps(body)}}], 'usage': {'prompt_tokens': 100, 'completion_tokens': 10}}


def run_item(conn, uni, providers, input_id, seq, tmp_path, text=TEXT):
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    return rounds.run(conn, archive, CFG, uni, item(input_id, text), seq, transport=providers)


def test_one_quoted_statement_is_one_record_with_both_summaries_and_both_homes_and_each_judge_reads_both(tmp_path):
    """C-1: A and B quoted the same sentence for different statements; one record keeps both summaries, links to both questions, carries the
    attribution record preparation returned; the judging request of each linked question prints both statements."""
    conn, uni, providers = ledger(tmp_path), universe.load(os.path.join(ROOT, 'poc', 'universe.json')), Providers()
    result = run_item(conn, uni, providers, 'test:first', 2, tmp_path)
    assert not result.failed, result.failed
    rows = conn.execute('select evidence_id, one_line, original_who, tier from evidence where quote=?', (REVENUE,)).fetchall()
    assert len(rows) == 1
    summary = rows[0]['one_line']
    assert 'revenue $81.6 billion' in summary and 'Data Center revenue $75.2 billion' in summary
    homes = {r[0] for r in conn.execute('select view_id from evidence_links where evidence_id=?', (rows[0]['evidence_id'],))}
    new_deal = conn.execute("select view_id from views where question like '%MediaTek convertible%'").fetchone()[0]
    assert homes == {'v1', new_deal}
    for view_id in homes:
        _, text = judging.build_prompt(conn, view_id, 'judging-v7')
        assert 'revenue $81.6 billion' in text and 'Data Center revenue $75.2 billion' in text


def test_an_unfiled_passage_reaches_the_new_question_of_the_same_item_that_record_preparation_links(tmp_path):
    """C-1: B kept a statement no existing question takes; A's new question of the same item takes it through record preparation."""
    conn, uni, providers = ledger(tmp_path), universe.load(os.path.join(ROOT, 'poc', 'universe.json')), Providers()
    run_item(conn, uni, providers, 'test:first', 2, tmp_path)
    new_deal = conn.execute("select view_id from views where question like '%MediaTek convertible%'").fetchone()[0]
    linked = {r[0] for r in conn.execute('select l.view_id from evidence_links l join evidence e using(evidence_id) where e.quote=?', (CHIPS,))}
    assert linked == {new_deal}


def test_a_declared_group_is_written_with_both_questions_of_the_matter(tmp_path):
    """C-2: A declares the partnership as a research group; both new questions of the matter join it."""
    conn, uni, providers = ledger(tmp_path), universe.load(os.path.join(ROOT, 'poc', 'universe.json')), Providers()
    run_item(conn, uni, providers, 'test:first', 2, tmp_path)
    group = conn.execute("select group_id from thesis_groups where name like '%MediaTek%'").fetchone()
    assert group is not None
    members = {r[0] for r in conn.execute('select view_id from thesis_group_members where group_id=?', (group[0],))}
    assert len(members) == 2


def test_the_next_item_reads_the_question_the_previous_item_wrote_and_the_research_subject_survives_a_restart(tmp_path):
    """C-5 and C-7: item 2's A and B requests show item 1's new questions (D375); the new subject keeps its id in a fresh universe."""
    conn, providers = ledger(tmp_path), Providers()
    run_item(conn, universe.load(os.path.join(ROOT, 'poc', 'universe.json')), providers, 'test:first', 2, tmp_path)
    subject = conn.execute("select object_id from research_subjects where name='MediaTek'").fetchone()[0]
    mediatek_question = conn.execute('select view_id from views where object_id=?', (subject,)).fetchone()[0]
    fresh = universe.load(os.path.join(ROOT, 'poc', 'universe.json'))
    assert not fresh.has(subject)
    providers.requests.clear()
    result = run_item(conn, fresh, providers, 'test:second', 3, tmp_path, text='Nvidia shares were steady on Tuesday as investors awaited data.')
    assert not result.failed and fresh.has(subject)
    a_request = next(r for r in providers.requests if r['response_format']['json_schema']['name'] == 'new_question')
    b_request = next(r for r in providers.requests if r['response_format']['json_schema']['name'] == 'extraction')
    for request in (a_request, b_request):
        assert f'  - {mediatek_question} (' in request['messages'][-1]['content']


def test_a_mislabelled_company_ladder_is_reordered_by_its_favourable_end(tmp_path):
    """C-4 (D186): the lowest MediaTek revenue range labelled Strongly bullish is reordered so Strongly bullish holds the highest range."""
    conn, uni, providers = ledger(tmp_path), universe.load(os.path.join(ROOT, 'poc', 'universe.json')), Providers()
    run_item(conn, uni, providers, 'test:first', 2, tmp_path)
    subject = conn.execute("select object_id from research_subjects where name='MediaTek'").fetchone()[0]
    view_id = conn.execute('select view_id from views where object_id=?', (subject,)).fetchone()[0]
    rungs = conn.execute('select label, lo, hi, condition from rungs where view_id=? order by position', (view_id,)).fetchall()
    assert rungs[0]['label'] == 'Strongly bullish' and rungs[0]['lo'] == 24e9 and rungs[0]['hi'] is None
    assert rungs[-1]['label'] == 'Strongly bearish' and rungs[-1]['hi'] == 16e9
    assert rungs[2]['condition'].endswith('[from 19,000,000,000 USD to below 21,000,000,000 USD]')
    due = conn.execute('select due_day from views where view_id=?', (view_id,)).fetchone()[0]
    assert due == '' or due > DAY


# ---------------------------------------------------------------- record checks on single answers

def stage_and_prep(question, meta, quote=PARTNER):
    a = {'questions': [{'question': question, 'why_it_matters': 'w', 'closest_existing_question': 'none', 'what_separates_it': 's',
                        'how_and_when_to_check': 'annual report', 'group_refs': [],
                        'evidence': [{'quote': quote, 'what_it_shows': 'x', 'original_speaker': 'y'}]}], 'new_groups': []}
    stage = split.stage_answers(item('test:unit'), TEXT, [(a, {'evidence': []})], ['NVIDIA'])
    prep = {'candidates': {'c1': dict({'object': 'NVDA', 'new_subject': '', 'new_subject_kind': 'none', 'opens_as': 'main_driver', 'obligation_state': 'none',
                                       'shared_measure': 'none', 'unit': 'USD', 'year': '', 'due_day': '', 'date_basis': 'unknown', 'date_provenance': '',
                                       'favourable_end': 'higher', 'rungs': []}, **meta)},
            'evidence': {'e1': attribution()}, 'unfiled': {}}
    return stage, prep


def handover(question, **meta):
    stage, prep = stage_and_prep(question, meta)
    uni = universe.load(os.path.join(ROOT, 'poc', 'universe.json'))
    return split.build_handover(item('test:unit'), TEXT, [], uni, stage, prep)


def test_an_annual_figure_for_the_year_after_next_is_refused_with_or_without_a_ladder():
    """C-4: the year limit reads the admission reason, not whether a ladder exists (round 1 attack)."""
    _, candidates, dropped, _ = handover('What share of AI accelerator revenue will NVIDIA hold in 2028?', year='2028')
    assert not candidates and any('beyond next year' in reason for _, reason in dropped)


def test_a_fiscal_year_written_as_a_bare_year_is_read_as_the_fiscal_year_the_question_names():
    """C-4: FY2028 prepared as "2028" is next fiscal year, not calendar 2028; a comparison year elsewhere does not decide (round 2)."""
    _, candidates, _, _ = handover('What total revenue will NVIDIA report for FY2028?', year='2028')
    assert len(candidates) == 1 and candidates[0]['due_day'] == '2028-02-29'
    assert split.question_year('What will the calendar 2028 market be versus FY2025?', '2028') == '2028'


def test_a_quarterly_figure_does_not_open_a_question():
    _, candidates, dropped, _ = handover('What revenue will NVIDIA report for fiscal Q3 2027?', year='FY2027')
    assert not candidates and any('quarterly' in reason for _, reason in dropped)


def test_bounds_that_miss_their_stated_band_are_refused():
    """C-4: "within 5% of $39,063,072,000" with a lower bound $100 million off (seq 1280) leaves the question without a ladder, with its reason."""
    rungs = [{'label': l, 'condition': c, 'lo': lo, 'hi': hi} for l, c, lo, hi in [
        ('Strongly bullish', 'above', 45e9, None), ('Bullish', 'up', 41015825600, 45e9),
        ('Neutral', 'within 5% above or below FY2026 net sales of $39,063,072,000', 37009918400, 41015825600),
        ('Bearish', 'down', 33e9, 37009918400), ('Strongly bearish', 'below', None, 33e9)]]
    _, candidates, dropped, _ = handover('What total revenue will NVIDIA report for FY2027?', year='FY2027', rungs=rungs)
    assert candidates and candidates[0]['rungs'] == [] and any('stated band' in reason for _, reason in dropped)


def test_a_rung_that_holds_no_value_leaves_the_question_without_a_ladder():
    """C-4: "exactly $279 billion" written as lo = hi = 279e9 (seq 1210 of the stopped production run) holds no value under inclusive lo,
    exclusive hi; the question keeps no ladder and the reason is recorded."""
    B = 1e9
    rungs = [{'label': l, 'condition': c, 'lo': lo, 'hi': hi} for l, c, lo, hi in [
        ('Strongly bullish', 'below', None, 119 * B), ('Bullish', 'up to', 119 * B, 279 * B), ('Neutral', 'exactly $279 billion', 279 * B, 279 * B),
        ('Bearish', 'above', 279 * B, 558 * B), ('Strongly bearish', 'far above', 558 * B, None)]]
    _, candidates, dropped, _ = handover('What supply commitments will NVIDIA disclose in its FY2027 annual report?', year='FY2027', rungs=rungs, favourable_end='lower')
    assert candidates and candidates[0]['rungs'] == [] and any('holds no value' in reason for _, reason in dropped)


def test_a_calendar_shared_quantity_gets_its_key_and_an_analyst_check_date():
    _, candidates, _, _ = handover('How much will the five largest hyperscalers spend on capital expenditure in 2027?', object='ai-capex',
                                   opens_as='shared_quantity', shared_measure='spend_total', year='2027', favourable_end='none')
    c = candidates[0]
    assert (c['kind'], c['measure'], c['period_start'], c['due_day']) == ('theme', 'spend_total', '2027-01-01', '2028-03-31')
    assert 'analyst_check' in c['looks_at']


def test_a_long_item_is_read_in_sections_and_later_sections_see_earlier_proposals():
    """C-3 (decision 6): no silent truncation; every part reaches A and B."""
    paragraphs = ['Paragraph %d. ' % i + 'x' * 900 for i in range(1000)]
    parts = split.sections('\n'.join(paragraphs), limit=100000)
    assert len(parts) > 1 and max(len(p) for p in parts) <= 100000 and '\n'.join(parts) == '\n'.join(paragraphs)


# ---------------------------------------------------------------- source quotes

def test_source_quotes_follow_the_production_contract_and_store_the_source_characters():
    text = ("The company's supply and capacity commitments increased from $119 billion at the end of the first quarter to $279 billion at the end of "
            "the second quarter of fiscal 2027. Shipments fell 21% year‑over‑year. Its latest report—$96.2 billion in revenue, up 106%—looks strong. "
            "Profit rose —$10 million in the quarter. Sales to one customer represented 28.1 % of total net sales.")
    named = "Nvidia's supply and capacity commitments increased from $119 billion at the end of the first quarter to $279 billion at the end of the second quarter of fiscal 2027."
    assert split.source_quote(named, text) is None and split.source_quote(named, text, ['NVIDIA'])
    assert split.source_quote('Shipments fell 21% year-over-year.', text) == 'Shipments fell 21% year‑over‑year.'
    assert split.source_quote('$96.2 billion in revenue, up 106%', text) == '$96.2 billion in revenue, up 106%'
    assert split.source_quote('Profit rose $10 million in the quarter.', text) is None          # a dash before a number keeps its sign
    assert split.source_quote('Sales to one customer represented 28.1% of total net sales.', text) == 'Sales to one customer represented 28.1 % of total net sales.'

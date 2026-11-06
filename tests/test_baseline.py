"""The coverage-start reading (D363, D364; docs/research/2026-11-04-filing-end-to-end/production-design.md): each test names the design row it proves.
Real ledgers and items databases on temporary paths; only the model transport is fake."""
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import baseline, config, model, seeding, service, testdb  # noqa: E402
from hivemind.views import round as round_module, store  # noqa: E402

SEED = ROOT / 'poc' / 'seeds' / 'nvda-2026-07-01-v2.json'
V116 = ROOT / 'poc' / 'config' / 'poc-v116.json'
START = '2026-07-01'
RELEASE = 'edgar:NVDA:0001045810-26-000051:q1fy27pr.htm'
COMMENTARY = 'edgar:NVDA:0001045810-26-000051:q1fy27cfocommentary.htm'
NEWSROOM = 'nvidianews:nvidia-announces-financial-results-for-first-quarter-fiscal-2027'
# excerpts of the May 20, 2026 release's page text as stored (each table cell on its own line)
PAGE = ('NVIDIA Announces Financial Results for First Quarter Fiscal 2027\n• Record revenue of $81.6 billion, up 85% from a year ago\n'
        'Non-GAAP\n($ in millions, except earnings per share)\nQ1 FY27\nQ4 FY26\nQ1 FY26\nQ/Q\nY/Y\nRevenue\n$81,615\n$68,127\n$44,062\n20\n%\n85\n%\n'
        'Operating income\n$53,783\n$44,474\n$21,801\n21\n%\n147\n%\n'
        'Non-GAAP operating income*\n$\n53,783\n$\n44,474\n$\n21,801\n'
        'Purchases related to property and equipment and intangible assets\n(1,757)\n(1,227)\nAcquisitions, net of cash acquired\n(87)\n(383)\n'
        'Expanded collaboration with Google Cloud, including new NVIDIA Vera Rubin-powered A5X instances.\n')
FIGURE = lambda quote, value, period='Q1 FY27': {'quote': quote, 'value': value, 'unit': '$ in millions', 'period': period, 'basis': 'non-GAAP',
                                                'one_line': f'{quote.splitlines()[0]} was {value} in {period}.'}
ANSWERS = {   # question -> the figures the fake reading writes, on either item
    'v10': [FIGURE('Revenue\n$81,615', '$81,615'), FIGURE('Operating income\n$53,783', '$53,783')],
    'v1': [FIGURE('Revenue\n$81,615', '$81,615')],
    'v12': [FIGURE('Purchases related to property and equipment and intangible assets\n(1,757)', '(1,757)')],
    'v7': [FIGURE('Expanded collaboration with Google Cloud, including new NVIDIA Vera Rubin-powered A5X instances.', 'new NVIDIA Vera Rubin-powered A5X instances')],
}


def items_database(path, page_text=PAGE, with_page_column=True, items=None):
    if os.path.exists(path):                     # a second step on the same ledger reads the same items database
        return testdb.open_db(path)
    conn = sqlite3.connect(path)
    page = ', text_page text' if with_page_column else ''
    conn.execute(f'create table items (input_id text, publication_day text, publisher text, title text, channel text, category text, object_identifiers text, text text{page}, '
                 'feed integer default 1, copy_of text, klass text, published_at text)')     # the replay's feed reads the last four
    names = ['input_id', 'publication_day', 'publisher', 'title', 'channel', 'category', 'object_identifiers', 'text'] + (['text_page'] if with_page_column else [])
    ticker = json.dumps([{'kind': 'ticker', 'value': 'NVDA', 'why': 'upstream feed for this object'}])
    rows = items or [(RELEASE, '2026-05-20', 'NVIDIA Corporation', 'NVDA 8-K EX-99.1', 'EDGAR', 'T1', ticker),
                     (COMMENTARY, '2026-05-20', 'NVIDIA Corporation', 'NVDA 8-K EX-99.2', 'EDGAR', 'T1', ticker),
                     (NEWSROOM, '2026-05-20', 'NVIDIA Corporation', 'NVIDIA newsroom copy', 'company newsroom', 'T1', ticker),
                     ('edgar:NVDA:0001045810-26-000019:q4fy26pr.htm', '2026-02-25', 'NVIDIA Corporation', 'NVDA 8-K EX-99.1', 'EDGAR', 'T1', ticker),
                     ('edgar:NVDA:0001045810-26-000073:q2fy27pr.htm', '2026-08-26', 'NVIDIA Corporation', 'NVDA 8-K EX-99.1', 'EDGAR', 'T1', ticker)]
    for row in rows:
        values = row + ('cleaned text without tables',) + ((page_text,) if with_page_column else ())
        conn.execute(f'insert into items ({",".join(names)}) values ({",".join("?" * len(values))})', values)
    conn.commit()
    conn.close()
    return testdb.open_db(path)


def fake_transport(answers=ANSWERS):
    sent = []

    def transport(provider, request):
        user = request['messages'][1]['content']
        view_id = user.split('\n  - ', 1)[1].split(' ', 1)[0]
        sent.append(view_id)
        return {'choices': [{'message': {'content': json.dumps({'figures': answers.get(view_id, [])})}}], 'usage': {'prompt_tokens': 10, 'completion_tokens': 5}}
    return transport, sent


def seeded_ledger(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    seeding.seed_views(conn, str(SEED), created_at=f'{START}T00:00:00Z')
    return conn


def run_step(tmp_path, conn=None, items=None, answers=ANSWERS, coverage_start=START):
    conn = conn or seeded_ledger(tmp_path)
    items = items or items_database(str(tmp_path / 'items.sqlite'))
    transport, sent = fake_transport(answers)
    record = baseline.run(conn, items, model.Archive(str(tmp_path / 'archive.sqlite')), config.load(str(V116)), ticker='NVDA',
                          coverage_start=coverage_start, transport=transport, log=lambda *a: None)
    return conn, record, sent


def test_documents_are_the_latest_filed_report_before_coverage_start(tmp_path):
    """Design, Documents: the latest T1 day before coverage start; of that day the filed items, not the newsroom copy; not the later report."""
    chosen = baseline.report_items(items_database(str(tmp_path / 'items.sqlite')), 'NVDA', START)
    assert sorted(r['input_id'] for r in chosen) == sorted([RELEASE, COMMENTARY])
    assert baseline.report_items(items_database(str(tmp_path / 'other.sqlite')), 'AMD', START) == []


def test_check_keeps_the_reports_row_and_refuses_what_is_not_its_text():
    """Design, Check (round 24): a footnote mark left off or a cell left out is stored as the report's row; a changed label, a figure not in the row,
    two figures in one value and digits inside a product name are refused."""
    cases = [('Non-GAAP operating income $53,783', '$53,783', True, 'Non-GAAP operating income*\n$\n53,783'),
             ('Purchases related to property and equipment and intangible assets (1,227)', '(1,227)', True,
              'Purchases related to property and equipment and intangible assets\n(1,757)\n(1,227)'),
             ('Revenue\n$81,615', '$81,615', True, 'Revenue\n$81,615'),
             ('Record revenue of $81.6 billion, up 85% from a year ago', '$81.6 billion', True, 'Record revenue of $81.6 billion, up 85% from a year ago'),
             ('Non-GAAP operating profit $53,783', '$53,783', False, None),
             ('Purchases related to property and equipment and intangible assets (1,894)', '(1,894)', False, None),
             ('Revenue $81,615 $68,127', '$81,615 and $68,127', False, None),
             ('Expanded collaboration with Google Cloud, including new NVIDIA Vera Rubin-powered A5X instances.', 'A5X instances', False, None)]
    for quote, value, kept, stored in cases:
        checked = baseline.check_figures([FIGURE(quote, value)], PAGE)[0]
        assert checked['kept'] is kept, quote
        if stored is not None:
            assert checked['quote'] == stored, quote


def test_missing_page_text_refuses_before_any_call(tmp_path):
    """Table 1: an items database without text_page, or an empty page text, is refused before any call."""
    conn = seeded_ledger(tmp_path)
    for name, items in (('no column', items_database(str(tmp_path / 'a.sqlite'), with_page_column=False)),
                        ('empty text', items_database(str(tmp_path / 'b.sqlite'), page_text=''))):
        transport, sent = fake_transport()
        with pytest.raises(baseline.BaselineRefused):
            baseline.run(conn, items, model.Archive(str(tmp_path / f'{name}.sqlite')), config.load(str(V116)), ticker='NVDA', coverage_start=START,
                         transport=transport, log=lambda *a: None)
        assert sent == [], name
    assert conn.execute("select count(*) from processing_steps where step='baseline'").fetchone()[0] == 0


def test_one_record_per_item_and_quote_linked_to_every_question_that_kept_it(tmp_path):
    """D364 and Records: revenue kept by v1 and v10 on one item is one record linked to both; each item has its own record; the A5X text is refused."""
    conn, record, sent = run_step(tmp_path)
    assert len(sent) == 22 * 2                                      # every seed question on both filed items, the copy not read
    revenue = [r['evidence_id'] for r in conn.execute("select evidence_id from evidence where quote like 'Revenue%'")]
    assert len(revenue) == 2                                        # one per item
    for evidence_id in revenue:
        assert set(store.views_linked_to(conn, evidence_id)) == {'v1', 'v10'}
    capex = conn.execute("select * from evidence where quote like 'Purchases%'").fetchone()
    assert capex['tier'] == 'fact' and capex['original_day'] == '2026-05-20' and capex['speaker'] == 'NVIDIA Corporation'
    assert capex['one_line'].endswith('(unit: $ in millions)')     # the value "(1,757)" carries no scale of its own
    assert sorted(record['changed']) == ['v1', 'v10', 'v12'] and all(r['view_id'] == 'v7' for r in record['refused'])
    assert len(record['refused']) == 2                             # the A5X text on each item, "value not printed in the quote"


def test_first_days_round_judges_the_linked_questions(tmp_path):
    """Design, Judging: round.changed_views_of_day on the coverage-start day returns the questions the step linked."""
    conn, record, _ = run_step(tmp_path)
    assert round_module.changed_views_of_day(conn, START) == set(record['changed'])
    assert round_module.changed_views_of_day(conn, '2026-07-02') == set()


def test_records_and_seeds_are_visible_from_coverage_start(tmp_path):
    """Design, Sequence number and Seeded questions visible: the step takes sequence 1; the service shows the seeds and records from coverage start."""
    conn, record, _ = run_step(tmp_path)
    assert conn.execute("select sequence_no from processing_steps where step='baseline'").fetchone()[0] == 1
    assert store.next_sequence(conn) == 2
    v10 = store.view(conn, 'v10')
    assert service.view_exists(conn, v10, START) and not service.view_exists(conn, v10, '2026-06-30')


def test_the_step_runs_once(tmp_path):
    """Table 1: a resumed ledger whose coverage-start day completed skips the step; nothing is written twice."""
    conn, _, _ = run_step(tmp_path)
    store.complete_day(conn, START, 1, f'{START}T23:00:00')
    conn.commit()
    before = conn.execute('select count(*) from evidence').fetchone()[0]
    _, record, sent = run_step(tmp_path, conn=conn)
    assert record is None and sent == [] and conn.execute('select count(*) from evidence').fetchone()[0] == before


def test_unfinished_coverage_start_day_refuses_a_later_start(tmp_path):
    """Table 1: the step ran but its day did not complete: a run from that day skips the step; a run from a later day is refused."""
    conn, _, _ = run_step(tmp_path)
    _, record, sent = run_step(tmp_path, conn=conn)                 # resumed from the coverage-start day itself
    assert record is None and sent == []
    with pytest.raises(baseline.BaselineRefused):
        run_step(tmp_path, conn=conn, coverage_start='2026-07-02')


def test_a_progressed_ledger_refuses_the_step_before_any_call(tmp_path):
    """Table 1: a ledger that processed an item before the step was configured is refused (coverage start has passed)."""
    conn = seeded_ledger(tmp_path)
    store.mark_step(conn, 'some-item', 1, 'handed_over', 'ok', '', START, f'{START}T10:00:00')
    conn.commit()
    with pytest.raises(baseline.BaselineRefused):
        run_step(tmp_path, conn=conn)


def test_a_configuration_without_the_step_writes_nothing(tmp_path):
    """Design, Entry: poc-v108 has no baseline setting; the step returns None and writes nothing."""
    conn = seeded_ledger(tmp_path)
    transport, sent = fake_transport()
    assert baseline.run(conn, items_database(str(tmp_path / 'items.sqlite')), model.Archive(str(tmp_path / 'a.sqlite')),
                        config.load(str(ROOT / 'poc' / 'config' / 'poc-v108.json')), ticker='NVDA', coverage_start=START, transport=transport) is None
    assert sent == [] and conn.execute("select count(*) from processing_steps where step='baseline'").fetchone()[0] == 0


def test_only_the_validated_prompt_is_built(tmp_path):
    """Design, Configuration: the code builds only baseline-v3; the prompt file is the validated text (pinned)."""
    with pytest.raises(config.ConfigError):
        baseline.require_supported('baseline-v4')
    digest = hashlib.sha256((ROOT / 'src' / 'hivemind' / 'prompts' / 'baseline-v3.json').read_bytes()).hexdigest()
    assert digest == PROMPT_SHA256
    assert config.load(str(V116)).baseline.prompt_version == 'baseline-v3'


PROMPT_SHA256 = 'a38f684bfc60fa5698a3d4c374fd52cc8187d27bd62129311f24483fd7377a5b'   # baseline-v3.json as validated (rounds 14-16, 24-26)

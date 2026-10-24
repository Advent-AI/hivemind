"""The service's as-of reads on the sealed ledger (real data, read-only). Requirements: docs/poc/service.md
"Checks the new path must pass": as_of never looks ahead (views, switches, judgements, evidence, sources,
relationships); evaluate reads every money ladder as one partition or refuses; a corrupt record is refused.

Run: python3 -m pytest tests/test_service.py -q
"""
import os
import re
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import service  # noqa: E402
from hivemind.views import store  # noqa: E402

LEDGER = os.path.join(ROOT, 'poc', 'data', 'sealed-2026-10-24-run3-through-0815', 'views.sqlite')
INF = float('inf')


@pytest.fixture(scope='module')
def ledger():
    return service.open_ledger(LEDGER)


def test_default_as_of_is_the_last_completed_day(ledger):
    assert service.default_as_of(ledger) == '2026-08-15'


def test_state_as_of_never_looks_ahead(ledger):
    # v3 (data center revenue) moved from position 3 to 2 on 2026-05-20
    before, after = service.view(ledger, 'v3', '2026-05-19'), service.view(ledger, 'v3', '2026-05-20')
    assert before['state']['position'] == 3 and after['state']['position'] == 2
    assert after['state']['previous_position'] == 3 and after['state']['since_day'] == '2026-05-20'
    assert before['counts']['evidence'] < after['counts']['evidence']


def test_a_view_does_not_exist_before_its_opening_day(ledger):
    opened = ledger.execute("select publication_day from processing_steps where sequence_no=(select created_seq from views where view_id='v16') limit 1").fetchone()[0]
    assert opened == '2026-07-24'
    assert service.view(ledger, 'v16', '2026-07-23') is None
    assert service.view(ledger, 'v16', '2026-07-24') is not None
    assert 'v16' not in {v['view_id'] for v in service.views(ledger, 'NVDA', '2026-07-23')}


def test_frozen_views_are_closed_only_from_their_freeze_day(ledger):
    assert service.view(ledger, 'v24', '2026-08-01')['open'] is True
    assert service.view(ledger, 'v24', '2026-08-02')['open'] is False
    assert 'v24' not in {v['view_id'] for v in service.views(ledger, 'NVDA', '2026-08-15')}
    assert 'v24' in {v['view_id'] for v in service.views(ledger, 'NVDA', '2026-08-15', include_closed=True)}


def test_relationships_are_as_of_too(ledger):
    # v94 (opened 2026-08-15) depends on v1; on 2026-02-25 v1 cannot yet have it as a dependant
    assert 'v94' in service.view(ledger, 'v1', '2026-08-15')['dependants']
    assert 'v94' not in service.view(ledger, 'v1', '2026-02-25')['dependants']
    late = ledger.execute("""with m as (select sequence_no, min(publication_day) d from processing_steps where sequence_no>0 group by 1)
        select count(*) from dependencies dep join views v on v.view_id=dep.depends_on join m md on md.sequence_no=dep.seq join m mv on mv.sequence_no=v.created_seq where md.d > mv.d""").fetchone()[0]
    assert late == 28          # the relationships that would leak without the filter (Codex's census)
    for dep in service.view(ledger, 'v3', '2026-05-20')['dependencies']:
        assert dep['since_day'] <= '2026-05-20'


def test_history_lists_the_change_with_its_cited_evidence(ledger):
    h = service.history(ledger, 'v1', '2026-07-01', '2026-08-15')
    moves = [(c['day'], c['moved_from'], c['position']) for c in h['changes']]
    assert ('2026-07-26', 3, 4) in moves and ('2026-08-15', 4, 5) in moves
    assert all(j['cited'] for j in h['changes'])
    assert sum(b['evidence'] for b in h['arrivals'].values()) > 0


def test_evidence_excludes_replaced_guidance_after_the_replacement_day(ledger):
    repl = ledger.execute('select r.old_evidence_id, r.new_evidence_id, r.seq, l.view_id from replacements r join evidence_links l on l.evidence_id=r.old_evidence_id limit 1').fetchone()
    day = service.day_of_seq(ledger, repl['seq'])
    before = {e['evidence_id'] for e in service.evidence(ledger, repl['view_id'], service.day_of_seq(ledger, repl['seq'] - 1) or '2026-05-19')}
    after = {e['evidence_id'] for e in service.evidence(ledger, repl['view_id'], day)}
    assert repl['old_evidence_id'] in before and repl['old_evidence_id'] not in after and repl['new_evidence_id'] in after


def test_changes_cite_evidence_with_only_the_sources_known_that_day(ledger):
    # e3 under v4 gained outlets on 05-20 and 08-06; the 02-25 change must not show them
    changed = [c for c in service.changes(ledger, '2026-02-24', '2026-02-25') if c['view_id'] == 'v4']
    assert changed and any(e['evidence_id'] == 'e3' for e in changed[0]['cited'])
    e3 = next(e for e in changed[0]['cited'] if e['evidence_id'] == 'e3')
    assert all(s['publication_day'] <= '2026-02-25' for s in e3['sources']) and e3['outlets'] == len(e3['sources'])
    assert ledger.execute("select count(*) from evidence_sources where evidence_id='e3'").fetchone()[0] > e3['outlets']


def test_every_money_ladder_reads_as_one_partition_or_is_refused(ledger):
    # a money ladder is one whose conditions name dollar amounts; decided by the text, not by the parser under test
    money = re.compile(r'\d\s*(?:万亿|千亿|亿|万)?\s*美元')
    evaluable, refused, no_money = [], [], []
    for (view_id,) in ledger.execute('select view_id from views'):
        rungs = store.rungs_of(ledger, view_id)
        if sum(1 for r in rungs if money.search(r['condition'])) < 3:
            no_money.append(view_id)
            continue
        bands, problem = service.ladder_bands(rungs)
        (evaluable if bands else refused).append((view_id, problem))
    assert len(evaluable) == 43 and refused == [], refused
    # the non-money ladders (percentages, gigawatts) read partially or not at all, and evaluate refuses them
    for view_id in ('v32', 'v51', 'v52', 'v61', 'v81', 'v93'):
        assert service.evaluate(ledger, view_id, '>=', 1)['evaluable'] is False
    assert service.band('最终担保融资金额为0至不足1000亿美元') == (0.0, True, 1e11, False)
    assert service.band('截至2026-12-31，筹集总额不低于5000亿美元且低于7500亿美元。') == (5e11, True, 7.5e11, False)   # the dateline is not the bound
    assert service.band('不低于100亿美元，且低于200亿美元') == (1e10, True, 2e10, False)                              # a continued clause is
    assert service.band('FY2027 OEM设备及大型数据中心收入不低于FY2026按披露占比计算的269.79亿美元、且低于400亿美元')[0] == 26979000000.0   # exact, not ...000.000004
    assert service.ladder_bands([{'position': 1, 'condition': '低于100亿美元'}, {'position': 2, 'condition': '高于100亿美元'}])[0] is None   # nobody owns 100亿
    assert service.band('FY2026 全年总费用不低于 1650 亿美元且不高于 1690 亿美元，处于公司指引区间') == (1.65e11, True, 1.69e11, True)
    assert service.band('FY2027全年总收入为650亿美元至720亿美元（含两端）') == (6.5e10, True, 7.2e10, True)
    assert service.band('FY2027全年总收入不低于FY2025的220亿美元、且低于FY2026的391亿美元') == (2.2e10, True, 3.91e10, False)
    assert service.band('FY2026全年总收入大于或等于104亿美元（Q2收入26亿美元按四个季度年化）且小于124亿美元') == (1.04e10, True, 1.24e10, False)
    assert service.band('达到9000亿美元及以上') == (9e11, True, INF, False)
    assert service.band('园区总成本恰为5000亿美元') == (5e11, True, 5e11, True)
    assert service.band('同比增长超过70%且不超过100%') is None


def test_evaluate_judges_the_claim_against_the_judged_band(ledger):
    holds = service.evaluate(ledger, 'v3', '>=', 300e9)
    assert holds['claim_position'] == 2 and holds['judged_position'] == 2 and holds['verdict'] == 'holds'
    assert service.evaluate(ledger, 'v3', '>=', 325e9)['verdict'] == 'borderline'
    assert service.evaluate(ledger, 'v3', '>=', 350e9)['verdict'] == 'not_yet'
    assert service.evaluate(ledger, 'v3', '<', 350e9)['verdict'] == 'holds'
    assert service.evaluate(ledger, 'v3', '=', 325e9)['verdict'] == 'borderline'        # a band does not establish equality
    assert service.evaluate(ledger, 'v3', '>=', 300e9, '2026-05-19')['judged_position'] == 3
    # Codex's two cases: a [0, 1000亿) band straddles 500亿; "不高于 1690 亿" puts 1690 亿 inside position 3
    assert service.evaluate(ledger, 'v17', '>=', 50e9)['verdict'] == 'borderline'
    v27 = service.evaluate(ledger, 'v27', '>=', 169e9)
    assert v27['claim_position'] == 3 and v27['verdict'] == 'borderline'
    # Codex's second pass: a boundary written as 269.79亿 is exactly 26,979,000,000 and belongs to position 3; v70's
    # dateline does not hide its bound
    v84 = service.evaluate(ledger, 'v84', '=', 26979000000)
    assert v84['claim_position'] == 3 and v84['verdict'] == 'borderline'
    v70 = service.evaluate(ledger, 'v70', '>=', 500e9)
    assert v70['evaluable'] and v70['claim_position'] == 3 and v70['verdict'] in ('holds', 'borderline', 'not_yet')
    assert service.evaluate(ledger, 'v7', '>=', 1e9)['evaluable'] is False      # a yes/no ladder has no amounts
    assert service.evaluate(ledger, 'v51', '>=', 1)['evaluable'] is False       # a percentage ladder is refused, not guessed
    with pytest.raises(ValueError):
        service.evaluate(ledger, 'v3', '>', 300e9)


def test_record_and_changes_name_real_rounds(ledger):
    rec = service.record(ledger, 'v3', '2026-08-15')['last_check']
    assert rec['day'] == '2026-08-15' and rec['round'].startswith('day:') and rec['items_processed_that_day'] > 0
    moved = [c for c in service.changes(ledger, '2026-07-25', '2026-07-26') if c['position_moved']]
    assert any(c['view_id'] == 'v1' and c['from_position'] == 3 and c['to_position'] == 4 and c['cited'] for c in moved)
    assert service.changes(ledger, '2026-08-15') == []


def test_a_corrupt_judgement_record_is_refused_not_read_as_empty():
    with pytest.raises(service.LedgerError):
        service._json('[broken')
    assert service._json('') == [] and service._json('["e1"]') == ['e1']

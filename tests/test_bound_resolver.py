"""The bound resolver (docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md, row 3 and its product-facing
contract; proofs 2b to 2d): one owner for every upper date bound, explicit or omitted.

On four real store states (`bound_cases.py`) every public function that takes a date is called with an omitted, a past and a future
bound, and each outcome is compared with today's, recorded before the change (`fixtures/bound-baseline-2026-11-16.json`), except where
the contract changes it:
- an explicit bound after the last completed day is refused, naming that day (finished and partial stores);
- a first-day store refuses every call;
- on a store with work after its last completed day, the bundle functions' omitted bound reads as of that day, so the half-processed
  day is no longer returned;
- a range whose start is after its end is refused (council round 124); a start equal to the end reads as before.
Plus the structural check that no module resolves a bound elsewhere, and the API's mapping of the three refusals."""
import ast
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [HERE, os.path.join(ROOT, 'src'), os.path.join(ROOT, 'scripts')]
import bound_cases  # noqa: E402
from hivemind import service  # noqa: E402

BASELINE = json.load(open(os.path.join(HERE, 'fixtures', 'bound-baseline-2026-11-16.json')))
LAST = {'finished': '2026-08-15', 'partial': '2026-08-28'}
UNFILTERED = ('bundle.view_bundle', 'bundle.not_judged', 'bundle.days')       # their omitted bound read every record before
HELPERS = {'service': {'default_as_of', 'resolve_bound', 'resolve_range', 'visible', 'view_exists', 'is_open_as_of', 'state_as_of',
                       'dependencies', 'dependants', 'evidence_record'},
           'bundle': {'_bundles', 'research_groups', '_visible'},
           'search': set(), 'idea': {'judged', 'full_payload', 'lean_payload'}}


@pytest.fixture(scope='module')
def outcomes(tmp_path_factory):
    """Every call's outcome now, and for the partial store each unfiltered function's outcome with the last completed day given."""
    folder = str(tmp_path_factory.mktemp('stores'))
    found, explicit_last = {}, {}
    for state in bound_cases.STATES:
        conn = bound_cases.open_state(state, folder)
        for name, kind, call in bound_cases.calls(conn, state):
            found[(state, name, kind)] = bound_cases.outcome(call)
        if state == 'partial':
            view_id, created_seq = bound_cases.first_view(conn)
            item_of = bound_cases.bundle.item_lookup(None)
            explicit_last = {'bundle.view_bundle': bound_cases.outcome(lambda: bound_cases.bundle.view_bundle(conn, item_of, view_id, LAST['partial'])),
                             'bundle.not_judged': bound_cases.outcome(lambda: bound_cases.bundle.not_judged(conn, view_id, created_seq, LAST['partial'])),
                             'bundle.days': bound_cases.outcome(lambda: bound_cases.bundle.days(conn, LAST['partial']))}
        conn.close()
    return found, explicit_last


def expected(state, name, kind, explicit_last):
    before = BASELINE[f'{state}|{name}|{kind}']
    if state == 'first_day':
        return ['error', "FirstDayNotCompleted: the store's first day has not completed"]
    if kind == 'future' and state in LAST:
        return ['error', f"BoundNotCompleted: day not completed: {bound_cases.STATES[state]['future']} is after the last completed day {LAST[state]}"]
    if state == 'partial' and kind == 'omitted' and name in UNFILTERED:
        return explicit_last[name]
    if name == 'search.search' and kind == 'past' and before != ['ok', None]:
        # row 4a: the lexical ranking now counts only views visible at the bound, so a past bound no longer ranks among views created
        # after it; its own proof is the backup equality in test_search_live.py
        return CHANGED_BY_ROW_4A
    if state == 'empty' and name == 'bundle.not_judged' and kind in ('past', 'future'):
        # the direct-call rule (round 122): a view not visible at an explicit bound is refused, here one the empty store does not hold
        return ['error', f"KeyError: 'v1 is not available as of {bound_cases.STATES[state][kind]}'"]
    return before


CHANGED_BY_ROW_4A = 'changed by row 4a'


def test_every_call_on_every_state_keeps_todays_outcome_except_where_the_contract_changes_it(outcomes):
    found, explicit_last = outcomes
    assert len(found) == len(BASELINE) == 176
    wrong = {key: (got, expected(*key, explicit_last)) for key, got in found.items()
             if expected(*key, explicit_last) != CHANGED_BY_ROW_4A and got != expected(*key, explicit_last)}
    assert wrong == {}


def test_the_partial_store_no_longer_returns_its_half_processed_day_by_default(outcomes):
    """The decisive case: before the change an omitted bound on the served store's bundle functions read 2026-08-29's records."""
    found, explicit_last = outcomes
    changed = [name for name in UNFILTERED if BASELINE[f'partial|{name}|omitted'] != found[('partial', name, 'omitted')]]
    assert 'bundle.days' not in changed or found[('partial', 'bundle.days', 'omitted')] == explicit_last['bundle.days']
    assert all(found[('partial', name, 'omitted')] == explicit_last[name] for name in UNFILTERED)


def test_a_finished_store_answers_every_omitted_and_past_bound_exactly_as_before(outcomes):
    found, _ = outcomes
    for (state, name, kind), got in found.items():
        if state == 'finished' and kind in ('omitted', 'past', 'from equal to to'):
            assert got == BASELINE[f'{state}|{name}|{kind}'], (name, kind)


def test_the_resolver_is_idempotent_and_refuses_only_after_the_last_completed_day(tmp_path):
    conn = bound_cases.open_state('finished', str(tmp_path))
    assert service.resolve_bound(conn, None) == '2026-08-15'
    assert service.resolve_bound(conn, service.resolve_bound(conn, '2026-08-15')) == '2026-08-15'
    with pytest.raises(service.BoundNotCompleted) as refused:
        service.resolve_bound(conn, '2026-08-16')
    assert (refused.value.requested, refused.value.last_completed_day) == ('2026-08-16', '2026-08-15')
    assert service.resolve_range(conn, '2026-08-01', '2026-08-01') == '2026-08-01'
    with pytest.raises(service.RangeNotOrdered):
        service.resolve_range(conn, '2026-08-02', '2026-08-01')
    with pytest.raises(service.BoundNotCompleted):
        service.resolve_range(conn, '2026-08-01', '2026-08-16')


@pytest.mark.parametrize('state', ['finished', 'partial', 'empty'])
def test_a_range_starting_after_its_end_is_refused_on_every_store(tmp_path, state):
    conn = bound_cases.open_state(state, str(tmp_path))
    days = bound_cases.STATES[state]
    for name, kind, call in bound_cases.range_after_end_calls(conn, state):
        assert bound_cases.outcome(call) == ['error', f"RangeNotOrdered: range start after its end: {days['future']} to {days['past']}"], (name, kind)


def _date_functions(module):
    tree = ast.parse(open(os.path.join(ROOT, 'src', 'hivemind', f'{module}.py')).read())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and {a.arg for a in node.args.args + node.args.kwonlyargs} & {'as_of', 'to_day'}:
            calls = {n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, 'id', None)
                     for n in ast.walk(node) if isinstance(n, ast.Call)}
            yield node.name, calls


def structural_breaches():
    """Every function of the four modules with a date parameter calls the resolver or is a listed helper; nothing outside the
    resolver calls `default_as_of`."""
    breaches = []
    for module in HELPERS:
        for name, calls in _date_functions(module):
            if name not in HELPERS[module] and not calls & {'resolve_bound', 'resolve_range'}:
                breaches.append(f'{module}.{name}: takes a date and does not resolve it')
        source = open(os.path.join(ROOT, 'src', 'hivemind', f'{module}.py')).read()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.FunctionDef) and node.name not in ('resolve_bound', 'default_as_of'):
                for call in ast.walk(node):
                    if isinstance(call, ast.Call) and (getattr(call.func, 'attr', None) == 'default_as_of' or getattr(call.func, 'id', None) == 'default_as_of'):
                        breaches.append(f'{module}.{node.name}: calls default_as_of outside the resolver')
    return breaches


def test_no_module_resolves_a_bound_outside_the_resolver():
    assert structural_breaches() == []


def test_the_api_maps_the_three_refusals_with_their_days():
    import hivemind_api
    assert hivemind_api.error_response(service.FirstDayNotCompleted()) == (503, {'error': "the store's first day has not completed"})
    assert hivemind_api.error_response(service.BoundNotCompleted('2026-09-30', '2026-08-28')) == (
        409, {'error': 'day not completed', 'requested': '2026-09-30', 'last_completed_day': '2026-08-28'})
    assert hivemind_api.error_response(service.RangeNotOrdered('2026-08-21', '2026-08-20')) == (
        409, {'error': 'range start after its end', 'start': '2026-08-21', 'end': '2026-08-20'})
    assert hivemind_api.error_response(KeyError('v9')) == (404, {'error': "not found: 'v9'"})


def test_a_ledger_without_the_completed_day_table_fails_with_the_missing_table_error(tmp_path):
    """What is checked (council round 126): today's default (`default_as_of`, unchanged) already fails on such a ledger with SQLite's
    missing-table error, so an omitted bound failed this way before too; every public function, with an omitted or an explicit bound,
    now fails with that same error. Before the resolver an explicit bound skipped `default_as_of` and could answer; that case is a
    change, with no such ledger among the 143 stored ones."""
    import sqlite3
    from hivemind import bundle
    path = str(tmp_path / 'legacy.sqlite')
    bound_cases.store.open_db(path).close()
    raw = sqlite3.connect(path)
    raw.execute('drop table days_completed')
    raw.commit()
    raw.close()
    conn = service.open_ledger(path)
    with pytest.raises(sqlite3.OperationalError) as before:
        service.default_as_of(conn)
    for call in (lambda: service.views(conn), lambda: service.changes(conn, '2026-08-01'), lambda: bundle.days(conn),
                 lambda: service.views(conn, None, '2026-08-01')):
        with pytest.raises(sqlite3.OperationalError) as now:
            call()
        assert str(now.value) == str(before.value) == 'no such table: days_completed'

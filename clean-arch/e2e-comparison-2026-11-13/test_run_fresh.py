"""The run states of one draw (WIRING-DESIGN.md §D, D448; council mo, D449; `run_fresh.py`): every test is a state × event cell. The
components are fakes that write the outputs the orchestrator reads; the ledger, the record, the locks and the files are real, under a
temporary folder. No model, no network, no credential (the credentials path points at a temporary file)."""
import fcntl
import importlib.util
import io
import json
import os
import signal
import sqlite3
import urllib.error
import urllib.request
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('run_fresh', HERE / 'run_fresh.py')
run_fresh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_fresh)
OPTIONS = {'until_day': '2026-07-01', 'passes': 1}
REASON = 'transport failure after the runner retried (log line 12)'


class Components:
    """Fake component processes keyed by script name: 'ok' writes the outputs; 'fail' exits 1; 'killed' exits as a SIGKILLed process
    does (-9); 'die' starts a (fake) child and then raises inside the launcher, as an unexpected error would; 'sigterm' sends SIGTERM to
    the launcher mid-component; 'budget' stops the shared ledger, as a refused reservation does, and exits 1."""

    def __init__(self, ledger, **behaviour):
        self.ledger, self.behaviour, self.calls, self.argv = ledger, behaviour, [], {}
        self.cases = [{'case': 'c1/clean-1'}]
        self.ladder_configuration = ('clean-ladder-stage-a', 'd3b4a5f696c7cc82')
        self.prod_failed = 0

    def __call__(self, argv, log_path, on_start=lambda process: None):
        script = Path(str(argv[1])).name
        self.calls.append(script)
        self.argv[script] = [str(a) for a in argv]
        how = self.behaviour.get(script, 'ok')
        if isinstance(how, list):
            how = how.pop(0)
        if how == 'die':
            self.child = FakeChild()
            on_start(self.child)
            raise RuntimeError('an unexpected error in the launcher')
        if how == 'sigterm':
            os.kill(os.getpid(), signal.SIGTERM)
        if how == 'killed':
            return -9
        if how == 'budget':
            self.ledger.stop('a reservation would pass the ceiling')
            return 1
        if how == 'fail':
            return 1
        value = lambda flag: Path(str(argv[argv.index(flag) + 1]))
        if script == 'run_live.py':
            value('--output').write_text('trace')
        elif script == 'budget_step2.py':
            Path(str(argv[-1])).mkdir()
            (Path(str(argv[-1])) / 'library.json').write_text('{}')
        elif script == 'build_cases.py':
            value('--output').write_text(json.dumps(self.cases))
        elif script in ('stage_a.py', 'stage_a_astra.py'):
            passes = int(str(argv[argv.index('--passes') + 1]))
            for pass_number in range(1, passes + 1):
                (value('--folder') / f'send-{pass_number}').mkdir(parents=True)
                conn = sqlite3.connect(value('--folder') / f'send-{pass_number}' / 'archive.sqlite')
                conn.execute('create table model_calls (config_version, config_checksum)')
                configuration = self.ladder_configuration
                if isinstance(configuration, dict):                   # a configuration per pass
                    configuration = configuration[pass_number]
                conn.execute('insert into model_calls values (?, ?)', configuration)
                conn.commit()
                conn.close()
        elif script == 'budget_replay.py':
            (value('--views').parent / 'replay.log').write_text(
                f"totals: {{'items': 13, 'failed': {self.prod_failed}, 'not_processed': 0}}\n")
        return 0


class FakeChild:
    pid = None

    def __init__(self):
        self.terminated = False

    def poll(self):
        return 0 if self.terminated else None

    def terminate(self):
        self.terminated = True

    def wait(self, timeout=None):
        return -15

    def kill(self):
        self.terminated = True


def left_started(draw, root, ledger, component='step2'):
    """The state a SIGKILL of the launcher leaves: the attempt saved as started and the launcher's entry never removed."""
    record = {'identity': draw.identity(), 'state': 'running', 'components': {
        'step1': {'attempts': [{'folder': 'step1', 'state': 'completed'}], 'state': 'completed', 'folder': 'step1'},
        component: {'attempts': [{'folder': component, 'state': 'started'}]}}}
    (root / 'c1').mkdir(parents=True, exist_ok=True)
    (root / 'c1' / 'run.json').write_text(json.dumps(record))
    ledger.register_launcher('c1', root / 'c1' / 'launch.lock')


@pytest.fixture()
def setup(tmp_path, monkeypatch):
    credentials = tmp_path / 'credentials-placeholder.json'
    credentials.write_text('{}')
    monkeypatch.setattr(run_fresh, 'CREDENTIALS', credentials)
    ledger_path = tmp_path / 'ledger.json'
    run_fresh.budget_replay.SharedLedger.init(ledger_path, 15.0)
    ledger = run_fresh.budget_replay.SharedLedger(ledger_path)

    def draw(kind='clean', label='c1', components=None, check=lambda argv, log: 0, options=OPTIONS):
        return run_fresh.Draw(kind, tmp_path / 'root', label, ledger_path, options, run_component=components, run_check=check)
    return ledger, draw, tmp_path / 'root'


def test_success_runs_every_component_in_order_hands_each_its_inputs_and_unregisters(setup):
    ledger, draw, root = setup
    components = Components(ledger)
    record = draw(components=components).launch()
    assert record['state'] == 'complete'
    assert components.calls == ['run_live.py', 'budget_step2.py', 'build_cases.py', 'stage_a.py', 'run_stage_b.py']
    inputs = json.loads((root / 'c1' / 'judge-inputs.json').read_text())['c1']
    assert inputs['trace'] == str(root / 'c1' / 'step1' / 'trace.sqlite') and inputs['ladders'].endswith('ladder/send-1/outcomes.jsonl')
    assert inputs['output_root'] == str(root / 'c1' / 'judge')
    assert json.loads((root / 'c1' / 'step1' / 'manifest.json').read_text())['item_limit'] == 13
    stage_a_argv = components.argv['stage_a.py']
    assert stage_a_argv[stage_a_argv.index('--cap') + 1] == '15.0'                 # the local cap is the shared ceiling
    assert ledger.read().get('launchers') == {}                                    # removed on a normal end
    assert all(a.get('started at') and a.get('ended at') for e in record['components'].values() for a in e['attempts'])


def test_a_stopped_ledger_starts_nothing(setup):
    ledger, draw, root = setup
    ledger.stop('another draw crashed')
    components = Components(ledger)
    record = draw(components=components).launch()
    assert components.calls == [] and 'another draw crashed' in record['refused launches'][0]


def test_a_first_stop_awaits_a_redo_decision_and_only_a_reasoned_redo_goes_on(setup):
    ledger, draw, root = setup
    components = Components(ledger, **{'run_live.py': ['fail', 'ok']})
    record = draw(components=components).launch()
    assert record['state'] == 'awaiting a redo decision' and record['awaiting'] == 'step1' and not ledger.read()['stopped']
    with pytest.raises(SystemExit, match='awaits a redo decision'):
        draw(components=components).launch()
    with pytest.raises(SystemExit, match='needs --redo-reason'):
        draw(components=components).launch(redo='step1')
    record = draw(components=components).launch(redo='step1', redo_reason=REASON)
    assert record['state'] == 'complete' and record['components']['step1']['folder'] == 'step1-redo'
    assert record['components']['step1']['attempts'][1]['redo reason'] == REASON


def test_a_redo_that_stops_again_stops_the_whole_run_and_a_third_launch_sends_nothing(setup):
    ledger, draw, root = setup
    components = Components(ledger, **{'budget_step2.py': ['fail', 'fail']})
    draw(components=components).launch()
    record = draw(components=components).launch(redo='step2', redo_reason=REASON)
    assert record['state'] == 'stopped' and ledger.read()['stopped'] and 'c1: step2' in ledger.read()['stop_reason']
    draw(components=components).launch(redo='step2', redo_reason=REASON)
    assert components.calls.count('budget_step2.py') == 2


def test_a_child_killed_by_a_signal_is_a_crash_that_stops_the_run(setup):
    ledger, draw, root = setup
    components = Components(ledger, **{'run_live.py': 'killed'})
    record = draw(components=components).launch()
    assert record['components']['step1']['attempts'][-1]['state'] == 'crashed' and record['state'] == 'stopped'
    assert ledger.read()['stopped'] and 'crashed' in ledger.read()['stop_reason']


def test_an_interrupted_launcher_records_the_crash_stops_the_run_and_unregisters(setup):
    ledger, draw, root = setup
    components = Components(ledger, **{'budget_step2.py': 'sigterm'})
    with pytest.raises(run_fresh.Interrupted):
        draw(components=components).launch()
    record = json.loads((root / 'c1' / 'run.json').read_text())
    assert record['components']['step2']['attempts'][-1]['state'] == 'crashed' and ledger.read()['stopped']
    assert ledger.read().get('launchers') == {}


def test_an_unexpected_launcher_error_ends_the_child_records_the_crash_and_stops_the_run_before_unregistering(setup):
    ledger, draw, root = setup
    components = Components(ledger, **{'budget_step2.py': 'die'})
    with pytest.raises(RuntimeError):
        draw(components=components).launch()
    record = json.loads((root / 'c1' / 'run.json').read_text())
    assert record['components']['step2']['attempts'][-1]['state'] == 'crashed' and components.child.terminated
    assert 'RuntimeError' in ledger.read()['stop_reason'] and ledger.read().get('launchers') == {}


def test_the_stop_is_written_before_the_child_is_ended_and_refuses_other_sends_while_it_ends(setup, monkeypatch):
    """Council mo round 5: while the launcher waits for its child to end, the run is already stopped."""
    ledger, draw, root = setup
    seen = {}
    sent = []
    monkeypatch.setattr(urllib.request, 'urlopen', lambda request, *a, **k: sent.append(request))

    class SlowChild(FakeChild):
        def terminate(self):
            seen['stopped while ending the child'] = ledger.read()['stopped']
            remove = run_fresh.budget_replay.install_stop_gate(ledger)      # another draw's send during the wait
            try:
                urllib.request.urlopen(urllib.request.Request('https://example.invalid/', data=b'{}'))
            except urllib.error.HTTPError as refusal:
                seen['other send'] = refusal.code
            finally:
                remove()
            super().terminate()
    components = Components(ledger, **{'budget_step2.py': 'die'})
    original = components.__call__

    def with_slow_child(argv, log_path, on_start=lambda process: None):
        if Path(str(argv[1])).name == 'budget_step2.py':
            on_start(SlowChild())
            raise RuntimeError('an unexpected error in the launcher')
        return original(argv, log_path, on_start)
    with pytest.raises(RuntimeError):
        draw(components=with_slow_child).launch()
    assert seen == {'stopped while ending the child': True, 'other send': 403} and sent == []


def test_a_signal_just_after_started_is_saved_is_still_a_crash(setup, monkeypatch):
    """Council mo round 5: the crash is judged from the record on disk, so the instant between saving `started` and calling the
    component is covered."""
    ledger, draw, root = setup
    original_save = run_fresh.Draw.save
    fired = []

    def save_then_signal(self, record):
        original_save(self, record)
        if not fired and any(e['attempts'] and e['attempts'][-1]['state'] == 'started' for e in record['components'].values()):
            fired.append(1)
            raise run_fresh.Interrupted('SIGTERM')
    monkeypatch.setattr(run_fresh.Draw, 'save', save_then_signal)
    components = Components(ledger)
    with pytest.raises(run_fresh.Interrupted):
        draw(components=components).launch()
    record = json.loads((root / 'c1' / 'run.json').read_text())
    assert components.calls == [] and record['components']['step1']['attempts'][-1]['state'] == 'crashed'
    assert ledger.read()['stopped'] and ledger.read().get('launchers') == {}


@pytest.mark.parametrize('after', ['step1', 'judge'])
def test_an_interruption_between_components_or_before_the_end_is_saved_stops_the_run(setup, monkeypatch, after):
    """Council mo round 6: a signal after a component is saved as completed and before the next starts (or before the draw is saved
    complete) is a crash: the run stops before the registration is removed, and another draw is refused."""
    ledger, draw, root = setup
    original_save = run_fresh.Draw.save
    fired = []

    def save_then_signal(self, record):
        original_save(self, record)
        entry = record['components'].get(after, {})
        if not fired and entry.get('state') == 'completed' and record['state'] == 'running':
            fired.append(1)
            raise run_fresh.Interrupted('SIGTERM')
    monkeypatch.setattr(run_fresh.Draw, 'save', save_then_signal)
    with pytest.raises(run_fresh.Interrupted):
        draw(components=Components(ledger)).launch()
    record = json.loads((root / 'c1' / 'run.json').read_text())
    assert record['state'] == 'stopped' and ledger.read()['stopped'] and ledger.read().get('launchers') == {}
    other = Components(ledger)
    draw(kind='prod', label='p1', components=other).launch()
    assert other.calls == []


def test_a_refusal_before_any_work_unregisters_without_stopping_the_run(setup):
    ledger, draw, root = setup
    with pytest.raises(SystemExit, match='nothing started'):
        draw(components=Components(ledger), check=lambda argv, log: 1).launch()
    assert not ledger.read()['stopped'] and ledger.read().get('launchers') == {}


def test_a_stop_that_cannot_be_written_keeps_the_registration_for_the_gate(setup, monkeypatch):
    ledger, draw, root = setup
    components = Components(ledger, **{'budget_step2.py': 'die'})
    monkeypatch.setattr(run_fresh.budget_replay.SharedLedger, 'stop', lambda self, reason: (_ for _ in ()).throw(OSError('disk full')))
    with pytest.raises((RuntimeError, OSError)):
        draw(components=components).launch()
    assert 'c1' in ledger.read().get('launchers', {})          # once this process's lock is gone, the gate stops the run


def test_an_attempt_left_started_by_a_killed_launcher_is_a_crash_at_the_next_launch_with_no_redo(setup):
    ledger, draw, root = setup
    left_started(draw(), root, ledger)
    components = Components(ledger)
    record = draw(components=components).launch(redo='step2', redo_reason=REASON)
    assert record['components']['step2']['attempts'][-1]['state'] == 'crashed' and record['state'] == 'stopped'
    assert ledger.read()['stop_reason'] == 'the launcher of c1 is gone' and components.calls == []


def test_a_launcher_that_died_registered_is_found_by_the_gate_before_any_send(setup, monkeypatch):
    ledger, draw, root = setup
    dead_lock = root / 'p1' / 'launch.lock'
    dead_lock.parent.mkdir(parents=True)
    dead_lock.write_text('')
    ledger.register_launcher('p1', dead_lock)                 # a launcher SIGKILLed after registering: nobody holds its lock
    sent = []
    monkeypatch.setattr(urllib.request, 'urlopen', lambda request, *a, **k: sent.append(request))
    remove = run_fresh.budget_replay.install_stop_gate(ledger)
    try:
        with pytest.raises(urllib.error.HTTPError) as refusal:
            urllib.request.urlopen(urllib.request.Request('https://example.invalid/', data=b'{}'))
    finally:
        remove()
    assert refusal.value.code == 403 and sent == [] and ledger.read()['stop_reason'] == 'the launcher of p1 is gone'


def test_a_live_launcher_keeps_the_run_going(setup):
    ledger, draw, root = setup
    live_lock = root / 'p1' / 'launch.lock'
    live_lock.parent.mkdir(parents=True)
    with open(live_lock, 'w') as held:
        fcntl.flock(held, fcntl.LOCK_EX)
        ledger.register_launcher('p1', live_lock)
        assert not ledger.stop_if_a_launcher_is_gone().get('stopped')


def test_a_launcher_that_dies_between_the_probe_and_the_new_lock_is_still_caught(setup, monkeypatch):
    """Council mo round 4: the old launcher is alive when the probe runs and dead when the new launcher takes the lock. The probe and the
    lock are one ledger-locked step, and a label still registered once its lock is held is a dead launcher."""
    ledger, draw, root = setup
    left_started(draw(), root, ledger)
    monkeypatch.setattr(run_fresh.budget_replay, 'lock_is_free', lambda path: False)     # the probe sees the old launcher alive
    record = draw(components=Components(ledger)).launch()
    assert ledger.read()['stop_reason'] == 'the launcher of c1 is gone'
    assert record['components']['step2']['attempts'][-1]['state'] == 'crashed'


def test_a_later_launch_with_other_inputs_is_refused(setup):
    ledger, draw, root = setup
    draw(components=Components(ledger, **{'run_live.py': 'fail'})).launch()
    with pytest.raises(SystemExit, match='this launch differs'):
        draw(components=Components(ledger), options={'until_day': '2026-07-14', 'passes': 1}).launch(redo='step1', redo_reason=REASON)


def test_a_budget_refusal_stops_this_draw_and_every_other_draw_at_its_next_launch(setup):
    ledger, draw, root = setup
    record = draw(components=Components(ledger, **{'run_live.py': 'budget'})).launch()
    assert record['state'] == 'stopped' and 'the shared ledger' in record['stopped']
    other = Components(ledger)
    draw(kind='prod', label='p1', components=other).launch()
    assert other.calls == []


def test_another_draw_stopping_the_run_between_components_keeps_the_finished_one_and_starts_no_more(setup):
    ledger, draw, root = setup
    components = Components(ledger)
    original = components.__call__

    def stop_after_step1(argv, log_path, on_start=lambda process: None):
        status = original(argv, log_path, on_start)
        if Path(str(argv[1])).name == 'run_live.py':
            ledger.stop('p1: prod crashed')
        return status
    record = draw(components=stop_after_step1).launch()
    assert record['components']['step1']['state'] == 'completed' and record['state'] == 'stopped'
    assert components.calls == ['run_live.py'] and 'before step2' in record['stopped']


@pytest.mark.parametrize('script, component', [('stage_a.py', 'ladder'), ('run_stage_b.py', 'judge'), ('build_cases.py', 'cases')])
def test_the_cases_the_ladder_and_the_judge_have_no_outer_redo(setup, script, component):
    ledger, draw, root = setup
    record = draw(components=Components(ledger, **{script: 'fail'})).launch()
    assert record['state'] == 'stopped' and f'c1: {component}' in ledger.read()['stop_reason']


def test_a_judge_found_started_stops_the_run_and_the_judge_is_not_launched_again(setup):
    ledger, draw, root = setup
    left_started(draw(), root, ledger, component='judge')
    components = Components(ledger)
    record = draw(components=components).launch(redo='judge', redo_reason=REASON)
    assert record['state'] == 'stopped' and 'run_stage_b.py' not in components.calls
    assert record['components']['judge']['attempts'][-1]['state'] == 'crashed'


def test_a_draw_that_opened_no_thesis_skips_the_ladder_and_the_judge(setup):
    ledger, draw, root = setup
    components = Components(ledger)
    components.cases = []
    record = draw(components=components).launch()
    assert record['state'] == 'complete' and 'stage_a.py' not in components.calls
    assert record['components']['ladder']['state'] == record['components']['judge']['state'] == 'skipped'


def test_a_ladder_run_under_another_configuration_stops_the_run(setup):
    ledger, draw, root = setup
    components = Components(ledger)
    components.ladder_configuration = ('clean-ladder-stage-a', '0000000000000000')
    record = draw(components=components).launch()
    assert record['state'] == 'stopped' and 'not the frozen' in ledger.read()['stop_reason']


def test_a_failed_precondition_starts_nothing(setup):
    ledger, draw, root = setup
    components = Components(ledger)
    with pytest.raises(SystemExit, match='nothing started'):
        draw(components=components, check=lambda argv, log: 1).launch()
    assert components.calls == []


def test_a_second_launch_while_one_runs_is_refused(setup):
    ledger, draw, root = setup
    (root / 'c1').mkdir(parents=True)
    with open(root / 'c1' / 'launch.lock', 'w') as held:
        fcntl.flock(held, fcntl.LOCK_EX)
        with pytest.raises(SystemExit, match='another launch'):
            draw(components=Components(ledger)).launch()


def test_production_with_failed_items_awaits_a_redo_and_a_clean_replay_completes(setup):
    ledger, draw, root = setup
    components = Components(ledger)
    components.prod_failed = 2
    record = draw(kind='prod', label='p1', components=components).launch()
    assert record['state'] == 'awaiting a redo decision' and record['prod totals']['failed'] == 2
    assert '--cap' not in components.argv['budget_replay.py']                     # production has no cap of its own
    components.prod_failed = 0
    record = draw(kind='prod', label='p1', components=components).launch(redo='prod', redo_reason=REASON)
    assert record['state'] == 'complete' and record['components']['prod']['folder'] == 'prod-redo'


def test_a_folder_left_without_a_recorded_attempt_stops_the_run(setup):
    ledger, draw, root = setup
    (root / 'c1' / 'step1').mkdir(parents=True)
    record = draw(components=Components(ledger)).launch()
    assert record['state'] == 'stopped' and 'exists with no recorded attempt' in record['stopped']


# The release comparison's options (D667; plan §1.5 A, C, D, E). Defaults are unchanged: the success test above runs stage_a.py.

def comparison_options(tmp_path, **extra):
    limits = tmp_path / 'comparison-limits.json'
    limits.write_text(json.dumps({'max_usd': 40.0, 'max_seconds': 172800, 'max_calls': 12000,
                                  'input_usd_per_million': 0.5, 'output_usd_per_million': 1.2}))
    return dict(OPTIONS, items=str(run_fresh.ITEMS), limits=str(limits), judge_end_day='2026-07-03', **extra)


def test_the_given_items_limits_and_judge_end_day_reach_every_component(setup, tmp_path):
    """§1.2 A, §1.5 C and E: both systems read the given items database, Step 1 gets the given limits, the judge walks to the given day."""
    ledger, draw, root = setup
    options = comparison_options(tmp_path)
    components = Components(ledger)
    assert draw(components=components, options=options).launch()['state'] == 'complete'
    step1 = components.argv['run_live.py']
    assert step1[step1.index('--source') + 1] == str(run_fresh.ITEMS)
    assert json.loads((root / 'c1' / 'step1' / 'limits.json').read_text())['max_calls'] == 12000
    assert json.loads((root / 'c1' / 'judge-inputs.json').read_text())['c1']['end_day'] == '2026-07-03'
    prod = Components(ledger)
    assert draw(kind='prod', label='p1', components=prod, options=options).launch()['state'] == 'complete'
    replay = prod.argv['budget_replay.py']
    assert replay[replay.index('--testdb') + 1] == str(run_fresh.ITEMS)


def test_the_astra_variant_runs_the_wrapper_and_checks_every_pass(setup, tmp_path):
    """§1.5 D: astra-frozen runs stage_a_astra.py; every pass's archive must carry the astra configuration."""
    ledger, draw, root = setup
    astra = tuple(run_fresh.LADDER_CONFIGURATIONS['astra-frozen'].split())
    components = Components(ledger)
    components.ladder_configuration = astra
    options = comparison_options(tmp_path, ladder_variant='astra-frozen', passes=3)
    assert draw(components=components, options=options).launch()['state'] == 'complete'
    assert 'stage_a_astra.py' in components.calls and 'stage_a.py' not in components.calls


def test_one_pass_under_another_configuration_stops_the_run(setup, tmp_path):
    """§1.5 D: a pass the judge does not read is checked too; a luna pass in an astra draw stops the run."""
    ledger, draw, root = setup
    astra = tuple(run_fresh.LADDER_CONFIGURATIONS['astra-frozen'].split())
    luna = tuple(run_fresh.LADDER_CONFIGURATION.split())
    components = Components(ledger)
    components.ladder_configuration = {1: astra, 2: astra, 3: luna}
    options = comparison_options(tmp_path, ladder_variant='astra-frozen', passes=3)
    record = draw(components=components, options=options).launch()
    assert record['state'] == 'stopped' and 'astra-frozen configuration' in record['stopped'] and ledger.read()['stopped']

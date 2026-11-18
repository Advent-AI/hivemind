"""One draw of the diagnostic same-day run (WIRING-DESIGN.md §A, §D; D447, D448; council mo, D449): a clean draw (Step 1 c8 → Steps 2–3
→ the opened theses as cases → the ladder step → the frozen judge) or a production draw (v118 through `budget_replay`), every paid call on
one shared ledger. One launcher process runs one draw; several draws run at once, each in its own folder `<root>/<label>`, on one ledger.

**States** (`<root>/<label>/run.json`, written before and after each component): each attempt is `started`, `completed`, `stopped`
(with its reason) or `crashed`. The draw is `running`, `complete`, `awaiting a redo decision` or `stopped`. The draw's kind, label,
ledger and options are written at its first launch; a later launch that differs is refused.

**The launcher is alive while it holds `<root>/<label>/launch.lock`.** Before it takes the lock it runs the ledger's dead-launcher check
(under the ledger's lock, so its own new lock never hides a stale entry); after taking it, it registers the lock path on the ledger, and it
removes the entry before releasing the lock on a normal end. A launcher that dies without removing it (a SIGKILL) is found by the stop
gate before the next actual send of any process, which stops the ledger: its orphaned child's next send is refused, and so is every other
draw's.

**What stops the whole run** (the shared ledger's persisted stop): a budget refusal or an overrun; a crash (a component killed by a signal,
a launcher interrupted, a launcher found dead, an attempt found `started`); a component that stops after its one redo, or that has no
redo (the cases, the ladder step, the judge, whose own one redo is inside `run_stage_b`); a configuration that is not the frozen one.

**The one redo** (Step 1, Step 2, production; D449): a first stop that is neither the ledger's nor a crash ends this draw only, as
`awaiting a redo decision`. The redo is a later launch with `--redo <component> --redo-reason <text>`, made only when the component's
output shows an eligible failure (a transport failure after its own retries, an answer refused or not fitting its schema); the reason is
written to the record. Once per component, in a new folder; its stop stops the run.

  python3 run_fresh.py clean --root R --label c1 --ledger L [--until-day 2026-07-01] [--passes 3] [--redo C --redo-reason TEXT]
  python3 run_fresh.py prod  --root R --label p1 --ledger L [--until-day 2026-07-01] [--redo prod --redo-reason TEXT]

A window other than the full run's (D486's lean step 2) is given with --manifest M: a Step 1 manifest whose items both systems read (built by
`docs/research/2026-11-14-use-acceptance/fresh_week_inputs.py`); the draw then runs from its from_day to --until-day (default its until_day).
"""
import argparse
import ast
import fcntl
import hashlib
import importlib.util
import json
import os
import shutil
import signal
import sqlite3
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STEP4 = ROOT / 'clean-arch/step4-2026-11-10'
STAGE2 = ROOT / 'clean-arch/e2e-2026-11-09'
ITEMS = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
FROM_DAY, LAST_DAY = '2026-07-01', '2026-07-14'
CLEAN = ('step1', 'step2', 'cases', 'ladder', 'judge')
PROD = ('prod',)
REDO_ALLOWED = {'step1', 'step2', 'prod'}                          # design §D's table: the ladder and the judge have no outer redo
LADDER_CONFIGURATION = 'clean-ladder-stage-a d3b4a5f696c7cc82'       # run 4's, the configuration D426 froze
ASTRA_WRAPPER = ROOT / 'docs/research/2026-11-17-product-comparison/stage0/stage_a_astra.py'   # D667: the frozen request on gpt-6-astra
LADDER_CONFIGURATIONS = {'frozen': LADDER_CONFIGURATION,
                         'astra-frozen': 'clean-ladder-stage-a 14d0e269c8fe0335'}   # stage_a_astra.configuration_checksum
CREDENTIALS = Path.home() / '.config/hivemind/credentials.json'
PROD_CONFIG = ROOT / 'poc/config/poc-v118.json'
PROD_CONFIG_SHA256 = '1f2246047d121849fe2db46d31736373d28bc6ea08ccf7887a9675580444ce81'   # the config draws q1–q3 ran


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


budget_replay = load('budget_replay', HERE / 'budget_replay.py')


def now():
    """Wall-clock time for the timing report only (nothing is ordered by it)."""
    import time
    return time.strftime('%Y-%m-%dT%H:%M:%S%z')


class Interrupted(BaseException):
    """SIGTERM or SIGINT reached the launcher."""


def child_environment():
    """The launcher's environment, with the repository's `src` first on the import path (an existing path is kept after it)."""
    path = os.pathsep.join(part for part in (str(ROOT / 'src'), os.environ.get('PYTHONPATH')) if part)
    return dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=path)


def execute(argv, log_path, on_start=lambda process: None):
    """Run one component as its own process (its output to its log); `on_start` receives the process before the launcher waits.
    Returns the exit status: negative when a signal killed it."""
    env = child_environment()
    with open(log_path, 'a') as log:
        process = subprocess.Popen([str(a) for a in argv], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, env=env)
        on_start(process)
        return process.wait()


def check(argv, log_path):
    with open(log_path, 'a') as log:
        return subprocess.run([str(a) for a in argv], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, env=child_environment()).returncode


def frozen_unseeded_changed(listing=ROOT / 'clean-arch/unseeded-2026-11-10/unseeded-frozen.sha256'):
    """The files of the unseeded freeze whose sha256 differs from the listing (paths relative to the listing's folder)."""
    changed = []
    for line in listing.read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        path = listing.parent / name.strip()
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            changed.append(name.strip())
    return changed


def preconditions(kind, run_check=check, log_path=None):
    """The checks the old launcher made, plus the frozen production configuration; a failure starts nothing."""
    failures = []
    if not CREDENTIALS.exists():                                       # its existence only; never read here
        failures.append('the credentials file is missing')
    changed = frozen_unseeded_changed()
    if changed:
        failures.append(f'a frozen unseeded file changed: {changed}')
    checks = [([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', ROOT / 'tests/test_frozen_clean_step2.py'], 'a frozen Step 2 file changed')]
    if kind == 'clean':
        checks.append(([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', ROOT / 'clean-arch/step1/test_runner.py', '-k', 'adopted_c8'],
                       'the PRD request is not c8'))
    for argv, failure in checks:
        if run_check(argv, log_path) != 0:
            failures.append(failure)
    if kind == 'prod' and hashlib.sha256(PROD_CONFIG.read_bytes()).hexdigest() != PROD_CONFIG_SHA256:
        failures.append('poc-v118.json is not the configuration q1–q3 ran')
    return failures


def manifest_until(until_day, manifest_path=None, items=ITEMS):
    """The run's manifest (the full run's 243 items, or the one given) cut to the items published on or before `until_day`, in the same order."""
    manifest = json.loads(Path(manifest_path or STAGE2 / 'stage2-manifest.json').read_text())
    if until_day == manifest['until_day']:
        return manifest
    conn = sqlite3.connect(f'file:{items}?mode=ro', uri=True)
    try:
        day_of = {item_id: conn.execute('select publication_day from items where input_id=?', (item_id,)).fetchone()[0]
                  for item_id in manifest['item_ids']}
    finally:
        conn.close()
    kept = [item_id for item_id in manifest['item_ids'] if day_of[item_id] <= until_day]
    if not kept:
        raise SystemExit(f'no item on or before {until_day}')
    return dict(manifest, until_day=until_day, item_limit=len(kept), item_ids=kept)


class Draw:
    def __init__(self, kind, root, label, ledger_path, options, run_component=execute, run_check=check):
        self.kind, self.label, self.options = kind, label, dict(options)
        self.folder = Path(root) / label
        self.ledger_path = Path(ledger_path).resolve()
        self.ledger = budget_replay.SharedLedger(self.ledger_path)
        self.run_component, self.run_check = run_component, run_check
        self.record_path = self.folder / 'run.json'
        self.lock_path = self.folder / 'launch.lock'
        self.child = None

    # the record
    def identity(self):
        return {'kind': self.kind, 'label': self.label, 'ledger': str(self.ledger_path), 'options': dict(self.options)}

    def load(self):
        if self.record_path.exists():
            return json.loads(self.record_path.read_text())
        return {'identity': self.identity(), 'state': 'running', 'components': {}}

    def save(self, record):
        temporary = self.record_path.with_suffix('.tmp')
        temporary.write_text(json.dumps(record, indent=1) + '\n')
        os.replace(temporary, self.record_path)

    def stop_run(self, record, reason):
        """A stop of the whole run: on the shared ledger first (every other draw stops at its next send), then here."""
        self.ledger.stop(f'{self.label}: {reason}')
        record['state'], record['stopped'] = 'stopped', reason
        self.save(record)
        return record

    # one launch
    def launch(self, redo=None, redo_reason=None):
        if redo is not None and not (redo_reason or '').strip():
            raise SystemExit('--redo needs --redo-reason: what in the component\'s output shows an eligible failure')
        self.folder.mkdir(parents=True, exist_ok=True)
        with open(self.lock_path, 'w') as lock:
            if not self.ledger.claim_launcher(self.label, lock):    # the probe, this lock and the registration in one ledger-locked step
                raise SystemExit(f'another launch of {self.label} is running')
            handlers = {}

            def interrupted(signal_number, frame):
                raise Interrupted(signal.Signals(signal_number).name)
            for signal_number in (signal.SIGTERM, signal.SIGINT):
                handlers[signal_number] = signal.signal(signal_number, interrupted)
            self.working = False
            try:
                return self._launch(redo, redo_reason)
            finally:
                self.close(handlers)

    def close(self, handlers):
        """Fail closed (council mo, D449). An abnormal exit is any exit of a launch that began work (past its refusals) other than a
        normal return, or any exit that leaves an attempt `started` in the record on disk; its first write is the shared stop, before
        the child is ended and the record marked. The registration is removed only after a normal end, a refusal before any work, or
        that stop; any other exit (a stop that cannot be written, an error while reading the record) leaves it, so the gate stops the
        run once this process's lock is released. Further signals are ignored while closing."""
        for signal_number in handlers:
            signal.signal(signal_number, signal.SIG_IGN)
        try:
            in_flight = sys.exc_info()[1]
            started = self.started_attempt()
            if started is not None or (in_flight is not None and self.working):
                reason = (f'the launcher ended abnormally ({type(in_flight).__name__}: {str(in_flight)[:200]})' if in_flight is not None
                          else 'the launcher ended with an attempt still started')
                self.ledger.stop(f'{self.label}: {started or "between components"}: {reason}')   # the first write
                self.end_child()
                self.mark_crashed(reason)
            self.ledger.remove_launcher(self.label)
        finally:
            for signal_number, handler in handlers.items():
                signal.signal(signal_number, handler)

    def started_attempt(self):
        """The component whose last attempt the record on disk holds as `started`, or None."""
        record = self.load()
        return next((component for component, entry in record['components'].items()
                     if entry['attempts'] and entry['attempts'][-1]['state'] == 'started'), None)

    def mark_crashed(self, reason):
        """The attempt left `started`, if any, becomes `crashed`; the draw is stopped either way."""
        record = self.load()
        record['state'], record['stopped'] = 'stopped', f'the launcher crashed: {reason}'
        for component, entry in record['components'].items():
            if entry['attempts'] and entry['attempts'][-1]['state'] == 'started':
                entry['attempts'][-1].update(state='crashed', reason=reason)
                record['stopped'] = f'{component} crashed: {reason}'
        self.save(record)

    def _launch(self, redo, redo_reason):
        record = self.load()
        if record.get('identity') != self.identity():
            raise SystemExit(f"{self.label} was first launched as {record.get('identity')}; this launch differs: refused")
        for component, entry in record['components'].items():   # an attempt left started: its launcher died (a crash)
            if entry['attempts'] and entry['attempts'][-1]['state'] == 'started':
                entry['attempts'][-1].update(state='crashed', reason='found started at a later launch: its launcher died')
                return self.stop_run(record, f'{component} crashed in {entry["attempts"][-1]["folder"]} (recorded; no redo)')
        ledger_state = self.ledger.read()
        if ledger_state.get('stopped'):
            record.setdefault('refused launches', []).append(f"the run is stopped: {ledger_state.get('stop_reason')}")
            self.save(record)
            return record
        if record['state'] in ('stopped', 'complete'):
            return record
        if record['state'] == 'awaiting a redo decision' and redo != record.get('awaiting'):
            raise SystemExit(f"{self.label} awaits a redo decision on {record['awaiting']}: relaunch with --redo {record['awaiting']} "
                             '--redo-reason <text> after reading its output')
        failures = preconditions(self.kind, self.run_check, self.folder / 'preconditions.log')
        if failures:
            record.setdefault('refused launches', []).append('; '.join(failures))
            self.save(record)
            raise SystemExit('nothing started: ' + '; '.join(failures))
        record['state'] = 'running'
        record.pop('awaiting', None)
        self.working = True                                # from here on, any exit but a normal return stops the run (close)
        self.local_cap = ledger_state['ceiling']           # the shared ledger binds first: local reservations are smaller
        for component in (CLEAN if self.kind == 'clean' else PROD):
            entry = record['components'].setdefault(component, {'attempts': []})
            if entry.get('state') in ('completed', 'skipped'):
                continue
            stopped = self.ledger.read()
            if stopped.get('stopped'):                     # another draw, or a component of this one, stopped the run
                record['state'], record['stopped'] = 'stopped', f"the shared ledger, before {component}: {stopped.get('stop_reason')}"
                self.save(record)
                return record
            attempts = entry['attempts']
            if attempts:                                   # the last attempt stopped: only an explicit redo goes on (a stopped redo has
                # already stopped the run on the ledger, so a third attempt is refused above)
                if redo != component or component not in REDO_ALLOWED:
                    return self.stop_run(record, f'{component}: no redo allowed after {len(attempts)} attempt(s)')
            folder_name = component if not attempts else f'{component}-redo'
            if (self.folder / folder_name).exists():
                attempts.append({'folder': folder_name, 'state': 'crashed', 'reason': 'its folder exists with no recorded attempt'})
                return self.stop_run(record, f'{component}: {folder_name} exists with no recorded attempt')
            attempts.append({'folder': folder_name, 'state': 'started', 'started at': now(), **({'redo reason': redo_reason} if attempts else {})})
            self.save(record)
            outcome, reason = getattr(self, f'_{component}')(record, self.folder / folder_name)   # any exception: `close` handles it
            attempts[-1]['ended at'] = now()
            if outcome == 'crashed':
                attempts[-1].update(state='crashed', reason=reason)
                return self.stop_run(record, f'{component} crashed: {reason}')
            if outcome not in ('completed', 'skipped') and self.ledger.read().get('stopped'):
                attempts[-1].update(state='stopped', reason=f"the shared ledger: {self.ledger.read().get('stop_reason')}")
                record['state'], record['stopped'] = 'stopped', attempts[-1]['reason']
                self.save(record)
                return record
            if outcome in ('completed', 'skipped'):
                attempts[-1]['state'] = 'completed'
                entry['state'], entry['folder'] = outcome, folder_name
                if reason:
                    entry['note'] = reason
                self.save(record)
                continue
            attempts[-1].update(state='stopped', reason=reason)
            if outcome == 'stopped' and component in REDO_ALLOWED and len(attempts) == 1:
                record['state'], record['awaiting'] = 'awaiting a redo decision', component
                self.save(record)
                return record
            return self.stop_run(record, f'{component}: {reason}')
        record['state'] = 'complete'
        self.save(record)
        return record

    def end_child(self):
        if self.child is not None and self.child.poll() is None:
            self.child.terminate()
            try:
                self.child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.child.kill()
                self.child.wait()

    def done_folder(self, record, component):
        return self.folder / record['components'][component]['folder']

    def items(self):
        """The items database both systems read: the one given (--items), or the default corpus."""
        return Path(self.options.get('items', ITEMS))

    def _call(self, argv, folder, record=None):
        """Run a component; returns ('crashed', reason) for a signal exit, else (None, exit status)."""
        def started(process):
            self.child = process
            if record is not None and getattr(process, 'pid', None):
                attempt = next(entry['attempts'][-1] for entry in record['components'].values()
                               if entry['attempts'] and entry['attempts'][-1]['state'] == 'started')
                attempt['pid'] = process.pid                # for the operator and the proof; liveness is the launcher's lock
                self.save(record)
        status = self.run_component(argv, folder.parent / f'{folder.name}.log', started)
        self.child = None
        if status < 0:
            return 'crashed', f'killed by signal {-status} (see {folder.name}.log)'
        return None, status

    # the components: each returns (outcome, reason); outcome 'completed', 'stopped' (a redo may follow), 'stopped-run' or 'crashed'
    def _step1(self, record, folder):
        folder.mkdir()
        (folder / 'manifest.json').write_text(json.dumps(manifest_until(self.options['until_day'], self.options.get('manifest'), self.items()), indent=1))
        shutil.copy(ROOT / 'clean-arch/unseeded-2026-11-10/initial-empty.json', folder / 'initial.json')
        shutil.copy(STAGE2 / 'stage2-settings.json', folder / 'settings.json')
        shutil.copy(self.options.get('limits') or STAGE2 / 'stage2-limits.json', folder / 'limits.json')
        crash, status = self._call([sys.executable, ROOT / 'clean-arch/step1/run_live.py', '--source', self.items(), '--output', folder / 'trace.sqlite',
                                    '--manifest', folder / 'manifest.json', '--initial', folder / 'initial.json', '--settings', folder / 'settings.json',
                                    '--limits', folder / 'limits.json', '--shared-ledger', self.ledger_path], folder, record)
        if crash:
            return crash, status
        return ('completed', None) if status == 0 else ('stopped', f'run_live exit {status}: the trace is not complete (see its log)')

    def _step2(self, record, folder):
        trace = self.done_folder(record, 'step1') / 'trace.sqlite'
        crash, status = self._call([sys.executable, HERE / 'budget_step2.py', '--shared-ledger', self.ledger_path, trace, folder], folder, record)
        if crash:
            return crash, status
        if status != 0:
            return 'stopped', f'Step 2 exit {status}: refused, pending or unresolved links, or a failed call (see its log)'
        stamp = '\n'.join(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path}' for path in (trace, folder / 'library.json'))
        (folder / 'inputs.sha256').write_text(stamp + '\n')
        return 'completed', None

    def _cases(self, record, folder):
        folder.mkdir()
        step1 = self.done_folder(record, 'step1')
        crash, status = self._call([sys.executable, STEP4 / 'stage_a/build_cases.py', '--fresh', self.label, '--draws', step1, '--parts', 'trace.sqlite',
                                    '--output', folder / 'cases.json'], folder, record)
        if crash:
            return crash, status
        if status != 0:
            return 'stopped-run', f'build_cases exit {status}: the cases do not match the opened theses (see its log)'
        if not json.loads((folder / 'cases.json').read_text()):
            for component in ('ladder', 'judge'):
                record['components'][component] = {'attempts': [], 'state': 'skipped', 'note': 'the draw opened no thesis'}
            return 'completed', 'no thesis opened: the ladder step and the judge have nothing to do'
        return 'completed', None

    def _ladder(self, record, folder):
        cases = self.done_folder(record, 'cases') / 'cases.json'
        variant = self.options.get('ladder_variant', 'frozen')
        script = ASTRA_WRAPPER if variant == 'astra-frozen' else STEP4 / 'stage_a/stage_a.py'
        crash, status = self._call([sys.executable, script, '--folder', folder, '--cap', self.local_cap,
                                    '--passes', self.options['passes'], '--cases-file', cases, '--shared-ledger', self.ledger_path], folder, record)
        if crash:
            return crash, status
        if status != 0:
            return 'stopped-run', f'stage_a exit {status}: a pass is incomplete (see its log)'
        expected = LADDER_CONFIGURATIONS[variant]
        for pass_number in range(1, self.options['passes'] + 1):       # every pass, each on its own: an empty pass fails too
            archive = folder / f'send-{pass_number}' / 'archive.sqlite'
            if not archive.exists():
                return 'stopped-run', f'pass {pass_number} wrote no archive'
            conn = sqlite3.connect(f'file:{archive}?mode=ro', uri=True)
            try:
                found = sorted(f'{v} {c}' for v, c in conn.execute('select distinct config_version, config_checksum from model_calls').fetchall())
            finally:
                conn.close()
            if found != [expected]:
                record['configuration mismatch'] = {f'pass {pass_number}': found}
                return 'stopped-run', f'pass {pass_number} of the ladder ran {found}, not the {variant} configuration {expected}'
        return 'completed', None

    def _judge(self, record, folder):
        ladder = self.done_folder(record, 'ladder')
        inputs = {self.label: {'trace': str(self.done_folder(record, 'step1') / 'trace.sqlite'), 'step2': str(self.done_folder(record, 'step2')),
                               'ladders': str(ladder / 'send-1' / 'outcomes.jsonl'), 'ladder_archive': str(ladder / 'send-1' / 'archive.sqlite'),
                               'cases': str(self.done_folder(record, 'cases') / 'cases.json'), 'output_root': str(folder)}}
        if self.options.get('judge_end_day'):
            inputs[self.label]['end_day'] = self.options['judge_end_day']   # the judge walks and closes to this day (D667)
        inputs_path = self.folder / f'{folder.name}-inputs.json'
        inputs_path.write_text(json.dumps(inputs, indent=1))
        crash, status = self._call([sys.executable, STEP4 / 'stage_b/run_stage_b.py', '--root', folder, '--runs', self.label, '--inputs', inputs_path,
                                    '--cap', self.local_cap, '--shared-ledger', self.ledger_path], folder, record)
        if crash:
            return crash, status
        return ('completed', None) if status == 0 else ('stopped-run', f'run_stage_b exit {status}: the draw is incomplete after its own redo rule')

    def _prod(self, record, folder):
        folder.mkdir()
        argv = [sys.executable, HERE / 'budget_replay.py', '--ledger', self.ledger_path, '--from', self.options.get('from_day', FROM_DAY), '--until', self.options['until_day'],
                '--views', folder / 'views.sqlite', '--archive', folder / 'archive.sqlite', '--config', PROD_CONFIG, '--workers', 16]
        if 'items' in self.options:
            argv += ['--testdb', self.items()]                               # the same items database the clean draw reads
        crash, status = self._call(argv, folder, record)
        if crash:
            return crash, status
        if status != 0:
            return 'stopped', f'budget_replay exit {status} (see its log)'
        totals = [line for line in (folder / 'replay.log').read_text().splitlines() if line.startswith('totals: ')]
        if len(totals) != 1:
            return 'stopped', 'the replay wrote no totals line'
        counts = ast.literal_eval(totals[0][len('totals: '):])
        record['prod totals'] = counts
        if counts.get('failed') or counts.get('not_processed'):
            return 'stopped', f"{counts.get('failed')} failed and {counts.get('not_processed')} unprocessed items (see the log for transport failures)"
        return 'completed', None


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('kind', choices=('clean', 'prod'))
    parser.add_argument('--root', required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--ledger', required=True)
    parser.add_argument('--until-day', default=None)
    parser.add_argument('--manifest', default=None)
    parser.add_argument('--passes', type=int, default=3)
    parser.add_argument('--redo', default=None)
    parser.add_argument('--redo-reason', default=None)
    parser.add_argument('--items', default=None, help='the items database both systems read (default: the corpus)')
    parser.add_argument('--limits', default=None, help="Step 1's limits file (default: the frozen stage2-limits.json)")
    parser.add_argument('--ladder-variant', choices=sorted(LADDER_CONFIGURATIONS), default='frozen')
    parser.add_argument('--judge-end-day', default=None, help='the last day the judge walks and closes (default: the last article day)')
    arguments = parser.parse_args(argv)
    if not Path(arguments.ledger).exists():
        raise SystemExit('the shared ledger does not exist: it is created by a recorded decision (budget_replay.py --init-ledger)')
    window = (FROM_DAY, LAST_DAY)
    if arguments.manifest:
        given = json.loads(Path(arguments.manifest).read_text())
        window = (given['from_day'], given['until_day'])
    until_day = arguments.until_day or window[1]
    if not (window[0] <= until_day <= window[1]):
        raise SystemExit(f'--until-day must lie in {window[0]}..{window[1]}')
    options = {'until_day': until_day, 'passes': arguments.passes}
    if arguments.manifest:
        options.update(from_day=window[0], manifest=str(Path(arguments.manifest).resolve()))
    for key, value in (('items', arguments.items), ('limits', arguments.limits)):
        if value:
            options[key] = str(Path(value).resolve())
    if arguments.ladder_variant != 'frozen':
        options['ladder_variant'] = arguments.ladder_variant
    if arguments.judge_end_day:
        options['judge_end_day'] = arguments.judge_end_day
    record = Draw(arguments.kind, arguments.root, arguments.label, arguments.ledger, options).launch(arguments.redo, arguments.redo_reason)
    print(json.dumps({k: v for k, v in record.items() if k != 'components'}, indent=1))
    return 0 if record['state'] == 'complete' else 1


if __name__ == '__main__':
    sys.exit(main())

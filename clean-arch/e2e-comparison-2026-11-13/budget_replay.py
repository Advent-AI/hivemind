"""Production as it now runs (`scripts/replay.py`, `poc-v118`), with every paid call held to one shared ceiling (D442's comparison,
design shape B'). The replay is `hivemind.replay.run` with the same arguments `scripts/replay.py` passes; the only difference is the
transport, which the production code already accepts (`replay.run(transport=...)`, passed to extraction, matching, the collision judge
and the day's judging): `BudgetTransport` sends each request exactly as the production transports do, after reserving its worst cost
on a ledger shared by every run under one ceiling.

Reservation per attempt: a language-model request reserves (2 × its JSON bytes + 4,096) input tokens and its whole output cap
(`max_completion_tokens`) at `model.PRICES`; a Jev request reserves (2 × its bytes + 4,096) input tokens at Jev's input rate, times
Jev's own three attempts (`jev.transport` retries inside one call). A Jev call settles at three times its own reported input tokens
(a hidden retry is the same request, billed at most the same input; Jev's output is free), the whole charge settled so that one above
the reservation sets the overrun flag; usage missing, invalid or zero settles at the whole reservation. A language-model attempt goes out once (`max_attempts=1`) and is
sent again, up to three attempts with production's pauses, when the service gave no answer: no HTTP status, or 429 or 5xx, as
`model.openai_transport` retries; a client HTTP error is not. A response settles at its usage (the formula of `model.call`); one with no
usage, and every failed attempt, at its reservation. An attempt whose reservation would pass the ceiling is not sent: it raises
`model.TransportError`, and the production code records that item or judgement as failed. A response that costs more than its
reservation sets an overrun flag that refuses every later attempt of every run.

  python3 budget_replay.py --ledger L --from D --until D --views V --archive A [--config C] [--only NVDA] [--workers 16] [--cap X]
  python3 budget_replay.py --init-ledger L --ceiling 12.25
"""
import argparse
import contextlib
import fcntl
import io
import json
import math
import os
import sys
import threading
import time
import types
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, jev, model, parallel_day, replay, universe  # noqa: E402

CLIENT_ERRORS = {400, 401, 403, 404}
# How many reservations the calling thread holds and has not settled (the interception proofs read it). One object per process, kept in
# sys.modules, because each component loads this file under its own module object.
_MARK = sys.modules.setdefault('hivemind_shared_ledger_live_mark', types.ModuleType('hivemind_shared_ledger_live_mark'))
if not hasattr(_MARK, 'local'):
    _MARK.local = threading.local()
_LIVE = _MARK.local


def holds_live_reservation():
    """Whether the calling thread holds a reservation it has not yet settled (WIRING-DESIGN.md §B2, the interception trap)."""
    return getattr(_LIVE, 'depth', 0) > 0


def lock_is_free(lock_path):
    """Whether no process holds the lock file: a shared, non-blocking flock succeeds only when no exclusive holder is alive."""
    try:
        with open(lock_path, 'a') as handle:
            try:
                fcntl.flock(handle, fcntl.LOCK_SH | fcntl.LOCK_NB)
            except BlockingIOError:
                return False
            fcntl.flock(handle, fcntl.LOCK_UN)
            return True
    except OSError:
        return True


def install_stop_gate(ledger):
    """Process-wide: every `urllib.request.urlopen` call, a helper's internal retry included, first reads the shared ledger. When it is
    stopped, or when a registered launcher's lock is free (that launcher died without removing its entry: the gate then stops the
    ledger), the call is refused as HTTP 403 (no component retries a 403) and nothing is sent. An attempt whose read came before a stop
    was written may finish; one that reads after it is refused. Returns a function that removes the gate."""
    original = urllib.request.urlopen

    def gated(request, *arguments, **keywords):
        state = ledger.stop_if_a_launcher_is_gone()
        if state.get('stopped'):
            raise urllib.error.HTTPError(getattr(request, 'full_url', str(request)), 403,
                                         f"the shared ledger is stopped ({state.get('stop_reason')}): not sent", {},
                                         io.BytesIO(b'{"error": {"type": "shared_ledger_stopped"}}'))
        return original(request, *arguments, **keywords)
    urllib.request.urlopen = gated

    def remove():
        if urllib.request.urlopen is gated:
            urllib.request.urlopen = original
    return remove


class SharedLedger:
    """One JSON ledger for every run under a ceiling, guarded by an exclusive file lock (processes and threads). The first refused
    reservation, or an explicit `stop`, persists `stopped` with its reason under the lock: every later reservation, in any thread or
    process, is refused (WIRING-DESIGN.md §B2, D448)."""

    def __init__(self, path):
        self.path = Path(path)
        self.lock_path = self.path.with_suffix('.lock')
        self.attempts_path = self.path.with_suffix('.attempts.jsonl')   # one line per settled or refused attempt: the measurement record

    def _note(self, entry):
        """Append one attempt line (the process, the call kind, the amounts, the tokens when reported, the moment) for per-component
        spend and timing. Written only after the ledger's state is saved, and best-effort: a failed append never blocks a stop, a charge
        or an overrun. A crash between the two writes leaves the lines short of the ledger, never ahead of it; the tally reports the gap
        as unaccounted. One short append, so concurrent lines do not interleave."""
        line = json.dumps(dict(entry, pid=os.getpid(), at=time.strftime('%Y-%m-%dT%H:%M:%S%z'))) + '\n'
        try:
            with open(self.attempts_path, 'a') as handle:
                handle.write(line)
        except OSError:
            pass

    @contextlib.contextmanager
    def _locked(self):
        with open(self.lock_path, 'a+') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            try:
                state = json.loads(self.path.read_text())
                yield state
                temporary = self.path.with_suffix('.tmp')
                temporary.write_text(json.dumps(state, indent=1))
                os.replace(temporary, self.path)          # a reader never sees a half-written ledger
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)

    @staticmethod
    def init(path, ceiling):
        Path(path).write_text(json.dumps({'ceiling': ceiling, 'spent': 0.0, 'reserved': 0.0, 'overrun': False, 'refused': 0, 'attempts': 0,
                                          'stopped': False, 'stop_reason': None}, indent=1))

    def reserve(self, amount):
        with self._locked() as state:
            granted = not (state.get('stopped') or state['overrun'] or state['spent'] + state['reserved'] + amount > state['ceiling'])
            if granted:
                state['reserved'] += amount
                state['attempts'] += 1
            else:
                state['refused'] += 1
                if not state.get('stopped'):
                    state['stopped'] = True
                    state['stop_reason'] = 'overrun' if state['overrun'] else f'a reservation of ${amount:.6f} would pass the ${state["ceiling"]:.2f} ceiling'
        if not granted:
            self._note({'refused': amount})                  # after the stop is saved
            return False
        _LIVE.depth = getattr(_LIVE, 'depth', 0) + 1
        return True

    @staticmethod
    def estimate(request):
        """The shared reservation of one language-model attempt (WIRING-DESIGN.md §B): `llm_estimate`."""
        return llm_estimate(request)

    def settle(self, reserved, actual, kind='llm', tokens=None):
        """Settle one attempt. A missing, non-finite, zero or negative charge settles at the whole reservation: an answered paid
        request never costs nothing, and a failed attempt is charged its reservation. `kind` (llm, jev, embeddings) and the reported
        `tokens` go to the attempt line only."""
        _LIVE.depth = max(0, getattr(_LIVE, 'depth', 0) - 1)
        if not isinstance(actual, (int, float)) or isinstance(actual, bool) or not math.isfinite(actual) or actual <= 0:
            actual = reserved
        with self._locked() as state:
            state['reserved'] = max(0.0, state['reserved'] - reserved)
            state['spent'] += actual
            if actual > reserved + 1e-12:
                state['overrun'] = True
                if not state.get('stopped'):
                    state['stopped'], state['stop_reason'] = True, 'overrun'
        self._note({'kind': kind, 'reserved': reserved, 'charged': actual, **({'tokens': tokens} if tokens is not None else {})})

    def stop_if_a_launcher_is_gone(self):
        """Under the ledger's lock: a registered launcher whose lock no process holds died without removing its entry; the ledger is
        stopped. A relaunch calls this before it takes its own lock, so its new lock never makes a stale entry look alive; the stop gate
        calls it before every send. Returns the state after the check."""
        with self._locked() as state:
            if not state.get('stopped'):
                for label, lock_path in sorted((state.get('launchers') or {}).items()):
                    if lock_is_free(lock_path):
                        state['stopped'], state['stop_reason'] = True, f'the launcher of {label} is gone'
                        break
            return dict(state)

    def claim_launcher(self, label, lock_handle):
        """One step under the ledger's lock (council mo, D449): stop the ledger if any registered launcher's lock is free; try the
        launcher's own lock without blocking (False: another launch of this label is running); if this label is still registered once
        its lock is held, the previous launcher died without removing its entry, so the ledger stops; then register. The stop gate's
        probe takes the same lock, so no send can see a stale entry as alive while a new launcher takes its lock."""
        with self._locked() as state:
            launchers = state.setdefault('launchers', {})
            if not state.get('stopped'):
                for other, lock_path in sorted(launchers.items()):
                    if lock_is_free(lock_path):
                        state['stopped'], state['stop_reason'] = True, f'the launcher of {other} is gone'
                        break
            try:
                fcntl.flock(lock_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return False
            if label in launchers and not state.get('stopped'):
                state['stopped'], state['stop_reason'] = True, f'the launcher of {label} is gone'
            launchers[label] = os.path.abspath(lock_handle.name)
            return True

    def register_launcher(self, label, lock_path):
        """Register a launcher's lock path (tests and proofs; a launcher uses `claim_launcher`)."""
        with self._locked() as state:
            state.setdefault('launchers', {})[label] = str(lock_path)

    def remove_launcher(self, label):
        """Called by a launcher on a normal end, before it releases its lock."""
        with self._locked() as state:
            (state.get('launchers') or {}).pop(label, None)

    def stop(self, reason):
        """A stop any component records: every later reservation is refused."""
        with self._locked() as state:
            if not state.get('stopped'):
                state['stopped'], state['stop_reason'] = True, reason

    def read(self):
        with open(self.lock_path, 'a+') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            try:
                return json.loads(self.path.read_text())
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)


def llm_estimate(request):
    price_in, price_out = model.PRICES[request['model']]
    cap = request.get('max_completion_tokens', request.get('max_tokens'))
    if isinstance(cap, bool) or not isinstance(cap, int) or cap <= 0:
        raise model.TransportError('request without a positive output cap: refused by the budget')
    tokens_in = 2 * len(json.dumps(request).encode('utf-8')) + 4096
    return (tokens_in * price_in + cap * price_out) / 1e6


def whole(count):
    return isinstance(count, int) and not isinstance(count, bool) and count >= 0


def llm_cost(response, request):
    """The answer's cost by `model.call`'s formula; None (settled at the reservation) unless the counts are whole, nonnegative numbers
    with some input."""
    usage = response.get('usage') if isinstance(response, dict) else None
    if not isinstance(usage, dict):
        return None
    tokens_in, tokens_out = usage.get('prompt_tokens'), usage.get('completion_tokens')
    details = usage.get('prompt_tokens_details') or {}
    cached = (details.get('cached_tokens') or 0) if isinstance(details, dict) else None
    if not (whole(tokens_in) and whole(tokens_out) and whole(cached)) or tokens_in == 0:
        return None
    price_in, price_out = model.PRICES[request['model']]
    cached = min(tokens_in, cached)
    return (tokens_in - cached) / 1e6 * price_in + cached / 1e6 * price_in * model.CACHED_INPUT_SHARE + tokens_out / 1e6 * price_out


def jev_estimate(request):
    price_in, _ = model.PRICES[request['model']]
    tokens_in = 2 * len(json.dumps(request, sort_keys=True, ensure_ascii=False).encode('utf-8')) + 4096
    return jev.ATTEMPTS * tokens_in * price_in / 1e6


class BudgetTransport:
    """Called as production calls a transport: (provider, request) for a language model, (request,) for Jev."""

    def __init__(self, ledger, sleep=time.sleep):
        self.ledger, self.sleep = ledger, sleep

    def __call__(self, *args):
        if len(args) == 1:
            return self._jev(args[0])
        provider, request = args
        for attempt in range(3):
            estimate = llm_estimate(request)
            if not self.ledger.reserve(estimate):
                raise model.TransportError('the shared budget ceiling would be passed: not sent')
            try:
                response = model.openai_transport(provider, request, max_attempts=1)
            except model.TransportError as error:
                self.ledger.settle(estimate, estimate)
                status = getattr(error, 'http_status', None)
                if status in CLIENT_ERRORS or attempt == 2 or (status is not None and status != 429 and status < 500):
                    raise
                self.sleep(5 * (attempt + 1))
                continue
            except Exception:
                self.ledger.settle(estimate, estimate)
                raise
            cost = llm_cost(response, request)
            self.ledger.settle(estimate, estimate if cost is None else cost)
            return response
        raise model.TransportError('no answer after three attempts')

    def _jev(self, request):
        estimate = jev_estimate(request)
        if not self.ledger.reserve(estimate):
            raise model.TransportError('the shared budget ceiling would be passed: not sent')
        try:
            response = jev.transport(request)
        except Exception:
            self.ledger.settle(estimate, estimate, kind='jev')
            raise
        usage = response.get('usage') if isinstance(response, dict) else None
        tokens = usage.get('input_tokens') if isinstance(usage, dict) else None
        if isinstance(tokens, int) and not isinstance(tokens, bool) and tokens > 0:
            # an unanswered attempt inside jev.transport was the same request, so each of the three is billed at most this input;
            # the whole charge is settled, so a charge above the reservation sets the overrun flag
            actual = jev.ATTEMPTS * tokens * model.PRICES[request['model']][0] / 1e6
        else:
            actual = estimate                       # usage missing, invalid, or zero for a nonempty request: the whole reservation
        self.ledger.settle(estimate, actual, kind='jev', tokens=tokens if isinstance(tokens, int) else None)
        return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init-ledger')
    parser.add_argument('--ceiling', type=float)
    parser.add_argument('--ledger')
    parser.add_argument('--from', dest='from_day')
    parser.add_argument('--until', dest='until_day')
    parser.add_argument('--testdb', default=str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'))
    parser.add_argument('--views')
    parser.add_argument('--archive')
    parser.add_argument('--config', default=str(ROOT / 'poc/config/poc-v118.json'))
    parser.add_argument('--universe', default=str(ROOT / 'poc/universe.json'))
    parser.add_argument('--only', default='NVDA')
    parser.add_argument('--cap', type=float, default=None)
    parser.add_argument('--workers', type=int, default=16)
    parser.add_argument('--jev-workers', type=int, default=None)
    args = parser.parse_args()
    if args.init_ledger:
        if Path(args.init_ledger).exists():
            raise SystemExit('ledger exists: refused (a new ledger needs a new path)')
        SharedLedger.init(args.init_ledger, args.ceiling)
        print('ledger written:', args.init_ledger, 'ceiling', args.ceiling)
        return
    for name in ('ledger', 'from_day', 'until_day', 'views', 'archive'):
        if not getattr(args, name):
            raise SystemExit(f'--{name.replace("_day", "")} is required')
    os.makedirs(os.path.dirname(args.views), exist_ok=True)
    log_path = os.path.join(os.path.dirname(args.views), 'replay.log')

    def log(*parts):
        line = ' '.join(str(p) for p in parts)
        print(line, flush=True)
        with open(log_path, 'a', encoding='utf-8') as handle:
            handle.write(line + '\n')

    cfg = config.load(args.config)
    if cfg.baseline is not None:
        raise SystemExit(f'config {cfg.version} uses the retired seeded-question baseline: refused')
    import importlib.util
    spec = importlib.util.spec_from_file_location('scripts_replay', ROOT / 'scripts/replay.py')
    scripts_replay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scripts_replay)
    scripts_replay.refuse_links_engine(cfg)                   # the same refusals scripts/replay.py makes
    scripts_replay.refuse_seeded_ledger(args.views)
    scripts_replay.refuse_harness_ledger(args.views)
    uni = universe.load(args.universe)
    archive = model.Archive(args.archive)
    ledger = SharedLedger(args.ledger)
    install_stop_gate(ledger)                              # Jev's internal retries read the run's stop too (council mo R1)
    transport = BudgetTransport(ledger)
    jev_workers = args.jev_workers if args.jev_workers is not None else (8 if cfg.matching.engine == 'jev' else 1)
    day_runner = parallel_day.ParallelDay(os.path.abspath(args.testdb), os.path.join(os.path.dirname(os.path.abspath(args.views)), 'manifests'),
                                          extraction_workers=args.workers, jev_workers=jev_workers) if args.workers > 1 else None
    log(f'--- budgeted replay {args.from_day}..{args.until_day} config {cfg.version}/{cfg.checksum} provider {cfg.provider} universe {uni.version} '
        f'workers {args.workers}; ledger {args.ledger} {ledger.read()}')
    totals = replay.run(testdb_path=args.testdb, views_path=args.views, archive=archive, cfg=cfg, universe=uni,
                        from_day=args.from_day, until_day=args.until_day, spend_cap_usd=args.cap, log=log,
                        only_objects=set(args.only.split(',')) if args.only else None, transport=transport, day_runner=day_runner)
    log('totals:', totals)
    log('ledger:', ledger.read())


if __name__ == '__main__':
    main()

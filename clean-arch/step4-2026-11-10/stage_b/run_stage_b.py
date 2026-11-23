"""Send Stage B (D429): the three unseeded draws replayed in the adapter's ladder mode, one after another in this one process, under
one spending limit of $2 whose ledger is `<root>/spend.jsonl`. The limit starts from what the ledger already records.

**One stop rule.** The first stop of any kind ends the whole send and every later launch: the cap refusing a request (no other
thread sends after it), a draw that ends incomplete (after its one redo, by a stop code decides, or with no judgement), or a
redo left unfinished by a crash. The stop is written to the ledger before anything else, and a later launch that finds it sends
nothing. The only second chance is one redo of a draw, in a new folder, for a stop a second send can change (a judgement refused
twice, an answer that does not fit the schema, a transport failure after the retry policy). A draw folder with no recorded
outcome is a crash: recorded, never resumed, and counted as that folder's attempt. One launch runs at a time (an exclusive lock
on `<root>/launch.lock`). Every attempt is recorded in `<root>/run.json`.

  python3 clean-arch/step4-2026-11-10/stage_b/run_stage_b.py            # writes under poc/data/clean-stage-b-2026-11-11
  python3 clean-arch/step4-2026-11-10/stage_b/run_stage_b.py --root R --runs c1 --inputs I.json --cap 1.0 --shared-ledger L

With arguments (WIRING-DESIGN.md §A, D448): the draws, the root and the cap; `--inputs` maps each draw to the adapter's inputs
(`ladder_adapter.replay`); `--shared-ledger` is the run's shared ledger, reserved inside each attempt. The stop and redo rules are the
same.
"""
import json
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ladder_adapter  # noqa: E402

CAP_USD = 2.0
RUNS = ('u1', 'u2', 'u3')


def resendable(error):
    """A stop a second send can change, because it comes from the model's answer or the network: the judge's refusal of one
    judgement twice, an answer that does not fit the schema, or a transport failure."""
    from hivemind import model
    from hivemind.views import judging
    return isinstance(error, (judging.JudgementRefused, model.SchemaError, model.TransportError))


class AlreadyRunning(Exception):
    pass


def send(root, transport=None, sleep=None, *, runs=None, cap_usd=None, inputs_of=None, shared=None):
    """Run the send while holding an exclusive lock on `<root>/launch.lock`: a second launch while one runs is refused, so two
    processes never spend against the same balance."""
    import fcntl
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    with open(root / 'launch.lock', 'w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise AlreadyRunning(f'another launch holds {root / "launch.lock"}; this one sends nothing')
        return _send(root, transport, sleep, runs, cap_usd, inputs_of or {}, shared)


class Stopped(Exception):
    pass


def _send(root, transport, sleep, runs=None, cap_usd=None, inputs_of=None, shared=None):
    """One stop rule (`ladder_adapter.LedgerBudget`): the first stop of any kind ends the send and every later launch. A draw is
    replayed once more only for a stop a second send can change; any draw that ends incomplete records the stop."""
    record_path = root / 'run.json'
    record = json.loads(record_path.read_text()) if record_path.exists() else {}
    inputs_of = inputs_of or {}
    runs = RUNS if runs is None else runs                  # read at call time, so the module's constants stay the defaults
    cap_usd = CAP_USD if cap_usd is None else cap_usd
    limit = ladder_adapter.LedgerBudget(cap_usd, root / 'spend.jsonl', attempt=transport, sleep=sleep, shared=shared)
    if limit.stopped is not None:
        raise Stopped(f'the send is stopped ({limit.stopped}); nothing more is sent')

    def save():
        record['spent usd (ledger)'] = round(ladder_adapter.ledger_total(root / 'spend.jsonl'), 4)
        record_path.write_text(json.dumps(record, indent=1) + '\n')

    def end(run, reason):
        record[run]['state'] = 'incomplete'
        record['stopped'] = reason
        limit.stop(reason)
        save()
        return record

    for run in runs:
        entry = record.setdefault(run, {'attempts': []})
        if entry.get('state') == 'complete':
            continue
        for folder_name in (f'draw-{run}', f'draw-{run}-redo'):
            if (root / folder_name).exists():
                if not any(attempt['folder'] == folder_name for attempt in entry['attempts']):
                    # a folder with no recorded outcome: the process that wrote it ended mid-replay (a crash); it is never resumed
                    entry['attempts'].append({'folder': folder_name, 'stopped': 'the process ended without recording an outcome (a crash)'})
                    save()
                if folder_name.endswith('-redo'):
                    return end(run, f'{run} incomplete: its redo did not finish')
                continue
            try:
                runner = ladder_adapter.replay(run, root / folder_name, transport=transport, limit=limit, inputs=inputs_of.get(run),
                                               end_day=(inputs_of.get(run) or {}).get('end_day'))
            except BaseException as error:              # a second send only where it can differ
                attempt = {'folder': folder_name, 'stopped': f'{type(error).__name__}: {error}', 'traceback': traceback.format_exc()[-2000:]}
                if not isinstance(error, (Exception, SystemExit)):
                    entry['attempts'].append(attempt)
                    save()
                    raise
                if isinstance(error, ladder_adapter.budget.OverBudget):
                    reason = limit.stopped or f'the spending cap: {error}'
                elif isinstance(error, ladder_adapter.WriterStopped):
                    reason = f'{run} incomplete: {error.reason}'         # the stop's own reason, at the run level too
                elif folder_name.endswith('-redo') or not resendable(error):
                    reason = f'{run} incomplete: {type(error).__name__}'
                else:
                    reason = None
                if reason is not None:
                    limit.stop(reason)                  # the stop is on disk before the attempt is: a crash between them cannot lead to a redo
                    entry['attempts'].append(attempt)
                    return end(run, reason)
                entry['attempts'].append(attempt)
                save()
                continue
            entry['attempts'].append({'folder': folder_name, 'judgements': runner.counts['judgements'],
                                      'views': runner.counts['views written from a ladder']})
            if runner.counts['judgements'] == 0:      # design §8: a draw with no judgement is incomplete
                return end(run, f'{run} incomplete: no judgement')
            entry['state'] = 'complete'
            save()
            break
    save()
    return record


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=str(ladder_adapter.OUTPUT_ROOT))
    parser.add_argument('--runs', default=','.join(RUNS))
    parser.add_argument('--cap', type=float, default=CAP_USD)
    parser.add_argument('--inputs', default=None, help='a JSON file: {draw: adapter inputs}')
    parser.add_argument('--shared-ledger', default=None)
    arguments = parser.parse_args()
    runs = tuple(arguments.runs.split(','))
    inputs_of = json.loads(Path(arguments.inputs).read_text()) if arguments.inputs else {}
    shared = None
    if arguments.shared_ledger:
        import importlib.util
        spec = importlib.util.spec_from_file_location('budget_replay', HERE.parents[2] / 'clean-arch/e2e-comparison-2026-11-13/budget_replay.py')
        budget_replay = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(budget_replay)
        shared = budget_replay.SharedLedger(arguments.shared_ledger)
        budget_replay.install_stop_gate(shared)            # every actual send reads the run's stop first (council mo R1)
    result = send(arguments.root, runs=runs, cap_usd=arguments.cap, inputs_of=inputs_of, shared=shared)
    print(json.dumps({run: {k: v for k, v in entry.items() if k != 'attempts'} if isinstance(entry, dict) else entry
                      for run, entry in result.items()}, indent=1))
    return result, runs


if __name__ == '__main__':
    result, runs = main()
    if any(result.get(run, {}).get('state') != 'complete' for run in runs) or 'stopped' in result:
        raise SystemExit('STOPPED: a draw is incomplete; Stage B misses line 1 and goes to Alex')

"""Send Stage B (D429): the three unseeded draws replayed in the adapter's ladder mode, one after another in this one process, under
one spending limit of $2 whose ledger is `<root>/spend.jsonl`. The limit starts from what the ledger already records, so a later
process (a redo launched after this one ends) cannot spend past the cap either.

A draw that stops is replayed once more in a new folder (`draw-<run>-redo`) when the stop can differ on a second send (a judgement
refused twice, an answer that does not fit the schema, a transport failure after the retry policy); a stop that code decides the same way every time (a leakage or selection
refusal, the due-day guard, an identity check) is not resent, and the draw is incomplete. The cap stops every draw: nothing more is
sent and the cap is never raised. The outcome of every draw and attempt is written to `<root>/run.json` as it happens. One launch
runs at a time: it holds an exclusive lock on `<root>/launch.lock`, and a second launch while it runs sends nothing.

  python3 clean-arch/step4-2026-11-10/stage_b/run_stage_b.py            # writes under poc/data/clean-stage-b-2026-11-11
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


def send(root, transport=None, sleep=None):
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
        return _send(root, transport, sleep)


def _send(root, transport, sleep):
    record_path = root / 'run.json'
    record = json.loads(record_path.read_text()) if record_path.exists() else {}
    limit = ladder_adapter.LedgerBudget(CAP_USD, root / 'spend.jsonl', attempt=transport, sleep=sleep)
    for run in RUNS:
        if record.get(run, {}).get('state') in ('complete', 'incomplete'):
            continue
        for folder_name in (f'draw-{run}', f'draw-{run}-redo'):
            if (root / folder_name).exists():
                continue
            entry = record.setdefault(run, {'attempts': []})
            try:
                runner = ladder_adapter.replay(run, root / folder_name, transport=transport, limit=limit)
            except ladder_adapter.budget.OverBudget as error:
                entry['attempts'].append({'folder': folder_name, 'stopped': f'the spending cap: {error}'})
                entry['state'] = 'incomplete'
                record['stopped'] = 'the spending cap'
                record_path.write_text(json.dumps(record, indent=1) + '\n')
                return record
            except BaseException as error:              # any other stop: written down; a second send only where it can differ
                entry['attempts'].append({'folder': folder_name, 'stopped': f'{type(error).__name__}: {error}',
                                          'traceback': traceback.format_exc()[-2000:]})
                if not isinstance(error, Exception) and not isinstance(error, SystemExit):
                    record_path.write_text(json.dumps(record, indent=1) + '\n')
                    raise
                if folder_name.endswith('-redo') or not resendable(error):
                    entry['state'] = 'incomplete'
                    record_path.write_text(json.dumps(record, indent=1) + '\n')
                    break
                record_path.write_text(json.dumps(record, indent=1) + '\n')
                continue
            entry['attempts'].append({'folder': folder_name, 'judgements': runner.counts['judgements'],
                                      'views': runner.counts['views written from a ladder']})
            entry['state'] = 'complete'
            record_path.write_text(json.dumps(record, indent=1) + '\n')
            break
        else:
            record.setdefault(run, {'attempts': []})['state'] = 'incomplete'
    record['spent usd (ledger)'] = round(ladder_adapter.ledger_total(root / 'spend.jsonl'), 4)
    record_path.write_text(json.dumps(record, indent=1) + '\n')
    return record


if __name__ == '__main__':
    result = send(ladder_adapter.OUTPUT_ROOT)
    print(json.dumps({run: {k: v for k, v in entry.items() if k != 'attempts'} if isinstance(entry, dict) else entry
                      for run, entry in result.items()}, indent=1))
    if any(isinstance(entry, dict) and entry.get('state') != 'complete' for run, entry in result.items() if run in RUNS) or 'stopped' in result:
        raise SystemExit('STOPPED: a draw is incomplete; Stage B misses line 1 and goes to Alex')

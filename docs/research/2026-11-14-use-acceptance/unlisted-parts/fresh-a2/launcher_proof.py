"""$0 proof of the exact first-step launcher the paid run uses (council round 99): `clean-arch/step1/run_live.py` with
`--shared-ledger`, its LiveTransport and the run's stop gate, on the frozen inputs, with only the network send replaced by a recorded
answer that fits every article (a stored "nothing kept" answer of the 10-06 week, with its usage). No model call.

  python3 launcher_proof.py <new scratch folder>

  L1  25 articles complete; the ledger charges each attempt at its answer's usage, releases every reservation, and never holds more
      than one reservation at a time;
  L2  a network loss on one attempt is sent again; the lost attempt is charged at its reservation; the run completes;
  L3  a ceiling that cannot cover the run stops it: the ledger refuses, records the stop, the launcher exits 1, and the trace reads as
      incomplete (no verdict);
  L4  the largest reservation among the 25 requests with the 13-topic library, and what a $6.50 ceiling leaves for it.
LAUNCHER_MUTANT=no-shared-ledger must fail L1 (nothing reaches the ledger); L5 prints why that launcher would stop the week early.
"""
import copy
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path[:0] = [str(HERE), str(ROOT / 'src'), str(ROOT / 'clean-arch/step1')]
import fresh_a2  # noqa: E402

INPUTS = HERE / 'inputs'
MUTANT = os.environ.get('LAUNCHER_MUTANT', '')
WRAPPER = r'''
import copy, json, sys
sys.path[:0] = [{step1!r}, {src!r}]
import live, run_live
from hivemind import model
answer = json.loads({answer!r})
plan = json.loads({plan!r})
count = [0]
def send(provider, request, timeout=None, max_attempts=1):
    count[0] += 1
    if count[0] in plan['lose']:
        raise model.TransportError('connection reset by peer (recorded loss)')
    return copy.deepcopy(answer)
live.model.openai_transport = send
sys.argv = ['run_live.py'] + plan['arguments']
sys.exit(run_live.main())
'''


class Failed(Exception):
    pass


def expect(condition, message):
    if not condition:
        raise Failed(message)


def recorded_answer():
    connection = sqlite3.connect(f'file:{ROOT}/poc/data/clean-second-week-2026-11-15/week-continued/merged-step1.sqlite?mode=ro&immutable=1', uri=True)
    raw = connection.execute('select raw_response from trace where sequence = 8').fetchone()[0]
    connection.close()
    answer = json.loads(raw)
    expect(json.loads(answer['choices'][0]['message']['content']) == {'new_theses': [], 'evidence': []}, 'the recorded answer is not a "nothing kept" answer')
    return raw, answer


def launch(scratch, name, articles, ceiling, lose=(), shared=True):
    folder = Path(scratch) / name
    folder.mkdir()
    manifest = json.loads((INPUTS / 'manifest-2026-10-13-10-19.json').read_text())
    manifest.update(item_ids=manifest['item_ids'][:articles], item_limit=articles)
    (folder / 'manifest.json').write_text(json.dumps(manifest))
    (folder / 'limits.json').write_text(json.dumps({'max_usd': 40.0, 'max_seconds': 28800, 'max_calls': 1200, 'input_usd_per_million': 0.5,
                                                    'output_usd_per_million': 1.2}))
    sys.path.insert(0, str(ROOT / 'clean-arch/e2e-comparison-2026-11-13'))
    import budget_replay
    budget_replay.SharedLedger.init(folder / 'ledger.json', ceiling)
    arguments = ['--source', str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'), '--output', str(folder / 'trace.sqlite'),
                 '--manifest', str(folder / 'manifest.json'), '--initial', str(INPUTS / 'initial-10-06-library.json'),
                 '--settings', str(INPUTS / 'settings.json'), '--limits', str(folder / 'limits.json')]
    if shared:
        arguments += ['--shared-ledger', str(folder / 'ledger.json')]
    raw, _ = recorded_answer()
    wrapper = WRAPPER.format(step1=str(ROOT / 'clean-arch/step1'), src=str(ROOT / 'src'), answer=raw,
                             plan=json.dumps({'lose': list(lose), 'arguments': arguments}))
    run = subprocess.run([sys.executable, '-c', wrapper], capture_output=True, text=True, timeout=1800,
                         env=dict(os.environ))
    ledger = json.loads((folder / 'ledger.json').read_text())
    lines = [json.loads(line) for line in (folder / 'ledger.attempts.jsonl').read_text().splitlines()] if (folder / 'ledger.attempts.jsonl').exists() else []
    return run, ledger, lines, folder


def main(scratch):
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=False)
    _, answer = recorded_answer()
    usage = answer['usage']
    from hivemind import model
    price_in, price_out = model.PRICES[json.loads((INPUTS / 'settings.json').read_text())['model']]
    per_answer = (usage['prompt_tokens'] * price_in + usage['completion_tokens'] * price_out) / 1_000_000   # live.ledger_cost's rule

    run, ledger, lines, folder = launch(scratch, 'l1', 25, 6.50, shared=MUTANT != 'no-shared-ledger')
    topics, complete, done, total = fresh_a2.opened_topics(folder / 'trace.sqlite')
    expect(run.returncode == 0 and complete and done == total == 25, f'L1: the run did not complete ({run.returncode}, {done} of {total}): {run.stderr[-300:]}')
    expect(ledger['attempts'] == 25 and abs(ledger['reserved']) < 1e-9 and not ledger['stopped'], f'L1: the ledger is not settled: {ledger}')
    expect(all(abs(line['charged'] - per_answer) < 1e-9 for line in lines) and len(lines) == 25, 'L1: an attempt is not charged at its usage')
    reservations = [line['reserved'] for line in lines]
    print(f'L1 ok: 25 of 25 articles complete through run_live.py --shared-ledger; ledger spent ${ledger["spent"]:.4f} = 25 x ${per_answer:.5f} '
          f'at usage, reserved back to $0 at the end; reservations ${min(reservations):.4f} to ${max(reservations):.4f}')

    run, ledger, lines, folder = launch(scratch, 'l2', 5, 6.50, lose=(3,))
    _, complete, done, total = fresh_a2.opened_topics(folder / 'trace.sqlite')
    lost = [line for line in lines if abs(line['charged'] - line['reserved']) < 1e-9]
    expect(run.returncode == 0 and complete and done == 5 and ledger['attempts'] == 6 and len(lost) == 1, f'L2: the loss was not resent and charged at its reservation: {ledger}, {run.stderr[-300:]}')
    print(f'L2 ok: one network loss (attempt 3) sent again; 6 attempts for 5 articles; the lost attempt charged at its reservation ${lost[0]["charged"]:.4f}; run complete')

    ceiling = 0.17                                          # covers a reservation plus a few answers, not 25 articles
    run, ledger, lines, folder = launch(scratch, 'l3', 25, ceiling)
    _, complete, done, total = fresh_a2.opened_topics(folder / 'trace.sqlite')
    expect(run.returncode != 0 and ledger['stopped'] and not complete and 0 < done < total, f'L3: the run was not stopped midway and reported incomplete: {ledger}, {done}')
    print(f'L3 ok: a ${ceiling:.4f} ceiling stops the run: ledger stopped ({ledger["stop_reason"]}), launcher exit {run.returncode}, '
          f'{done} of {total} articles complete, read as incomplete (no verdict)')

    print(f'L4: the largest reservation among the 25 with the 13-topic library is ${max(reservations):.4f}; a $6.50 ceiling holds the week\'s '
          f'expected $3.60 to $6.06 charges plus one reservation only up to ${6.50 - max(reservations):.2f} charged')
    mean = sum(reservations) / len(reservations)
    print(f'L5: without --shared-ledger the transport adds each full reservation to a running total and checks it against max_usd: '
          f'at the mean ${mean:.4f}, a $6.50 limit refuses after about {int(6.50 // mean)} attempts, not the week\'s ~450')
    print('ALL OK')


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except Failed as failure:
        print('FAILED:', failure)
        sys.exit(1)

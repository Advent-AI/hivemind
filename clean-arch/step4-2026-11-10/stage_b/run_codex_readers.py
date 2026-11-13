"""Run the Codex family's sessions of the Stage B baseline reading: one fresh read-only session a packet, six at a time.

A session that has not returned after 60 minutes is stopped and run once more; every session started is logged with its
time and whether it returned (`sessions-codex-<kind>.json`). No model call of the pipeline is made; the reader is the Codex
CLI with the operator's usual model and setting.

  python3 clean-arch/step4-2026-11-10/stage_b/run_codex_readers.py first <data folder>     # the 40 packets
  python3 clean-arch/step4-2026-11-10/stage_b/run_codex_readers.py third <data folder>     # the third reader's packets
"""
import concurrent.futures
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
LADDER = REPO / 'clean-arch' / 'step4-2026-11-10' / 'ladder'
MOST_SECONDS, MOST_ATTEMPTS, AT_ONCE = 3600, 2, 6
KINDS = {'first': {'packets': 'readers', 'answers': 'readers-answers', 'packet_name': 'packet-{n}.json', 'answer_name': 'reader-codex-packet-{n}.jsonl',
                   'brief': LADDER / 'stage-b-reader-brief.md', 'unit': 'judgements, each of a different research question'},
         'third': {'packets': 'third-reader', 'answers': 'third-reader', 'packet_name': 'ruling-packet-{n}.json', 'answer_name': 'rulings-codex-{n}.jsonl',
                   'brief': LADDER / 'stage-b-third-reader-brief.md', 'unit': 'judgements to rule on'}}


def handoff(kind, packet_file, count):
    settings = KINDS[kind]
    return (f"You are an independent reader. Read `{settings['brief']}` and follow it exactly"
            + (f"; it sends you to the form `{LADDER / 'stage-b-reader-brief.md'}`, which you read first" if kind == 'third' else '') + ". It is your whole task.\n\n"
            f"The packet it speaks of is `{packet_file}` ({count} {settings['unit']}).\n\n"
            "Rules: the only files you may open are " + ('those two briefs' if kind == 'third' else 'that brief') + " and that packet. Do not open or list any other file or folder, in the "
            "repository or anywhere else. Do not run model calls or start runs. Read each judgement's whole request before judging its answer.\n\n"
            f"Output: exactly {count} lines, one JSON object per line, in packet order, each with the `judgement` number the packet gives and the fields the brief lists, "
            "and nothing else (no prose, no code fence).\n")


def read_packet(kind, folder, number):
    settings = KINDS[kind]
    packet_file = folder / settings['packets'] / settings['packet_name'].format(n=number)
    count = len(json.loads(packet_file.read_text()))
    answer_file = folder / settings['answers'] / settings['answer_name'].format(n=number)
    attempts = []
    for attempt in range(1, MOST_ATTEMPTS + 1):
        started = time.monotonic()
        stream = answer_file.with_suffix(f'.attempt-{attempt}.stream')
        try:
            with stream.open('w') as out:
                run = subprocess.run(['codex', 'exec', '-s', 'read-only', '-C', str(REPO), '--skip-git-repo-check', '--ephemeral', '--json', '-o', str(answer_file), '-'],
                                     input=handoff(kind, packet_file, count), text=True, stdout=out, stderr=subprocess.STDOUT, timeout=MOST_SECONDS)
            rows = sum(1 for line in answer_file.read_text().splitlines() if line.strip().startswith('{')) if answer_file.exists() else 0
            returned = run.returncode == 0 and rows == count
        except subprocess.TimeoutExpired:
            returned = False
        attempts.append({'seconds': round(time.monotonic() - started, 1), 'outcome': 'returned' if returned else 'stopped'})
        if returned:
            break
        if answer_file.exists():
            answer_file.rename(answer_file.with_suffix(f'.attempt-{attempt}.not-used'))
    return number, attempts


def main():
    kind, folder = sys.argv[1], Path(sys.argv[2]).resolve()
    settings = KINDS[kind]
    numbers = sorted(int(path.stem.split('-')[-1]) for path in (folder / settings['packets']).glob(settings['packet_name'].format(n='*')))
    (folder / settings['answers']).mkdir(exist_ok=True)
    log_file = folder / f'sessions-codex-{kind}.json'
    if log_file.exists():
        raise SystemExit(f'{log_file.name} exists: this reading was already run')
    log = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=AT_ONCE) as pool:
        for number, attempts in pool.map(lambda number: read_packet(kind, folder, number), numbers):
            log[str(number)] = attempts
            log_file.write_text(json.dumps(log, indent=1) + '\n')
            print(f'packet {number}: {attempts}', flush=True)
    unread = [number for number, attempts in log.items() if attempts[-1]['outcome'] != 'returned']
    print(f'{len(numbers)} packets; {len(numbers) - len(unread)} read; not read: {unread}; session time in all {sum(a["seconds"] for attempts in log.values() for a in attempts) / 60:.0f} minutes')


if __name__ == '__main__':
    main()

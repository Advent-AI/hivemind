"""The probe's readers (DESIGN.md, "Reading"): the handoff each reader gets, and the Codex family's read-only sessions, one fresh
session a packet, six at a time; a session not back within 60 minutes is stopped and run once more; every session is logged. The
Claude family's sessions get the same handoff (`handoff` prints it). No model call of the pipeline is made.

  python3 run_readers.py codex <first|third|h> <reading folder>
  python3 run_readers.py handoff <first|third|h> <reading folder> <packet number>
"""
import concurrent.futures
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
LADDER = REPO / 'clean-arch/step4-2026-11-10/ladder'
MOST_SECONDS, MOST_ATTEMPTS, AT_ONCE = 3600, 2, 6
THEMES = (REPO / 'poc/data/clean-carried-run-2026-11-16/stage-a-reread/handoffs/reader-packet-1.md').read_text().splitlines()[2]
KINDS = {
    'first': {'briefs': [LADDER / 'stage-a-reader-brief.md', HERE / 'h-brief.md'], 'packets': 'readers', 'packet': 'packet-{n}.json',
              'answers': 'readers-answers', 'answer': 'reader-{family}-packet-{n}.jsonl', 'unit': 'items',
              'order': 'in item order, each with the `item` number the packet gives and the fields the two briefs list (H included)'},
    'third': {'briefs': [LADDER / 'stage-a-third-reader-brief.md', LADDER / 'stage-a-reader-brief.md'], 'packets': 'third-reader',
              'packet': 'ruling-packet-{n}.json', 'answers': 'third-reader', 'answer': 'rulings-{family}-{n}.jsonl', 'unit': 'items to rule on',
              'order': 'in the order the packet gives the points'},
    'h': {'briefs': [HERE / 'h-third-reader-brief.md', HERE / 'h-brief.md'], 'packets': 'third-reader', 'packet': 'h-packet-{n}.json',
          'answers': 'third-reader', 'answer': 'h-rulings-{family}-{n}.jsonl', 'unit': 'points to rule on',
          'order': 'in the order the packet gives the points, each with the point\'s `id`'},
    'class': {'briefs': [HERE / 'a3-class-brief.md'], 'packets': 'a3', 'packet': 'class-packet-{n}.json', 'answers': 'a3',
              'answer': 'class-{family}-{n}.jsonl', 'unit': 'entries', 'order': "in packet order, each with the entry's `id`"},
    'named': {'briefs': [HERE / 'a3-named-way-brief.md', HERE / 'h-brief.md'], 'packets': 'a3', 'packet': 'named-packet-{n}.json',
              'answers': 'a3', 'answer': 'named-{family}-{n}.jsonl', 'unit': 'points to rule on',
              'order': "in packet order, each with the point's `id`"},
}


def count_of(kind, packet_file):
    packet = json.loads(packet_file.read_text())
    if kind == 'third':
        return sum(len(item['to_rule']) for item in packet)
    return len(packet)


def handoff(kind, packet_file, count):
    settings = KINDS[kind]
    briefs = ' and '.join(f'`{brief}`' for brief in settings['briefs'])
    return (f"You are an independent reader. Read {briefs} and follow them exactly. They are your whole task.\n"
            f"The packet is `{packet_file}` ({count} {settings['unit']}). The company in every item is NVIDIA (ticker NVDA); each\n"
            f"{THEMES}\n\n"
            "You are read-only: do not edit files, run model calls or start runs. The only files you may open are those two briefs and that\n"
            "packet. Do not open or list any other file or folder, in the repository or anywhere else, and nothing under `/private/tmp`.\n\n"
            f"You cannot write files: return your answer as your final message, exactly {count} lines, one JSON object per line, "
            f"{settings['order']}, and nothing else: no prose before or after, no code fence.\n")


def packets_of(kind, folder):
    settings = KINDS[kind]
    return sorted(int(path.stem.split('-')[-1]) for path in (folder / settings['packets']).glob(settings['packet'].format(n='*')))


def read_packet(kind, folder, number):
    settings = KINDS[kind]
    packet_file = folder / settings['packets'] / settings['packet'].format(n=number)
    count = count_of(kind, packet_file)
    answer_file = folder / settings['answers'] / settings['answer'].format(family='codex', n=number)
    attempts = []
    for attempt in range(1, MOST_ATTEMPTS + 1):
        started = time.monotonic()
        stream = folder / 'handoffs' / f'{kind}-codex-packet-{number}.attempt-{attempt}.stream'
        try:
            with stream.open('w') as out:
                run = subprocess.run(['codex', 'exec', '-s', 'read-only', '-C', str(REPO), '--skip-git-repo-check', '--ephemeral', '--json',
                                      '-o', str(answer_file), '-'], input=handoff(kind, packet_file, count), text=True, stdout=out,
                                     stderr=subprocess.STDOUT, timeout=MOST_SECONDS)
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


def run_codex(kind, folder):
    folder = Path(folder).resolve()
    (folder / KINDS[kind]['answers']).mkdir(exist_ok=True)
    (folder / 'handoffs').mkdir(exist_ok=True)
    log_file = folder / f'sessions-codex-{kind}.json'
    if log_file.exists():
        raise SystemExit(f'{log_file.name} exists: this reading was already run')
    numbers = packets_of(kind, folder)
    for number in numbers:
        packet_file = folder / KINDS[kind]['packets'] / KINDS[kind]['packet'].format(n=number)
        (folder / 'handoffs' / f'{kind}-packet-{number}.md').write_text(handoff(kind, packet_file, count_of(kind, packet_file)))
    log = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=AT_ONCE) as pool:
        for number, attempts in pool.map(lambda number: read_packet(kind, folder, number), numbers):
            log[str(number)] = attempts
            log_file.write_text(json.dumps(log, indent=1) + '\n')
            print(f'packet {number}: {attempts}', flush=True)
    unread = [number for number, attempts in log.items() if attempts[-1]['outcome'] != 'returned']
    print(f'{len(numbers)} packets; {len(numbers) - len(unread)} read; not read: {unread}')


if __name__ == '__main__':
    command, kind, folder = sys.argv[1], sys.argv[2], Path(sys.argv[3]).resolve()
    if command == 'codex':
        run_codex(kind, folder)
    else:
        number = int(sys.argv[4])
        packet_file = folder / KINDS[kind]['packets'] / KINDS[kind]['packet'].format(n=number)
        print(handoff(kind, packet_file, count_of(kind, packet_file)), end='')

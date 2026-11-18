"""The split probe's readers (DESIGN.md v4 §3 item 3): the earlier probe's reader runner (unlisted-parts/run_readers.py) with this
reading's briefs. First readers read `stage-a-reader-brief.md` and `split-brief.md`; third readers of the form's marks read Stage A's
third-reader brief; third readers of `BY` and `LQ` read `split-third-reader-brief.md`. The Codex family runs here, one fresh read-only
session a packet; the Claude family gets the same handoff (`handoff`).

  python3 run_split_readers.py codex <first|third|split> <reading folder>
  python3 run_split_readers.py handoff <first|third|split> <reading folder> <packet number>
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'unlisted-parts'))
import run_readers  # noqa: E402

LADDER = run_readers.LADDER
run_readers.KINDS = {
    'first': {'briefs': [LADDER / 'stage-a-reader-brief.md', HERE / 'split-brief.md'], 'packets': 'readers', 'packet': 'packet-{n}.json',
              'answers': 'readers-answers', 'answer': 'reader-{family}-packet-{n}.jsonl', 'unit': 'items',
              'order': 'in item order, each with the `item` number the packet gives and the fields the two briefs list (BY and LQ included)'},
    'third': run_readers.KINDS['third'],
    'split': {'briefs': [HERE / 'split-third-reader-brief.md', HERE / 'split-brief.md'], 'packets': 'third-reader',
              'packet': 'split-packet-{n}.json', 'answers': 'third-reader', 'answer': 'split-rulings-{family}-{n}.jsonl',
              'unit': 'points to rule on', 'order': "in the order the packet gives the points, each with the point's `id`"},
}

if __name__ == '__main__':
    command, kind, folder = sys.argv[1], sys.argv[2], Path(sys.argv[3]).resolve()
    if command == 'codex':
        run_readers.run_codex(kind, folder)
    else:
        number = int(sys.argv[4])
        packet_file = folder / run_readers.KINDS[kind]['packets'] / run_readers.KINDS[kind]['packet'].format(n=number)
        print(run_readers.handoff(kind, packet_file, run_readers.count_of(kind, packet_file)), end='')

"""The reference control's first readers (DESIGN.md): the earlier probe's reader runner with Stage A's reader brief alone (the full
gate form). The Codex family runs here; the Claude family gets the same handoff (`handoff`).

  python3 run_ref_readers.py codex first <reading folder>
  python3 run_ref_readers.py handoff first <reading folder> <packet number>
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'unlisted-parts'))
import run_readers  # noqa: E402

run_readers.KINDS = {'first': {'briefs': [run_readers.LADDER / 'stage-a-reader-brief.md'], 'packets': 'readers', 'packet': 'packet-{n}.json',
                               'answers': 'readers-answers', 'answer': 'reader-{family}-packet-{n}.jsonl', 'unit': 'items',
                               'order': 'in item order, each with the `item` number the packet gives and the fields the brief lists'}}
run_readers.handoff_original = run_readers.handoff


def handoff(kind, packet_file, count):
    return run_readers.handoff_original(kind, packet_file, count).replace('Read `', 'Read `', 1).replace(' and follow them exactly. They are', ' and follow it exactly. It is', 1).replace('those two briefs and that\npacket', 'that brief and that\npacket', 1)


run_readers.handoff = handoff

if __name__ == '__main__':
    command, kind, folder = sys.argv[1], sys.argv[2], Path(sys.argv[3]).resolve()
    if command == 'codex':
        run_readers.run_codex(kind, folder)
    else:
        number = int(sys.argv[4])
        packet_file = folder / run_readers.KINDS[kind]['packets'] / run_readers.KINDS[kind]['packet'].format(n=number)
        print(run_readers.handoff(kind, packet_file, run_readers.count_of(kind, packet_file)), end='')

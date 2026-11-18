"""Gate 1 of the fortnight, per topic: which marks fail in which attempt, as the accounting settles them under each counting
($0; for the council's choice of the next class). It uses the collector's and the accounting's own functions and judges nothing.

  python3 faults_by_topic.py <stage-a folder> <key path>
"""
import collections
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'clean-arch/step4-2026-11-10/stage_a'))
import accounting  # noqa: E402
import collect_readings as collector  # noqa: E402


def main(run_folder, key_path):
    _, item_of, outcomes, readers, _ = collector.read_rows(run_folder, key_path)
    families = collector.third_reader_families(run_folder)
    of_family = {f: collector.read_rulings(run_folder, item_of, outcomes, readers, f)[0] for f in families}
    for label, unresolved_as in (('unresolved counted for the answer', 'holds'), ('unresolved counted against it', 'fails')):
        print(f'===== {label} =====')
        by_topic = collections.defaultdict(dict)
        fault_counts = collections.Counter()
        for send, outcome in sorted(outcomes.items()):
            kind = accounting.kind_of(outcome)
            if kind == 'refused twice':
                by_topic[send[0]][send[1]] = ['refused twice']
                continue
            rows = (readers['reader 1'].get(send), readers['reader 2'].get(send))
            ruling, _ = accounting.rulings_of_two(of_family[families[0]].get(send, {'marks': {}, 'W': {}}),
                                                  of_family[families[1]].get(send, {'marks': {}, 'W': {}}), unresolved_as) \
                if send in of_family[families[0]] else ({'marks': {}, 'W': {}}, [])
            failed = []
            for mark in accounting.marks_that_apply(kind):
                value = rows[0][mark] if rows[0][mark] == rows[1][mark] else ruling['marks'].get(mark)
                if value == 'fails':
                    failed.append(mark)
            for number, row in enumerate(rows, start=1):
                if row['W'].strip() and ruling['W'].get(f'reader {number}'):
                    failed.append('W')
                    break
            by_topic[send[0]][send[1]] = failed if failed else ['ok']
            fault_counts.update(set(failed))
        right = 0
        for topic, passes in sorted(by_topic.items(), key=lambda kv: int(kv[0].split('-')[-1])):
            good = sum(v == ['ok'] for v in passes.values())
            right += good >= 2
            print(f"  {topic:<14} {'RIGHT' if good >= 2 else 'wrong'}  " + ' | '.join(f"p{p}: {','.join(v)}" for p, v in sorted(passes.items())))
        print(f'  right {right} of {len(by_topic)}; sends failing each mark: {dict(fault_counts)}')
        only = collections.Counter()
        for topic, passes in by_topic.items():
            if sum(v == ['ok'] for v in passes.values()) >= 2:
                continue
            for mark in ('XR', 'L', 'Q', 'R', 'W', 'D', 'X', 'O'):
                fixed = sum(v == ['ok'] or set(v) == {mark} for v in passes.values())
                if fixed >= 2:
                    only[mark] += 1
        print(f'  wrong topics that one mark alone keeps wrong (fixing that mark alone would make them right): {dict(only)}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

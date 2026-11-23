"""Spend and time by component for a run under one shared ledger (council mo, the slice's measurement): each attempt line the ledger
wrote (`<ledger>.attempts.jsonl`: process id, reserved, charged or refused) is mapped to its draw and component through the draws'
records (`<root>/<label>/run.json`, each attempt's pid and start and end times). A line whose process no record names is reported as
unattributed, never dropped; each component is split by call kind (llm, jev, embeddings) with the tokens reported. A line can be lost
(it is written after the ledger, best-effort), never added, so the ledger's spent minus the lines is reported as unaccounted. Charges are
the ledger's (conservative: Jev and embeddings at three times their reported tokens), not a bill.

  python3 spend_by_component.py <root> <ledger.json>
"""
import collections
import json
import sys
from pathlib import Path


def tally(root, ledger_path):
    root, ledger_path = Path(root), Path(ledger_path)
    owner = {}
    times = {}
    for record_path in sorted(root.glob('*/run.json')):
        label = record_path.parent.name
        for component, entry in json.loads(record_path.read_text())['components'].items():
            for attempt in entry['attempts']:
                key = f"{label}/{component}/{attempt['folder']}"
                times[key] = (attempt.get('started at'), attempt.get('ended at'), attempt['state'])
                if attempt.get('pid'):
                    owner[attempt['pid']] = key
    lines = [json.loads(line) for line in ledger_path.with_suffix('.attempts.jsonl').read_text().splitlines()]
    totals = collections.defaultdict(lambda: {'attempts': 0, 'charged': 0.0, 'reserved': 0.0, 'refused': 0, 'by kind': {}})
    for line in lines:
        key = owner.get(line['pid'], f"unattributed (pid {line['pid']})")
        row = totals[key]
        if 'refused' in line:
            row['refused'] += 1
        else:
            row['attempts'] += 1
            row['charged'] += line['charged']
            row['reserved'] += line['reserved']
            kind = row['by kind'].setdefault(line.get('kind', 'llm'), {'attempts': 0, 'charged': 0.0, 'tokens reported': 0})
            kind['attempts'] += 1
            kind['charged'] += line['charged']
            kind['tokens reported'] += line.get('tokens') or 0
    ledger = json.loads(ledger_path.read_text())
    return {'by component': {key: dict(totals.get(key, {'attempts': 0, 'charged': 0.0, 'reserved': 0.0, 'refused': 0, 'by kind': {}}),
                                       **dict(zip(('started at', 'ended at', 'state'), times.get(key, (None, None, None)))))
                             for key in sorted(set(totals) | set(times))},
            'ledger spent': ledger['spent'], 'sum of lines': sum(row['charged'] for row in totals.values()),
            'unaccounted (ledger spent minus the lines; a line lost to a crash or a failed append)':
                ledger['spent'] - sum(row['charged'] for row in totals.values()),
            'unattributed lines': sum(1 for line in lines if line['pid'] not in owner)}


if __name__ == '__main__':
    print(json.dumps(tally(sys.argv[1], sys.argv[2]), indent=1))

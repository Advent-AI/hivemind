"""Reader packets for the Step 2 reference (no model calls). Readers never see a pair's discovery route or any system output.

Usage:
  build_reader_packets.py triage <folder>     candidate pairs → summary-only triage packets of 100 pairs
  build_reader_packets.py scan <folder>       exhaustive sample → scan packets: each incoming item in full, every earlier summary
  build_reader_packets.py label <folder>      triage-possible pairs + scan-flagged pairs + an audit of unflagged pairs → full-context packets
"""
import json, random, sys
from pathlib import Path


def short(it):
    return {'summary': it['summary'], 'original_party': it['original_party'], 'statement_date': it['statement_date'] or it['statement_date_text'],
            'period': it['evidence_period'], 'publication_date': it['publication_date']}


def full(it):
    return {**short(it), 'tier': it['tier'], 'reporting_speaker': it['reporting_speaker'], 'publisher': it['publisher'], 'title': it['title'],
            'passages': it['passages'], 'source_context': [c for c in it['context'] if c], 'theses': [t['question'] for t in it['theses']]}


def main():
    mode, folder = sys.argv[1], Path(sys.argv[2])
    items = {it['key']: it for it in json.loads((folder / 'items.json').read_text())}
    order = list(items)
    chooser = random.Random(7)
    if mode == 'triage':
        pairs = json.loads((folder / 'candidate-pairs.json').read_text())
        chooser.shuffle(pairs)
        key = {}
        for start in range(0, len(pairs), 100):
            packet = []
            for p in pairs[start:start + 100]:
                pid = f"T{len(key) + 1}"
                key[pid] = [p['earlier'], p['later']]
                packet.append({'id': pid, 'earlier': short(items[p['earlier']]), 'later': short(items[p['later']])})
            (folder / f'triage-packet-{start // 100 + 1}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
        (folder / 'triage-key.json').write_text(json.dumps(key))
        print('triage packets', (len(pairs) + 99) // 100, 'pairs', len(pairs))
    elif mode == 'scan':
        sample = json.loads((folder / 'exhaustive-sample.json').read_text())
        for part in range(0, len(sample), 5):
            packet = []
            for s in sample[part:part + 5]:
                incoming = items[s['key']]
                earlier = [k for k in order if items[k]['article'] < incoming['article']]
                packet.append({'incoming_key': s['key'], 'incoming': full(incoming),
                               'earlier_items': [{'key': k, 'summary': items[k]['summary'], 'original_party': items[k]['original_party']} for k in earlier]})
            (folder / f'scan-packet-{part // 5 + 1}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
        print('scan packets', (len(sample) + 4) // 5, 'items', len(sample))
    elif mode == 'label':
        triage_key = json.loads((folder / 'triage-key.json').read_text())
        possible = set()
        for path in sorted(folder.glob('triage-answer-*.json')):
            for row in json.loads(path.read_text()):
                if row['verdict'] != 'different':
                    possible.add(tuple(triage_key[row['id']]))
        flagged, unflagged = set(), []
        sample_keys = [s['key'] for s in json.loads((folder / 'exhaustive-sample.json').read_text())]
        for path in sorted(folder.glob('scan-answer-*.json')):
            for row in json.loads(path.read_text()):
                for k in row['possible_earlier']:
                    if k in items and items[k]['article'] < items[row['incoming_key']]['article']:
                        flagged.add((k, row['incoming_key']))
        for incoming in sample_keys:
            for k in order:
                if items[k]['article'] < items[incoming]['article'] and (k, incoming) not in flagged:
                    unflagged.append((k, incoming))
        audit = chooser.sample(unflagged, min(60, len(unflagged)))
        pairs = sorted(possible | flagged | set(audit))
        chooser.shuffle(pairs)
        key = {}
        for start in range(0, len(pairs), 40):
            packet = []
            for earlier, later in pairs[start:start + 40]:
                pid = f"L{len(key) + 1}"
                key[pid] = {'earlier': earlier, 'later': later, 'from_triage': (earlier, later) in possible,
                            'from_scan': (earlier, later) in flagged, 'audit': (earlier, later) in set(audit)}
                packet.append({'id': pid, 'earlier': full(items[earlier]), 'later': full(items[later])})
            (folder / f'label-packet-{start // 40 + 1}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
        (folder / 'label-key.json').write_text(json.dumps(key))
        print('label packets', (len(pairs) + 39) // 40, 'pairs', len(pairs), f'(triage-possible {len(possible)}, scan-flagged {len(flagged)}, unflagged audit {len(audit)})')


if __name__ == '__main__':
    main()

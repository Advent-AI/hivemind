"""Blind library packet: each named run's final thesis library with evidence counts, shuffled to letters X, Y, Z ...

Usage: build_library_packet.py <output.json> <key path> <label>=<trace.sqlite>[+<segment>] ..."""
import collections, json, random, sqlite3, sys
from pathlib import Path

def library(traces):
    links, final = collections.Counter(), None
    for trace in traces.split('+'):
        conn = sqlite3.connect(f'file:{trace}?mode=ro', uri=True)
        for result, after in conn.execute("select result, after_state from trace where status='complete' order by sequence"):
            r = json.loads(result); ids = r.get('new_thesis_ids', {})
            for ev in r['evidence']:
                for link in ev['links']:
                    links[ids.get(link['target_id'], link['target_id'])] += 1
            final = json.loads(after)
    return [{'id': t['id'], 'question': t['description'], 'outcome': t['outcome'], 'evidence_items': links[t['id']]} for t in final]

def main():
    out, key_path, specs = Path(sys.argv[1]), Path(sys.argv[2]), [s.split('=', 1) for s in sys.argv[3:]]
    random.Random(17).shuffle(specs)
    packet, key = {}, {}
    for letter, (label, traces) in zip('XYZW', specs):
        packet[letter] = library(traces); key[letter] = label
    out.write_text(json.dumps(packet, ensure_ascii=False, indent=1)); Path(key_path).write_text(json.dumps(key))
    print({letter: len(v) for letter, v in packet.items()})

if __name__ == '__main__':
    main()

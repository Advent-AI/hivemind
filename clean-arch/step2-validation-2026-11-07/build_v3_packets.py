"""Reader packets for the forward simulation (no model calls).

  pairs: never-labelled pairs Jev called same_statement (v3-pairs.json) → packets in the reference v2 format (two-question prompt).
  loss:  every item the forward simulation merged away → the incoming record, every receiving record (the text the library keeps) and the
         dossier (summaries of the final library's other records on the incoming item's theses).

Usage: build_v3_packets.py <folder>"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_reader_packets import full  # noqa: E402


def main():
    folder = Path(sys.argv[1])
    items = {it['key']: it for it in json.loads((folder / 'items.json').read_text())}
    pairs = json.loads((folder / 'v3-pairs.json').read_text())
    key = {}
    for start in range(0, len(pairs), 24):
        packet = []
        for earlier, later in pairs[start:start + 24]:
            vid = f'W{len(key) + 1}'
            key[vid] = {'earlier': earlier, 'later': later}
            packet.append({'id': vid, 'earlier': full(items[earlier]), 'later': full(items[later])})
        (folder / f'v3-packet-{start // 24 + 1}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
    (folder / 'v3-key.json').write_text(json.dumps(key, indent=1))
    sim = json.loads((folder / 'forward-sim.json').read_text())
    library = sim['library']
    merged = [d for d in sim['decisions'] if d['outcome'] == 'merged']
    loss_key = {}
    for start in range(0, len(merged), 10):
        packet = []
        for d in merged[start:start + 10]:
            mid = f'M{len(loss_key) + 1}'
            loss_key[mid] = {'key': d['key'], 'merged_into': d['merged_into']}
            theses = {t['id'] for t in items[d['key']]['theses']}
            dossier = [{'summary': items[k]['summary'], 'original_party': items[k]['original_party'], 'publication_date': items[k]['publication_date']}
                       for k, rec in library.items() if k not in d['merged_into'] and theses & set(rec['theses'])]
            packet.append({'id': mid, 'incoming': full(items[d['key']]), 'receiving': [full(items[k]) for k in d['merged_into']], 'dossier': dossier})
        (folder / f'loss-packet-{start // 10 + 1}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
    (folder / 'loss-key.json').write_text(json.dumps(loss_key, indent=1))
    print(f'pair packets {(len(pairs) + 23) // 24} ({len(pairs)} pairs); loss packets {(len(merged) + 9) // 10} ({len(merged)} merged items)')


if __name__ == '__main__':
    main()

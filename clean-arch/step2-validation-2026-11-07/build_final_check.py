"""Close-out check packets for the Step 2 forward run (no model calls).

  merges   every repeat in decisions.json as a pair (the chosen group's original record, the incoming record) with full fields and
           article context, for blind readers, previously labelled pairs included;
  views    the three reader views of each predeclared dossier rebuilt from the run's library.json (none / source / group), masked,
           with prompts for the frozen reader test (reader-test/questions.json, unchanged).

Usage: build_final_check.py <validation folder> <forward run folder>"""
import importlib.util, json, random, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('clean_step3_library', ROOT / 'clean-arch/step3/library.py')
library = importlib.util.module_from_spec(spec)
spec.loader.exec_module(library)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_reader_packets import full  # noqa: E402
from build_views import DOSSIERS, as_record  # noqa: E402


def main():
    folder, run = Path(sys.argv[1]), Path(sys.argv[2])
    items = {it['key']: it for it in json.loads((folder / 'items.json').read_text())}
    decisions = json.loads((run / 'decisions.json').read_text())
    saved = json.loads((run / 'library.json').read_text())
    pairs = [(d['outcome']['repeat_of'][0], d['id']) for d in decisions if d['outcome']['kind'] == 'repeat']
    key = {}
    for start in range(0, len(pairs), 26):
        packet = []
        for original, incoming in pairs[start:start + 26]:
            mid = f'X{len(key) + 1}'
            key[mid] = {'earlier': original, 'later': incoming}
            packet.append({'id': mid, 'earlier': full(items[original]), 'later': full(items[incoming])})
        (run / f'merge-packet-{start // 26 + 1}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
    (run / 'merge-key.json').write_text(json.dumps(key, indent=1))
    store = library.Library()
    store.groups, store.order, store.placement = saved['groups'], saved['order'], saved['placement']
    theses = {t['id']: t['question'] for it in items.values() for t in it['theses']}
    views_dir = run / 'views'
    views_dir.mkdir(exist_ok=True)
    codes = random.Random(20261108 + 1).sample(range(100, 1000), 9)
    vkey = {}
    for (name, thesis_ids), triplet in zip(DOSSIERS.items(), [codes[0:3], codes[3:6], codes[6:9]]):
        header = 'Research questions in this dossier:\n' + '\n'.join(f'- {theses[t]}' for t in thesis_ids) + '\n\nEvidence entries:\n'
        groups = [g for g in store.order if any(t in store.groups[g]['links'] for t in thesis_ids)]
        labels = {g: f'E{n}' for n, g in enumerate(groups, 1)}
        none = [k for k in items if any(t in {x['id'] for x in items[k]['theses']} for t in thesis_ids)]
        rendered = {'none': [library.record_text(as_record(items[k]), f'E{n}') for n, k in enumerate(none, 1)],
                    'source': [library.group_text(store, g, labels[g], labels, member_text=False) for g in groups],
                    'group': [library.group_text(store, g, labels[g], labels, member_text=True) for g in groups]}
        for (view, entries), code in zip(rendered.items(), triplet):
            text = header + '\n\n'.join(entries) + '\n'
            (views_dir / f'{code}.txt').write_text(text)
            vkey[str(code)] = {'dossier': name, 'view': view, 'entries': len(entries), 'characters': len(text)}
    (run / 'views-key.json').write_text(json.dumps(vkey, indent=1))
    placed = set(store.placement)
    missing = [d['id'] for d in decisions if d['id'] not in placed]
    print(f'merge pairs {len(pairs)} in {(len(pairs) + 25) // 26} packets; views {len(vkey)}; records not placed {len(missing)}')
    for code, v in vkey.items():
        print(f"  {v['dossier']}/{v['view']}: entries {v['entries']}, characters {v['characters']}")


if __name__ == '__main__':
    main()

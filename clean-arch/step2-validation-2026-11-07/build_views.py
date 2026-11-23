"""Three reader views of each predeclared dossier, rebuilt from the forward simulation's stored decisions through the isolated Step 3
library (no model calls). This is a fixed-decision reconstruction, not a new forward run.

Test convention for several repeat targets (not a product rule; council/group/b-codex.md): such an item is kept once as its own entry,
with a visible note naming every group it was judged to repeat, identically in the source-only and grouped views.

Views (labels masked in the files):
  none     every stored item as its own entry, as if nothing were merged (the full-information control);
  source   one entry per group: the original record plus a source line per later report;
  group    one entry per group: the original record plus each later report's own text.

Usage: build_views.py <folder>   writes views/<code>.txt, views-key.json, views-replay.json"""
import importlib.util, json, random, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('clean_step3_library', ROOT / 'clean-arch/step3/library.py')
library = importlib.util.module_from_spec(spec)
spec.loader.exec_module(library)

DOSSIERS = {'financing': ['clean-1'], 'competition': ['clean-18', 'clean-24'], 'roadmap': ['clean-11', 'clean-17']}


def as_record(it):
    return {'id': it['key'], 'article': it['article'], 'publisher': it['publisher'], 'publication_date': it['publication_date'],
            'summary': it['summary'], 'passages': it['passages'], 'original_party': it['original_party'],
            'reporting_speaker': it['reporting_speaker'], 'tier': it['tier'],
            'statement_date': it['statement_date'] or it['statement_date_text'], 'evidence_period': it['evidence_period'],
            'thesis_ids': [t['id'] for t in it['theses']]}


def main():
    folder = Path(sys.argv[1])
    items = {it['key']: it for it in json.loads((folder / 'items.json').read_text())}
    sim = json.loads((folder / 'forward-sim.json').read_text())
    store = library.Library()
    also_matches = {}
    refused = []
    for d in sim['decisions']:
        record = as_record(items[d['key']])
        targets, revises = d['merged_into'], d['later_version_of']
        if len(targets) > 1:
            also_matches[d['key']] = targets
            outcome = {'kind': 'revision' if revises else 'new', 'revises': revises}
        elif targets:
            outcome = {'kind': 'repeat', 'repeat_of': targets, 'revises': revises}
        else:
            outcome = {'kind': 'revision' if revises else 'new', 'revises': revises}
        try:
            store.apply(record, outcome)
        except library.Refused as error:
            refused.append({'key': d['key'], 'reason': str(error)})
    print(f'decisions {len(sim["decisions"])}; groups {len(store.groups)}; several-target items kept as own entries {len(also_matches)}; refused {len(refused)}')
    theses = {t['id']: t['question'] for it in items.values() for t in it['theses']}
    views_dir = folder / 'views'
    views_dir.mkdir(exist_ok=True)
    codes = random.Random(20261108).sample(range(100, 1000), 9)
    key, sizes = {}, {}
    for (name, thesis_ids), code_triplet in zip(DOSSIERS.items(), [codes[0:3], codes[3:6], codes[6:9]]):
        header = 'Research questions in this dossier:\n' + '\n'.join(f'- {theses[t]}' for t in thesis_ids) + '\n\nEvidence entries:\n'
        groups = [g for g in store.order if any(t in store.groups[g]['links'] for t in thesis_ids)]
        labels = {g: f'E{n}' for n, g in enumerate(groups, 1)}
        def notes(g):
            if g not in also_matches:
                return ()
            named = ', '.join(f'[{labels[t]}]' if t in labels else 'an entry outside this dossier' for t in also_matches[g])
            return (f'Also judged a repeat of {named}; kept as its own entry.',)
        rendered = {
            'none': [library.record_text(as_record(items[k]), f'E{n}') for n, k in
                     enumerate([k for k in items if any(t in {x['id'] for x in items[k]['theses']} for t in thesis_ids)], 1)],
            'source': [library.group_text(store, g, labels[g], labels, member_text=False, notes=notes(g)) for g in groups],
            'group': [library.group_text(store, g, labels[g], labels, member_text=True, notes=notes(g)) for g in groups]}
        for (view, entries), code in zip(rendered.items(), code_triplet):
            text = header + '\n\n'.join(entries) + '\n'
            (views_dir / f'{code}.txt').write_text(text)
            key[str(code)] = {'dossier': name, 'view': view, 'entries': len(entries), 'characters': len(text)}
            sizes[f'{name}/{view}'] = (len(entries), len(text))
    (folder / 'views-key.json').write_text(json.dumps(key, indent=1))
    (folder / 'views-replay.json').write_text(json.dumps({'refused': refused, 'also_matches': also_matches,
                                                           'groups': {g: [m['id'] for m in store.groups[g]['members']] for g in store.order}}, indent=1))
    for k, (n, c) in sizes.items():
        print(f'  {k:22s} entries {n:3d}  characters {c}')


if __name__ == '__main__':
    main()

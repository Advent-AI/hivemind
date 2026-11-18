"""The probe's reading folder (DESIGN.md, "Reading"): the control and changed arms' outcomes and three planted H controls merged into
one Stage A run folder, so the existing packet builder, collector and accounting read it unchanged.

  python3 reading_prep.py [--arm a3] <probe data folder> <key folder outside the repository>

Writes <probe data folder>/reading/send-{1,2,3}/outcomes.jsonl and reading/cases.json, and the plants' expected H marks to
<key folder>/plants-expected.json. Each plant is a stored fortnight answer (pass 1 or 3) with its own case name `plant|<n>`; two
have one item added to their list (H should mark it already_judged, or settlement), and one is unchanged (H should mark its cap
`part`). Refuses an existing reading folder.
"""
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STORED = ROOT / 'poc/data/clean-carried-run-2026-11-16'
sys.path.insert(0, str(HERE))
import probe  # noqa: E402   (the configured arms: two, or three for A3)
PLANTS = [   # (plant name, stored case, stored pass, item added to its list or None, the planted item's text, its expected H mark)
    ('plant|1', 'c1/clean-6', 1, {'part': 'Whether NVIDIA or Hugging Face terminates the acquisition agreement before the check date',
                                  'why': 'Termination is a different outcome from completion.'},
     'Whether NVIDIA or Hugging Face terminates the acquisition agreement before the check date', 'already_judged'),
    ('plant|2', 'c1/clean-13', 3, {'part': "Nvidia's networking revenue disclosures and suppliers' CPO/NPO laser shipments",
                                   'why': 'These are the sources through which the shipment volume is observed.'},
     "Nvidia's networking revenue disclosures and suppliers' CPO/NPO laser shipments", 'settlement'),
    ('plant|3', 'c1/clean-7', 1, None, 'Whether MIIT caps the quantities approved', 'part'),
]


def stored_outcome(case, pass_number):
    rows = [json.loads(line) for line in (STORED / f'stage-a/send-{pass_number}/outcomes.jsonl').read_text().splitlines() if line]
    found = [row for row in rows if row['case'] == case and row['pass'] == pass_number]
    if len(found) != 1:
        raise SystemExit(f'{case} pass {pass_number}: {len(found)} stored outcomes, not one')
    return found[0]


def plants():
    """The plant outcomes (all filed as pass 1), their cases, and the expected mark of each planted item by its position."""
    stored_cases = {case['case']: case for case in json.loads((STORED / 'c1/cases/cases.json').read_text())}
    outcomes, cases, expected = [], [], {}
    for name, case_name, pass_number, added, planted_text, mark in PLANTS:
        outcome = copy.deepcopy(stored_outcome(case_name, pass_number))
        parts = outcome['answer']['ladder']['not_judged']
        if added is not None:
            parts.append(added)
        position = [part['part'] for part in parts].index(planted_text)
        outcome.update(case=name, **{'pass': 1})
        outcomes.append(outcome)
        cases.append(dict(stored_cases[case_name], case=name))
        expected[name] = {'position': position, 'part': planted_text, 'expected': mark}
    return outcomes, cases, expected


def main(probe_folder, key_folder):
    probe_folder, key_folder = Path(probe_folder), Path(key_folder)
    if key_folder.resolve().is_relative_to(ROOT.resolve()):
        raise SystemExit('the key folder must be outside the repository')
    reading = probe_folder / 'reading'
    reading.mkdir(exist_ok=False)
    plant_outcomes, plant_cases, expected = plants()
    cases = [case for arm in probe.ARMS for case in json.loads((probe_folder / arm / 'cases.json').read_text())] + plant_cases
    if len({case['case'] for case in cases}) != len(cases):
        raise SystemExit('a case name repeats across the arms and the plants')
    for pass_number in (1, 2, 3):
        rows = [line for arm in probe.ARMS for line in (probe_folder / arm / f'send-{pass_number}' / 'outcomes.jsonl').read_text().splitlines() if line]
        if pass_number == 1:
            rows += [json.dumps(outcome, ensure_ascii=False) for outcome in plant_outcomes]
        (reading / f'send-{pass_number}').mkdir()
        (reading / f'send-{pass_number}' / 'outcomes.jsonl').write_text('\n'.join(rows) + '\n')
    (reading / 'cases.json').write_text(json.dumps(cases, ensure_ascii=False, indent=1) + '\n')
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / 'plants-expected.json').write_text(json.dumps(expected, indent=1) + '\n')
    print(f'reading folder: {len(cases)} cases ({len(plant_cases)} plants); expected plant marks in {key_folder / "plants-expected.json"}')
    return 0


if __name__ == '__main__':
    arguments = sys.argv[1:]
    if arguments[:1] == ['--arm']:
        probe.configure(arguments[1])
        arguments = arguments[2:]
    sys.exit(main(*arguments))

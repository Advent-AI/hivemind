"""python3 chain_dry_run.py <scratch folder>

End-to-end dry run of the comparison's reading chain on the stored slice (no model call, no real key written):
eligibility-shaped input -> mapping export/read/third/result -> deck/mark/debate/readings -> score_comparison.verdict,
then the D400 code check. The six draws are scratch copies of slice-2 (new x3, old x3) relabelled as the run's draws."""
import json
import re
import shutil
import sys
from pathlib import Path

STAGE0 = Path('/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0')
sys.path[:0] = [str(STAGE0), str(STAGE0 / 'census')]
import census_readers  # noqa: E402
import eligibility  # noqa: E402
import mapping  # noqa: E402
import mark_cards  # noqa: E402
import score_comparison  # noqa: E402
import d400_code_check  # noqa: E402

if len(sys.argv) != 2:
    raise SystemExit('usage: python3 chain_dry_run.py <scratch folder outside the repository>')
SCRATCH = Path(sys.argv[1]).resolve()
if str(SCRATCH).startswith('/Users/lchingen/hivemind'):
    raise SystemExit('refused: the scratch folder must be outside the repository (keys are written there)')
SLICE = Path('/Users/lchingen/hivemind/poc/data/comparison-2026-11-17/slice-2')
shutil.rmtree(SCRATCH, ignore_errors=True)
root = SCRATCH / 'run'
root.mkdir(parents=True)
for draw in mapping.DRAWS:
    source = SLICE / ('s-new' if draw.startswith('new') else 's-old')
    shutil.copytree(source, root / draw, ignore=shutil.ignore_patterns('launch.lock', '*.lock'))
    record = json.loads((root / draw / 'run.json').read_text())
    record['identity']['label'] = draw
    (root / draw / 'run.json').write_text(json.dumps(record))
    if draw.startswith('new'):
        inner_path = root / draw / 'judge' / 'run.json'
        inner = json.loads(inner_path.read_text())
        inner[draw] = inner.pop('s-new')
        for attempt in inner[draw]['attempts']:
            attempt['folder'] = f'draw-{draw}'
        inner_path.write_text(json.dumps(inner))
        (root / draw / 'judge' / 'draw-s-new').rename(root / draw / 'judge' / f'draw-{draw}')

keys = SCRATCH / 'keys'
mapping.KEY_FOLDER = keys
mark_cards.mapping_tool.KEY_FOLDER = keys
mark_cards.KEY = keys / 'deck-key.json'

eligible = {'eligible': True, 'problems': [], 'draws': {}}
for draw in mapping.DRAWS:
    paths = mapping.store_paths(root, draw)
    record = json.loads((root / draw / 'run.json').read_text())
    eligible['draws'][draw] = {'stores': {Path(p).name: {'path': str(p), 'sha256': eligibility.sha256(p)} for p in paths},
                               'inputs': {rel: eligibility.sha256(root / draw / rel) for rel in eligibility.section_inputs(root, draw, record)}}
elig_path = SCRATCH / 'eligibility.json'
elig_path.write_text(json.dumps(eligible))

PLANTS = set()
calls = {'read': 0, 'third': 0, 'mark': 0, 'debate': 0, 'other': 0}


def fake_run(family, prompt):
    if '## The matters' in prompt and '## Library' in prompt:
        calls['read'] += 1
        matters = re.findall(r'^- (M\d\d):', prompt, re.M)
        ids = re.findall(r'^- id (Q\d+) ', prompt, re.M)
        rows = []
        for k, m in enumerate(matters):
            if k == 0 and ids:
                rows.append({'matter': m, 'status': 'opened', 'ids': [ids[0]], 'main_outcome': None, 'note': 'fake'})
            elif k == 1 and len(ids) > 1 and family == 'claude':
                rows.append({'matter': m, 'status': 'narrower', 'ids': [ids[1]], 'main_outcome': True, 'note': 'fake'})
            else:
                rows.append({'matter': m, 'status': 'missed', 'ids': [], 'main_outcome': None, 'note': 'fake'})
        return '\n'.join(json.dumps(r) for r in rows), None
    if 'Third reader: does this question cover' in prompt:
        calls['third'] += 1
        return json.dumps({'covers': family == 'codex', 'why': 'fake'}), None
    if '## The card' in prompt:
        debating = '## A second look' in prompt
        if any(text in prompt for text in PLANTS):
            calls['debate' if debating else 'mark'] += 1
            return json.dumps({'worth': 'worth', 'answer': 'unsupported', 'why': 'fake: the plant is rejected'}), None
        calls['debate' if debating else 'mark'] += 1
        no_answer = 'Latest answer at the cutoff: no answer' in prompt
        answer = None if no_answer else ('insufficient' if family == 'claude' and not debating and len(prompt) % 3 == 0 else 'supported')
        return json.dumps({'worth': 'worth', 'answer': answer, 'why': 'fake'}), None
    calls['other'] += 1
    return None, 'unexpected prompt'


census_readers.run = fake_run
mark_cards.confirmed_by_reader = lambda text, supported: (True, {'supported': supported, 'why': 'fake'})

out, deck = SCRATCH / 'mapping-out', SCRATCH / 'deck'
mapping.export(root, out, elig_path)
mapping.read(out)
mapping.third(out)
mapping.result(out)
mark_cards.deck(out, deck)
deck_key = json.loads(mark_cards.KEY.read_text())
PLANTS.update((deck / f'{cid}.txt').read_text() for cid, k in deck_key.items() if k['role'] == 'plant')
mark_cards.mark(deck)
mark_cards.debate(deck, 1)
mark_cards.debate(deck, 2)
mark_cards.readings(out, deck)
try:
    verdict = score_comparison.score(out, deck)
    print('VERDICT', verdict['verdict'], verdict.get('why'))
    print('beside keys', list(verdict.get('beside', {}).keys()))
    print(json.dumps({k: verdict.get(k) for k in ('N', 'margin')}, default=str))
except SystemExit as refusal:
    print('SCORER REFUSED', refusal)
print('sessions', calls)
result, status = d400_code_check.check(root, eligible)
print('D400 code check', status)

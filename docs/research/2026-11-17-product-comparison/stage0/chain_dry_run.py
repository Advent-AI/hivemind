"""python3 chain_dry_run.py <scratch folder>

End-to-end dry run of the comparison's reading chain on the stored slice (no model call, no real key written):
eligibility-shaped input -> mapping export/read/third/result -> deck/mark/debate/readings -> score_comparison.score (which rebuilds
every derived file first), then three edited derived files that the scorer must refuse, then the D400 code check. The six draws are
scratch copies of slice-2 (new x3, old x3) relabelled as the run's draws. `run` restores every module attribute it replaces, so the tests
call it in process."""
import json
import re
import shutil
import sys
from pathlib import Path

STAGE0 = Path(__file__).resolve().parent
sys.path[:0] = [str(STAGE0), str(STAGE0 / 'census')]
import census_readers  # noqa: E402
import eligibility  # noqa: E402
import mapping  # noqa: E402
import mark_cards  # noqa: E402
import score_comparison  # noqa: E402
import d400_code_check  # noqa: E402

REPOSITORY = STAGE0.parents[3]
SLICE = REPOSITORY / 'poc' / 'data' / 'comparison-2026-11-17' / 'slice-2'


def run(scratch):
    """The dry run's report lines."""
    scratch = Path(scratch).resolve()
    if str(scratch).startswith(str(REPOSITORY)):
        raise SystemExit('refused: the scratch folder must be outside the repository (keys are written there)')
    saved = (census_readers.run, eligibility.check, mapping.KEY_FOLDER, mark_cards.KEY, mark_cards.confirmed_by_reader)
    try:
        return chain(scratch)
    finally:
        census_readers.run, eligibility.check, mapping.KEY_FOLDER, mark_cards.KEY, mark_cards.confirmed_by_reader = saved


def chain(scratch):
    lines = []
    shutil.rmtree(scratch, ignore_errors=True)
    root = scratch / 'run'
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

    keys = scratch / 'keys'
    mapping.KEY_FOLDER = keys                                   # mark_cards reads the same module's KEY_FOLDER
    mark_cards.KEY = keys / 'deck-key.json'

    eligible = {'eligible': True, 'problems': [], 'draws': {}}
    for draw in mapping.DRAWS:
        paths = mapping.store_paths(root, draw)
        record = json.loads((root / draw / 'run.json').read_text())
        eligible['draws'][draw] = {'stores': {Path(p).name: {'path': str(p), 'sha256': eligibility.sha256(p)} for p in paths},
                                   'inputs': {rel: eligibility.sha256(root / draw / rel) for rel in eligibility.section_inputs(root, draw, record)}}
    elig_path = scratch / 'eligibility.json'
    eligibility.write(eligible, elig_path)

    plants = set()
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
            calls['debate' if debating else 'mark'] += 1
            if any(text in prompt for text in plants):
                return json.dumps({'worth': 'worth', 'answer': 'unsupported', 'why': 'fake: the plant is rejected'}), None
            no_answer = 'Latest answer at the cutoff: no answer' in prompt
            answer = None if no_answer else ('insufficient' if family == 'claude' and not debating and len(prompt) % 3 == 0 else 'supported')
            return json.dumps({'worth': 'worth', 'answer': answer, 'why': 'fake'}), None
        calls['other'] += 1
        return None, 'unexpected prompt'

    census_readers.run = fake_run
    eligibility.check = lambda run_root: eligible               # the slice has no ledgers; the eligibility-shaped input stands in
    mark_cards.confirmed_by_reader = lambda text, supported: (True, {'supported': supported, 'why': 'fake'})

    out, deck = scratch / 'mapping-out', scratch / 'deck'
    mapping.export(root, out, elig_path)
    mapping.read(out)
    mapping.third(out)
    mapping.result(out)
    mark_cards.deck(out, deck)
    deck_key = json.loads(mark_cards.KEY.read_text())
    plants.update((deck / f'{cid}.txt').read_text() for cid, k in deck_key.items() if k['role'] == 'plant')
    mark_cards.mark(deck)
    mark_cards.debate(deck, 1)
    mark_cards.debate(deck, 2)
    mark_cards.readings(out, deck)
    try:
        verdict = score_comparison.score(root, out, deck)
        lines.append(f"VERDICT {verdict['verdict']} {verdict.get('why')}")
        lines.append(f"beside keys {list(verdict.get('beside', {}).keys())}")
        lines.append(json.dumps({k: verdict.get(k) for k in ('N', 'margin')}, default=str))
    except SystemExit as refusal:
        lines.append(f'SCORER REFUSED {refusal}')

    def edited(path, change):
        """Scores with one derived file edited, twice: with the readings record rewritten from it by its writer (as Codex did in round
        19), and with the record left as it was (so only the file's own comparison can see the edit). Records whether the scorer refused
        each, and restores both files."""
        original, readings_record = path.read_bytes(), (deck / 'readings.json').read_bytes()
        refused = []
        for rewrite_record in (True, False):
            change(path)
            if rewrite_record:
                mark_cards.readings(out, deck)
            try:
                score_comparison.score(root, out, deck)
                refused.append('scored')
            except SystemExit as refusal:
                refused.append(str('derived files differ' in str(refusal)))
            finally:
                path.write_bytes(original)
                (deck / 'readings.json').write_bytes(readings_record)
        lines.append(f"EDIT {'REFUSED' if 'scored' not in refused else 'SCORED'} {path.name} {' '.join(refused)}")

    def bump_distinct(path):
        data = json.loads(path.read_text())
        data['distinct']['new-1']['ids'] += 1
        path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + '\n')

    def move_opened(path):
        data = json.loads(path.read_text())
        cid = next(c for c, k in data.items() if k['role'] == 'product')
        data[cid]['opened'] = '2026-09-19'
        path.write_text(json.dumps(data, indent=1) + '\n')

    edited(out / 'mapping.json', bump_distinct)                 # Codex round 19
    edited(mark_cards.KEY, move_opened)
    edited(deck / 'C001.txt', lambda p: p.write_text(p.read_text() + ' edited'))
    record, original = deck / 'readings.json', (deck / 'readings.json').read_bytes()
    data = json.loads(original)
    data['distinct']['new-1']['ids'] += 1                      # the record alone, not rewritten by its writer
    record.write_text(json.dumps(data, indent=1, ensure_ascii=False) + '\n')
    try:
        score_comparison.score(root, out, deck)
        lines.append('EDIT SCORED readings.json')
    except SystemExit as refusal:
        lines.append(f"EDIT REFUSED readings.json {'derived files differ' in str(refusal)}")
    finally:
        record.write_bytes(original)
    import contextlib
    import io
    import rebuild
    path_before, printed = list(sys.path), io.StringIO()
    with contextlib.redirect_stdout(printed):
        scored_from = rebuild.scored(root, out, deck, mapping.KEY_FOLDER, lambda readings: readings['inputs']['mapping_path'])
    lines.append(f'SCORED FROM SNAPSHOT {not scored_from.startswith(str(out))}')   # the verdict reads the rebuilt files, never the stored
    lines.append(f'REBUILD STDOUT EMPTY {printed.getvalue() == ""}')                # progress goes to stderr; stdout carries only the verdict
    lines.append(f'IMPORT PATH RESTORED {sys.path == path_before}')
    confirmations = mapping.KEY_FOLDER / 'control-confirmations.jsonl'
    kept = confirmations.read_bytes()
    confirmations.unlink()                                      # a failure during setup (Codex round 21)
    try:
        score_comparison.score(root, out, deck)
    except (SystemExit, OSError):
        pass
    finally:
        confirmations.write_bytes(kept)
    lines.append(f'IMPORT PATH RESTORED AFTER A FAILED SETUP {sys.path == path_before}')
    lines.append(f'sessions {calls}')
    result, status = d400_code_check.check(root, eligible)
    lines.append(f'D400 code check {status}')
    return lines


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python3 chain_dry_run.py <scratch folder outside the repository>')
    print('\n'.join(run(sys.argv[1])))

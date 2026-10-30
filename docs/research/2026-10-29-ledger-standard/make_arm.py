"""One arm's files (page §9.3): role-v<N>.txt from role-v<BASE>.txt with the listed replacements (each old text must occur
exactly once), categories-v<N>.json with the base's entries and the reason first in its _note, poc-v<N+16>.json from the
base's config naming T*-v<N>. A new version needs no code change (extraction names the current four reasons for every
version after role-v15). Prints the size change.

    python3 make_arm.py <N> <BASE> <pairs.json> <note> [<category-pairs.json>]   # pairs.json: [[old, new], ...]; category pairs: {"T8.read": [old, new]}
"""
import datetime, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
PROMPTS = ROOT / 'src/hivemind/prompts'
TODAY = datetime.date.today().isoformat()
n, base, pairs, note = int(sys.argv[1]), int(sys.argv[2]), json.loads(Path(sys.argv[3]).read_text()), sys.argv[4]
role = (PROMPTS / f'role-v{base}.txt').read_text()
for target in (PROMPTS / f'role-v{n}.txt', PROMPTS / f'categories-v{n}.json', ROOT / f'poc/config/poc-v{n + 16}.json'):
    assert not target.exists(), f'{target} exists'
new_role = role
for old, new in pairs:
    assert new_role.count(old) == 1, f'occurs {new_role.count(old)} times: {old[:80]}'
    new_role = new_role.replace(old, new)
(PROMPTS / f'role-v{n}.txt').write_text(new_role)
cats = json.loads((PROMPTS / f'categories-v{base}.json').read_text())
for key, (old, new) in (json.loads(Path(sys.argv[5]).read_text()) if len(sys.argv) > 5 else {}).items():   # optional: {"T8.read": [old, new]}
    cat, field = key.split('.')
    assert cats[cat][field].count(old) == 1, f'{key}: occurs {cats[cat][field].count(old)} times'
    cats[cat][field] = cats[cat][field].replace(old, new)
cats['_note'] = f'Version {n} ({TODAY}, arm on version {base}, D244): entries identical to version {base}; {note} ' + cats['_note']
(PROMPTS / f'categories-v{n}.json').write_text(json.dumps(cats, ensure_ascii=True, indent=1) + '\n')
cfg = json.loads((ROOT / f'poc/config/poc-v{base + 16}.json').read_text())
cfg['version'] = f'poc-v{n + 16}'
cfg['_note'] = f'poc-v{n + 16} ({TODAY}): poc-v{base + 16} with extraction T*-v{n} (role-v{n}, categories-v{n}); everything else as poc-v{base + 16}. ' + cfg['_note']
for setting in cfg['extraction'].values():
    assert setting['prompt_version'].endswith(f'-v{base}')
    setting['prompt_version'] = setting['prompt_version'][:-len(str(base))] + str(n)
(ROOT / f'poc/config/poc-v{n + 16}.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n')
print('role', len(role), '->', len(new_role), 'characters')

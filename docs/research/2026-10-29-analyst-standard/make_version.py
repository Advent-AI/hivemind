"""One loop round's files (Alex 2026-10-29: 一类一类改，快速迭代然后测regression): role-v<N>.txt from role-v<N-1>.txt with one
sentence replaced, categories-v<N>.json with the entries unchanged and the reason first in its _note, poc-v<N+16>.json naming
T*-v<N>. A new version needs no code change (extraction names the current four reasons for every version after
role-v15).

    python3 make_version.py <N> <old-sentence-file> <new-sentence-file> <note>
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
PROMPTS = ROOT / 'src/hivemind/prompts'


def main(number, old_file, new_file, note):
    n, prev = int(number), int(number) - 1
    old, new = Path(old_file).read_text().strip('\n'), Path(new_file).read_text().strip('\n')
    role = (PROMPTS / f'role-v{prev}.txt').read_text()
    assert role.count(old) == 1, f'the old sentence occurs {role.count(old)} times in role-v{prev}'
    for target in (PROMPTS / f'role-v{n}.txt', PROMPTS / f'categories-v{n}.json', ROOT / f'poc/config/poc-v{n + 16}.json'):
        assert not target.exists(), f'{target} exists'
    (PROMPTS / f'role-v{n}.txt').write_text(role.replace(old, new))
    text = (PROMPTS / f'categories-v{prev}.json').read_text()
    cats = json.loads(text)
    cats['_note'] = f'Version {n} (2026-10-29, direct read of the v{prev} answers): entries identical to version {prev}; {note} ' + cats['_note']
    (PROMPTS / f'categories-v{n}.json').write_text(json.dumps(cats, ensure_ascii=True, indent=1) + '\n')
    cfg_text = (ROOT / f'poc/config/poc-v{prev + 16}.json').read_text()
    cfg = json.loads(cfg_text)
    cfg['version'] = f'poc-v{n + 16}'
    cfg['_note'] = f'poc-v{n + 16} (2026-10-29): poc-v{prev + 16} with extraction T*-v{n} (role-v{n}, categories-v{n}); everything else as poc-v{prev + 16}. ' + cfg['_note']
    for setting in cfg['extraction'].values():
        assert setting['prompt_version'].endswith(f'-v{prev}')
        setting['prompt_version'] = setting['prompt_version'][:-len(str(prev))] + str(n)
    (ROOT / f'poc/config/poc-v{n + 16}.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n')
    print('role', len(role), '->', len((PROMPTS / f'role-v{n}.txt').read_text()), 'characters')


if __name__ == '__main__':
    main(*sys.argv[1:])

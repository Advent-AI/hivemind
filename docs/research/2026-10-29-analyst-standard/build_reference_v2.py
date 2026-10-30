"""Reference v2: the frozen v1 references (reference.sha256 checked) with the dated changes of reference-v2-changes.json, each with
its reason and authority. v1 stays untouched; v2 is frozen in reference-v2.sha256. Added spans must be verbatim in the item text."""
import copy
import hashlib
import json
from pathlib import Path
import sqlite3

HERE = Path(__file__).resolve().parent
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'


def frozen(name):
    expected = dict(line.split()[::-1] for line in (HERE / 'reference.sha256').read_text().splitlines())
    data = (HERE / name).read_bytes()
    assert hashlib.sha256(data).hexdigest() == expected[name], f'{name} changed after the freeze'
    return json.loads(data)


def main():
    conn = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    changes = json.loads((HERE / 'reference-v2-changes.json').read_text())
    sets = {s: copy.deepcopy(frozen(f'reference-{s}.json')) for s in ('week', 'holdout')}
    applied = 0
    for ch in changes:
        arts = sets[ch['set']]['articles']
        if ch['change'] == 'exclude_to_optional':
            for art in arts:
                keep = []
                for x in art.get('exclude', []):
                    if x['id'] in ch['ids']:
                        art.setdefault('statements', []).append(dict(x, weight='optional', note=x['note'] + ' [v2: optional per D231]'))
                        applied += 1
                    else:
                        keep.append(x)
                art['exclude'] = keep
        elif ch['change'] == 'must_propose_to_acceptable':
            for art in arts:
                if art.get('call_id') in ch['call_ids']:
                    art['acceptable_propose'] = art.get('must_propose', [])
                    art['must_propose'] = []
                    applied += 1
        elif ch['change'] == 'add_statements':
            art = next(a for a in arts if a.get('call_id') == ch['call_id'])
            text = conn.execute('select text from items where input_id=?', (art['input_id'],)).fetchone()[0]
            for s in ch['statements']:
                for span in [s['span']] + s['also']:
                    assert span in text, (s['id'], span)
                art.setdefault('statements', []).append(s)
                applied += 1
    digests = {}
    for s, data in sets.items():
        data['about'] = dict(data['about'], v2='2026-10-29: v1 plus reference-v2-changes.json (each change with its reason)')
        name = f'reference-{s}-v2.json'
        (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n')
        digests[name] = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
    (HERE / 'reference-v2.sha256').write_text(''.join(f'{d}  {n}\n' for n, d in digests.items()))
    print('applied', applied, digests)


if __name__ == '__main__':
    main()

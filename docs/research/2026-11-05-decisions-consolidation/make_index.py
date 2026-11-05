"""Build the register's index (every decision number with its status and section) from final.jsonl and the log's titles, plus the
per-area lists of in-force rules (with the second reader's checks) that the register's sections are written from.

usage: python3 make_index.py   (writes index.md and in-force-by-area.md)
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = Path('/Users/lchingen/hivemind/docs/DECISIONS.md')
SECTION = {'system': 'System', 'universe': 'Universe', 'classification': 'Classification', 'config': 'Config', 'dispatch': 'Dispatch',
           'extraction': 'Extraction', 'library': 'Thesis library', 'closing': 'Closing and pull mode', 'review-pool': 'Review pool',
           'filing-phase': 'Current phase', 'ruler': 'Ruler and measurement', 'idea-service': 'Idea and service', 'frontend': 'Frontend',
           'data': 'Data', 'operations': 'Operations', 'working-rules': 'Working rules'}


def titles():
    found = {}
    for m in re.finditer(r'^## (D\d+) · ([^·]+?) · (.+)$', LOG.read_text(encoding='utf-8'), re.M):
        found[m.group(1)] = (m.group(2).strip(), m.group(3).strip())
    return found


def status_text(record):
    later = ', '.join(record['by'])
    if record['status'] == 'in-force':
        return f'in force (amended by {later})' if later else 'in force'
    if record['status'] == 'superseded':
        return f'superseded by {later}' if later else 'superseded'
    if record['status'] == 'retired':
        return f'retired ({later})' if later else 'retired'
    return 'record'


def main():
    names = titles()
    records = [json.loads(l) for l in (HERE / 'final.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
    rows = ['| D | Date | Decision | Status | Section |', '|---|---|---|---|---|']
    for r in records:
        date, title = names[r['id']]
        title = title.replace('|', '/')
        if len(title) > 110:
            title = title[:107].rstrip() + '…'
        rows.append(f'| {r["id"]} | {date[:10]} | {title} | {status_text(r)} | {SECTION[r["area"]]} |')
    (HERE / 'index.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')
    out = []
    for area, name in SECTION.items():
        live = [r for r in records if r['area'] == area and r['status'] == 'in-force']
        out.append(f'\n## {name} ({len(live)} in force)\n')
        for r in live:
            out.append(f'- {r["id"]} [{r["authority"]}] {r["rule"]} (home {r["home"]}; agrees {r["home_agrees"]})')
            for c in r.get('checks') or []:
                if c['field'] in ('rule', 'status', 'conflicts', 'home', 'home_agrees'):
                    out.append(f'    · check {c["field"]}: {c["problem"]} → {c["correct"]}')
            for c in r['conflicts'] or []:
                out.append(f'    · conflict: {c}')
    (HERE / 'in-force-by-area.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(f'index rows {len(records)}; in force {sum(r["status"] == "in-force" for r in records)}')


if __name__ == '__main__':
    main()

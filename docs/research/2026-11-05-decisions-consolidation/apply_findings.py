"""Apply the second reader's (Codex's) findings to the merged first-pass records and write final.jsonl.

Status, authority and superseding-decision corrections are applied when the finding states the corrected value plainly; rule and
conflict findings are attached to the record as `checks` for the person writing the register to read. Prints what it changed.

usage: python3 apply_findings.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATUSES = ('in-force', 'superseded', 'retired', 'record')


def main():
    records = {r['id']: r for r in (json.loads(l) for l in (HERE / 'merged.jsonl').read_text(encoding='utf-8').splitlines() if l.strip())}
    changed, unchecked = [], []
    for path in sorted(HERE.glob('verify-*.jsonl')):
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line.strip():
                continue
            try:
                finding = json.loads(line)
            except json.JSONDecodeError:
                continue
            if 'checked' in finding:
                unchecked += finding.get('unchecked') or []
                continue
            record = records.get(finding.get('id'))
            if record is None:
                continue
            record.setdefault('checks', []).append({k: finding.get(k) for k in ('field', 'problem', 'correct', 'evidence')})
            field, correct = finding.get('field'), str(finding.get('correct') or '')
            if field == 'status':
                lead = correct.strip().lower()
                status = next((s for s in STATUSES if lead.startswith(s)), None) or ('in-force' if lead.startswith('in force') else None)
                if status and status != record['status']:
                    changed.append(f'{record["id"]}: status {record["status"]} -> {status} ({correct[:90]})')
                    record['status'] = status
            elif field == 'authority' and correct.strip().lower().split(' ')[0].strip('.;,') in ('alex', 'claude', 'unconfirmed'):
                value = correct.strip().lower().split(' ')[0].strip('.;,')
                if value != record['authority']:
                    changed.append(f'{record["id"]}: authority {record["authority"]} -> {value}')
                    record['authority'] = value
            elif field == 'by':
                for later in re.findall(r'D\d+', correct):
                    if later not in record['by']:
                        record['by'].append(later)
                        changed.append(f'{record["id"]}: by + {later}')
    ordered = sorted(records.values(), key=lambda r: int(r['id'][1:]))
    (HERE / 'final.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in ordered), encoding='utf-8')
    print(f'{len(ordered)} records; {sum(1 for r in ordered if r.get("checks"))} carry checks; unchecked by the second reader: {unchecked}')
    print('\n'.join(changed))


if __name__ == '__main__':
    main()

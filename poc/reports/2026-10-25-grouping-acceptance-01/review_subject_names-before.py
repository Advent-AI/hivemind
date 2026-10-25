"""Read a subject-names experiment directory without model calls and report, per sample and separately: what the
third article's extraction proposed, which subject names it chose, how code resolved them, wiring errors (impossible
by construction, counted anyway), re-declared shown subjects, and the two semantic checks the plan fixed in advance for
the development article (the OpenAI deployment belongs to the Rubin subject and its own, never to the SK-specific one;
the PC SoC thesis belongs to no shown subject) and for the held-out articles (Google's Rubin deployment joins the Rubin
subject; AMD's own revenue never does). The semantic labels are the assistant's reading of the articles, not gold.

Usage: python3 poc/hierarchy_study/review_subject_names.py --out DIR [--case dev|google|amd]
"""
import argparse
import json
import re
from pathlib import Path

RUBIN = re.compile(r'rubin', re.I)
SK = re.compile(r'\bSK\b|SK Telecom', re.I)
OPENAI = re.compile(r'openai', re.I)
PC = re.compile(r'\bPC\b|SoC|Windows', re.I)
AMD_OWN = re.compile(r'\bAMD\b.*(revenue|server|data center|growth)', re.I)
GOOGLE = re.compile(r'google|A5X', re.I)


def read_sample(folder):
    extract = json.loads((folder / 'item3-extract.json').read_text()) if (folder / 'item3-extract.json').exists() else None
    projection = json.loads((folder / 'item3-extract-projection.json').read_text()) if (folder / 'item3-extract-projection.json').exists() else None
    result = json.loads((folder / 'item3-result.json').read_text()) if (folder / 'item3-result.json').exists() else None
    failed = json.loads((folder / 'failed.json').read_text()) if (folder / 'failed.json').exists() else None
    return extract, projection, result, failed


def subject_names_of(result, view_id):
    names = {t['thread_id']: t['name'] for t in result['threads']}
    return [names[m['thread_id']] for m in result['memberships'] if m['view_id'] == view_id]


def review(out, case):
    manifest = json.loads((out / 'manifest.json').read_text())
    rows = []
    for label in manifest['plan'][case]:
        folder = out / f'sample-{label}'
        extract, projection, result, failed = read_sample(folder)
        row = {'sample': label, 'failed': failed['error'][:160] if failed else None, 'proposed': [], 'memberships': {}, 'wiring_errors': 0, 'redeclared': 0,
               'scope_errors': [], 'core_kept': None, 'notes': []}
        if extract and extract.get('answer'):
            answer = extract['answer']
            row['proposed'] = [c['question'][:70] for c in answer['candidates']]
            if label.endswith('-names') and projection:
                row['redeclared'] = projection['counts']['redeclared_existing']
                # a wiring error would be a candidate whose chosen subject names do not match its resolved IDs; by construction zero
                for chosen, ids in zip(projection['subjects'], projection['thread_ids']):
                    want = sum(1 for s in chosen if s['existing'] != 'none') + sum(1 for s in chosen if s['existing'] == 'none')
                    if len(ids) > want:
                        row['wiring_errors'] += 1
        if result:
            names = {t['thread_id']: t['name'] for t in result['threads']}
            for view in result['views']:
                vid = view['view_id']; q = view.get('question', '')
                members = subject_names_of(result, vid)
                row['memberships'][q[:60]] = members
                if case == 'dev':
                    if OPENAI.search(q):
                        if any(SK.search(n) for n in members): row['scope_errors'].append(f'OpenAI thesis in the SK-specific subject: {members}')
                        if not any(RUBIN.search(n) for n in members): row['notes'].append(f'OpenAI thesis not in the Rubin subject: {members}')
                    if PC.search(q) and not OPENAI.search(q):
                        if any(RUBIN.search(n) or SK.search(n) for n in members): row['scope_errors'].append(f'PC thesis in {members}')
                if case == 'google' and GOOGLE.search(q) and RUBIN.search(q):
                    row['core_kept'] = any(RUBIN.search(n) and not GOOGLE.search(n) for n in members)
                if case == 'amd' and AMD_OWN.search(q):
                    if any(RUBIN.search(n) for n in members): row['scope_errors'].append(f'AMD own-revenue thesis in a Rubin subject: {members}')
            core = [vid for vid, q in ((v['view_id'], v.get('question', '')) for v in result['views']) if RUBIN.search(q) and 'shipment' in q.lower()]
            if core and case == 'dev':
                row['core_kept'] = all(any(RUBIN.search(n) for n in subject_names_of(result, vid)) for vid in core)
        rows.append(row)
    print(f"{case}: {len(rows)} samples")
    for r in rows:
        print(f"\n{r['sample']}: " + (f"FAILED {r['failed']}" if r['failed'] else f"proposed {len(r['proposed'])}; wiring errors {r['wiring_errors']}; re-declared shown {r['redeclared']}; scope errors {r['scope_errors'] or 'none'}; core kept {r['core_kept']}"))
        for q, members in r['memberships'].items():
            print(f"   {q:60s} → {members}")
        for n in r['notes']:
            print('   note:', n)
    done = [r for r in rows if not r['failed'] and r['memberships']]      # a sample counts as completed only with a written result
    print(f"\n{case} summary: completed {len(done)}/{len(rows)}; wiring errors {sum(r['wiring_errors'] for r in done)}; re-declared shown subjects {sum(r['redeclared'] for r in done)}; samples with a scope error {sum(bool(r['scope_errors']) for r in done)}; core connection kept {sum(1 for r in done if r['core_kept'])}/{sum(1 for r in done if r['core_kept'] is not None)}")
    budget = json.loads((out / 'budget.json').read_text())
    print(f"requests {len(budget['attempts'])}, estimated ${budget['estimated_spent']:.4f}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--case', choices=['dev', 'google', 'amd'], default='dev')
    args = parser.parse_args()
    review(args.out.resolve(), args.case)

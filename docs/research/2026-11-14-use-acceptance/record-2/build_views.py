"""The record test on unread articles: the two readers' views ($0; RECORD-TEST-2-DESIGN.md). Code only, the same rules for both arms.

Rows: every figure of every kept statement whose stored measure names revenue, sales or gross margin, from the articles for which BOTH arms
gave a valid answer (an article either arm lacks is left out of both views and listed). A row's source is the figure's own party where
the arm stores one, else the statement's party; its period key is the arm's fixed period where it stores one, else the stored period in
one spelling. Rows are merged only when measure, period key, value, kind, source and basis are all equal after normalising case and
spacing; a merged line lists every article it came from. Every line carries an id; `view-rows-<label>.json` keeps, for each id, the arm's
statement ids, passages and articles, so a reader's answer can be traced to its rows. Labels A and B are drawn by seed; the key goes
outside the repository.

  python3 build_views.py <records.jsonl> <cases.json> <key folder outside the repository> [--arms c8,c22] [--name views]
"""
import collections
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAIN = re.compile(r'\b(revenues?|sales|gross margins?)\b', re.I)


def normal(text):
    return ' '.join(str(text).split()).lower() if text is not None else ''


def rows_of(records, arm, article_of, allowed):
    rows = []
    for record in records:
        if record['arm'] != arm or record['case'] not in allowed:
            continue
        for statement in record.get('links') or []:
            for figure in statement.get('figures') or []:
                if not MAIN.search(figure.get('measure') or ''):
                    continue
                rows.append({'article': article_of[record['case']], 'statement': statement.get('local_id'),
                             'measure': figure.get('measure'), 'period': figure.get('period'), 'fixed': figure.get('fiscal_period'),
                             'value': figure.get('value'), 'kind': figure.get('kind'), 'basis': figure.get('basis'),
                             'source': figure['party'] if 'party' in figure else statement.get('original_party'),
                             'said': statement.get('statement_date') or statement.get('statement_date_text'),
                             'passages': statement.get('verified_source_passages') or statement.get('source_passages')})
    return rows


def view(rows, label):
    merged = collections.OrderedDict()
    for row in rows:
        period_key = row['fixed'] or normal(row['period'])
        key = (normal(row['measure']), period_key, normal(row['value']), row['kind'], normal(row['source']), normal(row['basis']))
        merged.setdefault(key, []).append(row)
    headings = collections.OrderedDict()
    for key, members in merged.items():
        headings.setdefault((key[0], key[1]), []).append(members)
    out = [f'# Company record {label}: revenue and gross margin',
           '',
           'Each line is one stored figure with its id: its value, its kind (actual = reported; guidance = the company\'s own outlook; estimate =',
           'someone\'s forecast), its source as stored, the basis as stored, the statement date when stored, and the articles it came from.',
           'Headings are the measure and the period as stored (a code such as FY2027-Q3 is the third quarter of fiscal 2027).',
           '']
    trace, number = {}, 0
    for (measure, period_key), groups in sorted(headings.items()):
        out.append(f'## {measure} | {period_key or "(no period stored)"}')
        for members in groups:
            number += 1
            row_id = f'{label}-{number:03d}'
            first = members[0]
            articles = sorted({m['article'] for m in members})
            dates = sorted({str(m['said']) for m in members if m['said']})
            out.append(f"- [{row_id}] **{first['value']}** | {first['kind']} | source: {first['source'] or 'not stored'} | basis: {first['basis'] or 'not stored'}"
                       f" | said: {', '.join(dates) if dates else 'not stored'} | articles {', '.join(str(a) for a in articles)}")
            trace[row_id] = [{'article': m['article'], 'statement': m['statement'], 'passages': m['passages']} for m in members]
        out.append('')
    return '\n'.join(out), trace, len(merged), len(headings)


def main():
    records = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
    cases = json.loads(Path(sys.argv[2]).read_text())
    key_folder = Path(sys.argv[3])
    arms = sys.argv[sys.argv.index('--arms') + 1].split(',') if '--arms' in sys.argv else ['c8', 'c22']
    name = sys.argv[sys.argv.index('--name') + 1] if '--name' in sys.argv else 'views'
    article_of = {case['case']: case['sequence'] for case in cases}
    valid = {arm: {r['case'] for r in records if r['arm'] == arm and r['attempts'] and r['attempts'][-1].get('outcome') == 'valid'} for arm in arms}
    allowed = set.intersection(*valid.values())
    left_out = sorted(set(article_of) - allowed)
    rng = random.Random(20261124)
    labels = ['A', 'B'] if rng.random() < 0.5 else ['B', 'A']
    key = {'labels': dict(zip(arms, labels)), 'articles_left_out': left_out}
    for arm, label in zip(arms, labels):
        rows = rows_of(records, arm, article_of, allowed)
        text, trace, merged, headings = view(rows, label)
        (HERE / f'{name}-record-{label}.md').write_text(text)
        (HERE / f'{name}-rows-{label}.json').write_text(json.dumps(trace, ensure_ascii=False, indent=1))
        key[arm] = {'label': label, 'rows': len(rows), 'lines': merged, 'headings': headings, 'with_fixed_period': sum(1 for r in rows if r['fixed'])}
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / f'record-2-key-{name}.json').write_text(json.dumps(key, indent=1))
    print(f"articles in both views: {len(allowed)}; left out (an arm has no valid answer): {left_out}")
    for arm in arms:
        print(f"  {arm}: {key[arm]['rows']} rows, {key[arm]['lines']} lines under {key[arm]['headings']} headings; rows with a fixed period {key[arm]['with_fixed_period']}")


if __name__ == '__main__':
    main()

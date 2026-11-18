"""The company record test ($0; RECORD-TEST-DESIGN.md): every figure entry of every kept statement of the clean week draw, one row each
(`record-week.json`); the reader's view of the revenue and gross-margin rows of the 40 sampled articles (`record-view.md`); and the seeded
fidelity sample of 20 rows from each stratum with its article (`fidelity-packet.json`). Code only: no row is edited, no measure is judged.
A row is in stratum R when its stored measure names revenue, sales or gross margin, otherwise in O.

  python3 build_record.py <key folder outside the repository>
"""
import collections
import json
import random
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = Path('/Users/lchingen/hivemind/poc/data/clean-lean-week-2026-11-14/week-r2/c1')
ITEMS = Path('/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite')
PACKET = HERE.parent / 'week/packet-A1.json'
MAIN = re.compile(r'\b(revenues?|sales|gross margins?)\b', re.I)
FISCAL = re.compile(r'\b(?:fiscal(?:\s+year)?\s+|FY\s?)(?:20)?(\d\d)\b', re.I)


def normal(text):
    """Case and spacing only, and one written form for a fiscal year that is written out; nothing is inferred."""
    if text is None:
        return ''
    text = FISCAL.sub(lambda match: f'FY20{match.group(1)}', ' '.join(str(text).split()))
    return text.lower()


def rows_of_week():
    trace = sqlite3.connect(f'file:{RUN / "step1/trace.sqlite"}?mode=ro', uri=True)
    items = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    library = json.loads((RUN / 'step2/library.json').read_text())
    groups = library['groups']
    group_of = {}
    for name, group in (groups.items() if isinstance(groups, dict) else enumerate(groups)):
        for member in group.get('members') or []:
            group_of[member if isinstance(member, str) else member.get('id')] = str(name)
    rows = []
    for sequence, input_id, result_json in trace.execute("select sequence, input_id, result from trace where status='complete' order by sequence"):
        day, title = items.execute('select publication_day, title from items where input_id = ?', (input_id,)).fetchone()
        for statement in json.loads(result_json).get('evidence') or []:
            for position, figure in enumerate(statement.get('figures') or [], 1):
                rows.append({'row': len(rows) + 1, 'step': sequence, 'input_id': input_id, 'day': day, 'title': title,
                             'statement': statement['local_id'], 'figure': position,
                             'measure': figure.get('measure'), 'basis': figure.get('basis'), 'period': figure.get('period'),
                             'value': figure.get('value'), 'kind': figure.get('kind'),
                             'original_party': statement.get('original_party'), 'reporting_speaker': statement.get('reporting_speaker'),
                             'statement_date': statement.get('statement_date'), 'statement_date_text': statement.get('statement_date_text'),
                             'tier': statement.get('tier'), 'summary': statement.get('summary'),
                             'passages': statement.get('verified_source_passages') or statement.get('source_passages'),
                             'linked': bool(statement.get('links')), 'group': group_of.get(f"{sequence}:{statement['local_id']}"),
                             'stratum': 'R' if MAIN.search(figure.get('measure') or '') else 'O'})
    return rows


def write_view(rows, article_number):
    chosen = [row for row in rows if row['stratum'] == 'R' and row['input_id'] in article_number]
    merged = collections.OrderedDict()
    for row in chosen:
        key = (normal(row['measure']), normal(row['period']), normal(row['value']), row['kind'], normal(row['original_party']))
        merged.setdefault(key, []).append(row)
    by_heading = collections.OrderedDict()
    for key, members in merged.items():
        by_heading.setdefault((key[0], key[1]), []).append(members)
    out = ['# Company record: revenue and gross margin, from 40 articles of 2026-09-22..28',
           '',
           'Each line is one stored figure: its value, its kind (actual = reported; guidance = the company\'s own outlook; estimate = a named',
           'party\'s or consensus forecast), the basis as stored, who it is from, the statement date when stored, and the articles it came from',
           '(article number and day). Headings are the measure and period exactly as stored, in one spelling.',
           '']
    for (measure, period), groups in sorted(by_heading.items()):
        out.append(f'## {measure} | {period or "(no period stored)"}')
        for members in groups:
            first = members[0]
            sources = ', '.join(f"article {article_number[m['input_id']]} ({m['day']})" for m in members)
            bases = sorted({str(m['basis']) for m in members if m['basis']})
            dates = sorted({m['statement_date'] or m['statement_date_text'] or '' for m in members} - {''})
            out.append(f"- **{first['value']}** | {first['kind']} | from: {first['original_party'] or 'not stored'}"
                       f" | basis: {'; '.join(bases) if bases else 'not stored'} | said: {', '.join(dates) if dates else 'not stored'} | {sources}")
        out.append('')
    (HERE / 'record-view.md').write_text('\n'.join(out))
    return len(chosen), len(merged), len(by_heading)


def main():
    key_folder = Path(sys.argv[1])
    rows = rows_of_week()
    (HERE / 'record-week.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    packet = json.loads(PACKET.read_text())
    key = json.loads((key_folder / 'week-key-A1.json').read_text())
    article_number = {row['input_id']: row['article'] for row in key}
    assert len(article_number) == len(packet) == 40
    used, merged, headings = write_view(rows, article_number)
    strata = collections.Counter(row['stratum'] for row in rows)
    rng = random.Random(20261119)
    sample = []
    for stratum in ('R', 'O'):
        pool = [row for row in rows if row['stratum'] == stratum]
        sample += rng.sample(pool, min(20, len(pool)))
    items = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    order = rng.sample(sample, len(sample))
    entries = []
    for number, row in enumerate(order, 1):
        text = items.execute('select text from items where input_id = ?', (row['input_id'],)).fetchone()[0]
        entries.append({'entry': number, 'record_row': {name: row[name] for name in ('measure', 'basis', 'period', 'value', 'kind', 'original_party',
                                                                                 'statement_date', 'statement_date_text')},
                        'article': {'day': row['day'], 'title': row['title'], 'text': text}})
    (HERE / 'fidelity-packet.json').write_text(json.dumps(entries, ensure_ascii=False, indent=1))
    (key_folder / 'record-key-fidelity.json').write_text(json.dumps(
        [{'entry': number, 'row': row['row'], 'stratum': row['stratum'], 'step': row['step'], 'statement': row['statement']}
         for number, row in enumerate(order, 1)], indent=1))
    statements = len({(row['step'], row['statement']) for row in rows})
    print(f'full-week record: {len(rows)} figure rows from {statements} statements of {len({row["step"] for row in rows})} articles; '
          f'strata R {strata["R"]}, O {strata["O"]}; kinds {dict(collections.Counter(row["kind"] for row in rows))}')
    print(f'missing: period {sum(row["period"] is None for row in rows)}, basis {sum(row["basis"] is None for row in rows)}, '
          f'original party {sum(row["original_party"] is None for row in rows)}, statement date {sum(row["statement_date"] is None for row in rows)}')
    print(f'view (40 articles): {used} revenue and margin rows, {merged} after merging equal rows, under {headings} headings')
    print(f'fidelity sample: {sum(1 for row in sample if row["stratum"] == "R")} from R, {sum(1 for row in sample if row["stratum"] == "O")} from O')


if __name__ == '__main__':
    main()

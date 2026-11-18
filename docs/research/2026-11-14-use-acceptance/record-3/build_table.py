"""The financial table ($0; TABLE-TEST-DESIGN.md, D501): one arm's stored revenue and gross-margin figures laid out by code alone.

Rows are the same rows the record test used (`record-2/build_views.rows_of`: one owner of the selection rule). Code joins only what the
stored text itself establishes:

- **Whose figure.** A source is the covered company when, with a trailing parenthesis set aside, it is the company's name alone or with
  "Corporation", "Corp", "Inc" or "management" (a full match; the name is an argument). Every other source stays as written and is
  joined only with the same spelling. The source as written is kept on every line.
- **Period.** A stored period becomes a fixed key only when the whole string (a trailing parenthesis set aside) is one of a closed set
  of forms that write the word "fiscal", one year and at most one quarter ("fiscal q2 2027", "second quarter of fiscal 2027",
  "fiscal 2028"). Anything else ("last quarter", "this year", "twelve months to fiscal q2 2027", "q3 2026") stays as written: no period
  is derived from the article's day or from outside knowledge. The period as stored is kept on every line. The stored period is the
  reading system's label, which may itself hold a year the article only implies: the table does not verify it.
- **One line.** Rows are one line only when whose figure it is (the company, or the same spelling of another source), the kind, the
  period key, the measure and the value are equal after normalising case and spacing. On such a line every article keeps its own
  stored basis, source, period and date beneath it: a qualification is never shown as if every article gave it.

Layout: a section for the company's figures of each kind and one for others' figures of each kind (a layout only: others' figures are
never joined across spellings); inside a section a block for each period key (fixed keys first, then periods as written, then no
period); inside a block, lines sorted by measure and value. `table-rows.json` keeps each line's statements, passages and articles.

  python3 build_table.py <records.jsonl> <cases.json> --company NVIDIA [--arm c8]
  python3 build_table.py --trace <a finished run's step1/trace.sqlite> --company NVIDIA --name week

With `--trace` the rows come from a finished run's stored Step 1 answers (read-only), each article numbered by its place in the run;
the outputs are `financial-table-<name>.md` and `table-rows-<name>.json`.
"""
import collections
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'record-2'))
from build_views import normal, rows_of  # noqa: E402  (the record test's row rule, one owner)

QUARTER = {'q1': 1, 'q2': 2, 'q3': 3, 'q4': 4, 'first': 1, 'second': 2, 'third': 3, 'fourth': 4}
WORD = r'(first|second|third|fourth)'
PERIOD_FORMS = [  # full matches only; each writes "fiscal", one year and at most one quarter
    (re.compile(r'fiscal (q[1-4]) (\d{4})'), lambda m: (m.group(2), m.group(1))),
    (re.compile(r'(q[1-4]) (?:of )?fiscal (?:year )?(\d{4})'), lambda m: (m.group(2), m.group(1))),
    (re.compile(rf'fiscal {WORD} quarter of (\d{{4}})'), lambda m: (m.group(2), m.group(1))),
    (re.compile(rf'{WORD} quarter of fiscal (?:year )?(\d{{4}})'), lambda m: (m.group(2), m.group(1))),
    (re.compile(rf'fiscal (?:year )?(\d{{4}}) {WORD} quarter'), lambda m: (m.group(1), m.group(2))),
    (re.compile(rf'fiscal {WORD} quarter (\d{{4}})'), lambda m: (m.group(2), m.group(1))),
    (re.compile(r'fiscal (?:year )?(\d{4})'), lambda m: (m.group(1), None)),
]
MUST_STAY_AS_WRITTEN = ['twelve months to fiscal q2 2027', 'year-ago quarter (fiscal q3 2026)', 'fiscal 2026 to fiscal 2029',
                        'fiscal q2 (ended july 26)', 'fourth quarter (fiscal year not stated)', 'q3 2026', '2026', 'second quarter',
                        'fiscal year ended jan. 25, 2026', 'next year (after the 10 september 2026 comment)', 'fiscal second quarter']
MUST_BE_FIXED = {'fiscal q2 2027': 'FY2027-Q2', 'q2 fiscal 2027': 'FY2027-Q2', 'fiscal second quarter of 2027': 'FY2027-Q2',
                 'second quarter of fiscal 2027': 'FY2027-Q2', 'fiscal 2027 second quarter': 'FY2027-Q2',
                 'fiscal q2 2027 (quarter ended july 26, 2026)': 'FY2027-Q2', 'fiscal 2028 (ending january 2028)': 'FY2028',
                 'fiscal year 2028': 'FY2028'}


def period_key(stored):
    """(key, fixed?): a fixed key for the closed set of forms, else the stored period in one spelling."""
    text = normal(stored)
    if text in ('', 'none', 'null'):
        return '(no period stored)', False
    core = re.sub(r'\s*\([^()]*\)$', '', text)
    for pattern, read in PERIOD_FORMS:
        match = pattern.fullmatch(core)
        if match:
            year, quarter = read(match)
            return (f'FY{year}-Q{QUARTER[quarter]}' if quarter else f'FY{year}'), True
    return text, False


def source_group(stored, company):
    """'company' for the covered company's name alone or with a legal suffix or "management"; else the source as written."""
    text = normal(stored)
    if text in ('', 'none', 'null'):
        return '(no source stored)'
    core = re.sub(r'\s*\([^()]*\)$', '', text)
    name = re.escape(company.lower())
    if re.fullmatch(rf'{name}(?: corporation| corp\.?| inc\.?)?(?: management)?', core):
        return 'company'
    return text


def self_check(company):
    for stored in MUST_STAY_AS_WRITTEN:
        assert not period_key(stored)[1], f'the period check must leave this as written: {stored!r}'
    for stored, key in MUST_BE_FIXED.items():
        assert period_key(stored) == (key, True), f'the period check must read {stored!r} as {key}'
    assert source_group(f'{company} (CFO Colette Kress)', company) == 'company' and source_group(f'{company} Corporation (management)', company) == 'company'
    for other in ('Wall Street analysts', 'AMD', f'analysts covering {company}', f'{company} supplier SK Hynix', 'Zacks Investment Research'):
        assert source_group(other, company) != 'company', f'not the company: {other!r}'


def stored_run(trace_path):
    """A finished run's stored Step 1 answers in the shape the row rule reads: one record an article, numbered by its sequence."""
    trace = sqlite3.connect(f'file:{trace_path}?mode=ro', uri=True)
    records, article_of = [], {}
    for sequence, status, result in trace.execute('select sequence, status, result from trace order by sequence'):
        if status != 'complete' or not result:
            raise SystemExit(f'article {sequence} has no stored answer (status {status}): refused, a missing answer is not an empty table')
        records.append({'arm': 'stored', 'case': str(sequence), 'links': json.loads(result).get('evidence') or []})
        article_of[str(sequence)] = sequence
    return records, article_of


def main():
    company = sys.argv[sys.argv.index('--company') + 1]
    name = sys.argv[sys.argv.index('--name') + 1] if '--name' in sys.argv else None
    self_check(company)
    if '--trace' in sys.argv:
        arm = 'stored'
        records, article_of = stored_run(sys.argv[sys.argv.index('--trace') + 1])
        valid = set(article_of)
    else:
        records = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
        cases = json.loads(Path(sys.argv[2]).read_text())
        arm = sys.argv[sys.argv.index('--arm') + 1] if '--arm' in sys.argv else 'c8'
        article_of = {case['case']: case['sequence'] for case in cases}
        valid = {r['case'] for r in records if r['arm'] == arm and r['attempts'] and r['attempts'][-1].get('outcome') == 'valid'}
    rows = rows_of(records, arm, article_of, valid)
    kind_order = {'actual': 0, 'guidance': 1, 'estimate': 2}
    titles = {('company', 'actual'): f'Stored as reported by {company} (actual)', ('company', 'guidance'): f"Stored as {company}'s own outlook (guidance)",
              ('company', 'estimate'): f"Stored as {company}'s own estimate (estimate)",
              ('others', 'actual'): 'Stored as reported by someone else (actual); the stored source is on each line',
              ('others', 'guidance'): "Stored as someone else's own outlook (guidance); the stored source is on each line",
              ('others', 'estimate'): "Stored as someone else's forecast (estimate); the stored source is on each line"}
    sections = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.OrderedDict()))
    for row in rows:
        group = source_group(row['source'], company)
        key, fixed = period_key(row['period'])
        row['period_fixed'] = fixed
        section = ('company' if group == 'company' else 'others', row['kind'])
        sections[section][(0 if fixed else (2 if key == '(no period stored)' else 1), key)].setdefault(
            (normal(row['measure']), normal(row['value']), group), []).append(row)
    out = [f'# Financial table: revenue and gross margin as stored about {company}',
           '',
           'Everything here is what a system stored after reading each article: the measure, the kind, the source, the period and the basis are',
           'the system\'s stored labels, not the article\'s own sentences. Sections say whose figure the system stored it as, and of what kind',
           '(actual = reported; guidance = the company\'s own outlook; estimate = a forecast). Inside a section, a block is one period: a code',
           'such as FY2027-Q3 (the third quarter of fiscal 2027) where the stored period writes the fiscal year, else the period exactly as',
           'stored (it may be relative: "current quarter"). Each line is one figure with its id. Where several articles were stored with the',
           'same measure, value, kind, period and source, they are one line, and each article keeps its own stored details beneath it.',
           '']
    trace, number, blocks = {}, 0, 0
    ordered = sorted(sections, key=lambda sk: (0 if sk[0] == 'company' else 1, kind_order.get(sk[1], 9)))
    for section in ordered:
        out.append(f'## {titles[section]}')
        for rank_and_key in sorted(sections[section]):
            block = sections[section][rank_and_key]
            blocks += 1
            out.append(f'### {rank_and_key[1]}')
            for _, members in sorted(block.items()):
                number += 1
                line_id = f'T-{number:03d}'
                first = members[0]

                def details(member):
                    return (f"basis: {member['basis'] or 'not stored'} | source as stored: {member['source'] or 'not stored'}"
                            f" | period as stored: {member['period'] or 'not stored'} | said: {member['said'] or 'not stored'}")
                if len(members) == 1:
                    out.append(f"- [{line_id}] {first['measure']}: **{first['value']}** | {details(first)} | article {first['article']}")
                else:
                    out.append(f"- [{line_id}] {first['measure']}: **{first['value']}** | stored from {len(members)} articles, each with its own details:")
                    for member in sorted(members, key=lambda m: m['article']):
                        out.append(f"    - article {member['article']}: {details(member)}")
                trace[line_id] = [{'article': m['article'], 'statement': m['statement'], 'measure': m['measure'], 'period': m['period'], 'value': m['value'],
                                   'kind': m['kind'], 'basis': m['basis'], 'source': m['source'], 'passages': m['passages']} for m in members]
            out.append('')
    assert sum(len(members) for members in trace.values()) == len(rows), 'every row must be in exactly one line'
    suffix = f'-{name}' if name else ''
    (HERE / f'financial-table{suffix}.md').write_text('\n'.join(out))
    (HERE / f'table-rows{suffix}.json').write_text(json.dumps(trace, ensure_ascii=False, indent=1))
    merged = {line_id: members for line_id, members in trace.items() if len(members) > 1}
    print(f"{arm}: {len(rows)} rows in {len(trace)} lines, {len(ordered)} sections, {blocks} period blocks; rows with a fixed period "
          f"{sum(1 for r in rows if r['period_fixed'])}; lines holding more than one row {len(merged)} ({sum(len(m) for m in merged.values())} rows)")
    print('periods as stored -> key:')
    for stored, count in collections.Counter(normal(r['period']) for r in rows).most_common():
        print(f'   {count:2d}x {stored!r} -> {period_key(stored)[0]}')
    print('sources as stored -> group:')
    for stored, count in collections.Counter(str(r['source']) for r in rows).most_common():
        print(f'   {count:2d}x {stored!r} -> {source_group(stored, company)}')


if __name__ == '__main__':
    main()

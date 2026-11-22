"""The reading worksheet of the paid comparison (PAID-DESIGN.md §4, "The worksheet"; pinned before the launch).

  python3 worksheet.py build <out folder> <worksheet.json> <key.json>   # P rows (blind labels) and the H3, H4, H5 rows
  python3 worksheet.py gains <out folder> <read worksheet.json> <key.json> <gains.json>   # the gain review rows, after P is read

P rows (`part: P`): one per distinct v9/v14 answer pair per sequence on the fixed window 07-10..09-20 (each answer the last accepted
judgement on or before the date), keyed by both judgement ids, with the dates the pair covers, both answers' full forecast and reasons,
`contradictions.py`'s lead class (an order for the reading, never the count) and the reader's fields. Sequences carry shuffled labels
(S-A .. S-F); the key goes to <key.json>, kept outside the repository.

H rows carry the exact request each answer was given (its user text from the archive; the dependency block is part of it and is marked
by its own lines), the read judgements it was shown (judgement ids from the harness's snapshots), and the reader's fields:
  H4: every post-link v14 judgement of the linked sequences, with the CPU (v8) conclusion it received and the paired control's v14
      conclusion in force that day;
  H5: v9 and v14 at the seven fixed dates in all six sequences (the conclusion in force), for July's rule B;
  H3: every reader answer whose reference text differs from that reader's previous reference in the sequence, every reader answer whose
      reference or reasons name a market figure (consensus, guidance, analyst, "market expect"), and the H5 answers.
The H rows reveal the arm (a linked request carries the dependency block); only the P rows are blind.
"""
import datetime
import json
import random
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import contradictions                                                    # noqa: E402

SEQUENCES = ('linked-1', 'linked-2', 'linked-3', 'control-1', 'control-2', 'control-3')
SPAN = ('2026-07-10', '2026-09-20')
FIXED_DATES = ('2026-07-12', '2026-07-26', '2026-08-09', '2026-08-23', '2026-09-06', '2026-09-13', '2026-09-20')
SEGMENT, COMPANY, CPU = 'v9', 'v14', 'v8'
READERS = ('v9', 'v14', 'v16', 'v21')
ORDER = {'definite': 0, 'ambiguous': 1, 'overlap': 2, 'unparsed': 3, 'clear': 4}
MARKET = re.compile(r'consensus|guidance|analyst|market expect', re.I)
READER_P = {'segment low': None, 'segment high': None, 'segment excerpt': '', 'company low': None, 'company high': None,
            'company excerpt': '', 'class': None, 'note': ''}
READER_H = {'finding': None, 'error type': None, 'excerpt': '', 'source traced': '', 'note': ''}   # findings by part: verdict.H_FINDINGS


def window_dates():
    day, end = datetime.date.fromisoformat(SPAN[0]), datetime.date.fromisoformat(SPAN[1])
    while day <= end:
        yield day.isoformat()
        day += datetime.timedelta(days=1)


def connect(path):
    return sqlite3.connect(f'file:{path}?mode=ro', uri=True)


def judgements(conn, view):
    return conn.execute('select judgement_id, publication_day, implied_outcome, reasons, reference, call_id from judgements where view_id=? '
                        'order by judgement_id', (view,)).fetchall()


def in_force(rows, date):
    held = [j for j in rows if j[1] <= date]
    return held[-1] if held else None


def request_text(archive, call_id):
    row = archive.execute('select request_json from model_calls where call_id=?', (call_id,)).fetchone()
    return json.loads(row[0])['messages'][-1]['content'] if row else None


def snapshots(folder):
    path = Path(folder) / 'snapshots.jsonl'
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def shown(snaps, view, day):
    """The read judgements a reader was shown for its judgement on `day` (the last prompt built for it that day)."""
    built = [s for s in snaps if s['view'] == view and s['day'] == day]
    return {target: (state or {}).get('judgement_id') for target, state in (built[-1]['reads'] if built else {}).items()}


def p_rows(folder, label):
    conn = connect(Path(folder) / 'views.sqlite')
    segment_rows, company_rows = judgements(conn, SEGMENT), judgements(conn, COMPANY)
    rows = {}
    for date in window_dates():
        segment, company = in_force(segment_rows, date), in_force(company_rows, date)
        if not segment or not company:
            continue
        key = (segment[0], company[0])
        if key not in rows:
            rows[key] = {'part': 'P', 'sequence': label, 'segment judgement': segment[0], 'company judgement': company[0], 'dates': [],
                         'segment forecast': segment[2], 'segment reasons': segment[3], 'company forecast': company[2],
                         'company reasons': company[3],
                         'lead class': contradictions.classify(contradictions.annual(segment[2]), contradictions.annual(company[2])),
                         'reader': dict(READER_P)}
        rows[key]['dates'].append(date)
    return list(rows.values())


AMOUNT = re.compile(r'\$\s?(\d{1,4}(?:,\d{3})*(?:\.\d+)?)\s?(B\b|bn\b|billion\b|trillion\b)', re.I)


def amounts(text):
    out = set()
    for match in AMOUNT.finditer(text or ''):
        value = float(match.group(1).replace(',', '')) * (1000 if match.group(2).lower() == 'trillion' else 1)
        out.add(round(value, 1))
    return out


def sections(request):
    """The request split into the system's own figures (the dependency block's entries and the previous conclusion) and the rest (the
    evidence and the question): H3's structural rule looks for a reference amount found only in the former."""
    own, rest = [], []
    target = rest
    for line in (request or '').split('\n'):
        if line.startswith('[Previous conclusion') or line.startswith('- v') and '(open;' in line or line.startswith('- v') and '(closed;' in line:
            target = own
        elif line.startswith('[') or (line.startswith('- e') and target is own):
            target = rest
        target.append(line)
    return '\n'.join(own), '\n'.join(rest)


def structural_flag(view, reference, request):
    """H3's structural rule, the same in both arms: a reference amount found in the system's own figures (a read judgement's
    comparison point or forecast, or the previous conclusion) and nowhere in the evidence ('own figure as market'); or a part question
    (Data Center, CPU) naming a consensus whose amount appears in the evidence ('scope check')."""
    own, rest = sections(request)
    ref = amounts(reference)
    if ref & amounts(own) - amounts(rest):
        return 'own figure as market'
    if view in ('v9', 'v16') and re.search(r'consensus', reference or '', re.I) and ref & amounts(rest):
        return 'scope check'
    return None


def read_judgement_trace(conn, archive, read_ids):
    """For each read judgement a reader was shown: its id, comparison point, forecast and its own request (where its figures' dated
    sources are), so a linked figure can be followed to its outside statement."""
    out = {}
    for target, judgement_id in read_ids.items():
        if judgement_id is None:
            continue
        row = conn.execute('select reference, implied_outcome, call_id from judgements where judgement_id=?', (judgement_id,)).fetchone()
        if row:
            out[target] = {'judgement': judgement_id, 'reference': row[0], 'forecast': row[1], 'request': request_text(archive, row[2])}
    return out


def h_rows(out, name, label):
    folder = Path(out) / name
    conn, archive, snaps = connect(folder / 'views.sqlite'), connect(folder / 'archive.sqlite'), snapshots(folder)
    reader_days = json.loads((folder / 'summary.json').read_text())['reader days']
    pair = name.replace('linked', 'control') if name.startswith('linked') else name.replace('control', 'linked')
    other = connect(Path(out) / pair / 'views.sqlite')
    rows = []

    def row(part, view, judgement, **extra):
        read_ids = shown(snaps, view, judgement[1])
        counterpart = in_force(judgements(other, view), judgement[1])
        return {'part': part, 'sequence': name, 'view': view, 'judgement': judgement[0], 'day': judgement[1],
                'forecast': judgement[2], 'reasons': judgement[3], 'reference': judgement[4],
                'request': request_text(archive, judgement[5]), 'shown': read_ids, 'trace': read_judgement_trace(conn, archive, read_ids),
                'paired arm in force': {'sequence': pair, 'judgement': counterpart[0], 'forecast': counterpart[2],
                                        'reference': counterpart[4]} if counterpart else None,
                **extra, 'reader': dict(READER_H)}
    if name.startswith('linked'):
        for j in judgements(conn, COMPANY):
            if j[1] >= reader_days[COMPANY]:
                rows.append(row('H4', COMPANY, j, cpu_shown=shown(snaps, COMPANY, j[1]).get(CPU)))
    for view in (SEGMENT, COMPANY):
        for date in FIXED_DATES:
            j = in_force(judgements(conn, view), date)
            if j:
                rows.append(row('H5', view, j, fixed_date=date))
    for view in READERS:
        for j in judgements(conn, view):
            if j[1] < reader_days.get(view, '9999'):
                continue
            flag = structural_flag(view, j[4], request_text(archive, j[5]))
            fixed = j[1] in FIXED_DATES
            if flag or fixed:
                rows.append(row('H3', view, j, structural_flag=flag, fixed_date=j[1] if fixed else None))
        for date in FIXED_DATES:                     # the conclusion in force on each fixed date, when it was judged earlier
            j = in_force(judgements(conn, view), date)
            if j and j[1] >= reader_days.get(view, '9999') and j[1] != date and not any(r['part'] == 'H3' and r['judgement'] == j[0] for r in rows):
                rows.append(row('H3', view, j, structural_flag=structural_flag(view, j[4], request_text(archive, j[5])), fixed_date=date))
    return rows


def build(out, target, key_path, seed=None):
    """Two packets: <target> with `.p.json` (the blind P rows only, shuffled labels) and `.h.json` (the H rows, which reveal the arm);
    the key goes to <key_path>, outside the repository."""
    labels = [f'S-{c}' for c in 'ABCDEF']
    random.Random(seed).shuffle(labels) if seed is not None else random.SystemRandom().shuffle(labels)
    key = dict(zip(labels, SEQUENCES))
    p_packet, h_packet = [], []
    for label, name in key.items():
        p_packet += p_rows(Path(out) / name, label)
        h_packet += h_rows(out, name, label)
    random.Random(seed).shuffle(p_packet) if seed is not None else random.SystemRandom().shuffle(p_packet)
    p_packet.sort(key=lambda r: ORDER.get(r['lead class'], 9))
    h_packet.sort(key=lambda r: (r['part'], r['sequence'], r['day']))
    Path(f'{target}.p.json').write_text(json.dumps(p_packet, indent=1, ensure_ascii=False))
    Path(f'{target}.h.json').write_text(json.dumps(h_packet, indent=1, ensure_ascii=False))
    Path(key_path).parent.mkdir(parents=True, exist_ok=True)
    Path(key_path).write_text(json.dumps(key, indent=1))
    summary = {'P': len(p_packet), **{part: sum(1 for r in h_packet if r['part'] == part) for part in ('H3', 'H4', 'H5')},
               'H3 structural flags': sum(1 for r in h_packet if r['part'] == 'H3' and r.get('structural_flag')),
               'P dates per label': {label: sum(len(r['dates']) for r in p_packet if r['sequence'] == label) for label in key}}
    print(json.dumps(summary))
    return p_packet, h_packet


def build_pilot(out, target, key_path, seed=None):
    """The pilot's packets (D708): the blind P rows of linked-1 and control-1 under two shuffled labels, and the H4 rows of linked-1 (every
    post-link v14 answer with the CPU conclusion it saw and control-1's v14 in force); the key to <key_path>."""
    labels = ['S-A', 'S-B']
    random.Random(seed).shuffle(labels) if seed is not None else random.SystemRandom().shuffle(labels)
    key = dict(zip(labels, ('linked-1', 'control-1')))
    p_packet = [r for label, name in key.items() for r in p_rows(Path(out) / name, label)]
    random.Random(seed).shuffle(p_packet) if seed is not None else random.SystemRandom().shuffle(p_packet)
    p_packet.sort(key=lambda r: ORDER.get(r['lead class'], 9))
    h4_packet = [r for r in h_rows(out, 'linked-1', None) if r['part'] == 'H4']
    Path(f'{target}.p.json').write_text(json.dumps(p_packet, indent=1, ensure_ascii=False))
    Path(f'{target}.h4.json').write_text(json.dumps(h4_packet, indent=1, ensure_ascii=False))
    Path(key_path).parent.mkdir(parents=True, exist_ok=True)
    Path(key_path).write_text(json.dumps(key, indent=1))
    print(json.dumps({'P': len(p_packet), 'H4': len(h4_packet)}))
    return p_packet, h4_packet


def gains(out, read_sheet, key_path, target):
    """The gain review rows: for every date a linked sequence's pair is read overlap or clear while its control's is read definite, the
    two linked answers in force (v9's and v14's), deduplicated by judgement id, each with its exact request, for rule B and H4."""
    key = json.loads(Path(key_path).read_text())
    sheet = json.loads(Path(read_sheet).read_text())
    classes = {}
    for row in sheet:
        if row['part'] == 'P':
            for date in row['dates']:
                classes[(key[row['sequence']], date)] = (row['reader']['class'], row['segment judgement'], row['company judgement'])
    rows = []
    for n in [p for p in ('1', '2', '3') if f'linked-{p}' in key.values()]:
        archive = connect(Path(out) / f'linked-{n}' / 'archive.sqlite')
        conn = connect(Path(out) / f'linked-{n}' / 'views.sqlite')
        gain_dates = {}
        for date in window_dates():
            linked, control = classes.get((f'linked-{n}', date)), classes.get((f'control-{n}', date))
            if linked and control and linked[0] in ('overlap', 'clear') and control[0] == 'definite':
                for judgement_id in linked[1:]:
                    gain_dates.setdefault(judgement_id, []).append(date)
        for judgement_id, dates in sorted(gain_dates.items()):
            j = conn.execute('select judgement_id, view_id, publication_day, implied_outcome, reasons, reference, call_id from judgements '
                             'where judgement_id=?', (judgement_id,)).fetchone()
            rows.append({'part': 'gain', 'pair': n, 'judgement': j[0], 'view': j[1], 'day': j[2],
                         'forecast': j[3], 'reasons': j[4], 'reference': j[5], 'request': request_text(archive, j[6]), 'gain dates': dates,
                         'reader': {'rule B material failure': None, 'reliance by date': {}, 'rule B inputs': [], 'rule B reasoning': '',
                                    'cpu increment': None, 'increment removed': None,
                                    'corrected low': None, 'corrected high': None, 'note': ''}})
    Path(target).write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    print(json.dumps({'gain review rows': len(rows)}))
    return rows


if __name__ == '__main__':
    if sys.argv[1] == 'build':
        build(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'build-pilot':
        build_pilot(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'gains':
        gains(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        raise SystemExit('build or gains')

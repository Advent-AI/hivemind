"""The coverage-start reading (D363, D364): at coverage start, after the seed questions are written and before the first day's items, each open
question reads the company's latest earnings report once, item by item, for the figure its quantity stands at in the report's most recent period;
the figures code keeps become evidence linked to the questions that read them, and the first day's judging round judges those questions. The
daily path is unchanged. What is built is what was validated (docs/research/2026-11-04-filing-end-to-end/baseline-design.md rounds 13-26; the
design with its four tables: production-design.md there).

Code owns identity only: which items are the latest report (`report_items`), whether a figure's quote is the report's own text and prints the figure
written as the value (`check_figures`), and one record per item and quote linked to every question that kept it (D364). Which question a figure
belongs to and which column of a table it is from stay the reading's.
"""
import json
import re
import time

from . import config, extraction, model, placement
from .extraction import normalise
from .views import store
from .views.writing import _next_id

SUPPORTED_VERSIONS = ('baseline-v3',)       # the validated third version (rounds 14-16, 24-26); the code builds no other
SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['figures'], 'properties': {'figures': {'type': 'array', 'items': {
    'type': 'object', 'additionalProperties': False, 'required': ['quote', 'value', 'unit', 'period', 'basis', 'one_line'],
    'properties': {k: {'type': 'string'} for k in ('quote', 'value', 'unit', 'period', 'basis', 'one_line')}}}}}
SCHEMA_NAME = 'extraction'                  # the name the validated requests carry (their bytes are compared at $0)
STEP = 'baseline'
SCALE = re.compile(r'%|\d\s*(?:k|m|b|t|bn|mn|mm|bln|mln|bil)\b|\b(?:thousand|million|billion|trillion)s?\b', re.I)


class BaselineRefused(RuntimeError):
    pass

NUMBER = re.compile(r'(?<![\w.])\d[\d,]*(?:\.\d+)?(?!\w)')     # a number standing alone, never digits inside a name (Q1, FY27, A5X)
CELL = re.compile(r'\s*(?:\$\s*)?\(?\d[\d,]*(?:\.\d+)?\)?(?:\s*%)?(?:\s*pts)?|\s*[—–-](?=\s|$)')   # one table cell as a page prints it
FOOTNOTE = r'(?:\s*\*+|\s*\([A-Z]\))?'
MIN_QUOTE = 8                                                   # the extraction's shortest quote


def comparable(text):
    """The form in which a quote is compared with the report: the extraction's normalise, with a currency sign and a percent sign joined to their
    number (a flattened table prints each cell, and each sign, on its own line)."""
    text = normalise(text)
    return re.sub(r'(?<=\d) %', '%', re.sub(r'\$ (?=\d)', '$', text))


def numbers(text):
    """The numbers of a text as printed, without sign, parentheses or thousands separators."""
    return [float(n.replace(',', '')) for n in NUMBER.findall(text)]


def row_span(quote, value, text):
    """For a table-row quote the plain check misses: the exact span of the report's row from the quote's label to its figure, when the label is
    the report's (a footnote mark left off is allowed) and the quote's figures are that row's cells in order (cells left out between the label and
    the figure are allowed). None for a quote that is not a label followed by figures only, or when no row of the report holds them."""
    split = re.match(r'(?s)\s*(?P<label>.*?[A-Za-z].*?)(?P<tail>(?:\s*(?:\$\s*)?\(?\d[\d,]*(?:\.\d+)?\)?(?:\s*%)?(?:\s*pts)?|\s*[—–-])+)\s*$', quote)
    if not split or re.search(r'[A-Za-z]', split['tail'].replace('pts', '')):
        return None
    label = re.sub(r'(?:\s*\*+|\s*\([A-Z]\))\s*$', '', split['label']).strip()
    wanted, value_numbers = numbers(split['tail']), numbers(value)
    if len(label) < 3 or len(value_numbers) != 1 or value_numbers[0] not in wanted:
        return None
    pattern = re.compile(r'(?<![\w-])' + r'\s+'.join(re.escape(word) for word in label.split()) + FOOTNOTE, re.I)
    for hit in pattern.finditer(text):
        cells, at = [], hit.end()
        while True:
            cell = CELL.match(text, at)
            if not cell or cell.end() == at:
                break
            cells.append((numbers(cell.group()), cell.end()))
            at = cell.end()
        aligned, end = 0, None
        for found, cell_end in cells:                            # the quote's figures as a subsequence of the row's cells, in order
            if aligned < len(wanted) and found and found[0] == wanted[aligned]:
                if wanted[aligned] == value_numbers[0]:
                    end = cell_end
                aligned += 1
        if aligned == len(wanted) and end is not None:
            return text[hit.start():end]
    return None


def check_figures(figures, text):
    """Each figure the reading wrote, with the code's identity checks; a table-row quote the plain check misses is replaced by the report's exact
    row span (`row_span`) and keeps the model's text as `quote_as_written`."""
    body = comparable(text)
    out = []
    for f in figures:
        quote, repaired = f['quote'], False
        if not (len(comparable(quote)) >= MIN_QUOTE and comparable(quote) in body):
            span = row_span(quote, f['value'], text)
            if span is not None:
                quote, repaired = span, True
        in_report = len(comparable(quote)) >= MIN_QUOTE and comparable(quote) in body
        labelled = bool(re.search(r'[a-z]{3,}', comparable(quote)))
        value = numbers(f['value'])
        value_in_quote = len(value) == 1 and value[0] in numbers(quote)
        checked = dict(f, quote=quote, in_report=in_report, labelled=labelled, value_in_quote=value_in_quote,
                       kept=in_report and labelled and value_in_quote)
        if repaired:
            checked['quote_as_written'] = f['quote']
        out.append(checked)
    return out


def require_supported(prompt_version):
    if prompt_version not in SUPPORTED_VERSIONS:
        raise config.ConfigError(f'baseline {prompt_version!r} is not built; this code builds only {", ".join(SUPPORTED_VERSIONS)} (D364)')


def prompt(prompt_version):
    """(system, task) of the reading, from prompts/<version>.json."""
    require_supported(prompt_version)
    with open(config.prompt_path(prompt_version + '.json'), encoding='utf-8') as handle:
        texts = json.load(handle)
    return texts['system'], texts['task']


def report_items(items_db, ticker, coverage_start):
    """The company's latest earnings report before coverage start: items of category T1 whose object identifiers carry its ticker, of the latest such
    publication day; of that day the filed ones (channel EDGAR) when there are any, since the company's newsroom and investor-site copies of the same
    documents are not marked as copies; else all of them. Each with its page text (the tables the cleaned text drops)."""
    columns = {r[1] for r in items_db.execute('pragma table_info(items)')}
    if 'text_page' not in columns:
        raise BaselineRefused('the items database has no page text (text_page); the coverage-start reading needs the report\'s tables')
    rows = [dict(r) for r in items_db.execute("select input_id, publication_day, publisher, title, channel, object_identifiers, text_page from items "
                                             "where category='T1' and publication_day < ? order by publication_day, input_id", (coverage_start,))]
    rows = [r for r in rows if any(o.get('kind') == 'ticker' and o.get('value') == ticker for o in json.loads(r['object_identifiers'] or '[]'))]
    if not rows:
        return []
    day = max(r['publication_day'] for r in rows)
    of_day = [r for r in rows if r['publication_day'] == day]
    chosen = [r for r in of_day if r['channel'] == 'EDGAR'] or of_day
    empty = [r['input_id'] for r in chosen if not (r['text_page'] or '').strip()]
    if empty:
        raise BaselineRefused(f'no page text for {empty}; the coverage-start reading needs the report\'s tables')
    return chosen


def user_message(lines, item, task):
    return (f'[Question]\n' + '\n'.join(lines) + f'\n\n[Report] id {item["input_id"]}, published {item["publication_day"]} by {item["publisher"]}: '
            f'{item["title"]}\n{item["text_page"]}\n\n{task}')


def one_line_of(figure):
    """The model's one-line, followed by the unit it read when the value carries no scale or percent sign of its own (a table cell such as "(1,757)"
    or "$53,783": the row's quote carries no scale, and the one-line need not)."""
    return figure['one_line'] if SCALE.search(figure['value']) else f'{figure["one_line"]} (unit: {figure["unit"]})'


def step_id(ticker, report_day):
    return f'baseline:{ticker}:{report_day}'


def guard(conn, ticker, coverage_start):
    """'run' on a ledger at coverage start, 'skip' when the step ran (its day completed, or the run starts on that day to complete it); refuses a
    ledger past coverage start without the step, and a run that would start after an unfinished coverage-start day."""
    row = conn.execute("select publication_day from processing_steps where step=? and input_id like ? order by id limit 1",
                       (STEP, f'baseline:{ticker}:%')).fetchone()
    if row is not None:
        done = conn.execute('select 1 from days_completed where day=? limit 1', (row['publication_day'],)).fetchone()
        if not done and coverage_start != row['publication_day']:
            raise BaselineRefused(f'the coverage-start day {row["publication_day"]} is not finished; run from it so its round judges the starting figures')
        return 'skip'
    progressed = conn.execute('select 1 from processing_steps where sequence_no > 0 limit 1').fetchone() or \
        conn.execute('select 1 from days_completed limit 1').fetchone()
    if progressed:
        raise BaselineRefused('coverage start has passed in this ledger: the coverage-start reading runs only on a ledger that has processed nothing yet')
    return 'run'


def run(conn, items_db, archive, cfg, *, ticker, coverage_start, transport=None, log=print):
    """Reads, checks and writes the starting figures; returns the step's record (or None when the configuration has no baseline setting or the step
    ran before). All model calls first (archived, so a rerun after a failure reuses them), then every record, link and the step row in one commit."""
    setting = getattr(cfg, 'baseline', None)
    if setting is None:
        return None
    system, task = prompt(setting.prompt_version)
    if guard(conn, ticker, coverage_start) == 'skip':
        log(f'--- coverage-start reading of {ticker}: done before, skipped')
        return None
    items = report_items(items_db, ticker, coverage_start)
    seq = store.next_sequence(conn)
    at = time.strftime('%Y-%m-%dT%H:%M:%S')
    if not items:
        record = {'changed': [], 'report': [], 'kept': 0, 'refused': [], 'empty': [], 'note': f'no earnings report of {ticker} before {coverage_start}'}
        store.mark_step(conn, step_id(ticker, 'none'), seq, STEP, 'ok', json.dumps(record), coverage_start, at)
        conn.commit()
        return record
    shown = extraction.shown_views(conn, cfg, {'publication_day': items[0]['publication_day'], 'category': 'T1', 'object_identifiers': [{'value': ticker}]}, [ticker])
    readings = []
    for view in sorted(shown, key=lambda v: int(v['view_id'][1:]) if v['view_id'][1:].isdigit() else 0):
        lines = placement.question_lines([view])
        for item in items:
            answer = model.call(archive, cfg, setting, system, user_message(lines, item, task), SCHEMA, SCHEMA_NAME, STEP, transport=transport)
            readings.append((view['view_id'], item, check_figures(answer.data.get('figures', []), item['text_page'])))
    records, changed, refused, empty, kept = {}, [], [], [], 0
    for view_id, item, figures in readings:
        if not figures:
            empty.append([view_id, item['input_id']])
        for f in figures:
            if not f['kept']:
                refused.append({'view_id': view_id, 'input_id': item['input_id'], 'quote': f['quote'][:300], 'value': f['value'],
                                'reason': 'quote not in the report' if not f['in_report'] else ('no label' if not f['labelled'] else 'value not printed in the quote')})
                continue
            key = (item['input_id'], comparable(f['quote']))
            if key not in records:
                evidence_id = _next_id(conn, 'evidence', 'evidence_id', 'e')
                store.add_evidence(conn, evidence_id=evidence_id, quote=f['quote'], one_line=one_line_of(f), speaker=item['publisher'],
                                   original_who=item['publisher'], original_day=item['publication_day'], tier='fact', event_time='', seq=seq,
                                   input_id=item['input_id'])
                store.add_source(conn, evidence_id, item['input_id'], 'T1', item['publication_day'], '', seq)
                records[key] = evidence_id
            if store.link(conn, records[key], view_id, seq) and view_id not in changed:
                changed.append(view_id)
            kept += 1
    record = {'changed': changed, 'report': [item['input_id'] for item in items], 'kept': kept, 'records': len(records), 'refused': refused, 'empty': empty}
    store.mark_step(conn, step_id(ticker, items[0]['publication_day']), seq, STEP, 'ok', json.dumps(record, ensure_ascii=False), coverage_start, at)
    conn.commit()
    log(f'--- coverage-start reading of {ticker}: {len(items)} report items, {len(readings)} readings, {len(records)} records linked to {changed}, '
        f'{len(refused)} figures refused')
    return record

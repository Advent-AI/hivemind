"""Isolated, ordered Step 1 runner. The caller supplies the model transport."""
import copy
import datetime
import hashlib
import json
import os
import sqlite3
from pathlib import Path
from types import SimpleNamespace

from hivemind import config, extraction, model, testdb
from live import LiveTransport, SUPPORTED
import quote_lookup


class ContractError(ValueError):
    pass


def preserves_quote(quote, recovered):
    """Require the normalized quoted text to occur contiguously in the source span."""
    original = extraction.normalise(quote)
    return bool(original) and original in extraction.normalise(recovered)


class RecordedTransport:
    """Offline-only responses for developing and inspecting the handoff."""
    def __init__(self, responses):
        self.responses = iter(responses)

    def __call__(self, provider, request):
        return next(self.responses)


def prd_block(prd_path, heading, language):
    """One fenced block of the architecture PRD, under its heading. The block keeps its final newline, so a request built from the PRD
    is byte for byte the frozen configuration's files (D387)."""
    text = Path(prd_path).read_text(encoding='utf-8')
    start = text.index('```' + language + '\n', text.index('### ' + heading + '\n'))
    start = text.index('\n', start) + 1
    return text[start:text.index('\n```', start) + 1]


def draft(prd_path):
    """Read the one authoritative system prompt and schema from the architecture PRD (§12)."""
    return prd_block(prd_path, 'System prompt', 'text'), json.loads(prd_block(prd_path, 'Structured-output schema', 'json'))


def closing_check(prd_path):
    """Read the closing check that ends the user message from the architecture PRD (§12)."""
    return prd_block(prd_path, 'Closing check', 'text')


def selected_items(source_path, manifest):
    """Freeze the explicit article selection in caller-supplied order."""
    ids = manifest['item_ids']
    if not ids or len(ids) != len(set(ids)):
        raise ContractError('item IDs must be nonempty and unique')
    entity = manifest['entity']
    start = datetime.date.fromisoformat(manifest['from_day'])
    end = datetime.date.fromisoformat(manifest['until_day'])
    if not entity or start > end:
        raise ContractError('invalid entity or date window')
    conn = sqlite3.connect(Path(source_path).resolve().as_uri() + '?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute('begin')
        items = []
        for item_id in ids:
            row = conn.execute('select * from items where input_id = ?', (item_id,)).fetchone()
            if row is None:
                raise ContractError(f'unknown item: {item_id}')
            item = testdb.item_of(row)
            day = datetime.date.fromisoformat(item['publication_day'])
            tags = [x['value'] for x in item['object_identifiers'] if x.get('kind') == 'ticker']
            if (not (start <= day <= end) or entity not in tags or not item.get('text')
                    or item.get('feed') != 1 or item.get('copy_of') or item.get('supersedes')):
                raise ContractError(f'item outside selection or missing text: {item_id}')
            items.append(item)
        return items
    finally:
        conn.close()


CONDITION_KINDS = ('actual', 'guidance', 'estimate')


def figure_in_passages(value, passages):
    """A condition's figure is quoted when it occurs, whitespace normalised, in one verified passage, with numeric boundaries: not
    preceded by a digit or by a decimal point or comma that follows a digit, and not followed by a digit or by a decimal point or comma
    that precedes a digit. It proves the figure is quoted, not that it belongs to the stated measure (that is a reader's check)."""
    figure = ' '.join(value.split())
    if not figure:
        return False
    for passage in passages:
        if passage is None:
            continue
        text = ' '.join(passage.split())
        start = text.find(figure)
        while start != -1:
            end = start + len(figure)
            before, before2 = text[start - 1:start], text[start - 2:start - 1]
            after, after2 = text[end:end + 1], text[end + 1:end + 2]
            left = not (before.isdigit() or (before in ('.', ',') and before and before2.isdigit()))
            right = not (after.isdigit() or (after in ('.', ',') and after and after2.isdigit()))
            if left and right:
                return True
            start = text.find(figure, start + 1)
    return False


def validate(answer, schema, item, shown):
    errors = model.check_schema(answer, schema)
    if errors:
        raise ContractError('; '.join(errors))
    thesis_ids = [x['local_id'] for x in answer['new_theses']]
    evidence_ids = [x['local_id'] for x in answer['evidence']]
    for name, ids in [('thesis', thesis_ids), ('evidence', evidence_ids)]:
        if any(not x.strip() for x in ids) or len(ids) != len(set(ids)):
            raise ContractError(f'{name} local IDs must be nonempty and unique')
    for thesis in answer['new_theses']:
        if not thesis['description'].strip() or not thesis['outcome'].strip():
            raise ContractError('new thesis requires a question and outcome')
    existing = {x['id'] for x in shown}
    linked_new = set()
    unresolved = []
    lookup_index = None
    index_failure = None
    lookup_errors = []
    interpreted = copy.deepcopy(answer)
    for ev in interpreted['evidence']:
        if not ev['summary'].strip():
            raise ContractError('evidence requires a summary')
        verified = []
        repaired = []
        for passage_number, quote in enumerate(ev['source_passages'], 1):
            if not quote.strip():
                raise ContractError('empty source passage')
            exact = quote in item['text']
            source = quote if exact else extraction.repair_quote(quote, item['text'])
            if not exact and (not source or source not in item['text'] or not preserves_quote(quote, source)):
                if lookup_index is None and index_failure is None:
                    try:
                        lookup_index = quote_lookup.build_index(item['text'])
                    except Exception as error:
                        index_failure = (type(error).__name__, str(error))
                failure = index_failure
                if failure is None:
                    try:
                        located = quote_lookup.find_quote(quote, item['text'], lookup_index)
                        if located and preserves_quote(quote, located):
                            source = located
                    except Exception as error:
                        failure = (type(error).__name__, str(error))
                if failure is not None:
                    lookup_errors.append({'evidence_id': ev['local_id'], 'passage_number': passage_number,
                                          'error_type': failure[0], 'message': failure[1]})
            if (not source or source not in item['text'] or not preserves_quote(quote, source)
                    or (item.get('source_preparation') and source not in (item.get('text_page') or ''))):
                verified.append(None)
                repaired.append(False)
                continue
            verified.append(source)
            repaired.append(source != quote)
        ev['verified_source_passages'] = verified
        ev['source_passages_repaired'] = repaired
        if ev['statement_date'] is not None:
            try:
                datetime.date.fromisoformat(ev['statement_date'])
            except ValueError as error:
                raise ContractError('invalid original statement date') from error
        for link in ev['links']:
            if not link['relevance'].strip():
                raise ContractError('evidence link requires relevance')
            target = link['target_id']
            if link['target_type'] == 'existing' and target not in existing:
                unresolved.append({'evidence_id': ev['local_id'], 'target_type': 'existing', 'target_id': target})
            if link['target_type'] == 'new':
                if target not in thesis_ids:
                    unresolved.append({'evidence_id': ev['local_id'], 'target_type': 'new', 'target_id': target})
                else:
                    linked_new.add(target)
    interpreted['unresolved_links'] = unresolved
    # A statement of the company's own financial performance lists its `figures` (STEP1-CONDITIONS-DESIGN.md §16). Each figure's value
    # must be quoted in one of the item's verified passages; a figure that fails is removed and the reason recorded.
    figure_issues = []
    for ev in interpreted['evidence']:
        valid = []
        for figure in ev.get('figures') or []:
            reason = None
            if figure.get('kind') not in CONDITION_KINDS or not str(figure.get('measure') or '').strip():
                reason = 'figure shape'
            elif not figure_in_passages(str(figure.get('value') or ''), ev['verified_source_passages']):
                reason = 'figure value not quoted in a verified passage'
            if reason:
                figure_issues.append({'evidence_id': ev['local_id'], 'reason': reason, 'figure': figure})
            else:
                valid.append(figure)
        if 'figures' in ev:
            ev['figures'] = valid
    interpreted['figure_issues'] = figure_issues
    # Every returned evidence item is kept (Alex, 2026-11-08, the second amendment of D209): an item no thesis takes is stored unlinked
    # in the company's record and linked when a covering thesis opens (Step 3). What the closing check rejects is never returned.
    interpreted['unfiled_evidence'] = []
    interpreted['unlinked_new_thesis_ids'] = [x for x in thesis_ids if x not in linked_new]
    if lookup_errors:
        interpreted['quote_lookup_errors'] = lookup_errors
    return interpreted


class FormatFailure(ContractError):
    """A live answer failed the format check on its send and on one identical retry."""


def run(source_path, output_path, manifest, initial_theses, settings, transport, prd_path, texts=None, schema=None):
    """Run once. A live answer that fails the format check (not JSON, or not the schema) is sent once more unchanged; if the retry
    also fails, the item is marked failed with both reasons and the run continues, ending 'complete_with_failures' with the failed
    items listed (Alex, 2026-11-08). Any other failure stops the run. Every item retains its request and response. `texts`, when given, is a candidate's
    (system prompt, closing check) used in place of the PRD's; either way the closing check ends the user message, after the item, so
    the model applies it last (AGENTS §6). `schema`, when given, is a candidate's response schema in place of the PRD's."""
    if type(transport) not in (RecordedTransport, LiveTransport):
        raise ContractError('unsupported transport')
    cap = settings['max_output_tokens']
    if isinstance(cap, bool) or not isinstance(cap, int) or not 0 < cap <= 128000:
        raise ContractError('max_output_tokens must be a positive integer within the model limit')
    limit = manifest['item_limit']
    if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
        raise ContractError('item_limit must be a positive integer')
    if type(transport) is LiveTransport and (settings['provider'], settings['model']) not in SUPPORTED:
        raise ContractError('live transport supports OpenAI gpt-6-luna and DeepSeek flash or v4-pro only')
    if type(transport) is LiveTransport:
        transport.reasoning_effort = settings['reasoning_effort']
    prompt, prd_schema = draft(prd_path)
    schema = schema or prd_schema
    closing = closing_check(prd_path)
    if texts is not None:
        prompt, closing = texts
        if not prompt.strip() or not closing.strip():
            raise ContractError('a candidate needs a system prompt and a closing check')
    items = selected_items(source_path, manifest)
    entity = manifest['entity']
    ids = [t['id'] for t in initial_theses]
    if len(ids) != len(set(ids)) or any(not isinstance(x, str) or not x.strip() for x in ids):
        raise ContractError('initial thesis IDs must be unique and nonempty')
    for t in initial_theses:
        if (t['entity'] != entity or not isinstance(t['description'], str) or not t['description'].strip()
                or not isinstance(t['outcome'], str) or not t['outcome'].strip() or 'period' not in t):
            raise ContractError('initial thesis requires entity, question, outcome and period')
    # The caller chooses limits for an exploratory run; never guess a paid-run budget.
    if len(items) > manifest['item_limit']:
        raise ContractError('item limit exceeded')
    setting = config.Setting('clean-step1', settings['model'], 'clean-step1', settings['reasoning_effort'], settings['max_output_tokens'])
    fd = os.open(output_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    conn = sqlite3.connect(output_path)
    archive = None
    try:
        conn.executescript('''
          create table run (manifest text not null, settings text not null, source_items text not null, initial_theses text not null);
          create table trace (sequence integer primary key, input_id text not null, before_state text not null,
            request text not null, raw_response text, result text, after_state text, status text not null, error text, reserved_usd real,
            retry_reason text);
        ''')
        dump = lambda obj: json.dumps(obj, ensure_ascii=False)
        conn.execute('insert into run values (?, ?, ?, ?)', (dump(manifest), dump(settings), dump(items), dump(initial_theses)))
        conn.commit()
        if type(transport) is LiveTransport:
            archive = model.Archive(str(output_path))
            checksum = hashlib.sha256(dump({'settings': settings, 'prompt': prompt, 'closing': closing, 'schema': schema}).encode()).hexdigest()
            call_config = SimpleNamespace(provider=settings['provider'], version='clean-step1', checksum=checksum)
        theses = copy.deepcopy(initial_theses)
        outcome = {'status': 'complete', 'error': None}
        failed_items = []
        for sequence, item in enumerate(items, 1):
            shown = [{k: t[k] for k in ('id', 'description', 'outcome', 'period')} for t in theses]
            tags = [x['value'] for x in item['object_identifiers'] if x.get('kind') == 'ticker']
            payload = {'current_entity': entity, 'company_tags': tags, 'open_theses': shown, 'source_item': {
                'id': item['input_id'], 'publisher': item['publisher'], 'publication_date': item['publication_day'],
                'published_at': item['published_at'], 'publisher_type': item.get('publisher_type'),
                'authors': item.get('authors'), 'category': item.get('category'),
                'source_uri': item['source_uri'], 'title': item['title'], 'text': item['text']}}
            user = dump(payload) + (f'\n\n{closing}' if closing else '')
            request = model.build_request(setting, prompt, user, schema, 'clean_step1', settings['provider'])
            conn.execute('insert into trace (sequence,input_id,before_state,request,status) values (?,?,?,?,?)',
                         (sequence, item['input_id'], dump(theses), json.dumps(request), 'in_flight'))
            conn.commit()
            if type(transport) is LiveTransport:
                def record_reservation(amount):
                    conn.execute('update trace set reserved_usd=? where sequence=?', (amount, sequence))
                    conn.commit()
                transport.on_reserve = record_reservation
            response = None
            notes = []          # this step's retries, network and format, in order: written to retry_reason, none overwriting another
            try:
                if type(transport) is LiveTransport:
                    def capture(provider, built_request):
                        nonlocal response
                        try:
                            response = transport(provider, built_request)
                        except model.TransportError as error:
                            if hasattr(error, 'response_body'):
                                response = {'http_status': error.http_status, 'raw_body': error.response_body}
                                if hasattr(error, 'response_body_base64'):
                                    response['raw_body_base64'] = error.response_body_base64
                            raise
                        finally:
                            notes.extend(f'network retry, {note}' for note in transport.network_errors)
                            if notes:
                                with conn:
                                    conn.execute('update trace set retry_reason=? where sequence=?', ('; '.join(notes), sequence))
                        if transport.last_sent is not built_request:   # a provider adaptation changed the bytes: keep what was sent
                            response = dict(response, sent_request=transport.last_sent)
                        conn.execute('update trace set raw_response=? where sequence=?', (dump(response), sequence))
                        conn.commit()
                        choice = response['choices'][0]
                        if choice['message'].get('refusal'):
                            raise ContractError('provider refused')
                        if choice.get('finish_reason') == 'length':   # a cut answer is not JSON: the format rule retries it once
                            raise model.SchemaError('incomplete output: the answer reached the output limit')
                        if choice.get('finish_reason') != 'stop':
                            raise ContractError('provider refused or returned incomplete output')
                        return response
                    try:
                        recorded = model.call(archive, call_config, setting, prompt, user, schema,
                                              'clean_step1', 'clean_step1', transport=capture)
                    except model.SchemaError as first:
                        first_reason = f'SchemaError: {first}'
                        notes.append(first_reason)
                        with conn:
                            conn.execute('update trace set retry_reason=? where sequence=?', ('; '.join(notes), sequence))
                        try:   # the failed answer is archived under its own key, so the identical request is sent again
                            recorded = model.call(archive, call_config, setting, prompt, user, schema,
                                                  'clean_step1', 'clean_step1', transport=capture)
                        except model.SchemaError as second:
                            raise FormatFailure(f'{first_reason}; retry: SchemaError: {second}') from second
                    if recorded.cached:
                        raise ContractError('unexpected cached answer in fresh run')
                    answer = recorded.data
                else:
                    response = transport(settings['provider'], request)
                    answer = json.loads(response['choices'][0]['message']['content'])
                result = validate(answer, schema, item, shown)
                updated = copy.deepcopy(theses)
                used = {t['id'] for t in updated}
                allocated = {}
                counter = 1
                for proposed in answer['new_theses']:
                    if proposed['local_id'] in result['unlinked_new_thesis_ids']:
                        continue
                    while f'clean-{counter}' in used:
                        counter += 1
                    thesis_id = f'clean-{counter}'
                    used.add(thesis_id)
                    allocated[proposed['local_id']] = thesis_id
                    updated.append({'id': thesis_id, 'entity': entity, 'description': proposed['description'],
                                    'outcome': proposed['outcome'], 'period': proposed['period']})
                result['new_thesis_ids'] = allocated
                with conn:
                    conn.execute('update trace set raw_response=?,result=?,after_state=?,status=? where sequence=?',
                                 (dump(response), dump(result), dump(updated), 'complete', sequence))
                theses = updated
            except Exception as error:
                reason = f'{type(error).__name__}: {error}'
                with conn:
                    conn.execute('update trace set raw_response=?,after_state=?,status=?,error=? where sequence=?',
                                 (dump(response) if response is not None else None, dump(theses), 'failed',
                                  reason, sequence))
                if isinstance(error, FormatFailure):
                    failed_items.append({'input_id': item['input_id'], 'error': reason})
                    continue
                outcome = {'status': 'failed', 'input_id': item['input_id'], 'error': reason}
                break
        if failed_items:
            outcome['failed_items'] = failed_items
            if outcome['status'] == 'complete':
                outcome['status'] = 'complete_with_failures'
        if type(transport) is LiveTransport:
            outcome['reserved_usd'] = transport.reserved
            outcome['calls'] = transport.calls
        return outcome
    finally:
        if archive is not None:
            archive.conn.close()
        conn.close()

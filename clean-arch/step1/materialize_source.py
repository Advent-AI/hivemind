#!/usr/bin/env python3
"""Create a separate exploratory source database from recorded source-role answers."""
import argparse
import hashlib
import json
import os
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import model

ROLES = ('article_line_ids', 'byline_or_source_line_ids', 'caption_or_credit_line_ids',
         'generated_summary_line_ids', 'uncertain_line_ids')
INCLUDED = ('article_line_ids', 'byline_or_source_line_ids', 'caption_or_credit_line_ids', 'uncertain_line_ids')


def _read(path):
    data = Path(path).read_bytes()
    return json.loads(data), hashlib.sha256(data).hexdigest()


def select_source(item, packet, record, expected, packet_hash, record_hash):
    """Reconstruct selected original lines and retain the decisions that selected them."""
    archived = packet['source_record']
    for key in ('input_id', 'title', 'publisher', 'publisher_type', 'source_uri', 'published_at',
                'publication_day', 'authors', 'category', 'feed', 'copy_of', 'supersedes',
                'content_sha256', 'text_page'):
        if archived.get(key) != item.get(key):
            raise ValueError(f'archived source differs for {key}: {item["input_id"]}')
    identifiers = item.get('object_identifiers')
    if isinstance(identifiers, str):
        identifiers = json.loads(identifiers or '[]')
    if identifiers != archived.get('object_identifiers'):
        raise ValueError(f'archived source differs for object_identifiers: {item["input_id"]}')
    if (packet.get('article_number') != expected['article_number']
            or record.get('article') != expected['article_number']
            or record.get('arm') != expected['arm'] or record.get('draw') != expected['draw']):
        raise ValueError('source-role record does not match the selected article, arm and draw')
    if record.get('status') != 'complete':
        raise ValueError('source-role response was not completed')
    request = record['request']
    payload = json.loads(request['messages'][1]['content'])
    lines = [line for line in (item.get('text_page') or '').splitlines() if line.strip()]
    if not lines or payload.get('title') != item.get('title') or payload.get('publisher_as_stored') != item.get('publisher'):
        raise ValueError('source-role request does not identify the archived article')
    if payload.get('lines') != [{'id': n, 'text': line} for n, line in enumerate(lines, 1)]:
        raise ValueError('source-role request page does not match the archived page')
    response = record['response']
    choice = response['choices'][0]
    if choice.get('finish_reason') != 'stop' or choice['message'].get('refusal'):
        raise ValueError('source-role provider response is incomplete or refused')
    roles = json.loads(choice['message']['content'])
    schema = request['response_format']['json_schema']['schema']
    if set(roles) != set(ROLES) or model.check_schema(roles, schema):
        raise ValueError('source-role response does not match the recorded schema')
    for role in ROLES:
        if not isinstance(roles[role], list) or any(type(n) is not int or n < 1 or n > len(lines) for n in roles[role]):
            raise ValueError(f'invalid page line ID in {role}')
    ids = sorted(set().union(*(set(roles[role]) for role in INCLUDED)))
    if not ids:
        raise ValueError('source-role response selected no source lines')
    selected = '\n'.join(lines[n - 1] for n in ids)
    preparation = {
        'version': 1, 'status': 'experimental', 'input_id': item['input_id'],
        'article_number': packet.get('article_number'), 'source_role_arm': record['arm'],
        'source_role_draw': record['draw'], 'original_cleaned_text': item.get('text'),
        'original_text_chars': item.get('text_chars'), 'original_cleaning': item.get('cleaning'),
        'selected_text_sha256': hashlib.sha256(selected.encode('utf-8')).hexdigest(),
        'page_sha256': hashlib.sha256(item['text_page'].encode('utf-8')).hexdigest(),
        'packet_sha256': packet_hash, 'source_role_record_sha256': record_hash,
        'selected_line_ids': ids, 'roles': roles,
        'article_generated_overlap': sorted(set(roles['article_line_ids']) & set(roles['generated_summary_line_ids'])),
        'source_role_request': request, 'source_role_response': response,
    }
    return selected, preparation


def materialize(source_path, selection_path, output_path):
    """Publish a completed prepared source without changing the original database."""
    source = Path(source_path).resolve()
    output = Path(output_path).resolve()
    if source == output or output.exists():
        raise ValueError('output must be a new path separate from the original source')
    selection, _ = _read(selection_path)
    items = selection.get('items')
    if not isinstance(items, list) or not items:
        raise ValueError('selection requires items')
    ids = [entry['input_id'] for entry in items]
    if len(set(ids)) != len(ids):
        raise ValueError('selection contains duplicate source IDs')
    original = sqlite3.connect(source.as_uri() + '?mode=ro', uri=True)
    original.row_factory = sqlite3.Row
    prepared = []
    try:
        original.execute('begin')
        for entry in items:
            row = original.execute('select * from items where input_id=?', (entry['input_id'],)).fetchone()
            if row is None:
                raise ValueError(f'unknown source ID: {entry["input_id"]}')
            item = dict(row)
            packet, packet_hash = _read(entry['packet'])
            record, record_hash = _read(entry['source_role_record'])
            selected, metadata = select_source(item, packet, record, entry, packet_hash, record_hash)
            item['text'] = selected
            if 'text_chars' in item:
                item['text_chars'] = len(selected)
            if 'cleaning' in item:
                item['cleaning'] = json.dumps({'method': 'experimental_source_roles_v1',
                                               'selected_lines': len(metadata['selected_line_ids']),
                                               'selected_chars': len(selected)})
            item['source_preparation'] = json.dumps(metadata, ensure_ascii=False)
            prepared.append(item)
        fd, tmp_name = tempfile.mkstemp(prefix=f'.{output.name}.', suffix='.tmp', dir=output.parent)
        os.close(fd)
        try:
            destination = sqlite3.connect(tmp_name)
            try:
                destination.execute('attach database ? as original', (source.as_uri() + '?mode=ro',))
                destination.execute('create table items as select * from original.items where 0')
                destination.execute('alter table items add column source_preparation text')
                for item in prepared:
                    columns = list(item)
                    destination.execute(f'insert into items ({",".join(columns)}) values ({",".join("?" for _ in columns)})',
                                        [item[k] for k in columns])
                destination.commit()
            finally:
                destination.close()
            os.link(tmp_name, output)
        finally:
            Path(tmp_name).unlink(missing_ok=True)
    finally:
        original.close()
    return {'output': str(output), 'items': len(prepared), 'status': 'experimental'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--selection', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    print(json.dumps(materialize(args.source, args.selection, args.output)))


if __name__ == '__main__':
    main()

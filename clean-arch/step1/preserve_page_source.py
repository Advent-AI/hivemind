#!/usr/bin/env python3
"""Build a separate full-page test source while retaining the original cleaned input."""
import argparse
import hashlib
import json
import os
import sqlite3
import tempfile
from pathlib import Path


def sha256_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest() if text is not None else None


def snapshot_sha256(rows):
    """Hash ordered item values from the same read transaction used to build the copy."""
    digest = hashlib.sha256()
    for item_id in sorted(rows):
        digest.update(json.dumps(rows[item_id], sort_keys=True, ensure_ascii=False,
                                 separators=(',', ':')).encode('utf-8'))
        digest.update(b'\n')
    return digest.hexdigest()


def create_candidate(clean_path, raw_path, output_path):
    """Copy a cleaned source and expose upstream-fed articles' captured page text."""
    clean_path = Path(clean_path).resolve()
    raw_path = Path(raw_path).resolve()
    output_path = Path(output_path).resolve()
    if output_path in (clean_path, raw_path) or output_path.exists():
        raise ValueError('output must be a new path separate from both sources')
    clean = sqlite3.connect(clean_path.as_uri() + '?mode=ro', uri=True)
    raw = sqlite3.connect(raw_path.as_uri() + '?mode=ro', uri=True)
    clean.row_factory = sqlite3.Row
    raw.row_factory = sqlite3.Row
    temporary_path = None
    try:
        clean.execute('begin')
        raw.execute('begin')
        raw_rows = {row['input_id']: dict(row) for row in raw.execute('select * from items')}
        clean_rows = {row['input_id']: dict(row) for row in clean.execute('select * from items')}
        if not raw_rows or raw_rows.keys() != clean_rows.keys():
            raise ValueError('source item IDs must be nonempty and identical')
        if any(row.get('text_page') != raw_rows[key].get('text') for key, row in clean_rows.items()):
            raise ValueError('saved pages differ from the raw snapshot')
        identity_fields = ('document_format', 'source_uri', 'publisher', 'title', 'published_at',
                           'publication_day', 'retrieved_at', 'object_identifiers', 'copy_of', 'supersedes')
        if any(any(row.get(field) != raw_rows[key].get(field) for field in identity_fields)
               for key, row in clean_rows.items()):
            raise ValueError('source identity metadata differs between snapshots')
        fd, name = tempfile.mkstemp(prefix=f'.{output_path.name}.', suffix='.tmp', dir=output_path.parent)
        os.close(fd)
        temporary_path = Path(name)
        destination = sqlite3.connect(temporary_path)
        try:
            clean.backup(destination)
            destination.execute('alter table items add column page_source_audit text')
            destination.execute('create table page_source_build (manifest text not null)')
            build = {'raw_source': str(raw_path), 'clean_source': str(clean_path),
                     'raw_items_sha256': snapshot_sha256(raw_rows),
                     'clean_items_sha256': snapshot_sha256(clean_rows),
                     'snapshot_hash_format': 'ordered-items-json-v1',
                     'scope': 'isolated clean Step 1 source-preservation experiment',
                     'content_sha256_semantics': 'historical source content hash, not candidate text identity',
                     'coverage_semantics': 'historical cleaned coverage; not a candidate completeness judgment',
                     'text_identity_field': 'page_source_audit.candidate_text_sha256'}
            destination.execute('insert into page_source_build values (?)', (json.dumps(build),))
            counts = {'items': len(clean_rows), 'full_page_articles': 0, 'restored_feed': 0, 'missing_page': 0}
            for item_id, item in clean_rows.items():
                original = raw_rows[item_id]
                selected = original.get('document_format') == 'article' and original.get('feed') == 1
                candidate_text = item.get('text_page') if selected else item.get('text')
                candidate_feed = 1 if selected else item.get('feed')
                audit = {
                    'representation': 'captured_page' if selected else 'historical_clean',
                    'source_identity': 'unassessed',
                    'source_completeness': 'unassessed',
                    'original_cleaned_text': item.get('text'),
                    'original_cleaned_text_chars': item.get('text_chars'),
                    'upstream_feed': original.get('feed'), 'cleaned_feed': item.get('feed'),
                    'upstream_coverage': original.get('coverage'), 'cleaned_coverage': item.get('coverage'),
                    'candidate_text_sha256': sha256_text(candidate_text),
                    'captured_page_sha256': sha256_text(item.get('text_page')),
                }
                if selected:
                    counts['full_page_articles'] += 1
                    counts['restored_feed'] += item.get('feed') != 1
                    counts['missing_page'] += not bool(candidate_text)
                destination.execute('update items set text=?, text_chars=?, feed=?, page_source_audit=? where input_id=?',
                                    (candidate_text, len(candidate_text or ''), candidate_feed,
                                     json.dumps(audit, ensure_ascii=False), item_id))
            destination.commit()
        finally:
            destination.close()
        os.link(temporary_path, output_path)
        return counts
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raw.close()
        clean.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--clean', required=True)
    parser.add_argument('--raw', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    print(json.dumps(create_candidate(args.clean, args.raw, args.output), sort_keys=True))


if __name__ == '__main__':
    main()

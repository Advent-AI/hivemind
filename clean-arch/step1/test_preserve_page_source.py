"""Verify that the test-source candidate preserves both recorded source versions."""
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from preserve_page_source import create_candidate


class SourceCandidateTest(unittest.TestCase):
    def test_missing_page_and_copy_identity_are_preserved_without_claiming_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw, clean, candidate = (root / name for name in ('raw.db', 'clean.db', 'candidate.db'))
            for path in (raw, clean):
                with sqlite3.connect(path) as conn:
                    conn.execute('create table items (input_id text primary key, document_format text, feed integer, '
                                 'text text, text_page text, text_chars integer, coverage text, copy_of text)')
                    conn.execute('insert into items values (?,?,?,?,?,?,?,?)',
                                 ('missing', 'article', 1, None, None, 0, 'none', 'original'))
                    conn.execute('insert into items values (?,?,?,?,?,?,?,?)',
                                 ('nonarticle', 'video', 0, 'Video description.', 'Video description.', 18, 'none', None))
            result = create_candidate(clean, raw, candidate)
            self.assertEqual(result['missing_page'], 1)
            with sqlite3.connect(candidate) as conn:
                missing = conn.execute('select text,feed,copy_of,page_source_audit from items where input_id="missing"').fetchone()
                other = conn.execute('select text,feed from items where input_id="nonarticle"').fetchone()
            self.assertEqual(missing[:3], (None, 1, 'original'))
            self.assertEqual(json.loads(missing[3])['source_completeness'], 'unassessed')
            self.assertEqual(other, ('Video description.', 0))

    def test_mismatched_source_identity_refuses_without_publishing_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw, clean, candidate = (root / name for name in ('raw.db', 'clean.db', 'candidate.db'))
            for path, title in ((raw, 'Original article'), (clean, 'Different article')):
                with sqlite3.connect(path) as conn:
                    conn.execute('create table items (input_id text primary key, document_format text, feed integer, '
                                 'text text, text_page text, text_chars integer, coverage text, title text)')
                    conn.execute('insert into items values (?,?,?,?,?,?,?,?)',
                                 ('article', 'article', 1, 'Page.', 'Page.', 5, 'full', title))
            with self.assertRaisesRegex(ValueError, 'source identity metadata differs'):
                create_candidate(clean, raw, candidate)
            self.assertFalse(candidate.exists())

    def test_candidate_restores_page_without_changing_original_or_inventing_completeness(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw, clean, candidate = (root / name for name in ('raw.db', 'clean.db', 'candidate.db'))
            for path, raw_version in ((raw, True), (clean, False)):
                with sqlite3.connect(path) as conn:
                    conn.execute('create table items (input_id text primary key, document_format text, feed integer, '
                                 'text text, text_page text, text_chars integer, coverage text, title text)')
                    text = 'Article body. Additional context.' if raw_version else ''
                    conn.execute('insert into items values (?,?,?,?,?,?,?,?)',
                                 ('article', 'article', 1 if raw_version else 0, text,
                                  None if raw_version else 'Article body. Additional context.', len(text),
                                  'full' if raw_version else 'none', 'Example article'))
            result = create_candidate(clean, raw, candidate)
            self.assertEqual((result['items'], result['restored_feed']), (1, 1))
            with sqlite3.connect(candidate) as conn:
                text, page, length, feed, coverage, audit = conn.execute(
                    'select text,text_page,text_chars,feed,coverage,page_source_audit from items').fetchone()
                metadata = json.loads(audit)
                build = json.loads(conn.execute('select manifest from page_source_build').fetchone()[0])
            self.assertEqual((text, page, length, feed, coverage),
                             ('Article body. Additional context.', 'Article body. Additional context.', 33, 1, 'none'))
            self.assertEqual((metadata['original_cleaned_text'], metadata['upstream_feed'], metadata['cleaned_feed'],
                              metadata['source_identity'], metadata['source_completeness']), ('', 1, 0, 'unassessed', 'unassessed'))
            self.assertNotEqual(build['raw_items_sha256'], build['clean_items_sha256'])
            with sqlite3.connect(clean) as conn:
                self.assertEqual(conn.execute('select text,feed from items').fetchone(), ('', 0))
            with self.assertRaises(ValueError):
                create_candidate(clean, raw, candidate)


if __name__ == '__main__':
    unittest.main()

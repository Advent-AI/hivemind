"""Source preparation preserves original material and source-location integrity."""
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import materialize_source
import render_replay
import runner

ROOT = HERE.parents[1]


class PreparedSourceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.source = self.dir / 'source.sqlite'
        self.output = self.dir / 'prepared.sqlite'
        self.page = ('Quarterly outlook\nSubscribe to another newsletter.\n'
                     'The retailer raised its sales forecast.\nThe retailer expects demand to grow.\nBy Alice Reporter.')
        self.original_text = 'The retailer raised its sales forecast.'
        with sqlite3.connect(self.source) as conn:
            conn.execute('create table items (input_id text primary key, title text, publisher text, text text, text_page text, text_chars integer, cleaning text, source_uri text)')
            conn.execute('insert into items values (?, ?, ?, ?, ?, ?, ?, ?)',
                         ('source-1', 'Quarterly outlook', 'Example publisher', self.original_text, self.page, len(self.original_text), '{"method":"old_cleaner"}', 'https://example.com/article'))
        self.packet = self.dir / 'packet.json'
        self.packet.write_text(json.dumps({'article_number': 2, 'source_record': {'input_id': 'source-1',
            'title': 'Quarterly outlook', 'publisher': 'Example publisher', 'text_page': self.page,
            'source_uri': 'https://example.com/article'}}))
        names = materialize_source.ROLES
        schema = {'type': 'object', 'additionalProperties': False,
                  'properties': {name: {'type': 'array', 'items': {'type': 'integer'}} for name in names}, 'required': list(names)}
        roles = {'article_line_ids': [1, 3, 4], 'byline_or_source_line_ids': [5],
                 'caption_or_credit_line_ids': [], 'generated_summary_line_ids': [], 'uncertain_line_ids': []}
        payload = {'title': 'Quarterly outlook', 'publisher_as_stored': 'Example publisher',
                   'lines': [{'id': n, 'text': text} for n, text in enumerate(self.page.splitlines(), 1)]}
        self.record = self.dir / 'record.json'
        self.record.write_text(json.dumps({'status': 'complete', 'article': 2, 'arm': 'baseline', 'draw': 1,
            'request': {'messages': [{'role': 'system', 'content': 'Select source lines.'}, {'role': 'user', 'content': json.dumps(payload)}],
                        'response_format': {'json_schema': {'schema': schema}}},
            'response': {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(roles)}}]}}))
        self.selection = self.dir / 'selection.json'
        self.selection.write_text(json.dumps({'items': [{'input_id': 'source-1', 'article_number': 2, 'arm': 'baseline',
            'draw': 1, 'packet': str(self.packet), 'source_role_record': str(self.record)}]}))

    def build(self):
        return materialize_source.materialize(self.source, self.selection, self.output)

    def test_prepared_source_keeps_original_page_and_reports_selected_role(self):
        self.assertEqual(self.build()['items'], 1)
        with sqlite3.connect(self.output) as conn:
            conn.row_factory = sqlite3.Row
            item = dict(conn.execute('select * from items').fetchone())
        with sqlite3.connect(self.source) as conn:
            self.assertEqual(conn.execute('select text from items').fetchone()[0], self.original_text)
        self.assertEqual(item['text'], 'Quarterly outlook\nThe retailer raised its sales forecast.\nThe retailer expects demand to grow.\nBy Alice Reporter.')
        self.assertEqual(item['text_page'], self.page)
        self.assertEqual(item['text_chars'], len(item['text']))
        preparation = json.loads(item['source_preparation'])
        self.assertEqual(preparation['selected_line_ids'], [1, 3, 4, 5])
        self.assertEqual(preparation['original_cleaned_text'], self.original_text)
        self.assertEqual(json.loads(item['cleaning'])['method'], 'experimental_source_roles_v1')
        self.assertEqual(json.loads(preparation['original_cleaning'])['method'], 'old_cleaner')
        self.assertIn('By Alice Reporter.', render_replay.source_preparation_detail(item))
        self.assertEqual(render_replay.source_preparation_detail({}), '')

    def test_wrong_arm_and_changed_page_do_not_publish_a_source(self):
        record = json.loads(self.record.read_text())
        record['arm'] = 'candidate'
        self.record.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, 'article, arm and draw'):
            self.build()
        self.assertFalse(self.output.exists())
        record['arm'] = 'baseline'
        payload = json.loads(record['request']['messages'][1]['content'])
        payload['lines'][2]['text'] = 'The retailer lowered its sales forecast.'
        record['request']['messages'][1]['content'] = json.dumps(payload)
        self.record.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, 'does not match the archived page'):
            self.build()
        self.assertFalse(self.output.exists())
        payload['lines'][2]['text'] = 'The retailer raised its sales forecast.'
        record['request']['messages'][1]['content'] = json.dumps(payload)
        self.record.write_text(json.dumps(record))
        with sqlite3.connect(self.source) as conn:
            conn.execute('update items set source_uri=?', ('https://example.com/other-article',))
        with self.assertRaisesRegex(ValueError, 'source_uri'):
            self.build()
        self.assertFalse(self.output.exists())

    def test_quote_crossing_omitted_page_line_is_unverified(self):
        self.build()
        with sqlite3.connect(self.output) as conn:
            conn.row_factory = sqlite3.Row
            item = dict(conn.execute('select * from items').fetchone())
        _, schema = runner.draft(ROOT / 'clean-arch/PRD.md')
        def answer(quote):
            return {'new_theses': [], 'evidence': [{'local_id': 'e1', 'summary': quote, 'source_passages': [quote],
                'original_party': 'retailer', 'reporting_speaker': None, 'tier': 'party_statement',
                'statement_date': None, 'statement_date_text': None, 'evidence_period': None, 'figures': [],
                'links': [{'target_type': 'existing', 'target_id': 't1', 'relevance': 'The forecast informs sales.'}]}]}
        joined = 'Quarterly outlook\nThe retailer raised its sales forecast.'
        contiguous = 'The retailer raised its sales forecast.\nThe retailer expects demand to grow.'
        self.assertEqual(runner.validate(answer(joined), schema, item, [{'id': 't1'}])['evidence'][0]['verified_source_passages'], [None])
        self.assertEqual(runner.validate(answer(contiguous), schema, item, [{'id': 't1'}])['evidence'][0]['verified_source_passages'], [contiguous])
        old_item = {'text': joined}
        self.assertEqual(runner.validate(answer(joined), schema, old_item, [{'id': 't1'}])['evidence'][0]['verified_source_passages'], [joined])


if __name__ == '__main__':
    unittest.main()
